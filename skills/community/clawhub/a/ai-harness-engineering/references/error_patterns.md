# 常见错误模式库

本文档记录 OpenClaw 常见的错误模式，帮助识别和避免重复犯错。

---

## 一、编码相关错误模式

### 模式 1：CSV 文件编码错误

**错误表现**：
- Windows Excel 打开 CSV 显示乱码
- 中文字符变成 `锟斤拷` 或 `?`

**根本原因**：
- 未使用 UTF-8 BOM 编码
- Windows Excel 默认使用系统代码页（GBK）

**正确做法**：
```python
# Windows 平台 CSV 必须使用 utf-8-sig（带 BOM）
with open('data.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['姓名', '年龄'])
```

**相关错误ID**：查询 `--keywords "CSV 编码"`

---

### 模式 2：bat/cmd 脚本中文乱码

**错误表现**：
- Windows cmd.exe 执行 .bat 脚本时中文显示乱码
- 脚本中的中文路径无法识别

**根本原因**：
- cmd.exe 默认使用 GBK 编码
- 用 UTF-8 编写的脚本在 cmd 中无法正确显示

**正确做法**：
```python
# Windows 上 .bat 文件含中文时使用 GBK 编码
with open('run.bat', 'w', encoding='gbk') as f:
    f.write('@echo 你好世界\n')
```

**相关错误ID**：查询 `--keywords "bat cmd 编码"`

---

### 模式 3：Python 文件读写编码错误

**错误表现**：
- `UnicodeDecodeError: 'gbk' codec can't decode byte...`
- 读取文件时出现乱码

**根本原因**：
- 未显式指定 encoding 参数
- Windows 默认使用 GBK，与文件实际编码不符

**正确做法**：
```python
# 始终显式指定 encoding
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 写入时同样指定
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write(content)
```

---

## 二、跨平台兼容错误模式

### 模式 4：换行符不一致

**错误表现**：
- 脚本在不同平台上执行失败
- 文件在 Windows 记事本中显示为一行

**根本原因**：
- Windows 使用 CRLF (`\r\n`)
- Unix/Linux/macOS 使用 LF (`\n`)
- 未正确处理换行符

**正确做法**：
```python
# 写入时自动处理换行符
with open('file.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(content)

# 或显式指定
with open('file.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
```

---

### 模式 5：路径分隔符问题

**错误表现**：
- 文件路径在 Windows 上无法识别
- macOS 生成的路径在 Windows 上失败

**根本原因**：
- 混用 `/` 和 `\`
- 硬编码路径分隔符

**正确做法**：
```python
from pathlib import Path

# 使用 Path 自动处理分隔符
data_file = Path('data') / 'subdir' / 'file.txt'

# 或使用 os.path
import os
data_file = os.path.join('data', 'subdir', 'file.txt')
```

---

## 三、文件操作错误模式

### 模式 6：文件未关闭导致资源泄漏

**错误表现**：
- 文件写入后内容未刷新到磁盘
- 大量文件打开导致系统资源耗尽

**根本原因**：
- 使用 `open()` 后未调用 `close()`
- 异常发生时文件未正确关闭

**正确做法**：
```python
# 使用 with 语句自动关闭
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write(content)
# 文件自动关闭

# 错误示范
f = open('file.txt', 'w')
f.write(content)
# 忘记关闭！
```

---

### 模式 7：文件覆盖未备份

**错误表现**：
- 重要文件被意外覆盖
- 无法恢复原始内容

**根本原因**：
- 写入前未检查文件是否存在
- 未创建备份

**正确做法**：
```python
import shutil
from pathlib import Path

target = Path('important.txt')
if target.exists():
    # 创建备份
    backup = target.with_suffix('.txt.bak')
    shutil.copy(target, backup)

