#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tile_setup.py — 「资料拆卡」任务编排（工作目录内自包含）

一次资料拆卡任务 = 工作目录下的**一个任务文件夹**（以任务命名，例如「标点符号规范」）。
本脚本负责建目录、生成操作手册与进度、导出文本稿、拼总览图、校验、记进度。

    <工作目录>/<任务名>/
      ├── GUIDE.md      操作手册（读这一份就能接手；不依赖任何平台）
      ├── PROGRESS.md   进度（只增不删，底部最新）
      ├── cards.json    唯一事实源（每张卡的 id/index/title/blocks）
      ├── src/          原文提取（full_text.txt 等）
      ├── refs/         参考图 / 标准图（可选）
      └── out/          PNG 产物 + _check.json + _contact_sheet.png

用法：
    python tile_setup.py init     --dir "工作目录/任务名" --title "任务名" --source "资料出处" --count 47
    python tile_setup.py export-md --dir "…"
    python tile_setup.py sheet    --dir "…" [--cols 6]
    python tile_setup.py check    --dir "…"          # 调 gen_card_tile --check-only
    python tile_setup.py log      --dir "…" --entry "2026-10-05：已出图 47 张。"
    python tile_setup.py status   --dir "…"

⚠️ 手册与进度**只建在工作目录**，不建在 skill 目录里 —— 这样换环境（无 IMA、无网络、
   换执行者）都能读到，也是本工作流「跨平台为底」的关键。
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

TODAY = datetime.date.today().isoformat()

POS_NAME = {'bl': '左下', 'br': '右下', 'bc': '下中', 'c': '居中',
            'l': '左', 'r': '右', 'top': '上'}


def _cell_txt(c):
    """把一个 diagram 图元转成可读文本，让文本稿与图片信息一致。"""
    if c.get('vtext'):
        return c['vtext'].replace('\n', '')
    if c.get('pair'):
        return ''.join(str(x) for x in c['pair'])
    base = c.get('t') or c.get('base') or c.get('glyph')
    if not base:
        return '[' + (c.get('c') or '') + ']'
    base = str(base)
    if c.get('w') == 0.5:
        base += '(半格)'
    elif c.get('w') == 2:
        base += '(双格)'
    if c.get('under') == 'dot':
        base += '(下加圆点)'
    elif c.get('under') == 'line':
        base += '(下加直线)'
    elif c.get('side') == 'right':
        base += '(右侧圆点)'
    elif c.get('side') == 'left':
        base += '(左侧直线)'
    if c.get('lmark'):
        base = '同格左' + POS_NAME.get(c.get('where', 'l'), '左') + c['lmark'] + base
    if c.get('mark'):
        base += '＋%s(%s)' % (c['mark'], POS_NAME.get(c.get('where', 'c'), c.get('where', 'c')))
    return base


TEXT_TMPL = {
    'text': lambda b: b.get('text', ''),
    'list': lambda b: '\n'.join('· ' + i.replace('\n', ' ') for i in b.get('items', [])),
    'compare': lambda b: '\n'.join('误：%s\n正：%s' % (p.get('wrong', ''), p.get('right', ''))
                                   for p in b.get('pairs', [])),
    'marked': lambda b: b.get('text', '') + ('（字下加圆点）' if b.get('mark') != 'line' else '（字下加直线）'),
    'emphasis': lambda b: '★ ' + b.get('text', ''),
    'diagram': lambda b: '\n'.join(
        '%s：%s' % (r.get('label', ''), ' '.join(_cell_txt(c) for c in r.get('cells', [])))
        + (('  ▸ ' + r['note']) if r.get('note') else '')
        for r in b.get('rows', [])),
}


def load(dir_):
    with open(os.path.join(dir_, 'cards.json'), encoding='utf-8') as f:
        return json.load(f)


def cards_of(data):
    return data.get('cards', []) if isinstance(data, dict) else data


