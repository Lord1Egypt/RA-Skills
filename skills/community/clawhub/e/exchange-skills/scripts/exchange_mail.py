#!/usr/bin/env python3
"""
Exchange Mail CLI - Full email management for Microsoft Exchange/Outlook.

A Claude Code skill for managing Exchange emails and calendar from the terminal.

Commands:
  list      - List unread emails (default)
  read      - Read full email by ID
  reply     - Reply to email
  mark-read - Mark email(s) as read
  archive   - Archive email(s)
  calendar  - List calendar events

Usage:
  python3 exchange_mail.py list [--days N] [--all]
  python3 exchange_mail.py read <email_id>
  python3 exchange_mail.py reply <email_id> "<message>"
  python3 exchange_mail.py mark-read <email_id|--external|--internal|--all>
  python3 exchange_mail.py archive <email_id|--external|--internal|--all>
  python3 exchange_mail.py calendar [--days N] [--today]

Environment Variables:
  EXCHANGE_SERVER   - Exchange server hostname (required)
  EXCHANGE_EMAIL    - Your email address (required)
  EXCHANGE_USERNAME - Your username (required)
  EXCHANGE_PASSWORD - Your password (required)
  EXCHANGE_DOMAIN   - Windows domain (optional)

Author: DmitryBMsk (https://github.com/DmitryBMsk)
License: MIT
"""
import os
import sys
import argparse
import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

# SSL verification is enabled by default for security
# If you need to disable SSL verification for corporate certificates,
# set EXCHANGE_DISABLE_SSL_VERIFY=1 environment variable
if os.environ.get('EXCHANGE_DISABLE_SSL_VERIFY') == '1':
    import urllib3
    urllib3.disable_warnings()

# Load .env file from script directory
def load_env_file():
    """Load environment variables from .env file in script directory."""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env_file()

# Global connection cache
_account = None
_emails_cache = {}


def get_account():
    """Get or create Exchange account connection."""
    global _account
    if _account:
        return _account

    try:
        from exchangelib import Credentials, Account, Configuration, DELEGATE
        from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
    except ImportError:
        print("Error: exchangelib not installed.", file=sys.stderr)
        print("Run: pip install exchangelib", file=sys.stderr)
        sys.exit(1)

    # SSL verification is enabled by default for security
    # Only disable if explicitly requested via environment variable
    if os.environ.get('EXCHANGE_DISABLE_SSL_VERIFY') == '1':
        BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

    # Get credentials from environment
    server = os.environ.get('EXCHANGE_SERVER')
    email = os.environ.get('EXCHANGE_EMAIL')
    username = os.environ.get('EXCHANGE_USERNAME')
    password = os.environ.get('EXCHANGE_PASSWORD')
    domain = os.environ.get('EXCHANGE_DOMAIN')

    # Validate required environment variables
    missing = []
    if not server:
        missing.append('EXCHANGE_SERVER')
    if not email:
        missing.append('EXCHANGE_EMAIL')
    if not username:
        missing.append('EXCHANGE_USERNAME')
    if not password:
        missing.append('EXCHANGE_PASSWORD')

    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        print("\nRequired environment variables:", file=sys.stderr)
        print("  EXCHANGE_SERVER   - Exchange server hostname", file=sys.stderr)
        print("  EXCHANGE_EMAIL    - Your email address", file=sys.stderr)
        print("  EXCHANGE_USERNAME - Your username", file=sys.stderr)
        print("  EXCHANGE_PASSWORD - Your password", file=sys.stderr)
        sys.exit(1)

    # Build credentials
    if domain:
        username = f"{domain}\\{username}"

    credentials = Credentials(username=username, password=password)
    config = Configuration(server=server, credentials=credentials)

    try:
        _account = Account(
            primary_smtp_address=email,
            config=config,
            autodiscover=False,
            access_type=DELEGATE
        )
    except Exception as e:
        print(f"Error connecting to Exchange: {e}", file=sys.stderr)
        sys.exit(1)

    return _account


