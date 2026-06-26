---
name: code-sandbox
description: 代码沙箱 - 原创技能。安全执行未验证的AI生成代码，防止恶意代码、系统破坏或意外损害。适用于代码审查、安全验证、AI编程辅助等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [sandbox, security, code-execution, isolation, safety]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 安全策略完整
- [x] 隔离机制清晰
- [x] 危险模式覆盖全
- [x] 无语法错误

---

# Code Sandbox - 代码沙箱

> 原创技能 | 激活词: 安全执行 / 沙箱运行 / 验证代码

## 核心问题

AI生成的代码可能包含：
- 恶意代码
- 破坏性操作
- 无限循环
- 系统调用风险
- 数据泄露风险

直接运行非常危险！

## 沙箱架构

```
┌─────────────────────────────────────────────┐
│              代码沙箱                        │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│  │ 资源限制 │   │ 网络隔离 │   │ 文件隔离 │   │
│  │         │   │         │   │         │   │
│  │ CPU限制  │   │ 无外网   │   │ 只读目录 │   │
│  │ 内存限制  │   │ 无DNS   │   │ 临时目录 │   │
│  │ 时间限制  │   │ 无socket│   │ 无敏感路径│   │
│  └─────────┘   └─────────┘   └─────────┘   │
│                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│  │ 危险API │   │ 进程限制 │   │ 监控审计 │   │
│  │         │   │         │   │         │   │
│  │ rm -rf  │   │ 禁用fork │   │ 操作日志 │   │
│  │ curl    │   │ 禁用spawn│   │ 资源使用 │   │
│  │ system  │   │ 子进程数 │   │ 安全告警 │   │
│  └─────────┘   └─────────┘   └─────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

## 安全策略

### 1. 资源限制

```python
RESOURCE_LIMITS = {
    'cpu_time': 10,        # 最大10秒
    'memory': 256,        # 最大256MB
    'disk_write': 10,     # 最多写10MB
    'processes': 5,        # 最多5个进程
    'threads': 10,         # 最多10个线程
}
```

### 2. 网络限制

```python
NETWORK_RESTRICTIONS = {
    'allow_outbound': False,    # 禁止出站连接
    'allow_inbound': False,     # 禁止入站连接
    'allow_dns': False,         # 禁止DNS查询
    'allow_internet': False,     # 禁止访问互联网
}
```

### 3. 文件系统限制

```python
FILESYSTEM_RULES = {
    'read_whitelist': ['/tmp', '/sandbox'],
    'write_whitelist': ['/tmp/sandbox'],
    'blocked_paths': [
        '/',
        '/home',
        '/root',
        '/etc',
        '/var',
        '*.key',
        '*.pem',
        '.env',
    ],
    'max_file_size': 10 * 1024 * 1024,  # 10MB
}
```

### 4. 危险API黑名单

```python
DANGEROUS_APIS = {
    'python': [
        'os.system',
        'os.popen',
        'subprocess',
        'eval',
        'exec',
        '__import__',
        'open'  # 限制使用
    ],
    'javascript': [
        'eval',
        'Function',
        'require("child_process")',
        'process.binding',
        'fs.delete',
    ],
}
```

## 危险模式检测

### 高危模式

```python
HIGH_RISK_PATTERNS = [
    r'rm\s+-rf\s+/',                    # 删除根目录
    r'format\s+.*:',                     # 格式化磁��
    r'drop\s+database',                  # 删除数据库
    r'chmod\s+777',                      # 权限过大
    r'eval\s*\(',                        # 动态执行
    r'system\s*\(',                      # 系统命令
    r'shell_exec',                       # Shell执行
]
```

### 中危模式

```python
MEDIUM_RISK_PATTERNS = [
    r'fetch\s*\(',                      # 网络请求
    r'curl\s+',                         # curl命令
    r'wget\s+',                         # wget命令
    r'\.env',                           # 访问环境变量
    r'password',                        # 密码相关
    r'secret',                          # 密钥相关
]
```

## 沙箱执行流程

```
1. 代码输入
      ↓
2. 静态分析 (危险模式检测)
      ↓
3. 修改代码 (包装危险调用)
      ↓
4. 沙箱配置 (设置资源限制)
      ↓
5. 执行代码 (在隔离环境)
      ↓
6. 结果收集 (输出/错误/资源)
      ↓
7. 清理环境
```

## 执行示例

### 安全代码

```python
def safe_code():
    # 这段代码会被允许执行
    result = []
    for i in range(10):
        result.append(i * 2)
    return result

# 输出: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### 危险代码 (被拦截)

```python
def dangerous_code():
    import os
    os.system('rm -rf /')  # ❌ 拦截!

# 错误: 检测到危险操作 "rm -rf /"
# 建议: 这是破坏性操作，禁止执行
```

## 输出格式

```markdown
## 沙箱执行报告

### 执行状态
- **状态**: ✅ 安全通过 / ❌ 已拦截
- **执行时间**: 0.23秒
- **内存使用**: 12MB
- **CPU使用**: 0.15秒

### 安全检查
✅ 危险模式检测: 通过
✅ 资源限制: 未超限
✅ 文件系统访问: 合规
✅ 网络请求: 已阻止

### 执行结果
```python
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### 警告
⚠️ 代码访问了临时目录
⚠️ 代码包含循环操作
```

## 执行结果处理

### 通过

```python
SANDBOX_PASS = {
    'status': 'passed',
    'output': '...',
    'execution_time': 0.23,
    'memory_used': 12,
    'warnings': [],
}
```

### 拒绝

```python
SANDBOX_REJECT = {
    'status': 'rejected',
    'reason': 'dangerous_pattern',
    'pattern': 'rm -rf /',
    'line': 5,
    'suggestion': '删除根目录是破坏性操作',
}
```

### 超时

```python
SANDBOX_TIMEOUT = {
    'status': 'timeout',
    'reason': 'infinite_loop',
    'iteration_count': 100000,
    'suggestion': '检查循环终止条件',
}
```

## 集成建议

| 配合技能 | 效果 |
|---------|------|
| hallucination-detector | 先检测幻觉再沙箱运行 |
| workflow-verifier | 验证安全后执行 |
| iteration-optimizer | 优化时安全执行测试代码 |

## 原创性声明

本技能为原创，融合了：
- 容器化隔离技术
- 系统调用过滤
- 资源配额管理
- 危险模式识别

---

**作者**: laosi
**创建日期**: 2026-04-28