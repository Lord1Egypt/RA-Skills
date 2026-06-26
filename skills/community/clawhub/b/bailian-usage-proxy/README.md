# 阿里百炼用量统计代理

多人共享账号场景下的精细化用量统计方案。

## 快速开始（无需 Docker）

### 1. 一键启动

```bash
cd skills/bailian-usage-proxy

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的阿里百炼 API Key

# 启动服务
./start.sh
```

服务启动后：
- API 地址: http://localhost:8080
- 管理后台: http://localhost:8081

### 2. 手动安装（如需自定义）

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install fastapi uvicorn httpx sqlalchemy aiosqlite pydantic python-dotenv jinja2 python-multipart

# 初始化数据库
python3 scripts/init_db.py

# 创建用户
python3 scripts/create_user.py --name "张三" --department "算法部"

# 启动服务
python3 -m app.main
```

## 使用方式

### 客户端配置修改

```python
# 原配置（直接使用阿里百炼）
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "sk-xxx"  # 阿里百炼主账号Key

# 新配置（通过代理）
base_url = "http://localhost:8080/v1"
api_key = "bl-xxxx"  # 代理系统分配的Key
```

### 查看用量

```bash
# 今日用量
python3 scripts/usage_report.py --today

# 指定日期范围
python3 scripts/usage_report.py --start-date 2026-03-01 --end-date 2026-03-09

# 导出CSV
python3 scripts/usage_report.py --today --export usage.csv
```

## 功能特性

- ✅ OpenAI API 格式完全兼容
- ✅ 实时用量统计（按用户、模型、时间）
- ✅ 日限额/月限额控制
- ✅ Web 管理后台
- ✅ 用量报表导出
- ✅ 支持 SQLite/MySQL

## 项目结构

```
bailian-usage-proxy/
├── app/                    # 核心代码
│   ├── config.py          # 配置管理
│   ├── models.py          # 数据模型
│   ├── database.py        # 数据库操作
│   ├── proxy.py           # 代理转发
│   ├── api.py             # API路由
│   ├── admin.py           # 管理后台
│   └── main.py            # 主程序
├── scripts/               # 工具脚本
│   ├── init_db.py         # 初始化数据库
│   ├── create_user.py     # 创建用户
│   └── usage_report.py    # 用量报表
├── templates/             # HTML模板
├── start.sh              # 一键启动脚本 ⭐
├── requirements.txt       # Python依赖
└── .env.example          # 环境变量示例
```

## Docker 部署（可选）

如需 Docker 部署，参见 `docker-compose.yml`。
