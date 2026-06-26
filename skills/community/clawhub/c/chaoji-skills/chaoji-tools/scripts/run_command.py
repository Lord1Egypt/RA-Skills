#!/usr/bin/env python3
"""
Unified runner for ChaoJi API commands.

Security model:
- Command names resolved via whitelist (lib/commands.py).
- Input keys validated against command spec; unknown keys rejected.
- Uses subprocess to prevent command injection.
- See lib/executor.py and lib/input.py for implementation details.
"""

import sys
import os
import json
import argparse

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from commands import resolve_command_alias, COMMAND_SPECS
from executor import run_command, VIDEO_COMMANDS
from errors import build_error_response


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Run ChaoJi API command with validated input JSON.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_command.py --command model_tryon_quick --input-json '{"image_cloth": "...", "list_images_human": [...]}'
  python run_command.py --command cutout --input-json '{"image": "oss/path/photo.jpg"}'
  python run_command.py --command image2image --input-json '{"img": ["ref.jpg"], "prompt": "电商主图"}'
        '''
    )
    parser.add_argument('--command', required=True, help='Command name to execute')
    parser.add_argument('--input-json', required=True, help='Input parameters as JSON string')
    parser.add_argument('--poll', type=bool, default=True, help='Poll for task completion (default: True)')
    
    return parser.parse_args(argv)


def print_usage():
    """Print usage information."""
    usage = """
usage: run_command.py --command <command> --input-json '<json object>'

Run ChaoJi API command with validated input JSON (Python runtime).

Env toggles:
  CHAOJI_CONSOLE_URL=<url>                 console page for credential/auth guidance
  CHAOJI_ORDER_URL=<url>                   billing/order page for insufficient balance
  CHAOJI_TASK_WAIT_TIMEOUT_MS=<ms>         default: 600000 for video, 900000 for others
  CHAOJI_TASK_WAIT_INTERVAL_MS=<ms>        default: 2000

"""
    print(usage)


def main():
    """Main entry point."""
    try:
        args = parse_args()
    except SystemExit as e:
        if e.code != 0:
            print(json.dumps({"ok": False, "error": "command and input-json are required"}, ensure_ascii=False))
            return 2
        print_usage()
        return 0
    
    command_raw = args.command.strip()
    if not command_raw:
        print(json.dumps({"ok": False, "error": "command is required"}, ensure_ascii=False))
        return 2
    
    # Parse input JSON
    try:
        input_data = json.loads(args.input_json)
        if not isinstance(input_data, dict):
            raise ValueError("input-json must be a JSON object")
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"Invalid JSON: {str(e)}"}, ensure_ascii=False))
        return 2
    except ValueError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    
    # Resolve command alias
    try:
        command = resolve_command_alias(command_raw)
    except ValueError as e:
        error_response = build_error_response(
            error_type="INPUT_ERROR",
            error_code="CMD_001",
            error_name="不支持的命令",
            user_hint=f"不支持的命令：{command_raw}",
            next_action="请检查命令是否正确，或运行 'python run_command.py --help' 查看可用命令列表"
        )
        print(json.dumps(error_response, ensure_ascii=False))
        return 2
    
    # Validate input keys
    spec = COMMAND_SPECS.get(command, {})
    required_keys = spec.get('requiredKeys', [])
    optional_keys = spec.get('optionalKeys', [])
    all_keys = set(required_keys + optional_keys)
    
    # Check for unknown keys
    unknown_keys = set(input_data.keys()) - all_keys
    if unknown_keys:
        error_response = build_error_response(
            error_type="INPUT_ERROR",
            error_code="INPUT_001",
            error_name="未知参数",
            user_hint=f"命令 '{command}' 不支持以下参数：{', '.join(unknown_keys)}",
            next_action=f"请检查参数名称，支持的参数有：{', '.join(all_keys) if all_keys else '无'}"
        )
        print(json.dumps(error_response, ensure_ascii=False))
        return 2
    
    # Check required keys
    missing_keys = set(required_keys) - set(input_data.keys())
    if missing_keys:
        error_response = build_error_response(
            error_type="INPUT_ERROR",
            error_code="INPUT_002",
            error_name="缺少必填参数",
            user_hint=f"命令 '{command}' 缺少必填参数：{', '.join(missing_keys)}",
            next_action="请补充缺失的参数后重试"
        )
        print(json.dumps(error_response, ensure_ascii=False))
        return 2
    
    # Execute command
    try:
        result = run_command(command, input_data, poll=args.poll)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get('ok', False) else 1
    except Exception as e:
        error_response = build_error_response(
            error_type="RUNTIME_ERROR",
            error_code="RUNTIME_001",
            error_name="执行异常",
            user_hint=f"执行命令时发生异常：{str(e)}",
            next_action="请检查输入参数和环境配置后重试"
        )
        print(json.dumps(error_response, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
