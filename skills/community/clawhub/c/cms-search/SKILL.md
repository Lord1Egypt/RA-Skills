---
name: cms-search
description: "联网搜索与实时信息检索。用于用户要求搜索、网上查询、查最新资讯、新闻、政策、公告、当前数据、资料，以及竞品、市场、医学或金融等依赖互联网信息的问题。复杂问题先拆成多个搜索维度，再逐次检索并综合验证。"
---

**当前版本**: v1.5.5

# CMS Search

## 工作流

1. 根据问题、上下文、实体别名、时间范围和证据需求确定搜索词。
2. 简单事实搜索 1 次；需要总结、比较、验证或追踪最新信息时，拆成 2-7 个维度。
3. 每个搜索词分别调用一次 `cms_search.py`；完成后合并、去重并交叉验证结果。

常用维度包括：核心事实、官方来源、最新动态、数据证据、风险争议、竞品对比，以及中英文名称或别名。

## 执行

`cms_search.py` 与本 `SKILL.md` 位于同一目录。根据本文件的实际位置取得脚本的绝对路径，不要依赖当前工作目录。

每次只执行一条直接 Python 命令：

```bash
python3 <技能目录的绝对路径>/cms_search.py --keyword "搜索词" --format md
```

执行前必须把占位路径替换为实际绝对路径。禁止使用 `cd`、`&&`、管道、重定向、heredoc、`bash -lc`、`python3 -c` 或 shell 循环。

多维搜索时，分别发起多次独立工具调用；单次失败只重试或调整该搜索词。

## 渠道选择

- 国内或通用查询：不传 `--source`，由服务端自动选择。
- 国外资料、英文信息、海外机构、GitHub、Stack Overflow 或论文：传 `--source tavily`。
- 国内外维度混合：按上述规则分别调用，不要为所有搜索词强制使用同一渠道。

示例：

```bash
python3 <技能目录的绝对路径>/cms_search.py --keyword "康哲药业 最新公告" --format md
python3 <技能目录的绝对路径>/cms_search.py --keyword "Keytruda clinical trial latest" --source tavily --format md
```

## 参数

- `--keyword`：必填，单次搜索词。
- `--source`：可选，支持 `tavily`、`glm`、`minimax`、`bocha`。
- `--format`：可选，`raw` 或 `md`，默认 `raw`。
- `--datetime`：可选，格式为 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS`。

用户询问“今天”“现在”或时间敏感的“最新”信息时，传入当前时间；历史年份或月份通常直接写进搜索词。按 `Asia/Shanghai (UTC+8)` 理解当前时间。

## 鉴权与故障

- `CMS_USER_KEY` 必须由运行环境提供，不得写入脚本、文档或命令参数。
- `Missing CMS_USER_KEY environment variable.`：运行环境未注入密钥。
- `can't open file`：脚本路径不正确；重新根据本 `SKILL.md` 的位置取得绝对路径。
- `complex interpreter invocation detected`：命令包含了 Shell 组合语法；改成直接调用 Python 脚本。
