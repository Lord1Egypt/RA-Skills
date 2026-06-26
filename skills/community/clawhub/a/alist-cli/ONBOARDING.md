# AList CLI Onboarding

> 本文档指导 AI Agent 完成首次环境配置。按顺序执行，遇到问题时参考 Troubleshooting。

## Prerequisites | 前置条件

- Python 3.x（容器通常自带，运行 `python3 --version` 确认）
- 网络可访问目标 AList 服务器

## Step 1: 检查 Python 环境

```bash
python3 --version
```

如果不存在，尝试：
```bash
python --version
# 或
which python3 || which python
```

如果完全没有 Python，告知用户需要安装 Python 3。

## Step 2: 安装依赖

检查 `requests` 是否可用：
```bash
python3 -c "import requests" 2>/dev/null && echo "OK" || echo "NEED_INSTALL"
```

如果需要安装，按顺序尝试：

```bash
# 尝试 1: uv（最快）
uv pip install --system requests 2>/dev/null && echo "OK"

# 尝试 2: pip
pip3 install requests 2>/dev/null && echo "OK"

# 尝试 3: sudo pip（PEP 668 限制时）
sudo pip3 install --break-system-packages requests 2>/dev/null && echo "OK"

# 尝试 4: venv（隔离环境，不会污染系统）
SKILL_DIR="<skill_dir>"
cd "$SKILL_DIR" && uv venv .venv && .venv/bin/pip install requests
# 注意：使用 venv 时所有后续命令需用 .venv/bin/python 替代 python3
```

安装后验证：
```bash
python3 -c "import requests; print('OK')"
```

## Step 3: 创建命令别名

如果未创建 `alist-cli` 命令（检查 `which alist-cli`），创建 symlink：

```bash
# 确认脚本有执行权限
chmod +x <skill_dir>/scripts/alist_cli.py

# 创建 symlink 到 PATH 目录
sudo ln -sf <skill_dir>/scripts/alist_cli.py /usr/local/bin/alist-cli

# 验证
alist-cli --help
```

如果无 sudo 权限，可用 alias 替代：
```bash
alias alist-cli="python3 <skill_dir>/scripts/alist_cli.py"
```

## Step 4: 配置环境变量

检查现有配置：
```bash
echo $ALIST_URL
echo $ALIST_USERNAME
echo $ALIST_PASSWORD
```

| 变量 | 说明 | 如何获取 |
|------|------|---------|
| `ALIST_URL` | AList 服务器地址 | 用户提供，如 `https://cloud.example.com` |
| `ALIST_USERNAME` | 登录用户名 | 用户提供 |
| `ALIST_PASSWORD` | 登录密码 | 用户提供 |

**重要**：如果环境变量未设置，**必须询问用户提供**这三个值。不要猜测或使用默认值。

设置方式（选一种）：
```bash
# 临时（当前 session）
export ALIST_URL="https://..."
export ALIST_USERNAME="xxx"
export ALIST_PASSWORD="xxx"

# 持久化（写入 shell 配置）
echo 'export ALIST_URL="https://..."' >> ~/.bashrc
echo 'export ALIST_USERNAME="xxx"' >> ~/.bashrc
echo 'export ALIST_PASSWORD="xxx"' >> ~/.bashrc
source ~/.bashrc
```

## Step 5: 验证连接

```bash
alist-cli whoami
```

期望输出：
```
用户: <username>
ID: <id>
根目录 (base_path): /
```

如果输出 `❌ 请设置 ALIST_URL 环境变量` → 回到 Step 4
如果输出 `❌ 登录失败` → 检查用户名密码，回到 Step 4
如果输出 `❌ 未认证` → 环境变量已设置但 token 过期，尝试 `alist-cli login` 或检查 ALIST_USERNAME/PASSWORD

## Step 6: 确认目录结构

```bash
alist-cli ls /
alist-cli ls /private
alist-cli ls /public
```

期望看到：
```
/ → private, public
/private → storage (或其他子目录)
/public → (公开目录内容)
```

## Onboarding 完成

以上步骤全部通过后，onboarding 完成。后续可直接使用 `alist-cli <command>` 进行文件操作。

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决 |
|------|------|------|
| `No module named 'requests'` | 依赖未安装 | 回到 Step 2 |
| `Permission denied` | 无 sudo 权限 / 脚本无执行权 | Step 3 改用 alias 或 venv |
| `❌ 请设置 ALIST_URL` | 环境变量未设置 | Step 4 |
| `❌ 登录失败` | 用户名或密码错误 | 检查凭据，重新设置 |
| `❌ 未认证` | Token 过期 | 重新登录或设置 ALIST_USERNAME/PASSWORD 让脚本自动登录 |
| `sign invalid` | 下载链接过期 | 重新运行 `alist-cli url` 获取新链接 |
| `object not found` | 路径不存在或权限不足 | 检查路径，确认 public/private 路由 |
| `502 Bad Gateway` | AList 服务未启动或网络问题 | 检查 AList 服务状态 |
| `base_path: /` 但路径有双斜杠 | 旧版本 bug | 更新到最新版 skill |
