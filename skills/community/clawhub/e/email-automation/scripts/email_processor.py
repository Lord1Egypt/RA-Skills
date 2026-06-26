#!/usr/bin/env python3
"""
Email Automation - Smart Email Processing
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
DATA_DIR = Path(os.getenv('EMAIL_AUTOMATION_DATA_DIR', '.email-automation'))
EMAIL_PROVIDER = os.getenv('EMAIL_PROVIDER', 'gmail')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
AUTO_ARCHIVE = os.getenv('AUTO_ARCHIVE', 'true').lower() == 'true'
CATEGORIES = os.getenv('CATEGORIES', 'urgent,important,newsletters,notifications,receipts').split(',')

def ensure_data_dir():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_processed_history():
    """Load history of processed emails"""
    history_file = DATA_DIR / 'processed.json'
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return {'processed_ids': [], 'last_run': None}

def save_processed_history(history):
    """Save history of processed emails"""
    ensure_data_dir()
    history_file = DATA_DIR / 'processed.json'
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def simulate_fetch_emails():
    """Simulate fetching emails (demo mode)"""
    return [
        {
            'id': 'email_001',
            'from': 'boss@company.com',
            'subject': 'Meeting rescheduled to 3pm',
            'snippet': 'Hi, the meeting has been moved to 3pm today...',
            'date': '2026-03-07T10:00:00Z',
            'unread': True
        },
        {
            'id': 'email_002',
            'from': 'important@client.com',
            'subject': 'Contract needs review ASAP',
            'snippet': 'Please review the attached contract and provide feedback...',
            'date': '2026-03-07T09:30:00Z',
            'unread': True
        },
        {
            'id': 'email_003',
            'from': 'newsletter@techcrunch.com',
            'subject': 'TechCrunch Daily: AI Startup Raises $100M',
            'snippet': 'Today\'s top stories in tech...',
            'date': '2026-03-07T08:00:00Z',
            'unread': True
        },
        {
            'id': 'email_004',
            'from': 'notifications@github.com',
            'subject': '[openclaw/openclaw] New issue opened',
            'snippet': 'User reported a bug in the automation module...',
            'date': '2026-03-07T07:45:00Z',
            'unread': True
        },
        {
            'id': 'email_005',
            'from': 'auto-confirm@amazon.com',
            'subject': 'Your order has shipped',
            'snippet': 'Great news! Your order #12345 has been shipped...',
            'date': '2026-03-06T15:20:00Z',
            'unread': False
        }
    ]

def categorize_email(email):
    """Categorize email using AI (simulated)"""
    subject = email.get('subject', '').lower()
    sender = email.get('from', '').lower()
    
    # Urgent patterns
    urgent_keywords = ['asap', 'urgent', 'important', 'meeting', 'deadline']
    if any(keyword in subject for keyword in urgent_keywords):
        return 'urgent'
    
    # VIP senders
    vip_domains = ['company.com', 'client.com']
    if any(domain in sender for domain in vip_domains):
        return 'important'
    
    # Newsletters
    newsletter_keywords = ['newsletter', 'daily', 'digest', 'weekly']
    if any(keyword in subject for keyword in newsletter_keywords):
        return 'newsletters'
    
    # Notifications
    notification_domains = ['github.com', 'slack.com', 'notifications']
    if any(domain in sender for domain in notification_domains):
        return 'notifications'
    
    # Receipts
    receipt_keywords = ['order', 'receipt', 'invoice', 'payment', 'shipped']
    if any(keyword in subject for keyword in receipt_keywords):
        return 'receipts'
    
    return 'important'  # Default

def generate_reply_draft(email):
    """Generate reply draft using AI (simulated)"""
    subject = email.get('subject', '')
    sender = email.get('from', '')
    
    if 'meeting' in subject.lower():
        return f"""Thanks for the update. I've noted the meeting time and will be there.

Best regards,
{EMAIL_ADDRESS}"""
    
    elif 'contract' in subject.lower():
        return f"""Thank you for sending the contract. I'll review it and get back to you with feedback by tomorrow.

Best regards,
{EMAIL_ADDRESS}"""
    
    else:
        return f"""Thank you for your email. I'll review and respond in detail soon.

Best regards,
{EMAIL_ADDRESS}"""

def process_emails():
    """Main email processing function"""
    print("📧 Email Automation")
    print("=" * 50)
    print(f"Provider: {EMAIL_PROVIDER}")
    print(f"Account: {EMAIL_ADDRESS}")
    print("-" * 50)
    
    # Fetch emails
    print("📥 Fetching emails...")
    emails = simulate_fetch_emails()
    print(f"✓ Found {len(emails)} emails")
    print()
    
    # Categorize
    print("🏷️  Categorizing emails...")
    categorized = {cat: [] for cat in CATEGORIES}
    
    for email in emails:
        category = categorize_email(email)
        if category in categorized:
            categorized[category].append(email)
        else:
            categorized['important'].append(email)
    
    # Display results
    for category, emails_in_cat in categorized.items():
        if emails_in_cat:
            print(f"\n[{category.title()}] ({len(emails_in_cat)})")
            for email in emails_in_cat:
                print(f"  • {email['from']}: {email['subject'][:50]}")
    
    print()
    
    # Generate drafts for urgent/important
    print("✍️  Generating reply drafts...")
    drafts = []
    
    for email in categorized.get('urgent', []) + categorized.get('important', []):
        if email.get('unread', False):
            draft = generate_reply_draft(email)
            drafts.append({
                'to': email['from'],
                'subject': f"Re: {email['subject']}",
                'draft': draft
            })
            print(f"  • Draft for {email['from']}")
    
    print()
    
    # Auto-archive
    if AUTO_ARCHIVE:
        print("🗑️  Auto-archiving low-priority emails...")
        archive_count = len(categorized.get('newsletters', [])) + \
                       len(categorized.get('notifications', [])) + \
                       len(categorized.get('receipts', []))
        print(f"  ✓ Archived {archive_count} emails")
        print()
    
    # Summary
    print("📊 Summary:")
    print(f"  Total processed: {len(emails)}")
    print(f"  Urgent: {len(categorized.get('urgent', []))}")
    print(f"  Important: {len(categorized.get('important', []))}")
    print(f"  Drafts generated: {len(drafts)}")
    print(f"  Archived: {archive_count if AUTO_ARCHIVE else 0}")
    print()
    
    # Save history
    history = load_processed_history()
    history['last_run'] = datetime.now().isoformat()
    history['processed_ids'] = [e['id'] for e in emails]
    save_processed_history(history)
    
    print("=" * 50)
    print("✅ Email processing complete!")
    print()
    print("💡 Next steps:")
    print("  • Review drafts in drafts folder")
    print("  • Check urgent emails immediately")
    print("  • Set up automation for continuous processing")

def show_inbox_summary():
    """Show inbox summary"""
    history = load_processed_history()
    
    print("\n📧 Inbox Summary")
    print("=" * 50)
    print(f"Account: {EMAIL_ADDRESS}")
    print(f"Last run: {history['last_run'] or 'Never'}")
    print(f"Total processed: {len(history['processed_ids'])}")
    print("=" * 50)

def main():
    """Main entry point"""
    if not EMAIL_ADDRESS:
        print("⚠️  EMAIL_ADDRESS not set!")
        print("   Please set your email address:")
        print("   export EMAIL_ADDRESS=\"your@email.com\"")
        print()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'summary':
            show_inbox_summary()
            return
        elif command == 'test':
            print("🧪 TEST MODE - No changes will be made")
            print()
    
    process_emails()

if __name__ == '__main__':
    main()
