---
name: douyin-hot-topic-maker-free
description: Use an authorized Easy WebBridge browser to turn one Douyin account's currently visible hot-page and optional keyword-search signals into exactly five practical topic ideas, each with a title, 3-second hook, angle, three-part outline, and source citation. Use for 免费抖音热点选题、今天抖音发什么、抖音热点选题助手、抖音三秒钩子、抖音关键词选题、按账号定位追热点、EasyBR 多账号选题、免第三方内容 API Key 的抖音热点研究, Douyin hot topic ideas, or Douyin content planning. Reuses the user's browser login, auto-selects only when one browser is online, and requires explicit selection when several are online.
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# 免费抖音热点选题助手

免费使用，免第三方内容 API Key，复用用户已有浏览器登录状态。一次只操作一个 EasyBR 浏览器环境，账号与输出互不混用。

## 输入

- 账号定位：`niche`、`audience`、至少一个 `contentPillars`。
- 可选关键词：0-5 个。
- 浏览器环境：一个在线浏览器时可省略 `browserId`；多个在线浏览器时必须明确选择。
- 非敏感账号别名 `accountAlias`，仅用于区分本次输出。

## 执行

1. 确认已安装并启动 Easy WebBridge：[GitHub](https://github.com/xxjrq/easy-webbridge)，[Gitee 备用](https://gitee.com/xxjrq/easy-webbridge)。
2. 读取 [数据契约](references/data-schema.md) 和 [浏览器方法](references/browser-method.md)。不要启动另一套临时浏览器。
3. 运行 `list` 查看在线浏览器。只有一个在线环境时直接采集；多个时先让用户明确选择，再把完整 `browserId` 写进请求。
4. 运行 `collect`，在同一任务标签组依次采集抖音热点页和可选关键词搜索页。只使用页面当前可见内容。
5. 根据快照和 [编辑规则](references/editorial-rules.md) 写 `plan-draft.json`，固定生成 5 条。每条必须有标题、3 秒钩子、切入角度、账号适配、开场/核心展开/结尾行动三段提纲和本次快照的来源 ID。
6. 运行 `validate-plan`，生成 `publishable-plan.json` 和 `publishable-plan.md`。交给用户审核，不执行发布。

```bash
node scripts/douyin-hot-topic-maker-free.mjs list
node scripts/douyin-hot-topic-maker-free.mjs collect --request ./request.json --output ./output/account
node scripts/douyin-hot-topic-maker-free.mjs validate-plan --snapshot ./output/account/research-snapshot.json --draft ./plan-draft.json --output ./output/account
```

最小请求见 `fixtures/request-valid.json`，草稿结构见 `fixtures/plan-draft-valid.json`。

## 输出

- `research-snapshot.json`：本次可见热点与搜索来源。
- `publishable-plan.json`：结构化的 5 条选题。
- `publishable-plan.md`：人能直接审核的选题单。
- `run-diagnostic.json`：需要登录、验证码处理、明确浏览器或修正输入时的诊断。

## 边界

只描述“指定浏览器在采集时刻可见的页面信号”。不声称是全网热榜，不保证爆款，不自动发布，不互动，不绕过验证码，不保存 Cookie、Token 或登录身份。人物、政策、医疗、金融、灾害、伤亡、引语、诉讼及快速变化数字在发布前进行事实复核。
