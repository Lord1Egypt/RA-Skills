#!/usr/bin/env python3
"""
Setup script for the Enhanced Attio Skill
"""

import sys


def check_prerequisites():
    """Check if prerequisites are met"""
    print("Checking prerequisites...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    
    print("✅ Python version is sufficient")
    return True


def main():
    """Main setup function"""
    print("🚀 Setting up Enhanced Attio Skill...")
    print()
    
    if not check_prerequisites():
        return False
    
    print()
    print("✅ Setup complete!")
    print()
    print("📋 Required environment variables:")
    print("   ATTIO_API_KEY - Your Attio API key")
    print("   ATTIO_WORKSPACE_ID - Your Attio workspace ID")
    print()
    print("📋 Get your API key from: https://app.attio.com/settings/api")
    print("📋 Find workspace ID in Attio URL: app.attio.com/[workspace-id]/...")
    
    return True


if __name__ == "__main__":
    main()
