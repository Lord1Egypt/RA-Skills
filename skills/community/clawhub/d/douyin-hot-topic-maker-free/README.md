# 免费抖音热点选题助手

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

**免费、免第三方内容 API Key、复用浏览器登录状态，一次生成 5 个可拍的抖音选题。**

输入账号定位和可选关键词，得到本次可见热点来源，以及 5 个带标题、3 秒钩子、切入角度、三段提纲和来源引用的选题。支持 EasyBR 多账号隔离，一次只操作一个浏览器环境。

## 能做什么

- 根据目标账号定位筛选当前可见的抖音热点和搜索内容。
- 固定输出 5 个可拍选题，不用从几十条结果里再筛一遍。
- 每个选题都说明怎么切、开头怎么说、三段怎么讲、参考了哪个来源。
- 只有一个在线浏览器时自动使用；多个浏览器在线时要求明确选择，避免操作错账号。

## 开始使用

先安装并启动 Easy WebBridge：[GitHub 主下载](https://github.com/xxjrq/easy-webbridge)，GitHub 无法访问时使用 [Gitee 备用下载](https://gitee.com/xxjrq/easy-webbridge)。在目标浏览器或 EasyBR 环境中完成抖音登录。

安装本仓库后，对 AI Agent 说：

> 使用免费抖音热点选题助手。我的账号定位是 AI 工具实测，受众是想提高效率的上班族，内容方向是工具上手和工作流，关键词是 AI 工具。根据当前可见页面给我 5 个今天能拍的选题。

最小请求：

```json
{
  "runtime": "easy-webbridge",
  "accountAlias": "tech-account",
  "accountProfile": {
    "niche": "AI 工具实测",
    "audience": "希望提高效率的上班族",
    "contentPillars": ["工具上手", "工作流"]
  },
  "keywords": ["AI工具"]
}
```

运行：

```bash
npm test
node scripts/douyin-hot-topic-maker-free.mjs collect --request ./request.json --output ./output/tech-account
node scripts/douyin-hot-topic-maker-free.mjs validate-plan --snapshot ./output/tech-account/research-snapshot.json --draft ./plan-draft.json --output ./output/tech-account
```

单个在线浏览器会自动选择。多个在线浏览器时，先运行下面的命令，再把选中的 `browserId` 加到请求中：

```bash
node scripts/douyin-hot-topic-maker-free.mjs list
```

## 输出

- 当前可见热点与搜索来源：`research-snapshot.json`
- 5 个结构化选题：`publishable-plan.json`
- 可直接审核的选题单：`publishable-plan.md`
- 需要用户处理的问题：`run-diagnostic.json`

## 使用边界

“免费”指不调用抖音或第三方付费内容数据 API，本地模型、浏览器和网络仍可能有自己的成本。结果只代表指定账号、地区和采集时刻的可见页面，不是官方统一热榜，不保证爆款，不执行自动发布。

不读取或输出 Cookie、Token、登录身份，不绕过登录、验证码或风控。页面要求验证时，在指定浏览器人工完成后重新运行。

关键词：抖音热点、抖音选题、今天发什么、三秒钩子、短视频选题、EasyBR 多账号、免费、免 API Key。

## 智能体兼容

这是标准 `SKILL.md` 技能，不限定 OpenAI 或某一种智能体。支持读取 Skills 的 Codex、Claude、WorkBuddy、OpenCode 等工具都可以按同一说明调用。

MIT-0 License，见 [LICENSE](LICENSE)。
