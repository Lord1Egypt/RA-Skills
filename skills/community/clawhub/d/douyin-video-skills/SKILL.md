---
name: douyin-video-skills
description: "抖音视频搜索、筛选、链接获取、文案提取与修正工具。支持在抖音网页中登录后搜索自定义关键词，按筛选参数从搜索结果中选择合适视频；点开候选视频后先校验当前弹层标题与目标搜索结果标题是否一致，若不一致则自动关闭弹层并继续尝试后续候选，再提取视频语音文案并输出原始稿、修正版、修正说明。适用场景包括抖音二次创作前的素材采集、竞品研究、视频文案提取与清洗。"
---

# 抖音视频搜索、文案提取与修正

从抖音网页中搜索自定义关键词，筛选并选定目标视频，校验当前视频是否正确，再提取视频语音文案，并对抽取结果进行修正和落盘。

## 功能概述

- **搜索视频**: 从抖音首页输入关键词并进入视频搜索结果，避免直接跳搜索 URL
- **筛选结果**: 按标题关键词、账号类型、点赞、时长、内容类型等参数筛选候选视频
- **锁定目标视频**: 点开候选视频后，校验标题是否匹配（支持归一化匹配、包含匹配、相似度匹配）
- **获取稳定链接**: 优先使用页面 `modal_id` 组装稳定视频链接，必要时再尝试分享按钮
- **提取文案**: 下载视频、提取音频、调用 ASR 获取语音文案
- **修正文案**: 结合标题、标签、上下文和领域常识修正 ASR 错误
- **自动保存**: 输出原始稿、修正版、修正说明、meta 信息等文件

## 环境要求

### 依赖安装

```bash
pip install requests ffmpeg-python
```

### 系统要求

- FFmpeg 必须安装在系统中（用于音视频处理）
- macOS: `brew install ffmpeg`
- Ubuntu: `apt install ffmpeg`

### 浏览器自动化要求

需要可用的 `playwright-cli` 以及它的 skills。

#### 安装 playwright-cli

```bash
npm install -g @playwright/cli@latest
```

#### 安装 playwright-cli 的 skills

```bash
playwright-cli install --skills
```

#### 校验安装

```bash
playwright-cli --version
```

推荐使用有头模式、持久化登录态，并显式指定 profile 目录：

```bash
playwright-cli -s=douyinflow open https://www.douyin.com/ --headed --persistent --profile ~/.playwright/douyinflow
```

### API 密钥配置（仅文案提取需要）

文案提取功能使用硅基流动 API，需要设置环境变量：

```bash
export API_KEY="your-siliconflow-api-key"
```

对 OpenClaw / Gateway 环境，建议写入：

```bash
~/.openclaw/.env
```

获取 API 密钥: https://cloud.siliconflow.cn/

## 使用方法

### 方法一：使用总控脚本（推荐）

```bash
python3 skills/douyin-video-skills/scripts/run_pipeline.py \
  --keyword "青少年无人机" \
  --pick-index 1 \
  --must-include 青少年 \
  --must-include 无人机 \
  --content-type-hint 培训 \
  --content-type-hint 科普 \
  --account-hint 教育 \
  --profile ~/.playwright/douyinflow \
  --human-delay-min-ms 800 \
  --human-delay-max-ms 2500 \
  --captcha-max-waits 3 \
  --title-match-mode default \
  --title-min-similarity 0.82 \
  --max-title-retry 5 \
  --headed \
  --persistent
```

### 总控脚本支持的主要参数

```bash
--keyword              自定义搜索词（必填）
--pick-index           选择第几个符合条件的结果（默认 1）
--must-include         标题必须包含的词，可多次传入
--exclude-word         需要排除的词，可多次传入
--content-type-hint    内容类型提示，如 培训 / 科普 / 推荐，可多次传入
--account-hint         账号类型提示，如 教育 / 俱乐部 / 教练，可多次传入
--min-likes            最低点赞量
--duration-min-sec     最短时长（秒）
--duration-max-sec     最长时长（秒）
--profile              playwright-cli 持久化浏览器 profile 目录（默认 ~/.playwright/douyinflow）
--human-delay-min-ms   人类化操作最短等待时间（毫秒）
--human-delay-max-ms   人类化操作最长等待时间（毫秒）
--captcha-max-waits    验证码暂停等待次数（默认 3）
--title-match-mode     标题匹配模式：strict / default / loose
--title-min-similarity 标题最小相似度阈值（默认 0.82）
--max-title-retry      标题校验失败后最多尝试多少个候选（默认 5）
--headed               浏览器前台运行
--persistent           使用持久化登录态
--output-dir           输出目录（默认 output）
```

### 方法二：分步执行

#### 1. 打开抖音并复用登录态（首次运行后会在 `~/.playwright/douyinflow` 生成登录态文件，后续可复用）

```bash
playwright-cli -s=douyinflow open https://www.douyin.com/ --headed --persistent --profile ~/.playwright/douyinflow
```

#### 2. 从首页输入搜索词并进入视频结果页

推荐让总控脚本自动完成，不要直接手写跳转搜索 URL。这样更接近真人操作，更利于减少验证码。

#### 3. 选定视频后做标题一致性校验

