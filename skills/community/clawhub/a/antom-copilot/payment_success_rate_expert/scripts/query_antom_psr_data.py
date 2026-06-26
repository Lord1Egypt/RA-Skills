#!/usr/bin/env python3
"""
Antom Payment Success Rate Data Query Tool
Fetches transaction data from Antom server
"""

import argparse
import json
import os
import sys
import requests
from pathlib import Path
from datetime import datetime, timedelta
import platform

# API configuration
API_ENDPOINT = "https://antomaplusai.antom.com/antomcopilotai/mcp/api/v1/antomcopilot/RECALL_data"


def get_config_path():
    """Get configuration file path, compatible with macOS, Linux, and Windows"""
    if platform.system() == "Windows":
        base_dir = os.path.join(os.environ["USERPROFILE"], "antom")
    else:
        base_dir = os.path.expanduser("~/antom")
    
    config_path = os.path.join(base_dir, "conf.json")
    return config_path


def load_config():
    """Load configuration file"""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        print("Please configure conf.json file first")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error: Failed to read configuration file: {e}")
        sys.exit(1)


def validate_config(config):
    """Validate configuration completeness"""
    required_fields = ["merchant_token", "email_conf"]
    
    for field in required_fields:
        if field not in config:
            print(f"Error: Configuration file missing required field: {field}")
            sys.exit(1)
    
    # Validate email_conf
    email_conf = config["email_conf"]
    email_fields = ["smtp_server", "smtp_port", "username", "password"]
    
    for field in email_fields:
        if field not in email_conf:
            print(f"Error: email_conf missing required field: {field}")
            sys.exit(1)
    
    return True


def create_directories():
    """Create necessary directories"""
    if platform.system() == "Windows":
        base_dir = os.path.join(os.environ["USERPROFILE"], "antom")
    else:
        base_dir = os.path.expanduser("~/antom")
    
    success_rate_dir = os.path.join(base_dir, "success rate")
    
    os.makedirs(success_rate_dir, exist_ok=True)
    
    return success_rate_dir


