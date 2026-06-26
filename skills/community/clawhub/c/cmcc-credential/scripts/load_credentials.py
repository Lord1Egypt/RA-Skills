#!/usr/bin/env python3
"""
CMCC Digital Credential - Load and Manage Credentials

This script handles loading credentials from files and storing them in memory.
"""

import json
import os
import re
import sys

MEMORY_PATH = "memory/cmcc-digital-credential.json"


def parse_credentials_file(file_content: str) -> dict:
    """
    Parse credential file content.

    Supports both plain text (key=value) and JSON formats.

    Args:
        file_content: Content of the credential file

    Returns:
        Dictionary with appId and appKey only

    Raises:
        ValueError: If parsing fails or required fields missing

    Note:
        - appName is predefined and not loaded from file
        - templateId is predefined as: qfx9pkizs42up7y61jsehs9v8e1xms4m
        - Credential file uses field names: 智能体DID (maps to appId) and 智能体密钥 (maps to appKey)
    """
    # Field name mappings (Chinese -> internal)
    FIELD_MAPPINGS = {
        "智能体DID": "appId",
        "智能体密钥": "appKey",
        "appId": "appId",
        "appKey": "appKey",
    }

    # Try JSON format first
    try:
        data = json.loads(file_content)
        result = {}
        for key, value in data.items():
            normalized_key = FIELD_MAPPINGS.get(key, key)
            if normalized_key in ("appId", "appKey"):
                result[normalized_key] = value.strip()
        if "appId" in result and "appKey" in result:
            return result
    except json.JSONDecodeError:
        pass  # Not JSON, try plain text format

    # Try plain text format (key=value)
    credentials = {}
    for line in file_content.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Parse key=value (support Chinese characters in key)
        match = re.match(r'^([^=]+)\s*=\s*(.+)$', line)
        if match:
            key, value = match.groups()
            key = key.strip()
            normalized_key = FIELD_MAPPINGS.get(key, key)
            credentials[normalized_key] = value.strip()

    # Validate required fields (only appId and appKey)
    required_fields = ["appId", "appKey"]
    missing_fields = [f for f in required_fields if f not in credentials]

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    return {
        "appId": credentials["appId"],
        "appKey": credentials["appKey"]
    }


def load_credentials_from_file(file_path: str) -> dict:
    """
    Load credentials from a file.

    Args:
        file_path: Path to the credential file

    Returns:
        Dictionary with appId, appKey, and templateId

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If parsing fails
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return parse_credentials_file(content)


def save_credentials_to_memory(credentials: dict, memory_path: str = None) -> None:
    """
    Save credentials to memory file.

    Args:
        credentials: Dictionary with appId, appKey, and templateId
        memory_path: Path to memory file (default: MEMORY_PATH)
    """
    if memory_path is None:
        memory_path = MEMORY_PATH

    # Create memory directory if it doesn't exist
    os.makedirs(os.path.dirname(memory_path), exist_ok=True)

    # Save credentials
    with open(memory_path, 'w', encoding='utf-8') as f:
        json.dump(credentials, f, indent=2, ensure_ascii=False)


def load_credentials_from_memory(memory_path: str = None) -> dict:
    """
    Load credentials from memory file.

    Args:
        memory_path: Path to memory file (default: MEMORY_PATH)

    Returns:
        Dictionary with appId, appKey, and templateId

    Raises:
        FileNotFoundError: If memory file doesn't exist
    """
    if memory_path is None:
        memory_path = MEMORY_PATH

    with open(memory_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def credentials_exist(memory_path: str = None) -> bool:
    """
    Check if credentials exist in memory.

    Args:
        memory_path: Path to memory file (default: MEMORY_PATH)

    Returns:
        True if credentials exist, False otherwise
    """
    if memory_path is None:
        memory_path = MEMORY_PATH

    return os.path.exists(memory_path)


def validate_credentials(credentials: dict) -> bool:
    """
    Validate credential structure and content.

    Args:
        credentials: Dictionary with appId and appKey

    Returns:
        True if valid, False otherwise

    Note:
        Only validates appId and appKey.
        appName and templateId are predefined constants.
    """
    required_fields = ["appId", "appKey"]

    # Check all required fields exist
    for field in required_fields:
        if field not in credentials or not credentials[field]:
            return False

    # Validate appId format (should be 24 characters)
    if len(credentials["appId"]) != 24:
        return False

    # All validations passed
    return True


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Load and Manage CMCC Digital Credential')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Load command
    load_parser = subparsers.add_parser('load', help='Load credentials from file')
    load_parser.add_argument('file', help='Path to credential file')
    load_parser.add_argument('--force', '-f', action='store_true',
                             help='Overwrite existing credentials without confirmation')

    # Check command
    check_parser = subparsers.add_parser('check', help='Check if credentials exist')
    check_parser.add_argument('--memory-path', help='Path to memory file')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get credentials from memory')
    get_parser.add_argument('--memory-path', help='Path to memory file')
    get_parser.add_argument('--field', choices=['appId', 'appKey', 'templateId'],
                            help='Get specific field only')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate credentials structure')

    args = parser.parse_args()

    if args.command == 'load':
        # Check if credentials already exist
        if credentials_exist() and not args.force:
            response = input("Credentials already exist. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                sys.exit(0)

        # Load and parse credentials
        try:
            credentials = load_credentials_from_file(args.file)
            print(f"Loaded credentials from {args.file}")

            # Validate
            if not validate_credentials(credentials):
                print("Warning: Credentials validation failed", file=sys.stderr)
                response = input("Save anyway? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(1)

            # Save to memory
            save_credentials_to_memory(credentials)
            print("Credentials saved to memory")

            # Print summary
            print(f"appId (智能体DID): {credentials['appId']}")
            print("appKey (智能体密钥): *** (hidden)")
            print("\nNote:")
            print("  - appName: Use 'Javis' (predefined)")
            print("  - templateId: Fixed to qfx9pkizs42up7y61jsehs9v8e1xms4m")

        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'check':
        memory_path = args.memory_path or MEMORY_PATH
        if credentials_exist(memory_path):
            print("Credentials exist in memory")
            sys.exit(0)
        else:
            print("No credentials found in memory")
            sys.exit(1)

    elif args.command == 'get':
        memory_path = args.memory_path or MEMORY_PATH

        try:
            credentials = load_credentials_from_memory(memory_path)

            if args.field:
                print(credentials[args.field])
            else:
                print(json.dumps(credentials, indent=2, ensure_ascii=False))

        except FileNotFoundError:
            print(f"Error: Credentials not found in memory", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'validate':
        try:
            credentials = load_credentials_from_memory()

            if validate_credentials(credentials):
                print("Credentials are valid")
                sys.exit(0)
            else:
                print("Credentials are invalid", file=sys.stderr)
                sys.exit(1)

        except FileNotFoundError:
            print(f"Error: Credentials not found in memory", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
