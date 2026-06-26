# 代码验证钩子（Code-Verify Hook）

## 概述

自动检测AI输出中的代码，验证其正确性。

## 钩子类型

### 1. 语法验证钩子

```python
# 触发条件
code_blocks = [
    r'```python\n.*?\n```',  # Python代码块
    r'```javascript\n.*?\n```',  # JavaScript代码块
    r'```bash\n.*?\n```',  # Bash代码块
]

# 验证动作
def verify_syntax(code, language):
    # 1. 语法检查
    # 2. 返回验证结果
    return {
        "verified": True/False,
        "errors": [],
        "confidence": "确定/不确定"
    }
```

### 2. 依赖验证钩子

```python
# 触发条件
import_patterns = [
    r'import\s+\w+',  # Python import
    r'require\s*\(',  # Node.js require
    r'from\s+\w+\s+import',  # Python from import
]

# 验证动作
def verify_dependencies(code):
    # 1. 提取所有依赖
    # 2. 检查是否已安装
    # 3. 检查版本兼容性
    return {
        "verified": True/False,
        "missing_deps": [],
        "confidence": "确定/不确定"
    }
```

### 3. API验证钩子

```python
# 触发条件
api_patterns = [
    r'\w+\.\w+\(',  # 方法调用
    r'fetch\s*\(',  # fetch API
    r'requests\.\w+',  # requests库
]

# 验证动作
def verify_api(api_call):
    # 1. 搜索确认API存在
    # 2. 检查API签名
    # 3. 验证参数正确性
    return {
        "verified": True/False,
        "api_exists": True/False,
        "confidence": "确定/不确定"
    }
```

### 4. 执行验证钩子

```python
# 触发条件
executable_patterns = [
    r'```python\n.*?\n```',  # Python代码
    r'```bash\n.*?\n```',  # Bash脚本
    r'```javascript\n.*?\n```',  # JavaScript代码
]

# 验证动作
def verify_execution(code, language):
    # 1. 在沙箱中执行
    # 2. 捕获输出和错误
    # 3. 返回验证结果
    return {
        "verified": True/False,
        "output": "",
        "errors": [],
        "confidence": "确定/不确定"
    }
```

## 钩子执行流程

```
1. 检测输出中的代码块
2. 提取代码内容
3. 执行验证动作
4. 返回验证结果
5. 根据结果处理：
   - 验证通过 → 继续
   - 验证失败 → 标注错误，建议修正
   - 无法验证 → 标注 [需验证]
```

## 钩子配置

```yaml
hooks:
  code-verify:
    enabled: true
    auto_trigger: true
    sandbox: true
    timeout: 30
    actions:
      on_syntax_error: "fix_and_retry"
      on_missing_dep: "install_or_warn"
      on_api_not_found: "search_and_suggest"
      on_execution_error: "debug_and_retry"
```

## 验证级别

### 严格模式（Strict）

```
- 语法检查 ✓
- 依赖检查 ✓
- API检查 ✓
- 执行检查 ✓
- 回读校验 ✓
```

### 平衡模式（Balanced）

```
- 语法检查 ✓
- 依赖检查 ✓
- API检查 ✓
- 执行检查 ✗（可选）
- 回读校验 ✗（可选）
```

### 快速模式（Fast）

```
- 语法检查 ✓
- 依赖检查 ✗（可选）
- API检查 ✗（可选）
- 执行检查 ✗
- 回读校验 ✗
```
