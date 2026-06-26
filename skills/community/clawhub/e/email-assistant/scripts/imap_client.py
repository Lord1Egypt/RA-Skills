#!/usr/bin/env python3
"""
IMAP Client - Universal IMAP email client
Supports: 163, QQ, Outlook, Hotmail
"""

import imaplib
import email
import json
import argparse
import sys
from datetime import datetime
from typing import Optional, List, Dict


# IMAP server configurations
IMAP_CONFIG = {
    "163": {
        "server": "imap.163.com",
        "port": 993,
        "ssl": True
    },
    "qq": {
        "server": "imap.qq.com",
        "port": 993,
        "ssl": True
    },
    "outlook": {
        "server": "outlook.office365.com",
        "port": 993,
        "ssl": True
    },
    "hotmail": {
        "server": "outlook.office365.com",
        "port": 993,
        "ssl": True
    }
}


def parse_email_provider(email_addr: str) -> str:
    """Detect email provider from email address."""
    domain = email_addr.split("@")[-1].lower()
    
    if "163" in domain or "126" in domain or "yeah" in domain:
        return "163"
    elif "qq" in domain:
        return "qq"
    elif "outlook" in domain or "live" in domain or "msn" in domain:
        return "outlook"
    elif "hotmail" in domain or "live.com" in domain or "msn.com" in domain:
        return "hotmail"
    else:
        raise ValueError(f"Unsupported email provider: {domain}")


def connect_imap(server: str, email_addr: str, password: str) -> imaplib.IMAP4_SSL:
    """Connect to IMAP server."""
    try:
        config = IMAP_CONFIG.get(server)
        if not config:
            # Try as custom server
            config = {"server": server, "port": 993, "ssl": True}
        
        if config.get("ssl", True):
            imap = imaplib.IMAP4_SSL(config["server"], config["port"])
        else:
            imap = imaplib.IMAP4(config["server"], config["port"])
        
        imap.login(email_addr, password)
        print(f"✓ Connected to {config['server']}")
        return imap
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)


def get_email_list(imap: imaplib.IMAP4_SSL, limit: int = 50) -> List[Dict]:
    """Fetch email list from INBOX."""
    try:
        status, messages = imap.select("INBOX")
        if status != "OK":
            print(f"✗ Failed to select INBOX: {messages}")
            return []
        
        # Get total number of messages
        total_msgs = int(messages[0])
        print(f"Total messages in INBOX: {total_msgs}")
        
        # Calculate range to fetch
        start = max(1, total_msgs - limit + 1)
        end = total_msgs
        
        emails = []
        for num in range(end, start - 1, -1):
            try:
                status, msg_data = imap.fetch(str(num), "(RFC822)")
                if status != "OK":
                    continue
                
                msg = email.message_from_bytes(msg_data[0][1])
                
                # Parse email headers
                subject = msg.get("Subject", "(No Subject)")
                from_addr = email.utils.parseaddr(msg.get("From", ""))[1]
                date = msg.get("Date", "")
                
                # Get preview (first 100 chars of body)
                preview = ""
                if msg.is_multipart:
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                preview = part.get_payload(decode=True).decode("utf-8", errors="ignore")[:200]
                                break
                            except:
                                pass
                else:
                    try:
                        preview = msg.get_payload(decode=True).decode("utf-8", errors="ignore")[:200]
                    except:
                        pass
                
                emails.append({
                    "id": num,
                    "subject": subject,
                    "from": from_addr,
                    "date": date,
                    "preview": preview.replace("\n", " ").strip()
                })
                
            except Exception as e:
                print(f"  Warning: Failed to fetch email {num}: {e}")
                continue
        
        return emails
        
    except Exception as e:
        print(f"✗ Failed to fetch emails: {e}")
        return []


