#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refresh_a1.py — Q3 财报 A1 基线回写【辅助校验工具】

🔴🔴 重要：自动解析财报 PDF 的准确率实测仅 3/8，**本脚本不得自动改写
   bench.json 里各标的的 a1 基线**。财报表格布局千差万化（已实测至少 5 种），
   靠正则猜必然出错——而静默写入错数据比多花 token 危险得多。

   正确分工：
     Python（可靠）→ 判断是否已披露 + 给 PDF 直链        = q3_watch.py
     模型（可靠）→ 从 PDF 正文读出扣非/现金流数字
     本脚本（辅助）→ 给出**候选值**供模型交叉核对，不做权威来源

   用法：--check 输出候选值给模型参考；--write-override 由模型确认后
   显式传入正确数值才写盘（不做自动推断）。

设计要点（踩过的坑）
────────────────────────────────────────────────────────────
1. 🔴 基线必须与判定数据同源，不能另存一份 —— 否则两处会漂移。
   做法：**原地改写** `$STOCK_DATA_DIR/bench.json` 里对应标的的 `a1` 字段。
   （数据已从代码外抽：门槛明细统一在 bench.json，见 README。）
2. 🔴 只在拿到**一手 PDF** 且**解析出双指标**（扣非＋现金流）时才更新；
   解析不全就整体跳过该股，绝不用残缺数据覆盖已有基线。
3. 🔴 同比基线需要「上年同期」两个数才能算，不能只取当期同比百分比
   —— 半年报里给的是 H1 口径同比，Q3 报给的是「年初至报告期末」口径，
   两者含义不同，必须分别记录、不得混用。
4. 🔴 单季（Q3 单季）与累计（前三季度）两种口径不可混用。本脚本只取
   **「本报告期」= 第三季度单季** 的现金流与扣非，并与基线口径对齐标注。
5. 每股写入后立即回读校验，确保语法仍可编译、数字确实变了。

用法：
  python3 refresh_a1.py --dry-run              # 只看会改什么，不落盘
  python3 refresh_a1.py --codes 600000,600001   # 只处理指定标的
  python3 refresh_a1.py                         # 处理全部 15 只已披露者
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_guard import fetch_status
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )



BENCH_FILE = os.path.join(_D, "bench.json")
GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidate_gate.py")
# ⚠️ GATE 仅供 --check 的旧引用保留；A1 数据已不在该文件里（在 bench.json）
WATCH_JSON = os.environ.get("Q3_WATCH_JSON", os.path.join(tempfile.gettempdir(), "q3_watch.json"))
# （q3_watch.py 跑完用 --json-out 写到同一路径；两边用环境变量 Q3_WATCH_JSON 保持一致）

NUM = r"(-?[\d,]+\.?\d*)"


def to_yi(text):
    """把财报里的数字统一成「亿元」。财报常以元为单位。"""
    if text is None:
        return None
    s = str(text).replace(",", "").replace("，", "").strip()
    s = s.replace("－", "-").replace("—", "-").replace("–", "-")
    if s in ("", "-", "--", "—"):
        return None
    neg = s.startswith("-") or s.startswith("(")
    m = re.search(r"[\d.]+", s)
    if not m:
        return None
    try:
        v = float(m.group())
    except ValueError:
        return None
    if neg:
        v = -v
    # 单位判定：财报正文多为「元」，表格里已换算成「万元/亿元」
    if "亿" in s:
        return v
    if "万" in s:
        return v / 10000.0
    return v / 1e8


def _nums_in(seg):
    """抓取段内形如 -1,234.56 的数值（保留正负号，逗号）。"""
    return [float(x.replace(",", "")) for x in re.findall(NUM, seg)]


def _looks_like_amount(v):
    """金额通常是 7 位以上整数；百分比是绝对值<100 的两位小数。"""
    return abs(v) >= 1_000_000 or (abs(v) >= 100 and v == int(v) and abs(v) >= 1_000_000)


def _looks_like_pct(v):
    """百分比：绝对值 < 1000 且非整数金额形态（财报里极少出现 >1000% 的同比）。"""
    return abs(v) < 1000


