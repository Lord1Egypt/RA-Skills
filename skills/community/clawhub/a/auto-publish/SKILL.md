# auto-publish

多平台自动发布器 — 自动将视频/内容发布到抖音、小红书、B站、YouTube等平台。

## 功能特性

### 核心功能
- ✅ **多平台支持**：抖音、小红书、B站、YouTube、快手
- ✅ **自动填写**：标题、标签、描述、封面
- ✅ **智能推荐**：最佳发布时间推荐（基于平台算法）
- ✅ **批量发布**：队列管理，支持批量上传
- ✅ **数据追踪**：发布后浏览量、点赞、评论追踪
- ✅ **失败重试**：网络错误自动重试，发布失败告警

### 支持平台详情

| 平台 | 状态 | 功能 |
|------|------|------|
| 抖音 | ✅ 支持 | 视频发布、话题标签、@好友 |
| 小红书 | ✅ 支持 | 图文/视频发布、话题标签 |
| B站 | ✅ 支持 | 视频发布、分区选择、标签 |
| YouTube | ✅ 支持 | 视频发布、多语言字幕 |
| 快手 | ⏳ 开发中 | 即将支持 |

---

## 快速开始

### 1. 准备工作

#### 获取平台API凭证

**抖音：**
1. 访问 https://open.douyin.com/
2. 注册开发者账号
3. 创建应用，获取 `client_key` 和 `client_secret`

**小红书：**
1. 访问 https://open.xiaohongshu.com/
2. 申请开放平台权限
3. 获取 API Token

**B站：**
1. 访问 https://open.bilibili.com/
2. 创建应用，获取 `access_key`

**YouTube：**
1. 访问 https://console.cloud.google.com/
2. 创建项目，启用 YouTube Data API v3
3. 获取 OAuth 2.0 凭证

#### 配置凭证

编辑 `scripts/config.json`：

```json
{
  "douyin": {
    "client_key": "YOUR_CLIENT_KEY",
    "client_secret": "YOUR_CLIENT_SECRET"
  },
  "xiaohongshu": {
    "api_token": "YOUR_API_TOKEN"
  },
  "bilibili": {
    "access_key": "YOUR_ACCESS_KEY"
  },
  "youtube": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
  }
}
```

---

### 2. 发布单个视频

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

# 初始化发布器
publisher = AutoPublisher()

# 发布到抖音
result = publisher.publish(
    platform="douyin",
    video_path="path/to/video.mp4",
    title="我的视频标题",
    description="视频描述 #话题1 #话题2",
    tags=["话题1", "话题2", "话题3"],
    publish_time="best"  # 自动选择最佳发布时间
)

print(result)
# 输出: {'success': True, 'url': 'https://douyin.com/video/xxx', 'publish_time': '2026-06-13 18:00'}
```

---

### 3. 批量发布

#### 准备发布列表

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

#### 执行批量发布

```bash
python scripts/batch_publish.py --list publish_list.json
```

---

## 高级功能

### 1. 最佳发布时间推荐

基于平台算法和用户活跃数据，推荐最佳发布时间：

```python
from scripts.best_time import BestTimeRecommender

recommender = BestTimeRecommender()
best_time = recommender.recommend(platform="douyin", target_audience="18-24")

print(best_time)
# 输出: {'time': '2026-06-13 18:30', 'reason': '目标受众活跃高峰'}
```

### 2. 发布后数据追踪

自动追踪发布后的数据变化：

```python
from scripts.tracker import DataTracker

tracker = DataTracker()
data = tracker.track(video_url="https://douyin.com/video/xxx", platform="douyin")

print(data)
# 输出: {'views': 10000, 'likes': 500, 'comments': 50, 'shares': 100}
```

### 3. 智能标签生成

基于视频内容自动生成标签：

```python
from scripts.tag_generator import TagGenerator

generator = TagGenerator()
tags = generator.generate(video_path="path/to/video.mp4", platform="douyin")

print(tags)
# 输出: ["AI工具", "视频生成", "教程", "科技"]
```

---

## 配置文件详解

### config.json

```json
{
  "platforms": {
    "douyin": {
      "enabled": true,
      "client_key": "",
      "client_secret": "",
      "auto_schedule": true,
      "best_time": true
    },
    "xiaohongshu": {
      "enabled": true,
      "api_token": "",
      "auto_schedule": true
    },
    "bilibili": {
      "enabled": true,
      "access_key": "",
      "auto_schedule": false
    },
    "youtube": {
      "enabled": false,
      "client_id": "",
      "client_secret": ""
    }
  },
  "global": {
    "retry_count": 3,
    "retry_delay": 5,
    "notify_on_success": true,
    "notify_on_failure": true,
    "save_log": true
  }
}
```

---

## 工作流程

### 完整发布流程

1. **准备内容** → 视频/图文文件
2. **生成元数据** → 标题、描述、标签（可自动生成）
3. **选择平台** → 单个或批量
4. **推荐时间** → 自动推荐最佳发布时间
5. **执行发布** → 调用平台API上传
6. **追踪数据** → 定期获取浏览量、点赞等数据
7. **生成报告** → 汇总发布结果和数据

---

## 故障排查

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

---

## 开发者信息

- **版本**：1.0.0
- **作者**：QClaw Team
- **依赖**：
  - Python 3.8+
  - requests
  - pillow（图片处理）
  - moviepy（视频处理，可选）

---

## 许可证

MIT License

---

## 更新日志

### v1.0.0 (2026-06-13)
- ✅ 初始版本
- ✅ 支持抖音、小红书、B站、YouTube
- ✅ 自动填写标题、标签、描述
- ✅ 最佳发布时间推荐
- ✅ 发布后数据追踪
- ✅ 批量发布队列管理

---
## 💰 付费增值服务

想要更省事？我还提供：

| 服务 | 价格 | 内容 |
|------|------|------|
| 🚗 代安装调试 | ¥68/次 | 帮你安装配置，解决环境问题 |
| 🛠️ 定制技能开发 | ¥200起 | 根据需求开发专属技能 |
| 🚀 视频自动化陪跑 | ¥999/月 | 从0到1搭建完整视频自动化 |
| 📦 技能全家桶 | ¥199 | 11个AI技能永久用 + 代安装 |

**微信咨询**：[微信号待填写]

---
