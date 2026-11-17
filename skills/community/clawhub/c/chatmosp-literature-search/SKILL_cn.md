---
name: chatmosp-literature-search
description: |
  chatMOSP 系统的学术文献检索器。当 MOSP_database 缺少匹配参数时，从开放获取期刊
  （Nature Communications、Science Advances、PNAS 等）和其他学术资源搜索并提取
  MSR/KMC 所需参数（表面能、吸附能、相互作用矩阵等）。
  触发场景：parameter-builder 检测到关键参数缺失，且用户选择通过文献检索补全时。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_cn.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-literature-search

## 1. 核心职责

1. 期刊搜索：按优先级访问 3 层期刊
2. 文章检索：3 阶段（摘要→正文→SI）
3. 参数提取：从表格中提取 E_ads、w、gamma 等
4. 参数验证：完整性 + 合理性 + 一致性
5. 返回带评分的结果给 parameter-builder

## 2. 输入契约

| 字段 | 必填 | 示例 |
|------|------|------|
| 金属元素 | 是 | Pd、Pt、Au、Cu、Ni |
| 气体体系 | 是 | CO+O₂、H₂+CO₂、CO+H₂ |
| 温度范围 | 否 | 300-500K |
| 压力范围 | 否 | 1-10 atm |

## 3. 输出契约

返回参数表格（JSON），包含：

| 字段 | 说明 |
|------|------|
| 表面能 | 各晶面（100、110、111）的 γ（eV/Å²） |
| 吸附能 | 各晶面 + 各气体的 E_ads（eV） |
| 相互作用矩阵 | CO-CO、CO-O、O-O 的 w（eV） |
| 参数来源 | DOI、文献标题、作者 |
| 完整性评分 | 1-10 分 |

> **⚠️ 文献搜索不返回气体熵**。返回后 parameter-builder 必须按 §3.1 公式重算。

## 4. 工作流程

```
输入（金属 + 气体）
  → 期刊搜索（按优先级 3 层）
  → 文章检索（3 阶段：摘要→正文→SI）
  → 参数提取（pdftotext + 关键词搜索）
  → 参数验证（完整性、合理性、一致性）
  → 输出（带评分的参数表）
```

## 5. 期刊搜索优先级

### 第 1 层：顶刊（优先但可能无法获取）

- Science、Nature、JACS、Angewandte Chemie、PRL、JCP
- 策略：DOI 解析 → 摘要 → 正文 → SI
- 遇到 API 限制或 CAPTCHA → **立即跳到第 2 层**

### 第 2 层：完全开放获取期刊（**推荐**）

- **Nature Communications**
- **Science Advances**
- **PNAS**
- **ACS Central Science**
- **Chemical Science**

优势：完全免费、质量高、SI 完整

### 第 3 层：预印本平台（最后选择）

- arXiv、ChemRxiv、bioRxiv
- 注意：未同行评审，参数可能不准确，需要用户确认

## 6. 工具选择

### 6.1 优先用当前环境可用的交互式浏览/网页工具

- ✅ 支持 JS 渲染
- ✅ 支持登录态
- ✅ 支持交互操作
- ✅ 适合期刊网站访问

### 6.2 不要用 web_fetch

- ❌ 期刊网站常有限制（403、CAPTCHA）
- ❌ 无法执行 JS
- ❌ 拿不到动态加载内容

### 6.3 降级

如果当前环境没有可用的浏览、网页检索或 PDF 工具，不要假装完成文献检索；
请用户提供文献、DOI、SI 文件或直接提供参数。

## 7. 详细文献检索流程

### 步骤 1：构建搜索关键词

**✅ 正确格式**（必须用）：

```
"keyword1" AND "keyword2" AND "keyword3"
```

**示例**：

- `Cu` 团簇在 CO 氧化环境 → `"Cu" AND "CO oxidation"`
- `Pd` 团簇在 CO 氧化环境 → `"Pd" AND "CO oxidation"`
- `Pt` 团簇在 H₂ 环境 → `"Pt" AND "H2"`

**❌ 错误格式**（禁止）：

```
Pd CO oxidation
```

空格分隔会导致搜索系统把整个短语当一个关键词，结果不准确。

### 步骤 2：访问期刊网站

- 用当前环境可用的浏览/网页工具进入期刊搜索页
- 输入关键词
- 默认按相关性排序

