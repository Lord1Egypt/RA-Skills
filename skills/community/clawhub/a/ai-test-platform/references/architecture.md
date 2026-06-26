# AI 自动化测试平台 - 系统架构说明

## 技术架构确认

### 分层架构
```
【前端交互层】Vue3 + Element Plus + Pinia (状态管理)
      ↓ (轮询机制)
【API接入层】FastAPI 接口服务 + 授权拦截器
      ↓
【业务逻辑层】授权管理、测试设计、执行调度、报告生成
      ↓
【AI核心层】LangChain + DeepSeek大模型 + RAG检索
      ↓
【测试引擎层】Pytest(接口) + Playwright(UI)
      ↓
【数据持久层】MySQL(业务数据) + Chroma(向量数据)
```

### 核心技术栈

| 层级 | 技术选型 | 版本要求 | 说明 |
|------|---------|---------|------|
| 前端 | Vue3 | ^3.3.0 | 响应式框架 |
| 前端UI | Element Plus | ^2.4.0 | UI组件库 |
| 状态管理 | Pinia | ^2.1.0 | 全局状态管理 |
| 后端 | FastAPI | ^0.104.0 | 异步Web框架 |
| AI框架 | LangChain | ^0.1.0 | 大模型编排框架 |
| 大模型 | DeepSeek | API | AI能力支撑 |
| 接口测试 | Pytest | ^7.4.0 | 测试框架 |
| 接口测试插件 | pytest-json-report | ^1.5.0 | JSON报告生成 |
| UI测试 | Playwright | ^1.40.0 | 浏览器自动化 |
| 数据库 | MySQL | 8.0 | 关系型数据库 |
| 向量库 | Chroma | ^0.4.0 | 向量检索 |
| 部署 | Docker | 最新 | 容器化部署 |
| 编排 | Docker Compose | 最新 | 容器编排 |

## 核心模块设计确认

### 1. 授权管理模块

**权限粒度：**
- `all` - 全功能权限
- `generate` - 仅生成权限
- `execute` - 仅执行权限

**加密机制：**
- 算法：AES
- 密钥生成规则：`"yanghua" + 当前时间戳 + "360sb"`
- 存储方式：授权码加密后存储

**验证流程：**
```
用户请求 → 携带auth_code → AuthInterceptor拦截
→ 验证有效性、过期时间、使用次数、权限类型
→ 通过：放行 + 使用次数+1
→ 失败：返回401/403
```

### 2. 脚本执行环境隔离

**Docker容器化执行：**
- 所有Pytest和Playwright脚本在Docker容器内执行
- 通过`pytest.main()`调用测试
- 使用`pytest-json-report`插件解析结果

**依赖管理：**
- `requirements.txt`统一管理所有Python依赖
- Docker镜像构建时预装所有依赖
- 测试环境与主服务隔离

### 3. AI调用策略

**DeepSeek API配置：**
- 无QPS限制
- 失败重试：2次
- 预计调用频率：≤20次/天

**重试机制：**
```python
max_retries = 2
timeout = 30  # 秒
```

### 4. 文档解析支持

**支持的文档格式：**
- Word (.docx)
- Excel (.xlsx)
- PDF (.pdf)
- Markdown (.md)

**解析库：**
- Word: `python-docx`
- Excel: `openpyxl`
- PDF: `PyPDF2` 或 `pdfplumber`
- Markdown: `markdown`

### 5. RAG向量数据库选型

**选择：Chroma**

**理由：**
1. 轻量级，无需额外部署服务
2. 本地持久化存储，适合内网环境
3. 支持中文向量检索（配合中文Embedding模型）
4. 与LangChain集成良好
5. 零配置，开箱即用

**向量模型：**
- 使用OpenAI的`text-embedding-ada-002`（需API）
- 或使用本地模型：`text2vec-chinese`（推荐，无需API）

### 6. 测试报告AI分析

**Prompt模板（简单分析）：**
```
请分析以下测试执行日志，找出失败原因：
{execution_log}

请提供：
1. 失败的主要原因
2. 可能的问题定位
3. 建议的解决方案

分析要求：简洁明了，突出关键信息。
```

### 7. 前端实时进度展示

**实现方案：**
- 状态管理：Pinia
- 进度更新：轮询机制（每2秒查询一次）
- 进度类型：
  - AI生成进度（文档解析 → 向量化 → 生成中 → 完成）
  - 脚本执行进度（执行中 → 收集结果 → 生成报告）

