#!/usr/bin/env python3
import os
import imaplib
import email
from email.header import decode_header
import json

# Configuration from environment variables
EMAIL_USER = os.getenv("GMAIL_ADDRESS")
EMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")
IMAP_SERVER = "imap.gmail.com"

# Fetch delivery notifications from Gmail

def fetch_delivery_notifications():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search for emails containing delivery notifications
        status, messages = mail.search(None, 'SUBJECT "Delivery"')
        if status != "OK":
            print(json.dumps({"error": "Search failed"}))
            return

        email_ids = messages[0].split()
        results = []
        for e_id in email_ids[-5:]:  # Get the last 5 emails
            try:
                _, msg_data = mail.fetch(e_id, "(RFC822)")
                print(f"Fetch response for email {e_id}: {msg_data}")

                for response_part in msg_data:
                    print(f"Response part type: {type(response_part)}, value: {response_part}")
                    if isinstance(response_part, tuple) and len(response_part) > 1:
                        print(f"Response part[1] type: {type(response_part[1])}")
                        if response_part[1] is not None:
                            msg = email.message_from_bytes(response_part[1])
                            subject_parts = decode_header(msg["Subject"])
                            subject = "".join([part.decode(encoding if encoding else 'utf-8', errors='replace') if isinstance(part, bytes) else str(part) for part, encoding in subject_parts])
                            from_ = str(msg.get("From"))
                            body = msg.get_payload(decode=True).decode(errors='replace')
                            results.append({"id": e_id.decode() if isinstance(e_id, bytes) else str(e_id), "from": from_, "subject": subject, "body": body})
                    else:
                        print("Skipping response_part - not a tuple with >1 elements")

            except Exception as e:
                print(f"Error processing email {e_id}: {e}")
                import traceback
                traceback.print_exc()
                continue

        mail.close()
        mail.logout()
        return results
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    notifications = fetch_delivery_notifications()
    print(json.dumps(notifications, indent=2))