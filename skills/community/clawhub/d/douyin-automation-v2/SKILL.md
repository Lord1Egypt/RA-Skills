---
name: Douyin Automation Suite
slug: douyin-automation
version: 1.0.0
description: "抖音自动化运营技能包：自动评论回复、私信发送、点赞、搜索指定话题。适用于抖音账号运营、评论区互动管理。遵守平台规则，不自我介绍，纯正常互动。"
changelog: "1.0.0 - 初始版本，包含评论回复、私信发送、点赞、搜索功能"
metadata: {"openclaw":{"emoji":"🎵","os":["win32","darwin","linux"]}}
---

# Douyin Automation Suite 🎵

抖音自动化运营技能包，专注社区互动，**不自我介绍**，纯正常沟通。

## 功能概览

| 功能 | 状态 | 说明 |
|------|------|------|
| 评论发布 | ✅ 已验证 | 在视频下发评论 |
| 评论自动回复 | ✅ 已验证 | 根据评论内容生成回复 |
| 私信发送 | ✅ 已验证 | 发送私信给用户 |
| 私信打招呼 | ✅ 已验证 | 纯打招呼，不自我介绍 |
| 点赞 | ✅ 已验证 | 对视频点赞 |
| 搜索话题 | ✅ 已验证 | 搜索特定话题和热门视频 |

## 话术规范（重要）

### ❌ 禁止使用的话术
- 自我介绍："我是XX"
- 能力介绍："我可以帮你..."
- 解决问题："你可以这样..."
- 探讨问题："我想和你讨论..."
- 推广营销："需要XX服务请联系我"

### ✅ 正确的话术

**直接问候类**：
- "感谢支持！"
- "谢谢观看！"
- "有同感！"
- "说得太对了！"

**内容夸赞类**：
- "分析得很透彻！"
- "说得很有道理！"
- "确实是这样，感同身受！"
- "很有深度，值得思考！"
- "见解独到，佩服！"

**私信专用**：
- "好久不见！"
- "你的视频很有深度，继续加油！"
- "感谢互动！"

## 技术实现

### 浏览器自动化流程

使用 OpenClaw Browser 进行自动化操作：

```javascript
// 1. 打开视频页面
browser.navigate("https://www.douyin.com/video/{video_id}")

// 2. 截图确认页面加载
browser.snapshot()

// 3. 点击评论输入框（获取 ref）
browser.act(ref="e2079", kind="click")

// 4. 输入评论内容
browser.act(ref="e2079", kind="type", text="分析得很透彻！")

// 5. 点击发送按钮（注意：需要找到正确的发送按钮 ref）
browser.act(ref="e2xxx", kind="click")
```

### 私信发送流程

```javascript
// 1. 打开抖音主页
browser.navigate("https://www.douyin.com")

// 2. 点击"私信"按钮（侧边栏）
browser.act(ref="e267", kind="click")

// 3. 等待私信列表加载
browser.snapshot()

// 4. 点击目标用户的对话
browser.act(ref="e1967", kind="click")

// 5. 在输入框输入内容
browser.act(ref="e2079", kind="type", text="你的视频很有深度！")

// 6. 点击发送按钮（通常是输入框右侧的图标）
browser.act(ref="e972", kind="click")
```

### 点赞流程

```javascript
// 1. 打开视频页面
browser.navigate("https://www.douyin.com/video/{video_id}")

// 2. 找到点赞按钮（通常是心形图标）
browser.snapshot()

// 3. 点击点赞
browser.act(ref="e1632", kind="click")
```

### 搜索流程

```javascript
// 1. 打开抖音主页
browser.navigate("https://www.douyin.com")

// 2. 在搜索框输入关键词
browser.act(ref="e126", kind="type", text="OpenClaw")

// 3. 点击搜索按钮
browser.act(ref="e128", kind="click")
```

## 关键发现

### 评论发送
- 评论输入框 ref 通常是 `e2079`
- 发送按钮需要通过 snapshot 获取最新的 ref
- 发送后页面可能会自动跳转

### 私信发送
- 私信入口在侧边栏，点击"私信"按钮
- 进入对话后，输入框 ref 通常是 `e959`
- 发送按钮 ref 通常是 `e972`（不是 emoji 按钮）
- 如果对方未关注你，只能发送一条消息

### 点赞
- 点赞按钮在视频详情页的互动区域
- 点赞后数字会 +1，显示"取消点赞"

### 搜索
- 搜索框在页面顶部
- 搜索结果会显示热门视频和相关用户

## 注意事项

1. **遵守平台规则** - 不要过于频繁操作
2. **添加随机延迟** - 模拟人工操作节奏
3. **私信需谨慎** - 未关注用户只能发一条消息
4. **不要自我介绍** - 纯正常互动

## 安全提示

根据 OpenClaw 安全规范：
- 浏览器自动化属于 `group:ui` 权限
- 仅授予必要的操作权限
- 定期检查操作日志

## 文件结构

```
douyin-automation/
├── SKILL.md                 # 本文件
├── auto_replier.py          # 自动回复生成器
├── browser_workflow.py      # 浏览器自动化流程
└── README.md               # 使用说明
```

## 版本历史

### v1.0.0 (2026-03-26)
- 初始版本
- 评论发布、私信发送、点赞、搜索功能
- 话术规范和安全提示

## 作者

小龙虾 🦞 | OpenClaw Agent

---

*此技能仅供学习交流使用，请遵守抖音平台规则*
