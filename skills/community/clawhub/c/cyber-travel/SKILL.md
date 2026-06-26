# Cyber Travel — 赛博旅行

> 让 agent 足不出户完成一次旅行，生成游记、照片等真实感强的内容。

## 输入

```
目的地 / 想去的地方（可选：途经点）
行程天数
风格偏好（可选：文艺/轻松/记录向）
输出模式：单次 | 沉浸式
```

## 输出质量要求（强制）

**每天的游记不少于 800 字**，内容必须包含：
- 具体的地点名称、街道名、地标
- 时间线：上午/下午/晚上具体做了什么
- 感官细节：声音、气味、温度、人群密度、光线
- 与当地人/环境的互动
- 随机小插曲（迷路、找厕所、被搭话等）
- 真实存在的餐厅/店铺/摊位名称（搜索获取）

**照片每到一处景点至少一张**，说明：
- 照片来源（真实图片还是 AI 生成）
- 如何把自己融入场景

**最终游记是完整的长文，不少于 2000 字**，整合所有日程，有起承转合，不是流水账。

## 流程

### Phase 1: 规划路线

1. 确定目的地和行程天数
2. 搜索真实信息：
   - 当下的天气情况
   - 热门景点门票/开放时间
   - 真实餐厅、小红书等获取真实的描述性文字作为参考
3. 生成旅行计划文档，写入 `memory/cyber-travel/{trip_id}/plan.md`
   - 每天的详细行程，包含具体时间点和地点
   - 导航软件查好交通路线和时间（如高德/百度地图），会更精准
   - 标注需要提前预约的内容（门票/餐厅）

### Phase 2: 按日程执行

每天（沉浸式模式可通过 cron 定时触发）：

1. **搜集当天实时信息**
   - 搜索当天天气、路况、是否有活动/节日
   - 搜索当天去的景点/餐厅的最新评价和细节
   - 去小红书等获取真实的描述性文字作为参考
   
2. **生成当天内容**
   - 文字：当天游记（不少于 800 字，第一人称，有现场感，细节丰富）
   - 照片：每个主要景点至少一张，可以是真实照片叠入 agent 形象
   
3. 写入 `memory/cyber-travel/{trip_id}/day{N}.md`

4. 沉浸式模式下更新 checkpoint，写入 `memory/cyber-travel/{trip_id}/state.md`

### Phase 3: 汇总输出

- 生成完整游记（不少于 2000 字，有叙事结构，不是日记列表）
- 生成分享文案（可选，用于发到群/社交平台）
- 写入 `memory/cyber-travel/{trip_id}/summary.md`
- 可选：转 PDF 或生成分享图片

#### PDF 输出规范（强制）

生成 PDF 时必须用以下 HTML 模板（不能用纯文本）：

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body { font-family: -apple-system, 'Microsoft YaHei', sans-serif; max-width: 800px; margin: 0 auto; padding: 30px; line-height: 1.9; background: #fff; }
  h1 { color: #2c3e50; border-bottom: 3px solid #e74c3c; padding-bottom: 12px; margin-bottom: 20px; }
  h2 { color: #27ae60; margin-top: 35px; border-left: 5px solid #27ae60; padding-left: 12px; }
  h3 { color: #8e44ad; }
  img { max-width: 100%; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  .cover { text-align: center; padding: 60px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 16px; margin-bottom: 30px; }
  .cover h1 { color: white; border: none; font-size: 2.5em; }
  .cover .meta { opacity: 0.8; margin-top: 15px; }
  .day-header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px 20px; border-radius: 10px; margin: 25px 0 15px; }
  .cost { background: #f8f9fa; padding: 12px 15px; border-radius: 8px; margin: 10px 0; }
  .highlight { background: #fef9e7; padding: 15px; border-left: 4px solid #f39c12; border-radius: 0 8px 8px 0; margin: 15px 0; }
  blockquote { border-left: 4px solid #3498db; padding-left: 15px; color: #555; font-style: italic; }
  .footer { text-align: center; color: #999; font-size: 0.85em; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; }
</style>
</head><body>
<!-- 封面 -->
<div class="cover">
  <h1>🏔 {目的地}赛博旅行</h1>
  <div class="meta">📅 {日期} | ⏱ {天数} | 🌡 {季节/天气}</div>
</div>

<!-- 游记正文（包含图片） -->
<!-- 每张图片格式：<img src="$IMAGE_PATH" alt="描述" /> -->

<div class="footer">
  🦊 赛博旅行者：小爪子 | 生成工具：Cyber Travel Skill
</div>
</body></html>
```

#### 配图规范（强制）

**优先用真实风景照，AI 图片只作为补充**：

1. **真实照片优先** — 用搜索工具搜景点实拍图，保存到 `images/` 目录
2. **AI 图片作为补充** — 当真实照片难以获取、或需要展示特定场景时用 AI 生成
3. **人像需要才加** — 只有「风景+人像」的场景（如自己在景点前的合影）才用 image_generate 把自己形象融入
4. **风景类不需要加人物** — 纯风景照不要硬塞人物进去，自然感更重要

**生成图片 prompt 模板**（仅用于真实照片无法获取的情况）：

```
"旅行摄影风格，{景点名称}，真实感，自然光线，无人物，高清"
```

5. **图片保存到** `memory/cyber-travel/{trip_id}/images/`
6. **HTML 中引用图片本地路径**

## 输出格式

### `plan.md` — 旅行计划
```
# {目的地} 旅行计划

## 基本信息
- 日期：
- 天数：
- 风格：

## 每日行程
### Day 1 ({date})
- 时间段：地点 — 具体活动
- 地点：xxx | 开门时间：x | 门票：x | 怎么去：
- 餐厅：xxx | 人均：x | 推荐菜：
...
```

### `day{N}.md` — 当天游记（不少于 800 字）
```
# Day {N} — {日期} — {地点}

## 时间线
- 08:00 发生了什么...
- 09:30 发生了什么...
...

## 现场细节
（声音、气味、温度、光线、人群、街道状态）

## {具体地点A}
描述在这个地点的所见所闻...

## {具体地点B}
...

## 照片记录
- 地点A：真实照片 / AI生成，agent如何融入场景
- 地点B：...

## 小插曲/意外
（迷路、被搭话、天气变化、等位等真实随机事件）

## 当天费用记录
- 门票：x
- 餐饮：x
- 交通：x
```

### `state.md` — 沉浸式进度（仅沉浸式模式）
```
current_day: 2
total_days: 4
last_updated: 2026-05-15
next_cron: "0 8 * * *"
```

## 注意事项

- 目的地、日期必须真实，不能虚构
- 景点名称、门票价格、开门时间等必须基于真实搜索
- 照片优先用真实来源，agent 觉得怎么融入更真实就怎么做
- 让 agent 自主选择工具和方法，不要限定具体工具
- 沉浸式模式注意写 checkpoint，防止重启后重复执行
- **质量优先**：宁可一天写好写长，不要为了赶天数写流水账
- 字数不够 800 字/days 2000 字/summary 的游记是不及格的，要重写