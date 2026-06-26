---
name: cowhorse-skill
description: A skill that actively extracts and quantifies workflow requirements from users through structured Q&A about inputs, outputs, and objectives. Build reusable skills with scripts/references/assets. Use when user describes a task they want AI to help with repeatedly, e.g. "帮我做一个workflow", "建一个skill", "梳理流程", "帮我做一个工具", "把这个做成一个skill".
---

# 牛马Skill (CowHorseSkill)

主动询问用户的输入、输出和客观需求，通过迭代确认构建可复用的 workflow skill。

## Workflow

### Step 1: Discovery (初始需求挖掘)

When user describes a task they want AI to support, **actively lead the conversation** — don't wait for the user to volunteer details. Ask the following questions **one at a time**, wait for each answer before proceeding.

#### 1.1 Goal Clarification (目标澄清)
- 您最终要交付什么结果？
- "完成"的定义是什么？怎么算做好了？
- 这个工作流解决的核心问题是什么？

#### 1.2 Input Specification (输入规格)
每次必须问清楚以下所有维度：

| 维度 | 必问问题 |
|------|---------|
| **数据来源** | 数据从哪来？文件、API、数据库、还是手动输入？ |
| **文件格式** | 是 .xlsx / .csv / .json / .txt / 其他？ |
| **文件位置** | 文件在哪？本地路径、网盘、飞书文档？ |
| **数据结构** | 数据长什么样？有哪些列/字段？有表头吗？ |
| **数据量** | 大概多少条/多少文件？ |
| **数据质量** | 有脏数据吗？缺失值、格式不一致怎么处理？ |
| **参数** | 需要用户传入什么参数？（筛选条件、时间范围、阈值等） |

**追问策略：** 如果用户说"一个Excel"，必须追问：
- 里面有哪些 sheet？
- 每个 sheet 的表头是什么？
- 有没有合并单元格？
- 大概多少行数据？

#### 1.3 Output Specification (输出规格)
每次必须问清楚以下所有维度：

| 维度 | 必问问题 |
|------|---------|
| **产出形式** | 输出是文件、表格、图表、报告、还是直接执行动作？ |
| **文件格式** | 输出什么格式？.xlsx / .pdf / .html / .png / 控制台打印？ |
| **输出位置** | 输出到哪里？本地路径、飞书文档、邮件发送？ |
| **输出内容** | 具体包含哪些信息？汇总数据、明细、统计指标？ |
| **输出格式要求** | 有模板吗？需要特定排版、颜色、公式吗？ |
| **输出粒度** | 是汇总还是明细？按什么维度分组？ |

**追问策略：** 如果用户说"生成一个报表"，必须追问：
- 报表里具体要哪些字段？
- 需要排序吗？按什么排？
- 需要筛选/过滤吗？条件是什么？
- 需要统计计算吗？（求和、平均、计数等）

#### 1.4 Process Steps (流程步骤)
- 整个流程分几步？每一步做什么？
- 哪些步骤是手动的？哪些需要自动化？
- 步骤之间有依赖关系吗？顺序能变吗？

#### 1.5 Constraints (约束条件)
- 有什么时间要求？（定时执行、截止日期）
- 有什么技术限制？（必须用某个工具、不能联网等）
- 有什么业务规则？（特殊计算方式、例外情况）
- 有什么性能要求？（处理速度、数据量上限）

**核心原则：不假设，不猜测，不确定就问。**

**处理用户输入时：**
- 接受中英文拼写错误
- 项目名/表单名允许模糊匹配
- 不确定时问用户确认，不要假设

### Step 2: Confirmation (需求确认)

After initial discovery, present a structured summary. **每个维度必须明确，不能留"待定"。**

```
## 工作流需求确认

### 目标
[用户描述的目标 — 一句话概括]

### 输入规格
| 项目 | 详情 |
|------|------|
| 数据来源 | [文件路径 / API / 手动输入] |
| 文件格式 | [.xlsx / .csv / .json 等] |
| 数据结构 | [表头列名、数据类型] |
| 数据量 | [行数/文件数] |
| 输入参数 | [筛选条件、时间范围等] |
| 脏数据处理 | [缺失值/异常值策略] |

### 输出规格
| 项目 | 详情 |
|------|------|
| 产出形式 | [文件 / 报表 / 图表 / 动作] |
| 输出格式 | [.xlsx / .pdf / 控制台 等] |
| 输出位置 | [本地路径 / 飞书 / 邮件] |
| 输出内容 | [包含的字段/信息] |
| 排序/筛选 | [排序字段、筛选条件] |
| 统计计算 | [求和、平均、计数等] |
| 格式要求 | [模板、颜色、公式] |

### 流程步骤
1. [步骤1 — 明确输入→输出]
2. [步骤2]
...

### 约束条件
- [约束1]
- [约束2]

### 确认问题
1. 以上输入/输出规格是否正确？
2. 步骤顺序和依赖关系对吗？
3. 哪些步骤需要自动化，哪些保留手动？
4. 有遗漏的字段或规则吗？
```

Wait for user confirmation. Iterate until user says "确认" or "可以".

### Step 3: Build (构建Skill)

Once confirmed, build the skill:

1. **Create skill directory** using `scripts/init_skill.py` from skill-creator
2. **Write SKILL.md** with:
   - Frontmatter: name, description (triggers + when to use)
   - Body: Complete workflow instructions, all steps, decision trees
3. **Add scripts** if automation is needed:
   - Python scripts for data processing, file operations, etc.
   - Shell scripts for system commands
4. **Add references** if domain knowledge is needed:
   - Schemas, API docs, business rules, templates
5. **Add assets** if output files are needed:
   - Templates, boilerplate, sample data

**Skill structure:**
```
skill-name/
├── SKILL.md (required)
├── scripts/ (optional)
│   ├── main_script.py
│   └── helpers.py
├── references/ (optional)
│   └── workflow_guide.md
└── assets/ (optional)
    └── template.xlsx
```

### Step 4: Present and Validate (呈现确认)

After building:

1. **Show the skill structure** - List all files created
2. **Show SKILL.md summary** - Key sections and triggers
3. **Test the skill** - Run a sample execution if possible
4. **Ask for feedback** - Does this match what you need?
5. **Iterate** - Update based on feedback

### Step 5: Finalize (完成)

1. **Package the skill** using `scripts/package_skill.py` from skill-creator
2. **Update MEMORY.md** with the new skill info
3. **Notify user** - Skill is ready for use

## Fuzzy Matching Rules

When processing user input for names, paths, or identifiers:

1. **Trim whitespace** and normalize case
2. **Strip punctuation** from start/end
3. **Allow partial matches** for long strings (e.g., "孝感中心" matches "孝感中心医院东城院区")
4. **Handle common typos** for known values (e.g., "受理单" vs "受理单据")
5. **When uncertain, ask** - "您是指 X 还是 Y？"

## Error Handling

- If a step fails, report the error clearly
- Do not silently skip failed steps
- Ask user how to proceed
- Keep a log of what was done for debugging

## Resources

### scripts/
- `scripts/init_skill.py` - From skill-creator, initialize new skill
- `scripts/package_skill.py` - From skill-creator, package skill to .skill
- Add custom scripts as needed for the specific workflow

### references/
- `references/workflow_guide.md` - Detailed workflow patterns and examples
- Add domain-specific references as needed

### assets/
- Add templates, boilerplate, or sample data as needed
