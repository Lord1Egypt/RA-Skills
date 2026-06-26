#!/usr/bin/env python3
"""
Tests for AliYun Bailian LLM scripts.

Run:
    python scripts/tests.py
"""

import sys
import json

# Add parent directory to path for imports
sys.path.insert(0, __file__.rsplit("/", 1)[0])

from scripts import chat, translate, models


def test_chat():
    """Test chat function."""
    print("Testing chat...")
    result = chat(messages=[{"role": "user", "content": "Say 'test passed' in exactly those words"}], model="qwen3.5-plus")

    assert result.get("success"), f"chat failed: {result.get('error')}"
    content = result.get("result", {}).get("content", "")
    assert "test passed" in content.lower(), f"Unexpected response: {content}"
    print(f"  PASS: {content[:80]}...")
    return True


def test_translate():
    """Test translate function."""
    print("Testing translate...")
    result = translate(text="Hello", target_lang="zh", model="qwen3.5-plus")

    assert result.get("success"), f"translate failed: {result.get('error')}"
    translated = result.get("result", {}).get("translated_text", "")
    assert len(translated) > 0, "Empty translation"
    print(f"  PASS: 'Hello' -> '{translated}'")
    return True


def test_models():
    """Test models function."""
    print("Testing models...")
    result = models()

    assert result.get("success"), f"models failed: {result.get('error')}"
    model_list = result.get("result", {})
    assert "flagship" in model_list, "Missing flagship models"
    assert "qwen3.5-plus" in model_list["flagship"], "Missing qwen3.5-plus"
    assert "coder" in model_list, "Missing coder models"
    assert "other" in model_list, "Missing other models"
    print(f"  PASS: {list(model_list.keys())}")
    return True


def test_env_check():
    """Check environment variables."""
    import os

    print("Checking environment...")
    api_key = os.environ.get("ALIYUN_BAILIAN_API_KEY")
    api_host = os.environ.get("ALIYUN_BAILIAN_API_HOST", "https://coding.dashscope.aliyuncs.com/v1")

    if not api_key:
        print("  WARN: ALIYUN_BAILIAN_API_KEY not set")
        return False
    print(f"  API_KEY: {'*' * 20}{api_key[-4:]}")
    print(f"  API_HOST: {api_host}")
    return True


def main():
    print("=" * 50)
    print("AliYun Bailian LLM - Test Suite")
    print("=" * 50)

    if not test_env_check():
        print("\nSet ALIYUN_BAILIAN_API_KEY to run tests")
        print("export ALIYUN_BAILIAN_API_KEY='your-key'")
        sys.exit(1)

    print()

    tests = [
        ("models", test_models),
        ("chat", test_chat),
        ("translate", test_translate),
    ]

    passed = 0
    failed = 0

    for name, fn in tests:
        try:
            if fn():
                passed += 1
        except AssertionError as e:
            print(f"  FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
