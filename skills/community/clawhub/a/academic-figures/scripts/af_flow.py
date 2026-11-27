# -*- coding: utf-8 -*-
"""af_flow — 流程图布局/路由引擎 v2（英寸绝对坐标系）。

坐标系铁律（v8.0.0 重构核心）：所有尺寸测量与布局都在**英寸**这一绝对量上
进行——文字的英寸宽度只依赖字号与字体，与画布范围/DPI/宽高比完全无关。
旧版在"随内容变化的 data 坐标"下测量，测量↔范围互相污染（自引用死循环），
是六轮修补总别扭的体系性根因。渲染收尾把 figure 尺寸设成内容尺寸，
xlim/ylim = 内容英寸数 → 1 data unit = 1 inch，所见即所得。

设计来源（2026-11 SOTA 研究）：
- ELK Layered：回边 lane 绕行（上/下错层）、边标签参与布局（预留标签带）。
- TALA（2026-09 开源）：正交路由+磁吸框边 = 白板级观感；禁 arc3/rad 手调。
- adjustText/d3-labeler：measure-then-resolve（先测后画，墨迹实测过检）。
- 期刊规格：600dpi 线稿、矢量优先、字号下限保护（exit 3 拒溢出）。

六大能力（FLOW_SKILL_DEV_SPEC 对齐）：
R1 磁吸逐段箭头零穿框+lane 回边+虚线生效；R2 边标签墨迹级避让+两行折行+
数字-单位粘行；R3 文本测量驱动自适应（下限报错不溢出）；R4 chain/layered
布局+lane 错层；R5 画布=内容尺寸（零空白）；R6 --gate strict 三层 bbox 断言。
"""
import math
import sys

# v8.0.5 F1：形状注册表绘制原语在模块层解析（draw 闭包非 render 局部作用域）
from matplotlib.patches import (FancyBboxPatch, Polygon, Rectangle, Ellipse,
                                PathPatch)

# ── 常量（单位=英寸；pt→inch 换算 1pt=1/72in） ──────────────────────────
LAST_GEOM = None   # v8.0.9 render 几何快照（QC 边车）
LAST_POOL = None   # v8.1.0 最近一次 route() 的候选池 [(代价, 路径), ...]（QC 边车）
LAST_REJECT = None  # v8.1.0 最近一次 route() 的肘部被拒候选 [(键, 走廊位, 拦它的段)]
GAP_TRACKS = []     # v8.1.0 泳道 LR 行间隙通道轨道（layout 写、route/标签读；QC 边车导出）
LABEL_LOG = {}   # v8.1.0 标签放置轨迹 {标签文本: [[(x, y, 对齐, 被拒原因), ...], ...]}
                   # 每次调用 place_edge_label 追加一条（多轮放置=多条；成功轮最后一条）
LANE_GAP = 0.45          # 回边 lane 与内容外缘的最小间距
LANE_STAGGER = 0.38      # 多条回边错层步距
MAGNET_PAD = 0.02        # 箭头起点与框边的微距
EDGE_NIB = -0.01         # 箭头终点回退量（负=尖端止于描边外沿，绝不入框填充；
                         # 正值咬入经 600dpi 逐像素实测=系统性刺框 13-18px）
EDGE_STAGGER = 0.18      # 同一框边上多箭头的错位步距（>2×箭头头半宽 0.134，
                         # 同缘多箭头体之间保证白隙——0.13 实测两头部粘连 9px）
LABEL_PAD = 0.10         # 边标签与任意元素的强制间隙
FONT_FLOOR = 8.0         # 文本缩放下限（pt；期刊预设字号以下不再缩）
BOX_PAD_X = 0.15         # 框内水平内边距
BOX_PAD_Y = 0.11         # 框内垂直内边距
LINE_K = 1.18            # 行距系数
ROW_GAP = 0.62           # 分层行间（框缘到框缘）
COL_GAP = 0.62           # 横链列间
LANE_LABEL_ALLOW = 0.32  # lane 外侧的标签预留带
CANVAS_PAD_X = 0.22      # 画布左右留白
CANVAS_PAD_Y = 0.28      # 画布上下留白
HEAD_LEN = 0.16          # 箭头头三角边长


# ── 基础测量（英寸；transform 无关） ────────────────────────────────────
def measure_in(ax, s, fontsize, fp=None, weight="normal", ls=1.15):
    """字符串的英寸尺寸 (w, h)。get_window_extent 直接给 px，/fig.dpi=in，
    与画布范围/宽高比无关——测量绝对性的根基。"""
    fig = ax.figure
    t = ax.text(0.5, 0.5, s, fontsize=fontsize, fontproperties=fp,
                fontweight=weight, alpha=0, linespacing=ls)
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    t.remove()
    return bb.width / fig.dpi, bb.height / fig.dpi


def _unit_len(t):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in t)


def has_cjk_local(s):
    return any(0x2E80 <= ord(ch) <= 0x9FFF or 0x3000 <= ord(ch) <= 0x303F
               or 0xFF00 <= ord(ch) <= 0xFFEF for ch in str(s))


def _wrap_mid(t):
    """v8.0.9 折行断点=最靠近中点的空格（旧版固定首空格："48 h SLA" 断成
    "48"/"h SLA" 头轻脚重，judge 备注实锤；中点断法="48 h"/"SLA"）。"""
    ws = [i for i, ch in enumerate(t) if ch == " "]
    if not ws:
        return t
    bi = min(ws, key=lambda i: abs(i - len(t) / 2))
    return t[:bi] + "\n" + t[bi + 1:]


def _wrap(s, avail_w_in, unit_w_in=None):
    """按显示单位断行（CJK=2:1）。词元=不可拆原子（ASCII 连续段/数字-单位
    粘合体/CJK 单字）；单词永不拆断（出版排版禁忌），超宽由外层缩字号兜底。"""
    s = str(s)
    # 数字+CJK 单位粘合（48周/12.5mg 单词元，永不拆到两行）
    s2, i = s, 0
    while i < len(s2) - 1:
        if s2[i].isdigit() and ord(s2[i + 1]) > 0x2E80:
            s2 = s2[:i + 1] + "\x00" + s2[i + 1:]
            i += 2
            continue
        i += 1
    toks, cur, cur_lat, glue = [], "", False, False
    for ch in s2:
        if ch == "\x00":
            glue = True
            continue
        if ch == " ":
            if cur:
                toks.append(cur)
                cur, cur_lat = "", False
            glue = False
            continue
        is_lat = ord(ch) <= 0x2E80
        if glue:
            cur += ch          # 粘合：无视类属切换并入当前词元（48→周）
            glue = False
        elif is_lat == cur_lat or not cur:
            cur += ch
            cur_lat = is_lat
        else:
            toks.append(cur)
            cur, cur_lat = ch, is_lat
    if cur:
        toks.append(cur)
    if unit_w_in is None:
        unit_w_in = 0.5
    out, line, lw = [], "", 0.0
    for t in toks:
        t_disp = t.replace("\x00", "")
        uw = sum(2 if ord(c) > 0x2E80 else 1 for c in t)
        w_in = uw * unit_w_in
        if line and lw + unit_w_in + w_in > avail_w_in:
            out.append(line.rstrip())
            line, lw = "", 0.0
        line = (line + " " + t_disp).strip() if line else t_disp
        lw += (unit_w_in + w_in) if lw else w_in
    if line.strip():
        out.append(line.rstrip())
    return out or [s]


# ── 文本自适应（R3：测量驱动，下限报错不溢出） ──────────────────────────
def fit_text(ax, label, sub, box_w_in, box_h_in, fs, fp_l=None, fp_s=None):
    """测量驱动：换行+缩放至框内；返回 (lab_lines, sub_lines, fs_m, fs_s)。
    低于字号下限→ValueError（exit 3）拒绝溢出渲染。"""
    avail_w = box_w_in - 2 * BOX_PAD_X
    avail_h = box_h_in - 2 * BOX_PAD_Y
    floor_m = min(FONT_FLOOR, fs)
    floor_s = min(FONT_FLOOR - 0.5, fs - 2)

    def _try(s, f, fp, weight):
        uw = measure_in(ax, s, f, fp, weight)[0] / max(_unit_len(s), 1)
        lines = _wrap(s, avail_w, uw)
        w_max = max((measure_in(ax, ln, f, fp, weight)[0] for ln in lines),
                    default=0)
        h_in = measure_in(ax, "\n".join(lines), f, fp, weight, ls=LINE_K)[1]
        return lines, w_max, h_in

    f_m = fs
    lab_lines, lab_w, lab_h = _try(label, f_m, fp_l, "bold")
    while lab_w > avail_w or lab_h > avail_h:
        f_m -= 0.5
        if f_m < floor_m:
            raise ValueError(
                f"flow: 节点文本在字号下限 {floor_m:g}pt 下仍超出框体 "
                f"（{box_w_in:.2f}×{box_h_in:.2f}in）——请加宽框体/精简文案")
        lab_lines, lab_w, lab_h = _try(label, f_m, fp_l, "bold")
    sub_lines, sub_w, sub_h = [], 0.0, 0.0
    f_s = fs - 2
    if sub:
        sub_lines, sub_w, sub_h = _try(sub, f_s, fp_s, "normal")
        while sub_w > avail_w or sub_h > avail_h:
            f_s -= 0.5
            if f_s < floor_s:
                raise ValueError(
                    f"flow: 节点 sublabel 低于字号下限仍超出框——请精简文案")
            sub_lines, sub_w, sub_h = _try(sub, f_s, fp_s, "normal")
    while True:
        total = lab_h + (sub_h + 0.05 if sub_lines else 0.0)
        if total <= avail_h:
            break
        if f_m > floor_m:
            f_m -= 0.5
        elif f_s > floor_s:
            f_s -= 0.5
        else:
            raise ValueError(
                f"flow: 节点主副文本联合高度超框——请精简文案或加高框体")
        lab_lines, lab_w, lab_h = _try(label, f_m, fp_l, "bold")
        if sub:
            sub_lines, sub_w, sub_h = _try(sub, f_s, fp_s, "normal")
    return lab_lines, (sub_lines if sub else []), f_m, (f_s if sub else fs - 2)


# ── 布局（R4：语义→坐标，英寸空间） ────────────────────────────────────
def layout_semantic(nodes, edges, layout="chain", direction="TB", ax=None,
                    fs=11, cjk_fp=None, columns=None, lanes=None):
    """-t flow 自动布局。英寸空间：行高/列宽由实测文本尺寸累计，
    带标签的边预留标签带（ELK edgeLabels 语义）。返回 blocks 列表。
    layout="snake"：链式环绕（v8.0.4，R4 收官）——每 columns 个节点换行、
    奇数行反序（蛇形），横向边行内直连、换行边正交直降、回边走行间槽，
    宽高比 ≈2:1，论文版心缩放后字号不再跌破可读下限。
    layout="swimlane"（v8.0.6，F3）：泳道布局——lanes=[名称...] 顺序即
    泳道次序，节点 "lane": 索引/名称归属；TB=垂直列（左→右）、LR=水平行。
    泳道背景条+标题带由 render 依 _lanes_geo 绘制（块层 z=1）。"""
    global GAP_TRACKS
    GAP_TRACKS = []      # 每次布局清表（仅泳道 LR 写入）
    ids = [n["id"] for n in nodes]
    idset = set(ids)
    for e in edges:
        if e["from"] not in idset or e["to"] not in idset:
            raise ValueError(f"flow: 边 {e['from']}→{e['to']} 引用未定义节点")

    _labeled = any(e.get("label") for e in edges)
    blocks = []
    for n in nodes:
        _lab = str(n.get("label", n["id"]))
        _sub = str(n["sublabel"]) if n.get("sublabel") else None
        _fp_l = cjk_fp if cjk_fp and has_cjk_local(_lab) else None
        _fp_s = cjk_fp if cjk_fp and has_cjk_local(_sub or "") else None
        lab_lines = _wrap(_lab, 2.4, measure_in(ax, _lab, fs, _fp_l,
                                                "bold")[0] / max(_unit_len(_lab), 1))
        w_text = max((measure_in(ax, ln, fs, _fp_l, "bold")[0]
                      for ln in lab_lines), default=0.5)
        h_text = measure_in(ax, "\n".join(lab_lines), fs, _fp_l, ls=LINE_K)[1]
        sub_lines = []
        if _sub:
            sub_lines = _wrap(_sub, 2.4,
                              measure_in(ax, _sub, max(fs - 2, fs * 0.8), _fp_s)[0]
                              / max(_unit_len(_sub), 1))
            w_text = max(w_text, max((measure_in(ax, ln, max(fs - 2, fs * 0.8),
                                                 _fp_s)[0]
                                      for ln in sub_lines), default=0.3))
            h_text += measure_in(ax, "\n".join(sub_lines), max(fs - 2, fs * 0.8),
                                 _fp_s, ls=LINE_K)[1] + 0.05
        # v8.0.5 F1：非矩形形状按文本内接系数放大框（菱形×0.54 可用区→
        # 框=需求/tw），文本需求在 layout 期就满足——render 期 fit_text
        # 不再因形状收缩而拒（顶刊体验=引擎自动放大，而非报错）
        _spec = SHAPES[resolve_shape(n.get("shape", "round"))]
        _tw, _th = _spec["tb"]
        w = min(4.6, max((w_text + 2 * BOX_PAD_X + 0.08) / _tw, 1.5))
        h = max((h_text + 2 * BOX_PAD_Y + 0.06) / _th, 0.62)
        blocks.append({"id": n["id"], "label": _lab, "sublabel": _sub,
                       "w": w, "h": h, "color": n.get("color"),
                       "_lane": n.get("lane", 0),
                       "shape": n.get("shape", "round")})
    bmap = {b["id"]: b for b in blocks}

    if layout == "chain":
        # 富余宽度均匀分配进列间距（--width 横幅契约：内容铺满画布宽，
        # 不留大片空白；间距上限 2.4in 防节点过少时拉散）
        _target = ax.figure.get_size_inches()[0] - 2 * CANVAS_PAD_X
        _total_w = sum(b["w"] for b in blocks)
        _n = max(len(blocks) - 1, 1)
        _gap = min(2.4, max(COL_GAP, (_target - _total_w) / _n))
        _row_h = max(b["h"] for b in blocks)
        x = 0.0
        for b in blocks:
            # v8.0.4 行内**垂直居中**（旧版 y=0 底对齐）：异高框（副标题换行）
            # 中心不齐 → 相邻边轴线断差（judge 实测 69px）。居中后同行共轴。
            b["x"], b["y"] = x, (_row_h - b["h"]) / 2
            x += b["w"] + _gap
        return blocks
    if layout == "snake":
        # 链式环绕（R4 收官）：columns 列蛇形折行，行内垂直居中+列网格对齐
        # （列宽=跨行最大值、列内水平居中→换行边两端中心精确共线，
        # C→D 类垂直边退化为单一直线；judge 实测：逐行独立排版致 453px 中心
        # 偏移+Z 折）
        n = len(blocks)
        cols = max(2, int(columns or max(2, math.ceil(math.sqrt(n)))))
        rows = []
        r = 0
        while r * cols < n:
            seg = [b["id"] for b in blocks[r * cols:(r + 1) * cols]]
            rows.append(seg[::-1] if r % 2 else seg)   # 奇数行反序=蛇形
            r += 1
        col_w = [max(bmap[rows[ri][ci]]["w"] for ri in range(len(rows))
                     if ci < len(rows[ri])) for ci in range(cols)]
        col_x = [0.0]
        for cw in col_w[:-1]:
            col_x.append(col_x[-1] + cw + COL_GAP)
        _labeled_any = any(e.get("label") for e in edges)
        y_cursor = 0.0
        for ri, seg in enumerate(rows):
            row_h = max(bmap[i]["h"] for i in seg)
            for ci, i in enumerate(seg):
                bmap[i]["x"] = col_x[ci] + (col_w[ci] - bmap[i]["w"]) / 2
                bmap[i]["y"] = y_cursor + (row_h - bmap[i]["h"]) / 2  # 行内共轴
            y_cursor += row_h + ROW_GAP + (0.68 if _labeled_any else 0)
        for i in ids:   # 镜像：首行在顶
            bmap[i]["y"] = y_cursor - bmap[i]["y"] - bmap[i]["h"]
        return blocks
    if layout == "swimlane":
        # 泳道（F3 v8.0.6）：lanes=[名称...]，节点 "lane": 索引/名称归属；
        # TB=垂直列（左→右）、LR=水平行。列宽=lane 内最大节点宽+padding；
        # lane 内节点自上而下堆叠+水平居中；跨 lane 边由磁吸/路由照常处理。
        # 背景条+标题带几何写进 _lanes_geo（render 块层 z=1 绘制）。
        if not lanes:
            raise ValueError("flow: layout=swimlane 需要 'lanes'（名称列表）")
        _lane_names = [str(x) for x in lanes]
        _lidx = {}
        for i in ids:
            lv = bmap[i].get("_lane", 0)
            if isinstance(lv, str):
                if lv not in _lane_names:
                    raise ValueError(f"flow: 节点 {i} lane '{lv}' 不在 lanes 中")
                _lidx[i] = _lane_names.index(lv)
            else:
                _lidx[i] = int(lv)
        for i in ids:
            if not (0 <= _lidx[i] < len(_lane_names)):
                raise ValueError(f"flow: 节点 {i} lane 索引 {_lidx[i]} 越界")
        if direction in ("LR", "RL"):
            # v8.1.0 泳道 LR：水平行带（docstring v8.0.6 即承诺 LR=水平行，
            # 引擎落地）——lane 自上而下堆叠为横条带（lane0=顶行），lane 内
            # 节点自左向右按声明序排布（行内整体居中）。**标题=左侧竖排**
            # （经典泳道形态，render 依 "dir":"LR" 画左侧 0.42 深色竖条+
            # 旋转标题）：行带纯内容化→行间 0.30 间隙成为干净水平走廊，
            # 相邻行跨行边由 V 肘直接穿越（v8.0.9 的头域/总线避让全继承）。
            row_h = [0.0] * len(_lane_names)
            for i in ids:
                ci = _lidx[i]
                row_h[ci] = max(row_h[ci], bmap[i]["h"])
            _n_lane = len(_lane_names)
            _GUT = 0.42   # 左侧标题竖条宽
            # v8.1.0 行间隙通道分配（channel tracks）：相邻两行之间每条要横穿的
            # 边分到一条自己的轨道——带标签的边轨道更高（线下方留一个标签区），
            # 间隙高度按实际需要累加。旧版行间隙恒 0.30、走线高度靠候选取样碰
            # 运气：LR 样例回边 70 个候选全败、掉进穿节点的兜底（轨迹实测）。
            _cross = [[] for _ in range(max(_n_lane - 1, 0))]
            for _e in edges:
                _la, _lb = _lidx.get(_e.get("from")), _lidx.get(_e.get("to"))
                if _la is None or _lb is None or abs(_la - _lb) != 1:
                    continue
                _cross[min(_la, _lb)].append(_e)
            _gap, _trk = [], []
            for _es in _cross:
                _es = sorted(_es, key=lambda e: 1 if e.get("label") else 0)  # 稳定：无标签在下
                _off, _ts = 0.03, []
                for _e in _es:
                    _lab = bool(_e.get("label"))
                    _ts.append([_e["from"], _e["to"], _off, _lab])
                    _off += 0.50 if _lab else 0.18
                _gap.append(_off + 0.10 if _es else 0.30)
                _trk.append(_ts)
            _extra = sum(_g - 0.30 for _g in _gap)
            _total_h = sum(rh + 0.30 for rh in row_h) + 0.30 * (_n_lane - 1) \
                + _extra + 0.15   # 底部呼吸
            _cursor = _total_h
            row_y = [0.0] * _n_lane
            for ci in range(_n_lane):   # 顶→底
                _band_top = _cursor
                row_y[ci] = _band_top - 0.15 - row_h[ci]   # 内容区底（带 0.15 上垫）
                _cursor = row_y[ci] - 0.15 \
                    - (_gap[ci] if ci < _n_lane - 1 else 0.30)   # 带下垫+行距
            # v8.1.0 行内标签带预留：同一行里相邻两节点之间若有带标签的边，间距
            # 按标签宽度加宽（标签≈0.075in/字+净空）。否则短箭头放不下自己的标签
            # ——LR 期刊模板 accept：菱形与胶囊间 0.61in，标签 0.6in 宽，8 个段旁
            # 候选全败（轨迹实测）。与行间隙通道分配同一原则：标签位在布局期留。
            _gap_after = {}
            _prev = {}
            for i in ids:
                ci = _lidx[i]
                _gap_after.setdefault(i, COL_GAP)
                if ci in _prev:
                    # 带标签的边在「前一个节点→当前节点」之间：加宽的是**前一个
                    # 节点后面**的间距（曾误记到当前节点后面→完全没生效，对账实测）
                    for _e in edges:
                        if _e.get("label") and {_e.get("from"), _e.get("to")} \
                                == {_prev[ci], i}:
                            _gap_after[_prev[ci]] = max(
                                COL_GAP,
                                COL_GAP + 0.075 * min(len(_e["label"]), 40) + 0.25)
                _prev[ci] = i
            _row_w = [0.0] * _n_lane
            for i in ids:
                ci = _lidx[i]
                _row_w[ci] += bmap[i]["w"] + _gap_after[i]
            _max_row_w = max(_row_w) - COL_GAP
            _cur_x = [0.0] * _n_lane
            for i in ids:   # 声明序=行内自左向右；行内整体居中（右移避开竖条）
                ci = _lidx[i]
                bmap[i]["x"] = _GUT + (_max_row_w - (_row_w[ci] - COL_GAP)) / 2 \
                    + _cur_x[ci]
                _cur_x[ci] += bmap[i]["w"] + _gap_after[i]
                bmap[i]["y"] = row_y[ci] + (row_h[ci] - bmap[i]["h"]) / 2
            _geo = [{"x": -0.18, "w": _max_row_w + _GUT + 0.36,
                     "y": row_y[ci] - 0.15, "h": row_h[ci] + 0.30,
                     "label": _lane_names[ci], "dir": "LR"}
                    for ci in range(_n_lane)]
            for i in ids:
                bmap[i]["_lanes_geo"] = _geo
            # 轨道绝对坐标：间隙 gi 的底=下行带顶=row_y[gi]-0.15-_gap[gi]。
            # 带标签轨道：线下方 [off+0.04, off+0.30] 为标签区，线在 off+0.39。
            _gt = []
            for _gi, _ts in enumerate(_trk):
                _gb = row_y[_gi] - 0.15 - _gap[_gi]
                _gt.append({"y_lo": _gb, "y_hi": _gb + _gap[_gi],
                            "tracks": [{"edge": [t_[0], t_[1]],
                                        "line_y": _gb + t_[2] + (0.39 if t_[3] else 0.09),
                                        "label_y": (_gb + t_[2] + 0.17) if t_[3] else None,
                                        "label": t_[3]} for t_ in _ts]})
            GAP_TRACKS = _gt
            return blocks
        col_w = [0.0] * len(_lane_names)
        for i in ids:
            ci = _lidx[i]
            col_w[ci] = max(col_w[ci], bmap[i]["w"])
        col_w = [cw + 0.5 for cw in col_w]
        col_x = [0.0]
        for cw in col_w[:-1]:
            col_x.append(col_x[-1] + cw + 0.30)
        col_ys = [0.0] * len(_lane_names)
        _max_col_h = 0.0
        for i in ids:   # 按 lane 分组堆叠（读取序=声明序，自上而下）
            ci = _lidx[i]
            bmap[i]["x"] = col_x[ci] + (col_w[ci] - bmap[i]["w"]) / 2
            bmap[i]["y"] = col_ys[ci]
            col_ys[ci] += bmap[i]["h"] + ROW_GAP
        _max_col_h = max(col_ys) - ROW_GAP
        # v8.0.7 结构修正（judge 两轮实锤：偏移同时抬高 band 底→恒侵入 0.20）：
        # 节点区顶=H（偏移 0），标题带在节点区上方独立区间 [H+0.30, H+0.80]，
        # lane 背景条顶=H+0.80——节点顶与 band 底恒有 0.30in 间隙
        for i in ids:   # 镜像：首个节点在顶
            bmap[i]["y"] = _max_col_h - bmap[i]["y"] - bmap[i]["h"]
        # v8.0.9 列内纵向均衡（judge E7：短列底部空白带 0.82in 与最高列持平
        # =观感失衡）——节点序不变，富余高度均摊到列内间隙+列底
        _col_nodes = {}
        for i in ids:
            _col_nodes.setdefault(_lidx[i], []).append(i)
        for _ci, _ns in _col_nodes.items():
            _ns.sort(key=lambda i: -bmap[i]["y"])   # 镜像后 y 大=顶
            _ch = sum(bmap[i]["h"] for i in _ns)
            # v8.0.9 修正：free 必须扣除既有 (n-1)*ROW_GAP——漏扣时 _add
            # 过大→内容溢出泳道带下缘 0.68in（judge R8 无锚走廊根因，
            # CLI 真几何审计实锤：tlf 出口行/回路行全部掉出带域）
            _n = len(_ns)
            # v8.0.9 修正：free 必须扣除既有 (n-1)*ROW_GAP——漏扣时 _add
            # 过大→内容溢出泳道带下缘 0.68in（judge R8 无锚走廊根因，
            # CLI 真几何审计实锤：tlf 出口行/回路行全部掉出带域）
            _free = _max_col_h - _ch - ROW_GAP * (_n - 1)
            if _n <= 0 or _free <= 0.02:
                continue
            if _n == 1:
                bmap[_ns[0]]["y"] -= _free / 2
                continue
            _add = min(_free / _n, 1.0)
            _cy = _max_col_h
            for _k, i in enumerate(_ns):
                bmap[i]["y"] = _cy - bmap[i]["h"]
                _cy = bmap[i]["y"] - (ROW_GAP + _add)
        _lane_h = _max_col_h + 0.80
        # v8.0.9 band 底向下延 0.15（judge E6：圆柱下缘贴画布底框 1px）——
        # 内容底与 band 底分离，tight 裁剪下亦有底部呼吸空间
        _geo = [{"x": col_x[ci] - 0.18, "w": col_w[ci] + 0.36,
                 "y": -0.15, "h": _lane_h + 0.15, "label": _lane_names[ci]}
                for ci in range(len(_lane_names))]
        for i in ids:
            bmap[i]["_lanes_geo"] = _geo   # 共享引用，render 画一次
        return blocks
    # layered：最长路径分层（回边不计层）
    indeg = {i: 0 for i in ids}
    back = set()
    seen, stack = set(), []

    def _dfs(u):
        seen.add(u)
        stack.append(u)
        for e in edges:
            if e["from"] == u:
                v = e["to"]
                if v not in seen:
                    _dfs(v)
                elif v in stack:
                    back.add((e["from"], e["to"]))
        stack.pop()

    for r in ids:
        if r not in seen:
            _dfs(r)
    for e in edges:
        if (e["from"], e["to"]) not in back:
            indeg[e["to"]] += 1
    layer = {}
    frontier = [i for i in ids if indeg[i] == 0]
    lv = 0
    while frontier:
        for u in frontier:
            layer[u] = lv
        nxt = []
        for u in frontier:
            for e in edges:
                if e["from"] == u and (e["from"], e["to"]) not in back:
                    indeg[e["to"]] -= 1
                    if indeg[e["to"]] == 0:
                        nxt.append(e["to"])
        frontier = nxt
        lv += 1
    for i in ids:
        layer.setdefault(i, lv)
    if direction in ("LR",):
        cols = {}
        for i in ids:
            cols.setdefault(layer[i], []).append(i)
        x = 0.0
        for lv_i in sorted(cols):
            col = cols[lv_i]
            col_w = max(bmap[i]["w"] for i in col)
            y = 0.0
            for i in col:
                bmap[i]["x"], bmap[i]["y"] = x, y
                y += bmap[i]["h"] + 0.55
            x += col_w + COL_GAP
    else:   # TB：层=行（自上而下），行高实测累计+标签带预留
        rows = {}
        for i in ids:
            rows.setdefault(layer[i], []).append(i)
        # v8.0.4 ELK barycenter：父行先放，子行按父质心 x 排序——
        # 父子列对齐使主链边退化为干净直降/短肘（旧版固定顺序致父行
        # 与子行错位，子边被迫 lane 大绕行）。
        _parents = {}
        for e in edges:
            if (e["from"], e["to"]) not in back:
                _parents.setdefault(e["to"], []).append(e["from"])
        y_cursor = 0.0
        for lv_i in sorted(rows):
            row = rows[lv_i]

            def _bx(pid):
                b = bmap[pid]
                return b["x"] + b["w"] / 2 if "x" in b else 0.0
            row.sort(key=lambda i: (
                sum(_bx(p) for p in _parents.get(i) or [i])
                / max(len(_parents.get(i) or [i]), 1),
                ids.index(i)))
            row_h = max(bmap[i]["h"] for i in row)
            x = 0.0
            for i in row:
                bmap[i]["x"] = x
                bmap[i]["y"] = y_cursor + (row_h - bmap[i]["h"]) / 2   # 行内垂直居中（读取序向下增长，放完统一镜像）
                x += bmap[i]["w"] + COL_GAP
            # 行级对中：整行平移使其父质心加权中心对齐父行（ELK barycenter
            # 定位步）——父列对齐后主链边退化为直降，lane 大绕行不再触发
            _ps = [_parents.get(i) or [i] for i in row]
            _pm = sum(sum(_bx(p) for p in ps) / len(ps) for ps in _ps) / len(row)
            _rm = sum(bmap[i]["x"] + bmap[i]["w"] / 2 for i in row) / len(row)
            for i in row:
                bmap[i]["x"] += _pm - _rm
            y_cursor += row_h + ROW_GAP + (0.68 if _labeled else 0)   # 带标签边预留 1.3in 行距（白底标签 0.29+双侧 0.12 气垫 + 余量）
        for i in ids:   # 镜像回画布方向（sources 在顶）
            bmap[i]["y"] = y_cursor - bmap[i]["y"] - bmap[i]["h"]
    return blocks