### 步骤 3：获取前 10 个结果

- 只检查前 10 个（相关性最高）
- 输出标题、DOI、摘要（可选）

### 步骤 4：初步筛选（基于题目）

筛选标准：

1. 反应气氛体系匹配（必须是 CO 氧化、WGSR 等目标反应）
2. 金属体系匹配（必须是 Pd、Pt、Cu 等目标金属，排除合金）

输出筛选后的文献列表 + 筛选理由

### 步骤 5：用户交互

请选择下一步：

1. 仔细检查全部筛选后的文章
2. 仔细检查某一篇（用户指定）
3. 换另一期刊

### 步骤 6：详细检查文章

**步骤 6.1**：检查正文

- 确认金属体系匹配
- 确认反应气氛匹配
- 是否有参数表格

**步骤 6.2**：没有参数 → 下载 SI

- 参数只可能存在于文字和表格，**不会**在图像中
- 下载 SI PDF：`si_{first_author}_{year}.pdf`
- 同作者同年多篇：`si_smith_2023a.pdf` / `b` / `c`

**步骤 6.3**：检查 SI

- 搜索关键词：Table、Supplementary Table、S1、S2
- 提取参数表格

### 步骤 7：参数提取

**步骤 7.1**：下载 SI

```bash
# 用当前环境可用的浏览/网页工具访问文章页下载 SI
```

**步骤 7.2**：PDF 转文本

```bash
pdftotext si_{author}_{year}.pdf si_{author}_{year}.txt
```

**步骤 7.3**：搜索参数表格关键词

- Table S, Supplementary Table
- adsorption energy, E_ads, binding energy
- surface energy, γ, surface tension
- interaction parameter, interaction matrix

**步骤 7.4**：用 `read` 工具读取文本，定位参数表格

**步骤 7.5**：从表格中提取数值，注意单位转换

**步骤 7.6**：验证参数

- 是否在合理范围内
- 是否符合物理规律
- 是否一致

### 步骤 8：向用户展示参数

```
📊 从文献中提取到以下参数：

【文献信息】
- 标题：{title}
- DOI：{doi}
- 期刊：{journal}

【参数表格】
- 表面能：{values}
- 吸附能：{values}
- 相互作用矩阵：{values}

【参数完整性评分】
- 评分：{score}/10
- 说明：{description}

请选择：
1. ✅ 使用这些参数 → 传给 parameter-builder
2. ❌ 拒绝，继续检索下一篇
3. ❌ 取消任务
```

## 8. 文章检索 3 阶段

| 阶段 | 目的 | 检索内容 |
|------|------|----------|
| 1. 摘要 | 确认相关性 | 金属、反应环境、研究类型 |
| 2. 正文 | 找参数表格 | Methods、Results、Tables、Figures |
| 3. SI | 补全参数 | Supplementary Tables、Methods、Data |

> ⚠️ **重要**：正文没提到参数不代表 SI 没有。如果文章相关性高，仍要下载 SI 检查。

## 9. MSR 需求的数据清单

### 基本参数

- ✅ 金属元素、温度、压力
- ✅ 团簇半径、气体种类、气体分压

### 表面参数（每个晶面）

- ✅ 表面能 γ（eV/Å²）：(100)、(110)、(111)、(211)、(311) 等

### 吸附参数（每个晶面 + 每种气体）

- ✅ 吸附能 E_ads（eV）：例 CO 在 Pd(111)、O₂ 在 Pd(100)

### 相互作用参数

- ✅ w 矩阵（eV）：CO-CO、CO-O、O-O

### 气体参数

- ✅ 气体熵（eV/K）：可通过公式计算（温度依赖）或从文献提取

> ⚠️ 文献搜索不返回气体熵，parameter-builder 必须自动计算

## 10. 参数完整性评分

### 分值表

| 参数类型 | 分值 | 说明 |
|----------|------|------|
| 表面能 | 2 分 | 至少 (100)、(110)、(111) 三个晶面 |
| 吸附能 | 3 分 | 每种气体在各晶面 |
| 相互作用矩阵 | 3 分 | CO-CO、CO-O、O-O |
| 参数来源 | 1 分 | DOI、标题、作者 |
| 参数合理性 | 1 分 | 在合理范围内、符合物理规律 |

### 等级处理

