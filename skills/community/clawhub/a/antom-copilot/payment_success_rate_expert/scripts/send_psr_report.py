#!/usr/bin/env python3
"""
Antom Payment Success Rate Report Sender
Send payment success rate report emails with intelligent analysis
"""

import argparse
import json
import os
import sys
import smtplib
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import mimetypes


def get_config_path():
    """Get configuration file path, compatible with macOS, Linux and Windows"""
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
        print("Please configure conf.json first")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error: Failed to read configuration file: {e}")
        sys.exit(1)


def get_report_file_path(date_str):
    """Get report file path"""
    if platform.system() == "Windows":
        base_dir = os.path.join(os.environ["USERPROFILE"], "antom", "success rate")
    else:
        base_dir = os.path.expanduser("~/antom/success rate")
    
    report_dir = os.path.join(base_dir, date_str)
    filename = f"{date_str}-Payment-Success-Rate-Report.pdf"
    filepath = os.path.join(report_dir, filename)
    
    return filepath


def get_executive_summary_path(date_str):
    """Get executive summary file path"""
    if platform.system() == "Windows":
        base_dir = os.path.join(os.environ["USERPROFILE"], "antom", "success rate")
    else:
        base_dir = os.path.expanduser("~/antom/success rate")
    
    report_dir = os.path.join(base_dir, date_str)
    filename = f"{date_str}_executive_summary.txt"
    filepath = os.path.join(report_dir, filename)
    
    return filepath


def get_raw_data_path(date_str):
    """Get raw data file path"""
    if platform.system() == "Windows":
        base_dir = os.path.join(os.environ["USERPROFILE"], "antom", "success rate")
    else:
        base_dir = os.path.expanduser("~/antom/success rate")
    
    filename = f"{date_str}_raw_data.json"
    filepath = os.path.join(base_dir, filename)
    
    return filepath


def send_email_with_attachment(smtp_config, recipient, subject, body, attachment_path):
    """
    Send email with attachment
    
    Args:
        smtp_config: SMTP configuration dictionary
        recipient: Recipient email address
        subject: Email subject
        body: Email body
        attachment_path: Attachment path
    """
    # Create email object
    msg = MIMEMultipart()
    msg['From'] = smtp_config['username']
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Add email body
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Add attachment
    if os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        
        # Guess file type
        ctype, encoding = mimetypes.guess_type(attachment_path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        
        maintype, subtype = ctype.split('/', 1)
        
        with open(attachment_path, 'rb') as f:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())
            
        encoders.encode_base64(mime)
        mime.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(mime)
        
        print(f"Attachment added: {filename}")
    else:
        print(f"Warning: Attachment file not found: {attachment_path}")
    
    # Connect to SMTP server and send email
    try:
        print(f"Connecting to SMTP server {smtp_config['smtp_server']}...")
        
        # Create SMTP connection
        server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
        
        # Enable TLS if needed
        if smtp_config.get('use_tls', True):
            server.starttls()
        
        # Login
        server.login(smtp_config['username'], smtp_config['password'])
        print("Login successful")
        
        # Send email
        text = msg.as_string()
        server.sendmail(smtp_config['username'], recipient, text)
        print(f"Email successfully sent to: {recipient}")
        
        # Close connection
        server.quit()
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"Error: SMTP authentication failed, please check username and password: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"Error: Email sending failed: {e}")
        return False
    except Exception as e:
        print(f"Error: Unknown error occurred while sending email: {e}")
        return False


def generate_email_content(date_str, executive_summary_path):
    """Generate email content with executive summary"""
    # Read executive summary from file
    try:
        with open(executive_summary_path, 'r', encoding='utf-8') as f:
            executive_summary = f.read()
    except:
        executive_summary = "Executive Summary is not available."
    
    content = f"""Dear Merchant,

Please find attached your Payment Success Rate Report for {date_str}:

{'=' * 60}
EXECUTIVE SUMMARY
{'=' * 60}

{executive_summary}

{'=' * 60}
DETAILED REPORT ATTACHED
{'=' * 60}

The attached PDF contains complete analysis including:
• Comprehensive success rate trends and comparisons
• Detailed error code distribution charts
• Country and bank performance breakdowns
• System type analysis for APM payments
• Historical data comparisons and actionable recommendations

Please review the detailed report for full insights.

Best regards,
Antom Payment Success Rate Analytics System

This is an automated report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."""
    return content


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


