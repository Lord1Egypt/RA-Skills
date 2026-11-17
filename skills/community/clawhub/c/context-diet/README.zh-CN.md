# 🥗 Context Diet

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**[English](README.md)** | **中文**

你的智能体变慢变笨了？Context Diet 扫描所有加载进上下文的内容——系统提示、技能描述、记忆文件——测量 token 重量，标记冗余，输出可执行的瘦身清单。

**4 个重量区。1 份瘦身清单。0 猜测。**

**解决的痛点**：你装的每个 skill 的描述都会注入每一轮对话。你写的每条记忆永久占据上下文。AGENTS.md 里的过时规则每次都被读取。它们默默堆积——直到你的 agent 背着 5 万 token 的死重给出模糊回答。Context Diet 让看不见的变看得见。

## 目录

<details>
<summary>点击展开</summary>

- [工作原理](#工作原理)
- [四个重量区](#四个重量区)
- [安装](#安装)
- [快速开始](#快速开始)
- [文件结构](#文件结构)
- [许可](#许可)

</details>

## 工作原理

```
AGENTS.md ──┐
SOUL.md  ──┤
skills/* ──┼──▶ Context Diet ──▶ 重量报告
MEMORY.md ─┤                      + 瘦身清单
memory/* ──┘                      + 节省百分比
```

不调 API、不用外部工具——Agent 读取自己的工作区文件，估算 token 重量（英文 ÷ 4、中文 ÷ 2），交叉验证什么在真正被使用。

## 四个重量区

| 区 | 称量什么 | 常见发现 |
|---|---|---|
| **1. 指令文件** | AGENTS.md、SOUL.md、USER.md | 重复规则、过时策略 |
| **2. 技能** | 每个已装 skill 的描述（**每轮对话的永久税**） | 从未使用的 skill、预加载的重引用文件 |
| **3. 记忆库** | MEMORY.md + memory/ 目录 | 过期数字、已完成项目仍标活跃 |
| **4. 当前会话** | 对话长度 | 超过阈值 → 建议压缩 |

## 安装

```bash
# ClawHub
clawhub install context-diet

# 或从源码
git clone https://github.com/Thomaszhou22/context-diet.git
cp -r context-diet ~/.openclaw/skills/
```

## 快速开始

对 Agent 说：**"跑一次上下文瘦身"** —— 一分钟内拿到完整重量报告和按节省量排序的瘦身清单。

## 文件结构

```
context-diet/
├── SKILL.md        # 扫描流程（4 区 + 瘦身清单 + 复验闭环）
├── README.md       # 英文说明
└── LICENSE         # MIT
```

## 许可

MIT
