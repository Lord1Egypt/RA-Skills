#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ecosystem-auditor —— 技能生态健康度审计

扫描技能生态（默认 ~/.workbuddy/skills），对每枚技能做体检：
  - frontmatter 合法性（YAML 前置含 name/description）
  - 脚本可编译性（scripts/*.py 经 py_compile）
  - 陈旧度（最后修改距今超过 stale_days）
  - 近重复（SKILL.md 正文 shingle Jaccard >= dup_threshold）
  - 孤儿 meta（meta-X 但教师 X 不存在）
输出结构化健康报告（JSON）+ 人类摘要，供元进化引擎定位"该修/该并/该弃"的技能。

纯标准库；`python ecosystem_auditor.py --selftest` 跑内置断言（自建临时沙箱，无副作用）。
"""
import argparse
import json
import os
import py_compile
import shutil
import sys
import tempfile
import time

sys.dont_write_bytecode = True  # 审计时不向技能目录写入 __pycache__/*.pyc


def _shingles(text, k=4):
    t = "".join(text.lower().split())
    return set(t[i:i + k] for i in range(max(0, len(t) - k + 1)))


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def check_frontmatter(path):
    try:
        body = open(path, encoding="utf-8").read()
    except Exception:
        return False, "不可读"
    if not body.startswith("---"):
        return False, "缺少 YAML 前置（未以 --- 开头）"
    end = body.find("\n---", 3)
    if end == -1:
        return False, "YAML 前置未闭合"
    fm = body[3:end]
    if "name:" not in fm or "description:" not in fm:
        return False, "前置缺少 name 或 description"
    return True, ""


def audit_skill(sdir):
    """对单个技能目录体检，返回问题清单（空=健康）。"""
    issues = []
    skill_md = os.path.join(sdir, "SKILL.md")
    if not os.path.isfile(skill_md):
        issues.append("missing_skillmd")
    else:
        ok, msg = check_frontmatter(skill_md)
        if not ok:
            issues.append("bad_frontmatter:" + msg)
    # 脚本编译（内存编译，零文件副作用，不写 __pycache__）
    sdir_scripts = os.path.join(sdir, "scripts")
    if os.path.isdir(sdir_scripts):
        for f in os.listdir(sdir_scripts):
            if f.endswith(".py"):
                try:
                    src = open(os.path.join(sdir_scripts, f), encoding="utf-8").read()
                    compile(src, f, "exec")
                except SyntaxError as e:
                    issues.append("syntax_error:" + f + ":" + (str(e)[:60]))
    return issues


def audit(skills_root, stale_days=120, dup_threshold=0.9):
    """扫描生态，返回完整报告。"""
    skills = {}
    for name in sorted(os.listdir(skills_root)):
        sd = os.path.join(skills_root, name)
        if not os.path.isdir(sd):
            continue
        if name.startswith("_"):
            continue
        skills[name] = sd

    now = time.time()
    report = {"root": skills_root, "healthy": [], "broken": [], "stale": [],
              "duplicates": [], "orphans": [], "detail": {}}
    bodies = {}
    for name, sd in skills.items():
        issues = audit_skill(sd)
        detail = {"issues": issues}
        # 陈旧度（排除 __pycache__/*.pyc，避免编译产物干扰 mtime）
        try:
            def _walk_files(sd):
                for r, dirs, fs in os.walk(sd):
                    if "__pycache__" in r.split(os.sep):
                        continue
                    for f in fs:
                        if f.endswith(".pyc"):
                            continue
                        yield os.path.join(r, f)
            mtime = max((os.path.getmtime(p) for p in _walk_files(sd)), default=0)
            age_days = (now - mtime) / 86400
            detail["age_days"] = round(age_days, 1)
            if age_days > stale_days:
                report["stale"].append(name)
        except Exception:
            pass
        # 孤儿 meta
        if name.startswith("meta-"):
            teacher = name[5:].replace("-", "_")
            if not os.path.isdir(os.path.join(skills_root, teacher)):
                report["orphans"].append(name)
                detail["orphan_teacher"] = teacher
        # 正文收集（去重检测）
        md = os.path.join(sd, "SKILL.md")
        if os.path.isfile(md):
            bodies[name] = _shingles(open(md, encoding="utf-8").read())
        if issues:
            report["broken"].append(name)
        else:
            report["healthy"].append(name)
        report["detail"][name] = detail

    # 近重复（两两 Jaccard）
    names = list(bodies)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            jc = _jaccard(bodies[names[i]], bodies[names[j]])
            if jc >= dup_threshold:
                report["duplicates"].append({"a": names[i], "b": names[j], "jaccard": round(jc, 3)})
    report["summary"] = {
        "total": len(skills),
        "healthy": len(report["healthy"]),
        "broken": len(report["broken"]),
        "stale": len(report["stale"]),
        "duplicates": len(report["duplicates"]),
        "orphans": len(report["orphans"]),
    }
    return report


def selftest():
    print("== ecosystem-auditor selftest ==")
    tmp = tempfile.mkdtemp(prefix="eco_audit_")
    try:
        old = time.time() - 200 * 86400

        def mk(name, body, py=None, mtime=None):
            d = os.path.join(tmp, name)
            os.makedirs(os.path.join(d, "scripts"), exist_ok=True)
            open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(body)
            if py is not None:
                open(os.path.join(d, "scripts", "m.py"), "w", encoding="utf-8").write(py)
            if mtime is not None:
                for r, _, fs in os.walk(d):
                    for f in fs:
                        os.utime(os.path.join(r, f), (mtime, mtime))

        good = "---\nname: good\ndescription: ok\n---\n# Good\n正文内容用于去重检测A。\n"
        mk("good_skill", good, py="def f():\n    return 1\n")
        mk("broken_fm", "# 没有前置\n正文B。\n")
        mk("broken_py", good.replace("good", "broken_py"), py="def f(:\n    return\n")  # 语法错
        mk("stale_skill", good.replace("Good", "Stale"), py="def f():\n    return 2\n", mtime=old)
        dup_a = "---\nname: dup_a\ndescription: ok\n---\n# Dup\n这是一段会被判为近重复的长正文用于测试去重逻辑是否生效。第二段落提供更多共享内容以提升重合度确保被判定为近重复样本。\n"
        dup_b = "---\nname: dup_b\ndescription: ok\n---\n# Dup\n这是一段会被判为近重复的长正文用于测试去重逻辑是否生效。第二段落提供更多共享内容以提升重合度确保被判定为近重复样本。\n"
        mk("dup_a", dup_a)
        mk("dup_b", dup_b)
        mk("meta-ghost", "---\nname: meta-ghost\ndescription: ok\n---\n# Ghost\n孤儿meta测试。\n")

        rep = audit(tmp, stale_days=120, dup_threshold=0.9)
        assert "broken_fm" in rep["broken"], rep["broken"]
        assert any("broken_py" in b for b in rep["broken"]), rep["broken"]
        assert "stale_skill" in rep["stale"], rep["stale"]
        assert "good_skill" in rep["healthy"], rep["healthy"]
        assert any(d["a"] == "dup_a" and d["b"] == "dup_b" for d in rep["duplicates"]), rep["duplicates"]
        assert "meta-ghost" in rep["orphans"], rep["orphans"]
        print("  [1] 坏frontmatter/语法错/陈旧/近重复/孤儿meta 全部检出  PASS")
        print("  summary:", rep["summary"])
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="技能生态健康度审计")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=os.path.expanduser("~/.workbuddy/skills"))
    ap.add_argument("--stale-days", type=int, default=120)
    ap.add_argument("--json", action="store_true", help="仅输出 JSON")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    rep = audit(args.root, stale_days=args.stale_days)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        s = rep["summary"]
        print(f"技能生态审计（{args.root}）：共 {s['total']} 枚")
        print(f"  健康 {s['healthy']} ｜ 损坏 {s['broken']} ｜ 陈旧 {s['stale']} ｜ 近重复 {s['duplicates']} ｜ 孤儿meta {s['orphans']}")
        if rep["broken"]:
            print("  损坏：", rep["broken"])
        if rep["orphans"]:
            print("  孤儿meta：", rep["orphans"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