# ── R1 磁吸与路由 ──────────────────────────────────────────────────────
def _bbox(b):
    return (b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"])


def _overlap(a, b, pad=0.0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0]
                or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def magnet(src, dst, attach_in=0, attach_out=0, force_key=None):
    """R1：吸附框边（终点咬入 EDGE_NIB=负值→尖端止于描边外沿）。
    v8.0.4：轴线对齐的边共享同一出线坐标（随目标入线槽错层）；
    force_key 强制 H/V 出入边方向（路由换向回退用）。"""
    sx0, sy0, sx1, sy1 = _bbox(src)
    dx0, dy0, dx1, dy1 = _bbox(dst)
    scx, scy = (sx0 + sx1) / 2, (sy0 + sy1) / 2
    dcx, dcy = (dx0 + dx1) / 2, (dy0 + dy1) / 2
    _k = force_key or ("H" if abs(dcx - scx) >= abs(dcy - scy) else "V")
    if _k == "H":
        sy = scy + attach_out * EDGE_STAGGER
        dy = dcy - attach_in * EDGE_STAGGER
        if abs(dcy - scy) <= 0.25:
            sy = dy  # 同行对齐：起终点共 y（错层槽由入端统一决定）
        # v8.0.9 端点行钳制：attach 错层过大时 sy/dy 可能落到 bbox 外——
        # 轮廓拟合钳 fx 但 y 仍用框外行=端点悬浮（judge E3 hexagon 悬空
        # 0.084in 实锤）。钳回 [y0+0.06, y1-0.06]=端点恒在轮廓可达域。
        sy = min(max(sy, sy0 + 0.06), sy1 - 0.06)
        dy = min(max(dy, dy0 + 0.06), dy1 - 0.06)
        # v8.0.7 H 边贴合：斜边形状（菱形顶点/IO 斜边/六边形收腰）出入点
        # x 按实际轮廓取（judge 实锤：H 悬空 88-280px 同根因）
        _ssx = resolve_shape(src.get("shape", "round"))
        _dsx = resolve_shape(dst.get("shape", "round"))
        # v8.1.1 侧向端口离框角 ≥0.12in（箭头半宽 0.10——旧余量 0.06 时翼片探出框角）。
        # 注：试过对文件形（波浪底）再按真实轮廓抬高，夹具看图是把另一条入线挤成了
        # 从下方戳进波浪底，更难看，已撤回——文件形侧向端口沿用同一余量。
        sy = min(max(sy, sy0 + 0.12), sy1 - 0.12)
        dy = min(max(dy, dy0 + 0.12), dy1 - 0.12)
        _sfy = min(max((sy - sy0) / max(sy1 - sy0, 1e-9), 0.0), 1.0)
        _dfy = min(max((dy - dy0) / max(dy1 - dy0, 1e-9), 0.0), 1.0)
        if dcx >= scx:
            _ofx, _ox = _edge_fit_x(_ssx, "r", _sfy)
            _ifx, _ix = _edge_fit_x(_dsx, "l", _dfy)
            return ((sx0 + _ox * (sx1 - sx0), sy),
                    (dx0 + _ix * (dx1 - dx0) + EDGE_NIB, dy))
        _ofx, _ox = _edge_fit_x(_ssx, "l", _sfy)
        _ifx, _ix = _edge_fit_x(_dsx, "r", _dfy)
        return ((sx0 + _ox * (sx1 - sx0), sy),
                (dx0 + _ix * (dx1 - dx0) - EDGE_NIB, dy))
    sx = scx + attach_out * EDGE_STAGGER
    dx = dcx - attach_in * EDGE_STAGGER
    if abs(dcx - scx) <= 0.25:
        sx = dx  # 同列对齐：起终点共 x（直降无 Z 折）
    # v8.0.9 端点列钳制（同 H 分支行钳制：错层过大时 x 出 bbox=悬浮）
    sx = min(max(sx, sx0 + 0.12), sx1 - 0.12)      # v8.1.1 同上：顶/底端口离框角 ≥0.12in
    dx = min(max(dx, dx0 + 0.12), dx1 - 0.12)
    # v8.1.3 入列避开源节点侧尖顶点：菱形/六边形/IO 等的左右顶点就在 bbox 竖边
    # 上，入列（竖段）距顶点 <0.10in 读作贴着尖角走（decision「Low」边竖段离
    # 菱形左顶点 0.045in，评审 minor）。外推到 0.10in 净空；外推后落在目标边
    # 内才生效，否则维持原值（窄目标的候选不因净空而消失）。
    if resolve_shape(src.get("shape", "round")) in (
            "diamond", "hexagon", "io", "manual-op", "manual-input"):
        for _vx in (sx0, sx1):
            if abs(dx - _vx) < 0.10:
                _dx2 = _vx - 0.10 if dx <= _vx else _vx + 0.10
                if dx0 + 0.12 <= _dx2 <= dx1 - 0.12:
                    dx = _dx2
    # v8.0.5 边贴合：非平顶/平底形状（斜顶/顶点/收腰）入出点按**实际轮廓
    # 高度**取——at_t/at_b 语义=该 x 处轮廓边的 y 分数（1.0=bbox 顶 dy1，
    # 0.0=bbox 底 dy0）。入点在边外 |EDGE_NIB| 处，出点在边线上。
    _ss = resolve_shape(src.get("shape", "round"))
    _ds = resolve_shape(dst.get("shape", "round"))
    if dcy >= scy:   # 目标在上：源顶出 / 目标底边入（外偏 |NIB|=下方向）
        _ofx, _oy = _edge_fit(_ss, "t", (sx - sx0) / max(sx1 - sx0, 1e-9))
        _ifx, _iy = _edge_fit(_ds, "b", (dx - dx0) / max(dx1 - dx0, 1e-9))
        return ((sx0 + _ofx * (sx1 - sx0), sy0 + _oy * (sy1 - sy0)),
                (dx0 + _ifx * (dx1 - dx0),
                 dy0 + _iy * (dy1 - dy0) + EDGE_NIB))
    _ofx, _oy = _edge_fit(_ss, "b", (sx - sx0) / max(sx1 - sx0, 1e-9))
    _ifx, _iy = _edge_fit(_ds, "t", (dx - dx0) / max(dx1 - dx0, 1e-9))
    return ((sx0 + _ofx * (sx1 - sx0), sy0 + _oy * (sy1 - sy0)),
            (dx0 + _ifx * (dx1 - dx0),
             dy0 + _iy * (dy1 - dy0) - EDGE_NIB))  # 顶边入=框外上方 |NIB|


def _seg_hits(p0, p1, blocks, skip_ids):
    sb = (min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1]))
    for b in blocks:
        if b["id"] in skip_ids:
            continue
        if _overlap(sb, _bbox(b), -0.02):
            return True
    return False


def af_flow_last_pool():
    """最近一次 route() 的候选池 [(代价, 路径), ...]（按入池顺序；QC 诊断用）。"""
    return LAST_POOL


def af_flow_last_reject():
    """最近一次 route() 的肘部被拒候选（QC 诊断用；lane 兜底时为空）。"""
    return [] if LAST_REJECT is None else list(LAST_REJECT)


def _pt_seg_dist(px, py, p0, p1):
    """点到线段距离（in）——箭头头域避让用。"""
    vx, vy = p1[0] - p0[0], p1[1] - p0[1]
    wx, wy = px - p0[0], py - p0[1]
    L2 = vx * vx + vy * vy
    t_ = max(0.0, min(1.0, (wx * vx + wy * vy) / max(L2, 1e-12)))
    return math.hypot(px - (p0[0] + t_ * vx), py - (p0[1] + t_ * vy))


def _seg_cross_line(a, b, p, q):
    """轴对齐段 ab 与线段 pq 是否规范相交（端点相触不算）。未路由边的交叉估计用。"""
    def _o(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])
    d1, d2 = _o(p, q, a), _o(p, q, b)
    if d1 * d2 >= 0:
        return False
    d3, d4 = _o(a, b, p), _o(a, b, q)
    return d3 * d4 < 0


def _bus_overlap(pts, buses, min_sep=0.12, min_ov=0.05, end_trim=0.30):
    """候选路径是否有段与已路由总线**共线重叠**（两条不同的边叠成一条线=其中
    一条被遮住）。候选段两端各 end_trim 内的共用不算（同源/同汇边的合法短干）。"""
    for k in range(len(pts) - 1):
        (ax_, ay_), (bx_, by_) = pts[k], pts[k + 1]
        if abs(ax_ - bx_) < 1e-9:
            axis, c, lo, hi = "v", ax_, min(ay_, by_), max(ay_, by_)
        elif abs(ay_ - by_) < 1e-9:
            axis, c, lo, hi = "h", ay_, min(ax_, bx_), max(ax_, bx_)
        else:
            continue
        lo2, hi2 = lo + end_trim, hi - end_trim
        for (axk, bc, blo, bhi) in buses:
            if axk != axis or abs(c - bc) >= min_sep:
                continue
            o_lo, o_hi = max(lo, blo, lo2), min(hi, bhi, hi2)
            if o_hi - o_lo > min_ov:
                return True
    return False


def _head_zone_hit(p0, p1, hx, hy, ux, uy):
    """段是否侵入箭头头域矩形（tip 沿进入方向 u 后延 0.16、横向 ±0.08）。
    路由全正交→u 轴对齐→矩形轴对齐，直接区间相交判定。"""
    if abs(ux) >= abs(uy):   # 水平进入：头三角沿 x 展开
        x_lo, x_hi = hx - 0.16 * (1 if ux > 0 else -1), hx + 0.02 * (1 if ux > 0 else -1)
        x_lo, x_hi = min(x_lo, x_hi), max(x_lo, x_hi)
        y_lo, y_hi = hy - 0.08, hy + 0.08
    else:
        y_lo, y_hi = hy - 0.16 * (1 if uy > 0 else -1), hy + 0.02 * (1 if uy > 0 else -1)
        y_lo, y_hi = min(y_lo, y_hi), max(y_lo, y_hi)
        x_lo, x_hi = hx - 0.08, hx + 0.08
    sx_lo, sx_hi = min(p0[0], p1[0]), max(p0[0], p1[0])
    sy_lo, sy_hi = min(p0[1], p1[1]), max(p0[1], p1[1])
    return sx_lo < x_hi and x_lo < sx_hi and sy_lo < y_hi and y_lo < sy_hi


# ── v8.0.9 软障碍几何（judge R6 机械探针根修）──────────────────────────
# _seg_hits 对 src/dst 全豁免的盲区：端点不贴轮廓时段穿本体/目标体无检出
# （菱形横穿 2.79in/埋顶点出线 1.29in 实锤）。软检查=对 src/dst 用**真实
# 轮廓**（多边形/椭圆）测内部穿透，端点 tol 内贴轮廓出入豁免。
def _pt_in_poly(x, y, poly):
    c = False
    n = len(poly)
    for i in range(n):
        ax_, ay_ = poly[i]
        bx_, by_ = poly[(i + 1) % n]
        if (ay_ > y) != (by_ > y):
            xx = ax_ + (y - ay_) / (by_ - ay_) * (bx_ - ax_)
            if x < xx:
                c = not c
    return c


def _shape_poly(b):
    """块 → 轮廓顶点；圆类（round/terminal/delay）返回 None（走椭圆判）。"""
    x0, y0, x1, y1 = _bbox(b)
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    sh = resolve_shape(b.get("shape", "round"))
    if sh == "diamond":
        return [(cx, y1), (x1, cy), (cx, y0), (x0, cy)]
    if sh == "hexagon":
        return [(x0 + .22 * w, y1), (x0 + .78 * w, y1), (x1, cy),
                (x0 + .78 * w, y0), (x0 + .22 * w, y0), (x0, cy)]
    if sh == "io":
        return [(x0 + .14 * w, y1), (x1, y1), (x1 - .14 * w, y0), (x0, y0)]
    if sh == "manual-op":
        return [(x0 + .14 * w, y1), (x1 - .14 * w, y1), (x1, y0), (x0, y0)]
    if sh == "manual-input":
        return [(x0, y0), (x0, y0 + .74 * h), (x1, y1), (x1, y0)]
    if sh == "document":
        # v8.0.9 R11：波浪底多边形（贝塞尔采样）——软检查用 bbox 会把
        # 波浪出点→下方的合法轴线判成「穿 bbox 底部条带」（直连被拒→
        # lane 兜底垃圾路由实锤）
        wav = 0.14 * h
        pts_ = [(x0, y0 + wav), (x0, y1), (x1, y1), (x1, y0 + wav)]
        for i in range(1, 20):
            t_ = i / 20
            px_ = x1 - w * ((1 - t_) ** 3 + 3 * t_ * (1 - t_) ** 2 * 0.75
                            + 3 * t_ ** 2 * (1 - t_) * 0.5)
            py_ = y0 + wav * ((1 - t_) ** 3 + 3 * t_ * (1 - t_) ** 2 * 0.1
                              + 3 * t_ ** 2 * (1 - t_) * 1.9 + t_ ** 3)
            pts_.append((px_, py_))
        return pts_
    return None


def _pt_in_soft(x, y, b):
    """点是否在块实体内部（真实轮廓语义）。"""
    poly = _shape_poly(b)
    if poly is not None:
        return _pt_in_poly(x, y, poly)
    x0, y0, x1, y1 = _bbox(b)
    sh = resolve_shape(b.get("shape", "round"))
    if sh in ("round", "terminal", "delay"):
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        return ((x - cx) / max(rx, 1e-9)) ** 2 + \
            ((y - cy) / max(ry, 1e-9)) ** 2 <= 1.0
    return x0 <= x <= x1 and y0 <= y <= y1


def _seg_soft_pen(p0, p1, b, tol=0.03):
    """段在块实体内部的穿透长度（in）。端点 tol 内=贴轮廓出入豁免。"""
    import math as _m
    L = _m.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if L < 1e-9:
        return 0.0
    n = max(int(L / 0.02), 8)
    _in = 0
    for k in range(n + 1):
        t = k / n
        px = p0[0] + (p1[0] - p0[0]) * t
        py = p0[1] + (p1[1] - p0[1]) * t
        if _m.hypot(px - p0[0], py - p0[1]) < tol \
                or _m.hypot(px - p1[0], py - p1[1]) < tol:
            continue
        if _pt_in_soft(px, py, b):
            _in += 1
    return _in / n * L