def meta_of(data):
    """cards.json 允许两种形态：完整对象（含 group/footer/ratio）或纯 cards 数组。"""
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------- init
GUIDE_TMPL = '''# 【{title} · 卡片长图任务】操作手册

> 本文件是本任务的**唯一操作指南**，放在工作目录内，不依赖任何平台。
> 会话记忆被压缩 / 换设备 / 换执行者之后，**先读这一份**，再按其中路径查数据。

## 0. 一句话任务
把 **{source}** 拆成「一图一知识点」的 **{ratio}** 卡片长图：一次性拆分、批量出图、归档。
- 目标张数：**{count}** 张（以 `cards.json` 实际为准）
- 产物：`out/*.png`（{ratio}，@192dpi → {px}）+ 一份全量文本稿 md
- 数据唯一事实源：`cards.json`（改内容只改它，**用脚本改，勿手改**）

## 1. 工作目录
```
{title}/
  GUIDE.md       ← 本手册
  PROGRESS.md    ← 进度（只增不删，底部最新）
  cards.json     ← 唯一事实源
  src/           ← 原文提取（full_text.txt 等，逐字提取、勿摘要）
  refs/          ← 参考图 / 标准图（可选）
  out/           ← PNG 产物 + _check.json + _contact_sheet.png
```

## 2. 进度查看位置
- **以 `PROGRESS.md` 底部「更新记录」最新一段为准**。

## 3. 命名与编号
- 产物文件名：`NN_标题.png`（NN = `index`，两位零填充），与他人协作时不要改编号规则。
- 卡片角标：`第 index / total 张 · {group}`。
- 重排顺序后，**编号必须一次性重排**（用脚本改 `index` 与 `total`），避免手改遗漏。

## 4. 强制工作流（五道门禁，**不得跳过**）
1. **提取原文** → `src/full_text.txt`（逐字，不摘要）。
2. **清单与张数确认**：列出知识点清单 + 预计张数，**用户确认后**才继续。
3. **示例卡确认**：先只出第 1 张，请用户确认样式（版式/配色/字号/信息密度）。
4. **全量文本稿确认**：`python tile_setup.py export-md --dir .` 生成 `TEXT.md`，
   **用户逐条确认后**（改错别字、修误正对比、补例子）才批量出图。
5. **批量出图 + 逐张复核 + 归档**。
> 前三道门禁是刻意设的闸门：样式/文本没定就批量出图 = 全部返工。

## 5. 渲染规则
- 画布：`{ratio}`（默认 3:4；另有 9:16 / 1:1 / 4:3 / 16:9 可选，`--ratio` 指定）。
- 命令：`python <SKILL>/gen_card_tile.py --cards cards.json --outdir out [--only c07]`
- **内容自适应**：脚本先测量内容真实高度，超出画布则整体等比缩小字号（k 从 1.0 递减，
  下限 0.62），直到完整落入画布 —— 杜绝「固定高度溢出被静默裁剪」。
  k **低于 0.7 左右就说明该卡该拆张**，不要硬塞。
- 配色语义：核心用法=蓝 / 要点·其他用法=橙 / 易错=红（误红正绿）/ 提示=绿 / 图示=青。
- 页脚只有来源，**不放日期**；正文中文一律用中文弯引号“”‘’。

## 6. 复核方法（**像素优先，视觉辅助**）
1. 每次生成后脚本自动做像素校验（尺寸 / **PDF 页数=1** / 空白 / **页脚底色带**），
   结果在 `out/_check.json`；失败即非 0 退出 —— **不要交付校验不过的产物**。
   > 页脚必须看**页脚底色带**，不能用「底部有没有文字」判断：内容溢出时正文文字会落在
   > 页 1 底部造成假通过（实测 5 页 PDF 曾被判通过）；颜色容差 ≤3。
2. `python tile_setup.py check --dir .` 可对既有产物复检。
3. `python tile_setup.py sheet --dir .` 拼总览图，整体扫一眼。
4. 放大局部人工复核时注意：**视觉模型容易把「斜线 / 弯引号 / 细竖线 / 全角字符」
   误判成「裁切 / 缺失」**，凡有疑问一律回到像素证据（`_check.json` 的 ink_bbox 等）。

## 7. 踩坑要点（实战踩过，务必照做）
1. 固定高度容器溢出**可能不产生第 2 页**，页数检测抓不到 → 必须用「先测量再缩字号」。
2. 测量内容高度时，**阈值要与页面底色比较**（页脚是浅灰，用"接近纯白"判定会漏掉页脚）。
3. 块/行设 `flex: 0 0 auto`（禁止压缩），否则长内容会把相邻元素挤出边界、造成重叠。
4. 空 `<span>` 画线宽度可能失效 → 用 `border-left` 或显式 `width/height`。
5. 表格/文本里的字号标记（如"半字"占半格）要真的画半宽格，否则与说明不符。
6. **误/正对比必须是同一句话、仅差一处标点**；不要把规则讲解塞进"误"里。
7. 顺序**就近**：易混对比、连用规则卡紧跟对应主卡。
8. "少见用法"要**单独立卡**，不要只埋在要点里。
9. 原资料里的内部章节号（如"第 5 章"）、页眉页脚属于噪音，不要出现在卡片上。
10. 中文引号规范：中文正文一律用弯引号“”‘’；仅英文句/代码/URL 内用直引号。
11. 内容修订/拆卡/重排统一写 `transform*.py`（幂等、可复跑），不要手工编辑 JSON。
12. 会话/环境重置会回滚文件 → 关键中间产物每轮改完**立即验证文件内容**，不依赖上一轮记忆。

## 8. 归档（可选，视环境能力）
- 若目标平台有上传能力（如 IMA 知识库），复制产物 + 文本稿到目标位置。
- **目标端若无删除接口**：重推前先把旧文件**改名**为 `【旧版N-可删除】…` 腾出干净名，
  再传新版，并明确告知用户需要手动清理哪些旧文件。

## 9. 变更记录
- {today}：任务初始化（{count} 张，{ratio}）。
'''


