#!/usr/bin/env python3
"""
本地违禁词检测脚本 — 基于何归明 11 类违禁词体系 + 陈晶直播违规文档
覆盖：广告法 + 抖音/小红书/视频号/快手/B站/公众号 六平台通用规则

🔗 违禁词唯一事实源：~/.workbuddy/skills/内容合规审核/references/违禁词库/
2026-10-12 架构重构：每平台独立词库文档，脚本按 --platform 加载「通用+平台」组合。

用法:
    python3 check_prohibited_words.py --content "待检测文案"
    python3 check_prohibited_words.py --file /path/to/script.md
    python3 check_prohibited_words.py --content "文案" --platform 抖音,小红书

输出: JSON 格式检测报告
"""

import json
import re
import argparse
import sys
from pathlib import Path

# ============================================================
# 违禁词库 — 从 references/违禁词库/ 目录动态解析（唯一事实源）
# 2026-10-12 重构：单文件 → 目录（通用 + 每平台独立文档）
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROHIBITED_WORDS_DIR = SCRIPT_DIR.parent / "references" / "违禁词库"

# 平台名 → 词库文件名映射（通用词库始终叠加）
PLATFORM_FILES = {
    "小红书": "小红书违禁词库.md",
    "抖音": "抖音违禁词库.md",
    "视频号": "视频号违禁词库.md",
    "快手": "快手违禁词库.md",
    "B站": "B站违禁词库.md",
    "公众号": "公众号违禁词库.md",
    "闲鱼": "闲鱼违禁词库.md",
}
GENERAL_FILE = "通用违禁词库.md"


def parse_prohibited_words_md(md_path: Path) -> dict:
    """从词库md解析出 {分类名: {level, words, suggestion}} 字典。

    解析规则（各平台文件统一格式）：
    - `## N. 类别名` 开始一个新类别
    - `**等级**：P0/P1` 指定等级（缺省 P1）
    - `**违禁词**：` 后接 bullet list（每行一个词或词组）
    - `**修正建议**：` 后接建议文本
    """
    text = md_path.read_text(encoding="utf-8")
    categories = {}

    # 按 `## N. ` 分割各分类
    parts = re.split(r'\n##\s+\d+\.\s+', text)
    for part in parts[1:]:  # parts[0] 是文件头部
        lines = part.strip().split('\n')
        category_name = lines[0].strip()
        if not category_name:
            continue

        level = "P1"
        words = []
        suggestion = ""
        collecting_words = False

        for line in lines[1:]:
            line = line.strip()
            if line.startswith('**等级**：'):
                level = line.replace('**等级**：', '').strip()
                collecting_words = False
            elif line.startswith('**违禁词**：'):
                collecting_words = True
            elif line.startswith('**修正建议**：'):
                collecting_words = False
                suggestion = line.replace('**修正建议**：', '').strip()
            elif line.startswith('- ') and collecting_words:
                word_line = line[2:].strip()
                # 每行可能用 、 分隔多个词；加粗前缀（**xx**：）先剥离
                word_line = re.sub(r'^\*\*[^*]+\*\*[：:]\s*', '', word_line)
                for word in re.split(r'[、，,；;]', word_line):
                    word = word.strip().strip('*').strip()
                    # 过滤过长短语（含括号说明的整句不是词）
                    if word and len(word) <= 20:
                        words.append(word)

        if category_name and words:
            categories[category_name] = {
                "level": level,
                "words": words,
                "suggestion": suggestion,
            }

    return categories


def load_prohibited_words(platforms: list = None) -> dict:
    """加载违禁词库：通用词库始终加载 + 各平台词库按需加载，分类名加平台前缀避免冲突。"""
    if not PROHIBITED_WORDS_DIR.exists():
        print(f"⚠️ 词库目录不存在：{PROHIBITED_WORDS_DIR}，使用内置兜底词库", file=sys.stderr)
        return _FALLBACK_PROHIBITED_WORDS

    merged = {}

    # 1. 通用词库（始终加载）
    general_path = PROHIBITED_WORDS_DIR / GENERAL_FILE
    if general_path.exists():
        try:
            for cat, cfg in parse_prohibited_words_md(general_path).items():
                merged[f"通用/{cat}"] = cfg
        except Exception as e:
            print(f"⚠️ 解析通用词库失败：{e}", file=sys.stderr)

    # 2. 平台词库（按 --platform 参数加载）
    if platforms:
        for platform in platforms:
            fname = PLATFORM_FILES.get(platform.strip())
            if not fname:
                continue
            pfile = PROHIBITED_WORDS_DIR / fname
            if pfile.exists():
                try:
                    for cat, cfg in parse_prohibited_words_md(pfile).items():
                        merged[f"{platform}/{cat}"] = cfg
                except Exception as e:
                    print(f"⚠️ 解析{platform}词库失败：{e}", file=sys.stderr)

    if not merged:
        return _FALLBACK_PROHIBITED_WORDS
    return merged


