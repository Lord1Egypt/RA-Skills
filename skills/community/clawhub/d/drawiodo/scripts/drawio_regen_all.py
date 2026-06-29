"""
drawio_regen_all.py — 一次性重新生成所有问题图
class_diagram, er_diagram, mindmap, network_datacenter
全部使用结构化布局 + 互斥避让路由 + 动态间距
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))

from drawio_gen import DrawIOBuilder, NodeStyle, EdgeStyle, Styles
from drawio_layout import text_width
from drawio_route import ObstacleRouter, Rect

OUTPUT_DIR = r"C:\Users\sm001\WorkBuddy\2026-06-19-11-30-56"
GAP_X = 30  # 节点水平间距


# ================================================================
# 辅助
# ================================================================

def auto_node_size(label: str, font_size: int = 12) -> tuple:
    """根据标签文本自动计算节点宽高"""
    tw = text_width(label, font_size)
    w = max(90, min(tw + 24, 220))
    h = 50
    if tw > 196:
        lines = math.ceil(len(label) / 14)
        h = max(50, lines * 18 + 14)
    return int(w), int(h)


def _path_clear(points: list, obstacles: list, exclude: set) -> bool:
    """检查路径是否不碰任何障碍物"""
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        sx_min, sx_max = (x1, x2) if x1 <= x2 else (x2, x1)
        sy_min, sy_max = (y1, y2) if y1 <= y2 else (y2, y1)
        seg = Rect(sx_min, sy_min, sx_max - sx_min, sy_max - sy_min)
        for r, nid in obstacles:
            if nid in exclude:
                continue
            if seg.overlaps(r):
                return False
    return True


def _fanout_route(src_node, tgt_node, obstacles: list,
                  exclude: set, lane_offset: float = 0) -> list:
    """带扇出偏移的路径规划"""
    sx = src_node.x + src_node.width / 2
    sy = src_node.y + src_node.height
    tx = tgt_node.x + tgt_node.width / 2
    ty = tgt_node.y

    # 水平方向
    mid_x = sx + (tx - sx) * 0.3 + lane_offset
    path = [(sx, sy), (mid_x, sy), (mid_x, ty), (tx, ty)]
    if _path_clear(path, obstacles, exclude):
        return [(mid_x, sy), (mid_x, ty)]

    # 垂直方向
    mid_y = sy + (ty - sy) * 0.5 + lane_offset
    path = [(sx, sy), (sx, mid_y), (tx, mid_y), (tx, ty)]
    if _path_clear(path, obstacles, exclude):
        return [(sx, mid_y), (tx, mid_y)]

    return []


# ================================================================
# 1. CLASS DIAGRAM — 居中网格 + 同层连接优先
# ================================================================

def generate_class_diagram():
    """生成 UML 类图 — 电商系统"""
    classes = [
        {
            "name": "User",
            "fields": ["- id: Long", "- username: String", "- email: String", "- createdAt: Date"],
            "methods": ["+ login(): void", "+ logout(): void"],
        },
        {
            "name": "Product",
            "fields": ["- id: Long", "- name: String", "- price: BigDecimal", "- stock: Integer"],
            "methods": ["+ getStockStatus(): String"],
        },
        {
            "name": "Order",
            "fields": ["- orderId: Long", "- userId: Long", "- totalAmount: BigDecimal", "- status: String"],
            "methods": ["+ pay(): void", "+ cancel(): void"],
        },
        {
            "name": "Payment",
            "fields": ["- paymentId: Long", "- amount: BigDecimal", "- method: String", "- paidAt: Date"],
            "methods": ["+ process(): boolean", "+ refund(): void"],
        },
        {
            "name": "CartItem",
            "fields": ["- cartId: Long", "- productId: Long", "- quantity: Integer"],
            "methods": ["+ updateQty(n): void"],
        },
        {
            "name": "OrderItem",
            "fields": ["- itemId: Long", "- orderId: Long", "- productId: Long", "- price: BigDecimal"],
            "methods": ["+ subtotal(): BigDecimal"],
        },
    ]

    relationships = [
        ("User", "Order", "1 → *"),
        ("User", "CartItem", "1 → *"),
        ("Order", "OrderItem", "1 → *"),
        ("Product", "OrderItem", "1 → *"),
        ("Product", "CartItem", "1 → *"),
        ("Order", "Payment", "1 → -1"),
    ]

    builder = DrawIOBuilder(name="UML Class Diagram - E-Commerce")

    # 网格布局：2列3行
    cols = 2
    rows = math.ceil(len(classes) / cols)
    cell_w = 240
    cell_h = 130
    gap_x = 60
    gap_y = 50
    canvas_w = 1100
    margin_x = 40

    node_map = {}
    for i, cls in enumerate(classes):
        col = i % cols
        row = i // cols
        items_this_row = min(cols, len(classes) - row * cols)
        row_w = items_this_row * cell_w + gap_x * (items_this_row - 1)
        start_x = margin_x + (canvas_w - margin_x * 2 - row_w) / 2
        x = start_x + col * (cell_w + gap_x)
        y = 40 + row * (cell_h + gap_y)

        # 构建 UML 类 HTML value
        fields_html = "".join(f'        <tr><td style="border:1px solid #6c8ebf;padding:4px;">{f}</td></tr>\n'
                              for f in cls["fields"])
        methods_html = "".join(f'        <tr><td style="border:1px solid #6c8ebf;padding:4px;">{m}</td></tr>\n'
                               for m in cls["methods"])
        value = (
            '       <table style="border-collapse:collapse;width:100%;">\n'
            '         <tr><td style="border:1px solid #6c8ebf;padding:6px;text-align:center;'
            f'background-color:#dae8fc;font-weight:bold;font-size:13px;">{cls["name"]}</td></tr>\n'
            f'{fields_html}'
            f'        <tr><td style="border:1px solid #6c8ebf;padding:4px;"></td></tr>\n'
            f'{methods_html}'
            '       </table>'
        )

        # 计算实际高度
        n_lines = 1 + len(cls["fields"]) + 1 + len(cls["methods"])
        actual_h = n_lines * 26 + 8

        style = NodeStyle(
            shape="rounded=1;whiteSpace=wrap;html=1;overflow=hidden;",
            fill_color="#FFFFFF", stroke_color="#6c8ebf", font_color="#000000"
        )
        node = builder.add_node("", x, y, cell_w, max(cell_h, actual_h),
                                style=style, value=value)
        node_map[cls["name"]] = node

    # 连线
    router = ObstacleRouter(pad=5)
    obstacles = []
    for n in builder.nodes:
        obstacles.append((Rect(n.x, n.y, n.width, n.height), n.id))
        router.add_obstacles([n])

    for src_name, tgt_name, label in relationships:
        if src_name not in node_map or tgt_name not in node_map:
            continue
        src = node_map[src_name]
        tgt = node_map[tgt_name]

        # 判断相对位置
        if tgt.y > src.y + src.height:  # 目标在下
            src_port = 2; tgt_port = 0
        elif tgt.x > src.x + src.width:  # 目标在右
            src_port = 1; tgt_port = 3
        elif tgt.x + tgt.width < src.x:  # 目标在左
            src_port = 3; tgt_port = 1
        elif tgt.y + tgt.height < src.y:  # 目标在上
            src_port = 0; tgt_port = 2
        else:
            src_port = 2; tgt_port = 0

        exclude = {src.id, tgt.id}
        waypoints = []
        try:
            waypoints = router.route(src, tgt, src_port=src_port, tgt_port=tgt_port)
        except:
            pass
        if not waypoints:
            waypoints = _fanout_route(src, tgt, obstacles, exclude)

        edge_style = EdgeStyle(
            line_color="#6c8ebf", font_color="#6c8ebf", font_size=10,
            shape="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;labelBackgroundColor=#FFFFFF;"
        )
        builder.add_edge(src.id, tgt.id, label=label,
                         style=edge_style,
                         source_port=src_port, target_port=tgt_port,
                         waypoints=waypoints)

    path = os.path.join(OUTPUT_DIR, "class_diagram_ecommerce.drawio")
    builder.save(path)
    print(f"✅ class_diagram_ecommerce.drawio saved")
    return path


# ================================================================
# 2. ER DIAGRAM — 单行布局 + 跨行避让
# ================================================================

def generate_er_diagram():
    """生成 ER 图 — 教育系统"""
    entities = [
        {"name": "Lessons", "attrs": "lesson_id PK\\nname\\nduration\\nteacher_id FK"},
        {"name": "Courses",  "attrs": "course_id PK\\ntitle\\ndescription\\nlesson_id FK"},
        {"name": "Students", "attrs": "student_id PK\\nname\\nemail\\nenrolled_date"},
        {"name": "Enrollments", "attrs": "enrollment_id PK\\nstudent_id FK\\ncourse_id FK\\ngrade\\nenrolled_at"},
        {"name": "Users",    "attrs": "user_id PK\\nusername\\npassword\\nrole"},
        {"name": "Reviews",  "attrs": "review_id PK\\ncourse_id FK\\nuser_id FK\\nrating\\ncomment"},
    ]
    relationships = [
        ("Lessons", "Courses", "1 → *", 2, 0),
        ("Courses", "Enrollments", "1 → *", 2, 0),
        ("Students", "Enrollments", "1 → *", 1, 3),
        ("Courses", "Reviews", "1 → *", 2, 0),
        ("Users", "Reviews", "1 → *", 1, 3),
    ]

    builder = DrawIOBuilder(name="ER Diagram - Education System")
    margin_x = 20
    margin_y = 40
    canvas_w = 1169

    n = len(entities)
    node_w = 160
    node_h = 100

    # 计算最长实体属性决定间距
    max_attr = max(entities, key=lambda e: len(e["attrs"]))["attrs"]
    gap_x = max(40, text_width(max_attr, 10) + 60)

    total_w = n * node_w + (n - 1) * gap_x
    start_x = margin_x + (canvas_w - margin_x * 2 - total_w) / 2

    node_map = {}
    for i, ent in enumerate(entities):
        x = start_x + i * (node_w + gap_x)
        y = margin_y

        # 实体属性 text (换行)
        attrs_html = ent["attrs"].replace("\\n", "<br>")
        value = f'<b>{ent["name"]}</b><hr>{attrs_html}'

        style = NodeStyle(
            shape="rounded=1;whiteSpace=wrap;html=1;overflow=hidden;",
            fill_color="#dae8fc", stroke_color="#6c8ebf", font_color="#000000",
            font_size=11,
        )
        node = builder.add_node(ent["name"], x, y, node_w, node_h,
                                style=style, value=value)
        node_map[ent["name"]] = node

    # 连线
    router = ObstacleRouter(pad=5)
    obstacles = []
    for n in builder.nodes:
        obstacles.append((Rect(n.x, n.y, n.width, n.height), n.id))
        router.add_obstacles([n])

    for src_name, tgt_name, label, s_port, t_port in relationships:
        if src_name not in node_map or tgt_name not in node_map:
            continue
        src = node_map[src_name]
        tgt = node_map[tgt_name]

        # 确定端口
        if s_port is None:
            if tgt.y > src.y: s_port = 2; t_port = 0
            else: s_port = 0; t_port = 2

        exclude = {src.id, tgt.id}
        waypoints = []
        try:
            waypoints = router.route(src, tgt, src_port=s_port, tgt_port=t_port)
        except:
            pass
        if not waypoints:
            waypoints = _fanout_route(src, tgt, obstacles, exclude)

        edge_style = EdgeStyle(
            line_color="#6c8ebf", font_color="#6c8ebf", font_size=10,
            shape="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;labelBackgroundColor=#FFFFFF;"
        )
        builder.add_edge(src.id, tgt.id, label=label,
                         style=edge_style,
                         source_port=s_port, target_port=t_port,
                         waypoints=waypoints)

    path = os.path.join(OUTPUT_DIR, "er_diagram_education.drawio")
    builder.save(path)
    print(f"✅ er_diagram_education.drawio saved")
    return path


# ================================================================
# 3. MIND MAP — 水平树（代替径向，避免重叠）
# ================================================================

def generate_mindmap():
    """生成思维导图 — AI技术栈"""
    center = "AI Technology Stack"
    branches = [
        {
            "label": "Machine Learning",
            "sub": ["Supervised", "Unsupervised", "Reinforcement", "Semi-supervised"]
        },
        {
            "label": "Deep Learning",
            "sub": ["CNN", "RNN/LSTM", "Transformer", "GAN", "VAE"]
        },
        {
            "label": "NLP",
            "sub": ["Text Classification", "NER", "Machine Translation", "Sentiment Analysis", "Question Answering"]
        },
        {
            "label": "Computer Vision",
            "sub": ["Object Detection", "Image Segmentation", "Face Recognition", "OCR"]
        },
        {
            "label": "MLOps",
            "sub": ["Pipeline Automation", "Model Registry", "Feature Store", "Monitoring"]
        },
        {
            "label": "LLM / GenAI",
            "sub": ["GPT / LLaMA", "RAG", "Fine-tuning", "Prompt Engineering", "Agent Framework"]
        },
    ]

    builder = DrawIOBuilder(name="Mindmap - AI Technology Stack")
    canvas_w = 1169
    canvas_h = 827
    margin_x = 40
    margin_y = 20

    center_w = text_width(center, 16) + 40
    center_h = 60
    center_x = margin_x
    center_y = canvas_h / 2 - center_h / 2

    cx = center_x + center_w
    cy = center_y + center_h / 2

    # 中心节点
    center_style = NodeStyle(
        fill_color="#1ba1e2", stroke_color="#006EAF",
        font_color="#ffffff", font_size=16, font_style=1,
        shape="rounded=1;whiteSpace=wrap;html=1;"
    )
    center_node = builder.add_node(center, center_x, center_y, center_w, center_h,
                                   style=center_style)

    # 一级分支：垂直均匀分布
    n_branches = len(branches)
    usable_h = canvas_h - margin_y * 2 - 40
    branch_gap = usable_h / (n_branches + 1)
    l1_x = cx + 80

    node_map = {"__center__": center_node}
    parent_map = {}

    for i, br in enumerate(branches):
        bw = text_width(br["label"], 13) + 24
        bw = max(100, min(bw, 180))
        bh = 40
        by = margin_y + (i + 1) * branch_gap - bh / 2

        sw = text_width(br["label"], 13)
        # 分支节点
        l1_style = NodeStyle(
            fill_color="#dae8fc", stroke_color="#6c8ebf",
            font_color="#000000", font_size=13, font_style=1,
        )
        l1_node = builder.add_node(br["label"], l1_x, by, bw, bh, style=l1_style)
        node_map[br["label"]] = l1_node
        parent_map[br["label"]] = "__center__"

        # 子节点：垂直堆叠
        subs = br.get("sub", [])
        n_subs = len(subs)
        sub_h = 30
        sub_gap_y = 4
        total_sub_h = n_subs * sub_h + max(0, n_subs - 1) * sub_gap_y
        sub_x = l1_x + bw + 20
        sub_start_y = by + bh / 2 - total_sub_h / 2

        for j, sub in enumerate(subs):
            sw = text_width(sub, 11) + 16
            sw = max(80, min(sw, 150))
            sx = sub_x
            sy = sub_start_y + j * (sub_h + sub_gap_y)
            sub_style = NodeStyle(
                fill_color="#f5f5f5", stroke_color="#666666",
                font_color="#333333", font_size=11,
            )
            sub_node = builder.add_node(sub, sx, sy, sw, sub_h, style=sub_style)
            node_map[sub] = sub_node
            parent_map[sub] = br["label"]

    # ===== 连线 =====
    # 中心 → 一级分支
    for br in branches:
        child = node_map[br["label"]]
        # 水平直线
        edge_style = EdgeStyle(
            shape="edgeStyle=none;html=1;",
            line_color="#6c8ebf", font_color="#6c8ebf", font_size=10,
        )
        builder.add_edge(center_node.id, child.id,
                         style=edge_style,
                         source_port=1, target_port=3)  # 右→左

    # 一级分支 → 子节点
    for br in branches:
        parent = node_map[br["label"]]
        objs = []
        for n in builder.nodes:
            objs.append((Rect(n.x, n.y, n.width, n.height), n.id))

        for j, sub in enumerate(br.get("sub", [])):
            child = node_map[sub]
            # 正交连线：从父节点右侧出，到子节点左侧入
            edge_style = EdgeStyle(
                line_color="#666666", font_color="#666666", font_size=9,
                shape="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            )
            builder.add_edge(parent.id, child.id,
                             style=edge_style,
                             source_port=1, target_port=3)

    path = os.path.join(OUTPUT_DIR, "mindmap_ai_stack.drawio")
    builder.save(path)
    print(f"✅ mindmap_ai_stack.drawio saved")
    return path


# ================================================================
# 4. NETWORK TOPOLOGY — 分层 + 扇出路由
# ================================================================

def generate_network():
    """生成网络拓扑图"""
    from build_network import build_network_topology

    layers = [
        {"name": "Core Layer", "nodes": [{"label": "Core-SW1"}, {"label": "Core-SW2"}]},
        {"name": "Distribution Layer", "nodes": [{"label": "Dist-SW1"}, {"label": "Dist-SW2"}, {"label": "Dist-SW3"}]},
        {"name": "Access Layer", "nodes": [{"label": "Access-SW1"}, {"label": "Access-SW2"}, {"label": "Firewall-1"}, {"label": "LoadBalancer"}]},
        {"name": "Server Layer", "nodes": [{"label": "Web-Server-1"}, {"label": "Web-Server-2"}, {"label": "App-Server-1"}, {"label": "App-Server-2"}, {"label": "DB-Master"}, {"label": "DB-Slave"}]},
    ]
    connections = [
        {"from": "Core-SW1", "to": "Dist-SW1", "label": "40Gbps", "type": "core_dist"},
        {"from": "Core-SW1", "to": "Dist-SW2", "label": "40Gbps", "type": "core_dist"},
        {"from": "Core-SW2", "to": "Dist-SW2", "label": "40Gbps", "type": "core_dist"},
        {"from": "Core-SW2", "to": "Dist-SW3", "label": "40Gbps", "type": "core_dist"},
        {"from": "Dist-SW1", "to": "Access-SW1", "label": "10Gbps", "type": "dist_access"},
        {"from": "Dist-SW1", "to": "Access-SW2", "label": "10Gbps", "type": "dist_access"},
        {"from": "Dist-SW2", "to": "Access-SW1", "label": "10Gbps", "type": "dist_access"},
        {"from": "Dist-SW2", "to": "Firewall-1", "label": "10Gbps", "type": "dist_access"},
        {"from": "Dist-SW3", "to": "Access-SW2", "label": "10Gbps", "type": "dist_access"},
        {"from": "Dist-SW3", "to": "LoadBalancer", "label": "10Gbps", "type": "dist_access"},
        {"from": "Access-SW1", "to": "Web-Server-1", "label": "1Gbps", "type": "access_srv"},
        {"from": "Access-SW1", "to": "Web-Server-2", "label": "1Gbps", "type": "access_srv"},
        {"from": "Access-SW2", "to": "Web-Server-1", "label": "1Gbps", "type": "access_srv"},
        {"from": "Access-SW2", "to": "Web-Server-2", "label": "1Gbps", "type": "access_srv"},
        {"from": "Firewall-1", "to": "App-Server-1", "label": "1Gbps", "type": "access_srv"},
        {"from": "Firewall-1", "to": "App-Server-2", "label": "1Gbps", "type": "access_srv"},
        {"from": "LoadBalancer", "to": "App-Server-1", "label": "1Gbps", "type": "access_srv"},
        {"from": "LoadBalancer", "to": "App-Server-2", "label": "1Gbps", "type": "access_srv"},
        {"from": "Web-Server-1", "to": "App-Server-1", "label": "API", "type": "redundant"},
        {"from": "Web-Server-2", "to": "App-Server-2", "label": "API", "type": "redundant"},
        {"from": "App-Server-1", "to": "DB-Master", "label": "JDBC", "type": "redundant"},
        {"from": "App-Server-2", "to": "DB-Slave", "label": "JDBC", "type": "redundant"},
        {"from": "DB-Master", "to": "DB-Slave", "label": "Replication", "type": "redundant"},
    ]

    builder = build_network_topology(layers, connections,
                                     title="Data Center Network Topology")
    path = os.path.join(OUTPUT_DIR, "network_datacenter.drawio")
    builder.save(path)
    print(f"✅ network_datacenter.drawio saved")
    return path


# ================================================================
if __name__ == "__main__":
    print("=" * 50)
    print("🔄 重新生成所有图...")
    print("=" * 50)

    p1 = generate_class_diagram()
    print()
    p2 = generate_er_diagram()
    print()
    p3 = generate_mindmap()
    print()
    p4 = generate_network()
    print()
    print("=" * 50)
    print("✅ 全部生成完毕！")
    print(f"  class_diagram_ecommerce.drawio  → {p1}")
    print(f"  er_diagram_education.drawio      → {p2}")
    print(f"  mindmap_ai_stack.drawio          → {p3}")
    print(f"  network_datacenter.drawio        → {p4}")

    # 用 draw.io 打开查看
    try:
        drawio_path = r"C:\Program Files\draw.io\draw.io.exe"
        if os.path.exists(drawio_path):
            import subprocess
            subprocess.Popen([drawio_path, p1])
            subprocess.Popen([drawio_path, p2])
            subprocess.Popen([drawio_path, p3])
            subprocess.Popen([drawio_path, p4])
            print("📂 已在 draw.io 中打开")
    except Exception as e:
        print(f"⚠️ 打开 draw.io 失败: {e}")
