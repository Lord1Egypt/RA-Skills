#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Feishu Response with Mermaid Diagram
Complete example of Axiang response with architecture diagram
"""

import sys
import os
sys.path.insert(0, 'scripts')

from mermaid-generator import MermaidGenerator

print("=" * 70)
print("Demo: Feishu Response with Mermaid Diagram")
print("=" * 70)

# Create generator
generator = MermaidGenerator()

# Define architecture diagram
mermaid_code = """
graph TB
    subgraph 用户层
        A[用户提问]
        F[用户收到回复]
    end
    
    subgraph OpenClaw
        B[阿香 AI]
        C[记忆检索钩子]
        D[提示词增强]
        E[LLM 生成回复]
    end
    
    subgraph 数据层
        G[阿里云 Embedding API]
        H[(Chroma 向量库)]
        I[记忆文件 memory/*.md]
    end
    
    A --> B
    B --> C
    C --> G
    C --> H
    H --> I
    B --> D
    D --> E
    E --> F
    
    style A fill:#e1f5ff
    style F fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#fff4e1
    style D fill:#fff4e1
    style E fill:#fff4e1
    style G fill:#f0f8e1
    style H fill:#f0f8e1
    style I fill:#f0f8e1
"""

print("\n[1] Generating Architecture Diagram...")
diagram_path = generator.generate(
    mermaid_code, 
    filename="axiang-architecture",
    width=1000,
    height=800
)

if diagram_path:
    print(f"[OK] Diagram generated: {diagram_path}")
    print(f"[OK] Size: {diagram_path.stat().st_size / 1024:.1f} KB")
else:
    print("[FAIL] Diagram generation failed")
    sys.exit(1)

# Prepare Feishu response
print("\n[2] Preparing Feishu Response...")

response_text = """
## 🦞 阿香记忆增强系统架构

你好呀！香香给你介绍一下现在的系统架构～✨

### 📊 架构图

系统分为三层：用户层、OpenClaw 层、数据层

### 🔍 工作流程

1. **用户提问** → 阿香收到消息
2. **记忆检索钩子** → 自动检索相关记忆
3. **阿里云 Embedding** → 生成查询向量
4. **Chroma 向量库** → 搜索相似记忆
5. **提示词增强** → 注入记忆上下文
6. **LLM 生成回复** → 基于记忆回答问题
7. **用户收到回复** → 带上下文的智能回答

### 💡 核心优势

- ✅ **语义搜索** - 不是关键词匹配，是理解语义
- ✅ **跨会话记忆** - 昨天的对话今天还记得
- ✅ **自动检索** - 回复前自动找相关记忆
- ✅ **智能增强** - 有记忆就引用，没有就自然回复

### 📈 性能指标

| 指标 | 数值 |
|------|------|
| 向量化文件 | 24 个 |
| 向量数量 | 527 个 |
| 向量维度 | 1024 维 |
| 搜索延迟 | < 500ms |
| 每月成本 | < 1 元 |

---

_架构图已生成，稍后发送图片版～_ 🦞✨
"""

print(f"[OK] Response text prepared ({len(response_text)} chars)")

# Save response to file
response_file = "C:/Users/Xiabi/.openclaw/workspace/mermaid-output/demo-response.txt"
with open(response_file, 'w', encoding='utf-8') as f:
    f.write(response_text)

print(f"[OK] Response saved to: {response_file}")

# Show how to send to Feishu
print("\n[3] How to Send to Feishu:")
print("=" * 70)
print("""
# Step 1: Send text response
message --action send --channel feishu --message "上面的回复文本"

# Step 2: Send architecture diagram
message --action send --channel feishu --filePath "C:\\Users\\Xiabi\\.openclaw\\workspace\\mermaid-output\\axiang-architecture.png"

# Or use Python:
from message_tool import send_message
send_message(channel="feishu", text=response_text)
send_message(channel="feishu", file_path=str(diagram_path))
""")
print("=" * 70)

print("\n" + "=" * 70)
print("Demo Complete!")
print("=" * 70)
print("\nGenerated Files:")
print(f"  1. Diagram: {diagram_path}")
print(f"  2. Response: {response_file}")
print("\nNext Step: Send to Feishu and test!")
print("=" * 70)
