# 代码审查规则库

> Code Review Rules — 按维度和语言分类的审查规则

---

## 一、安全维度 🔒

### 通用安全规则

| # | 规则 | 严重级别 | 检测模式 |
|---|------|---------|---------|
| S-01 | SQL 拼接而非参数化查询 | 🔴 | `SELECT.*\+.*\|".*".*\+` |
| S-02 | 硬编码密钥/密码/Token | 🔴 | `password\s*=\s*["']\|api_key\s*=\s*["']\|secret\s*=\s*["']` |
| S-03 | 不安全的反序列化 | 🔴 | `pickle\.load\|unserialize\|ObjectInputStream` |
| S-04 | 命令注入 | 🔴 | `exec\(|Runtime\.getRuntime\(\)\.exec\|os\.system\(` |
| S-05 | XSS 风险 — 未转义的用户输入直接输出到 HTML | 🔴 | `innerHTML\s*=.*\$\|document\.write` |
| S-06 | 不安全的随机数生成 | 🟡 | `Math\.random()\|random\.random()` (用于安全场景时) |
| S-07 | 过于宽松的 CORS 配置 | 🟡 | `Access-Control-Allow-Origin.*\*` |
| S-08 | 未验证的 URL 重定向 | 🟡 | `redirect.*request\.\|header.*Location.*\+` |
| S-09 | 敏感信息写入日志 | 🟡 | `log\.\(.*password\|print\(.*token\|console\.log\(.*secret` |
| S-10 | 缺少认证/授权检查 | 🟡 | 公开 API 端点没有 auth middleware |

### Java 安全规则

| # | 规则 | 严重级别 |
|---|------|---------|
| S-J01 | 使用 `java.security.MessageDigest` 但未指定安全算法 | 🔴 |
| S-J02 | Spring Security 配置中 `permitAll()` 使用不当 | 🔴 |
| S-J03 | 未关闭的数据库连接/文件流（缺少 try-with-resources） | 🟡 |
| S-J04 | 在日志中打印完整的 HttpServletRequest body | 🟡 |

### Python 安全规则

| # | 规则 | 严重级别 |
|---|------|---------|
| S-P01 | `eval()` 或 `exec()` 处理用户输入 | 🔴 |
| S-P02 | Django `DEBUG = True` 在生产环境 | 🔴 |
| S-P03 | Flask `secret_key` 硬编码或过弱 | 🔴 |
| S-P04 | `subprocess` 使用 `shell=True` | 🟡 |

### Go 安全规则

| # | 规则 | 严重级别 |
|---|------|---------|
| S-G01 | `crypto/md5` 或 `crypto/sha1` 用于安全场景 | 🔴 |
| S-G02 | `math/rand` 用于生成安全随机数 | 🔴 |
| S-G03 | HTTP 服务未设置超时 | 🟡 |

---

## 二、性能维度 ⚡

### 通用性能规则

| # | 规则 | 严重级别 | 检测说明 |
|---|------|---------|---------|
| P-01 | 循环内执行数据库查询（N+1 问题） | 🔴 | for/while 循环体内有 SQL 查询或 ORM 查询 |
| P-02 | O(n²) 或更高复杂度算法处理大数据集 | 🟡 | 嵌套循环且内层循环与外层循环使用相同数据 |
| P-03 | 在循环内创建不可变对象（如 Java String 拼接） | 🟡 | `String += ` 在循环内 |
| P-04 | 未使用分页的大数据量查询 | 🟡 | `SELECT *` 无 LIMIT 且无分页 |
| P-05 | 频繁的小文件 I/O 替代批量操作 | 🔵 | 循环内 open/write/close |
| P-06 | 可以并行但串行执行的独立任务 | 🔵 | 顺序 await 多个无依赖的异步操作 |
| P-07 | 缓存可复用的计算结果 | 🔵 | 重复计算相同值 |
| P-08 | 未关闭的资源（连接/流/文件） | 🟡 | 缺少 finally/close 保障 |

### Java 性能规则

| # | 规则 | 严重级别 |
|---|------|---------|
| P-J01 | HashMap 初始容量过小导致频繁扩容 | 🔵 |
| P-J02 | 使用 `LinkedList` 而非 `ArrayList`（随机访问场景） | 🔵 |
| P-J03 | BigDecimal 构造使用 double 而非 String | 🟡 |
| P-J04 | 未使用连接池 | 🔴 |

### Python 性能规则

| # | 规则 | 严重级别 |
|---|------|---------|
| P-P01 | 列表推导替代 map/filter 的简单场景（可读性换性能） | 🔵 |
| P-P02 | 使用 Python 循环替代 numpy 向量化操作（数值计算） | 🟡 |
| P-P03 | 未使用 `__slots__` 的大量实例化类 | 🔵 |