def is_valid_data(data):
    """
    Check if the data is valid (not empty)
    
    Args:
        data: Raw data dictionary
    
    Returns:
        bool: True if data is valid, False otherwise
    """
    try:
        # Check if card.total has data
        card_total = data.get('card', {}).get('total', {})
        if not card_total or card_total.get('total_count', 0) == 0:
            return False
        
        # Check if apm.total has data
        apm_total = data.get('apm', {}).get('total', {})
        if not apm_total or apm_total.get('total_count', 0) == 0:
            return False
            
        return True
    except Exception as e:
        print(f"Warning: Error checking data validity: {e}")
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
    from datetime import datetime, timedelta
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
                        print(f"Note: Data for {target_date_str} is invalid, using most recent valid date: {check_date_str}")
                    return check_date_str
            except Exception as e:
                print(f"Warning: Error reading {data_file}: {e}")
        
        if i == max_lookback - 1:
            print(f"Warning: No valid data found for {target_date_str} and previous {max_lookback} days")
    
    # If no valid data found, return original date
    return target_date_str


def parse_recipients(recipient_input):
    """
    Parse recipients from input string, supporting comma-separated and space-separated formats
    
    Args:
        recipient_input: String containing recipients (comma or space separated)
    
    Returns:
        list: List of cleaned recipient email addresses
    """
    # Replace semicolons and spaces with commas, then split by commas
    recipients = recipient_input.replace(';', ',').replace(' ', ',')
    recipients_list = [r.strip() for r in recipients.split(',') if r.strip()]
    
    # Validate email addresses
    valid_recipients = []
    for email in recipients_list:
        if '@' in email and '.' in email and len(email) >= 5:
            valid_recipients.append(email)
        else:
            print(f"Warning: Ignoring invalid email address: {email}")
    
    return valid_recipients


def main():
    parser = argparse.ArgumentParser(description='Send payment success rate report email with intelligent analysis')
    parser.add_argument('--date', required=True, help='Report date, format: YYYYMMDD (T+1 logic: if requesting today, will use yesterday)')
    parser.add_argument('--recipient', required=True, help='Recipient email address(es), supports comma or space separated list')
    
    args = parser.parse_args()
    
    # Validate date format
    try:
        datetime.strptime(args.date, "%Y%m%d")
    except ValueError:
        print(f"Error: Date format is incorrect, should be YYYYMMDD format")
        sys.exit(1)
    
    # Parse recipients
    recipients_list = parse_recipients(args.recipient)
    if not recipients_list:
        print(f"Error: No valid recipient email addresses found in: {args.recipient}")
        sys.exit(1)
    
    print(f"Found {len(recipients_list)} valid recipient(s): {', '.join(recipients_list)}")
    
    # Apply T+1 logic: check if user wants today's data
    actual_date, is_today = calculate_t1_date(args.date)
    
    if is_today:
        print(f"User requested to send report for: {args.date} (today)")
        print(f"Due to T+1 data generation, will use report from: {actual_date}")
    else:
        print(f"User requested to send report for: {args.date}")
        print(f"Using historical report from: {actual_date}")
    
    # Load configuration
    config = load_config()
    
    email_conf = config.get("email_conf")
    if not email_conf:
        print("Error: email_conf is missing from configuration file")
        sys.exit(1)
    
    # Validate email_conf fields
    required_fields = ["smtp_server", "smtp_port", "username", "password"]
    for field in required_fields:
        if field not in email_conf:
            print(f"Error: email_conf is missing required field: {field}")
            sys.exit(1)
    
    # Find the last valid date with data (skip empty dates)
    valid_date = find_last_valid_date(actual_date)
    
    if valid_date != actual_date:
        print(f"Note: Searching for most recent valid data date: {valid_date}")
    
    # Get report file path (using valid_date)
    report_file_path = get_report_file_path(valid_date)
    if not os.path.exists(report_file_path):
        print(f"Error: Report file not found: {report_file_path}")
        print(f"Please confirm that the report for {valid_date} has been generated using analyse_and_gen_report tool")
        sys.exit(1)
    
    # Get executive summary file path (using valid_date)
    executive_summary_path = get_executive_summary_path(valid_date)
    if not os.path.exists(executive_summary_path):
        print(f"Warning: Executive summary not found: {executive_summary_path}")
    
    # Generate email content (using valid_date)
    subject = f"{valid_date}-Payment Success Rate Report"
    body = generate_email_content(valid_date, executive_summary_path)
    
    # Send email to each recipient
    success_count = 0
    fail_count = 0
    
    for i, recipient in enumerate(recipients_list, 1):
        print(f"\n[{i}/{len(recipients_list)}] Sending {valid_date} payment success rate report to {recipient}...")
        success = send_email_with_attachment(email_conf, recipient, subject, body, report_file_path)
        
        if success:
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Email sending completed!")
    print(f"  Success: {success_count}")
    print(f"  Failed: {fail_count}")
    print(f"{'='*60}")
    
    if fail_count > 0:
        print("Some emails failed to send, please check the errors above")
        sys.exit(1)
    else:
        print("All emails sent successfully!")


if __name__ == "__main__":
    main()
