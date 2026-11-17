#!/usr/bin/env python3
"""生成微信表情开放平台提交清单 submit.md —— 平台表单每个字段填什么、传哪张图,照抄即可。

这是「最后一公里」:机检通过之后,人还得去平台逐字段填写。
清单按表单顺序给出「字段 → 值 / 文件」,避免对着一堆 PNG 猜编号。

用法:
  python3 make_submit.py ./wechat_pack --name 表情名称 --intro 介绍 --copyright 作者名
  python3 make_submit.py ./wechat_pack --name 表情名称 --intro 介绍 --copyright 作者名 --meanings meanings.txt

参数:
  --name       表情名称(≤8 汉字,无标点无空格,避免与已有专辑重名)
  --intro      表情介绍(≤80 汉字,充分展现形象特点或故事情节)
  --copyright  版权信息(≤10 汉字,未注册版权填设计师/工作室名,可简写)
  --meanings   含义词文件(每行一条,与主图一一对应;不给则表中标注待填)

输出: <dir>/submit.md
"""
import argparse
import os
import sys

LIMITS = {"name": 8, "intro": 80, "copyright": 10}


def find(d, *pats):
    import glob
    for pat in pats:
        hit = sorted(glob.glob(os.path.join(d, pat)))
        if hit:
            return hit
    return []


def main():
    ap = argparse.ArgumentParser(description="生成微信表情提交清单 submit.md")
    ap.add_argument("dir", help="素材根目录(resize_stickers.py --wechat 的输出)")
    ap.add_argument("--name", required=True, help="表情名称,≤8 汉字")
    ap.add_argument("--intro", required=True, help="表情介绍,≤80 汉字")
    ap.add_argument("--copyright", required=True, help="版权信息,≤10 汉字")
    ap.add_argument("--meanings", default=None, help="含义词文件(每行一条)")
    args = ap.parse_args()

    d = args.dir
    if not os.path.isdir(d):
        sys.stderr.write(f"目录不存在: {d}\n")
        sys.exit(2)

    # 字数校验
    for label, val, key in (("表情名称", args.name, "name"),
                            ("表情介绍", args.intro, "intro"),
                            ("版权信息", args.copyright, "copyright")):
        if len(val) > LIMITS[key]:
            sys.stderr.write(f"{label}「{val}」超 {LIMITS[key]} 字(当前 {len(val)} 字)\n")
            sys.exit(1)

    meanings = []
    if args.meanings:
        meanings = [w.strip() for w in open(args.meanings, encoding="utf-8") if w.strip()]

    main_dir = os.path.join(d, "主图")
    mains = sorted(f for f in os.listdir(main_dir)
                   if not f.startswith(".") and f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))) \
        if os.path.isdir(main_dir) else []

    if mains and meanings and len(mains) != len(meanings):
        sys.stderr.write(f"警告: 含义词 {len(meanings)} 条 ≠ 主图 {len(mains)} 张,清单中会标注缺漏\n")

    cover = find(d, "封面图/*.png")
    icon = find(d, "聊天面板图标/*.png")
    banner = find(d, "详情页横幅/*.png", "详情页横幅/*.jpg")
    guide = find(d, "赞赏引导图/*.png", "赞赏引导图/*.gif")
    thanks = find(d, "赞赏致谢图/*.png", "赞赏致谢图/*.gif")

    rows = "\n".join(
        f"| {i} | `主图/{f}` | {meanings[i - 1] if i <= len(meanings) else '⚠️ 待填'} |"
        for i, f in enumerate(mains, 1)
    )

    def rel(ps):
        return os.path.relpath(ps[0], d) if ps else "（缺失）"

    md = f"""# 微信表情开放平台提交清单

> 登录 sticker.weixin.qq.com → 创作者后台 → 「提交作品」→ 选择「表情专辑」,
> 按下表逐项填写/上传。生成于 make_submit.py,素材已过 check_assets.py 机检为前提。

## 一、表单字段

| 字段 | 填写内容 | 官方约束 |
|---|---|---|
| 表情名称 | **{args.name}** | ≤8 汉字,无标点/空格,避免与已有专辑重名 |
| 表情介绍 | {args.intro} | ≤80 汉字,充分展现形象特点或故事情节 |
| 版权信息 | {args.copyright} | ≤10 汉字,未注册版权填设计师/工作室名 |

## 二、上传素材

| 素材 | 文件 | 规格 |
|---|---|---|
| 表情主图({len(mains)} 张) | `主图/` 目录整包上传 | 240×240,≤500KB |
| 表情封面 | `{rel(cover)}` | 240×240 PNG 透明底,≤500KB |
| 聊天面板图标 | `{rel(icon)}` | 50×50 PNG 透明底,≤100KB |
| 详情页横幅 | `{rel(banner)}` | 750×400,≤500KB,禁透明底/纯白底/文字 |
| 赞赏引导图(可选) | `{rel(guide)}` | 750×560,≤500KB |
| 赞赏致谢图(可选) | `{rel(thanks)}` | 750×750,≤500KB |

## 三、含义词(与主图一一对应)

| 序号 | 文件 | 含义词 |
|---|---|---|
{rows}

> 含义词 = 用户在表情面板搜索的词(如「我没事」),不是画面里的台词;
> ≤4 汉字、避免标点、同套不重复。

## 四、提交前自查

1. `python3 scripts/check_assets.py {d} --meanings {args.meanings or 'meanings.txt'}` → FAIL 必须为 0
2. 文案过违禁词校验: `python3 scripts/check_compliance.py "{args.name} {args.intro}"`
3. 同一套统一动/静;整套画风统一;各表情差异充分(第一拒因)
4. 原创或持有版权;不含联系方式/二维码;不蹭名人热点
"""
    out = os.path.join(d, "submit.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"已生成: {out}")
    print(f"下一步: 打开 submit.md 照抄到平台表单;先跑 check_assets.py 确认 FAIL=0")


if __name__ == "__main__":
    main()
