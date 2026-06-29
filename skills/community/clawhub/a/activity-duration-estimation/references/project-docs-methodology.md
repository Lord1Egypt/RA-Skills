# 项目文档生成（:project-docs）— 方法论文档

> 本文件说明:project-docs 子技能的双模式设计、模板结构、操作流程和使用规范。

---

## 一、概述

:project-docs 是 activity-duration-estimation 技能的第三个子技能，提供**项目文档生成**能力。

### 与其他子技能的关系

| 子技能 | 输入 | 输出 | 关联 |
|--------|------|------|------|
| `:estimation` | OMP值+紧前关系 | 估算报告+CPM+甘特图 | 向:project-docs 提供估算数据 |
| `:wbs` | 模糊需求 | WBS树+工作包列表 | 向:project-docs 提供范围依据 |
| `:project-docs` | 项目资料+模板 | 项目文档 | 消费以上两个子技能的产出 |

### 核心原则

1. **模板即数据不消耗token** — 模板定义为纯JSON，预置在`references/templates/`中
2. **双模式可选** — 手动模式输出空结构，自动模式逐节生成
3. **逐节确认不可跳过（自动模式）** — 每节独立LLM调用，质量一致
4. **输出为Markdown** — 最低公分母格式，用户可直接使用或转换

---

## 二、双模式设计

### 手动模式（Manual Mode）

**适用场景**：
- 正式文档需要人工把关
- token预算有限
- 文档内容敏感性高
- 只需要结构参考

**流程**：
1. 用户指定文档类型（立项申请书/结项报告书/相关方登记册/风险登记册）
2. 系统加载模板JSON
3. 根据项目资料（WBS/估算/CPM）特化模板结构
4. 输出Markdown空模板，每节包含：
   - 章节标题和描述
   - 填充提示
   - 已有资料引用标记（✅ WBS分解 / ✅ CPM分析 / ✅ 估算结果）
   - 空内容占位
5. 用户手动填充，或单独调LLM填充某一节

**输出示例**：
```markdown
## 项目背景
> 说明项目的提出原因、当前业务痛点、市场机会

**可参考的已有资料**:
- ✅ WBS分解
- ✅ 语义分析

**填充提示**: 建议从以下几个方面描述：业务现状与痛点、外部环境变化、技术发展驱动

---

*（在此处填写内容）*

---
```

### 自动模式（Auto Mode）

**适用场景**：
- 快速出草稿
- 内容填充为主的工作
- 用于初稿后人工更新

**流程**：
1. 用户指定文档类型
2. 系统加载模板JSON并特化
3. 逐节生成：每节按mode处理
   - `auto` → 独立LLM调用生成完整内容
   - `outline` → 独立LLM调用生成概要思路
   - `manual` → 跳过，输出空占位
4. 每节生成后用户确认 → 进入下一节
5. 不满意某节时：只重生成该节（不浪费之前的工作）
6. 全部确认后拼合成完整文档

**上下文控制**：
- 每节只带入上一节的摘要（~100字），不是全文
- 避免上下文累积导致的注意力衰减
- 保证每节生成质量一致

---

## 三、模板定义规范

### 文件位置

```
references/templates/
├── 立项申请书.json
├── 结项报告书.json
├── 相关方登记册.json
├── 风险登记册.json
└── （更多模板可添加）
```

### JSON结构

每个模板JSON包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 模板名称 |
| `description` | string | 模板说明 |
| `version` | string | 版本号 |
| `output_filename` | string | 输出文件名（支持`{project_name}`占位符） |
| `sections` | array | 章节定义列表 |
| `appendix` | array | 附录列表 |

### 章节类型（section.type）

| 类型 | 说明 | 手动模式输出 | 自动模式行为 |
|------|------|-------------|-------------|
| `rich_text` | 富文本段落 | 空占位+提示 | LLM生成自然语言段落 |
| `fields` | 键值字段表 | 字段名+空值行 | LLM生成一行一值 |
| `table` | 表格 | 表头+空行 | LLM填充各行 |
| `wbs_attachment` | WBS附件引用 | 输出WBS文本树 | 输出WBS文本树（不生成） |

### 引用源（section.reference_sources）

标记本节点可能引用哪些已有资料：

