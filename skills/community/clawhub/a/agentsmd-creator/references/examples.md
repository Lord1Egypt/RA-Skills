# 编程原则示例

> 来源：[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)

Real-world code examples demonstrating the four principles. Each example shows what LLMs commonly do wrong and how to fix it.

---

## 1. 编码前先思考

### 示例 1：隐藏的假设

**用户请求：** "Add a feature to export user data"

**❌ 错误做法（隐含假设）**

```python
def export_users(format='json'):
    """Export all users to a file."""
    users = User.query.all()
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    return f"Exported {len(users)} users"
```

**问题：** 假设导出全部用户（隐私？分页？）；未确认文件存放位置；未确认包含哪些字段；未确认 CSV 列名是否匹配实际数据结构。

**✅ 正确做法（亮出假设）**

```
实施前需要确认：
1. 范围：导出全部用户还是筛选子集？（隐私影响）
2. 方式：浏览器下载 / 后台任务邮件通知 / API 直接返回？
3. 字段：导出哪些用户字段？（部分可能敏感）
4. 量级：通常多少用户？（影响方案选择）

最简方案：添加分页 JSON API 端点。文件导出需要更多信息。
你的偏好是？
```

### 示例 2：多种理解

**用户请求：** "Make the search faster"

**❌ 错误做法（静默选择）**

```python
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # ... 200 lines of optimization code
```

**✅ 正确做法**

```
"更快"可能指：
1. 响应时间更快（500ms → <100ms）— 加索引、缓存
2. 并发量更大（吞吐量）— 异步、连接池
3. 感知速度更快（UX）— 渐进式加载

当前搜索约 500ms，你最关心哪方面？
```

---

## 2. 简单至上

### 示例 1：过度抽象

**用户请求：** "Add a function to calculate discount"

**❌ 错误做法** — Strategy 模式 + ABC + Enum + dataclass + Config 类，30+ 行只为一个乘法。

**✅ 正确做法**

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)
```

**何时增加复杂度：** 真正需要多种折扣类型时再加，到时候再重构。

### 示例 2：推测性功能

**用户请求：** "Save user preferences to database"

**❌ 错误做法** — 自动加了缓存、校验、合并、通知，没人要的功能全上了。

**✅ 正确做法**

```python
def save_preferences(db, user_id: int, preferences: dict):
    """Save user preferences to database."""
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

**后续按需添加：** 缓存（性能不够时）、校验（出现脏数据时）、合并（需求出现时）。

---

## 3. 手术式改动

### 示例 1：搭便车重构

**用户请求：** "Fix the bug where empty emails crash the validator"

**❌ 错误做法** — 顺手改进了邮箱校验、增加了用户名校验、改了注释、加了 docstring。

**✅ 正确做法** — 只改了处理空邮箱那几行，其余不动。

### 示例 2：风格漂移

**用户请求：** "Add logging to the upload function"

**❌ 错误做法** — 改了引号风格、加了类型提示、加了 docstring、重排了空白、改了布尔逻辑。

**✅ 正确做法** — 保持单引号、不加类型提示、沿用既有布尔写法，只加日志。

---

## 4. 目标驱动型执行

### 示例 1：模糊 vs 可验证

**用户请求：** "Fix the authentication system"

**❌ 错误做法** — "Review → Identify → Improve → Test"，没有明确成功标准。

**✅ 正确做法**

```
如果是「改密码后旧 session 未失效」：
1. 写测试：改密码 → 验证旧 session 失效 → 确认失败（复现 bug）
2. 实现：改密码时失效 session → 确认测试通过
3. 边界：多活跃 session、并发修改 → 确认额外测试通过
4. 回归：现有 auth 测试全部通过 → 确认全绿
```

### 示例 2：多步迭代

**用户请求：** "Add rate limiting to the API"

**❌ 错误做法** — 一次性 300 行提交，Redis + 多策略 + 配置系统 + 监控。

**✅ 正确做法** — 每步独立可验证：

1. 内存限流（单端点）→ 验证：100 次请求前 10 成功其余 429
2. 提取为中间件（全部端点）→ 验证：各端点均生效，现有测试通过
3. Redis 后端（多服务器）→ 验证：跨实例共享计数
4. 配置化（按端点）→ 验证：不同端点不同限额

### 示例 3：先复现再修复

**用户请求：** "The sorting breaks when there are duplicate scores"

**❌ 错误做法** — 直接改 sort 逻辑，没有先确认 bug。

**✅ 正确做法** — 先写复现测试 → 确认失败 → 再用稳定排序修复 → 确认通过。

---

## 反模式总结

| 原则 | 反模式 | 修正 |
|------|--------|------|
| 编码前先思考 | 静默假设文件格式、字段、范围 | 显式列出假设，请求澄清 |
| 简单至上 | 一次计算用 Strategy 模式 | 一个函数搞定，复杂度真正需要时再加 |
| 手术式改动 | 修 bug 时顺手改引号、加类型提示 | 只改修 bug 必须改的行 |
| 目标驱动型执行 | "我来 review 并改进" | "写测试复现 bug → 修通 → 验证无回归" |

## 关键洞察

"过度复杂"的代码并不是明显错误——它们遵循设计模式和最佳实践。问题在于**时机**：在不需要的时候加了复杂度，导致更难理解、更多 bug、更慢实现、更难测试。

简单版本的优势：更容易理解、实现更快、更容易测试、真正需要时再重构。

**好代码是简单解决今天的问题，而不是提前解决明天的问题。**