def _sep_zones(blocks):
    """泳道分隔带区间列表 [(lo, hi, kind)]：kind="v"=垂直带（TB 列间），
    "h"=水平带（LR v8.1.0 行间）；±0.03 keep-out。非泳道=[]。"""
    zs = []
    if blocks and "_lanes_geo" in blocks[0]:
        lg = blocks[0]["_lanes_geo"]
        _horiz = len(lg) > 1 and all(
            abs(g["x"] - lg[0]["x"]) < 1e-6
            and abs(g["w"] - lg[0]["w"]) < 1e-6 for g in lg)
        for a, b2 in zip(lg, lg[1:]):
            if _horiz:
                # LR 行带（v8.1.0）：相邻行带的可见线=上带底缘与下带顶缘，
                # 各 ±0.03 细 zone——中间 0.24in 自由走廊留给跨行水平段
                # （整带大 zone 会把走廊也封死，跨行路由全堵死实锤）
                zs.append((a["y"] - 0.03, a["y"] + 0.03, "h"))
                zs.append((b2["y"] + b2["h"] - 0.03, b2["y"] + b2["h"] + 0.03, "h"))
            else:        # TB 列带：分隔带为垂直区间
                lo = min(a["x"] + a["w"], b2["x"]) - 0.03
                hi = max(a["x"] + a["w"], b2["x"]) + 0.03
                zs.append((lo, hi, "v"))
    return zs


def _sep_parallel(p0, p1, zones, min_run=0.2):
    """段是否沿分隔带平行长跑（骑线=与分隔线视觉合并，judge E4 实锤）。
    垂直段 vs "v" 带 / 水平段 vs "h" 带（LR），平行覆盖 >min_run → True；
    垂直穿越不拦。"""
    if not zones:
        return False
    if abs(p0[0] - p1[0]) <= 1e-6 and abs(p0[1] - p1[1]) > min_run:
        x = p0[0]
        for z in zones:
            if z[2] == "v" and z[0] <= x <= z[1]:
                return True
    if abs(p0[1] - p1[1]) <= 1e-6 and abs(p0[0] - p1[0]) > min_run:
        y = p0[1]
        for z in zones:
            if z[2] == "h" and z[0] <= y <= z[1]:
                return True
    return False


def _edge_between(src, dst):
    sx0, sy0, sx1, sy1 = _bbox(src)
    dx0, dy0, dx1, dy1 = _bbox(dst)
    scx, scy = (sx0 + sx1) / 2, (sy0 + sy1) / 2
    dcx, dcy = (dx0 + dx1) / 2, (dy0 + dy1) / 2
    if abs(dcx - scx) >= abs(dcy - scy):
        return "H", (1 if dcx >= scx else -1)
    return "V", (1 if dcy >= scy else -1)


def _lane_y(blocks, side, level):
    tops = max(_bbox(b)[3] for b in blocks)
    bots = min(_bbox(b)[1] for b in blocks)
    if "_lanes_geo" in blocks[0]:
        # swimlane：lane 绕行走标题带之外（band 区间 [H+0.30,H+0.80]→外扩 1.0）
        tops += 1.0
        bots -= 1.0
    return (tops + LANE_GAP + LANE_STAGGER * level) if side > 0 else \
           (bots - LANE_GAP - LANE_STAGGER * level)


