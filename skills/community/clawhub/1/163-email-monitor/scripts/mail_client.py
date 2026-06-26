#!/usr/bin/env python3
"""
163/126/yeah.net (Coremail) Mail Client
Handles the Coremail-specific IMAP ID command requirement.
"""
import imaplib
import smtplib
import email
import os
import sys
import json
import argparse
import re
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


def load_config(env_path=None):
    """
    Load email configuration from environment file.
    Only reads IMAP/SMTP server settings and credentials.
    """
    if env_path is None:
        env_path = os.path.expanduser("~/.openclaw/email-monitor/.env")
    
    config = {}
    if not os.path.exists(env_path):
        print(f"Error: Configuration file not found: {env_path}")
        print("Please create the file with your email settings.")
        sys.exit(1)
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)
    
    # Validate required fields
    required = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD']
    for field in required:
        if not config.get(field):
            print(f"Error: Missing required config field: {field}")
            sys.exit(1)
    
    return {
        "imap_server": config.get("IMAP_SERVER", "imap.163.com"),
        "imap_port": int(config.get("IMAP_PORT", "993")),
        "smtp_server": config.get("SMTP_SERVER", "smtp.163.com"),
        "smtp_port": int(config.get("SMTP_PORT", "465")),
        "email": config["EMAIL_ADDRESS"],
        "password": config["EMAIL_PASSWORD"],
    }


def decode_email_header(header_value):
    """
    Safely decode email header strings that may contain encoded parts.
    Handles various character encodings safely.
    """
    if header_value is None:
        return ""
    
    try:
        parts = decode_header(header_value)
        result_parts = []
        for part, charset in parts:
            if isinstance(part, bytes):
                # Use safe decoding with fallback
                decoded = part.decode(charset or 'utf-8', errors='replace')
                result_parts.append(decoded)
            else:
                result_parts.append(str(part))
        return " ".join(result_parts)
    except Exception:
        # Fallback: return as string with replacement characters
        return str(header_value)


def extract_text_content(email_message):
    """
    Extract plain text content from email message.
    Handles both plain text and HTML emails.
    """
    if not email_message:
        return ""
    
    if email_message.is_multipart():
        # Walk through message parts
        for part in email_message.walk():
            content_type = part.get_content_type()
            
            if content_type == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        return payload.decode(charset, errors='replace')
                except Exception:
                    continue
                    
            elif content_type == "text/html":
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        html_content = payload.decode(charset, errors='replace')
                        # Convert HTML to plain text
                        text = re.sub(r'<[^>]+>', ' ', html_content)
                        text = re.sub(r'\s+', ' ', text).strip()
                        return text[:2000]
                except Exception:
                    continue
    else:
        # Single part message
        try:
            payload = email_message.get_payload(decode=True)
            if payload:
                charset = email_message.get_content_charset() or 'utf-8'
                return payload.decode(charset, errors='replace')
        except Exception:
            pass
    
    return ""


def establish_imap_connection(config):
    """
    Establish secure IMAP connection with Coremail ID protocol.
    Coremail servers require an ID command before mailbox operations.
    """
    try:
        # Create SSL connection
        connection = imaplib.IMAP4_SSL(
            host=config["imap_server"],
            port=config["imap_port"]
        )
        
        # Send IMAP ID command (required by Coremail/163/126/yeah.net)
        # This identifies the client to the server
        tag = connection._new_tag()
        id_command = tag + b' ID ("name" "IMAPClient" "version" "1.0.0")\r\n'
        connection.send(id_command)
        # Read and discard responses
        connection.readline()
        connection.readline()
        
        # Authenticate
        connection.login(config["email"], config["password"])
        
        return connection
        
    except imaplib.IMAP4.error as e:
        print(f"IMAP connection error: {e}")
        raise
    except Exception as e:
        print(f"Connection failed: {e}")
        raise


