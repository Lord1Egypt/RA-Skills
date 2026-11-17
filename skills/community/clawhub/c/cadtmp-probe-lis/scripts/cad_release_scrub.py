#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布前脱敏自检：扫描技能目录里混入的项目实测数据并可选就地打码。

判敏感的五类：结果工程量数值（带小数的实测值）、标高数值、绝对介质路径、
文件摘要串、本机阶段产物文件名。构件计数（如 42 块）与 .py 里的代码常量属方法说明，不算敏感；
语义版本号（0.12.6）、接口版本标记（v0.21）、耗时/内存标记（11.8s、94MB）、置信度/规则权重/示例参数和螺栓等级同样先摘除再判。
默认扫文档与入口脚本（.md/.txt/.sh/.json/.toml），跳过 vendor 等第三方目录。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION_TOKEN = re.compile(r'\d+\.\d+\.\d+')  # 语义版本号不是实测结果
PERF_TOKEN = re.compile(r'\d+(?:\.\d+)?\s*(?:ms|s(?![a-zA-Z])|秒|MB|GB|%)')  # 耗时/内存不是工程量
SCHEMA_VERSION = re.compile(r'[vV]\d+\.\d+(?:\.\d+)?')  # v0.21 这类接口版本是标识符
RUNTIME_VERSION = re.compile(r'(?i)(?:python|pip)[\s=/]*3\.\d+(?:\.\d+)?\+?')  # Python 3.10 这类运行环境版本不是实测结果
METHOD_TOKEN = re.compile(
    r'(?i)(?:"?(?:direct_label|pattern_match|context_match|geometry_pattern)"?\s*[:=]?\s*\d+(?:\.\d+)?'
    r'|置信度\s*[≥><]?\s*\d+(?:\.\d+)?\s*[，,]\s*[^；\n]*?\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?'
    r'|置信度[^，。；\n]*\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?'
    r'|--thickness-m\s+\d+(?:\.\d+)?'
    r'|(?:confidence_base|confidence)["\']?\s*[:=]?\s*\d+(?:\.\d+)?(?:\s*[、，,]\s*\d+(?:\.\d+)?)*' 
    r'|\b\d{1,2}\.\dS\b)'
)  # 置信度阈值、示例参数、规则权重与螺栓等级不是工程量

PATTERNS = [
    ("绝对路径", re.compile(r'/Volumes/|' + '/' + r'Users/[^/\s]+/[A-Za-z\u4e00-\u9fff]')),
    ("文件摘要", re.compile(r'\b[0-9a-f]{16,}\b')),
    ("结果数值", re.compile(r'\b\d{2,4}\.\d{2,}\b|\b\d\.\d{4}\b'
                            r'|(?<![\d./])\d{2,3}\.\d(?![\d.])'
                            r'|(?<![\d./])\d\.\d{2,3}(?![\d.])')),
    ("标高数值", re.compile(r'(?<![\d.])[-−]?[1-9]\d{0,3}\.\d{3}(?![\d.])')),
    ("阶段产物名", re.compile(r'阶段[一二三四五六七八九十]{1,4}')),
]
# 算法/规则配置键（比值、阈值等）是代码常量，不是图纸实测值，豁免“结果数值”误报。
TOLERATED_CONFIG_KEYS = ("min_insert_plant_layer_ratio", "roundish_min_aspect", "max_ring_area_ratio")


REDACTIONS = [
    (re.compile(r'/Volumes/[^\s、，）)]*'), '<介质路径>'),
    (re.compile(r'\b[0-9a-f]{16,}\b'), '〈摘要已隐去〉'),
    (re.compile(r'(?<![\d./])\d{2,3}\.\d(?![\d.])'), '〈实测〉'),
    (re.compile(r'(?<![\d./])\d\.\d{2,3}(?![\d.])'), '〈实测〉'),
    (re.compile(r'\b\d{2,4}\.\d{2,}\b'), '〈实测〉'),
    (re.compile(r'\b\d\.\d{4}\b'), '〈实测〉'),
    (re.compile(r'(?<![\d.])[-−]?[1-9]\d{0,3}\.\d{3}(?![\d.])'), '〈标高〉'),
    (re.compile(r'阶段[一二三四五六七八九十]{1,4}'), '<项目阶段产物>'),
]


def scan(files):
    findings = []
    for path in files:
        text = path.read_text(errors="ignore")
        for number, line in enumerate(text.splitlines(), 1):
            # 先把 0.12.6 / 1.4.4 这类语义版本号摘掉，避免把版本当成实测结果
            probe = METHOD_TOKEN.sub("M", PERF_TOKEN.sub("P", SCHEMA_VERSION.sub("V",
                        RUNTIME_VERSION.sub("V",
                        VERSION_TOKEN.sub("V", line)))))
            kinds = [name for name, pattern in PATTERNS if pattern.search(probe)]
            if "结果数值" in kinds and any(k in line for k in TOLERATED_CONFIG_KEYS):
                kinds.remove("结果数值")
            if kinds:
                findings.append((str(path), number, kinds, line.strip()[:120]))
    return findings


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="要检查的文件或目录")
    parser.add_argument("--ext", default=".md,.txt,.sh,.json,.toml",
                        help="扫描后缀，逗号分隔（默认只查文档与入口脚本，"
                             ".py 里的数值是代码常量，不算敏感）")
    parser.add_argument("--skip-dirs", default="vendor,__pycache__,.git,node_modules,tests",
                        help="跳过的目录名，逗号分隔")
    parser.add_argument("--apply", action="store_true", help="就地打码（默认只报告）")
    parser.add_argument("--allow", default="", help="豁免子串，逗号分隔")
    args = parser.parse_args()
    suffixes = tuple(item.strip() for item in args.ext.split(",") if item.strip())
    allow = [item.strip() for item in args.allow.split(",") if item.strip()]

    files = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_dir():
            skips = tuple(item.strip() for item in args.skip_dirs.split(",") if item.strip())
            files.extend(sorted(
                p for p in path.rglob("*")
                if p.suffix in suffixes and not allow_hit(p, allow)
                and not any(part in skips for part in p.parts)))
        elif path.exists() and not allow_hit(path, allow):
            files.append(path)

    if args.apply:
        changed = 0
        for path in files:
            text = original = path.read_text(errors="ignore")
            for pattern, repl in REDACTIONS:
                text = pattern.sub(repl, text)
            if text != original:
                path.write_text(text)
                changed += 1
        print("已打码文件 %d 个" % changed)

    findings = scan(files)
    for path, number, kinds, line in findings[:40]:
        print("%s:%d [%s] %s" % (path, number, ",".join(kinds), line))
    print("扫描 %d 个文件，命中 %d 处" % (len(files), len(findings)))
    return 1 if findings else 0


def allow_hit(path, allow):
    text = str(path)
    return any(token and token in text for token in allow)


if __name__ == "__main__":
    sys.exit(main())
