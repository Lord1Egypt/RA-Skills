---
name: feishu-channel-cleaner
description: 自动检测并修复飞书频道配置冲突，智能保留完整配置的频道，解决飞书机器人无响应问题。
version: 1.1.0
author: "liuxuebin20260309"
license: MIT
tags:
  - feishu
  - configuration
  - channel-management
triggers:
  - 修复飞书
  - 飞书无响应
  - 频道配置冲突
  - feishu error
  - 通道合并
scripts:
  - path: cleaner.py
    interpreter: python3
    description: 核心清理脚本
tools_required:
  - python3
  - file-system
permissions:
  - config:read
  - config:write
  - gateway:restart
---

# 飞书频道配置清理技能

## 概述
本技能自动化处理 OpenClaw 配置文件中常见的飞书频道冲突问题，智能识别完整配置的通道并合并白名单和策略。

## 触发条件
当用户提到“修复飞书”、“飞书无响应”、“频道配置冲突”、“通道合并”或类似关键词时，应激活此技能。

## 工作流程
1. 备份配置文件
2. 检测 channels 下是否同时存在 `feishu` 和 `openclaw-feishu`
3. 判断哪个通道包含完整的 `appId` 和 `appSecret`
4. 保留完整通道，合并 allowlist 和 dmPolicy 到保留通道
5. 删除冗余通道，清理非法字段
6. 提示重启 Gateway

## 使用示例
**用户**：我的飞书没反应了，帮我修复一下飞书频道。

**AI**：（调用技能）正在扫描配置… 已智能修复，请重启 Gateway 生效。

## 注意事项
- 执行前自动备份配置文件。
- 需要 Python 3 环境。
- 如果只有一个飞书通道，技能会报告“无需清理”。
