---
name: fnclub-signer
description: 飞牛论坛(club.fnnas.com)自动签到。触发场景：(1) 用户要求"飞牛签到"、"飞牛论坛签到"、"fnclub签到"；(2) 设置定时飞牛论坛签到任务；(3) 查询飞牛论坛签到状态。
---

# 飞牛论坛签到

自动完成飞牛私有云论坛(club.fnnas.com)每日签到，获取飞牛币奖励。

## 凭证要求

本技能需要以下环境变量才能正常运行：

| 变量名 | 说明 | 是否必需 | 敏感性 |
|--------|------|---------|--------|
| `FNCLUB_USERNAME` | club.fnnas.com 登录用户名 | ✅ 是 | 🔴 高 |
| `FNCLUB_PASSWORD` | club.fnnas.com 登录密码 | ✅ 是 | 🔴 高 |
| `BAIDU_OCR_API_KEY` | 百度 OCR API 访问密钥 | ✅ 是 | 🟡 中 |
| `BAIDU_OCR_SECRET_KEY` | 百度 OCR API 密钥 | ✅ 是 | 🟡 中 |

### 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FNCLUB_CONFIG` | 配置文件路径 | `scripts/config.json` |
| `FNCLUB_DATA_DIR` | 数据目录（Cookie/Token缓存） | `scripts/` |

### 方式一：ClawHub 环境变量（推荐）

> 注意：这样添加环境变量会保存在 openclaw.json 中，不会暴露在系统环境变量中。

```bash
openclaw config set env.vars.FNCLUB_USERNAME "你的用户名"
openclaw config set env.vars.FNCLUB_PASSWORD "你的密码"
openclaw config set env.vars.BAIDU_OCR_API_KEY  "你的百度OCR API Key"
openclaw config set env.vars.BAIDU_OCR_SECRET_KEY "你的百度OCR Secret Key"
```

### 方式二：配置文件

在 `scripts/config.json` 中配置：

```json
{
  "username": "你的用户名",
  "password": "你的密码",
  "baidu_ocr_api_key": "百度OCR API Key",
  "baidu_ocr_secret_key": "百度OCR Secret Key"
}
```

### 获取百度OCR API

1. 访问 [百度AI开放平台](https://ai.baidu.com/)
2. 创建应用，选择"文字识别"服务
3. 获取 API Key 和 Secret Key

## 安装
### 安装 Node.js 依赖
```bash
cd scripts
npm install
```

这将安装以下依赖：
- `axios` - HTTP 请求库
- `cheerio` - HTML 解析库
- `tough-cookie` - Cookie 管理库

## 使用

### 手动签到

```
node scripts/fnclub_signer.js
```

### 定时签到

使用 OpenClaw cron 设置每日自动签到：

```
openclaw cron add \
  --name "fnclub-signer" \
  --every "1d" \
  --session main \
  --system-event "fnclub-sign" \
  --description "飞牛论坛每日签到" \
  --tz "Asia/Shanghai"
```

## 文件说明
- `scripts/fnclub_signer.js` - 主签到脚本 (Node.js) ✅ 推荐
- `scripts/config.json.example` - 配置文件模板
- `scripts/config.json` - 配置文件（需手动创建，通过命令的形式设置变量不需要创建）
- `scripts/cookies.json` - Cookie缓存（首次登录后自动生成）
- `scripts/token_cache.json` - 百度OCR Token缓存（首次需要验证码时自动生成）
- `scripts/node_modules/` - Node.js 依赖
