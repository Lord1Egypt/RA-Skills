#!/usr/bin/env python3
"""
SMTP utilities for Postfix - Pure Python, no external dependencies
"""

import smtplib
import imaplib
import email
import json
import argparse
import os
import sys
from email.message import EmailMessage
from pathlib import Path
import time

def load_config():
    """Load configuration from config.json"""
    possible_paths = [
        Path(__file__).parent.parent / 'config.json',
        Path.cwd() / 'config.json',
        Path.home() / '.openclaw' / 'skills' / 'email-manager' / 'config.json',
    ]
    
    for config_path in possible_paths:
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
    
    return {
        "email_address": os.getenv('EMAIL_ADDRESS', ''),
        "email_password": os.getenv('EMAIL_PASSWORD', ''),
        "smtp_server": os.getenv('SMTP_SERVER', 'localhost'),
        "smtp_port": int(os.getenv('SMTP_PORT', '465')),
        "imap_server": os.getenv('IMAP_SERVER', 'localhost'),
        "imap_port": int(os.getenv('IMAP_PORT', '993')),
        "folders": {
            "sent": os.getenv('SENT_FOLDER', 'Sent')
        }
    }

CONFIG = load_config()

class PostfixSMTP:
    def __init__(self, config=None):
        self.config = config or CONFIG
        
        self.email = self.config.get('email_address', '')
        self.password = self.config.get('email_password', '')
        self.smtp_server = self.config.get('smtp_server', 'localhost')
        self.smtp_port = self.config.get('smtp_port', 465)
        self.imap_server = self.config.get('imap_server', 'localhost')
        self.imap_port = self.config.get('imap_port', 993)
        self.folders = self.config.get('folders', {})
        self.save_sent = self.config.get('defaults', {}).get('save_sent_copy', True)
        
        if not all([self.email, self.password, self.smtp_server]):
            raise ValueError("Missing required configuration")
        
        # Connect to Postfix SMTP
        self.smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        self.smtp.login(self.email, self.password)
    
    def send_email(self, to_addr, subject, body, cc=None, bcc=None):
        """Send email via SMTP"""
        msg = EmailMessage()
        msg['From'] = self.email
        msg['To'] = to_addr
        msg['Subject'] = subject
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc
        msg.set_content(body)
        msg['Date'] = email.utils.formatdate(localtime=True)
        
        # Build recipient list
        recipients = [to_addr]
        if cc:
            recipients.append(cc)
        if bcc:
            recipients.append(bcc)
        
        # Send via SMTP
        self.smtp.send_message(msg)
        
        # Save to Sent folder if configured
        if self.save_sent:
            self._save_to_sent(msg)
        
        return {
            'status': 'sent',
            'to': to_addr,
            'subject': subject
        }
    
    def _save_to_sent(self, msg):
        """Save copy to Sent folder via IMAP"""
        try:
            imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            imap.login(self.email, self.password)
            
            # Find Sent folder
            sent_folder = self.folders.get('sent', 'Sent')
            try:
                imap.select(sent_folder)
            except:
                # Try to find it
                result, data = imap.list()
                for item in data:
                    folder_str = item.decode()
                    if 'Sent' in folder_str:
                        if ' "/" ' in folder_str:
                            sent_folder = folder_str.split(' "/" ')[-1].strip('"')
                            break
            
            # Append to Sent folder
            imap.append(sent_folder, '\\Seen', 
                       imaplib.Time2Internaldate(time.time()),
                       msg.as_bytes())
            
            imap.close()
            imap.logout()
        except Exception as e:
            # Log but don't fail
            print(f"Warning: Could not save to Sent folder: {e}", file=sys.stderr)
    
    def close(self):
        """Close SMTP connection"""
        try:
            self.smtp.quit()
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description='SMTP email operations')
    
    # Global options
    parser.add_argument('--email', help='Email address (overrides config)')
    parser.add_argument('--password', help='Password (overrides config)')
    parser.add_argument('--smtp-server', help='SMTP server (overrides config)')
    parser.add_argument('--smtp-port', type=int, help='SMTP port (overrides config)')
    parser.add_argument('--config', help='Path to custom config file')
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Send email
    send_parser = subparsers.add_parser('send')
    send_parser.add_argument('--to', required=True)
    send_parser.add_argument('--subject', required=True)
    send_parser.add_argument('--body', required=True)
    send_parser.add_argument('--cc')
    send_parser.add_argument('--bcc')
    
    args = parser.parse_args()
    
    # Load config
    config = CONFIG
    if hasattr(args, 'config') and args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Override with command line args
    if args.email:
        config['email_address'] = args.email
    if args.password:
        config['email_password'] = args.password
    if args.smtp_server:
        config['smtp_server'] = args.smtp_server
    if args.smtp_port:
        config['smtp_port'] = args.smtp_port
    
    smtp = PostfixSMTP(config)
    
    try:
        if args.command == 'send':
            result = smtp.send_email(args.to, args.subject, args.body, args.cc, args.bcc)
            print(json.dumps(result))
    
    finally:
        smtp.close()

if __name__ == '__main__':
    main()