| 引用源 | 来源 | 说明 |
|--------|------|------|
| `wbs_tree` | :wbs 输出 | WBS文本树结构 |
| `wbs_json` | :wbs 输出 | WBS字典JSON |
| `wbs_work_packages` | :wbs 输出 | 工作包列表 |
| `wbs_scope` | :wbs 输出 | 范围描述 |
| `cpm_result` | :estimation 输出 | CPM关键路径结果 |
| `estimation_result` | :estimation 输出 | 历时估算结果 |
| `semantic_analysis` | :estimation Phase 0 | 语义分析结果 |
| `risk_register` | 本文档 | 风险登记册（另一模板） |
| `stakeholder_register` | 本文档 | 相关方登记册（另一模板） |

---

## 四、模板定制（增/删/改/排序 + 另存）

> `scripts/project_docs_engine.py` 第8节

模板不是死的。用户可以在生成前定制模板结构，也可以将定制结果另存为永久模板。

### 支持的定制操作

| 操作 | 说明 | 示例 |
|------|------|------|
| **删除章节** | 按key或标题删除不需要的节 | `remove_section(tpl, "预算估算")` |
| **新增章节** | 在指定位置后/前插入新节 | `add_section(tpl, {...}, after_key="范围与交付物")` |
| **重排顺序** | 按指定的key顺序重排所有节 | `reorder_sections(tpl, ["key1","key2",...])` |
| **重命名** | 改章节标题或key | `rename_section(tpl, "旧标题", new_title="新标题")` |
| **批量操作** | 一次执行多个操作 | `customize_sections(tpl, [op1, op2, ...])` |
| **另存为新模板** | 将定制结果保存为新JSON模板 | `save_template(tpl, "我的模板名")` |

### 操作流程

```
1. 用户说"删除预算，加一个数据迁移章节"
2. LLM解析意图 → 调用 customize_sections()
3. 展示更新后的模板结构供确认
4. 用户可选"另存为'我的立项模板'" → 保存到 references/templates/
5. 之后可直接用"我的立项模板"生成文档
```

### 自定义章节模板

新增的章节支持所有预置类型：

```json
{
  "key": "custom_section",        // 唯一标识
  "title": "自定义章节标题",
  "type": "rich_text",            // rich_text / fields / table
  "description": "章节描述",
  "hint": "填充提示",
  "reference_sources": [],        // 可引用的资料源
  // table类型额外：
  "columns": ["列1", "列2"],
  "rows": 3,
  // fields类型额外：
  "fields": [{"key": "f1", "label": "字段1", "type": "text", "hint": ""}]
}
```

### 调用接口汇总

```python
# LLM可直接调用的函数（所有函数都在 project_docs_engine 中）
add_section(template, new_section, after_key=None, before_key=None)
remove_section(template, target_key_or_title)
reorder_sections(template, ordered_keys)
rename_section(template, target, new_title=None, new_key=None)
set_section_mode(template, target, mode)            # 设章节模式 auto/manual/outline
customize_sections(template, operations)             # 批量（含 set_mode 操作）
save_template(template, new_name, overwrite=False)   # 另存
delete_template(template_name)                       # 删除已保存的自定义模板
list_sections_by_mode(template)                      # 按模式分组
assemble_mixed_document(template, project, filled_sections)  # 按模式混合组装
get_template_structure_summary(template_name)         # 预览章节结构（含模式）
get_template_mode_summary(template_name)              # 只看模式分配
```

---

## 五、章节模式（auto / manual / outline）

每个章节可以独立指定模式，模式固化在模板JSON中，下次直接调用无需重新配置。

### 三种模式对比

| 模式 | 输出 | token消耗 | 适用场景 | 用户操作 |
|------|------|----------|---------|---------|
| `auto` | LLM生成完整段落（300-800字） | 中 | 内容熟悉的章节 | 确认即可 |
| `outline` | LLM生成概要思路（2-5条要点） | 低 | 需要方向但不需完整内容的章节 | 在思路上扩展 |
| `manual` | 空占位 + 填充提示 | ≈0 | 需要人工把关的章节 | 手动填写 |

### 使用示例

```text
# 创建带模式的模板
用户："帮我把立项申请书存为公司模板，项目背景和目标自动生成，
       预算估算手动填，范围与交付物写个思路概要"
→ 加载立项申请书
→ set_section_mode("项目背景", "auto")
→ set_section_mode("项目目标", "auto")
→ set_section_mode("预算估算", "manual")
→ set_section_mode("范围与交付物", "outline")
→ save_template(tpl, "公司立项模板")

# 下次直接调用
用户："用公司立项模板"
→ 读取模板章节模式
→ 自动节: LLM生成内容
→ 概要节: LLM生成思路
→ 手动节: 输出空占位
→ 混合组装输出
```

---

## 六、思维工具参考（质量提升）

