#!/usr/bin/env python3
"""Cleanup expired AgentRelay files and registry entries."""

import json
import sys
from pathlib import Path


script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from __init__ import AgentRelayTool


def main():
    default_ttl_hours = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    registry_ttl_hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24 * 7

    result = AgentRelayTool.cleanup(default_ttl_hours, registry_ttl_hours)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
