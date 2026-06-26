# AI 视频剧本模板 - Scene Structure

**视频主题**: [填写视频标题]  
**预计时长**: [X] 秒  
**风格**: [励志/科技/故事]  
**BGM 建议**: [填写背景音乐风格]

---

## [Scene 1] - 开场钩子

```markdown
[时间戳]: 0:00-0:15
画面描述：AI 数字人半身像，直视镜头
台词（Prompt）："我突然意识到一件事……我已经 40 岁了。"
图片参考：avatar-headshot.jpg
背景元素：简洁背景 + 心跳音效字幕
转场：渐入黑屏 → 主播出现
```

---

## [Scene 2] - 抛出痛点

```markdown
[时间戳]: 0:15-0:35
画面描述：主播侧脸 + 新闻截图闪过
台词（Prompt）："今早刷到一条新闻：AI 数字人主播已经能取代 80% 的传统客服岗位了。我愣了三分钟。翻了下记录，发现从 2 月到 3 月，我一直在问些无关紧要的问题……"
图片参考：news-screenshot.png / chat-history.png
背景音乐：紧张感音乐渐强
转场：快速闪回聊天记录界面
```

---

## [Scene 3] - 现状分析

```markdown
[时间戳]: 0:35-1:00
画面描述：PPT 图表对比新旧技术
台词（Prompt）："我在 IT 咨询干了这么多年，会建系统、部署云服务器、写 SQL、调 API……这些技能放到 2020 年，是核心竞争力。但到了 2026 年呢？那些年轻的技术大牛们，他们已经在用 AI 工具一个人活成一支队伍了。而我还在纠结'要不要学''什么时候开始'……"
图片参考：tech-comparison-chart.png
背景音乐：激昂音乐
转场：主播严肃脸特写
```

---

## [Scene 4] - 转折点

```markdown
[时间戳]: 1:00-1:30
画面描述：主播眼神坚定
台词（Prompt）："但今天，我决定不再拖延。我用 OpenClaw 搭建了第一个 AI Agent，注册了 Supabase 数据库，还规划了整个知识库系统……我想做一件事：用 AI 数字人出镜，每天记录我从 40 岁开始学 AI 的全过程。"
图片参考：dify-dashboard.png / supabase-setup.png
背景音乐：励志音乐高潮
转场：火花特效 + "40 岁从零学 AI"标题
```

---

## [Scene 5] - 自我激励金句

```markdown
[时间戳]: 1:30-2:00
画面描述：主播正面对视镜头，特写
台词（Prompt）：
"A. 我问自己：我真的能行吗？
B. 我答自己：你不行谁行？你不开始，这辈子就只能在后悔里度过了。
C. 万一半途而废呢？至少你试过。总比老了以后坐在阳台上想'如果当初……'要强。
D. 最大的敌人不是 AI，而是我自己的犹豫不决。40 岁不晚，只要你从今天开始行动。明天见。"
图片参考：close-up-emotional.jpg
背景音乐：音乐推向高潮后渐弱
转场：黑屏 → 品牌 Logo
```

---

## [Scene 6] - 结尾互动

```markdown
[时间 timestamp]: 2:00-2:10
画面描述：主播指向屏幕下方
台词（Prompt）："如果你也 40 岁，或者在担心被时代淘汰——关注我，我们一起逆袭。下一条：第一天实操复盘，看我如何用 Dify 搭建第一个 AI Agent。"
图片参考：follow-button-animation.png
背景音乐：收尾音乐
转场：二维码动画 + 关注按钮
```

---

# 技术备注

## 图片资源清单
- `avatar-headshot.jpg` - 头像照片
- `news-screenshot.png` - 新闻截图
- `chat-history.png` - 聊天记录截图
- `dify-dashboard.png` - Dify 控制台截图
- `supabase-setup.png` - Supabase 配置图

## 音效素材
- heartbeat.mp3 - 心跳音效
- bgm-tension.mp3 - 紧张感 BGM
- bgm-inspire.mp3 - 励志 BGM

## Seedance 调用参数建议
```yaml
model: seedance-2.0
resolution: 1080p
watermark: false
duration: 15
mode: image_to_video  # 基于照片生成动态效果
prompt_template: "[AI 数字人][中性光线][专业表情][口播节奏]"
```

---

_此剧本由 OpenClaw + Xiabi 共同维护_
_Last updated: 2026-03-03_
