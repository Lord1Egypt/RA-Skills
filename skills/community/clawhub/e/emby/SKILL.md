---
name: emby
description: Emby Server API integration for managing media libraries, users, devices, live TV, and encoding settings. Use when interacting with Emby media server including: (1) Querying movies, shows, artists, albums, genres, (2) Managing users and authentication, (3) Controlling playback sessions, (4) Live TV and recording management, (5) Library and folder operations, (6) Device management, (7) System configuration and encoding options.
---

# Emby Server API Skill

## Configuration

配置参数位于 `emby.py` 文件顶部:

```python
BASE_URL = "https://emby.example.com/emby"  # 修改为你的Emby服务器地址
API_KEY = "652436b1ffa84d9a85f579eeb34b87aa"     # 修改为你的API Key
```

## 使用方式

导入 `emby` 模块并调用相应函数:

```python
from emby import get_items, get_user_by_id, download_item_image
```

## 返回值类型

- **JSON返回**: 大多数API调用返回 `Dict` (字典)
- **Stream返回**: 图片、视频、音频下载等返回 `Response` 对象或 `bytes`

### Stream 类型函数 (返回 Response)

| 函数 | 用途 |
|------|------|
| `get_item_image()` | 获取媒体项图片 |
| `download_item_image()` | 下载媒体项图片到文件或返回bytes |
| `get_video_stream_url()` | 获取视频流地址 |
| `download_video()` | 下载视频到文件或返回bytes |
| `get_audio_stream_url()` | 获取音频流地址 |
| `download_audio()` | 下载音频到文件或返回bytes |
| `post_devices_camera_uploads()` | 上传摄像头内容 |
| `restore_backup()` | 恢复备份 |

## 常用函数示例

### 查询媒体库

```python
# 查询所有电影
movies = get_items(include_item_types="Movie", recursive=True, limit=20)

# 搜索媒体
results = get_items(search_term="avatar", recursive=True)

# 按类型查询
series = get_items(include_item_types="Series", recursive=True)
```

### 用户管理

```python
# 获取所有用户
users = query_users()

# 获取指定用户
user = get_user_by_id("user-id-here")

# 标记影片为已播放
mark_item_played(user_id="user-id", item_id="item-id")
```

### 图片操作

```python
# 获取图片Response对象
resp = get_item_image(item_id="xxx", image_type="Primary", index=0)

# 下载图片到文件
download_item_image(item_id="xxx", image_type="Primary", output_path="poster.jpg")

# 直接获取图片bytes
bytes_data = download_item_image(item_id="xxx", image_type="Primary")
```

### 视频/音频下载

```python
# 下载视频
download_video(item_id="xxx", output_path="movie.mp4")

# 下载音频
download_audio(item_id="xxx", output_path="song.mp3")
```

### Live TV

```python
# 获取频道
channels = get_live_tv_channels()

# 获取节目指南
programs = get_live_tv_programs(channel_id="xxx", start_time="2024-01-01", end_time="2024-01-07")

# 获取录制
recordings = get_live_tv_recordings()
```

## 完整API列表

详见 `emby.py` 文件，包含以下分类:

- Artists - 艺术家相关
- Albums - 专辑相关
- Codecs - 编解码器
- Channels/Collections - 频道/收藏
- Devices - 设备管理
- Genres - 类型
- Items - 媒体项
- Users - 用户管理
- UserData - 用户数据
- Sessions - 会话
- Playlists - 播放列表
- Plugins - 插件
- Library - 媒体库
- LiveTV - 直播电视
- LiveStreams - 直播流
- Localization - 本地化
- Movies - 电影
- AudioBooks - 有声书
- Auth - 认证
- Backup - 备份
- Branding - 品牌
- Connect - Emby Connect
- DisplayPreferences - 显示偏好
- DLNA - DLNA
- Encoding - 编码设置
- Environment - 环境
- Images - 图片
- Packages - 包
- Persons - 人物
- Studios - 工作室
- Tags - 标签
- Trailers - 预告片
- Years - 年份
- Features - 特性
- UI - 用户界面
- Videos - 视频操作
- Web - Web配置
- OpenAPI - OpenAPI文档
- Playback - 播放
- Hubs - 中心
- Search - 搜索
