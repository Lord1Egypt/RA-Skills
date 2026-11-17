#!/usr/bin/env python3
"""Single source of truth for netflag/netport body orientation.

The whole 12-entry rotation table is determined by four facts (see
orientation.json): the +90° body cycle ``up → right → down → left`` and the
body direction at rotation 0 for each family (power=down, ground=up, port=right).
(2026-06-29: cycle/anchors re-calibrated from rendered flag bodies; this visual
rotation mapping is independent of the schematic endpoint coordinate signs.)
``derive`` reconstructs the table; ``load_body_rotation`` reads the canonical
spec next to this file. The lint check and the connector's connect_pin both
derive from these same facts, so they can never drift — scripts/skill-lint-tests/run.py (repo) asserts it.
"""
import json
import os

# orientation.json is the canonical truth and lives in the easyeda-agent
# skill (single source); this operational script reads it within the merged skill package.
DEFAULT_SPEC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'references', 'orientation.json')


def derive(rotation_cycle, body_anchor):
    """Derive {family: {direction: rotation}} from the cycle + per-family anchor.

    rotation that makes the body point `direction` = (index(direction) -
    index(anchor)) mod 4, times 90. Pure function — no I/O.
    """
    table = {}
    for family, anchor in body_anchor.items():
        ai = rotation_cycle.index(anchor)
        table[family] = {
            d: ((rotation_cycle.index(d) - ai) % 4) * 90
            for d in rotation_cycle
        }
    return table


def load_spec(path=DEFAULT_SPEC):
    # utf-8 固定编码:orientation.json 含中文,Windows 中文环境默认 cp936/cp950
    # 解码会抛 UnicodeDecodeError(仓库文件一律按 utf-8 读)。
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_body_rotation(path=DEFAULT_SPEC):
    """Return the derived body-rotation table from the canonical spec."""
    spec = load_spec(path)
    return derive(spec['rotationCycle'], spec['bodyAnchorAtRot0'])


if __name__ == '__main__':
    # Print the derived table so a human can eyeball it against frozenTable.
    print(json.dumps(load_body_rotation(), indent=2))