def get_internal_domain() -> str:
    """Get internal domain from email address."""
    email = os.environ.get('EXCHANGE_EMAIL', '')
    if '@' in email:
        return '@' + email.split('@')[1].lower()
    return ''


def generate_email_id(item) -> str:
    """Generate stable 8-character ID from email."""
    id_source = (item.message_id or item.id or str(item.datetime_received))
    return hashlib.md5(id_source.encode()).hexdigest()[:8]


def get_emails(days_back: int = 0, show_all: bool = False, include_read: bool = False) -> List[Dict[str, Any]]:
    """Fetch emails from Exchange."""
    global _emails_cache

    account = get_account()
    user_email = account.primary_smtp_address.lower()
    internal_domain = get_internal_domain()

    # Calculate date filter
    if days_back > 0:
        start_date = datetime.now(timezone.utc) - timedelta(days=days_back)
    else:
        start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    emails = []

    # Build filter - include read emails only if requested
    if include_read:
        email_filter = {'datetime_received__gte': start_date}
    else:
        email_filter = {'is_read': False, 'datetime_received__gte': start_date}

    for item in account.inbox.filter(
        **email_filter
    ).order_by('-datetime_received')[:50]:

        # Get recipients
        to_list = [r.email_address.lower() for r in (item.to_recipients or []) if r.email_address]
        cc_list = [r.email_address.lower() for r in (item.cc_recipients or []) if r.email_address]
        is_direct = user_email in to_list + cc_list

        # Skip if not direct recipient (unless --all flag)
        if not show_all and not is_direct:
            continue

        sender = item.sender.email_address if item.sender else 'Unknown'
        sender_name = item.sender.name if item.sender and item.sender.name else sender
        is_internal = sender.lower().endswith(internal_domain) if sender and internal_domain else False

        email_id = generate_email_id(item)

        email_data = {
            'id': email_id,
            'item_id': item.id,
            'message_id': item.message_id,
            'time': item.datetime_received.strftime('%H:%M') if item.datetime_received else '??:??',
            'date': item.datetime_received.strftime('%Y-%m-%d') if item.datetime_received else '',
            'sender': sender,
            'sender_name': sender_name,
            'subject': item.subject or '(No subject)',
            'preview': (item.text_body or '')[:150].replace('\n', ' ').strip(),
            'is_internal': is_internal,
            'is_direct': is_direct,
            'to': to_list[:5],
            'cc': cc_list[:5],
        }

        emails.append(email_data)
        _emails_cache[email_id] = item

    return emails


def find_email_by_id(email_id: str):
    """Find email item by short ID."""
    global _emails_cache

    if email_id in _emails_cache:
        return _emails_cache[email_id]

    # Search in recent emails
    account = get_account()
    start_date = datetime.now(timezone.utc) - timedelta(days=7)

    for item in account.inbox.filter(
        datetime_received__gte=start_date
    ).order_by('-datetime_received')[:100]:
        item_id = generate_email_id(item)
        _emails_cache[item_id] = item
        if item_id == email_id:
            return item

    return None


def cmd_list(args):
    """List emails."""
    emails = get_emails(days_back=args.days, show_all=args.all, include_read=args.include_read)

    if args.json:
        print(json.dumps(emails, ensure_ascii=False, indent=2))
        return

    if not emails:
        period = f"from last {args.days} days" if args.days > 0 else "today"
        print(f"📭 No emails {period}")
        return

    internal = [e for e in emails if e['is_internal']]
    external = [e for e in emails if not e['is_internal']]

    period = f"from last {args.days} days" if args.days > 0 else "today"
    status = "all emails" if args.include_read else "unread emails"
    print(f"📧 {len(emails)} {status} {period}:")
    print()

    if internal:
        print(f"━━━ Internal ({len(internal)}) ━━━")
        for e in internal:
            print(f"[{e['id']}] [{e['time']}] {e['sender_name']}")
            print(f"        {e['subject']}")
            if e['preview']:
                print(f"        {e['preview'][:60]}...")
            print()

    if external:
        print(f"━━━ External ({len(external)}) ━━━")
        for e in external[:10]:
            print(f"[{e['id']}] [{e['time']}] {e['sender']}")
            print(f"        {e['subject']}")
            print()
        if len(external) > 10:
            print(f"        ... and {len(external) - 10} more")

    print("─" * 50)
    print("Commands: read <id>, reply <id> \"text\", mark-read <id>, archive <id>")


