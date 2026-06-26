---
name: xhs-post
description: 小红书图文/视频笔记发布。包含标题优化、正文模板、标签策略、发布后数据跟踪。
emoji: ✍️
version: "1.0.0"
triggers:
  - 发笔记
  - 发布
  - 上传
  - 写一篇
  - post
  - 定时发布
---

# ✍️ xhs-post

> 小红书图文/视频笔记发布完整指南

## 何时触发

- "发一篇笔记"
- "发布图文"
- "上传视频"
- "写一篇种草文"
- "定时发布"
- `/xhs-post`

---

## 前置必检

```python
# 1. 检查登录
status = await mcp.check_login_status()
assert status["logged_in"], "❌ 未登录，请先 /xhs-login"

# 2. 检查当天发布配额
# 每天最多3篇图文，2篇视频
# 超出后会被平台限制
```

---

## 图文笔记发布流程

### Step 1：素材准备

**图片规范**：
| 类型 | 尺寸 | 大小 | 格式 |
|------|------|------|------|
| 封面图 | 3:4（竖版）| ≤10MB | JPG/PNG |
| 内页图 | 1:1 或 3:4 | ≤5MB/张 | JPG/PNG |
| 最多图片 | 9张 | — | — |

**封面图优化**：
- 文字清晰，大字号
- 人物/产品居中
- 高对比度，色彩鲜明
- 避免过多文字堆砌

### Step 2：标题撰写

**结构公式**：
```
[效果/感受] + [核心亮点] + [场景/人群]
```

**示例**：
```
"用了3个月皮肤真的变好了！| 混干皮真实测评"
"上海周边1h直达！| 适合遛娃的小众农场攻略"
"手残党也能做！3道简单家常菜教程"
```

**emoji 使用**：
- 开头 1-2 个 emoji 吸引注意
- 避免 emoji 堆砌（最多 3-4 个）
- 常见：📕✨🔥💄🛍️🎀📸🌸

**禁止出现**：
- 最、第一、绝对、保证、神器、神药
- 免费、白嫖、退款保证
- 吊打、完败、碾压

### Step 3：正文撰写

**五段式模板**：

```markdown
## 第一段：痛点/引入（50字内）
我之前一直XXX，最近终于发现了...

## 第二段：核心内容（100-200字）
具体怎么做/用什么/体验如何

## 第三段：细节补充（100字内）
补充一些细节或注意事项

## 第四段：个人结论（50字内）
整体来说我觉得...

## 第五段：互动引导（可选）
你们有没有类似经历？评论区见~
```

**话题标签策略**：
- 3-10 个话题
- 格式：`#话题名#`
- 组合：1-2个大类词 + 2-3个精准词 + 1个流量词

### Step 4：MCP 发布调用

```python
# 发布图文笔记
result = await mcp.post_note(
    title="标题文本",
    content="正文内容，支持 Markdown",
    images=[
        "/path/to/cover.jpg",   # 封面（必须）
        "/path/to/img2.jpg",    # 内页
        "/path/to/img3.jpg",    # 最多9张
    ],
    topics=["#护肤#", "#测评#", "#好物分享#"],
    visibility="public",  # public / private
)

# 返回格式
{
    "success": true,
    "note_id": "64xxxxxxx",
    "url": "https://www.xiaohongshu.com/explore/64xxxxxxx",
    "draft": false
}
```

### Step 5：视频笔记发布

```python
# 发布视频笔记
result = await mcp.post_video(
    title="视频标题",
    description="视频描述（正文）",
    video_path="/path/to/video.mp4",
    cover_path="/path/to/cover.jpg",  # 可选，让平台自动截帧
    topics=["#vlog#", "#日常#"],
)

# 视频规范
# 时长：15秒 - 15分钟
# 大小：≤2GB
# 格式：MP4（H.264）
# 建议：1080p + 60fps
```

---

## 发布前检查清单

```markdown
### 标题
- [ ] 无绝对化词汇（最/第一/绝对/保证/神器）
- [ ] 无欺诈词汇（免费/白嫖/退款保证）
- [ ] 字数 10-20 字
- [ ] 有吸引力，有信息量

### 正文
- [ ] 无违禁词（见 xhs-compliance.md）
- [ ] 有个人体验/效果因人而异声明
- [ ] 无外链/二维码/联系方式
- [ ] 图片版权清晰（原创或授权）

### 标签
- [ ] 3-10 个话题
- [ ] 无硬广告植入话题
- [ ] 话题与内容相关

### 图片
- [ ] 封面图清晰，吸引眼球
- [ ] 无品牌完整 logo（需马赛克）
- [ ] 无二维码/水印
- [ ] 数量合理（1-9张）
```

---

## 发布后跟踪

### 数据获取

```python
# 获取笔记数据
note_data = await mcp.get_note_stats("64xxxxxxx")

# 返回
{
    "likes": 156,
    "collects": 89,
    "comments": 23,
    "views": 2340,
    "share_count": 12,
    "crawl_time": "2026-04-23T10:00:00Z"
}
```

### 数据分析指标

| 指标 | 计算方式 | 合格线 |
|------|---------|--------|
| 点赞率 | 点赞/浏览 | ≥3% |
| 收藏率 | 收藏/浏览 | ≥5% |
| 评论率 | 评论/浏览 | ≥0.5% |
| 转发率 | 转发/浏览 | ≥0.3% |

### 数据差时的应对

```python
def analyze_underperformance(note_id):
    stats = get_note_stats(note_id)
    rates = {
        'like_rate': stats['likes'] / stats['views'],
        'collect_rate': stats['collects'] / stats['views'],
    }
    
    if rates['like_rate'] < 0.03:
        return "标题/封面不够吸引，建议优化"
    if rates['collect_rate'] < 0.05:
        return "内容实用性不够，建议增加干货"
    if stats['views'] < 100:
        return "曝光不足，可能是标签问题或平台审核"
```

---

## 定时发布

```python
# 定时发布（下一次流量高峰）
from datetime import datetime, timedelta

# 小红书流量高峰：7-9点、12-14点、18-22点
peak_hours = [8, 13, 20]

now = datetime.now()
# 计算下一个高峰时段
next_peak = None
for h in peak_hours:
    candidate = now.replace(hour=h, minute=0, second=0)
    if candidate > now:
        next_peak = candidate
        break

if next_peak is None:
    next_peak = (now + timedelta(days=1)).replace(hour=8, minute=0)

result = await mcp.schedule_note(
    title="...",
    content="...",
    images=[...],
    topics=[...],
    publish_at=next_peak.isoformat()
)
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `20021` | 图片尺寸不符 | 按规范裁剪后重试 |
| `20022` | 视频时长超限 | 剪辑到15分钟内 |
| `20023` | 包含违禁词 | 修改文案后重试 |
| `20024` | 超出日发布限额 | 等待24小时后重试 |
| `30001` | 需要重新登录 | `/xhs-login` 刷新 Cookie |

---

*Version: 1.0.0 | Updated: 2026-04-23*