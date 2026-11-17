#!/usr/bin/env python3
"""Generate a lightweight AgentScope agent test harness."""

import argparse
import sys
from pathlib import Path


TEMPLATE = '''\
"""Auto-generated test harness for {agent_module}."""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agent_module"))

from {agent_module} import build_agent  # noqa: E402


class FakeModel:
    def __init__(self, response="fake response"):
        self.response = response

    async def __call__(self, *args, **kwargs):
        class FakeChoice:
            message = type("Msg", (), {"content": self.response})
        class FakeResp:
            choices = [FakeChoice()]
        return FakeResp()


def test_agent_returns_fake_response():
    agent = build_agent(model=FakeModel("hello"))
    result = agent("ping")
    assert result.choices[0].message.content == "hello"
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AgentScope test harness")
    parser.add_argument("--agent", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    module_name = args.agent.stem
    content = TEMPLATE.format(agent_module=module_name)
    args.output.write_text(content, encoding="utf-8")
    print(f"Wrote test harness to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
