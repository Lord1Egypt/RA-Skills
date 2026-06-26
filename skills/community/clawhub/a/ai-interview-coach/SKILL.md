---
name: ai-interview-coach
description: >-
  AI-powered interview preparation assistant with three difficulty levels (junior/mid/senior),
  flexible question count (5/10/15/20), five question types (knowledge, coding, system design,
  case study, behavioral), and interview history tracking with progress analysis and capability
  radar charts. Includes 7-day sprint plans, job readiness scoring, and answer rewriting for
  higher interview performance. Supports both document generation mode and interactive mock
  interview mode.
  Use when preparing for job interviews, practicing interview skills, conducting mock interviews,
  tracking progress, or when the user mentions "面试", "interview practice", "模拟面试", "面试题",
  "简历分析", "历史记录", "进步", "冲刺计划", "就绪度", "润色答案", or asks to generate interview questions.
---

# AI Interview Coach

Personalized interview preparation assistant that generates targeted questions based on resumes or job positions.

## Quick Start

当用户想要准备面试时，识别以下任意一种输入方式：

### 自然对话方式（推荐）

用户可以用自然的对话方式发起请求，系统自动识别难度和题量：

| 场景 | 示例输入 | 识别结果 |
|------|----------|----------|
| **提供简历** | "你好考官，这是我的简历：path/to/resume.pdf" | 难度：自动推断，题数：默认10题 |
| **经验描述** | "你好考官，我是3年经验的前端工程师" | 难度：中级，题数：默认10题 |
| **应届生** | "你好考官，我是应届生准备面试" | 难度：初级，题数：默认10题 |
| **资深专家** | "准备一下架构师面试，5年经验" | 难度：高级，题数：默认10题 |
| **指定题量** | "我想面试 AI 算法工程师，生成5道题" | 难度：自动推断，题数：5题 |
| **快速练习** | "来几道简单的题热热身" | 难度：初级，题数：默认5题 |
| **深度准备** | "系统准备一下，要20道题" | 难度：默认中级，题数：20题 |
| **明确指定** | "给我15道中级难度的后端题" | 难度：中级，题数：15题 |

### 处理流程

1. **识别用户意图和输入信息**（简历文件或职位描述）
2. **确定难度级别**（初级/中级/高级，或从用户描述推断）
3. **确定题目数量**（5/10/15/20题，或从用户描述推断）
4. **读取并分析简历内容**（如果提供）
5. **生成 N 道指定难度的面试题**
6. **输出格式化的 markdown 文档**（含难度标识、答题空格和参考答案）

## Input Handling

### Resume Files

Read different formats:

- **Markdown (.md)**: Read as text file directly
- **PDF (.pdf)**: Use PDF tool to extract text content
- **Word (.docx)**: Extract text content (typically contains readable text)

Extract key information:
- Technical skills and tools
- Work experience and projects
- Education background
- Achievements and highlights

**Infer difficulty from resume:**
- 应届生 / < 2年经验 → 初级 (junior)
- 2-5年经验 → 中级 (mid)
- > 5年 / 资深 / 架构师 / 专家 → 高级 (senior)

### Job Position Input

When user specifies a job role (e.g., "前端工程师", "产品经理"):
- Generate questions based on typical role requirements
- Cover common interview topics for that position
- Include role-specific technical and behavioral questions
- Use default difficulty (mid) unless specified

### Difficulty Detection

Parse user's natural language for difficulty hints:

| 关键词 | 判定难度 |
|--------|----------|
| 应届生、毕业生、新手、入门、初级 | 初级 (junior) |
| 1-2年、初级开发、初级工程师 | 初级 (junior) |
| 3-5年、中级、有经验 | 中级 (mid) |
| 5年以上、资深、专家、架构师、高级 | 高级 (senior) |
| 简单点、基础题、来点简单的 | 初级 (junior) |
| 深入点、难点、高级问题 | 高级 (senior) |

**示例：**
- "我是应届生，帮我准备前端面试" → 初级
- "来几道深入一点的算法题" → 高级
- "工作4年了，准备跳槽" → 中级（从年限推断）

### Question Count Detection

Parse user's natural language for question count:

