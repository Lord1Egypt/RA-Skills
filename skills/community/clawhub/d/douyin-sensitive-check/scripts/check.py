#!/usr/bin/env python3
"""
抖音/短视频违禁词检测脚本（本地词库版）

用法:
  python3 check.py "你的文案内容"
  python3 check.py -f input.txt
  echo "文案" | python3 check.py
  python3 check.py --update          # 强制更新词库
  python3 check.py --status          # 查看词库状态

工作流:
  1. 每天首次运行自动更新词库（从多个 GitHub 开源词库拉取）
  2. 对输入文案做全词匹配（含子串匹配）
  3. 输出命中词及上下文位置，给出替换建议
"""

import sys
import re
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from update_words import update_words, load_words, status, needs_update


# 按类别匹配关键词（用于显示风险等级）
# 这些词不在通用违禁词库，但抖音/短视频平台已知会限流或违规
BUILTIN_RISK_WORDS = {
    "广告极限词（广告法）": [
        "史上最", "最好", "第一", "唯一", "顶级", "极致", "无敌", "全网最",
        "最强", "最优", "最大", "最低", "最高", "最便宜", "最实惠", "最划算",
        "专家级", "国家级", "行业第一", "销量第一", "NO.1", "no.1",
        "绝对", "100%", "永久", "终身", "彻底", "根治",
    ],
    "平台限流词（抖音）": [
        "推广", "广告", "营销", "引流", "涨粉", "买粉", "刷量",
        "私信", "加微信", "加我微信", "微信号", "扫码", "二维码",
        "点链接", "点击链接", "下单", "购买", "下载", "安装",
        "优惠券", "领券", "领红包", "福利", "免费领",
        "秒杀", "限时", "限量", "抢购", "团购",
        "代理", "招商", "加盟", "合作", "分销",
    ],
    "医疗健康违禁词": [
        "包治", "根治", "治愈", "特效", "祖传秘方", "偏方",
        "无副作用", "无任何副作用", "药到病除", "立竿见影",
    ],
}


def categorize_word(word: str) -> str:
    """对命中词做简单分类，没有精确分类就返回通用"""
    for cat, keywords in BUILTIN_RISK_WORDS.items():
        if word in keywords or any(k in word for k in keywords):
            return cat
    return "违禁/敏感词"

def find_hits(text: str, words: set) -> list[dict]:
    """
    在文案中查找所有命中的词，返回列表。
    同时检测词库词 + 内置平台限流词。
    每条包含: word, positions, category, source
    """
    # 合并词库词 + 内置词
    all_check: list[tuple[str, str]] = []  # (word, source)
    for word in words:
        all_check.append((word, "词库"))
    for cat, cat_words in BUILTIN_RISK_WORDS.items():
        for word in cat_words:
            all_check.append((word, cat))

    # 按词长从长到短排序，优先匹配长词
    all_check.sort(key=lambda x: len(x[0]), reverse=True)

    hits = []
    found_words = set()

    for word, source in all_check:
        if word in found_words:
            continue
        positions = [m.span() for m in re.finditer(re.escape(word), text, re.IGNORECASE)]
        if positions:
            cat = source if source != "词库" else categorize_word(word)
            hits.append({
                "word": word,
                "positions": positions,
                "category": cat,
                "source": source,
                "count": len(positions),
            })
            found_words.add(word)

    # 按出现位置排序
    hits.sort(key=lambda h: h["positions"][0][0])
    return hits

def highlight_text(text: str, hits: list[dict]) -> str:
    """在命中位置插入标记（用于终端显示）"""
    if not hits:
        return text
    # 收集所有命中区间
    spans = []
    for h in hits:
        for start, end in h["positions"]:
            spans.append((start, end))
    spans.sort()

    result = []
    prev = 0
    for start, end in spans:
        result.append(text[prev:start])
        result.append(f"【{text[start:end]}】")
        prev = end
    result.append(text[prev:])
    return "".join(result)

