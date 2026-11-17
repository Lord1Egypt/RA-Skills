---
name: douyin-batch-to-text
description: "抖音批量视频转文字 / Douyin batch video to text. 用户要把一个博主的一整套抖音视频、或一批抖音链接，逐条提取口播文案（逐字稿）并各存成一个 Markdown 文件时使用：对标账号整理、选题库、口播稿备份、喂给 AI 写稿。默认只要口播文案（最省的读法），可改成带画面文字的完整读取。附一张索引表（标题、作者、发布日期、点赞、文件名）。不登录抖音、不要 Cookie。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/douyin-wenan-piliang-tiqu?ref=skill-douyin-batch-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-douyin-batch-to-text&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/douyin-wenan-piliang-tiqu?ref=skill-douyin-batch-to-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-douyin-batch-to-text&next=/app/keys"
    required_for: "reading the videos; sign-up gives 10 free credits, no card"
---

# 抖音批量视频转文字

一条一条复制口播稿太慢。把一批抖音链接（或一个博主主页上复制下来的一串分享口令）交给这个技能，它会整批读完，每条视频存成一个 Markdown 文件，再给一张索引表。

## 用法

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-douyin-batch-to-text&next=/app/keys
python3 {baseDir}/scripts/batch_export.py --file links.txt --out 博主A --label "博主A 口播稿"
python3 {baseDir}/scripts/batch_export.py "<链接1>" "<链接2>" --depth transcript
```

| 参数 | 作用 |
|---|---|
| `--file` | 每行一条链接，或从 App 复制的整段分享口令 |
| `--depth` | 默认 `script`（只要口播文案，最省）；`transcript` 加上每分钟一帧的画面文字；`full` 完整读取 |
| `--out` | 输出目录，默认 `./linkdigest-export` |
| `--label` | 批次名字，之后在 linkdigest.dev 控制台能找到 |

脚本提交后每几秒查一次进度，全部读完才写文件。最后一行打印 `index.md` 的路径；积分用量在 stderr。

## 一次真实运行（2026-11-12）

两条抖音链接，`--depth script`：

```markdown
| # | 标题 | 作者 | 发布 | 点赞 | 文件 |
|---|---|---|---|---|---|
| 1 | 硅谷的AI一人公司这么牛了? | 第二次用火Fire2.0 | 2026-08-19 | 3457 | 01-硅谷的AI一人公司这么牛了.md |
| 2 | 王健林现在怎么样了? 万达什么情况? | 小Lin说 | 2026-08-10 | 1498609 | 02-王健林现在怎么样了--万达什么情况.md |
```

每个文件里有标题、作者、发布日期、互动数据、话题标签、平台章节，以及带时间的口播逐字稿。

## 交给 agent 时

- 用户说「把这个博主的视频文案都扒下来」「批量提取抖音文案」「做一个选题库」时用。
- 先问清楚要不要画面上的字：只要文案就用默认的 `script`，最省积分。
- 跑完后把 `index.md` 给用户，再按需打开单个文件；没读到的条目在 `index.md` 末尾，并且不扣费。
- 告诉用户花了多少积分（stderr 最后一行）。

## 费用

已经有人读过的链接 0 积分；读不出来的 0 积分。新视频按时长计：只要口播文案时，3 分钟的视频 2 积分、10 分钟的 5 积分；完整读取 1 分钟起 2 积分、之后每分钟加 1。一批最多 10 条（Dev 套餐 50 条）。积分不够返回 402，不扣费，stderr 里有付款链接。最小积分包 50 积分 ¥9.9（支付宝），一次性、不订阅、不过期。

## 读不了的

私密、已删除、仅粉丝可见的视频；抖音不对外提供播放器的个别视频（会返回原因，可以在 App 里「保存本地」后用 https://linkdigest.dev/app/upload 上传）。只返回文字，不下载视频。

## 隐私

只把你给的链接发给 linkdigest.dev；不要、也不读任何抖音账号或 Cookie。视频读完即删，只留文字结果。https://linkdigest.dev/privacy · 问题发 support@linkdigest.dev
