# 🔐 Credential Exposure Map

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**[English](README.md)** | **中文**

看清你的 agent 能碰到的每一个凭证。评估爆炸半径。收缩攻击面。

**6 个扫描区。1 份风险评分报告。0 个隐形凭证。**

**解决的痛点**：你的 agent 能访问环境变量、配置文件、记忆库、已装技能、MCP 服务器和整个 git 历史。每一个里面都可能藏着 API key、token 或密码——而你没办法一眼看全。Credential Exposure Map 一次扫描，全量清单，逐项风险评分。

## 目录

<details>
<summary>点击展开</summary>

- [工作原理](#工作原理)
- [六个扫描区](#六个扫描区)
- [安装](#安装)
- [快速开始](#快速开始)
- [Onboarding](#onboarding)
- [许可](#许可)

</details>

## 工作原理

```
环境变量  ──┐
配置文件  ──┤
memory/  ──┼──▶ Credential Exposure Map ──▶ 风险评分报告
skills/  ──┤                              + 收缩建议
MCP 配置 ──┤
git log  ──┘
```

## 六个扫描区

| 区 | 检查什么 | 风险因素 |
|---|---|---|
| 环境变量 | env 中的 API key、token、密码 | 明文、权限范围 |
| 配置文件 | openclaw.json、.env、credentials | 版本控制中的明文 |
| 记忆库 | MEMORY.md / memory/ 中提到的凭证 | 持久暴露 |
| 已装技能 | 引用或使用凭证的 skill | 第三方信任 |
| MCP 服务器 | 内嵌认证的服务器配置 | 跨服务访问 |
| Git 历史 | 过去提交过的秘密 | 永久记录 |

每项发现按凭证类型、范围、持久性、是否活跃使用评分（低/中/高/严重）。

## 安装

```bash
# ClawHub
clawhub install credential-exposure-map

# 或从源码
git clone https://github.com/Thomaszhou22/credential-exposure-map.git
cp -r credential-exposure-map ~/.openclaw/skills/
```

## 快速开始

对 Agent 说：**"跑一次凭证审计"** —— 6 区全扫 + 风险评分 + 收缩建议。

## Onboarding

首次使用会问 3 个快速问题（都有默认值）：扫描范围、风险阈值、是否保存上次扫描结果用于对比。之后直接用。说 "reset settings" 随时重新配置。

## 许可

MIT