def route(src, dst, blocks, lane_level=0, side=None, orthogonal=False,
          attach_in=0, attach_out=0, avoid_x=(), avoid_heads=(),
          avoid_ports=(), pending=()):
    """R1/R4：直连（干净）→离轴 3 段正交肘（多走廊位验证）→lane 绕行
    （双侧×错层验证）。肘与 lane 统一「验证通过者优先」，无 lane_level 硬闸。
    v8.0.4：attach 错层在入口传入 magnet——所有分支（直连/肘/lane）端点
    统一吃错层，杜绝多边同点叠撞（蛇形 F→B 回边与 A→B 同点实测抓获）。
    v8.0.9：①统一 _blocked 判定=_seg_hits+分隔带骑线+src/dst 软穿透
    （端点不贴轮廓的穿本体根除）②avoid_x=往返对总线分离（肘 gx/lane lx
    避开先行边总线 ±0.16，judge 实锤 Δ=0.01in 视觉重合假 T 分岔）。"""
    key, sgn = _edge_between(src, dst)
    if side is None:
        side = sgn
    p0, p1 = magnet(src, dst, attach_in=attach_in, attach_out=attach_out)
    _skip = (src["id"], dst["id"])
    _zones = _sep_zones(blocks)
    _rej = []      # QC：肘部被拒候选 (键, 走廊位, [被拦的段号]) / (键, 走廊位, "总线避让")

    def _blocked(q0, q1):
        if _seg_hits(q0, q1, blocks, _skip):
            return True
        if _sep_parallel(q0, q1, _zones):
            return True
        if _seg_soft_pen(q0, q1, src) > 0.02 \
                or _seg_soft_pen(q0, q1, dst) > 0.02:
            return True
        # v8.0.9 R10：已路由边的箭头头域禁区——方向感知矩形（头三角实测
        # 0.145×0.10in：沿进入方向后延 0.16、横向 ±0.08）。径向 0.22 过杀
        # （query→sitefix mid 候选距头尖 0.221 被边际拒掉→全候选灭→lane
        # 兜底，手算复算实锤）。rework 虚线压印 TLF→review 头仍被拦截。
        for (hx, hy, ux, uy) in avoid_heads:
            if _head_zone_hit(q0, q1, hx, hy, ux, uy):
                return True
        return False

    # v8.1.0 本边起/终节点的**直边贴边**：线段（掐掉出入口 0.13in）在节点
    # 包围盒外侧、与盒边平行、相距 <0.06in、并行 >0.15in → 计贴近。旧版对
    # 起/终节点整段豁免：「沿框右缘外侧 0.02in 滑 0.67in 止于右下圆角」因此
    # 零代价中标（scRNA-seq 参考基因组→Alignment，r23/r32 看图实测）。只认
    # 侧边是直边的形状：菱形/六边形/梯形的包围盒侧线只在顶点处与轮廓重合，
    # 按盒算会把斜边旁的合法走线误判（r29 实测）。
    def _hug_own(pts_):
        _n = 0
        for k2 in range(len(pts_) - 1):
            (ax_, ay_), (bx_, by_) = pts_[k2], pts_[k2 + 1]
            _L_ = abs(bx_ - ax_) + abs(by_ - ay_)
            if _L_ <= 0.26:
                continue
            _c = 0.13 / _L_
            _sx0, _sx1 = sorted((ax_ + (bx_ - ax_) * _c,
                                 ax_ + (bx_ - ax_) * (1 - _c)))
            _sy0, _sy1 = sorted((ay_ + (by_ - ay_) * _c,
                                 ay_ + (by_ - ay_) * (1 - _c)))
            for b in blocks:
                if b["id"] not in _skip:
                    continue
                if resolve_shape(b.get("shape", "round")) in (
                        "diamond", "hexagon", "manual-op", "manual-input", "io"):
                    continue
                _x0, _y0, _x1, _y1 = _bbox(b)
                if abs(ax_ - bx_) < 1e-9:          # 竖段贴左/右缘
                    if (min(_sy1, _y1) - max(_sy0, _y0) > 0.15
                            and 0.0 < min(abs(ax_ - _x0), abs(ax_ - _x1)) < 0.06):
                        _n += 1
                elif abs(ay_ - by_) < 1e-9:        # 横段贴上/下缘
                    if (min(_sx1, _x1) - max(_sx0, _x0) > 0.15
                            and 0.0 < min(abs(ay_ - _y0), abs(ay_ - _y1)) < 0.06):
                        _n += 1
        return _n

    # v8.1.0 已路由边的拐点 (x, y, 竖段 y 范围, 横段 x 范围)——拐角咬合检查用
    _ex_c = []
    for (_axk, _c, _lo_, _hi_) in avoid_x:
        if _axk != "h":
            continue
        for (_axk2, _c2, _lo2, _hi2) in avoid_x:
            if _axk2 != "v":
                continue
            for _exx in (_lo_, _hi_):
                if abs(_exx - _c2) < 1e-6 \
                        and (abs(_c - _lo2) < 1e-6 or abs(_c - _hi2) < 1e-6):
                    _ex_c.append((_exx, _c, tuple(sorted((_lo2, _hi2))),
                                  tuple(sorted((_lo_, _hi_)))))

    def _route_cost(pts):
        """候选代价（越小越好）=（与已路由边交叉数, 节点同角相对而行数, 拐弯数,
        与未路由边的直线估计交叉数, 总长）。v8.1.0：旧版取「第一个合法」，把几何
        合法当成了好——LR 期刊模板 review→decide 因此横穿 accept 边并与它共用菱形
        右角。真实交叉与同角冲突排在拐弯数之前（少一次交叉值得多拐一个弯）；未路由
        边只是直线估计，排在拐弯数之后。"""
        cross = conflict = pend = 0
        length = 0.0
        for k2 in range(len(pts) - 1):
            (ax_, ay_), (bx_, by_) = pts[k2], pts[k2 + 1]
            length += abs(bx_ - ax_) + abs(by_ - ay_)
            for (_axk, _c, _lo_, _hi_) in avoid_x:
                if _axk == "h" and abs(ax_ - bx_) < 1e-9 \
                        and _lo_ + 0.02 < ax_ < _hi_ - 0.02 \
                        and min(ay_, by_) + 0.02 < _c < max(ay_, by_) - 0.02:
                    cross += 1
                elif _axk == "v" and abs(ay_ - by_) < 1e-9 \
                        and _lo_ + 0.02 < ay_ < _hi_ - 0.02 \
                        and min(ax_, bx_) + 0.02 < _c < max(ax_, bx_) - 0.02:
                    cross += 1
            for (_pa, _pb) in pending:
                if _seg_cross_line(pts[k2], pts[k2 + 1], _pa, _pb):
                    pend += 1
        for (_px, _py, _nid, _kind) in avoid_ports:
            if _nid == dst["id"] and _kind == "tail" \
                    and math.hypot(pts[-1][0] - _px, pts[-1][1] - _py) < 0.16:
                conflict += 1
            if _nid == src["id"] and _kind == "head" \
                    and math.hypot(pts[0][0] - _px, pts[0][1] - _py) < 0.16:
                conflict += 1
        # 共线重叠（与交叉同级——被遮住的边比交叉更糟）与贴近（线贴着节点走：
        # 合法性判定有 0.02in 容差，评分制会选到钻容差空子的候选——incident 模板
        # 横线贴 page 底边 0.015in 实锤）
        overlap = 1 if _bus_overlap(pts, avoid_x) else 0
        near = 0
        for k2 in range(len(pts) - 1):
            (ax_, ay_), (bx_, by_) = pts[k2], pts[k2 + 1]
            _sx0, _sx1 = sorted((ax_, bx_))
            _sy0, _sy1 = sorted((ay_, by_))
            for b in blocks:
                if b["id"] in _skip:
                    continue
                _x0, _y0, _x1, _y1 = _bbox(b)
                _dx = max(_x0 - _sx1, _sx0 - _x1, 0.0)
                _dy = max(_y0 - _sy1, _sy0 - _y1, 0.0)
                if math.hypot(_dx, _dy) < 0.06:
                    near += 1
        near += _hug_own(pts)
        # 注：「线贴泳道分隔线平行长跑」试过计贴近（<0.12in），r20 实测引发贪心
        # 路由失败——先路由的边为躲分隔线挪走，把后面边唯一的干净走法堵死
        # （泳道主图 crf→query 实锤），且 0.11in 的间距看放大图可接受，故撤回。
        # 排序（2026-11-24 实测校正）：贴近排在交叉之前——泳道主图 re-check 回边
        # 的几条候选里，「贴着 eCRF 右缘走 0.87in」比「多一次垂直交叉」糟得多，
        # 旧排序（交叉优先）恰恰选了前者。往返边对按拓扑必然交叉一次，可接受。
        # 通道轨道（泳道 LR 行间隙）：分到轨道的边不走在自己轨道上=+1，排在
        # 「未路由边的直线估计交叉」之前——否则估计值会压过轨道分配，三条边
        # 走到与分配相反的轨道上（LR 样例实测）
        _otrk = [t_["line_y"] for g_ in GAP_TRACKS for t_ in g_["tracks"]
                 if tuple(t_["edge"]) == (src["id"], dst["id"])]
        off_track = 0
        if _otrk and not any(abs(p_[1] - _otrk[0]) < 0.02 for p_ in pts):
            off_track = 1
        # 近端口交叉：与已路由边的交叉点离任一端的出入口（或拐点）<0.30in，
        # 或距本边出入口 <0.30in——读起来像从节点直接分出的 T 形分岔（决策模板
        # No 旁路线在菱形底顶点下 0.15in 处穿过 High 分支；泳道主图 crf→query 出
        # eCRF 0.18in 即被 48 h SLA 竖线穿过）。排在普通交叉之前。
        tj = 0
        _own_ends = [pts[0], pts[-1]]
        for k2 in range(len(pts) - 1):
            (ax_, ay_), (bx_, by_) = pts[k2], pts[k2 + 1]
            for (_axk, _c, _lo_, _hi_) in avoid_x:
                if _axk == "h" and abs(ax_ - bx_) < 1e-9 \
                        and _lo_ + 0.02 < ax_ < _hi_ - 0.02 \
                        and min(ay_, by_) + 0.02 < _c < max(ay_, by_) - 0.02:
                    _px, _py, _bn = ax_, _c, [(_lo_, _c), (_hi_, _c)]
                elif _axk == "v" and abs(ay_ - by_) < 1e-9 \
                        and _lo_ + 0.02 < ay_ < _hi_ - 0.02 \
                        and min(ax_, bx_) + 0.02 < _c < max(ax_, bx_) - 0.02:
                    _px, _py, _bn = _c, ay_, [(_c, _lo_), (_c, _hi_)]
                else:
                    continue
                _pe = [any(math.hypot(_ex - _qx, _ey - _qy) < 1e-6
                           for (_qx, _qy, _n, _k) in avoid_ports)
                       for (_ex, _ey) in _bn]
                # 出入口 0.30（读作从节点分出的岔线）；拐点 0.20（拐点处两条臂
                # 都看得见，歧义小于节点旁）——泳道主图 query→sitefix 穿 0.60in
                # 短段时 0.30/0.30 的窗只有一个点，实测 12 个候选全部落空
                # 本边自己的拐点同尺 0.20（r20 泳道主图：48 h SLA 出六边形左顶点
                # 0.18in 即被 crf→query 横段穿过——机械审计抓到、代价函数漏算）
                if min(math.hypot(_px - _ex, _py - _ey)
                       for (_ex, _ey) in _own_ends) < 0.30 - 1e-6 \
                        or min((math.hypot(_px - _ex, _py - _ey)
                                for (_ex, _ey) in pts[1:-1]), default=9) < 0.20 - 1e-6 \
                        or any(math.hypot(_px - _ex, _py - _ey)
                               < (0.30 if _ip else 0.20) - 1e-6
                               for (_ex, _ey), _ip in zip(_bn, _pe)):
                    tj += 1
        # v8.1.0 拐角咬合：本边拐点与已路由边的拐点横向错开 <0.10、纵向相距
        # 0.08-0.20，且两者的竖段上下错开、横段几乎不重叠（或转置）——两条线的
        # 拐角一上一下咬在一起，读起来像接线/交叉（决策模板 No 旁路线与
        # IV→Reassess 的拐角横向只错开 0.06in，r34 看图实测）。与近端口交叉同级：
        # 并排错层的往返边对横段重叠，不会命中。
        def _ov(u_, v_):
            return min(u_[1], v_[1]) - max(u_[0], v_[0])
        for _k3 in range(1, len(pts) - 1):
            _vy_, _hx_ = None, None
            for (_sa_, _sb_) in ((pts[_k3 - 1], pts[_k3]), (pts[_k3], pts[_k3 + 1])):
                if abs(_sa_[0] - _sb_[0]) < 1e-9:
                    _vy_ = sorted((_sa_[1], _sb_[1]))
                else:
                    _hx_ = sorted((_sa_[0], _sb_[0]))
            if _vy_ is None or _hx_ is None:
                continue
            for (_exx, _eyy, _evy, _ehx) in _ex_c:
                _dx, _dy = abs(pts[_k3][0] - _exx), abs(pts[_k3][1] - _eyy)
                if (_dx < 0.10 and 0.08 < _dy < 0.20
                        and _ov(_vy_, _evy) <= 0.02 and _ov(_hx_, _ehx) <= 0.10) \
                        or (_dy < 0.10 and 0.08 < _dx < 0.20
                            and _ov(_hx_, _ehx) <= 0.02 and _ov(_vy_, _evy) <= 0.10):
                    tj += 1
        for (_pa, _pb) in pending:
            for k2 in range(len(pts) - 1):
                if not _seg_cross_line(pts[k2], pts[k2 + 1], _pa, _pb):
                    continue
                (ax_, ay_), (bx_, by_) = pts[k2], pts[k2 + 1]
                _dxl, _dyl = _pb[0] - _pa[0], _pb[1] - _pa[1]
                if abs(ax_ - bx_) < 1e-9 and abs(_dxl) > 1e-9:
                    _tt = (ax_ - _pa[0]) / _dxl
                    _px, _py = ax_, _pa[1] + _tt * _dyl
                elif abs(_dyl) > 1e-9:
                    _tt = (ay_ - _pa[1]) / _dyl
                    _px, _py = _pa[0] + _tt * _dxl, ay_
                else:
                    continue
                # 未路由边的端点是节点中心：距中心 <0.60in（≈半节点+0.30）视为近端口
                if min(math.hypot(_px - _pa[0], _py - _pa[1]),
                       math.hypot(_px - _pb[0], _py - _pb[1])) < 0.60:
                    tj += 1
        # v8.1.0 箭头末段过短：末段（箭头所在段）短于 箭头长 0.145+净空 0.08 时，
        # 箭头翼片垂在拐角之外（竖线下来立刻横走 0.17in 进侧边——翼片后半截露在
        # 竖线下端之下，像一个线头；决策模板 High→IV、伦理模板 conditions→
        # Amendment，视觉评审 R1 放大图实测）。按多两个拐弯计：有「拐弯多一个但
        # 末段够长」的候选时让位；没有时仍可选（好过 lane 兜底）。
        _short_end = 2 if len(pts) >= 3 and (
            abs(pts[-1][0] - pts[-2][0]) + abs(pts[-1][1] - pts[-2][1])) < 0.225 else 0
        return (overlap, near, tj, cross, conflict, off_track,
                len(pts) - 2 + _short_end, pend, round(length, 4))

    if not orthogonal:
        # ① 直连干净→直连（错槽循环 _stag∈{0,1}：槽位计数按物理侧统计，
        # 但相邻侧的先行头/尾仍可能占住本侧默认行——crf→query 头在
        # query 右侧同 rows、query→lock 出点重合行被头域正确拦截（R10
        # 机制）→错一槽重试即得净出口）
        def _direct_pts(aoo, aii):
            _q0, _q1 = magnet(src, dst, attach_in=aii, attach_out=aoo)
            if "_lanes_geo" in blocks[0] and key == "V" \
                    and abs(_q0[0] - _q1[0]) <= 0.02:
                # swimlane：V 直连 x 恰落泳道分隔带 ±0.15 时平移 0.22，平移后
                # 按**真实轮廓重贴**出入点（旧版平移不改 y=端点悬空根因）；
                # 平移后仍在带内则放弃平移（交由肘部/lane 扫描避让）
                _sb, _db = _bbox(src), _bbox(dst)
                _up = (_db[1] + _db[3]) >= (_sb[1] + _sb[3])
                _lo = max(_sb[0] + 0.04, _db[0] + 0.04)
                _hi = min(_sb[2] - 0.04, _db[2] - 0.04)
                for g in blocks[0]["_lanes_geo"]:
                    _div = g["x"] + g["w"]
                    if abs(_q0[0] - _div) <= 0.15:
                        _nx = min(max(_q0[0] + 0.22, _lo), _hi)
                        if not any(zl <= _nx <= zh for (zl, zh, zk) in _zones
                                   if zk == "v"):
                            _ss2 = resolve_shape(src.get("shape", "round"))
                            _ds2 = resolve_shape(dst.get("shape", "round"))
                            _ofx2, _oy2 = _edge_fit(
                                _ss2, "t" if _up else "b",
                                (_nx - _sb[0]) / max(_sb[2] - _sb[0], 1e-9))
                            _ifx2, _iy2 = _edge_fit(
                                _ds2, "b" if _up else "t",
                                (_nx - _db[0]) / max(_db[2] - _db[0], 1e-9))
                            _q0 = (_nx, _sb[1] + _oy2 * (_sb[3] - _sb[1]))
                            _q1 = (_nx, _db[1] + _iy2 * (_db[3] - _db[1])
                                   + (EDGE_NIB if _up else -EDGE_NIB))
                        break
            return _q0, _q1

        # v8.1.0 候选评分制：收集全部合法候选，按 _route_cost 取最优。入池顺序
        # 保留旧版优先序，作代价完全相同时的并列裁决（旧选择不被无故改动）。
        _pool = []

        def _corners_ok(pts):
            """拐点不得落入非端点块（弯在框里=贴框/穿框；此前只有 lane 兜底查）。"""
            for _p in pts[1:-1]:
                for b in blocks:
                    if b["id"] in _skip:
                        continue
                    x0, y0, x1, y1 = _bbox(b)
                    if x0 - 0.01 < _p[0] < x1 + 0.01 and y0 - 0.01 < _p[1] < y1 + 0.01:
                        return False
            return True

        def _add(pts):
            _cl = []
            for _p in pts:      # 去零长段
                if not _cl or abs(_p[0] - _cl[-1][0]) > 1e-9 \
                        or abs(_p[1] - _cl[-1][1]) > 1e-9:
                    _cl.append(_p)
            if len(_cl) >= 2 and _corners_ok(_cl):
                _pool.append(_cl)

        for _stag in (0, 1):
            _aoo, _aii = attach_out + _stag, attach_in + _stag
            _p0, _p1 = (p0, p1) if _stag == 0 else \
                magnet(src, dst, attach_in=_aii, attach_out=_aoo)
            _p0, _p1 = _direct_pts(_aoo, _aii)
            if not _blocked(_p0, _p1):
                if key == "H" and abs(_p0[1] - p1[1]) > 0.05:
                    gx = (_p0[0] + _p1[0]) / 2
                    _add([(_p0[0], _p0[1]), (gx, _p0[1]), (gx, _p1[1]),
                          (_p1[0], _p1[1])])
                elif key == "V" and abs(_p0[0] - _p1[0]) > 0.05:
                    gy = (_p0[1] + _p1[1]) / 2
                    _add([(_p0[0], _p0[1]), (_p0[0], gy), (_p1[0], gy),
                          (_p1[0], _p1[1])])
                else:
                    _add([_p0, _p1])
        # ② 直连穿框→正交肘：走廊**限定在两锚点之间**（v8.0.4 根修两处——
        #    旧版 H 键误用 Y 中值当 X 走廊（轴向错用），且走廊无界扫描可落在
        #    目标框远侧 → 末段整段横穿目标框内部，而 _seg_hits 的端点豁免
        #    把目标框整体豁免导致零检出（visual-judge 实锤「箭头穿框」根因）。
        #    走廊限位后末段永远从附着边外侧进线，穿框在构造上不可能。）
        #    v8.0.4 轴向回退：主轴向走廊区间空/全堵时换垂直轴向重试（force_key
        #    换边磁吸）——蛇形回边 F→B 因此改走行间槽（H 走廊仅 0.16in 且
        #    出口 T 压在 E→F 边上，judge 实锤）。
        def _elbow_scan(k, q0, q1, first_only=True):
            if k == "H":
                _lo = min(q0[0], q1[0]) + 0.3
                _hi = max(q0[0], q1[0]) - 0.3
                _mid = (q0[0] + q1[0]) / 2
            else:
                _lo = min(q0[1], q1[1]) + 0.3
                _hi = max(q0[1], q1[1]) - 0.3
                _mid = (q0[1] + q1[1]) / 2
            if _lo > _hi:
                return None if first_only else []
            found = []
            # v8.0.9 候选采样升级：0.3 步进网格会跨过「分隔带侧翼/走廊缘」
            # 之间的有效窄窗（宽 0.06-0.15in）——query↔sitefix 往返对实测
            # 唯一净窗被网格跨过→误判全堵→画布外 lane 环（judge R8 无锚
            # 走廊根因之一）。候选=中点±步进 ∪ 分隔带两侧翼 ∪ 走廊两缘。
            _cands = [_mid]
            _step = 0.3
            while _step <= max(_hi - _lo, 0.3) + 0.3:
                _cands += [_mid - _step, _mid + _step]
                _step += 0.3
            if "_lanes_geo" in blocks[0]:
                if k == "H":
                    for (zl, zh, zk) in _zones:
                        if zk == "v":   # TB 垂直带侧翼
                            _cands += [zl - 0.08, zh + 0.08]
                else:   # V 肘：LR 行间隙候选（行带纯内容化后 0.30 间隙
                    # =干净水平走廊）——中心±0.07 预播种：多边共享走廊时
                    # 错层而非拒绝（R14 实锤：拒绝→第二边落 lane 兜底穿节点）
                    _lg_ = blocks[0]["_lanes_geo"]
                    for _a, _b2 in zip(_lg_, _lg_[1:]):
                        _gmid = (_a["y"] + _b2["y"] + _b2["h"]) / 2
                        # v8.1.0：缝够宽（≥0.6，带标签带）时两条走线拉开到 ±0.14，
                        # 线与行带边之间各留出放标签的净空
                        _hs = 0.14 if (_a["y"] - (_b2["y"] + _b2["h"])) >= 0.6 else 0.07
                        _cands += [_gmid - _hs, _gmid, _gmid + _hs]
                _cands += [_lo + 0.05, _hi - 0.05]
            # v8.0.9 R10 走廊外扩：锚点 ±0.3 的走廊会把窄净窗关在门外
            # （incident re-triage 唯一净窗 hi+0.15 实锤）——四档有界外扩
            _cands += [_lo - 0.15, _lo - 0.35, _hi + 0.15, _hi + 0.35]

            # v8.1.0 净空推导候选：中段每穿过一条已路由的线，交叉点离那条线的
            # 出入口 ≥0.30in、离拐点 ≥0.20in 才不读作 T 形分岔。固定步进取样会
            # 跨过这种窄窗（泳道主图 query→sitefix 穿 crf→query 的 0.60in 短段，
            # 合法窗只有一个点，12 个候选全落在窗外实测）——按被穿线段的两端
            # 直接推导：两端净空都够→窗的中点；不够（短段）→贴近要求低的一端
            # 让位，另给线段中点，由代价函数择优。
            def _clr(_a, _b, _bc):
                _e0, _e1 = ((_a, _bc), (_b, _bc)) if k == "H" else ((_bc, _a), (_bc, _b))
                _ca = 0.31 if any(math.hypot(_e0[0] - _qx, _e0[1] - _qy) < 1e-6
                                  for (_qx, _qy, _n, _k) in avoid_ports) else 0.21
                _cb = 0.31 if any(math.hypot(_e1[0] - _qx, _e1[1] - _qy) < 1e-6
                                  for (_qx, _qy, _n, _k) in avoid_ports) else 0.21
                if _a + _ca <= _b - _cb:
                    return [(_a + _ca + _b - _cb) / 2]
                return [_a + _ca, _b - _cb, (_a + _b) / 2]

            _sp = ((min(q0[0], q1[0]), max(q0[0], q1[0])) if k == "V"
                   else (min(q0[1], q1[1]), max(q0[1], q1[1])))
            for (_ax_, _bc, _blo_, _bhi_) in avoid_x:
                if _ax_ == ("v" if k == "V" else "h") \
                        and _sp[0] + 0.02 < _bc < _sp[1] - 0.02:
                    _cands += _clr(_blo_, _bhi_, _bc)
            # v8.1.0 通道轨道：本边分到的轨道高度排最前，其余轨道高度次之
            # （自己的轨道被占时才退而求其次）。
            if k == "V" and GAP_TRACKS:
                _own = (src["id"], dst["id"])
                _tl = [t_["line_y"] for g_ in GAP_TRACKS
                       for t_ in g_["tracks"] if tuple(t_["edge"]) == _own]
                _to = [t_["line_y"] for g_ in GAP_TRACKS
                       for t_ in g_["tracks"] if tuple(t_["edge"]) != _own]
                _cands = _tl + _to + _cands
            _qy_lo, _qy_hi = min(q0[1], q1[1]), max(q0[1], q1[1])
            _qx_lo, _qx_hi = min(q0[0], q1[0]), max(q0[0], q1[0])
            _alo, _ahi = _lo - 0.4, _hi + 0.4   # v8.0.9 R10 外扩验收窗
            if k == "V" and GAP_TRACKS:
                # 通道轨道的下界：轨道就在目标上方的标题带之上，「离目标 ≥0.3」
                # 的旧下界会把底部轨道挡在验收窗外——放宽到不离目标顶太近即可
                _alo = min(q0[1], q1[1]) + 0.05
            # v8.1.0 自由区间中点候选：中段行程上，已路由的平行线（±0.16，与总线
            # 避让同口径）和非本端节点包围盒（±0.10：合法性只拦 ±0.02，取中点时
            # 给节点角多留净空——菱形左角旁 0.079in 实测偏挤）占掉的
            # 区间之外，每段自由区间的中点——窄缝里唯一的净位。泳道主图
            # sitefix→query：crf→query 竖线与 lock 菱形左角之间只有 0.15in，固定
            # 取样一个都落不进去（66 个候选全拒实测），于是退回 3 处交叉的走法。
            _occ = []
            for (_ax_, _bc, _blo_, _bhi_) in avoid_x:
                if _ax_ == ("v" if k == "H" else "h") \
                        and min(_qy_hi, _bhi_) - max(_qy_lo, _blo_) > 0.1:
                    _occ.append((_bc - 0.16, _bc + 0.16))
            for _b in blocks:
                if _b["id"] in _skip:
                    continue
                _bb = _bbox(_b)
                if k == "H":
                    if min(_qy_hi, _bb[3]) - max(_qy_lo, _bb[1]) > 0.02:
                        _occ.append((_bb[0] - 0.10, _bb[2] + 0.10))
                elif min(_qx_hi, _bb[2]) - max(_qx_lo, _bb[0]) > 0.02:
                    _occ.append((_bb[1] - 0.10, _bb[3] + 0.10))
            _occ.sort()
            _mrg = []
            for _s, _e in _occ:
                if _mrg and _s <= _mrg[-1][1]:
                    _mrg[-1][1] = max(_mrg[-1][1], _e)
                else:
                    _mrg.append([_s, _e])
            _cur = _alo
            for _s, _e in _mrg + [(_ahi, _ahi)]:
                _s = max(_s, _alo)
                if _s - _cur >= 0.04:
                    _cands.append(round((_cur + _s) / 2, 3))
                _cur = max(_cur, min(_e, _ahi))
            for _g in _cands:
                if not (_alo <= _g <= _ahi):
                    continue
                # v8.0.9 总线区间避让（R14 扩双轴）：候选轴上任意已路由
                # 线 |Δ|<0.16 且本边行程与其区间重叠 >0.1 → 拒（共线树干
                # 根除，垂直/水平各查各轴，不限同对）
                if any(((_k == "H" and _ax_ == "v") or (_k == "V" and _ax_ == "h"))
                       and abs(_g - _bc) < 0.16
                       and (min(_qy_hi, _bhi) - max(_qy_lo, _blo) > 0.1
                            if _k == "H" else
                            min(_qx_hi, _bhi) - max(_qx_lo, _blo) > 0.1)
                       for (_ax_, _bc, _blo, _bhi) in avoid_x):
                    _rej.append((k, round(_g, 3), "总线避让"))
                    continue
                _cand = ([(q0[0], q0[1]), (_g, q0[1]), (_g, q1[1]), (q1[0], q1[1])]
                         if k == "H" else
                         [(q0[0], q0[1]), (q0[0], _g), (q1[0], _g), (q1[0], q1[1])])
                _bad = [k2 for k2 in range(3) if _blocked(_cand[k2], _cand[k2 + 1])]
                if not _bad:
                    if first_only:
                        return _cand
                    found.append(_cand)
                else:
                    _rej.append((k, round(_g, 3), _bad, [round(_q, 3) for _q in q0],
                                 [round(_q, 3) for _q in q1]))
            return None if first_only else found

        for _stag in (0, 1):
            _aoo, _aii = attach_out + _stag, attach_in + _stag
            for _k in (key, "V" if key == "H" else "H"):
                _q0, _q1 = (_p0, _p1) if (_k == key and _stag == 0) else \
                    magnet(src, dst, attach_in=_aii, attach_out=_aoo,
                           force_key=_k)
                for _c in _elbow_scan(_k, _q0, _q1, first_only=False):
                    _add(_c)
            # v8.1.0 混合键候选：从源节点左/右缘出、进目标节点顶/底（或反之）
            # ——「源在目标的斜上/斜下方」这类跨行连接的自然走法（2 个弯）。
            # 仅靠 H/V 单键肘无法表达它（LR 期刊模板 review→decide 实锤）。
            _h0, _ = magnet(src, dst, attach_in=_aii, attach_out=_aoo,
                            force_key="H")
            _, _h1 = magnet(src, dst, attach_in=_aii, attach_out=_aoo,
                            force_key="H")
            _v0, _ = magnet(src, dst, attach_in=_aii, attach_out=_aoo,
                            force_key="V")
            _, _v1 = magnet(src, dst, attach_in=_aii, attach_out=_aoo,
                           force_key="V")
            for (_a_, _b_) in ((_h0, _v1), (_v0, _h1)):
                # 拐点按「先沿出段方向、再转入段方向」取：侧出→顶/底入=先横后竖；
                # 顶/底出→侧入=先竖后横。旧写法两种都按先横后竖拼，后一种的末段
                # 沿目标侧边线下行=贴边滑到角上（参考基因组→Alignment 沿框右缘
                # 外侧 0.02in 滑 0.67in 止于右下圆角，r23 看图实测）
                _cand = [_a_, ((_b_[0], _a_[1]) if _a_ is _h0 else (_a_[0], _b_[1])),
                         _b_]
                if all(not _blocked(_cand[k2], _cand[k2 + 1])
                       for k2 in range(len(_cand) - 1)):
                    _add(_cand)
        # v8.1.0 镜像入槽：分到中线一侧的入槽（attach_in ≥ 1）且候选池里有**贴着自己节点
        # 直边**的候选时，再试「入槽镜像到中线另一侧」的肘形候选——同一侧
        # 的第 2 条入线挤在先前那条的拐角旁，标准候选要么擦到它、要么贴边滑行
        # （scRNA-seq 参考基因组→Alignment：入槽与 Sequencing→Alignment 的末段只
        # 隔 0.18in，r23/r32 看图实测）。镜像候选排在标准候选之后——只有代价
        # 严格更低才会选中；触发条件收窄到「贴边」，不影响其它边。
        # v8.1.0 对齐直落/直升：源节点的中心列落在目标顶/底边内侧时，试一条竖直
        # 直达线（目标入点取源出点同一 x）——宽节点接收上方多个来源时各走各的竖线，
        # 而不是先横到目标中线附近再折下（两方法对照模板：Sectioning 与
        # Cryosectioning 各伸出一小段横线、在同一高度叠成一条贯通横线，读起来像
        # 两个互不相连的平行臂直接相连；视觉评审 FAIL + 机械审计 D 共线重叠 0.18in
        # 实测）。入点离两角 ≥0.16、离已用端口 ≥0.18，双方顶/底边为直边才试。
        _STR810 = ("round", "rect", "document", "predefined", "io")
        _sbx, _sby, _sbX, _sbY = _bbox(src)
        _dbx, _dby, _dbX, _dbY = _bbox(dst)
        _scx_, _scy_ = (_sbx + _sbX) / 2, (_sby + _sbY) / 2
        _dcx_, _dcy_ = (_dbx + _dbX) / 2, (_dby + _dbY) / 2
        _ss810 = resolve_shape(src.get("shape", "round"))
        _ds810 = resolve_shape(dst.get("shape", "round"))
        if (_ss810 in _STR810 and _ds810 in _STR810
                and _dbx + 0.16 <= _scx_ <= _dbX - 0.16
                and abs(_dcy_ - _scy_) > 0.25):
            _fs810 = (_scx_ - _sbx) / max(_sbX - _sbx, 1e-9)
            _fd810 = (_scx_ - _dbx) / max(_dbX - _dbx, 1e-9)
            if _dcy_ < _scy_:      # 目标在下：源底出、目标顶入
                _of8, _og8 = _edge_fit(_ss810, "b", _fs810)
                _if8, _ig8 = _edge_fit(_ds810, "t", _fd810)
                _pa8 = (_sbx + _of8 * (_sbX - _sbx), _sby + _og8 * (_sbY - _sby))
                _pb8 = (_dbx + _if8 * (_dbX - _dbx),
                        _dby + _ig8 * (_dbY - _dby) - EDGE_NIB)
            else:                  # 目标在上：源顶出、目标底入
                _of8, _og8 = _edge_fit(_ss810, "t", _fs810)
                _if8, _ig8 = _edge_fit(_ds810, "b", _fd810)
                _pa8 = (_sbx + _of8 * (_sbX - _sbx), _sby + _og8 * (_sbY - _sby))
                _pb8 = (_dbx + _if8 * (_dbX - _dbx),
                        _dby + _ig8 * (_dbY - _dby) + EDGE_NIB)
            _free8 = True
            for (_px8, _py8, _n8, _k8) in avoid_ports:
                _ref8 = _pa8 if _n8 == src["id"] else (_pb8 if _n8 == dst["id"] else None)
                if _ref8 is not None and math.hypot(_px8 - _ref8[0], _py8 - _ref8[1]) < 0.18:
                    _free8 = False
            if _free8 and not _blocked(_pa8, _pb8):
                _add([_pa8, _pb8])

        _hg = 0
        if attach_in >= 1 and _pool:
            # 候选池里只要有「贴自己节点直边」的候选就触发（贴边候选计了贴近后已
            # 不是最优，按「最优者是否贴边」触发会漏——r33 实测）
            _hg = sum(1 for _p in _pool if _hug_own(_p))
        if _hg:
            for _stag in (0, 1):
                _aoo, _aii = attach_out + _stag, -(attach_in + _stag)
                for _k in (key, "V" if key == "H" else "H"):
                    _q0, _q1 = magnet(src, dst, attach_in=_aii, attach_out=_aoo,
                                      force_key=_k)
                    for _c in _elbow_scan(_k, _q0, _q1, first_only=False):
                        _add(_c)
        global LAST_POOL, LAST_REJECT
        LAST_REJECT = list(_rej)
        if _pool:
            _scored = [(_route_cost(_p), _p) for _p in _pool]
            LAST_POOL = _scored
            return min(enumerate(_scored),
                       key=lambda _e: (_e[1][0], _e[0]))[1][1], side
    sx0, sy0, sx1, sy1 = _bbox(src)
    dx0, dy0, dx1, dy1 = _bbox(dst)

    def _v_corridor_y(x, y_from, going_up=True, sd=1, lv=1):
        """x 列上方（或下方）首个障碍的下/上沿-0.15；无障碍→lane 高度。
        v8.0.5：V lane 直升段穿中间层框（形状放大后布局变密实锤）→
        首段先升到障碍之下，横移到 lane x 后再升。"""
        _ly = _lane_y(blocks, sd, lv)
        best = _ly
        for b in blocks:
            if b["id"] in _skip:
                continue
            bx0, by0, bx1, by1 = _bbox(b)
            if bx0 - 0.05 <= x <= bx1 + 0.05:
                if going_up and by0 > y_from + 0.05 and by0 - 0.15 < best:
                    best = by0 - 0.15
                if not going_up and by1 < y_from - 0.05 and by1 + 0.15 > best:
                    best = by1 + 0.15
        return best

    def _lane_pts(sd, lv):
        # 终点与磁吸同纪律：负咬合回退（EDGE_NIB=-0.01），尖端止于描边外沿。
        # v8.0.5 边贴合：V lane 终点按形状实际轮廓高度取（斜顶/顶点）；
        # 首末垂直段经走廊探测避障（5 段 L-L-L 形，judge 实锤穿层根除）
        _ss = resolve_shape(src.get("shape", "round"))
        _ds = resolve_shape(dst.get("shape", "round"))
        if key == "H":
            # v8.1.0：H 键绕行的顶/底出入点同样按**真实轮廓**贴合（旧版直接取
            # 包围盒边——文档波浪底/菱形顶点/IO 斜边上回边端点悬空，CRISPR 模板
            # rank→transduce 起点浮离 0.114in 实锤）
            ly = _lane_y(blocks, sd, lv)
            _ofx, _oy = _edge_fit(_ss, "t" if sd > 0 else "b", 0.5)
            _ifx, _iy = _edge_fit(_ds, "t" if sd > 0 else "b", 0.5)
            return [((sx0 + sx1) / 2, sy0 + _oy * (sy1 - sy0)),
                    ((sx0 + sx1) / 2, ly),
                    ((dx0 + dx1) / 2, ly),
                    ((dx0 + dx1) / 2,
                     dy0 + _iy * (dy1 - dy0) + (-EDGE_NIB if sd > 0 else EDGE_NIB))]
        lx = (max(_bbox(b)[2] for b in blocks) + LANE_GAP + LANE_STAGGER * lv) \
            if sd > 0 else \
            (min(_bbox(b)[0] for b in blocks) - LANE_GAP - LANE_STAGGER * lv)
        _lyy_lo, _lyy_hi = min(sy0, sy1, dy0, dy1), max(sy0, sy1, dy0, dy1)
        if any(_ax_ == "v" and abs(lx - _bx) < 0.16
               and min(_lyy_hi, _byhi) - max(_lyy_lo, _bylo) > 0.1
               for (_ax_, _bx, _bylo, _byhi) in avoid_x):
            lx += 0.20 * (1 if sd > 0 else -1)   # v8.0.9 lane 总线区间分离
        # v8.0.7 lane 出入点吃 attach 错层（往返对 lane 路径两线贴合根因）
        _stag = attach_out * EDGE_STAGGER * (sx1 - sx0)
        _stag2 = attach_in * EDGE_STAGGER * (dx1 - dx0)
        _dfx = ((dx0 + dx1) / 2 + _stag2 - dx0) / max(dx1 - dx0, 1e-9)
        _ly = _lane_y(blocks, sd, lv)
        if sd > 0:   # 上行 lane：从源顶出、目标顶入
            _ofx, _oy = _edge_fit(_ss, "t", ((sx0 + sx1) / 2 + _stag - sx0) / max(sx1 - sx0, 1e-9))
            _ifx, _iy = _edge_fit(_ds, "t", _dfx)
            _px = sx0 + _ofx * (sx1 - sx0)
            _py = sy0 + _oy * (sy1 - sy0)
            _yv1 = _v_corridor_y(_px, _py, going_up=True, sd=sd, lv=lv) \
                - LANE_STAGGER * (lv - 1)      # v8.1.0：走廊随层下移，给先行边留位
            # v8.1.0 根修：末段必须正交——倒数第二点与入点的 x 共用（旧版前者
            # 多加了一次错层、后者不加，两者不等时末段成斜线：细胞周期模板 M→G1
            # 回边末端斜虚线，自 8.0.5 上线）
            _fx = dx0 + _ifx * (dx1 - dx0)      # 目标顶入点 x（轮廓拟合+错层，经 _dfx）
            _yv2 = _v_corridor_y(_fx, dy0 + _iy * (dy1 - dy0), going_up=True, sd=sd, lv=lv) \
                - LANE_STAGGER * (lv - 1)
            _yv2 = max(_yv2, min(_yv1, dy0 + _iy * (dy1 - dy0) + 0.3))
            # v8.1.0：入线走廊尽量贴近目标（目标顶 +0.45 封顶）——贴着上方障碍
            # 走会让入线横段紧邻那个障碍的出入口，交叉读作 T 形分岔
            _yv2 = max(min(_yv2, dy0 + _iy * (dy1 - dy0) + 0.45),
                       min(_yv1, dy0 + _iy * (dy1 - dy0) + 0.3))
            return [(_px, _py), (_px, _yv1), (lx, _yv1), (lx, _yv2),
                    (_fx, _yv2), (_fx, dy0 + _iy * (dy1 - dy0) - EDGE_NIB)]
        _ofx, _oy = _edge_fit(_ss, "b", ((sx0 + sx1) / 2 + _stag - sx0) / max(sx1 - sx0, 1e-9))
        _ifx, _iy = _edge_fit(_ds, "b", _dfx)
        _px = sx0 + _ofx * (sx1 - sx0)
        _py = sy0 + _oy * (sy1 - sy0)
        _yv1 = _v_corridor_y(_px, _py, going_up=False, sd=sd, lv=lv) \
            + LANE_STAGGER * (lv - 1)          # v8.1.0：下行走廊随层上移
        _fx = dx0 + _ifx * (dx1 - dx0)          # 同上：末段正交（v8.1.0）
        _yv2 = _v_corridor_y(_fx, dy0 + _iy * (dy1 - dy0), going_up=False, sd=sd, lv=lv) \
            + LANE_STAGGER * (lv - 1)
        _yv2 = min(_yv2, max(_yv1, dy0 + _iy * (dy1 - dy0) - 0.3))
        _yv2 = min(max(_yv2, dy0 + _iy * (dy1 - dy0) - 0.45),     # v8.1.0 同上（镜像）
                   max(_yv1, dy0 + _iy * (dy1 - dy0) - 0.3))
        return [(_px, _py), (_px, _yv1), (lx, _yv1), (lx, _yv2),
                (_fx, _yv2), (_fx, dy0 + _iy * (dy1 - dy0) + EDGE_NIB)]

    def _segs_hit(pts):
        for k in range(len(pts) - 1):
            if _blocked(pts[k], pts[k + 1]):
                return True
        # 顶点检查：拐点/端点不得落在非端点框内（弯在框里=judge 必抓）
        for (px, py) in pts:
            for b in blocks:
                if b["id"] in _skip:
                    continue
                x0, y0, x1, y1 = _bbox(b)
                if x0 - 0.01 < px < x1 + 0.01 and y0 - 0.01 < py < y1 + 0.01:
                    return True
        return False

    # v8.1.0：绕行候选**择优**而非取第一个合法的——按（近端口交叉数, 总长）
    # 取最小；且不得与已路由边共线重叠（细胞周期模板两条回边叠在同一条绕行线
    # 上、方向相反，其中一段只看得见一条线）。
    _lane_cands = []
    for _lv in range(max(lane_level, 1), max(lane_level, 1) + 9):
        for _try_side in (side, -side):
            _cand = _lane_pts(_try_side, _lv)
            if _segs_hit(_cand) or _bus_overlap(_cand, avoid_x):
                continue
            _len = sum(abs(_cand[k2 + 1][0] - _cand[k2][0])
                       + abs(_cand[k2 + 1][1] - _cand[k2][1])
                       for k2 in range(len(_cand) - 1))
            _lane_cands.append(((_route_cost(_cand)[2], round(_len, 4)), _cand, _try_side))
            if len(_lane_cands) >= 12:
                break
        if len(_lane_cands) >= 12:
            break
    if _lane_cands:
        _best = min(_lane_cands, key=lambda _e: _e[0])
        return _best[1], _best[2]
    return _lane_pts(side, max(lane_level, 1)), side


