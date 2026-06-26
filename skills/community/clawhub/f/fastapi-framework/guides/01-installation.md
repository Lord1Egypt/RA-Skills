# 安装指南

**适用场景**: 首次使用 FastAPI，需要安装和配置开发环境

---

## 一、安装前准备

### 目标

确保系统具备运行 FastAPI 的基础 Python 环境

### 前置条件

- Python 3.8 或更高版本（推荐 3.11+）
- pip 包管理器
- （推荐）虚拟环境工具

### 检查 Python 环境

**AI 执行说明**: AI 将自动检查你的 Python 版本和 pip 可用性

```bash
# 检查 Python 版本
python --version
# 或
python3 --version

# 检查 pip
pip --version

# 检查 Python 路径
which python
```

**期望结果**:

- Python 3.8+ ✅
- pip 已安装 ✅

---

## 二、创建虚拟环境（推荐）

使用虚拟环境可以隔离项目依赖，避免版本冲突。

### 方法 1：使用 venv（Python 内置）

**AI 执行说明**: AI 可以自动创建并激活虚拟环境

```bash
# 创建虚拟环境（在项目目录中）
python -m venv .venv

# 激活虚拟环境
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat
```

**验证激活状态**:

```bash
# 激活后命令行前会显示 (.venv)
which python  # 应指向 .venv/bin/python
```

### 方法 2：使用 uv（更快的现代工具）

```bash
# 安装 uv
pip install uv

# 创建并激活虚拟环境
uv venv
source .venv/bin/activate

# 使用 uv 安装包（比 pip 快 10-100x）
uv pip install "fastapi[standard]"
```

### 方法 3：使用 conda

```bash
# 创建 conda 环境
conda create -n myproject python=3.11

# 激活环境
conda activate myproject
```

---

## 三、安装 FastAPI

### 标准安装（推荐）

**AI 执行说明**: AI 可以直接执行安装命令

```bash
pip install "fastapi[standard]"
```

`[standard]` 安装包含以下依赖：

| 包名 | 用途 |
|------|------|
| `uvicorn[standard]` | ASGI 服务器，运行 FastAPI 应用 |
| `pydantic` | 数据验证和序列化 |
| `fastapi-cli` | `fastapi dev` / `fastapi run` 命令行工具 |
| `email-validator` | Email 字段验证 |
| `httpx` | 测试客户端 |
| `jinja2` | 模板引擎（可选） |
| `python-multipart` | 表单和文件上传支持 |

### 最小化安装

如果只需要 FastAPI 核心功能：

```bash
# 仅安装 FastAPI
pip install fastapi

# 单独安装 ASGI 服务器
pip install "uvicorn[standard]"
```

### 验证安装

**AI 执行说明**: AI 将验证 FastAPI 是否正确安装

```bash
# 检查 FastAPI 版本
python -c "import fastapi; print(fastapi.__version__)"

# 检查 uvicorn 版本
uvicorn --version

# 检查 pydantic 版本
python -c "import pydantic; print(pydantic.__version__)"
```

**期望输出示例**:

```
0.115.0
Running uvicorn 0.32.0 with CPython 3.11.0 on Darwin
2.9.2
```

---

## 四、安装可选依赖

根据项目需求选择安装：

### 数据库支持

```bash
# SQLModel（推荐，基于 SQLAlchemy + Pydantic）
pip install sqlmodel

# 纯 SQLAlchemy
pip install sqlalchemy

# PostgreSQL 驱动
pip install asyncpg          # 异步驱动（推荐生产环境）
pip install psycopg2-binary  # 同步驱动

# MySQL 驱动
pip install aiomysql

# SQLite（Python 内置，无需安装）
```

### 安全认证

```bash
# JWT 令牌
pip install pyjwt

# 密码哈希
pip install "pwdlib[argon2]"

# 或使用 passlib（旧版方案）
pip install "passlib[bcrypt]"
```

### 测试工具

```bash
# pytest 测试框架
pip install pytest

# 异步测试支持
pip install anyio pytest-anyio

# HTTP 测试客户端（已包含在 standard 中）
pip install httpx
```

### 其他常用包

```bash
# 环境变量管理
pip install python-dotenv

# 跨域支持（FastAPI 内置，无需额外安装）
# 使用 app.add_middleware(CORSMiddleware, ...) 即可

# 后台任务队列
pip install celery redis

# 缓存
pip install aioredis
```

---

## 五、生成 requirements.txt

```bash
# 导出当前环境依赖
pip freeze > requirements.txt

# 从 requirements.txt 安装
pip install -r requirements.txt
```

**典型的 requirements.txt 示例**:

```
fastapi[standard]>=0.115.0
sqlmodel>=0.0.21
pyjwt>=2.9.0
pwdlib[argon2]>=0.2.0
python-dotenv>=1.0.0
```

---

## 六、使用 pyproject.toml（现代项目推荐）

```toml
[project]
name = "my-fastapi-app"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = [
    "fastapi[standard]>=0.115.0",
    "sqlmodel>=0.0.21",
    "pyjwt>=2.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "httpx>=0.27.0",
]
```

---

## 七、常见安装问题

### 问题 1：Python 版本过低

**错误**: `ERROR: Package 'fastapi' requires a different Python`

**解决方案**:

```bash
# 检查当前版本
python --version

# 使用 pyenv 安装新版本 Python
pyenv install 3.11.0
pyenv local 3.11.0
```

### 问题 2：pip 网络超时

**解决方案**:

```bash
# 使用清华大学镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple "fastapi[standard]"

# 或配置永久镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 3：权限错误

**解决方案**:

```bash
# 使用用户级别安装（不推荐，优先使用虚拟环境）
pip install --user "fastapi[standard]"
```

### 问题 4：pydantic v1/v2 兼容性问题

FastAPI 0.100+ 使用 Pydantic v2，API 有所变化。

```bash
# 查看当前 pydantic 版本
python -c "import pydantic; print(pydantic.VERSION)"

# 如需强制使用 pydantic v1 兼容模式
pip install "pydantic[v1]"
```

---

## 完成确认

### 检查清单

- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] FastAPI 已安装（`fastapi[standard]`）
- [ ] uvicorn 可用（`uvicorn --version`）
- [ ] 导入测试通过（`python -c "import fastapi"`）

### 下一步

继续阅读 [快速开始](02-quickstart.md) 创建你的第一个 FastAPI 应用
