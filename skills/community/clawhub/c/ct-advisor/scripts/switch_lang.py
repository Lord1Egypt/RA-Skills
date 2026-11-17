#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-sentence interface-language switch for ct-advisor.

The methodology agent invokes this when the user asks to switch language.

Usage:
  python scripts/switch_lang.py <zh-CN|en> [--permanent|--session]
    default scope = session  (lasts the current conversation only)
    --permanent            writes config.json `language` (persists across sessions)
    --session              explicit session scope (same as default)

Examples:
  python scripts/switch_lang.py en            # 临时：仅本次对话
  python scripts/switch_lang.py zh-CN          # 临时：仅本次对话
  python scripts/switch_lang.py en --permanent # 永久：写入 config.json

Resolution chain in i18n._current_lang() (highest → lowest):
  process override → session file → config.json `language` → OS locale.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from i18n import (  # noqa: E402
    set_lang_session,
    set_lang_permanent,
    _current_lang,
)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Switch ct-advisor interface language")
    ap.add_argument("lang", choices=["zh-CN", "en"], help="target language")
    scope = ap.add_mutually_exclusive_group()
    scope.add_argument("--permanent", action="store_true",
                       help="write config.json `language` (persists across sessions)")
    scope.add_argument("--session", action="store_true",
                       help="write data/.lang_session (default scope)")
    args = ap.parse_args(argv)

    if args.permanent:
        set_lang_permanent(args.lang)
        scope_label = "permanent (config.json updated)"
    else:
        set_lang_session(args.lang)
        scope_label = "session (this conversation only)"

    cur = _current_lang()
    msg = {
        "zh": "已切换界面语言为：中文（作用范围：%s）。" % scope_label,
        "en": "Interface language switched to: English (scope: %s)." % scope_label,
    }[cur]
    print(msg)


if __name__ == "__main__":
    main()
