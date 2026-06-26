---
name: asoul-support
description: "A-SOUL 粉丝应援工具 — 检测开播自动点亮粉丝牌+移动端心跳挂机涨亲密度、视频点赞/投币/收藏、动态点赞。纯Python实现，零外部依赖。触发词：A-SOUL、asoul、签到、点赞、三连、应援、动态、点亮、粉丝牌、心跳、挂机、直播、嘉然、贝拉、乃琳、心宜、思诺。"
---

# A-SOUL Support

A-SOUL 粉丝自动应援工具 — 开播检测 + 粉丝牌点亮 + 移动端心跳挂机涨亲密度 + 视频/动态互动。

纯 Python 实现，零外部依赖（不需要 Node.js 签名服务）。

## 触发规则

| 模式 | 示例 |
|------|------|
| 包含 `A-SOUL` / `asoul` + `签到` / `点亮` | "帮我给asoul签到" |
| 包含 `A-SOUL` / `asoul` + `心跳` / `挂机` | "给asoul直播间挂机" |
| 包含 `A-SOUL` / `asoul` + `点赞` / `三连` | "给asoul视频点赞" |
| 包含 `A-SOUL` / `asoul` + `动态` | "给asoul动态点赞" |
| 包含成员名 + `签到` / `点赞` / `挂机` | "给嘉然签到" |
| 包含 `应援` | "A-SOUL每日应援" |

## 内置成员

| 成员 | UID | 直播间 |
|------|-----|--------|
| 嘉然 | 672328094 | 22637261 |
| 贝拉 | 672353429 | 22632424 |
| 乃琳 | 672342685 | 22625027 |
| 心宜 | 3537115310721181 | 30849777 |
| 思诺 | 3537115310721781 | 30858592 |

## 功能 1 — 心跳挂机（涨亲密度，需开播）

使用 B站移动端心跳协议（`mobileHeartBeat`），纯 Python 签名（sha512→sha3_512→sha384→sha3_384→blake2b），零外部依赖。

检测成员是否在播 → 自动佩戴粉丝牌 → 发弹幕点亮 → 心跳挂机。
每 5 分钟 +6 亲密度，挂满 30/天/成员。

```bash
python3 {baseDir}/scripts/heartbeat.py
python3 {baseDir}/scripts/heartbeat.py --members 嘉然,贝拉
python3 {baseDir}/scripts/heartbeat.py --check-only
python3 {baseDir}/scripts/heartbeat.py --duration 30
python3 {baseDir}/scripts/heartbeat.py --until-offline
```

## 功能 2 — 粉丝牌点亮（需开播）

检测开播后发 10 条弹幕点亮牌子（保持 3 天可见）。
**注意：需要成员正在直播时才能点亮。**

```bash
python3 {baseDir}/scripts/checkin.py --live-only
python3 {baseDir}/scripts/checkin.py --live-only --members 嘉然,贝拉
python3 {baseDir}/scripts/checkin.py --live-only --msg 签到 --msg 加油
```

## 功能 3 — 视频点赞/投币/收藏（不需要开播）

给成员新发布的视频批量互动。默认仅点赞，投币和收藏需明确指定。

```bash
python3 {baseDir}/scripts/videos.py --month 3
python3 {baseDir}/scripts/videos.py --days 7 --coin --fav
python3 {baseDir}/scripts/videos.py --month 3 --members 嘉然 --coin --fav
```

## 功能 4 — 动态点赞（不需要开播）

```bash
python3 {baseDir}/scripts/dynamics.py --month 3
python3 {baseDir}/scripts/dynamics.py --days 7
python3 {baseDir}/scripts/dynamics.py --days 7 --members 嘉然,贝拉
```

## 推荐 OpenClaw 定时任务

```
每 30 分钟检测一次开播，开播了就自动弹幕点亮+挂机涨亲密度：
openclaw cron add --name "A-SOUL开播挂机" --cron "*/30 * * * *" \
  --message "帮我检测A-SOUL成员是否在直播，在播的话先挂机涨亲密度，再发弹幕点亮牌子" \
  --timeout-seconds 21600

视频和动态由 GitHub Actions 自动处理（每 2 天），无需额外配置。
```

## Cookie 设置

与 `bilibili-live-checkin` 共用 Cookie。如果已在那个 skill 设置过，无需重复操作。

手动设置：
```bash
python3 {baseDir}/scripts/checkin.py --save-cookie --sessdata "{SESSDATA}" --bili-jct "{bili_jct}"
```
