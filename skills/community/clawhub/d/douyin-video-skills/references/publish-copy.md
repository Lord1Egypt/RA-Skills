# douyin-video-skills 发布文案

## 标题
抖音视频搜索、文案提取与修正 Skill

## 一句话介绍
从抖音搜索结果中筛选目标视频，校验当前视频是否正确，再提取并修正视频文案。

## 短描述
适用于抖音二次创作、竞品研究、素材采集。支持：
- 自定义搜索词
- 登录后网页搜索与筛选
- 当前弹层标题与目标搜索结果标题的复合匹配校验（归一化 + 包含 + 相似度）
- 从首页输入搜索词 + 人类化延迟 + 验证码暂停恢复
- 视频文案提取
- 文案修正与多文件落盘

## 完整描述
这是一个面向抖音素材采集与文本提取的完整工作流 skill。

它覆盖的不只是“给我一个链接，然后提文案”，而是更前面的真实流程：
1. 打开抖音并复用登录态
2. 使用固定 profile 目录复用登录态
3. 搜索自定义关键词
3. 按筛选参数选择候选视频
4. 从首页输入搜索词并进入视频结果页，必要时等待人工过验证码
5. 点进视频后做标题复合匹配校验（归一化 + 包含 + 相似度）
6. 如果不一致，关闭弹层并继续尝试后续候选
7. 用稳定视频链接提取文案
6. 对 ASR 结果进行语义修正
7. 输出原始稿、修正版、修正说明、meta 信息

## 功能卖点
- 不把“复制链接”当唯一依赖
- 优先使用 `modal_id` 组装稳定视频链接
- 内置标题复合匹配校验与自动重试，避免点错视频还继续提取
- 支持自定义搜索词、筛选参数、固定 profile 目录复用登录态，以及验证码暂停恢复
- 提取后自动输出 `transcript-raw` / `transcript-clean` / `transcript-fixes`
- 适合 analyst / planner 的前置素材采集与文案清洗流程

## 推荐标签
- douyin
- video
- transcript
- playwright
- asr
- content-research
- creator-tools

## 发布说明
### v1.0.0
- 支持抖音网页搜索、筛选、视频锁定
- 支持标题复合匹配校验（归一化 + 包含 + 相似度）
- 支持视频文案提取与修正
- 支持输出 meta / source-link / transcript 系列文件

## 打包文件检查结果
当前 `.skill` 包内包含：
- `douyin-video-skills/SKILL.md`
- `douyin-video-skills/references/filter-rules.md`
- `douyin-video-skills/references/publish-copy.md`
- `douyin-video-skills/scripts/run_pipeline.py`
- `douyin-video-skills/scripts/title_match_check.py`
- `douyin-video-skills/scripts/douyin_downloader.py`
- `douyin-video-skills/scripts/transcript_cleanup.py`

未发现多余脏文件（如 `.DS_Store`）。