def get_email_detail(imap: imaplib.IMAP4_SSL, email_id: int) -> Optional[Dict]:
    """Get full email details."""
    try:
        status, msg_data = imap.fetch(str(email_id), "(RFC822)")
        if status != "OK":
            return None
        
        msg = email.message_from_bytes(msg_data[0][1])
        
        # Parse headers
        subject = msg.get("Subject", "(No Subject)")
        from_addr = email.utils.parseaddr(msg.get("From", ""))
        to_addr = email.utils.parseaddr(msg.get("To", ""))
        date = msg.get("Date", "")
        
        # Parse body
        body_text = ""
        body_html = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain" and not body_text:
                    try:
                        body_text = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    except:
                        pass
                elif content_type == "text/html" and not body_html:
                    try:
                        body_html = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    except:
                        pass
        else:
            try:
                body_text = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
            except:
                pass
        
        return {
            "id": email_id,
            "subject": subject,
            "from": from_addr,
            "to": to_addr,
            "date": date,
            "body_text": body_text,
            "body_html": body_html
        }
        
    except Exception as e:
        print(f"✗ Failed to fetch email {email_id}: {e}")
        return None


def mark_as_read(imap: imaplib.IMAP4_SSL, email_id: int) -> bool:
    """Mark email as read."""
    try:
        status, _ = imap.store(str(email_id), "+FLAGS", "\\Seen")
        return status == "OK"
    except Exception as e:
        print(f"✗ Failed to mark email as read: {e}")
        return False


def mark_as_unread(imap: imaplib.IMAP4_SSL, email_id: int) -> bool:
    """Mark email as unread."""
    try:
        status, _ = imap.store(str(email_id), "-FLAGS", "\\Seen")
        return status == "OK"
    except Exception as e:
        print(f"✗ Failed to mark email as unread: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Universal IMAP Email Client")
    parser.add_argument("--server", help="IMAP server (auto-detected from email if not provided)")
    parser.add_argument("--email", required=True, help="Email address")
    parser.add_argument("--password", required=True, help="Password or app token")
    parser.add_argument("--limit", type=int, default=50, help="Number of emails to fetch (default: 50)")
    parser.add_argument("--list", action="store_true", help="List emails")
    parser.add_argument("--read", type=int, help="Read specific email by ID")
    parser.add_argument("--mark-read", type=int, help="Mark email as read")
    parser.add_argument("--mark-unread", type=int, help="Mark email as unread")
    parser.add_argument("--output", help="Output file (JSON)")
    
    args = parser.parse_args()
    
    # Auto-detect provider if not specified
    server = args.server or parse_email_provider(args.email)
    print(f"Using provider: {server}")
    
    # Connect
    imap = connect_imap(server, args.email, args.password)
    
    try:
        if args.list:
            print(f"\nFetching last {args.limit} emails...")
            emails = get_email_list(imap, args.limit)
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(emails, f, ensure_ascii=False, indent=2)
                print(f"✓ Saved to {args.output}")
            else:
                print(f"\n{'='*60}")
                for i, email in enumerate(emails, 1):
                    print(f"\n[{i}] Subject: {email['subject']}")
                    print(f"    From: {email['from']}")
                    print(f"    Date: {email['date']}")
                    print(f"    Preview: {email['preview'][:80]}...")
                    
        elif args.read:
            email_detail = get_email_detail(imap, args.read)
            if email_detail:
                print(f"\nSubject: {email_detail['subject']}")
                print(f"From: {email_detail['from']}")
                print(f"To: {email_detail['to']}")
                print(f"Date: {email_detail['date']}")
                print(f"\n{'='*60}")
                print(email_detail["body_text"][:2000])
            else:
                print("Email not found")
                
        elif args.mark_read:
            if mark_as_read(imap, args.mark_read):
                print(f"✓ Email {args.mark_read} marked as read")
            else:
                print(f"✗ Failed to mark email as read")
                
        elif args.mark_unread:
            if mark_as_unread(imap, args.mark_unread):
                print(f"✓ Email {args.mark_unread} marked as unread")
            else:
                print(f"✗ Failed to mark email as unread")
        else:
            parser.print_help()
            
    finally:
        imap.logout()
        print("\n✓ Logged out")


if __name__ == "__main__":
    main()