| 关键词 | 判定题数 |
|--------|----------|
| 几道题、几道、少量 | 5题 |
| 快速练习、热身、简单练 | 5题 |
| 10道题、标准、常规 | 10题 |
| 15道题、系统准备、深度 | 15题 |
| 20道题、全面、完整 | 20题 |
| 具体数字（如"8道题"） | 使用该数字 |

**示例：**
- "给我5道题" → 5题
- "来几道简单的热热身" → 5题
- "系统准备一下，全面一点" → 20题
- "生成12道题" → 12题（支持任意数量）

**Explicit Prompts:**
如果用户没有明确指定，主动询问：
- "需要多少道题？快速(5题)、标准(10题)、深度(15题)、全面(20题)"
- "请选择难度：初级(junior)、中级(mid)、高级(senior)"

## Question Generation Guidelines

Generate N questions (as determined by user) at specified difficulty level:

### Distribution by Question Count

| 题数 | 技术知识 | 项目经验 | 问题解决 | 行为面试 |
|------|----------|----------|----------|----------|
| **5题** | 1-2题 | 1题 | 1题 | 1题 |
| **10题** | 2-3题 | 2-3题 | 2题 | 2-3题 |
| **15题** | 4-4题 | 4题 | 3题 | 3-4题 |
| **20题** | 5-6题 | 5-6题 | 4题 | 4-5题 |

### Difficulty-Specific Guidelines

#### 初级 (Junior) - 适合应届生、1-2年经验

**技术知识题：**
- 问"是什么"、"有什么作用"
- 考察基础概念和常用API
- 避免原理深挖和源码分析

**项目经验题：**
- 问"你做了什么"、"用了什么技术"
- 关注具体实现和基础功能

**问题解决题：**
- 常见错误排查（如404、跨域、样式问题）
- 标准解决方案（如防抖节流、表单验证）

**行为面试题：**
- 团队协作基础场景
- 学习和成长经历

#### 中级 (Mid) - 适合3-5年经验

**技术知识题：**
- 问"为什么"、"原理是什么"
- 考察机制理解（如Event Loop、Diff算法）
- 方案对比和选型（如React vs Vue）

**项目经验题：**
- 问"为什么这样设计"、"遇到过什么挑战"
- 技术选型的权衡考量
- 性能优化和工程化实践

**问题解决题：**
- 复杂场景分析（如大数据量渲染、内存泄漏）
- 技术方案设计（如权限系统、数据同步）

**行为面试题：**
- 冲突解决和团队协作
- 技术影响力（如code review、知识分享）

#### 高级 (Senior) - 适合5年以上/专家/架构师

**技术知识题：**
- 问"源码如何实现"、"设计思想是什么"
- 框架/库的内部机制
- 底层原理（如V8引擎、操作系统、网络协议）

**项目经验题：**
- 问"如果重新设计会怎么做"
- 架构演进和技术债务处理
- 团队技术决策和长期规划

**问题解决题：**
- 系统性难题（如高并发、分布式一致性）
- 设计完整的技术方案（含容错、监控、扩展性）
- 疑难问题排查和根因分析

**行为面试题：**
- 技术决策和风险管理
- 培养团队和推动技术文化
- 跨团队协作和影响力

### Question Characteristics

All questions should:
- Be specific and relevant to input (resume or job role)
- Match the specified difficulty level in depth and scope
- Mix question types (see Question Types below)
- Include "参考答案" that match the difficulty level's depth

## Question Types

Generate diverse question types to match real interview scenarios. Each type has a specific output format.

### Type 1: Knowledge-Based (问答型)

**Purpose**: Assess depth of technical knowledge
**Format**: Open-ended theoretical questions
**Example**: "Explain how React's Virtual DOM works and its advantages"

**Output Format:**
```markdown
### 第X题 (问答型)
[Question text]

---

（请在此作答）



---
```

### Type 2: Coding/Algorithm (编程题)

**Purpose**: Assess coding ability and problem-solving
**Format**: LeetCode-style problems with requirements
**Example**: "Implement a function to find the kth largest element in an array"

**Output Format:**
```markdown
### 第X题 (编程题)
**题目**: [Problem description]

**要求**:
- 时间复杂度: [e.g., O(n log n)]
- 空间复杂度: [e.g., O(1)]
- 请用 [Language if specified, otherwise any] 实现

**示例**:
```
输入: [example input]
输出: [example output]
```

---

**请在此处编写你的代码**:

```



