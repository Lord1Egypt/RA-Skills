---
name: docx-chapter
description: "Research-backed chapter pipeline: outline → parallel ACP research → MD synthesis → DOCX generation → source verification → screenshot verification (mandatory)"
metadata:
  openclaw:
    emoji: "📄"
    requires:
      bins: ["pandoc"]
---

# docx-chapter

> 大纲 → 并行搜索 → 内容合成 → DOCX 生成 → 来源验证 → 交付

## 依赖

- `unified-search` skill → install from https://clawhub.ai/ccmxigua/unified-search-suite
- `tavily-research` skill → requires Tavily API key

## 输入格式

```yaml
title: "章节标题"
description: "章节定位与目标"
sections:
  - heading: "3.1 第一级标题"
    topics:
      - "子主题 1"
      - "子主题 2"
  - heading: "3.2 第一级标题"
    topics:
      - "..."
reference_docx: "/path/to/reference.docx"  # 可选，DOCX 样式参考
output_dir: "/path/to/output"              # 可选，默认 ~/.openclaw/media/outbound/
```

## 工作流程

### 阶段一：大纲解析 → 并行研究计划

1. 解析大纲 YAML，将每个 section 拆为独立研究主题
2. 为每个主题生成 ACP agent 任务：`/unified_search <关键词>` + Tavily Research 深度搜索 → 来源采集
3. 输出研究计划清单：主题 → 搜索关键词 → 预期来源数

### 阶段二：并行 ACP 研究（双搜索源：unified_search + Tavily Research）

**必须**使用 `sessions_spawn(runtime="acp", agentId="claude", mode="run")`，**禁止**默认 `runtime="subagent"`（继承 Telegram 路由会失败）。

> **ACP 参数固定规则**：以上参数为固定模板，**禁止**添加 `lightContext`（仅 subagent 有效，ACP 不认）、
> **禁止**添加 `runTimeoutSeconds` 等额外参数。AC 使用各自后端默认超时。