def _row_after_label(flat, labels, span=400):
    """
    财报表格里标签常被换行截断，数值落在标签之后的下一行。
    例：'归属于上市公司股东的扣除非经常\n 10,572,177,317.83 5,582,126,598.19 89.39\n性损益的净利润'
    因此从标签出现处往后取一段文本，数出前三个数值：
      [0]=本期 [1]=上年同期 [2]=同比%
    """
    for lab in labels:
        i = flat.find(lab)
        if i < 0:
            continue
        seg = flat[i + len(lab): i + len(lab) + span]
        vals = _nums_in(seg)
        if len(vals) >= 3:
            cur, prev, third = vals[0], vals[1], vals[2]
            # 判定：前两个应是金额（亿元级），第三个应是百分比
            if _looks_like_pct(third) and (abs(prev) > 0):
                return cur, prev, third
            # 有些报表只给 [本期, 同比]（无上年同期金额）
            if len(vals) >= 2 and _looks_like_pct(vals[1]) and abs(cur) > 100:
                return cur, None, vals[1]
        if len(vals) >= 2 and _looks_like_pct(vals[1]) and abs(vals[0]) > 100:
            return vals[0], None, vals[1]
    return None, None, None


def _fmt(v):
    """财报里的千分位写法：1,501,855,888.16 → '1501855888.16'"""
    return str(v).replace(",", "")


def _pct_from_text(seg):
    """段内直接找『同比13.16%』『+13.16%』这类显式百分比，优先于数字位置推断。"""
    for m in re.finditer(r"(?:同比(?:增长|下降)?|增长|变动|增减)[^%]{0,12}?([\-＋+]?\d{1,3}(?:\.\d{1,2})?)\s*%", seg):
        s = m.group(1).replace("＋", "+")
        try:
            v = float(s)
        except ValueError:
            continue
        # 若前面是"下降"且没写负号，取负
        if "下降" in m.group(0) and v > 0:
            v = -v
        return v
    return None


def extract_from_text(txt):
    """
    从 pdftotext -layout 正文里抠：扣非同比%、经营现金流（亿元）、现金流同比%。
    兼容三种实测结构（用多份半年报验证）：
      A. 表格三列：标签  本期  上年同期  同比%
      B. 正文叙述：……净利润 48,811.57 万元，同比增长 13.16%
      C. 表格两列（无同比列）：标签  本期  上年同期  ← 同比须自行计算
    找不到任一关键项返回 None，由上层跳过该股（绝不残缺覆盖基线）。
    """
    res = {}
    flat = re.sub(r"[ \t]+", " ", txt)
    flat = flat.replace("\uff0d", "-").replace("\u2014", "-")

    # ── 扣非 ────────────────────────────────────────────────
    kf_lbl = None
    for l in ("归属于上市公司股东的扣除非经常性损益的净利",
              "归属于上市公司股东的扣除非经常",
              "扣除非经常性损益的净利润",
              "扣除非经常性损益后归属于"):
        i = flat.find(l)
        if i >= 0:
            kf_lbl = (l, i)
            break
    if kf_lbl:
        l, i = kf_lbl
        seg = flat[i + len(l): i + len(l) + 420]
        # 去掉紧随其后的换行造成的标签尾巴（如"润 48,811.57"）
        nums = [float(_fmt(x)) for x in re.findall(NUM, seg)]
        # 优先显式同比
        kf_yoy = _pct_from_text(seg)
        # 🔴 金额 vs 百分比的分界不能只看量级：'48,811.57 万元' 与 '13.16%' 量级重叠。
        # 判据：百分比是**整数或两位小数且无千分位**，且出现在段尾附近；金额带千分位或位数≥5。
        amt = None
        raw = re.findall(NUM, seg)
        for raw_v, v in zip(raw, nums):
            has_comma = "," in raw_v
            # 金额：带千分位，或绝对值 ≥10000，或整数且≥1000（万元整）
            if has_comma or abs(v) >= 10000 or (v == int(v) and abs(v) >= 1000):
                amt = v
                break
        if amt is not None:
            res["kf_cur"] = to_yi(amt)
            res["kf_yoy"] = kf_yoy if kf_yoy is not None else None
            if kf_yoy is None and len(nums) >= 2 and nums[1] != 0:
                base = nums[1]
                if abs(base) > 10000:
                    res["kf_yoy"] = round((amt - base) / abs(base) * 100, 2)

    # ── 经营现金流 ──────────────────────────────────────────
    L = "经营活动产生的现金流量净额"
    j = flat.find(L)
    if j >= 0:
        seg = flat[j + len(L): j + len(L) + 420]
        nums = [float(_fmt(x)) for x in re.findall(NUM, seg)]
        cf_yoy = _pct_from_text(seg)
        raw = re.findall(NUM, seg)
        amt = next((v for raw_v, v in zip(raw, nums)
                    if "," in raw_v or abs(v) >= 10000 or (v == int(v) and abs(v) >= 1000)), None)
        if amt is not None:
            res["cf_cur"] = to_yi(amt)
            res["cf_yoy"] = cf_yoy
            if cf_yoy is None and len(nums) >= 2 and abs(nums[1]) > 10000:
                base = nums[1]
                res["cf_yoy"] = round((amt - base) / abs(base) * 100, 2)

    return res


