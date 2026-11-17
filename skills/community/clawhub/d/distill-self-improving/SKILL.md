---
name: distill-self-improving
description: 当用户明确指定文件、目录、项目或资料时，把确认范围加入本机知识库，建立便于查找的目录导航，并逐份读取和整理。对有长期价值的内容分别形成独立总结；对无法读取、敏感、重复或不适合保留的文件逐件说明处理结果。代码项目侧重关键入口和重要说明文档，资料目录按用户要求逐文件处理，是否由 Git 管理只作参考而不会单独决定类型。普通查看、问答或自动发现不会触发，原始文件始终保持不变。
---

# 建立文件索引与蒸馏

## When to use

- 自然请求包括“把这个目录加入知识库”“把该目录及其下所有文件收录”“只登记这个项目”“整理这份设计文档”“更新已登记资料集”。路径清晰时直接执行；仅在路径或范围仍有多个合理解释时问一个自然问题。
- “只索引、只登记、不整理正文”完成导航与台账后停止。“加入知识库”在本流程中只指导航、台账、单文件结果和项目综合，不自动创建知识或经验条目。
- 不用于普通阅读、一般问答、普通错误、工作完成后的自动沉淀，或未获用户确认的扫描命中目录。
- 首次建设、目录批量处理、collection 迁移、分类犹豫或异常时，开始前完整读取 [批量迁移、异常与真实场景](references/distillation-scenarios.md)；单个清晰文件可只执行下面适用阶段。

## Workflow

完整 collection 必须依次通过 G0–G7；小规模索引或单文件请求只执行适用子集。每个阶段当场校验，失败时不得进入后续阶段。纯本阶段错误只修本阶段；若根因来自上游，回到最早受影响阶段，保留此前已验证产物，修后顺序重跑全部受影响下游。最终报告不能掩盖中间失败。

### G0 初始化、路径与契约

- **输入**：用户明确对象、`~/.agent-knowledge/` 当前状态、本包模板。
- **动作**：确认数据根是预期目录且非 reparse；缺失时从 [根导航模板](assets/root-readme-template.md) 初始化最小 README、`indexes/projects.md`、`indexes/files.md`、`indexes/projects/` 和 `indexes/collections/`。只创建本流程拥有的索引结构；已有内容只补缺项，不覆盖。
- **通过条件**：数据根、README、索引入口可读；所有计划写入路径均位于数据根内；原文件根保持只读。
- **失败回退**：路径非法、越界、权限或磁盘故障时停止受影响项，保留已有文件，用普通语言报告；不要另找目录绕过。

### G1 冻结范围与目录类型

- **输入**：用户明示范围、现场文件清单，以及 README、项目说明或其他入口文档、构建与依赖清单、`src`/`test` 布局、源码扩展名密度、文档格式和目录结构等证据；版本控制只作佐证。
- **动作**：判定 `code-project`、`document-collection` 或 `mixed-general`，冻结 included/excluded/expected paths；有分组时同时冻结 `path→group`。用户明确“目录及其下所有文件”时递归列入全部用户内容普通文件，不跟随 reparse；固定排除版本控制内部元数据、依赖、构建、cache、temp 派生树，并逐条报告规则与数量，根部用户配置文件不因此排除。
- **通过条件**：路径唯一、范围无重叠、类型证据与处理策略一致，排除规则有数量；逐件合法跳过分类与 reason 口径已冻结。Git 存在不证明是代码项目，缺失也不证明不是。
- **失败回退**：证据冲突或对象边界不清时停在本阶段，不猜。解析器、权限等临时故障不是“无价值”理由，必须在后续读取阶段诚实暴露为未完成。

处理策略：普通代码项目仅冻结高价值入口；未入选源码为 out-of-scope。若明确“全部文件”，所有用户内容源码进入范围，但默认仅索引并以具体 reason 合法跳过正文整理。文档目录默认逐文件。mixed 普通模式由根项目导航、有限代码 inventory 和互不重叠的文档子树 collection 组成；mixed 全文件模式由根 collection 唯一持有逐文件范围，文档子树仅作 group/summary。任何单文件结果都由唯一 collection manifest 持有；代码项目需要整理 README、设计或规范时，建立唯一 `<project-slug>-docs` collection。构建/依赖清单默认仅索引，只有被明确点名或原文确有稳定人类说明时才整理。

### G2 建立索引与审计台账

