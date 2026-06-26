#!/usr/bin/env python3
"""
Auto-generated test suite for skill: a2a-protocol
Run with: python tests/test_skill.py
"""

import sys, os, re, yaml

def _p(name, passed, msg=''):
    emoji = "✅" if passed else "❌"
    result = "PASS" if passed else "FAIL"
    print(f"  [{emoji}] {result} -- {name}{msg}")
    return passed

def _skill_md():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'SKILL.md')

def _frontmatter():
    with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    end = text.find('\n---', 3)
    if end == -1:
        return None
    try:
        return yaml.safe_load(text[3:end]) or {}
    except Exception:
        return None

def test_frontmatter_delimiters():
    with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return _p("frontmatter_delimiters", text.startswith("---"))

def test_frontmatter_name():
    fm = _frontmatter()
    if fm is None:
        return _p("frontmatter_name", False, " -- no frontmatter")
    name = fm.get('name', '').strip()
    skill_dir = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return _p('frontmatter_name', name == skill_dir,
             f" (got '{name}', expected '{skill_dir}')")

def test_frontmatter_description():
    fm = _frontmatter()
    if fm is None:
        return _p("frontmatter_description", False)
    return _p('frontmatter_description', bool(fm.get('description', '').strip()))

def test_frontmatter_license():
    fm = _frontmatter()
    if fm is None:
        return _p("frontmatter_license", False)
    lic = fm.get('license', '').strip().upper()
    return _p('frontmatter_license', lic == 'MIT' or 'MIT' in lic)

def test_frontmatter_metadata():
    fm = _frontmatter()
    if fm is None:
        return _p("frontmatter_metadata", False)
    meta = fm.get('metadata', {}) or {}
    has_version = bool(str(meta.get('version', '')).strip())
    has_category = bool(str(meta.get('category', '')).strip())
    return _p('frontmatter_metadata', has_version and has_category,
             f" (version={has_version}, category={has_category})")

def test_has_modes():
    with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return _p("has_modes", "## Modes" in text or "## Mode" in text or "## Core Position" in text)

def test_has_do_not():
    with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return _p("has_do_not", "Do not" in text or "do-not" in text or "Must not" in text)

def test_no_secrets():
    SECRET_PATTERNS = [
        r"sk-[A-Za-z0-9]{20,}",
        r"sk-[A-Za-z0-9][A-Za-z0-9-]{19,}",
        r"AKIA[A-Z0-9]{16}",
        r"ghp_[A-Za-z0-9]{36}",
        r"(?i)api[_-]?key\s*[=:]\s*['\"]?[A-Za-z0-9_-]{20,}",
    ]
    skill_path = os.path.dirname(os.path.abspath(__file__))
    passed = True
    for root, dirs, files in os.walk(skill_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and "installed_skills" not in d]
        for fname in files:
            if fname.startswith("."):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                continue
            for pat in SECRET_PATTERNS:
                if re.search(pat, content):
                    rel = os.path.relpath(fpath, skill_path)
                    print(f"  \u274c FAIL -- secret found: {rel}")
                    passed = False
                    break
    return _p('no_secrets', passed)

def test_scripts_shebangs():
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    if not os.path.isdir(scripts_dir):
        return _p("scripts_shebangs_skipped", True, " (no scripts/ dir)")
    passed = True
    for fname in os.listdir(scripts_dir):
        if fname.startswith("."):
            continue
        if fname.endswith((".py", ".sh")):
            fpath = os.path.join(scripts_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    first = f.read(10)
                if not first.startswith("#!"):
                    print(f"  \u274c FAIL -- missing shebang: scripts/{fname}")
                    passed = False
            except Exception:
                pass
    return _p('scripts_have_shebangs', passed)

def test_skill_md_size():
    with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    line_count = content.count('\n') + 1
    if line_count <= 400:
        hint = "\u2705 good"
    elif line_count <= 800:
        hint = "\u26a0\ufe0f consider extracting to references/"
    else:
        hint = "\u274c too large"
    return _p('skill_md_size', line_count <= 800,
             f" ({line_count} lines -- {hint})")

def _main():
    print()
    print("=" * 60)
    print(f"  \U0001f9ea TEST SUITE -- {os.path.basename(os.path.dirname(os.path.abspath(__file__)))}")
    print("=" * 60)
    print()
    tests = [
        test_frontmatter_delimiters,
        test_frontmatter_name,
        test_frontmatter_description,
        test_frontmatter_license,
        test_frontmatter_metadata,
        test_has_modes,
        test_has_do_not,
        test_no_secrets,
        test_scripts_shebangs,
        test_skill_md_size,
    ]
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:
            print(f"  \u274c FAIL -- {t.__name__} raised {e}")
            results.append(False)
    passed = sum(results)
    total = len(results)
    print()
    print("=" * 60)
    print(f"  \U0001f4ca RESULTS: {passed}/{total} passed")
    print("=" * 60)
    if passed == total:
        print("  \u2705 ALL TESTS PASSED")
    else:
        print(f'  \u274c {total - passed} test(s) FAILED -- fix before submission')
    print()
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(_main())