def cmd_init(a):
    d = os.path.abspath(a.dir)
    for sub in ('src', 'refs', 'out'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)

    cards_path = os.path.join(d, 'cards.json')
    ratio = a.ratio
    if not os.path.exists(cards_path):
        skeleton = {
            'group': a.group or a.title,
            'footer': a.footer or a.source,
            'ratio': ratio,
            'cards': [],
        }
        with open(cards_path, 'w', encoding='utf-8') as f:
            json.dump(skeleton, f, ensure_ascii=False, indent=2)
        created_cards = True
    else:
        created_cards = False
        with open(cards_path, encoding='utf-8') as f:
            skeleton = json.load(f)
        if not isinstance(skeleton, dict):
            skeleton = {'cards': skeleton}
        ratio = skeleton.get('ratio', ratio)

    W, H = RATIO_PX.get(ratio, RATIO_PX['3:4'])
    with open(os.path.join(d, 'GUIDE.md'), 'w', encoding='utf-8') as f:
        f.write(GUIDE_TMPL.format(
            title=a.title, source=a.source, count=a.count, ratio=ratio,
            group=skeleton.get('group', ''), px='%d×%d' % (W * 2, H * 2), today=TODAY))

    prog = os.path.join(d, 'PROGRESS.md')
    if not os.path.exists(prog):
        with open(prog, 'w', encoding='utf-8') as f:
            f.write('# 【%s·卡片长图·进度】\n\n'
                    '> 进度以最底部「更新记录」最新一段为准。全量清单共 **%s** 张。\n'
                    '> 维护约定：更新记录**只增不删**，最新在最底部。\n\n'
                    '## 一、全量清单\n\n| 序号 | 卡片 | 状态 |\n|---|---|---|\n'
                    '| （待核定） | | |\n\n'
                    '## 二、更新记录（只增不删，最新在最底部）\n\n'
                    '%s：任务初始化（%s 张，%s）。\n'
                    % (a.title, a.count, TODAY, a.count, ratio))

    print('已初始化任务目录：%s' % d)
    print('  操作手册：%s/GUIDE.md   ← 先读这一份' % d)
    print('  进度    ：%s/PROGRESS.md' % d)
    print('  数据源  ：%s/cards.json%s' % (d, '（新建骨架）' if created_cards else '（已存在，保留）'))
    print('下一步：把原文提取写入 src/full_text.txt → 梳理清单 → '
          '写入 cards.json → gen_card_tile.py 出图')
    return 0


