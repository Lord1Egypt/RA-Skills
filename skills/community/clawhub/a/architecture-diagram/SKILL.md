---
name: architecture-diagram
description: AI architecture diagram generator supporting Mermaid charts. Generate system architecture, cloud architecture, neural network, graph theory, flowchart, ER diagram, network topology, or Docker/K8s architecture diagrams. Supports both Mermaid code output and direct image generation via Kroki API (free, no API key required). 生成系统架构、云架构、神经网络、图论、流程图、ER图、网络拓扑、Docker/K8s架构等Mermaid架构图，支持直接生成SVG/PNG图片。
---

# Architecture Diagram / 架构图生成助手

## 功能 / Features

1. **Generate Mermaid code** (copy & paste anywhere)
2. **Direct image generation** via Kroki API (free, no API key!)
3. **Online editor link** for customization

### Supported Types / 支持类型

| 类型 | 关键词 |
|------|--------|
| 🤖 AI/LLM 大模型 | `大模型`, `llm`, `neural`, `transformer` |
| 📊 图论/矩阵 | `图论`, `7x7`, `矩阵`, `graph`, `matrix` |
| ☁️ 云架构 | `云`, `aws`, `cloud`, `azure`, `阿里云` |
| 🌐 网络拓扑 | `网络`, `router`, `network`, `openwrt` |
| 🔀 流程图 | `流程`, `flow`, `flowchart`, `工作流` |
| 📋 ER图 | `er`, `database`, `数据库` |
| 🐳 Docker/K8s | `docker`, `k8s`, `container` |

## Usage / 使用方法

### Command Format / 命令格式

```
生成架构图 <描述>      # 中文
architecture <desc>   # English
```

### Examples / 示例

```
生成架构图 大模型系统架构
architecture cloud aws architecture
生成架构图 神经网络
architecture neural network
```

## Image Generation / 图片生成

Uses **Kroki API** (https://kroki.io) - 100% free, no API key needed!

**IMPORTANT: Use PNG format, NOT SVG!**
- SVG → image conversion (cairosvg/PIL) loses text inside boxes
- Kroki PNG API directly bakes text into the image correctly
- PNG format works perfectly on Telegram, mobile, and desktop

```python
import urllib.request
import base64
import zlib

def generate_diagram_image(mermaid_code: str, output_path: str = "diagram.png"):
    """Generate PNG image from Mermaid code using Kroki API (text intact!)"""
    
    # Encode: zlib compress + base64 URL-safe encode
    compressed = zlib.compress(mermaid_code.encode('utf-8'))
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    # Use PNG format - text renders correctly, no font dependencies
    url = f"https://kroki.io/mermaid/png/{encoded}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    
    return output_path
```

## Mermaid Templates / Mermaid 模板

### 1. AI/LLM Architecture (default)

```mermaid
graph TD
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
    end
```

### 2. Cloud Architecture

```mermaid
graph TD
    User[用户] --> CDN[CDN加速]
    CDN --> LB[负载均衡]
    LB --> Web[Web服务集群]
    Web --> API[API网关]
    API --> Auth[认证服务]
    API --> DB[(数据库)]
    API --> Cache[Redis缓存]
    DB --> Backup[备份存储]
```

### 3. Neural Network

```mermaid
graph TD
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
    end
```

### 4. Network Topology

```mermaid
graph LR
    Internet[互联网] --> FW[防火墙]
    FW --> Router[主路由]
    Router --> AP[无线AP]
    Router --> Switch[交换机]
    Switch --> PC[PC设备]
    Switch --> Server[服务器]
    Router --> IoT[智能设备]
```

### 5. Flowchart

```mermaid
graph TD
    Start[开始] --> Step1[步骤1]
    Step1 --> Step2[步骤2]
    Step2 --> Judge{判断?}
    Judge -->|是| Step3[执行3]
    Judge -->|否| Step4[执行4]
    Step3 & Step4 --> End[结束]
```

### 6. Graph Theory 7×7

```mermaid
graph TD
    A[7×7输入矩阵] --> B[邻接矩阵/邻接表]
    B --> C[图结构构建]
    C --> D[BFS/DFS遍历]
    C --> E[Dijkstra最短路径]
    C --> F[Prim最小生成树]
    D & E & F --> G[图特征输出]
    G --> H[神经网络融合]
```

### 7. Docker/K8s Architecture

```mermaid
graph TD
    User[用户] --> CI[CI/CD流水线]
    CI --> Registry[镜像仓库]
    Registry --> K8s[K8s集群]
    K8s --> Svc1[Service A]
    K8s --> Svc2[Service B]
    K8s --> DB[(数据库)]
    Svc1 --> DB
    Svc2 --> DB
```

## Output Format / 输出格式

When user requests image, generate:

```markdown
🤖 **架构图：{标题}**
━━━━━━━━━━━━━━━━━━━━

![Architecture Diagram](https://kroki.io/mermaid/png/{encoded})

📊 **Mermaid 代码：**
```mermaid
{mermaid_code}
```

🔗 [在线编辑](https://mermaid.live/edit#pako:{encoded})
```

**For Telegram/mobile:** Always use PNG format directly - text is baked in and displays correctly everywhere.

## Smart Detection / 智能识别

```python
def detect_type(input_text):
    text = input_text.lower()
    
    if any(k in text for k in ["大模型", "llm", "神经网络", "neural", "transformer", "ai"]):
        return "ai_llm"
    elif any(k in text for k in ["图论", "7x7", "矩阵", "graph", "matrix"]):
        return "graph_theory"
    elif any(k in text for k in ["云", "aws", "cloud", "azure", "阿里云"]):
        return "cloud"
    elif any(k in text for k in ["网络", "router", "network", "openwrt", "拓扑"]):
        return "network"
    elif any(k in text for k in ["流程", "flow", "flowchart", "工作流"]):
        return "flowchart"
    elif any(k in text for k in ["er", "database", "数据库", "er图"]):
        return "er"
    elif any(k in text for k in ["docker", "k8s", "container", "容器"]):
        return "docker"
    else:
        return "general"
```

## Color Themes / 配色主题

```mermaid
%%{init: {'theme':'base'}}%%
%%{init: {'theme':'dark'}}%%
%%{init: {'theme':'neutral'}}%%
```

Add theme in SKILL.md body for custom styling.

## Notes / 注意事项

- **Always use PNG format** - SVG to image conversion loses text, use Kroki PNG API directly
- **Kroki API** (https://kroki.io) is 100% free, no registration required
- **Online editor** (https://mermaid.live) allows visual customization
- **PNG works everywhere** - Telegram, mobile, desktop - text renders correctly
