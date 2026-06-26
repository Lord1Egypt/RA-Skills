# skill-publisher

[English](README.md) | [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: macOS | Linux | Windows (WSL)](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows%20(WSL)-lightgrey.svg)](https://github.com/bryant24hao/skill-publisher)

> 一条命令，把你的 agent 技能发布到 GitHub、ClawdHub 和 skills.sh。

一个 Claude Code 技能，自动化整个技能发布流程——从发布前检查到三个平台的安装验证。

## 为什么需要它

发布一个技能本应很简单，但现实是：

- **GitHub** 需要建仓库、加 topic 标签确保可被发现、配置正确的 badge 链接
- **ClawdHub** 的 CLI 有已知 bug（`acceptLicenseTerms`），slug 冲突需要手动处理
- **skills.sh** 不会自动索引——你必须到 `vercel-labs/skills` 仓库提 issue 请求收录
- README 里的安装命令必须和最终的仓库名在所有平台上保持一致
- 双语 README 需要内容同步和正确的语言切换链接

漏掉任何一步，你的技能要么搜不到，要么装不上。

**skill-publisher 在一个会话里搞定全部流程。**

## 它做什么

```
1. 发布前检查    → 验证 SKILL.md、README、LICENSE、密钥扫描
2. GitHub 发布   → 创建仓库、推送、添加发现标签
3. ClawdHub 发布 → 登录、检查 slug、发布（含 bug 绕过）
4. skills.sh 提交 → 自动创建索引请求 issue
5. 安装验证      → 端到端测试 3 种安装方式
6. 发布总结      → 汇总所有链接和安装命令
```

## 快速安装

```bash
npx skills add bryant24hao/skill-publisher -g -y
```

**手动安装**：

```bash
git clone https://github.com/bryant24hao/skill-publisher.git ~/.claude/skills/skill-publisher
```

## 使用方法

```
/skill-publisher
publish my skill
上架技能
发布 skill 到 clawhub 和 skills.sh
```

## 前置要求

- **[gh](https://cli.github.com/)** — GitHub CLI（用于创建仓库和提交 issue）
- **git** — 版本控制

可选：
- **clawhub CLI** — 用于 ClawdHub 发布（`npx clawhub` 无需全局安装）

## 已知问题

| 问题 | 处理方式 |
|------|----------|
| ClawdHub CLI v0.7.0 缺少 `acceptLicenseTerms` | 发布时自动修补 |
| skills.sh 不自动索引 | 自动提交 issue 到 vercel-labs/skills |
| ClawdHub slug 冲突 | 创建 GitHub 仓库前预先检查可用性 |

## 许可证

[MIT](LICENSE)