def query_antom_api(date_range, merchant_token):
    """
    Call Antom API to get payment success rate data
    
    Args:
        date_range: Date range, format: "20260310~20260312"
        merchant_token: Merchant token
    
    Returns:
        dict: JSON data returned by API
    """
    # Parse date range
    try:
        start_date, end_date = date_range.split("~")
        datetime.strptime(start_date, "%Y%m%d")
        datetime.strptime(end_date, "%Y%m%d")
    except ValueError:
        print(f"Error: Incorrect date format, should be YYYYMMDD~YYYYMMDD format")
        sys.exit(1)
    
    # Build request payload
    text_content = f"{start_date}~{end_date}"
    
    payload = {
        "textContent": text_content,
        "merchantToken": merchant_token,
        "scene": "PSR"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Fetching data from Antom, date range: {date_range}...")
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Check for errors
        if "error" in result:
            print(f"Error: API returned error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
        
        print(f"Successfully fetched data, date range: {date_range}")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON response: {e}")
        sys.exit(1)


def calculate_date_range(end_date_str):
    """
    Calculate 7 dates for the week before the specified date
    
    Args:
        end_date_str: End date, format: YYYYMMDD
    
    Returns:
        list: List of 7 date strings, format: [YYYYMMDD, YYYYMMDD, ...]
    """
    try:
        # Parse end date
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
        
        # Generate list of 7 days (previous 6 days + specified date)
        dates = []
        for i in range(6, -1, -1):  # 6, 5, 4, 3, 2, 1, 0
            date = end_date - timedelta(days=i)
            dates.append(date.strftime("%Y%m%d"))
        
        return dates
    except ValueError as e:
        print(f"Error: Incorrect date format: {e}")
        sys.exit(1)


def calculate_t1_date(target_date_str):
    """
    Calculate T+1 date for Antom data generation
    
    Since Antom data is T+1, when user wants today's report, 
    we actually need yesterday's data.
    
    Args:
        target_date_str: Target date in YYYYMMDD format
    
    Returns:
        tuple: (actual_date_str, is_today) where actual_date_str is the date to use in YYYYMMDD format,
               and is_today is a boolean indicating whether T+1 logic was applied
    """
    try:
        # Parse target date
        target_date = datetime.strptime(target_date_str, "%Y%m%d")
        
        # Get today's date
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check if target date is today
        is_today = target_date.date() == today.date()
        
        # If target is today, use yesterday (T+1 logic), otherwise use target date
        if is_today:
            actual_date = target_date - timedelta(days=1)
        else:
            actual_date = target_date
            
        return actual_date.strftime("%Y%m%d"), is_today
    except ValueError as e:
        print(f"Error: Incorrect date format: {e}")
        sys.exit(1)


def is_valid_data(data):
    """
    Check if the data is valid (not empty)
    
    Data is considered valid if either card or apm has transactions.
    This aligns with the report generation logic that can handle
    partial data (card-only or apm-only scenarios).
    
    Args:
        data: Raw data dictionary
    
    Returns:
        bool: True if data is valid, False otherwise
    """
    try:
        # Check if card.total has data
        card_total = data.get('card', {}).get('total', {})
        card_valid = bool(card_total and card_total.get('total_count', 0) > 0)
        
        # Check if apm.total has data
        apm_total = data.get('apm', {}).get('total', {})
        apm_valid = bool(apm_total and apm_total.get('total_count', 0) > 0)
        
        # Data is valid if either card or apm has data (OR logic)
        return card_valid or apm_valid
        
    except Exception as e:
        print(f"Warning: Error checking data validity: {e}")
        return False


def save_raw_data(data, start_date):
    """
    Save raw data to file
    
    Extract JSON field from data->messageList[0]->content->text in the large JSON returned by API as raw_data
    
    Args:
        data: JSON data returned by API
        start_date: Start date
    
    Returns:
        str: File path if saved successfully, None if data is invalid
    """
    success_rate_dir = create_directories()
    filename = f"{start_date}_raw_data.json"
    filepath = os.path.join(success_rate_dir, filename)
    
    try:
        # Extract real data from nested JSON structure
        # Path: data -> data -> messageList[0] -> content[0] -> text
        message_list = data.get("data", {}).get("messageList", [{}])
        if message_list and len(message_list) > 0:
            content_list = message_list[0].get("content", [])
            if content_list and len(content_list) > 0:
                raw_data_str = content_list[0].get("text", "")
            else:
                raw_data_str = ""
        else:
            raw_data_str = ""
        
        if not raw_data_str:
            print(f"Warning: Unable to extract valid data from API response, attempting to save complete response")
            raw_data = data
        else:
            # text field is a JSON string, needs parsing
            try:
                raw_data = json.loads(raw_data_str)
                print("Successfully extracted JSON data from text field")
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse JSON in text field: {e}")
                print("Will save complete API response")
                raw_data = data
        
        # Check if data is valid (not empty)
        if not is_valid_data(raw_data):
            print(f"Warning: Data for {start_date} is empty, skipping save")
            return None
        
        # Ensure subfolder "success rate" exists
        os.makedirs(success_rate_dir, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)
        
        print(f"Raw data saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error: Failed to save data file: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Fetch payment success rate data from Antom')
    parser.add_argument('--date', required=True, help='Specify date, automatically pull data for each day of the previous week, format: YYYYMMDD')
    parser.add_argument('--merchant_token', help='Merchant token (optional, read from configuration file)')
    
    args = parser.parse_args()
    
    # Apply T+1 logic: check if user wants today's data
    actual_date, is_today = calculate_t1_date(args.date)
    
    if is_today:
        print(f"User requested to query today's data ({args.date})")
        print(f"Due to Antom T+1 data generation, will actually query: {actual_date} and the previous week")
    else:
        print(f"User requested to query date: {args.date}")
        print(f"Will query: {actual_date} and the previous week")
    print()
    
    # Calculate 7 dates of the previous week (based on actual_date)
    dates = calculate_date_range(actual_date)
    print(f"Will fetch data for the following 7 days:")
    for i, date in enumerate(dates):
        print(f"  {i+1}. {date}")
    print()
    
    # Load configuration
    config = load_config()
    validate_config(config)
    
    # Get merchant_token
    merchant_token = args.merchant_token or config.get("merchant_token")
    
    if not merchant_token:
        print("Error: merchant_token must be provided (via parameter or configuration file)")
        sys.exit(1)
    
    # Loop to fetch data for each day
    success_count = 0
    skipped_count = 0
    saved_dates = []
    
    for date in dates:
        date_range = f"{date}~{date}"
        print(f"\n[{success_count + skipped_count + 1}/7] Fetching data for {date}...")
        
        try:
            # Fetch data
            data = query_antom_api(date_range, merchant_token)
            
            # Save data (automatically checks if data is empty)
            saved_path = save_raw_data(data, date)
            
            if saved_path:
                success_count += 1
                saved_dates.append(date)
                print(f"  ✓ Data for {date} saved")
            else:
                skipped_count += 1
                print(f"  ⊘ Data for {date} is empty, skipped")
        except Exception as e:
            skipped_count += 1
            print(f"  ✗ Failed to fetch {date}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print(f"Data pulling completed!")
    print(f"  Successful: {success_count} days")
    print(f"  Skipped: {skipped_count} days")
    print(f"{'='*60}")
    
    if success_count > 0:
        print(f"\nDates with saved data:")
        for date in saved_dates:
            print(f"  - {date}")
        print(f"\nMost recent valid data date: {saved_dates[0]}")
    else:
        print(f"\n⚠️  Warning: No valid data retrieved")
        sys.exit(1)


if __name__ == "__main__":
    main()
