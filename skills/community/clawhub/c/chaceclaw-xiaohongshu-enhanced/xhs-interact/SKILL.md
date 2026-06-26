---
name: xhs-interact
description: 小红书互动操作。点赞、收藏、评论。包含话术模板、限流规则、防封指南。
emoji: 💬
version: "1.0.0"
triggers:
  - 点赞
  - 收藏
  - 评论
  - 互动
  - 回复
  - interact
---

# 💬 xhs-interact

> 小红书互动操作完整指南（点赞/收藏/评论）

## 何时触发

- "点赞这条笔记"
- "收藏一下"
- "写个评论"
- "回复一下"
- `/xhs-interact`

---

## 前置必检

```python
status = await mcp.check_login_status()
assert status["logged_in"], "❌ 未登录"
```

---

## 限流核心参数（必须遵守）

| 操作 | 每小时上限 | 每天上限 | 最小间隔 | 硬性限制 |
|------|-----------|---------|---------|---------|
| **点赞** | 60次 | 300次 | 60秒 | 超限封号 |
| **收藏** | 60次 | 300次 | 60秒 | 超限封号 |
| **评论** | 15次 | 30次 | 300秒 | 超限禁言 |
| **回复** | 并入评论次数 | — | — | — |

### 退避算法

```python
import random

def safe_wait(base_seconds, jitter_range=(1.1, 1.3)):
    """带随机抖动的安全等待"""
    jitter = random.uniform(*jitter_range)
    return base_seconds * jitter

# 使用
await asyncio.sleep(safe_wait(60))  # 点赞间隔 66-78秒
await asyncio.sleep(safe_wait(300)) # 评论间隔 330-390秒
```

---

## 点赞操作

### 标准点赞

```python
# 点赞笔记
result = await mcp.like_note(note_id="64xxxxxxx")

# 返回
{
    "success": true,
    "note_id": "64xxxxxxx",
    "action": "liked"  # liked / unliked
}
```

### 批量安全点赞

```python
class SafeLiker:
    def __init__(self, mcp):
        self.mcp = mcp
        self.today_count = 0
        self.hourly_count = 0
        self.last_action = time.time()
    
    async def like(self, note_id):
        # 检查每日限额
        if self.today_count >= 300:
            print("⚠️ 今日点赞已达上限（300）")
            return False
        
        # 检查每小时限额
        if self.hourly_count >= 60:
            print("⚠️ 本小时点赞已达上限（60）")
            return False
        
        # 冷却检查
        elapsed = time.time() - self.last_action
        if elapsed < 60:
            wait = 60 - elapsed
            wait_jitter = wait * random.uniform(1.1, 1.3)
            print(f"⏳ 等待 {wait_jitter:.0f}秒冷却...")
            await asyncio.sleep(wait_jitter)
        
        try:
            result = await self.mcp.like_note(note_id)
            if result.get("success"):
                self.today_count += 1
                self.hourly_count += 1
                self.last_action = time.time()
                return True
        except RateLimitError:
            print("⚠️ 触发限流，等待 10 分钟...")
            await asyncio.sleep(600)
        
        return False

# 使用
liker = SafeLiker(mcp)
for note_id in note_ids:
    await liker.like(note_id)
    print(f"已点赞 {note_id}，今日累计: {liker.today_count}")
```

### 点赞话术（主动互动）

```python
# 点赞时附带评论（增加曝光）
result = await mcp.like_note(note_id, comment="真的绝了！👍")
```

---

## 收藏操作

### 标准收藏

```python
# 收藏笔记
result = await mcp.collect_note(note_id="64xxxxxxx")

# 返回
{
    "success": true,
    "note_id": "64xxxxxxx",
    "action": "collected"  # collected / uncollected
}
```

### 收藏 + 评论组合

```python
# 推荐：先收藏，再评论，提高互动质量
await mcp.collect_note(note_id)
await asyncio.sleep(5)
await mcp.comment_note(note_id, "这篇太实用了，收藏了！")
```

---

## 评论操作

### 发表评论

```python
# 普通评论
result = await mcp.comment_note(
    note_id="64xxxxxxx",
    content="这篇笔记太有帮助了！"
)

# 返回
{
    "success": true,
    "comment_id": "xxx",
    "note_id": "64xxxxxxx"
}
```

### 评论话术模板库

