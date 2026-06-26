---
name: dochub
description: >
  专业文档知识库管理技能。将 .docx/.xlsx 原始文档编译为结构化 Markdown 知识库，基于 Andrej Karpathy 三层架构方法论（raw -> wiki -> schema）。支持初始化、增量更新、渐进式检索问答和知识健康检查四大操作。触发场景：用户初始化文档知识库、消化新文档、搜索文档内容、对文档提问、运行知识库健康检查 (lint) 时。
license: MIT
agent_created: true
---

# dochub — 文档知识库管理技能

基于 Andrej Karpathy LLM Wiki 方法论，将原始办公文档编译为结构化、可检索、可生长的 Markdown 知识库。

## 核心架构

采用 Karpathy 三层架构（详细原理见 `references/karpathy-methodology.md`）：

```
KNOWLEDGE_BASE_ROOT/               # 知识库根目录（由用户指定，如 C:\Users\xx\Documents\工作文档）
├── raw/                           # Layer 1: 不可变原始文档
│   └── {category}/{subdir}/*.docx, *.xlsx
├── wiki/                          # Layer 2: LLM 生成与维护的知识层
│   ├── _index.md                  #   主编排索引（渐进式披露 L1）
│   ├── _log.md                    #   仅追加操作日志
│   ├── _overview.md               #   知识库概况与统计
│   ├── sources/                   #   源文档摘要（markitdown 转换产物）
│   │   └── {category}/{subdir}/*.md
│   ├── concepts/                  #   概念页（LLM 生成）
│   ├── entities/                  #   实体页（LLM 生成）
│   └── comparisons/               #   对比分析页（LLM 生成）
├── update/                        # 增量更新投放区
├── _schema.md                     # Layer 3: dochub 治理规则
└── _dochub_knowledge_base.md      # 友好概览（向后兼容旧版）
```

### 三层架构要点

| 层 | 目录 | 角色 | 可变性 |
|----|------|------|--------|
| 原始层 | `raw/` | 源文档仓库，所有知识的真相来源 | **不可变** — LLM 只读不写 |
| 知识层 | `wiki/` | LLM 生成的结构化 Markdown | **完全由 LLM 维护** |
| Schema 层 | `_schema.md` | 治理规则、模板、工作流定义 | 人与 LLM 共同迭代 |

## 文档格式支持

| 格式 | 状态 | 说明 |
|------|------|------|
| `.docx` | 支持 | Word 现代格式，使用 python-docx 转换 |
| `.xlsx` | 支持 | Excel 现代格式，使用 openpyxl 转换 |
| `.doc / .xls / .pdf / .pptx / 其他` | **不支持** | 跳过转换，但建立索引（可定位 raw/ 原文） |

## 四大核心操作

### 操作 1: 初始化 (init)

将工作目录中原有的原始文档转化为完整知识库。

**触发方式：** 用户在 KNOWLEDGE_BASE_ROOT 下运行初始化，或明确说「初始化知识库」「dochub init」。

**完整流程：**

```
[1/7] 安全确认 → [2/7] 移动原始文档到 raw/ → [3/7] 文件名规范化 → [4/7] 检测不支持格式 → [5/7] MD转换 → [6/7] 生成知识层 → [7/7] 创建Schema
```

#### [1/7] 安全确认
- 询问用户：「是否已确认所有文档不含敏感个人信息、机密数据？(y/n)」
- **必须获得明确确认后才能继续。** 未经确认不允许进入下一步。
- 如果用户是首次使用，先确认 KNOWLEDGE_BASE_ROOT 目录路径。如果用户未指定，询问用户目标目录。

#### [2/7] 移动原始文档到 raw/
- 将 KNOWLEDGE_BASE_ROOT 下所有文件（除已有 raw/、wiki/、update/ 和 _schema.md 外）移动到 `raw/` 目录
- 保持原始目录结构，按现有分类子目录组织
- 同时排除 `.fnsync_temp_dir` 等临时目录
- 非 .docx/.xlsx 文件一并移动（将在步骤 4 处理）