def assign_lanes(blocks, edges):
    """R4：cycle-breaking（ELK 语义）——回边/直连穿框的边分配 lane 错层。"""
    bmap = {b["id"]: b for b in blocks}
    fwd = {}
    for e in edges:
        fwd.setdefault(e["from"], []).append(e["to"])
    back_pairs = set()
    seen, stack = set(), []

    def _dfs(u):
        seen.add(u)
        stack.append(u)
        for v in fwd.get(u, []):
            if v not in seen:
                _dfs(v)
            elif v in stack:
                back_pairs.add((u, v))
        stack.pop()

    for r in [b["id"] for b in blocks]:
        if r not in seen:
            _dfs(r)
    out = {}
    lvl = 0
    for i, e in enumerate(edges):
        s_, t_ = bmap.get(e["from"]), bmap.get(e["to"])
        if s_ is None or t_ is None:
            continue
        p0, p1 = magnet(s_, t_)
        if (e["from"], e["to"]) in back_pairs or _seg_hits(p0, p1, blocks,
                                                           (e["from"], e["to"])):
            _, sgn = _edge_between(s_, t_)
            out[i] = (lvl + 1, sgn)
            lvl += 1
    return out


# ── R2 边标签（墨迹级避让） ────────────────────────────────────────────
def _orient_of(route_pts):
    if len(route_pts) >= 4:
        _bs, _be, _blen = route_pts[1], route_pts[2], -1.0
        for k in range(1, len(route_pts) - 1):
            (ax_, ay_), (bx_, by_) = route_pts[k], route_pts[k + 1]
            _L = abs(bx_ - ax_) + abs(by_ - ay_)
            if _L > _blen:
                _blen, _bs, _be = _L, (ax_, ay_), (bx_, by_)
        return "H" if abs(_be[0] - _bs[0]) >= abs(_be[1] - _bs[1]) else "V"
    return "H" if abs(route_pts[-1][0] - route_pts[0][0]) \
        >= abs(route_pts[-1][1] - route_pts[0][1]) else "V"


def place_edge_label(ax, fig, text, route_pts, blocks, placed_boxes, **kw):
    """边标签放置（对外入口）：记录本次调用的候选轨迹到 LABEL_LOG[text]。"""
    _tr = []
    LABEL_LOG.setdefault(text, []).append(_tr)
    return _place_edge_label(ax, fig, text, route_pts, blocks, placed_boxes,
                             _trace=_tr, **kw)


def _place_edge_label(ax, fig, text, route_pts, blocks, placed_boxes, fp=None,
                      fs=9.0, color="#444444", dashed_hint=False,
                      line_segs=(), force_side=0, lane_base=None,
                      strict_assoc=False, no_wrap=False, primary_only=False,
                      _trace=None, prefer=None):
    """R2：measure-then-resolve——候选生成于**每条线段的两侧**（单一绝对坐标
    系，无帧混用），逐候选画→墨迹实测→碰撞→移除重试；窄间隙自动折两行；
    全失败→框行上方+垂直引线。返回 (artist, bb)。"""
    # 锚点段集合：全部线段，长段优先
    segs = list(zip(route_pts[:-1], route_pts[1:]))
    seg_info = []
    for (a, b) in segs:
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        L = abs(b[0] - a[0]) + abs(b[1] - a[1])
        orient = "H" if abs(b[0] - a[0]) >= abs(b[1] - a[1]) else "V"
        seg_info.append({"mx": mx, "my": my, "orient": orient, "L": L})
    seg_info.sort(key=lambda m: -m["L"])

    _renderer = [None]

    def _ink_bb(t):
        # 文字范围只需渲染器排版，不必每个候选重绘整幅画布（多轮放置下重绘占
        # 了渲染时间的大半——13 张工件 66s→151s 实测）。渲染器取一次复用；
        # 回归对比要求：标签范围与逐候选重绘版逐位相同。
        if _renderer[0] is None:
            fig.canvas.draw()
            _renderer[0] = fig.canvas.get_renderer()
        bb = t.get_window_extent(renderer=_renderer[0])
        inv = ax.transData.inverted()
        (x0, y0) = inv.transform((bb.x0, bb.y0))
        (x1, y1) = inv.transform((bb.x1, bb.y1))
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))

    _sep_zs = _sep_zones(blocks)   # v8.0.9 标签禁跨泳道分隔带（judge E5 实锤）
    _sp_cache = {}                 # 节点真实轮廓缓存（本次放置内复用）
    _band_union = None
    if "_lanes_geo" in blocks[0]:
        _lg = blocks[0]["_lanes_geo"]
        # v8.1.0 R15：标签带域**排除 LR 标题竖条**（白字标签落在深色竖条上
        # 遮挡旋转标题实锤）——LR 带 x 从竖条右缘 0.42 起算
        _band_union = (
            min(g["x"] + (0.42 if g.get("dir") == "LR" else 0) for g in _lg) + 0.05,
            min(g["y"] for g in _lg) + 0.05,
            max(g["x"] + g["w"] for g in _lg) - 0.05,
            max(g["y"] + g["h"] for g in _lg) - 0.05)

    def _box_seg_dist(bb, a, b):
        """标签框到线段的最短距离（in；相交=0）。归属按框算而不是按中心算——
        宽标签竖放在线旁时中心天然离线半个标签宽，按中心算会被「离自己的边
        太远」误杀（泳道主图 re-check：0.56in 宽、离线 0.16in，中心 0.44in，
        113 个候选轨迹实测），最后落到压线兜底。"""
        _n = max(int(math.hypot(b[0] - a[0], b[1] - a[1]) / 0.02), 1)
        _best = 1e9
        for _i in range(_n + 1):
            _u = _i / _n
            _px_, _py_ = a[0] + (b[0] - a[0]) * _u, a[1] + (b[1] - a[1]) * _u
            _dx_ = max(bb[0] - _px_, _px_ - bb[2], 0.0)
            _dy_ = max(bb[1] - _py_, _py_ - bb[3], 0.0)
            _best = min(_best, math.hypot(_dx_, _dy_))
        return _best

    def _own_dist(bb):
        return min(_box_seg_dist(bb, a, b) for a, b in segs)

    def _foreign_dist(bb):
        return min((_box_seg_dist(bb, q0, q1) for q0, q1 in line_segs),
                   default=1e9)

    def _chip(cx, cy):
        """标签底垫色：泳道内=所在泳道带底色（融底，不出现白色贴片）；否则白色。"""
        return lane_fill_at(blocks, lane_base, cx, cy) or "white"

    def _hit(bb, _pad=0.05):
        """候选位被拒的原因（None=可用）。v8.1.0：返回原因字符串而非布尔值，
        供放置轨迹（LABEL_LOG）诊断「标签为什么落在这里」。"""
        # v8.1.0 R14：标签必须整体落在泳道带域内（带外标签=归属不明，
        # judge R14 rework/accept/48h SLA 出带实锤）
        if _band_union is not None and not (
                bb[0] >= _band_union[0] and bb[1] >= _band_union[1]
                and bb[2] <= _band_union[2] and bb[3] <= _band_union[3]):
            return "落在泳道带域之外"
        for (zl, zh, zk) in _sep_zs:
            if zk == "v" and bb[0] < zh and zl < bb[2]:   # 覆盖垂直带
                return "跨泳道分隔带"
            if zk == "h" and bb[1] < zh and zl < bb[3]:   # 覆盖水平带（LR）
                return "跨泳道分隔带"
        for b in blocks:
            if _label_hits_block(bb, b, 0.12, _sp_cache):
                return f"撞节点 {b.get('id')}"
        for pb in placed_boxes:
            if _overlap(bb, pb, 0.02):
                return "撞已放的标签"
        for (q0, q1) in line_segs:
            if _overlap(bb, (min(q0[0], q1[0]), min(q0[1], q1[1]),
                             max(q0[0], q1[0]), max(q0[1], q1[1])), _pad):
                return "压到别的边"
        if strict_assoc:
            _cx, _cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
            # 归属贴近：严格轮要求标签中心离自己的边 ≤0.40in（离得更远的位
            # 置读起来不像在标注这条边——"accept" 0.62in / "re-check" 0.66in 实测）
            if _own_dist(bb) > 0.40:
                return "离自己的边太远(>0.40in)"
            if line_segs:
                # 归属净空（v8.1.0）：别的边离标签不得近于「自己的边 + 0.12in」——
                # 横向文字贴在别的横线上下，读起来就是在标注那条线（决策模板
                # Afebrile 紧贴 Persistent fever 横线下方 0.18in、离自己的竖线
                # 0.16in，r30 看图实测）。沿自己的线滑动到净空够的位置即可。
                if _foreign_dist(bb) < _own_dist(bb) + 0.12:
                    return "离别的边几乎等距(归属不明)"
                # 归属规则（严格轮）：标签离**别的边**比离自己的边还近=读起来
                # 像在标注那条边（LR 期刊模板 "accept" 贴在 review→decide 主干旁实锤）
                if _foreign_dist(bb) + 0.10 < _own_dist(bb):
                    return "离别的边更近(归属不明)"
        return None

    _w, _h = measure_in(ax, text, fs, fp)
    _txt = text
    # 窄间隙预判：锚点贴近某框缘（间隙 < 行高×2.6）→ 两行折行（断点=_wrap_mid）
    if "\n" not in _txt and " " in _txt and not no_wrap:
        for b in blocks:
            x0, y0, x1, y1 = _bbox(b)
            for m in seg_info:
                if x0 - 0.3 <= m["mx"] <= x1 + 0.3 and \
                        min(abs(m["my"] - y0), abs(m["my"] - y1)) < _h * 2.6:
                    _txt = _wrap_mid(_txt)
                    break
            if "\n" in _txt:
                break
    _h2 = measure_in(ax, _txt, fs, fp, ls=1.15)[1]
    _w2 = max((measure_in(ax, ln, fs, fp)[0] for ln in _txt.split("\n")),
              default=_w)
    _fp_t = fp if fp and has_cjk_local(text) else None

    def _try(cx, cy, va, _pad=0.05):
        t = ax.text(cx, cy, _txt, ha="center", va=va, fontsize=fs, color=color,
                    style="italic", linespacing=1.15,
                    bbox=dict(boxstyle="round,pad=0.1", facecolor=_chip(cx, cy),
                              edgecolor="none", alpha=1.0),
                    fontproperties=_fp_t, zorder=6)
        bb = _ink_bb(t)
        _why = _hit(bb, _pad)
        if not _why:
            placed_boxes.append(bb)
            return t, bb
        if _trace is not None:
            _trace.append((round(cx, 3), round(cy, 3), va, _why))
        t.remove()
        return None, None

    # 候选生成（绝对坐标）：每段两侧，长段优先；swimlane 下段旁候选扩容
    # （禁用框行回退后候选不足→标签互撞 4 处，judge 实锤）——旁侧±两级偏移
    # +沿线滑动 3 档
    tried = 0
    _swim = "_lanes_geo" in blocks[0]
    # v8.1.0 压线候选：标签直接压在自己的线段上（底色遮住一小段线=线被标签
    # 打断，流程图传统画法，归属毫无悬念）。用于两种情形：①通道轨道上的带
    # 标签边（优先）②段旁候选全败时——夹在两条平行线之间的标签无论偏向
    # 哪边都有歧义（LR 期刊图 accept 实测）。已放得好的段旁标签不受影响。
    # v8.1.0：压线候选不只取中点——中点被交叉线贴住时沿线滑动（±0.30 步进，
    # 标签两端各留 0.10），且离别的线保持 ≥0.14in（段旁候选仍是 0.05）：线
    # 紧贴着压线标签穿过，读起来像标签长在线角上（LR 样例 48 h SLA 离穿过的
    # 竖线 0.06in、决策模板 Yes 贴在 No 横线交叉点上方 0.07in，r22 看图实测）
    _on_line = []
    for m in seg_info:
        if m["L"] < _w2 + 0.20:
            continue
        _room = (m["L"] - _w2) / 2 - 0.10
        _offs, _o = [0.0], 0.30
        while _o <= _room:
            _offs += [_o, -_o]
            _o += 0.30
        for _o in _offs:
            _on_line.append((m["mx"] + (_o if m["orient"] == "H" else 0.0),
                             m["my"] + (_o if m["orient"] == "V" else 0.0),
                             "center"))
    if prefer:
        for (cx, cy, va) in _on_line:
            t, bb = _try(cx, cy, va, 0.14)
            if t is not None:
                return t, bb
    for m in seg_info:
        if m["orient"] == "V":
            # V 跨行段（CONSORT 主列）：标签放行间带内、竖段旁侧——带由布局
            # 预留（ROW_GAP+标签带），物理无框，零引线（文献标准形态）
            cands = [(m["mx"] + _w2 / 2 + 0.16, m["my"], "center"),
                     (m["mx"] - _w2 / 2 - 0.16, m["my"], "center")]
            if _swim:
                cands += [(m["mx"] + _w2 / 2 + 0.34, m["my"], "center"),
                          (m["mx"] - _w2 / 2 - 0.34, m["my"], "center"),
                          (m["mx"] + _w2 / 2 + 0.16, m["my"] + 0.30, "center"),
                          (m["mx"] - _w2 / 2 - 0.16, m["my"] + 0.30, "center"),
                          (m["mx"] + _w2 / 2 + 0.16, m["my"] - 0.30, "center"),
                          (m["mx"] - _w2 / 2 - 0.16, m["my"] - 0.30, "center")]
        else:
            cands = [(m["mx"], m["my"] + _h2 / 2 + 0.07, "bottom"),
                     (m["mx"], m["my"] - _h2 / 2 - 0.07, "top")]
            if _swim:
                cands += [(m["mx"] + 0.45, m["my"] + _h2 / 2 + 0.07, "bottom"),
                          (m["mx"] - 0.45, m["my"] + _h2 / 2 + 0.07, "bottom"),
                          (m["mx"] + 0.45, m["my"] - _h2 / 2 - 0.07, "top"),
                          (m["mx"] - 0.45, m["my"] - _h2 / 2 - 0.07, "top")]
        if prefer == "below":
            # 通道轨道的带标签边：标签区在线下方——线下方候选优先
            cands.sort(key=lambda c: 0 if c[2] == "top" else 1)   # va=top=文字在线下
        # v8.1.0 沿线滑动：长段（>1.2in）中点两侧 ±0.75/1.20/1.80in 取位——段旁
        # 中点被节点占住时（泳道主图 "48 h SLA" 左侧即 eCRF）标签仍能贴线落位，
        # 而不是退到螺旋扫描的远离位置。排在中点候选之后：中点有位则行为不变。
        # v8.1.0 步长加密：原四档（0.75/1.20/1.80）会跨过净空够的位置（事故模板
        # re-triage 沿线滑动全败→兜底网格压到虚线上，r31 实测）
        for _off in (0.22, 0.42, 0.62, 0.90, 1.20, 1.60, 2.00):
            if _off + _h2 / 2 + 0.10 > m["L"] / 2:
                break
            for _s in (1, -1):
                if m["orient"] == "V":
                    cands += [(m["mx"] + _w2 / 2 + 0.16, m["my"] + _s * _off, "center"),
                              (m["mx"] - _w2 / 2 - 0.16, m["my"] + _s * _off, "center")]
                else:
                    cands += [(m["mx"] + _s * _off, m["my"] + _h2 / 2 + 0.07, "bottom"),
                              (m["mx"] + _s * _off, m["my"] - _h2 / 2 - 0.07, "top")]
        if force_side and not strict_assoc:
            # 往返回边（48h SLA vs re-check 同走廊互撞根因）：候选沿走廊
            # **纵向错开** 0.45×force——第二标签落走廊另一段位置。
            # v8.1.0：仅最后放宽轮启用——严格轮有碰撞检查+归属规则兜底，
            # 强制平移反而把标签推离自己的边（re-check 离自己 0.66in 实测）
            cands = [(cx, cy + force_side * 0.45, va) for (cx, cy, va) in cands]
        for (cx, cy, va) in cands:
            t, bb = _try(cx, cy, va)
            if t is not None:
                return t, bb
            tried += 1
            # v8.1.0 外推重试：仅因「压到别的边/跨分隔带」差一点被拒的候选，沿
            # 垂直于本段的方向外推 0.08/0.16/0.24in 再试（归属贴近上限 0.40in
            # 自然封顶）。泳道主图 re-check：竖段两侧被分界线与 eCRF 夹死，最佳
            # 位在自己短横线正下方，固定偏移差 0.005in 碰到邻线被拒（轨迹实测）
            if _trace and _trace[-1][3] in ("压到别的边", "跨泳道分隔带"):
                _px_, _py_ = (0.08, 0.0) if m["orient"] == "V" else (0.0, 0.08)
                _ax_, _ay_ = (0.0, 0.08) if m["orient"] == "V" else (0.08, 0.0)
                # 外推不得跨过自己的线、也不得贴到线上（离线 < 半宽+0.05）——
                # 压线是段旁候选全败后的兜底，不是外推的顺路结果（事故模板
                # "no"：右侧候选外推第三档正好退回线上被接受，线旁的左侧空位
                # 根本没轮到，r21 放置轨迹实测）
                _bn_ = (cx - m["mx"]) if m["orient"] == "V" else (cy - m["my"])
                _hw_ = (_w2 if m["orient"] == "V" else _h2) / 2 + 0.05
                for _k in (1, 2, 3):
                    for (_ux_, _uy_) in ((_px_, _py_), (-_px_, -_py_),
                                         (_ax_, _ay_), (-_ax_, -_ay_)):
                        _nx_ = ((cx + _k * _ux_) - m["mx"]) if m["orient"] == "V" \
                            else ((cy + _k * _uy_) - m["my"])
                        if abs(_nx_) < _hw_ or _nx_ * _bn_ < 0:
                            continue
                        t, bb = _try(cx + _k * _ux_, cy + _k * _uy_, va)
                        if t is not None:
                            return t, bb
    if strict_assoc and not prefer:      # 段旁候选全败：试压线
        for (cx, cy, va) in _on_line:
            t, bb = _try(cx, cy, va, 0.14)
            if t is not None:
                return t, bb
    if primary_only:      # 单行优先轮：段旁与压线候选全败即让路（交给折行轮）
        return None, None
    # 框行上/下（x=最长段中点 x）+ 垂直引线（fig2 PASS 形态）——
    # swimlane 下禁用（chip 会落在泳道标题带/画布顶+leader 穿带穿字，judge 实锤）：
    # 直接跳到折行重试（候选恒在内容区内）
    _bt = max(_bbox(b)[3] for b in blocks)
    _bb0 = min(_bbox(b)[1] for b in blocks)
    _mx_long = seg_info[0]["mx"]
    _swim = "_lanes_geo" in blocks[0]
    _row_cands = [] if _swim else [
        (_mx_long, _bt + _h2 / 2 + 0.14, "bottom"),
        (_mx_long, _bb0 - _h2 / 2 - 0.14, "top")]
    for (cx, cy, va) in _row_cands:
        t, bb = _try(cx, cy, va)
        if t is not None:
            ax.plot([_mx_long, _mx_long], [min(_midy(route_pts), cy),
                      max(_midy(route_pts), cy)],
                    color=color, lw=0.7, alpha=0.75, zorder=5)
            return t, bb
    # 折行重试于框行上方 —— swimlane 禁用（chip 飞画布顶+leader 穿带，
    # judge 实锤；t=None 时 t.remove() 亦为潜伏炸弹）
    if (not _swim) and "\n" not in _txt and " " in _txt:
        _txt2 = _wrap_mid(_txt)
        _h3 = measure_in(ax, _txt2, fs, fp, ls=1.15)[1]
        _w3 = max((measure_in(ax, ln, fs, fp)[0] for ln in _txt2.split("\n")),
                  default=_w)
        t, bb = _try(_mx_long, _bt + _h3 / 2 + 0.14, "bottom")
        if t is not None:
            ax.plot([_mx_long, _mx_long], [min(_midy(route_pts), cy), cy],
                    color=color, lw=0.7, alpha=0.75, zorder=5)
            return t, bb
    # 全失败兜底：远置分支（画布外）仅限非 swimlane；swimlane 强制塞在
    # 最长段中点旁 0.34（白垫压线优于飞出画布，judge 实锤）
    if _swim:
        import itertools as _it
        _mid = _midy(route_pts)
        for _r, _ang in _it.chain(
                ((r, a) for r in (0.34, 0.55, 0.80, 1.20, 1.60)
                 for a in (0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi,
                           -3*math.pi/4, -math.pi/2, -math.pi/4))):
            _cx = _mx_long + math.cos(_ang) * _r
            _cy = _mid + math.sin(_ang) * _r
            t, bb = _try(_cx, _cy, "center")
            if t is not None:
                return t, bb
        # 16 向全占满→带域网格扫描（0.3 步进，首个无撞位即取——R14 实锤：
        # 硬塞中点旁 0.34 撞节点）→ 仍无位才硬塞中点旁 0.34
        if _band_union is not None:
            _x0, _y0, _x1, _y1 = _band_union
            # v8.1.0 R15：网格候选按**距锚点距离排序**（就近落位——顺序扫描
            # 会把标签吸到带域远端，orphaned 2000px 实锤）
            _cand_grid = []
            _gx = _x0 + _w2 / 2 + 0.05
            while _gx <= _x1 - _w2 / 2 - 0.05:
                _gy = _y0 + _h2 / 2 + 0.05
                while _gy <= _y1 - _h2 / 2 - 0.05:
                    _cand_grid.append((_gx, _gy))
                    _gy += 0.3
                _gx += 0.3
            _cand_grid.sort(key=lambda c: (c[0] - _mx_long) ** 2
                            + (c[1] - _mid) ** 2)
            for (_cgx, _cgy) in _cand_grid:
                tt_, bb_ = _try(_cgx, _cgy, "center")
                if tt_ is not None:
                    return tt_, bb_
        if strict_assoc:
            return None, None          # 严格轮无解：交给调用方放宽后重试，不硬塞
        cx, cy = _mx_long + _w2 / 2 + 0.34, _mid
        t = ax.text(cx, cy, _txt, ha="center", va="center", fontsize=fs,
                    color=color, style="italic",
                    bbox=dict(boxstyle="round,pad=0.1", facecolor=_chip(cx, cy),
                              edgecolor="none"),
                    fontproperties=fp if fp and has_cjk_local(text) else None,
                    zorder=6)
        bb = _ink_bb(t)
        placed_boxes.append(bb)
        return t, bb
    cx, cy = _mx_long, _bb0 - _h2 / 2 - 0.2
    t, bb = _try(cx, cy, "top")
    if t is None and strict_assoc:
        return None, None          # 严格轮无解：交给调用方放宽后重试
    if t is None:
        t = ax.text(cx, cy, _txt, ha="center", va="top", fontsize=fs,
                    color=color, style="italic",
                    fontproperties=fp if fp and has_cjk_local(text) else None,
                    zorder=6)
        bb = _ink_bb(t)
    ax.plot([_mx_long, _mx_long], [_bb0, cy], color=color, lw=0.7,
            alpha=0.75, zorder=5)
    placed_boxes.append(bb)
    return t, bb