def get_context(text: str, start: int, end: int, window: int = 10) -> str:
    """截取命中词的上下文"""
    ctx_start = max(0, start - window)
    ctx_end = min(len(text), end + window)
    prefix = "…" if ctx_start > 0 else ""
    suffix = "…" if ctx_end < len(text) else ""
    return f"{prefix}{text[ctx_start:start]}【{text[start:end]}】{text[end:ctx_end]}{suffix}"

def format_result(text: str, hits: list[dict]) -> str:
    lines = []

    if not hits:
        lines.append("✅ 检测通过 — 未发现违禁词/敏感词")
        lines.append(f"📊 检测字数: {len(text)} 字")
        return "\n".join(lines)

    # 分类
    forbidden = [h for h in hits if h["source"] == "词库"]
    platform  = [h for h in hits if "平台限流词" in h["category"]]
    adwords   = [h for h in hits if "广告极限词" in h["category"]]
    medical   = [h for h in hits if "医疗" in h["category"]]

    lines.append(f"🚨 发现 {len(hits)} 个风险词，建议修改后再发布\n")

    if forbidden:
        lines.append("🔴 违禁词（高风险，必改）:")
        for h in forbidden:
            ctx = get_context(text, *h["positions"][0])
            times = f"（出现{h['count']}次）" if h["count"] > 1 else ""
            lines.append(f"   ▸ {h['word']}{times}  [{h['category']}]")
            lines.append(f"     上下文: {ctx}")

    if platform:
        lines.append("\n🟠 平台限流词（建议替换，影响流量）:")
        for h in platform:
            ctx = get_context(text, *h["positions"][0])
            times = f"（出现{h['count']}次）" if h["count"] > 1 else ""
            lines.append(f"   ▸ {h['word']}{times}")
            lines.append(f"     上下文: {ctx}")

    if adwords:
        lines.append("\n🟡 广告极限词（广告法风险）:")
        for h in adwords:
            ctx = get_context(text, *h["positions"][0])
            times = f"（出现{h['count']}次）" if h["count"] > 1 else ""
            lines.append(f"   ▸ {h['word']}{times}")
            lines.append(f"     上下文: {ctx}")

    if medical:
        lines.append("\n🟡 医疗违禁词（广告法）:")
        for h in medical:
            ctx = get_context(text, *h["positions"][0])
            lines.append(f"   ▸ {h['word']}  上下文: {ctx}")

    lines.append("\n── 标注后文案 ──")
    lines.append(highlight_text(text, hits))
    lines.append(f"\n📊 检测字数: {len(text)} 字 | 风险词: {len(hits)} 个")
    return "\n".join(lines)


def main():
    # 处理特殊参数
    if "--status" in sys.argv:
        s = status()
        print(f"词库状态:")
        print(f"  最后更新: {s['last_update']}")
        print(f"  词条数量: {s['word_count']:,}")
        print(f"  词库文件: {s['words_file']}")
        print(f"  今日需更新: {'是' if s['needs_update'] else '否'}")
        return

    if "--update" in sys.argv:
        from update_words import update_words as _update_words
        _update_words(force=True)
        return

    # 读取输入文案
    if len(sys.argv) >= 3 and sys.argv[1] == "-f":
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            content = f.read()
    elif len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        content = " ".join(sys.argv[1:])
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        print("用法: python3 check.py \"文案内容\"")
        print("      python3 check.py -f input.txt")
        print("      python3 check.py --update    # 强制更新词库")
        print("      python3 check.py --status    # 查看词库状态")
        sys.exit(1)

    content = content.strip()
    if not content:
        print("❌ 内容为空")
        sys.exit(1)

    # 每天第一次自动更新词库
    if needs_update():
        update_words()
        print()

    # 加载词库
    words = load_words()
    if not words:
        print("⚠️  词库为空，请先运行: python3 check.py --update")
        sys.exit(1)

    # 检测
    hits = find_hits(content, words)
    print(format_result(content, hits))


if __name__ == "__main__":
    main()
