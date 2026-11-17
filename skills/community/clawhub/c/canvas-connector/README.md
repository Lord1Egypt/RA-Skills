# 画布连接器（Infinite Canvas Connector）

> 让本机 [LobsterAI](https://lobsterai.youdao.com/) 一键接入你的「无限画布」平台 —— 对 AI 说一句话，自动下载、启动、连接（本地模式不限次数）。

## 它做什么

1. 下载并启动本机连接器（监听 `http://127.0.0.1:17371`）；
2. 生成「打开即连」链接（`https://你的画布/app/#agentUrl=…&agentToken=…`）；
3. 用浏览器打开该链接后，画布右侧「AI 助手」面板由本机 LobsterAI 提供能力。

## 安装方式（三选一）

**方式一 · ClawHub（推荐）**

对 LobsterAI 说：

> 从 ClawHub 安装 canvas-connector 技能

或命令行：

```bash
openclaw skills install canvas-connector
```

**方式二 · Git 仓库**

对 LobsterAI 说：

> 安装技能 git:https://github.com/rainbow-boy-max/canvas-connector-skill

或命令行：

```bash
openclaw skills install git:https://github.com/rainbow-boy-max/canvas-connector-skill
```

**方式三 · 下载技能包**

从你的画布站点下载 `canvas-connector-skill.zip`，解压后对 LobsterAI 说「安装这个技能包」。

## 使用

对 LobsterAI 说：

> 用画布连接器技能帮我连上画布（https://你的画布域名）

之后按 AI 的指引打开生成的链接即可。

## 要求

- Node.js ≥ 20
- LobsterAI 桌面端（免费开源：https://lobsterai.youdao.com/）

## 安全

- 连接器文件下载带 SHA-256 校验，校验不符拒绝安装；
- 「打开即连」链接仅对官方画布域名携带连接令牌，避免令牌泄露给不信任来源。

## 更新

本仓库与画布站点、ClawHub 三渠道同步发布；发布流程见画布仓库 `deploy/release-connector-skill.mjs`。