#### [3/7] 文件名规范化
对 `raw/` 下所有文件执行文件名规范化：
- 保留：中文、英文、数字、中横线 `-`
- 替换：其他字符替换为 `-`
- 合并连续多个 `-` 为单个 `-`
- 去除首尾 `-`

#### [4/7] 检测不支持格式
- 扫描 `raw/` 下所有文件
- 识别非 `.docx` / `.xlsx` 文件（如 `.pptx`、`.pdf`、`.doc`、`.xls`、`.txt`、`.jpg`）
- 以表格形式列出跳过的文件清单
- 输出：「共发现 N 个不支持格式文件，将被跳过（不删除，仅不转换）。是否继续？(y/n)」

#### [5/7] MD 文档转换
将 `raw/` 下所有 .docx 和 .xlsx 转换为 Markdown，输出到 `wiki/sources/`，保持相同目录结构。

**转换工具选择：**

由于 markitdown 的 extra dependencies 在部分环境下解析不稳定，**优先使用原生库**：

| 格式 | 工具 | 方法 |
|------|------|------|
| `.docx` | `python-docx` | 提取段落（Heading 样式 -> `#` 标题）+ 提取表格（-> Markdown 表格） |
| `.xlsx` | `openpyxl` | 遍历 Sheet，每 Sheet 一个 `##` 标题 + Markdown 表格 |

如原生方案失败，可回退尝试 `markitdown[all]`。

**Python 路径：** 始终使用 `C:/Users/skya2/.workbuddy/binaries/python/envs/default/Scripts/python.exe`
如需安装依赖：`pip install python-docx openpyxl`

**写脚本执行：** 中文文件名在 here-doc 中可能编码异常，将转换脚本写入临时 .py 文件后执行，完成后删除临时脚本。

转换规则：
- 输入：`raw/{category}/{subdir}/file.docx`
- 输出：`wiki/sources/{category}/{subdir}/file.md`
- 转换前检查目标文件是否已存在
  - 首次存在时：询问「跳过 / 覆盖 / 全部跳过 / 全部覆盖」
  - 记录用户选择，后续同批处理自动应用
- 转换结束后输出统计：「成功 X 个，失败 Y 个，跳过 Z 个」
- 对于超过 50MB 的 xlsx 文件，使用 `read_only=True, data_only=True` 参数避免内存溢出

#### [6/7] 生成知识层
生成 wiki/ 下的核心文件：

**6a. 生成 `wiki/sources/` 下的源文档摘要页**

对每个转换后的 MD 文件，在文件头部添加 YAML frontmatter：

```yaml
---
title: {文档标题，从原始文件名推导}
type: source-summary
sources:
  - raw/{category}/{subdir}/{filename}.docx
domain: {从目录结构推导领域}
tags: [{从内容提取 3-5 个关键词}]
created: {转换日期}
updated: {转换日期}
confidence: high
---
```

**6b. 生成 `wiki/_overview.md`**（知识库概览）

```markdown
---
title: 知识库概览
type: overview
updated: {日期}
---

## 文档统计
- 总文档数: N
- 总大小: X MB
- 分类数: N
- 最后更新: {日期}

## 分类目录树
(可视化 ASCII 树状结构)

## 高频关键词标签云
(按频率排列的关键词列表)

## 文档索引
(按分类组织的完整文件清单，每项包含文件名、一句话摘要、标签)
```

**6c. 生成 `wiki/_index.md`**（主编排索引 — Karpathy 核心）

这是 LLM 检索的入口点，采用两级索引结构：

```markdown
---
title: 知识库索引
type: index
updated: {日期}
---

# 知识库索引

> **检索优先级：** 先查 MD 文档（可全文检索），无结果时再查原始文档（仅索引）。

## 分类导航

### {分类1}

#### MD 文档（可全文检索）
- [[{path}.md]]  {文档名}
...

#### 原始文档（仅索引，不可搜索内容）
- [{格式}] `raw/{path}`  {文档名}
...

### {分类2}
...

## 文档统计
- 原始文档: N 个 (X MB)
- MD 可检索: N 个
- 原始仅索引: N 个
- 分类: N 个
- 初始化: YYYY-MM-DD | 更新: YYYY-MM-DD
```