```bash
python3 skills/douyin-video-skills/scripts/title_match_check.py \
  --expected "目标搜索结果标题" \
  --actual "当前弹层标题" \
  --mode default \
  --min-similarity 0.82
```

> 默认不是死板的逐字完全相等，而是按“归一化标题 + 包含关系 + 相似度阈值”综合判断。  
> 若仍不匹配，不继续当前视频提取；应自动关闭弹层并尝试下一个候选。

#### 4. 提取视频文案

```bash
python3 skills/douyin-video-skills/scripts/douyin_downloader.py \
  --link "https://www.iesdouyin.com/share/video/<videoId>" \
  --action extract \
  --output ./output
```

#### 5. 修正文案并生成附加文件

```bash
python3 skills/douyin-video-skills/scripts/transcript_cleanup.py \
  --title "视频标题" \
  --raw ./output/<videoId>/transcript.md \
  --outdir ./output/<videoId>
```

### 筛选参数示例

```json
{
  "keyword": "青少年无人机",
  "pickIndex": 1,
  "mustInclude": ["青少年", "无人机"],
  "excludeWords": ["直播", "纯广告", "录播回放"],
  "minLikes": 0,
  "durationMinSec": 15,
  "durationMaxSec": 120,
  "contentTypeHints": ["培训", "科普", "推荐"],
  "accountHints": ["教育", "俱乐部", "教练"]
}
```

更详细的筛选思路参考：

- `references/filter-rules.md`

发布文案参考：

- `references/publish-copy.md`

## 输出目录结构

完整执行后，每个视频建议保存到独立文件夹：

```text
output/
└── <videoId>/
    ├── meta.json
    ├── source-link.txt
    ├── transcript.md
    ├── transcript-raw.md
    ├── transcript-clean.md
    └── transcript-fixes.md
```

### 文件说明

- `meta.json`: 标题、关键词、视频ID、筛选参数、提取时间
- `source-link.txt`: 最终用于提取的链接
- `transcript.md`: 提取器原始产物
- `transcript-raw.md`: 原始转写稿
- `transcript-clean.md`: 修正版文案
- `transcript-fixes.md`: 修正说明与待确认项

## 工作流程

### 搜索与筛选

1. 打开抖音首页并复用登录态
2. 以较慢节奏输入搜索词并点击搜索
3. 切换到视频结果页
4. 从搜索结果中读取候选视频列表
5. 按筛选参数过滤候选项
6. 选中第 N 个符合条件的视频

### 标题一致性校验

1. 记录目标搜索结果标题
2. 点开视频进入弹层
3. 读取当前页面 `modal_id`
4. 读取当前弹层标题
5. 执行标题校验脚本（默认使用归一化匹配 + 相似度阈值）
6. 若标题不一致，自动关闭弹层，回到结果列表继续尝试后续候选，直到找到校验通过的视频

### 提取与修正

1. 用 `modal_id` 组装稳定视频链接：`https://www.iesdouyin.com/share/video/<videoId>`
2. 下载视频到临时目录
3. 使用 FFmpeg 从视频中提取音频（MP3 格式）
4. 调用硅基流动 SenseVoice API 进行语音识别
5. 保存 `transcript.md`
6. 基于标题、标签、上下文和领域常识修正 ASR 文案
7. 输出 `transcript-raw.md`、`transcript-clean.md`、`transcript-fixes.md`

## 常见问题

### 搜索时频繁触发验证码怎么办

建议优先使用以下方式减少验证码：

- 使用固定 profile 目录复用登录态
- 从首页输入搜索，不要直接跳搜索 URL
- 增加人类化延迟，不要秒点秒跳
- 遇到验证码时先手工完成，再继续流程

当前脚本已支持：

- 人类化延迟参数：`--human-delay-min-ms` / `--human-delay-max-ms`
- 验证码暂停恢复：检测到验证码后暂停，等待人工处理完成再继续

### 搜索结果点开后，当前视频变了

这是抖音网页常见问题。必须增加校验：

- 标题先做归一化
- 再判断包含关系
- 最后再看相似度是否达到阈值

若仍不一致，不要在错误视频上继续提取。应执行：关闭弹层 → 回到结果列表 → 尝试下一个候选标题 → 重新校验，直到找到正确视频。

### 分享按钮不稳定

PC 端分享按钮可能：
- 只在悬停时出现
- 位于播放器浮层中，不易点击
- DOM 结构经常变化

因此本 skill 默认：
- 优先读取 `modal_id`
- 用 `modal_id` 组装稳定视频链接
- 不把“复制链接”当成唯一依赖

### 提取文案失败

- 检查 `API_KEY` 是否已设置
- 确保 API 密钥有效且有足够额度
- 确保 FFmpeg 已正确安装
- 确保输入链接为有效抖音分享链接或可解析的视频链接

### 文案有错别字或语义不通

ASR 常见问题包括：
- 同音错字
- 连词错误
- 重复词
- 断句错误
- 领域术语误识别

因此提取后必须执行修正步骤。

## 注意事项

- 本工具仅供学习和研究使用
- 使用时需遵守相关法律法规
- 请勿用于任何侵犯版权或违法的目的
- 不要把分享按钮点击成功作为唯一成功条件
- 不要直接信任 ASR 文案用于分析
- 不要在未完成标题一致性校验前就进入提取
- 不要把 Playwright 的 element ref 写死成固定编号