```

---

**参考答案**:
```[language]
[Reference implementation with comments]
```

**复杂度分析**:
- 时间: O(?)
- 空间: O(?)

**解题思路**:
1. [Key insight 1]
2. [Key insight 2]
3. [Key insight 3]
```

### Type 3: System Design (系统设计题)

**Purpose**: Assess architecture and large-scale system design skills
**Format**: Design problems requiring diagrams and explanations
**Example**: "Design a URL shortening service like bit.ly"

**Output Format:**
```markdown
### 第X题 (系统设计)
**场景**: [System to design, e.g., "设计一个微博系统"]

**需求**:
- 功能需求: [List functional requirements]
- 非功能需求: [QPS, latency, availability, etc.]
- 约束条件: [Constraints]

---

**请设计系统架构**（可以画图+文字说明）:

[用户在此处作答，建议包含：]
- 系统架构图描述
- 核心组件设计
- 数据模型设计
- 关键算法/策略



---

**参考答案**:

**系统架构**:
```
[ASCII diagram or component list]
```

**核心设计要点**:
1. [Design decision 1 with rationale]
2. [Design decision 2 with rationale]
3. [Design decision 3 with rationale]

**关键问题处理**:
- [Problem 1]: [Solution]
- [Problem 2]: [Solution]

**扩展性考虑**:
- [Scalability point 1]
- [Scalability point 2]
```

### Type 4: Case Study/Scenario (案例分析)

**Purpose**: Assess product thinking and business analysis (especially for PMs)
**Format**: Real-world business scenarios requiring analysis and solutions
**Example**: "User retention drops by 20% in month 3. How would you investigate and solve this?"

**Output Format:**
```markdown
### 第X题 (案例分析)
**背景**: [Scenario description]

**问题**: [Specific problem to solve]

**要求**:
1. 分析问题根本原因
2. 提出至少3个解决方案
3. 评估各方案的优缺点
4. 给出最终推荐及理由

---

**请分析此案例**:

[用户在此处作答]



---

**参考答案**:

**问题分析框架**:
[结构化分析方法, e.g., HEART framework for product metrics]

**根本原因**:
1. [Root cause 1 with evidence]
2. [Root cause 2 with evidence]

**解决方案对比**:

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| A | ... | ... | ... |
| B | ... | ... | ... |
| C | ... | ... | ... |

**推荐方案**: [Solution X]
**理由**: [Why this solution best fits the scenario]
```

### Type 5: Behavioral (行为面试)

**Purpose**: Assess soft skills, teamwork, and cultural fit using STAR method
**Format**: Situational questions about past experiences
**Example**: "Describe a time you had a conflict with a teammate. How did you resolve it?"

**Output Format:**
```markdown
### 第X题 (行为面试)
**问题**: [Behavioral question]

**建议回答框架** (STAR法则):
- **S**ituation: 描述背景
- **T**ask: 你的任务/目标
- **A**ction: 你采取的具体行动
- **R**esult: 最终结果，最好有量化指标

---

**请用STAR法则回答**:

Situation:

Task:

Action:

Result:


---

**参考答案**:

**考察点**: [What interviewer is looking for, e.g., conflict resolution, leadership]

**STAR示例**:
- **S**: [Example situation]
- **T**: [Example task]
- **A**: [Example action with details]
- **R**: [Example result with metrics]

**答题要点**:
1. [Key point 1]
2. [Key point 2]
3. [Key point 3]

**常见错误**:
- [Mistake to avoid 1]
- [Mistake to avoid 2]
```

### Question Type Distribution by Role

Adjust type distribution based on job role:

| 职位类型 | 问答型 | 编程题 | 系统设计 | 案例分析 | 行为面试 |
|----------|--------|--------|----------|----------|----------|
| **前端/后端开发** | 30% | 30% | 20% | 0% | 20% |
| **算法工程师** | 20% | 50% | 10% | 0% | 20% |
| **产品经理** | 20% | 0% | 0% | 40% | 40% |
| **全栈/架构师** | 25% | 25% | 30% | 0% | 20% |
| **运维/DevOps** | 35% | 20% | 25% | 10% | 10% |

