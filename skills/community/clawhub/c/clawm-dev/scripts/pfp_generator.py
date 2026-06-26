# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""MBTI 龙虾 PFP 生成器 — ASCII 字符画 + 真实图片路径。

基础龙虾骨架 + 按 MBTI 类型替换配件（帽子、眼部装饰、左右钳持有物），
生成 16 种不同风格的龙虾 PFP 字符画。同时提供真实 PFP 图片路径查询。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# ============================================================
# 组件构造工具
# ============================================================


def _hat(s: str) -> str:
    """生成帽子行，居中于约第 17 列（触角汇合点）。"""
    col = 17 - len(s) // 2
    return " " * col + s


def _lc(top: str = " . ", bot: str = " . ") -> tuple[str, str, str, str]:
    """构造左钳（4 行 x 8 字符），填入 3 字符宽的钳内物品。"""
    return (" ,---.  ", f" |{top}|==", f" |{bot}|  ", " '---'==")


def _rc(top: str = " . ", bot: str = " . ") -> tuple[str, str, str, str]:
    """构造右钳（4 行 x 8 字符），填入 3 字符宽的钳内物品。"""
    return ("  ,---. ", f"==|{top}| ", f"  |{bot}| ", "=='---' ")


# ============================================================
# 类型配件定义
# ============================================================


@dataclass(frozen=True)
class TypeParts:
    """单个 MBTI 类型的龙虾配件组合。"""

    hat: str = ""
    eyes: str = "(o)    (o)"
    left_claw: tuple[str, str, str, str] = (
        " ,---.  ",
        " | . |==",
        " | . |  ",
        " '---'==",
    )
    right_claw: tuple[str, str, str, str] = (
        "  ,---. ",
        "==| . | ",
        "  | . | ",
        "=='---' ",
    )


TYPE_PARTS: dict[str, TypeParts] = {
    # ---- 分析师 (Analysts) ----
    "INTJ": TypeParts(  # 策略家：单片眼镜 + 棋盘
        eyes="(O)    (o)",
        left_claw=_lc("#_#", "_#_"),
    ),
    "INTP": TypeParts(  # 逻辑学家：圆框眼镜 + 公式板
        eyes="{o}    {o}",
        left_claw=_lc("E=m", "c^2"),
    ),
    "ENTJ": TypeParts(  # 指挥官：头盔 + 权杖
        hat=_hat(".===."),
        left_claw=_lc(" * ", " | "),
    ),
    "ENTP": TypeParts(  # 辩论家：指天钳 + 比划钳
        left_claw=_lc(" | ", " / "),
        right_claw=_rc(" | ", " \\ "),
    ),
    # ---- 外交家 (Diplomats) ----
    "INFJ": TypeParts(  # 提倡者：兜帽 + 水晶球
        hat=_hat("/^^\\"),
        left_claw=_lc("( )", "(_)"),
    ),
    "INFP": TypeParts(  # 调停者：羽毛笔 + 星光装饰
        left_claw=_lc(" ) ", " )|"),
    ),
    "ENFJ": TypeParts(  # 主人公：花冠 + 默认张开双钳
        hat=_hat("*~*~*"),
    ),
    "ENFP": TypeParts(  # 探险家：彩色双钳
        left_claw=_lc("~*~", "*~*"),
        right_claw=_rc("~*~", "*~*"),
    ),
    # ---- 哨兵 (Sentinels) ----
    "ISTJ": TypeParts(  # 检查官：军帽 + 清单
        hat=_hat("[___]"),
        left_claw=_lc("[v]", "[v]"),
    ),
    "ISFJ": TypeParts(  # 守护者：急救箱
        left_claw=_lc(" + ", "+_+"),
    ),
    "ESTJ": TypeParts(  # 总经理：公文包
        left_claw=_lc("===", "   "),
    ),
    "ESFJ": TypeParts(  # 执政官：蛋糕
        left_claw=_lc("^v^", "___"),
    ),
    # ---- 探险家 (Explorers) ----
    "ISTP": TypeParts(  # 工匠：扳手 + 电路板
        left_claw=_lc("-Y-", " | "),
        right_claw=_rc("[=]", "[_]"),
    ),
    "ISFP": TypeParts(  # 冒险家：贝雷帽 + 画笔
        hat=_hat(".'`."),
        left_claw=_lc(" / ", "/  "),
    ),
    "ESTP": TypeParts(  # 企业家：墨镜 + 骰子
        eyes="[-]    [-]",
        left_claw=_lc("o o", " o "),
    ),
    "ESFP": TypeParts(  # 表演者：派对帽 + 麦克风
        hat=_hat("/|\\"),
        left_claw=_lc(" O ", " | "),
    ),
}


# ============================================================
# 字符画合成
# ============================================================

_types_cache: dict[str, Any] | None = None


def _load_types_json() -> dict[str, Any]:
    """加载 resources/mbti_types.json（带缓存）。"""
    global _types_cache
    if _types_cache is None:
        p = Path(__file__).resolve().parent.parent / "resources" / "mbti_types.json"
        _types_cache = json.loads(p.read_text("utf-8")) if p.exists() else {}
    return _types_cache


