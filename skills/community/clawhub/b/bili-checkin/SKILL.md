---
name: bili-checkin
description: "B站全自动签到工具 — 每日经验任务（登录+观看+分享+投币=65EXP/天）+ 直播间弹幕签到刷亲密度。支持UP主名字/UID查找直播间。触发词：B站签到、每日任务、bilibili checkin、升级、刷经验、弹幕打卡、刷亲密度。"
---

# Bili Checkin

B站全自动签到 — 每日经验任务 + 直播间弹幕签到，一键搞定。

## 触发规则

| 模式 | 示例 |
|------|------|
| 包含 `B站签到` / `B站每日` | "帮我B站签到", "B站每日任务" |
| 包含 `升级` / `刷经验` / `每日经验` | "帮我刷B站经验", "B站升级" |
| 包含 `弹幕签到` / `直播签到` | "帮我直播间签到", "弹幕打卡" |
| 包含 `bilibili` + `checkin`/`daily` | "bilibili daily checkin" |
| 包含 `亲密度` / `粉丝牌` | "刷亲密度", "升粉丝牌" |

## 两大功能

### 功能 1 — 每日经验任务（升级用）

每天最多 +65 EXP：

| 任务 | 经验 | 说明 |
|------|------|------|
| 登录 | +5 | 自动完成 |
| 观看视频 | +5 | 随机选热门视频发心跳 |
| 分享视频 | +5 | 随机分享一个视频 |
| 投币（5枚） | +50 | 默认关闭，需 --do-coin 开启（消耗硬币） |
| **合计** | **65** | |

```bash
python3 {baseDir}/scripts/daily.py
python3 {baseDir}/scripts/daily.py --do-coin
python3 {baseDir}/scripts/daily.py --do-coin --coin 3
python3 {baseDir}/scripts/daily.py --status
```

### 功能 2 — 直播间弹幕签到（亲密度用）

| 动作 | 亲密度 | 经验值 |
|------|--------|--------|
| 发送弹幕 | +2 | +5 |

```bash
python3 {baseDir}/scripts/checkin.py --room {room_id}
python3 {baseDir}/scripts/checkin.py --room {room_id} --msg "打卡"
```

## 前置：Cookie 设置（首次使用）

```bash
python3 {baseDir}/scripts/checkin.py --save-cookie --sessdata "{SESSDATA}" --bili-jct "{bili_jct}"
```

Cookie 获取方法见 `persona.md`。保存一次后所有脚本共用。

## 辅助：查找直播间

```bash
python3 {baseDir}/scripts/lookup.py "UP主名字或UID"
```