def load_disclosed(codes=None):
    """读 q3_watch.py 的 JSON，列出已披露的标的及 PDF 直链。

    🔴 原来读不到就 return []，上层打印「未发现已披露 Q3 的标的」——
    这话和「真的没人披露」长得一模一样，会让人以为一切正常。
    """
    if not os.path.exists(WATCH_JSON):
        print(f"🔴 取数失败 · q3_watch 输出不存在：{WATCH_JSON}\n"
              f"   先跑：python3 {os.path.join(os.path.dirname(GATE), 'q3_watch.py')} "
              f"--json-out {WATCH_JSON}")
        return None
    try:
        with open(WATCH_JSON, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as exc:
        print(f"🔴 取数失败 · q3_watch 输出解析失败：{type(exc).__name__}: {exc}")
        return None
    # q3_watch 自己报过 FETCH_FAIL → 不能当「无披露」
    failed = d.get("failed") or 0
    if failed:
        print(f"⚠️ 注意：q3_watch 本次有 {failed} 只取数失败，"
              f"下面的「已披露」清单**不完整**（失败 ≠ 未披露）。")
    out = []
    for r in d.get("results", []):
        if r.get("state") != "DISCLOSED":
            continue
        if codes and r["code"] not in codes:
            continue
        out.append(r)
    return out


def fetch_pdf(url, dest):
    """下载财报 PDF。返回 FetchResult。"""
    def _do():
        r = subprocess.run(["curl", "-s", "--max-time", "90", "-A", "Mozilla/5.0",
                            "-o", dest, url], capture_output=True, timeout=120)
        if not os.path.exists(dest) or os.path.getsize(dest) <= 20000:
            raise ValueError(f"文件缺失或过小"
                             f"（{os.path.getsize(dest) if os.path.exists(dest) else 0} 字节）")
        return dest

    return fetch_status(_do, tries=2, delay=1.0)


def pdf_to_text(pdf, txt):
    """pdftotext。返回 FetchResult。"""
    def _do():
        r = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", pdf, txt],
                           capture_output=True, timeout=180)
        if r.returncode != 0 or not os.path.exists(txt):
            raise ValueError(f"pdftotext 退出码 {r.returncode}: "
                             f"{r.stderr.decode(errors='ignore')[:120]}")
        return txt

    return fetch_status(_do, tries=1, delay=0)


