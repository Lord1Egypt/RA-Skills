---
slug: douyin-script-writer
name: Douyin Short Video Script Writer
name_zh: 抖音短视频脚本助手
version: 1.0.0
author: ClawHub Community
category: content-creation
description: Turn a topic into a Douyin-ready short video script with hook, storyboard, captions, and BGM suggestions.
model: default
tags:
  - douyin
  - short-video
  - script-writing
  - storyboard
  - content-creation
  - tiktok
  - video-production
search_keywords:
  en:
    - douyin script
    - short video script
    - tiktok script writer
    - video storyboard
    - douyin content
  zh:
    - 抖音脚本
    - 短视频脚本
    - 抖音文案
    - 短视频分镜
    - 抖音内容创作
first_success_path:
  command: "douyin-script-writer --topic \"上海隐藏版葱油拌面\" --duration 15"
  description: "Enter a topic and get a complete 15-second Douyin script with storyboard, voiceover, subtitles, BGM, and publishing tips."
  duration: "30 seconds"
---

# Douyin Short Video Script Writer

## Overview

The **Douyin Short Video Script Writer** transforms any topic into a polished, production-ready Douyin short video script. It generates a complete package: golden hook, voice-over script, visual storyboard with camera directions, subtitle style suggestions, BGM recommendations, optimal publish time windows, and cover copy.

Designed for **15s, 30s, and 60s** video formats — the three most popular durations on Douyin. Each duration follows the platform's proven engagement structure.

### Who Is This For?

| User | Pain Point | This Skill Solves |
|------|-----------|-------------------|
| Individual creator | Daily posting pressure | Generates 1-3 scripts instantly |
| New account starter | Not sure what to film | Provides ready-to-film storyboards |
| E-commerce seller | Can't write sales scripts | Creates compelling product hooks |
| Trend chaser | Hot topic needs fast output | Delivers a script in 1 prompt |
| Video editing assistant | Needs clear direction | Gives detailed shot-by-shot instructions |

---

## Workflow (6 Steps)

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  1.      │   │  2.      │   │  3.      │   │  4.      │   │  5.      │   │  6.      │
│ Topic    │ → │ Hook     │ → │ Structure│ → │ Voiceover│ → │ Story-   │ → │ Packaging│
│ Input    │   │ Design   │   │ Split    │   │ Script   │   │ board    │   │ Tips     │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Step 1: Topic Input
- Read user input: topic, target duration (15/30/60s), style, audience
- Accept product name + selling points for e-commerce scripts

### Step 2: Hook Design (The Golden 3 Seconds)
- Generate a compelling opening (suspense, conflict, curiosity, or benefit)
- First 3 seconds determine whether the viewer scrolls past or keeps watching

### Step 3: Structure Split
- Divide the script into timed sections based on duration:

| Duration | Hook | Development | Climax | CTA |
|----------|------|------------|--------|-----|
| **15s** | 0-3s | 3-8s | 8-12s | 12-15s |
| **30s** | 0-3s | 3-12s | 12-22s | 22-30s |
| **60s** | 0-3s (Pain) | 3-15s (Problem) | 15-50s (Solution+Results) | 50-60s (Conversion) |

### Step 4: Voiceover Script
- Generate word-for-word voiceover lines for each section
- Natural, conversational tone optimized for Douyin's audience

### Step 5: Storyboard Generation
- For each voiceover segment, produce:
  - Visual description (what appears on screen)
  - Shot type (close-up, mid-shot, wide, POV)
  - Camera angle (eye-level, top-down, low-angle)

### Step 6: Packaging Suggestions
- Subtitle style and keywords to highlight
- BGM genre and example tracks
- Best publish time windows
- Cover/thumbnail copy

---

## Sample Prompts (with Expected Output)

### Sample 1: Food Exploration — 15s

**Prompt:**
```
Topic: 上海隐藏版葱油拌面
Duration: 15 seconds
Style: 快节奏诱人
Audience: 美食爱好者
```

