---
name: geo-prohibited-word-checker
description: GEO/SEO内容违禁词检测与智能替换。当用户需要检测文章中的违禁词、检查GEO/SEO内容合规性、或要求替换违禁词时使用此技能。支持检测广告法违禁词（绝对化用语）、夸大宣传词、违法内容词、误导性词汇等，并根据上下文智能生成保留原意的替换方案。触发词：检测违禁词、检查违禁词、违禁词替换、违禁词修改、违规词、GEO合规检查、SEO合规、文章合规、内容合规。
agent_created: true
---

# GEO 违禁词检测与替换

写完文章后自动检测违禁词并智能替换，全程无需用户干预。脚本做确定性检测，AI做语义替换。

## 收费模式

| 模式 | 功能 | 费用 |
|---|---|---|
| **免费层** | 检测前3个违禁词 + AI替换 | 0元 |
| **付费层** | 完整检测全部违禁词 + AI替换 | 按次扣费 |

付费层通过 API Key 激活。用户通过环境变量配置：

```
环境变量 GEO_API_KEY=<用户的API Key>
环境变量 GEO_API_ENDPOINT=<验证服务地址>
```

或在脚本调用时通过 `--api-key` 和 `--api-endpoint` 参数传入。

未配置 API Key 时自动进入免费层（仅显示前3个违禁词）。

## 触发场景

- 用户写完文章后要求检测/替换违禁词
- 智能体写文章流程中的合规检查步骤
- 用户提供文章（文件路径或粘贴文本）要求检查合规性

## 自动化流程（3步完成）

### 第1步：获取文章内容

从以下来源自动获取内容，**不要询问用户**：
- 对话中已有的文章文本 → 直接使用
- 用户提供的文件路径 → 用 Read 工具读取
- 用户粘贴的文本 → 直接使用

### 第2步：运行检测脚本

执行检测脚本扫描文章。脚本和词库路径相对于本技能目录：

```bash
python <本技能目录>/scripts/detect_words.py --file <文章路径> --wordlist <本技能目录>/assets/prohibited_words.txt --classify
```

如果是粘贴文本，先将文本写入临时文件再检测，避免 shell 转义问题：

```bash
python <本技能目录>/scripts/detect_words.py --text "<文章文本>" --wordlist <本技能目录>/assets/prohibited_words.txt --classify
```

**付费模式调用**（如果用户配置了 API Key）：

```bash
python <本技能目录>/scripts/detect_words.py --file <文章路径> --wordlist <本技能目录>/assets/prohibited_words.txt --classify --api-key <KEY> --api-endpoint <URL>
```

脚本输出 JSON，包含：
- `summary.total_matches`：匹配总数
- `summary.categories`：按类别统计（advertising/exaggeration/illegal/misleading/general）
- `matches`：每个匹配的词、位置、上下文、类别
- `billing.mode`：`"free"` 或 `"paid"`
- `billing.truncated`：免费模式下是否截断了结果
- `billing.hidden_count`：免费模式下隐藏的违禁词数量
- `billing.message`：计费状态说明

### 第3步：智能替换并输出

**如果 total_matches 为 0**：告知用户"文章未检测到违禁词，内容合规"，结束。

**如果有违禁词**：读取 `references/replacement_guide.md` 获取替换策略，然后自动执行替换：

1. 按类别优先级处理：违法内容 → 误导性 → 广告法 → 夸大宣传
2. 同类别内按词长降序处理（长词优先，解决重叠词问题）
3. 根据每个匹配词的上下文，按替换指南生成保留原意的替换文本
4. 从文本末尾向前替换，保持位置索引正确
5. 替换完成后通读全文，确保语句通顺

**输出**：
- 展示修改对照表（原文 → 替换后）
- 保存修改后的文件为 `原文件名_clean.原后缀`（如 `article_clean.md`）
- 粘贴文本则保存为 `article_clean.txt` 到当前工作目录

**免费模式额外提示**：
如果 `billing.truncated` 为 `true`，在输出末尾附加提示：
> 当前为免费模式，仅检测并替换了前3个违禁词。文章中还有 {hidden_count} 个违禁词未检测。配置 API Key 可启用完整检测。API Key 购买方式：[你的购买渠道]

## 文件说明

| 文件 | 用途 |
|---|---|
| `scripts/detect_words.py` | 检测脚本，加载词库并逐词匹配，输出JSON，支持免费/付费模式 |
| `scripts/billing_worker.js` | Cloudflare Worker 验证服务代码（技能作者部署，用户无需关心） |
| `references/replacement_guide.md` | 4类违禁词替换策略和示例 |
| `references/deploy_guide.md` | 付费模式部署指南（技能作者使用） |
| `assets/prohibited_words.txt` | 9409个违禁词，每行一个，UTF-8编码 |

### 词库更新

替换 `assets/prohibited_words.txt` 即可。支持两种格式：每行一词（首选）或逗号+引号分隔。

## 设计要点

- **检测确定性**：Python `str.find()` 精确匹配，9409词×5000字约0.02秒
- **替换语义化**：AI理解上下文后替换，"顶级"在不同语境有不同替换方案
- **长词优先**："排名第一"先于"第一"处理，替换后短词自动消失
- **全程自动**：检测→替换→输出一气呵成，无需用户逐步确认
- **免费增值**：免费层可用但有限制，付费层完整功能，Key验证通过HTTP在线完成
