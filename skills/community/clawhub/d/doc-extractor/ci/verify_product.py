#!/usr/bin/env python3
"""
verify_product.py - portfolio verification harness (7-axis check per product).

Run from a product folder (or pass folders). Checks:
  1. structure   - SKILL.md + (a .py tool OR an external-tool skill: requirements.txt / install note)
  2. frontmatter - name/version/description in SKILL.md
  3. compiles    - every .py compiles (py_compile)
  4. self-test   - a declared test passes:
                     (a) any .py exposes `self-test` and it passes, OR
                     (b) a test_*.py / *_test.py exists and passes, OR
                     (c) SKILL.md declares a `test:` instruction (external-tool skill)
  5. security    - no HARDCODED secrets (key=value with real value)
  6. docs        - SKILL.md has Usage/Why/Example section
  7. deploy-ready- ci/ci_check.py passes (frontmatter + tool/structure)
Exits non-zero if any axis fails. Stdlib only. Used by CI and locally.

Usage:
  python verify_product.py [folder ...]     # default: cwd
"""
import os
import re
import sys
import subprocess

REQ = ["name", "version", "description"]
SECRET = re.compile(r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{8,}', re.I)
INSTALL = re.compile(r'(?i)(pip install|npm i|requirements\.txt|brew install|go install|cargo install)', re.I)


def axis(ok, name):
    print(("  PASS" if ok else "  FAIL") + f" - {name}")
    return bool(ok)


def has_self_test(fp):
    r = subprocess.run([sys.executable, fp, "self-test"], capture_output=True, text=True, timeout=30)
    return r.returncode == 0 and "PASS" in r.stdout


def verify(folder):
    print(f"== verify: {os.path.basename(folder)} ==")
    all_ok = True
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".py")]
    skill = os.path.join(folder, "SKILL.md")
    skill_txt = open(skill, encoding="utf-8").read() if os.path.isfile(skill) else ""
    has_install = bool(INSTALL.search(skill_txt))
    is_external = has_install or os.path.isfile(os.path.join(folder, "requirements.txt"))

    # 1 structure
    struct_ok = os.path.isfile(skill) and (bool(files) or is_external)
    all_ok &= axis(struct_ok, "structure (SKILL.md + .py tool OR external-tool skill)")
    # 2 frontmatter
    if os.path.isfile(skill):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", skill_txt, re.S)
        fm_ok = bool(m)
        if m:
            for k in REQ:
                fm_ok &= bool(re.search(rf"^{k}\s*:", m.group(1), re.M))
        all_ok &= axis(fm_ok, "frontmatter (name/version/description)")
        all_ok &= axis(bool(re.search(r"(?i)(usage|why|example)", skill_txt)),
                          "docs (Usage/Why/Example present)")
    else:
        all_ok &= axis(False, "frontmatter (no SKILL.md)")
        all_ok &= axis(False, "docs (no SKILL.md)")
    # 3 compiles
    comp_ok = all(subprocess.run([sys.executable, "-m", "py_compile", fp],
                                capture_output=True).returncode == 0 for fp in files)
    all_ok &= axis(comp_ok, "compiles (py_compile all .py)")
    # 4 self-test (any of 3 valid forms)
    st_ok = False
    st_note = ""
    if any(has_self_test(fp) for fp in files):
        st_ok, st_note = True, "self-test subcommand"
    else:
        tests = [os.path.join(folder, f) for f in os.listdir(folder)
                 if (f.startswith("test_") or f.endswith("_test.py")) and f.endswith(".py")]
        if tests:
            st_ok = all(subprocess.run([sys.executable, t], capture_output=True, text=True,
                                      timeout=30).returncode == 0 for t in tests)
            st_note = f"{len(tests)} test_*.py"
        elif re.search(r"(?im)^test\s*:", skill_txt):
            st_ok = True
            st_note = "test: declared in SKILL.md"
    all_ok &= axis(st_ok, f"self-test ({st_note or 'none found'})")
    # 5 security
    sec_ok = not any(SECRET.search(open(fp, encoding="utf-8", errors="ignore").read()) for fp in files)
    all_ok &= axis(sec_ok, "security (no hardcoded secret)")
    # 7 deploy-ready
    ci = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ci_check.py")
    if os.path.isfile(ci) and os.path.isfile(skill):
        r = subprocess.run([sys.executable, ci], cwd=folder, capture_output=True, text=True)
        all_ok &= axis(r.returncode == 0, "deploy-ready (ci/ci_check.py PASS)")
    else:
        all_ok &= axis(True, "deploy-ready (skipped)")
    print(("RESULT: PASS\n" if all_ok else "RESULT: FAIL\n"))
    return all_ok


def main():
    folders = [a for a in sys.argv[1:]] or [os.getcwd()]
    ok = all(verify(f) for f in folders)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
