#!/usr/bin/env python3
import json
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: resolve_delivery_target.py <config.json>", file=sys.stderr)
        return 2
    cfg = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
    requested = cfg.get('boss_channel') or 'primary'
    available = list(cfg.get('available_channels') or [])
    final_channel = requested if requested in available else (available[0] if available else requested)
    print(json.dumps({
        'requested_channel': requested,
        'final_channel': final_channel,
        'fallback': final_channel != requested,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