**Expected Output:**
```
【15秒脚本】

0-3s 钩子：
画面：热气腾腾的面端上桌特写
景别：特写 | 角度：俯拍
口播："上海这碗葱油拌面，我排队了40分钟！"

3-8s 展开：
画面：筷子挑起面条，葱油裹满每一根
景别：大特写 | 角度：平视
口播："葱炸得焦香，酱汁是老板自己熬的"

8-12s 高潮：
画面：第一口吃下去的表情
景别：中景（面部表情）| 角度：正面
口播："一口下去，满嘴都是童年味道"

12-15s 结尾：
画面：店铺门头+定位
景别：远景 | 角度：平视
口播："地址在评论区，先去收藏！"

字幕：大字报风格，关键词放大：「40分钟」「童年味道」
BGM：热门美食探店 BGM（节奏感强）
发布时间：11:30-13:00 或 17:30-19:00
封面文案：为了这碗葱油拌面我排了40分钟
```

---

### Sample 2: Knowledge Sharing — 30s

**Prompt:**
```
Topic: 为什么你总是存不下钱
Duration: 30 seconds
Style: 干货温和
Audience: 职场白领
```

**Expected Output:**
```
【30秒脚本】

0-3s 钩子：
画面：数钱/空钱包特写
景别：特写 | 角度：俯拍
口播："为什么你月薪一万，月底还是月光？"

3-12s 展开：
画面：列出三个消费场景（奶茶、打车、会员）
景别：中景 | 角度：正面
口播："因为你把钱花在了看不见的地方，奶茶、打车、会员自动续费"

12-22s 高潮：
画面：记账APP截图
景别：特写 | 角度：俯拍
口播："想改变，先做一件事：记录每一笔支出，坚持7天"

22-30s 结尾：
画面：点赞手势
景别：中景 | 角度：正面
口播："关注我，下期教你3个存钱技巧"

字幕：逐字字幕，重点标黄：「月薪一万」「月光」「7天」
BGM：轻快知识类BGM（Tobu - Candyland风格）
发布时间：21:00-22:00
封面文案：月薪一万为什么还是月光？
```

---

### Sample 3: E-Commerce Product — 60s

**Prompt:**
```
Product: 手持挂烫机
Selling Points: 3秒出蒸汽, 便携, 不伤衣
Duration: 60 seconds
Style: 种草真实
Audience: 出差党
```

**Expected Output:**
```
【60秒脚本】

0-3s 钩子：
画面：皱巴巴衬衫 VS 熨好衬衫对比
景别：特写-特写 | 角度：平视
口播："出差党的救星来了！"

3-15s 痛点：
画面：酒店没有熨斗，衣服皱着出门
景别：中景 | 角度：正面
口播："以前出差，衬衫皱得像咸菜，见客户太尴尬"

15-35s 产品介绍：
画面：手持挂烫机使用过程
景别：特写 | 角度：俯拍
口播："这个挂烫机，3秒出蒸汽，巴掌大小，行李箱角落就能塞"

35-50s 效果展示：
画面：熨烫前后对比
景别：大特写 | 角度：平视
口播："真丝、羊毛都能熨，不会烫坏衣服"

50-60s 促单：
画面：产品+价格标签
景别：中景 | 角度：正面
口播："链接在左下角，今天下单还送便携收纳袋"

字幕：卖点关键词放大：「3秒出蒸汽」「不伤衣」「送收纳袋」
BGM：带货节奏BGM（节奏感强但不抢话）
发布时间：19:00-21:00
封面文案：出差党必入！3秒拯救皱衬衫
```

---

### Sample 4: Emotional Story — 30s

**Prompt:**
```
Topic: 北漂十年，我第一次给妈妈买了房
Duration: 30 seconds
Style: 情感共鸣
Audience: 25-35岁职场人
```

**Expected Output:**
```
【30秒脚本】

0-3s 钩子：
画面：老旧小区 vs 新小区航拍对比
景别：远景切近景 | 角度：航拍
口播："北漂十年，我终于在北京给妈妈买了一套房。"

3-12s 展开：
画面：旧照片翻页效果（妈妈年轻时、自己刚毕业）
景别：特写 | 角度：平视
口播："十年前，妈妈送我来北京，说'好好干，妈等着你带妈妈住大房子'"

12-22s 高潮：
画面：新房钥匙递给妈妈的手部特写
景别：大特写 | 角度：俯拍
口播："今天，我把钥匙放在她手里，她哭了，我也哭了"

22-30s 结尾：
画面：妈妈在新房阳台笑
景别：远景 | 角度：平视
口播："你有多努力，家就有多好。给所有正在打拼的人。"

字幕：慢速字幕「十年」「妈妈」「大房子」「打拼」
BGM：River Flows in You - Yiruma风格
发布时间：20:00-22:00
封面文案：北漂十年，我终于做到了
```

