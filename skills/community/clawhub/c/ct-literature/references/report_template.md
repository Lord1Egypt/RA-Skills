# Report Template / 报告模板（通用外壳 · Generic Shell）

> **🌐 Output language / 输出语言 (configurable, opt-in / 可配置、按需):**
> Output language follows the user's stated preference and is **not mandated**.
> - Default recommendation: bilingual `English / 中文` (both shown side by side) for ct- skills that follow the bilingual policy.
> - Single-language output (English-only or Chinese-only) is fully supported — just set the user's requested language.
> - In regulated clinical workflows where output language must be tightly controlled, use the user's single requested language only.
> / 输出语言**遵循使用者指定偏好，不做强制**。默认推荐双语 `English / 中文`（并列展示），对套用双语策略的技能；也完全支持单语输出（仅英文或仅中文），只需按使用者要求的语言即可；在输出语言须严格管控的受监管临床试验场景中，仅使用使用者指定的单一语言。
>
> **English / 中文:** By default, end every analysis with this structure + results; include the standalone R code block ONLY when the user explicitly asks for it. / 默认每次分析以该结构 + 结果收尾；仅当使用者明确要求时，才附上完整可运行的 R 代码块。

---

## Structure / 报告结构

> This is a **generic analysis-report skeleton** shared by every ct- skill.
> Replace the bracketed placeholders with your domain content; add or drop
> sections as the analysis requires. / 这是**全库通用的分析报告骨架**。把方括号占位符替换为你的领域内容；按分析需要增删章节。

### 1. Title / 标题
```
## 📊 [Analysis Type] Report / [分析类型] 报告
```

### 2. Context / 背景与设定
```
- **Scope / 范围**: [what is being analyzed]
- **Method / 方法**: [approach / engine used]
- **Data Source / 数据来源**: [input files / public registries / ...]
```

### 2b. Search Provenance / 检索上下文（可复现性，检索/下载类技能强制）

> 2026-08-14 新增。检索 / 下载类技能（ct-literature / ct-registry / ct-safety 等）的**任何报告产物**（HTML / Excel / Markdown 等）头部必须包含检索上下文，使报告**脱离原始对话也能复现"当时查了什么"**——参考实现：ct-literature HTML banner 与 Excel scope（2026-08-14）。

```
- **User Query / 用户检索词**: [原始输入，如 奥希替尼 间质性肺病]
- **Derived Query / 实际检索式**: [翻译/扩展后的 query，如 (osimertinib OR Tagrisso) interstitial lung disease (ILD)]
- **Generated Keywords / 生成关键字**: [技能派生的关键词，无则 "—"]
- **Filter / 筛选条件**: [review type / 年份范围 / safety 模式等]
```

**要点**：
1. **原始输入必须保留**（翻译 / 规范化后不得覆盖用户原文）——meta 中 `topic_zh`（原文）与 `topic_en`（派生）并存，报告展示 `原文 → 英文`。
2. 实际执行的检索式（含同义词 OR 扩展）须可见——证据日志 / 溯源表记录 `query` 字段。
3. 生成关键字（`keywords`）须随报告输出（此前 ct-literature 曾漏传 meta 至 HTML 渲染器，导致报告缺检索信息——2026-08-14 修复，教训：meta 必须一路携带到所有导出器）。

### 3. Input Parameters / 输入参数
```
- **Parameter 1 / 参数 1**: [value]
- **Parameter 2 / 参数 2**: [value]
```

### 4. Results / 计算结果
```
- **Primary result / 主要结果**: [value]
- **Secondary result / 次要结果**: [value]
```

### 5. Interpretation / 结果解释
```
[Plain-language explanation of what the result means]
[用通俗语言解释结果]
```

### 6. Assumptions / 前提假设
```
[model / distribution / independence assumptions, etc.]
```

### 7. Methodological Limits / 方法学限制
```
[approximation conditions / fallback simplifications]
```

### 8. Sensitivity / 敏感性建议
```
[how results change if a key input moves]
```

---

## ⚠️ On Request: Reproducible R Code / 按需提供：可复现的 R 代码

> **EN/CN:** Include this block ONLY when the user explicitly asks for the reproducible R code; it is hidden by default.

```markdown
---

## 📋 Reproducible R Code / 可复现的 R 代码

> Copy to R Studio or save as `.R` and run with `Rscript` to reproduce.

```r
# ============================================================
# [Analysis Title] — Standalone R Script
# [分析标题] - 可独立运行的 R 脚本
# Generated / 生成时间: [YYYY-MM-DD]
# Path / 计算路径: [engine used]
# ============================================================

# ---- 0. Setup (uncomment first run) / 环境准备 ----
# install.packages(c("[pkg1]", "[pkg2]"))

# ---- 1. Load packages / 加载包 ----
# library([pkg1])

# ---- 2. Parameters / 参数设置 ----
param1 <- [value]

# ---- 3. Calculate / 计算 ----
[core function calls with hardcoded values]

# ---- 4. Output / 输出 ----
cat("\n===== Result / 计算结果 =====\n")
```

**Run / 运行方式**:
- R Studio: paste into script window
- CLI / 命令行: `Rscript analysis.R`
```

---

## R Code Generation Rules / R 代码生成规则

| Rule 规则 | Description 说明 |
|:---------|:----------------|
| **Complete 完整** | install.packages / library / calc / output |
| **Hardcoded 硬编码** | Actual values, no placeholders |
| **Runnable 可复现** | Copy-paste executable in R |
| **Sanitized 脱敏** | Paths stripped, no subject data in output |
