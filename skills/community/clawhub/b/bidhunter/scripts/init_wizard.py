#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BidHunter 首次运行引导（v2.6 · E002 攻坚）
==========================================

目标
----
把「装完面对一张白纸」压缩到 3 个问题、5 分钟内产出第一份结果。

设计原则
--------
1. **行业不设固定选项**——用户自由输入，支持直接粘贴营业执照经营范围，
   自动按分隔符拆成能力词。不预置"政府采购/建筑工程/IT设备"这类死模板，
   因为真实经营范围千差万别，选错模板比没有模板更糟。
2. **只替换该替换的**——保留 qual_rules.json 原有的红警、门禁、排除表等所有结构，
   只写入 entities 与 region_priority，避免覆盖用户已有配置。
3. **不做任何联网**——不内置真实采集源，只生成配置骨架 + 清晰的填写指引。

用法
----
    python3 init_wizard.py                 # 交互式三问
    python3 init_wizard.py --selftest      # 自检
    python3 init_wizard.py --preview       # 只看将要生成什么，不写盘

退出码
------
    0 成功  1 非交互环境无法收集  2 用户取消  3 写盘失败
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    from usage import track
except Exception:
    def track(*a, **k):
        return False

# 规则库与采集源都放在 scripts/ 下——与 status.py / doctor.py / api_server.py /
# bid_monitor.sh 的默认读取路径保持一致（全项目统一，不是 ~/.config）。
# 埋点数据则放 ~/.config，避免污染 skill 目录、也避免被打包进发布包。
RULES_PATH = Path(SCRIPT_DIR) / "qual_rules.json"
SOURCES_PATH = Path(SCRIPT_DIR) / "sources.json"
EXAMPLE_SOURCES = Path(SCRIPT_DIR) / "sources.example.json"

# 拆词分隔符：中英文逗号、顿号、分号、斜杠、竖线、空格、换行
SPLIT_RE = re.compile(r"[,，、;；/|\s\n]+")

PROMPTS = {
    "entity": "你们主体叫什么？（营业执照上的公司简称即可）",
    "industry": "主营什么？直接粘贴经营范围或写几个关键词（逗号分隔）",
    "region": "重点盯哪些地区？（逗号分隔，直接回车=全国）",
}

EXAMPLES = {
    "entity": "例：某某建筑工程有限公司",
    "industry": "例：建筑施工、市政公用工程、装饰装修、机电安装",
    "region": "例：天津、青岛、深圳",
}


def split_words(raw):
    """把自由输入拆成能力词列表，去空、去重、去过长词。"""
    if not raw:
        return []
    parts = [p.strip() for p in SPLIT_RE.split(raw)]
    out, seen = [], set()
    for p in parts:
        if not p or len(p) > 30 or p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out


