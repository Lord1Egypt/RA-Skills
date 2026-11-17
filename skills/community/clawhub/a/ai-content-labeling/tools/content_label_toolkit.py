#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
content_label_toolkit.py — AI 内容标识合规本地工具包
仅使用 Python 标准库，零网络、零数据采集。

命令：
  must      --content "<内容/服务描述>"   标识义务判定（中欧）
  checklist --scene <text|image|audio|video|virtual|app>   合规检查清单
  metadata  --type <text|image|audio|video|virtual>   隐式标识元数据字段模板（JSON）
  compare                        中欧要求对照
  audit                          违规风险与整改自查
  --help                         查看帮助
"""

import argparse
import json
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------- must

MUST_RULES = [
    ("生成", "图片", "中国：图片显式标识（角标提示）+ 隐式标识（EXIF/水印）"),
    ("生成", "视频", "中国：起始画面+播放周边显式提示 + 隐式标识；欧盟：深度伪造标识+机器可读标记"),
    ("生成", "音频", "中国：语音提示/节奏提示 + 隐式标识（ID3/水印）"),
    ("生成", "文本", "中国：文本提示或符号提示 + 隐式标识；欧盟：AI 文本披露（公共利益相关）"),
    ("虚拟场景", "", "中国：起始画面提示 + 隐式标识"),
    ("聊天机器人", "", "欧盟：必须告知正在与 AI 互动（无过渡期）"),
    ("聊天", "", "欧盟：交互式 AI 须告知 AI 身份（2026-08-02 起）"),
    ("客服", "", "欧盟：交互式 AI 须告知 AI 身份；中国：生成回复内容需标识（如适用）"),
    ("深度伪造", "", "欧盟：清晰披露 + 机器可读标记（2026-08-02 起）"),
    ("合成", "", "中国：显式+隐式双标识（2025-09-01 起强制）"),
]


def must(content):
    if not content or not content.strip():
        print("错误：--content 不能为空。示例：--content \"用AI生成的产品宣传图片，发到公众号\"")
        return 2
    print("=" * 62)
    print("标识义务判定（中欧）")
    print("=" * 62)
    print(f"内容/服务：{content}")
    print("-" * 62)
    hit = False
    for kw, sub, rule in MUST_RULES:
        if kw in content and (not sub or sub in content):
            hit = True
            print(f"  🔖 [{kw}{('+'+sub) if sub else ''}] → {rule}")
    if not hit:
        print("  未命中明确标识义务关键词——请对照 01 模块判定（是否对外发布/是否 AI 生成合成）。")
    print("-" * 62)
    print("快速建议：对外发布 AI 生成内容一律按『显式+隐式』双标识执行（中国），")
    print("面向欧盟用户再加机器可读标记与 AI 交互告知（欧盟 Article 50）。")
    return 0


# ---------------------------------------------------------------- checklist

CHECKLISTS = {
    "text": [
        "文本起始/末尾/中间加文字提示或通用符号提示（如「AI生成」/⚠️）",
        "交互界面/文字周边加显著提示标识（如固定提示条）",
        "文本文件元数据写入隐式标识（生成属性/服务商编码/内容编号）",
        "下载/导出文件含显式标识",
    ],
    "image": [
        "图片适当位置加显著提示标识（角标水印）",
        "图像元数据（EXIF/XMP/IPTC）写入隐式标识",
        "叠加数字水印（增强抗剥离，可选但推荐）",
        "下载/导出文件含显式标识",
    ],
    "audio": [
        "音频起始/末尾/中间添加语音提示或节奏提示",
        "交互界面加显著提示",
        "音频元数据（ID3 等）写入隐式标识",
        "音频水印（可选）",
        "下载/导出文件含显式标识",
    ],
    "video": [
        "视频起始画面 + 播放周边加显著提示标识",
        "可末尾/中间适当位置加提示",
        "视频容器元数据写入隐式标识 + 帧内水印（可选）",
        "下载/导出文件含显式标识",
    ],
    "virtual": [
        "虚拟场景起始画面加显著提示标识",
        "持续服务过程中适当位置加提示（可选）",
        "场景数据元数据写入隐式标识",
    ],
    "app": [
        "上架审核：说明是否提供 AI 生成合成服务",
        "提供者提交生成合成内容标识相关材料",
        "服务协议中写明标识方法/样式规范",
        "提供无显式标识内容时留存用户/提供对象日志（≥6 个月）",
        "对外生成内容：显式+隐式双标识落地",
        "欧盟市场：AI 交互告知 + 机器可读标记",
    ],
}

SCENE_NAMES = {"text": "文本", "image": "图片", "audio": "音频", "video": "视频", "virtual": "虚拟场景", "app": "应用/服务"}


def checklist(scene):
    if scene not in CHECKLISTS:
        print("错误：--scene 仅支持 text/image/audio/video/virtual/app。")
        return 2
    print(f"{'=' * 62}")
    print(f"{SCENE_NAMES[scene]} 标识合规检查清单")
    print(f"{'=' * 62}")
    for i, s in enumerate(CHECKLISTS[scene], 1):
        print(f"  [ ] {i}. {s}")
    print("\n[说明] 详细做法见 02/04 模块；隐式标识技术方案见 05 模块。")
    return 0


# ---------------------------------------------------------------- metadata

METADATA_FIELDS = [
    ("content_attribute", "生成合成内容属性信息", "ai_generated"),
    ("provider_name", "服务提供者名称或编码", "Provider-Code-001"),
    ("content_id", "内容编号", "GEN-20260827-0001"),
    ("generated_at", "生成时间", "2026-08-27T16:00:00+08:00"),
    ("label_version", "标识方案版本", "1.0"),
    ("modality", "内容类型", ""),
]


def metadata(mtype):
    if mtype not in {"text", "image", "audio", "video", "virtual"}:
        print("错误：--type 仅支持 text/image/audio/video/virtual。")
        return 2
    obj = {f: (v if f != "modality" else mtype) for f, _, v in METADATA_FIELDS}
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    print(f"\n[说明] 中国隐式标识核心字段（{SCENE_NAMES[mtype]}）；欧盟机器可读标记可复用同一套字段。")
    print("       完整字段定义与实现见 05 模块。")
    return 0


# ---------------------------------------------------------------- compare

def compare():
    print("=" * 66)
    print("中国 vs 欧盟 AI 内容标识要求对照")
    print("=" * 66)
    print(f"{'维度':<14s} {'中国（标识办法）':<24s} {'欧盟（AI Act 50条）':<24s}")
    print("-" * 66)
    rows = [
        ("生效时间", "2025-09-01", "2026-08-02（旧系统 12-02 过渡）"),
        ("用户可感知标识", "显式标识（文字/声音/图形）", "深度伪造披露/交互告知"),
        ("机器可读标识", "隐式标识（元数据/水印）", "机器可读标记"),
        ("内容范围", "文本/图片/音频/视频/虚拟场景", "合成内容/深度伪造/交互"),
        ("义务主体", "服务商+平台+用户", "提供者+部署者"),
        ("App 上架", "须说明并提交标识材料", "（DSA 平台额外要求）"),
        ("执法", "网信/工信/公安/广电", "成员国市场监督机构"),
        ("罚款/后果", "责令整改/约谈/处罚", "1500 万欧 或 3% 营业额"),
    ]
    for dim, cn, eu in rows:
        print(f"{dim:<14s} {cn:<24s} {eu:<24s}")
    print("-" * 66)
    print("复用策略：一套显式标识组件 + 元数据/水印方案，两区域分别映射（见 03/05 模块）。")
    return 0


# ---------------------------------------------------------------- audit

AUDIT_ITEMS = [
    "盘点：所有对外 AI 生成内容与 AI 服务（App/接口/平台）",
    "判义务：逐类判定是否需标识（must 命令）",
    "补显式：各类内容显式标识落地（04 模块）",
    "补隐式：元数据/水印接入（05 模块）",
    "补链路：下载/复制/导出文件含标识",
    "补平台：核验+三档提示+用户声明功能（06 模块）",
    "补上架：App 商店提交标识材料",
    "建机制：生成管线接入标识 SDK，产出即标",
    "留日志：无显式标识内容服务日志 ≥6 个月",
    "测抗性：转码/剥离测试（元数据+水印双轨）",
]


def audit():
    print("=" * 62)
    print("AI 内容标识合规整改自查清单")
    print("=" * 62)
    for i, s in enumerate(AUDIT_ITEMS, 1):
        print(f"  [ ] {i}. {s}")
    print("\n[说明] 逐项自查并留痕；违规风险与整改流程见 07 模块。")
    return 0


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        prog="content_label_toolkit",
        description=f"AI 内容标识合规本地工具包 v{VERSION}（零网络、零数据采集，仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_must = sub.add_parser("must", help="标识义务判定")
    p_must.add_argument("--content", required=True, help="内容/服务描述")

    p_cl = sub.add_parser("checklist", help="合规检查清单")
    p_cl.add_argument("--scene", required=True, choices=["text", "image", "audio", "video", "virtual", "app"],
                      help="text/image/audio/video/virtual/app")

    p_md = sub.add_parser("metadata", help="隐式标识元数据模板")
    p_md.add_argument("--type", required=True, choices=["text", "image", "audio", "video", "virtual"],
                      help="内容类型")

    sub.add_parser("compare", help="中欧要求对照")
    sub.add_parser("audit", help="违规整改自查")

    args = parser.parse_args()

    if args.command == "must":
        return must(args.content)
    if args.command == "checklist":
        return checklist(args.scene)
    if args.command == "metadata":
        return metadata(args.type)
    if args.command == "compare":
        return compare()
    if args.command == "audit":
        return audit()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
