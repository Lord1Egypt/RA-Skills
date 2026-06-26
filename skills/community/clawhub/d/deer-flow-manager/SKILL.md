---
name: deer-flow-manager
description: |
  DeerFlow 2.0（字节跳动开源 Deep Research 框架）管理技能。
  用于安装、配置、更新、卸载 DeerFlow 2.0，以及排查启动问题。
  触发词：DeerFlow部署、DeerFlow安装、DeerFlow配置、DeerFlow更新、DeerFlow卸载、DeerFlow启动、deer-flow
---

# DeerFlow 2.0 管理技能

本技能用于管理 DeerFlow 2.0 的完整生命周期：安装、配置、更新、卸载、启动。

## 使用场景

1. 首次安装 DeerFlow 2.0
2. 配置或更换大模型
3. 更新 DeerFlow 到最新版本
4. 卸载 DeerFlow
5. 排查启动问题

---

## 第一步：收集大模型配置信息

在开始安装前，需要向用户收集大模型配置信息。

### 询问用户

> 你好！在安装 DeerFlow 2.0 之前，我需要确认大模型配置。请提供以下信息：

1. **模型来源**：你想使用哪个大模型？
   - OpenCode Zen big-pickle（免费，无需 API Key）
   - OpenAI（GPT-4o, GPT-4o-mini 等）
   - Anthropic（Claude 3.5 Sonnet 等）
   - Google（Gemini 2.5 Pro 等）
   - DeepSeek
   - Ollama（本地模型）
   - 其他 OpenAI 兼容接口

2. **API 信息**（根据选择的模型）：
   - API Key（如需要）
   - API Base URL（如使用第三方接口）
   - 模型名称

### 配置模板

根据用户选择，按以下模板配置 `config.yaml` 中的 models 部分：

#### OpenCode Zen big-pickle（免费）
```yaml
models:
  - name: big-pickle
    display_name: Big Pickle (OpenCode Zen)
    use: langchain_openai:ChatOpenAI
    model: big-pickle
    api_key: ""
    base_url: https://opencode.ai/zen/v1
    request_timeout: 600.0
    max_retries: 2
    max_tokens: 8192
```

#### OpenAI
```yaml
models:
  - name: gpt-4o
    display_name: GPT-4o
    use: langchain_openai:ChatOpenAI
    model: gpt-4o
    api_key: $OPENAI_API_KEY
    request_timeout: 600.0
    max_retries: 2
    max_tokens: 4096
```

#### Claude
```yaml
models:
  - name: claude-3-5-sonnet
    display_name: Claude 3.5 Sonnet
    use: langchain_anthropic:ChatAnthropic
    model: claude-sonnet-4-20250514
    api_key: $ANTHROPIC_API_KEY
    default_request_timeout: 600.0
    max_retries: 2
```

#### Ollama 本地模型
```yaml
models:
  - name: qwen3-local
    display_name: Qwen3 32B (Ollama)
    use: langchain_ollama:ChatOllama
    model: qwen3:32b
    base_url: http://localhost:11434
    num_predict: 8192
    temperature: 0.7
```

---

## 第二步：安装流程

### 1. 检测操作系统

```bash
# 检测操作系统类型
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
echo "Detected OS: $OS"
```

### 2. 环境检测

```bash
echo "=== Node.js ===" && node --version
echo "=== pnpm ===" && pnpm --version
echo "=== uv ===" && uv --version
echo "=== Python ===" && python3 --version
echo "=== nginx ===" && nginx -v
echo "=== Docker ===" && docker --version
echo "=== Git ===" && git --version
echo "=== make ===" && make --version
```

### 3. 依赖安装（按系统）

**macOS:**
```bash
# 安装 Homebrew（如未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装依赖
brew install node pnpm uv python@3.12 nginx git make
```

**Linux (Ubuntu/Debian):**
```bash
# 安装系统依赖
sudo apt update
sudo apt install -y curl git make nginx python3.12 python3-pip

# 安装 Node.js 和 pnpm
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
npm install -g pnpm

# 安装 uv
curl -fsSL https://astral.sh/uv/install.sh | sh
```

**Windows (WSL2 推荐):**
```bash
# 使用 WSL2 或 PowerBox
# 推荐在 WSL2 Ubuntu 环境下安装
wsl --install -d Ubuntu
```

### 4. 安装步骤

```bash
# 1. 确定安装目录
INSTALL_DIR="$HOME/deer-flow"

# 2. 克隆仓库
git clone https://github.com/bytedance/deer-flow.git "$INSTALL_DIR"
cd "$INSTALL_DIR"

# 3. 创建配置文件
cp .env.example .env
cp config.example.yaml config.yaml

# 4. 编辑 config.yaml，添加模型配置
# 使用第一步收集的信息，编辑 config.yaml 中的 models 部分

# 5. 安装依赖
make check
make install
```