**Special Instructions:**
- **Coding questions**: Only for technical roles; skip for PMs and non-technical positions
- **System design**: Mid-Senior level only; replace with "方案设计" for junior
- **Case study**: Primarily for PMs, but can include for senior technical roles (technical case studies)
- **Behavioral**: Always include for all levels and roles

### Detecting Question Type Preference

Users may explicitly request certain question types:

| User Input | Detected Preference |
|------------|---------------------|
| "来点算法题" / "coding" | Increase Coding type to 50%+ |
| "系统设计题" / "system design" | Increase System Design type to 40%+ |
| "行为面试" / "BQ" / "soft skills" | Increase Behavioral to 50%+ |
| "产品分析" / "case study" | Increase Case Study to 50%+ |
| "八股文" / "基础知识" | Increase Knowledge-Based to 60%+ |

## Output Format

Use this exact structure, dynamically generating N questions based on selected count:

```markdown
# 面试练习题 - [Job Title/Resume Focus] ([Difficulty] · [N]题)

> Generated on: [Date]
> Source: [Resume filename OR Job position]
> Difficulty: [初级/中级/高级]
> Questions: [N]题

---

## 答题说明

1. 请在每道题下方的空白处写下你的答案
2. 完成后对照文档末尾的参考答案进行自我评估
3. **建议用时**：[根据题数计算，5题=15分钟, 10题=30分钟, 15题=45分钟, 20题=60分钟]

---

## 面试题目

### 第1题 ([Question Type])
[Question text here - adjusted for difficulty level]

---

（请在此作答）



---

### 第2题 ([Question Type])
[Question text here - adjusted for difficulty level]

---

（请在此作答）



---

[Continue pattern through question N]

---

## 参考答案

### 第1题答案

**难度**: [初级/中级/高级]

**题型**: [技术知识/项目经验/问题解决/行为面试]

**考察点**: [Key skills/knowledge being tested - adjusted for difficulty]

**参考答案**:
[Detailed reference answer with key points - depth varies by difficulty]

**答题建议**:
- Key point 1
- Key point 2
- Key point 3

---

### 第2题答案

**难度**: [初级/中级/高级]

**题型**: [技术知识/项目经验/问题解决/行为面试]

**考察点**: [Key skills/knowledge being tested - adjusted for difficulty]

**参考答案**:
[Detailed reference answer with key points - depth varies by difficulty]

**答题建议**:
- Key point 1
- Key point 2
- Key point 3

---

[Continue pattern through question N]
```

**难度差异化示例：**

| 考察点 | 初级版本 | 中级版本 | 高级版本 |
|--------|----------|----------|----------|
| React useEffect | "简述useEffect的作用和基本用法" | "useEffect的依赖数组原理，如何避免闭包陷阱" | "useEffect源码实现，与useLayoutEffect的区别及选择策略" |
| 浏览器缓存 | "HTTP缓存有哪些类型" | "Cache-Control各指令的区别，协商缓存实现" | "设计一个多级缓存架构，处理缓存穿透/雪崩/击穿" |
| 项目难点 | "描述你遇到的一个技术问题" | "如何排查和解决性能瓶颈，用了哪些工具" | "设计一个通用的性能监控和自动降级方案" |

## Difficulty Levels

Support three difficulty levels to match user's experience:

| 难度 | 英文标识 | 适用对象 | 题目特点 |
|------|----------|----------|----------|
| **初级** | `junior` | 应届生、1-2年经验 | 基础概念、常见场景、标准八股 |
| **中级** | `mid` | 3-5年经验 | 原理深挖、方案对比、实际应用 |
| **高级** | `senior` | 5年以上/专家 | 架构设计、源码分析、疑难排查 |

**难度判定规则：**
1. 用户明确指定（如"来几道中级难度的题"）
2. 从简历推断（根据工作年限）
3. 默认为中级（`mid`）

**题目难度调整：**
- **初级**：问"是什么"、"怎么用"，避免深入原理
- **中级**：问"为什么"、"原理是什么"、"如何优化"
- **高级**：问"如何设计"、"源码如何实现的"、"遇到XX问题怎么解决"

## Question Count Options

Flexible question count to fit different time budgets:

