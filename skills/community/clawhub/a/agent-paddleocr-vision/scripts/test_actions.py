#!/usr/bin/env python3
"""
Standalone test for actions (no relative imports).
"""

import sys
from pathlib import Path

# Add current directory to path for direct import
sys.path.insert(0, str(Path(__file__).parent))

# Direct import (not relative)
import classify
import actions

classify_cls = classify.classify
suggest_actions = actions.suggest_actions

def test():
    samples = [
        ("發票號碼: AB12345678\n發票日期: 2025年03月15日\n統一編號: 12345678\n金額: NT$ 1,200", "invoice"),
        ("身分證字號: A123456789\n姓名: 李四\n出生日期: 1990年01月01日", "id_card"),
        ("合約甲方: 某某公司\n第1條\n簽署人: 張三", "contract"),
    ]

    print("Testing actions...\n")
    for text, expected in samples:
        result = classify_cls(text)
        print(f"[{expected}] detected as: {result.doc_type} (conf={result.confidence:.2f})")
        acts = suggest_actions(result.doc_type, text, {})
        print(f"  Top action: {acts[0].name if acts else 'none'}")
        for a in acts:
            print(f"    - {a.name} ({a.confidence:.2f}): {a.description}")
        print()

if __name__ == "__main__":
    test()
