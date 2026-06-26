#!/usr/bin/env python3
"""
Feishu Webhook Message Sender
Supports multiple message types: text, post, interactive, image
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Any, Optional


def load_config() -> Dict[str, Any]:
    """
    Load webhook URLs from ~/.openclaw/skills/feishu-notify/config.json

    Returns:
        Dictionary containing webhook URLs

    Raises:
        FileNotFoundError: If config file does not exist
        ValueError: If config file is missing required fields
    """
    # Determine home directory
    home_dir = os.path.expanduser("~")
    skill_config_dir = os.path.join(home_dir, ".openclaw", "skills", "feishu-notify")
    config_file_path = os.path.join(skill_config_dir, "config.json")

    # Check if config file exists
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_file_path}\n"
            f"Please create this file with your webhook URLs:\n"
            f"  {{'webhooks': {{'default': 'https://open.feishu.cn/open-apis/bot/v2/hook/your-url'}}}}"
        )

    # Load and parse config file
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")

    # Validate required fields
    if 'webhooks' not in config:
        raise ValueError(
            f"Config file is missing 'webhooks' field\n"
            f"Current config: {config}"
        )

    if not isinstance(config['webhooks'], dict):
        raise ValueError(
            f"'webhooks' field must be a dictionary\n"
            f"Current type: {type(config['webhooks'])}"
        )

    if not config['webhooks']:
        raise ValueError(
            f"No webhook URLs configured\n"
            f"Please add at least one webhook URL"
        )

    return config['webhooks']


def load_template(template_path: str, skill_dir: str = None) -> Dict[str, Any]:
    """
    Load message template from file (restricted to templates directory)

    Args:
        template_path: Path to template JSON file
        skill_dir: Skill directory path (for security validation)

    Returns:
        Template dictionary

    Raises:
        FileNotFoundError: If template file does not exist
        ValueError: If template file is invalid or outside templates directory
    """
    # Get skill directory if not provided
    if skill_dir is None:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(skill_dir, "templates")

    # Normalize paths for comparison
    template_abs = os.path.abspath(template_path)
    templates_abs = os.path.abspath(templates_dir)

    # Security: Ensure template is within templates directory
    if not template_abs.startswith(templates_abs):
        raise ValueError(
            f"Security error: Template must be within templates directory\n"
            f"Template path: {template_path}\n"
            f"Allowed directory: {templates_abs}"
        )

    if not os.path.exists(template_abs):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    try:
        with open(template_abs, 'r', encoding='utf-8') as f:
            template = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in template file: {e}")

    return template


def fill_template(template: Dict[str, Any], variables: Dict[str, str]) -> Dict[str, Any]:
    """
    Fill template with variables (with proper JSON escaping)

    Args:
        template: Template dictionary
        variables: Variable values to fill

    Returns:
        Filled template
    """
    template_str = json.dumps(template, ensure_ascii=False)
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        # Properly escape the value to preserve JSON structure
        # Dump the value to JSON and remove outer quotes to preserve special characters
        escaped_value = json.dumps(str(value), ensure_ascii=False)[1:-1]
        template_str = template_str.replace(placeholder, escaped_value)

    try:
        return json.loads(template_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse filled template: {e}")


def send_message(
    webhook_url: str,
    message: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Send message to Feishu webhook

    Args:
        webhook_url: Feishu webhook URL
        message: Message object to send

    Returns:
        Response data, or None if failed
    """
    # Prepare request
    message_json = json.dumps(message, ensure_ascii=False)
    headers = {
        "Content-Type": "application/json"
    }

    # Send HTTP POST request
    try:
        req = urllib.request.Request(
            webhook_url,
            data=message_json.encode('utf-8'),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            response_body = response.read().decode('utf-8')
            response_code = response.getcode()

            # Parse response
            response_data = json.loads(response_body)

            if response_code != 200:
                print(f"Error: HTTP status code is not 200, actual: {response_code}", file=sys.stderr)
                return None

            if response_data.get('code') != 0:
                print(f"Error: Response code is not 0, actual: {response_data.get('code')}", file=sys.stderr)
                print(f"Error message: {response_data.get('msg')}", file=sys.stderr)
                return None

            # Return success response
            return response_data

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error response: {error_body}", file=sys.stderr)
        except:
            pass
        return None
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unknown error: {e}", file=sys.stderr)
        return None


def main():
    """Main function - command line test"""
    import argparse

    parser = argparse.ArgumentParser(description='Send message to Feishu webhook')
    parser.add_argument('webhook_name', help='Name of the webhook (e.g., default, alerts, notifications)')
    parser.add_argument('--type', choices=['text', 'post', 'interactive', 'image'], default='text',
                       help='Message type (default: text)')
    parser.add_argument('--message', help='Message content')
    parser.add_argument('--template', help='Path to template file')
    parser.add_argument('--var', action='append', help='Template variables in format key=value',
                       metavar='KEY=VALUE')

    args = parser.parse_args()

    # Load webhook URLs
    try:
        webhooks = load_config()
    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    # Get webhook URL
    webhook_url = webhooks.get(args.webhook_name)
    if not webhook_url:
        print(f"Error: Webhook '{args.webhook_name}' not found in config", file=sys.stderr)
        print(f"Available webhooks: {list(webhooks.keys())}", file=sys.stderr)
        sys.exit(1)

    # Build message
    if args.template:
        # Load and fill template (with security validation)
        try:
            template = load_template(args.template)
        except (FileNotFoundError, ValueError) as e:
            print(f"Template error: {e}", file=sys.stderr)
            sys.exit(1)

        # Parse variables
        variables = {}
        if args.var:
            for var in args.var:
                if '=' in var:
                    key, value = var.split('=', 1)
                    variables[key.strip()] = value.strip()

        # Fill default variables
        if 'time' not in variables:
            variables['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'source' not in variables:
            variables['source'] = 'Feishu Notify Skill'

        message = fill_template(template, variables)
    else:
        # Build simple message
        if args.type == 'text':
            message = {
                "msg_type": "text",
                "content": {
                    "text": args.message or "Hello from Feishu Notify Skill!"
                }
            }
        elif args.type == 'post':
            message = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": "Notification",
                            "content": [
                                [
                                    {
                                        "tag": "text",
                                        "text": args.message or "Hello from Feishu Notify Skill!"
                                    }
                                ]
                            ]
                        }
                    }
                }
            }
        elif args.type == 'interactive':
            message = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": "Notification"
                        },
                        "template": "blue"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": args.message or "Hello from Feishu Notify Skill!"
                            }
                        }
                    ]
                }
            }
        elif args.type == 'image':
            message = {
                "msg_type": "image",
                "content": {
                    "image_key": args.message or ""
                }
            }

    # Send message
    result = send_message(webhook_url, message)

    if result:
        print("Message sent successfully!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)
    else:
        print("Failed to send message", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
