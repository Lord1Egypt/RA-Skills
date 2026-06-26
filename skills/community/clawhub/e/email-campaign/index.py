"""
Email Campaign Automation for OpenClaw
PayLessTax - 4x daily, 250 emails each = 1,000/day
"""

import os
import json
import base64
import random
import time
import argparse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

class EmailCampaign:
    def __init__(self, service_account_json, user_email, alias_email, mailing_list_path):
        self.service_account = json.loads(service_account_json) if isinstance(service_account_json, str) else service_account_json
        self.user_email = user_email
        self.alias_email = alias_email
        self.mailing_list_path = mailing_list_path

        self.sent_tracking = set()
        self.bounces = set()
        self.unsubscribes = set()

        SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        credentials = service_account.Credentials.from_service_account_info(
            self.service_account, scopes=SCOPES, subject=self.user_email
        )
        self.gmail = build('gmail', 'v1', credentials=credentials)

        # Load mailing list
        df = pd.read_excel(mailing_list_path)
        self.email_col = 'email'
        self.mailing_list = df[self.email_col].dropna().tolist()

        self.signature = """---

Best regards,

The PayLessTax Team
🌐 www.paylesstax.co.za
📧 info@paylesstax.co.za
📱 +27 76 917 6267

PayLessTax — AI-Powered Tax Solutions for South Africans

---

Should you wish to no longer receive these emails, simply reply with the word UNSUBSCRIBE

---

DISCLAIMER: THE INFORMATION CONTAINED IN THIS MESSAGE AND ANY ATTACHMENTS MAY BE PRIVILEGED, CONFIDENTIAL, PROPRIETARY OR OTHERWISE PROTECTED FROM DISCLOSURE."""

    def send_batch(self, batch_size=250, tax_tip=""):
        """Send a batch of emails"""
        batch_id = datetime.now().strftime("%Y-%m-%d-%H-%M")
        results = {
            "batch_id": batch_id,
            "sent_count": 0,
            "failed": [],
            "bounces": [],
            "errors": []
        }

        to_send = [e for e in self.mailing_list if e not in self.sent_tracking][:batch_size]

        for email in to_send:
            try:
                subject = "Important Tax Updates from PayLessTax"
                body = f"""Dear Valued Client,

{tax_tip}

Don't miss critical tax deadlines. The 2026 tax season requires careful planning.

Key dates to remember:
• First provisional tax: 31 August 2026
• Second provisional tax: 28 February 2027
• Third top-up: 30 September 2027

{self.signature}"""

                message = MIMEMultipart()
                message['to'] = email
                message['from'] = f"PayLessTax <{self.alias_email}>"
                message['subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
                self.gmail.users().messages().send(userId='me', body={'raw': raw}).execute()

                self.sent_tracking.add(email)
                results["sent_count"] += 1

                # Rate limit delay
                time.sleep(0.5)

            except HttpError as e:
                if 'bounce' in str(e).lower() or 'invalid' in str(e).lower():
                    self.bounces.add(email)
                    results["bounces"].append(email)
                else:
                    results["errors"].append({"email": email, "error": str(e)})
            except Exception as e:
                results["failed"].append({"email": email, "error": str(e)})

        return results

    def scrape_bounces_and_unsubscribes(self):
        """Check inbox for bounces and unsubscribe requests"""
        try:
            # Search for bounces (delivery status notifications)
            bounces = self.gmail.users().messages().list(
                userId='me', q='subject:Delivery Status Notification (Failure) is:unread'
            ).execute()

            # Search for unsubscribe requests
            unsubscribes = self.gmail.users().messages().list(
                userId='me', q='unsubscribe OR "remove me" is:unread'
            ).execute()

            return {
                "bounces": len(bounces.get('messages', [])),
                "unsubscribes": len(unsubscribes.get('messages', []))
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--service-account', required=True, help='Path to service account JSON')
    parser.add_argument('--user-email', required=True, help='Authorized user email')
    parser.add_argument('--alias-email', default='info@paylesstax.co.za')
    parser.add_argument('--mailing-list', required=True, help='Path to Excel mailing list')
    parser.add_argument('--batch-size', type=int, default=250)
    parser.add_argument('--tax-tip', default='Stay ahead of SARS deadlines with our automated reminders.')
    parser.add_argument('--output', default='campaign_result.json')

    args = parser.parse_args()

    with open(args.service_account, 'r') as f:
        sa_json = f.read()

    campaign = EmailCampaign(sa_json, args.user_email, args.alias_email, args.mailing_list)
    result = campaign.send_batch(args.batch_size, args.tax_tip)
    bounce_info = campaign.scrape_bounces_and_unsubscribes()
    result["inbox_status"] = bounce_info

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
