---
name: game-valuation
description: "YY 游戏账号估值助手。用于查询某个具体游戏账号的估值价格，支持王者荣耀、和平精英、三角洲行动。当用户表达我的号值多少钱、帮我估价、账号估值、账号估价、估值查询、游戏号值多少、单个账号价格评估时使用。不要用于行情、交易行情、最近交易行情、挂牌数据、市场数据、价格分布、行情报告、账号市场分析类请求；这些应使用 mall-market-overview。"
---

# 游戏账号估值

通过游戏账号估值测试服务，帮用户查询王者荣耀、和平精英、三角洲行动某个具体账号的估值价格。

## 路由边界

Use this skill only for single-account valuation intent, such as 我的号值多少钱、帮我估价、账号估值、账号估价、估值查询、游戏号值多少、单个账号价格评估.

Do not use this skill for market行情 or data-report intent, such as 最近交易行情、账号交易行情、挂牌数据、价格分布、市场数据、行情报告、账号市场分析. Use `mall-market-overview` for those requests.

## 服务接口

默认服务前缀：`http://ruliurobot.baizhanlive.com/game_valuation`

脚本只调用三个新接口：

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/qrcode` | POST | 获取三角洲行动、和平精英扫码二维码 |
| `/api/poll?login_uuid=...` | GET | 轮询扫码结果 |
| `/api/query` | POST | 查询资产并请求 jocloud 估值 |

## 工作流程

```
1. 确认游戏 → 2. 引导填写属性 → 3. 如需扫码则获取二维码并轮询 → 4. 调用查询估值 → 5. 展示报告
```

## 支持游戏

| 游戏 | game | 是否扫码 | 必填属性 |
|------|------|---------|---------|
| 王者荣耀 | `hok` | 否 | 区服、营地 ID、实名情况、防沉迷 |
| 和平精英 | `pubg` | 是 | 区服、实名情况、防沉迷，可选 role_id |
| 三角洲行动 | `delta` | 是 | 登录方式、实名情况、安全箱 |

## 参数枚举

### 区服 server

用于王者荣耀、和平精英。

| 用户选项 | 值 |
|---------|----|
| 安卓 QQ | `android_qq` |
| 苹果 QQ | `ios_qq` |
| 安卓微信 | `android_wx` |
| 苹果微信 | `ios_wx` |

和平精英不单独询问登录方式，根据区服自动推导：`*_qq` 使用 QQ 扫码（`account_type=1`），`*_wx` 使用微信扫码（`account_type=2`）。

### 登录方式 account_type

用于三角洲行动。

| 用户选项 | 值 |
|---------|----|
| QQ | `1` |
| 微信 | `2` |

### 实名情况 real_name_status

| 用户选项 | 值 |
|---------|----|
| 可二次实名 | `re_auth_allowed` |
| 不可二次实名 | `re_auth_denied` |

### 防沉迷 anti_addiction

用于王者荣耀、和平精英。

| 用户选项 | 值 |
|---------|----|
| 有防沉迷 | `yes` |
| 无防沉迷 | `no` |

### 安全箱 safety_box

用于三角洲行动。服务端当前要求必填，必须让用户选择一个。

| 用户选项 | 值 |
|---------|----|
| 顶级安全箱 | `top` |
| 高级安全箱 | `advanced` |
| 进阶安全箱 | `intermediate` |
| 基础安全箱 | `basic` |

## 引导用户填写

根据游戏不同，用对话方式逐步询问属性。使用 AskUserQuestion 工具提供选项，不要让用户自由输入选项类属性。

### 王者荣耀

询问：
1. 区服：安卓 QQ / 苹果 QQ / 安卓微信 / 苹果微信
2. 营地 ID：用户输入，建议校验为数字
3. 实名情况：可二次实名 / 不可二次实名
4. 防沉迷：有防沉迷 / 无防沉迷

调用：

```bash
<skill-dir>/scripts/valuation.sh hok <server> <yingdi_id> <real_name_status> <anti_addiction>
```

示例：

```bash
<skill-dir>/scripts/valuation.sh hok android_qq 548928090 re_auth_allowed yes
```

### 三角洲行动

询问：
1. 登录方式：QQ / 微信
2. 实名情况：可二次实名 / 不可二次实名
3. 安全箱：顶级 / 高级 / 进阶 / 基础

调用：

```bash
<skill-dir>/scripts/valuation.sh delta <account_type> <real_name_status> <safety_box>
```

示例：

```bash
<skill-dir>/scripts/valuation.sh delta 1 re_auth_allowed top
```

脚本会自动获取二维码、打开二维码、每 4 秒轮询扫码状态，扫码成功后调用 `/api/query` 查询估值。告诉用户：

> 二维码已打开，请用手机扫码并确认登录，扫码成功后会自动完成估值。

### 和平精英

询问：
1. 区服：安卓 QQ / 苹果 QQ / 安卓微信 / 苹果微信
2. 实名情况：可二次实名 / 不可二次实名
3. 防沉迷：有防沉迷 / 无防沉迷
4. role_id：可选；用户不知道就留空

调用：

```bash
<skill-dir>/scripts/valuation.sh pubg <server> <real_name_status> <anti_addiction> [role_id]
```

示例：

```bash
<skill-dir>/scripts/valuation.sh pubg android_qq re_auth_allowed no
```

脚本会根据区服自动选择 QQ 或微信二维码，并在扫码成功后查询估值。

## 低级命令

仅在调试时使用：

```bash
<skill-dir>/scripts/valuation.sh qrcode delta 1
<skill-dir>/scripts/valuation.sh poll '<login_uuid>'
<skill-dir>/scripts/valuation.sh query '{"game":"hok","server":"android_qq","yingdi_id":"548928090","real_name_status":"re_auth_allowed","anti_addiction":"yes"}'
```

## 结果展示

脚本会优先读取响应中的 `estimate.extra.estimate_info`，输出格式化报告：

```text
🎮 王者荣耀 — 账号估值报告
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 预估价格: ¥2298.2
📈 价格区间: ¥2068 ~ ¥2528
🏆 超越用户: 93%
👑 最值钱单品: 马可波罗_怪盗基德

📊 核心数据:
  皮肤数量: 801
  英雄数量: 390

🔍 详细估值: https://mall.yy.com/?pageId=20000
```

如果估值响应结构不包含 `estimate_info`，展示去除 `request_logs` 后的原始 JSON，便于排查。

注意：结果中不要主动展示游戏昵称；如果原始 JSON 中包含 nickname/nick，只在排查错误时才提及。

## 错误处理

| 场景 | 处理 |
|------|------|
| 参数不合法 | 根据接口返回的 `message` 提醒用户重新选择或输入 |
| 二维码过期 | 提示用户重新发起估值，重新获取二维码 |
| 扫码未完成 | 等待轮询；脚本最多等待约 10 分钟 |
| 资产查询失败 | 展示接口返回的 `message`，提示用户确认区服、营地 ID、扫码账号是否正确 |
| 估值失败 | 展示接口返回的 `message`，不要编造价格 |

## 售卖引导

展示结果后，可以主动引导用户：

> 如果你想出售这个账号，可以前往 YY 游仓发布卖单：https://mall.yy.com/?pageId=20000

如果用户确认想卖，再打开链接：

```bash
open "https://mall.yy.com/?pageId=20000"
```
