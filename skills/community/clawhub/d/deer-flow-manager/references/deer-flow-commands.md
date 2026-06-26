# DeerFlow 2.0 常用命令速查表

## 📦 安装与初始化

| 命令 | 说明 | 场景 |
|------|------|------|
| `make setup` | 交互式安装向导（推荐新手） | 首次安装引导 |
| `make check` | 检查系统依赖是否齐全 | 安装前验证 |
| `make install` | 安装前后端全部依赖 | 手动安装依赖 |
| `make config` | 生成配置文件（需手动编辑） | 高级用户手动配置 |
| `make config-upgrade` | 合并模板新字段到现有配置 | 配置升级 |
| `make doctor` | 检查配置和系统要求 | 诊断问题 |
| `make setup-sandbox` | 预拉取沙箱容器镜像 | Docker 模式准备 |

## 🚀 启动与运行

| 命令 | 说明 | 端口 | 场景 |
|------|------|------|------|
| `make dev` | 开发模式（热重载） | localhost:2026 | 本地开发（推荐） |
| `make dev-pro` | 开发模式 + Gateway | localhost:2026 | 实验特性 |
| `make dev-daemon` | 后台开发模式 | localhost:2026 | 守护进程 |
| `make start` | 生产模式（无热重载） | localhost:2026 | 正式运行 |
| `make start-pro` | 生产模式 + Gateway | localhost:2026 | 实验特性 |
| `make start-daemon` | 后台生产模式 | localhost:2026 | 守护进程 |

## ⏹ 停止与管理

| 命令 | 说明 |
|------|------|
| `make stop` | 停止所有运行中的服务 |
| `make clean` | 停止服务并清理临时文件 |

## 🐳 Docker 模式

| 命令 | 说明 | 场景 |
|------|------|------|
| `make up` | 构建并启动生产 Docker | 生产部署（推荐） |
| `make up-pro` | 生产 Docker + Gateway | 实验特性 |
| `make down` | 停止并移除容器 | 清理 |
| `make docker-init` | 拉取沙箱镜像 | 初始化 |
| `make docker-start` | 启动 Docker 开发 | 开发模式 |
| `make docker-stop` | 停止 Docker 开发 | 停止 |
| `make docker-logs` | 查看 Docker 日志 | 调试 |

## 🔧 常用操作

| 操作 | 命令 |
|------|------|
| **查看帮助** | `make help` |
| **进入目录** | `cd ~/deer-flow` |
| **手动启动** | `./scripts/serve.sh --dev` |
| **手动停止** | `./scripts/serve.sh --stop` |
| **查看日志** | `tail -f ~/deer-flow/logs/langgraph.log` |

## ⚙️ 配置文件位置

| 文件 | 说明 |
|------|------|
| `config.yaml` | 主配置文件（模型、工具、沙箱等） |
| `.env` | 环境变量（API Keys） |
| `logs/` | 运行日志目录 |

## 📋 手动部署步骤（极简版）

### 前置条件

| 依赖 | 要求 |
|------|------|
| Python | ≥3.12 |
| Node.js | ≥22 |
| pnpm | 包管理器 |
| uv | Python包管理 |
| nginx | Web服务器 |
| Git | 版本控制 |

### 部署步骤

```bash
# 1. 克隆仓库
git clone https://github.com/bytedance/deer-flow.git ~/deer-flow
cd ~/deer-flow

# 2. 创建配置文件（从模板复制）
cp .env.example .env
cp config.example.yaml config.yaml

# 3. 编辑 config.yaml，添加模型配置
# （配置 big-pickle：base_url=https://opencode.ai/zen/v1，api_key 留空）

# 4. 安装依赖
make check    # 检查环境
make install  # 安装前后端

# 5. 启动服务
make dev
```

### 卸载步骤

```bash
cd ~/deer-flow

# 1. 停止服务
make stop

# 2. 清理临时文件
make clean

# 3. 删除目录
cd ~ && rm -rf ~/deer-flow
```

### 更新步骤

```bash
cd ~/deer-flow

# 1. 拉取最新代码
git pull origin main

# 2. 合并新配置字段
make config-upgrade

# 3. 重新安装依赖
cd backend && rm -rf .venv && uv sync && cd ..
make install
```

## 🔌 服务端口映射

| 服务 | 端口 | 说明 |
|------|------|------|
| LangGraph | 2024 | Agent 运行时 |
| Gateway | 8001 | REST API |
| Frontend | 3000 | Next.js 前端 |
| Nginx | 2026 | 反向代理（主入口） |

## 🖥️ 多平台支持

### 检测脚本

```bash
# 自动检测操作系统
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
    darwin*)     echo "macOS" ;;
    linux*)     echo "Linux" ;;
    mingw*|nt*) echo "Windows" ;;
    *)          echo "Unknown: $OS" ;;
esac
```

### 路径变量

```bash
# 统一使用 $HOME 或 ~
INSTALL_DIR="$HOME/deer-flow"
CONFIG_FILE="$INSTALL_DIR/config.yaml"
ENV_FILE="$INSTALL_DIR/.env"
LOG_DIR="$INSTALL_DIR/logs"
```

### 常用命令差异

| 操作 | macOS/Linux | Windows (PowerShell) |
|------|-------------|---------------------|
| 查看进程 | `lsof -i :端口` | `netstat -ano | findstr "端口"` |
| 终止进程 | `kill -9 PID` | `taskkill /PID PID` |
| 环境变量 | `echo $VAR` | `$env:VAR` |

> **Windows 用户注意**：推荐使用 WSL2 运行 DeerFlow。在 PowerShell 中安装 WSL：
> ```powershell
> wsl --install -d Ubuntu
> ```
> 安装后进入 WSL Ubuntu 环境，所有命令与 Linux 一致。