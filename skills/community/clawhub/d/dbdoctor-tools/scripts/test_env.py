"""
test_env.py - Test .env file configuration loading

Used to verify if .env file loads environment variables correctly
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from common.config import config, LOGIN_MODE_PASSWORD, LOGIN_MODE_EMAIL


def test_env_loading():
    """Test environment variable loading"""
    print("=" * 60)
    print("Testing .env Configuration Loading")
    print("=" * 60)
    
    # Check common environment variables
    url = os.environ.get("DBDOCTOR_URL")
    print(f"\n✓ DBDOCTOR_URL: {url if url else '❌ NOT SET'}")

    # Check mode-specific environment variables
    email = os.environ.get("DBDOCTOR_EMAIL")
    user = os.environ.get("DBDOCTOR_USER")
    password = os.environ.get("DBDOCTOR_PASSWORD")

    print(f"✓ DBDOCTOR_EMAIL: {email if email else '(not set)'}")
    print(f"✓ DBDOCTOR_USER: {user if user else '(not set)'}")
    print(f"✓ DBDOCTOR_PASSWORD: {'***' if password else '(not set)'}")
    
    # Check config object
    print("\n" + "=" * 60)
    print("Config Object Values:")
    print("=" * 60)
    try:
        print(f"✓ Login Mode: {config.login_mode}")
        print(f"✓ Base URL: {config.base_url}")
        if config.login_mode == LOGIN_MODE_PASSWORD:
            print(f"✓ Username: {config.username}")
            print(f"✓ Password: {'***' if config.password else '❌ EMPTY'}")
        else:
            print(f"✓ Email: {config.email}")
        print(f"✓ User ID: {config.user_id}")
        print(f"✓ Role: {config.role}")
        print("\n✅ Configuration loaded successfully!")
    except Exception as e:
        print(f"\n❌ Error loading configuration: {e}")
        return False
    
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_env_loading()
    sys.exit(0 if success else 1)