# 降级兜底词库（仅违禁词库.md不存在时启用）
_FALLBACK_PROHIBITED_WORDS = {
    "绝对化用语": {"level": "P1", "words": ["最佳", "最具", "第一", "唯一", "顶级", "完美", "100%"], "suggestion": "用主观体验替代"},
    "收益承诺": {"level": "P0", "words": ["月入", "财富自由", "稳赚", "被动收入"], "suggestion": "说过程不说结果"},
    "引流违规": {"level": "P0", "words": ["加微信", "私信我", "进群", "免费领取"], "suggestion": "用评论区聊替代"},
}


# ============================================================
# 渠道豁免 — 按发布渠道分支（2026-08-24 用户确立）
# ============================================================

CHANNEL_EXEMPT = {
    # 微信群社群发布专项：
    #  - "社群"：豁免社群自指词（社群早报/会员社群精选等）
    #  - 境外 AI 品牌名：AI 工具/资讯类社群日报常态提及这些品牌，群发渠道放行；
    #    但敏感描述词（境外AI/AI副业/AI月入/人工智能赚钱）仍按 P0 拦截，不在此豁免。
    "group": {
        "社群",
        "OpenAI", "ChatGPT", "GPT-4", "Google", "Gemini", "Anthropic",
        "Claude", "Meta", "Microsoft", "Copilot", "Perplexity", "xAI",
        "Grok", "Midjourney", "Runway", "Mistral", "Llama",
    },
}

# 安全替代表达（展示用，不检测）

SAFE_ALTERNATIVES = {
    "变现": "跑通闭环 / 拿到反馈 / 看到正循环",
    "赚钱": "产生价值 / 获得回报 / 跑通商业模式",
    "免费": "开放 / 目前不收费",
    "领取": "获取 / 拿到 / 用起来",
    "关注": "常来看看 / 蹲后续",
    "私信": "评论区聊 / 留言区见",
}

# 词边界感知匹配的特殊词（2026-09-09 修复）：
# 默认匹配是朴素子串 `word in text`，会误伤 URL slug 等长字母数字串中的子串
# （如 OPC 短链 slug `2eaovx` 含 `vx` 被 P0「引流违规」误判为假阳性）。
# 这些词改用「前后非字母数字」正则：保留「加vx / vx号 / 微信VX」等真实微信缩写拦截力，
# 同时不匹配嵌在更长字母数字 token 内的子串（如 2eaovx / 2EAOVX）。
SPECIAL_REGEX = {
    "vx": r"(?<![A-Za-z0-9])vx(?![A-Za-z0-9])",
    "VX": r"(?<![A-Za-z0-9])VX(?![A-Za-z0-9])",
}


def _match_pattern(word: str) -> str:
    """返回某违禁词的匹配正则；特殊词走词边界感知正则，其余走 re.escape 子串。"""
    return SPECIAL_REGEX.get(word, re.escape(word))


