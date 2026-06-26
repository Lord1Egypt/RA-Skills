#!/usr/bin/env python3
"""
Configure Claude Code to use a custom model provider.

Usage:
    python configure_model.py --base-url <url> --model <name> --api-key <key>

Example:
    python configure_model.py --base-url https://api.deepseek.com/anthropic --model deepseek-v4-flash --api-key sk-xxx
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def get_claude_config_path() -> Path:
    """Get the path to Claude Code config directory."""
    home = Path.home()
    return home / ".claude"


def update_environment_variables(base_url: str, model: str, api_key: str) -> None:
    """Set user-level environment variables on Windows."""
    if sys.platform == "win32":
        # PowerShell commands to set user environment variables
        commands = [
            f'[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "{api_key}", "User")',
            f'[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "{base_url}", "User")',
            f'[Environment]::SetEnvironmentVariable("ANTHROPIC_MODEL", "{model}", "User")',
            '[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "", "User")',
        ]
        for cmd in commands:
            subprocess.run(["powershell", "-Command", cmd], check=True)
        print("✓ Environment variables updated")
    else:
        # For Unix-like systems, update shell profile
        shell_profile = Path.home() / ".bashrc"
        if not shell_profile.exists():
            shell_profile = Path.home() / ".zshrc"
        
        env_lines = [
            f'export ANTHROPIC_API_KEY="{api_key}"',
            f'export ANTHROPIC_BASE_URL="{base_url}"',
            f'export ANTHROPIC_MODEL="{model}"',
            'unset ANTHROPIC_AUTH_TOKEN',
        ]
        
        print(f"Add these lines to your shell profile ({shell_profile}):")
        for line in env_lines:
            print(f"  {line}")


def update_config_json(base_url: str, model: str, api_key: str) -> None:
    """Update ~/.claude/config.json."""
    config_path = get_claude_config_path() / "config.json"
    
    config = {"env": {}}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    
    # Update env section
    if "env" not in config:
        config["env"] = {}
    
    config["env"]["ANTHROPIC_API_KEY"] = api_key
    config["env"]["ANTHROPIC_BASE_URL"] = base_url
    config["env"]["ANTHROPIC_MODEL"] = model
    
    # Remove old auth token if present
    if "ANTHROPIC_AUTH_TOKEN" in config["env"]:
        del config["env"]["ANTHROPIC_AUTH_TOKEN"]
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Updated {config_path}")


def update_settings_json(base_url: str, model: str, api_key: str) -> None:
    """Update ~/.claude/settings.json."""
    settings_path = get_claude_config_path() / "settings.json"
    
    settings = {}
    if settings_path.exists():
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    
    # Update model
    settings["model"] = model
    
    # Update env section
    if "env" not in settings:
        settings["env"] = {}
    
    settings["env"]["ANTHROPIC_BASE_URL"] = base_url
    settings["env"]["ANTHROPIC_API_KEY"] = api_key
    
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    
    print(f"✓ Updated {settings_path}")


def verify_configuration() -> bool:
    """Test if Claude Code is using the new model."""
    print("\nTesting configuration...")
    try:
        result = subprocess.run(
            ["claude", "--print", "hi, what model are you?"],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"Response: {result.stdout.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error testing: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Configure Claude Code model")
    parser.add_argument("--base-url", required=True, help="API endpoint URL")
    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--api-key", required=True, help="API key")
    parser.add_argument("--skip-env", action="store_true", help="Skip environment variable update")
    
    args = parser.parse_args()
    
    print(f"Configuring Claude Code to use: {args.model}")
    print(f"API endpoint: {args.base_url}")
    print()
    
    if not args.skip_env:
        update_environment_variables(args.base_url, args.model, args.api_key)
    
    update_config_json(args.base_url, args.model, args.api_key)
    update_settings_json(args.base_url, args.model, args.api_key)
    
    print()
    print("Configuration complete!")
    print()
    print("Note: Open a new terminal window for environment variables to take effect.")
    print("Then run 'claude' to start using the new model.")


if __name__ == "__main__":
    main()