---

## 三、可维护性维度 🔧

### 通用可维护性规则

| # | 规则 | 严重级别 | 说明 |
|---|------|---------|------|
| M-01 | 方法/函数超过 50 行 | 🟡 | 拆分为更小的函数 |
| M-02 | 嵌套超过 3 层的 if/for | 🟡 | 提取方法或使用卫语句 |
| M-03 | 重复代码块（>5 行相似） | 🟡 | 提取公共方法 |
| M-04 | 魔法数字/字符串未提取为常量 | 🔵 | 定义命名常量 |
| M-05 | 函数参数超过 4 个 | 🔵 | 使用对象/结构体封装 |
| M-06 | 过于通用的命名（data/info/result/temp） | 🔵 | 使用具体描述性命名 |
| M-07 | 缺少必要的注释（复杂逻辑/业务规则） | 🔵 | 添加为什么（why）的注释 |
| M-08 | 过多的注释（注释掉的代码） | 🔵 | 删除无用代码，版本控制负责历史 |
| M-09 | 上帝类/上帝函数（职责过多） | 🟡 | 单一职责原则 |
| M-10 | 硬编码的配置值 | 🔵 | 移到配置文件 |

### 命名规范

| 语言 | 类/类型 | 方法/函数 | 变量 | 常量 |
|------|--------|---------|------|------|
| Java | PascalCase | camelCase | camelCase | UPPER_SNAKE |
| Python | PascalCase | snake_case | snake_case | UPPER_SNAKE |
| Go | PascalCase（导出）/ camelCase（未导出） | PascalCase/camelCase | camelCase | 不推荐常量命名 |
| JS/TS | PascalCase | camelCase | camelCase | UPPER_SNAKE |

---

## 四、逻辑维度 🧩

### 通用逻辑规则

| # | 规则 | 严重级别 | 说明 |
|---|------|---------|------|
| L-01 | 未处理的 null/None/nil 返回值 | 🔴 | 空指针是头号 bug |
| L-02 | 数组越界风险（循环边界条件） | 🔴 | off-by-one 错误 |
| L-03 | 竞态条件（并发修改共享状态） | 🔴 | 需要同步/锁 |
| L-04 | 浮点数精度问题（金额用 float/double） | 🟡 | 使用 BigDecimal 或整数分 |
| L-05 | 资源泄漏（异常路径未关闭） | 🟡 | try-with-resources / finally |
| L-06 | 错误的异常处理（吞掉异常或 catch Exception） | 🟡 | 具体异常类型 + 适当处理 |
| L-07 | 死代码（永远不会执行的分支） | 🟡 | if (false) / 永假条件 |
| L-08 | 边界条件未覆盖（空集合、0、负数） | 🟡 | 缺少边界检查 |
| L-09 | 时区问题（未指定时区的日期操作） | 🔵 | 使用 UTC 或明确指定时区 |
| L-10 | 编码问题（未指定字符集的字符串操作） | 🔵 | UTF-8 为默认 |

---

## 五、风格维度 📐

### 通用风格规则

| # | 规则 | 严重级别 |
|---|------|---------|
| T-01 | 不一致的缩进（Tab vs Space 混用） | 🔵 |
| T-02 | 行长度超过 120 字符 | 🔵 |
| T-03 | 未使用的 import / 变量 | 🔵 |
| T-04 | 缺少文件头注释（模块/类说明） | 🔵 |
| T-05 | TODO/FIXME/HACK 注释未关联 issue | 🔵 |

### 最佳实践对照

| 实践 | 说明 |
|------|------|
| DRY | 不要重复自己（Don't Repeat Yourself） |
| KISS | 保持简单（Keep It Simple, Stupid） |
| YAGNI | 你不需要它（You Aren't Gonna Need It） |
| SOLID | 单一职责、开闭、里氏替换、接口隔离、依赖倒置 |
| Fail Fast | 尽早失败，快速反馈 |

---

## 六、严重级别升级规则

以下情况自动升级问题严重级别：

| 情况 | 升级 |
|------|------|
| 问题出现在核心/关键路径代码中 | +1 级 |
| 问题影响范围广（公共 API / 基础库） | +1 级 |
| 问题可能影响用户数据安全 | 升至 🔴 |
| 同一类型问题出现 3 次以上 | +1 级（系统性问题） |

---

## 七、审查排除规则

以下情况不需要标记为问题：

- 代码风格与项目现有风格一致（即使不是最佳实践）
- 测试代码中的简化写法（如硬编码测试数据）
- 配置文件中的默认值
- 已经有 TODO 注释且关联了 issue
- 框架生成的代码
