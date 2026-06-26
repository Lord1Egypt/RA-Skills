# Code Simplifier - 最佳实践

## 代码质量金字塔

```
第一层: 可运行 (Works)
   ↓
第二层: 可读 (Readable)
   ↓
第三层: 可维护 (Maintainable)
   ↓
第四层: 可测试 (Testable)
   ↓
第五层: 可扩展 (Extensible)
```

## 函数设计原则

### 1. 单一职责 (SRP)

```python
# ❌ 违反 SRP: 一个函数做太多事
def process_user_registration(user_data):
    # 验证数据
    # 创建用户
    # 发送邮件
    # 记录日志
    pass

# ✅ 遵循 SRP: 每个函数只做一件事
def validate_user_data(user_data):
    pass

def create_user(user_data):
    pass

def send_welcome_email(user):
    pass

def log_registration(user):
    pass

# 组合调用
def process_user_registration(user_data):
    validate_user_data(user_data)
    user = create_user(user_data)
    send_welcome_email(user)
    log_registration(user)
    return user
```

### 2. 函数长度控制

```python
# 推荐长度
# ✅ 1-10行: 理想
# ✅ 11-30行: 可接受
# ⚠️ 31-50行: 需要考虑拆分
# ❌ >50行: 必须拆分

def ideal_function(data):
    """理想长度函数"""
    processed = preprocess(data)
    result = core_logic(processed)
    return postprocess(result)
```

### 3. 参数数量限制

```python
# ❌ 参数过多
def create_user(name, email, age, address, phone, country, city, zip_code):
    pass

# ✅ 使用数据类
@dataclass
class UserProfile:
    name: str
    email: str
    age: int
    address: str
    phone: str
    country: str
    city: str
    zip_code: str

def create_user(profile: UserProfile):
    pass
```

## 代码组织

### 1. 文件结构

```
module/
├── __init__.py
├── models.py       # 数据模型
├── services.py     # 业务逻辑
├── utils.py        # 工具函数
└── constants.py    # 常量定义
```

### 2. 导入顺序

```python
# 1. 标准库
import os
import sys
from datetime import datetime

# 2. 第三方库
import numpy as np
from openai import OpenAI

# 3. 本地模块
from .models import User
from .utils import validate_email
```

### 3. 依赖注入

```python
# ❌ 硬编码依赖
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # 硬编码

# ✅ 依赖注入
class UserService:
    def __init__(self, database):
        self.db = database  # 注入依赖
```

## 错误处理

### 1. 具体异常

```python
# ❌ 捕获所有异常
try:
    process_data()
except:
    pass

# ✅ 捕获具体异常
try:
    process_data()
except ValueError as e:
    logger.error(f"数据验证失败: {e}")
except NetworkError as e:
    logger.error(f"网络错误: {e}")
```

### 2. 异常链

```python
# ✅ 保留原始异常
def process_user(user_id):
    try:
        user = fetch_user(user_id)
    except DatabaseError as e:
        raise UserProcessingError(f"用户 {user_id} 处理失败") from e
```

### 3. 资源管理

```python
# ✅ 使用 context manager
with open('file.txt', 'r') as f:
    data = f.read()

# ✅ 自定义 context manager
@contextmanager
def database_transaction():
    tx = begin_transaction()
    try:
        yield tx
        tx.commit()
    except Exception:
        tx.rollback()
        raise
```

## 性能优化

### 1. 避免过早优化

```python
# ❌ 过早优化
def process_items(items):
    # 复杂的优化逻辑
    # 但性能提升微乎其微
    pass

# ✅ 先简洁,后优化
def process_items(items):
    result = []
    for item in items:
        if is_valid(item):
            result.append(transform(item))
    return result
```

### 2. 使用生成器

```python
# ❌ 列表: 占用大量内存
def process_large_file(file_path):
    with open(file_path) as f:
        return [process_line(line) for line in f]

# ✅ 生成器: 节省内存
def process_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield process_line(line)
```

### 3. 缓存结果

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # 昂贵计算
    return result
```

## 测试友好设计

### 1. 依赖注入

```python
# ✅ 便于测试
class UserService:
    def __init__(self, database, email_service):
        self.db = database
        self.email = email_service

# 测试时可以注入 mock 对象
def test_user_service():
    mock_db = MockDatabase()
    mock_email = MockEmailService()
    service = UserService(mock_db, mock_email)
    # 测试代码
```

### 2. 纯函数

```python
# ✅ 纯函数: 易测试
def calculate_discount(price, rate):
    return price * rate

# ❌ 有副作用的函数: 难测试
def calculate_and_save_discount(price, rate):
    discount = price * rate
    database.save(discount)  # 副作用
    return discount
```

### 3. 避免全局状态

```python
# ❌ 全局状态
state = {"count": 0}

def increment():
    state["count"] += 1
    return state["count"]

# ✅ 显式传递状态
def increment(count):
    return count + 1
```

## 代码审查清单

### 提交前检查

- [ ] 代码符合项目风格指南
- [ ] 函数长度 < 50行
- [ ] 嵌套层级 < 3层
- [ ] 变量命名清晰
- [ ] 无重复代码
- [ ] 有适当的错误处理
- [ ] 有必要的注释
- [ ] 通过所有测试

### Pull Request 检查

- [ ] PR 描述清晰
- [ ] 代码变更合理
- [ ] 无引入新的技术债务
- [ ] 性能影响可接受
- [ ] 文档已更新
- [ ] 测试覆盖率足够

## 重构策略

### 1. 小步重构

```python
# 步骤1: 提取函数
def process(data):
    # ... 复杂逻辑
    result = helper(data)
    return result

def helper(data):
    # 提取的逻辑
    pass

# 步骤2: 验证
# 运行测试确保功能不变

# 步骤3: 继续优化
# 逐步改进
```

### 2. 测试先行

```python
# 1. 先写测试
def test_process_data():
    assert process_data([1, 2, 3]) == [2, 4, 6]

# 2. 重构代码
def process_data(data):
    return [x * 2 for x in data]

# 3. 验证测试通过
```

### 3. 安全重构

```bash
# 创建分支
git checkout -b refactor/user-service

# 小步提交
git commit -m "refactor: 提取用户验证逻辑"
git commit -m "refactor: 简化数据处理流程"

# 持续测试
pytest tests/

# 合并前回顾
git diff master
```

## 文档和注释

### 1. Docstring

```python
def process_payment(user_id: int, amount: float) -> bool:
    """
    处理用户支付

    Args:
        user_id: 用户ID
        amount: 支付金额

    Returns:
        是否成功

    Raises:
        InsufficientFundsError: 余额不足
        PaymentGatewayError: 支付网关错误

    Example:
        >>> process_payment(123, 99.99)
        True
    """
    pass
```

### 2. 注释原则

```python
# ✅ 好的注释: 解释"为什么"
# 使用幂等性确保重试安全
result = retry_with_backoff(api_call, max_retries=3)

# ❌ 坏的注释: 重复代码
# 调用 API 并重试
result = retry_with_backoff(api_call, max_retries=3)
```

## 参考资源

- [重构模式详解](refactoring_patterns.md) - 重构模式
- [故障排除](troubleshooting.md) - 代码异味诊断与复杂度分析
