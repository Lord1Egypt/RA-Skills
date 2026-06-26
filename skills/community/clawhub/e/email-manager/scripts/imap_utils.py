#!/usr/bin/env python3
"""
IMAP utilities for Dovecot - Pure Python, no external dependencies
Includes Spam/Junk folder support
"""

import imaplib
import email
import json
import argparse
import os
import sys
from email.message import EmailMessage
from email.header import decode_header
from datetime import datetime
from pathlib import Path
import base64
import time

def load_config():
    """Load configuration from config.json (pure Python)"""
    # Look for config in multiple locations
    possible_paths = [
        Path(__file__).parent.parent / 'config.json',  # ../config.json
        Path.cwd() / 'config.json',                    # ./config.json
        Path.home() / '.openclaw' / 'skills' / 'email-manager' / 'config.json',
        Path('/etc/openclaw/skills/email-manager/config.json')
    ]
    
    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing {config_path}: {e}", file=sys.stderr)
                sys.exit(1)
    
    # Fallback to environment variables
    print("⚠️  No config.json found, falling back to environment variables", file=sys.stderr)
    return {
        "email_address": os.getenv('EMAIL_ADDRESS', ''),
        "email_password": os.getenv('EMAIL_PASSWORD', ''),
        "imap_server": os.getenv('IMAP_SERVER', 'localhost'),
        "imap_port": int(os.getenv('IMAP_PORT', '993')),
        "smtp_server": os.getenv('SMTP_SERVER', 'localhost'),
        "smtp_port": int(os.getenv('SMTP_PORT', '465')),
        "folders": {
            "inbox": os.getenv('INBOX_FOLDER', 'INBOX'),
            "drafts": os.getenv('DRAFTS_FOLDER', 'Drafts'),
            "sent": os.getenv('SENT_FOLDER', 'Sent'),
            "trash": os.getenv('TRASH_FOLDER', 'Trash'),
            "junk": os.getenv('JUNK_FOLDER', 'Junk')      # Added Spam/Junk
        }
    }

# Load config once
CONFIG = load_config()