def _midy(route_pts):
    if len(route_pts) >= 4:
        (a, b) = route_pts[1], route_pts[2]
        return (a[1] + b[1]) / 2
    return (route_pts[0][1] + route_pts[-1][1]) / 2


# ── R6 三层 bbox 闸 ────────────────────────────────────────────────────
def gate_strict(ax, fig, blocks, label_bboxes, route_lines, ratios=None,
                route_meta=None):
    """R6：三层 bbox 断言（端点所属框豁免——EDGE_NIB 咬合是设计语义）。"""
    violations = []
    seg_bbs, seg_ends = [], []
    for (p0, p1) in route_lines:
        seg_bbs.append((min(p0[0], p1[0]), min(p0[1], p1[1]),
                        max(p0[0], p1[0]), max(p0[1], p1[1])))
        seg_ends.append((p0, p1))

    def _end_owner(seg_end_pts):
        ids = set()
        for (px, py) in seg_end_pts:
            for b in blocks:
                x0, y0, x1, y1 = _bbox(b)
                if x0 - 0.02 <= px <= x1 + 0.02 and y0 - 0.02 <= py <= y1 + 0.02:
                    ids.add(b["id"])
        return ids

    # v8.0.7 去重（dedup-at-gate）：同值 bb 的重复条目=单标签视觉实体，
    # 双记会产生假撞（swimlane 实锤 #1×#2/#3×#4）——判定前先去重
    _seen_lbs = []
    for _bb in label_bboxes:
        if _bb not in _seen_lbs:
            _seen_lbs.append(_bb)
    label_bboxes = _seen_lbs
    for i, lb in enumerate(label_bboxes):
        for j, b in enumerate(blocks):
            # v8.1.0：与放置阶段同一把尺——斜边多边形按真实轮廓（菱形顶点旁的空白
            # 位放标签不算相撞；矩形族仍按包围盒）
            if _label_hits_block(lb, b, -0.06):
                violations.append(f"层1 边标签#{i} 与节点「{b.get('id')}」相交")
    for i in range(len(label_bboxes)):
        for j in range(i + 1, len(label_bboxes)):
            if _overlap(label_bboxes[i], label_bboxes[j], 0.02):
                violations.append(f"层2 边标签#{i} 与 边标签#{j} 相交")
    for i, sb in enumerate(seg_bbs):
        _own = _end_owner(seg_ends[i])
        for j, b in enumerate(blocks):
            if b.get("id") in _own:
                continue
            if _overlap(sb, _bbox(b), -0.01):
                violations.append(f"层3 箭头段#{i} 与节点「{b.get('id')}」相交")
    if ratios is not None and ratios < 0.55:
        violations.append(f"层4 内容占比 {ratios:.0%} < 55%")
    return violations


def trim_limits(ax, blocks, extra_pts=(), pad=0.4, ratio_hint=True,
                pad_x=None, pad_y=None, pad_top=None, pad_bot=None,
                set_lim=True):
    """R5：内容包围盒（英寸）→figure 尺寸+xlim/ylim=英寸数（1 unit=1in，
    transform 恒定 → 一切测量绝对）。返回内容占比。"""
    xs, ys = [], []
    for b in blocks:
        x0, y0, x1, y1 = _bbox(b)
        xs += [x0, x1]
        ys += [y0, y1]
    for (x, y) in extra_pts:
        xs.append(x)
        ys.append(y)
    px = pad if pad_x is None else pad_x
    py = pad if pad_y is None else pad_y
    pt_ = pad if pad_top is None else pad_top
    pb_ = pad if pad_bot is None else pad_bot
    x0, x1 = min(xs) - px, max(xs) + px
    y0, y1 = min(ys) - pb_, max(ys) + pt_
    fig = ax.figure
    # 用户宽度契约：fig 宽=最大(用户请求宽, 内容宽)；范围=fig 宽（1 unit=1in
    # 保持），内容在画布内居中（v2 初版覆盖用户宽致右半空白+标签远角漂移）
    _user_w = fig.get_size_inches()[0]
    _range_w = max(_user_w, x1 - x0)
    _cx = (x0 + x1) / 2
    x0, x1 = _cx - _range_w / 2, _cx + _range_w / 2
    if set_lim:
        fig.set_size_inches(_range_w, max(y1 - y0, 1.5))
        ax.set_position([0, 0, 1, 1])
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
    if ratio_hint:
        fx = (max(xs) - min(xs)) / max(x1 - x0, 1e-9)
        fy = (max(ys) - min(ys)) / max(y1 - y0, 1e-9)
        return (fx + fy) / 2
    return 1.0


def _text_color(bg):
    from af_shared import cell_text_color
    return cell_text_color(bg)


# ── F1 形状注册表（v8.0.5）：语义形状绘制原语 + 文本内接系数 ─────────────
# 契约与 round/rect 完全一致：几何 bbox = 声明 b["x..w"]，全部绘制内接其中
# （磁吸/strict 闸/apex 断言零特判）；draw() 返回 artist 或 artist 列表。
# tb = (w_frac, h_frac)：fit_text 可用区系数（菱形内接矩形×0.55 等）；
# ty = 文字中心相对 bbox 中心的 y 偏移分数（cylinder 偏下避顶部椭圆）。
# 形状语义对齐 mermaid v11.3+ 官方命名（学术高频 12 形子集）。

def _sh_round(ax, b, fc, ec, lw):
    return [FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"],
                           boxstyle="round,pad=0,rounding_size=0.14",
                           facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)]


def _sh_rect(ax, b, fc, ec, lw):
    return [FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"],
                           boxstyle="square,pad=0", facecolor=fc, edgecolor=ec,
                           linewidth=lw, zorder=3)]


def _sh_poly(pts):
    def _draw(ax, b, fc, ec, lw):
        return [Polygon([(b["x"] + px * b["w"], b["y"] + py * b["h"])
                         for (px, py) in pts], closed=True,
                        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)]
    return _draw


def _sh_diamond(ax, b, fc, ec, lw):
    return _sh_poly([(0.5, 1.0), (1.0, 0.5), (0.5, 0.0), (0.0, 0.5)])(
        ax, b, fc, ec, lw)


def _sh_cylinder(ax, b, fc, ec, lw):
    """数据库圆柱：底椭圆+矩形身+顶椭圆（顶椭圆盖住身顶边=经典投影画法）。"""
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    ry = h * 0.10
    from matplotlib.patches import Ellipse
    bottom = Ellipse((x + w / 2, y + ry), w, 2 * ry, facecolor=fc,
                     edgecolor=ec, linewidth=lw, zorder=3)
    body = Rectangle((x, y + ry), w, h - 2 * ry, facecolor=fc,
                     edgecolor="none", zorder=3)
    top = Ellipse((x + w / 2, y + h - ry), w, 2 * ry, facecolor=fc,
                  edgecolor=ec, linewidth=lw, zorder=3)
    # 身体侧边两条竖线（矩形边被 none 藏了，重画左右边）
    side_l = Rectangle((x, y + ry), 0.004, h - 2 * ry, facecolor=ec,
                       edgecolor="none", zorder=3)
    side_r = Rectangle((x + w - 0.004, y + ry), 0.004, h - 2 * ry,
                       facecolor=ec, edgecolor="none", zorder=3)
    return [bottom, body, side_l, side_r, top]


