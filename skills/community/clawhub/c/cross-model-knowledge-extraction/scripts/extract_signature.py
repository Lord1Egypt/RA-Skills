#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cross-model-knowledge-extraction: 从教师技能 SKILL.md 结构化提取能力签名。

用法:
  python extract_signature.py <教师技能目录> [--json]
  python extract_signature.py --selftest
"""
import os, re, sys, json, tempfile, shutil


def extract_signature(skill_dir):
    """读取 skill_dir/SKILL.md，返回结构化能力签名 dict。"""
    md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(md):
        raise SystemExit(f"❌ 找不到 SKILL.md: {md}")
    body = open(md, encoding="utf-8").read()

    # 显性编号工作流步骤
    steps = re.findall(r"(?m)^\s*\d+\.\s+(.+)$", body)
    # 标题层级
    headings = re.findall(r"(?m)^#{1,4}\s+(.+)$", body)
    # 触发/使用场景行
    triggers = re.findall(
        r"(?im)^\s*(?:#{1,4}\s*)?(?:触发|trigger|when|使用场景|使用时机)\b[^\n:：]*[:：]?\s*(.+)$",
        body,
    )
    # 限制/坑/失败模式段
    limits = re.findall(
        r"(?is)(?:限制|注意|caution|已知问题|失败模式|坑|风险)\b[^\n]*\n((?:.+\n){0,3})",
        body,
    )
    limits = [l.strip() for l in limits]
    # 去重（保留顺序）
    seen = set(); limits = [x for x in limits if not (x in seen or seen.add(x))]
    # 工具脚本
    scripts = sorted(os.path.basename(s) for s in
                     __import__("glob").glob(os.path.join(skill_dir, "scripts", "*.py")))
    # 可蒸馏决策规则：含 if/当...时/若/必须/则/should/must 的句子
    sents = re.split(r"(?<=[。！？\n])", body)
    rule_kw = re.compile(r"(?i)(若|如果|当.{0,8}时|则|必须|should|must|if\b.+then|除非|否则)")
    decision_rules = []
    for s in sents:
        s = s.strip()
        if 6 <= len(s) <= 200 and rule_kw.search(s):
            decision_rules.append(s)
    seen = set(); decision_rules = [x for x in decision_rules if not (x in seen or seen.add(x))][:20]

    return {
        "name": os.path.basename(os.path.normpath(skill_dir)),
        "headings": headings[:30],
        "workflow_steps": steps[:25],
        "triggers": triggers[:10],
        "limits": limits[:8],
        "scripts": scripts,
        "decision_rules": decision_rules,
        "body_size": len(body),
    }


def selftest():
    tmp = tempfile.mkdtemp(prefix="cmke_test_")
    try:
        sample = """# 示例教师技能

## 概述
用于演示知识提取。

## 触发
触发：用户要求做翻译时

## 工作流
1. 读取源文本
2. 调用模型翻译
3. 后处理校对

## 限制
注意：超过 1 万字会截断，需分批。

## 规则
若输入为空则直接返回，避免空跑。
当目标语言缺失时必须向用户追问。
"""
        os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
        open(os.path.join(tmp, "SKILL.md"), "w", encoding="utf-8").write(sample)
        open(os.path.join(tmp, "scripts", "do.py"), "w", encoding="utf-8").write("# tool\n")

        sig = extract_signature(tmp)
        assert sig["name"] == os.path.basename(tmp), f"name 错: {sig['name']}"
        assert len(sig["workflow_steps"]) == 3, f"应抽 3 步，实际 {len(sig['workflow_steps'])}: {sig['workflow_steps']}"
        assert any("翻译" in t for t in sig["triggers"]), f"触发未命中: {sig['triggers']}"
        assert any("截断" in l for l in sig["limits"]), f"限制未命中: {sig['limits']}"
        assert sig["scripts"] == ["do.py"], f"脚本错: {sig['scripts']}"
        assert any("输入为空" in r for r in sig["decision_rules"]), f"决策规则缺失: {sig['decision_rules']}"
        assert any("目标语言缺失" in r for r in sig["decision_rules"]), f"决策规则2缺失"
        print("🧪 selftest PASS：工作流=%d 触发=%d 限制=%d 脚本=%s 决策规则=%d"
              % (len(sig["workflow_steps"]), len(sig["triggers"]), len(sig["limits"]),
                 sig["scripts"], len(sig["decision_rules"])))
        return 0
    except AssertionError as e:
        print("❌ selftest FAIL:", e); return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if not args:
        raise SystemExit("用法: extract_signature.py <教师技能目录> [--selftest]")
    sig = extract_signature(args[0])
    print(json.dumps(sig, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
