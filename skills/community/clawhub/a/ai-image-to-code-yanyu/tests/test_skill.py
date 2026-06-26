#!/usr/bin/env python3
"""
Auto-generated test suite for skill: user-provides-screenshot
Run with: python tests/test_skill.py
"""

import sys, os, re, yaml

def _p(name, passed, msg=''):
    emoji = "\u2705" if passed else "\u274c"
    result = "PASS" if passed else "FAIL"
    print(f"  [{emoji}] {result} -- {name}{msg}")
    return passed

def _skill_md():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'SKILL.md')

def _skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        with open(_skill_md(), "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return _p("frontmatter_delimiters", text.startswith("---"))

def test_frontmatter_name():
        fm = _frontmatter()
        if fm is None:
            return _p('frontmatter_name', False, ' -- no frontmatter')
        name = fm.get('name', '').strip()
        skill_dir = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return _p('frontmatter_name', name == skill_dir,
                 f" (got '{name}', expected '{skill_dir}')")

def test_frontmatter_name_is_kebab_case():
        fm = _frontmatter()
        if fm is None:
            return _p('name_is_kebab_case', False)
        name = fm.get('name', '')
        is_kebab = bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))
        return _p('name_is_kebab_case', is_kebab, f" (got '{name}')")

def test_frontmatter_description():
        fm = _frontmatter()
        if fm is None:
            return _p('frontmatter_description', False)
        return _p('frontmatter_description', bool(fm.get('description', '').strip()))

def test_description_has_trigger_conditions():
        fm = _frontmatter()
        if fm is None:
            return _p('description_is_trigger', False)
        desc = fm.get('description', '')
        has_trigger = ('use when' in desc.lower() or
                      re.search(r'\([0-9]+\)', desc) or
                      ('when the user' in desc.lower()))
        return _p('description_is_trigger', has_trigger,
                  ' (must be trigger condition, not capability statement)')

def test_description_length():
        fm = _frontmatter()
        if fm is None:
            return _p('description_length', False)
        desc = fm.get('description', '')
        length = len(desc.strip())
        ok = 50 <= length <= 500
        hint = 'optimal' if ok else f'{length} chars'
        return _p('description_length', ok, f' ({hint} -- optimal: 50-500)')

def test_frontmatter_license():
        fm = _frontmatter()
        if fm is None:
            return _p('frontmatter_license', False)
        lic = fm.get('license', '').strip().upper()
        return _p('frontmatter_license', lic == 'MIT' or 'MIT' in lic)

def test_frontmatter_metadata():
        fm = _frontmatter()
        if fm is None:
            return _p('frontmatter_metadata', False)
        meta = fm.get('metadata', {}) or {}
        has_version = bool(str(meta.get('version', '')).strip())
        has_category = bool(str(meta.get('category', '')).strip())
        return _p('frontmatter_metadata', has_version and has_category,
                  f' (version={has_version}, category={has_category})')

def test_has_modes():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return _p('has_modes', '## Modes' in text or '## Mode' in text or '## Core Position' in text)

def test_modes_are_distinct():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        mode_blocks = re.findall(r'^#{1,3} [^#\n].+$', text, re.MULTILINE)
        distinct = len(mode_blocks)
        return _p('modes_distinct', distinct >= 2,
                  f' ({distinct} distinct sections -- need 2+ for multi-mode)')

def test_has_do_not():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return _p('has_do_not', 'Do not' in text or 'do-not' in text or 'Must not' in text)

def test_do_not_section_has_content():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        do_not_match = re.search(r'(?i)##?\s*(do not|mandatory rules)[:\n](.+?)(?=##|\Z)', text, re.DOTALL)
        if not do_not_match:
            return _p('do_not_has_rules', False, ' (no Do not section found)')
        do_not_text = do_not_match.group(1)
        rules = re.findall(r'^\s*[-*]\s+\w', do_not_text, re.MULTILINE)
        return _p('do_not_has_rules', len(rules) >= 2,
                  f' ({len(rules)} rules -- need at least 2)')

def test_execution_steps_are_numbered():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        has_numbered = bool(re.search(r'(?:^|\n)\d+\.?\s+\w', text, re.MULTILINE))
        return _p('steps_numbered', has_numbered,
                  ' (execution steps must be numbered, not bullets or prose)')

def test_has_quality_bar():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return _p('has_quality_bar', 'Quality Bar' in text or 'quality bar' in text)

