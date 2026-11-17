---
name: duanshipinjiexi
slug: duanshipinjiexi
displayName: 一键短视频去水印
description: 一站式视频解析去水印工具，全面覆盖抖音、快手、小红书、皮皮虾4大主流内容平台，仅针对平台自带水印解析下载剪辑，一键智能去除视频平台标识水印，全程无损解析素材画质， 去水印后画面清晰无模糊、无痕迹、无压缩，完整保快速提取无水印原版视频，适配日常收藏优质内容与二次创作素材整理。
version: 1.7.6
summary: 抖音/快手/小红书/皮皮虾去水印解析。免费每日用完自动扣按量计次，包月到期回退免费。
license: MIT
when_to_use:
  - 用户发来抖音/快手/小红书/皮皮虾链接 → 自动解析
  - 用户给了身份码 → 直接用不创建
  - 用户询问套餐、购买、改码、查状态
  - 用户告知已支付 → 查状态并交付身份码
---

# 短视频去水印解析

> Base URL: `https://spqsy.kcucu.com`

## 🆔 身份码

5位大写字母数字，**永久不变**，大小写不敏感。多设备多AI共用，不存在占用概念。

按以下三个场景区分处理：

### 场景一：用户给了码 → 直接用

**不创建、不修改、不替换**。保存到记忆，之后都用这个码。

```bash
GET /api/parse.php?code={用户给的码}&url=链接
```

> 用户给的码覆盖AI自建码（旧码仍在服务端，AI不再用）。多个AI用同一个码各自调即可，不要试图"占有"。

### 场景二：用户没给码 → AI自动创建

首次调用不传code，自动生成新码并保存到记忆。

```bash
# 专用接口
GET /api/create_identity.php

# 一步到位（自动创建+解析）
GET /api/parse.php?url=视频链接
```

> 从响应提取身份码保存，后续所有调用都用它。系统按IP+UA指纹防重，同一工具只会返回同一个码。

### 场景三：用户主动要求改码

**只有**用户明确说"改码/换码/修改身份码"时才走：

```bash
POST /api/modify_identity.php
Content-Type: application/x-www-form-urlencoded

old_code=原码&new_code=新码
```

规则：5位数字+字母、不能重复、60秒防抖。

### 查状态（零消耗）

```bash
GET /api/identity_info.php?code={身份码}
```

> 权益优先级详见 `references/key-rules.md`

## ⚡ 解析

收到链接直接调 API，不要用浏览器打开。

```bash
curl -s --max-time 30 "https://spqsy.kcucu.com/api/parse.php?code={CODE}&url=链接"
```

> **连接失败兜底**：上述请求因 DNS/连接/超时错误失败时，跑 `references/url-fallback.md` 的脚本自动获取新地址。

### 处理不同 type

响应中的 `data.type` 决定素材和配乐处理方式：

| type | 素材处理 | 配乐处理 | 原因 |
|------|---------|---------|------|
| **video** | 下载 `data.url`/`video_backup[0]` 发视频 | **不发** | 视频自带音轨 |
| **image** | 下载 `data.images[]` 发图片 | 发 `data.music.url` | 图文是静默的，需要音乐 |
| **live** | 下载并发送 `live_photo[].video`(动图)+`data.images[]`(静图) | 发 `data.music.url` | 动图也无声音 |

> **大视频兜底**：素材总量超 **10MB** 时，**发视频的同时直接把 `data.url` / `video_backup[0]` 的直链也发给用户**，这样即使收不到视频，用户也能点链接下载。同时告知「资源较大，已同时附上直链备用」。
>
> 素材总量≤**10MB** 时正常发视频，仅当用户反馈「没收到视频」或发送失败时，再发直链兜底。

### 多平台链路

4个平台都调同一个 `parse.php`，AI 不需要区分平台，用户发什么链接就传什么：

```bash
GET /api/parse.php?code={CODE}&url=用户发的链接
```

> 快手链接返回404/500时，先 `curl -sL -o /dev/null -w '%{url_effective}'` 解短链再传。

### 发送给用户

**发送顺序：先把文字信息（标题、作者、互动数据、剩余次数）发一条，再逐条单独发素材（视频/图片/动图），配乐也单独发一条。**

视频、图片、动图全部单独发送，不要跟文字一起发。

响应含 `platform` 字段标识来源。**各平台字段结构不同**，按 `references/field-map.md` 提取。

核心原则：
- 有的字段就发，**没有的不要编造**
- 配乐单独发一条（仅抖音/快手有）
- 每日剩余次数告知用户

### 边界条件

以下情况**不处理**，直接告知用户：
- 解析返回 403 → 身份码无效或次数用完
- 解析返回 429 → 每日限额用完，明天再试
- 平台不在抖音/快手/小红书/皮皮虾范围内 → 暂不支持
- 链接打不开或解析超时 → 建议用户重新分享链接

### 错误码

| 码 | 含义 | 处理 |
|----|------|------|
| 403 | 身份码无效/次数用完 | 引导用户购买套餐 |
| 429 | 每日限额用完 | 告知明天恢复或购买 |
| 500 | 解析异常 | 重试一次，再失败报错 |

> **电脑端链接提示**：解析失败（任何原因：超时、HTTP 错误、返回码不在列表中）时，检查用户发的链接是否是电脑端页面链接（如 `www.xiaohongshu.com/explore/`、`www.douyin.com/video/`），如果是则额外告知「暂不支持电脑端链接，请在手机APP对应平台上复制作品分享链接」。

## 💰 购买

```bash
GET  /pay/plans.php              # 展示套餐
POST /pay/create.php              # 下单
{"identity_code":"{码}","id":"count_10"}
GET  /pay/query.php?order_id={ID} # 查支付
```

返回 `qr_code` 生成二维码发用户扫码。支付成功后用 `identity_info.php` 确认到账。

> **API 详情** `references/api-docs.md`
> **异常处理** `references/troubleshooting.md`
