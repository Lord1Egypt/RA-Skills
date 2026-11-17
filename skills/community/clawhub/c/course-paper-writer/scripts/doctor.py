#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""course-paper-writer — pre-publish doctor.

Zero-dependency. Checks a skill folder against ClawHub's most common
rejection reasons before you upload it.

    python scripts/doctor.py [skill_dir]

Scoring: any CRIT blocks the upload. Each WARN costs 8 points.
  >=90 healthy | 60..89 fix before publishing | <60 blocked
"""

import json
import os
import re
import sys

SEMVER = re.compile(r"^\d+\.\d+\.\d+([\-+][0-9A-Za-z\-.]+)?$")
SLUG_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.=]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{12,}"),
]
DIRTY_NAMES = {".git", ".DS_Store", "node_modules", "__pycache__", ".idea", ".vscode"}
DIRTY_EXTS = {".pyc", ".pyo", ".log", ".swp", ".bak", ".tmp"}
BANNED_FILES = {"LICENSE", "LICENSE.txt", "LICENSE.md"}
GENERIC_WORDS = ["general", "productivity", "various", "misc", "tool", "helper",
                 "通用", "万能", "各种", "工具", "助手"]
HIGH_RISK_TOOLS = {"exec", "shell", "sudo", "eval", "system"}

GREY = "\033[90m"
RED = "\033[31m"
YEL = "\033[33m"
GRN = "\033[32m"
RST = "\033[0m"


def color(s, c):
    return s if os.environ.get("NO_COLOR") else c + s + RST


class Result:
    def __init__(self):
        self.rows = []       # (level, label, detail)

    def crit(self, label, detail):
        self.rows.append(("CRIT", label, detail))

    def ok(self, label, detail=""):
        self.rows.append(("OK", label, detail))

    def warn(self, label, detail):
        self.rows.append(("WARN", label, detail))

    def report(self):
        for level, label, detail in self.rows:
            if level == "CRIT":
                head = color("[CRIT]", RED)
            elif level == "WARN":
                head = color("[WARN]", YEL)
            else:
                head = color("[OK  ]", GRN)
            print("%s %-22s → %s" % (head, label, detail))
        crit = sum(1 for r in self.rows if r[0] == "CRIT")
        warn = sum(1 for r in self.rows if r[0] == "WARN")
        score = 0 if crit else max(0, 100 - 8 * warn)
        if crit:
            decision = "BLOCK"
        elif score >= 90:
            decision = "PASS"
        elif score >= 60:
            decision = "FIX"
        else:
            decision = "BLOCK"
        print("─" * 58)
        print("健康分：%d/100  (CRIT %d / WARN %d)" % (score, crit, warn))
        print("发布决策：%s" % decision)
        return decision


def parse_frontmatter(text):
    """Minimal YAML frontmatter parser: flat key: value plus inline [a, b] lists."""
    if not text.startswith("---"):
        return None, None
    end = text.find("\n---", 3)
    if end < 0:
        return None, None
    block = text[3:end].strip("\n")
    body = text[end + 4:]
    meta = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            val = val.strip("'\"")
        meta[key] = val
    return meta, body


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for d in list(dirnames):
            if d in DIRTY_NAMES:
                yield os.path.join(dirpath, d), True
                dirnames.remove(d)
        for f in filenames:
            yield os.path.join(dirpath, f), False


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                           os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if not os.path.isdir(root):
        print("not a directory:", root)
        return 2

    r = Result()
    print("checking: %s\n" % root)

    # 1 — required files
    skill_md = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill_md):
        r.crit("必需文件 SKILL.md", "不存在")
        return 1 if r.report() == "BLOCK" else 0
    text = open(skill_md, encoding="utf-8", errors="replace").read()
    r.ok("必需文件 SKILL.md", "存在，%d 字符" % len(text))

    if os.path.isfile(os.path.join(root, "README.md")):
        r.ok("README.md", "存在")
    else:
        r.warn("README.md", "缺失，商店落地页会是空白")

    # 2 — frontmatter
    meta, body = parse_frontmatter(text)
    if meta is None:
        r.crit("YAML frontmatter", "缺失或未闭合（必须位于首行 --- 之间）")
        meta = {}
    else:
        missing = [k for k in ("name", "description", "version") if not meta.get(k)]
        if missing:
            r.crit("YAML frontmatter", "缺字段: %s" % ", ".join(missing))
        else:
            r.ok("YAML frontmatter",
                 "name=%s, desc=%d字" % (meta.get("name"), len(str(meta.get("description", "")))))

    name = str(meta.get("name", "")).strip()
    version = str(meta.get("version", "")).strip()
    desc = str(meta.get("description", ""))

    # 3 — slug
    slug = os.path.basename(root.rstrip("\\/"))
    cfg = os.path.join(root, "clawhub.json")
    cfg_data = {}
    if os.path.isfile(cfg):
        try:
            cfg_data = json.load(open(cfg, encoding="utf-8"))
            slug = cfg_data.get("slug") or cfg_data.get("name") or slug
            r.ok("clawhub.json", "存在，slug=%s" % slug)
        except Exception as e:
            r.crit("clawhub.json", "JSON 解析失败: %s" % e)
    else:
        r.warn("clawhub.json", "缺失，将用目录名作 slug")

    if SLUG_OK.match(str(slug)):
        r.ok("Slug 合规", slug)
    else:
        r.crit("Slug 合规", "'%s' 不合规，必须小写字母/数字 + 短横线" % slug)

    if name and name != slug:
        r.warn("name 与 slug 不一致", "name=%s slug=%s（建议统一）" % (name, slug))

    # 4 — semver
    cfg_ver = str(cfg_data.get("version", "")).strip()
    if SEMVER.match(version) and (not cfg_ver or cfg_ver == version):
        r.ok("版本号 semver", version)
    elif SEMVER.match(version):
        r.warn("版本号一致", "SKILL.md=%s clawhub.json=%s" % (version, cfg_ver))
    else:
        r.warn("版本号 semver", "'%s' 非标准 semver，建议 X.Y.Z" % version)

    # 5 — dirty files
    dirty, banned = [], []
    for path, is_dir in walk(root):
        base = os.path.basename(path)
        if base in BANNED_FILES:
            banned.append(os.path.relpath(path, root))
        if is_dir and base in DIRTY_NAMES:
            dirty.append(os.path.relpath(path, root))
        elif os.path.splitext(base)[1].lower() in DIRTY_EXTS:
            dirty.append(os.path.relpath(path, root))
    if dirty or banned:
        r.crit("污染文件清理", "检出 %d 个: %s" % (len(dirty) + len(banned),
                                          ", ".join((dirty + banned)[:6])))
    else:
        r.ok("污染文件清理", "干净")

    # 6 — secrets
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            p = os.path.join(dirpath, f)
            if os.path.getsize(p) > 2_000_000:
                continue
            try:
                content = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for pat in SECRET_PATTERNS:
                for m in pat.finditer(content):
                    hits.append("%s: %s" % (os.path.relpath(p, root), m.group(0)[:18] + "..."))
    if hits:
        r.crit("凭证泄露扫描", "硬编码密钥 %d 处: %s" % (len(hits), hits[0]))
    else:
        r.ok("凭证泄露扫描", "未发现硬编码密钥")

    # 7 — description quality
    if desc:
        low = desc.lower()
        bad = [w for w in GENERIC_WORDS if w in low]
        if bad:
            r.warn("description 触发精度", "含泛词 %s，触发率会很低" % bad)
        elif len(desc) < 20:
            r.warn("description 触发精度", "过短（%d 字），说清何时触发" % len(desc))
        elif len(desc) > 800:
            r.warn("description 长度", "%d 字过长，advertise 层建议 ≤100 tokens" % len(desc))
        else:
            r.ok("description 触发精度", "含具体触发条件，%d 字" % len(desc))

    # 8 — tools
    tools = meta.get("tools", [])
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.strip("[]").split(",") if t.strip()]
    risky = [t for t in tools if str(t).lower() in HIGH_RISK_TOOLS]
    if risky:
        r.crit("tools 高危接口", "声明了 %s，人工审核会驳回" % risky)
    elif tools:
        r.ok("tools 声明", ", ".join(tools))
    else:
        r.warn("tools 声明", "未声明，建议显式列出所需工具")

    decision = r.report()
    return 0 if decision == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
