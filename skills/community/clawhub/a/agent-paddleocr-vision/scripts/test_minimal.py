#!/usr/bin/env python3
"""
Minimal test without external deps: just classification + action + simple template fallback.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Import only modules we need (avoid templates if jinja2 missing)
import classify
import actions

def simple_render(doc_type: str, data: dict, text: str) -> str:
    """Fallback renderer if Jinja2 missing."""
    templates = {
        "invoice": "You are a financial assistant. The user has provided an invoice.\nExtracted data:\n- Amount: {{ amount }}\n- Vendor: {{ vendor }}\n- Date: {{ date }}\n\nPossible actions:\n1. create_expense\n2. archive\n3. tax_report",
        "business_card": "You are a contact manager.\nName: {{ name }}\nPhone: {{ phone }}\nEmail: {{ email }}\nActions: add_contact, save_vcard",
        "general": "You are an AI assistant.\nActions: summarize, translate, search_keywords",
    }
    tpl = templates.get(doc_type, templates["general"])
    for k, v in data.items():
        tpl = tpl.replace(f"{{{{ {k} }}}}", str(v) if v else "unknown")
    return tpl

def test_classify_and_actions():
    test_cases = [
        ("發票", "發票號碼: AB12345678\n金額: NT$ 1,200\n日期: 2025-03-15\n賣方: 某某科技"),
        ("身分證", "身分證字號: A123456789\n姓名: 李四\n出生日期: 1990-01-01"),
        ("名片", "姓名: 王大明\n電話: 0912-345-678\nEmail: test@example.com"),
    ]

    print("=== Classification + Actions test ===\n")
    for expected, text in test_cases:
        res = classify.classify(text)
        acts = actions.suggest_actions(res.doc_type, text, {})
        print(f"[{expected}] -> type={res.doc_type} (conf={res.confidence:.2f})")
        if acts:
            print(f"  top action: {acts[0].name} ({acts[0].confidence:.2f}): {acts[0].description}")
            if acts[0].parameters:
                print(f"    params: {acts[0].parameters}")
        # Render prompt with fallback
        prompt = simple_render(res.doc_type, acts[0].parameters if acts else {}, text)
        print(f"  prompt preview: {prompt[:120]}...")
        print()

if __name__ == "__main__":
    test_classify_and_actions()
    print("✅ Internal logic OK (no external deps).")
