---
name: movie-search
description: 搜索电视剧、动漫、电影的百度网盘和夸克网盘资源链接。当用户询问任何影视作品的网盘链接、资源、下载地址时使用此技能，包括但不限于"有XX的网盘链接吗"、"XX在哪里下载"、"找XX的资源"等问题。
---

# 影视资源搜索技能

当用户询问电视剧、动漫或电影的百度网盘或夸克网盘链接时，使用此技能。

## 触发条件

用户询问包含以下关键词的内容：
- 电视剧/电视/剧集 + 网盘/百度/夸克/链接/资源
- 动漫/动画 + 网盘/百度/夸克/链接/资源
- 电影 + 网盘/百度/夸克/链接/资源

## 使用方法

1. 从用户的问题中提取影视作品的名称（keyword）
2. 调用 API 接口获取资源信息
3. 格式化展示结果给用户

## API 接口

- 接口地址：`https://meng-ge.top/api/movieData/getMoviesByType`
- 请求方法：GET
- 请求参数：
  - `page`: 页码（默认 1）
  - `size`: 每页数量（默认 50）
  - `keyword`: 影视作品名称（需要 URL 编码）

## 响应格式

```json
{
  "code": 0,
  "timestamp": 1773299629789,
  "message": "操作成功",
  "data": [
    {
      "id": 2605,
      "movieName": "逐玉.1080P更 15",
      "baiduLink": "https://pan.baidu.com/s/xxx?pwd=1120",
      "quarkLink": "https://pan.quark.cn/s/xxx",
      "type": "TV",
      "updateTime": "2026-03-12 11:55:10",
      "hash": "EaM7XP",
      "hot": true
    }
  ]
}
```

## 展示格式

当获取到结果后，按以下格式展示：

```
找到 [影视名称] 的资源：

1. [movieName]
   - 类型：[type 转换为中文]
   - 百度网盘：[baiduLink]
   - 夸克网盘：[quarkLink]
   - 更新时间：[updateTime]

2. ...
```

类型映射：
- TV: 电视剧
- TV_4K: 电视剧（4K）
- MOVIE: 电影
- MOVIE_4K: 电影（4K）
- ANIME: 动漫
- ANIME_4K: 动漫（4K）

## 注意事项

1. keyword 需要进行 URL 编码
2. 如果没有找到结果（data 为空数组），告知用户未找到相关资源
3. 如果 API 返回错误（code 不为 0），告知用户查询失败
4. 优先展示热门资源（hot 为 true）
5. 如果有多个版本（1080P、4K等），都展示给用户选择