### 5. 验证安装

```bash
cd "$INSTALL_DIR"
make doctor
```

### 6. 启动服务

```bash
cd "$INSTALL_DIR"
make dev
```

服务启动后，访问 **http://localhost:2026**。

---

## 第三步：更新流程

```bash
# 确定安装目录
INSTALL_DIR="$HOME/deer-flow"

cd "$INSTALL_DIR"

# 1. 拉取最新代码
git pull origin main

# 2. 合并新配置字段
make config-upgrade

# 3. 重建 venv
cd backend && rm -rf .venv && uv sync && cd ..

# 4. 重新安装依赖
make install
```

---

## 第四步：卸载流程

```bash
# 确定安装目录
INSTALL_DIR="$HOME/deer-flow"

cd "$INSTALL_DIR"

# 1. 停止服务
make stop

# 2. 清理临时文件
make clean

# 3. 删除目录
rm -rf "$INSTALL_DIR"
```

---

## 第五步：常见问题排查

### LangGraph 启动卡住

**问题**：LangGraph 服务启动在 2024 端口等待超时。

**原因**：可能是 venv 路径问题（项目迁移后 shebang 失效）。

**解决**：
```bash
cd "$INSTALL_DIR/backend"
rm -rf .venv
uv sync
cd ..
make dev
```

### 模型连接失败

**问题**：大模型 API 调用失败。

**排查**：
1. 检查 `config.yaml` 中的模型配置是否正确
2. 检查 API Key 是否有效（环境变量或直接填写）
3. 检查 base_url 是否可访问

### 端口被占用

**问题**：2024/8001/3000/2026 端口被占用。

**排查**：
```bash
# Linux/macOS
lsof -i :2024
lsof -i :2026

# Windows
netstat -ano | findstr "2024"
```

**解决**：停止占用进程或修改 `config.yaml` 中的端口配置。

---

## 输出常用命令表格

在完成安装或更新后，向用户输出以下常用命令表格：

---

### 🦌 DeerFlow 2.0 常用命令速查表

#### 📦 安装与初始化

| 命令 | 说明 | 场景 |
|------|------|------|
| `make setup` | 交互式安装向导（推荐新手） | 首次安装引导 |
| `make check` | 检查系统依赖是否齐全 | 安装前验证 |
| `make install` | 安装前后端全部依赖 | 手动安装依赖 |
| `make config` | 生成配置文件（需手动编辑） | 高级用户手动配置 |
| `make config-upgrade` | 合并模板新字段到现有配置 | 配置升级 |
| `make doctor` | 检查配置和系统要求 | 诊断问题 |
| `make setup-sandbox` | 预拉取沙箱容器镜像 | Docker 模式准备 |

#### 🚀 启动与运行

| 命令 | 说明 | 端口 | 场景 |
|------|------|------|------|
| `make dev` | 开发模式（热重载） | localhost:2026 | 本地开发（推荐） |
| `make dev-pro` | 开发模式 + Gateway | localhost:2026 | 实验特性 |
| `make dev-daemon` | 后台开发模式 | localhost:2026 | 守护进程 |
| `make start` | 生产模式（无热重载） | localhost:2026 | 正式运行 |
| `make start-pro` | 生产模式 + Gateway | localhost:2026 | 实验特性 |
| `make start-daemon` | 后台生产模式 | localhost:2026 | 守护进程 |

#### ⏹ 停止与管理

| 命令 | 说明 |
|------|------|
| `make stop` | 停止所有运行中的服务 |
| `make clean` | 停止服务��清理临时文件 |

#### 🐳 Docker 模式

| 命令 | 说明 | 场景 |
|------|------|------|
| `make up` | 构建并启动生产 Docker | 生产部署（推荐） |
| `make up-pro` | 生产 Docker + Gateway | 实验特性 |
| `make down` | 停止并移除容器 | 清理 |

#### ⚙️ 配置文件位置

| 文件 | 说明 |
|------|------|
| `config.yaml` | 主配置文件（模型、工具、沙箱等） |
| `.env` | 环境变量（API Keys） |
| `logs/` | 运行日志目录 |

#### 🔌 服务端口映射

| 服务 | 端口 | 说明 |
|------|------|------|
| LangGraph | 2024 | Agent 运行时 |
| Gateway | 8001 | REST API |
| Frontend | 3000 | Next.js 前端 |
| Nginx | 2026 | 反向代理（主入口） |

---

### 快速启动

```bash
cd ~/deer-flow && make dev
```

访问 **http://localhost:2026** 即可使用 DeerFlow 2.0。

---

## 文件位置（动态获取）

- **安装目录**：`~/deer-flow/`
- **配置文件**：`~/deer-flow/config.yaml`
- **环境变量**：`~/deer-flow/.env`
- **日志目录**：`~/deer-flow/logs/`

详细命令参考见 `references/deer-flow-commands.md`。