def _ask(prompt, example="", default=None):
    """带示例的输入；EOF/中断时返回 default。"""
    hint = f"\n   {example}" if example else ""
    tail = f" [默认: {default}]" if default is not None else ""
    try:
        v = input(f"{prompt}{tail}{hint}\n   > ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default
    return v if v else default


def collect():
    """交互式收集三问。非交互环境返回 None。"""
    if not sys.stdin.isatty():
        return None

    print("=" * 52)
    print(" BidHunter 首次运行引导（3 个问题，约 1 分钟）")
    print("=" * 52)
    print("填完会生成你的资质规则库和采集源骨架。")
    print("随时可改：qual_rules.json / sources.json\n")

    entity = _ask(PROMPTS["entity"], EXAMPLES["entity"])
    if not entity:
        print("\n主体名称是必填项，已取消。")
        return None

    industry = _ask(PROMPTS["industry"], EXAMPLES["industry"]) or ""
    region_raw = _ask(PROMPTS["region"], EXAMPLES["region"], default="") or ""

    caps = split_words(industry)
    regions = split_words(region_raw)

    return {"entity": entity, "capabilities": caps, "regions": regions}


def build_rules(data, base=None):
    """基于现有规则库（或示例）生成新规则，只覆盖 entities 与 region_priority。"""
    rules = json.loads(json.dumps(base)) if base else _default_base()

    rules["entities"] = {
        "main": {
            "name": data["entity"],
            "capabilities": data["capabilities"],
            "note": f"由 bidhunter init 于 {datetime.now():%Y-%m-%d} 生成，"
                    f"请按营业执照核对能力词。",
        }
    }
    if "region_priority" not in rules:
        rules["region_priority"] = {}
    rules["region_priority"]["high"] = data["regions"]

    # 标记已初始化：doctor 的 E002 不再把它当示例占位
    rules["_initialized"] = True
    rules["_initialized_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules["description"] = f"{data['entity']} 资质规则（由 init 生成）"
    return rules


def _default_base():
    """没有现有规则库时的最小骨架（保留关键结构字段）。"""
    return {
        "version": "1.2",
        "_match_loose": True,
        "entities": {},
        "red_alerts": [],
        "region_priority": {"high": []},
        "industry_categories": {},
        "industry_priority": [],
        "budget_priority": {"min": None, "max": None},
    }


def build_sources():
    """生成采集源骨架。不内置任何真实源，只给结构 + 填写指引。"""
    return {
        "_note": "采集源配置。BidHunter 不内置任何真实平台源——"
                 "请按 sources.presets/ 下的模板填入你自己要监控的平台。",
        "_how": "复制 scripts/sources.presets/ 里对应平台的 .json 到本文件的 sources 数组，"
                "改掉 url 与选择器即可。",
        "_compliance": "请确认目标站点的 robots 协议与内容版权后再采集。",
        "sources": [],
    }


def write_all(data, dry_run=False):
    """写规则库与采集源骨架（先备份原文件）。返回写入路径列表。"""
    written = []

    # 规则库
    base = None
    if RULES_PATH.exists():
        try:
            base = json.loads(RULES_PATH.read_text(encoding="utf-8"))
        except Exception:
            base = None
    rules = build_rules(data, base)

    # 采集源
    if SOURCES_PATH.exists():
        try:
            sources_cfg = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
            if not isinstance(sources_cfg.get("sources"), list):
                sources_cfg["sources"] = []
        except Exception:
            sources_cfg = build_sources()
    else:
        sources_cfg = build_sources()

    if dry_run:
        return rules, sources_cfg, []

    RULES_PATH.parent.mkdir(parents=True, exist_ok=True)
    for path, obj in ((RULES_PATH, rules), (SOURCES_PATH, sources_cfg)):
        if path.exists():
            bak = path.with_suffix(path.suffix + ".bak")
            try:
                shutil.copy2(path, bak)
                written.append(str(bak))
            except Exception:
                pass
        try:
            path.write_text(
                json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            written.append(str(path))
        except Exception as e:
            print(f"[error] 写入失败 {path}: {e}", file=sys.stderr)
            return rules, sources_cfg, written
    return rules, sources_cfg, written


def run_init(dry_run=False):
    track("init_start")
    data = collect()
    if data is None:
        print("非交互环境无法运行 init 引导，请直接运行：python3 bidhunter.py init",
              file=sys.stderr)
        return 1
    if not data.get("capabilities"):
        print("\n⚠ 未填主营能力词，规则库会是空的——不过可以先跑，之后再补。")

    rules, sources, written = write_all(data, dry_run=dry_run)

    print("\n" + "=" * 52)
    if dry_run:
        print(" 预览（未写盘）")
        print("=" * 52)
        print(json.dumps(rules, ensure_ascii=False, indent=2)[:1500])
        return 0

    print(" 配置已生成")
    print("=" * 52)
    print(f"主体：{data['entity']}")
    print(f"能力词 {len(data['capabilities'])} 个："
          f"{'、'.join(data['capabilities'][:8]) or '（空）'}"
          f"{' …' if len(data['capabilities']) > 8 else ''}")
    print(f"重点地区：{'、'.join(data['regions']) or '全国（未限定）'}")
    print()
    for p in written:
        if not p.endswith(".bak"):
            print(f"  ✓ {p}")
    print("\n下一步：")
    print("  1) 跑通示例看效果：python3 bidhunter.py demo")
    print("  2) 已有招标文件？零配置直接出废标风险报告：")
    print("     python3 bidhunter.py paste <文件.pdf>")
    print("  3) 要监控平台？把 sources.presets/ 里的模板填进 sources.json")
    track("init_done")
    return 0


def selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  {'✓' if cond else '✗'} {name}")
        if not cond:
            ok = False

    print("init_wizard.py 自检")
    check("逗号拆词", split_words("建筑施工,市政工程") == ["建筑施工", "市政工程"])
    check("顿号拆词", split_words("装饰装修、机电安装") == ["装饰装修", "机电安装"])
    check("混排拆词", len(split_words("A、B, C;  D / E")) == 5)
    check("去空去重", split_words("施工,施工,,") == ["施工"])
    check("空输入安全", split_words("") == [])
    check("超长词被丢弃", split_words("x" * 40) == [])

    fake = {"entity": "测试公司", "capabilities": ["施工"], "regions": ["天津"]}
    r = build_rules(fake)
    check("生成主体名", r["entities"]["main"]["name"] == "测试公司")
    check("生成能力词", r["entities"]["main"]["capabilities"] == ["施工"])
    check("生成地区", r["region_priority"]["high"] == ["天津"])
    check("标记已初始化", r.get("_initialized") is True)
    check("无 entity_a 残留", "entity_a" not in json.dumps(r, ensure_ascii=False))

    s = build_sources()
    check("源骨架为空数组", s["sources"] == [])
    check("源骨架含合规提醒", "_compliance" in s)

    print("\n" + ("自检全部通过 ✓" if ok else "存在失败项 ✗"))
    return 0 if ok else 1


def main():
    import argparse
    ap = argparse.ArgumentParser(description="BidHunter 首次运行引导（三问生成配置）")
    ap.add_argument("--preview", action="store_true", help="只预览不写盘")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    return run_init(dry_run=args.preview)


if __name__ == "__main__":
    sys.exit(main())
