---
name: barog-booking
title: Barog医院（江南店）预约 Barog Booking
entry: api/skill.js
version: 1.0.0
tags:
  - Barog
  - barog皮肤科
  - 江南
  - 皮肤科
  - 首尔
  - 注射
  - 激光
description: "Barog医院（江南店） — 首尔江南区Barog皮肤科，人气注射/激光/皮肤管理"
---

# Barog医院（江南店） 预约助手

根据用户输入，为 Barog医院（江南店） 提供完整的预约服务。支持查看指南、打开页面、提交预约、咨询客服、查询价格。

## 依赖

无外部依赖（纯 Node.js 内置模块）

## 入口

`api/skill.js` 导出 `processQuery(query, lang, context)` 函数

## 意图流程

- **view** → 查看预约指南
- **open** → 打开医院详情页
- **book** → 收集信息 → 提交预约 API
- **consult** → 打开在线客服
- **price** → 查项目价格 / 打开价格表
- **download** → APP 下载链接

## 数据

- 医院数据：`data/hospital.json`
- 预约模板：`templates/booking.tpl`
- 多语言：`i18n/zh.json` / `i18n/en.json`
