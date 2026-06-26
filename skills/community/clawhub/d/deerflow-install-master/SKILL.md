---
name: deerflow-install
description: |
  DeerFlow 2.0 一键安装与配置技能。基于真实部署经验（2026-03-29），涵盖从下载仓库到成功运行的全流程，包括踩坑规避方案。
  Use when: (1) 需要在 OpenClaw 环境安装 DeerFlow 2.0, (2) 需要快速排查安装问题, (3) 需要了解 DeerFlow 的最佳实践。
author: 小飞侠 (基于 DeerFlow 部署经验)
homepage: https://github.com/bytedance/deer-flow
source: https://github.com/bytedance/deer-flow
version: "1.0.0"
---

# DeerFlow 安装技能

快速、可靠地在 OpenClaw 环境中安装和配置 DeerFlow 2.0 Super Agent。

## 快速开始

```bash
# 直接调用技能（示例）
skill: deerflow-install
参数: environment=openclaw, model=step-3.5-flash, proxy=http://your-proxy:port
```

或通过自然语言：
- "安装 DeerFlow"
- "部署 DeerFlow 2.0"
- "配置 DeerFlow 环境"

## 安装流程概览

1. **环境检查** → 验证 Docker/Python、端口占用、权限
2. **仓库获取** → 克隆 deer-flow 仓库或下载最新 release
3. **依赖安装** → 根据环境选择 Docker 模式或本地模式
4. **配置写入** → 设置 API Keys、模型、工具
5. **服务启动** → 启动 LangGraph + Gateway
6. **功能测试** → 验证聊天、搜索、文件操作
7. **文档输出** → 生成安装报告和故障排查指南

## 详细步骤

### 阶段 1：环境检查

```bash
# 检查 Python 版本（推荐 3.12+，3.11 需要补丁）
python3 --version  # 应 >= 3.11

# 检查 Docker 权限（Docker 模式需要）
groups $USER | grep docker  # 应在 docker 组

# 检查端口占用
netstat -tlnp | grep -E "2024|8091"
```

**常见问题**：
- ❌ Python 3.11 会触发 PEP 695 语法错误 → 应用补丁（见阶段 2）
- ❌ Docker permission denied → 将用户加入 docker 组：`sudo usermod -aG docker $USER`

### 阶段 2：获取 DeerFlow 仓库

```bash
cd /vol1/@apphome/trim.openclaw/data/workspace
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
```

如果网络慢，可以使用镜像或代理。

### 阶段 3：选择安装模式

#### 模式 A：Docker 模式（推荐）

```bash
make docker-init   # 首次拉取 sandbox 镜像
make docker-start  # 启动所有服务
```

**优点**：环境隔离，无 Python 版本问题。

#### 模式 B：本地 Python 模式（3.12+ 或 3.11+ 补丁）

如果使用 Python 3.11，**必须应用以下补丁**：

```bash
# 1. 修复 typing.override 和 TypedDict 导入
find backend/packages/harness/deerflow -name "*.py" -exec \
  sed -i 's/from typing import override/from typing_extensions import override/' {} \;
find backend/packages/harness/deerflow -name "*.py" -exec \
  sed -i 's/from typing import TypedDict/from typing_extensions import TypedDict/' {} \;

# 2. 修复 PEP 695 函数泛型（如果有）
# 手动修改 deerflow/reflection/resolvers.py 第 75 行：
# def resolve_variable[T] → def resolve_variable(T)
```

然后创建虚拟环境并安装依赖：

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # 或直接使用 .venv/bin/pip
pip install -U pip
pip install fastapi uvicorn httpx langchain langchain-openai \
  langgraph-cli[inmem] langgraph-checkpoint-sqlite tavily-python
```

### 阶段 4：配置文件设置

**1. 环境变量文件**（`.env`）：

```env
OPENROUTER_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
INFOQUEST_API_KEY=your-key-here  # 可选备用
```

**2. 模型配置**（`config.yaml`）：

确保模型 ID 正确：
```yaml
models:
  - name: step-3.5-flash
    model: stepfun/step-3.5-flash:free  # OpenRouter 免费模型
    api_key: $OPENROUTER_API_KEY
    base_url: https://openrouter.ai/api/v1
```

**3. 工具配置**（默认启用）：

```yaml
tools:
  - name: web_search
    use: deerflow.community.tavily.tools:web_search_tool
    api_key: $TAVILY_API_KEY
  - name: ls
    use: deerflow.sandbox.tools:ls_tool
  - name: read_file
    use: deerflow.sandbox.tools:read_file_tool
  - name: write_file
    use: deerflow.sandbox.tools:write_file_tool
  - name: str_replace
    use: deerflow.sandbox.tools:str_replace_tool
  - name: bash
    use: deerflow.sandbox.tools:bash_tool
