---
name: easy-google-play
description: 自动完成 Android 应用的 Google Play 上架工作。Use when an agent needs to inspect an Android project, build or locate a release AAB, upload binaries and store assets, fill Play Console listing and policy forms, create a Production release, send changes for review, check review or publication status, or read a rejection and fix the app or listing. Requires Easy WebBridge and an already logged-in Google Play Console browser.
license: MIT-0
metadata:
  author: xxjrq
  version: "0.2.1"
  runtime: "easy-webbridge >=0.3.2"
  runtime-repository: "https://github.com/xxjrq/easy-webbridge"
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# easyGooglePlay

把一个 Android 项目从本地工程带到 Google Play。Agent 根据项目实际情况自动决定构建命令，并通过 Easy WebBridge 操作已经登录的 Google Play Console。本 Skill 遵循 Agent Skills 标准，可由 Claude Code、Codex、OpenCode、WorkBuddy 及其他兼容 Agent 使用。

## 先确认可以运行

在本 Skill 根目录执行：

```bash
node scripts/easy-webbridge-client.mjs preflight
```

自检会确认 Node.js、Easy WebBridge、访问令牌和在线浏览器，并返回可选浏览器的名称与 `browserId`。若运行时尚未安装，按自检结果先完成一次 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge) 安装；后续所有 Easy WebBridge 业务 Skill 共用这一套运行时。

## 能做什么

- 识别原生 Android、Flutter、React Native、Unity、Gradle 和 Fastlane 项目，找到正确的 applicationId、版本名和版本号。
- 检查签名与 Release 配置，按项目现有工具构建或找到可上传的 AAB。
- 上传 AAB、App 图标、Feature Graphic、手机和平板截图及审核视频资料。
- 填写应用名称、简短说明、完整说明、分类、联系方式、隐私政策和版本说明。
- 填写 Data Safety、广告、应用访问权限、内容分级、目标受众和新闻应用等政策表单。
- 按应用能力填写 VPN、前台服务、健康、金融或其他需要的声明与审核资料。
- 创建 Production Release，选择发布范围，并把改动真正发送审核。
- 检查审核和发布状态，读取驳回原因，修改安装包、商店资料或政策声明后重新提交。

## 开始

1. 读取应用项目和现有发布配置，沿用项目当前构建体系。
2. 确认目标 App、包名、版本、国家或地区、发布比例和用户期望的终点。
3. 根据自检结果选择已经登录 Google Play Console 的浏览器。
4. 为本次上架创建一个 `easy-google-play-<run-id>` 标签组；后续操作复用组内当前页面。
5. 汇总本次需要的文字、图片、视频、测试账号和政策资料；能从项目可靠读取的内容直接读取。

## 执行

1. 使用项目已有的 Gradle、构建脚本或 Fastlane 完成 Release AAB 构建。
2. 在 Play Console 选择正确应用，上传 AAB 和商店素材。
3. 填完商店详情、应用内容、Data Safety 和本应用实际需要的声明页面。
4. 创建 Production Release，填写版本说明并检查发布范围。
5. 用户要求“上架”或“提交审核”时，继续完成发布概览中的“发送更改以供审核”；用户只要求准备或检查时，停在对应结果页。
6. 提交后重新读取页面，记录实际显示的版本、versionCode 和状态。
7. 若被退回，读取完整政策或技术信息，定位问题，修改对应内容并重新走本次流程。

## Easy WebBridge 使用方式

- Easy WebBridge 地址固定为 `127.0.0.1:17777`。
- 一次任务固定控制一个 `browserId`。
- 顺序步骤复用同一标签页；确实需要对照时才在同一任务组增加标签页。
- 使用本 Skill 的 `scripts/easy-webbridge-client.mjs` 调用 `list`、`navigate`、`snapshot`、`click`、`fill`、`upload` 和 `command`；它直接连接运行中的 Easy WebBridge，不依赖另一个 Skill 的本地路径。
- 使用 `upload` 上传绝对路径文件；页面变化后重新读取页面再继续。
- 任务结束时只关闭本 Skill 创建的标签组，保留用户原来的页面。

## 完成标准

向用户清楚给出：

- App 名称、包名、版本名和 versionCode。
- AAB 的生成或上传结果。
- 商店资料、图片、Data Safety 和政策声明的完成情况。
- Google Play Console 当前真实状态，例如“尚未发送审核”“更改正在审核”“被拒绝”“已发布”。
- 若有审核问题，给出具体原因、已修改内容和下一步。

分别记录“表单已保存”“Release 已创建”“更改已发送审核”和“应用已发布”，以 Play Console 最终页面为准。
