#!/usr/bin/env python3
"""
Architecture Diagram Image Generator
Uses Kroki API (https://kroki.io) - 100% FREE, no API key required!

Usage:
    python generate_diagram.py "大模型架构" --output diagram.png
    python generate_diagram.py "cloud aws" --output cloud.png --type cloud
"""

import urllib.request
import urllib.parse
import base64
import zlib
import sys
import argparse
import os

def encode_mermaid(mermaid_code: str) -> str:
    """Encode mermaid code for Kroki URL"""
    # Remove markdown code blocks if present
    mermaid_code = mermaid_code.strip()
    if mermaid_code.startswith("```mermaid"):
        mermaid_code = mermaid_code[10:]
    if mermaid_code.startswith("```"):
        mermaid_code = mermaid_code[3:]
    if mermaid_code.endswith("```"):
        mermaid_code = mermaid_code[:-3]
    mermaid_code = mermaid_code.strip()
    
    # Compress using zlib, then use URL-safe base64
    compressed = zlib.compress(mermaid_code.encode('utf-8'))
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    return encoded

def generate_image(mermaid_code: str, output_path: str = "diagram.png", 
                   diagram_type: str = "mermaid", output_format: str = "svg"):
    """Generate diagram image using Kroki API"""
    
    encoded = encode_mermaid(mermaid_code)
    url = f"https://kroki.io/{diagram_type}/{output_format}/{encoded}"
    
    print(f"📥 Downloading from: {url[:80]}...")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read()
        
        # Auto-detect format from content if response is SVG
        if output_format == "svg" or output_path.endswith('.svg'):
            if not output_path.endswith('.svg'):
                output_path = output_path.replace('.png', '.svg')
        
        with open(output_path, 'wb') as f:
            f.write(content)
    
    print(f"✅ Saved to: {output_path} ({len(content)} bytes)")
    return output_path

# ===================== Mermaid Templates =====================

TEMPLATES = {
    "ai_llm": """graph TD
    A[用户输入] --> B[Tokenizer 编码]
    B --> C[Embedding 层]
    C --> D[Transformer Layer × N]
    D --> E[LM Head 输出]
    E --> F[生成回答]
    
    subgraph 模型核心
    C
    D
    E
    end
    
    subgraph 推理引擎
    B
    F
    end""",
    
    "cloud": """graph TD
    User[用户] --> CDN[CDN加速]
    CDN --> LB[负载均衡]
    LB --> Web[Web服务集群]
    Web --> API[API网关]
    API --> Auth[认证服务]
    API --> DB[(数据库)]
    API --> Cache[Redis缓存]
    DB --> Backup[备份存储]""",
    
    "neural": """graph TD
    Input[输入层] --> H1[隐藏层1]
    H1 --> H2[隐藏层2]
    H2 --> H3[隐藏层3]
    H3 --> Output[输出层]
    
    subgraph 层 / Layers
    Input
    H1
    H2
    H3
    Output
    end""",
    
    "network": """graph LR
    Internet[互联网] --> FW[防火墙]
    FW --> Router[主路由]
    Router --> AP[无线AP]
    Router --> Switch[交换机]
    Switch --> PC[PC设备]
    Switch --> Server[服务器]
    Router --> IoT[智能设备]""",
    
    "flowchart": """graph TD
    Start[开始] --> Step1[步骤1]
    Step1 --> Step2[步骤2]
    Step2 --> Judge{判断?}
    Judge -->|是| Step3[执行3]
    Judge -->|否| Step4[执行4]
    Step3 & Step4 --> End[结束]""",
    
    "graph_theory": """graph TD
    A[7×7输入矩阵] --> B[邻接矩阵/邻接表]
    B --> C[图结构构建]
    C --> D[BFS/DFS遍历]
    C --> E[Dijkstra最短路径]
    C --> F[Prim最小生成树]
    D & E & F --> G[图特征输出]
    G --> H[神经网络融合]""",
    
    "docker": """graph TD
    User[用户] --> CI[CI/CD流水线]
    CI --> Registry[镜像仓库]
    Registry --> K8s[K8s集群]
    K8s --> Svc1[Service A]
    K8s --> Svc2[Service B]
    K8s --> DB[(数据库)]
    Svc1 --> DB
    Svc2 --> DB""",
    
    "general": """graph TD
    Input[数据输入] --> Process[处理模块]
    Process --> Logic[业务逻辑]
    Logic --> Store[存储]
    Logic --> Output[结果输出]"""
}

def detect_type(text: str) -> str:
    """Detect diagram type from text"""
    text_lower = text.lower()
    
    if any(k in text_lower for k in ["大模型", "llm", "神经网络", "neural", "transformer", "ai"]):
        return "ai_llm"
    elif any(k in text_lower for k in ["图论", "7x7", "矩阵", "graph", "matrix"]):
        return "graph_theory"
    elif any(k in text_lower for k in ["云", "aws", "cloud", "azure", "阿里云"]):
        return "cloud"
    elif any(k in text_lower for k in ["网络", "router", "network", "openwrt", "拓扑"]):
        return "network"
    elif any(k in text_lower for k in ["流程", "flow", "flowchart", "工作流"]):
        return "flowchart"
    elif any(k in text_lower for k in ["er", "database", "数据库", "er图"]):
        return "graph_theory"  # reuse for ER
    elif any(k in text_lower for k in ["docker", "k8s", "container", "容器"]):
        return "docker"
    else:
        return "general"

def main():
    parser = argparse.ArgumentParser(description='Generate architecture diagrams using Kroki API')
    parser.add_argument('description', nargs='?', default='通用系统架构', help='Diagram description')
    parser.add_argument('--output', '-o', default='diagram.png', help='Output file path')
    parser.add_argument('--type', '-t', choices=list(TEMPLATES.keys()), help='Force diagram type')
    parser.add_argument('--format', '-f', default='png', choices=['png', 'svg', 'pdf'], help='Output format')
    parser.add_argument('--code', help='Output mermaid code to file')
    
    args = parser.parse_args()
    
    # Detect type
    diagram_type = args.type or detect_type(args.description)
    mermaid_code = TEMPLATES[diagram_type]
    
    print(f"🎨 Detected type: {diagram_type}")
    print(f"📝 Mermaid code:\n{mermaid_code}\n")
    
    # Generate image
    output_path = args.output
    generate_image(mermaid_code, output_path, output_format=args.format)
    
    # Optionally save mermaid code
    if args.code:
        with open(args.code, 'w') as f:
            f.write(mermaid_code)
        print(f"💾 Mermaid code saved to: {args.code}")
    
    # Generate URLs
    encoded = encode_mermaid(mermaid_code)
    print(f"\n🔗 Online viewer: https://mermaid.live/edit#pako:{encoded}")

if __name__ == "__main__":
    main()
