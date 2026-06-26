#!/usr/bin/env python3
"""
Initialize GeeLark API Configuration

This script helps users create their config.json from config_template.json
on first use.
"""

import os
import json
import sys


def init_config():
    """Initialize config.json from config_template.json"""

    # Get project root directory (parent of scripts directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    assets_dir = os.path.join(project_root, 'assets')

    # Paths
    template_path = os.path.join(assets_dir, 'config_template.json')
    config_path = os.path.join(assets_dir, 'config.json')

    # Check if config.json already exists
    if os.path.exists(config_path):
        print("✅ config.json already exists")
        print(f"   Location: {config_path}")

        # Ask if user wants to reconfigure
        choice = input("\nDo you want to reconfigure? (y/n): ").strip().lower()
        if choice != 'y':
            print("\n✅ Keeping existing configuration")
            return config_path

    # Load template
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return None

    with open(template_path, 'r') as f:
        template = json.load(f)

    print("=" * 60)
    print("🔧 GeeLark API Configuration Setup")
    print("=" * 60)
    print()

    # Get user input
    print("Please enter your GeeLark API credentials:")
    print()

    token = input("Token: ").strip()
    if not token:
        print("❌ Token is required")
        return None

    app_id = input("App ID (optional, press Enter to skip): ").strip()
    api_key = input("API Key (optional, press Enter to skip): ").strip()

    # Create config
    config = {
        "auth": {
            "token": token,
        },
        "baseUrl": "https://openapi.geelark.com",
        "rateLimit": {
            "perMinute": 200,
            "perHour": 24000
        }
    }

    if app_id:
        config["auth"]["appId"] = app_id

    if api_key:
        config["auth"]["apiKey"] = api_key

    # Save config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 60)
    print("✅ Configuration saved successfully!")
    print("=" * 60)
    print(f"   Location: {config_path}")
    print()
    print("⚠️  IMPORTANT:")
    print("   - config.json contains your sensitive credentials")
    print("   - Do NOT commit config.json to version control")
    print("   - config.json is already in .gitignore")
    print()
    print("✅ You can now use the GeeLark API skill!")
    print()

    return config_path


if __name__ == "__main__":
    init_config()