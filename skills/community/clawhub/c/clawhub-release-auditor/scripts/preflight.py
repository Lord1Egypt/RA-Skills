#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "metadata", "allowed-tools"}
PLACEHOLDER_PATTERNS = [
    re.compile(r"/path/to/", re.I),
    re.compile(r"your[-_ ]?(api[-_ ]?)?key", re.I),
    re.compile(r"example\.com", re.I),
    re.compile(r"TODO", re.I),
]
ENV_RE = re.compile(r"(?:getenv|environ\.get|environ\[)\(?['\"]([A-Z][A-Z0-9_]{2,})['\"]")
BIN_HINTS = ["uv", "uvx", "python3", "python", "node", "npm", "npx", "curl", "bash", "git", "gh", "gog", "jq", "openclaw", "clawhub"]
SKIP_PARTS = {".git", ".clawhub", "__pycache__"}
LOW_VALUE_BINS = {"python", "python3", "bash", "sh", "sed", "awk"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, "SKILL.md is missing YAML frontmatter"
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None, "SKILL.md frontmatter is not closed with ---"
    raw = parts[0][4:]
    data = {}
    current_key = None
    nested = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "":
                data[key] = {}
                nested[key] = []
            else:
                if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                    value = value[1:-1]
                data[key] = value
        elif current_key and current_key in nested:
            nested[current_key].append(line)
        else:
            return None, f"Unsupported or malformed frontmatter line: {line}"
    data["_nested"] = nested
    return data, None


def classify_placeholders(text: str):
    examples = set()
    risky = set()
    lower = text.lower()
    for pat in PLACEHOLDER_PATTERNS:
        for m in pat.finditer(text):
            token = m.group(0)
            window = lower[max(0, m.start()-80):m.end()+80]
            if any(hint in window for hint in ["example", "placeholder", "local file", "url:", "quick start", "prerequisites"]):
                examples.add(token)
            else:
                risky.add(token)
    return sorted(risky), sorted(examples)


def extract_declared(frontmatter: dict):
    raw_metadata = "\n".join(frontmatter.get("_nested", {}).get("metadata", []))
    envs = set(re.findall(r"-\s*([A-Z][A-Z0-9_]{2,})", raw_metadata))
    bins = set(re.findall(r"-\s*([a-z0-9][a-z0-9_-]*)", raw_metadata)) & set(BIN_HINTS)
    for m in re.findall(r"env:\s*\[([^\]]+)\]", raw_metadata):
        envs.update(x.strip() for x in m.split(",") if x.strip())
    for m in re.findall(r"bins:\s*\[([^\]]+)\]", raw_metadata):
        bins.update(x.strip() for x in m.split(",") if x.strip())
    homepage_match = re.search(r"homepage:\s*(\S+)", raw_metadata)
    homepage = homepage_match.group(1).strip() if homepage_match else None
    return envs, bins, homepage


def scan_codebase(skill_dir: Path):
    found_envs = set()
    found_bins = set()
    external_execs = []
    script_dirs = [skill_dir / "scripts"]
    candidates = []
    for base in script_dirs:
        if base.exists():
            candidates.extend([p for p in base.rglob("*") if p.is_file()])
    for path in candidates:
        if path.name == ".DS_Store" or any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            text = read_text(path)
        except Exception:
            continue
        for env in ENV_RE.findall(text):
            if env.startswith(("HTTP_", "PATH", "HOME", "USER", "SHELL", "TERM", "PWD", "TMP")):
                continue
            found_envs.add(env)
        lower = text.lower()
        commandish = []
        for line in text.splitlines():
            if any(token in line for token in ["subprocess", "os.system", "popen(", "run(", "cmd =", "command ="]):
                commandish.append(line.lower())
        joined = "\n".join(commandish)
        for hint in BIN_HINTS:
            if re.search(rf"(?<![\w-]){re.escape(hint)}(?![\w-])", joined):
                found_bins.add(hint)
        if any(token in lower for token in ["subprocess", "os.system", "popen("]):
            external_execs.append(str(path.relative_to(skill_dir)))
    return found_envs, found_bins, external_execs


def run_package_check(skill_dir: Path):
    cmd = ["python3", os.path.expanduser("~/project/openclaw/skills/skill-creator/scripts/package_skill.py"), str(skill_dir)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def main():
    ap = argparse.ArgumentParser(description="Preflight checker for ClawHub skill publishing")
    ap.add_argument("skill_dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    skill_dir = Path(os.path.expanduser(args.skill_dir)).resolve()
    skill_md = skill_dir / "SKILL.md"
    result = {"ok": True, "errors": [], "warnings": [], "notes": []}

    if not skill_md.exists():
        result["ok"] = False
        result["errors"].append("SKILL.md not found")
    else:
        text = read_text(skill_md)
        frontmatter, err = parse_frontmatter(text)
        if err:
            result["ok"] = False
            result["errors"].append(err)
        else:
            unknown = sorted(set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS - {"_nested"})
            if unknown:
                result["ok"] = False
                result["errors"].append(f"Unsupported frontmatter keys: {', '.join(unknown)}")
            for key in ["name", "description"]:
                if not frontmatter.get(key):
                    result["ok"] = False
                    result["errors"].append(f"Missing required frontmatter field: {key}")
            risky_placeholders, example_placeholders = classify_placeholders(text)
            if risky_placeholders:
                result["warnings"].append(f"Potentially risky placeholder text in SKILL.md: {', '.join(risky_placeholders[:8])}")
            if example_placeholders:
                result["notes"].append(f"Example placeholder text detected in SKILL.md: {', '.join(example_placeholders[:8])}")
            declared_envs, declared_bins, homepage = extract_declared(frontmatter)
            found_envs, found_bins, external_execs = scan_codebase(skill_dir)
            missing_envs = sorted(e for e in found_envs if e not in declared_envs and not e.startswith(("PYTHON", "OPENCLAW", "GITHUB_")))
            missing_bins = sorted(b for b in found_bins if b not in declared_bins and b not in LOW_VALUE_BINS)
            if missing_envs:
                result["warnings"].append("Likely undeclared env vars used in scripts: " + ", ".join(missing_envs[:12]))
            if missing_bins:
                result["warnings"].append("Likely undeclared binaries invoked by scripts: " + ", ".join(missing_bins[:12]))
            if external_execs:
                result["notes"].append("Scripts using external execution: " + ", ".join(external_execs[:10]))
            if not homepage:
                result["warnings"].append("No metadata homepage detected")
            package_rc, package_out = run_package_check(skill_dir)
            if package_rc != 0:
                result["ok"] = False
                result["errors"].append("package_skill validation failed")
                result["notes"].append(package_out[-2000:])
            else:
                result["notes"].append("package_skill validation passed")

    if not result['ok']:
        result['verdict'] = 'do-not-publish'
    elif result['warnings']:
        result['verdict'] = 'review-before-publish'
    else:
        result['verdict'] = 'ready-to-package'

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"Skill: {skill_dir}")
    print(f"Status: {'OK' if result['ok'] else 'FAIL'}")
    print(f"Verdict: {result['verdict']}")
    if result["errors"]:
        print("\nErrors:")
        for e in result["errors"]:
            print(f"- {e}")
    if result["warnings"]:
        print("\nWarnings:")
        for w in result["warnings"]:
            print(f"- {w}")
    if result["notes"]:
        print("\nNotes:")
        for n in result["notes"]:
            print(f"- {n}")
    print("\nRecommendation:")
    if result['verdict'] == 'do-not-publish':
        print('- Fix hard errors first. Do not publish yet.')
    elif result['verdict'] == 'review-before-publish':
        print('- Warnings found. Review and address them before publishing.')
        print('- To resolve: fix warnings above, then re-run: python3 scripts/preflight.py <skill-dir>')
        print('- Once clean, proceed to publish.')
    else:
        print('- Safe to package and prepare a publish confirmation step.')
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
