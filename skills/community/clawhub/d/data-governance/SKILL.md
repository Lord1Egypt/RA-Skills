---
name: data-governance
description: 数据治理与资产管理技能。用于数据质量评估、元数据管理、数据血缘追踪、数据标准制定、数据合规检查等任务。
---

# Data Governance Skill

数据治理（Data Governance）是指对数据资产管理行使权力和控制的活动集合。

## ⚠️ 安全警示

使用前请阅读以下安全建议：

1. **仅使用环境变量** - 不写入配置文件
2. **使用最小权限账户** - 生产环境使用只读用户
3. **勿在命令行明文传密码** - 使用环境变量
4. **敏感数据脱敏** - 分享报告前移除真实数据

## 首次配置

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

**当前会话有效：**
```bash
# MySQL
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=your_user
export DB_PASS=your_password
export DB_NAME=your_database

# PostgreSQL
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=your_user
export DB_PASS=your_password
export DB_NAME=your_database

# SQLite（无需凭证）
export DB_PATH=/path/to/your/database.db
```

**使用前导入：**
```bash
# 每次使用前source环境变量文件（不推荐写入~/.bashrc）
source ~/db-env.sh
python scripts/data_quality_check.py --table users --db-type mysql
```

### 3. 运行脚本

```bash
# 数据质量检查（必须指定 --db-type）
export DB_HOST=localhost DB_USER=admin DB_PASS=xxx DB_NAME=mydb
python scripts/data_quality_check.py --table users --db-type mysql

# 元数据生成
python scripts/generate_metadata.py --source users --db-type postgresql

# 数据血缘分析（可选加数据库）
python scripts/lineage_analysis.py --table orders --db-type sqlite

# 合规检查
python scripts/compliance_check.py --table users --db-type mysql
```

## 依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| sqlalchemy | ==2.0.25 | 数据库抽象层 |
| pymysql | ==1.1.0 | MySQL 连接 |
| psycopg2-binary | ==2.9.9 | PostgreSQL 连接 |
| pandas | ==2.1.4 | 数据处理 |

详见 [requirements.txt](requirements.txt)

## 何时使用

当用户提及以下内容时使用此 skill：
- 数据质量、数据标准、数据血缘
- 元数据管理、数据目录、数据资产
- 数据合规、隐私保护、数据安全
- 数据治理框架、数据资产管理

## 核心能力

### 1. 数据质量评估

评估数据的完整性、准确性、一致性、时效性：

**检查维度：**
- 缺失值检测
- 重复记录检测
- 格式校验
- 范围校验
- 业务规则验证

### 2. 元数据管理

帮助构建和管理元数据：

**技术元数据：** 表结构、字段类型、数据来源
**业务元数据：** 字段定义、业务规则、所有者
**运营元数据：** 更新频率、ETL信息、访问统计

### 3. 数据血缘追踪

追踪数据的来龙去脉：

**来源追溯：** 数据从哪来
**转换追踪：** 经过哪些处理
**下游影响：** 谁在使用这些数据

### 4. 数据标准

制定和执行数据标准：

**命名规范：** 表名、字段名命名规则
**类型规范：** 数据类型、格式标准
**编码规范：** 枚举值、代码表

## 输出格式

完成数据治理任务后，输出结构化报告：

```markdown
## 数据治理报告

### 数据质量
- 完整性：XX%
- 准确率：XX%
- 发现问题：N个

### 元数据
- 表数量：N
- 字段数量：N

### 建议
1. ...
2. ...
```

## 常见场景

| 场景 | 输出 |
|------|------|
| 数据质量评估 | 质量报告 + 问题清单 |
| 元数据梳理 | 数据字典 + 关系图 |
| 血缘分析 | 链路图 + 影响分析 |
| 合规检查 | 合规报告 + 风险点 |