RATIO_PX = {'3:4': (900, 1200), '9:16': (900, 1600), '1:1': (900, 900),
            '4:3': (1200, 900), '16:9': (1200, 675)}


# ---------------------------------------------------------------- export-md
def cmd_export_md(a):
    d = os.path.abspath(a.dir)
    data = load(d)
    meta = meta_of(data)
    cards = cards_of(data)
    total = len(cards)
    lines = ['# %s · 卡片文本稿' % (meta.get('group') or os.path.basename(d)),
             '',
             '> 本文件由 `cards.json` 自动导出（与图片内容一致），供**批量出图前的逐条确认**。',
             '> 复核重点：错别字 / 误正对比是否同一句 / 例子是否遗漏 / 少见用法是否单独立卡。',
             '> 共 %d 张。来源：%s' % (total, meta.get('footer') or '—'),
             '']
    for c in cards:
        lines.append('---')
        lines.append('')
        lines.append('## %s. %s（%s）' % (c.get('index', '?'), c.get('title', ''),
                                        c.get('filename', c.get('id', ''))))
        if c.get('subtitle'):
            lines.append('*%s*' % c['subtitle'])
        lines.append('')
        for b in c.get('blocks', []):
            t = b.get('type', 'text')
            tag = b.get('tag', '')
            body = TEXT_TMPL.get(t, lambda x: '')(b)
            lines.append('**[%s]**' % tag)
            lines.append('')
            lines.append(body)
            lines.append('')
    out = os.path.join(d, 'TEXT.md')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('已导出文本稿：%s（%d 张）' % (out, total))
    return 0


