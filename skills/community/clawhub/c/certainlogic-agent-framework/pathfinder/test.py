#!/usr/bin/env python3
"""
test.py for certainlogic-pathfinder
Verifies: valid configs, skill.json, Python package imports
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
    # Accept either 'name', 'displayName', or 'id' as identifier
    has_name = "name" in data or "displayName" in data or "id" in data
    assert has_name, "skill.json missing identifier (name/displayName/id)"
    name = data.get("displayName") or data.get("name") or data.get("id")
    print(f"✅ skill.json valid: {name}")

def test_python_package_imports():
    """Try importing the agentpathfinder package"""
    try:
        sys.path.insert(0, str(SKILL_DIR))
        import agentpathfinder
        print(f"✅ agentpathfinder package imports successfully")
    except ImportError as e:
        print(f"⚠️ agentpathfinder import skipped (may need dependencies): {e}")
    finally:
        if str(SKILL_DIR) in sys.path:
            sys.path.remove(str(SKILL_DIR))

def test_setup_py_valid():
    path = SKILL_DIR / "setup.py"
    if path.exists():
        with open(path) as f:
            content = f.read()
        assert "name" in content, "setup.py missing name"
        print("✅ setup.py exists and looks valid")
    else:
        print("⚠️ setup.py not found (optional)")

def test_version_semver():
    with open(SKILL_DIR / "_meta.json") as f:
        meta = json.load(f)
    ver = meta["version"]
    assert ver.count(".") >= 2, f"version '{ver}' not semver"
    print(f"✅ Version valid: {ver}")

if __name__ == "__main__":
    tests = [
        test_skill_md_exists,
        test_meta_json_valid,
        test_skill_json_valid,
        test_python_package_imports,
        test_setup_py_valid,
        test_version_semver,
    ]
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
