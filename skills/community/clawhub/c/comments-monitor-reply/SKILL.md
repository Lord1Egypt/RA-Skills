---
name: comments-monitor-reply
description: 全平台评论区自动监控、智能回复与舆情分析工具。支持小红书、抖音、视频号、公众号、微博等主流平台，自动识别评论情感、生成个性化回复、实时监控负面舆情，大幅提升新媒体运营效率。所有凭证本地加密存储，保障数据安全。
license: MIT
tags: ["social-media", "comments-management", "autoreply", "public-opinion", "operations", "xiaohongshu", "douyin", "wechat"]
author: "OpenClaw Community"
version: "1.0.1"
keywords: ["新媒体运营", "评论回复", "舆情监控", "自动回复", "效率工具"]
requirements: ["nodejs>=18.0.0", "axios>=1.6.0", "cheerio>=1.0.0-rc.12", "crypto-js>=4.1.1"]
repository: "https://github.com/openclaw-skills/comments-monitor-reply"
homepage: "https://github.com/openclaw-skills/comments-monitor-reply#readme"
platform: "all"
security:
  data_encryption: "AES-256-GCM"
  credentials_storage: "Local encrypted storage, never uploaded to third-party servers"
  network_access: "Only access to configured social platform APIs and user-specified webhooks"
  permissions: "Minimal privilege principle, no unnecessary system access"
---

# 评论区自动回复与舆情监控 Skill

## Description
全平台评论区自动监控、智能回复与舆情分析工具。支持小红书、抖音、视频号、公众号、微博等主流平台，自动识别评论情感、生成个性化回复、实时监控负面舆情，大幅提升新媒体运营效率。

## Core Features
### 🤖 自动回复能力
✅ 多平台统一监控：小红书/抖音/视频号/公众号/微博/B站
✅ 智能情感识别：正面/负面/中性/提问/投诉 5分类
✅ 个性化回复生成：符合品牌调性，支持自定义话术模板
✅ 关键词触发回复：特定关键词自动回复预设内容
✅ 自动@提醒：需要人工处理的评论自动@运营人员
✅ 防重复回复：同一用户相同问题不重复回复

### 🚨 舆情监控能力
✅ 实时负面预警：负面评论/投诉/差评 实时推送提醒
✅ 舆情分级：按严重程度自动分级（一般/重要/紧急）
✅ 趋势分析：评论量/情感趋势变化统计
✅ 关键词监控：敏感词/竞品词自动识别告警
✅ 舆情报告：自动生成周/月评论舆情分析报告

### ⚙️ 高级配置
✅ 多账号管理：支持同时管理多个品牌/账号
✅ 白名单/黑名单：指定用户自动回复/屏蔽
✅ 人工审核模式：高风险评论先人工审核再发送
✅ 回复历史记录：所有自动回复内容可追溯可查询
✅ 数据导出：支持评论/回复数据导出Excel

## Usage
### 基础命令
```
# 启动评论监控
/comments start [platform]

# 停止监控
/comments stop [platform]

# 设置回复模板
/comments template set <keyword> <reply-content>

# 配置舆情预警
/comments alert set <level> <webhook>

# 生成舆情报告
/comments report [period] [output-format]
```

### 常用示例
```
# 启动全平台监控
/comments start all

# 只监控小红书和抖音
/comments start xiaohongshu,douyin

# 设置"价格"关键词自动回复
/comments template set "价格" "您好，我们产品的价格是XXX元，现在购买还有优惠活动哦~"

# 配置负面评论预警到飞书群
/comments alert set urgent https://open.feishu.cn/xxxxxx

# 生成最近7天的舆情报告
/comments report 7d markdown
```

## Supported Platforms
- 小红书（Xiaohongshu）
- 抖音（Douyin）
- 视频号（Wechat Channels）
- 公众号（Wechat MP）
- 微博（Weibo）
- B站（Bilibili）
- 快手（Kuaishou）

## Configuration
首次使用需要配置各平台的Cookie/API Token：
```
/comments config xiaohongshu cookie <your-xiaohongshu-cookie>
/comments config douyin token <your-douyin-api-token>
```

---

## 🔒 安全与凭证管理
### 凭证存储机制
所有敏感凭证（Cookie/API Token）均采用 **AES-256-GCM** 加密算法本地加密存储，加密密钥由系统随机生成且仅存储在用户本地设备中，**绝对不会上传到任何第三方服务器**。

### 权限说明
- 本技能仅会访问你明确配置的平台API接口，以及你指定的Webhook地址
- 不会读取、上传或存储任何与评论监控无关的用户数据
- 所有网络请求均为HTTPS加密传输，确保数据安全
- 严格遵循最小权限原则，不请求任何不必要的系统权限

### 环境变量配置（可选）
你也可以通过环境变量配置敏感信息，避免在交互命令中明文输入：
| 环境变量名 | 说明 | 是否必填 |
|-----------|------|----------|
| `CMR_XHS_COOKIE` | 小红书Cookie | 否 |
| `CMR_DOUYIN_TOKEN` | 抖音API Token | 否 |
| `CMR_WECHAT_TOKEN` | 视频号/公众号Token | 否 |
| `CMR_WEBHOOK_URL` | 告警Webhook地址 | 否 |
| `CMR_ENCRYPTION_KEY` | 自定义加密密钥（16/24/32位字符串） | 否 |

---

## 📦 安装与依赖
### 系统要求
- Node.js >= 18.0.0（必需）
- 支持Windows/macOS/Linux全平台

### 自动安装（推荐）
```bash
# 通过ClawHub一键安装，自动处理依赖
clawhub install comments-monitor-reply
```

### 手动安装
```bash
# 克隆仓库
git clone https://github.com/openclaw-skills/comments-monitor-reply.git
cd comments-monitor-reply

# 安装依赖
npm install

# 加载到OpenClaw
openclaw skills add .
```

---

## 🛡️ 数据隐私保护
1. **数据存储**：所有评论数据、回复记录仅存储在用户本地，默认保留30天，可配置自动清理
2. **数据使用**：仅用于评论分析和回复生成，不会用于其他任何用途
3. **数据传输**：仅在用户配置的平台和Webhook地址之间传输，无第三方中转
4. **审计日志**：所有操作均有日志记录，可追溯所有配置变更和回复记录

---

## ⚠️ 安全最佳实践
1. 建议为每个平台使用独立的、权限最小的API Token，避免使用主账号Cookie
2. 定期轮换平台凭证，降低泄露风险
3. 敏感环境变量建议通过系统密钥管理工具存储，避免明文写入配置文件
4. 不要在公共设备或共享服务器上使用本技能
5. 高风险场景建议开启人工审核模式，所有回复确认后再发送

## Requirements
- Node.js 18+
- 无额外系统依赖
- 支持ClawHub所有版本
