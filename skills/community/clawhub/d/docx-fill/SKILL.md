---
name: docx-fill
description: Generate Word documents by filling templates with content based on reference materials. Use this skill whenever the user provides a .docx template (or asks to fill a Word document) along with reference materials and wants the content written into the template with original styles preserved. Specialized for table-heavy templates like project proposals, lesson plans, curriculum standards, course outlines, and reports. Trigger this skill even if the user doesn't explicitly say "fill template" — any request to write content into a structured Word document, generate a report from a template, or produce a formatted .docx from source materials should invoke it.
compatibility:
  - Claude Code
  - Cursor
  - Codex
  - Gemini CLI
  - WorkBuddy
  - OpenClaw
---

# docx-fill

以模板锚定填充（Template-Anchored Fill）方式生成 Word 文档：识别模板中的占位符与约束，依据参考资料撰写内容，填回模板对应位置，样式自动保留。尤其擅长处理表格密集型模板（项目申报书、教案、课程标准、报表等整个文档由表格构成的场景）。

## 触发条件

当用户同时提供以下两项时触发：
1. **模板文件**：`.docx` 文件路径，其中含占位符提示文字（如「请填写XXX」「本部分需依据XXX」）或需填充的空白表格单元格
2. **参考资料**：用于填充的内容来源（文本、文档、数据等）

典型场景：
- 项目申报书填写（整篇文档由多层级表格构成）
- 教案撰写（含课程信息表、教学过程表）
- 课程标准生成（含学时分配表、考核标准表）
- 定期报表生成（含数据汇总表、统计表）
- 课程总结报告（含结构化章节与表格）

## 输入要求

- `template_path`：模板的绝对路径
- `reference_materials`：参考资料（路径列表或直接文本）
- `output_path`：输出文档路径（可选，默认在模板同目录生成 `filled_<原文件名>.docx`）

## 9 步执行流程

每步产出结构化 JSON，供后续步骤读取。中间产物由宿主智能体自行存储管理。

### Step 1: 结构提取（代码）

调用脚本提取模板的原子结构与样式定义：

```bash
python3 scripts/extract_structure.py --template <template_path> --output <raw_structure.json>
python3 scripts/extract_styles.py --template <template_path> --output <style_defs.json>
```

**Why 代码先行**：模板结构是确定性的，用代码提取可保证零幻觉，避免 LLM 误读表格嵌套、合并单元格等复杂结构。`raw_structure.json` 包含段落、表格（含每个 cell 的行列索引与文本）、标题层级，是后续所有判断的事实基础。

### Step 2: 结构理解（LLM，角色 STRUCTURE_AGENT）

加载 `references/structure_agent.md`，输入 `raw_structure.json`，产出 `fill_contract.json`。

任务：识别占位符、抽取约束（仅来自模板原文显式文字）、输出 Fill Contract。

**Why 需要契约**：直接让 LLM 边读模板边写内容会混入推理过程，且约束隐式不可校验。Fill Contract 把约束显式化、结构化，后续角色只读契约不读推理，实现职责隔离。

详见 [references/fill_contract_schema.md](references/fill_contract_schema.md)。

### Step 3: 契约校验（代码，Tier 1+2）

```bash
python3 scripts/validate_contract.py --contract <fill_contract.json> --structure <raw_structure.json>
```

- 通过 → 进入 Step 4
- 未通过 → 宿主智能体按 `fix_hint` 修改契约后进入 Step 4（不重新评估）

**Why 单次评估**：避免无限循环。未通过的修改直接进入下一步，由后续校验点继续把关。

### Step 4: 冲突检测（LLM，角色 CONFLICT_CHECKER）

加载 `references/conflict_checker.md`，输入 `fill_contract.json` + 参考资料。

- 无冲突 → 进入 Step 5
- 有冲突 → 列出冲突选项，**对话等待用户选择**，用户选择写入 `fill_contract.json` 的 `conflicts` 字段后进入 Step 5

**Why 需要冲突检测**：参考资料间可能矛盾（如两份资料给出不同数据），由 LLM 主动暴露冲突交给用户决策，避免悄悄选一方。

### Step 5: 内容撰写（LLM，角色 CONTENT_AGENT）

加载 `references/content_agent.md`，输入 `fill_contract.json` + 参考资料，产出 `generated_content.json`。

按契约逐占位符生成内容。参考资料过长则先摘要（策略由宿主智能体决定）。

