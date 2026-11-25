"""af_mermaid.py — mermaid flowchart 语法子集 → academic-figures flow 语义 JSON（F5 v8.0.6）。

生态互操作：mermaid 用户零成本迁移。支持子集（官方 flowchart 语法经典层）：
- 声明：flowchart TD/TB/LR/BT/RL、graph ...
- 节点形状 → SHAPES 映射：[x] rect、(x)/([x]) round、{x} diamond、{{x}} hexagon、
  [(x)] cylinder、((x))/(((x))) terminal、[[x]] predefined、[/x/] io、[\\x\\] io、
  [/x\\] manual-op、[\\x/] manual-input、>x] asymmetric→rect
- 边：--> 实线 / -.-> dashed / ==> thick / --- open / --o --x 端饰简化 open /
  <--> o--o x--x bidirectional；边标签 |text| 与 -- text -->；链式 A-->B-->C、
  & 并联 A & B --> C
- subgraph 标题 ... end → 泳道（layout=swimlane，按出现次序；TB 方向直通泳道 v8.1.0；LR/BT/RL→分组框诚实降级；嵌套摊平最外层）
- style/classDef/class/linkStyle **样式映射 v8.1.0**：linkStyle <i>[,j…|default]
  stroke:<color> → 边 color、stroke-dasharray → dashed、stroke-width≥3px →
  thick；classDef <名> fill:<color> + class <n…> <名> → 节点 color；style <n>
  fill:<color> → 节点 color。其余属性（宽度/字体等）忽略（诚实边界：仅映射
  形状语义样式）。click/%% 注释行忽略

诚实边界：图标/图片节点、curve 样式、动画、markdown 标签为超出子集——遇到即
ValueError（exit 3），绝不静默丢边。
"""
import re

_DECL_RE = re.compile(r"^(?:flowchart|graph)\s+(TB|TD|BT|RL|LR)\b", re.I)
_SUBGRAPH_RE = re.compile(r"^\s*subgraph\s+(.+?)\s*$", re.I)
_END_RE = re.compile(r"^\s*end\s*$", re.I)
_IGNORE_RE = re.compile(r"^\s*(%%|click\s)", re.I)
_CLASSDEFS = {}   # classDef 名 → fill 色（parse 期间填充）
_STYLE_LINK_RE = re.compile(
    r"^\s*linkStyle\s+(default|[\d,\s]+)\s+(.+)$", re.I)
_CLASSDEF_RE = re.compile(r"^\s*classDef\s+(\w+)\s+(.+)$", re.I)
_CLASS_APPLY_RE = re.compile(r"^\s*class\s+([\w,\s]+?)\s+(\w+)\s*$", re.I)
_STYLE_NODE_RE = re.compile(r"^\s*style\s+(\w+)\s+(.+)$", re.I)


def _style_fill(props):
    """样式属性串 → fill 色（诚实映射：仅 fill:<色>）。"""
    m = re.search(r"fill:\s*([^,;\s]+)", props or "")
    if not m:
        return None
    c = m.group(1).strip().strip('"\'')
    return None if c.lower() in ("none", "transparent") else c


def _apply_link_style(m, edges):
    """linkStyle <索引…|default> <属性> → 边 color/dashed/thick（v8.1.0）。"""
    idx_part, props = m.group(1).strip(), m.group(2)
    mst = re.search(r"stroke:\s*([^,;\s]+)", props)
    color = mst.group(1).strip() if mst else None
    dashed = bool(re.search(r"stroke-dasharray\s*:", props))
    thick = False
    mw = re.search(r"stroke-width:\s*([\d.]+)px", props)
    if mw and float(mw.group(1)) >= 3:
        thick = True
    targets = list(range(len(edges))) \
        if idx_part == "default" else \
        [int(x) for x in re.split(r"[,\s]+", idx_part) if x != ""]
    for i in targets:
        if 0 <= i < len(edges):
            if color:
                edges[i]["color"] = color
            if dashed:
                edges[i]["dashed"] = True
            if thick:
                edges[i]["thick"] = True

# 边操作符（长前缀优先）
_EDGE_OPS = ["<==>", "o==o", "x==x", "<-->", "o--o", "x--x", "-.->", "==>",
             "-->", "---", "--o", "--x", "-.-", "==="]
_OP_SPLIT_RE = re.compile(
    r"(" + "|".join(re.escape(o) for o in sorted(
        _EDGE_OPS, key=len, reverse=True)) + r")")
_LABEL_PIPE_RE = re.compile(r"[|]([^|]*)[|]")

