# 达梦数据库知识库生成支持 - 修改记录

## 概述

本次修改实现了对达梦数据库知识库生成的完整支持，采用多驱动策略，让客户可以根据自己的环境选择最合适的驱动方式。

## 主要修改

### 1. 重构 `scripts/knowledge/generate.py`

#### 新增 `DatabaseDriver` 类
- 自动检测并加载合适的数据库驱动
- 支持三种数据库类型：MySQL、达梦、Oracle
- 达梦数据库支持两种驱动方式：
  - **dmPython** (推荐用于 Linux/Windows)：性能最好
  - **pyodbc** (推荐用于 macOS)：跨平台兼容性好

#### 驱动检测逻辑
```python
# 1. 尝试 dmPython（性能最好）
# 2. 尝试 pyodbc（跨平台兼容性好）
# 3. 都不可用时给出详细的安装指南
```

#### 统一的数据库操作接口
- `connect()`：建立数据库连接
- `create_cursor()`：创建游标
- `execute()`：执行 SQL（自动处理参数占位符差异）
- `fetchall()`：获取所有结果

### 2. 创建 `scripts/knowledge/requirements.txt`

```
pymysql>=1.0.0          # MySQL 支持
dmPython>=2.5.0         # 达梦数据库支持（Linux/Windows）
pyodbc>=4.0.0           # 达梦数据库支持（macOS）
oracledb>=1.0.0         # Oracle 支持
```

### 3. 更新 `README.md`

添加了详细的知识库生成文档，包括：
- 各数据库类型的驱动安装说明
- 达梦数据库的两种安装方式（dmPython 和 pyodbc）
- 环境变量配置说明
- 故障排除指南

## 使用方法

### MySQL
```bash
cd scripts/knowledge
python3 generate.py --db-type mysql --apply
```

### 达梦数据库
脚本会自动检测可用的驱动：

```bash
cd scripts/knowledge
python3 generate.py --db-type dm --apply
```

如果未找到驱动，脚本会给出详细的安装指南。

### Oracle
```bash
cd scripts/knowledge
python3 generate.py --db-type oracle --apply
```

## 环境变量配置

```bash
export ACM_DB_TYPE=dm                    # 数据库类型
export ACM_DB_HOST=192.168.3.11          # 主机地址
export ACM_DB_PORT=5236                  # 端口号
export ACM_DB_USER=ACM_CLOUD_AVIC_100    # 用户名
export ACM_DB_PASSWORD=ACM_CLOUD_AVIC_100 # 密码
export ACM_DB_NAME=DM                    # 数据库名
```

## 故障排除

### dmPython 方案
- 检查是否安装了达梦数据库客户端
- 检查环境变量 `DM_HOME` 是否配置正确
- 运行 `python3 -c "import dmPython"` 验证安装

### pyodbc 方案
- 检查是否安装了 pyodbc：`pip3 show pyodbc`
- 检查是否安装了达梦 ODBC 驱动
- 运行 `python3 -c "import pyodbc; print(pyodbc.drivers())"` 查看可用驱动

### 手动创建
如果无法安装任何驱动，可以手动创建知识库文件，参考 `knowledge/mysql/tables.json` 的格式。

## 技术细节

### 多驱动支持架构
```
DatabaseDriver
├── detect()          # 自动检测可用驱动
├── connect()         # 建立连接
├── create_cursor()   # 创建游标
├── execute()         # 执行 SQL
└── fetchall()        # 获取结果
```

### SQL 适配
- MySQL：使用 `information_schema`，参数占位符 `%s`
- 达梦：使用 `USER_TAB_COLUMNS`，参数占位符 `?`
- Oracle：使用 `USER_TAB_COLUMNS`，参数占位符 `?`

### 列名大小写处理
不同数据库返回的列名大小写不一致，使用 `.get('COLUMN_NAME') or .get('column_name')` 方式兼容。

## 测试验证

- ✅ MySQL 知识库生成正常
- ✅ 达梦数据库驱动检测正常
- ✅ 错误提示信息清晰完整
- ✅ 文档更新完整

## 后续建议

1. 在实际达梦数据库环境中测试 dmPython 驱动
2. 在实际达梦数据库环境中测试 pyodbc 驱动
3. 根据客户反馈进一步优化错误提示信息