def cmd_read(args):
    """Read full email content."""
    item = find_email_by_id(args.email_id)

    if not item:
        print(f"❌ Email with ID {args.email_id} not found")
        return

    sender = item.sender.email_address if item.sender else 'Unknown'
    sender_name = item.sender.name if item.sender and item.sender.name else sender

    print("=" * 60)
    print(f"📧 {item.subject or '(No subject)'}")
    print("=" * 60)
    print(f"From:  {sender_name} <{sender}>")
    print(f"Date:  {item.datetime_received.strftime('%Y-%m-%d %H:%M') if item.datetime_received else 'Unknown'}")

    to_list = [r.email_address for r in (item.to_recipients or []) if r.email_address]
    if to_list:
        print(f"To:    {', '.join(to_list[:5])}")

    cc_list = [r.email_address for r in (item.cc_recipients or []) if r.email_address]
    if cc_list:
        print(f"CC:    {', '.join(cc_list[:5])}")

    print("-" * 60)

    body = item.text_body or item.body or ''
    if hasattr(body, 'text'):
        body = body.text or ''

    body = body.strip()
    if len(body) > 3000:
        body = body[:3000] + "\n\n... [truncated, email too long]"

    print(body if body else "(Empty email)")
    print("=" * 60)
    print(f"\nID for reply: {args.email_id}")
    print(f"Commands: reply {args.email_id} \"text\", mark-read {args.email_id}, archive {args.email_id}")


def cmd_reply(args):
    """Reply to email."""
    item = find_email_by_id(args.email_id)

    if not item:
        print(f"❌ Email with ID {args.email_id} not found")
        return

    reply_body = args.message

    # Add original message quote
    original_sender = item.sender.email_address if item.sender else 'Unknown'
    original_date = item.datetime_received.strftime('%Y-%m-%d %H:%M') if item.datetime_received else ''
    original_body = (item.text_body or '')[:500]

    full_body = f"""{reply_body}

---
{original_date}, {original_sender} wrote:
> {original_body.replace(chr(10), chr(10) + '> ')}
"""

    try:
        subject = item.subject or ''
        if not subject.lower().startswith('re:'):
            subject = f"Re: {subject}"

        item.reply(
            subject=subject,
            body=full_body,
            to_recipients=[item.sender] if item.sender else None
        )
        print(f"✅ Reply sent to {original_sender}")
        print(f"   Subject: {subject}")
    except Exception as e:
        print(f"❌ Send error: {e}")


def cmd_mark_read(args):
    """Mark email(s) as read."""
    batch_mode = args.external or args.internal or args.all_emails

    if batch_mode:
        emails = get_emails(days_back=args.days, show_all=True)

        if args.external:
            emails = [e for e in emails if not e['is_internal']]
            mode_name = "external"
        elif args.internal:
            emails = [e for e in emails if e['is_internal']]
            mode_name = "internal"
        else:
            mode_name = "all"

        if not emails:
            print(f"📭 No {mode_name} emails to process")
            return

        count = 0
        for e in emails:
            item = find_email_by_id(e['id'])
            if item:
                item.is_read = True
                item.save(update_fields=['is_read'])
                count += 1

        print(f"✅ Marked as read: {count} {mode_name} emails")
    elif args.target:
        item = find_email_by_id(args.target)
        if not item:
            print(f"❌ Email with ID {args.target} not found")
            return

        item.is_read = True
        item.save(update_fields=['is_read'])
        print(f"✅ Email {args.target} marked as read")
    else:
        print("❌ Specify email ID or flag --external/--internal/--all")