**索引规则：**
- 每个分类下分两层，MD 文档在上（优先），原始文档在下（备用）
- 不支持格式文件不跳过——全部纳入原始文档索引层
- 原始文档以 `[格式]` 标签标注（如 `[PPTX]`, `[PDF]`, `[TXT]`, `[JPG]`, `[DOC]`, `[XLS]`）
- 顶部添加检索优先级提示语

**6d. 初始化 `wiki/_log.md`**

```markdown
---
title: 操作日志
type: log
created: {日期}
---

## [{日期}] init | 知识库初始化
- 操作: 初始化知识库
- 文档总数: N
- 成功转换: X
- 跳过: Z (不支持格式)
```

#### [7/7] 创建 `_schema.md`
在 KNOWLEDGE_BASE_ROOT 下创建治理规则文件。

参考 `references/entity-types.md` 中的模板定义，生成适用于当前文档领域的 schema 文件。内容包括：
- 项目结构定义
- 页面类型与命名约定
- YAML frontmatter 规范
- 四大操作工作流
- 领域标签体系

---

### 操作 2: 增量更新 (update)

将新文档放入 `update/` 目录后运行。

**触发方式：** 用户说「dochub update」「增量更新」「有新文档」或明确指向 update/ 目录。

**完整流程：**

```
[1/6] 安全确认 → [2/6] 扫描update/ → [3/6] 检测不支持格式 → [4/6] MD转换 → [5/6] 更新知识层 → [6/6] 追加日志
```

#### [1/6] 安全确认
同 init 操作。确认新文档已脱敏。

#### [2/6] 扫描 update/ 目录
- 列出 `update/` 下所有文件
- 检测与 `raw/` 和 `wiki/sources/` 中已有文件的对应关系
- 输出变更摘要：「新增 M 个，更新 N 个，无变化 L 个」

文件对应判定：
- 同名文件（不含扩展名）= 同一文档的不同格式版本 → 视为更新
- 新文件名 → 新增文档

#### [3/6] 检测不支持格式
同 init 操作，列出非 .docx/.xlsx 文件。

#### [4/6] MD 转换
仅转换新增或已修改的文件：
- 新增 .docx/.xlsx → 转换
- 已修改（与 raw/ 中已有文件同名但内容不同）→ 转换（覆盖 wiki/sources/ 中对应 MD）
- 已有且未修改 → 跳过

转换方法同 init 操作 [5/7]，使用 python-docx + openpyxl 原生方案。

**文档归类（重要）：** 新文档不直接以其 update/ 中的目录结构存放，而应根据文档名/内容分析归入已有分类。规则：
- 文档名含「进港货站」「新货站」「发货」「分拣」「AGV」「ETV」「EMS」等关键词 → 归入「新进港货站」
- 文档名含「设施」「设备」「维修」「漏水」等关键词 → 归入「设施设备」
- 如果无法匹配现有分类，创建新分类目录（以文档名中提取的关键词命名）
- 仓库路径：`wiki/sources/{分类}/{YYYY-MM-DD-子主题}/文件.md`

#### [5/6] 更新知识层
级联更新受影响的 wiki 页面：

**必须更新的文件：**
- `wiki/_index.md` — 添加新条目
- `wiki/_overview.md` — 更新统计
- `wiki/sources/` — 新文档的摘要页

**建议更新的文件（LLM 自行判断）：**
- 相关概念页 — 如果新文档引入了新信息
- 相关实体页 — 如果新文档涉及已有实体
- 对比页 — 如果新文档与已有文档有互补/矛盾信息

**新类型页面的创建条件：**
- concept：多个源文档涉及同一主题，且主题足够独立 → 创建概念页
- entity：多个源文档提及同一实体 → 创建实体页
- comparison：两个或多个文档/概念存在对比价值 → 创建对比页