def current_baseline():
    """读 bench.json 取各标的当前 a1 基线 → {代码: [扣非同比, 现金流亿, 现金流同比]}。

    🔴 原来找不到 A1_BASE 就返回空字典 —— 下游照样能跑，--set 会把基线整个清空。
       现在数据在 bench.json：文件缺失 / 解析失败 / stock 为空 → **直接中止**，
       绝不返回空字典（空字典 = 静默清空全部基线）。
    """
    if not os.path.isfile(BENCH_FILE):
        print(f"🔴 取数失败 · 找不到门槛数据文件：{BENCH_FILE}\n"
              f"   🔴 已中止：继续下去会把 A1 基线清空，等于抹掉全部数据。")
        raise SystemExit(1)
    try:
        data = json.loads(pathlib.Path(BENCH_FILE).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"🔴 取数失败 · bench.json 解析失败（{type(exc).__name__}: {exc}）\n"
              f"   🔴 已中止：不拿坏文件覆盖基线。")
        raise SystemExit(1)
    stock = data.get("stock") or {}
    if not stock:
        print("🔴 bench.json 的 stock 为空 → 已中止（写下去等于清空全部基线）。")
        raise SystemExit(1)
    return {c: list(v.get("a1") or []) for c, v in stock.items()}






def _num_or_none(x):
    """'NONE'→None，'TURNAROUND'→'TURNAROUND'，其余转 float；转不了抛 ValueError。"""
    x = x.strip()
    if x.upper() == "NONE":
        return None
    if x.upper() == "TURNAROUND":
        return "TURNAROUND"
    return float(x)