def cmd_archive(args):
    """Archive email(s) - move to Archive folder."""
    account = get_account()

    # Find archive folder
    from exchangelib import Folder

    archive_folder = None
    for folder in account.root.walk():
        if folder.name.lower() in ['archive', 'архив', 'deleted items', 'удаленные']:
            archive_folder = folder
            break

    if not archive_folder:
        try:
            archive_folder = account.trash
        except:
            archive_folder = Folder(parent=account.inbox.parent, name='Archive')
            archive_folder.save()
            print("📁 Created Archive folder")

    batch_mode = args.external or args.internal or args.all_emails

    if batch_mode:
        emails = get_emails(days_back=args.days, show_all=True)

        if args.external:
            emails = [e for e in emails if not e['is_internal']]
            mode_name = "external"
        elif args.internal:
            emails = [e for e in emails if e['is_internal']]
            mode_name = "internal"
        else:
            mode_name = "all"

        if not emails:
            print(f"📭 No {mode_name} emails to archive")
            return

        count = 0
        errors = 0
        for e in emails:
            item = find_email_by_id(e['id'])
            if item:
                try:
                    item.move(archive_folder)
                    count += 1
                except Exception:
                    errors += 1

        result = f"✅ Archived: {count} {mode_name} emails"
        if errors:
            result += f" (errors: {errors})"
        print(result)
    elif args.target:
        item = find_email_by_id(args.target)
        if not item:
            print(f"❌ Email with ID {args.target} not found")
            return

        try:
            item.move(archive_folder)
            print(f"✅ Email {args.target} archived")
        except Exception as e:
            print(f"❌ Archive error: {e}")
    else:
        print("❌ Specify email ID or flag --external/--internal/--all")


# ========== Calendar Functions ==========

def get_calendar_events(days_back: int = 0, days_forward: int = 7) -> List[Dict[str, Any]]:
    """Fetch calendar events from Exchange.
    
    Args:
        days_back: Number of days to look back from today (0 = today start)
        days_forward: Number of days to look forward from today
    """
    account = get_account()

    # Calculate date range
    now = datetime.now(timezone.utc)
    
    # Handle both past and future dates
    if days_back > 0:
        start_date = now - timedelta(days=days_back)
    else:
        # Default: start from today at midnight
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # end_date is always in the future (or today)
    end_date = now + timedelta(days=days_forward)

    events = []

    # Access calendar folder
    try:
        calendar = account.calendar
    except Exception as e:
        print(f"❌ Error accessing calendar: {e}")
        return []

    # Query calendar items
    try:
        from exchangelib import EWSTimeZone
        
        # Try to filter calendar items
        query = calendar.filter(
            start__gte=start_date,
            end__lte=end_date
        ).order_by('start')

        tz = EWSTimeZone.localzone()
        
        for item in query[:50]:
            # Convert times to local
            start_local = item.start
            end_local = item.end
            
            # Handle timezone-aware vs naive datetimes
            if hasattr(start_local, 'astimezone'):
                start_local = start_local.astimezone(tz)
                end_local = end_local.astimezone(tz)
            
            event_data = {
                'id': str(item.id)[:8],
                'subject': item.subject or '(No subject)',
                'start': start_local.strftime('%Y-%m-%d %H:%M') if start_local else '',
                'end': end_local.strftime('%Y-%m-%d %H:%M') if end_local else '',
                'start_time': start_local.strftime('%H:%M') if start_local else '',
                'end_time': end_local.strftime('%H:%M') if end_local else '',
                'date': start_local.strftime('%Y-%m-%d') if start_local else '',
                'location': item.location or '',
                'organizer': item.organizer.name if item.organizer else '',
                'is_all_day': item.is_all_day if hasattr(item, 'is_all_day') else False,
                'busy_status': item.show_as if hasattr(item, 'show_as') else '',
            }
            events.append(event_data)
            
    except Exception as e:
        print(f"❌ Error fetching calendar: {e}")
        return []

    return events


