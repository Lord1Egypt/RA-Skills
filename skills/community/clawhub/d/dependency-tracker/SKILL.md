---
name: dependency-tracker
version: 1.0.0
description: 每周依赖检查。检查 Node.js、npm 版本和全局包是否有可用更新。触发时机：cron 定时任务或手动调用。
---

# Dependency Tracker

每周检查项目依赖是否有更新，确保安全和兼容性。

## 核心流程

1. 读取 references/spec.md 获取详细规范
2. 检查 Node.js 版本
3. 检查 npm 版本
4. 检查全局安装的包
5. 运行 npm outdated 检查可更新包
6. 生成报告并发送

## 触发时机

- cron 定时任务（建议每周）
- 用户明确要求时

## 投递规则（必须）

完成报告后，通过消息工具发送。
- 渠道：feishu
- 目标：<飞书群ID或用户ID>
如果报告超过 3800 字符，分成多条消息发送。
每条消息必须语义完整（不断开 URL 或格式）。
如果发送失败，重试一次。如果仍然失败，输出错误——永远不要静默退出。

## 输出

- 报告位置：`data/exec-logs/dependency-tracker/YYYY-MM-DD.md`
- 消息推送到飞书群