# ============================================================
# 图片路径
# ============================================================

_PFP_DIR = Path(__file__).resolve().parent.parent / "resources" / "mbti-pfp"
_CDN_BASE = "https://pub-statics.finchain.global/clawmbit-nft"


def get_image_path(mbti_type: str) -> Path | None:
    """返回指定 MBTI 类型的 PFP 图片绝对路径，不存在则返回 None。"""
    mbti_type = mbti_type.upper().strip()
    info = _load_types_json().get(mbti_type, {})
    filename = info.get("image")
    if filename:
        p = _PFP_DIR / filename
        if p.exists():
            return p
    # 回退：按命名约定查找
    for ext in ("png", "jpg"):
        p = _PFP_DIR / f"{mbti_type} Lobster NFT PFP.{ext}"
        if p.exists():
            return p
    return None


def get_image_url(mbti_type: str) -> str:
    """返回指定 MBTI 类型的 PFP 在线图片 URL（CDN）。"""
    return f"{_CDN_BASE}/{mbti_type.upper().strip()}.webp"


def compose(mbti_type: str) -> str:
    """合成指定 MBTI 类型的龙虾 PFP 字符画。"""
    mbti_type = mbti_type.upper().strip()
    if mbti_type not in TYPE_PARTS:
        valid = ", ".join(sorted(TYPE_PARTS))
        raise ValueError(f"Unknown type: {mbti_type}. Valid: {valid}")

    parts = TYPE_PARTS[mbti_type]
    info = _load_types_json().get(mbti_type, {})
    lc, rc = parts.left_claw, parts.right_claw

    lines: list[str] = []

    # 触角
    lines.append("              ||    ||")
    lines.append("               \\\\  //")

    # 帽子（可选）
    if parts.hat:
        lines.append(parts.hat)

    # 头部
    lines.append("          .--'    '--.")
    lines.append("         / " + parts.eyes + " \\")
    lines.append("        |    '----'    |")

    # 身体 + 左右钳（4 行）
    body = [
        "|              |",
        "|   .------.   |",
        "|   |      |   |",
        "|   '------'   |",
    ]
    for i in range(4):
        lines.append(lc[i] + body[i] + rc[i])

    # 下半身 + 尾部
    lines.append("         \\            /")
    lines.append("          '-..____.-'")
    lines.append("         / ||    || \\")
    lines.append("        /  ||    ||  \\")
    lines.append("           '--  --'")

    # 类型标签
    lines.append("")
    nickname = info.get("nickname_cn", "???")
    lines.append("       [ " + mbti_type + " | " + nickname + " ]")

    return "\n".join(line.rstrip() for line in lines)


# ============================================================
# CLI
# ============================================================


def cmd_generate(args: argparse.Namespace) -> None:
    """生成指定类型的龙虾 PFP 字符画。"""
    mbti_type = args.type.upper().strip()
    if mbti_type not in TYPE_PARTS:
        print(
            json.dumps(
                {"error": f"unknown type: {mbti_type}", "valid": sorted(TYPE_PARTS)}
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    art = compose(mbti_type)

    if args.json:
        info = _load_types_json().get(mbti_type, {})
        image_path = get_image_path(mbti_type)
        result: dict[str, Any] = {
            "type": mbti_type,
            "nickname_cn": info.get("nickname_cn", ""),
            "nickname_en": info.get("nickname_en", ""),
            "art": art,
            "image_path": str(image_path) if image_path else None,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(art)


def cmd_all(_args: argparse.Namespace) -> None:
    """生成全部 16 种类型的龙虾 PFP（预览用）。"""
    for i, mbti_type in enumerate(sorted(TYPE_PARTS)):
        if i > 0:
            print("\n" + "=" * 40 + "\n")
        print(compose(mbti_type))


def cmd_image_path(args: argparse.Namespace) -> None:
    """输出指定 MBTI 类型的 PFP 图片路径和在线 URL。"""
    mbti_type = args.type.upper().strip()
    image_path = get_image_path(mbti_type)
    image_url = get_image_url(mbti_type)

    if args.json:
        info = _load_types_json().get(mbti_type, {})
        result: dict[str, Any] = {
            "type": mbti_type,
            "image_url": image_url,
            "image_path": str(image_path) if image_path else None,
            "image_filename": image_path.name if image_path else None,
            "nickname_cn": info.get("nickname_cn", ""),
            "nickname_en": info.get("nickname_en", ""),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(image_url)


def main() -> None:
    parser = argparse.ArgumentParser(description="MBTI 龙虾 PFP 生成器")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="生成指定类型的龙虾 PFP 字符画")
    gen.add_argument("--type", required=True, help="MBTI 类型（如 INTJ、ENFP）")
    gen.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    sub.add_parser("all", help="生成全部 16 种类型（预览用）")

    img = sub.add_parser("image-path", help="获取指定类型的 PFP 图片路径")
    img.add_argument("--type", required=True, help="MBTI 类型（如 INTJ、ENFP）")
    img.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()
    commands: dict[str, Any] = {
        "generate": cmd_generate,
        "all": cmd_all,
        "image-path": cmd_image_path,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