def cmd_calendar(args):
    """List calendar events."""
    # Determine date range
    if args.today:
        events = get_calendar_events(days_back=0, days_forward=1)
    elif args.days_back > 0:
        # Looking back in time
        events = get_calendar_events(days_back=args.days_back, days_forward=args.days)
    else:
        # Default: today + upcoming
        events = get_calendar_events(days_back=0, days_forward=args.days)

    if args.json:
        print(json.dumps(events, ensure_ascii=False, indent=2))
        return

    if not events:
        print("📅 No calendar events found")
        return

    # Group events by date
    from collections import defaultdict
    events_by_date = defaultdict(list)
    for e in events:
        events_by_date[e['date']].append(e)

    print(f"📅 {len(events)} calendar events:")
    print()

    for date in sorted(events_by_date.keys()):
        day_events = events_by_date[date]
        print(f"━━━ {date} ({len(day_events)} events) ━━━")
        
        for e in day_events:
            time_str = f"{e['start_time']} - {e['end_time']}"
            if e['is_all_day']:
                time_str = "全天"
            
            print(f"  [{time_str}] {e['subject']}")
            if e['location']:
                print(f"           📍 {e['location']}")
        print()

    print("─" * 50)
    print("Commands: calendar --days N, calendar --today")


# ========== Contacts Functions ==========

