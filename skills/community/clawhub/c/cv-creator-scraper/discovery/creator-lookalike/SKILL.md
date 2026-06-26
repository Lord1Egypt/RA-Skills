---
name: creator-lookalike
description: |
  相似达人发现能力，支持种子达人解析、相似度匹配、跨平台搜索。通过 username、profile_url 或自动全平台搜索找到风格相似的创作者。
  Use when: 相似达人, 类似达人, similar creators, lookalike, find similar
compatibility: Node.js 20.6+
metadata:
  layer: discovery
  parent: creator-scraper-cv
---

## 概述

基于种子达人查找风格相似的创作者，支持同平台匹配和跨平台发现（如从 TikTok 达人找到 YouTube 上的相似创作者）。

## 脚本引用

| 脚本 | 路径 | 模式 | 状态 |
|------|------|------|------|
| find_lookalike.mjs | `../../scripts/find_lookalike.mjs` | Sync, 自动解析 username/URL | ✅ |

## 输入方式

API 内部自动将 username/URL 解析为平台 ID，无需额外 resolve 步骤。

### 方式一：username + platform（指定平台）

明确指定达人所在平台，直接在该平台查找相似达人：

```bash
node ../../scripts/find_lookalike.mjs '{"username":"creator_demo","platform":"tiktok","limit":10}'
```

### 方式二：profile_url（自动识别平台）

传入达人主页链接，API 自动解析平台和用户名：

```bash
node ../../scripts/find_lookalike.mjs '{"profile_url":"https://www.tiktok.com/@creator_demo","limit":10}'
```

支持的 URL 格式：
- TikTok: `https://www.tiktok.com/@username`
- YouTube: `https://www.youtube.com/@username`
- Instagram: `https://www.instagram.com/username`

### 方式三：username only（搜索全平台）

仅传入用户名，不指定平台，API 自动在 TikTok、YouTube、Instagram 三个平台搜索匹配：

```bash
node ../../scripts/find_lookalike.mjs '{"username":"creator_demo","limit":10}'
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `username` | string | 二选一 | 达人用户名（不含 `@`），与 `profile_url` 二选一 |
| `platform` | string | 否 | 种子达人平台：`tiktok` / `youtube` / `instagram`，省略则搜索全平台 |
| `profile_url` | string | 二选一 | 达人主页链接（自动识别平台），与 `username` 二选一 |
| `target_platform` | string | 否 | 目标搜索平台，省略则与种子达人同平台。设为不同平台可实现跨平台搜索 |
| `target_region` | string | 否 | 目标国家代码，`all` 表示不限 |
| `target_language` | string | 否 | 目标语言代码，`all` 表示不限 |
| `limit` | integer | 否 | 返回数量，默认 20，最大 50 |
| `follower_min` | integer | 否 | 最小粉丝数 |
| `follower_max` | integer | 否 | 最大粉丝数 |
| `avg_views_min` | integer | 否 | 最小平均播放量 |
| `avg_views_max` | integer | 否 | 最大平均播放量 |
| `female_rate_min` | number | 否 | 最小女性受众比例（0~100） |
| `lang` | string | 否 | 响应语言：`cn` / `en`，仅控制返回字段翻译，不筛选达人 |
| `service_level` | string | 否 | 服务等级，默认 `S1` |

### 跨平台搜索说明

设置 `target_platform` 与种子达人不同平台，可发现跨平台相似达人：

```bash
# 从 TikTok 达人找 YouTube 上的相似创作者
node ../../scripts/find_lookalike.mjs '{"username":"creator_demo","platform":"tiktok","target_platform":"youtube","limit":10}'
```

## 输出格式

```
🔍 找到 N 个与 @seed_username 相似的达人

📊 相似达人列表

| #   | 用户名      | 昵称        | 粉丝数  | 平均播放 | 互动率  | 相似度  | 国家 | 主页链接          |
| --- | ----------- | ----------- | ------- | -------- | ------- | ------ | ---- | ----------------- |
| 1   | username1   | Nickname1   | 120K    | 3.8万    | 7.20%   | 85.0%  | US   | [查看][link1]     |
| 2   | username2   | Nickname2   | 95.5K   | 2.1万    | 5.50%   | 78.3%  | US   | [查看][link2]     |

[link1]: https://www.tiktok.com/@username1
[link2]: https://www.tiktok.com/@username2

📈 统计信息
• 种子达人：@seed_username（平台ID：7123456789）
• 结果总数：N 个相似达人
• 本次消耗：10 积分
• 剩余配额：xxx 次
• 请求ID：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

返回字段：`uid`、`username`、`nickname`、`avatar_url`、`profile_url`、`country_code`、`followers_count`、`avg_views`、`engagement_rate`、`match_score`。

其中 `match_score` 为相似度评分（0~100），按相似度降序排列。

## 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 40401 | 达人不在数据库中 | 告知用户该达人尚未被平台收录，建议换一个达人或提交采集任务 |
| 40001 | 参数无效 | 检查 username/profile_url 格式 |
| 42902 | 每日配额耗尽 | 等待 UTC 00:00 重置或升级套餐 |

## 决策规则

- 用户给出主页链接 → 使用 `profile_url` 参数
- 用户给出用户名 + 平台 → 使用 `username` + `platform`
- 用户仅给出用户名 → 仅传 `username`，API 搜索全平台
- 用户要求"找 YouTube 上类似的" → 设置 `target_platform: "youtube"`
