#!/usr/bin/env python3
"""
Check if an operation requires user confirmation based on permission level.
"""

import sys
import argparse
import yaml
from pathlib import Path

def load_permission_config(config_path=None):
    """Load permission configuration from PERMISSION_CONFIG.yaml"""
    if config_path is None:
        # Try to find config in workspace
        current = Path.cwd()
        config_path = current / 'PERMISSION_CONFIG.yaml'
        
        if not config_path.exists():
            # Try parent directories
            for parent in current.parents:
                candidate = parent / 'PERMISSION_CONFIG.yaml'
                if candidate.exists():
                    config_path = candidate
                    break
    
    if not config_path or not Path(config_path).exists():
        # Return default config
        return {
            'permission_level': 2,
            'red_lines': [
                'spend_money',
                'send_public_message',
                'delete_database',
                'restart_production_service'
            ],
            'yellow_lines': [
                'delete_file',
                'modify_system_config',
                'install_system_package',
                'restart_service',
                'send_email'
            ],
            'custom_red_lines': [],
            'custom_yellow_lines': []
        }
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def check_permission(action, config):
    """
    Check if an action requires confirmation.
    
    Returns:
        bool: True if confirmation required, False otherwise
    """
    level = config.get('permission_level', 2)
    
    # Combine default and custom rules
    red_lines = config.get('red_lines', []) + config.get('custom_red_lines', [])
    yellow_lines = config.get('yellow_lines', []) + config.get('custom_yellow_lines', [])
    
    # Level 3: Everything requires confirmation
    if level == 3:
        return True
    
    # Level 2: Red + Yellow require confirmation
    if level == 2:
        return action in red_lines or action in yellow_lines
    
    # Level 1: Only Red requires confirmation
    if level == 1:
        return action in red_lines
    
    return False

def main():
    parser = argparse.ArgumentParser(
        description='Check if an operation requires confirmation'
    )
    parser.add_argument(
        '--action',
        required=True,
        help='Action to check (e.g., delete_file, send_email)'
    )
    parser.add_argument(
        '--config',
        help='Path to PERMISSION_CONFIG.yaml (default: auto-detect)'
    )
    parser.add_argument(
        '--level',
        type=int,
        choices=[1, 2, 3],
        help='Override permission level'
    )
    
    args = parser.parse_args()
    
    # Load config
    config = load_permission_config(args.config)
    
    # Override level if specified
    if args.level:
        config['permission_level'] = args.level
    
    # Check permission
    requires_confirmation = check_permission(args.action, config)
    
    # Output result
    level = config['permission_level']
    level_name = ['Master', 'Collaborative', 'Assistant'][level - 1]
    
    if requires_confirmation:
        print(f"⚠️  CONFIRMATION REQUIRED")
        print(f"Action: {args.action}")
        print(f"Level: {level} ({level_name} Mode)")
        sys.exit(1)
    else:
        print(f"✅ OK TO PROCEED")
        print(f"Action: {args.action}")
        print(f"Level: {level} ({level_name} Mode)")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)