def cmd_read_emails(args, config):
    """
    Read emails from inbox.
    Supports filtering by unread status and limiting results.
    """
    connection = None
    try:
        connection = establish_imap_connection(config)
        connection.select("INBOX", readonly=True)
        
        # Search for emails
        if args.unread:
            status, message_numbers = connection.search(None, "UNSEEN")
        else:
            status, message_numbers = connection.search(None, "ALL")
        
        if status != "OK":
            print("Search operation failed")
            return
        
        message_ids = message_numbers[0].split()
        if not message_ids:
            print("No emails found in inbox")
            return
        
        # Limit results
        limit = args.latest or len(message_ids)
        target_ids = message_ids[-limit:]
        
        results = []
        print(f"Found {len(message_ids)} emails, displaying {len(target_ids)}\n")
        
        for msg_id in target_ids:
            try:
                _, msg_data = connection.fetch(msg_id, "(RFC822)")
                email_message = email.message_from_bytes(msg_data[0][1])
                
                subject = decode_email_header(email_message["Subject"])
                from_addr = decode_email_header(email_message["From"])
                date = decode_email_header(email_message["Date"])
                body = extract_text_content(email_message) if args.body else ""
                
                entry = {
                    "id": msg_id.decode() if isinstance(msg_id, bytes) else str(msg_id),
                    "subject": subject,
                    "from": from_addr,
                    "date": date,
                }
                if body:
                    entry["body"] = body[:500]
                results.append(entry)
                
                print(f"{'─'*60}")
                print(f"Subject: {subject}")
                print(f"From: {from_addr}")
                print(f"Date: {date}")
                if body:
                    preview = body[:200].replace('\n', ' ')
                    print(f"Preview: {preview}...")
                    
            except Exception as e:
                print(f"Error processing message {msg_id}: {e}")
                continue
        
        if args.json:
            print("\n" + json.dumps(results, ensure_ascii=False, indent=2))
        
        print(f"\nCompleted. Retrieved {len(results)} emails.")
        
    finally:
        if connection:
            try:
                connection.close()
                connection.logout()
            except Exception:
                pass


def cmd_search_emails(args, config):
    """
    Search emails with local filtering.
    Downloads emails and filters locally for better accuracy.
    """
    connection = None
    try:
        connection = establish_imap_connection(config)
        connection.select("INBOX", readonly=True)
        
        # Build IMAP date filter if provided
        criteria = []
        if args.since:
            criteria.append(f'SINCE {args.since}')
        if args.before:
            criteria.append(f'BEFORE {args.before}')
        
        if criteria:
            search_string = " ".join(criteria)
            status, message_numbers = connection.search(None, search_string)
        else:
            status, message_numbers = connection.search(None, "ALL")
        
        if status != "OK" or not message_numbers[0]:
            print("No emails match the criteria")
            return
        
        message_ids = message_numbers[0].split()
        scan_limit = min(len(message_ids), args.scan or 200)
        target_ids = message_ids[-scan_limit:]
        
        query_lower = args.query.lower() if args.query else None
        sender_lower = args.sender.lower() if args.sender else None
        result_limit = args.latest or 20
        
        results = []
        print(f"Scanning {len(target_ids)} emails...\n")
        
        for msg_id in reversed(target_ids):
            if len(results) >= result_limit:
                break
                
            try:
                _, msg_data = connection.fetch(msg_id, "(RFC822)")
                email_message = email.message_from_bytes(msg_data[0][1])
                
                subject = decode_email_header(email_message["Subject"])
                from_addr = decode_email_header(email_message["From"])
                date = decode_email_header(email_message["Date"])
                
                # Apply local filters
                if query_lower:
                    searchable_text = (subject + " " + from_addr).lower()
                    if query_lower not in searchable_text:
                        body_text = extract_text_content(email_message).lower()
                        if query_lower not in body_text:
                            continue
                
                if sender_lower and sender_lower not in from_addr.lower():
                    continue
                
                body = extract_text_content(email_message) if args.body else ""
                
                entry = {
                    "id": msg_id.decode() if isinstance(msg_id, bytes) else str(msg_id),
                    "subject": subject,
                    "from": from_addr,
                    "date": date,
                }
                if body:
                    entry["body"] = body[:500]
                results.append(entry)
                
                print(f"{'─'*60}")
                print(f"Subject: {subject}")
                print(f"From: {from_addr}")
                print(f"Date: {date}")
                
            except Exception as e:
                print(f"Error processing message {msg_id}: {e}")
                continue
        
        if not results:
            print("No matching emails found")
            return
        
        if args.json:
            print("\n" + json.dumps(results, ensure_ascii=False, indent=2))
        
        print(f"\nCompleted. Found {len(results)} results.")
        
    finally:
        if connection:
            try:
                connection.close()
                connection.logout()
            except Exception:
                pass


