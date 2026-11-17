---
name: bilibili 视频监控
description: 运行 B站每周播报脚本，读取生成的报告文件，将内容整理成文字，并通过双通道推送给用户（默认 UID 请在脚本中配置）。触发场景：用户请求"查看B站播报"、"运行播报脚本"、"生成本周投稿报告"、或类似表达。也适用于自动化定时任务执行完毕后读取报告内容并推送。脚本路径：`bibili_weekly.js`；报告文件路径：`./bilibili_report.txt`；Cookie 文件路径：`./bilibili_cookie.txt`（需自行创建，切勿提交真实 Cookie）。推送通道1：调用 @skill://微信 PC 端自动控制 发送到配置的微信联系人；推送通道2：调用 @skill://agently-mail（Agent Mail）发送报告到配置的邮箱地址（两阶段确认：发信前展示摘要，用户确认后发出）。
version: 1.1.0
author: 微光浮影
homepage: https://skillhub.cn/skills/bilibili-video-monitoring
license: Apache-2.0
tags:
  - bilibili
  - video
  - monitoring
  - automation
  - nodejs
---

# bilibili 视频监控 v1.1.0

自动监控 B站 UP主投稿数据，生成周报并通过微信 + Agent Mail 双通道推送。

> ⚠️ **隐私提醒**：本仓库**不包含任何真实 Cookie 文件**。请在你自己的机器上创建 `bilibili_cookie.txt` 并填入你的 B站 Cookie；切勿将该文件提交到任何公开仓库。

## 功能

- 读取 B站 Cookie，通过内置 WBI 签名算法验证身份
- 获取 UP主最新投稿列表（默认 UID 请在 `bibili_weekly.js` 中配置 `YOUR_BILIBILI_UID`）
- 统计播放、点赞、收藏、分享、评论数据
- 获取最新3个视频的高赞评论（TOP5）
- 生成结构化文字报告，自动双通道推送

## 文件结构

```
bilibili-video-monitoring/
├── SKILL.md            # Skill 定义（本文件）
├── bibili_weekly.js    # 主执行脚本
├── bilibili_wechat_push.js  # 微信推送联动脚本
├── bilibili_cookie.txt # Cookie 配置（需自行创建，切勿提交真实值）
└── README.md           # 详细使用说明
```

## 依赖

- Node.js（建议使用系统 PATH 中的 `node`）
- 无额外 npm 依赖，WBI 签名纯 JS 实现
- 需提前配置「微信 PC 端自动控制」Skill
- 需提前配置「agently-mail」Skill（Agent Mail，收件地址请自行填写）

## 使用方法

### 1. 配置 Cookie

在本目录**自行创建** `bilibili_cookie.txt`，填入你的 B站 Cookie：

```
SESSDATA=你的SESSDATA值
bili_jct=你的bili_jct值
DedeUserID=你的DedeUserID
DedeUserID__ckMd5=你的DedeUserID__ckMd5值
```

**获取方式：**
1. 浏览器登录 https://www.bilibili.com
2. F12 → Application → Cookies → https://www.bilibili.com
3. 找到上述四个字段，复制值填入

> ⚠️ Cookie 为敏感信息，请勿分享给他人，也不要提交到公开仓库。

### 2. 配置 UP主 UID

编辑 `bibili_weekly.js` 顶部的：

```js
const UID = 'YOUR_BILIBILI_UID'; // 改为你要监控的 UP主 UID
```

### 3. 手动运行（测试）

```bash
node bibili_weekly.js
```

运行后自动：
1. 验证 Cookie 有效性
2. 拉取最新投稿数据
3. 生成报告写入 `./bilibili_report.txt`
4. （若由 Skill 调用）自动双通道推送

### 4. 触发词

以下表达均可触发本 Skill：
- 查看B站播报
- 运行播报脚本
- 生成本周投稿报告
- B站周报
- 检查我的B站投稿

## 双通道推送

| 通道 | 实现方式 | 推送目标 |
|------|----------|----------|
| 通道1 | 微信 PC 端自动控制 Skill | 微信联系人（在 `bilibili_wechat_push.js` 中配置 `YOUR_WECHAT_CONTACT`） |
| 通道2 | agently-mail Skill（agently-cli，两阶段确认） | 你的 Agent Mail 地址（请在配置中填写） |

## 报告示例

```
🦞 B站每周播报
UP主：YOUR_BILIBILI_NAME
数据周期：本周
─────────────────────
📹 投稿概览（共 2 个视频）

▎【视频标题】
  BV号：BV1xx411x7xx
  发布时间：2026-04-20
  播放：12.3万 | 点赞：8456 | 收藏：2345 | 分享：876 | 评论：1234

  💬 高赞评论 TOP5：
    1. 评论内容...
       👍 1234
...

─────────────────────
📊 本周合计
  总播放：XXX | 总点赞：XXX | 总评论：XXX

Powered by WorkBuddy 🦞
```

## 注意事项

1. Cookie 为敏感信息，勿泄露，勿提交到公开仓库
2. 脚本内置 WBI 签名，无需安装任何 npm 包
3. 报告文件默认输出到 `./bilibili_report.txt`
4. 推送失败请检查：微信是否登录、agently-cli 是否已完成 auth login（Agent Mail 授权）

## 更新日志

### v1.0.0（2026-04-27）
- 初始版本，提交 SkillHub
- Slug：bilibili-video-monitoring
- 支持 WBI 签名自动生成
- 双通道推送（微信 + 邮箱）

### v1.1.0（2026-07-17）
- 推送通道2 由「QQ邮箱」替换为「Agent Mail（agently-mail Skill）」
- 引入 Agent Mail 两阶段确认安全机制：发信前 WorkBuddy 展示摘要，用户确认后发出
- 微信通道保持不变
- 自动化定时任务默认走微信无感推送；Agent Mail 作为用户主动索取时的确认发送通道
