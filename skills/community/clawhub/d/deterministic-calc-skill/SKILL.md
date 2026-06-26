# deterministic-calc Skill

**核心理念：** 大模型擅长预测（猜），但不擅长确定性计算。本 Skill 将确定性计算固化为代码执行，避免模型"猜"结果。

---

## 🧠 问题背景

### ❌ 错误用法：让模型直接计算

```
用户：123456789 × 987654321 = ?
模型：（开始猜）大概是 121932631...（可能错）
```

### ✅ 正确用法：模型生成代码 → 执行 → 返回

```
用户：123456789 × 987654321 = ?
模型：（生成代码）print(123456789 * 987654321)
执行：121932631112635269
返回：正确答案
```

---

## 📦 安装

```bash
npx clawhub install deterministic-calc
```

---

## 🛠️ 可用函数

### `calculate(expression)`

执行数学表达式计算。

**参数：**
- `expression` (string): 数学表达式

**返回：**
```json
{
  "success": true,
  "expression": "123456789 * 987654321",
  "result": 121932631112635269
}
```

---

### `run_python(code)`

执行 Python 代码并返回结果。

**参数：**
- `code` (string): Python 代码

**返回：**
```json
{
  "success": true,
  "stdout": "121932631112635269\n",
  "stderr": "",
  "exit_code": 0
}
```

---

### `run_shell(command)`

执行 Shell 命令并返回结果。

**参数：**
- `command` (string): Shell 命令

**返回：**
```json
{
  "success": true,
  "stdout": "...",
  "stderr": "",
  "exit_code": 0
}
```

---

### `safe_eval(expression)`

安全执行数学表达式（无代码注入风险）。

**参数：**
- `expression` (string): 数学表达式

**返回：**
```json
{
  "success": true,
  "result": 42
}
```

---

## 📝 使用示例

### 数学计算

```python
from deterministic_calc import calculate

result = calculate("123456789 * 987654321")
print(result["result"])  # 121932631112635269
```

### 复杂计算

```python
from deterministic_calc import run_python

code = """
import math
result = sum(i**2 for i in range(1000))
print(result)
"""
result = run_python(code)
print(result["stdout"])  # 332833500
```

### Shell 命令

```python
from deterministic_calc import run_shell

result = run_shell("ls -la /tmp")
print(result["stdout"])
```

---

## ⚠️ 安全说明

- `calculate()` 和 `safe_eval()` 是沙箱安全的
- `run_python()` 和 `run_shell()` 可执行任意代码，需谨慎使用
- 生产环境建议只暴露 `calculate()` 和 `safe_eval()`

---

## 📄 License

MIT
