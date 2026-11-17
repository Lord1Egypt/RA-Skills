---
name: error-classifier
version: 1.0.0
description: "四类错误分类与处理引擎。自动识别临时错误/永久错误/验证错误/上下文错误，并提供相应处理策略（重试/报告/修复/压缩）。当工具调用失败、API 报错、编译测试出错、上下文超限时自动分类并给出处理建议。"
tags: ["error-handling", "retry", "classification", "exponential-backoff"]
---

# Error Classifier

四类错误自动分类与处理引擎。

## 错误类型

| 类型 | 含义 | 处理策略 | 典型场景 |
|------|------|----------|----------|
| TRANSIENT | 临时错误 | 自动重试（指数退避 1s/2s/4s） | timeout, 429, 503, 连接重置 |
| PERMANENT | 永久错误 | 报告用户，不可恢复 | 403, 404, 权限不足, API key 无效 |
| VALIDATION | 验证错误 | 回传模型修复 | 语法错误, 测试失败, 类型错误 |
| CONTEXT | 上下文错误 | 触发压缩 | token 超限, 上下文窗口溢出 |

## 分类优先级

CONTEXT > VALIDATION > PERMANENT > TRANSIENT

当错误消息同时匹配多种类型时，优先级高的类型胜出。

## 使用方法

### 基本用法

```python
import sys
sys.path.insert(0, "skills/error-classifier/scripts")

from classifier import ErrorClassifier, ErrorType

classifier = ErrorClassifier()

# 分类错误
error_type = classifier.classify(exception)
# → ErrorType.TRANSIENT / PERMANENT / VALIDATION / CONTEXT

# 获取处理动作
action = classifier.handle(exception, context={"retry_count": 0})
# action.action → "retry" / "report_user" / "fix" / "compress"
# action.message → 人类可读的处理说明
# action.retry_delay → 重试等待秒数（仅 retry 动作）
```

### 带重试的执行

```python
from classifier import ErrorClassifier

classifier = ErrorClassifier()

def call_api():
    # 你的 API 调用
    ...

try:
    result = classifier.execute_with_retry(call_api, on_retry=lambda a, d, e: print(f"重试 {a+1}/3"))
except Exception as e:
    print(f"全部重试失败: {e}")
```

### 便捷函数

```python
from classifier import classify_error, handle_error, get_retry_delay

error_type = classify_error(exception)
action = handle_error(exception, context={"retry_count": 0})
delay = get_retry_delay(attempt=0)  # → 1
```

## 指数退避策略

```
第1次重试: 等待 1s  (BASE_DELAY × 2^0)
第2次重试: 等待 2s  (BASE_DELAY × 2^1)
第3次重试: 等待 4s  (BASE_DELAY × 2^2)
超过3次:  报告用户
```

## 错误模式库

共 50+ 种错误模式，覆盖中英文场景：

- **TRANSIENT**: timeout, timed out, 连接超时, rate limit, 429, too many requests, 限流, connection reset, 503, 502 ...
- **PERMANENT**: permission denied, 403, forbidden, not found, 404, unauthorized, 401, invalid api key, access denied ...
- **VALIDATION**: syntax error, compilation failed, 编译失败, test failed, assertion error, 测试失败, type error, import error ...
- **CONTEXT**: token limit, context length, max tokens, 上下文超限, prompt too long, input too long ...

## 集成点

- **coding-framework** Step 5.5（异常处理）：工具调用失败时自动分类
- **daily-agent** 任务调度：根据错误类型决定重试/报告/修复/压缩
- **context-compressor** 上下文压缩：CONTEXT 错误触发压缩流程

## 文件结构

```
skills/error-classifier/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── classifier.py           # 错误分类器核心
│   ├── patterns.py             # 错误模式库（50+ 种模式）
│   └── test_classifier.py      # 测试用例
└── references/
    └── retry_strategies.md     # 重试策略详细说明
```