_NODE_TOKEN_RE = re.compile(
    r"^([A-Za-z0-9_\-]+)\s*"
    r"(?:\[\[([^\[\]]*)\]\]|\[\(([^\[\]()]*)\)\]|\(\(([^\(\)]*)\)\)|"
    r"\{([^{}]*)\}|>([^\]]*)\]|\[([^\[\]]*)\]|\(([^()]*)\))?\s*$")


def _shape_from_token(token):
    """节点 token → (id, label, shape)。纯 id→(id, id, rect)。"""
    token = token.strip()
    m = _NODE_TOKEN_RE.match(token)
    if not m:
        raise ValueError(f"mermaid: 无法解析节点 {token[:40]!r}")
    nid = m.group(1)
    forms = {2: "predefined", 3: "cylinder", 4: "terminal", 5: "diamond",
             6: "asym", 7: "raw-sq", 8: "round"}
    form = next((forms[i] for i in range(2, 9) if m.group(i) is not None),
                None)
    if form is None:
        return nid, nid, "rect"
    label = m.group(next(i for i in range(2, 9) if m.group(i) is not None))
    if form == "asym":
        return nid, label.strip(), "rect"   # mermaid asymmetric（bookmark）→rect
    label = label.strip()
    if form == "raw-sq":
        if label.startswith("/") and label.endswith("\\"):
            return nid, label[1:-1].strip(), "manual-op"
        if label.startswith("\\") and label.endswith("/"):
            return nid, label[1:-1].strip(), "manual-input"
        if label.startswith(("/", "\\")) and label.endswith(("/", "\\")):
            return nid, label[1:-1].strip(), "io"
        return nid, label, "rect"
    if form == "round" and label.startswith("[") and label.endswith("]"):
        label = label[1:-1].strip()   # stadium ([x])
    if label.startswith('"') and label.endswith('"'):
        label = label[1:-1]
    label = label.replace("#quot;", '"').replace("fa:fa-", "").strip()
    return nid, label, form


def _classify_op(op):
    """边操作符 → (kind, dir_text)。kind ∈ solid/dashed/thick/open/bidirectional。"""
    core = op.strip()
    if core in ("<-->", "o--o", "x--x", "<==>", "o==o", "x==x"):
        return "bidirectional"
    if core.startswith("==") or core.endswith("=="):
        return "thick"
    if core.startswith("-.") or core.endswith(".-"):
        return "dashed"
    if core in ("---", "--o", "--x"):
        return "open"
    return "solid"


