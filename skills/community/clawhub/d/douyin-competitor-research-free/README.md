# 免费抖音竞品研究助手

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

按关键词或指定账号读取抖音公开作品样本，输出竞品矩阵、钩子结构、可见证据、差异机会和选题建议。它只看当前页面可见信号，不复制作品原文，不推断后台数据，也不声称掌握平台算法。

## 能做什么

- 研究一个公开账号页、一个或多个关键词搜索页的作品卡片。
- 对每个样本标注视频/图文、钩子结构、开场动作、受众承诺和证据来源。
- 提供基于样本结构的差异化测试方向与 3 条选题建议。
- `mock` 模式完全离线；`easy-webbridge` 模式复用用户已授权浏览器，只读并在结束时关闭本次会话。

## 开始使用

最小请求：

```json
{
  "runtime": "mock",
  "accountAlias": "fixture-tech-competitors",
  "accountUrl": "https://www.douyin.com/user/fixture",
  "keywords": ["AI工具"],
  "sampleLimit": 8
}
```

本地 mock：

```bash
node scripts/douyin-competitor-research-free.mjs collect \
  --request fixtures/request-valid.json \
  --input fixtures/visible-snapshot-success.json \
  --output ./output/competitors
node scripts/douyin-competitor-research-free.mjs analyze \
  --snapshot ./output/competitors/research-snapshot.json \
  --output ./output/competitors
```

真实浏览器：先安装并启动 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)，在目标浏览器完成抖音登录，再运行：

```bash
node scripts/douyin-competitor-research-free.mjs list
node scripts/douyin-competitor-research-free.mjs collect \
  --request ./request.json --output ./output/competitors
node scripts/douyin-competitor-research-free.mjs analyze \
  --snapshot ./output/competitors/research-snapshot.json \
  --output ./output/competitors
```

## 输出

- `research-snapshot.json`：带 runtime 标记的公开页面快照，不含原文。
- `competitor-research.json`：结构化竞品矩阵、钩子统计、证据、差异机会和选题建议。
- `competitor-research.md`：可读研究报告，适合人工审核。
- `run-diagnostic.json`：登录、验证码、空页面、浏览器选择或输入错误诊断。

## 边界

结果只代表指定页面在采集时刻的公开可见样本，不代表全网排名、播放效果、转化率或算法规律。脚本不会保存标题、简介、字幕、评论等原文，不读取 Cookie、Token 或后台接口，不执行互动和发布。页面要求登录或验证时，在浏览器中人工处理后重试。

MIT-0，见 [LICENSE](LICENSE)。
