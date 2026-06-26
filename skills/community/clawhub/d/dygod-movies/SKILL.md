---
name: dygod-movies
description: >
  爬取电影天堂(dygod.net)最新电影和电视剧信息，支持查询最近更新、高分电影，
  并可一键下载到群晖NAS。当用户询问最近更新的电影/电视剧、高分电影、或想下载影视资源时使用此技能。
---

# 电影天堂 (DYGod) 影视爬虫技能

爬取电影天堂最新电影和电视剧，支持查询和下载到群晖NAS。

## 功能

1. **查询最新电影** - 获取电影天堂最新更新的电影列表
2. **查询高分电影** - 筛选豆瓣/IMDb高分电影
3. **查询电视剧** - 支持国产剧、日韩剧、欧美剧
4. **搜索影视** - 按片名搜索电影和电视剧
5. **下载到群晖** - 一键添加到群晖DownloadStation下载

## 影视资源分类

| 分类 | URL | 说明 |
|------|-----|------|
| 最新电影 | `/html/gndy/dyzz/` | 最新电影资源 |
| 国产剧 | `/html/tv/hytv/` | 国产电视剧 |
| 日韩剧 | `/html/tv/rihantv/` | 日韩电视剧 |
| 欧美剧 | `/html/tv/oumeitv/` | 欧美电视剧 |

## 使用方法

### 1. 爬取/刷新电影数据

```bash
python scripts/dygod_crawler.py --pages 2 --no-cache
```

参数说明：
- `--pages N` - 爬取N页（每页约25部电影）
- `--no-cache` - 忽略缓存，重新爬取
- 不带参数时使用缓存数据（缓存1小时）

### 2. 查询最近更新的电影

```bash
python scripts/dygod_crawler.py --recent 7
```

显示最近7天内更新的电影。

### 3. 查询高分电影

```bash
python scripts/dygod_crawler.py --high-score
```

筛选豆瓣≥7.5或IMDb≥7.0的高分电影。

### 4. 搜索电影

```bash
python scripts/dygod_crawler.py --search "肖申克"
```

按片名、译名、导演、主演搜索。

### 5. 搜索电视剧

```python
from scripts.dygod_crawler import search_tv, get_tv_detail

# 搜索电视剧
results = search_tv("我喜欢的人变成猫")

# 获取详情和下载链接
if results:
    detail = get_tv_detail(results[0]["detail_url"])
    print(detail["download_links"])
```

## 输出JSON格式

脚本也支持作为模块导入，返回JSON数据：

```python
from scripts.dygod_crawler import get_movies, get_high_score_movies, search_movies

# 获取电影列表
movies = get_movies(max_pages=2)

# 获取高分电影
high_score = get_high_score_movies(movies, min_douban=8.0)

# 搜索电影
results = search_movies(movies, "黑客帝国")

# 每部电影的字段
# {
#   "title": "原始标题",
#   "片名": "克莱默夫妇",
#   "译名": "Kramer vs. Kramer",
#   "年代": "1979",
#   "产地": "美国",
#   "类别": "剧情/家庭",
#   "豆瓣评分": 8.5,
#   "IMDb评分": 7.8,
#   "导演": "罗伯特·本顿",
#   "主演": "达斯汀·霍夫曼",
#   "文件大小": "3311 MB",
#   "download_links": ["magnet:...", "ftp://..."]
# }
```

## 群晖NAS下载

使用 synology-dsm 技能将电影下载到群晖。

### 登录群晖获取SID

```bash
curl.exe -s "http://192.168.123.223:5000/webapi/entry.cgi?api=SYNO.API.Auth&version=6&method=login&account=xiaoai&passwd=Xx654321&session=DownloadStation&format=sid"
```

返回：`{"success":true,"data":{"sid":"YOUR_SID"}}`

### 添加下载任务

**注意：DownloadStation API路径是 `/webapi/DownloadStation/task.cgi`**

```bash
# 下载电影 → 存放到 /video/电影
# destination 参数格式：共享文件夹名/子目录，如 "video/电影"
curl.exe -s -X POST -d "api=SYNO.DownloadStation.Task&version=1&method=create&uri=magnet:?xt=urn:btih:XXX&destination=video/电影&_sid=YOUR_SID" "http://192.168.123.223:5000/webapi/DownloadStation/task.cgi"

# 下载电视剧 → 存放到 /video/电视剧
curl.exe -s -X POST -d "api=SYNO.DownloadStation.Task&version=1&method=create&uri=magnet:?xt=urn:btih:XXX&destination=video/电视剧&_sid=YOUR_SID" "http://192.168.123.223:5000/webapi/DownloadStation/task.cgi"
```

### 使用Python脚本下载

```python
from scripts.dygod_crawler import download_movie, syno_add_download

# 下载电影到指定目录
result = syno_add_download(
    uri='magnet:?xt=urn:btih:XXX',
    destination='video/电影'  # 下载到 /video/电影
)
print(result)  # {'success': True, 'task_id': 'xxx'}

# 或者直接传入电影信息下载
movie = {
    '片名': '黑暗之城',
    'download_links': ['magnet:?xt=urn:btih:XXX']
}
download_movie(movie, destination='video/电影')
```

### 查看下载任务

```bash
curl.exe -s "http://192.168.123.223:5000/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&method=list&additional=transfer&_sid=YOUR_SID"
```

### 删除下载任务

```bash
curl.exe -s "http://192.168.123.223:5000/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&method=delete&id=TASK_ID&force_complete=false&_sid=YOUR_SID"
```

## 交互流程示例

用户问：**最近有什么好看的电影？**

1. 调用爬虫获取最新电影数据
2. 筛选高分电影展示给用户
3. 用户选择想看的电影
4. 提取下载链接，添加到群晖下载

用户问：**帮我下载《肖申克的救赎》**

1. 搜索电影
2. 展示搜索结果让用户确认版本
3. 获取下载链接
4. 添加到群晖DownloadStation

用户问：**帮我找电视剧《我喜欢的人变成猫是怎样的体验》**

1. 搜索电视剧分类（国产剧/日韩剧/欧美剧）
2. 找到匹配结果
3. 获取详情页下载链接
4. 用户确认后添加到群晖下载

## 数据缓存

- 电影缓存：`data/movies_cache.json`
- 电视剧缓存：`data/tv_cache.json`
- 缓存有效期：1小时
- 手动刷新：使用 `--no-cache` 参数

## 注意事项

1. **爬取频率**：脚本已加入请求延时，请勿频繁爬取
2. **下载链接**：包含 magnet 和 ftp 两种格式，优先使用 magnet
3. **版权声明**：仅供学习研究使用，请勿用于商业用途