# ---------------------------------------------------------------- sheet
def cmd_sheet(a):
    d = os.path.abspath(a.dir)
    outdir = os.path.join(d, 'out')
    if not os.path.isdir(outdir):
        print('out/ 目录不存在，先批量出图', file=sys.stderr)
        return 1
    from PIL import Image
    files = sorted(f for f in os.listdir(outdir)
                   if f.lower().endswith('.png') and not f.startswith('_'))
    if not files:
        print('out/ 下没有产物', file=sys.stderr)
        return 1
    cols = a.cols
    tw = a.thumb
    thumbs = []
    for f in files:
        im = Image.open(os.path.join(outdir, f)).convert('RGB')
        th = im.resize((tw, max(1, int(tw * im.height / im.width))))
        thumbs.append((f, th))
    # 行高取所有缩略图的最大高度：万一混了不同比例，也不会互相压盖
    row_h = max(t.height for _, t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    pad = 14
    canvas = Image.new('RGB', (cols * (tw + pad) + pad, rows * (row_h + pad) + pad), (238, 242, 247))
    for i, (f, im) in enumerate(thumbs):
        r, c = divmod(i, cols)
        canvas.paste(im, (pad + c * (tw + pad), pad + r * (row_h + pad)))
    out = os.path.join(outdir, '_contact_sheet.png')
    canvas.save(out)
    print('已生成总览图：%s（%d 张，%d 列）' % (out, len(thumbs), cols))
    return 0


# ---------------------------------------------------------------- check
def cmd_check(a):
    d = os.path.abspath(a.dir)
    data = load(d)
    ratio = a.ratio or meta_of(data).get('ratio') or '3:4'
    cmd = [sys.executable, os.path.join(SKILL_DIR, 'gen_card_tile.py'),
           '--cards', os.path.join(d, 'cards.json'), '--outdir', os.path.join(d, 'out'),
           '--ratio', ratio, '--check-only']
    return subprocess.call(cmd)


# ---------------------------------------------------------------- log / status
def cmd_log(a):
    d = os.path.abspath(a.dir)
    p = os.path.join(d, 'PROGRESS.md')
    if not os.path.exists(p):
        print('缺少 PROGRESS.md，先 init', file=sys.stderr)
        return 1
    entry = (a.entry or '更新。').strip()
    line = entry if entry.startswith(TODAY) else '%s：%s' % (TODAY, entry)
    with open(p, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    print('已追加进度：%s' % line)
    return 0


def cmd_status(a):
    d = os.path.abspath(a.dir)
    data = load(d)
    cards = cards_of(data)
    outdir = os.path.join(d, 'out')
    pngs = [f for f in os.listdir(outdir) if f.lower().endswith('.png')
            and not f.startswith('_')] if os.path.isdir(outdir) else []
    rep = {}
    cp = os.path.join(outdir, '_check.json')
    if os.path.exists(cp):
        rep = json.load(open(cp, encoding='utf-8'))
    ks = [i.get('k') for i in rep.get('items', []) if i.get('k')]
    print('任务目录：%s' % d)
    print('清单张数：%d ｜ 已出图：%d ｜ 比例：%s'
          % (len(cards), len(pngs), meta_of(data).get('ratio') or '3:4'))
    if rep:
        line = '校验：%d/%d 通过' % (rep.get('total', 0) - rep.get('failed', 0), rep.get('total', 0))
        if ks:
            line += '；自适应系数 k 区间 %.2f~%.2f（<0.7 建议拆张）' % (min(ks), max(ks))
        print(line)
    p = os.path.join(d, 'PROGRESS.md')
    if os.path.exists(p):
        lines = [l for l in open(p, encoding='utf-8').read().splitlines() if l.strip()]
        print('最新进度：%s' % lines[-1])
    return 0


def main():
    ap = argparse.ArgumentParser(description='资料拆卡任务编排')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('init', help='在**工作目录**新建任务文件夹并生成手册/进度')
    p.add_argument('--dir', required=True, help='任务目录（工作目录下，以任务命名）')
    p.add_argument('--title', required=True)
    p.add_argument('--source', default='（资料出处）')
    p.add_argument('--count', type=int, default=0)
    p.add_argument('--ratio', default='3:4')
    p.add_argument('--group', default=None)
    p.add_argument('--footer', default=None)
    p.set_defaults(func=cmd_init)

    p = sub.add_parser('export-md', help='由 cards.json 导出全量文本稿 TEXT.md')
    p.add_argument('--dir', required=True)
    p.set_defaults(func=cmd_export_md)

    p = sub.add_parser('sheet', help='拼缩略总览图')
    p.add_argument('--dir', required=True)
    p.add_argument('--cols', type=int, default=6)
    p.add_argument('--thumb', type=int, default=300)
    p.set_defaults(func=cmd_sheet)

    p = sub.add_parser('check', help='校验既有产物（尺寸/页数/空白/页脚）')
    p.add_argument('--dir', required=True)
    p.add_argument('--ratio', default=None)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser('log', help='追加进度记录（只增不删）')
    p.add_argument('--dir', required=True)
    p.add_argument('--entry', default=None)
    p.set_defaults(func=cmd_log)

    p = sub.add_parser('status', help='打印任务状态')
    p.add_argument('--dir', required=True)
    p.set_defaults(func=cmd_status)

    a = ap.parse_args()
    sys.exit(a.func(a))


if __name__ == '__main__':
    main()
