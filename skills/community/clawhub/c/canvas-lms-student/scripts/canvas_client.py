#!/usr/bin/env python3
"""
Canvas LMS API Client
Shared authentication and client initialization for all Canvas scripts.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

try:
    from canvasapi import Canvas
    from canvasapi.exceptions import CanvasException
except ImportError:
    print("Error: canvasapi not installed. Run: pip install canvasapi", file=sys.stderr)
    sys.exit(1)


# Config file location (same as CLI tool)
CONFIG_FILE = Path.home() / ".config" / "canvas-lms" / "config.json"


def get_config() -> Tuple[Optional[str], Optional[str]]:
    """
    Get Canvas configuration from environment variables or config file.
    
    Returns:
        Tuple of (base_url, api_token) - either may be None if not configured
    """
    # First check environment variables (highest priority)
    base_url = os.environ.get("CANVAS_BASE_URL")
    api_token = os.environ.get("CANVAS_API_TOKEN")
    
    if base_url and api_token:
        return base_url, api_token
    
    # Fall back to config file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
            if not base_url:
                base_url = data.get("base_url")
            if not api_token:
                api_token = data.get("api_token")
        except (json.JSONDecodeError, IOError):
            pass
    
    return base_url, api_token


def print_setup_instructions():
    """Print configuration instructions to stderr."""
    print("\nCanvas LMS is not configured. Please set up using one of these methods:", file=sys.stderr)
    print("\nMethod 1: Environment Variables", file=sys.stderr)
    print('  export CANVAS_BASE_URL="https://your-school.instructure.com"', file=sys.stderr)
    print('  export CANVAS_API_TOKEN="your-token-here"', file=sys.stderr)
    print("\nMethod 2: CLI Tool (easier)", file=sys.stderr)
    print("  pip install canvas-lms-cli", file=sys.stderr)
    print("  canvas-lms config", file=sys.stderr)
    print("\nGet your API token from Canvas:", file=sys.stderr)
    print("  1. Log into Canvas → Account → Settings", file=sys.stderr)
    print("  2. Scroll to 'Approved Integrations'", file=sys.stderr)
    print("  3. Click '+ New Access Token'", file=sys.stderr)


def get_canvas_client(silent: bool = False) -> Canvas:
    """
    Initialize and return authenticated Canvas API client.
    
    Args:
        silent: If True, don't print connection info (useful for JSON output mode)
    
    Raises:
        SystemExit: If configuration is missing or connection fails
    """
    base_url, api_token = get_config()
    
    if not base_url or not api_token:
        print("Error: Canvas LMS is not configured", file=sys.stderr)
        print_setup_instructions()
        sys.exit(1)
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    
    try:
        canvas = Canvas(base_url, api_token)
        # Verify connection by getting current user
        user = canvas.get_current_user()
        if not silent:
            print(f"Connected as: {user.name}", file=sys.stderr)
        return canvas
    except CanvasException as e:
        print(f"Error connecting to Canvas: {e}", file=sys.stderr)
        print("\nCheck that:", file=sys.stderr)
        print("  - CANVAS_BASE_URL is correct (e.g., https://canvas.university.edu)", file=sys.stderr)
        print("  - CANVAS_API_TOKEN is valid and not expired", file=sys.stderr)
        print("\nConfig source: " + ("environment variables" if os.environ.get("CANVAS_API_TOKEN") else f"{CONFIG_FILE}"), file=sys.stderr)
        sys.exit(1)


def test_connection() -> bool:
    """Test Canvas connection and return success status."""
    base_url, api_token = get_config()
    
    if not base_url or not api_token:
        print("✗ Not configured", file=sys.stderr)
        print_setup_instructions()
        return False
    
    try:
        canvas = get_canvas_client()
        user = canvas.get_current_user()
        print(f"✓ Successfully connected to Canvas")
        print(f"✓ Logged in as: {user.name} (ID: {user.id})")
        
        # Count active courses
        courses = list(canvas.get_courses(enrollment_state='active'))
        print(f"✓ Found {len(courses)} active courses")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_connection()
        sys.exit(0 if success else 1)
    else:
        get_canvas_client()
        print("Canvas client initialized successfully")
