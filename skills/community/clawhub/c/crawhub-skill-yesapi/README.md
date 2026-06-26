# YesApi 果创云低代码平台 Skill

为 OpenCraw 开发的 YesApi 果创云低代码平台接口封装技能，支持在线数据库表单结构管理（创建表单和管理表单字段）和数据操作（增删改查）。

## 功能特性

### 🏗️ 表单结构管理
- 获取表单模型列表
- 创建新的表单模型
- 更新现有表单结构
- 删除表单模型

### 📊 表单数据操作
- 通用数据查询（支持分页、过滤、排序）
- 数据新增
- 数据更新
- 数据删除
- 批量操作支持

### 🔧 配置管理
- 支持本地环境变量配置
- 灵活的域名设置
- 安全的签名机制

## 安装和配置

### 1. 环境要求
- Python 3.8+
- OpenCraw 环境

### 2. 安装依赖
```bash
pip3 install -r requirements.txt
```

### 3. 配置环境变量
复制 `.env.example` 为 `.env` 并配置你的信息：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
YESAPI_APP_KEY=your_app_key_here
YESAPI_DOMAIN=https://api.yesapi.net
YESAPI_SIGN=your_sign_key_here
```

## 本地验证和调试

### 1. 运行测试脚本
```bash
python3 test_yesapi.py
```

测试脚本会验证：
- ✅ 环境配置是否正确
- ✅ 客户端初始化是否成功
- ✅ API连接是否正常
- ✅ 自然语言解析功能

### 2. 发布到Crawhub
```bash
clawhub publish . --name "YesApi 果创云低代码平台" --version "1.0.0" --tags "api,lowcode,yesapi,form,database"
```

### 3. 单元测试
```bash
# 测试客户端功能
python -c "from yesapi_client import create_client; client = create_client(); print(client.get_models())"

# 测试技能处理器
python -c "from skill_handler import process_request; print(process_request('获取模型列表'))"
```

### 4. 调试模式
在代码中添加调试信息：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看详细的API请求和响应
client = create_client()
result = client.query_data('your_table_name', page=1, perpage=10)
print(result)
```

## 使用方法

### 在 OpenCraw 中使用

1. **获取表单列表**
   ```
   获取我的表单模型列表
   ```

2. **查询数据**
   ```
   查询用户表的数据，限制10条记录
   查询订单表中状态为待支付的数据
   ```

3. **添加数据**
   ```
   向用户表添加数据：{"name": "张三", "email": "zhangsan@example.com"}
   ```

4. **更新数据**
   ```
   更新用户表中ID为123的数据：{"name": "李四"}
   ```

5. **删除数据**
   ```
   删除用户表中ID为456的记录
   ```

### 编程接口使用

```python
from yesapi_client import create_client
from skill_handler import process_request

# 使用客户端
client = create_client()
models = client.get_models()
data = client.query_data('users', page=1, perpage=10)

# 使用技能处理器
result = process_request('获取模型列表')
result = process_request('查询用户表数据', {'table_name': 'users'})
```

## API 接口说明

### 表单结构接口 (App.Platform_MyModels)

| 功能 | 方法 | 参数 |
|------|------|------|
| 获取模型列表 | `get_models()` | 无 |
| 创建模型 | `create_model(data)` | 模型数据字典 |
| 更新模型 | `update_model(id, data)` | 模型ID, 更新数据 |
| 删除模型 | `delete_model(id)` | 模型ID |

### 表单数据接口 (App.Table)

| 功能 | 方法 | 参数 |
|------|------|------|
| 查询数据 | `query_data(table, **params)` | 表名, 查询参数 |
| 插入数据 | `insert_data(table, data)` | 表名, 数据字典 |
| 更新数据 | `update_data(table, id, data)` | 表名, 记录ID, 数据 |
| 删除数据 | `delete_data(table, id)` | 表名, 记录ID |
| 批量查询 | `batch_query(table, ids)` | 表名, ID列表 |
| 批量删除 | `batch_delete(table, ids)` | 表名, ID列表 |

## 错误处理

所有API调用都会返回详细错误信息：

```python
try:
    result = client.query_data('nonexistent_table')
except YesApiError as e:
    print(f"错误代码: {e.code}")
    print(f"错误信息: {e}")
    print(f"详细数据: {e.data}")
```

## 项目结构

```
crawhub_skill_yesapi/
├── yesapi_client.py          # YesApi 客户端实现
├── skill_handler.py          # Skill 处理器
├── test_yesapi.py            # 测试脚本
├── .env.example              # 环境变量示例
├── .env                      # 环境变量配置（需要手动创建）
├── requirements.txt          # 依赖包
├── README.md                 # 项目说明
└── SKILL.md                  # Skill 描述文件
```

## 常见问题

### Q: 如何获取 App Key 和 Sign？
A: 登录果创云控制台，在应用管理页面可以找到相关信息。

### Q: API 调用失败怎么办？
A: 检查以下几点：
1. 网络连接是否正常
2. App Key 和 Sign 是否正确
3. 表名和字段名是否存在
4. 查看详细的错误日志

### Q: 支持哪些查询条件？
A: 支持以下查询参数：
- `page`: 页码
- `perpage`: 每页数量
- `where`: 查询条件
- `order`: 排序字段
- `by`: 排序方式 (ASC/DESC)

## 部署到 ClawHub

1. 确保所有测试通过
2. 提交代码到仓库
3. 使用 clawhub 命令发布：
```bash
clawhub publish
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
