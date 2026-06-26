#!/usr/bin/env python3
"""
Smoke test for Agent Vision skill.

Checks configuration and runs a quick classification test on sample text.
Does NOT require actual OCR API (uses simulated text).
"""

import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

def test_classify():
    from classify import classify, DOC_TYPE_INVOICE, DOC_TYPE_ID_CARD, DOC_TYPE_CONTRACT
    samples = [
        ("發票號碼: AB12345678\n發票日期: 2025年03月15日\n統一編號: 12345678\n金額: NT$ 1,200", DOC_TYPE_INVOICE),
        ("身分證字號: A123456789\n姓名: 李四\n出生日期: 1990年01月01日", DOC_TYPE_ID_CARD),
        ("合約甲方: 某某公司\n第1條\n簽署人: 張三", DOC_TYPE_CONTRACT),
    ]
    for text, expected in samples:
        result = classify(text)
        assert result.doc_type == expected, f"Expected {expected}, got {result.doc_type} ({result.scores})"
        assert result.confidence > 0.5, f"Confidence too low: {result.confidence}"
        print(f"✅ classify: {result.doc_type} (conf={result.confidence:.2f})")
    return True


def test_actions():
    from actions import suggest_actions
    sample = """發票號碼: AB12345678
金額: NT$ 1,200
發票日期: 2025年03月15日
賣方: 某某股份有限公司
"""
    actions = suggest_actions("invoice", sample, {})
    assert len(actions) > 0, "No actions suggested"
    assert any(a.name == "create_expense" for a in actions), "Missing create_expense"
    print(f"✅ actions: top={actions[0].name} ({actions[0].confidence:.2f})")
    return True


def test_template_rendering():
    from templates import render_agent_prompt
    data = {"amount": "1200", "vendor": "某某公司", "date": "2025-03-15"}
    prompt = render_agent_prompt("invoice", data, "")
    assert "1200" in prompt, "Amount not in prompt"
    assert "某某公司" in prompt, "Vendor not in prompt"
    print("✅ template rendering: invoice prompt generated")
    return True


def test_dependencies():
    """Check required Python packages."""
    missing = []
    try:
        import jinja2
    except ImportError:
        missing.append("jinja2")
    try:
        import httpx
    except ImportError:
        missing.append("httpx")
    try:
        import pydantic
    except ImportError:
        missing.append("pydantic")
    # Optional ones not required for smoke test
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("   Install: pip install -r scripts/requirements.txt")
        return False
    print("✅ dependencies OK")
    return True


def main():
    print("Running Agent Vision smoke test...\n")
    all_ok = True
    all_ok &= test_dependencies()
    all_ok &= test_classify()
    all_ok &= test_actions()
    all_ok &= test_template_rendering()
    print()
    if all_ok:
        print("✅ All smoke tests passed")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
