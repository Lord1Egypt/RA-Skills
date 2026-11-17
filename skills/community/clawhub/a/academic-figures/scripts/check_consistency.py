#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_consistency — 文档与能力注册表自动一致性检查（v7.1.0 主菜）。

评测建议机制化：全部「命令载体」（templates/realworld _command + 文档代码块）
× 能力注册表（_FLAG_DOMAINS 域表 + --verify/PDF 特殊规则）逐条校验；另含
CSV 旧口径残留扫描。有发现 exit 1（发车闸），全绿 exit 0。

用法：python3 scripts/check_consistency.py [--root <skill目录>]
"""
import argparse
import ast as _ast
import glob
import json
import os
import re
import sys

_D = chr(34)


def load_domains(root):
    src = open(os.path.join(root, "scripts", "af_shared.py"), encoding="utf-8").read()
    for node in _ast.walk(_ast.parse(src)):
        if isinstance(node, _ast.Assign) and any(
                isinstance(t, _ast.Name) and t.id == "_FLAG_DOMAINS" for t in node.targets):
            return _ast.literal_eval(node.value)
    raise SystemExit("FAIL: _FLAG_DOMAINS 未解析到")


def canon_domains(domains):
    out = {}
    for f, (dom, note) in domains.items():
        out[f.lstrip("-")] = (dom, note)
    return out


def check_cmd(cmd, ctype, where, domains, hits):
    for tk in re.findall(r"--[a-z][a-z0-9-]*", cmd):
        canon = tk[2:]
        if canon in domains and ctype:
            dom, _note = domains[canon]
            if ctype not in dom:
                hits.append(f"{where} ({ctype}): {tk} 域={','.join(dom)}")
    # --verify 仅 PDF：该命令行的全部 -o 输出均非 .pdf 才算违规
    if "--verify" in cmd:
        outs = [os.path.splitext(m.group(1))[1]
                for m in re.finditer(r"-o\s+(\S+)", cmd)]
        if outs and all(o != ".pdf" for o in outs):
            hits.append(f"{where} ({ctype}): --verify 但输出均非 PDF（{outs[0] or '无'}）")


def scan(root):
    domains = canon_domains(load_domains(root))
    os.chdir(root)
    hits = []
    n_cmds = 0
    # 1) 模板/realworld _command
    for tf in sorted(glob.glob("templates/*.json")) + sorted(glob.glob("examples/realworld/*.json")):
        d = json.load(open(tf))
        cmd = d.get("_command", "")
        if not cmd:
            continue
        n_cmds += 1
        ctype = d.get("type") or d.get("chart")
        check_cmd(cmd, ctype, os.path.basename(tf), domains, hits)
    # 2) 文档代码块命令（含 gen_figure 调用的行；反斜杠续行跨行聚合——
    #    v7.1.0 漏网实锤：scenario-cards 卡1 `-t bar ... \` 与 `--stats auto`
    #    分居两行，单行提取使域检查逃逸（评测 accuracy 4.6 命中））
    docs = sorted(glob.glob("references/*.md")) + ["SKILL.md", "SKILL_ZH.md", "README.md"]
    for md in docs:
        if not os.path.exists(md):
            continue
        raw = open(md, encoding="utf-8").read().split("\n")
        i = 0
        while i < len(raw):
            line = raw[i]
            if "gen_figure" not in line:
                i += 1
                continue
            full = line
            j = i
            while full.rstrip().endswith("\\") and j + 1 < len(raw):
                j += 1
                full = full.rstrip()[:-1] + " " + raw[j]
            m = re.search(r"-t\s+(\S+)", full)
            if m:
                n_cmds += 1
                ctype = m.group(1).strip("`\"'")
                check_cmd(full, ctype, f"{md}:{i+1}", domains, hits)
            i = j + 1
    # 3) CSV 旧口径残留（v6.0 后缀列已实现，禁再说「CSV 不支持误差棒」）
    _STALE = re.compile(
        r"CSV 不支持误差棒|CSV 不支持 errors|误差棒需 JSON errors 字段"
        r"|does not support errors|error bars? require JSON")
    _SCAN_DOCS = docs + ["references/antipatterns.md"]
    for md in _SCAN_DOCS:
        if not os.path.exists(md):
            continue
        for i, line in enumerate(open(md, encoding="utf-8").read().split("\n"), 1):
            if _STALE.search(line):
                hits.append(f"{md}:{i}: CSV 误差旧口径残留（v6.0 起后缀列已支持）")
    # 3b) v7.2.0：引擎源码运行时文案入扫描面（CHART_NOTES 等 --explain 输出
    # 手写字典是历史漂移重灾区——v7.2.0 前的准确性审查抓到 af_shared 旧文案）
    for py in sorted(glob.glob("scripts/*.py")):
        if os.path.basename(py) == "check_consistency.py":
            continue  # 本扫描器自身含禁词模式字面量
        for i, line in enumerate(open(py, encoding="utf-8").read().split("\n"), 1):
            s = line.strip()
            if s.startswith("#") or s.startswith('''"""'''):
                continue  # 注释/docstring 属历史描述，非运行时文案
            if _STALE.search(line):
                hits.append(f"{py}:{i}: 引擎文案 CSV 旧口径残留（--explain 运行时输出）")
    # 3c) v7.2.1：changelog 主文件（平台详情页展示面）禁评测导向表述
    # （7.2.0 安全审核未过的直接暴露面；changelog-full 历史档豁免不回改）
    _DEFAULT_BANNED = ("直击官方评测", "主靶", "扣分项", "对齐官方评测", "official-eval",
                       "评测失分", "全家桶", "评测抓到", "评测点名", "官方评测",
                       "评测导向", "evaluation-caught", "evaluation caught")
    _bf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banned_af.txt")
    try:
        _words = [l.strip() for l in open(_bf, encoding="utf-8")
                  if l.strip() and not l.strip().startswith("#")]
    except OSError:
        _words = list(_DEFAULT_BANNED)  # 词表缺失回退内置默认
    _EV = re.compile("|".join(re.escape(w) for w in _words))
    _cl = open("references/changelog.md", encoding="utf-8").read()
    for i, line in enumerate(_cl.split("\n"), 1):
        if _EV.search(line):
            hits.append(f"references/changelog.md:{i}: 评测导向表述（平台详情页展示面禁令）")
    # 3d) v7.7.1：主题色板「（默认）」标记唯一性+真值一致——v7.6 默认切 glm-brand
    # 时 glm 行漏改且扫描器盲区（--list-themes 会把 agent 引导回旧默认）。AST 提取
    # THEME_SWATCH_DESCRIPTIONS 与 resolve_theme(None) 首个字面返回值机械对拍。
    try:
        import ast as _ast
        _gf = "scripts/gen_figure.py"
        _tree = _ast.parse(open(_gf, encoding="utf-8").read())
        _swatch, _default_ret, _aliases, _order = None, None, None, None
        for _node in _tree.body:
            if isinstance(_node, _ast.FunctionDef) and _node.name == "resolve_theme":
                for _n2 in _ast.walk(_node):
                    if isinstance(_n2, _ast.Return) and isinstance(_n2.value, _ast.Constant) \
                            and isinstance(_n2.value.value, str):
                        _default_ret = _n2.value.value
                        break
            if isinstance(_node, _ast.Assign) and any(
                    isinstance(_t, _ast.Name) and _t.id == "THEME_SWATCH_DESCRIPTIONS"
                    for _t in _node.targets) and isinstance(_node.value, _ast.Dict):
                _swatch = {k.value: v.value for k, v in
                           zip(_node.value.keys, _node.value.values)
                           if isinstance(k, _ast.Constant) and isinstance(v, _ast.Constant)}
            if isinstance(_node, _ast.Assign) and any(
                    isinstance(_t, _ast.Name) and _t.id == "THEME_ALIASES"
                    for _t in _node.targets) and isinstance(_node.value, _ast.Dict):
                _aliases = {k.value: v.value for k, v in
                            zip(_node.value.keys, _node.value.values)
                            if isinstance(k, _ast.Constant) and isinstance(v, _ast.Constant)}
            if isinstance(_node, _ast.Assign) and any(
                    isinstance(_t, _ast.Name) and _t.id == "THEME_ORDER"
                    for _t in _node.targets) and isinstance(_node.value, _ast.List):
                _order = [e.value for e in _node.value.elts if isinstance(e, _ast.Constant)]
        if _swatch and _default_ret:
            _marked = [k for k, v in _swatch.items() if "（默认）" in str(v)]
            if len(_marked) != 1:
                hits.append(f"{_gf}: THEME_SWATCH_DESCRIPTIONS「（默认）」标记 "
                            f"{len(_marked)} 处（应恰 1 处=引擎默认主题）")
            elif _marked[0] != _default_ret:
                hits.append(f"{_gf}: 默认标记在 '{_marked[0]}'，但 resolve_theme(None)="
                            f"'{_default_ret}'——主题默认声明不一致")
            if _aliases is not None and _aliases.get("default") != _default_ret:
                hits.append(f"{_gf}: --theme default 别名解析为 "
                            f"'{_aliases.get('default')}'，但引擎默认是 '{_default_ret}'")
            if _order is not None and _default_ret not in _order:
                hits.append(f"{_gf}: THEME_ORDER 不含默认主题 '{_default_ret}'"
                            "（--list-themes 将缺席默认项）")
    except (OSError, SyntaxError):
        pass  # gen_figure.py 缺失/异常态容错（镜像最小树）
    return n_cmds, hits


def main():
    ap = argparse.ArgumentParser(description="文档与能力注册表一致性检查")
    ap.add_argument("--root", default=None, help="skill 目录（默认=脚本上级）")
    args = ap.parse_args()
    root = args.root or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    n_cmds, hits = scan(root)
    print(f"[check-consistency] 扫描 {n_cmds} 条命令载体 + 文档口径")
    if hits:
        for h in hits:
            print("DOMAIN-X:", h)
        print(f"FAIL: {len(hits)} 处不一致")
        sys.exit(1)
    print("CONSISTENCY OK: 命令与旗标域全对齐，CSV 口径零残留")


if __name__ == "__main__":
    main()