class DovecotIMAP:
    def __init__(self, config=None):
        self.config = config or CONFIG
        
        # Get settings from config
        self.email = self.config.get('email_address', '')
        self.password = self.config.get('email_password', '')
        self.imap_server = self.config.get('imap_server', 'localhost')
        self.imap_port = self.config.get('imap_port', 993)
        
        # Get folder names
        self.folders = self.config.get('folders', {})
        self.draft_folder = self.folders.get('drafts', 'Drafts')
        self.inbox_folder = self.folders.get('inbox', 'INBOX')
        self.sent_folder = self.folders.get('sent', 'Sent')
        self.trash_folder = self.folders.get('trash', 'Trash')
        self.junk_folder = self.folders.get('junk', 'Junk')      # Added Spam/Junk
        self.archive_folder = self.folders.get('archive', 'Archive')
        
        # Defaults
        self.defaults = self.config.get('defaults', {})
        self.list_limit = self.defaults.get('list_limit', 20)
        
        if not all([self.email, self.password, self.imap_server]):
            raise ValueError("Missing required configuration. Check config.json or environment variables.")
        
        # Connect to Dovecot IMAP
        self.imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        self.imap.login(self.email, self.password)
    
    def list_folders(self):
        """List all available mail folders"""
        result, data = self.imap.list()
        if result != 'OK':
            return []
        
        folders = []
        for item in data:
            # Parse IMAP folder listing
            folder_info = self._parse_list_response(item.decode())
            folders.append(folder_info)
        return folders
    
    def _parse_list_response(self, line):
        #Parse IMAP LIST response and clean folder names
        # Default values
        flags = []
        delimiter = '/'
        name = line
        
        try:
            # Standard IMAP LIST response format: (FLAGS) "/" "FOLDER.NAME"
            if line.startswith('('):
                end_flags = line.index(')')
                flags = line[1:end_flags].split()
                
                # Rest looks like: "/" "Folder.Name"
                rest = line[end_flags+1:].strip()
                
                # Split into parts
                parts = rest.split('"')
                if len(parts) >= 3:
                    # parts[0] is delimiter with spaces, parts[1] is empty or delimiter
                    delimiter = parts[1].strip() if parts[1].strip() else '/'
                    # parts[2] is the actual folder name
                    name = parts[2].strip('" ')
                else:
                    name = rest.strip('" ')
        except:
            pass
        
        return {
            'name': name,
            'delimiter': delimiter,
            'flags': flags
    }
    
    def find_folder(self, folder_type='inbox'):
        """Find folder by type (drafts, sent, trash, junk, etc.)"""
        # First try configured name
        folder_map = {
            'drafts': self.draft_folder,
            'sent': self.sent_folder,
            'trash': self.trash_folder,
            'junk': self.junk_folder,      # Added
            'inbox': self.inbox_folder,
            'archive': self.archive_folder
        }
        
        configured_name = folder_map.get(folder_type)
        if configured_name:
            try:
                self.imap.select(configured_name)
                return configured_name
            except:
                pass
        
        # Then try to find by scanning
        folders = self.list_folders()
        keywords = {
            'drafts': ['Drafts', 'Draft', 'INBOX.Drafts'],
            'sent': ['Sent', 'Sent Messages', 'INBOX.Sent'],
            'trash': ['Trash', 'Deleted', 'INBOX.Trash'],
            'junk': ['Junk', 'Spam', 'INBOX.Junk', 'INBOX.Spam', 'Bulk'],  # Added
            'inbox': ['INBOX', 'Inbox'],
            'archive': ['Archive', 'Archives', 'INBOX.Archive']
        }
        
        search_terms = keywords.get(folder_type, [])
        for folder in folders:
            folder_name = folder['name']
            for term in search_terms:
                if term.lower() in folder_name.lower():
                    try:
                        self.imap.select(folder_name)
                        return folder_name
                    except:
                        continue
        
        # Fallback
        fallback = {
            'drafts': 'Drafts',
            'sent': 'Sent',
            'trash': 'Trash',
            'junk': 'Junk',          # Added
            'inbox': 'INBOX',
            'archive': 'Archive'
        }.get(folder_type, folder_type)
        
        return fallback
    
    def select_folder(self, folder):
        """Select a folder for operations"""
        try:
            result, data = self.imap.select(folder)
            if result != 'OK':
                # Try to find the folder
                folder = self.find_folder(folder.lower())
                result, data = self.imap.select(folder)
            
            if result != 'OK':
                raise Exception(f"Failed to select folder {folder}")
            
            return int(data[0]) if data[0] else 0
        except Exception as e:
            raise Exception(f"Failed to select folder {folder}: {e}")
    
    def list_messages(self, folder='INBOX', limit=None, flagged_only=False, output_json=False):
        """List messages in folder"""
        if limit is None:
            limit = self.list_limit
            
        try:
            self.select_folder(folder)
        except Exception as e:
            print(f"Error selecting folder: {e}", file=sys.stderr)
            return []
        
        # Build search criteria
        criteria = 'ALL'
        if flagged_only:
            criteria = 'FLAGGED'
        
        result, data = self.imap.search(None, criteria)
        if result != 'OK':
            return []
        
        message_ids = data[0].split()
        messages = []
        
        # Apply limit (get most recent first)
        for msg_id in message_ids[-limit:]:
            try:
                # Get flags
                flag_result, flag_data = self.imap.fetch(msg_id, '(FLAGS)')
                flags = []
                starred = False
                if flag_result == 'OK':
                    flag_str = flag_data[0].decode()
                    if '\\Flagged' in flag_str:
                        flags.append('\\Flagged')
                        starred = True
                
                # Get message envelope
                result, data = self.imap.fetch(msg_id, '(RFC822)')
                if result != 'OK':
                    continue
                
                msg = email.message_from_bytes(data[0][1])
                
                messages.append({
                    'id': msg_id.decode(),
                    'subject': self._decode_header(msg.get('Subject', 'No Subject')),
                    'from': self._decode_header(msg.get('From', 'Unknown')),
                    'to': self._decode_header(msg.get('To', '')),
                    'date': msg.get('Date', ''),
                    'flags': flags,
                    'starred': starred,
                    'folder': folder
                })
            except Exception as e:
                continue  # Skip problematic messages
        
        if output_json:
            print(json.dumps(messages, indent=2))
            return
        
        return messages
    
    def read_message(self, message_id, folder='INBOX'):
        """Read full message content"""
        self.select_folder(folder)
        result, data = self.imap.fetch(str(message_id).encode(), '(RFC822)')
        if result != 'OK':
            raise Exception(f"Failed to fetch message {message_id}")
        
        msg = email.message_from_bytes(data[0][1])
        
        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode('utf-8', errors='ignore')
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode('utf-8', errors='ignore')
        
        # Mark as read if configured
        if self.defaults.get('mark_as_read', True):
            self.imap.store(str(message_id).encode(), '+FLAGS', '\\Seen')
        
        return {
            'id': message_id,
            'subject': self._decode_header(msg.get('Subject', '')),
            'from': self._decode_header(msg.get('From', '')),
            'to': self._decode_header(msg.get('To', '')),
            'cc': self._decode_header(msg.get('Cc', '')),
            'date': msg.get('Date', ''),
            'body': body,
            'folder': folder
        }
    
    def _decode_header(self, header):
        """Decode email header"""
        if not header:
            return ""
        try:
            decoded_parts = decode_header(header)
            result = []
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        result.append(part.decode(encoding, errors='ignore'))
                    else:
                        result.append(part.decode('utf-8', errors='ignore'))
                else:
                    result.append(str(part))
            return " ".join(result)
        except:
            return str(header)
    
    def save_draft(self, to_addr, subject, body, cc=None, bcc=None):
        """Save message as draft"""
        draft_folder = self.find_folder('drafts')
        
        # Create email message
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
        
        # Save as draft (append with \Draft flag)
        result = self.imap.append(
            draft_folder,
            '\\Draft',
            imaplib.Time2Internaldate(time.time()),
            msg.as_bytes()
        )
        
        if result[0] != 'OK':
            raise Exception(f"Failed to save draft: {result}")
        
        # Try to extract UID from response
        uid = None
        if result[1] and result[1][0]:
            resp = result[1][0].decode()
            if 'APPENDUID' in resp:
                parts = resp.split()
                uid = parts[-1].rstrip(')')
        
        return {
            'status': 'saved',
            'folder': draft_folder,
            'uid': uid
        }
    
    def list_drafts(self, output_json=False):
        """List all drafts"""
        draft_folder = self.find_folder('drafts')
        return self.list_messages(folder=draft_folder, output_json=output_json)
    
    def list_spam(self, output_json=False):
        """List all messages in Spam/Junk folder"""
        junk_folder = self.find_folder('junk')
        return self.list_messages(folder=junk_folder, output_json=output_json)
    
    def flag_message(self, message_id, add=True, folder=None):
        """Add or remove star/flag"""
        if folder is None:
            folder = self.inbox_folder
        
        self.select_folder(folder)
        flag = '\\Flagged'
        
        if add:
            result = self.imap.store(str(message_id).encode(), '+FLAGS', flag)
        else:
            result = self.imap.store(str(message_id).encode(), '-FLAGS', flag)
        
        if result[0] != 'OK':
            raise Exception(f"Failed to {'add' if add else 'remove'} flag")
        
        return {'status': 'flagged' if add else 'unflagged', 'folder': folder}
    
    def mark_as_spam(self, message_id, from_folder=None):
        """Move message to Spam/Junk folder"""
        if from_folder is None:
            from_folder = self.inbox_folder
        
        junk_folder = self.find_folder('junk')
        return self.move_message(message_id, from_folder, junk_folder)
    
    def mark_as_ham(self, message_id, from_folder=None):
        """Move message from Spam to Inbox (mark as not spam)"""
        if from_folder is None:
            from_folder = self.junk_folder
        
        return self.move_message(message_id, from_folder, self.inbox_folder)
    
    def move_message(self, message_id, from_folder, to_folder):
        """Move message between folders"""
        self.select_folder(from_folder)
        
        # Copy to destination
        result = self.imap.copy(str(message_id).encode(), to_folder)
        if result[0] != 'OK':
            raise Exception(f"Failed to copy message to {to_folder}")
        
        # Mark for deletion in source
        self.imap.store(str(message_id).encode(), '+FLAGS', '\\Deleted')
        self.imap.expunge()
        
        return {
            'status': 'moved',
            'from': from_folder,
            'to': to_folder,
            'message_id': message_id
        }
    
    def create_folder(self, folder_name):
        """Create new mail folder"""
        result = self.imap.create(folder_name)
        if result[0] != 'OK':
            raise Exception(f"Failed to create folder {folder_name}")
        return {'status': 'created', 'name': folder_name}
    
    def delete_message(self, message_id, folder=None):
        """Delete message (move to trash or permanent)"""
        if folder is None:
            folder = self.inbox_folder
        
        # If trash folder exists, move there first
        try:
            trash_folder = self.find_folder('trash')
            if trash_folder and trash_folder != folder:
                return self.move_message(message_id, folder, trash_folder)
        except:
            pass
        
        # Otherwise permanent delete
        self.select_folder(folder)
        self.imap.store(str(message_id).encode(), '+FLAGS', '\\Deleted')
        self.imap.expunge()
        return {'status': 'deleted', 'folder': folder}
    
    def empty_trash(self):
        """Permanently delete all messages in Trash"""
        trash_folder = self.find_folder('trash')
        self.select_folder(trash_folder)
        self.imap.store("1:*", '+FLAGS', '\\Deleted')
        self.imap.expunge()
        return {'status': 'trash_emptied', 'folder': trash_folder}
    
    def empty_spam(self):
        """Permanently delete all messages in Spam/Junk"""
        junk_folder = self.find_folder('junk')
        self.select_folder(junk_folder)
        self.imap.store("1:*", '+FLAGS', '\\Deleted')
        self.imap.expunge()
        return {'status': 'spam_emptied', 'folder': junk_folder}
    
    def search_messages(self, query, folder='INBOX'):
        """Search messages using IMAP search"""
        self.select_folder(folder)
        
        # Parse simple query (can be expanded)
        result, data = self.imap.search(None, query)
        if result != 'OK':
            return []
        
        message_ids = data[0].split()
        messages = []
        
        for msg_id in message_ids[-50:]:  # Limit to 50 results
            try:
                result, data = self.imap.fetch(msg_id, '(RFC822)')
                if result != 'OK':
                    continue
                msg = email.message_from_bytes(data[0][1])
                messages.append({
                    'id': msg_id.decode(),
                    'subject': self._decode_header(msg.get('Subject', '')),
                    'from': self._decode_header(msg.get('From', '')),
                    'folder': folder
                })
            except:
                continue
        
        return messages
    
    def close(self):
        """Close IMAP connection"""
        try:
            self.imap.close()
            self.imap.logout()
        except:
            pass

