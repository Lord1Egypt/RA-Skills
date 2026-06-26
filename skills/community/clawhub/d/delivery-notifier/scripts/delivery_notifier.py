#!/usr/bin/env python3
"""
Improved Delivery Notifier
- Filters out marketing spam (AliExpress, Temu, etc.)
- Distinguishes personal deliveries from marketing
- Tracks expected deliveries with known courier companies
- Only sends NEW delivery notifications (not duplicates)
"""
import os
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime, timedelta
import re

# Configuration from environment variables
EMAIL_USER = os.getenv("GMAIL_ADDRESS")
EMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")
IMAP_SERVER = "imap.gmail.com"
STATE_FILE = "/home/o0o/.openclaw/workspace/logs/delivery_notifier_state.json"
MAX_STATE_AGE_HOURS = 24  # Only remember deliveries for 24 hours

# Known courier companies (for tracking)
KNOWN_COURIERS = [
    "FAN Courier",
    "FAN Courier Romania",
    "Fan Courier",
    "Fan Courier Romania",
    "KROM",
    "DHL",
    "DHL Express",
    "GLS",
    "Orange Conveyors",
    "DPD",
    "Romposta",
    "Poseta",
    "DPD Romania",
    "Rompetrol Transport",
    "Speedy",
    "Transilvania Express",
    "UPC Courier",
    # Romanian couriers
    "Posta Romana",
    "Posta Română",
    "Sameday",
    "Cargus",
    "easybox",
    "FanBox",
    "Fan Box",
    # International couriers (keep these)
    "AliExpress",
    "Temu",
    "Shein",
    "Amazon",
    "Amazon Orders",
    "Amazon Shipping",
    "Shopify",
    "WooCommerce",
]

# Marketing/Spam senders to filter out (only obvious marketing, not actual delivery updates)
MARKETING_SENDERS = [
    # Keep AliExpress, Temu, etc. here because they're legitimate personal orders
    # Only filter out if they're clearly marketing spam (e.g., "Your order has been delivered - no action required")
    # The script now recognizes them as couriers, so they'll pass through
]

# Delivery keywords that indicate real deliveries
DELIVERY_KEYWORDS = [
    "delivery",
    "shipment",
    "tracking",
    "package",
    "courier",
    "delivery center",
    "out for delivery",
    "PO-",
    "at your doorstep",
    "arriving today",
    "package at",
    "shipped",
    "delivered",
]

def load_state():
    """Load previous delivery state from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)

                # Filter out old notifications (older than MAX_STATE_AGE_HOURS)
                now = datetime.now()
                state['notifications'] = [
                    n for n in state.get('notifications', [])
                    if datetime.fromisoformat(n.get('timestamp', '')) > (now - timedelta(hours=MAX_STATE_AGE_HOURS))
                ]

                return state
    except Exception as e:
        print(f"Error loading state: {e}")

    return {'notifications': []}

def save_state(state):
    """Save delivery state to file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving state: {e}")

def is_notification_duplicate(notification, state):
    """Check if a notification has already been sent"""
    notification_id = notification.get('id')
    notification_courier = notification.get('courier', '').lower()
    notification_tracking = str(notification.get('tracking') or '').lower()
    notification_summary = notification.get('summary', '').lower()

    # Check if this exact notification was already sent
    for existing in state.get('notifications', []):
        if existing.get('id') == notification_id:
            return True

        # Check if same courier with same tracking number was already sent
        if (existing.get('courier', '').lower() == notification_courier and
            str(existing.get('tracking') or '').lower() == notification_tracking):
            return True

        # Check if same courier with similar summary was already sent (to avoid duplicates)
        if existing.get('courier', '').lower() == notification_courier:
            existing_summary = existing.get('summary', '').lower()
            if notification_summary in existing_summary or existing_summary in notification_summary:
                return True

    return False

def mark_notification_sent(state, notification):
    """Mark a notification as sent"""
    # Remove old notifications if we have too many
    if len(state.get('notifications', [])) > 100:
        state['notifications'] = state['notifications'][-50:]

    # Add this notification to state
    notification['timestamp'] = datetime.now().isoformat()
    state['notifications'].append(notification)
    return state

# Filter function to check if email is a real delivery notification
def is_real_delivery(subject, body, from_email):
    """Determine if an email is a real delivery notification vs marketing spam"""
    subject_lower = subject.lower()
    body_lower = body.lower()

    # Check for marketing senders first
    from_email_lower = from_email.lower()
    for marketing_sender in MARKETING_SENDERS:
        if marketing_sender.lower() in from_email_lower:
            return False

    # Check if it's a known courier
    is_known_courier = any(courier.lower() in from_email_lower or courier.lower() in subject_lower for courier in KNOWN_COURIERS)

    # Check delivery keywords
    has_delivery_keyword = any(keyword.lower() in subject_lower or keyword.lower() in body_lower for keyword in DELIVERY_KEYWORDS)

    # Must have either known courier OR delivery keyword
    return is_known_courier or has_delivery_keyword

