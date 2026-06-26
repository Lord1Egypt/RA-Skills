---
name: binance-square-hot-posts
description: 获取币安广场12小时内散户讨论话题，输出内容、浏览量、评论数到表格，剔除大V和机构号。
---

# 币安广场散户热帖抓取

## 功能
访问币安广场 API 获取 12 小时内的热帖内容，过滤掉大 V、机构账号，只保留真实散户讨论的话题，并以表格形式输出。

## API 信息
- **URL**: `https://www.bmwweb.cc/bapi/composite/v9/friendly/pgc/feed/feed-recommend/list`
- **方法**: POST

## 必需请求头
```json
{
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate, br",
  "Origin": "https://www.bmwweb.cc",
  "Referer": "https://www.bmwweb.cc/zh-CN/square",
  "Bnc-Uuid": "2510c36b-606d-450c-ade3-4cde8745680b",
  "Clienttype": "web",
  "Versioncode": "web",
  "Cookie": "bnc-uid=2510c36b-606d-450c-ade3-4cde8745680b; lang=zh-CN"
}
```

## 请求参数
```json
{
  "pageIndex": 1,
  "pageSize": 50,
  "scene": "web-homepage",
  "contentIds": []
}
```

## 剔除规则
过滤以下账号类型：
- `authorVerificationType > 0` (认证用户/大 V)
- `authorRole != 0` (特殊角色用户)
- 账号名含关键词: "官方"、"交易所"、"财经"、"研究院"、"机构"、"认证"、"Admin"

## 输出格式
表格列：内容摘要 | 作者 | 发布时间 | 浏览量 | 评论数

## 使用方式
直接调用此 skill 获取币安广场散户热帖数据。