def parse_mermaid(text):
    """mermaid flowchart 文本 → flow 语义 dict。语法外内容 ValueError。"""
    nodes_by_id = {}
    order = []
    edges = []
    lanes = []
    node_lane = {}
    direction = "TB"
    cur_lane = None
    _node_colors = {}
    _CLASSDEFS.clear()
    for raw in text.splitlines():
        line = raw.rstrip()
        s = line.strip()
        if not s or _IGNORE_RE.match(s):
            continue
        ms_ = _STYLE_LINK_RE.match(s)
        if ms_:
            _apply_link_style(ms_, edges)
            continue
        ms_ = _CLASSDEF_RE.match(s)
        if ms_:
            _fill = _style_fill(ms_.group(2))
            if _fill:
                _CLASSDEFS[ms_.group(1)] = _fill
            continue
        ms_ = _CLASS_APPLY_RE.match(s)
        if ms_:
            _fill = _CLASSDEFS.get(ms_.group(2))
            for nid_ in re.split(r"[,\s]+", ms_.group(1).strip()):
                if nid_:
                    _node_colors[nid_] = _fill
            continue
        ms_ = _STYLE_NODE_RE.match(s)
        if ms_:
            _node_colors[ms_.group(1)] = _style_fill(ms_.group(2))
            continue
        md = _DECL_RE.match(s)
        if md:
            direction = md.group(1).upper()
            if direction == "TD":
                direction = "TB"
            continue
        if _END_RE.match(s):
            cur_lane = None
            continue
        ms = _SUBGRAPH_RE.match(s)
        if ms:
            title = ms.group(1).strip()
            mtitle = re.match(r"^[A-Za-z0-9_]+\s+\[(.+)\]\s*$", title)
            if mtitle:
                title = mtitle.group(1).strip("'")   # subgraph id [title] 形态
            title = title.strip('"').strip()
            if title not in lanes:
                lanes.append(title)
            cur_lane = title
            continue
        # 边行：提取 |label|（挂在第一个含它的 op 上）
        pipe_lbl = None
        mp = _LABEL_PIPE_RE.search(s)
        if mp:
            pipe_lbl = mp.group(1).strip()
        parts = [p for p in _OP_SPLIT_RE.split(s) if p and p.strip()]
        if len(parts) >= 3 and any(p in _EDGE_OPS for p in parts[1::2]):
            # 交替 [tok, op, tok, op, tok...]
            pending_op = None
            chunk_lbl = pipe_lbl
            toks = []
            for seg in parts:
                if seg in _EDGE_OPS:
                    toks.append(("op", seg))
                else:
                    # op 后紧跟的 |label| 粘在下一 token 头部——剥出归属前 op
                    mlbl = re.match(r"^\s*[|]([^|]*)[|]\s*(.*)$", seg.strip())
                    if mlbl and toks and toks[-1][0] == "op":
                        toks.append(("tok", mlbl.group(2)))
                        if not chunk_lbl:
                            chunk_lbl = mlbl.group(1).strip()
                    else:
                        toks.append(("tok", seg))
            # 归一：确保交替（tok 开头）
            for k in range(0, len(toks) - 2, 2):
                ta, op, tb = toks[k], toks[k + 1], toks[k + 2]
                if ta[0] != "tok" or op[0] != "op" or tb[0] != "tok":
                    raise ValueError(
                        f"mermaid: 边语句解析失败——{s[:60]!r}")
                kind = _classify_op(op[1])
                # op 内嵌 |label|（A -->|text| B → op 段含 |）——pipe 已在行级提取
                lbl = chunk_lbl
                a_id, a_lbl, a_shape = _shape_from_token(ta[1])
                b_id, b_lbl, b_shape = _shape_from_token(tb[1])
                for nid, lbl_, shp in ((a_id, a_lbl, a_shape),
                                       (b_id, b_lbl, b_shape)):
                    if nid not in nodes_by_id:
                        nodes_by_id[nid] = {"id": nid, "label": lbl_,
                                            "shape": shp}
                        order.append(nid)
                        if cur_lane is not None:
                            node_lane[nid] = cur_lane
                    elif lbl_ != nid:   # 首个形状声明生效
                        nodes_by_id[nid]["label"] = lbl_
                        nodes_by_id[nid]["shape"] = shp
                        if cur_lane is not None and nid not in node_lane:
                            node_lane[nid] = cur_lane
                e = {"from": a_id, "to": b_id}
                if kind == "dashed":
                    e["dashed"] = True
                if kind == "thick":
                    e["thick"] = True
                if kind == "open":
                    e["open"] = True
                if kind == "bidirectional":
                    e["bidirectional"] = True
                if lbl:
                    e["label"] = lbl
                edges.append(e)
            continue
        # 纯节点声明行
        nid, lbl_, shp = _shape_from_token(s)
        if nid not in nodes_by_id:
            nodes_by_id[nid] = {"id": nid, "label": lbl_, "shape": shp}
            order.append(nid)
            if cur_lane is not None:
                node_lane[nid] = cur_lane
        else:
            nodes_by_id[nid]["label"] = lbl_
            nodes_by_id[nid]["shape"] = shp
    if not nodes_by_id:
        raise ValueError("mermaid: 未发现任何节点定义（需 flowchart 声明+节点）")
    nodes = [nodes_by_id[i] for i in order]
    # v8.1.0：TB 方向 + subgraph → 泳道直通（v8.0.9 泳道转正后接通；v8.0.6
    # 时因泳道 experimental 质量红线改 groups 回退）。subgraph 外节点归首
    # 泳道。LR/BT/RL 保持 groups 回退——subgraph 在 mermaid LR 的排列语义
    # 与泳道行不对应，诚实降级不猜测用户意图。
    for n in nodes:
        _c = _node_colors.get(n["id"])
        if _c:
            n["color"] = _c
    out = {"layout": "layered", "direction": direction,
           "nodes": nodes, "edges": edges}
    if lanes:
        for n in nodes:
            n["lane"] = lanes.index(node_lane[n["id"]]) \
                if n["id"] in node_lane else 0
        if direction == "TB":
            out["layout"] = "swimlane"
            out["lanes"] = list(lanes)
        else:
            _groups = []
            for lname in lanes:
                _blk = [nid for nid in order if node_lane.get(nid) == lname]
                if _blk:
                    _groups.append({"blocks": _blk, "label": lname})
            if _groups:
                out["groups"] = _groups
    return out
