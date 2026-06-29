"""
generate_network_topology.py — 生成数据中心网络拓扑图
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from build_network import build_network_topology

# ================================================================
# 数据中心网络拓扑数据
# ================================================================

layers = [
    {
        "name": "Core Layer",
        "nodes": [{"label": "Core-SW1"}, {"label": "Core-SW2"}],
    },
    {
        "name": "Distribution Layer",
        "nodes": [
            {"label": "Dist-SW1"},
            {"label": "Dist-SW2"},
            {"label": "Dist-SW3"},
        ],
    },
    {
        "name": "Access Layer",
        "nodes": [
            {"label": "Access-SW1"},
            {"label": "Access-SW2"},
            {"label": "Firewall-1"},
            {"label": "LoadBalancer"},
        ],
    },
    {
        "name": "Server Layer",
        "nodes": [
            {"label": "Web-Server-1"},
            {"label": "Web-Server-2"},
            {"label": "App-Server-1"},
            {"label": "App-Server-2"},
            {"label": "DB-Master"},
            {"label": "DB-Slave"},
        ],
    },
]

# 连接定义：每条连接指定类型（决定颜色）
connections = [
    # === Core → Distribution (蓝色) ===
    {"from": "Core-SW1", "to": "Dist-SW1", "label": "40Gbps", "type": "core_dist"},
    {"from": "Core-SW1", "to": "Dist-SW2", "label": "40Gbps", "type": "core_dist"},
    {"from": "Core-SW2", "to": "Dist-SW2", "label": "40Gbps", "type": "core_dist"},
    {"from": "Core-SW2", "to": "Dist-SW3", "label": "40Gbps", "type": "core_dist"},

    # === Distribution → Access (绿色) ===
    {"from": "Dist-SW1", "to": "Access-SW1", "label": "10Gbps", "type": "dist_access"},
    {"from": "Dist-SW1", "to": "Access-SW2", "label": "10Gbps", "type": "dist_access"},
    {"from": "Dist-SW2", "to": "Access-SW1", "label": "10Gbps", "type": "dist_access"},
    {"from": "Dist-SW2", "to": "Firewall-1", "label": "10Gbps", "type": "dist_access"},
    {"from": "Dist-SW3", "to": "Access-SW2", "label": "10Gbps", "type": "dist_access"},
    {"from": "Dist-SW3", "to": "LoadBalancer", "label": "10Gbps", "type": "dist_access"},

    # === Access/FW/LB → Server (深蓝) ===
    {"from": "Access-SW1", "to": "Web-Server-1", "label": "1Gbps", "type": "access_srv"},
    {"from": "Access-SW1", "to": "Web-Server-2", "label": "1Gbps", "type": "access_srv"},
    {"from": "Access-SW2", "to": "Web-Server-1", "label": "1Gbps", "type": "access_srv"},
    {"from": "Access-SW2", "to": "Web-Server-2", "label": "1Gbps", "type": "access_srv"},
    {"from": "Firewall-1", "to": "App-Server-1", "label": "1Gbps", "type": "access_srv"},
    {"from": "Firewall-1", "to": "App-Server-2", "label": "1Gbps", "type": "access_srv"},
    {"from": "LoadBalancer", "to": "App-Server-1", "label": "1Gbps", "type": "access_srv"},
    {"from": "LoadBalancer", "to": "App-Server-2", "label": "1Gbps", "type": "access_srv"},

    # === Server → Server (红色 - 内部通信) ===
    {"from": "Web-Server-1", "to": "App-Server-1", "label": "API", "type": "redundant"},
    {"from": "Web-Server-2", "to": "App-Server-2", "label": "API", "type": "redundant"},
    {"from": "App-Server-1", "to": "DB-Master", "label": "JDBC", "type": "redundant"},
    {"from": "App-Server-2", "to": "DB-Slave", "label": "JDBC", "type": "redundant"},

    # === 冗余链路 (红色) ===
    {"from": "DB-Master", "to": "DB-Slave", "label": "Replication", "type": "redundant"},
]


# ================================================================
# 生成
# ================================================================
output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "network_datacenter.drawio")

builder = build_network_topology(layers, connections,
                                 title="Data Center Network Topology")
builder.save(output_path)
print(f"✅ Generated: {output_path}")

# 尝试用 draw.io 打开
try:
    drawio_path = r"C:\Program Files\draw.io\draw.io.exe"
    if os.path.exists(drawio_path):
        import subprocess
        subprocess.Popen([drawio_path, output_path])
        print("📂 Opened in draw.io")
except Exception as e:
    print(f"⚠️  Could not open draw.io: {e}")