def extract_tracking_number(text):
    """Extract tracking number from text"""
    # Various tracking number formats
    tracking_patterns = [
        r'#PO-\d+',  # Fan Courier style
        r'Tracking:\s*(\D*\d+\D*)',
        r'Tracking:\s*(\S+)',
        r'Order:\s*(\S+)',
        r'Tracking No:\s*(\S+)',
        r'(\d{20,})',  # Long numeric tracking numbers
    ]

    for pattern in tracking_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Return first match that looks like a tracking number
            for match in matches:
                if len(match) > 5:  # Minimum length check
                    return match.strip()

    return None

def get_courier_info(from_email, subject):
    """Determine which courier is shipping based on email"""
    from_email_lower = from_email.lower()
    subject_lower = subject.lower()

    for courier in KNOWN_COURIERS:
        if courier.lower() in from_email_lower:
            return courier

        # Check if courier name appears in subject
        if courier.lower() in subject_lower:
            return courier

    return "Unknown Courier"

def fetch_delivery_notifications():
    """Fetch delivery notifications from Gmail"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search for emails containing delivery notifications
        # More specific search criteria
        status, messages = mail.search(None, 'SUBJECT "Delivery"')
        if status != "OK":
            print(json.dumps({"error": "Search failed"}))
            return []

        email_ids = messages[0].split()
        results = []

        for e_id in email_ids[-20:]:  # Check last 20 emails
            try:
                e_id_str = e_id.decode('utf-8') if isinstance(e_id, bytes) else str(e_id)
                _, msg_data = mail.fetch(e_id, "(RFC822)")

                if isinstance(msg_data, list):
                    for response_part in msg_data:
                        if isinstance(response_part, tuple) and len(response_part) > 1:
                            msg = email.message_from_bytes(response_part[1])
                            subject_parts = decode_header(msg.get("Subject", ""))
                            subject = "".join([
                                part.decode(encoding if encoding else 'utf-8', errors='replace') if isinstance(part, bytes) else str(part)
                                for part, encoding in subject_parts
                            ])
                            from_ = str(msg.get("From", ""))
                            body = msg.get_payload(decode=True).decode(errors='replace') if msg.get_payload(decode=True) else ""

                            # Check if it's a real delivery notification
                            if is_real_delivery(subject, body, from_):
                                tracking = extract_tracking_number(subject + " " + body)

                                results.append({
                                    "id": e_id_str,
                                    "from": from_,
                                    "subject": subject,
                                    "body": body,
                                    "tracking": tracking,
                                    "courier": get_courier_info(from_, subject),
                                    "timestamp": datetime.now().isoformat()
                                })
            except Exception as e:
                print(f"Error processing email {e_id}: {e}")
                continue

        mail.close()
        mail.logout()
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

def send_whatsapp_notification(notification):
    """Send a formatted WhatsApp notification"""
    try:
        # Build notification message
        courier = notification.get('courier', 'Unknown')
        tracking = notification.get('tracking', 'N/A')
        subject = notification.get('subject', 'Delivery notification')

        # Format the message
        message = f"""📦 *LIVRARE NOUĂ*

🏢 *Curier:* {courier}
📋 *Trimitere:* {tracking}
📄 *Mesaj:* {subject}

---
*Generat automat de OpenClaw Delivery Notifier*
"""

        # Send via WhatsApp message tool
        import openclaw
        openclaw.message.send(
            target='+40746085791',
            channel='whatsapp',
            message=message
        )

        return True
    except Exception as e:
        print(f"Error sending WhatsApp notification: {e}")
        return False

def main():
    """Main function"""
    print(f"Fetching delivery notifications at {datetime.now()}...")

    # Load previous state
    state = load_state()
    print(f"Loaded state with {len(state.get('notifications', []))} previous notifications")

    notifications = fetch_delivery_notifications()

    if not notifications:
        print("No delivery notifications found")
        return

    print(f"Found {len(notifications)} delivery notifications")

    # Check for duplicates and filter
    new_notifications = []
    duplicate_count = 0

    for notification in notifications:
        if not is_notification_duplicate(notification, state):
            new_notifications.append(notification)
        else:
            duplicate_count += 1
            print(f"Skipping duplicate: {notification.get('courier', 'Unknown')} - {notification.get('tracking', 'N/A')}")

    print(f"Duplicates found: {duplicate_count}")

    if not new_notifications:
        print("No new deliveries, retrying in one hour.")
        return

    # Send new notifications
    for notification in new_notifications:
        print(f"Sending notification for: {notification.get('courier', 'Unknown')} - {notification.get('tracking', 'N/A')}")
        send_whatsapp_notification(notification)

        # Mark as sent in state
        state = mark_notification_sent(state, notification)

    # Save state
    save_state(state)

    # Print brief summary
    print(f"\n{datetime.now()} - {len(new_notifications)} new delivery notification(s) sent")

if __name__ == '__main__':
    main()