#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_derived_sync.py —— 派生 example 面 ↔ 生成器 的同源档（当前形制＝登记态）。

判什么：
  1. 应检枚数从盘上名册现算（examples/ 下带 SKILL.md 的目录），另与档内声明的枚数（FACES_DECLARED）对拍，两值不符即红——
     只认名册会被「整枚 example 目录消失」洗绿，只认常量会被「删一枚入参」洗绿，两道锁一起才堵得住。
     每枚必出一行读数：跑成的报该枚漂移行数，跑不成的也成行并点名原因（入参缺位／派生件缺位／生成器退非零…）。
     实跑枚数≠应检枚数＝红，并点名少的是哪枚。
  2. 重跑 scripts/derive_skill.py 现产该枚面（入参固化，见下），与在盘面按「块」比：frontmatter 逐键，正文按去编号的二级标题切块。
  3. 差异行数超出本档登记的「已知漂移」＝红；未登记的块或键一旦漂＝红。
  4. 人工拥有项（HUMAN_LOCK，逐枚双向锁）：盘面缺这一枚＝红（人工内容被抹掉不该静默），
     生成器长出这一枚＝红（重跑派生会把人工内容覆盖掉）。两向各出各的点名句。
  5. 豁免键若在生成器现产或在盘面任一侧不在场＝红（防豁免清单自己烂掉变成静默放行）；
     metadata.version 是豁免键 version 的第二份抄本，按行镜像豁免（EXEMPT_FM_LINES），其余子字段照硬比。

登记态与判定制：
  本档现在是登记态——已知漂移逐枚自报、末行报「已知漂移 N 行｜实跑 P／应检 Q 枚（登记态，归属路线待定）」并退 0，
  好让发布链不被堵。回填票把那几块补回生成器现产之后，撤掉 KNOWN_DRIFT 里相应登记项即可翻成
  判定制（登记清单空＝非空 diff 即红）；判定逻辑本身不为翻面而改。

入参固化（不从 displayName 或任何盘面字段反推）：
  实测过两种刊名入参各跑一趟会差出 frontmatter 16 行 vs 14 行——从盘面字段反推入参等于自造漂移，
  所以三对入参写死成档内常量，--spec 与 --unit-patterns 从 examples/<名>/assets/ 现读。

口径（读数以块级为主）：
  块体＝二级标题行之后到下一块标题之前的正文（去首尾空行）；差异行＝unified diff 的 +/- 行数
  （不含 +++/---/@@ 头）；标题行本身不计，编号移位（五→六）不算漂移——按去编号标题对齐。
  全文逐行 diff 只作附注，不进登记读数。

