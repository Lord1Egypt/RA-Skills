#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fmt_list(items, fallback='- 无'):
    items = items or [fallback]
    return "\n".join(f"- {x}" if not str(x).startswith("-") else str(x) for x in items)


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: build_boss_summary.py <input.json> <template.md> <output.md>", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    template = Path(sys.argv[2]).read_text(encoding='utf-8')
    configured = payload.get('boss_channel') or 'primary'
    available = list(payload.get('available_channels') or [])
    final_channel = configured if configured in available else (available[0] if available else configured)
    fallback_note = '无' if final_channel == configured else f'{configured} -> {final_channel}'
    text = template
    text = text.replace('{{date}}', payload.get('date', ''))
    text = text.replace('{{headline}}', payload.get('headline', '生成完成'))
    text = text.replace('{{priorities}}', fmt_list(payload.get('priorities')))
    text = text.replace('{{channel_status}}', fmt_list(payload.get('channel_status')))
    text = text.replace('{{delivery_mode}}', payload.get('delivery_mode', 'boss-primary'))
    text = text.replace('{{final_channel}}', final_channel)
    text = text.replace('{{fallback_note}}', fallback_note)
    out = Path(sys.argv[3])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    print(json.dumps({"final_channel": final_channel, "fallback_note": fallback_note, "output": str(out)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