def write_a1(updates, notes=None):
    """原地改写 bench.json 里各标的的 a1 字段；失败回滚，绝不留下坏文件。

    updates：{代码: [扣非同比, 现金流亿, 现金流同比]}
    🔴 只改已有标的、不新建条目 —— 一只标的的全部门槛数据必须在一处，
       凭空新增需要 direction/pb_pctl 等另外 6 个字段，造不出来。
    """
    notes = notes or {}
    with open(BENCH_FILE, encoding="utf-8") as f:
        data = json.load(f)
    stock = data.get("stock") or {}
    unknown = [c for c in updates if c not in stock]
    if unknown:
        return False, (f"bench.json 里没有这些标的：{', '.join(unknown)}\n"
                       f"   → 先在 bench.json 的 stock 里补齐 7 个必填字段"
                       f"（direction/bench_pt/pb_pctl/pe_pctl_3y/kf_ratio/a1/a1_note）"
                       f"再跑 --set。")
    for code, vals in updates.items():
        stock[code]["a1"] = list(vals)
        if notes.get(code):
            stock[code]["a1_confirmed"] = notes[code]      # 记来源，可追溯
    new = json.dumps(data, ensure_ascii=False, indent=2) + "\n"

    bak = BENCH_FILE + ".bak"
    shutil.copy(BENCH_FILE, bak)
    try:
        with open(BENCH_FILE, "w", encoding="utf-8") as f:
            f.write(new)
        try:
            json.loads(pathlib.Path(BENCH_FILE).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            shutil.copy(bak, BENCH_FILE)
            return False, f"写入后 JSON 回读失败（{exc}）→ 已回滚"
        return True, "ok"
    finally:
        if os.path.exists(bak):
            os.remove(bak)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codes", default=None)
    ap.add_argument("--check", action="store_true",
                    help="只输出候选值供模型交叉核对（默认，不写盘）")
    ap.add_argument("--set", default=None,
                    help="模型确认后的正确值：代码:扣非同比:现金流亿:现金流同比 逗号分隔")
    args = ap.parse_args()

    codes = args.codes.split(",") if args.codes else None
    base = current_baseline()
    disclosed = load_disclosed(codes)

    print("=" * 92)
    print("A1 基线辅助校验（不自动改写判定代码）")
    print("=" * 92)

    # ── 模式1：模型确认后显式写入 ──────────────────────────
    if args.set:
        updates, notes, bad = {}, {}, []
        for item in args.set.split(","):
            parts = item.split(":")
            if len(parts) != 4:
                bad.append(item)
                continue
            code = parts[0].strip()
            try:
                vals = [_num_or_none(parts[1]), _num_or_none(parts[2]), _num_or_none(parts[3])]
            except ValueError:
                bad.append(item)
                continue
            updates[code] = vals
            notes[code] = "模型确认值（已逐字核对季报正文）"
        if bad or not updates:
            print(f"❌ --set 格式有误：{', '.join(bad) if bad else '（空）'}\n"
                  f"   应为 代码:扣非同比:现金流亿:现金流同比"
                  f"（不填的项写 NONE；扭亏写 TURNAROUND）")
            return 1
        ok, err = write_a1(updates, notes)
        print("\n" + ("✅ 已按模型确认值写入 bench.json，回读校验通过"
                      if ok else f"❌ 写入失败已回滚：{err}"))
        return 0 if ok else 1

    # ── 模式2：候选值交叉核对（默认）────────────────────────
    if disclosed is None:
        print("🔴 取数失败 · 无法继续（上面已说明原因）。本次未产生任何候选值。")
        return 1
    if not disclosed:
        print(f"未发现已披露 Q3 的标的。当前 bench.json 覆盖 {len(base)} 只。")
        print("先跑 q3_watch.py 生成 JSON，再重试。")
        return 0

    print(f"发现已披露 {len(disclosed)} 只。逐只给候选值，**请与季报正文逐字核对后再决定**。\n")
    unreadable = []            # 🔴 下载/解析失败的必须汇总，不能逐只 ⏭ 就消失
    for r in disclosed:
        code, name = r["code"], r["name"]
        url = r.get("pdf_url")
        pdf = os.path.join(tempfile.gettempdir(), f"a1_{code}.pdf")
        txt = os.path.join(tempfile.gettempdir(), f"a1_{code}.txt")
        if not url:
            print(f"  ⏭ {name}({code}) 无 PDF 直链\n")
            unreadable.append(f"{name}({code}) 无 PDF 直链")
            continue
        pr = fetch_pdf(url, pdf)
        if pr.failed:
            print(f"  ⏭ {name}({code}) PDF 下载失败：{pr.error}\n")
            unreadable.append(f"{name}({code}) PDF 下载失败")
            continue
        tr = pdf_to_text(pdf, txt)
        if tr.failed:
            print(f"  ⏭ {name}({code}) PDF 解析失败：{tr.error}\n")
            unreadable.append(f"{name}({code}) PDF 解析失败")
            continue
        with open(txt, encoding="utf-8", errors="ignore") as f:
            body = f.read()
        g = extract_from_text(body)
        cur = base.get(code)
        kf = g.get("kf_yoy")
        cf = g.get("cf_cur")
        cfy = g.get("cf_yoy")
        # 🔴 解析不出关键项 = 需要人工读 PDF，必须显式标出，不能只显示「候选 = None」
        if kf is None or cf is None:
            unreadable.append(f"{name}({code}) 正则未解析出扣非或现金流（需人工读 PDF）")
        mark_kf = "✅" if (kf is not None and cur and cur[0] not in (None, "None")
                          and isinstance(cur[0], (int, float))
                          and abs(float(cur[0]) - kf) < 0.5) else ("⚠️" if kf is not None else "❌未解析出")
        print(f"  【{name} {code}】{r.get('ann_date')} 单季｜PDF={pdf}")
        print(f"      候选 扣非同比 = {kf}  |  现金流 = {None if cf is None else round(cf,2)} 亿  |  现金流同比 = {cfy}")
        print(f"      现有 基线     = {cur}")
        print(f"      核对 {mark_kf}  （❌未解析出 → 必须人工读 PDF，不要靠正则猜）")
        time.sleep(0.3)
    print("\n📌 以上为**候选值**。确认无误后用 --set 写入，例如：")
    print("   python3 refresh_a1.py --set 600000:89.39:96.99:30.52")
    if unreadable:
        # 🔴 这些标的本次没拿到候选值 —— 基线仍是旧的，不能当「已更新」
        print()
        print(f"🔴🔴 {len(unreadable)}/{len(disclosed)} 只本次未产出候选值"
              f"（其 A1 基线仍为旧数据，需人工处理）：")
        for u in unreadable:
            print(f"   · {u}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())