# 然后写入
target.write_text(new_content, encoding='utf-8')
```

---

## 四、逻辑推理错误模式

### 模式 8：边界条件遗漏

**错误表现**：
- 程序在边界值处行为异常
- 循环多执行或少执行一次

**根本原因**：
- 未考虑所有边界情况
- 条件判断不完整

**正确做法**：
```python
# 列举所有边界情况
def divide(a, b):
    # 边界检查
    if b == 0:
        raise ValueError("除数不能为0")
    if a == 0:
        return 0
    # 正常逻辑
    return a / b

# 循环边界
for i in range(len(items)):  # 0 到 len-1
    process(items[i])

# 或更安全
for item in items:
    process(item)
```

---

### 模式 9：空值处理缺失

**错误表现**：
- `AttributeError: 'NoneType' object has no attribute...`
- 程序因 None 值崩溃

**根本原因**：
- 未检查函数返回值是否为 None
- 未处理空数据

**正确做法**：
```python
# 始终检查 None
result = get_data()
if result is None:
    return "无数据"

# 使用默认值
result = get_data() or {}

# 使用可选类型（Python 3.10+）
def get_data() -> dict | None:
    ...
```

---

## 五、API 调用错误模式

### 模式 10：API 参数错误

**错误表现**：
- API 返回 400 错误
- 参数类型不匹配

**根本原因**：
- 未查阅最新 API 文档
- 参数类型或格式错误

**正确做法**：
```python
# 查阅官方文档确认参数格式
import requests

# 错误示范
response = requests.post(url, data={'key': 'value'})  # 可能是 form data

# 正确：根据 API 要求选择
response = requests.post(url, json={'key': 'value'})  # JSON 格式
```

---

## 六、安全相关错误模式

### 模式 11：敏感信息泄露

**错误表现**：
- 日志中包含密码或 API 密钥
- 错误信息暴露系统内部细节

**根本原因**：
- 未脱敏敏感信息
- 调试信息未清理

**正确做法**：
```python
import os

# 从环境变量读取敏感信息
api_key = os.getenv('API_KEY')

# 日志脱敏
def log_request(key):
    masked = key[:4] + '****' if len(key) > 4 else '****'
    print(f"API Key: {masked}")
```

---

### 模式 12：SQL 注入风险

**错误表现**：
- SQL 查询使用字符串拼接
- 用户输入直接嵌入 SQL

**根本原因**：
- 未使用参数化查询
- 未验证用户输入

**正确做法**：
```python
import sqlite3

# 错误示范
sql = f"SELECT * FROM users WHERE name = '{name}'"  # 危险！

# 正确：使用参数化查询
sql = "SELECT * FROM users WHERE name = ?"
cursor.execute(sql, (name,))
```

---

## 七、错误模式识别清单

回答问题前，检查是否涉及以下场景：

| 场景 | 常见错误 | 检查点 |
|------|---------|--------|
| 文件写入 | 编码错误、换行符问题 | 是否指定 encoding？是否处理 newline？ |
| CSV 导出 | Excel 乱码 | Windows 上是否使用 utf-8-sig？ |
| 跨平台代码 | 路径分隔符、换行符 | 使用 Path 还是字符串拼接？ |
| 条件判断 | 边界遗漏、空值处理 | 是否列举所有情况？是否检查 None？ |
| API 调用 | 参数错误、版本不匹配 | 是否查阅最新文档？ |
| 敏感信息 | 密码泄露、日志暴露 | 是否脱敏？是否使用环境变量？ |
| 数据库操作 | SQL 注入 | 是否使用参数化查询？ |

---

## 八、如何使用本模式库

1. **回答前自检**：对照清单检查是否涉及常见错误模式
2. **记录新错误**：发现新的错误模式时，更新本文档
3. **查询历史错误**：使用 `query_errors.py` 查询相关错误
4. **持续优化**：定期复盘高频错误，完善模式库

---

*本文档会持续更新，记录 OpenClaw 的所有错误模式，形成最佳实践库。*
