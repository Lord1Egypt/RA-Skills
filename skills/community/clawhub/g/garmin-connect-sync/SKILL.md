---
name: garmin-sync
description: 佳明国际账号数据同步到国内账号（基于 garminconnect 开源库）
author: assistant
version: 2.0.0
homepage: https://github.com/cyberjunky/python-garminconnect
triggers:
  - "佳明"
  - "Garmin"
  - "同步"
  - "运动数据"
  - "手表"
metadata:
  clawdbot:
    emoji: "⌚"
    requires:
      bins: ["python3"]
      pip: ["garminconnect"]
    config:
      env:
        GARMIN_INTL_USERNAME:
          description: 佳明国际版账号
          required: true
        GARMIN_INTL_PASSWORD:
          description: 佳明国际版密码
          required: true
        GARMIN_CN_USERNAME:
          description: 佳明国内版账号
          required: true
        GARMIN_CN_PASSWORD:
          description: 佳明国内版密码
          required: true
        SYNC_INTERVAL_HOURS:
          description: 同步间隔（小时）
          default: "24"
---

# Garmin 国际→国内账号同步技能 v2.0

基于 [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) 开源库，
从 Garmin Connect International 读取活动数据，下载 FIT 文件后上传到 Garmin Connect China。

## 功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 🔄 同步 | `sync` | 执行一次完整同步（读取国际版→下载FIT→上传国内版） |
| 📊 状态 | `status` | 查看同步状态和统计 |
| 📋 列表 | `list` | 查看最近活动记录 |
| 🔧 认证测试 | `auth-test` | 测试国际版和国内版账号认证 |

## 使用方式

```javascript
// 完整同步（最近7天）
sync()

// 同步最近30天
sync({ days: 30 })

// 查看同步状态
status()

// 列出最近活动
list()

// 测试认证
auth-test()
```

## 同步原理

1. 🔐 登录国际版 Garmin Connect，获取活动列表
2. ⬇️ 下载每条活动的原始 FIT 文件
3. 📤 登录国内版 Garmin Connect，上传 FIT 文件
4. 💾 记录已同步的活动 ID，避免重复

## 环境变量配置

| 变量 | 必填 | 说明 |
|------|------|------|
| `GARMIN_INTL_USERNAME` | ✅ | 国际版 Garmin 账号（邮箱） |
| `GARMIN_INTL_PASSWORD` | ✅ | 国际版 Garmin 密码 |
| `GARMIN_CN_USERNAME` | ✅ | 国内版 Garmin 账号（邮箱/手机） |
| `GARMIN_CN_PASSWORD` | ✅ | 国内版 Garmin 密码 |
| `GARMIN_SYNC_DIR` | ❌ | 数据存储目录（默认 ~/.garmin-sync） |

## ⚠️ 注意事项

1. **API 限流**: Garmin API 有请求频率限制，同步间隔会自动处理
2. **重复检测**: 已同步的活动会自动跳过，不会重复上传
3. **FIT 缓存**: 下载的 FIT 文件保存在本地，可定期清理
4. **首次使用**: 建议先用 `auth-test` 验证账号配置是否正确

## 版本历史

### v2.0.0 (2026-04-29)
- 全面重写，基于 python-garminconnect 真实 API
- 支持完整的认证流程（含 OAuth token 持久化）
- 支持 FIT 文件下载 + 国内版上传
- 支持活动去重和状态记录

### v1.0.0 (2026-04-16)
- 初始版本（模拟实现，未对接真实 API）