| 模式 | 题数 | 建议用时 | 适用场景 |
|------|------|----------|----------|
| **快速** | 5题 | 15分钟 | 碎片时间自测 |
| **标准** | 10题 | 30分钟 | 常规练习 |
| **深度** | 15题 | 45分钟 | 系统性复习 |
| **全面** | 20题 | 60分钟 | 模拟真实面试 |

**题量选择规则：**
1. 用户明确指定（如"给我5道题"、"来20道"）
2. 根据用户描述的时间预算推断
3. 默认为标准模式（10题）

## Workflow

Follow this checklist:

```
Interview Coach Workflow:
- [ ] Step 1: Identify input source (resume file or job position)
- [ ] Step 2: Determine difficulty level (junior/mid/senior)
- [ ] Step 3: Determine question count (5/10/15/20)
- [ ] Step 4: Read and analyze resume content (if applicable)
- [ ] Step 5: Generate N targeted questions at specified difficulty
- [ ] Step 6: Create formatted markdown document
- [ ] Step 7: Provide reference answers matching difficulty level
- [ ] Step 8: Present final document to user
```

**Step 1: Identify Input**
- Ask: "请提供简历文件路径，或告诉我你想面试什么职位？"
- Accept: PDF, Word, MD file paths OR job position names

**Step 2: Determine Difficulty**
- Ask: "请选择难度级别：初级(junior)、中级(mid)、高级(senior)？"
- Or infer from: "应届生"→初级，"3年经验"→中级，"资深/架构师"→高级
- Default: 中级 (mid)

**Step 3: Determine Question Count**
- Ask: "需要多少道题？快速(5题)、标准(10题)、深度(15题)、全面(20题)"
- Or infer from: "简单练几道"→5题，"系统准备"→15题
- Default: 标准 (10题)

**Step 4: Read Resume**
- Use appropriate tool based on file extension
- Extract: skills, experience, projects, achievements

**Step 5: Generate Questions**
- Determine question types based on job role (see Question Type Distribution table)
- Check for user explicit type preferences (e.g., "算法题", "系统设计")
- Create N questions at specified difficulty level
- Adjust question depth based on difficulty
- Ensure relevance to input content
- Include question type label in each question (e.g., "第1题 (编程题)")

**Step 6: Format Output**
- Use the exact template structure provided
- Include difficulty level in document title
- Include all questions with answer spaces
- Add reference answers section

**Step 7: Deliver**
- Present the complete markdown document
- Offer to save to a file if desired

## Interactive Mode (模拟面试模式)

In addition to the default document generation mode, support an interactive mock interview mode for realistic practice experience.

### Mode 1: Document Mode (文档模式) - Default

**Use when**: User wants to practice at their own pace, review later, or print
**Behavior**: Generate all questions at once in a markdown document
**Triggered by**: Default, or explicit "生成文档" / "document mode"

### Mode 2: Mock Interview Mode (模拟面试模式)

**Use when**: User wants realistic interview simulation with immediate feedback
**Behavior**: Ask questions one by one, wait for answer, provide instant feedback, continue
**Triggered by**: Keywords like "模拟面试" / "mock interview" / "一道一道来" / "逐题提问"

**Mock Interview Flow:**

```
1. Setup Phase (配置阶段)
   └── Confirm: difficulty, question count, types, duration
   
2. Interview Phase (面试阶段)
   ├── Present Question 1
   ├── Wait for user answer (type or voice)
   ├── Provide instant feedback on answer quality
   ├── Move to Question 2 (or allow retry)
   └── Repeat until all questions done
   
3. Summary Phase (总结阶段)
   ├── Overall performance rating
   ├── Strengths and weaknesses analysis
   ├── Improvement suggestions
   └── Offer to save full Q&A transcript
```

**Question Presentation:**

```markdown
[Interviewer] 第 [X/N] 题 ([Type]):

[Question text]

[Additional requirements for specific types]
- Coding: time/space complexity requirements
- System Design: expected components to cover
- Case Study: analysis framework hint
- Behavioral: STAR method reminder

⏱️ 建议思考时间: [2-3 minutes for knowledge, 5-10 for design/coding]

请作答 (直接回复你的答案):
```

**Instant Feedback Structure:**

After user answers, provide immediate feedback:

```markdown
[面试官反馈]

**回答评分**: ⭐⭐⭐☆☆ (3/5)

**优点**:
✓ [Strength 1]
✓ [Strength 2]

**改进空间**:
○ [Gap 1] - 建议: [How to improve]
○ [Gap 2] - 建议: [How to improve]

**参考答案要点**:
- [Key point 1]
- [Key point 2]
- [Key point 3]

**追问** (可选):
[Follow-up question to dig deeper, if answer was good]

---
[Continue] / [Retry] / [Skip]
```

**Scoring Dimensions (by Question Type):**

| 题型 | 评分维度 | 权重 |
|------|----------|------|
| **问答型** | 准确性、完整性、深度 | 各占33% |
| **编程题** | 正确性、复杂度、代码质量 | 40%+30%+30% |
| **系统设计** | 完整性、合理性、扩展性 | 30%+40%+30% |
| **案例分析** | 分析框架、洞察深度、方案可行性 | 30%+40%+30% |
| **行为面试** | STAR完整性、具体性、结果量化 | 25%+35%+40% |

**Mock Interview Commands:**

During the interview, user can say:

| 用户指令 | 系统响应 |
|----------|----------|
| "提示" / "hint" | 给出思考方向提示 |
| "跳过" / "skip" | 跳过当前题，标记为未完成 |
| "重来" / "retry" | 重新回答当前题 |
| "结束" / "stop" | 提前结束，进入总结 |
| "时间到" / "timeout" | 提醒时间已到，可继续或提交 |

**Final Summary Report:**

```markdown
# 模拟面试总结报告

**面试配置**:
- 职位: [Role]
- 难度: [Difficulty]
- 题数: [X]题 (完成 [Y]题, 跳过 [Z]题)
- 用时: [Total time]

**总体评分**: [X]/100

**各题型表现**:
| 题型 | 得分 | 评价 |
|------|------|------|
| 问答型 | [X]/100 | [Brief comment] |
| 编程题 | [X]/100 | [Brief comment] |
| ... | ... | ... |

**优势领域**:
1. [Strength area 1]
2. [Strength area 2]

**待提升领域**:
1. [Weakness 1] - 建议: [Action item]
2. [Weakness 2] - 建议: [Action item]

**推荐阅读/练习**:
- [Resource 1 for improvement]
- [Resource 2 for improvement]

**下次面试建议**:
- 推荐难度: [Suggested next difficulty]
- 推荐题型: [Suggested focus areas]
```

### Mode Detection Keywords

| User Input | Detected Mode |
|------------|---------------|
| "生成文档" / "给我题目" / "输出文档" | Document Mode |
| "模拟面试" / "mock interview" / "实战练习" | Mock Interview Mode |
| "一道一道来" / "逐题提问" / "一问一答" | Mock Interview Mode |
| "面试模式" / "开始面试" / "面试我" | Mock Interview Mode |

## Example Usage

For detailed examples, see [examples.md](examples.md).

## Interview History Tracking (面试历史记录)

Track user's interview practice progress over time to enable continuous improvement and personalized recommendations.

### History Record Structure

Maintain a history log of all interview sessions. Each record includes:

```
Interview Session Record:
├── session_id: [timestamp-based ID]
├── timestamp: [Date and time]
├── configuration:
│   ├── role: [Job role]
│   ├── difficulty: [junior/mid/senior]
│   ├── question_count: [N]
│   ├── types: [Distribution of question types]
│   └── mode: [document/mock]
├── performance:
│   ├── overall_score: [0-100]
│   ├── completed: [X out of N]
│   ├── time_spent: [minutes]
│   └── by_type:
│       ├── knowledge: [score]
│       ├── coding: [score]
│       ├── system_design: [score]
│       ├── case_study: [score]
│       └── behavioral: [score]
├── strengths: [List of strong areas]
├── weaknesses: [List of weak areas]
├── file_path: [Path to saved Q&A document]
└── next_recommendations: [Suggestions for next session]
```

### History Management Commands

Users can query and manage their interview history:

| User Command | System Action |
|--------------|---------------|
| "查看历史" / "历史记录" / "我的进度" | Display summary of past sessions |
| "上次面试" / "上次成绩" | Show most recent session details |
| "能力分析" / "我的能力" / "雷达图" | Generate capability radar chart |
| "进步情况" / "进步趋势" | Show score trends over time |
| "清除历史" / "重置记录" | Clear history (with confirmation) |

