#!/usr/bin/env python3
"""
Antom Payment Success Rate Report Generator
Analyzes payment success rate data and generates PDF report with comprehensive executive summary
"""

import argparse
import json
import os
import sys
import platform
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import numpy as np


# Font configuration for English
ENGLISH_FONT_PATHS = {
    "Darwin": "/System/Library/Fonts/Helvetica.ttc",
    "Windows": "C:/Windows/Fonts/arial.ttf"
}


def register_font():
    """Register font (fallback to default if needed)"""
    system = platform.system()
    font_path = ENGLISH_FONT_PATHS.get(system, ENGLISH_FONT_PATHS["Darwin"])
    
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('Helvetica', font_path))
            return True
        except Exception:
            pass
    return False


register_font()

# Path utilities
CONFIG_PATH = os.path.join(os.path.expanduser("~/antom"), "conf.json")


def load_config():
    """Load configuration"""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_t1_date(target_date_str=None):
    """
    Calculate T+1 date for Antom data generation
    
    Since Antom data is T+1:
    - When user wants "today's" report (current date), we need yesterday's data
    - When user wants a specific historical date, use that date directly
    
    Args:
        target_date_str: Target date in YYYYMMDD format, or None for "today"
    
    Returns:
        str: Actual date to use in YYYYMMDD format
        bool: Whether T+1 logic was applied (True if used yesterday)
    """
    try:
        if target_date_str:
            # User specified a date
            target_date = datetime.strptime(target_date_str, "%Y%m%d")
            
            # Check if it's "today" or future date
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            if target_date >= today:
                # User wants "today" or future date, use yesterday (T+1 logic)
                actual_date = target_date - timedelta(days=1)
                return actual_date.strftime("%Y%m%d"), True
            else:
                # User wants historical date, use the date directly
                return target_date_str, False
        else:
            # User wants "today", use yesterday (T+1 logic)
            actual_date = datetime.now() - timedelta(days=1)
            return actual_date.strftime("%Y%m%d"), True
    except ValueError as e:
        print(f"Error: Incorrect date format: {e}")
        sys.exit(1)