**轮询API：**
```python
GET /api/progress/{task_id}
Response: {
  "status": "processing|completed|failed",
  "progress": 50,  # 百分比
  "message": "正在生成测试用例..."
}
```

### 8. Playwright运行模式

**配置：**
- Headless模式（无界面运行）
- 每个用例执行后自动截图
- 失败时保存完整trace文件
- 提供可视化回放功能（HTML Trace Viewer）

**截图策略：**
```python
# 每个用例执行后
page.screenshot(path=f"screenshots/{test_name}.png")

# 失败时额外记录
browser_context.tracing.stop(path=f"traces/{test_name}.zip")
```

## 数据库设计补充

### 核心表结构

#### 1. 授权码表 auth_codes
```sql
CREATE TABLE auth_codes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(100) UNIQUE NOT NULL COMMENT '授权码（加密后）',
    permission VARCHAR(20) NOT NULL COMMENT '权限类型：all/generate/execute',
    expire_time DATETIME NOT NULL COMMENT '过期时间',
    use_count INT DEFAULT 0 COMMENT '已使用次数',
    max_count INT NOT NULL COMMENT '最大使用次数',
    is_active TINYINT DEFAULT 1 COMMENT '启用状态：1启用/0禁用',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='授权码表';
```

#### 2. 测试用例表 test_cases
```sql
CREATE TABLE test_cases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL COMMENT '用例标题',
    content TEXT NOT NULL COMMENT '用例详情',
    type VARCHAR(10) NOT NULL COMMENT '类型：api/ui',
    created_by VARCHAR(50) COMMENT '创建者（授权码）',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试用例表';
```

#### 3. 自动化脚本表 auto_scripts
```sql
CREATE TABLE auto_scripts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL COMMENT '脚本名称',
    content TEXT NOT NULL COMMENT '脚本代码',
    type VARCHAR(10) NOT NULL COMMENT '类型：api/ui',
    status VARCHAR(10) DEFAULT 'active' COMMENT '状态：active/archived',
    created_by VARCHAR(50) COMMENT '创建者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='自动化脚本表';
```

#### 4. 执行记录表 execute_records
```sql
CREATE TABLE execute_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    script_id INT NOT NULL COMMENT '脚本ID',
    auth_code VARCHAR(50) COMMENT '执行者授权码',
    result VARCHAR(10) NOT NULL COMMENT '结果：success/fail',
    log TEXT COMMENT '执行日志',
    execute_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    duration INT COMMENT '执行耗时（秒）',
    INDEX idx_script_id (script_id),
    INDEX idx_result (result),
    INDEX idx_execute_time (execute_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='执行记录表';
```

#### 5. 测试报告表 test_reports
```sql
CREATE TABLE test_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    record_id INT NOT NULL COMMENT '执行记录ID',
    report_content TEXT COMMENT '报告内容（JSON/HTML）',
    file_path VARCHAR(255) COMMENT '报告文件路径',
    ai_analysis TEXT COMMENT 'AI分析结果',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_record_id (record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试报告表';
```

#### 6. 任务进度表 task_progress (新增)
```sql
CREATE TABLE task_progress (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id VARCHAR(100) UNIQUE NOT NULL COMMENT '任务ID',
    task_type VARCHAR(20) NOT NULL COMMENT '任务类型：generate/execute',
    status VARCHAR(20) NOT NULL COMMENT '状态：pending/processing/completed/failed',
    progress INT DEFAULT 0 COMMENT '进度百分比',
    message VARCHAR(255) COMMENT '进度消息',
    result_data TEXT COMMENT '结果数据（JSON）',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_task_id (task_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务进度表';
```

## API接口设计规范

### 统一响应格式
```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

### 公共参数
- `auth_code`: 授权码（必需，所有核心接口）

### 错误码定义
- `200`: 成功
- `400`: 参数错误
- `401`: 未授权/授权码无效
- `403`: 权限不足
- `500`: 服务器错误
- `503`: AI服务不可用

## 部署架构

### Docker Compose编排
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: ai_test_platform
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mysql
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=mysql+pymysql://root:root123@mysql:3306/ai_test_platform
      - DEEPSEEK_API_KEY=your_api_key

volumes:
  mysql_data:
```

### 数据持久化
- MySQL数据：Docker Volume
- 脚本文件：`./data/scripts/`
- 测试报告：`./data/reports/`
- 截图文件：`./data/screenshots/`
- 向量数据：`./data/chroma/`