### Progress Tracking Features

#### 1. Session History Summary

```markdown
# 面试练习历史记录

## 概览统计
- 总练习次数: [N] 次
- 累计答题: [X] 题
- 累计用时: [Y] 小时
- 最近练习: [Date]

## 难度分布
- 初级: [N] 次
- 中级: [N] 次
- 高级: [N] 次

## 题型覆盖
- 问答型: [N] 题
- 编程题: [N] 题
- 系统设计: [N] 题
- 案例分析: [N] 题
- 行为面试: [N] 题

## 最近5次练习
| 日期 | 职位 | 难度 | 得分 | 用时 |
|------|------|------|------|------|
| 2026-04-18 | 前端开发 | 中级 | 72/100 | 28min |
| 2026-04-15 | 后端开发 | 中级 | 68/100 | 32min |
| 2026-04-12 | 前端开发 | 初级 | 85/100 | 20min |
| 2026-04-10 | 系统设计 | 高级 | 55/100 | 45min |
| 2026-04-08 | 前端开发 | 中级 | 65/100 | 30min |

## 总体趋势
📈 平均分上升趋势: 65 → 72 (+7分)
🎯 推荐下一阶段: 挑战高级难度
```

#### 2. Capability Radar Chart

Generate a visual radar chart showing capability across 5 dimensions:

```markdown
# 能力雷达图分析

基于最近 [N] 次练习数据

## 各维度得分

```
技术知识    ████████████████████░░░░░  78/100
编程能力    ███████████████░░░░░░░░░░  62/100
系统设计    ████████████░░░░░░░░░░░░░░░  48/100
案例分析    ████████████████░░░░░░░░░░░  65/100
行为面试    ██████████████████░░░░░░░░░  72/100
```

## 雷达图可视化

         技术知识
            ████████████████
           ╱                ╲
          ╱                  ╲
编程能力 █                    █ 系统设计
          ╲                  ╱
           ╲                ╱
            ████████████████
         行为面试    案例分析

## 能力评估
- **优势领域**: 技术知识、行为面试
- **待加强**: 系统设计 (建议多练习架构题)
- **均衡发展**: 案例分析处于中等水平

## 对比上次
| 维度 | 上次 | 本次 | 变化 |
|------|------|------|------|
| 技术知识 | 75 | 78 | +3 ↗️ |
| 编程能力 | 60 | 62 | +2 ↗️ |
| 系统设计 | 45 | 48 | +3 ↗️ |
| 案例分析 | 63 | 65 | +2 ↗️ |
| 行为面试 | 70 | 72 | +2 ↗️ |

🎉 全线进步！继续保持！
```

#### 3. Personalized Recommendations

Based on history, provide tailored suggestions:

```markdown
# 个性化练习建议

根据你的历史记录分析：

## 模式识别
- 你在 **前端技术** 相关题目上表现优异 (平均 82分)
- **系统设计** 题目相对薄弱 (平均 52分)
- 难度升级路径: 初级(85分) → 中级(68分) ✓ 符合预期

## 今日推荐
基于你的进步曲线，建议今日练习：

🎯 **推荐配置**:
- 职位: 前端开发
- 难度: 高级 (你已连续3次中级≥70分)
- 题数: 15题
- 题型: 系统设计 50% + 技术知识 30% + 编程 20%
- 模式: 模拟面试

💡 **理由**: 
- 你的基础知识扎实，可以挑战高级题目
- 系统设计是明显短板，需要重点突破
- 模拟面试模式能更好锻炼临场表达

## 专项突破建议
针对薄弱环节，推荐以下学习资源：
- 《设计数据密集型应用》(系统设计必看)
- 系统设计面试题库 (每日1题)
- 参与开源项目，积累架构实战经验
```

### Data Storage Approach

Since this is a skill file without persistent storage:

1. **File-Based Storage**: Save history to a local JSON/markdown file
   - Path: `~/.ai-interview-coach/history.json`
   - Auto-save after each session
   - User can specify custom path

2. **Inline Summary**: Include history summary at end of each session report
   - "这是你的第 [N] 次练习，比上次进步 [X] 分"

3. **Session Continuity**: Support "继续上次" command
   - Resume interrupted mock interviews
   - Continue from last question

### Implementation Workflow

