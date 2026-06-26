"""
Example usage of 163email Skill

Note: Modify the configuration in src/send_email.py before running.
"""

from src.send_email import send_mail

# Send a single email
send_mail(
    to="recipient@example.com",
    subject="Test Email from 163email Skill",
    content="This is a test email sent using the 163email skill for ClawHub."
)

# Send to multiple recipients
send_mail(
    to="user1@example.com, user2@example.com",
    subject="Notification",
    content="This email is sent to multiple recipients."
)
