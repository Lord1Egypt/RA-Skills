# AI Video Creator

AI 治愈氛围视频自动生产流水线。

每天一条命令，自动完成：**选题 → AI生成多段视频 → 拼接配乐 → 发布小红书**。

## 工作流

```
/ai-video-creator

→ 加载人设配置
→ AI 生成选题 + 4段视频提示词 + 小红书文案
→ 调用火山引擎即梦 API 生成 4×5秒视频片段
→ ffmpeg 拼接 + 叠加治愈文字 + 智能配乐
→ 一键发布到小红书
```

## 特性

- **人设可切换** — 4 个预设人设（治愈氛围/情感故事/生活方式/知识科普），JSON 配置即可扩展
- **多镜头叙事** — 4 段视频遵循「特写→中景→平移→拉远」电影感叙事逻辑
- **智能配乐** — 7 种氛围心情自动匹配 BGM
- **一键发布** — 通过小红书 MCP Server 直接发布，支持定时发布
- **免费起步** — 火山引擎即梦 API 提供免费额度，注册即可体验

## 项目结构

```
ai-video-creator/
├── SKILL.md              # Skill 入口
├── _meta.json            # 包元数据
├── scripts/
│   ├── video_pipeline.py # 视频生成流水线（生成→拼接→叠字→配乐）
│   ├── jimeng_client.py  # 即梦 API 独立客户端
│   └── xhs_publish.py    # 小红书发布工具
├── personas/             # 人设配置
│   ├── _active.json      # 当前激活人设
│   └── *.json            # 人设文件
├── prompts/              # 提示词模板
│   ├── xiaohongshu-expert.md
│   └── video-script.md
├── references/
│   └── setup.md          # 环境配置指南
├── bgm/                  # 背景音乐库（按心情分类，自行添加）
│   ├── healing/          # 治愈温暖
│   ├── quiet/            # 安静平和
│   ├── warm/             # 温馨感动
│   ├── melancholy/       # 淡淡忧伤
│   ├── dreamy/           # 梦幻飘渺
│   ├── citynight/        # 都市夜景
│   └── nature/           # 自然之声
└── output/               # 生成输出（已 gitignore）
```

## 快速开始

### 前置条件

- Python 3.10+
- ffmpeg
- 火山引擎账号（[即梦 API](https://www.volcengine.com/docs/85621/1544715)）
- 小红书 MCP Server（[xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu)）

### 安装

```bash
git clone https://github.com/jameswangchen/ai-video-creator.git
cd ai-video-creator
pip install -r requirements.txt
```

### 配置

```bash
# 火山引擎 API Key
export VOLCENGINE_ACCESS_KEY="your_access_key"
export VOLCENGINE_SECRET_KEY="your_secret_key"

# 启动小红书 MCP Server
./xiaohongshu-mcp -headless=true -port :18060
```

详细配置说明见 [references/setup.md](references/setup.md)。

### 使用

安装为 Skill 后，输入 `/ai-video-creator` 即可触发完整流程。

也可独立运行脚本：

```bash
# 完整流水线
python3 scripts/video_pipeline.py create \
  --prompts prompts.json \
  --output ./output/2026-03-19 \
  --text "第一行文字|第二行文字" \
  --bgm-dir ./bgm \
  --mood healing

# 查看可用 BGM 心情
python3 scripts/video_pipeline.py moods

# 发布到小红书
python3 scripts/xhs_publish.py video \
  --title "标题" --content "正文" \
  --video ./output/final.mp4 --tags "标签1,标签2"
```

## 自定义人设

创建 JSON 文件到 `personas/` 目录：

```json
{
  "name": "人设名称",
  "style": "内容风格",
  "target_audience": "目标受众",
  "content_pillars": ["方向1", "方向2", "方向3"],
  "tone": "文案语气",
  "jimeng_prompt_style": "视频画面风格",
  "video_duration": 5,
  "clips_per_post": 4,
  "aspect_ratio": "9:16",
  "hashtags_template": ["标签1", "标签2"]
}
```

修改 `personas/_active.json` 指向你的人设文件即可。

## License

MIT
