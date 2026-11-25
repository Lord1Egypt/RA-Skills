# CreatiVault Creator Ecosystem Skill

> **当前版本**：1.9.7 · **运行环境**：Node.js 20.6+ · **发布渠道**：stable

`creator-scraper-cv` 是 CreatiVault 官方达人营销 Skill，可帮助 AI Agent 完成达人发现、内容洞察、数据采集、邮件建联和账号审核等工作。

## v1.9.7 更新

- 结构化达人搜索新增 `union_user_ids` 和 `profile_urls` 批量精确查询。
- 两个列表均支持最多 200 条记录，可单独使用或同时使用。
- 批量精确查询可继续叠加地区、粉丝量、联系方式等筛选条件。
- 搜索接口单页最多返回 100 条；需要更多结果时可继续分页获取。

完整更新记录请查看 [CHANGELOG](CHANGELOG.md)。

## 主要能力

| 能力 | 说明 |
|------|------|
| 达人搜索 | 支持自然语言搜索、结构化筛选，以及按达人 ID 或主页链接批量精确查询 |
| 视频搜索 | 按 Hashtag、标题、播放量、互动率和达人标识查找视频 |
| 品牌洞察 | 查找品牌相关视频和已收录的品牌合作达人 |
| 相似达人 | 根据达人用户名或主页链接发现同平台或跨平台相似达人 |
| 批量采集 | 按主页链接、用户名或关键词提交异步采集任务 |
| 数据导出 | 支持 xlsx、csv 和 html 格式 |
| 邮件建联 | 支持单笔或批量发送、任务查询、沟通历史和跟进待办 |
| 假粉检测 | 提供假粉率估算、互动质量评分和账号风险信号 |
| 视频脚本审核 | 从 Hook、选题、痛点、植入、镜头、情绪和文案等维度分析视频 |
| 工作流编排 | 组合达人发现、内容分析、采集、导出和建联流程 |

## 平台支持

| 能力 | TikTok | Instagram | YouTube | Twitter (X) |
|------|:------:|:---------:|:-------:|:-----------:|
| 达人搜索 | ✅ | ✅ | ✅ | — |
| 视频搜索与品牌视频洞察 | ✅ | ✅ | ✅ | — |
| 相似达人 | ✅ | ✅ | ✅ | — |
| 批量采集 | ✅ | ✅ | ✅ | ✅ |
| 假粉检测 | ✅ | ✅ | ✅ | — |
| 已发布视频审核 | ✅ | Reels | Shorts | — |

Twitter (X) 支持链接、用户名和关键词采集，不支持视频采集。

## 快速开始

### 1. 安装

从 CreatiVault Skills 仓库安装：

```bash
npx skills add creativault/skills --skill creator-scraper-cv
```

也可以将本目录安装到支持 `SKILL.md` 的 AI Agent 环境中。项目使用单一 `main` 分支，common 和 Navos 环境使用同一套源码。

### 2. 配置

common 环境需要设置 CreatiVault API Key 和操作者身份：

```powershell
# Windows PowerShell
$env:CV_API_KEY = "cv_live_your_key_here"
$env:CV_USER_IDENTITY = "your_email@example.com"
```

```bash
# Linux / macOS
export CV_API_KEY=cv_live_your_key_here
export CV_USER_IDENTITY=your_email@example.com
```

API Key 可从 CreatiVault 管理后台获取。使用自定义 API 地址时，可额外设置 `CV_API_BASE_URL`。

Navos 用户无需手动配置 CreatiVault API Key；安装后将使用当前 Navos 登录身份完成授权。

### 3. 在 AI Agent 中使用

安装后，可以直接用自然语言描述任务，例如：

```text
帮我找 20 位美国 TikTok 美妆达人，粉丝数不少于 10 万，并且有公开邮箱。
```

```text
分析 Fenty Beauty 在 Instagram 上的热门视频和主要合作达人。
```