def display_folders_cleanly(folders):
    """Display folders in a clean, human-readable format"""
    print("📁 Available folders:")
    for f in folders:
        folder_name = f['name']
        
        # Handle different naming patterns seen in Dovecot
        # Remove leading dot and quotes if present
        if folder_name.startswith('".'):
            # Format: ". INBOX.Drafts"
            parts = folder_name.split('" ')
            if len(parts) > 1:
                folder_name = parts[-1].strip('"')
        
        # Remove any remaining quotes
        folder_name = folder_name.strip('"')
        
        # Clean up common prefixes like "INBOX."
        if folder_name.startswith('INBOX.'):
            display_name = folder_name[6:]  # Remove "INBOX."
        else:
            display_name = folder_name
        
        # Mark special folders with emoji
        lower_name = folder_name.lower()
        if any(word in lower_name for word in ['junk', 'spam', 'bulk']):
            print(f"  • {display_name} 📧 SPAM")
        elif any(word in lower_name for word in ['draft']):
            print(f"  • {display_name} 📝 DRAFTS")
        elif any(word in lower_name for word in ['sent']):
            print(f"  • {display_name} 📤 SENT")
        elif any(word in lower_name for word in ['trash', 'deleted']):
            print(f"  • {display_name} 🗑️ TRASH")
        elif 'inbox' in lower_name:
            print(f"  • {display_name} 📥 INBOX")
        else:
            print(f"  • {display_name}")