> 详见 `references/thinking-tools.md`（12个完整工具的详细说明和示例）

生成各章节内容时，可参考以下思维工具来组织材料，保证内容的结构完整性和说服力：

| 章节 | 推荐工具 | 作用 |
|------|---------|------|
| 项目背景 | SWOT / 5W2H | 结构化分析内外部环境和项目必要性 |
| 项目目标 | SMART | 确保目标可衡量、可追踪 |
| 范围与交付物 | MoSCoW / 思维导图 / Top-down+Bottoms-up | 清晰划分优先级，避免范围蔓延 |
| 工作分解 (WBS) | 思维导图 / Top-down+Bottoms-up | 双重验证确保分解完整 |
| 进度计划 | 甘特图 / CPM（已有） | 识别关键路径 |
| 资源需求 | RACI | 明确各角色权责 |
| 风险评估 | Pareto / 概率-影响矩阵 / 头脑风暴 | 找到关键20%风险 |
| 相关方分析 | RACI / SWOT | 识别并分类相关方 |
| 经验教训 | PDCA / 鱼骨图 | 根因分析而非表面归因 |
| 需求排序 | MoSCoW / Pareto | 识别Must vs Nice-to-have |

**使用方式**: LLM 在生成对应章节时，先查阅 `thinking-tools.md` 中对应工具的说明和示例，按框架结构组织输出内容。每个工具都有完整的结构化示例可直接参考。

---

## 五、操作指引

### 快速开始

```text
场景1：手动模式
用户："帮我针对电商后台项目生成一份立项申请书的空模板，手动模式"
→ 系统加载模板→特化（填入WBS/CPM引用）→输出空模板MD
→ 用户拿MD手动填充，或单独调LLM填充特定章节

场景2：自动模式
用户："帮我生成结项报告书，自动模式，从项目概况开始"
→ 逐节生成→每节用户确认→拼合完整文档
→ 第4节进度对比不满意→只重算第4节

场景3：混用
用户："先手动模式出结构，然后帮我自动填充第1节和第3节"
→ 先出空模板→用户看了结构→单独生成指定节→拼入

场景4：模板定制
用户："立项申请书帮我改一下，删除预算章节，在范围后面加一个数据迁移章节"
→ LLM: customize_sections(template, [
  {"action": "remove", "target": "预算估算"},
  {"action": "add", "after": "范围与交付物", "section": {
    "key": "data_migration", "title": "数据迁移方案",
    "type": "rich_text",
    "description": "数据迁移的范围、方案与计划"
  }}
])
→ 然后另存为新模板"我的立项模板"
→ 后续可直接用"我的立项模板"生成文档

场景5：模板重排+重命名+另存
用户："把审批放到最前面，项目背景改名'业务分析'，存为'精简立项模板'"
→ 重排+重命名 → save_template(template, "精简立项模板")
```

### 六、可用模板列表

| 模板 | 章节数 | 推荐场景 |
|------|--------|---------|
| `立项申请书` | 11节 | 项目启动时 |
| `结项报告书` | 10节 | 项目结束时 |
| `相关方登记册` | 4节 | 项目规划阶段 |
| `风险登记册` | 5节 | 项目全周期 |
| 自定义模板 | 可变 | 用户通过定制+另存添加 |

---

## 八、限制与边界

| 维度 | 说明 |
|------|------|
| 模板数量 | 预置4个P0模板，用户可通过定制+另存添加任意数量自定义模板 |
| 模板定制 | 支持增/删/改/重排章节，自定义章节与预置章节功能完全一致 |
| 文档长度 | 手动模式≈0消耗，自动模式每节约300-800字，建议不超过20节 |
| 自动模式 | 逐节生成需用户逐节确认，不可跳过。不满意时只重算该节 |
| 上下文 | 每节只带入前一节摘要（~100字），不累积全文上下文 |
| 格式 | 仅支持MD输出。用户可自行转HTML/PDF/DOCX |
| 模板依赖 | 依赖:wbs和:estimation的产出物。无产出时模板的填充提示不准确 |

---

## 九、反模式

- **依赖自动模式生成正式文档**：正式文档建议手动模式出结构后人工填充，自动模式适合草稿
- **一次性生成所有节**：必须逐节确认，跳过确认就是质量下降的根源
- **模板定义包含正文内容**：模板只定义结构（JSON），不包含正文。正文由用户或LLM填充
- **强行让LLM填写审批表格**：审批部分（签名/印章）保持空表，由实际审批流程完成
- **忽略WBS/估算引用**：手动模式下已有资料引用是核心价值，不应跳过
