"""
错误模式库 - Error Pattern Library

四类错误的正则表达式模式定义。
模式匹配不区分大小写。
"""

# ============================================================
# TRANSIENT（临时错误）- 可自动重试
# ============================================================
TRANSIENT_PATTERNS = [
    # 超时类
    r"timeout",
    r"timed out",
    r"连接超时",
    r"请求超时",
    r"read timed out",
    r"connect timed out",
    # 限流类
    r"rate limit",
    r"429",
    r"too many requests",
    r"限流",
    r"throttl",
    r"quota exceeded",
    # 连接类
    r"connection reset",
    r"connection refused",
    r"connection aborted",
    r"broken pipe",
    r"network unreachable",
    r"dns resolution",
    r"no route to host",
    # 服务不可用
    r"temporarily unavailable",
    r"503",
    r"502",
    r"bad gateway",
    r"service unavailable",
    # 重试类
    r"please retry",
    r"try again later",
    r"稍后重试",
]

# ============================================================
# PERMANENT（永久错误）- 不可恢复，报告用户
# ============================================================
PERMANENT_PATTERNS = [
    # 权限类
    r"permission denied",
    r"403",
    r"forbidden",
    r"access denied",
    r"insufficient permissions",
    r"privilege",
    # 资源不存在
    r"not found",
    r"404",
    r"does not exist",
    r"no such file",
    r"resource not found",
    r"entity not found",
    # 认证类
    r"unauthorized",
    r"401",
    r"invalid api key",
    r"authentication failed",
    r"invalid token",
    r"expired token",
    r"credentials",
    # 冲突类
    r"409",
    r"conflict",
    r"already exists",
    r"duplicate",
]

# ============================================================
# VALIDATION（验证错误）- 回传模型修复
# ============================================================
VALIDATION_PATTERNS = [
    # 语法类
    r"syntax\s*error",
    r"parse\s*error",
    r"unexpected token",
    # 编译类
    r"compilation failed",
    r"编译失败",
    r"build failed",
    r"compile error",
    # 测试类
    r"test failed",
    r"assertion\s*error",
    r"测试失败",
    r"assertion failed",
    # Lint/类型检查
    r"lint error",
    r"flake8",
    r"mypy",
    r"pylint",
    r"eslint",
    r"type\s*error",
    r"name\s*error",
    r"import\s*error",
    r"indentation\s*error",
    r"attribute\s*error",
    r"value\s*error",
    r"key\s*error",
    # 验证类
    r"验证失败",
    r"validation error",
    r"schema error",
    r"invalid format",
]

# ============================================================
# CONTEXT（上下文错误）- 触发压缩
# ============================================================
CONTEXT_PATTERNS = [
    # Token 限制
    r"token limit",
    r"context length",
    r"too many tokens",
    r"max tokens",
    r"context window",
    r"上下文超限",
    r"token count",
    r"token exceeded",
    # 压缩相关
    r"compression failed",
    r"压缩失败",
    # 输入过长
    r"input too long",
    r"prompt too long",
    r"message too long",
    r"content too large",
    r"request too large",
    # 内存/上下文溢出
    r"out of memory",
    r"memory limit",
    r"context overflow",
]
