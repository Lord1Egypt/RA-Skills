# auto-publish

> 多平台自动发布器 — 自动将视频 / 内容发布到抖音、小红书、B站、YouTube 等平台

[![Skill Version](https://img.shields.io/badge/Skill%20Version-2026.06-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-OpenClaw-green.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](#)

## 截图预览

> 以下截图展示典型多平台发布界面效果，实际界面以平台官方为准。

| 发布队列 | 发布进度 | 数据追踪面板 |
|:---:|:---:|:---:|
| 批量排队管理 | 实时发布进度 | 浏览/点赞/评论/转发 |

## 📦 功能特性

### ✨ 核心功能

- ✅ **多平台支持**：抖音、小红书、B站、YouTube、快手
- ✅ **自动填写**：标题、标签、描述、封面
- ✅ **智能推荐**：最佳发布时间推荐（基于平台算法）
- ✅ **批量发布**：队列管理，支持批量上传
- ✅ **数据追踪**：发布后浏览量、点赞、评论追踪
- ✅ **失败重试**：网络错误自动重试，发布失败告警
- ✅ **智能标签**：基于视频内容自动生成标签

### 🎯 适用场景

- 内容创作者在多个平台发布视频
- 需要批量发布大量视频
- 想找到最佳发布时间提高曝光
- 需要追踪发布后的数据表现

## 🚀 快速开始

### 1. 安装 Skill

```bash
skillhub install auto-publish
```

或从本地安装：

```bash
skillhub install /path/to/auto-publish.skill
```

### 2. 配置平台API凭证

编辑 `scripts/config.json`，填入各平台的API凭证：

```json
{
  "platforms": {
    "douyin": {
      "enabled": true,
      "client_key": "YOUR_CLIENT_KEY",
      "client_secret": "YOUR_CLIENT_SECRET"
    }
  }
}
```

**获取API凭证的方法：**

- **抖音**：访问 https://open.douyin.com/ 注册开发者
- **小红书**：访问 https://open.xiaohongshu.com/ 申请权限
- **B站**：访问 https://open.bilibili.com/ 创建应用
- **YouTube**：访问 https://console.cloud.google.com/ 启用YouTube Data API v3

### 3. 发布单个视频

#### 命令行方式

```bash
python scripts/auto_publish.py \
  --platform douyin \
  --video path/to/video.mp4 \
  --title "我的视频标题" \
  --desc "视频描述 #话题1 #话题2" \
  --tags "话题1,话题2,话题3"
```

#### Python脚本方式

```python
from scripts.auto_publish import AutoPublisher

publisher = AutoPublisher()
result = publisher.publish(
    platform="douyin",
    video_path="path/to/video.mp4",
    title="我的视频标题",
    description="视频描述",
    tags=["标签1", "标签2"],
    publish_time="best"  # 自动选择最佳发布时间
)

print(result)
# {'success': True, 'url': 'https://douyin.com/video/xxx', 'publish_time': '...'}
```

### 4. 批量发布

创建 `publish_list.json`：

```json
[
  {
    "platform": "douyin",
    "video": "videos/video1.mp4",
    "title": "视频1标题",
    "desc": "视频1描述",
    "tags": ["标签1", "标签2"]
  },
  {
    "platform": "xiaohongshu",
    "video": "videos/video2.mp4",
    "title": "视频2标题",
    "desc": "视频2描述",
    "tags": ["标签3", "标签4"]
  }
]
```

执行批量发布：

```bash
python scripts/batch_publish.py --list publish_list.json
```

## 🔧 高级功能

### 1. 最佳发布时间推荐

```python
from scripts.best_time import BestTimeRecommender

recommender = BestTimeRecommender()
best_time = recommender.recommend(
    platform="douyin",
    target_audience="18-24",
    content_type="video"
)

print(best_time)
# {'time': '2026-06-13 18:30', 'reason': '目标受众活跃高峰'}
```

### 2. 发布后数据追踪

```python
from scripts.tracker import DataTracker

tracker = DataTracker()
data = tracker.track(
    video_url="https://douyin.com/video/xxx",
    platform="douyin",
    track_days=7
)

print(data)
# {'views': 10000, 'likes': 500, 'comments': 50, ...}
```

### 3. 智能标签生成

```python
from scripts.tag_generator import TagGenerator

generator = TagGenerator()
tags = generator.generate(
    video_path="path/to/video.mp4",
    title="AI工具教程",
    description="介绍最新的AI工具",
    platform="douyin"
)

print(tags)
# ["AI工具", "教程", "科技", "干货"]
```

## 📋 配置文件详解

### config.json

```json
{
  "platforms": {
    "douyin": {
      "enabled": true,
      "client_key": "...",
      "client_secret": "...",
      "auto_schedule": true,
      "best_time": true
    }
  },
  "global": {
    "retry_count": 3,
    "retry_delay": 5,
    "notify_on_success": true,
    "notify_on_failure": true
  }
}
```

**配置项说明：**

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `platforms.*.enabled` | 是否启用该平台 | `false` |
| `global.retry_count` | 失败重试次数 | `3` |
| `global.retry_delay` | 重试延迟（秒） | `5` |
| `best_time.enabled` | 是否启用最佳时间推荐 | `true` |

## 📊 工作流程

```
准备内容 → 生成元数据 → 选择平台 → 推荐时间 → 执行发布 → 追踪数据 → 生成报告
```

## 🔍 故障排查

### 常见问题

#### 1. API凭证错误

**错误**：`Authentication failed`

**解决**：
- 检查 `config.json` 中的凭证是否正确
- 确认API权限是否已开通
- 重新获取Token（可能已过期）

#### 2. 视频格式不支持

**错误**：`Video format not supported`

**解决**：
- 转换为平台支持的格式（通常MP4 H.264）
- 使用 `video-auto-generator` Skill生成兼容格式

#### 3. 网络错误

**错误**：`Network error, retry failed`

**解决**：
- 检查网络连接
- 增加 `retry_count` 和 `retry_delay`
- 使用代理（如有需要）

## 📚 安装方法

### 方式一：SkillHub 在线安装（推荐）

```bash
skillhub install auto-publish
```

### 方式二：本地 Zip 安装

```bash
skillhub install /path/to/auto-publish-x.x.x.zip
```

### 方式三：手动安装

1. 下载 Skill 包，解压到 `~/.qclaw/skills/auto-publish/`
2. 配置 `scripts/config.json` 中的平台 API 凭证
3. 重启 QClaw Gateway

## 📚 依赖说明

| 依赖 | 版本要求 | 用途 | 必选 |
|------|---------|------|------|
| Python | 3.8+ | 运行环境 | 必选 |
| requests | 最新版 | HTTP 请求（API 调用） | 必选 |
| Pillow | 最新版 | 图片处理（封面生成） | 可选 |
| moviepy | 最新版 | 视频处理 | 可选 |
| 各平台 API 凭证 | — | 抖音 / 小红书 / B站 / YouTube | 必选 |

**requests 安装**：
```bash
pip install requests pillow
```

## 📄 许可证

MIT License

## 🏆 完整工具链

这个 Skill 可以与其他 Skill 配合使用，形成完整的内容创作工具链：

1. **content-idea-generator** → 生成选题
2. **video-auto-generator** → 生成视频
3. **auto-publish** → 自动发布 ✅ 您在这里
4. **hot-topic-tracker** → 追踪热点
5. **competitor-price-monitor** → 监控竞品

## 更新日志

### v1.1.0 (2026-06-14)

- 补充 ClawHub 发布标准内容（徽章、截图、安装命令、依赖说明）
- 移除所有硬编码 AI 模型名
- 统一格式和风格

### v1.0.0 (2026-06-13)

- 初始版本
- 支持抖音、小红书、B站、YouTube
- 自动填写标题、标签、描述
- 最佳发布时间推荐
- 发布后数据追踪
- 批量发布队列管理

## 许可证

MIT License

## 联系方式

- QClaw 官方支持
- GitHub Issues：https://github.com/qclaw/auto-publish/issues
- ClawHub：https://clawhub.ai/skills/auto-publish

## 📞 支持

如有问题，请访问：
- GitHub Issues：https://github.com/qclaw/auto-publish/issues
- ClawHub：https://clawhub.ai/skills/auto-publish

---

**祝您创作顺利！** 🎉
