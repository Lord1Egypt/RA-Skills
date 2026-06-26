#!/usr/bin/env python
"""
模板渲染工具：选择对应模板并注入变量，输出 Markdown 到 stdout。

用法: echo '{"state_type":"attraction","message_count":0,...}' | python render_output.py
  或: python render_output.py --context '{"state_type":"attraction",...}'
输出: 渲染后的 Markdown 到 stdout
"""

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SKILL_DIR_STR = str(SKILL_DIR)
SKILL_DIR_PATH = Path(SKILL_DIR)
TEMPLATES_DIR = SKILL_DIR_PATH / "templates"

sys.path.insert(0, str(SCRIPT_DIR))


TEMPLATE_MAP = {
    "planning_start": "state_planning_start.md",
    "planning_final": "state_planning_final.md",
    "prep": "state_prep.md",
    "departure": "state_departure.md",
    "transit": "state_transit.md",
    "arrival": "state_arrival.md",
    "attraction": "state_attraction_first.md",  # message_count == 0
    "attraction_extra": "state_attraction_extra.md",  # message_count > 0
    "return": "state_return_home.md",
}


def select_template(state_type: str, message_count: int = 0) -> str:
    """根据状态和消息计数选择模板文件名。"""
    if state_type == "attraction" and message_count > 0:
        return TEMPLATE_MAP["attraction_extra"]
    return TEMPLATE_MAP.get(state_type, "state_attraction_first.md")


def render(context: dict) -> str:
    """渲染模板并返回 Markdown 字符串。"""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )

    state_type = context.get("state_type", "attraction")
    message_count = context.get("message_count", 0)
    template_name = select_template(state_type, message_count)

    template = env.get_template(template_name)
    return template.render(**context)


def main():
    parser = argparse.ArgumentParser(description="Render output template")
    parser.add_argument("--context", help="JSON context string")
    args = parser.parse_args()

    if args.context:
        context = json.loads(args.context)
    else:
        context = json.loads(sys.stdin.read())

    result = render(context)
    print(result)


if __name__ == "__main__":
    main()