| 评分 | 等级 | 处理 |
|------|------|------|
| 9-10 | 完整 | 直接使用 |
| 7-8 | 较完整 | 用户确认缺失项后使用 |
| 5-6 | 部分完整 | 补充缺失参数 |
| 3-4 | 不完整 | 用相似金属参数参考 |
| 1-2 | 极不完整 | 不推荐使用 |

> ⚠️ **气体熵不在评分范围**。无论评分多少，parameter-builder 都必须按公式重算气体熵。

## 11. 超时与降级

### 11.1 超时机制

- 总时间限制：5 分钟
- 单篇文章限制：2 分钟
- 超时立即停止，返回已找到的参数（即使不完整）

### 11.2 降级方案

搜索 5 篇文献无完整参数时：

```
⚠️ 我已经搜索了 5 篇文献，但未能找到完整的参数。
- 表面能：✅ 已找到
- 吸附能：❌ 未找到
- 相互作用矩阵：❌ 未找到

建议：
1. 使用相似金属的参数作为参考
2. 提供已知参数来源（DOI 或文章标题）
3. 使用默认/测试参数
```

### 11.3 一个期刊失败的提示

```
⚠️ 在{期刊}的前 10 篇相关文章中未找到参数

请选择：
1. 更换期刊
2. 取消任务（如果所有期刊都没有，建议更换体系或用户提供参数）
```

## 12. 经验教训

- **教训 1：关键词选择**
  - 先用宽泛关键词（`"Pd" AND "CO oxidation"`）
  - 再用具体关键词筛选（`"adsorption energy"`）
  - 不要只搜参数名，要搜文章主题
- **教训 2：DOI 优先**
  - 优先用已知 DOI 或标题
  - 有 DOI 直接访问
  - 不只依赖关键词搜索
- **教训 3：多平台搜索**
  - 不局限单一期刊
  - 优先用开放获取期刊
- **教训 4：不要浪费时间在访问受限资源**
  - API 限制或 CAPTCHA → 立即跳下一层
  - 优先开放获取
- **教训 5：正文没提参数不代表 SI 没有**
  - 文章相关性高 → 仍下载 SI
  - SI 通常含完整参数表

## 13. 跨技能衔接

- **被调用**：parameter-builder 检测到关键参数缺失 + 用户选文献检索
- **调用工具**：当前环境可用的浏览/网页/PDF/文件读取工具
- **返回给 parameter-builder**：带评分的参数表

## 14. 依赖

- **chatmosp-parameter-builder** — 调用方
- **浏览/网页工具** — 期刊网站访问、SI 下载
- **pdftotext** — PDF 转文本
- **read** — 读取文本文件

## 15. 文件结构

```
chatmosp-literature-search/
├── SKILL.md       # 本文件（中文）
└── SKILL_cn.md    # 英文版
```

## 16. 实际操作示例

```
用户：show me the Pd cluster under atmosphere of CO and O2

1. 提取需求：metal=Pd, gases=[CO, O₂]
2. 检查 MOSP_database：无匹配
3. parameter-builder 提示并提供 4 选项 → 用户选文献检索（开放获取期刊）
4. 启动本技能：
   - 平台：Nature Communications
   - 关键词：`"Pd" AND "CO oxidation" AND "adsorption energy"`
   - 工具：当前环境可用的浏览/网页工具
5. 找到相关文章，确认 DOI
6. 下载 SI → 保存到 literature/
7. pdftotext 转换 → 搜 "Supplementary Table" → 提取参数
8. 验证：完整性评分
9. 展示结果 + 标注缺失项
10. 用户确认 → 传给 parameter-builder 组装 input.json

关键点：
- 始终从开放获取期刊开始
- 文献搜索不返回气体熵，parameter-builder 必须重算
- 相互作用参数可能是 KMC 格式，需 MSR/KMC 格式转换（见 parameter-builder §9）
```
## ChatMOSP 配套技能

本技能属于 ChatMOSP 技能组。完整功能需要在 ClawHub 中安装以下配套技能：

- chatmosp-input-coordinator
- chatmosp-parameter-builder
- chatmosp-msr-generator
- chatmosp-kmc-simulator
- chatmosp-literature-search
- chatmosp-file-organizer

如果缺少必要的配套技能，请先提示用户从 ClawHub 安装缺失的 ChatMOSP 技能后再继续。GitHub 仓库只作为备用安装方式。
