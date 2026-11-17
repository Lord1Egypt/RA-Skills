---
name: baijimu-platform
description: 通过 `baijimu` CLI 使用百积木企业 AI 操作系统。用于认证、工作区与项目、Bundle 和 Module、Hosted Service、运行时服务、智能体、平台应用、本地 Connector，以及其他需要查询或操作百积木平台的任务。适用于能够读取 SKILL.md、访问百积木官方文档并执行本机命令的智能体平台。
version: 2.0.1
author: Baijimu
license: MIT-0
platforms: [openclaw, hermes]
metadata:
  openclaw:
    requires:
      bins: [baijimu]
    install:
      - kind: node
        package: "@baijimu/cli"
        bins: [baijimu]
    homepage: https://github.com/momoplan/baijimu-platform-skill
  hermes:
    tags: [baijimu, lowcode, automation, cli]
    requires_toolsets: [terminal]
---

# 百积木平台

通过本机 `baijimu` CLI 操作百积木。本技能是统一入口，不复制产品手册、领域架构、命令参数、Schema 或资源清单。

## 权威来源

- <https://docs.baijimu.com/> 是面向用户和开发者的产品、架构与工作流契约。
- 本机目标命令逐级 `--help` 是当前 CLI 版本的命令与参数事实来源。
- 工作区中的 `list`、`get`、`current`、`status`、运行时目录和审计结果是动态资源与执行状态的事实来源。

三者不一致时不要猜测或自行增加兼容逻辑；保留实际版本、命令和错误，报告文档、CLI 或运行时状态之间的不一致。

## 使用方式

1. 运行 `baijimu --version`。命令不在 `PATH` 时，检查官方固定安装位置：Windows 为 `$env:LOCALAPPDATA\Baijimu\bin\baijimu.exe`，macOS/Linux 为 `~/.local/bin/baijimu`。固定位置也不存在时，提示用户先安装官方 CLI，不要静默下载。
2. 运行 `baijimu auth status --verify`；未登录时运行 `baijimu auth login`，由用户完成授权。
3. 运行 `baijimu --help`，再只沿当前任务所需的命令路径逐级读取 `--help`。帮助中不存在的命令不得执行，也不要一次加载完整命令树。
4. 已知场景时直接读取对应的官方文档页面；路径未知时从 <https://docs.baijimu.com/llms.txt> 或 <https://docs.baijimu.com/docs-manifest.json> 定位 Markdown、版本化 Schema 和示例，不抓取 HTML 内嵌数据，也不以搜索结果或历史快照覆盖官方文档。
5. 写入前读取目标对象和当前状态，用 CLI 的资源解析或精确查询把名称转换为稳定 ID；零匹配或多匹配时停止，不取模糊结果的第一项。
6. 明确目标、权限、参数和副作用后执行；完成后用对应状态源回查。发布、安装、升级、部署和服务调用还要验证正式入口或真实 Runtime 行为。

## Bundle Capability

Hosted Service 需要查询自有 Bundle 的已安装资源，或查看、启动工作流与定时任务时，先读取
<https://docs.baijimu.com/development/bundle-development/hosted-service-capability.md> 和页面引用的版本化
OpenAPI，再运行 `baijimu bundle capability --help` 逐级发现当前管理命令。

只使用资源查询返回的 `resourceLocator`，不要自行构造；每个数据请求都显式传入权威查询得到的
`applicationRuntimeId`。Capability Token 只放入目标 Hosted Service Environment Secret，不输出到提示词、
聊天、源码、Artifact 或日志。Token、Client、scope 与 Bundle 所有权必须在操作前后分别回查。

## 执行边界

- 不编造 workspaceId、projectId、businessId、method、moduleId、versionId、sessionId 或其他协议标识。
- 不用内部 API、手工数据库或服务器修改、缓存态或临时兼容分支绕过官方文档和公开 CLI 定义的产品流程。
- 不直接编辑认证文件或输出 PAT、模型密钥、服务令牌、cookie 及完整认证响应。

查询、帮助、列表、状态和审计可直接执行。创建、更新、安装、升级、发布、部署或业务调用必须确保准确目标和参数；删除、卸载、回滚、重置、撤回、释放资源、覆盖远端内容、产生费用或向外部发送消息前，必须获得用户对准确目标的明确授权。

只有操作成功、权威状态源回查一致且所需端到端验证通过时，才报告完成。