更新完成后，逐个更新页面的 YAML frontmatter 中的 `updated` 字段。

**索引结构规范：**

`_index.md` 中每个分类下分两层，严格执行：

```markdown
### {分类名}

#### MD 文档（可全文检索）
- [[xxx.md]]  文档名
...

#### 原始文档（仅索引，不可搜索内容）
- [格式] `raw/xxx`  文档名
...
```

**关键规则：**
- MD 文档在上（优先），原始文档在下（备用）
- 不支持格式文件也要索引，以 `[格式]` 标签标注
- 新文档按内容归类到已有分类中，不应自建顶级分类
- 检索时先查 MD 全文，无结果才查原始文档索引定位 raw/ 原文

#### [6/6] 追加操作日志

```markdown
## [{日期}] update | {源文件名}
- 变更类型: 新增/更新
- 归类: {分类名}
- 影响页面: [{受影响 wiki 页面列表}]
- 摘要: {一句话描述}
```

**重要：** 更新完成后，将 `update/` 中的原始文件移动到 `raw/` 对应分类目录。不支持格式文件也一并移动并加入索引。

---

### 操作 3: 检索与问答 (search)

**触发方式：** 用户提问涉及文档内容，说「查一下」「搜索」「dochub search」等。

**检索策略（Karpathy 渐进式披露）：**

```
L0 → L1 → L2 → L3
```

| 级别 | 内容 | Token 预算 | 何时加载 |
|------|------|-----------|---------|
| L0 | 工作上下文（用户 profile） | ~200 | 每次会话 |
| L1 | `wiki/_index.md` | 1-2K | 每次检索开始 |
| L2 | 匹配页面内容（grep 定位） | 2-5K | 索引命中后 |
| L3 | 完整源文档（`wiki/sources/`） | 5-20K | 需要原始细节时 |

**检索流程：**

1. **读索引**：先读取 `wiki/_index.md`，确定相关页面
2. **关键词搜索**：在 `wiki/` 目录下使用 grep 搜索用户问题的关键词
3. **读匹配页**：读取匹配的 wiki 页面（优先 L2 级别）
4. **溯源验证**：如需要，追溯 `wiki/sources/` 中对应源文档验证细节
5. **综合回答**：

回答格式遵循 Karpathy 双输出原则：

```
## 回答
{基于文档内容的综合回答}

## 来源
- [[wiki/sources/{path}/file]] — {一句话说明}
- [[wiki/concepts/{concept}]] — {一句话说明}

## 置信度
{high / medium / low} — {简要说明}
```

**特别规则：**
- 如果回答具有长期价值，**主动提议**将其保存为新的概念页/对比页/实体页
- 必须引用来源，使用 `[[wikilinks]]` 格式
- 不编造信息——如果文档中没有相关内容，明确告知
- 如果发现文档间矛盾，标注并记录

---

### 操作 4: 健康检查 (lint)

定期对知识库进行全面体检。

**触发方式：** 用户说「dochub lint」「知识库检查」「健康检查」。

**检查维度（Karpathy Lint 操作）：**

| 检查项 | 说明 | 输出 |
|--------|------|------|
| **矛盾检测** | 扫描 wiki 页面间的冲突声明 | 矛盾清单（页面A vs 页面B，具体冲突点） |
| **孤立页面** | 无 [[wikilinks]] 入链的 wiki 页面 | 孤立页面清单 |
| **缺失概念** | 被引用但尚未创建页面的主题 | 缺失概念清单及引用来源 |
| **过期声明** | `updated` 超过 90 天的页面 | 过期页面清单 |
| **置信度异常** | `confidence: low` 且被广泛引用的页面 | 需复核页面清单 |
| **格式一致性** | YAML frontmatter 完整性、命名规范、交叉引用有效性 | 格式问题清单 |
| **知识缺口** | 建议深入研究或补充的领域 | 研究建议清单 |

