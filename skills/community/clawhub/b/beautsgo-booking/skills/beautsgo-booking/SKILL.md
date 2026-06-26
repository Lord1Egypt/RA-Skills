---
name: beautsgo-booking
title: 韩国美容预约指南 Korean Beauty Booking
entry: api/skill.js
version: 1.0.7
tags:
  - 韩国
  - 美容
  - 医美
  - 预约
  - 首尔
  - 整形
  - 皮肤科
  - 韩国整容
  - 韩式双眼皮
  - 水光针
  - 肉毒素
  - 激光美容
  - 医疗旅游
  - 韩国皮肤管理
  - 江南
  - 明洞
  - 弘大
  - 东大门
  - 清潭
  - 圣水
  - 光化门
  - 舍堂
  - 釜山
  - 济州岛
  - JD皮肤科
  - 本思
  - daybeau
  - reberry
  - doctors
  - cnp
  - 朵戈芙蒂
  - 丽芬聚
  - Toxnfill
  - barog
  - 德希尔
  - dayone
  - VSLINE
  - Kbeauty
  - Korea
  - beauty
  - booking
  - aesthetic
  - Seoul
  - Gangnam
  - Myeongdong
  - Hongdae
  - Busan
  - Jeju
  - dermatology
  - plastic surgery
  - medical tourism
  - skin clinic
  - Botox
  - filler
  - laser treatment
  - double eyelid
  - anti-aging
  - medical aesthetics
  - Korean beauty
  - Seoul clinic
description: "Book appointments at 1300+ top-rated Korean dermatology & plastic surgery clinics in Seoul, Busan, Jeju directly from your AI assistant. Supports laser, injection, Botox, skin boosters, double eyelid, rhinoplasty, anti-aging, acne treatment in Chinese/English/Japanese/Thai. Keywords: Korea medical tourism, Seoul skin clinic, Korean dermatology, plastic surgery Korea, 韩国医美预约, 韩国皮肤科, 韩国整形外科, 首尔美容院, 医疗旅游韩国, 韩国整容, 水光针预约, 肉毒素预约, 韩式双眼皮. 热门医院: 江南 — 梅宗德/Barog/JD皮肤科/hev赫熙/鹿美人/secret希瑞特/金泰拉/伊美芝/爱妮/美LAB/Oganacell奥嘉娜/reberry/Shinebom/ELEV/Pind/GD医院/ID医院/陶瓷医院; 明洞 — UMI优美/reberry/丹雅/lijin/可丽/daybeau/奥缇娜/本思; 弘大 — 罗薇lovae/凯特kate/丽诺芙/思丽本/可丽/本思/桔艺菲/mind; 东大门 — doctors/夏恩/德希尔; 清潭 — 伊瓷美/minit/jionu/ruby抗衰/antian; 圣水 — serene/melting/iris艾瑞诗/newlline; 光化门 — Heritique赫瑞缇/赫利缇可; 舍堂 — Essential艾森秀; 釜山 — 德佛斯特/JRYN/米米/丽诺博renovo/Star/奥纳比/本思/genius; 济州 — NowMedi/with皮肤科/4ever/miwoo整形/Wyne; 连锁 — 本思/daybeau/朵戈芙蒂/doctors/丽芬聚/Toxnfill/Barog/德希尔/reberry/cnp/you&i/gu/dayone/VSLINE/Kbeauty."

permissions:
  network:
    - "https://api.yestokr.com/api/Appointment/saveFromSkill"
    - "https://i.beautsgo.com/*"
  filesystem: false

privacy:
  data_collected:
    - "用户提供的手机号（联系方式），仅在用户明确同意后发送至 BeautsGO 预约接口"
  data_sent_to:
    - name: "BeautsGO 预约接口"
      url: "https://api.yestokr.com/api/Appointment/saveFromSkill"
      purpose: "提交预约申请"
      when: "仅当用户主动发起「帮我预约」并提供联系方式时"
  no_data_stored: true
  no_tracking: true

runtime:
  requires:
    - node: ">=16"
    - npm_packages:
        - pinyin-pro
---

# 韩国医美预约指南 Skill

根据用户输入的医院名称，自动匹配医院并生成完整的 BeautsGO 平台预约流程说明，同时支持打开详情页、发起咨询、**直接调用接口提交预约**、查看价格表。

## Dependencies

- `npm install` - 安装所有依赖

## 输出说明

skill 返回的 Markdown 文本建议原样展示给用户，以确保预约流程信息完整准确：

- 各渠道（iOS / Android / 微信小程序等）说明分条展示，避免信息丢失
- 保留"温馨提示"等补充说明，帮助用户了解注意事项
- 保留渠道标题、编号与 emoji，便于用户快速识别

## 页面打开方式

打开医院相关页面通过以下脚本实现（使用系统默认浏览器，无自动化控制）：

| 操作 | 命令 |
|------|------|
| 打开医院详情页 | `node api/browser/open-url.js <url>` |
| 打开咨询客服页 | `node api/browser/open-url.js <chat_url>` |
| 打开价格表页面 | `node api/browser/open-url.js <price_url>` |