def check_content(text: str, platforms: list = None, channel: str = "default") -> dict:
    """检测文本中的违禁词

    channel: 发布渠道，用于按渠道分支豁免。
      - "default": 全量约束（敏感话题等 P0 仍硬拦）
      - "group": 微信群社群发布专项
          · 豁免 CHANNEL_EXEMPT["group"] 中的自指词（如"社群"、境外AI品牌名）
          · 敏感话题整类 P0 降级为 P1（仅提示、不拦截）
          · 其余真风险 P0（引流/收益承诺/金融/医疗/涉赌…）仍硬拦
    """
    if platforms is None:
        platforms = ["抖音", "小红书", "视频号", "快手", "B站", "公众号"]

    PROHIBITED_WORDS = load_prohibited_words(platforms)
    exempt = CHANNEL_EXEMPT.get(channel, set())

    # 社群渠道「敏感话题」降级规则（2026-09-01 用户确认·方案一）：
    #   群发场景是熟人/订阅社群，敏感话题（翻墙/ChatGPT/政策/经济危机/招商加盟等）
    #   仅作提示不拦截；其余真风险 P0（引流/收益承诺/金融/医疗/涉赌…）仍硬拦。
    #   default 渠道完全不变，维持全量 P0 硬拦。
    # 2026-10-12 目录化后分类名带 "平台/" 前缀，用 endswith 匹配。
    SENSITIVE_CATEGORY = "敏感话题"
    group_demote_sensitive = (channel == "group")

    hits = []
    p0_count = 0
    p1_count = 0

    for category, config in PROHIBITED_WORDS.items():
        for word in config["words"]:
            pattern = _match_pattern(word)
            if not re.search(pattern, text):
                continue
            if word in exempt:
                # 该渠道豁免此自指词（如微信群豁免"社群"），跳过不计违规
                continue
            # 找到所有出现位置
            positions = [m.start() for m in re.finditer(pattern, text)]
            for pos in positions:
                # 提取上下文（前后各15字）
                start = max(0, pos - 15)
                end = min(len(text), pos + len(word) + 15)
                ctx = text[start:end]
                if start > 0:
                    ctx = "..." + ctx
                if end < len(text):
                    ctx = ctx + "..."

                # 社群渠道下，敏感话题整类降级为 P1（仅提示、不拦截）
                # 2026-10-12 目录化后分类名形如 "通用/敏感话题"，用 endswith 匹配
                if group_demote_sensitive and category.endswith(SENSITIVE_CATEGORY):
                    eff_level = "P1"
                else:
                    eff_level = config["level"]

                hit = {
                    "word": word,
                    "category": category,
                    "level": eff_level,
                    "position": pos,
                    "context": ctx,
                    "suggestion": config["suggestion"],
                }
                hits.append(hit)
                if eff_level == "P0":
                    p0_count += 1
                else:
                    p1_count += 1

    # 判定结果
    if p0_count > 0:
        verdict = "❌ 不通过 — 存在 P0 级违禁词，必须修改"
    elif p1_count > 0:
        verdict = "⚠️ 需修改 — 存在 P1 级风险词，建议替换"
    else:
        verdict = "✅ 通过 — 未命中违禁词库"

    # 安全替代提示
    alternatives = {}
    for word, alt in SAFE_ALTERNATIVES.items():
        if word in text:
            alternatives[word] = alt

    return {
        "verdict": verdict,
        "total_hits": len(hits),
        "p0_count": p0_count,
        "p1_count": p1_count,
        "hits": hits,
        "alternatives": alternatives,
        "platforms_checked": platforms,
        "text_length": len(text),
    }


def format_report(result: dict, text: str = "") -> str:
    """格式化输出检测报告"""
    lines = []
    lines.append("═" * 50)
    lines.append("         📋 违禁词检测报告（本地词库）")
    lines.append("═" * 50)
    lines.append(f"")
    lines.append(f"【检测结果】{result['verdict']}")
    lines.append(f"【文本长度】{result['text_length']} 字")
    lines.append(f"【检测平台】{'、'.join(result['platforms_checked'])}")
    lines.append(f"【命中违禁词】{result['total_hits']} 个（P0: {result['p0_count']}, P1: {result['p1_count']}）")
    lines.append(f"")

    if result["hits"]:
        lines.append("【违禁词明细】")
        lines.append(f"")
        for hit in result["hits"]:
            lines.append(f"  [{hit['level']}] {hit['word']}（{hit['category']}）")
            lines.append(f"  上下文：{hit['context']}")
            lines.append(f"  💡 {hit['suggestion']}")
            lines.append(f"")

    if result["alternatives"]:
        lines.append("【安全替代表达】")
        for word, alt in result["alternatives"].items():
            lines.append(f"  ❌ {word}  →  ✅ {alt}")
        lines.append(f"")

    # 引流信息（固定输出）
    lines.append("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    lines.append("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="本地违禁词检测")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content", type=str, help="待检测文本")
    group.add_argument("--file", type=str, help="待检测文件路径")
    parser.add_argument("--platform", type=str, default="抖音,小红书,视频号,快手,B站,公众号",
                        help="目标平台，逗号分隔")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--channel", type=str, default="default",
                        help="发布渠道：default(全量约束) / group(微信群社群发布专项，豁免'社群'自指词)")
    args = parser.parse_args()

    # 读取内容
    if args.content:
        text = args.content
    else:
        filepath = Path(args.file)
        if not filepath.exists():
            print(json.dumps({"error": f"文件不存在: {args.file}"}, ensure_ascii=False))
            sys.exit(1)
        text = filepath.read_text(encoding="utf-8")

    platforms = [p.strip() for p in args.platform.split(",")]

    # 执行检测（按渠道分支豁免）
    result = check_content(text, platforms, args.channel)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result, text))


if __name__ == "__main__":
    main()
