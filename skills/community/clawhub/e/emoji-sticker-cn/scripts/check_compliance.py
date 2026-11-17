#!/usr/bin/env python3
"""离线违禁词/极限词快速校验(给 agent 直接调用,避免人肉翻 references)。

设计:
- 种子词默认从 references/中文平台违禁词合规参考.md 第五节解析(《广告法》法定稳定词)。
- 平台专属敏感点(私域导流/站外引流等)为内置高频词表,方便快速预检。
- 这只是「离线兜底」,不是实时审核;正式发布前仍应优先调用 multi-wordcheck。

用法:
  python3 check_compliance.py "全网最低价,加微信详聊"
  python3 check_compliance.py copy.md --platform xiaohongshu douyin
  echo "顶级品牌" | python3 check_compliance.py -  # stdin
"""
import argparse
import os
import re
import sys

# 平台专属敏感点(高频触发,非穷举;正式审核以 multi-wordcheck 实时 API 为准)
PLATFORM_SENSITIVE = {
    "wechat": {  # 公众号:诱导分享 / 时政资质提示
        "诱导分享": ["转发朋友圈", "集赞", "点赞领", "分享给好友", "群发", "助力", "砍一刀", "拉人进群", "邀请好友得"],
        "时政提示": ["领导人", "时政", "新闻联播"],  # 仅提示资质,非判定
    },
    "xiaohongshu": {  # 小红书:零容忍绝对化词 + 严打私域导流
        "私域导流": ["加微信", "加V", "VX", "vx", "薇芯", "微信号", "公众号", "扫码加", "私聊我", "dd我", "s我"],
        "医美/医疗": ["美白针", "瘦脸针", "医美", "整容", "微整", "祛痘印"],
    },
    "douyin": {  # 抖音:严查站外引流 / 虚假库存
        "站外引流": ["加微信", "淘宝", "京东", "拼多多", "链接在主页", "橱窗", "小程序码", "二维码", "关注公众号"],
        "虚假营销": ["仅剩最后", "库存紧张", "马上涨价", "最后一天", "再不买就没了"],
    },
    "medical": {  # 医疗/保健:功效断言
        "功效断言": ["根治", "治愈", "痊愈", "康复", "无效退款", "包治", "百分百有效", "药到病除", "彻底根除", "无毒副作用"],
    },
}

SECTION_RE = re.compile(r"^##\s*五[、.]?\s*通用极限词种子集", re.M)
WORD_SPLIT = re.compile(r"[、,，;；\s]+")


def load_seed_words(seed_md):
    """从违禁词参考 md 解析第五节种子集,返回词列表。"""
    if not seed_md or not os.path.exists(seed_md):
        return []
    text = open(seed_md, encoding="utf-8").read()
    m = SECTION_RE.search(text)
    if not m:
        return []
    end = text.find("\n## ", m.end())
    body = text[m.end(): end if end != -1 else len(text)]
    words = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith(">") or line.startswith("#"):
            continue
        for w in WORD_SPLIT.split(line):
            # 跳过纯括号说明(如「无副作用(医疗类需资质)」的括号残留)
            if w and "(" not in w and "（" not in w:
                words.append(w)
    # 去重保序
    return list(dict.fromkeys(words))


def scan(text, words):
    hits = []
    for w in words:
        if w and w in text:
            hits.append(w)
    return hits


def main():
    ap = argparse.ArgumentParser(description="离线违禁词/极限词快速校验(兜底,非实时)")
    ap.add_argument("input", nargs="?", default="-",
                    help="文本、文件路径,或 '-' 表示 stdin")
    ap.add_argument("--platform", nargs="*",
                    choices=list(PLATFORM_SENSITIVE) + ["all"],
                    default=[],
                    help="附加平台敏感点检查: wechat/xiaohongshu/douyin/medical/all(默认仅扫种子集)")
    ap.add_argument("--seed", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "references", "中文平台违禁词合规参考.md"),
        help="违禁词参考 md 路径(默认本 skill 的 references)")
    ap.add_argument("--quiet", action="store_true", help="仅输出命中词,不输出解释")
    args = ap.parse_args()

    # 读取待检文本
    if args.input == "-":
        text = sys.stdin.read()
    elif os.path.isfile(args.input):
        text = open(args.input, encoding="utf-8").read()
    else:
        text = args.input
    text = text.strip()
    if not text:
        sys.stderr.write("无可检查文本\n")
        sys.exit(0)

    seed = load_seed_words(args.seed)
    all_hits = []
    for w in seed:
        if w and w in text:
            all_hits.append(("广告法极限词", w))

    platforms = [p for p in args.platform if p != "all"]
    if "all" in args.platform:
        platforms = list(PLATFORM_SENSITIVE)
    for p in platforms:
        for cat, words in PLATFORM_SENSITIVE.get(p, {}).items():
            for w in words:
                if w and w in text:
                    all_hits.append((cat, w))

    if not all_hits:
        if not args.quiet:
            print("PASS: 未命中离线词表")
        sys.exit(0)

    for cat, w in all_hits:
        if args.quiet:
            print(w)
        else:
            print(f"[{cat}] 命中: {w}")
    sys.stderr.write(f"\n共命中 {len(all_hits)} 处(离线兜底,非实时审核;正式发布前请调用 multi-wordcheck)\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
