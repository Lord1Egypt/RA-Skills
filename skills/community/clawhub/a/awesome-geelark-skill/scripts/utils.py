#!/usr/bin/env python3
"""
Shared utilities for GeeLark API Skill

This module provides common utility functions used across multiple scripts.
"""

import os
import uuid
import json
from typing import Dict, Optional
from pathlib import Path


def generate_traceid() -> str:
    """
    Generate a trace ID for API requests.

    Returns:
        str: Standard UUID4 format (with hyphens), in uppercase
    """
    return str(uuid.uuid4()).upper()


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Load GeeLark API configuration from config file.

    Args:
        config_path: Path to config file (optional, defaults to assets/config.json)

    Returns:
        dict: Configuration dictionary

    Raises:
        FileNotFoundError: If config file does not exist
        ValueError: If config file is invalid or missing required fields
    """
    if config_path is None:
        # Use pathlib for robust path resolution
        script_dir = Path(__file__).resolve().parent
        config_path = script_dir.parent / 'assets' / 'config.json'

    config_path = str(config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")

    # Validate required fields
    if 'auth' not in config:
        raise ValueError("Invalid config: missing 'auth' section")

    if 'token' not in config['auth']:
        raise ValueError("Invalid config: missing 'token' in 'auth' section")

    if 'baseUrl' not in config:
        raise ValueError("Invalid config: missing 'baseUrl' section")

    return config


def get_token(config_path: Optional[str] = None) -> str:
    """
    Get API token from config file.

    Args:
        config_path: Path to config file (optional)

    Returns:
        str: API token
    """
    config = load_config(config_path)
    return config['auth']['token']


def get_base_url(config_path: Optional[str] = None) -> str:
    """
    Get base URL from config file.

    Args:
        config_path: Path to config file (optional)

    Returns:
        str: Base URL from config
    """
    config = load_config(config_path)
    return config['baseUrl']


if __name__ == "__main__":
    # Test utility functions
    print("Testing utils.py...")

    # Test generate_traceid
    trace_id = generate_traceid()
    print(f"✅ generate_traceid(): {trace_id}")

    # Test load_config
    try:
        config = load_config()
        print(f"✅ load_config(): Loaded config with {len(config)} keys")
        print(f"   baseUrl: {config.get('baseUrl')}")
        print(f"   token: {config['auth']['token'][:20]}...")
    except Exception as e:
        print(f"❌ load_config(): {e}")

    print("\n✅ All tests completed!")