---

### Sample 5: Comedy Sketch — 15s

**Prompt:**
```
Topic: 健身教练看到我突然办卡的反应
Duration: 15 seconds
Style: 剧情搞笑
Audience: 年轻人
```

**Expected Output:**
```
【15秒脚本】

0-3s 钩子：
画面：健身教练疑惑表情特写
景别：大特写 | 角度：正面
口播："我说我要办年卡，教练看了我一眼……"

3-8s 展开：
画面：切换三个镜头——肥肉特写、薯片包装、沙发瘫
景别：快速切换 | 角度：各种
口播："然后他说'哥，你是来办卡还是来交保护费的？'"

8-12s 高潮：
画面：教练强忍笑意签字，Customer和Victim划掉Victim
景别：特写 | 角度：俯拍
口播："然后默默拿出合同，把'会员'两个字改成了'长期投资者'"

12-15s 结尾：
画面：自己在跑步机上气喘吁吁，教练在旁边数钱
景别：中景 | 角度：侧面
口播："我现在跑步机上喘得像狗，他在旁边数我的钱"

字幕：大字特效「保护费」「长期投资者」「喘得像狗」
BGM：搞笑剧情BGM（喜剧之王片尾曲风格）
发布时间：12:00-14:00 或 18:00-20:00
封面文案：教练看到我办卡的表情绝了😂
```

---

## Real-World Task Examples

### Task 1: Food Blogger's Daily Recipe

**Scenario:** A food blogger needs a daily video script for a hidden Shanghai noodle shop.

**Input:**
```
Topic: 上海弄堂里的老字号生煎
Duration: 15s
Style: 快节奏诱人
Audience: 本地美食爱好者
```

**Execution Steps:**
1. User invokes the skill with topic and duration
2. Skill analyzes the topic (food) and style (tempting, fast-paced)
3. Generates hook focusing on the hidden nature + food appeal
4. Produces 4 timed scenes with visuals, voiceover, camera directions
5. Suggests food-explore BGM category and publish time

**Expected Output:**
```
【15秒脚本】

0-3s 钩子：
画面：生煎底部金黄酥脆特写
景别：大特写 | 角度：俯拍
口播："上海这家生煎，我吃了十年都没腻！"

3-8s 展开：
画面：咬开生煎，汤汁流出
景别：特写 | 角度：平视
口播："皮薄馅大，一口咬下去满满的汤汁"

8-12s 高潮：
画面：蘸醋一口吃完的表情
景别：中景 | 角度：正面
口播："底部煎得焦脆，肉馅鲜甜"

12-15s 结尾：
画面：店铺门头+地址
景别：远景 | 角度：平视
口播："位置在评论区，趁热去！"

字幕：大字报风格，关键词放大：「十年」「汤汁」「焦脆」
BGM：热门美食探店BGM（快节奏）
发布时间：11:30-13:00
封面文案：吃了十年的生煎，还是这个味
```

---

### Task 2: Finance Knowledge Creator

**Scenario:** A personal finance creator wants a 30-second video on why young people can't save money.

**Input:**
```
Topic: 为什么年轻人存不住钱
Duration: 30s
Style: 干货温和
Audience: 22-30岁年轻人
```

**Execution Steps:**
1. User inputs topic and style
2. Skill designs hook around common pain point
3. Expands with 3 specific spending traps
4. Provides actionable tip as climax
5. Adds CTA for follow-up content

**Expected Output:**
```
【30秒脚本】

0-3s 钩子：
画面：年轻人看手机银行余额特写
景别：特写 | 角度：俯拍
口播："为什么你工资不低，却永远存不下钱？"

3-12s 展开：
画面：三个消费场景快速切换
景别：快速剪辑 | 角度：混合
口播："因为你中了三个陷阱：外卖、凑单、冲动消费"

12-22s 高潮：
画面：日历记录每日支出
景别：特写 | 角度：平视
口播："从现在开始，每天睡前记一笔账，7天你就知道钱去哪了"

22-30s 结尾：
画面：关注引导动画
景别：中景 | 角度：正面
口播："存钱没那么难，关注我，下次告诉你3个存钱技巧"

字幕：动态字幕配图标，「三个陷阱」「记一笔账」「7天」
BGM：轻快知识类BGM
发布时间：21:00-22:00
封面文案：3个让你永远存不下钱的陷阱
```