```

### 阶段 5：启动服务

**LangGraph Server**（端口 2024）：

```bash
cd backend
export DEER_FLOW_CONFIG_PATH=../config.yaml
export PYTHONPATH=$(pwd):.

# 允许阻塞调用（Python 3.11 必需）
nohup .venv/bin/langgraph dev \
  --port 2024 \
  --no-browser \
  --no-reload \
  --allow-blocking \
  > /tmp/langgraph.log 2>&1 &
```

**Gateway Lite**（端口 8091）：

```bash
nohup .venv/bin/python gateway_lite.py > /tmp/gateway.log 2>&1 &
```

验证：
```bash
curl http://localhost:2024/openapi.json  # 应返回 JSON
curl http://localhost:8091/health       # 应返回 {"status":"healthy"}
```

### 阶段 6：创建 OpenClaw 集成技能

**1. 创建技能目录**：

```bash
mkdir -p ./skills/deerflow/scripts
```

**2. 编写客户端脚本**（`scripts/deerflow_client.py`）：

包含以下功能：
- `chat(message)` → 调用 Gateway /api/chat
- `list_models()` → 调用 /api/models
- `list_skills()` → 调用 /api/skills

**3. 注册技能**：

创建 `_meta.json` 和 `SKILL.md`，描述能力、触发词、使用示例。

**4. 测试**：

```bash
python3 skills/deerflow/scripts/deerflow_client.py "你好"
```

---

## 踩坑记录与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `from typing import override` 错误 | Python 3.11 不支持 3.12+ 特性 | 批量替换为 `typing_extensions.override` |
| `def foo[T]` 语法错误 | PEP 695 函数泛型（3.12+） | 移除泛型或使用 TypeVar |
| `TypedDict` 导入失败 | 3.11 需从 `typing_extensions` 导入 | 替换导入源 |
| `BlockingError: os.getcwd()` | blockbuster 检测同步阻塞 | 使用 `--allow-blocking` 并设置 `DEER_FLOW_CONFIG_PATH` |
| `/runs/wait` 返回空 | 消息在顶层 `messages` 而非 `values` | 从 `wait_data.get("messages")` 提取 |
| `GRAPH_RECURSION_LIMIT` 错误 | 默认递归 25，深度任务超限 | 调用时设置 `config.recursion_limit=200+` |
| web_search 报错"技术问题" | Tavily API 配额耗尽 | 切换 InfoQuest 或检查配额 |
| 文件操作"无法访问" | Sandbox 权限/路径问题 | 使用 `/tmp` 测试，调整 sandbox 配置 |

---

## 最佳实践建议

1. **优先 Docker**：如果 Docker 可用，是最稳定的方案
2. **设置 recursion_limit**：复杂任务必须 >=100，建议 200+
3. **监控日志**：关注 `/tmp/langgraph*.log` 和 `/tmp/gateway*.log`
4. **API 配额管理**：Tavily 免费额度有限，InfoQuest 作为备用
5. **服务保活**：使用 `nohup` 或 `systemd`，创建 `start_all.sh` 一键脚本
6. **测试顺序**：简单聊天 → 列出模型/技能 → 深度任务

---

## 故障排查清单

- [ ] Python 版本 >= 3.11？3.12 最佳
- [ ] Docker 组权限（如使用 Docker）
- [ ] 端口 2024 (LangGraph) 和 8091 (Gateway) 未被占用
- [ ] 环境变量：`OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `DEER_FLOW_CONFIG_PATH`
- [ ] 启动参数包含 `--allow-blocking`
- [ ] `config.yaml` 中 model 格式正确（`stepfun/step-3.5-flash:free`）
- [ ] Gateway 提取 `messages` 而非 `values`
- [ ] 调用时传入 `recursion_limit>=100`

---

## 一键启动脚本示例

```bash
#!/bin/bash
# start_all.sh
cd /vol1/@apphome/trim.openclaw/data/workspace/deer-flow/backend
export DEER_FLOW_CONFIG_PATH=../config.yaml
export PYTHONPATH=$(pwd):.

# 启动 LangGraph
nohup .venv/bin/langgraph dev --port 2024 --no-browser --no-reload --allow-blocking &
sleep 5

# 启动 Gateway
nohup .venv/bin/python gateway_lite.py &
sleep 2

echo "DeerFlow 已启动：http://localhost:8091"
```

---

## 版本信息

- **DeerFlow 版本**：2.0 (截至 2026-03-29)
- **模型**：OpenRouter Step-3.5 Flash (免费)
- **安装耗时**：Docker 模式 ~5分钟；本地模式 ~30分钟
- **测试状态**：✅ 生产可用（递归限制、消息提取、API 调用均已验证）

---

**最后更新**：2026年3月29日  
**维护者**：OpenClaw Agent (小飞侠)
