---
name: gequhai-music
description: >
  搜索和下载歌曲海(gequhai.com)的音乐，支持搜索歌曲、获取下载链接（优先无损/高品质），
  并可一键下载到群晖NAS。当用户询问歌曲、搜索音乐、或想下载歌曲时使用此技能。
nacos:
  namespace: ai_space
  service: gequhai-music
  port: 8001
  capabilities: [search, download, ranking]
---

# 歌曲海 (Gequhai) 音乐搜索与下载技能

搜索歌曲海音乐，支持下载到群晖NAS。

## 功能

1. **搜索歌曲** - 按歌名/歌手搜索
2. **获取下载链接** - 优先无损/高品质，其次是标准品质
3. **排行榜** - 热门榜、新歌榜、飙升榜、抖音榜等
4. **下载到群晖** - 一键添加到群晖DownloadStation

## 网站信息

- 网站：https://www.gequhai.com/
- 特点：免费音乐搜索下载，支持高品质/无损音乐

## 下载链接类型

| 类型 | 说明 | 可下载到群晖 |
|------|------|-------------|
| 标准品质（API） | 通过API获取的直接mp3链接 | ✅ 可以 |
| 高品质（直接链接） | 页面上的直接mp3/flac链接 | ✅ 可以 |
| 高品质（网盘链接） | 夸克网盘等分享链接 | ❌ 需手动下载 |

**重要：** API请求需要带上 `X-Custom-Header: SecretKey` 才能成功！

## 使用方法

### 1. 搜索歌曲

```bash
python scripts/gequhai_crawler.py --search "青花瓷"
```

### 2. 获取歌曲详情和下载链接

```bash
python scripts/gequhai_crawler.py --detail 553
```

### 3. 搜索并下载

```bash
python scripts/gequhai_crawler.py --download "周杰伦 晴天"
```

### 4. Python脚本调用

```python
from scripts.gequhai_crawler import search_songs, get_download_url, download_song

# 搜索歌曲
songs = search_songs("青花瓷")
for s in songs[:5]:
    print(f"[{s['id']}] {s['title']} - {s['artist']}")

# 获取下载链接
detail = get_download_url("553")
print(f"标题: {detail['title']}")
print(f"下载链接: {detail.get('url', detail.get('netdisk_url'))}")
print(f"品质: {detail.get('quality')}")

# 下载到群晖
result = download_song(detail, destination="download/音乐下载")
print(f"下载结果: {result}")
```

## 群晖下载配置

| 配置项 | 值 |
|--------|-----|
| 主机 | `192.168.123.223:5000` |
| 用户 | `xiaoai` |
| 默认下载目录 | `download/音乐下载` |

## 交互流程示例

用户问：**帮我下载周杰伦的青花瓷**

1. 搜索"青花瓷"
2. 获取第一首歌的下载链接
3. 如果是直接链接 → 添加到群晖下载
4. 如果是网盘链接 → 告知用户网盘地址

用户问：**最近有什么好听的歌？**

1. 获取热门歌曲列表
2. 展示给用户选择
3. 用户选择后下载

## 注意事项

1. **API验证**：必须带上 `X-Custom-Header: SecretKey` header，否则API返回403
2. **Session**：需要使用Session保持cookie，先访问播放页再请求API
3. **下载链接类型**：高品质版本通常是网盘链接，标准品质是直接mp3链接
4. **请求频率**：避免频繁请求，以免被封IP

## 关键代码

```python
# API请求必须带上这个header
api_headers = {
    "X-Requested-With": "XMLHttpRequest",
    "X-Custom-Header": "SecretKey",  # 关键！
}

# 使用Session保持cookie
session = requests.Session()
# 先访问播放页面获取cookie
session.get(f"{BASE_URL}/play/{song_id}")
# 再请求API
session.post(f"{BASE_URL}/api/music", headers=api_headers, data={...})
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 未找到歌曲 | 关键词不匹配 | 尝试其他关键词 |
| 没有下载链接 | 歌曲暂无资源 | 换一首歌 |
| 网盘链接 | 高品质版本在网盘 | 手动下载或使用标准品质 |
