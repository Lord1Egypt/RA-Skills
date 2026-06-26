# 小红书 MCP 限流指南与防封策略

> 所有操作均有严格频率限制，超限将导致账号封禁或功能禁用。本文档为所有小红书操作的统一限流参考。

---

## ⚠️ 限流核心原则

1. **宁可慢，不要封** — 账号安全永远第一
2. **间隔 > 次数** — 保持足够冷却时间比限制操作次数更重要
3. **梯度操作** — 新账号前2周减少操作频率
4. **热操作分散** — 避免集中短时间大量操作

---

## 📊 官方限流阈值

| 操作类型 | 每小时上限 | 每天上限 | 最小冷却时间 | 备注 |
|---------|-----------|---------|------------|------|
| **搜索** | 30次 | 200次 | 120秒 | 搜索最容易被限流 |
| **点赞** | 60次 | 300次 | 60秒 | 批量点赞极易封号 |
| **收藏** | 60次 | 300次 | 60秒 | 与点赞合并计算 |
| **评论** | 15次 | 30次 | 300秒 | 最严格，超限直接禁言 |
| **关注/取关** | 20次 | 50次 | 180秒 | 批量取关比关注更危险 |
| **发布图文** | — | 3篇 | 3600秒 | 新账号1篇/天更安全 |
| **发布视频** | — | 2篇 | 7200秒 | 视频审核更严 |

---

## 🛡️ 防封操作模式

### 黄金间隔公式
```
安全间隔 = 基础冷却时间 × (1 + 随机抖动比例10-30%)
```

### 推荐操作模式

#### 模式 A：保守模式（新手账号/刚注册）
- 所有操作间隔 × 1.5
- 每天总操作数不超过上限的 50%
- 仅在白天（9:00-22:00）操作

#### 模式 B：标准模式（稳定运营账号）
- 所有操作按基础冷却时间
- 每天总操作数不超过上限的 70%
- 分散操作时间

#### 模式 C：激进模式（高权重老账号）
- 所有操作间隔 × 0.8
- 每天总操作数不超过上限的 85%
- 仍需遵守硬性上限

---

## 🔄 Token 刷新机制

### Token 有效期
- Cookie 方式：通常 7-30 天
- MCP 服务 token：通常 24 小时
- 建议每 12 小时主动刷新一次

### 刷新触发条件
```
任意 MCP 工具返回以下错误码时，触发刷新：
- 401 Unauthorized
- 403 Forbidden  
- 10003 (token过期)
- 操作返回空数据（非正常情况）
```

### 刷新流程
```python
# 伪代码 - token 刷新
def safe_call(mcp_tool, *args, **kwargs):
    try:
        result = mcp_tool(*args, **kwargs)
        return result
    except TokenExpiredError:
        # 1. 调用刷新接口
        refresh_token()
        # 2. 重试一次
        return mcp_tool(*args, **kwargs)
    except RateLimitError:
        # 1. 等待冷却
        wait(cooldown_seconds * random.uniform(1.5, 2.0))
        # 2. 重试一次
        return mcp_tool(*args, **kwargs)
```

### Token 存储位置
```
~/.config/xiaohongshu/
├── cookies.json      # 浏览器 Cookie
├── tokens.json       # API Token
└── accounts/
    └── {account_id}/
        └── token.json
```

---

## 🚫 封禁等级与应对

### 等级 1：功能限制
- **表现**：点赞/收藏失败，但仍可浏览
- **持续**：1-24 小时
- **应对**：停止所有操作，等待自然恢复

### 等级 2：账号限流
- **表现**：所有操作返回"操作过于频繁"
- **持续**：24-72 小时
- **应对**：完全停止 24 小时，之后按 30% 频率恢复

### 等级 3：临时封禁
- **表现**：需要验证，或某个功能完全不可用
- **持续**：3-7 天
- **应对**：停止所有操作 → 联系客服申诉 → 等待解封

### 等级 4：永久封禁
- **表现**：无法登录，账号回收
- **应对**：无法恢复，准备新账号

---

## 📋 操作前检查清单

每次批量操作前，必须确认：

```markdown
- [ ] 今日操作计数：
  - 搜索：X/200
  - 点赞：X/300
  - 收藏：X/300
  - 评论：X/30
  - 发布：X/3
- [ ] 上次操作时间已间隔 ≥ 60秒
- [ ] Token 有效期确认
- [ ] 账号无异常提示
- [ ] MCP 服务状态正常
```

---

## 🔧 自动保护实现

```python
class RateLimiter:
    def __init__(self):
        self.counters = {
            'search': {'count': 0, 'reset_at': 0},
            'like': {'count': 0, 'reset_at': 0},
            'comment': {'count': 0, 'reset_at': 0},
            'post': {'count': 0, 'reset_at': 0},
        }
        self.cooldowns = {
            'search': 120,
            'like': 60,
            'comment': 300,
            'post': 3600,
        }
    
    def can_proceed(self, action: str) -> tuple[bool, int]:
        """返回 (是否可以操作, 需等待秒数)"""
        now = time.time()
        c = self.counters[action]
        
        if now > c['reset_at']:
            c['count'] = 0
            c['reset_at'] = now + 3600
        
        limits = {'search': 30, 'like': 60, 'comment': 15, 'post': 3}
        if c['count'] >= limits[action]:
            return False, c['reset_at'] - now
        
        jitter = random.uniform(1.1, 1.3)
        time.sleep(self.cooldowns[action] * jitter)
        return True, 0
```

---

*Last updated: 2026-04-23 | Chaceclaw Enhanced*