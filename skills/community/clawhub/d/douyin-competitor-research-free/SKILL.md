---
name: douyin-competitor-research-free
description: 按关键词或指定抖音账号读取公开作品样本，生成不复制原文的竞品矩阵、钩子结构、可见证据、差异机会和选题建议。使用 mock 快照或用户已授权的 Easy WebBridge 只读访问；当用户要求抖音竞品分析、对标账号研究、同赛道作品结构拆解、按关键词找竞品样本或 Douyin competitor research 时使用。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# 免费抖音竞品研究

只研究采集时刻公开可见的作品卡片和页面字段。输出结构信号、来源 URL 和可见指标标签，不保存或复述作品标题、简介、字幕等原文，不读取 Cookie、Token、网络响应或后台数据，不执行点赞、评论、关注、发布、下载或绕过验证。

## 输入

请求 JSON 至少包含：

```json
{
  "runtime": "mock",
  "accountAlias": "tech-competitors",
  "accountUrl": "https://www.douyin.com/user/example",
  "keywords": ["AI工具"],
  "sampleLimit": 8
}
```

- `runtime` 只能是 `mock` 或 `easy-webbridge`。`mock` 只消费本地 fixture，不联网；`easy-webbridge` 才使用本机已授权浏览器。
- `accountUrl` 和 `keywords` 至少提供一个；关键词最多 5 个，样本数为 1～20。
- 真实运行有多个在线浏览器时必须先 `list`，再在请求中明确 `browserId`；脚本不会跨账号广播。

## 工作流

1. 读取本技能的 `fixtures` 了解快照字段；真实任务确认用户已登录且页面公开可见。
2. 运行 `collect`。mock 模式必须传 `--input`；真实模式只读账号页和关键词搜索页，并在结束时关闭本次会话。
3. 运行 `analyze`，生成 `competitor-research.json`、`competitor-research.md` 和可筛选的 `competitor-research.html`。
4. 把 Markdown 交给用户审核。发现登录、验证码、私密、删除或空页面时停止，查看 `run-diagnostic.json` 后由用户处理。

```bash
node scripts/douyin-competitor-research-free.mjs collect \
  --request fixtures/request-valid.json \
  --input fixtures/visible-snapshot-success.json \
  --output ./output/competitors

node scripts/douyin-competitor-research-free.mjs analyze \
  --snapshot ./output/competitors/research-snapshot.json \
  --output ./output/competitors

node scripts/douyin-competitor-research-free.mjs self-test
```

真实 WebBridge：

```bash
node scripts/douyin-competitor-research-free.mjs list
node scripts/douyin-competitor-research-free.mjs collect \
  --request ./request.json --output ./output/competitors
```

## 输出合同

成功的 `research-snapshot.json`：

- `runtime` 明确为 `mock` 或 `easy-webbridge`。
- `samples[]` 每条包含 `sampleId`、`sourceType`、`sourceUrl`、`workUrl`、`contentType`、作者显示名（如可见）、可见指标标签和 `evidence`。
- `evidence.originalTextStored` 永远为 `false`；只记录可复核 URL、观察到的字段名和采集时间。
- `limitations` 明确“不是全网样本、不是后台数据、没有算法结论”。

成功的 `competitor-research.json`：

- `matrix[]`：每个样本的格式、钩子结构、开场动作、证据类型、受众承诺和差异切入点。
- `hookStructures[]`：结构出现次数和样本 ID，只代表本次样本频次，不代表播放效果。
- `evidence[]`：与样本一一对应的 URL、可见字段、指标原文标签。
- `differentiationOpportunities[]` 与 `topicSuggestions[]`：给出可测试方向，不承诺流量，不复制原文。
- `safeguards`：敏感字段扫描、原文未保存、后台数据未推断、算法规则未声称。

成功的 `competitor-research.html`：

- 可在浏览器直接打开并筛选/查找的本地报告，至少包含竞品矩阵、差异机会和选题建议。
- 与 JSON、Markdown 使用同一批样本和同一份事实，不新增未经采集的结论。

失败时删除旧成功文件，只留下脱敏的 `run-diagnostic.json`。不得把失败目录当作研究结果。

## 研究边界

- 作品标题、简介、字幕和评论只用于本地分类，不进入 JSON、Markdown 或日志；不要把原文改写成“参考文案”。
- 可见点赞/评论等标签只作为“页面显示的证据”，不能换算播放量、转化率、排名、账号规模或平台算法规则。
- `差异机会`是基于样本结构的编辑假设；发布前仍需人工核验事实、版权、敏感行业和账号定位。
- 遇到人物、政策、医疗、金融、灾害、伤亡、诉讼、收益承诺或安全结论时，标为 `needs_fact_review`，不替用户下结论。
