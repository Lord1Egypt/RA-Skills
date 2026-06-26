# deterministic-calc Skill

> **核心理念：** 大模型擅长预测（猜），但不擅长确定性计算。本 Skill 将确定性计算固化为代码执行，避免模型"猜"结果。

---

## 🧠 为什么需要这个 Skill？

### 大模型的能力边界

| 擅长（概率性） | 不擅长（确定性） |
|---------------|-----------------|
| 编码（模式匹配） | 数学计算 |
| 翻译 | 逻辑推理 |
| 总结 | 事实查询（会幻觉） |
| 创意写作 | 精确计数 |

### 正确的使用范式

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   大模型    │ ──▶ │   代码      │ ──▶ │   执行结果  │
│  (猜/预测)  │     │  (确定性)   │     │  (确定性)   │
└─────────────┘     └─────────────┘     └─────────────┘
     ↓                                       ↑
  不可靠 ──────────────────────────────────  可靠
```

---

## 📦 安装

```bash
npx clawhub install deterministic-calc
```

---

## 🚀 快速开始

### Python 调用

```python
from deterministic_calc import calculate, safe_eval, run_python

# 简单计算
result = calculate("123456789 * 987654321")
print(result["result"])  # 121932631112635269

# 复杂计算
result = calculate("sum(i**2 for i in range(100))")
print(result["result"])  # 328350

# 安全求值（无代码注入风险）
result = safe_eval("2 + 3 * 4")
print(result["result"])  # 14
```

### CLI 调用

```bash
# 计算
python -m deterministic_calc calc "123456789 * 987654321"

# 安全求值
python -m deterministic_calc safe "2 + 3 * 4"

# 执行 Python
python -m deterministic_calc python "print(sum(range(100)))"

# 执行 Shell
python -m deterministic_calc shell "ls -la"
```

---

## 📚 API 参考

| 函数 | 描述 | 安全性 |
|------|------|--------|
| `calculate(expr)` | 数学表达式计算 | ⚠️ 中等 |
| `safe_eval(expr)` | 安全求值（沙箱） | ✅ 高 |
| `run_python(code)` | 执行 Python 代码 | ⚠️ 低（可执行任意代码） |
| `run_shell(cmd)` | 执行 Shell 命令 | ⚠️ 低（可执行任意命令） |
| `read_file(path)` | 读取文件 | ✅ 高 |
| `write_file(path, content)` | 写入文件 | ✅ 高 |
| `validate_json(str)` | 验证 JSON | ✅ 高 |
| `validate_xml(str)` | 验证 XML | ✅ 高 |

---

## 📝 使用场景

### 场景 1：数学计算

```python
from deterministic_calc import calculate

# 大模型可能会猜错
# 正确做法：调用 Skill
result = calculate("999999999 ** 2")
print(result["result"])  # 999999998000000001
```

### 场景 2：数据处理

```python
from deterministic_calc import run_python

code = """
import json
data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
average_age = sum(p["age"] for p in data) / len(data)
print(f"平均年龄：{average_age}")
"""
result = run_python(code)
print(result["stdout"])  # 平均年龄：27.5
```

### 场景 3：文件操作

```python
from deterministic_calc import read_file, write_file

# 读取
result = read_file("/path/to/file.txt")
if result["success"]:
    print(result["content"])

# 写入
result = write_file("/path/to/output.txt", "Hello, World!")
```

### 场景 4：数据验证

```python
from deterministic_calc import validate_json

# 大模型生成的 JSON 可能无效
json_str = '{"name": "Alice", "age": 30}'
result = validate_json(json_str)

if result["success"]:
    print("JSON 有效:", result["data"])
else:
    print("JSON 无效:", result["error"])
```

---

## ⚠️ 安全说明

| 函数 | 风险等级 | 说明 |
|------|---------|------|
| `safe_eval()` | ✅ 低 | 沙箱隔离，只允许数学运算 |
| `calculate()` | ⚠️ 中 | 可能调用 Python 执行 |
| `run_python()` | ⚠️ 高 | 可执行任意代码 |
| `run_shell()` | ⚠️ 高 | 可执行任意命令 |

**建议：**
- 生产环境只暴露 `safe_eval()` 和 `calculate()`
- `run_python()` 和 `run_shell()` 需要权限控制
- 不要直接执行用户输入的代码

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 License

MIT License
