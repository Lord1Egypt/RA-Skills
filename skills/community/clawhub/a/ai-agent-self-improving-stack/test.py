#!/usr/bin/env python3
"""
test.py for certainlogic-self-improving-stack
Verifies: valid configs, skill.json structure
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent

def test_skill_md_exists():
    path = SKILL_DIR / "SKILL.md"
    assert path.exists() and path.stat().st_size > 100, "SKILL.md missing or too short"
    print("✅ SKILL.md exists")

def test_meta_json_valid():
    path = SKILL_DIR / "_meta.json"
    assert path.exists(), "_meta.json not found"
    with open(path) as f:
        meta = json.load(f)
    assert "slug" in meta and "version" in meta, "missing required fields"
    print(f"✅ _meta.json valid: {meta['slug']} v{meta['version']}")

def test_skill_json_valid():
    path = SKILL_DIR / "skill.json"
    assert path.exists(), "skill.json not found"
    with open(path) as f:
        data = json.load(f)
    assert isinstance(data, dict), "skill.json must be object"
    assert "name" in data, "skill.json missing 'name'"
    print(f"✅ skill.json valid: {data['name']}")

def test_version_semver():
    with open(SKILL_DIR / "_meta.json") as f:
        meta = json.load(f)
    ver = meta["version"]
    assert ver.count(".") >= 2, f"version '{ver}' not semver"
    print(f"✅ Version valid: {ver}")

if __name__ == "__main__":
    tests = [test_skill_md_exists, test_meta_json_valid, test_skill_json_valid, test_version_semver]
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
    if failed == 0:
        print(f"\n✅ All {len(tests)} tests passed")
        sys.exit(0)
    else:
        print(f"\n❌ {failed}/{len(tests)} tests failed")
        sys.exit(1)