def search_contacts(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Search contacts from Exchange.
    
    Supported query fields:
    - display_name (顯示名稱)
    - given_name (名字)
    - surname (姓氏)
    - company_name (公司名稱)
    - email_alias (郵件別名)
    - email_addresses (郵件地址)
    
    Supported operators:
    - __contains: 包含關鍵字
    - __startswith: 開頭符合
    - __exact: 完全匹配
    - __icontains: 不區分大小寫
    """
    account = get_account()
    
    contacts = []
    
    try:
        # Try different contact sources
        contact_sources = []
        
        # Try account.contacts first
        try:
            contact_sources.append(('Contacts', account.contacts))
        except AttributeError:
            pass
        
        # Walk through folders to find contact folders
        for folder in account.root.walk():
            folder_name_lower = folder.name.lower()
            # Include all contact-related folders including Recipient Cache (GAL)
            if 'contact' in folder_name_lower or 'gal' in folder_name_lower or folder.name == 'Recipient Cache':
                contact_sources.append((folder.name, folder))
        
        if not contact_sources:
            print("❌ No contact folders found")
            return []
        
        # Try each contact source
        from exchangelib import Q
        
        for source_name, folder in contact_sources:
            try:
                # For some folders like Recipient Cache, we need to fetch all and filter in memory
                # Try Q filter first
                try:
                    q = (
                        Q(display_name__icontains=query) | 
                        Q(given_name__icontains=query) |
                        Q(surname__icontains=query) |
                        Q(company_name__icontains=query) |
                        Q(email_alias__icontains=query)
                    )
                    
                    items = list(folder.filter(q)[:limit])
                except:
                    # If filter fails, get all and filter in memory
                    items = []
                    for item in folder.all()[:100]:  # Limit to 100 for performance
                        item_name = getattr(item, 'display_name', '') or ''
                        item_email = ''
                        if hasattr(item, 'email_addresses') and item.email_addresses:
                            item_email = str(item.email_addresses[0]) if item.email_addresses else ''
                        
                        # Case-insensitive search
                        if query.lower() in item_name.lower() or query.lower() in item_email.lower():
                            items.append(item)
                            if len(items) >= limit:
                                break
                
                for item in items[:limit]:
                    contact_data = {
                        'id': str(item.id)[:8],
                        'name': getattr(item, 'display_name', '') or '',
                        'first_name': getattr(item, 'given_name', '') or '',
                        'last_name': getattr(item, 'surname', '') or '',
                        'email': '',
                        'phone': '',
                        'company': getattr(item, 'company_name', '') or '',
                        'department': getattr(item, 'department', '') or '',
                        'title': getattr(item, 'job_title', '') or '',
                        'office': getattr(item, 'office_location', '') or '',
                    }
                    
                    # Get email addresses
                    if hasattr(item, 'email_addresses') and item.email_addresses:
                        emails = [str(e) for e in item.email_addresses]
                        contact_data['email'] = emails[0] if emails else ''
                    
                    # Get phone numbers
                    if hasattr(item, 'phone_numbers') and item.phone_numbers:
                        phones = [f"{k}: {v}" for k, v in item.phone_numbers.items()]
                        contact_data['phone'] = ', '.join(phones)
                    
                    contacts.append(contact_data)
                    
                if contacts:
                    break  # Found some contacts
                    
            except Exception as e:
                continue  # Try next source
        
        # If still no contacts, try people_connect (if available)
        if not contacts and hasattr(account, 'people_connect'):
            try:
                for person in account.people_connect.filter(
                    display_name__icontains=query
                )[:limit]:
                    contact_data = {
                        'id': str(person.id)[:8],
                        'name': getattr(person, 'display_name', '') or '',
                        'first_name': '',
                        'last_name': "",
                        'email': '',
                        'phone': '',
                        'company': '',
                        'department': '',
                        'title': '',
                        'office': '',
                    }
                    contacts.append(contact_data)
            except Exception:
                pass
                
    except Exception as e:
        print(f"❌ Error searching contacts: {e}")
        return []
    
    return contacts


def cmd_contacts(args):
    """Search contacts."""
    if not args.query:
        print("❌ Please specify a search query")
        print("   Usage: contacts <name>")
        return
    
    contacts = search_contacts(args.query, limit=args.limit)
    
    if args.json:
        print(json.dumps(contacts, ensure_ascii=False, indent=2))
        return
    
    if not contacts:
        print(f"🔍 No contacts found matching '{args.query}'")
        return
    
    print(f"👤 {len(contacts)} contacts found:")
    print()
    
    for c in contacts:
        print(f"━━━ {c['name']} ━━━")
        if c['email']:
            print(f"   📧 {c['email']}")
        if c['phone']:
            print(f"   📞 {c['phone']}")
        if c['company']:
            print(f"   🏢 {c['company']}")
        if c['title']:
            print(f"   💼 {c['title']}")
        if c['office']:
            print(f"   📍 {c['office']}")
        print()


# ========== Tasks Functions ==========

def get_tasks(days_back: int = 0, days_forward: int = 30, status_filter: str = None) -> List[Dict[str, Any]]:
    """Fetch tasks from Exchange."""
    account = get_account()
    
    tasks = []
    
    try:
        # Find tasks folder (工作)
        task_folder = None
        for folder in account.root.walk():
            if folder.name == '工作' or 'task' in folder.name.lower():
                task_folder = folder
                break
        
        if not task_folder:
            try:
                task_folder = account.tasks
            except AttributeError:
                print("⚠️ No Tasks folder found")
                return []
        
        # Get all tasks without filtering - just use all() with limit
        try:
            all_items = list(task_folder.all()[:50])
        except Exception as e:
            # If all() doesn't work, try empty filter
            all_items = []
            try:
                from exchangelib import Q
                all_items = list(task_folder.filter(Q(is_read=True))[:50])
            except:
                pass
        
        from datetime import timedelta
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=days_back)
        
        for item in all_items:
            task_data = {
                'id': str(item.id)[:8],
                'subject': item.subject or '',
                'status': getattr(item, 'status', '') or '',
                'priority': getattr(item, 'importance', 'Normal') or 'Normal',
                'start_date': getattr(item, 'start_date', None),
                'due_date': getattr(item, 'due_date', None),
                'percent_complete': getattr(item, 'percent_complete', 0) or 0,
                'is_complete': getattr(item, 'is_complete', False),
                'body': (getattr(item, 'body', '') or '')[:100],
            }
            
            # Filter by status if requested
            if status_filter:
                if status_filter == 'completed' and not task_data['is_complete']:
                    continue
                if status_filter == 'pending' and task_data['is_complete']:
                    continue
            
            tasks.append(task_data)
            
    except Exception as e:
        print(f"❌ Error fetching tasks: {e}")
        return []
    
    return tasks


def cmd_tasks(args):
    """List tasks."""
    tasks = get_tasks(
        days_back=args.days_back,
        days_forward=args.days,
        status_filter=args.status
    )
    
    if args.json:
        print(json.dumps(tasks, ensure_ascii=False, indent=2, default=str))
        return
    
    if not tasks:
        print("📋 No tasks found (or Tasks folder is empty)")
        return
    
    print(f"📋 {len(tasks)} tasks:")
    print()
    
    for t in tasks:
        status_icon = "✅" if t['is_complete'] else "⬜"
        due_str = t['due_date'].strftime('%Y-%m-%d') if t['due_date'] else 'No due date'
        
        print(f"{status_icon} {t['subject']}")
        print(f"   📅 Due: {due_str}")
        print(f"   📊 Status: {t['status']} ({t['percent_complete']}%)")
        print()

    print("─" * 50)
    print("Commands: tasks --days N, tasks --status completed/pending")


# ========== Notes Functions ==========

def get_notes(limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch notes from Exchange."""
    account = get_account()
    
    notes = []
    
    try:
        # Find notes folders (記事, Notes)
        note_folders = []
        for folder in account.root.walk():
            if 'note' in folder.name.lower() or 'sticky' in folder.name.lower() or folder.name == '記事':
                note_folders.append(folder)
        
        # Also check Inbox for test notes
        for folder in account.root.walk():
            if folder.name == '收件匣':
                note_folders.append(folder)
        
        if not note_folders:
            print("⚠️ No Notes folder found")
            return []
        
        for folder in note_folders:
            try:
                all_items = list(folder.all()[:limit * 2])  # Get more items
                
                for item in all_items:
                    # Check if it's a note or test note
                    subject = getattr(item, 'subject', '') or ''
                    item_class = getattr(item, 'item_class', '') or ''
                    
                    # Include if it's in Notes folder or has "note" related subject
                    is_note = folder.name in ['記事', 'Notes'] or 'note' in folder.name.lower()
                    is_test_note = '筆記' in subject or 'note' in subject.lower() or 'Note' in subject
                    
                    if is_note or is_test_note:
                        note_data = {
                            'id': str(item.id)[:8],
                            'subject': subject,
                            'body': (getattr(item, 'body', '') or getattr(item, 'text_body', '') or '')[:200],
                            'folder': folder.name,
                            'last_modified': getattr(item, 'last_modified_time', None),
                        }
                        notes.append(note_data)
                        if len(notes) >= limit:
                            break
                            
            except Exception:
                continue
            
            if notes:
                break
    
    except Exception as e:
        print(f"❌ Error fetching notes: {e}")
        return []
    
    return notes


def cmd_notes(args):
    """List notes."""
    notes = get_notes(limit=args.limit)
    
    if args.json:
        print(json.dumps(notes, ensure_ascii=False, indent=2, default=str))
        return
    
    if not notes:
        print("📝 No notes found (or Notes folder is empty)")
        return
    
    print(f"📝 {len(notes)} notes:")
    print()
    
    for n in notes:
        print(f"━━━ {n['subject'] or '(No subject)'} ━━━")
        if n['body']:
            print(f"   {n['body'][:100]}...")
        print(f"   📁 {n['folder']}")
        print()

    print("─" * 50)
    print("Commands: notes")


def main():
    parser = argparse.ArgumentParser(
        description='Exchange Mail CLI - Manage Exchange emails from terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                      # Today's unread emails
  %(prog)s list --days 3             # Last 3 days
  %(prog)s read abc123               # Read email
  %(prog)s reply abc123 "Thanks!"    # Reply to email
  %(prog)s mark-read abc123          # Mark as read
  %(prog)s mark-read --external      # All external as read
  %(prog)s archive --external        # Archive all external
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # list command
    list_parser = subparsers.add_parser('list', help='List unread emails')
    list_parser.add_argument('--days', type=int, default=0, help='Days back (0=today)')
    list_parser.add_argument('--all', action='store_true', help='All emails (not just To/CC)')
    list_parser.add_argument('--include-read', action='store_true', help='Include read emails')
    list_parser.add_argument('--json', action='store_true', help='JSON output')

    # read command
    read_parser = subparsers.add_parser('read', help='Read email')
    read_parser.add_argument('email_id', help='Email ID')

    # reply command
    reply_parser = subparsers.add_parser('reply', help='Reply to email')
    reply_parser.add_argument('email_id', help='Email ID')
    reply_parser.add_argument('message', help='Reply message')

    # mark-read command
    markread_parser = subparsers.add_parser('mark-read', help='Mark as read')
    markread_parser.add_argument('target', nargs='?', default=None, help='Email ID')
    markread_parser.add_argument('--external', action='store_true', help='All external')
    markread_parser.add_argument('--internal', action='store_true', help='All internal')
    markread_parser.add_argument('--all', action='store_true', dest='all_emails', help='All emails')
    markread_parser.add_argument('--days', type=int, default=0, help='Days back for batch')

    # archive command
    archive_parser = subparsers.add_parser('archive', help='Archive emails')
    archive_parser.add_argument('target', nargs='?', default=None, help='Email ID')
    archive_parser.add_argument('--external', action='store_true', help='All external')
    archive_parser.add_argument('--internal', action='store_true', help='All internal')
    archive_parser.add_argument('--all', action='store_true', dest='all_emails', help='All emails')
    archive_parser.add_argument('--days', type=int, default=0, help='Days back for batch')

    # calendar command
    calendar_parser = subparsers.add_parser('calendar', help='List calendar events')
    calendar_parser.add_argument('--days', type=int, default=7, help='Days forward (default: 7)')
    calendar_parser.add_argument('--days-back', type=int, default=0, help='Days to look back (e.g., 1=yesterday, 7=last week)')
    calendar_parser.add_argument('--today', action='store_true', help='Show only today')
    calendar_parser.add_argument('--json', action='store_true', help='JSON output')

    # contacts command
    contacts_parser = subparsers.add_parser('contacts', help='Search contacts')
    contacts_parser.add_argument('query', nargs='?', default='', help='Search query (name or email)')
    contacts_parser.add_argument('--limit', type=int, default=20, help='Max results (default: 20)')
    contacts_parser.add_argument('--json', action='store_true', help='JSON output')

    # tasks command
    tasks_parser = subparsers.add_parser('tasks', help='List tasks')
    tasks_parser.add_argument('--days', type=int, default=30, help='Days forward (default: 30)')
    tasks_parser.add_argument('--days-back', type=int, default=0, help='Days to look back')
    tasks_parser.add_argument('--status', type=str, choices=['pending', 'completed', 'all'], help='Filter by status')
    tasks_parser.add_argument('--json', action='store_true', help='JSON output')

    # notes command
    notes_parser = subparsers.add_parser('notes', help='List notes')
    notes_parser.add_argument('--limit', type=int, default=20, help='Max results (default: 20)')
    notes_parser.add_argument('--json', action='store_true', help='JSON output')

    args = parser.parse_args()

    if not args.command or args.command == 'list':
        if not hasattr(args, 'days'):
            args.days = 0
            args.all = False
            args.json = False
            args.include_read = False
        cmd_list(args)
    elif args.command == 'read':
        cmd_read(args)
    elif args.command == 'reply':
        cmd_reply(args)
    elif args.command == 'mark-read':
        cmd_mark_read(args)
    elif args.command == 'archive':
        cmd_archive(args)
    elif args.command == 'calendar':
        cmd_calendar(args)
    elif args.command == 'contacts':
        cmd_contacts(args)
    elif args.command == 'tasks':
        cmd_tasks(args)
    elif args.command == 'notes':
        cmd_notes(args)


if __name__ == '__main__':
    main()
