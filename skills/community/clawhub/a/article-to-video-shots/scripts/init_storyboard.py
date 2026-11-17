#!/usr/bin/env python3
"""从长文生成分镜骨架

用法：
    python3 init_storyboard.py 文章.md
    python3 init_storyboard.py 文章.md --duration 75 --out 分镜.md
    python3 init_storyboard.py 文章.md --shots 8 --aspect 16:9

会读取文章的标题结构作为候选镜头主题，按钩子短、中段平均、收尾略长的规则分配时间轴，
生成一个带占位符的骨架文件。占位符一律写成 TODO，提醒逐个填实，不要批量生成糊弄。

镜头数默认按时长反推（单镜不超过 8 秒，落在 6 到 9 个之间），也可以 --shots 指定。
"""

import argparse
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from storyboard_lib import (  # noqa: E402
    DEFAULT_NEGATIVE_CN,
    DEFAULT_NEGATIVE_EN,
    DEFAULT_STYLE_CN,
    DEFAULT_STYLE_EN,
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
DROP_HEADINGS = {"封面", "标题", "摘要", "发布备注", "配图", "话题标签", "全局"}


def extract_topics(content):
    topics = []
    for line in content.splitlines():
        m = HEADING_RE.match(line.strip())
        if not m:
            continue
        title = m.group(2).strip().replace("**", "")
        if any(d in title for d in DROP_HEADINGS):
            continue
        topics.append(title)
    return topics


MAX_SHOT = 8


def allocate(n, duration):
    """按钩子短、中段平均、收尾略长的规则切分时间轴，单个镜头不超过 8 秒"""
    hook = max(3, min(MAX_SHOT, duration // 12))
    tail = max(5, min(MAX_SHOT, duration // 9))
    middle_total = max(duration - hook - tail, (n - 2) * 4)
    per = middle_total // max(n - 2, 1)
    per = max(4, min(MAX_SHOT, per))

    spans = [(0, hook)]
    cursor = hook
    for _ in range(n - 2):
        end = cursor + per
        spans.append((cursor, end))
        cursor = end
    spans.append((cursor, cursor + tail))
    return spans


def shot_count(duration):
    """按单镜不超过 8 秒反推需要几个镜头，落在 6 到 9 之间。

    先定镜头数再切时间，比先定镜头数再发现装不下要合理。
    """
    need = int(math.ceil(duration / float(MAX_SHOT)))
    return max(6, min(9, need))


def main():
    ap = argparse.ArgumentParser(description="从长文生成分镜骨架")
    ap.add_argument("article", help="长文 Markdown 文件")
    ap.add_argument("--out", help="输出文件，默认 分镜_<文章名>.md")
    ap.add_argument("--duration", type=int, default=60, help="目标总时长秒数，默认 60")
    ap.add_argument("--shots", type=int, help="镜头数，不给则由时长推算，落在 6 到 9 之间")
    ap.add_argument("--aspect", default="9:16", help="画幅，默认 9:16")
    args = ap.parse_args()

    path = Path(args.article)
    if not path.exists():
        sys.exit(f"文件不存在：{path}")

    content = path.read_text(encoding="utf-8")
    topics = extract_topics(content)

    if args.shots:
        n = args.shots
    else:
        n = shot_count(args.duration)
    spans = allocate(n, args.duration)

    title_hint = topics[0] if topics else path.stem
    out = Path(args.out) if args.out else Path(f"分镜_{path.stem}.md")

    style_cn = DEFAULT_STYLE_CN.replace("9:16", args.aspect)
    style_en = DEFAULT_STYLE_EN.replace("9:16", args.aspect)

    lines = [
        f"# {title_hint} · 分镜草稿",
        "",
        f"> 来源：{path.name}",
        f"> 目标：{args.aspect} 竖版，{n} 个镜头，{args.duration} 秒",
        f"> 待办：把每一处的 TODO 换成具体内容，不要留空缺；填完跑一次 check_storyboard.py",
        "",
        "## 全局风格前缀（每个镜头的提示词都必须原样带上开头这段）",
        "",
        style_cn,
        "",
        style_en,
        "",
        "## 全局负向提示词（每次一起提交）",
        "",
        DEFAULT_NEGATIVE_CN,
        "",
        DEFAULT_NEGATIVE_EN,
        "",
    ]

    roles = ["钩子"] + ["推进"] * (n - 2) + ["收束"]
    for i in range(n):
        start, end = spans[i]
        topic = topics[i + 1] if i + 1 < len(topics) else ""
        lines += [
            f"## 镜头 {i + 1}｜{roles[i]}（{start}-{end} 秒）",
            "",
            f"画面：TODO {topic} 对应的一个看得见的动作，写具体的东西而不是概念",
            "",
            f"中文提示词：TODO {style_cn} 追加镜头语言与画面动作",
            "",
            "英文提示词：TODO vertical 9:16, cinematic lighting, clean minimal tech aesthetic, soft depth of field, stable frames, no flicker. add camera language and action here",
            "",
            f"配音：TODO 控制在 {int((end - start) * 4.5)} 个汉字以内",
            "",
            "字幕：TODO 不超过 15 字的一句话",
            "",
        ]

    lines += [
        "## 发布注意事项",
        "",
        "- 视频里不放外链，链接统一放简介或评论区置顶",
        "- 界面类镜头录屏前核对当前版本，避免提示词与画面对不上",
        "- 金额和比例数字不进画面，只在配音里讲",
        "",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    actual = spans[-1][1]
    print(f"已生成 {out}：{n} 个镜头，时间轴 0-{actual} 秒")
    if args.duration - actual > 3:
        capacity = MAX_SHOT * 9
        print(f"注意：目标 {args.duration} 秒装不下。按单镜不超过 {MAX_SHOT} 秒、最多 9 个镜头算，")
        print(f"      一条片子的合理上限约 {capacity} 秒，多出来的 {args.duration - actual} 秒建议删内容，")
        print(f"      而不是把镜头拉长或加到 9 个以上。真要讲这么多，拆成上下两集。")
    print(f"下一步：python3 check_storyboard.py {out}")


if __name__ == "__main__":
    main()
