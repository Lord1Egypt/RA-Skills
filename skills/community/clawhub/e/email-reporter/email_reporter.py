#!/usr/bin/env python3
"""
Email Reporter - Generic Email Reporting Tool for OpenClaw
Supports Markdown/PDF auto-conversion and multiple email backends
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path

# Default config
DEFAULT_CONFIG = {
    "sender": os.getenv("EMAIL_SENDER", ""),
    "recipient": os.getenv("EMAIL_RECIPIENT", ""),
    "smtp_host": os.getenv("EMAIL_SMTP_HOST", "smtp.qq.com"),
    "smtp_port": int(os.getenv("EMAIL_SMTP_PORT", "587")),
    "smtp_user": os.getenv("EMAIL_SMTP_USER", ""),
    "smtp_pass": os.getenv("EMAIL_SMTP_PASS", ""),
    "use_msmtp": os.getenv("EMAIL_USE_MSMTP", "false").lower() == "true"
}

CONFIG_PATH = Path.home() / ".email_reporter.conf"

def load_config():
    """Load configuration from file or environment"""
    config = DEFAULT_CONFIG.copy()
    
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"⚠️  Config file error: {e}")
    
    return config

def get_sender(config, args):
    """Get sender email from args or config"""
    return args.sender or config.get("sender") or config.get("smtp_user")

def get_recipient(config, args):
    """Get recipient email from args or config"""
    return args.to or args.recipient or config.get("recipient")

def ensure_config(config):
    """Check if minimum config is present"""
    errors = []
    
    if not config.get("sender"):
        errors.append("Sender email not configured. Set EMAIL_SENDER or use --sender")
    if not config.get("recipient"):
        errors.append("Recipient email not configured. Set EMAIL_RECIPIENT or use --to")
    if not config.get("smtp_pass"):
        errors.append("SMTP password not configured. Set EMAIL_SMTP_PASS")
    
    if errors:
        print("❌ Configuration Error:")
        for err in errors:
            print(f"   - {err}")
        print("\n📖 Quick setup:")
        print("   export EMAIL_SENDER=\"your-email@qq.com\"")
        print("   export EMAIL_RECIPIENT=\"friend@example.com\"")
        print("   export EMAIL_SMTP_PASS=\"your-auth-code\"")
        return False
    
    return True

def send_report(report_path, config=None, args=None):
    """
    Send a report via email
    
    Automatically converts to PDF if:
    - File size > 500KB
    - Contains embedded images
    """
    if config is None:
        config = load_config()
    
    # Override config with CLI args
    sender = get_sender(config, args)
    recipient = get_recipient(config, args)
    agent = args.agent if args else "agent"
    subject = args.subject if args else None
    
    # Update config for validation
    temp_config = config.copy()
    temp_config["sender"] = sender
    temp_config["recipient"] = recipient
    
    if not ensure_config(temp_config):
        return False
    
    report_path = Path(report_path)
    if not report_path.exists():
        print(f"❌ Report not found: {report_path}")
        return False
    
    # Check file size and content
    file_size = report_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_images = '![' in content and ('.png' in content or '.jpg' in content or '.jpeg' in content or 'base64' in content)
    
    # Decide format
    if has_images or file_size_mb > 0.5:
        print(f"📄 Large file or images detected ({file_size_mb:.1f}MB), converting to PDF...")
        pdf_path = report_path.with_suffix('.pdf')
        
        try:
            # Find md2pdf.py
            skill_dir = Path(__file__).parent
            md2pdf_script = skill_dir / "md2pdf.py"
            
            if not md2pdf_script.exists():
                # Try shared utils
                md2pdf_script = Path("shared/utils/md2pdf.py")
            
            subprocess.run([
                'python3', str(md2pdf_script),
                str(report_path),
                str(pdf_path)
            ], check=True, capture_output=True)
            
            attachment = pdf_path
            format_type = "PDF"
        except Exception as e:
            print(f"⚠️  PDF conversion failed, using original: {e}")
            attachment = report_path
            format_type = "Markdown"
    else:
        attachment = report_path
        format_type = "Markdown"
    
    # Generate subject
    if not subject:
        filename = attachment.name
        subject = f"{agent}+{filename}"
    
    # Generate body
    body = f"""Hello,

This is a report from {agent} ({format_type} format).

Please find the attachment.

---
Sent by OpenClaw Email Reporter
"""
    
    # Send email
    print(f"📧 Sending {format_type} report to {recipient}...")
    
    try:
        # Find send_attachment.py
        skill_dir = Path(__file__).parent
        sender_script = skill_dir / "send_attachment.py"
        
        if not sender_script.exists():
            sender_script = Path("shared/utils/send_attachment.py")
        
        # Build command with config
        cmd = [
            'python3', str(sender_script),
            recipient,
            subject,
            str(attachment),
            body
        ]
        
        # Pass config via environment
        env = os.environ.copy()
        env["EMAIL_SENDER"] = sender
        env["EMAIL_SMTP_HOST"] = config.get("smtp_host", "smtp.qq.com")
        env["EMAIL_SMTP_PORT"] = str(config.get("smtp_port", 587))
        env["EMAIL_SMTP_USER"] = config.get("smtp_user", sender)
        env["EMAIL_SMTP_PASS"] = config.get("smtp_pass", "")
        env["EMAIL_USE_MSMTP"] = "true" if config.get("use_msmtp") else "false"
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Report sent successfully: {attachment.name}")
            return True
        else:
            print(f"❌ Failed to send: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_wizard():
    """Interactive setup wizard"""
    print("📧 Email Reporter Setup Wizard")
    print("=" * 40)
    
    config = {}
    
    config["sender"] = input("Your email address: ").strip()
    config["recipient"] = input("Default recipient email: ").strip()
    config["smtp_host"] = input("SMTP server [smtp.qq.com]: ").strip() or "smtp.qq.com"
    config["smtp_port"] = int(input("SMTP port [587]: ").strip() or "587")
    config["smtp_user"] = input(f"SMTP username [{config['sender']}]: ").strip() or config["sender"]
    config["smtp_pass"] = input("SMTP password/auth code: ").strip()
    
    use_msmtp = input("Use msmtp? [y/N]: ").strip().lower()
    config["use_msmtp"] = use_msmtp == 'y'
    
    # Save config
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n✅ Config saved to {CONFIG_PATH}")
    except Exception as e:
        print(f"\n❌ Failed to save config: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Email Reporter - Send Markdown/PDF reports via email",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s report.md
  %(prog)s report.md --agent invest-agent --to friend@example.com
  %(prog)s report.md --sender me@qq.com --subject "Weekly Report"
  %(prog)s --setup
        """
    )
    
    parser.add_argument("report", nargs="?", help="Path to Markdown report file")
    parser.add_argument("--agent", default="agent", help="Agent name (used in subject)")
    parser.add_argument("--to", "--recipient", dest="recipient", help="Recipient email address")
    parser.add_argument("--sender", help="Sender email address")
    parser.add_argument("--subject", help="Custom email subject")
    parser.add_argument("--setup", action="store_true", help="Run setup wizard")
    parser.add_argument("--version", action="version", version="%(prog)s 2.0.0")
    
    args = parser.parse_args()
    
    if args.setup:
        sys.exit(0 if setup_wizard() else 1)
    
    if not args.report:
        parser.print_help()
        sys.exit(1)
    
    config = load_config()
    success = send_report(args.report, config, args)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