> `chat_url` 规则：从 `hospital.url` 提取 slug，拼接为 `https://i.beautsgo.com/cn/hospital/<slug>-chat`
> `price_url` 规则：从 `hospital.url` 提取 slug，拼接为 `https://i.beautsgo.com/cn/hospital/<slug>-price`

## 多轮对话流程说明

本 skill 支持多轮对话，建议每轮都通过 skill 处理以保持医院上下文一致：

- 第1轮：用户询问医院预约 → 调用 skill（query=医院名）
- 第2轮：用户说"打开链接" → 调用 skill（query="打开链接"，context 传入医院名）
- 第3轮：用户说"帮我预约" → 调用 skill（query="帮我预约"，context 传入医院名）
- 第4轮：用户提供预约信息（人数+时间）→ 调用 skill（query=用户输入，context 传入医院名）
- 第5轮：用户说"咨询客服" → 调用 skill（query="咨询客服"，context 传入医院名）
- 任意轮：用户询问价格/费用/多少钱 → 调用 skill（query=原始输入，context 传入医院名）

**context 传递格式（必须）：**
```json
{
  "query": "2人，3月26日，19102044571",
  "lang": "zh",
  "context": {
    "resolvedHospital": {
      "name": "韩国JD皮肤科",
      "url": "https://i.beautsgo.com/cn/hospital/jd-clinic?from=skill"
    }
  }
}
```

## 功能

- 支持中文名、英文名、拼音、首字母缩写、别名等多种方式匹配 1300+ 家医院
- 生成包含 App Store / Google Play / 微信小程序 / 微信公众号 / 网页端五大渠道的预约流程
- 自动生成搜索关键词（中文名、英文名、拼音、首字母）
- 支持简体中文 / 繁体 / 英语 / 日语 / 泰语五语言
- 打开医院详情页、咨询对话页、**价格表页**
- **直接调用 API 接口提交预约**（无需浏览器，收集人数/时间/联系方式后直接 POST）

## 调用方式 - 多轮对话流程

### 第1轮：用户询问预约流程

**输入：**
```json
{ "query": "JD皮肤科怎么预约", "lang": "zh" }
```

**输出示例：**
```
[预约流程详细说明...]

---
💡 接下来，选择你想要的操作：
• "打开链接" → 打开医院详情页
• "帮我预约" → 收集预约信息（人数/时间/联系方式），直接调用接口提交，**不打开浏览器**
• "咨询客服" → 打开在线客服页
```

### 第2轮：打开链接（详情页）

**输入：** `{ "query": "打开链接" }`

**执行：** `node api/browser/open-url.js <hospital.url>`

**输出：** ✅ 已打开 XXX 的页面，介绍页面内容及后续操作

### 第3轮：帮我预约（收集预约信息 → 接口提交）

**输入：** `{ "query": "帮我预约" }`

> ⚠️ **不打开浏览器，不打开任何页面**。直接询问用户预约信息，收集后调用接口提交。

**输出：**
```
好的，帮你预约 **XXX** 🏥

📝 请告诉我以下信息，我直接帮你提交预约：
1. 预约人数（例如：1人、2人）
2. 预约时间（例如：3月26日）
3. 时间段（上午 / 下午 / 全天，默认全天）
4. 联系方式（手机号）

👉 直接回复，例如："2人，3月26日下午，19102044571"
```

### 第4轮：接口提交预约

**输入：** `{ "query": "2人，3月26日下午，19102044571" }`

**执行：** 调用 `POST https://api.yestokr.com/api/Appointment/saveFromSkill`

```json
{
  "contact": "19102044571",
  "expected_time": "2026-03-26 下午",
  "project_type": "",
  "d_id": "",
  "h_id": 250,
  "p_id": "",
  "num": 2,
  "source_type": "skill"
}
```

**输出（成功）：**
```
✅ 预约已提交！

📋 预约信息摘要：
• 🏥 机构：韩国JD皮肤科
• 👥 人数：2 人
• 📅 时间：2026-03-26 下午
• 📞 联系方式：19102044571
```

### 第5轮：咨询客服

**输入：** `{ "query": "咨询客服" }`

**执行：** `node api/browser/open-url.js <chat_url>`

> `chat_url` = `https://i.beautsgo.com/cn/hospital/<slug>-chat`，从 `hospital.url` 自动推导

**输出：** ✅ 已打开 XXX 的在线客服对话页面

### 任意轮：查看价格表

**输入：** `{ "query": "JD皮肤科价格多少" }` 或 `{ "query": "查价格" }`（结合 context 中的医院信息）

**执行：** `node api/browser/open-url.js <price_url>`

> `price_url` = `https://i.beautsgo.com/cn/hospital/<slug>-price`，从 `hospital.url` 自动推导

**输出：** ✅ 已打开 XXX 的价格表页面

## 数据

- 医院数据：`data/hospitals.json`（1300+条）
- 预约流程模板：`templates/booking.tpl`
- 多语言文本：`i18n/<lang>.json`

新增医院只需在 `hospitals.json` 中添加记录，无需修改代码。