- **输入**：G1 冻结的 expected paths、`path→group`、目录类型和 owner 边界。
- **动作**：用 [项目总表](assets/projects-index-template.md)、[文件总表](assets/files-index-template.md)、[项目 README](assets/project-readme-template.md) 和 [项目 inventory](assets/project-inventory-template.csv) 建导航；collection 复制 [README](assets/collection-readme-template.md)、[scope](assets/collection-scope-template.csv)、[inventory](assets/collection-inventory-template.csv) 与 [manifest](assets/collection-manifest-template.csv)。G2 只写 `indexed=true` 和索引/现场元数据；统一 manifest 表头中的 `read/distilled/skipped/reason/output_ids` 可留空，禁止用 “pending” 占位。现有旧 collection 缺 scope 时，只有显式只读 legacy 核验可用已一致的 inventory/manifest 共同路径集；任何更新都必须先按本次授权补 scope，禁止从结果反推 expected。
- **通过条件**：scope、inventory、manifest path 集合相等且唯一；manifest 每行 `indexed=true`，现场元数据合法；所有入口可互相反查。跨 collection 用宿主 CSV/Markdown 解析确认同一路径只有一个 owner。运行 `check --gate G2`；下游空字段不算失败，其他本阶段失败必须为零。
- **失败回退**：只修台账与 owner，不读取下一批正文。磁盘上被扫描到不构成入库理由；用户收窄范围时按路径键移除范围外记录，但删除已有结果仍需用户授权。

### G3 原文件读取与逐文件分类

- **输入**：G2 的每一条 inventory/manifest，以及只读原文件或经 identity 核验可复用的历史提取。
- **动作**：逐文件使用适合格式的安全解析器；记录本轮是否实际读取、是否有稳定价值、是否整理或跳过。历史摘要和提取缓存只是证词：只有 size/mtime 或必要内容 hash 与当前原文件一致时可辅助本轮读取；不一致必须重读。不得为了通过校验改写原始证词。
- **通过条件**：完整 collection 必须先完成全部 G3；每条都有真实 `read/skipped` 决策，`read=false` 或 `skipped=true` 时 reason 具体；`distilled/output_ids` 此时仍可留空。不可解析、受限、敏感、重复、工具噪声可合法 skip，临时故障仍是未完成。运行 `check --gate G3`。
- **失败回退**：停止受影响文件或批次，保留其他已读回证据；重新读取/提取或诚实报告未完成，禁止把失败伪装成低价值继续。

### G4 单文件独立蒸馏

- **输入**：G3 判定“已读、有稳定价值、可安全整理”的原文件。
- **动作**：每份原文件复制 [单文件模板](assets/file-distillation-template.md)，形成唯一独立 Markdown。写稳定 ID、唯一精确 source、`source_hash_version: portable-v1`、group、类型/时点、内容特异的一句话、至少两个特异要点、版本关系与复核边界；manifest 恰有一个 `distillation-file:<group>/<file>.md` 主输出。生成一份就立即运行 `check --gate G4 --source <精确路径>`，通过后再处理下一份。
- **通过条件**：完整 G3 后完成全 collection G4；逐份检查全部通过，批次再验 distilled rows、独立结果和 exact sources 三集合一一对应、零孤儿、零复用。summary 不能满足 distilled 输出。
- **失败回退**：模板空话、事实概括或 source 内容错只返工当前文件；path/identity/group/台账错必须回 G1/G2/G3，并顺序重跑受影响下游。缺确认并不允许伪造结果或自动扩大范围。

新结果名为 `d-<source_hash12>-<ascii-slug>.md`。`source_hash12` 将精确 source 做 Unicode NFC、分隔符统一为 `/`，仅将 Windows 盘符字母大写，保持 POSIX 前导 `/` 和其余大小写，再取 UTF-8 SHA-256 前 12 位。正常新建或更新必须写 `source_hash_version: portable-v1` 并严格匹配文件名；只有显式只读 legacy 模式可接受未改旧结果缺字段。授权更新旧结果时必须迁成 portable-v1；若需要重命名却没有移动/删除授权，停止并报告，不能借 legacy 绕过。

### G5 项目或主题综合

