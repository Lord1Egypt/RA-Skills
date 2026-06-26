#!/usr/bin/env python3
# Author: SQ
"""
Garmin OAuth Authentication Setup
One-time setup: saves credentials securely for future use
Supports both global (garmin.com) and China (garmin.cn) regions
"""

import base64
import getpass
import json
import os
import sys
from pathlib import Path

try:
    from garminconnect import Garmin
except ImportError:
    print("❌ garminconnect not installed. Run: pip install garminconnect")
    sys.exit(1)

def setup_oauth(email, password, is_cn=False):
    """Authenticate with Garmin and save credentials"""

    garth_dir = Path.home() / ".garth"
    session_file = garth_dir / "session.json"

    region = "China (garmin.cn)" if is_cn else "Global (garmin.com)"
    print(f"🔐 Authenticating with Garmin {region} ({email})...")

    try:
        # Test login to verify credentials
        garmin = Garmin(email, password, is_cn=is_cn)
        garmin.login()

        # Encode password with base64 (basic obfuscation, not encryption)
        # Note: For production, use proper encryption like cryptography.fernet
        encoded_password = base64.b64encode(password.encode()).decode()

        session_info = {
            "email": email,
            "password_encrypted": encoded_password,
            "region": "CN" if is_cn else "GLOBAL",
            "is_cn": is_cn
        }

        garth_dir.mkdir(exist_ok=True)

        # Save with restricted permissions (owner read/write only)
        with open(session_file, 'w') as f:
            json.dump(session_info, f, indent=2)

        # Set file permissions to 600 (owner read/write only)
        os.chmod(session_file, 0o600)

        print(f"✅ Authentication successful!")
        print(f"✅ Credentials saved to {session_file}")
        print(f"✅ Region: {region}")
        print("✅ You can now use garmin-sync.py")

        return True

    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\nCommon issues:")
        print("- Wrong email/password")
        print("- 2FA enabled (disable or use app-specific password)")
        print("- Garmin servers temporary unavailable")
        print("- Wrong region (use --cn for China accounts)")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 garmin-auth.py <email> <password> [--cn]")
        print("\nExamples:")
        print("  Global account: python3 garmin-auth.py user@example.com password123")
        print("  China account:   python3 garmin-auth.py user@qq.com password123 --cn")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    is_cn = "--cn" in sys.argv

    success = setup_oauth(email, password, is_cn)
    sys.exit(0 if success else 1)