def cmd_send_email(args, config):
    """
    Send email via SMTP with optional attachments.
    """
    # Build message
    if args.attach:
        message = MIMEMultipart()
        message.attach(MIMEText(args.body or "", "plain", "utf-8"))
        
        for filepath in args.attach:
            filepath = os.path.expanduser(filepath)
            if not os.path.exists(filepath):
                print(f"Error: Attachment not found: {filepath}")
                return
            
            try:
                part = MIMEBase("application", "octet-stream")
                with open(filepath, "rb") as f:
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}"
                )
                message.attach(part)
            except Exception as e:
                print(f"Error attaching file {filepath}: {e}")
                return
    else:
        message = MIMEText(args.body or "", "plain", "utf-8")
    
    # Set headers
    message["From"] = config["email"]
    message["To"] = args.to
    message["Subject"] = args.subject or "(No Subject)"
    if args.cc:
        message["Cc"] = args.cc
    
    # Send via SMTP
    smtp_connection = None
    try:
        smtp_connection = smtplib.SMTP_SSL(
            host=config["smtp_server"],
            port=config["smtp_port"]
        )
        smtp_connection.login(config["email"], config["password"])
        
        recipients = [args.to]
        if args.cc:
            recipients.extend(args.cc.split(","))
        
        smtp_connection.sendmail(
            config["email"],
            recipients,
            message.as_string()
        )
        
        print(f"Email sent successfully to {args.to}")
        if args.cc:
            print(f"CC: {args.cc}")
            
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        if smtp_connection:
            try:
                smtp_connection.quit()
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(
        description="163/Coremail Email Client - Read, search, and send emails"
    )
    parser.add_argument(
        "--env",
        help="Path to configuration file (default: ~/.openclaw/email-monitor/.env)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Read command
    read_parser = subparsers.add_parser("read", help="Read emails from inbox")
    read_parser.add_argument(
        "--unread",
        action="store_true",
        help="Show only unread emails"
    )
    read_parser.add_argument(
        "--latest",
        type=int,
        help="Limit to N most recent emails"
    )
    read_parser.add_argument(
        "--body",
        action="store_true",
        help="Include email body content"
    )
    read_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search emails")
    search_parser.add_argument(
        "query",
        nargs="?",
        help="Search text (searches subject and body)"
    )
    search_parser.add_argument(
        "--from",
        dest="sender",
        help="Filter by sender email address"
    )
    search_parser.add_argument(
        "--since",
        help="Search emails since date (DD-Mon-YYYY)"
    )
    search_parser.add_argument(
        "--before",
        help="Search emails before date (DD-Mon-YYYY)"
    )
    search_parser.add_argument(
        "--latest",
        type=int,
        default=20,
        help="Maximum number of results (default: 20)"
    )
    search_parser.add_argument(
        "--scan",
        type=int,
        default=200,
        help="Maximum emails to scan (default: 200)"
    )
    search_parser.add_argument(
        "--body",
        action="store_true",
        help="Include email body content in output"
    )
    search_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    # Send command
    send_parser = subparsers.add_parser("send", help="Send an email")
    send_parser.add_argument(
        "--to",
        required=True,
        help="Recipient email address"
    )
    send_parser.add_argument(
        "--subject",
        help="Email subject"
    )
    send_parser.add_argument(
        "--body",
        help="Email body text"
    )
    send_parser.add_argument(
        "--cc",
        help="CC recipients (comma-separated)"
    )
    send_parser.add_argument(
        "--attach",
        nargs="+",
        help="Attachment file paths"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    config = load_config(args.env)
    
    if args.command == "read":
        cmd_read_emails(args, config)
    elif args.command == "search":
        cmd_search_emails(args, config)
    elif args.command == "send":
        cmd_send_email(args, config)


if __name__ == "__main__":
    main()