---

### Task 3: E-commerce Seller Product Launch

**Scenario:** A seller needs a 60-second product demo script for a portable garment steamer targeting frequent travelers.

**Input:**
```
Product: 便携式手持挂烫机
Selling Points: 3秒出蒸汽, 仅手机大小, 不伤衣物, 干湿两用
Duration: 60s
Style: 种草真实
Audience: 出差族/商务人士
CTA: 左下角购买，今日下单送收纳袋
```

**Execution Steps:**
1. Product name and selling points provided
2. Skill constructs pain→solution→result→conversion narrative
3. 5-section structure for 60s e-commerce format
4. Each section has timed visuals matching product features
5. Includes specific conversion CTA with offer

**Expected Output:**
```
【60秒脚本】

0-3s 钩子：
画面：皱巴巴西服 VS 熨烫后笔挺西服
景别：特写 | 角度：平视
口播："出差党的噩梦，三秒解决。"

3-15s 痛点：
画面：酒店房间，衣服从行李箱拿出皱成一团
景别：中景 | 角度：平视
口播："以前出差，早上起床衬衫皱得像抹布，挨客户白眼"

15-35s 产品介绍：
画面：从口袋掏出挂烫机，插电即用
景别：特写 | 角度：俯拍
口播："这个挂烫机，只有手机大小，3秒出蒸汽，塞口袋都能带走"

35-50s 效果展示：
画面：真丝衬衫、羊毛大衣、棉T恤分别熨烫演示
景别：大特写 | 角度：俯拍
口播："真丝不烫坏，羊毛不变形，干熨湿熨都行"

50-60s 促单：
画面：产品+收纳袋+价格标签同时出现
景别：中景 | 角度：正面
口播："左下角上车，今天下单送收纳袋，出门带着走。"

字幕：卖点弹幕式出现，「3秒出蒸汽」「手机大小」「不伤衣」「送收纳袋」
BGM：带货节奏BGM（不抢话）
发布时间：19:00-21:00（周四或周五最佳）
封面文案：出差党必入！3秒解决所有穿衣尴尬
```

---

## First-Success Path (30 Seconds)

```bash
# ──────────────────────────────────────────────────
#  30-SECOND FIRST SUCCESS
# ──────────────────────────────────────────────────

# Step 1 (5s): Run the CLI with your topic
douyin-script-writer --topic "上海隐藏版葱油拌面" --duration 15

# Step 2 (10s): Read the output — hook, voiceover, storyboard, BGM, tips
# Step 3 (10s): Adjust any details (style, CTA)
# Step 4 (5s): Take the script and start filming!

# That's it — you now have a complete, production-ready video script.
```

### Quick-start for AI Assistants

```
Generate a 15-second Douyin video script about [TOPIC].
Style: [STYLE], audience: [AUDIENCE].
Include: hook, voiceover, storyboard, BGM suggestions, and publish time.
```

### Verification Checklist

After running the skill, confirm:
- [ ] Script has 4-5 timed scenes matching the duration
- [ ] Each scene has visual + voiceover + camera direction
- [ ] Hook is designed for the first 3 seconds
- [ ] Subtitle style and highlight keywords are provided
- [ ] BGM genre and at least 2 example tracks suggested
- [ ] Publish time windows are provided
- [ ] Cover/thumbnail copy is suggested

---

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Topic too vague | Ask user to be more specific (e.g., "上海美食" → "上海静安区一家手工葱油饼店") |
| Duration not supported | Supported: 15s, 30s, 60s only |
| Product script without selling points | Request at least 2 selling points for e-commerce scripts |
| No hook idea | Generate 3 alternative hook options for the user to choose from |

---

## Key Differentiators

- **Platform-optimized**: Designed specifically for Douyin's content ecosystem and proven engagement patterns
- **Actionable storyboard**: Every scene includes camera direction — not just text
- **Full production package**: Script + storyboard + BGM + publishing strategy in one output
- **Duration-specific structure**: 15s/30s/60s each have their own proven template
- **E-commerce ready**: Supports product scripts with pain→solution→conversion flow

---

## License

MIT-0 — No attribution required.

---

## Changelog

- **v1.0.0** (2026-06-15): Initial release — 15s/30s/60s script generation with full storyboard, BGM, and publishing suggestions.