```text
检测这个 YouTube 达人的假粉和互动质量：https://www.youtube.com/@creator
```

```text
拆解这条 Instagram Reel 的内容结构、开头 Hook 和转化设计。
```

Agent 会根据任务自动选择对应的搜索、采集、审核或建联能力。

## 脚本调用示例

如需直接调用脚本，所有脚本均位于 [`scripts`](scripts/)，并通过一个 JSON 参数接收输入。以下命令均从仓库根目录执行。

### 结构化搜索

```bash
node creator-scraper-cv/scripts/search_creators.mjs '{"platform":"tiktok","country_code":"US","industry":"beauty","followers_cnt_gte":100000,"has_email":true,"size":20}'
```

### 批量精确查询

```bash
node creator-scraper-cv/scripts/search_creators.mjs '{"platform":"tiktok","profile_urls":["https://www.tiktok.com/@creator_a"],"union_user_ids":["creator_b"]}'
```

`profile_urls` 和 `union_user_ids` 可分别传入最多 200 条记录。

### 自然语言搜索

```bash
node creator-scraper-cv/scripts/search_creators_nl.mjs '{"platform":"instagram","query":"Find US running creators with authentic training content","limit":20}'
```

### 视频搜索

```bash
node creator-scraper-cv/scripts/search_videos.mjs '{"platform":"tiktok","hashtag":["beauty","skincare"],"video_views_cnt_gte":100000,"page":1,"size":20}'
```

### 批量采集与导出

```bash
# 提交主页链接采集任务
node creator-scraper-cv/scripts/submit_collection_task.mjs '{"task_type":"LINK_BATCH","platform":"tiktok","values":["https://www.tiktok.com/@creator1","https://www.tiktok.com/@creator2"]}'

# 等待任务完成
node creator-scraper-cv/scripts/poll_task_status.mjs '{"task_id":"task_xxx"}'

# 导出结果
node creator-scraper-cv/scripts/export_task_data.mjs '{"task_id":"task_xxx","format":"xlsx"}'
```

## 视频审核说明

已发布视频链接支持：

- TikTok 完整视频链接；
- Instagram Reels；
- YouTube Shorts。

YouTube 普通长视频、TikTok 分享短链、抖音链接以及已删除或设为私密的视频不在链接审核范围内。

本地视频可先通过 `media_upload.mjs` 上传，再提交审核。支持 mp4、mov、avi、mkv 和 webm，单个文件不超过 500 MB。

## 项目结构

```text
creator-scraper-cv/
├── SKILL.md                 # Skill 入口
├── skill.json               # 版本与发布配置
├── CHANGELOG.md             # 更新记录
├── discovery/               # 达人、视频和相似达人发现
├── collection/              # 批量采集与导出
├── outreach/                # 邮件建联
├── audit/                   # 假粉检测与视频审核
├── workflow/                # 组合工作流
├── scripts/                 # Node.js 执行脚本
├── profiles/                # 运行环境配置
└── references/              # API 与参数参考
```

## 参考文档

- [API 接口参考](references/api-reference.md)
- [平台参数说明](references/platform-params.md)
- [行业类目](references/industry-categories.md)
- [国家代码](references/country-codes.md)
- [语言代码](references/language-codes.md)
- [错误码](references/error-codes.md)

## 版本更新

common 环境可通过以下命令检查或安装更新：

```bash
node creator-scraper-cv/scripts/skill_update.mjs --check
node creator-scraper-cv/scripts/skill_update.mjs --yes
```

Navos 环境中的版本更新由 Navos 统一管理。

## 安全说明

- 不要将真实的 `CV_API_KEY` 提交到代码仓库或写入公开日志。
- 建议通过环境变量或运行平台提供的密钥管理功能配置凭证。
- 假粉率和账号风险属于数据模型估算结果，不代表社交平台官方审计结论。

## 许可

本 Skill 由 CreatiVault 提供，仅供授权用户使用。API 访问需要有效授权，并受对应账户权限和服务条款约束。
