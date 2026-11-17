# CodeRisk Agent — 天禧 Skill 开发者说明

> 本文档面向天禧平台审核人员和 Skill 开发者，提供一键跑通的安装调试指南。

---

## 一、环境要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| Python | 3.10+ | 3.11+ |
| 操作系统 | Linux / macOS / Windows | Linux (Ubuntu 22.04+) |
| 内存 | 4GB RAM | 8GB+ |
| 磁盘 | 2GB 空闲 | 5GB+（含 CVE 数据库） |
| GPU | 可选 | AMD ROCm + 20GB+ VRAM（本地模式） |

---

## 二、脚本文件清单

| 文件路径 | 说明 |
|----------|------|
| `skill/mcp-server/server.py` | MCP 服务器入口脚本，提供 `coderisk_scan_code` 和 `coderisk_lookup_cve` 两个 Tool |
| `skill/mcp-server/requirements.txt` | MCP 服务器 Python 依赖清单 |

---

## 三、依赖安装

```bash
# 1. 进入 Skill 包目录
cd skill/

# 2. 安装 MCP Server 依赖
pip install -r mcp-server/requirements.txt

# 3. 核心代码（core/、agents/）已包含在 Skill 包内，无需额外安装
```

---

## 四、MCP 服务自动注册

```bash
# 注册到 OpenClaw MCP 管理器
openclaw mcp set code-risk \
    --command python3 \
    --args "./skill/mcp-server/server.py"

# 验证注册成功
openclaw mcp list
# 应看到: code-risk  [active]
```

---

## 五、本地测试启动步骤

### 5.1 配置 LLM（必须，否则语义分析不启用）

选择以下任一方案：

**方案 A：OpenAI（推荐，开箱即用）**
```bash
export CODERISK_LLM_BACKEND=openai
export CODERISK_API_KEY=sk-your-key-here
export CODERISK_MODEL=gpt-4o
```

**方案 B：DeepSeek（国内可用）**
```bash
export CODERISK_API_KEY=sk-your-key-here
export CODERISK_LLM_BACKEND=deepseek
export CODERISK_MODEL=deepseek-coder
```

**方案 C：本地 GPU（完全离线）**
```bash
export CODERISK_LLM_BACKEND=local
export CODERISK_LOCAL_MODEL_PATH=/path/to/qwen2.5-coder-32b-instruct-q4_k_m.gguf
# 需要 llama-cpp-python 和 ROCm 环境
```

### 5.2 准备测试代码

```bash
mkdir -p /tmp/test-project
cat > /tmp/test-project/vuln.c << 'EOF'
#include <stdio.h>
#include <string.h>

void unsafe_copy(char *input) {
    char buf[16];
    strcpy(buf, input);  // CWE-120: Buffer Overflow
}

int main() {
    char *user_input = "A" * 100;
    unsafe_copy(user_input);
    return 0;
}
EOF
```

### 5.3 启动 MCP Server（stdio 模式，推荐）

```bash
python3 skill/mcp-server/server.py
```

Server 启动后等待 stdio 输入，无报错即正常。

### 5.4 SSE 模式（仅供本地调试）

```bash
# 必须设置 SSE API Key（强随机字符串）
export CODERISK_SSE_API_KEY="your-strong-random-key-here"

# 启动 SSE（强制绑定 127.0.0.1，拒绝任何其他地址）
python3 skill/mcp-server/server.py --sse --host 127.0.0.1 --port 8080
```

**⚠️ SSE 安全限制**：
- 强制绑定 `127.0.0.1`，`--host` 传其他地址会被拒绝启动
- 必须配置 `CODERISK_SSE_API_KEY`，否则拒绝启动
- 所有 SSE 请求必须在 Header 中携带 `Authorization: Bearer <key>`
- Starlette 运行在生产模式（`debug=False`）
- **生产环境请使用 stdio 模式**

### 5.5 使用 OpenClaw 客户端测试

```bash
# 调用扫描工具
openclaw tool call coderisk_scan_code \
    --target_path /tmp/test-project \
    --output_format json \
    --enable_ai true

# 单独测试 CVE 查询
openclaw tool call coderisk_lookup_cve \
    --cwe_id CWE-120 \
    --max_results 5
```

### 5.6 预期输出

`coderisk_scan_code` 应返回 JSON 格式的扫描报告，包含：
- `files_analyzed`: 分析的文件数
- `risks`: 风险列表（含 CWE、严重级别、修复建议）
- `risk_breakdown`: Critical/High/Medium/Low/Info 分布统计

---

## 六、打包与校验

```bash
# 生成 .skp 安装包
skill pack skill/
# 输出: code-risk-agent-1.0.0.skp

# 官方校验
skill validate code-risk-agent-1.0.0.skp
# 无报错 = 包完全合规

# 本地模拟器安装测试
openclaw skill install code-risk-agent-1.0.0.skp
```

---

## 七、隐私合规声明

本 Skill 的隐私策略如下：

| 功能 | 执行位置 | 是否上传代码 |
|------|---------|-------------|
| 静态分析（27 条规则） | 本地 | 否 |
| Taint 数据流追踪 | 本地 | 否 |
| CVE 数据库查询 | 本地 SQLite | 否 |
| 依赖漏洞扫描 | 本地 | 否 |
| AI 语义分析 | 用户配置的 LLM API | 是（可切换本地） |
| 报告生成 | 本地 | 否 |

- **静态分析、Taint 追踪、CVE 查询、依赖扫描完全在本地执行，不上传任何代码**
- **AI 语义分析默认调用用户配置的云端 LLM API**，代码内容会发送至用户指定的 API 提供商（OpenAI / Anthropic / DeepSeek 等）
- 用户可通过设置 `CODERISK_LLM_BACKEND=local` 切换为**完全本地推理**，此时零外部网络调用
- 无遥测、无数据收集、无用户行为追踪

---

## 八、常见问题

| 问题 | 解决 |
|------|------|
| `mcp SDK not installed` | 执行 `pip install mcp>=1.0.0` |
| `LLM init failed` | 检查 API Key 和环境变量配置 |
| `No supported files found` | 确认目标路径包含 `.c`、`.h` 或 `.py` 文件 |
| `Semgrep skipped` | Semgrep 为可选依赖，不影响核心功能 |
| CVE 数据库为空 | CVE 查询功能不可用，不影响静态分析核心功能 |
| SSE 启动被拒绝 | 检查是否设置了 `CODERISK_SSE_API_KEY`，且 `--host` 必须为 `127.0.0.1` |

---

## 九、目录结构

```
code-risk-agent/
├── main.py                  # 原项目 CLI 入口
├── orchestrator.py          # 原项目四层流水线
├── agents/                  # 原项目 Agent 实现
├── core/                    # 原项目核心模块

├── skill/                   # 天禧 Skill 包（本目录）
│   ├── README_CN.md         # 本文件
│   ├── SKILL.md             # AI 导演脚本
│   ├── package.json         # Skill 元数据
│   ├── skill-card.md        # 市场展示卡片
│   ├── _meta.json           # ClawHub 发布元数据
│   └── mcp-server/
│       ├── server.py          # MCP 服务器入口
│       └── requirements.txt   # 依赖清单
└── pyproject.toml
```

---

**作者**: a9320 (Yang Weike)  
**License**: MIT  
**版本**: 1.0.0  
**天禧生态**: 苍穹共创计划