```python
COMMENT_TEMPLATES = {
    # 种草类
    "planting": [
        "种草了！已加入清单～",
        "这个真的好用吗？求更多测评！",
        "已收藏，等活动入手！",
        "终于有人推荐这个了！",
    ],
    
    # 提问类（增加评论互动）
    "question": [
        "请问在哪里买的呀？",
        "多少钱入的？",
        "适合干皮还是油皮？",
        "敏感肌可以用吗？",
        "有链接吗？",
    ],
    
    # 夸赞类
    "praise": [
        "博主写得超详细！",
        "这也太用心了吧！",
        "收藏了，感谢分享！",
        "写得真好，已点赞！",
    ],
    
    # 搞笑类（增加互动）
    "humor": [
        "看完感觉钱包在瑟瑟发抖😂",
        "博主是不是偷偷在我家装了摄像头？",
        "懂了，这就去买（并没有）",
        "我的钱包已经准备好了！",
    ]
}

def random_comment(category="planting"):
    """随机选一条评论"""
    import random
    return random.choice(COMMENT_TEMPLATES[category])
```

### 评论防限流策略

```python
class SafeCommenter:
    """安全评论包装器"""
    
    DAILY_LIMIT = 30
    MIN_INTERVAL = 300  # 5分钟
    
    def __init__(self, mcp):
        self.mcp = mcp
        self.today_count = 0
        self.last_comment_time = 0
    
    async def comment(self, note_id, content):
        # 1. 检查每日限额
        if self.today_count >= self.DAILY_LIMIT:
            print(f"⚠️ 今日评论已达上限（{self.DAILY_LIMIT}）")
            return None
        
        # 2. 检查间隔
        now = time.time()
        if now - self.last_comment_time < self.MIN_INTERVAL:
            wait = self.MIN_INTERVAL - (now - self.last_comment_time)
            jitter = wait * random.uniform(1.2, 1.5)
            print(f"⏳ 等待 {jitter:.0f}秒冷却...")
            await asyncio.sleep(jitter)
        
        # 3. 执行评论
        try:
            result = await self.mcp.comment_note(note_id, content)
            if result.get("success"):
                self.today_count += 1
                self.last_comment_time = time.time()
                print(f"✅ 评论成功，今日已评: {self.today_count}/{self.DAILY_LIMIT}")
                return result
        except RateLimitError as e:
            print(f"❌ 限流触发: {e}")
            if "comment" in str(e).lower():
                print("建议：等待 4 小时后重试")
            return None
```

---

## 回复评论

```python
# 获取评论 ID
note = await mcp.get_note_detail(note_id, fetch_comments=True)
comment_id = note['comments'][0]['comment_id']

# 回复评论
result = await mcp.reply_comment(
    note_id=note_id,
    comment_id=comment_id,
    content="谢谢喜欢！有问题可以私信我～"
)
```

---

## 批量互动安全脚本

```python
async def safe_batch_interact(mcp, note_ids, action="like", delay=60):
    """批量安全互动"""
    print(f"🚀 开始批量{action}，共 {len(note_ids)} 条")
    print(f"⚠️ 警告：大量操作可能导致封号！")
    
    action_count = 0
    for note_id in note_ids:
        try:
            if action == "like":
                await mcp.like_note(note_id)
            elif action == "collect":
                await mcp.collect_note(note_id)
            elif action == "comment":
                await mcp.comment_note(note_id, random_comment())
            
            action_count += 1
            print(f"✅ [{action_count}/{len(note_ids)}] {note_id}")
            
            # 随机抖动延迟
            jitter = delay * random.uniform(1.1, 1.5)
            await asyncio.sleep(jitter)
            
        except RateLimitError:
            print(f"❌ 限流触发，停止执行")
            break
        except Exception as e:
            print(f"⚠️ 跳过 {note_id}: {e}")
            continue
    
    print(f"🏁 完成：成功 {action_count} 条")
    return action_count
```

---

## 被封禁后的处理

### 检测封禁

```python
async def check_ban_status(mcp):
    """检测是否被限流/封禁"""
    try:
        # 尝试一个简单操作
        result = await mcp.like_note("test_note_id")
        return {"banned": False, "type": "none"}
    except Exception as e:
        error_msg = str(e).lower()
        if "frequent" in error_msg or "limit" in error_msg:
            return {"banned": True, "type": "rate_limit", "message": "操作过于频繁"}
        elif "banned" in error_msg or "forbid" in error_msg:
            return {"banned": True, "type": "ban", "message": "账号被限制"}
        else:
            return {"banned": False, "type": "unknown", "message": str(e)}
```

### 恢复流程

```
限流/封禁 → 停止所有操作 → 等待 24-72 小时 → 逐步恢复（从30%频率开始）
```

---

## 互动安全检查表

```markdown
- [ ] 今日点赞 ≤ 300次
- [ ] 本小时点赞 ≤ 60次
- [ ] 点赞间隔 ≥ 60秒
- [ ] 今日评论 ≤ 30次
- [ ] 评论间隔 ≥ 300秒（5分钟）
- [ ] 评论内容无违禁词
- [ ] 不在同一时段大量操作
- [ ] 操作分散在不同时间段
```

---

*Version: 1.0.0 | Updated: 2026-04-23*