def get_report_paths(date_str):
    """Get report directory and file paths"""
    base_dir = os.path.expanduser("~/antom/success rate")
    report_dir = os.path.join(base_dir, date_str)
    images_dir = os.path.join(report_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    pdf_path = os.path.join(report_dir, f"{date_str}-Payment-Success-Rate-Report.pdf")
    return report_dir, images_dir, pdf_path


def is_valid_data(data):
    """
    Check if the data is valid (not empty)
    
    Args:
        data: Raw data dictionary
    
    Returns:
        bool: True if data is valid, False otherwise
    """
    if not data or not isinstance(data, dict):
        return False
        
    try:
        # Check if has data for at least one payment method
        card_total = data.get('card', {}).get('total', {})
        apm_total = data.get('apm', {}).get('total', {})
        
        card_has_data = card_total and card_total.get('total_count', 0) > 0
        apm_has_data = apm_total and apm_total.get('total_count', 0) > 0
        
        # Valid if at least one has data
        return card_has_data or apm_has_data
    except Exception as e:
        print(f"Warning: Error checking data validity: {e}")
        return False


def has_valid_section(data, section_path):
    """
    Check if a specific section has valid data
    
    Args:
        data: Data dictionary  
        section_path: Dot-separated path (e.g., 'card.auth.3ds')
    
    Returns:
        bool: True if section exists and has data
    """
    try:
        current = data
        for key in section_path.split('.'):
            if not isinstance(current, dict):
                return False
            current = current.get(key, {})
        
        return isinstance(current, dict) and len(current) > 0
    except Exception:
        return False

def has_week_data(section_week_data):
    """
    Check if week data has any valid entries
    
    Args:
        section_week_data: Week data dictionary for a section
    
    Returns:
        bool: True if week data exists and is not all empty
    """
    if not section_week_data:
        return False
    
    try:
        # Check if it's a dict with actual data (not empty or all zeros)
        if isinstance(section_week_data, dict):
            # Check for any non-empty values
            for key, value in section_week_data.items():
                if isinstance(value, dict) and value.get("total_count", 0) > 0:
                    return True
                elif isinstance(value, (int, float)) and value > 0:
                    return True
            return False
        return False
    except Exception:
        return False


def find_last_valid_date(target_date_str, max_lookback=7):
    """
    Find the last valid date with data
    
    Args:
        target_date_str: Target date in YYYYMMDD format
        max_lookback: Maximum days to look back (default: 7)
    
    Returns:
        str: Last valid date with data
    """
    target_date = datetime.strptime(target_date_str, "%Y%m%d")
    
    for i in range(max_lookback):
        # Try dates from target_date backwards
        check_date = target_date - timedelta(days=i)
        check_date_str = check_date.strftime("%Y%m%d")
        
        data_file = os.path.expanduser(f"~/antom/success rate/{check_date_str}_raw_data.json")
        
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if is_valid_data(data):
                    if i > 0:
                        print(f"Note: {target_date_str}  data is invalid, using most recent valid date: {check_date_str}")
                    return check_date_str
            except Exception as e:
                print(f"Warning: Error reading {data_file} 时出错: {e}")
        
        if i == max_lookback - 1:
            print(f"Warning: No valid data found for {target_date_str}  and previous {max_lookback}  days of valid data")
    
    # If no valid data found, return original date
    return target_date_str


# Data loading
def load_raw_data(date_str):
    """Load raw data"""
    data_file = os.path.expanduser(f"~/antom/success rate/{date_str}_raw_data.json")
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def wrap_long_text(text, max_length=12):
    """
    Wrap long text by inserting newline characters every max_length characters
    
    Args:
        text: Text to wrap
        max_length: Maximum characters before wrapping (default: 12)
    
    Returns:
        Wrapped text with newline characters
    """
    if len(text) <= max_length:
        return text
    
    # Split text into chunks of max_length
    wrapped = '\n'.join([text[i:i+max_length] for i in range(0, len(text), max_length)])
    return wrapped


def load_previous_data(date_str, days_back=1):
    """Load previous day's data"""
    try:
        current_date = datetime.strptime(date_str, "%Y%m%d")
        previous_date = current_date - timedelta(days=days_back)
        return load_raw_data(previous_date.strftime("%Y%m%d"))
    except:
        return None


# Data extraction
def extract_card_data(raw_data):
    """Extract Card data and calculate success rates"""
    card = raw_data.get("card", {})
    
    # Calculate overall success rate
    total = card.get("total", {})
    if total:
        total["success_rate"] = (total["success_count"] / total["total_count"] * 100) if total.get("total_count", 0) > 0 else 0
    
    # Calculate success rates for auth types
    for key, data in card.get("auth", {}).items():
        data["success_rate"] = (data["success_count"] / data["total_count"] * 100) if data.get("total_count", 0) > 0 else 0
    
    # Calculate success rates for countries
    for key, data in card.get("country", {}).items():
        data["success_rate"] = (data["success_count"] / data["total_count"] * 100) if data.get("total_count", 0) > 0 else 0
    
    # Calculate success rates for banks
    for key, data in card.get("bank", {}).items():
        data["success_rate"] = (data["success_count"] / data["total_count"] * 100) if data.get("total_count", 0) > 0 else 0
    
    return card


def extract_apm_data(raw_data):
    """Extract APM data and calculate success rates"""
    apm = raw_data.get("apm", {})
    
    # Calculate overall success rate
    total = apm.get("total", {})
    if total:
        total["success_rate"] = (total["success_count"] / total["total_count"] * 100) if total.get("total_count", 0) > 0 else 0
    
    # Calculate system type success rates
    for key, data in apm.get("system_type", {}).items():
        data["success_rate"] = (data["success_count"] / data["total_count"] * 100) if data.get("total_count", 0) > 0 else 0
    
    # Calculate terminal success rates
    for key, data in apm.get("terminal", {}).items():
        # Convert string percentage to float if needed
        if isinstance(data.get("success_rate"), str):
            data["success_rate"] = float(data["success_rate"].rstrip('%'))
        else:
            data["success_rate"] = (data["success_count"] / data["total_count"] * 100) if data.get("total_count", 0) > 0 else 0
    
    return apm

def extract_card_data_with_fallback(target_data, prev_data, week_data):
    """Extract card data with fallback to 0 when today data is empty but historical data exists"""
    
    # First try to extract today's data
    card_today = extract_card_data(target_data)
    
    # Check if today has actual transaction data
    has_today_transactions = False
    total = card_today.get("total", {})
    if total and total.get("total_count", 0) > 0:
        has_today_transactions = True
    
    # If today has no data but historical data exists, return structure with 0s
    if not has_today_transactions and (prev_data or week_data):
        # Create minimal structure with zeros so week data can be shown
        card_today = {
            "total": {
                "total_count": 0,
                "success_count": 0,
                "success_rate": 0
            }
        }
        print("  Note: Today's card data is empty, using 0s for display (historical data exists)")
    
    return card_today

def extract_apm_data_with_fallback(target_data, prev_data, week_data):
    """Extract APM data with fallback to 0 when today data is empty but historical data exists"""
    
    # First try to extract today's data
    apm_today = extract_apm_data(target_data)
    
    # Check if today has actual transaction data
    has_today_transactions = False
    total = apm_today.get("total", {})
    if total and total.get("total_count", 0) > 0:
        has_today_transactions = True
    
    # If today has no data but historical data exists, return structure with 0s
    if not has_today_transactions and (prev_data or week_data):
        # Create minimal structure with zeros so week data can be shown
        apm_today = {
            "total": {
                "total_count": 0,
                "success_count": 0,
                "success_rate": 0
            }
        }
        print("  Note: Today's APM data is empty, using 0s for display (historical data exists)")
    
    return apm_today

# Chart generation
def draw_success_rate_chart(data_list, labels, title, save_path):
    """Draw success rate trend chart with fixed 0-100% y-axis"""
    fig, ax1 = plt.subplots(figsize=(6, 4))
    
    # Prepare data
    total_amounts = [d.get("total_count", 0) for d in data_list]
    success_amounts = [d.get("success_count", 0) for d in data_list]
    success_rates = [d.get("success_rate", 0) for d in data_list]
    
    # Bar chart - Transaction volume
    x = np.arange(len(labels))
    ax1.bar(x - 0.2, total_amounts, 0.4, label='Total', color='lightblue')
    ax1.bar(x + 0.2, success_amounts, 0.4, label='Success', color='lightgreen')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Volume')
    ax1.set_title(title)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend(loc='upper left')
    
    # Line chart - Success rate with fixed 0-100% y-axis
    ax2 = ax1.twinx()
    ax2.plot(x, success_rates, 'r-o', linewidth=2, markersize=6, label='Success Rate')
    ax2.set_ylabel('Success Rate (%)')
    ax2.set_ylim(0, 100)  # Force y-axis to show 0-100% range
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    return save_path


def draw_pie_chart(data, exclude_key, title, save_path):
    """Draw error code pie chart (with legend) - Reduced size by 1/3"""
    labels = []
    values = []
    
    for key, value in data.items():
        if key != exclude_key and value > 0:
            labels.append(key.replace("_", " ").title())
            values.append(value)
    
    if not values:
        return None
    
    # Reduce size by 1/3: original (8, 8) -> new (5.33, 5.33)
    plt.figure(figsize=(5.33, 5.33))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'][:len(labels)]
    
    patches, _, _ = plt.pie(values, labels=None, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.legend(patches, labels, loc="best", fontsize=9, bbox_to_anchor=(1, 0.5))
    plt.title(title, pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    return save_path


def draw_card_bank_trend_chart(card, card_prev, card_week, save_path):
    """Draw card payment success rate trend chart when bank data is unavailable"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    
    # Prepare data
    labels = ["Today", "Yesterday", "Week Avg"]
    
    # Overall success rates
    today_rate = card.get("total", {}).get("success_rate", 0)
    yesterday_rate = card_prev.get("total", {}).get("success_rate", today_rate) if card_prev else today_rate
    week_rate = card_week.get("total", {}).get("success_rate", today_rate) if card_week else today_rate
    
    rates = [today_rate, yesterday_rate, week_rate]
    
    # Top subplot: Bar chart for success rates
    colors = ['#4CAF50', '#2196F3', '#9C27B0']
    bars = ax1.bar(labels, rates, color=colors, alpha=0.8)
    ax1.set_ylabel('Success Rate (%)', fontsize=10)
    ax1.set_title('Card Payment Success Rate Trend', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 100)
    
    # Add value labels on bars
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Bottom subplot: Line chart for transaction volume
    today_volume = card.get("total", {}).get("total_count", 0)
    yesterday_volume = card_prev.get("total", {}).get("total_count", today_volume) if card_prev else today_volume
    week_volume = card_week.get("total", {}).get("total_count", today_volume) if card_week else today_volume
    
    volumes = [today_volume, yesterday_volume, week_volume]
    
    ax2.plot(labels, volumes, marker='o', linewidth=2, markersize=8, color='#FF9800')
    ax2.set_ylabel('Transaction Volume', fontsize=10)
    ax2.set_xlabel('Time Period', fontsize=10)
    ax2.set_title('Transaction Volume Trend', fontsize=12, fontweight='bold')
    
    # Add value labels on line points
    for i, (label, volume) in enumerate(zip(labels, volumes)):
        ax2.text(i, volume + max(volumes) * 0.02, f'{volume:,.0f}', 
                ha='center', va='bottom', fontsize=9)
    
    # Add grid
    ax1.grid(True, alpha=0.3)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    return save_path


# Analysis summary
def generate_analysis_summary(section_name, current_data, previous_data, week_data, filtered_banks=None, filtered_countries=None):
    """Generate analysis summary and recommendations
    
    Args:
        section_name: Section identifier
        current_data: Current period data
        previous_data: Previous period data
        week_data: Week average data
        filtered_banks: Optional list of bank names to filter analysis (for card_bank section)
        filtered_countries: Optional list of country codes to filter analysis (for card_country section)
    """
    summary = {}
    
    if section_name == "card_overall":
        current_rate = current_data.get("total", {}).get("success_rate", 0)
        previous_rate = previous_data.get("total", {}).get("success_rate", 0) if previous_data else current_rate
        week_rate = week_data.get("total", {}).get("success_rate", 0) if week_data else current_rate
        
        daily_change = current_rate - previous_rate
        
        if daily_change > 5:
            summary["analysis"] = f"Payment success rate significantly improved compared to yesterday ({daily_change:+.1f}%), excellent performance."
        elif daily_change < -5:
            summary["analysis"] = f"Payment success rate significantly decreased compared to yesterday ({daily_change:+.1f}%), attention required."
        else:
            summary["analysis"] = f"Payment success rate remained stable compared to yesterday ({daily_change:+.1f}%), stable operation."
        
        summary["recommendation"] = (
            "Focus on analyzing error code distribution and investigating system or partner issues." if current_rate < 70 else
            "Optimize 3DS authentication flow to reduce user drop-off." if current_rate < 85 else
            "Current success rate is good, recommend continuous monitoring and maintaining stability."
        )
    
    elif section_name == "card_auth":
        has_3ds_data = has_valid_section(current_data, 'auth.3ds')
        has_non3ds_data = has_valid_section(current_data, 'auth.non_3ds')
        
        rate_3ds = current_data.get("auth", {}).get("3ds", {}).get("success_rate", 0) if has_3ds_data else None
        rate_non3ds = current_data.get("auth", {}).get("non_3ds", {}).get("success_rate", 0) if has_non3ds_data else None
        
        if has_3ds_data and has_non3ds_data:
            summary["analysis"] = f"3DS Success Rate: {rate_3ds:.1f}%, Non-3DS Success Rate: {rate_non3ds:.1f}%."
        elif has_3ds_data:
            summary["analysis"] = f"3DS Success Rate: {rate_3ds:.1f}%."
        elif has_non3ds_data:
            summary["analysis"] = f"Non-3DS Success Rate: {rate_non3ds:.1f}%."
        else:
            summary["analysis"] = "No authentication data available."
        
        if has_3ds_data and has_non3ds_data and rate_3ds < rate_non3ds - 10:
            summary["recommendation"] = "Optimize 3DS process to reduce user operation steps."
        else:
            summary["recommendation"] = "Dynamically adjust Auth strategy based on different risk levels."
    
    elif section_name in ["card_error", "apm_error"]:
        errors = {k: v for k, v in current_data.get("error_code", {}).items() if k != "pay_success"}
        total_errors = sum(errors.values())
        
        summary["analysis"] = f"Total Errors: {total_errors} transactions. Main Errors: {', '.join([f'{k}({v})' for k, v in list(errors.items())[:3]])}."
        
        # Generate recommendation based on actual error types
        if total_errors > 50:
            if "timeout_close" in errors:
                summary["recommendation"] = "Prioritize handling timeout_close errors and check timeout settings."
            elif "failure" in errors and errors["failure"] > total_errors * 0.5:
                summary["recommendation"] = "Investigate root causes of failure errors and check integration with payment partners."
            elif "processing" in errors and errors["processing"] > total_errors * 0.3:
                summary["recommendation"] = "Check for stuck transactions and optimize payment processing flow."
            else:
                summary["recommendation"] = "Analyze error patterns and implement targeted fixes for the most common errors."
        elif section_name == "apm_error" and total_errors > 20:
            summary["recommendation"] = "Optimize error prompts to guide users to retry."
        else:
            summary["recommendation"] = "Monitor error code trends daily to detect anomalies in time."
    
    elif section_name == "card_country":
        countries = current_data.get("country", {})
        
        # If filtered_countries is provided, only analyze those countries
        if filtered_countries:
            # Filter countries to only include the ones in filtered_countries list
            countries_to_analyze = {k: v for k, v in countries.items() if k in filtered_countries}
        else:
            countries_to_analyze = countries
        
        low_rate = [f"{k}({v['success_rate']:.1f}%" for k, v in countries_to_analyze.items() if v["success_rate"] < 70]
        
        summary["analysis"] = f"Low Success Rate Countries: {', '.join(low_rate)}." if low_rate else "Analyzed country channels performing stably."
        summary["recommendation"] = "Check local payment habits and partner performance for low performing countries." if low_rate else "Continuously monitor success rate changes for key countries."
    
    elif section_name == "card_bank":
        banks = current_data.get("bank", {})
        
        # If filtered_banks is provided, only analyze those banks
        if filtered_banks:
            # Filter banks to only include the ones in filtered_banks list
            banks_to_analyze = {k: v for k, v in banks.items() if k.split('_')[0] in filtered_banks}
        elif len(banks) > 20:
            # If there are too many banks, only analyze Top 10 and Bottom 10 from the report
            # Get yesterday's data for comparison
            bank_changes = []
            for bank_name, bank_today in banks.items():
                bank_yesterday = current_data.get("bank", {}).get(bank_name, {}).get("success_rate", bank_today["success_rate"]) if previous_data else bank_today["success_rate"]
                daily_change = bank_today["success_rate"] - bank_yesterday
                volume = bank_today.get("total_count", 0)
                bank_changes.append({
                    'name': bank_name,
                    'today_rate': bank_today['success_rate'],
                    'daily_change': daily_change,
                    'volume': volume
                })
            
            # Sort to get Top 10 (by improvement) and Bottom 10 (by decline, min 5 txns)
            top_10 = sorted(bank_changes, key=lambda x: x['daily_change'], reverse=True)[:10]
            bank_changes_with_min_volume = [b for b in bank_changes if b['volume'] >= 5]
            bottom_10 = sorted(bank_changes_with_min_volume, key=lambda x: x['daily_change'])[:10]
            
            # Combine and deduplicate
            top_bottom_combined = {b['name']: banks[b['name']] for b in top_10 + bottom_10}
            banks_to_analyze = top_bottom_combined
            
            summary["analysis"] = f"Analyzed Top 10 and Bottom 10 banks by daily change from {len(banks)} total banks."
        else:
            banks_to_analyze = banks
            summary["analysis"] = f"Analyzed {len(banks)} bank channels."
        
        low_rate = [f"{wrap_long_text(k.split('_')[0], max_length=20)}({v['success_rate']:.1f}%" for k, v in banks_to_analyze.items() if v["success_rate"] < 70]
        
        if low_rate:
            summary["analysis"] += f" Low Performing: {', '.join(low_rate)}."
        
        summary["recommendation"] = "Investigate technical integration issues for low performing banks." if low_rate else "Deepen cooperation with top-tier banks and monitor volatile banks closely."
    
    elif section_name == "apm_overall":
        current_rate = current_data.get("total", {}).get("success_rate", 0)
        previous_rate = previous_data.get("total", {}).get("success_rate", 0) if previous_data else current_rate
        
        daily_change = current_rate - previous_rate
        summary["analysis"] = f"APM success rate {'improved' if daily_change > 0 else 'decreased'} compared to yesterday ({daily_change:+.1f}%)."
        summary["recommendation"] = (
            "Focus on analyzing timeout_close errors and optimizing payment flow." if current_rate < 70 else
            "Enrich payment methods to meet different user needs."
        )
    
    elif section_name == "apm_system":
        systems = current_data.get("system_type", {})
        web, wap, system = [systems.get(k, {}).get("success_rate", 0) for k in ["web", "wap", "system"]]
        
        summary["analysis"] = f"Web: {web:.1f}%, WAP: {wap:.1f}%, System: {system:.1f}%."
        min_rate = min(web, wap, system)
        summary["recommendation"] = "Investigate channels with success rate below 70%." if min_rate < 70 else "Recommend optimal payment methods based on device type."
    
    elif section_name == "apm_terminal":
        terminals = current_data.get("terminal", {})
        terminal_rates = []
        for terminal, info in terminals.items():
            rate_str = info.get("success_rate", "0%")
            rate = float(rate_str.rstrip('%')) if isinstance(rate_str, str) else rate_str
            terminal_rates.append((terminal, rate))
        
        if terminal_rates:
            terminal_summary = ", ".join([f"{t}: {r:.1f}%" for t, r in terminal_rates])
            summary["analysis"] = f"Terminal performance: {terminal_summary}."
            
            min_rate = min([r for _, r in terminal_rates])
            summary["recommendation"] = "Investigate terminals with success rate below 70%." if min_rate < 70 else "All terminals performing well."
        else:
            summary["analysis"] = "No terminal data available."
            summary["recommendation"] = "Check data source for terminal information."
    
    return summary


# Executive summary generation - COMPREHENSIVE VERSION
def generate_executive_summary(card_data, apm_data, card_prev, apm_prev):
    """Generate Executive Summary with comprehensive coverage of ALL sections"""
    critical_issues = []
    warnings = []
    observations = []
    recommendations = []
    
    # Extract previous data for comparison
    prev_card = card_prev or {}
    prev_apm = apm_prev or {}
    
    # ===== 1. OVERALL SUCCESS RATE ANALYSIS =====
    
    # Card overall
    if 'total' in card_data:
        card_rate = card_data['total'].get('success_rate', 0)
        prev_card_rate = prev_card.get('total', {}).get('success_rate', 0) if prev_card else card_rate
        rate_change = card_rate - prev_card_rate
        
        if prev_card_rate > 0:
            if rate_change < -10:
                critical_issues.append(f"Card payment success rate dropped {abs(rate_change):.1f}% - immediate investigation required")
            elif rate_change < -5:
                warnings.append(f"Card payment success rate decreased by {abs(rate_change):.1f}% compared to yesterday")
        
        if card_rate < 60:
            critical_issues.append(f"Card payment success rate critically low at {card_rate:.1f}%")
        elif card_rate < 70:
            warnings.append(f"Card payment success rate below threshold at {card_rate:.1f}%")
        elif card_rate >= 80:
            observations.append("Card payment performance is healthy")
    
    # APM overall
    if 'total' in apm_data:
        apm_rate = apm_data['total'].get('success_rate', 0)
        prev_apm_rate = prev_apm.get('total', {}).get('success_rate', 0) if prev_apm else apm_rate
        apm_change = apm_rate - prev_apm_rate
        
        if prev_apm_rate > 0:
            if apm_change < -10:
                critical_issues.append(f"APM payment success rate dropped {abs(apm_change):.1f}% - immediate investigation required")
            elif apm_change < -5:
                warnings.append(f"APM payment success rate decreased by {abs(apm_change):.1f}% compared to yesterday")
        
        if apm_rate < 60:
            critical_issues.append(f"APM payment success rate critically low at {apm_rate:.1f}%")
        elif apm_rate < 70:
            warnings.append(f"APM payment success rate below threshold at {apm_rate:.1f}%")
        elif apm_rate >= 80:
            observations.append("APM payment performance is healthy")
    
    # ===== 2. AUTHENTICATION ANALYSIS (Card) =====
    
    if 'auth' in card_data:
        # Check which auth types are available
        has_3ds = '3ds' in card_data['auth']
        has_non3ds = 'non_3ds' in card_data['auth']
        
        if has_3ds or has_non3ds:
            rate_3ds = card_data['auth']['3ds'].get('success_rate', 0) if has_3ds else None
            rate_non3ds = card_data['auth']['non_3ds'].get('success_rate', 0) if has_non3ds else None
            vol_3ds = card_data['auth']['3ds'].get('total_count', 0) if has_3ds else 0
            vol_non3ds = card_data['auth']['non_3ds'].get('total_count', 0) if has_non3ds else 0
            
            if has_3ds and has_non3ds:
                total_auth = vol_3ds + vol_non3ds
                if total_auth > 0:
                    pct_3ds = (vol_3ds / total_auth) * 100
                    
                    # 3DS success rate much lower than non-3DS
                    if rate_non3ds > 0 and rate_3ds < rate_non3ds - 15:
                        critical_issues.append(f"3DS authentication success rate ({rate_3ds:.1f}%) significantly lower than Non-3DS ({rate_non3ds:.1f}%)")
                        recommendations.append("Urgent: Review and optimize 3DS authentication flow")
                    
                    # High 3DS usage
                    if pct_3ds > 30:
                        warnings.append(f"High 3DS usage ({pct_3ds:.1f}%) may cause user friction")
                        recommendations.append("Consider reducing 3DS usage for low-risk transactions")
                    
                    # Low 3DS success rate
                    if rate_3ds < 50:
                        warnings.append(f"3DS success rate is poor at {rate_3ds:.1f}%")
                        recommendations.append("Investigate 3DS technical integration and user experience")
            elif has_3ds and rate_3ds < 50:
                warnings.append(f"3DS success rate is poor at {rate_3ds:.1f}%")
                recommendations.append("Investigate 3DS technical integration and user experience")
            elif has_non3ds and rate_non3ds < 50:
                warnings.append(f"Non-3DS success rate is poor at {rate_non3ds:.1f}%")
                recommendations.append("Investigate Non-3DS technical integration")
            
            # Add observation about available auth methods
            auth_methods = []
            if has_3ds:
                auth_methods.append(f"3DS ({rate_3ds:.1f}%)")
            if has_non3ds:
                auth_methods.append(f"Non-3DS ({rate_non3ds:.1f}%)")
            
            if auth_methods:
                # Include performance context for each authentication method
                auth_details = []
                if has_3ds:
                    if rate_3ds >= 80:
                        auth_details.append(f"3DS at {rate_3ds:.1f}%")
                        observations.append(f"3DS authentication performing well at {rate_3ds:.1f}%")
                    elif rate_3ds >= 70:
                        auth_details.append(f"3DS at {rate_3ds:.1f}% (acceptable)")
                    else:
                        warnings.append(f"⚠️  3DS authentication needs improvement at {rate_3ds:.1f}%")
                
                if has_non3ds:
                    if rate_non3ds >= 80:
                        auth_details.append(f"Non-3DS at {rate_non3ds:.1f}% (strong performance)")
                        observations.append(f"Non-3DS authentication strong at {rate_non3ds:.1f}%")
                    elif rate_non3ds >= 70:
                        auth_details.append(f"Non-3DS at {rate_non3ds:.1f}% (acceptable)")
                    else:
                        warnings.append(f"⚠️  Non-3DS authentication needs improvement at {rate_non3ds:.1f}%")
                
                # Only show combined authentication message if we have multiple methods
                if len(auth_methods) > 1:
                    if has_3ds and has_non3ds:
                        observations.append(f"Authentication methods overview: {', '.join(auth_details)}")
    
    # ===== 3. ERROR CODE ANALYSIS (Card & APM) =====
    
    # Card errors
    if 'error_code' in card_data:
        current_errors = {k: v for k, v in card_data['error_code'].items() 
                         if k != 'pay_success' and v > 0}
        prev_errors = {k: v for k, v in prev_card.get('error_code', {}).items() 
                      if k != 'pay_success' and v > 0}
        
        if current_errors:
            # Sort by count to get top errors
            sorted_errors = sorted(current_errors.items(), key=lambda x: x[1], reverse=True)
            prev_error_dict = prev_errors  # Already a dict
            
            for error_code, count in sorted_errors[:3]:
                prev_count = prev_error_dict.get(error_code, 0)
                if prev_count > 0:
                    change_pct = ((count - prev_count) / prev_count) * 100
                    
                    if change_pct > 100:
                        critical_issues.append(f"Card {error_code} errors surged {change_pct:.0f}% - potential system issue")
                        recommendations.append(f"Immediate investigation required for {error_code}")
                    elif change_pct > 50:
                        warnings.append(f"Card {error_code} errors increased {change_pct:.0f}%")
                        recommendations.append(f"Monitor {error_code} and investigate root cause")
                elif count > 20:  # New error with significant volume
                    warnings.append(f"Card {error_code} detected with {count} occurrences")
                    recommendations.append(f"Analyze {error_code} and implement fix")
    
    # APM errors
    if 'error_code' in apm_data:
        current_errors = {k: v for k, v in apm_data['error_code'].items() 
                         if k != 'pay_success' and v > 0}
        prev_errors = {k: v for k, v in prev_apm.get('error_code', {}).items() 
                      if k != 'pay_success' and v > 0}
        
        if current_errors:
            sorted_errors = sorted(current_errors.items(), key=lambda x: x[1], reverse=True)
            prev_error_dict = prev_errors  # Already a dict
            
            for error_code, count in sorted_errors[:3]:
                prev_count = prev_error_dict.get(error_code, 0)
                if prev_count > 0:
                    change_pct = ((count - prev_count) / prev_count) * 100
                    
                    if change_pct > 100:
                        critical_issues.append(f"APM {error_code} errors surged {change_pct:.0f}% - immediate action needed")
                        recommendations.append(f"Urgent: Investigate and resolve {error_code}")
                    elif change_pct > 50:
                        warnings.append(f"APM {error_code} errors increased {change_pct:.0f}%")
                        recommendations.append(f"Review {error_code} handling process")
                elif count > 30:
                    warnings.append(f"APM {error_code} detected with significant volume ({count})")
                    recommendations.append(f"Implement solution for {error_code}")
    
    # ===== 4. COUNTRY PERFORMANCE ANALYSIS (Card) =====
    
    if 'country' in card_data:
        low_performing_countries = []
        for country_code, country_data in card_data['country'].items():
            # Skip null/None country codes
            if country_code is None or (isinstance(country_code, str) and country_code.lower() == 'null'):
                continue
                
            rate = country_data.get('success_rate', 0)
            volume = country_data.get('total_count', 0)
            
            if rate < 50 and volume > 10:  # Low rate with significant volume
                low_performing_countries.append(f"{country_code} ({rate:.1f}%)")
        
        if low_performing_countries:
            warnings.append(f"Poor performance in markets: {', '.join(low_performing_countries[:3])}")
            recommendations.append("Review local payment partners and user experience in underperforming markets")
    
    # ===== 5. BANK PERFORMANCE ANALYSIS (Card) =====
    
    if 'bank' in card_data:
        low_performing_banks = []
        for bank_name, bank_data in card_data['bank'].items():
            rate = bank_data.get('success_rate', 0)
            volume = bank_data.get('total_count', 0)
            
            if rate < 60 and volume > 10:
                bank_name_clean = bank_name.split('_')[0] if '_' in bank_name else bank_name
                low_performing_banks.append(f"{bank_name_clean} ({rate:.1f}%)")
        
        if low_performing_banks:
            warnings.append(f"Underperforming banks: {', '.join(low_performing_banks[:3])}")
            recommendations.append("Investigate technical integration with low-performing banks")
    
    # ===== 6. SYSTEM TYPE ANALYSIS (APM) =====
    
    if 'system_type' in apm_data:
        low_performing_systems = []
        for system_type, system_data in apm_data['system_type'].items():
            rate = system_data.get('success_rate', 0)
            volume = system_data.get('total_count', 0)
            
            if rate < 60 and volume > 10:
                low_performing_systems.append(f"{system_type} ({rate:.1f}%)")
        
        if low_performing_systems:
            warnings.append(f"Low success rate in channels: {', '.join(low_performing_systems)}")
            recommendations.append("Investigate and optimize underperforming payment channels")
    
    # ===== 7. VOLUME ANALYSIS =====
    
    # Check for unusual volume patterns
    card_total_today = card_data.get('total', {}).get('total_count', 0)
    card_total_yesterday = prev_card.get('total', {}).get('total_count', 0) if prev_card else card_total_today
    
    if card_total_yesterday > 0:
        volume_change = ((card_total_today - card_total_yesterday) / card_total_yesterday) * 100
        if volume_change > 50:
            observations.append(f"Significant volume increase detected: +{volume_change:.1f}%")
        elif volume_change < -50:
            warnings.append(f"⚠️  Significant volume decline detected: {volume_change:.1f}%")
    
    # ===== COMPILE FINAL SUMMARY =====
    
    full_summary = []
    
    # Critical issues (always show first)
    if critical_issues:
        full_summary.append("🚨 CRITICAL ISSUES REQUIRING IMMEDIATE ACTION:")
        for issue in critical_issues[:4]:  # Max 4 critical issues
            full_summary.append(f"• {issue}")
        full_summary.append("")
    
    # Key risks and warnings
    if warnings:
        full_summary.append("⚠️  KEY RISKS AND CONCERNS:")
        for warning in warnings[:5]:  # Max 5 warnings
            full_summary.append(f"• {warning}")
        full_summary.append("")
    
    # Recommendations
    if recommendations:
        full_summary.append("💡 RECOMMENDED ACTIONS:")
        for rec in recommendations[:6]:  # Max 6 recommendations
            full_summary.append(f"• {rec}")
        full_summary.append("")
    
    # Positive observations
    if observations:
        full_summary.append("✅ POSITIVE PERFORMANCE:")
        for obs in observations[:3]:  # Max 3 observations
            full_summary.append(f"• {obs}")
        full_summary.append("")
    
    # If no issues
    if not critical_issues and not warnings:
        full_summary.append("✅ No critical issues detected. Overall performance is stable.")
        full_summary.append("")
    
    full_summary.append("📋 Detailed analysis and recommendations are provided in the following sections.")
    
    return "\n".join(full_summary)


# Table generation
def create_simple_table(data, headers):
    """Create a unified style table"""
    table_data = [headers] + data
    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica')
    ]))
    return t


# Main report generation
def generate_pdf_report(date_str, config):
    """Generate PDF report with robust data validation"""
    print(f"Generating report for date: {date_str}")
    
    # Load data
    current_data = load_raw_data(date_str)
    previous_data = load_previous_data(date_str, 1)
    week_data = [load_previous_data(date_str, i) for i in range(1, 8)]
    
    # Extract data
    card = extract_card_data_with_fallback(current_data, previous_data, week_data)
    card_prev = extract_card_data(previous_data) if previous_data else None
    card_week = extract_card_data(week_data[0]) if week_data and week_data[0] else None
    
    apm = extract_apm_data_with_fallback(current_data, previous_data, week_data)
    apm_prev = extract_apm_data(previous_data) if previous_data else None
    apm_week = extract_apm_data(week_data[0]) if week_data and week_data[0] else None
    
    # Create document
    report_dir, images_dir, pdf_path = get_report_paths(date_str)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                          rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=20)
    heading1_style = ParagraphStyle('Heading1', parent=styles['Heading2'], fontSize=16, spaceAfter=10)
    heading2_style = ParagraphStyle('Heading2', parent=styles['Heading2'])
    heading3_style = ParagraphStyle('Heading3', parent=styles['Heading3'])
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'])
    exec_sum_style = ParagraphStyle('ExecSum', parent=styles['Normal'], fontSize=10, leading=14, 
                                   spaceBefore=6, spaceAfter=6)
    
    story = []
    story.append(Paragraph(f"Payment Success Rate Report - {date_str}", title_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("📊 EXECUTIVE SUMMARY", heading1_style))
    
    # Generate executive summary
    executive_summary = generate_executive_summary(card, apm, card_prev, apm_prev)
    
    # Save executive summary to file for email
    summary_file_path = os.path.join(report_dir, f"{date_str}_executive_summary.txt")
    with open(summary_file_path, 'w', encoding='utf-8') as f:
        f.write(executive_summary)
    story.append(Paragraph(executive_summary.replace("\n", "<br/>"), exec_sum_style))
    story.append(Spacer(1, 20))
    
    # Check if Card data is valid
    card_has_data = card and card.get('total', {}).get('total_count', 0) > 0
    apm_has_data = apm and apm.get('total', {}).get('total_count', 0) > 0
    
    # Card Report Section
    if card_has_data:
        print("Adding Card Payment Analysis section...")
        story.append(Paragraph("Card Payment Analysis", heading2_style))
        story.append(Spacer(1, 10))
        card_section_counter = 0
        
        # Card Overall - Only show if week data exists or today has data
        if has_valid_section(card, 'total') or (has_week_data(card_week) and (not card_week or has_valid_section(card_week, 'total'))):
            card_section_counter += 1
            story.append(Paragraph(f"{card_section_counter}. Overall Payment Success Rate Analysis", heading3_style))
            card_chart_path = os.path.join(images_dir, "card_overall.png")
            draw_success_rate_chart(
                [card["total"], card_prev["total"] if card_prev else card["total"], card_week["total"] if card_week else card["total"]],
                ["Today", "Yesterday", "Week Avg"],
                "Card Overall Payment Success Rate Analysis",
                card_chart_path
            )
            story.append(Image(card_chart_path, width=6*inch, height=4*inch))
            story.append(Spacer(1, 10))
            
            card_summary = generate_analysis_summary("card_overall", card, card_prev, card_week)
            story.append(Paragraph(f"<b>Analysis Summary:</b> {card_summary['analysis']}", normal_style))
            story.append(Paragraph(f"<b>Recommendations:</b> {card_summary['recommendation']}", normal_style))
            story.append(Spacer(1, 20))
        
        # Card Auth - Only show if week data exists or today has data
        if has_valid_section(card, 'auth') or has_week_data(card_week.get('auth', {})):
            card_section_counter += 1
            story.append(Paragraph(f"{card_section_counter}. Authentication Type Analysis", heading3_style))
            
            # Safe access for 3DS data
            has_3ds = has_valid_section(card, 'auth.3ds')
            has_non3ds = has_valid_section(card, 'auth.non_3ds')
            
            if has_3ds or has_non3ds:
                auth_data = []
                
                if has_3ds:
                    auth_3ds_today = card['auth'].get('3ds', {}).get('success_rate', 0)
                    auth_3ds_yesterday = card_prev['auth'].get('3ds', {}).get('success_rate', 0) if card_prev and has_valid_section(card_prev, 'auth.3ds') else auth_3ds_today
                    auth_3ds_week = card_week['auth'].get('3ds', {}).get('success_rate', 0) if card_week and has_valid_section(card_week, 'auth.3ds') else auth_3ds_today
                    auth_data.append(["3DS", f"{auth_3ds_today:.1f}%", f"{auth_3ds_yesterday:.1f}%", f"{auth_3ds_week:.1f}%", 
                                     f"{auth_3ds_today - auth_3ds_yesterday:+.1f}%", f"{auth_3ds_today - auth_3ds_week:+.1f}%"])
                
                if has_non3ds:
                    auth_non3ds_today = card['auth'].get('non_3ds', {}).get('success_rate', 0)
                    auth_non3ds_yesterday = card_prev['auth'].get('non_3ds', {}).get('success_rate', 0) if card_prev and has_valid_section(card_prev, 'auth.non_3ds') else auth_non3ds_today
                    auth_non3ds_week = card_week['auth'].get('non_3ds', {}).get('success_rate', 0) if card_week and has_valid_section(card_week, 'auth.non_3ds') else auth_non3ds_today
                    auth_data.append(["Non-3DS", f"{auth_non3ds_today:.1f}%", f"{auth_non3ds_yesterday:.1f}%", f"{auth_non3ds_week:.1f}%",
                                     f"{auth_non3ds_today - auth_non3ds_yesterday:+.1f}%", f"{auth_non3ds_today - auth_non3ds_week:+.1f}%"])
                
                story.append(create_simple_table(auth_data, ["Auth Type", "Today", "Yesterday", "Week Avg", "Daily Change", "Weekly Change"]))
                story.append(Spacer(1, 10))
                
                auth_summary = generate_analysis_summary("card_auth", card, card_prev, card_week)
                story.append(Paragraph(f"<b>Analysis Summary:</b> {auth_summary['analysis']}", normal_style))
                story.append(Paragraph(f"<b>Recommendations:</b> {auth_summary['recommendation']}", normal_style))
                story.append(Spacer(1, 20))
        
        # Card Error Codes - Only show if week data exists or today has errors
        if has_valid_section(card, 'error_code') or has_week_data(card_week.get('error_code', {})):
            error_code_data = card.get("error_code", {})
            has_errors = any(k != "pay_success" and v > 0 for k, v in error_code_data.items())
            
            if has_errors:
                card_section_counter += 1
                story.append(Paragraph(f"{card_section_counter}. Error Code Analysis", heading3_style))
                card_error_pie = os.path.join(images_dir, "card_error_pie.png")
                draw_pie_chart(error_code_data, "pay_success", "Card Error Code Distribution", card_error_pie)
                story.append(Image(card_error_pie, width=4*inch, height=4*inch))
                story.append(Spacer(1, 10))
                
                # Prepare error code data
                error_data = []
                for error_code, today_count in error_code_data.items():
                    if error_code != "pay_success" and today_count > 0:
                        yesterday_count = card_prev.get("error_code", {}).get(error_code, 0) if card_prev else today_count
                        week_avg_count = card_week.get("error_code", {}).get(error_code, today_count) if card_week else today_count
                        
                        daily_change_pct = ((today_count - yesterday_count) / yesterday_count * 100) if yesterday_count > 0 else 0
                        weekly_change_pct = ((today_count - week_avg_count) / week_avg_count * 100) if week_avg_count > 0 else 0
                        
                        error_data.append([
                            error_code.replace("_", " ").title(),
                            f"{today_count}",
                            f"{yesterday_count}",
                            f"{week_avg_count}",
                            f"{daily_change_pct:+.1f}%" if yesterday_count > 0 else "N/A",
                            f"{weekly_change_pct:+.1f}%" if week_avg_count > 0 else "N/A"
                        ])
                
                if error_data:
                    story.append(create_simple_table(error_data, ["Error Code", "Today", "Yesterday", "Week Avg", "Daily Change %", "Weekly Change %"]))
                    story.append(Spacer(1, 10))
                
                error_summary = generate_analysis_summary("card_error", card, card_prev, card_week)
                story.append(Paragraph(f"<b>Analysis Summary:</b> {error_summary['analysis']}", normal_style))
                story.append(Paragraph(f"<b>Recommendations:</b> {error_summary['recommendation']}", normal_style))
                story.append(Spacer(1, 20))
        
        # Card Countries - Only show if week data exists or today has data
        if has_valid_section(card, 'country') or has_week_data(card_week.get('country', {})):
            country_data = card.get("country", {})
            has_multiple_countries = len(country_data) > 1
            
            if country_data and (has_multiple_countries or list(country_data.values())[0].get('total_count', 0) > 0):
                card_section_counter += 1
                story.append(Paragraph(f"{card_section_counter}. Card Issuing Country Analysis", heading3_style))
                
                # Calculate success rate changes for all countries
                countries_with_changes = []
                for country_code, country_today in country_data.items():
                    # Get yesterday's rate for comparison
                    country_yesterday = card_prev.get("country", {}).get(country_code, {}).get("success_rate", country_today["success_rate"]) if card_prev else country_today["success_rate"]
                    country_week = card_week.get("country", {}).get(country_code, {}).get("success_rate", country_today["success_rate"]) if card_week else country_today["success_rate"]
                    
                    daily_change = country_today["success_rate"] - country_yesterday
                    weekly_change = country_today["success_rate"] - country_week
                    volume = country_today.get("total_count", 0)
                    
                    countries_with_changes.append({
                        "code": country_code,
                        "today_rate": country_today["success_rate"],
                        "yesterday_rate": country_yesterday,
                        "week_rate": country_week,
                        "daily_change": daily_change,
                        "weekly_change": weekly_change,
                        "volume": volume
                    })
                
                # Determine display mode based on data size
                if len(countries_with_changes) <= 20:
                    # If 20 or fewer countries, show all sorted by daily change (descending)
                    countries_display = sorted(countries_with_changes, key=lambda x: x["daily_change"], reverse=True)
                    story.append(Paragraph("All Countries (sorted by success rate change):", heading3_style))
                    
                    # Generate table for all countries
                    country_table_data = []
                    for country in countries_display:
                        country_week = card_week.get("country", {}).get(country["code"], {}).get("success_rate", country["today_rate"]) if card_week else country["today_rate"]
                        weekly_change = country["today_rate"] - country_week
                        
                        country_table_data.append([
                            country["code"],
                            f"{country['today_rate']:.1f}%",
                            f"{country['volume']:.0f}",
                            f"{country['daily_change']:+.1f}%",
                            f"{weekly_change:+.1f}%"
                        ])
                    
                    story.append(create_simple_table(
                        country_table_data,
                        ["Country", "Today", "Volume", "Daily Change", "Weekly Change"]
                    ))
                    story.append(Spacer(1, 10))
                else:
                    # If more than 20 countries, show Top 10 and Bottom 10
                    countries_by_change_desc = sorted(countries_with_changes, key=lambda x: x["daily_change"], reverse=True)
                    top_10_by_change = countries_by_change_desc[:min(10, len(countries_by_change_desc))]
                    
                    # Sort by daily change (ascending) for Bottom 10, but only include countries with >= 5 transactions
                    countries_with_min_volume = [c for c in countries_with_changes if c["volume"] >= 5]
                    countries_by_change_asc = sorted(countries_with_min_volume, key=lambda x: x["daily_change"])
                    bottom_10_by_change = countries_by_change_asc[:min(10, len(countries_by_change_asc))]
                    
                    # Display Top 10 by improvement
                    if top_10_by_change:
                        story.append(Paragraph("Top 10 Countries by Success Rate Improvement:", heading3_style))
                        country_table_data = []
                        for country in top_10_by_change:
                            country_week = card_week.get("country", {}).get(country["code"], {}).get("success_rate", country["today_rate"]) if card_week else country["today_rate"]
                            weekly_change = country["today_rate"] - country_week
                            
                            country_table_data.append([
                                country["code"],
                                f"{country['today_rate']:.1f}%",
                                f"{country['volume']:.0f}",
                                f"{country['daily_change']:+.1f}%",
                                f"{weekly_change:+.1f}%"
                            ])
                        
                        story.append(create_simple_table(
                            country_table_data,
                            ["Country", "Today", "Volume", "Daily Change", "Weekly Change"]
                        ))
                        story.append(Spacer(1, 15))
                    
                    # Combine for bottom display section
                    countries_display = bottom_10_by_change
                    story.append(Paragraph("Bottom 10 Countries by Success Rate Decline (min 5 transactions):", heading3_style))
                    
                    # Display Bottom 10 table
                    country_table_data = []
                    for country in countries_display:
                        country_week = card_week.get("country", {}).get(country["code"], {}).get("success_rate", country["today_rate"]) if card_week else country["today_rate"]
                        weekly_change = country["today_rate"] - country_week
                        
                        country_table_data.append([
                            country["code"],
                            f"{country['today_rate']:.1f}%",
                            f"{country['volume']:.0f}",
                            f"{country['daily_change']:+.1f}%",
                            f"{weekly_change:+.1f}%"
                        ])
                    
                    story.append(create_simple_table(
                        country_table_data,
                        ["Country", "Today", "Volume", "Daily Change", "Weekly Change"]
                    ))
                    story.append(Spacer(1, 10))
                
                # Analysis summary (always show after tables)
                country_summary = generate_analysis_summary("card_country", card, card_prev, card_week)
                story.append(Paragraph(f"<b>Analysis Summary:</b> {country_summary['analysis']}", normal_style))
                story.append(Paragraph(f"<b>Recommendations:</b> {country_summary['recommendation']}", normal_style))
                story.append(Spacer(1, 20))
        
        # Card Banks - Only show if week data exists or today has data
        if has_valid_section(card, 'bank') or has_week_data(card_week.get('bank', {})):
            bank_data = card.get("bank", {})
            has_multiple_banks = len(bank_data) > 1
            
            if bank_data and (has_multiple_banks or list(bank_data.values())[0].get('total_count', 0) > 0):
                card_section_counter += 1
                story.append(Paragraph(f"{card_section_counter}. Card Issuing Bank Analysis", heading3_style))
                
                # Calculate success rate changes for all banks
                banks_with_changes = []
                for bank_name, bank_info in bank_data.items():
                    # Get yesterday's rate for comparison
                    bank_yesterday = card_prev.get("bank", {}).get(bank_name, {}).get("success_rate", bank_info["success_rate"]) if card_prev else bank_info["success_rate"]
                    daily_change = bank_info["success_rate"] - bank_yesterday
                    
                    banks_with_changes.append({
                        "name": bank_name,
                        "today_rate": bank_info["success_rate"],
                        "yesterday_rate": bank_yesterday,
                        "daily_change": daily_change,
                        "volume": bank_info.get("total_count", 0)
                    })
                
                # Determine display mode based on data size
                if len(banks_with_changes) <= 20:
                    # If 20 or fewer banks, show all sorted by daily change (descending)
                    banks_display = sorted(banks_with_changes, key=lambda x: x["daily_change"], reverse=True)
                    story.append(Paragraph("All Banks (sorted by success rate change):", heading3_style))
                    
                    bank_table_data = []
                    for bank in banks_display:
                        bank_week = card_week.get("bank", {}).get(bank["name"], {}).get("success_rate", bank["today_rate"]) if card_week else bank["today_rate"]
                        weekly_change = bank["today_rate"] - bank_week
                        
                        bank_table_data.append([
                            bank["name"][:30] + "..." if len(bank["name"]) > 30 else bank["name"],
                            f"{bank['today_rate']:.1f}%",
                            f"{bank['volume']:.0f}",
                            f"{bank['daily_change']:+.1f}%",
                            f"{weekly_change:+.1f}%"
                        ])
                    
                    story.append(create_simple_table(
                        bank_table_data,
                        ["Bank", "Today", "Volume", "Daily Change", "Weekly Change"]
                    ))
                else:
                    # If more than 20 banks, show Top 10 and Bottom 10
                    banks_by_change_desc = sorted(banks_with_changes, key=lambda x: x["daily_change"], reverse=True)
                    top_10_by_change = banks_by_change_desc[:min(10, len(banks_by_change_desc))]
                    
                    # Sort by daily change (ascending) for Bottom 10, but only include banks with >= 5 transactions
                    banks_with_min_volume = [b for b in banks_with_changes if b["volume"] >= 5]
                    banks_by_change_asc = sorted(banks_with_min_volume, key=lambda x: x["daily_change"])
                    bottom_10_by_change = banks_by_change_asc[:min(10, len(banks_by_change_asc))]
                    
                    # Display Top 10 by improvement
                    if top_10_by_change:
                        story.append(Paragraph("Top 10 Banks by Success Rate Improvement:", heading3_style))
                        bank_table_data = []
                        for bank in top_10_by_change:
                            bank_week = card_week.get("bank", {}).get(bank["name"], {}).get("success_rate", bank["today_rate"]) if card_week else bank["today_rate"]
                            weekly_change = bank["today_rate"] - bank_week
                            
                            bank_table_data.append([
                                bank["name"][:30] + "..." if len(bank["name"]) > 30 else bank["name"],
                                f"{bank['today_rate']:.1f}%",
                                f"{bank['volume']:.0f}",
                                f"{bank['daily_change']:+.1f}%",
                                f"{weekly_change:+.1f}%"
                            ])
                        
                        story.append(create_simple_table(
                            bank_table_data,
                            ["Bank", "Today", "Volume", "Daily Change", "Weekly Change"]
                        ))
                        story.append(Spacer(1, 15))
                    
                    # Display Bottom 10 by decline
                    if bottom_10_by_change:
                        story.append(Paragraph("Bottom 10 Banks by Success Rate Decline (min 5 transactions):", heading3_style))
                        bank_table_data = []
                        for bank in bottom_10_by_change:
                            bank_week = card_week.get("bank", {}).get(bank["name"], {}).get("success_rate", bank["today_rate"]) if card_week else bank["today_rate"]
                            weekly_change = bank["today_rate"] - bank_week
                            
                            bank_table_data.append([
                                bank["name"][:30] + "..." if len(bank["name"]) > 30 else bank["name"],
                                f"{bank['today_rate']:.1f}%",
                                f"{bank['volume']:.0f}",
                                f"{bank['daily_change']:+.1f}%",
                                f"{weekly_change:+.1f}%"
                            ])
                        
                        story.append(create_simple_table(
                            bank_table_data,
                            ["Bank", "Today", "Volume", "Daily Change", "Weekly Change"]
                        ))
                        story.append(Spacer(1, 10))
                
                bank_summary = generate_analysis_summary("card_bank", card, card_prev, card_week)
                story.append(Paragraph(f"<b>Analysis Summary:</b> {bank_summary['analysis']}", normal_style))
                story.append(Paragraph(f"<b>Recommendations:</b> {bank_summary['recommendation']}", normal_style))
                story.append(Spacer(1, 20))
    
    # APM Report Section
    if apm_has_data:
        print("Adding APM Payment Analysis section...")
        story.append(Paragraph("APM Payment Analysis", heading2_style))
        story.append(Spacer(1, 10))
        apm_section_counter = 0
        
        # APM Overall - Only show if week data exists or today has data
        if has_valid_section(apm, 'total') or (has_week_data(apm_week) and (not apm_week or has_valid_section(apm_week, 'total'))):
            apm_section_counter += 1
            story.append(Paragraph(f"{apm_section_counter}. Overall Payment Success Rate Analysis", heading3_style))
            apm_chart_path = os.path.join(images_dir, "apm_overall.png")
            draw_success_rate_chart(
                [apm["total"], apm_prev["total"] if apm_prev else apm["total"], apm_week["total"] if apm_week else apm["total"]],
                ["Today", "Yesterday", "Week Avg"],
                "APM Overall Payment Success Rate Analysis",
                apm_chart_path
            )
            story.append(Image(apm_chart_path, width=6*inch, height=4*inch))
            story.append(Spacer(1, 10))
            
            apm_summary = generate_analysis_summary("apm_overall", apm, apm_prev, apm_week)
            story.append(Paragraph(f"<b>Analysis Summary:</b> {apm_summary['analysis']}", normal_style))
            story.append(Paragraph(f"<b>Recommendations:</b> {apm_summary['recommendation']}", normal_style))
            story.append(Spacer(1, 20))
        
        # APM Error Codes - Only show if week data exists or today has errors
        if has_valid_section(apm, 'error_code') or has_week_data(apm_week.get('error_code', {})):
            error_code_data = apm.get("error_code", {})
            has_errors = any(k != "pay_success" and v > 0 for k, v in error_code_data.items())
            
            if has_errors:
                apm_section_counter += 1
                story.append(Paragraph(f"{apm_section_counter}. Error Code Analysis", heading3_style))
                apm_error_pie = os.path.join(images_dir, "apm_error_pie.png")
                draw_pie_chart(error_code_data, "pay_success", "APM Error Code Distribution", apm_error_pie)
                story.append(Image(apm_error_pie, width=4*inch, height=4*inch))
                story.append(Spacer(1, 10))
                
                # APM Error Code Data (Today, Yesterday, Week Avg)
                apm_error_data = []
                for error_code, today_count in error_code_data.items():
                    if error_code != "pay_success" and today_count > 0:
                        yesterday_count = apm_prev.get("error_code", {}).get(error_code, 0) if apm_prev else today_count
                        week_avg_count = apm_week.get("error_code", {}).get(error_code, today_count) if apm_week else today_count
                        
                        daily_change_pct = ((today_count - yesterday_count) / yesterday_count * 100) if yesterday_count > 0 else 0
                        weekly_change_pct = ((today_count - week_avg_count) / week_avg_count * 100) if week_avg_count > 0 else 0
                        
                        apm_error_data.append([
                            error_code.replace("_", " ").title(),
                            f"{today_count}",
                            f"{yesterday_count}",
                            f"{week_avg_count}",
                            f"{daily_change_pct:+.1f}%" if yesterday_count > 0 else "N/A",
                            f"{weekly_change_pct:+.1f}%" if week_avg_count > 0 else "N/A"
                        ])
                
                if apm_error_data:
                    story.append(create_simple_table(apm_error_data, ["Error Code", "Today", "Yesterday", "Week Avg", "Daily Change %", "Weekly Change %"]))
                    story.append(Spacer(1, 10))
                
                apm_error_summary = generate_analysis_summary("apm_error", apm, apm_prev, apm_week)
                story.append(Paragraph(f"<b>Analysis Summary:</b> {apm_error_summary['analysis']}", normal_style))
                story.append(Paragraph(f"<b>Recommendations:</b> {apm_error_summary['recommendation']}", normal_style))
                story.append(Spacer(1, 20))
        
        # APM Terminal Analysis
        if has_valid_section(apm, 'terminal'):
            terminal_data = apm.get("terminal", {})
            if terminal_data:
                apm_section_counter += 1
                story.append(Paragraph(f"{apm_section_counter}. Terminal Type Analysis", heading3_style))
                
                # Calculate terminal changes and sort by volume
                terminal_change_data = []
                for terminal_type, terminal_today in terminal_data.items():
                    terminal_yesterday = apm_prev.get("terminal", {}).get(terminal_type, {}).get("success_rate", 0) if apm_prev else 0
                    terminal_week = apm_week.get("terminal", {}).get(terminal_type, {}).get("success_rate", terminal_today["success_rate"]) if apm_week else terminal_today["success_rate"]
                    
                    daily_change = terminal_today["success_rate"] - terminal_yesterday
                    weekly_change = terminal_today["success_rate"] - terminal_week
                    volume = terminal_today.get("total_count", 0)
                    
                    terminal_change_data.append({
                        'type': terminal_type,
                        'today_rate': terminal_today['success_rate'],
                        'yesterday_rate': terminal_yesterday,
                        'week_rate': terminal_week,
                        'daily_change': daily_change,
                        'weekly_change': weekly_change,
                        'volume': volume
                    })
                
                # Sort by volume (descending) and show all terminals
                terminal_change_data.sort(key=lambda x: x['volume'], reverse=True)
                
                story.append(create_simple_table(
                    [[t['type'], f"{t['today_rate']:.1f}%", f"{t['yesterday_rate']:.1f}%", f"{t['week_rate']:.1f}%",
                      f"{t['daily_change']:+.1f}%", f"{t['weekly_change']:+.1f}%", f"{t['volume']:.0f}"] 
                     for t in terminal_change_data],
                    ["Terminal", "Today", "Yesterday", "Week Avg", "Daily Change", "Weekly Change", "Volume"]
                ))
                story.append(Spacer(1, 10))
                
                terminal_summary = generate_analysis_summary("apm_terminal", apm, apm_prev, apm_week)
                story.append(Paragraph(f"<b>Analysis Summary:</b> {terminal_summary['analysis']}", normal_style))
                story.append(Paragraph(f"<b>Recommendations:</b> {terminal_summary['recommendation']}", normal_style))
                story.append(Spacer(1, 20))
    
    # Build PDF
    if not card_has_data and not apm_has_data:
        print("Warning: No valid data found for Card or APM sections. Generating minimal report.")
        story.append(Paragraph("No payment data available for analysis.", normal_style))
    
    doc.build(story)
    print(f"PDF report generated: {pdf_path}")
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description='Generate payment success rate PDF report')
    parser.add_argument('--date', required=True, help='Date: YYYYMMDD (T+1 logic: if requesting today, will use yesterday)')
    args = parser.parse_args()
    
    try:
        # Apply T+1 logic: check if user wants today's data
        actual_date, is_today = calculate_t1_date(args.date)
        
        if is_today:
            print(f"User requested report for: {args.date} (today)")
            print(f"Due to T+1 data generation, analyzing data from: {actual_date}")
        else:
            print(f"User requested report for: {args.date}")
            print(f"Analyzing historical data from: {actual_date}")
        
        # Find the last valid date with data (skip empty dates)
        valid_date = find_last_valid_date(actual_date)
        
        if valid_date != actual_date:
            print(f"Note: Target date {actual_date} has no valid data, using most recent valid date: {valid_date}")
        
        # Check if we found any valid data
        data_file = os.path.expanduser(f"~/antom/success rate/{valid_date}_raw_data.json")
        if not os.path.exists(data_file):
            print(f"Error: No data file found for {valid_date}")
            print("Please ensure you have run query_antom_psr_data.py first to fetch the data.")
            sys.exit(1)
        
        # Verify data is not empty before proceeding
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
            
            card_total = test_data.get('card', {}).get('total', {})
            apm_total = test_data.get('apm', {}).get('total', {})
            
            card_has_data = card_total and card_total.get('total_count', 0) > 0
            apm_has_data = apm_total and apm_total.get('total_count', 0) > 0
            
            if not card_has_data and not apm_has_data:
                print(f"Warning: Data file exists for {valid_date} but contains no transaction data.")
                print("The report will be generated but will have minimal content.")
            else:
                if card_has_data:
                    print(f"✓ Card data found: {card_total.get('total_count', 0)} transactions")
                if apm_has_data:
                    print(f"✓ APM data found: {apm_total.get('total_count', 0)} transactions")
        
        except Exception as e:
            print(f"Warning: Could not verify data content: {e}")
        
        config = load_config()
        generate_pdf_report(valid_date, config)
        print(f"\n✓ Report generation completed successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease check:")
        print("1. Configuration file exists at ~/antom/conf.json")
        print("2. Data files have been generated by running query_antom_psr_data.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
