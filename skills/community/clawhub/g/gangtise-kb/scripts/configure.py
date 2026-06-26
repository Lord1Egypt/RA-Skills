#!/usr/bin/env python3
"""
Interactive configuration script for Gangtise Knowledge Base Skill.
Sets up ACCESS_KEY and SECRET_KEY for API authentication.
"""
import json
import os
import sys
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"


def load_config():
    """Load existing configuration if available."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_config(config):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        # Set restrictive permissions (user read/write only)
        os.chmod(CONFIG_FILE, 0o600)
        return True
    except Exception as e:
        print(f"Error saving config: {e}", file=sys.stderr)
        return False


def main():
    print("=" * 60)
    print("Gangtise Knowledge Base - Configuration Setup")
    print("=" * 60)
    print()
    print("Please enter your Gangtise API credentials.")
    print("You can obtain these from: https://open.gangtise.com")
    print()

    # Load existing config
    config = load_config()

    # Get ACCESS_KEY
    current_ak = config.get('ACCESS_KEY', '')
    ak_prompt = f"Access Key [{current_ak[:4]}...]: " if current_ak else "Access Key: "
    ak = input(ak_prompt).strip()
    if not ak and current_ak:
        ak = current_ak

    # Get SECRET_KEY
    current_sk = config.get('SECRET_KEY', '')
    sk_prompt = f"Secret Key [{current_sk[:4]}...]: " if current_sk else "Secret Key: "
    sk = input(sk_prompt).strip()
    if not sk and current_sk:
        sk = current_sk

    # Validate input
    if not ak or not sk:
        print("\nError: Both Access Key and Secret Key are required.", file=sys.stderr)
        sys.exit(1)

    # Save configuration
    config['ACCESS_KEY'] = ak
    config['SECRET_KEY'] = sk
    config['BASE_URL'] = config.get('BASE_URL', 'https://open.gangtise.com')

    if save_config(config):
        print(f"\nConfiguration saved successfully to: {CONFIG_FILE}")
        print("You can now use the Gangtise knowledge base queries.")
    else:
        print("\nFailed to save configuration.", file=sys.stderr)
        sys.exit(1)


def get_credentials():
    """Get credentials from config file. Returns (access_key, secret_key) or (None, None)."""
    config = load_config()
    return config.get('ACCESS_KEY'), config.get('SECRET_KEY')


def check_configured():
    """Check if the skill is properly configured."""
    ak, sk = get_credentials()
    return bool(ak and sk)


if __name__ == "__main__":
    main()