- **输入**：G1 的 `path→group` 与 G4 已通过的本组独立结果。
- **动作**：多文件确有跨文件事实、技术结论或版本脉络时，复制 [项目综合模板](assets/project-summary-template.md)；只写跨文件综合、版本关系、限制和本组每个独立结果的链接，不内嵌逐文件正文。
- **通过条件**：没有独立结果的组不要求 summary；单结果或没有跨文件综合价值的组也可不建。机器默认全量校验所有已存在 summary 的 group、章节、完整链接和内容边界；只有任务契约明确要求每个多结果组综合时才运行 `check --gate G5 --require-summary`，且该选项只要求至少两个独立结果的组。
- **失败回退**：漏链、错链或用综合替代单文件结果时只返工 summary；发现 group/owner 上游错误则回 G1/G2 后重跑。

### G6 可复用知识或经验建议

- **输入**：已通过 G4/G5 的文件级与跨文件结论，以及用户是否明确要求进一步保存。
- **动作**：只识别跨项目稳定事实、方法、条件、失败模式或护栏，报告“可另行保存为知识/经验”的具体建议。本流程不直接创建、纠正或归档这些条目；同一请求明确要求保存时，也必须先完成适用文件阶段，且后续记录的来源仍回到原始文件，不能以 summary 代替。
- **通过条件**：没有为了凑数量复制项目专属或易变信息；建议已给出原文件依据、适用边界与去重提醒。
- **失败回退**：证据不足、敏感或只在单项目成立时不建议保存；不确定时不写。

### G7 最终回归与交付

- **输入**：所有已通过阶段的范围、台账、结果、summary 和人工质量检查记录。
- **动作**：运行 `check --gate G7`；再全量人工检查内容特异性、事实忠实度、价值、脱敏和长原文风险。核对 expected/actual/diff、编码、敏感扫描、跨 collection owner 和 summary 链接。
- **通过条件**：集合差异、重复、孤儿、source/group 错配、漏链、安全或编码硬失败的 actual 均为 0；只有 manifest 已闭合且 reason 具体的合法 skip 可解释。结构、内容和用户范围全部通过。
- **失败回退**：任一硬断言失败都不得声称完成；运行 `explain <code>`，回到最早受影响阶段，修后顺序重跑下游。部分成功可交付已验证成果，但必须列明未完成范围。

面向用户先说“共 X 个文件，整理 Y 个，跳过 Z 个，剩余 N 个”，随后给重要结果与下一步。G、code、expected/actual、source_hash12、owner 等只放需要时的技术核验明细，不要求用户理解。

## Tools and data sources

- 原始事实来自用户指定的只读文件、文件现场元数据及必要时的当前运行现场；索引、摘要和历史提取不能覆盖原文件。
- 本流程写入 `~/.agent-knowledge/README.md` 与 `indexes/` 下自己拥有的导航、台账、独立结果和综合；不写知识/经验生命周期目录，不修改原文件。
- 优先使用宿主原生文件 API、固定字符串搜索、CSV/Markdown 安全解析和适合文件格式的只读解析器；不硬依赖 Git、特定搜索命令、PowerShell、网络、服务或数据库。
- 随包 `scripts/validate_collection.py` 是标准库只读校验器。先用 `describe` 查看机器契约；阶段用 `check --collection <目录> --gate G2|G3|G4|G5|G7`，单文件加 `--source <精确路径>`，失败用 `explain <code>`，安装后用 `self-test`。仅对未改旧集合的显式只读核验可加 `--legacy-read-only`；新建或更新不能使用。只有任务契约要求所有多结果组综合时才加 `--require-summary`。工具不可用时按相同契约人工/宿主解析并明确机械校验未运行。

## Gotchas

- 原始读取和提取是证词，不能因失败信息而被改写；校验器只读且不能自动修复。结构 PASS 不证明正文事实、价值、时点或脱敏正确。
- 敏感内容、凭据、隐私、精确基础设施值、合同金额和长原文不进入索引正文或结果；读取最少必要信息，无法安全处理就逐件说明。
- collection 不保存全文副本、OCR 缓存、向量库、专属脚本，不运行后台同步；临时抽取只在受控临时区并按授权清理。
- 文件名、路径、mtime、模板句、项目综合和“历史已处理”状态都不能冒充内容。不同路径的全文重复版本仍各有独立结果或逐件合法 skip，并说明版本关系。
- 校验器校验单一 collection 内部结构；跨 collection 唯一 owner、外部 summary 关系、事实真伪与敏感判断必须在对应阶段用宿主解析和人工检查完成。