def main():
    parser = argparse.ArgumentParser(description='IMAP email operations')
    
    # Global options
    parser.add_argument('--email', help='Email address (overrides config)')
    parser.add_argument('--password', help='Password (overrides config)')
    parser.add_argument('--imap-server', help='IMAP server (overrides config)')
    parser.add_argument('--imap-port', type=int, help='IMAP port (overrides config)')
    parser.add_argument('--config', help='Path to custom config file')
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # List folders
    list_folders_parser = subparsers.add_parser('list-folders')
    list_folders_parser.add_argument('--output', choices=['text', 'json'], default='text',
                                 help='Output format: text (human) or json (machine)')
    
    # List messages
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--folder', default='INBOX')
    list_parser.add_argument('--limit', type=int)
    list_parser.add_argument('--flagged-only', action='store_true')
    list_parser.add_argument('--output', choices=['text', 'json'], default='text')
    
    # List drafts
    list_drafts = subparsers.add_parser('list-drafts')
    list_drafts.add_argument('--output', choices=['text', 'json'], default='text')
    
    # List spam
    list_spam = subparsers.add_parser('list-spam')  # New
    list_spam.add_argument('--output', choices=['text', 'json'], default='text')
    
    # Read message
    read_parser = subparsers.add_parser('read')
    read_parser.add_argument('--message-id', required=True)
    read_parser.add_argument('--folder', default='INBOX')
    read_parser.add_argument('--output', choices=['text', 'json'], default='text')
    
    # Save draft
    draft_parser = subparsers.add_parser('save-draft')
    draft_parser.add_argument('--to', required=True)
    draft_parser.add_argument('--subject', required=True)
    draft_parser.add_argument('--body', required=True)
    draft_parser.add_argument('--cc')
    draft_parser.add_argument('--bcc')
    
    # Flag/star
    flag_parser = subparsers.add_parser('flag')
    flag_parser.add_argument('--message-id', required=True)
    flag_parser.add_argument('--add', action='store_true')
    flag_parser.add_argument('--remove', action='store_true')
    flag_parser.add_argument('--folder')
    
    # Mark as spam  (New)
    spam_parser = subparsers.add_parser('mark-spam')
    spam_parser.add_argument('--message-id', required=True)
    spam_parser.add_argument('--from-folder', default='INBOX')
    
    # Mark as ham (not spam)  (New)
    ham_parser = subparsers.add_parser('mark-ham')
    ham_parser.add_argument('--message-id', required=True)
    ham_parser.add_argument('--from-folder', default='Junk')
    
    # Empty spam  (New)
    subparsers.add_parser('empty-spam')
    
    # Empty trash
    subparsers.add_parser('empty-trash')
    
    # Move
    move_parser = subparsers.add_parser('move')
    move_parser.add_argument('--message-id', required=True)
    move_parser.add_argument('--from-folder', required=True)
    move_parser.add_argument('--to-folder', required=True)
    
    # Create folder
    create_parser = subparsers.add_parser('create-folder')
    create_parser.add_argument('--name', required=True)
    
    # Delete
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('--message-id', required=True)
    delete_parser.add_argument('--folder')
    
    # Search
    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('--query', required=True)
    search_parser.add_argument('--folder', default='INBOX')
    search_parser.add_argument('--output', choices=['text', 'json'], default='text')
    
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
    if args.imap_server:
        config['imap_server'] = args.imap_server
    if args.imap_port:
        config['imap_port'] = args.imap_port
    
    imap = DovecotIMAP(config)
    
    try:
        if args.command == 'list-folders':
            folders = imap.list_folders()
            if args.output == 'json':
                print(json.dumps(folders, indent=2))
            else:
                display_folders_cleanly(folders)
        
        elif args.command == 'list':
            msgs = imap.list_messages(
                args.folder, 
                args.limit, 
                args.flagged_only,
                args.output == 'json'
            )
            if args.output == 'text' and msgs:
                print(f"📧 Messages in {args.folder}:")
                for msg in msgs:
                    star = "⭐" if msg.get('starred') else "  "
                    print(f"{star} [{msg['id']}] {msg.get('date', '')[:16]}: {msg['subject']}")
                    print(f"    From: {msg['from'][:50]}")
                    print()
        
        elif args.command == 'list-drafts':
            imap.list_drafts(args.output == 'json')
        
        elif args.command == 'list-spam':  # New
            msgs = imap.list_spam(args.output == 'json')
            if args.output == 'text' and msgs:
                print(f"📧 Spam messages in {imap.junk_folder}:")
                for msg in msgs:
                    print(f"  [{msg['id']}] {msg.get('date', '')[:16]}: {msg['subject']}")
                    print(f"    From: {msg['from'][:50]}")
                    print()
        
        elif args.command == 'read':
            msg = imap.read_message(args.message_id, args.folder)
            if args.output == 'json':
                print(json.dumps(msg, indent=2))
            else:
                print(f"Subject: {msg['subject']}")
                print(f"From: {msg['from']}")
                print(f"To: {msg['to']}")
                print(f"Date: {msg['date']}")
                print(f"Folder: {msg['folder']}")
                print("\n" + "="*50)
                print(msg['body'])
        
        elif args.command == 'save-draft':
            result = imap.save_draft(args.to, args.subject, args.body, args.cc, args.bcc)
            print(json.dumps(result))
        
        elif args.command == 'flag':
            add_flag = args.add and not args.remove
            result = imap.flag_message(args.message_id, add_flag, args.folder)
            print(json.dumps(result))
        
        elif args.command == 'mark-spam':  # New
            result = imap.mark_as_spam(args.message_id, args.from_folder)
            print(json.dumps(result))
        
        elif args.command == 'mark-ham':  # New
            result = imap.mark_as_ham(args.message_id, args.from_folder)
            print(json.dumps(result))
        
        elif args.command == 'empty-spam':  # New
            result = imap.empty_spam()
            print(json.dumps(result))
        
        elif args.command == 'empty-trash':
            result = imap.empty_trash()
            print(json.dumps(result))
        
        elif args.command == 'move':
            result = imap.move_message(args.message_id, args.from_folder, args.to_folder)
            print(json.dumps(result))
        
        elif args.command == 'create-folder':
            result = imap.create_folder(args.name)
            print(json.dumps(result))
        
        elif args.command == 'delete':
            result = imap.delete_message(args.message_id, args.folder)
            print(json.dumps(result))
        
        elif args.command == 'search':
            results = imap.search_messages(args.query, args.folder)
            if args.output == 'json':
                print(json.dumps(results, indent=2))
            else:
                print(f"🔍 Search results for '{args.query}' in {args.folder}:")
                for msg in results:
                    print(f"  [{msg['id']}] {msg['subject']} - {msg['from']}")
    
    finally:
        imap.close()

if __name__ == '__main__':
    main()