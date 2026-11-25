---
name: easy-app-store
description: 自动完成 iOS 应用的 App Store 上架工作。Use when an agent needs to inspect an iOS project, build or locate an IPA, upload a build and store assets, fill App Store Connect metadata and compliance information, submit a version for review, check review or publication status, or read a rejection and fix the app or listing. Requires Easy WebBridge and an already logged-in App Store Connect browser.
license: MIT-0
metadata:
  author: xxjrq
  version: "0.2.3"
  runtime: "easy-webbridge >=0.3.2"
  runtime-repository: "https://github.com/xxjrq/easy-webbridge"
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# easyAppStore

把一个 iOS 项目从本地工程带到 App Store。Agent 根据项目实际情况自动决定构建命令，并通过 Easy WebBridge 操作已经登录的 App Store Connect。本 Skill 遵循 Agent Skills 标准，可由 Claude Code、Codex、OpenCode、WorkBuddy 及其他兼容 Agent 使用。

## 先确认可以运行

在本 Skill 根目录执行：

```bash
node scripts/easy-webbridge-client.mjs preflight
```

自检会确认 Node.js、Easy WebBridge、访问令牌和在线浏览器，并返回可选浏览器的名称与 `browserId`。若运行时尚未安装，按自检结果先完成一次 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge) 安装；后续所有 Easy WebBridge 业务 Skill 共用这一套运行时。

## 能做什么

- 识别 Xcode、Flutter、React Native、Unity、Fastlane 等项目，找到正确的应用、Bundle ID、版本号和构建号。
- 检查签名与发布配置，按项目现有工具构建或找到可上传的 IPA。
- 上传构建包、App 图标、各尺寸截图、预览视频和审核附件。
- 填写应用名称、副标题、描述、关键词、分类、支持网址、隐私政策和版本说明。
- 填写年龄分级、隐私信息、出口合规、内容版权和审核联系信息。
- 按需要填写审核账号、演示步骤、二维码或测试附件。
- 选择正确构建版本，提交 App Review，并继续检查真实审核状态。
- 读取审核意见，判断应修改代码、截图、商店文案还是审核资料，然后完成修正和重新提交。

## 开始

1. 读取应用项目和现有发布配置，沿用项目当前构建体系。
2. 确认目标 App、版本、市场、发布范围和用户期望的终点。
3. 根据自检结果选择已经登录 App Store Connect 的浏览器。
4. 为本次上架创建一个 `easy-app-store-<run-id>` 标签组；后续操作复用组内当前页面。
5. 汇总本次需要的文字、图片、视频、账号和审核附件；能从项目可靠读取的内容直接读取。

`preflight` 只验证 Node.js 版本、Bridge 健康状态、Token 可用性和扩展在线状态。它不检查 App Store Connect 登录会话、团队、应用身份、签名配置、构建是否上传完成或审核状态。选定 browserId 后，先在页面确认登录账号/团队和目标 App，再按实际页面回读确认后续结果；页面不可见或状态未知时不得把操作报告为完成。

## 执行

1. 检查本地项目和构建工具，用项目已有的 Xcode、构建脚本或 Fastlane 执行 Release 构建；通过 WebBridge 操作 App Store Connect。Skill 不自带 Xcode 构建器或 App Store Connect API 客户端。
2. 在 App Store Connect 选择正确应用和版本，关联刚上传的构建。
3. 填完版本页面、商店资料、隐私与合规页面、审核信息。
4. 上传所需截图和附件，并等待页面显示处理完成。
5. 用户要求“上架”或“提交审核”时，继续完成提交；用户只要求准备或检查时，停在对应结果页。
6. 提交后重新读取页面，记录实际显示的版本、构建号和状态。
7. 若被退回，读取完整审核信息，定位问题，修改对应内容并重新走本次流程。

## Easy WebBridge 使用方式

- Easy WebBridge 地址固定为 `127.0.0.1:17777`。
- 一次任务固定控制一个 `browserId`。
- 顺序步骤复用同一标签页；确实需要对照时才在同一任务组增加标签页。
- 使用本 Skill 的 `scripts/easy-webbridge-client.mjs` 调用 `list`、`navigate`、`snapshot`、`click`、`fill`、`upload` 和 `command`；它直接连接运行中的 Easy WebBridge，不依赖另一个 Skill 的本地路径。
- 使用 `upload` 上传绝对路径文件；页面变化后重新读取页面再继续。
- 任务结束时只关闭本 Skill 创建的标签组，保留用户原来的页面。

## 完成标准

向用户清楚给出：

- App 名称、Bundle ID、版本号和构建号。
- IPA 的生成或上传结果。
- 商店资料、截图、隐私合规和审核资料的完成情况。
- App Store Connect 当前真实状态，例如“准备提交”“正在等待审核”“审核中”“被拒绝”“可供销售”。
- 若有审核问题，给出具体原因、已修改内容和下一步。

分别记录“上传成功”“提交成功”“审核通过”和“商店可见”，以 App Store Connect 最终页面为准。
