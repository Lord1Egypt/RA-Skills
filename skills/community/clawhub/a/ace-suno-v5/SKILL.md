---
name: ace-suno-v5
description: 🌐 完整的 AceData Suno V5 AI音乐创作Web应用，支持简易/自定义两种创作模式，包含浏览器可视化界面，自动保存音乐文件到桌面，支持在线播放和下载。使用 Suno V5 模型通过 AceData API 生成 AI 音乐，无限购买昂贵的订阅也可以创作出完美的音乐。
---

# Ace Suno V5 - AI 音乐创作平台

## 🎵 简介

基于 AceData Suno API 打造的完整 AI 音乐创作 Web 应用，提供美观易用的浏览器界面，让你轻松通过 AI 创作高质量音乐。

### 核心特点
- OpenClaw命令打开创作音乐可以直接打开界面，.py文件，直接生成，不产生额外的tokens开销
- ✨ **美观现代UI**：居中大窗口，风格标签快速选择
- 🔄 **双模式创作**：简易模式 / 自定义模式一键切换
  - 简易模式：仅输入描述即可创作
  - 自定义模式：支持自定义歌词、标题、风格
- 🏷️ **快速标签选择**：分五大类预置标签（风格/情感/乐器/氛围/性别），点击添加
- 🎼 **完整参数支持**：支持所有 API 参数，包括片段替换、人声补全、伴奏补全等高级功能
- 💾 **自动保存**：生成完成自动保存到桌面 `music/YYYY-MM-DD/` 文件夹
- ▶️ **在线播放**：页面底部展示历史生成，直接在线试听
- 🔑 **API Key 本地保存**：输入一次保存在浏览器localStorage，无文件溢出风险，下次无需重复输入
- 🛑 **一键关闭服务**：右上角圆形按钮一键关闭后台服务

## 🚀 快速开始

### 启动服务

在终端中输入：
```bash
cd ~/.openclaw/workspace/skills/ace-suno-v5
python start_server.py
```

脚本会自动检测依赖，如果缺少 Flask 和 Requests 会自动安装，然后启动服务。

脚本会自动检测依赖，如果缺少 Flask 和 Requests 会自动安装，然后启动服务。

### 开始创作

1. 打开浏览器访问：`http://localhost:1688`
2. 第一次访问会提示输入 AceData API Key
   - 如果还没有，可以在这里申请：https://share.acedata.cloud/r/1uN88BrUTQ
   - API Key 会保存在浏览器本地，下次打开自动填充
3. 选择创作模式：
   - **简易模式**：直接输入你想要的音乐描述，点击标签添加风格标签
   - **自定义模式**：填写歌曲标题、歌词，添加风格标签
4. 打开/关闭「纯音乐」开关
5. 点击「立即创作」按钮，等待生成完成
6. 生成完成自动保存到桌面，在页面下方可以直接试听或下载

## 📋 功能说明

### 模式切换
- **简易模式**：适合灵感创作，只需描述想要的音乐
- **自定义模式**：适合精确创作，可以自定义歌词和标题

### 标签分类

| 分类 | 说明 |
|------|------|
| 风格 | 流行、摇滚、嘻哈、爵士、电子... |
| 情感 | 快乐、悲伤、激情、平静、浪漫... |
| 乐器 | 钢琴、吉他、小提琴、鼓、贝斯... |
| 氛围 | 温暖、夏日、冬日、夜晚、梦幻... |
| 声音性别 | 男声/女声 (二选一) |

点击大类显示该分类下标签，点击标签添加到当前文本中，点击 × 删除已添加标签。

### 支持的操作类型 (action) 
- `generate` - 生成新歌曲（默认）
- `extend` - 延长现有歌曲(以下限plus版)
- `cover` - 翻唱歌曲
- `stems` - 提取音轨
- `remaster` - 重新母带处理
- `replace_section` - 替换片段
- `concat` - 拼接歌曲

### 高级功能
- 纯音乐开关：生成纯音乐
- 支持为已有纯音乐补充人声 (overpainting)
- 支持为清唱添加伴奏 (underpainting)
- 支持继续延长已有音频
- 支持片段替换

## 📁 文件保存

生成的文件自动保存到：
```
~/Desktop/music/YYYY-MM-DD/
```
每个歌曲保存三个文件：
- `{标题}_{ID}.mp3` - 音频文件
- `{标题}_{ID}.jpg` - 封面图片
- `{标题}_{ID}.txt` - 歌词文本

## 💻 Python 客户端使用

如果你想在代码中直接调用，可以使用 Python 客户端：

```python
from scripts.suno_client import AceSunoClient

# 初始化客户端
client = AceSunoClient(api_key="your-acedata-api-key")

# 简易模式生成
response = client.generate(
    prompt="一首轻快的流行歌曲，带有温暖的旋律",
    model="chirp-v5",
    vocal_gender="m"
)

# 自定义模式生成
response = client.generate(
    model="chirp-v5",
    custom=True,
    title="冬日恋歌",
    style="流行,温暖,抒情",
    lyric="[Verse]\n雪花飘落...\n[Chorus]\n冬日恋歌..."
)

# 自动保存所有文件
output_dir = client.save_generation(response['data'])
print(f"文件已保存到: {output_dir}")
```

## 📋 项目结构

```
ace-suno-v5/
├── SKILL.md                  # 本文档
├── start_server.py          # 一键启动脚本（自动安装依赖）
├── scripts/
│   └── suno_client.py        # Python API 客户端
└── web/
    ├── app.py                # Flask Web 后端
    ├── requirements.txt      # 依赖列表
    ├── generation_history.json # 生成历史记录
    └── templates/
        └── index.html        # 前端页面
```

## 🎯 模型版本

支持所有 Suno 模型版本，默认使用最新的 `chirp-v5`：
- `chirp-v5` - 最新版本（推荐）
- `chirp-v4-5-plus`(以下可以自己添加)
- `chirp-v4-5`
- `chirp-v3-5`
- `chirp-v4`
- `chirp-v3`

## 🔒 关闭服务

使用完后，点击页面右上角黑色圆形关闭按钮，确认后即可关闭后台服务。

## 📝 获取 API Key

本技能使用 AceData 提供的 Suno API，需要 API Key 才能使用。  
申请地址：https://share.acedata.cloud/r/1uN88BrUTQ

---

**作者**：Jakey
**版本**：1.0.0  
**日期**：2026-03-12
**寄语**:   龙虾好吃又好用