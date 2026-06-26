---
name: douyin-comment-reply
description: 琪琪抖音评论监控与自动回复。两阶段解耦架构：Fetch（浏览器拉取→暂存JSON）+ Process（LLM 智能分类+安全审核+逐条回复+重试队列）。
---

# 琪琪抖音评论监控与自动回复 v2

> 账号：琪琪故事花园（抖音号：1167327950）
> 人设：5岁小女孩琪琪，讲睡前故事

## 架构总览

```
Phase A: Fetch（浏览器）          Phase B: Process（不依赖浏览器）
┌──────────────────────┐         ┌──────────────────────────┐
│ 1. 浏览器拉评论       │         │ 1. 读 staged/*.json      │
│ 2. 去重 → 暂存 JSON  │ ──────▶ │ 2. LLM 智能分类+安全审核 │
│ 3. 更新 state.json   │         │ 3. 逐条回复（重试3次）   │
│ 4. 浏览器挂？跳过    │         │ 4. 归档30天旧记录        │
└──────────────────────┘         │ 5. 飞书通知              │
                                 └──────────────────────────┘
```

## 文件结构

```
skills/douyin-comment-reply/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── comment_state.py        # JSON 原子状态管理
│   └── douyin_comment_fetch.py # 浏览器抓取指令生成
```

状态文件位置：
```
Obsidian/琪琪OPC项目/12-评论管理/
├── state.json                  # 主状态（已回复/已屏蔽 ID 列表）
├── staged/                     # 待处理评论（每个评论一个 JSON）
├── archive/                    # 30天归档
└── 评论记录.md                 # 人类可读的 Markdown 日志（保留）
```

## Phase A: Fetch 步骤

### 1. 浏览器导航
```
URL: https://creator.douyin.com/
```

### 2. 检查登录状态
snapshot 确认已登录琪琪故事花园账号

### 3. 进入创作者中心评论页
```
URL: https://creator.douyin.com/creator-micro/content/manage
```

### 4. 逐个视频读取评论
- 获取最近 5 个有评论数的视频
- 对每个视频：进入评论页 → snapshot → 提取评论数据

### 5. 输出原始数据到 JSON
```json
{
  "account": {"fans": 27, "likes": 31, "videos": 14, "following": 559},
  "videos": [
    {"title": "春天的生日会", "comments": [
      {"user": "小淘气", "text": "很精彩", "timestamp": "05-20 15:30"}
    ]}
  ]
}
```
保存到 `/tmp/douyin_comments_raw.json`

### 6. 调用状态管理脚本去重暂存
```bash
python3 skills/douyin-comment-reply/scripts/douyin_comment_fetch.py \
  --mode fetch --raw /tmp/douyin_comments_raw.json
```

### 降级：浏览器不可用
- 输出错误日志
- 飞书通知：「⚠️ 浏览器不可用，跳过 Fetch。已有暂存评论仍会处理」
- **不停止流程** → 继续 Phase B

## Phase B: Process 步骤

### 1. 读取暂存评论
```bash
python3 skills/douyin-comment-reply/scripts/comment_state.py list pending
```

### 2. 逐条处理
对每条评论执行：

**a. 安全审核**（关键词 + LLM 判断）
- 屏蔽词：约吗/加微信/私聊/电话/见面/地址/http/扫码
- 敏感内容：涉及个人信息、不当言论、广告
- 不确定 → 标记为 pending_review，飞书通知 Vincent 手动处理

**b. LLM 生成回复**
- 人设：5岁小女孩琪琪
- 风格：友好、可爱、简短（15-30字）
- 不透露真实个人信息（年龄说5岁，生日说7月10日）
- 根据评论类型智能回复：
  - 夸赞 → 感谢+开心
  - 催更 → 安抚+期待
  - 提问 → 简短回答
  - 互动 → 友好回应
  - 通用 → 温暖感谢

**c. 浏览器发送回复**
- 导航到对应视频评论页
- 找到评论 → 点击回复 → 输入回复内容 → 提交
- 失败 → 重试（最多3次，间隔5秒）
- 3次全失败 → 标记 failed，下次重试

**d. 更新状态**
```bash
# 成功后更新 state.json
# （由 comment_state.py 的 mark_replied() 处理）
```

### 3. 归档旧记录
```bash
python3 skills/douyin-comment-reply/scripts/comment_state.py archive
```

### 4. 更新 Markdown 日志（人类可读）
- 追加今日检查摘要到 `评论记录.md`
- 包含：新评论数、回复数、屏蔽数、待审核数、失败数

### 5. 飞书通知
```
👧 琪琪评论监控 | YYYY-MM-DD HH:MM

📊 Fetch: ✅/❌（浏览器状态）
📥 新评论: X 条
✅ 已回复: X 条
🚫 已屏蔽: X 条
⏸️ 待审核: X 条
❌ 回复失败: X 条
📦 累计已回复: X 条

📈 账号概况: 粉丝 X | 获赞 X | 作品 X
```

## 安全规则

### 自动屏蔽（不回复）
- 含联系方式：微信/电话/QQ/邮箱
- 约会/见面邀请
- 广告/推广/扫码
- 含 URL
- 不当言论（脏话、人身攻击）

### 需人工审核（暂存不回复，飞书通知）
- 询问真实姓名/学校/地址
- 过于热情的"喜欢你""爱你"类
- 评论者账号异常（新号、无头像）
- LLM 判断不确定的

### 可自动回复
- 夸赞类（可爱/好听/好棒）
- 催更类（什么时候更新/新故事）
- 互动类（明天还有吗/想听）
- 提问类（几岁/叫什么）— 按人设回答
- 感谢类（谢谢/辛苦了）
- 通用友好评论

## 容错机制

| 故障场景 | 处理方式 |
|----------|----------|
| 浏览器超时 | 跳过 Fetch，继续 Process 已有暂存 |
| 回复失败 | 自动重试3次，仍失败标记 failed |
| 状态文件损坏 | 从 staged/ 重建 |
| Markdown 写入失败 | 不影响 JSON 状态，下次重试 |
| 无新评论 | 正常输出"无新评论"通知 |

## 维护

### 手动添加评论（浏览器不可用时）
```bash
python3 skills/douyin-comment-reply/scripts/douyin_comment_fetch.py \
  --mode manual --video "视频名" --user "用户名" --text "评论内容"
```

### 查看状态
```bash
python3 skills/douyin-comment-reply/scripts/comment_state.py stats
```

### 查看待处理评论
```bash
python3 skills/douyin-comment-reply/scripts/comment_state.py list pending
```

### 归档
```bash
python3 skills/douyin-comment-reply/scripts/comment_state.py archive
```
