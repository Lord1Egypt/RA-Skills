# AI 自动化测试平台

基于 LangChain + DeepSeek 的智能自动化测试平台

## 🎯 项目概述

AI 自动化测试平台是一个集成了人工智能技术的测试自动化解决方案，支持：
- 智能测试用例生成
- API 自动化测试（Pytest + Requests）
- UI 自动化测试（Playwright）
- 自动化测试报告生成
- 授权管理系统

## 🏗️ 技术架构

```
【前端】Vue3 + Element Plus + Pinia
   ↓
【后端】FastAPI + LangChain + DeepSeek
   ↓
【测试引擎】Pytest (API) + Playwright (UI)
   ↓
【数据存储】MySQL + Chroma (向量数据库)
```

## 📁 项目结构

```
ai-test-platform/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # 应用入口
│   ├── tests/              # 测试文件
│   └── requirements.txt    # Python 依赖
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── stores/         # 状态管理
│   │   └── api/            # API 调用
│   └── package.json
├── data/                    # 数据目录
│   ├── scripts/            # 测试脚本
│   ├── reports/            # 测试报告
│   ├── screenshots/        # 截图文件
│   └── chroma/             # 向量数据
├── scripts/                 # 工具脚本
│   ├── generate_auth.py    # 授权码生成器
│   └── init_db.py          # 数据库初始化
├── docker-compose.yml       # Docker 编排
├── Dockerfile              # Docker 镜像
└── README.md               # 项目说明
```

## 🚀 快速开始

### 1. 环境要求

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### 2. 克隆项目

```bash
git clone <repository-url>
cd ai-test-platform
```

### 3. 配置环境变量

创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
SECRET_KEY=your_secret_key
```

### 4. 初始化数据库

```bash
# 方式1：使用 Docker Compose
docker-compose up -d mysql
python scripts/init_db.py

# 方式2：在 Docker 容器内执行
docker-compose up -d
docker exec -it ai_test_app python /app/scripts/init_db.py
```

### 5. 生成授权码

```bash
python scripts/generate_auth.py
```

按提示选择权限类型、有效期和使用次数。

### 6. 启动服务

```bash
# 使用 Docker Compose
docker-compose up -d

# 或本地开发
# 后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

### 7. 访问平台

- 前端：http://localhost:5173
- API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 📊 核心功能模块

### 1. 授权管理

- **权限类型**
  - `all`：全功能权限
  - `generate`：仅生成权限
  - `execute`：仅执行权限

- **加密机制**
  - AES 加密
  - 密钥：`"yanghua" + timestamp + "360sb"`

### 2. AI 测试生成

支持文档格式：
- Word (.docx)
- Excel (.xlsx)
- PDF (.pdf)
- Markdown (.md)

生成内容：
- 测试用例（功能、边界、异常）
- API 测试脚本（Pytest + Requests）
- UI 测试脚本（Playwright）

### 3. 测试执行

- Docker 容器隔离执行
- 实时日志捕获
- 失败重试机制
- 执行超时控制

### 4. 测试报告

- HTML 格式报告
- AI 智能失败分析
- 导出 PDF/HTML
- 截图和 Trace 回放

## 🔧 配置说明

### DeepSeek API

```python
# backend/app/core/config.py
DEEPSEEK_API_KEY = "your_api_key"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
```

### 数据库配置

```python
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/ai_test_platform"
```

### AI 调用策略

- 最大重试次数：2
- 超时时间：30秒
- 预期调用频率：≤20次/天

## 🛠️ 开发指南

### 后端开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn app.main:app --reload
```

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

### 数据库迁移

```bash
# 修改表结构后重新初始化
python scripts/init_db.py
```

## 📝 API 文档

访问 http://localhost:8000/docs 查看完整的 API 文档（Swagger UI）

主要接口：

- `POST /auth/verify` - 验证授权码
- `POST /generate/case` - 生成测试用例
- `POST /generate/api` - 生成 API 脚本
- `POST /generate/ui` - 生成 UI 脚本
- `POST /execute/run` - 执行测试
- `GET /progress/{task_id}` - 获取任务进度
- `GET /report/generate` - 生成测试报告

## 🔒 安全说明

- ✅ 内网部署，禁止外网访问
- ✅ 授权码 AES 加密存储
- ✅ 全局权限拦截
- ✅ 测试数据本地存储
- ✅ 操作日志审计

## 📈 性能指标

- AI 脚本生成响应：≤10秒
- 测试脚本执行：≤30秒（单脚本）
- 并发用户：≥5人
- 服务可用性：≥99%

## 🐛 故障排查

### 数据库连接失败

```bash
# 检查 MySQL 容器状态
docker ps | grep mysql

# 查看日志
docker logs ai_test_mysql
```

### AI 生成失败

- 检查 DeepSeek API Key 是否正确
- 查看网络连接
- 检查日志中的错误信息

### 脚本执行失败

- 检查 Docker 容器是否正常运行
- 查看执行日志
- 验证脚本语法

## 📄 许可证

本项目为公司内部使用，禁止对外开源。

## 👥 联系方式

- 开发团队：测试开发组
- 维护人员：yanghua

---

**版本**: v1.0.0
**更新日期**: 2026-03-21
