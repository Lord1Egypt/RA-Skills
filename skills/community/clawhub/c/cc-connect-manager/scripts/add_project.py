#!/usr/bin/env python3
"""Add a new project to cc-connect config.toml.

Usage:
    python3 add_project.py --name <project-name> --work-dir <path> \
        --platform <type> --token <token> [--agent <type>] [--mode <mode>] \
        [--guild-id <id>] [--config <path>]

Examples:
    # Add a Claude Code project with Telegram
    python3 add_project.py --name my-backend \
        --work-dir /path/to/backend \
        --platform telegram --token "123:ABC"

    # Add a Claude Code project with Discord
    python3 add_project.py --name my-frontend \
        --work-dir /path/to/frontend \
        --platform discord --token "MTQ..." --guild-id "148..."

    # Add a Codex project with Telegram
    python3 add_project.py --name codex-project \
        --work-dir /path/to/project \
        --platform telegram --token "123:ABC" \
        --agent codex --mode full-auto
"""

import argparse
import os
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Add a project to cc-connect config.toml")
    p.add_argument("--name", required=True, help="Project name")
    p.add_argument("--work-dir", required=True, help="Absolute path to project directory")
    p.add_argument("--platform", required=True, choices=[
        "telegram", "discord", "feishu", "dingtalk", "slack", "line", "wecom", "qq", "qqbot"
    ], help="Platform type")
    p.add_argument("--token", required=True, help="Platform bot token")
    p.add_argument("--agent", default="claudecode", choices=[
        "claudecode", "codex", "cursor", "gemini", "qoder", "opencode", "iflow"
    ], help="Agent type (default: claudecode)")
    p.add_argument("--mode", default="default", help="Agent permission mode (default: default)")
    p.add_argument("--guild-id", default="", help="Discord guild ID for instant slash commands")
    p.add_argument("--app-id", default="", help="Feishu/DingTalk app ID")
    p.add_argument("--app-secret", default="", help="Feishu/DingTalk app secret")
    p.add_argument("--bot-token", default="", help="Slack bot token (xoxb-...)")
    p.add_argument("--app-token", default="", help="Slack app token (xapp-...)")
    p.add_argument("--config", default=os.path.expanduser("~/.cc-connect/config.toml"),
                   help="Config file path")
    return p.parse_args()


def build_project_block(args):
    """Build a TOML project block string."""
    lines = []
    lines.append(f'\n[[projects]]')
    lines.append(f'  name = "{args.name}"')
    lines.append(f'  [projects.agent]')
    lines.append(f'    type = "{args.agent}"')
    lines.append(f'    [projects.agent.options]')
    lines.append(f'      mode = "{args.mode}"')
    lines.append(f'      work_dir = "{args.work_dir}"')

    lines.append(f'  [[projects.platforms]]')
    lines.append(f'    type = "{args.platform}"')
    lines.append(f'    [projects.platforms.options]')

    if args.platform == "telegram":
        lines.append(f'      token = "{args.token}"')
    elif args.platform == "discord":
        lines.append(f'      token = "{args.token}"')
        if args.guild_id:
            lines.append(f'      guild_id = "{args.guild_id}"')
    elif args.platform == "feishu":
        lines.append(f'      app_id = "{args.app_id or args.token}"')
        lines.append(f'      app_secret = "{args.app_secret}"')
    elif args.platform == "dingtalk":
        lines.append(f'      client_id = "{args.app_id or args.token}"')
        lines.append(f'      client_secret = "{args.app_secret}"')
    elif args.platform == "slack":
        lines.append(f'      bot_token = "{args.bot_token or args.token}"')
        lines.append(f'      app_token = "{args.app_token}"')
    elif args.platform == "qq":
        lines.append(f'      ws_url = "{args.token}"')
        lines.append(f'      allow_from = "*"')
    elif args.platform == "qqbot":
        lines.append(f'      app_id = "{args.app_id or args.token}"')
        lines.append(f'      app_secret = "{args.app_secret}"')
    elif args.platform == "wecom":
        lines.append(f'      corp_id = "{args.token}"')
    elif args.platform == "line":
        lines.append(f'      channel_token = "{args.token}"')

    lines.append('')  # trailing newline
    return '\n'.join(lines)


def main():
    args = parse_args()

    # Validate work_dir exists
    if not os.path.isdir(args.work_dir):
        print(f"WARNING: work_dir does not exist: {args.work_dir}", file=sys.stderr)

    # Read existing config
    config_path = args.config
    if not os.path.exists(config_path):
        print(f"ERROR: config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, 'r') as f:
        content = f.read()

    # Check for duplicate project name
    if f'name = "{args.name}"' in content:
        print(f"ERROR: project '{args.name}' already exists in config", file=sys.stderr)
        sys.exit(1)

    # Find insertion point: before the first non-project global section after projects,
    # or append to end. We insert before [log] or at end of file.
    block = build_project_block(args)

    # Append the new project block before global sections at the bottom
    # Find the last [[projects]] or [[projects.platforms]] block end
    # Simple approach: append before [log] if it exists, otherwise at end
    insert_markers = ['[log]', '[speech]', '[display]', '[stream_preview]', '[rate_limit]', '[cron]']
    insert_pos = -1
    for marker in insert_markers:
        pos = content.find(f'\n{marker}')
        if pos == -1:
            pos = content.find(marker)
            if pos == 0:
                insert_pos = 0
                break
        if pos != -1:
            if insert_pos == -1 or pos < insert_pos:
                insert_pos = pos if content[pos] == '[' else pos
                break

    if insert_pos > 0:
        # Insert before the global section
        content = content[:insert_pos] + block + '\n' + content[insert_pos:]
    else:
        # Append at end
        content = content.rstrip() + '\n' + block

    with open(config_path, 'w') as f:
        f.write(content)

    print(f"OK: project '{args.name}' added to {config_path}")


if __name__ == "__main__":
    main()