def _sh_dblcircle(ax, b, fc, ec, lw):
    """起止双圆：外描边环+内填充圆。"""
    from matplotlib.patches import Ellipse
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    outer = Ellipse((x + w / 2, y + h / 2), w, h, facecolor=fc,
                    edgecolor=ec, linewidth=lw * 1.4, zorder=3)
    inner = Ellipse((x + w / 2, y + h / 2), w * 0.86, h * 0.86,
                    facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    return [outer, inner]


def _sh_stacked(ax, b, fc, ec, lw):
    """多文档/多进程堆叠：主框内缩，垫片向外——bbox 外沿=最外垫片（
    内接契约：绘制绝不越出声明 bbox，磁吸/闸零特判）。"""
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    dx = min(0.10, w * 0.12)
    dy = min(0.10, h * 0.12)
    back = FancyBboxPatch((x, y), w, h,
                          boxstyle="square,pad=0", facecolor=fc,
                          edgecolor=ec, linewidth=lw * 0.8, zorder=2)
    mid = FancyBboxPatch((x + dx / 2, y + dy / 2), w - dx, h - dy,
                         boxstyle="square,pad=0", facecolor=fc,
                         edgecolor=ec, linewidth=lw * 0.8, zorder=2)
    main = FancyBboxPatch((x + dx, y + dy), w - 2 * dx, h - 2 * dy,
                          boxstyle="square,pad=0",
                          facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    return [back, mid, main]


def _sh_predefined(ax, b, fc, ec, lw):
    """预定义子流程：矩形+左右双竖线。"""
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    main = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                          facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    off = min(0.10 * w, 0.18)
    l1 = Rectangle((x + off, y), 0.008, h, facecolor=ec,
                   edgecolor="none", zorder=3)
    l2 = Rectangle((x + w - off, y), 0.008, h, facecolor=ec,
                   edgecolor="none", zorder=3)
    return [main, l1, l2]


def _sh_document(ax, b, fc, ec, lw):
    """文档形状：矩形+底边波浪（贝塞尔）。"""
    from matplotlib.path import Path as _MPath
    from matplotlib.patches import PathPatch
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    wav = h * 0.14
    verts = [(x, y + wav), (x, y + h), (x + w, y + h), (x + w, y + wav),
             (x + w * 0.75, y + wav - wav * 0.9),
             (x + w * 0.5, y + wav + wav * 0.9),
             (x + w * 0.25, y + wav - wav * 0.9), (x, y + wav)]
    codes = [_MPath.MOVETO, _MPath.LINETO, _MPath.LINETO, _MPath.LINETO,
             _MPath.CURVE4, _MPath.CURVE4, _MPath.CURVE4, _MPath.LINETO]
    patch = PathPatch(_MPath(verts, codes), facecolor=fc, edgecolor=ec,
                      linewidth=lw, zorder=3)
    return [patch]


def _sh_delay(ax, b, fc, ec, lw):
    """延迟：左侧直角+右侧半圆（rounding=h/2 仅右缘达成半圆观感）。"""
    from matplotlib.patches import FancyBboxPatch as _FBP
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    patch = _FBP((x, y), w, h,
                 boxstyle=f"round,pad=0,rounding_size={h / 2:.4f}",
                 facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    # 左缘重画直边（round 把四角全圆了，用窄条补左直边；内接 x+0.001）
    bar = Rectangle((x + 0.001, y + 0.001), 0.004, h - 0.002,
                    facecolor=ec, edgecolor="none", zorder=3)
    return [patch, bar]


def _sh_stored_data(ax, b, fc, ec, lw):
    """存储数据（横向圆柱/哑铃）：**单轮廓**——左右半圆弧+上下直腰，
    多边形弧采样（judge 实锤：双椭圆描边在填充内交叉=韦恩透镜观感）。"""
    import numpy as _np
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    rx = h * 0.5
    cy = y + h / 2
    n = 13
    # 弧序：上直腰（左→右）→右弧（顶→底）→下直腰→左弧（底→顶）闭合
    angs = _np.linspace(math.pi / 2, -math.pi / 2, n)   # 顶→底
    right = [(x + w - rx + rx * math.cos(a), cy + rx * math.sin(a))
             for a in angs]
    left = [(x + rx + rx * math.cos(a), cy - rx * math.sin(a))
            for a in angs]                               # 底→顶（y 镜像）
    pts = ([(x + rx, y + h)] + right + [(x + rx, y)] + left)
    return [Polygon(pts, closed=True, facecolor=fc, edgecolor=ec,
                    linewidth=lw, zorder=3)]


SHAPES = {
    "round":        {"draw": _sh_round,   "tb": (0.94, 0.90), "ty": 0.0,
                     "aliases": ("stadium", "stadium-shape", "event", "rounded", "pill")},
    "rect":         {"draw": _sh_rect,    "tb": (0.94, 0.90), "ty": 0.0,
                     "aliases": ("process", "rectangle", "box")},
    "diamond":      {"draw": _sh_diamond, "tb": (0.54, 0.50), "ty": 0.0,
                     "aliases": ("decision", "question", "decision-node")},
    "cylinder":     {"draw": _sh_cylinder, "tb": (0.86, 0.62), "ty": -0.06,
                     "aliases": ("database", "db", "datastore", "storage")},
    "io":           {"draw": _sh_poly([(0.14, 1.0), (1.0, 1.0), (0.86, 0.0), (0.0, 0.0)]),
                     "tb": (0.72, 0.80), "ty": 0.0,
                     "aliases": ("parallelogram", "data", "in-out")},
    "hexagon":      {"draw": _sh_poly([(0.22, 1.0), (0.78, 1.0), (1.0, 0.5), (0.78, 0.0), (0.22, 0.0), (0.0, 0.5)]),
                     "tb": (0.68, 0.72), "ty": 0.0,
                     "aliases": ("prepare", "prep")},
    "terminal":     {"draw": _sh_dblcircle, "tb": (0.52, 0.58), "ty": 0.0,
                     "aliases": ("start-end", "double-circle", "start", "stop")},
    "stacked":      {"draw": _sh_stacked, "tb": (0.72, 0.76), "ty": 0.0,
                     "aliases": ("multi-process", "stack", "multi-document")},
    "manual-input": {"draw": _sh_poly([(0.0, 0.0), (0.0, 0.74), (1.0, 1.0), (1.0, 0.0)]),
                     "tb": (0.84, 0.66), "ty": -0.04,
                     "aliases": ("input", "sloped")},
    "manual-op":    {"draw": _sh_poly([(0.14, 1.0), (0.86, 1.0), (1.0, 0.0), (0.0, 0.0)]),
                     "tb": (0.72, 0.80), "ty": 0.0,
                     "aliases": ("manual", "operation", "trapezoid")},
    "delay":        {"draw": _sh_delay, "tb": (0.78, 0.86), "ty": 0.0,
                     "aliases": ("half-rounded",)},
    "document":     {"draw": _sh_document, "tb": (0.88, 0.76), "ty": 0.04,
                     "aliases": ("doc",)},
    "predefined":   {"draw": _sh_predefined, "tb": (0.74, 0.88), "ty": 0.0,
                     "aliases": ("subprocess", "subroutine", "framed")},
    "stored-data":  {"draw": _sh_stored_data, "tb": (0.62, 0.66), "ty": 0.0,
                     "aliases": ("stored", "bow-tie", "disk")},
}


# ── F1 边贴合（v8.0.5）：非平顶/平底形状的入出点高度修正 ──────────────
# judge 实锤：斜顶形状（manual-input）入边落 bbox 顶=悬空 80px。机制=
# 每形状声明 top/bottom 的「覆盖域+高度函数」：magnet/route 入出点按
# 落点 x 分数取**实际轮廓高度**，覆盖域外钳制到域内（箭头永远贴形）。
# 平顶形状缺省 None=1.0/0.0 全覆盖。H 键斜边（io 左右）留 v8.0.6。

# 左右轮廓（H 键边贴合）：at_l(y 分数)→形状左边界 x 分数；缺省 0/1 全高直边
_SHAPE_EDGE_X = {
    # v8.0.9 根修（judge R6 实锤：旧 span_l/r=(0.5,0.5)+公式把「左侧进入」
    # 算到右顶点→箭头横穿整个菱形到远端+浮动出点 0.335in）。真实轮廓：
    # 左侧 fx=|fy-0.5|（fy=0.5→左顶点 0.0），右侧 fx=1-|fy-0.5|。
    "diamond":      {"span_l": (0.0, 1.0), "at_l": lambda fy: abs(fy - 0.5),
                     "span_r": (0.0, 1.0), "at_r": lambda fy: 1.0 - abs(fy - 0.5)},
    "io":           {"span_l": (0.0, 1.0), "at_l": lambda fy: 0.14 * (1 - fy),
                     "span_r": (0.0, 1.0), "at_r": lambda fy: 1.0 - 0.14 * fy},
    # hexagon 左右顶点在 fy=0.5（x=0/1），上下角 x=0.22/0.78——at_l 随 |fy-0.5| 增
    "hexagon":      {"span_l": (0.0, 1.0), "at_l": lambda fy: 0.44 * abs(fy - 0.5),
                     "span_r": (0.0, 1.0), "at_r": lambda fy: 1.0 - 0.44 * abs(fy - 0.5)},
    "manual-op":    {"span_l": (0.0, 1.0), "at_l": lambda fy: 0.14 * fy,
                     "span_r": (0.0, 1.0), "at_r": lambda fy: 1.0 - 0.14 * fy},
    "manual-input": {"span_l": (0.0, 0.74), "at_l": lambda fy: 0.0,
                     "span_r": (0.0, 1.0), "at_r": lambda fy: 1.0},
    "stored-data":  {"span_l": (0.0, 1.0), "at_l": lambda fy: 0.0,
                     "span_r": (0.0, 1.0), "at_r": lambda fy: 1.0},
}


def _edge_fit_x(shape, side, fy):
    """返回 (clamp 后 fy, 边界 x 分数)。side="l"|"r"。平直边→(fy, 0|1)。"""
    spec = _SHAPE_EDGE_X.get(shape) or {}
    key_s, key_a = (("span_l", "at_l") if side == "l" else ("span_r", "at_r"))
    if key_s not in spec:
        return fy, (0.0 if side == "l" else 1.0)
    lo, hi = spec[key_s]
    fy_c = min(max(fy, lo), hi)
    return fy_c, spec[key_a](fy_c)


def _doc_wave_y(fx):
    """document 底边波浪贝塞尔数值反解（v8.0.9 R11）：fx（x 分数）→轮廓
    y 分数。底边曲线 P0(x+w,y+0.14h)→C1(0.75w,-0.9wav)→C2(0.5w,+0.9wav)
    →P3(x,y+0.14h)——旧 at_b=0（bbox 底）在波峰段浮空 0.10-0.12in
    （judge R11 dossier→archive 出点实锤）。"""
    wav = 0.14
    best_t, best_e = 0.0, 1e9
    for i in range(41):
        t_ = i / 40
        xf = ((1 - t_) ** 3 + 3 * t_ * (1 - t_) ** 2 * 0.75
              + 3 * t_ ** 2 * (1 - t_) * 0.5)
        e = abs((1 - xf) - fx)
        if e < best_e:
            best_e, best_t = e, t_
    yv = ((1 - best_t) ** 3 + 3 * best_t * (1 - best_t) ** 2 * 0.1
          + 3 * best_t ** 2 * (1 - best_t) * 1.9 + best_t ** 3)
    return wav * yv


_SHAPE_EDGE = {
    # diamond：顶/底点在中心，但多出边（是/否分支）需错层→span 放宽到
    # 斜边全域（at_t/at_b 即斜边高度，出点永远贴轮廓）。
    # v8.0.9 根修：旧公式 1-2|fx-0.5| 是「压缩菱形」——中心处 at_b(0.5)=1.0
    # 让「底边出点」落在**顶点**、轴线整段穿本体（judge R6 机械探针 pen
    # 1.29in 实锤，R4 假 PASS）。真实轮廓：at_t=1-|fx-0.5|、at_b=|fx-0.5|。
    "diamond":      {"span_t": (0.08, 0.92), "at_t": lambda fx: 1.0 - abs(fx - 0.5),
                     "span_b": (0.08, 0.92), "at_b": lambda fx: abs(fx - 0.5)},
    "document":     {"span_b": (0.0, 1.0), "at_b": _doc_wave_y},
    "manual-input": {"span_t": (0.0, 1.0), "at_t": lambda fx: 0.74 + 0.26 * fx},
    "io":           {"span_t": (0.14, 1.0), "at_t": lambda fx: 1.0,
                     "span_b": (0.0, 0.86), "at_b": lambda fx: 0.0},
    "hexagon":      {"span_t": (0.22, 0.78), "at_t": lambda fx: 1.0,
                     "span_b": (0.22, 0.78), "at_b": lambda fx: 0.0},
    "manual-op":    {"span_t": (0.14, 0.86), "at_t": lambda fx: 1.0,
                     "span_b": (0.0, 1.0), "at_b": lambda fx: 0.0},
}


def _edge_fit(shape, side, fx):
    """返回 (clamp 后 fx, 边高 y 分数)。side="t"|"b"。平形状→(fx, 1|0)；
    单侧声明（如 manual-input 仅斜顶）另一侧取缺省平边。"""
    spec = _SHAPE_EDGE.get(shape) or {}
    key_s, key_a = (("span_t", "at_t") if side == "t" else ("span_b", "at_b"))
    if key_s not in spec:
        return fx, (1.0 if side == "t" else 0.0)
    lo, hi = spec[key_s]
    fx_c = min(max(fx, lo), hi)
    return fx_c, spec[key_a](fx_c)


def resolve_shape(name):
    if not name or name == "round":
        return "round"
    n = str(name).strip().lower()
    if n in SHAPES:
        return n
    for canon, spec in SHAPES.items():
        if n in spec["aliases"]:
            return canon
    raise ValueError(
        f"flow: 未知形状 '{name}'——可用: {', '.join(sorted(SHAPES))} "
        f"(别名含 {', '.join(a for s in SHAPES.values() for a in s['aliases'][:2])} 等)")


def _blend_hex(c1, c2, t):
    """线性混色：t=0 取 c1，t=1 取 c2（hex in/out）。"""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    m = [round(a[i] + (b[i] - a[i]) * t) for i in range(3)]
    return "#" + "".join(f"{v:02x}" for v in m)


def _tint(c, t):
    return _blend_hex(c, "#ffffff", t)


def _shade(c, t):
    return _blend_hex(c, "#000000", t)


def lane_palette(base, idx):
    """泳道配色（v8.1.0 期刊化，泳道用色的唯一来源）→ (带底, 分隔线, 标题带, 标题文字)。

    8.0.6–8.0.9 的带底写成 _shade(主色, 0.92)——向**黑**混合 92%，三条泳道成了近黑
    大色块（像素 4,8,9），本意是 _tint（向白）。黑底是仪表盘观感：灰箭头对比度低、
    印刷成实心黑，不属于期刊图。现为浅色斑马纹带底 + 细分隔线 + 深色标题文字。"""
    even = (idx % 2 == 0)
    return (_tint(base, 0.94 if even else 0.88),
            _tint(base, 0.55),
            _tint(base, 0.84 if even else 0.78),
            _shade(base, 0.55))


def lane_fill_at(blocks, base, x, y):
    """点 (x, y) 所在泳道的带底色（十六进制）；非泳道或点在带外 → None。"""
    if not blocks or base is None or "_lanes_geo" not in blocks[0]:
        return None
    for i, g in enumerate(blocks[0]["_lanes_geo"]):
        if g["x"] <= x <= g["x"] + g["w"] and g["y"] <= y <= g["y"] + g["h"]:
            return lane_palette(base, i)[0]
    return None


def _shape_paths(b, _cache=None):
    """节点真实轮廓的几何路径列表（数据坐标，直接取自绘制该形状的 artist）。
    _cache={id(块): 路径} 可复用（同一次放置里反复判碰撞）。失败返回 None。"""
    if _cache is not None and id(b) in _cache:
        return _cache[id(b)]
    try:
        _arts = SHAPES[resolve_shape(b.get("shape", "round"))]["draw"](
            None, b, "#000000", "#000000", 1.0)
        _ps = [_a.get_path().transformed(_a.get_transform()) for _a in _arts]
    except Exception:
        _ps = None
    if _cache is not None:
        _cache[id(b)] = _ps
    return _ps


def _label_hits_block(bb, b, pad=0.12, _cache=None):
    """标签框与节点是否相撞——按节点**真实形状**（不是包围盒）。

    v8.1.0：此前按包围盒判，胶囊形/圆角矩形/圆柱在角上多出的空白位全被判死，
    短边上的标签被迫退到离自己的边 0.6in 以外（LR 期刊模板 "accept"、泳道
    主图 "re-check" 实测）。斜边多边形此前已按轮廓判，现统一为真实路径。"""
    if not _overlap(bb, _bbox(b), pad):
        return False
    x0, y0, x1, y1 = bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad
    paths = _shape_paths(b, _cache)
    if paths is None:
        return True                      # 取不到轮廓：保守按包围盒算相撞

    def inside(px, py):
        return any(_p.contains_point((px, py)) for _p in paths)

    nx = max(2, int((x1 - x0) / 0.04))
    ny = max(2, int((y1 - y0) / 0.04))
    for i in range(nx + 1):               # 标签框上下边采样落入节点
        px = x0 + (x1 - x0) * i / nx
        if inside(px, y0) or inside(px, y1):
            return True
    for j in range(ny + 1):               # 左右边采样落入节点
        py = y0 + (y1 - y0) * j / ny
        if inside(x0, py) or inside(x1, py):
            return True
    bx0, by0, bx1, by1 = _bbox(b)         # 标签把小节点整个盖住
    return x0 < (bx0 + bx1) / 2 < x1 and y0 < (by0 + by1) / 2 < y1


def _role_colors(blocks, arrows, colors):
    """顶刊角色化配色（v8.0.4）：替代多饱和色轮转的杂色感——

    - 主链基色 = colors[0]，沿流程深度自动衍生**同族明度阶梯**
      （起点最深 → 下游渐浅），并行支路同深度同色（语义对齐）；
    - 终点节点（最深行的汇点）= colors[-1] **唯一强调色**（60-30-10 收束）；
    - 侧支出汇点（如 CONSORT Excluded，深度<最深行）随所在层阶梯色，
      不抢强调色的视觉焦点；
    - 饱和度纪律由默认系列保证（基色 S≈37%），显式 color > --palette > 本函数。

    返回 {block_index: hex}（仅无显式 color 的节点）。"""
    ids = [b.get("id") for b in blocks]
    idx = {nid: i for i, nid in enumerate(ids) if nid is not None}
    n = len(blocks)
    # v8.0.4 断环：回边（DFS 栈内重访，如 EXTINCT→Register 回退）不计入
    # 出度/深度——否则终点节点永不触发强调色、BFS 深度被环污染（论文 fig2 实测）
    fwd_of = {}
    for e in arrows:
        fwd_of.setdefault(e.get("from"), []).append(e.get("to"))
    back = set()
    _seen, _stack = set(), []

    def _dfs(u):
        _seen.add(u)
        _stack.append(u)
        for v in fwd_of.get(u, []):
            if v not in _seen:
                _dfs(v)
            elif v in _stack:
                back.add((u, v))
        _stack.pop()

    for nid in ids:
        if nid not in _seen:
            _dfs(nid)
    outdeg = [0] * n
    indeg = [0] * n
    depth = [0] * n
    adj = [[] for _ in range(n)]
    for e in arrows:
        s, d = idx.get(e.get("from")), idx.get(e.get("to"))
        if s is None or d is None or (e.get("from"), e.get("to")) in back:
            continue
        outdeg[s] += 1
        indeg[d] += 1
        adj[s].append(d)
    # BFS 深度（取最深路径；环时 depth 只增不回退，安全）
    from collections import deque
    q = deque(i for i in range(n) if indeg[i] == 0)
    seen = set(q)
    while q:
        u = q.popleft()
        for v in adj[u]:
            depth[v] = max(depth[v], depth[u] + 1)
            if v not in seen:
                seen.add(v)
                q.append(v)
    maxd = max(depth) if depth else 0
    base = colors[0]
    accent = colors[-1] if len(colors) >= 2 else _tint(base, 0.35)
    lo = _shade(base, 0.12)      # 阶梯深端（起点）
    hi = _tint(base, 0.46)       # 阶梯浅端（下游）
    out = {}
    for i in range(n):
        if maxd == 0:
            out[i] = base
        elif outdeg[i] == 0 and depth[i] == maxd:
            out[i] = accent                                   # 终点：唯一强调
        else:
            t = depth[i] / maxd if maxd else 0.0
            out[i] = _blend_hex(lo, hi, t)                    # 同族明度阶梯
    return out


# ── 渲染管线（diagram/flow 共用单一事实源） ──────────────────────────────
def render(ax, fig, blocks, arrows, groups=(), annotations=(), theme=None,
           cjk_fp=None, gate="basic", orthogonal=False, legend_flag=None,
           hops=False):
    """完整渲染。返回 (violations, ratio)。gate="strict" 违规由调用方 exit 2。"""
    from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

    bmap = {b["id"]: b for b in blocks}
    fs = (theme or {}).get("font_size", 11)
    text_color = "#1a1a1a"
    arrow_color = "#555555"

    # ── 1) 组背景 ──
    for grp in groups:
        gb = [bmap[i] for i in grp.get("blocks", []) if i in bmap]
        if not gb:
            continue
        pad = 0.18
        gx = min(_bbox(b)[0] for b in gb) - pad
        gy = min(_bbox(b)[1] for b in gb) - pad
        gw = max(_bbox(b)[2] for b in gb) - gx + pad
        gh = max(_bbox(b)[3] for b in gb) - gy + pad
        gc = grp.get("color", "#888888")
        ax.add_patch(Rectangle((gx, gy), gw, gh, linewidth=1.5, edgecolor=gc,
                               facecolor="none",
                               linestyle=grp.get("style", "dashed"),
                               alpha=0.8, zorder=1))
        if grp.get("label"):
            # v8.0.7 标题移框顶外上方（旧=框内顶部与节点顶压字 0.15in，judge 实锤）
            ax.text(gx + 0.08, gy + gh + 0.06, grp["label"], fontsize=fs - 1,
                    color=gc, fontweight="bold", va="bottom", ha="left", zorder=2,
                    fontproperties=cjk_fp if cjk_fp and has_cjk_local(grp["label"])
                    else None)

    # ── 1.5) 确定性画布：xlim/ylim=英寸内容域（1 unit=1in，测量绝对） ──
    lanes = assign_lanes(blocks, arrows)
    n_above = sum(1 for (_lv, sd) in lanes.values() if sd > 0)
    n_below = sum(1 for (_lv, sd) in lanes.values() if sd < 0)
    # v8.1.0 边样式图例：数据 legend:true/false 显式；缺省=混合样式自动
    _legend_on = legend_flag if legend_flag is not None else (
        any(e.get("dashed") for e in arrows)
        or any(e.get("thick") for e in arrows)
        or any(e.get("bidirectional") for e in arrows))
    trim_limits(ax, blocks, pad_x=CANVAS_PAD_X, pad_y=CANVAS_PAD_Y,
                pad_top=CANVAS_PAD_Y + LANE_LABEL_ALLOW +
                (LANE_GAP + LANE_STAGGER * n_above if n_above else 0),
                pad_bot=CANVAS_PAD_Y + LANE_LABEL_ALLOW +
                (LANE_GAP + LANE_STAGGER * n_below if n_below else 0)
                + (0.42 if _legend_on else 0),
                ratio_hint=False)
    ax.axis("off")

    # ── 2) 边路由 ──
    # attach 错层按「同侧接入」分组计数（物理侧= (node,key,±1)）；**尾槽并入
    # 同侧头槽**——出边尾端若与先行入边箭头头位重合即视觉 T 分岔（蛇形回边
    # 尾=E→F 头位实测），错层必须跨入/出统一排序。
    route_pools = []     # v8.1.0 QC：各边候选池（代价, 路径）
    route_rejects = []   # v8.1.0 QC：各边肘部被拒候选（与 route_pools 对齐）
    LABEL_LOG.clear()  # v8.1.0 QC：本次渲染的标签放置轨迹
    route_pts, route_lines, route_meta = [], [], []
    attach_out, attach_in = {}, {}
    # 往返边对检测（swimlane 多列回边常见：A→B 与 B→A 并存）——第二条边
    # 标签强制反侧，杜绝同走廊芯片互撞（judge 实锤 48h SLA vs re-check）
    _seen_pairs = set()
    _rt_force = {}
    _rt_offset = {}
    _bus_x = {}   # v8.0.9 往返对总线登记（avoid_x 兼容旧结构，保留）
    _all_buses = []   # v8.0.9 R10 全局垂直总线 (x,ylo,yhi)——共线树干根除
    _all_heads = []   # v8.0.9 R10 已路由边头尖——头域压印根除
    _all_ports = []   # v8.1.0 已路由边的出入点 (x, y, 节点, "tail"|"head")——同角冲突
    _pending_lines = []   # v8.1.0 各边两端中心连线——未路由边的交叉估计
    for e in arrows:
        _p = frozenset((e["from"], e["to"]))
        if _p in _seen_pairs:
            _rt_force[id(e)] = -1
            _rt_offset[id(e)] = 1   # 第二条边错层 +1 槽（与首边分离 ≥EDGE_STAGGER）
        else:
            _seen_pairs.add(_p)
    for i, e in enumerate(arrows):
        s, t = bmap.get(e["from"]), bmap.get(e["to"])
        if s is None or t is None:
            continue
        lv, side = lanes.get(i, (0, 1))
        key, sgn = _edge_between(s, t)
        # v8.0.9 R10 槽位改**物理侧**计数（旧 (node,key,sgn) 跨键不共享：
        # crf→query 头走 H 键槽、query→sitefix 出点走 V 键槽→同在左顶点
        # 重合，出口段必穿头域→全候选灭→lane 兜底，DBG 实锤）。同侧出入
        # 槽统一错层=「尾槽并入同侧头槽」的完整语义。
        _sb_, _db_ = _bbox(s), _bbox(t)
        _up = (_db_[1] + _db_[3]) >= (_sb_[1] + _sb_[3])
        _rt = (_db_[0] + _db_[2]) >= (_sb_[0] + _sb_[2])
        _so = ("t" if _up else "b") if key == "V" else ("r" if _rt else "l")
        _si = ("b" if _up else "t") if key == "V" else ("l" if _rt else "r")
        _outk, _ink = (e["from"], _so), (e["to"], _si)
        _off = _rt_offset.get(id(e), 0)
        ao = attach_out.get(_outk, 0) + attach_in.get(_outk, 0) + _off
        ai = attach_in.get(_ink, 0) + attach_out.get(_ink, 0) + _off
        _pk = frozenset((e["from"], e["to"]))
        if not _pending_lines:
            def _ctr(bid):
                if bid not in bmap:          # 无效端点：占位，切片时滤掉（索引不错位）
                    return None
                _x0, _y0, _x1, _y1 = _bbox(bmap[bid])
                return ((_x0 + _x1) / 2, (_y0 + _y1) / 2)
            _pending_lines = [(_ctr(e2["from"]), _ctr(e2["to"])) for e2 in arrows]
        pts, side = route(s, t, blocks, lane_level=lv, side=side,
                          orthogonal=orthogonal, attach_in=ai, attach_out=ao,
                          avoid_x=tuple(_all_buses),
                          avoid_heads=tuple(_all_heads),
                          avoid_ports=tuple(_all_ports),
                          pending=tuple(_l for _l in _pending_lines[i + 1:]
                                        if _l[0] and _l[1]))
        _pool_ = af_flow_last_pool()
        if _pool_ and any([tuple(_p) for _p in _c[1]] == [tuple(_p) for _p in pts]
                          for _c in _pool_):   # 选中方案来自候选池（非 lane 兜底）
            route_pools.append((e["from"], e["to"], _pool_))
        else:
            route_pools.append((e["from"], e["to"], []))
        route_rejects.append(af_flow_last_reject())
        _all_ports.append((pts[0][0], pts[0][1], e["from"], "tail"))
        _all_ports.append((pts[-1][0], pts[-1][1], e["to"], "head"))
        for _k2 in range(len(pts) - 1):
            (ax_, ay_), (bx_, by_) = pts[_k2], pts[_k2 + 1]
            if abs(ax_ - bx_) < 1e-9:
                _all_buses.append(("v", ax_, min(ay_, by_), max(ay_, by_)))
            elif abs(ay_ - by_) < 1e-9:
                _all_buses.append(("h", ay_, min(ax_, bx_), max(ax_, bx_)))
        _tx, _ty = pts[-2]
        _hl = math.hypot(pts[-1][0] - _tx, pts[-1][1] - _ty) or 1.0
        _all_heads.append((pts[-1][0], pts[-1][1],
                           (pts[-1][0] - _tx) / _hl,
                           (pts[-1][1] - _ty) / _hl))
        attach_out[_outk] = attach_out.get(_outk, 0) + 1
        attach_in[_ink] = attach_in.get(_ink, 0) + 1
        route_pts.append(pts)
        route_meta.append((e, pts))
        for k in range(len(pts) - 1):
            route_lines.append((pts[k], pts[k + 1]))

    # ── 3) 画块（文本自适应）──
    # ── 2.6) 泳道背景（F3 v8.0.6）：layout=swimlane 时块携带 _lanes_geo
    _tc = (theme or {}).get("colors", ["#56B4E9"])
    label_meta = []            # 与 label_bboxes 对齐：(from, to)——标签归属审计用
    if blocks and "_lanes_geo" in blocks[0]:
        _fs_lane = fs
        for _gi, _g in enumerate(blocks[0]["_lanes_geo"]):
            _body, _edge, _head, _htext = lane_palette(_tc[0], _gi)
            ax.add_patch(Rectangle((_g["x"], _g["y"]), _g["w"], _g["h"],
                                   facecolor=_body, edgecolor=_edge,
                                   linewidth=0.9, zorder=1))
            if _g.get("dir") == "LR":
                # v8.1.0 泳道 LR：左侧标题竖条+旋转 90° 标题（经典泳道形态）
                ax.add_patch(Rectangle((_g["x"], _g["y"]), 0.42, _g["h"],
                                       facecolor=_head, edgecolor=_edge,
                                       linewidth=0.9, zorder=1))
                # v8.1.0 R14：竖排标题长度=旋转后的纵向占距——超带高即缩
                # 字号（"Data coordinating centre" 长于行带被裁实锤）
                _tl_len = measure_in(ax, _g["label"], _fs_lane - 1,
                                     cjk_fp if cjk_fp and has_cjk_local(_g["label"])
                                     else None)[0]
                _tfs = _fs_lane - 1
                while _tl_len > _g["h"] - 0.12 and _tfs > 5:
                    _tfs -= 0.5
                    _tl_len = measure_in(ax, _g["label"], _tfs,
                                         cjk_fp if cjk_fp and has_cjk_local(
                                             _g["label"]) else None)[0]
                ax.text(_g["x"] + 0.21, _g["y"] + _g["h"] / 2,
                        _g["label"], ha="center", va="center", rotation=90,
                        fontsize=_tfs, fontweight="bold", color=_htext, zorder=2)
            else:
                ax.add_patch(Rectangle((_g["x"], _g["y"] + _g["h"] - 0.5),
                                       _g["w"], 0.5, facecolor=_head,
                                       edgecolor=_edge, linewidth=0.9, zorder=1))
                ax.text(_g["x"] + _g["w"] / 2, _g["y"] + _g["h"] - 0.25,
                        _g["label"], ha="center", va="center",
                        fontsize=_fs_lane - 1, fontweight="bold",
                        color=_htext, zorder=2)

    label_artists, label_bboxes = [], []
    # v8.0.4 顶刊角色化配色：同族明度阶梯 + 终点唯一强调色，
    # 替代 v8.0.3 色轮循环（多饱和色并列=杂色感的机制根因）。
    _rc = _role_colors(blocks, arrows, _tc)
    for bi, b in enumerate(blocks):
        fp_l = cjk_fp if cjk_fp and has_cjk_local(b.get("label", "")) else None
        fp_s = cjk_fp if cjk_fp and has_cjk_local(b.get("sublabel") or "") else None
        # 优先级：显式 color > 角色化配色（明度阶梯/终点强调）
        bc = b.get("color") or _rc.get(bi, _tc[0])
        # v8.0.5 F1 形状注册表：14 语义形状（几何 bbox 契约不变——磁吸/闸零特判）
        shape = resolve_shape(b.get("shape", "round"))
        spec = SHAPES[shape]
        # 顶刊描边纪律：描边=同色加深（完整度），填充满 alpha（印刷不发灰）。
        _ec = _shade(bc, 0.22)
        lw = 1.2 if shape == "rect" else 1.0
        for _a in spec["draw"](ax, b, bc, _ec, lw):
            ax.add_patch(_a)
        tcol = _text_color(bc)
        # 非矩形形状：fit_text 按内接区系数缩（菱形×0.54 等），
        # 文字中心随 ty 偏移（cylinder 偏下避顶椭圆）
        _tw, _th = spec["tb"]
        lab_lines, sub_lines, fs_m, fs_s = fit_text(
            ax, b.get("label", b.get("id", "")), b.get("sublabel"),
            b["w"] * _tw, b["h"] * _th, fs, fp_l, fp_s)
        lab_h = measure_in(ax, "\n".join(lab_lines), fs_m, fp_l, ls=LINE_K)[1]
        mid_y = b["y"] + b["h"] / 2 + spec["ty"] * b["h"]
        if sub_lines:
            sub_h = measure_in(ax, "\n".join(sub_lines), fs_s, fp_s,
                               ls=LINE_K)[1]
            cy = mid_y + (sub_h + 0.05) / 2
            sy = mid_y - (lab_h + 0.05) / 2
        else:
            cy, sy = mid_y, None
        ax.text(b["x"] + b["w"] / 2, cy, "\n".join(lab_lines), ha="center",
                va="center", fontsize=fs_m, color=tcol, fontweight="bold",
                fontproperties=fp_l, zorder=4, linespacing=LINE_K)
        if sub_lines:
            ax.text(b["x"] + b["w"] / 2, sy, "\n".join(sub_lines), ha="center",
                    va="center", fontsize=fs_s, color=tcol, alpha=0.85,
                    fontproperties=fp_s, zorder=4, linespacing=LINE_K)

    # ── 4) 画箭头（折线+实体头三角；v8.0.5 F4 边型 thick/bidirectional/open）──
    # v8.1.5 --flow-hops：交叉跳线。后画的边在与先画边的规范相交处断线画半圆弧
    # （半径 0.055in，交点距两端点 ≥0.06in 才记），读作「跳过」而非 T 形分岔。
    # off（默认）时 _hop_map 恒空，绘制路径与旧版逐字节等价。
    _hop_map = {}
    if hops:
        _segs = []
        for _i, (_e, _pts) in enumerate(route_meta):
            for _k in range(len(_pts) - 1):
                # 携带本边点数：末段换算守卫用存储值（外层 _pts 在配对循环时
                # 已是最后一条边的残留值——LES 级教训：循环变量泄漏进闭包外）
                _segs.append((_i, _k, _pts[_k], _pts[_k + 1], len(_pts)))
        for _a in range(len(_segs)):
            _i, _ka, _p0, _p1, _npts = _segs[_a]
            for _b in range(_a):
                _j, _kb, _q0, _q1, _qnpts = _segs[_b]
                if _j == _i or not _seg_cross_line(_p0, _p1, _q0, _q1):
                    continue
                # 交点（两段均为轴对齐；一般式解两线交点再钳到段内）
                _d1x, _d1y = _p1[0] - _p0[0], _p1[1] - _p0[1]
                _d2x, _d2y = _q1[0] - _q0[0], _q1[1] - _q0[1]
                _den = _d1x * _d2y - _d1y * _d2x
                if abs(_den) < 1e-12:
                    continue
                _t2 = ((_q0[0] - _p0[0]) * _d1y - (_q0[1] - _p0[1]) * _d1x) / _den
                _ip = (_q0[0] + _t2 * _d2x, _q0[1] + _t2 * _d2y)
                if not (min(_p0[0], _p1[0]) - 1e-9 <= _ip[0] <= max(_p0[0], _p1[0]) + 1e-9
                        and min(_p0[1], _p1[1]) - 1e-9 <= _ip[1] <= max(_p0[1], _p1[1]) + 1e-9
                        and min(_q0[0], _q1[0]) - 1e-9 <= _ip[0] <= max(_q0[0], _q1[0]) + 1e-9
                        and min(_q0[1], _q1[1]) - 1e-9 <= _ip[1] <= max(_q0[1], _q1[1]) + 1e-9):
                    continue                     # 交点不在两段之内（退化/镜像）：放弃
                if min(math.hypot(_ip[0] - _p0[0], _ip[1] - _p0[1]),
                       math.hypot(_ip[0] - _p1[0], _ip[1] - _p1[1]),
                       math.hypot(_ip[0] - _q0[0], _ip[1] - _q0[1]),
                       math.hypot(_ip[0] - _q1[0], _ip[1] - _q1[1])) < 0.06:
                    continue
                _L = math.hypot(_d1x, _d1y) or 1.0
                _tt = ((_ip[0] - _p0[0]) * _d1x + (_ip[1] - _p0[1]) * _d1y) / (_L * _L)
                if _ka == _npts - 2:             # 末段：参数换算到实际绘制的杆部
                    _Ld = max(_L - HEAD_LEN, 1e-9)
                    _tt = _tt * _L / _Ld
                    if _tt >= 0.9:               # 跳点落在头部区（不画线）：放弃
                        continue
                _hop_map.setdefault((_i, _ka), []).append((min(max(_tt, 0.0), 1.0), _ip))
        print(f"[flow-hops] {sum(len(v) for v in _hop_map.values())} crossing(s) hopped", file=sys.stderr)
    # 屏幕比例（像素/数据单位）：跳弧要画成屏幕正圆（数据坐标里 x/y 比例不同，
    # 直接用数据半径画出来是椭圆——虚线上的椭圆弧回摆会与下一根虚线粘连成
    # 「泪滴」，评审 R1 实锤）。渲染器尚未落图时用 get_renderer 现取。
    _hop_sx = _hop_sy = None
    if hops:
        try:
            _ren = fig.canvas.get_renderer()
            _ta, _tb = ax.transData.transform((0, 0)), ax.transData.transform((1, 1))
            _hop_sx, _hop_sy = abs(_tb[0] - _ta[0]) or 1.0, abs(_tb[1] - _ta[1]) or 1.0
        except Exception:
            _hop_sx = _hop_sy = None

    for _ei, (e, pts) in enumerate(route_meta):
        col = e.get("color", arrow_color)
        ls = (0, (5, 3)) if e.get("dashed") else "-"
        lw = 2.2 if e.get("thick") else (1.4 if e.get("dashed") else 1.5)
        _head, _tail = pts[-1], pts[-2]
        _dx, _dy = _head[0] - _tail[0], _head[1] - _tail[1]
        _L = math.hypot(_dx, _dy) or 1.0
        _ux, _uy = _dx / _L, _dy / _L
        _base = (_head[0] - _ux * HEAD_LEN, _head[1] - _uy * HEAD_LEN)
        # open=True：无头→shaft 画到 apex（留头回退只该在有头时发生——
        # judge 实锤：无头线短 HEAD_LEN=96px 悬空观感）
        _shaft_end = _head if e.get("open") else _base
        # v8.1.5：跳点处断线画弧（_hop_map 空=单段直画，与旧版等价）
        _P = list(pts[:-1]) + [_shaft_end]
        _pieces = [[_P[0]]]
        _arcs = []
        for _k in range(len(_P) - 1):
            _A, _B = _P[_k], _P[_k + 1]
            _hl = math.hypot(_B[0] - _A[0], _B[1] - _A[1]) or 1e-9
            for (_t, _ip) in sorted(_hop_map.get((_ei, _k), []), key=lambda z: z[0]):
                if _hop_sx is None:
                    continue                       # 拿不到屏幕比例：保持直线交叉
                _r = 0.055                          # 数据单位（终裁画布 1unit=1in=屏幕圆）
                _g = _r / _hl
                if _g * 2 >= 0.8:
                    continue                       # 段太短放不下跳弧：放弃
                _a = (_A[0] + (_B[0] - _A[0]) * (_t - _g),
                      _A[1] + (_B[1] - _A[1]) * (_t - _g))
                _b = (_A[0] + (_B[0] - _A[0]) * (_t + _g),
                      _A[1] + (_B[1] - _A[1]) * (_t + _g))
                _nv0 = (-( _B[1] - _A[1]) / _hl * _r, (_B[0] - _A[0]) / _hl * _r)
                _arc = []
                for _s in range(11):
                    _cs = math.cos(math.pi * _s / 10)
                    _sn = math.sin(math.pi * _s / 10)
                    _arc.append((_ip[0] + (_a[0] - _ip[0]) * _cs + _nv0[0] * _sn,
                                 _ip[1] + (_a[1] - _ip[1]) * _cs + _nv0[1] * _sn))
                _pieces[-1].append(_a)
                _arcs.append(_arc)
                _pieces.append([_b])
            _pieces[-1].append(_B)
        for _pc in _pieces:
            if len(_pc) >= 2:
                ax.plot([q_[0] for q_ in _pc], [q_[1] for q_ in _pc],
                        color=col, lw=lw, linestyle=ls, zorder=2,
                        solid_capstyle="butt")
        for _arc in _arcs:
            ax.plot([q_[0] for q_ in _arc], [q_[1] for q_ in _arc],
                    color=col, lw=lw, linestyle="-", zorder=2,
                    solid_capstyle="round")
        _px, _py = -_uy, _ux
        # open=True：无头线（开放连接）；默认实体箭头
        if not e.get("open"):
            ax.add_patch(Polygon([_head, (_base[0] + _px * HEAD_LEN * 0.42,
                                          _base[1] + _py * HEAD_LEN * 0.42),
                                  (_base[0] - _px * HEAD_LEN * 0.42,
                                   _base[1] - _py * HEAD_LEN * 0.42)],
                                 closed=True, facecolor=col, edgecolor=col,
                                 lw=0.4, zorder=2.5))
        # v8.1.3：箭头三角 zorder 5→2.5（连线 2 之上、节点 3 之下）——浅斜边上
        # 水平进入时翼片会探入节点 0.027in（mermaid 复查箭头实测），探入部分
        # 由节点填充盖住；尖端停在描边外沿（EDGE_NIB）不受影响。连线穿节点
        # 本来就是路由硬禁，节点置顶不会遮住任何合法线段。
        # bidirectional=True：起点反向箭头（双头）。apex 与终点头同纪律负咬合
        # （v8.0.5 补：apex=_tail 裸压源框边线=600dpi 刺描边同型缺陷）
        if e.get("bidirectional"):
            _apex0 = (_tail[0] + _ux * abs(EDGE_NIB), _tail[1] + _uy * abs(EDGE_NIB))
            _b2 = (_apex0[0] + _ux * HEAD_LEN, _apex0[1] + _uy * HEAD_LEN)
            ax.add_patch(Polygon([_apex0, (_b2[0] + _px * HEAD_LEN * 0.42,
                                           _b2[1] + _py * HEAD_LEN * 0.42),
                                  (_b2[0] - _px * HEAD_LEN * 0.42,
                                   _b2[1] - _py * HEAD_LEN * 0.42)],
                                 closed=True, facecolor=col, edgecolor=col,
                                 lw=0.4, zorder=2.5))
        if e.get("label"):
            fp_e = cjk_fp if cjk_fp and has_cjk_local(e["label"]) else None
            # 白底标签只避让**其他边**的线段（自身段有白垫可贴线，graphviz 同款）
            _own_keys = {(round(q0[0], 3), round(q0[1], 3), round(q1[0], 3),
                          round(q1[1], 3)) for q0, q1 in
                         zip(pts[:-1], pts[1:])}
            _other = [(q0, q1) for (q0, q1) in route_lines
                      if (round(q0[0], 3), round(q0[1], 3), round(q1[0], 3),
                          round(q1[1], 3)) not in _own_keys]
            # v8.1.0 两轮放置：严格轮要求「标签离自己的边最近」且不硬塞；无解才
            # 放宽重试（旧行为）——保证既有图不丢标签，同时优先选归属清楚的位
            _kw = dict(fp=fp_e, fs=max(8.0, fs - 2),
                       color=e.get("label_color", "#444444"),
                       line_segs=_other, force_side=_rt_force.get(id(e), 0),
                       lane_base=_tc[0])
            _n0 = len(label_bboxes)      # 本次放置前标签框数（归属按索引回填）
            _trk = [t_ for g_ in GAP_TRACKS for t_ in g_["tracks"]
                    if tuple(t_["edge"]) == (e["from"], e["to"]) and t_["label"]]
            if _trk and any(abs(p_[1] - _trk[0]["line_y"]) < 0.02 for p_ in pts):
                _kw["prefer"] = "below"     # 走在通道轨道上：标签放线下方的标签区
            t = bb = None
            if " " in e["label"] and "\n" not in e["label"]:
                # 单行优先：窄间隙预折行会把 "48 h SLA" 无谓地拆成两行——段旁
                # 有位放单行就放单行（v8.1.0）
                t, bb = place_edge_label(ax, fig, e["label"], pts, blocks,
                                         label_bboxes, strict_assoc=True,
                                         no_wrap=True, primary_only=True, **_kw)
            if t is None and "_lanes_geo" in blocks[0]:
                # 泳道：单行再试一轮全部非硬塞阶段（泳道无引线兜底位，单行贴线
                # 优于折行后贴线）；非泳道保留「折行贴边」优先于「单行引线远置」
                t, bb = place_edge_label(ax, fig, e["label"], pts, blocks,
                                         label_bboxes, strict_assoc=True,
                                         no_wrap=True, **_kw)
            if t is None:
                t, bb = place_edge_label(ax, fig, e["label"], pts, blocks,
                                         label_bboxes, strict_assoc=True, **_kw)
            if t is None:
                t, bb = place_edge_label(ax, fig, e["label"], pts, blocks,
                                         label_bboxes, **_kw)
            # v8.0.7 去重：place 成功路径与 8 向兜底可能对同一 bb 双记
            # （strict 层2 假撞 #1×#2 根因）——bb 已在 label_bboxes 则不再记
            if bb is not None:
                # 归属表与 label_bboxes **按索引严格对齐**：place_edge_label 成功时
                # 会直接往同一个列表（placed_boxes 即 label_bboxes）追加 bb，
                # 旧写法「不在列表里才登记归属」因此几乎从不登记→审计的「标签
                # 归属」检查对多数标签静默跳过（假绿，2026-11-24 自查发现）
                label_meta += [None] * (len(label_bboxes) - len(label_meta))
                _ii = next((k for k in range(_n0, len(label_bboxes))
                            if label_bboxes[k] == bb), None)
                if _ii is None:
                    label_bboxes.append(bb)
                    label_meta.append([e["from"], e["to"]])
                else:
                    label_meta[_ii] = [e["from"], e["to"]]
            label_artists.append(t)

    # ── 6) 自由注记 ──
    for ann in annotations:
        ax.text(ann["x"], ann["y"], ann["text"], ha=ann.get("ha", "center"),
                va=ann.get("va", "center"), fontsize=ann.get("fontsize", fs),
                color=ann.get("color", text_color),
                fontweight=ann.get("weight", "normal"),
                fontproperties=cjk_fp if cjk_fp and has_cjk_local(ann["text"])
                else None, zorder=5)

    # ── 7) 画布终裁（R5）：墨水包围盒 + 统一边距，1unit=1in 契约随 resize 保持。
    # v8.0.4 替换旧几何预留裁剪（按 lane 预留对称扩边=judged 实锤的
    # 「左侧整条空白/上下失衡」根因）；占比改按**面积**诚实计算。
    fig.canvas.draw()
    _rend = fig.canvas.get_renderer()
    _bbs = []
    for _a in (*ax.patches, *ax.lines, *ax.texts):
        try:
            _bbs.append(_a.get_window_extent(_rend))
        except Exception:
            pass
    _inv = ax.transData.inverted()
    _pts = _inv.transform([(_b.x0, _b.y0) for _b in _bbs] +
                          [(_b.x1, _b.y1) for _b in _bbs])
    _ix0 = min(p[0] for p in _pts)
    _ix1 = max(p[0] for p in _pts)
    _iy0 = min(p[1] for p in _pts)
    _iy1 = max(p[1] for p in _pts)
    if _legend_on:
        # v8.1.0 R18：图例条带必须在**最终 trim** 里预留（1.5 的底垫被此处
        # 自适应边距覆盖→图例行被挤回带区、分隔线/标题竖条穿条带实锤）——
        # 内容域下探 0.42，图例行=最终 ylim0+0.24 恒落带家具之下
        _iy0 -= 0.42
    # 自适应边距（v8.0.4）：按内容尺寸比例取边距、常数封顶——封顶值已按
    # savefig bbox_inches='tight' 的 pad_inches=0.1 第二层边距校准（双层叠加
    # 会稀释面积占比：论文 fig2 实测引擎 0.28+save 0.2 → 面积 71.8%<75% DoD）。
    _pad_x = min(0.18, max((_ix1 - _ix0) * 0.04, 0.10))
    _pad_y = min(0.20, max((_iy1 - _iy0) * 0.12, 0.10))
    _lx0, _ly0 = _ix0 - _pad_x, _iy0 - _pad_y
    _lx1, _ly1 = _ix1 + _pad_x, _iy1 + _pad_y
    ax.set_xlim(_lx0, _lx1)
    ax.set_ylim(_ly0, _ly1)
    fig.set_size_inches(max(_lx1 - _lx0, 1.5), max(_ly1 - _ly0, 1.5))
    ax.set_position([0, 0, 1, 1])
    ratio = ((_ix1 - _ix0) * (_iy1 - _iy0)) / max((_lx1 - _lx0) * (_ly1 - _ly0), 1e-9)
    ax.axis("off")
    # ── 7.5) 边样式图例（v8.1.0）：画布底部专用条带——线样+语义文字，
    # 语言随节点标签 CJK 检测；不进闸几何（纯注释层 z=4）
    if _legend_on:
        _has_d = any(e.get("dashed") for e in arrows)
        _has_t = any(e.get("thick") for e in arrows)
        _has_b = any(e.get("bidirectional") for e in arrows)
        _cjk = any(has_cjk_local(b.get("label", "")) for b in blocks)
        _items = []
        if _has_d:
            _items.append((True, False, False,
                           "dashed = feedback / rework" if not _cjk
                           else "虚线 = 反馈 / 返工回路"))
        if _has_t:
            _items.append((False, True, False,
                           "thick = critical path" if not _cjk
                           else "粗线 = 关键路径"))
        if _has_b:
            _items.append((False, False, True,
                           "double-head = bidirectional" if not _cjk
                           else "双头 = 双向"))
        if _items:
            _x_leg = ax.get_xlim()[0] + 0.2
            _y_leg = ax.get_ylim()[0] + 0.24
            # v8.1.0：图例文字/线色随画布底色自动反色（深色主题下灰字低对比）
            _fc = ax.get_facecolor()
            try:
                _lum = 0.299 * _fc[0] + 0.587 * _fc[1] + 0.114 * _fc[2]
            except (TypeError, IndexError):
                _lum = 1.0
            _leg_c = "#E8E8E8" if _lum < 0.5 else "#555555"
            for _i, (_d, _tk, _bi, _txt) in enumerate(_items):
                _xx = _x_leg + _i * 2.6
                _seg_kw = dict(color=_leg_c, lw=2.2 if _tk else 1.2,
                               zorder=4)
                if _d:
                    _seg_kw.update(linestyle=(0, (4, 3)))
                ax.plot([_xx, _xx + 0.34], [_y_leg, _y_leg], **_seg_kw)
                if _bi:
                    from matplotlib.patches import FancyArrowPatch
                    ax.add_patch(FancyArrowPatch(
                        (_xx, _y_leg), (_xx + 0.34, _y_leg),
                        arrowstyle="<|-|>", mutation_scale=9,
                        color=_leg_c, lw=1.2, zorder=4))
                ax.text(_xx + 0.42, _y_leg, _txt, ha="left", va="center",
                        fontsize=max(fs - 2, 6), color=_leg_c, zorder=4,
                        fontproperties=cjk_fp if cjk_fp and has_cjk_local(_txt)
                        else None)

    fig.canvas.draw()  # 终裁后刷新变换，闸门按最终几何测量

    # ── 8) 闸 ──
    violations = []
    if gate == "strict":
        violations = gate_strict(ax, fig, blocks, label_bboxes, route_lines,
                                 ratios=ratio)
    # v8.0.9 QC 边车：最后一次 render 的路由/块几何快照（--dump-flow-routes
    # 与几何闸测试的唯一真值源——CLI rcParams/DPI 与进程内探针的测量漂移
    # 会翻转 wrap 候选与路由决策（v19 假绿根因），探针必须消费 CLI 几何）
    global LAST_GEOM
    LAST_GEOM = {
        "blocks": [{"id": b["id"], "x": float(b["x"]), "y": float(b["y"]),
                    "w": float(b["w"]), "h": float(b["h"]),
                    "shape": resolve_shape(b.get("shape", "round")),
                    "lane": b.get("_lane")}
                   for b in blocks],
        "pools": [{"from": f_, "to": t_,
                   # 选中方案的代价=候选池里与实际路径逐点相同的那条（None=lane 兜底）
                   "selected": next((list(c2[0]) for c2 in pool_
                                     if [tuple(p) for p in c2[1]]
                                     == [tuple(p) for p in route_pts[_pi]]), None),
                   "lane_fallback": not pool_,
                   "rejected": route_rejects[_pi] if _pi < len(route_rejects) else [],
                   "cands": [{"cost": list(c2[0]),
                              "pts": [[float(p[0]), float(p[1])] for p in c2[1]]}
                             for c2 in pool_]}
                  for _pi, (f_, t_, pool_) in enumerate(route_pools)],
        "gap_tracks": GAP_TRACKS,
        "label_trace": {k_: [[list(c_) for c_ in run_] for run_ in v_]
                        for k_, v_ in LABEL_LOG.items()},
        "labels": [{"edge": (label_meta[i] if i < len(label_meta) else None),
                    "bb": [float(v) for v in bb]}
                   for i, bb in enumerate(label_bboxes)],
        "routes": [{"from": e["from"], "to": e["to"],
                    "pts": [[float(p[0]), float(p[1])] for p in pts]}
                   for (e, pts) in route_meta],
        "lanes_geo": [dict(g) for g in (blocks[0].get("_lanes_geo") or [])]
        if blocks else [],
    }
    return violations, ratio