def test_quality_bar_has_criteria():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        qb_match = re.search(r'(?i)##?\s*quality bar[:\n](.+?)(?=##|\Z)', text, re.DOTALL)
        if not qb_match:
            return _p('quality_bar_has_criteria', False, ' (no Quality Bar section)')
        qb_text = qb_match.group(1).lower()
        concrete_markers = ['must have', 'must be', 'must not', 'a good output', 'a bad output',
                            'is present', 'is valid', 'returns', 'provides', 'has a']
        has_concrete = any(m in qb_text for m in concrete_markers)
        return _p('quality_bar_has_criteria', has_concrete,
                  ' (Quality Bar must have concrete observable criteria)')

def test_has_good_bad_examples():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return _p('has_good_bad_examples', 'Good' in text and 'Bad' in text)

def test_no_secrets():
        SECRET_PATTERNS = [
            r'sk-[A-Za-z0-9]{20,}',
            r'sk-[A-Za-z0-9][A-Za-z0-9-]{19,}',
            r'AKIA[A-Z0-9]{16}',
            r'ghp_[A-Za-z0-9]{36}',
            r"(?i)api[_-]?key\s*[=:]\s*['\"]?[A-Za-z0-9_-]{20,}",
        ]
        skill_path = os.path.dirname(os.path.abspath(__file__))
        passed = True
        for root, dirs, files in os.walk(skill_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'installed_skills' not in d]
            for fname in files:
                if fname.startswith('.'):
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
                        print(f'  \u274c FAIL -- secret found: {rel}')
                        passed = False
                        break
        return _p('no_secrets', passed)

def test_readme_zh_exists():
        return _p('readme_zh_exists', os.path.isfile(os.path.join(_skill_dir(), 'README_zh.md')))

def test_contributing_exists():
        return _p('contributing_exists', os.path.isfile(os.path.join(_skill_dir(), 'CONTRIBUTING.md')))

def test_gitignore_exists():
        return _p('gitignore_exists', os.path.isfile(os.path.join(_skill_dir(), '.gitignore')))

def test_tests_dir_not_empty():
        tests_dir = os.path.join(_skill_dir(), 'tests')
        if not os.path.isdir(tests_dir):
            return _p('tests_dir_not_empty', False, ' (tests/ dir missing)')
        has_tests = any(f.startswith('test_') and f.endswith('.py')
                        for f in os.listdir(tests_dir) if not f.startswith('.'))
        return _p('tests_dir_not_empty', has_tests)

def test_license_badge_in_readme():
        readme = os.path.join(_skill_dir(), 'README.md')
        if not os.path.isfile(readme):
            return _p('license_badge_in_readme', False, ' (README.md missing)')
        with open(readme, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
        has_badge = 'license' in content and ('mit' in content or 'apache' in content or 'gpl' in content)
        return _p('license_badge_in_readme', has_badge)

def test_scripts_shebangs():
        scripts_dir = os.path.join(_skill_dir(), 'scripts')
        if not os.path.isdir(scripts_dir):
            return _p('scripts_shebangs_skipped', True, ' (no scripts/ dir)')
        passed = True
        for fname in os.listdir(scripts_dir):
            if fname.startswith('.'):
                continue
            if fname.endswith(('.py', '.sh')):
                fpath = os.path.join(scripts_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        first = f.read(10)
                    if not first.startswith('#!'):
                        print(f'  \u274c FAIL -- missing shebang: scripts/{fname}')
                        passed = False
                except Exception:
                    pass
        return _p('scripts_have_shebangs', passed)

def test_skill_md_size():
        with open(_skill_md(), 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        line_count = content.count('\n') + 1
        if line_count <= 400:
            hint = '\u2705 good'
        elif line_count <= 800:
            hint = '\u26a0\ufe0f consider extracting to references/'
        else:
            hint = '\u274c too large'
        return _p('skill_md_size', line_count <= 800,
                  f' ({line_count} lines -- {hint})')

def _main():
    print()
    print("=" * 60)
    print(f"  🧪 TEST SUITE -- skill-factory")
    print("=" * 60)
    print()
    tests = [
        test_frontmatter_delimiters,
        test_frontmatter_name,
        test_frontmatter_name_is_kebab_case,
        test_frontmatter_description,
        test_description_has_trigger_conditions,
        test_description_length,
        test_frontmatter_license,
        test_frontmatter_metadata,
        test_has_modes,
        test_modes_are_distinct,
        test_has_do_not,
        test_do_not_section_has_content,
        test_execution_steps_are_numbered,
        test_has_quality_bar,
        test_quality_bar_has_criteria,
        test_has_good_bad_examples,
        test_no_secrets,
        test_readme_zh_exists,
        test_contributing_exists,
        test_gitignore_exists,
        test_tests_dir_not_empty,
        test_license_badge_in_readme,
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


def _main():
    _run_unit_tests()
    return 0