**输出格式：** 生成 `wiki/_lint-{YYYY-MM-DD}.md` 文件，包含所有检查结果。

同时追加到 `wiki/_log.md`：

```markdown
## [{日期}] lint | 知识库健康检查
- 矛盾: N 处
- 孤立页面: N 个
- 缺失概念: N 个
- 过期页面: N 个
- 格式问题: N 处
- 建议: {摘要}
```

---

## 关键设计决策

### 为什么是三层架构而不是简单文件夹？

| 问题 | 简单文件夹方案 | dochub 三层架构 |
|------|---------------|----------------|
| 知识积累 | 每次搜索需要重新扫文档 | wiki 层持续生长，知识复利 |
| 交叉引用 | 无结构化关系 | `[[wikilinks]]` 预建关联 |
| 可追溯性 | 无法验证信息来源 | 每个声明可追溯到 `raw/` |
| 维护成本 | 人工手动组织 | LLM 自动维护索引和交叉引用 |
| 置信度 | 无法判断可靠性 | 每页标注 confidence |
| 知识衰减 | 无法发现过时信息 | lint 操作定期体检 |

### 与 RAG 的区别

dochub 不依赖向量数据库或嵌入管道。它的策略是**编译，而非检索**——LLM 提前将知识组织好，而非每次查询时临时拼接。

### 渐进式披露

`_index.md` 是解决上下文窗口退化的核心机制。LLM 始终先读索引（1-2K token），而非加载整个知识库。索引质量随知识库增长自动提升——因为它是 LLM 自己维护的。

## 安装依赖

**必需依赖（原生方案，推荐）：**
```bash
pip install python-docx openpyxl
```

**可选依赖（markitdown 回退方案）：**
```bash
pip install "markitdown[all]"
```

**Python 路径：** `C:/Users/skya2/.workbuddy/binaries/python/envs/default/Scripts/python.exe`

## 工作目录配置

- KNOWLEDGE_BASE_ROOT 由用户在首次 init 时指定，或从当前工作目录推断
- 如果用户未明确指定路径，询问：「请指定需要管理的文档目录路径（如 C:\Users\xx\Documents\工作文档）」
- 所有 dochub 操作默认在 KNOWLEDGE_BASE_ROOT 下执行

## 与用户的交互约定

1. **安全确认不可跳过**：init 和 update 操作必须先确认文档已脱敏
2. **进度可视化**：每个操作步骤以 `[X/N]` 格式显示进度
3. **批量确认**：覆盖/跳过等决策首次询问后自动应用
4. **主动提议**：检索中发现的长期价值内容，主动提议保存
5. **诚实告知**：文档中无相关内容的，明确告知而非编造
6. **增量输出**：阶段明显断开时，分批输出结果

## 实战经验

### 转换脚本模板

由于中文文件名在 bash heredoc 中可能编码出错，转换脚本应写入临时 .py 文件后执行：

```python
# docx 转换
import docx
doc = docx.Document(path)
for para in doc.paragraphs:
    if para.style.name.startswith('Heading'):
        level = para.style.name.split()[-1]
        lines.append('#' * level + ' ' + para.text)
    else:
        lines.append(para.text)
for table in doc.tables:
    # 转为 Markdown 表格

# xlsx 转换
import openpyxl
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
for ws_name in wb.sheetnames:
    lines.append(f'## {ws_name}\n')
    for row in ws.iter_rows(values_only=True):
        # 首行作表头，后续行作数据
```

### 大文件处理
- 超过 50MB 的 xlsx：`load_workbook(path, read_only=True, data_only=True)`
- 99MB 漏水点清单实测可用，但转换耗时较长

### 已知坑点
- `markitdown` 基础安装不含 docx/xlsx 支持，需 `markitdown[all]`
- 即使安装 `markitdown[all]`，部分环境仍报 MissingDependencyException
- 推荐直接用 python-docx + openpyxl 原生方案，确定性更高
- Windows 下移动文件到 Documents 目录可能触发沙箱拦截，需要 `dangerouslyDisableSandbox`
