---
name: deepseek-harness-desktop-shell
description: "把已在本地运行的 DeepSeek Harness Web UI（默认 http://127.0.0.1:3080）用 Electron 包装成桌面应用的实战指南：前置依赖、最小可运行壳、启动 Harness 与加载本地 URL 的方式、打包分发。仅覆盖桌面套壳本身；Harness 的安装 / 构建 / 排错由 deepseek-harness-windows-deploy 技能负责。"
license: MIT
allowed-tools: Read, Bash, PowerShell, WebFetch
metadata:
  source: https://github.com/deepseek-ai/deepseek-harness
  version: 1.0.0
  compatibility: "Windows 10/11 实测（Electron 本身跨平台，macOS / Linux 同理）。需已装 Node + npm 且能联网；纯 webview 壳无需 Visual Studio 编译工具。"
---

# DeepSeek Harness — 桌面套壳（Electron）

## 适用范围与边界（先读）

本技能只覆盖一件事：把**已经在本地跑起来的** DeepSeek Harness Web UI，用 Electron 包装成一个桌面应用（exe / app）。

明确**不**覆盖：

- DeepSeek Harness 本身的安装 / 构建 / 启动 / 排错——这些由 `deepseek-harness-windows-deploy` 技能负责；本技能只消费它跑起来的 Web UI。
- 与 Harness 无关的通用 Electron 教程或桌面应用开发。

高影响步骤（安装依赖、执行打包 / 分发命令、在用户目录下新建或修改工程文件）执行前**需先向用户说明并确认**。不得在本技能范围外自行搭建不相关的项目脚手架。

## 目的

DeepSeek Harness 自带一个 Web UI（默认 `http://127.0.0.1:3080`），但只在浏览器里跑。本技能给出用 Electron 把它包成独立桌面窗口的最小做法，让它像普通桌面软件一样打开即用，而不必每次先开浏览器再输地址。

## 前置依赖

- **Node.js + npm**：能联网安装 npm 包即可（不需要 Visual Studio 编译工具，纯 webview 壳）。
- **已运行的 Harness Web UI**：先按 `deepseek-harness-windows-deploy` 把 `dsh web` 跑起来，并确认 `http://127.0.0.1:3080` 可访问。
- 备选：也可以让壳在启动时顺便拉起 Harness 进程，但 Harness 的启动（含可能的 `NODE_OPTIONS` 处理）请交给部署技能，本技能只负责"加载本地 URL"。

## 核心思路

Electron 的主窗口直接 `loadURL('http://127.0.0.1:3080')`，不内嵌任何业务代码——Harness 的所有逻辑都在它自己的 Web 服务里。壳只是一个"指向本地地址的浏览器窗口"。这让桌面壳极薄、几乎不会随 Harness 升级而失效，也天然完整保留 Harness 的功能与插件体系（页面逻辑全在 Harness 侧）。

## 验证过的最小壳

完整的工程脚手架、主进程代码、插件/扩展保留策略、打包配置与分步任务提示词，见 `references/desktop-shell-prompt.md`。照着做即可得到一个能打开 `http://127.0.0.1:3080` 的最小桌面窗口。

## 安全注意

- 主窗口只加载本地 `http://127.0.0.1:3080`，不要放开到任意远程地址。
- 主进程关闭 `nodeIntegration`、开启 `contextIsolation`，避免网页内容拿到 Node 能力；preload 只暴露最小桥接 API（窗口控制、打开外部链接、读写壳自己的配置）。
- 插件可能打开新窗口 / 弹窗：对 Harness 同源导航在壳内处理，对外部链接用系统浏览器打开，确保插件交互不丢失。
- 打包分发前请用户确认产物去向（安装包路径、是否签名等）。