边界：只比 SKILL.md 那一枚面。生成器同批还产 README／assets／scripts，不在本档射程。
零网络、纯标准库、不改任何文件（临时目录用完即清）。退码：0＝登记态放行，1＝红（含少测一枚、双向锁、超出登记），2＝整档跑不动（生成器或名册目录本身缺位）。
"""

import difflib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent            # <包>/scripts
PKG = HERE.parent                                 # 包根
GEN = HERE / "derive_skill.py"

# 豁免键（人工策展的名述面与发布节奏）——逐键豁免，不是整块不看。
EXEMPT_FM_KEYS = ("displayName", "version", "summary", "description", "tags")

# 镜像豁免（逐行，只免这一行）：metadata.version 就是上面豁免键 version 的第二份抄本，
# 递进节奏由发布决定，生成器只会产初值。其余 metadata 子字段照硬比。
EXEMPT_FM_LINES = {"metadata": re.compile(r'^\s+version:\s*\S+\s*$')}

# 人工拥有块（去编号标题）：不计入块级漂移，只按 HUMAN_LOCK 双向锁存在性。
HUMAN_OWNED_BLOCKS = ("编辑质量与定位（不许做成信息堆叠）", "溯源（每条动态都得有去处）")

# 人工拥有项（逐枚双向锁）：盘面缺这一枚＝红（人工内容被抹掉不响），生成器长出这一枚＝红（重跑派生会覆盖它）。
# needle 取该枚独有的原文子串；锁不住整枚内容，只锁「这一枚在不在」，枚数仍由 KNOWN_DRIFT 计数锁住。
HUMAN_LOCK = {
    "journal-qiming-regional": (
        ("块·编辑质量与定位", "编辑质量与定位（不许做成信息堆叠）"),
        ("块·溯源", "溯源（每条动态都得有去处）"),
        ("行·类型含客户通讯", "| 类型 | 双月刊 / 客户通讯 |"),
        ("行·栏目实名清单", "| 栏目 | 01 法规动态、02 启明观察、03 启明业绩快讯、04 启明新闻 |"),
        ("行·免责声明已自行起草", "样例（第 21 期）没抽到"),
        ("行·坑已填实清单", "**已填实、不必再从头找的**"),
        ("行·metadata.requires.bins 单枚", 'bins: ["python"]'),
    ),
    "journal-hengshi-observation": (
        ("块·编辑质量与定位", "编辑质量与定位（不许做成信息堆叠）"),
        ("块·溯源", "溯源（每条动态都得有去处）"),
        ("行·metadata.requires.bins 单枚", 'bins: ["python"]'),
    ),
}

# 应检枚数＝名册现算（见 roster()），另在档内声明一个数作对照：两值不符即红。
# 只认名册会被「整枚 example 目录消失」洗绿（应检跟着变少就自洽了），所以这道声明是防那一形的第二把锁；
# 增删 example 时必须同时改这一枚数与 DERIVE_INPUTS／KNOWN_DRIFT／HUMAN_LOCK，改一处不改另一处即红。
FACES_DECLARED = 2

# 派生入参（固化）。--spec / --unit-patterns 走 examples/<名>/assets/ 现读，见 inputs()。
DERIVE_INPUTS = {
    "journal-qiming-regional": ("启明律师事务所", "区域观察", "双月刊"),
    "journal-hengshi-observation": ("衡石律师事务所", "衡石深度观察", "月刊"),
}

# 已知漂移登记（块级差异行数，取本档同口径实测；超登记即红）。
# (frontmatter)＝非豁免键（含 metadata 去掉镜像行）的差异行合计；(导语)＝首个二级标题之前的正文；其余按去编号块名。
KNOWN_DRIFT = {
    "journal-qiming-regional": {
        "(frontmatter)": 4,
        "(导语)": 2,
        "这本刊是什么": 4,
        "开工路径": 46,
        "还没填的坑": 20,
    },
    "journal-hengshi-observation": {
        "(frontmatter)": 2,
        "这本刊是什么": 1,
        "开工路径": 37,
        "还没填的坑": 1,
    },
}

FM_RX = re.compile(r"^---\n(.*?)\n---\n", re.S)
H2_RX = re.compile(r"^##\s+(.*\S)\s*$")
TOP_KEY_RX = re.compile(r"^[A-Za-z0-9_-]+:")
DENUM_RX = re.compile(r"^[一二三四五六七八九十]+(?:之[一二三四五六七八九十]+)?[、.\s]*")

LEDGER = []      # 已知漂移逐枚（name, item, registered, measured）
PER_NAME = {}    # 枚名 → 该枚实测已知漂移合计（每枚必出一行读数用）
REDS = []        # 红项逐枚


def die(code, msg):
    print(msg)
    sys.exit(code)


class FaceError(Exception):
    """单枚 example 跑不成——该枚出一行读数并点名原因，整档不静默少测。"""


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FaceError("读不到 %s（%s）" % (path.name, exc.strerror or exc))


def roster():
    """应检枚数＝从盘上名册现算，不抄档内常量——否则删掉一枚入参就等于少检一枚而尺不响。"""
    root = PKG / "examples"
    if not root.is_dir():
        die(2, "[ERROR] 名册目录缺位：%s" % root)
    names = sorted(p.name for p in root.iterdir() if (p / "SKILL.md").is_file())
    if not names:
        die(2, "[ERROR] examples/ 下一枚带 SKILL.md 的 example 都没有，本档无从检")
    return names


def split_fm(text):
    """→ (frontmatter 原文（可空）, 正文)"""
    m = FM_RX.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def fm_keys(fm):
    """frontmatter 切成顶层键 → {键: 该键块原文（含键行与其续行）}"""
    out, cur, buf = {}, None, []
    for line in fm.split("\n"):
        if TOP_KEY_RX.match(line):
            if cur is not None:
                out[cur] = "\n".join(buf).rstrip("\n")
            cur = line.split(":", 1)[0]
            buf = [line]
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).rstrip("\n")
    return out


def denum(title):
    return DENUM_RX.sub("", title.strip()).strip()


def body_blocks(body):
    """正文按二级标题切块 → {去编号标题: 块体}；首个标题之前记作 (导语)。"""
    out, cur, buf = {}, "(导语)", []
    for line in body.split("\n"):
        m = H2_RX.match(line)
        if m:
            out[cur] = "\n".join(buf).strip("\n")
            cur = denum(m.group(1))
            buf = []
        else:
            buf.append(line)
    out[cur] = "\n".join(buf).strip("\n")
    return out


def dlines(a, b):
    """两段文本的 unified diff +/- 行数（不含 +++/---/@@ 头）。

    这个计数与实参次序相关（同一对文本换向可差 2 行），本档一律「生成器在前、盘面在后」，
    与段0 分类表同口径，读数才可比。
    """
    n = 0
    for line in difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm=""):
        if line.startswith(("+++", "---", "@@")):
            continue
        if line.startswith("+") or line.startswith("-"):
            n += 1
    return n


def inputs(name):
    assets = PKG / "examples" / name / "assets"
    spec = assets / "stylespec.json"
    units = assets / "unit-patterns.md"
    for need in (spec, units):
        if not need.exists():
            raise FaceError("派生入参缺位：%s（本档入参固化，不许换源）"
                            % need.relative_to(PKG))
    return spec, units


def regenerate(name, workdir):
    """跑生成器现产一枚面 → 返回 (在盘面, 现产面) 文本。跑不成就抛 FaceError，由本档出一行点名读数。"""
    try:
        publisher, title, kind = DERIVE_INPUTS[name]
    except KeyError:
        raise FaceError("固化入参缺位（档内常量里没有这一枚，名册里有）")
    spec, units = inputs(name)
    out = Path(workdir) / name
    cmd = [sys.executable, "-B", str(GEN),
           "--spec", str(spec), "--unit-patterns", str(units),
           "--name", name, "--slug", name,
           "--publisher", publisher, "--title", title, "--kind", kind,
           "--out", str(out), "--force"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise FaceError("生成器退 %s（该枚无从比对）" % proc.returncode)
    produced = out / "SKILL.md"
    if not produced.exists():
        raise FaceError("生成器退 0 却没落 SKILL.md")
    disk = read(PKG / "examples" / name / "SKILL.md")
    return disk, produced.read_text(encoding="utf-8")


def strip_exempt_lines(key, block):
    """镜像豁免：该键若配了逐行豁免式，把命中的行从两侧一并摘掉再比。"""
    rx = EXEMPT_FM_LINES.get(key)
    if not rx:
        return block
    return "\n".join(l for l in block.split("\n") if not rx.match(l))


def check_frontmatter(name, gen_fm, disk_fm):
    g, d = fm_keys(gen_fm), fm_keys(disk_fm)
    for key in EXEMPT_FM_KEYS:
        miss = [s for s, kv in (("生成器现产", g), ("盘面", d)) if key not in kv]
        if miss:
            REDS.append("%s｜豁免键 %s 在%s不在场——豁免清单正在静默放行，红"
                        % (name, key, "与".join(miss)))
            print("  RED  豁免键 %s 在%s不在场" % (key, "与".join(miss)))
        else:
            print("  ok   豁免键 %s 两侧均在场" % key)
    drift = 0
    hard = []
    for key in sorted(set(g) | set(d)):
        if key in EXEMPT_FM_KEYS:
            continue
        gv, dv = strip_exempt_lines(key, g.get(key, "")), strip_exempt_lines(key, d.get(key, ""))
        if gv == dv:
            continue
        if key in g and key in d:
            n = dlines(gv, dv)
        else:
            n = len((gv or dv).split("\n"))
        drift += n
        hard.append("%s(%d)" % (key, n))
    verdict(name, "(frontmatter)", KNOWN_DRIFT.get(name, {}).get("(frontmatter)", 0),
            drift, "非豁免键不等＝%s" % ("、".join(hard) or "无"))


def check_human_lock(name, gen_text, disk_text):
    """人工拥有项双向锁：盘面缺即红，生成器长出即红。"""
    for label, needle in HUMAN_LOCK.get(name, ()):
        if needle not in disk_text:
            REDS.append("%s｜人工拥有项「%s」在盘面缺失——人工内容被抹掉了，红" % (name, label))
            print("  RED  人工拥有项「%s」在盘面缺失" % label)
        elif needle in gen_text:
            REDS.append("%s｜人工拥有项「%s」被生成器长出——重跑派生会覆盖人工内容，红"
                        % (name, label))
            print("  RED  人工拥有项「%s」出现在生成器现产里" % label)
        else:
            print("  ok   人工拥有项「%s」盘面在、生成器未长出" % label)


def record(name, item, registered, measured):
    LEDGER.append((name, item, registered, measured))
    PER_NAME[name] = PER_NAME.get(name, 0) + measured


def verdict(name, item, registered, measured, note=""):
    """登记项与实测的关系——超出登记、或形状变了即红；实测归零只报「该撤登记」。"""
    tail = ("｜" + note) if note else ""
    if measured == registered:
        record(name, item, registered, measured)
        print("  ok   %-14s 登记 %-4d 实测 %-4d%s" % (item, registered, measured, tail))
        return
    if measured == 0 and registered > 0:
        record(name, item, registered, 0)
        print("  ok   %-14s 登记 %-4d 实测 0   （已回填，该撤登记或翻判定制）%s"
              % (item, registered, tail))
        return
    if measured > registered:
        REDS.append("%s｜%s 实测漂移 %d 行 > 登记 %d 行（新漂出了 %d 行）%s"
                    % (name, item, measured, registered, measured - registered, tail))
        print("  RED  %-14s 登记 %-4d 实测 %-4d（超出登记）%s"
              % (item, registered, measured, tail))
        return
    REDS.append("%s｜%s 实测漂移 %d 行，既非登记的 %d 行也非 0——漂移形状变了，登记数已不可信%s"
                % (name, item, measured, registered, tail))
    print("  RED  %-14s 登记 %-4d 实测 %-4d（形状变了）%s"
          % (item, registered, measured, tail))


def check_blocks(name, gen_body, disk_body):
    g, d = body_blocks(gen_body), body_blocks(disk_body)
    for title in sorted(set(g) | set(d)):
        if title in HUMAN_OWNED_BLOCKS:
            continue
        gv, dv = g.get(title), d.get(title)
        if gv is None or dv is None:
            side = "只在生成器现产" if dv is None else "只在盘面"
            n = len((gv if dv is None else dv).split("\n"))
            verdict(name, title, KNOWN_DRIFT.get(name, {}).get(title, 0), n,
                    "%s（整块缺位）" % side)
            continue
        verdict(name, title, KNOWN_DRIFT.get(name, {}).get(title, 0), dlines(gv, dv))


def main():
    if not GEN.exists():
        die(2, "[ERROR] 生成器缺位：%s" % GEN)
    names = roster()
    if len(names) != FACES_DECLARED:
        REDS.append("名册现算应检 %d 枚 ≠ 档内声明 %d 枚——example 目录被增删而档内声明没跟着改，"
                    "或整枚面消失被洗绿，红（名册实得：%s）"
                    % (len(names), FACES_DECLARED, "、".join(names)))
    workdir = tempfile.mkdtemp(prefix="journal-draft-derived-sync.")
    print("同源档（登记态）｜生成器 scripts/derive_skill.py 现产 vs 在盘 examples/*/SKILL.md")
    print("应检名册从盘上现算（examples/ 下带 SKILL.md 的目录）＝%d 枚，档内声明 %d 枚：%s"
          % (len(names), FACES_DECLARED, "、".join(names)))
    print("口径：块级为主（按去编号标题对齐，差异行＝unified diff 的 +/- 行）；全文逐行 diff 只作附注。")
    print("豁免键＝%s（人工策展的名述与发布节奏）；其余键含 name/slug/license/metadata 入尺硬比。"
          % "/".join(EXEMPT_FM_KEYS))
    ran = []
    try:
        for name in names:
            print("== %s" % name)
            try:
                publisher, title, kind = DERIVE_INPUTS[name]
            except KeyError:
                publisher = title = kind = ""
            if publisher:
                print("  固化入参＝%s" % "／".join((publisher, title, kind)))
            try:
                disk, gen = regenerate(name, workdir)
            except FaceError as exc:
                print("  读数 %s｜未跑成｜%s" % (name, exc))
                REDS.append("%s｜未跑成：%s" % (name, exc))
                continue
            gen_fm, gen_body = split_fm(gen)
            disk_fm, disk_body = split_fm(disk)
            check_frontmatter(name, gen_fm, disk_fm)
            check_human_lock(name, gen, disk)
            check_blocks(name, gen_body, disk_body)
            print("  附注：全文逐行 diff %d 行（不计入登记读数）" % dlines(gen, disk))
            ran.append(name)
            print("  读数 %s｜实跑｜该枚已知漂移 %d 行"
                  % (name, PER_NAME.get(name, 0)))
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    missed = [n for n in names if n not in ran]
    if missed:
        REDS.append("少测 %d 枚：名册应检 %d 枚、实跑 %d 枚，缺 %s（同源尺少测一枚即不可信）"
                    % (len(missed), len(names), len(ran), "、".join(missed)))
    for red in REDS:
        print("[RED] " + red)
    total = sum(measured for _, _, _, measured in LEDGER)
    tail = "实跑 %d／应检 %d 枚" % (len(ran), len(names))
    if REDS:
        print("同源档红：%d 枚（见上列 RED 行；读数不作数，%s）" % (len(REDS), tail))
        return 1
    print("已知漂移 %d 行｜%s（登记态，归属路线待定）" % (total, tail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