### Step 6: 内容校验（代码，Tier 1+2）

```bash
python3 scripts/validate_content.py --content <generated_content.json> --contract <fill_contract.json>
```

- 通过 → 进入 Step 7
- 未通过 → 宿主智能体按 `fix_hint` 修改内容后进入 Step 7

### Step 7: 内容自评（LLM，角色 EVALUATOR，Tier 3）

加载 `references/evaluator.md`，输入 `generated_content.json` + `fill_contract.json` + 参考资料。

切换为评估角色，**忽略撰写时的思路**，独立检查语义连贯性、专业度、幻觉。

- 通过 → 进入 Step 8
- 未通过 → 宿主智能体按 `fix_hint` 修改内容后进入 Step 8

### Step 8: 渲染（代码）

```bash
python3 scripts/render_document.py --template <template_path> --contract <fill_contract.json> --content <generated_content.json> --output <output_path>
```

用 python-docx 打开原始模板（保留所有样式），按 `contract.placeholders` 的 `location` 定位并替换文本，`static_texts` 原样保留，保存到 `output_path`。

### Step 9: 最终校验（代码，Tier 1）

```bash
python3 scripts/validate_format.py --generated <output_path> --template <template_path>
```

- 通过 → 交付用户
- 未通过 → 标记问题位置，提示用户

## 角色切换规则

单宿主智能体内通过 prompt 切换实现近似职责隔离。每个角色 prompt 明确声明：
- 当前角色是什么
- 应忽略什么（前序角色的推理过程）
- 只能依据什么（结构化产物 + 基准材料）
- 应输出什么（结构化 JSON）

**Fill Contract 是角色间唯一交接物**：结构理解角色产出契约后，后续角色只读契约 + 基准材料，不依赖前序推理。

| 角色 | 加载的 prompt | 输入 | 输出 |
|------|--------------|------|------|
| STRUCTURE_AGENT | references/structure_agent.md | raw_structure.json | fill_contract.json |
| CONFLICT_CHECKER | references/conflict_checker.md | fill_contract.json + 参考资料 | conflicts 报告 |
| CONTENT_AGENT | references/content_agent.md | fill_contract.json + 参考资料 | generated_content.json |
| EVALUATOR | references/evaluator.md | generated_content.json + 契约 + 参考资料 | 评估报告 |

## 硬约束规则

以下规则约束宿主智能体行为，违反将导致输出不可控：

1. **约束仅来自模板原文**：不自行生成约束，模板没有要求的不添加。LLM 不得推断发挥
2. **评估只评一次**：未通过则修改后直接进入下一步，不循环评估
3. **角色切换时必须忽略前序角色的推理过程**：只依据结构化产物 + 基准材料
4. **静态文本不可修改**：`is_static=true` 的文本渲染时原样保留
5. **代码校验优先于 LLM 评估**：Tier 1+2 失败则不触发 Tier 3
6. **Fill Contract 是角色间唯一交接物**：不传递推理过程

## 表格密集型模板的处理要点

项目申报书、教案等模板常出现「整篇文档由表格构成」的情况，处理时需特别注意：

- **嵌套表格**：`extract_structure.py` 会递归提取嵌套表格，`location` 字段含 `nested_table_index` 定位嵌套层
- **合并单元格**：脚本输出 `merged_cells` 列表，标识横向/纵向合并的单元格范围，撰写内容时按合并后的逻辑单元格处理
- **表格作为段落流的一部分**：表格在 `raw_structure.json` 中按文档顺序出现于 `body_order` 列表，与段落交错
- **表头单元格默认 `is_static=true`**：除非模板原文显式要求填写表头，否则表头不填充
- **跨单元格内容**：当一处内容要求跨多个单元格时（如"项目简介"占 3 行 1 列），契约中用 `span` 字段标记起始单元格，内容由 LLM 写入起始单元格后由脚本保留其余单元格的合并状态

## 资源索引

- Fill Contract 字段详情：[references/fill_contract_schema.md](references/fill_contract_schema.md)
- 评估规则详情：[references/evaluation_rules.md](references/evaluation_rules.md)
- 结构理解 prompt：[references/structure_agent.md](references/structure_agent.md)
- 内容撰写 prompt：[references/content_agent.md](references/content_agent.md)
- 评估 prompt：[references/evaluator.md](references/evaluator.md)
- 冲突检测 prompt：[references/conflict_checker.md](references/conflict_checker.md)