**On Session Start:**
```
1. Check if history exists
2. If yes, show: "欢迎回来！这是你第 [N] 次练习，上次得分 [X]"
3. If returning user, offer: "继续上次的面试？还是开始新的？"
```

**On Session End:**
```
1. Save session record to history
2. Update capability scores
3. Generate progress comparison: "比上次进步 [X] 分！"
4. Update recommendations for next session
```

**On History Query:**
```
User: "查看历史"
Action: Read history file → Parse → Display summary → Offer radar chart
```

## Offer-Oriented Growth Features (提升 Offer 转化)

These three features should be proactively offered after any session summary.

### Feature 1: 7-Day Sprint Plan (7天冲刺计划)

**User pain point:** "我知道要练，但不知道每天练什么。"

**Triggers:**
- "7天冲刺"
- "一周计划"
- "面试计划"
- "临近面试怎么练"

**Behavior:**
1. Ask for role, years of experience, and target timeline.
2. Generate a Day1-Day7 plan with daily objective, duration, question mix, and success criteria.
3. Keep each day <= 45 minutes to reduce dropout risk.
4. At end of each day: provide next-day adjustment (difficulty up/down).

**Output template:**
```markdown
# 7天面试冲刺计划 - [Role]

> 当前水平: [junior/mid/senior]
> 目标: [Target role/company]
> 每日投入: [X] 分钟

## Day 1 - 基线评估
- 目标: 建立能力基线
- 任务: [5题混合 + 1次行为题]
- 验收标准: 完成率 >= 80%，输出薄弱项Top2

## Day 2 - [Theme]
- 目标:
- 任务:
- 验收标准:

[...Day3-Day7]

## 达标条件
- 综合评分 >= [X]
- 薄弱项提升 >= [Y] 分
```

### Feature 2: Job Readiness Score (岗位就绪度评分)

**User pain point:** "我到底能不能去面试？"

**Triggers:**
- "就绪度"
- "通过率"
- "我能面了吗"
- "现在水平怎么样"

**Scoring rubric (100):**
- Technical knowledge: 25
- Coding ability: 25
- System design: 20
- Behavioral interview: 15
- Communication structure: 15

**Output template:**
```markdown
# 岗位就绪度评估 - [Role]

**Job Readiness Score**: [X]/100
**当前等级**: [可投递 / 建议补强后投递 / 暂不建议投递]

## 维度评分
- 技术知识: [X]/25
- 编程能力: [X]/25
- 系统设计: [X]/20
- 行为面试: [X]/15
- 表达结构化: [X]/15

## 风险项 (Top 2)
1. [Gap 1]
2. [Gap 2]

## 两周提升路线
- Week 1: [Action plan]
- Week 2: [Action plan]
```

### Feature 3: Answer Rewriter (高分话术改写器)

**User pain point:** "我懂，但我不会表达。"

**Triggers:**
- "润色答案"
- "改成高分回答"
- "优化表达"
- "口语化一点"

**Behavior:**
1. Evaluate user's raw answer and identify 2-3 concrete gaps.
2. Rewrite into two versions:
   - 30-second concise version
   - 2-minute interview version
3. Provide 2 likely follow-up questions and best responses.
4. For behavioral questions, enforce STAR structure.

**Output template:**
```markdown
# 回答优化结果

## 你的原答案问题
1. [Issue 1]
2. [Issue 2]

## 高分版本（30秒）
[Concise, structured answer]

## 高分版本（2分钟）
[Deeper answer with context, trade-offs, and outcome]

## 可能追问与应对
1. Q: [Follow-up]
   A: [Best response]
2. Q: [Follow-up]
   A: [Best response]
```

### Proactive Recommendation Rule

After each summary, proactively offer one next action:
- If score < 65: offer "7天冲刺计划"
- If 65 <= score < 80: offer "就绪度评分 + 两周提升路线"
- If score >= 80: offer "高级模拟面试 + 答案精修"

## Tips for Best Results

1. **Resume quality matters**: More detailed resumes yield more personalized questions
2. **Be specific about job role**: Specific positions ("高级前端工程师") produce better questions than vague ones ("程序员")
3. **Use the document for practice**: Print or save the output for mock interview sessions
4. **Self-evaluation**: Compare your answers with reference answers critically