> ⚠️ **#50597 警告**：ACP Claude CLI 有 ~30% 概率返回空结果（只含 thinking block，0 输出 token）。
> 见 [GitHub #50597](https://github.com/anthropics/claude-code/issues/50597)。
> **降级策略**：子代理返回空、超时、或 Internal error 时，触发自动重试（最多 2 次）。
> 若 3 次全空/全失败，**降级走 `/unified_search`（三引擎搜索）**，禁止直接使用 llm-task。
>
> **为什么禁止 llm-task 降级**：llm-task 让模型直接搜索时，模型会编造/猜测 URL
>（已验证：BrowserStack `/guide/beta-testing`、`/guide/alpha-vs-beta-testing`、
> Testim `/blog/beta-testing/`、SoftwareTestingHelp `/alpha-testing-vs-beta-testing/`
> 均为 llm-task 幻觉 URL，返回 404）。`/unified_search` 返回真实可访问的 URL。

每个 ACP 子代理执行两路搜索后合并：

**① unified_search（快速结构化搜索）**
```
/unified_search <英文关键词>
```
记录每个来源的 URL、标题、日期、权威度、原文摘录。

**② Tavily 深度研究（补充覆盖面与深度）**
```bash
node ~/clawd/skills/tavily-research/scripts/research.mjs \
  "<英语研究问题>" --model pro --out /tmp/tavily_<topic>.md
```
读取 `/tmp/tavily_<topic>.md`，从报告中提取：
- 所有被引用的 URL、标题
- 与主题最相关的 2-3 句原文
- 补充 unified_search 未覆盖的来源

> Tavily Research 耗时 20-60s，等待期间可先整理 unified_search 的结果。

**③ 合并去重**
- 按 URL 去重，同一 URL 出现两次时保留内容更丰富的版本
- unified_search 优先用于 URL 准确性，tavily 用于深度补充
- 标注每个来源的搜索渠道：`source_channel`

返回结构化 JSON：
```
{
  "topic": "...",
  "sources": [
    {
      "url": "...",
      "title": "...",
      "date": "...",
      "authority": "gov|academic|news|commercial",
      "source_channel": "unified_search|tavily_research|both",
      "quotes": ["原文句1", "原文句2"],
      "key_data": {"metric": "value"}
    }
  ],
  "suggested_body": "基于来源的正文草稿"
}
```

### 阶段三：内容合成

0. **更新 research_results.json**：回填研究数据（仅更新，不覆盖已存在的 sources）：
   - `name` ← 从 `topics.json` 取对应的 `heading`（如 "Alpha 测试"）
   - `summary` ← 从 ACP agent 返回的 `suggested_body` 提取摘要（2-4 句）
   - `key_findings` ← 从 `suggested_body`/`sources` 提取 3-5 条关键发现
   - `status` ← `"research_completed"`
1. 合并所有子代理返回结果
2. **⚠️ 跨 agent URL 去重（强制硬步骤，不可依赖 LLM 自觉）**：
   ```bash
   python3 scripts/dedup_sources.py <research_dir>
   ```
   脚本自动完成：
   - 检测 `research_results.json` 中所有重复 URL
   - 保留脚注号最小的版本，删掉冗余条目
   - 重新连续编号所有来源
   - 重映射 `chapter.md` 中所有 `[^N]` 引用
   - 删除 `chapter.md` 中同一脚注号的重复定义
   - 同步更新 `verification_keywords.json`
   - 输出 `dedup_report.json` 记录去重详情

   **必须在生成 chapter.md 正文之前执行此步骤。**

3. 生成 MD 正文：每处数据/观点标注脚注引用 `[^N]`（每个来源只有一个脚注号，全文统一使用该号引用）
4. 脚注格式：`[^N]: 作者/机构。《标题》。发布日期。URL`
5. 脚注从 0 起连续编号
6. **同步输出 `verification_keywords.json`**：每写入一处 `[^N]` 时，顺带记录：
   - `footnote_id`：`N`
   - `source_url`：对应的来源 URL
   - `keywords`：该处引用的核心术语/数据（2-5 个英文词/短语，如 `["defect reduction", "85%", "alpha testing"]`）
   - 格式：`{ "footnotes": [ { "id": "0", "url": "...", "keywords": [...] }, ... ] }`
   - **原则**：写脚注的人最清楚自己在引用什么，关键词当场定下来。
7. **输出草稿 → 人工审阅**（必须，不可跳过）

#### 事后 Claim-Driven 关键词生成

当 `verification_keywords.json` 未在阶段三同步产出（或关键词来自 research quote 而非声明），
可使用 `keyword_generator.py` 基于声明（claim）反向生成关键词：

```bash
python3 scripts/keyword_generator.py chapter.json research_results.json verification_keywords.json
```

**原理**：遍历 `chapter.json` 中每个 `[^N]` 脚注，提取其所在句作为中文声明（claim），
在 `research_results.json` 中查找该脚注对应的英文研究原文，调用
`claim_keyword_extractor.py`（LLM）将中文声明翻译为英文关键词。

**关键差异**：
- **旧方式**：从 research quote 中提取高频英文短语（可能不反映声明中的断言）
- **新方式**：从中文声明出发，反向翻译为英文关键词，确保截图验证高亮的是"声明中实际断言的内容"

**示例**（fn#2 "CLSC 的关键特征包括：产品可回收性设计优先…"）：
- 旧方式输出：`"Jones Elite Logistics The"`, `"Closed Loop Supply Chain"`, `"includes product design"`
- 新方式输出：`"closed-loop supply chain"`, `"recyclable product design"`, `"forward reverse logistics"`, `"full lifecycle value"`, `"re-use and recycling"`

**原则**：同一套关键词既驱动内容写作，也驱动截图验证——声明驱动，追溯闭环。

### 阶段 3.5：正文脚注完整性检查（必须）

**此阶段不可跳过。** 在进入 DOCX 生成前，对 `chapter.md` 正文扫描**行内引用残留**——即未纳入 `[^N]` 脚注系统的括号引用。

扫描正则（Python）：
```python
INLINE_CITE_RE = re.compile(
    r'(?:'
    r'[（(][A-Z][A-Za-z]+(?:\s+et\s+al\.?|\s+等)?[，,\s]+\d{4}[a-z]?[)）]'  # （MDPI, 2022） / (Author, 2023)
    r'|[A-Z][A-Za-z]+[（(]\d{4}[)）]'                                         # Nature（2025）
    r')'
)
```

**检测流程**：
```bash
python3 -c "
import re, sys
with open(sys.argv[1], 'r') as f:
    text = f.read()
INLINE_CITE_RE = re.compile(
    r'(?:'
    r'[\（(][A-Z][A-Za-z]+(?:\s+et\s+al\.?|\s+等)?[，,\s]+\d{4}[a-z]?[)）]'
    r'|[A-Z][A-Za-z]+[\（(]\d{4}[)）]'
    r')'
)
for i, line in enumerate(text.split('\n'), 1):
    if line.lstrip().startswith('[^'):  # skip footnote definitions
        continue
    for m in INLINE_CITE_RE.finditer(line):
        print(f'L{i}: \"{m.group()}\" — 未纳入 [^N] 脚注系统')
" chapter.md
```

**处理规则**：
1. 每处匹配 → **ERROR** 级别。必须逐条回答：
   - 该引用对应哪个已验证的来源（URL）？
   - 若可对应 → 替换为 `[^N]` 脚注引用
   - 若无法对应任何已验证来源 → 删除该句或降级措辞（移除引用）
2. 检查通过条件：扫描零输出
3. 此检查必须在 `pandoc` 生成 DOCX 之前完成；若任一 ERROR 未解决，阻断进入阶段四

**常见坑**：
- 全大写缩写（如 MDPI、OECD）也会被捕获
- 中文/英文括号混合情况均覆盖
- 脚注定义行（`[^N]:`）自动跳过，不误报

### 阶段四：DOCX 生成

```bash
{{- if .args.reference_docx }}
# 先验证 reference.docx 存在，不存在则去掉 --reference-doc（否则 Pandoc exit 99）
pandoc chapter.md -o chapter.docx \
  --reference-doc="{{ .args.reference_docx }}" \
  --from markdown+footnotes+tex_math_dollars --to docx
{{- else }}
pandoc chapter.md -o chapter.docx \
  --from markdown+footnotes+tex_math_dollars --to docx
{{- end }}
```

> `--reference-doc` 可选：不指定时 Pandoc 使用内置默认样式。
> 
> ⚠️ **Pandoc 3.7 兼容性**：`tex_math_single_dollar` 扩展在 Pandoc 3.7.0.2 中不再支持，
> 仅使用 `tex_math_dollars`。若 `--reference-doc` 指向不存在的文件，Pandoc 会以 exit code 99 失败；
> 执行前必须 `test -f` 验证文件存在。

**Heading 层级映射**：
Pandoc 将 Markdown heading 映射为 Word 内置样式：
  - `# ` → Heading1
  - `## ` → Heading2
  - `### ` → Heading3
  - `#### ` → Heading4
章节编号需手动写入标题文字，Pandoc 不自动编号。

**脚注 URL 超链接化（强制）**：
Pandoc 默认将脚注中的 URL 输出为纯文本，在 Word 中不可点击。
生成 DOCX 后必须执行后处理脚本 `add_hyperlink_footnotes.py`：

```bash
python3 add_hyperlink_footnotes.py chapter.docx chapter.docx
```

> ⚠️ **Pandoc 会重编号脚注**：markdown 中的 `[^42]` 在 DOCX 中可能被重编号为 ID 37、38 等
> （Pandoc 按出现顺序分配连续 ID，且重复引用会被复制到不同 ID）。
> 排查时必须按 URL 内容定位，不可假设 markdown 编号 = DOCX 编号。

> ⚠️ **`add_hyperlink_footnotes.py` 依赖 `research_results.json`**：
> 脚本从 `research_results.json` 读取 URL→脚注映射来构建超链接。
> 若在修改 `chapter.md` / `research_results.json` 后未重跑此脚本，
> DOCX 中的脚注 URL 可能仍为旧值。变更三文件后必须重新执行：
> `pandoc` → `add_hyperlink_footnotes.py` → `verify_docx.py`。

后处理原理：
1. 解压 DOCX，解析 `word/footnotes.xml`
2. 找到每个脚注正文中的 URL（正确正则含 `（）`）
3. 将 URL 文本拆出独立的 `<w:hyperlink>` 元素（不含 `（日期访问）` 等中文后缀）
4. 为超链接内的 `<w:r>` 添加 `<w:rStyle w:val="Hyperlink"/>` 以显示蓝色下划线
5. 在 `word/_rels/footnotes.xml.rels` 中注册对应的 relationship
6. 重新打包 DOCX

### 阶段五：来源验证（Two-Pass 架构）

> 借鉴 citation-check v2 的 Two-Pass Architecture、Status Decision Tree、Numerical Precision Rules、Mandatory Search Templates。
> Pass 1 提取声明 → 直接进入 Pass 2 验证（无需人工闸门）。

#### 阶段 5A — Pass 1：声明提取

从 `chapter.md` 提取所有可验证的事实声明。使用 `scripts/extract_claims.py`：

```bash
python3 scripts/extract_claims.py chapter.md claims_pass1.json
```

**提取规则**（8 类声明，对齐 citation-check v2）：

| 类型 | 模式 | 示例 |
|------|------|------|
| **Statistic** | 含数字+单位的断言 | "准确率达 92.3%", "$4.7B 市场" |
| **Comparative** | X 比 Y 更/快/高/大 | "比基线快 3 倍" |
| **Temporal** | 时间限定断言 | "2024 年采用率达到…" |
| **Attribution** | 引用来源的声明 | "据 WHO…", "Smith 等发现…" |
| **Causal** | 因果关系 | "这使延迟降低了 40%" |
| **Existence** | 断言存在/为真 | "有 500M 用户" |
| **Ranking** | 排名/排他声明 | "最大", "首次", "前 3" |
| **Quote** | 直接引用 | 引号内归因文本 |

**排除**（不提取）：定义、明确标注的观点、假设、问题、无法来源的未来预测、方法论描述、致谢。

脚本输出 `claims_pass1.json`，包含每条声明的 `claim_id`、`text`、`claim_type`、`footnote_ids`。

#### 阶段 5B — Pass 2：内容级验证

对 Pass 1 输出的每条声明，使用以下决策树逐条验证。

**核心工具**：`/unified_search`（三引擎搜索）执行 Mandatory Search Templates。

##### Status Decision Tree（逐条应用）

```
START
│
├─ 是否为 Attribution 类型（引用论文/报告/来源）？
│   ├─ YES → 进入 CITATION VALIDATION
│   └─ NO  → 进入 STATISTIC/FACT VALIDATION
│
│
CITATION VALIDATION
│
├─ Step 1: 引用来源是否存在？
│   │   运行 Academic Search Templates（见 references/search_templates.md）
│   │
│   ├─ NO  → Status: "Citation Not Found"
│   │         Issue: "无法在任何数据库中定位 [引用]"
│   │         STOP
│   │
│   └─ YES → Step 2: 来源是否讨论声明所述主题？
│             │
│             ├─ NO  → Status: "Misquoted"
│             │         Issue: "来源存在但不讨论 [主题]"
│             │         STOP
│             │
│             └─ YES → Step 3: 来源是否支持原句？
│                       │
│                       ├─ YES (exact match)    → Verified (exact)
│                       ├─ YES (paraphrase)      → Verified (paraphrase)
│                       ├─ PARTIALLY (缺上下文)   → Misleading
│                       └─ NO (矛盾)              → Hallucination
│
│
STATISTIC/FACT VALIDATION
│
├─ Step 1: 能否找到权威来源？
│   │   按声明类型运行对应 Search Templates
│   │
│   ├─ NO  → Status: "Unverified"
│   │         Issue: "未找到权威来源"
│   │         STOP
│   │
│   └─ YES → Step 2: 数值是否精确匹配？
│             │
│             ├─ YES → Verified (exact)
│             │         STOP
│             │
│             └─ NO  → 进入 NUMERICAL ERROR DETAILS
│
│
NUMERICAL ERROR DETAILS
│
├─ 记录：来源值 / 声明值 / 偏差 / 来源位置
├─ 分类规则：
│   • 任何四舍五入    → Numerical Error
│   • 任何截断        → Numerical Error
│   • 有效位数不匹配  → Numerical Error
│   • 单位不匹配      → Numerical Error
│   • 方向反转        → Hallucination
│   • 数量级错误      → Hallucination
└─ 例外：来源自身提供近似值时（如 "96.555% (约 97%)"）→ Verified
```

##### 数值精度规则（学术标准）

| 规则 | 来源 | 声明 | 状态 |
|------|------|------|------|
| 精确匹配 | 96.555% | 96.555% | ✓ Verified |
| 任何四舍五入 | 96.555% | 97% | ✗ Numerical Error |
| 截断 | 96.555% | 96.5% | ✗ Numerical Error |
| 有效位不匹配 | 0.834 | 0.83 | ✗ Numerical Error |
| 单位不匹配 | 96.555% | 0.96555 | ✗ Numerical Error |
| 方向反转 | +12% growth | +15% growth | ✗ Hallucination |
| 数量级错误 | $4.7B | $47B | ✗ Hallucination |

##### 来源权威度分级

| Rank | 来源类型 | 示例 |
|------|----------|------|
| 1 | Primary source | 原始研究、官方报告、原始数据 |
| 2 | Government / Institutional | WHO, CDC, World Bank, 国家统计局 |
| 3 | Peer-reviewed | Nature, Science, IEEE, ACM |
| 4 | Industry reports (named) | Gartner, McKinsey, Statista |
| 5 | Reputable news citing primary | NYT, Reuters 引用原始来源 |
| 6 | Secondary compilations | Wikipedia（需核实其来源）|

**规则**：仅 Rank 5-6 来源 → Status = "Unverified" + 标注 "仅找到二级来源"。

##### Confidence 分类

| Level | 标准 | 使用场景 |
|-------|------|----------|
| **exact** | ≥95% 词重叠或同数字同单位 | 直接引用、精确统计 |
| **paraphrase** | 同事实，不同措辞，未加解读 | 重述发现 |
| **interpretation** | 从来源数据推断 | 从来源计算、综合得出 |

不确定时使用更保守的级别并标记审核。

##### 多源交叉验证

| 条件 | 所需来源 |
|------|----------|
| 找到 Primary source | 1 个（若权威：.gov, peer-reviewed, 官方） |
| 仅有二级来源 | ≥2 个独立来源一致 |
| 来源冲突 | Status = "Unverified"，标注冲突 |

##### Tie-Breaker Rules（边缘情况）

| 情况 | 规则 |
|------|------|
| 声明缺日期 | 假定指最近可用年份；标记 "需补充日期" |
| 来源冲突 | 使用最新权威来源；引用双方；标注冲突 |
| 所有搜索模板跑完未找到 | Status = "Unverified"（不是 Hallucination） |
| 数字因币种/单位转换不同 | 标记 "需澄清：币种/单位" |
| 同一机构多份报告 | 使用最新；标注日期 |
| 声明使用 "约""大约" 等 | 仍验证基数在来源 ±10% 范围内 |
| 来源 paywalled | 标注 "来源有付费墙，无法验证精确文本" |
| 来源为其他语言 | 翻译后验证；标注翻译 |

##### 结构性检查（继承原阶段五）

保留 `verify_docx.py` 的 DOCX 结构检查，合并进统一报告：

```bash
python3 verify_docx.py chapter.docx
```

检查项：URL 重复（坑 #4）、URL 无 hyperlink（补漏）、footnoteRef 缺失（坑 #6）、字体污染（坑 #7）、hyperlink 无样式、脚注编号缺口。

##### 搜索模板

详见 [references/search_templates.md](references/search_templates.md)。按声明类型分 5 组：Academic / Statistics / Company / Health / Government。

Pass 2 优先复用 Phase 2 的 `research_results.json` 中的搜索结果作为缓存（标注 `source: phase2_cache`），未覆盖的独立执行搜索。

##### Pass 2 输出

合并为统一验证报告 `chapter_verification.json`（Schema 见 [references/claim_verification_schema.json](references/claim_verification_schema.json)）：

```json
{
  "metadata": { ... },
  "pass1_extraction": { ... },
  "pass2_verification": {
    "summary": { "verified": N, "numerical_errors": N, "hallucinations": N, ... },
    "verified": [...],
    "numerical_errors": [...],
    "hallucinations": [...],
    "unverified": [...],
    "misleading": [...],
    "structural_issues": [...]
  },
  "sources_consulted": [...]
}
```

### 阶段六：截图标注验证

> Phase 6 触发前必须经用户确认（见 6A）。用户批准后方可执行截图。

#### 阶段 6A — 用户确认闸门（强制）

在截图开始前，输出以下信息并要求用户批准：

```
即将对 N 个来源进行截图验证：
  - 可达 URL: X 个
  - PDF（跳过）: Y 个
  - 不可达（跳过）: Z 个
  - 骨架网站（跳过）: W 个

每个截图将使用 Playwright 紫色高亮关键词标注。
预计耗时约 X 分钟。

请批准：回复 "批准截图" 继续 / "跳过截图" 跳过此阶段
```

**未收到用户批准前，绝对不执行任何截图操作。**

#### 阶段 6B — 截图执行

使用 `scripts/purple_highlight_screenshot.py`，**禁止**自行编写普通截图脚本。

```bash
# 单 URL 截图（Claim-Driven 推荐）
python3 scripts/purple_highlight_screenshot.py --smart --keywords-file verification_keywords.json <URL> <output.png>

# 单 URL 截图（手动指定关键词）
python3 scripts/purple_highlight_screenshot.py --smart <URL> <output.png> <keyword1> [keyword2] ...

# 批量截图（Claim-Driven 推荐）
python3 scripts/screenshot_verify.py <chapter.json> <output_dir> \
  --research research_results.json \
  --url-status url_status.json \
  --keywords-file verification_keywords.json
```

**--smart 模式**：自动提取页面文本，用 LLM 匹配关键词（处理同义改写）。

**--keywords-file**：从 `verification_keywords.json`（由 `keyword_generator.py` 或阶段三生成）
中读取 Claim-Driven 关键词。传递后，截图脚本使用声明驱动的英文关键词定位页面位置并高亮，
而非从 research quote 中提取关键词。

关键词来源（优先级）：
1. `--keywords-file` 传入的 Claim-Driven 关键词（推荐）
2. `verification_keywords.json`（阶段三或 keyword_generator.py 产出）
3. chapter.md 上下文中脚注所在句的关键词
4. research_results.json 中的 excerpt

特殊来源处理：
- PDF 来源 → 跳过截图，标注 `reason: PDF`
- 图片骨架网站 → `curl -s <URL>` 检查 HTML < 2000 chars → 跳过
- 不可达 URL（4xx/超时）→ 跳过，标注 `reason: unreachable`

#### 阶段 6C — 截图质量与声明对齐

每张截图分级（Grade）：

| Grade | 标准 | 含义 |
|-------|------|------|
| **A** | `highlighted_count > 0` AND body 含相关正文 | 高亮有效，可验证 |
| **B** | 页面加载正常但 `highlighted_count == 0` | 关键词不在页面或同义改写未匹配 |
| **C** | 页面加载但 body text < 100 chars | 骨架页/反爬/JS 渲染失败 |
| **F** | 截图失败（网络/超时/Roxy 额度不足） | 截图不可用 |
| **N/A** | 跳过（PDF/不可达/骨架网站） | 非截图问题 |

**声明对齐**：对 Grade A/B 的截图，提取页面中可见的数值/关键短语，与 Pass 1 对应声明做值级对比：

```
截图 fn03 → 声明 C004 "准确率 92.1%"
  页面可见文本："92.1% accuracy" → exact match ✓
  判定：Verified
```

#### 阶段六输出

截图的 `summary.json` 合并到统一验证报告 `chapter_verification.json` 的 `phase6_screenshots` 字段中（同 Schema）。

## 正文措辞审核规则

> 以下规则已纳入阶段五的 Pass 1 声明提取规则。声明提取时会自动标记以下类型的声明确保严格验证。

| 措辞类型 | 示例 | Pass 1 检查 | Claim Type |
|----------|------|-------------|------------|
| 排他性声明 | "列为重点""核心行动""首次提出" | 提取为 Ranking / Attribution | 来源原文必须逐字匹配 |
| 框架性声明 | "纳入…框架""建立…机制" | 提取为 Attribution / Existence | 需查看官方文件原文 |
| 量化断言 | "占比 X%""排名第 N" | 提取为 Statistic / Ranking | 来源直接引用，适用数值精度规则 |
| 时间关联 | "自 X 年起""Y 年 Z 月至" | 提取为 Temporal | 日期需与 HTTP Last-Modified 一致 |

**原则**：如果源文件中找不到逐字匹配的原句，降级措辞。宁可保守，不可夸大。

## DOCX 修改规范

修改已有 DOCX 正文前：

1. **先 dump 所有 run**：提取每个 `<ns0:r>` 的文本和脚注引用
2. **确认分隔边界**：脚注引用可能独占空 run（坑 #11）
3. **修改后连读验证**：确保 run 间逗号/句号完整
4. **保存前 git diff**：对比原始版本确认改动范围

## 搜索注意事项

- **中文主题：用英文关键词搜索**，避免 tokenizer 拆散整词（坑 #3）
- **双搜索源**：unified_search 提供结构化快速结果，Tavily Research 提供深度研究补充
- Tavily Research 失败（超时/API 错误/网络问题）→ 静默降级，仅使用 unified_search 结果，**不阻断** agent 执行
- 来源筛选：每个主题 3-5 个高质量来源，优先官方/学术
- 对不可达网站：尝试 `web.archive.org` 缓存版本

## 错误处理矩阵

| 严重度 | 定义 | 处理策略 | 示例 |
|--------|------|----------|------|
| **FATAL** | 管线无法继续 | 中断执行，报告用户 | 大纲解析失败、Pandoc 未安装 |
| **ERROR** | 某阶段失败但管线可降级 | 降级走 `/unified_search`（非 llm-task），跳过后继不阻塞 | ACP 返回空/失败、URL 不可达、Tavily Research 超时/失败 |
| **WARN** | 非阻塞异常 | 记录到报告，不中断 | 某个脚注缺 footnoteRef、字体异常 |
| **INFO** | 信息性提示 | 仅日志 | 使用了默认 reference.docx |

## Roxy 截图排坑（2026-05-28）

当截图验证（阶段六）遇到普通 Playwright 打不开的 URL（如 ACM DL、BMC、Splunk、ScyllaDB、CAP FAQ、AWS、HBase），需要走 Roxy 严格链路：

**正确链路**：
```
@roxybrowser/openapi MCP 开浏览器 → 从 open_browsers 响应提取 CDP WS
  → @roxybrowser/playwright-mcp --cdp-endpoint <ws_url>
  → browser_connect_roxy({ cdpEndpoint: ws_url })
  → browser_navigate → browser_take_screenshot
```

**关键约束**：
1. **不要调 `get_connection_info` 拿 WS URL** — 它返回所有已打开浏览器，regex 可能选错 → playwright-mcp 启动崩溃
2. **MCP stdio 交互用 Node.js 实现** — Python stdout 有缓冲，`bufsize=0` 不生效
3. **openapi MCP 进程保持存活** — 关闭会导致浏览器被清理，CDP WS 失效
4. **优先复用已有浏览器** — 窗口额度有限，用完截图 close + delete
5. **截图输出路径**：`browser_take_screenshot` 的 `filename` 为完整绝对路径时，文件保存到该路径（`~/.openclaw/media/outbound/xxx/screenshots_roxy/` 需提前 `mkdir -p`）

**参考实现**：`/tmp/roxy_full.cjs`（Node.js，2026-05-28 验证通过，6/7 URL 截图成功）

## 规则优先级

**规则优先级**：所有 DOCX 结构检查规则以 `verify_docx.py` 代码实现为准，本文档描述为辅助说明。若本文档与代码不一致，以代码为准。

## 脚注格式规范

- **多段脚注**：后续段落必须缩进 4 空格。未缩进时 Pandoc 将后续段落视为新脚注定义，导致正文截断
- **脚注内代码块**：**禁止**使用围栏代码块（```），改用 8 空格缩进
- **脚注内表格**：需额外 4 空格缩进（共 8 空格）；脚注内表格极易出错（行解析错误、跨列错位），建议尽量避免
- **章节标题编号**：需手动编写，Pandoc 不自动编号

## 已知陷阱与规避

| 坑 | 描述 | 规避方法 |
|----|------|----------|
| #50597 | ACP 空返回（~30%） | 自动重试 2 次 → 降级 `/unified_search` |
| llm-task 幻觉 | llm-task 直接搜索会编造 URL（404） | **禁止 llm-task 降级**，必须走 `/unified_search` |
| URL 重复 | 同一 URL 在 `<w:t>` 和 `<w:hyperlink>` 各一份 | `verify_docx.py` 自动检测 |
| footnoteRef 缺失 | ACP 修改后丢失 `<w:footnoteRef>` | `verify_docx.py` 检查 |
| 字体污染 | ACP 引入显式字体声明 | `verify_docx.py` 检查 BANNED_FONTS |
| URL 不可点击 | Pandoc 输出纯文本 URL | `add_hyperlink_footnotes.py` 后处理 |
| footnote_gap | Pandoc 重复引用同一脚注时，后续出现复制到不同连续 ID，中间 ID 被跳过（如 16→18、28→30） | **非阻塞 warning**；由 `verify_docx.py` 报告，不影响脚注功能。原因：Markdown 中同一 `[^N]` 被多次引用时 Pandoc 会占用新 ID |
| 超链接无样式 | URL 可点击但无蓝色下划线（缺 `rStyle="Hyperlink"`） | `add_hyperlink_footnotes.py` 已自动添加；`verify_docx.py` 检查 `hyperlink_no_style` |
| Roxy CDP WS 取错 | `get_connection_info` 返回所有浏览器，regex 可能匹配错误的 WS URL → playwright-mcp init timeout + EPIPE | 从 `open_browsers` 响应中按 dirId 精确提取 CDP WebSocket URL |
| Roxy 窗口额度不足 | 创建新浏览器报「窗口额度不足」 | 优先复用已有浏览器；截图后 close + delete 释放额度 |
| MCP stdio Python 缓冲 | Python `subprocess.Popen` stdout 在 `text=True` 下有缓冲 → MCP 响应延迟 → 脚本卡死 | 用 Node.js `child_process.spawn` + `stdout.on('data')` 逐行解析 JSON-RPC |

- `pandoc`（MD → DOCX 转换）
- ACP Claude CLI agent（并行研究 + DOCX 审查）
- `curl`（URL 可达性检查）
- Playwright（截图验证）
- `python3` + `lxml`（DOCX XML 检查）

## Checkpoint 持久化

大型章节管线执行时间较长（10+ 分钟），为避免重启丢失进度，每阶段完成后应将中间产物保存到 `output_dir`：

| 阶段 | 产物 | 保存路径 |
|------|------|----------|
| 阶段一 | 主题拆分 JSON | `output_dir/topics.json` |
| 阶段二 | 研究结果 JSON | `output_dir/research_results.json` |
| 阶段三 | 正文草稿 MD | `output_dir/chapter.md` |
| 阶段三 | 验证关键词 JSON | `output_dir/verification_keywords.json` |

恢复时从最近的 checkpoint 继续，跳过已完成的阶段。在 lobster pipeline 中可通过 `{{ .args.checkpoint_dir }}` 指定 checkpoint 目录（默认同 `output_dir`）。

## 输出

- `chapter.md` — 正文 + 脚注
- `chapter.docx` — 样式化的 DOCX（含 `reference.docx` 样式）
- `chapter_verification.json` — 验证结果（Phase 6）
- `verification_keywords.json` — 脚注 → 关键词映射（可由阶段三同步产出，或事后通过 `keyword_generator.py` 生成）
- `scripts/keyword_generator.py` — Claim-Driven 关键词生成编排器
- `scripts/claim_keyword_extractor.py` — LLM 驱动的声明→英文关键词翻译器
- `screenshots/` — 来源截图（Playwright 紫色高亮）

## 致谢 / Acknowledgments

本 skill 中的 Citation 提取（Pass 1）与验证（Pass 2）两阶段架构，在设计上参考了 **[serenakeyitan/citation-check-skill](https://github.com/serenakeyitan/citation-check-skill)**（MIT License, Copyright (c) 2026 Serena Keyi Tan）。感谢 Serena 的开源贡献。
