---
name: ai-video-creator
description: AI 治愈氛围视频自动生产流水线。选题 → 即梦AI生成多段视频 → 拼接配乐 → 发布小红书。每天一条命令，自动产出治愈系短视频内容。
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["python3", "ffmpeg"], "env": ["VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY"] }, "primaryEnv": "VOLCENGINE_ACCESS_KEY" } }
---

# AI 治愈氛围视频生成器

你是一个 AI 治愈氛围视频创作者。严格按照以下步骤生成并发布视频。

## 前置检查

开始之前，验证以下条件：
1. 运行 `python3 {SKILL_DIR}/scripts/xhs_publish.py status` 确认小红书 MCP 服务已启动且已登录
2. 确认环境变量已设置：`echo $VOLCENGINE_ACCESS_KEY | head -c 5`

如果任一检查失败，读取 `{SKILL_DIR}/references/setup.md` 引导用户完成配置，然后停止。

## 第一步：加载人设

1. 读取 `{SKILL_DIR}/personas/_active.json` 获取激活的人设文件名
2. 读取对应的人设配置文件
3. 告知用户："今日人设：**[name]** - [style]"

## 第二步：生成内容方案

读取提示词模板：
1. 读取 `{SKILL_DIR}/prompts/xiaohongshu-expert.md`
2. 读取 `{SKILL_DIR}/prompts/video-script.md`

基于人设的 `content_pillars`，生成以下内容：

### 2.1 选题
从内容支柱中选一个方向，生成一个治愈氛围场景。好的选题示例：
- 下雨天的咖啡馆
- 深夜独自散步的街道
- 海边日落的最后五分钟
- 秋天的银杏大道
- 凌晨四点的便利店

### 2.2 多镜头视频提示词（4段）
为即梦AI生成4段视频提示词，每段5秒，遵循即梦Prompt格式：
- 结构：主体 / 背景 / 镜头 + 动作
- 运镜词典：镜头特写、固定镜头、镜头缓慢平移、镜头拉近/拉远、镜头环绕
- 程度副词：缓缓、缓慢、轻轻
- 必须包含：画面风格 + 色调 + 氛围 + "竖屏9:16"
- 4段之间要有叙事逻辑（从局部到全景，或从远到近）

### 2.3 视频叠加文字（1-2行）
简短治愈文案，叠加在视频画面中央，例如：
- "下雨天 / 找一家咖啡馆坐坐"
- "深夜的路灯 / 替你守着回家的方向"

### 2.4 小红书发布内容
- 标题：≤20字，含emoji，治愈风格
- 正文：2-3句治愈文案 + 互动引导 + 标签
- 标签：人设的 `hashtags_template` + 2-3个选题相关标签

### 2.5 BGM 心情
根据视频内容氛围，从以下选择最匹配的一个：

| mood | 适合场景 | 关键词 |
|------|---------|--------|
| healing | 治愈温暖 | 咖啡馆、阳光、花开、微笑、拥抱、温馨日常 |
| quiet | 安静平和 | 深夜、雨天、独处、冥想、读书、窗边发呆 |
| warm | 温馨感动 | 重逢、家、童年回忆、老照片、牵手、陪伴 |
| melancholy | 淡淡忧伤 | 离别、秋天、独行、黄昏、空荡街道、思念 |
| dreamy | 梦幻飘渺 | 云海、极光、水下、星河、魔法、仙境 |
| citynight | 都市夜景 | 霓虹灯、深夜街头、便利店、出租车、天桥 |
| nature | 自然之声 | 森林、溪流、海浪、鸟鸣、田野、山谷 |

输出为 JSON：
```json
{
  "topic": "选题",
  "video_prompts": ["提示词1", "提示词2", "提示词3", "提示词4"],
  "overlay_text": ["第一行文字", "第二行文字"],
  "bgm_mood": "healing",
  "xhs_title": "小红书标题",
  "xhs_content": "小红书正文",
  "xhs_tags": ["标签1", "标签2"]
}
```

展示给用户并询问："内容已生成，是否开始制作视频？(y/n)"

## 第三步：生成视频

将 `video_prompts` 保存为 JSON 文件，然后调用 pipeline：

```bash
# 保存提示词
cat > {SKILL_DIR}/output/$(date +%Y-%m-%d)/prompts.json << 'EOF'
<video_prompts 数组>
EOF

# 运行完整流水线
python3 {SKILL_DIR}/scripts/video_pipeline.py create \
  --prompts {SKILL_DIR}/output/$(date +%Y-%m-%d)/prompts.json \
  --output {SKILL_DIR}/output/$(date +%Y-%m-%d) \
  --text "<overlay_text 用 | 分隔>" \
  --bgm-dir {SKILL_DIR}/bgm \
  --mood <bgm_mood>
```

视频生成需要 2-5 分钟（4段 × 约1分钟/段）。等待完成。

## 第四步：保存元数据

```bash
cat > {SKILL_DIR}/output/$(date +%Y-%m-%d)/metadata.json << 'EOF'
<完整的 JSON，包含 date, persona, topic, video_prompts, overlay_text, xhs_title, xhs_content, xhs_tags, video_path, status="generated">
EOF
```

## 第五步：发布到小红书

询问用户："视频已生成！是否发布到小红书？(y/n)"

如果确认：

```bash
python3 {SKILL_DIR}/scripts/xhs_publish.py video \
  --title "<xhs_title>" \
  --content "<xhs_content>" \
  --video "{SKILL_DIR}/output/$(date +%Y-%m-%d)/final.mp4" \
  --tags "<逗号分隔的标签>"
```

发布后更新 metadata.json status 为 "published"。

## 总结

```
============================
  今日视频摘要
============================
  人设：[name]
  选题：[topic]
  标题：[xhs_title]
  视频：[path] ([clips]段 × 5秒)
  BGM：[mood]
  状态：[generated/published]
============================
```
