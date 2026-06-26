---
name: "ad-account-manager"
description: "Manage ad accounts (广点通, 巨量引擎) via browser automation with cookie login. Invoke when user asks to manage ad accounts, login to ad platforms, or view account status."
---

# 广告账户管理 Skill

## 功能描述

通过浏览器自动化（Cookie登录），实现多平台广告账户的统一管理，无需逐个登录广告后台，提升账户切换和状态查看效率。

## 核心功能

1. **登录管理**：支持广点通（广告主/服务商）和巨量引擎的扫码登录，保存Cookie到本地
2. **一键登录**：使用已存储的Cookie自动登录对应广告后台
3. **账户状态总览**：拉取所有已登录账户的基础信息，异常账户标红提醒

## 使用场景

- 用户发送"管理广告账户"
- 用户请求登录广点通或巨量引擎
- 用户需要查看账户状态（余额、消耗、预算等）
