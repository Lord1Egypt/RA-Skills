---
name: academic-learning-assistant
description: 根据学科、年级生成个性化学习助理，支持数学、物理、化学、生物、语文、英语、历史、地理、计算机科学、工程技术、医学、经济学、文学、管理学、艺术学、农学等学科；当用户需要创建学科学习助手、定制教学内容或设计学习路径时使用
---

# 学科学习助理生成器

## 任务目标
- 本 Skill 用于: 根据用户提供的学科、年级、学习目标等信息，生成个性化的学科学习助理
- 能力包含: 助理角色设计、知识体系梳理、学习路径规划、教学方法定制
- 触发条件: 用户需要创建特定学科的学习助理、定制教学内容或设计学习路径

## 前置准备
- 无需特殊依赖或环境准备
- 确定目标学科、年级和主要学习目标

## 操作步骤

### 步骤 1: 收集学科信息
与用户确认以下核心信息：
- 学科名称（数学、物理、化学、生物、语文、英语、历史、地理、计算机科学、工程技术、医学、经济学、文学、管理学、艺术学、农学）
- 年级阶段（小学/初中/高中/大学/职业培训）
- 学习目标（知识巩固、能力提升、考试备考、兴趣拓展等）
- 特殊需求（教学风格偏好、交互方式等）

### 步骤 2: 设计助理角色
根据学科特点设计助理人设：
- **角色定位**: 参考学科特性（如数学强调逻辑推理、语文注重文学素养）
- **学科视角内核**: 提取该学科特有的思维方式和分析视角（见三重验证机制）
- **教学风格**: 选择启发性、引导式、系统化或趣味性风格
- **教学DNA**: 量化描述该学科特有的教学风格、表达方式、互动模式
- **交互方式**: 确定提问方式、反馈机制、难度调整策略
- **个性特征**: 赋予助理独特的教学人格（如严谨、耐心、幽默、鼓励型）

参考 [references/assistant-role-template.md](references/assistant-role-template.md) 获取角色设计模板
参考 [references/extraction-methodology.md](references/extraction-methodology.md) 了解学科视角内核提取方法

### 步骤 3: 生成核心内容
根据学科和年级生成教学内容：

#### 3.1 知识体系梳理
读取对应学科的 [references/<学科>-knowledge-system.md](references/) 文件，了解：
- 学科核心知识模块
- 年级对应的知识点分布
- 教学重点和难点

#### 3.2 学习路径设计
基于知识体系设计渐进式学习路径：
- 基础知识铺垫
- 核心概念深入
- 综合能力应用
- 拓展延伸探索

#### 3.3 教学方法制定
针对学科特点选择教学方法：
- **数学/物理/化学**: 强调概念理解、例题讲解、练习反馈
- **生物**: 注重知识点关联、实验思维培养
- **语文/英语**: 侧重阅读理解、写作表达、语言运用
- **历史/地理**: 强调时空观念、因果关系、记忆策略
- **计算机科学**: 重视代码实践、调试能力、项目驱动、技术跟踪
- **工程技术**: 强调理论联系实际、工程思维、系统设计、创新实践
- **医学**: 注重理论与实践结合、临床思维、人文关怀、循证决策
- **经济学**: 强调数据分析、经济建模、政策分析、决策能力
- **文学**: 注重文本分析与创作实践、审美体验、文学鉴赏
- **管理学**: 强化案例教学与模拟实训、团队协作、领导力培养
- **艺术学**: 强调审美体验与创作表达、技能训练、艺术创新
- **农学**: 重视田间实践与技术应用、生态保护、可持续发展

### 步骤 4: 输出助理配置
将设计结果结构化输出，包含：
- 助理基本信息（名称、角色、目标）
- 学科视角内核（三重验证通过的核心思维框架）
- 研究式学习工作流（何时调研、何时直接讲解）
- 教学策略与风格
- 教学DNA（量化的教学特征描述）
- 学科知识框架图
- 核心知识点解析
- 学习路径规划
- 学习方法指导
- 学科内在张力（学科内的固有矛盾和权衡）
- 学科谱系（学科发展脉络、关键人物、学派演变）
- 资源推荐清单
- 角色扮演规则（免责声明、退出机制）
- 交互示例与场景

### 步骤 5: 验证与优化
- 检查内容是否符合学科教学规律
- 验证学习路径的合理性和渐进性
- 确保助理角色与学科特点匹配

## 资源索引
- 角色设计参考: [references/assistant-role-template.md](references/assistant-role-template.md)
- 内核提取方法: [references/extraction-methodology.md](references/extraction-methodology.md)
- 数学知识体系: [references/math-knowledge-system.md](references/math-knowledge-system.md)
- 物理知识体系: [references/physics-knowledge-system.md](references/physics-knowledge-system.md)
- 化学知识体系: [references/chemistry-knowledge-system.md](references/chemistry-knowledge-system.md)
- 生物知识体系: [references/biology-knowledge-system.md](references/biology-knowledge-system.md)
- 语文知识体系: [references/chinese-knowledge-system.md](references/chinese-knowledge-system.md)
- 英语知识体系: [references/english-knowledge-system.md](references/english-knowledge-system.md)
- 历史知识体系: [references/history-knowledge-system.md](references/history-knowledge-system.md)
- 地理知识体系: [references/geography-knowledge-system.md](references/geography-knowledge-system.md)
- 计算机科学知识体系: [references/computer-science-knowledge-system.md](references/computer-science-knowledge-system.md)
- 工程技术知识体系: [references/engineering-technology-knowledge-system.md](references/engineering-technology-knowledge-system.md)
- 医学知识体系: [references/medicine-knowledge-system.md](references/medicine-knowledge-system.md)
- 经济学知识体系: [references/economics-knowledge-system.md](references/economics-knowledge-system.md)
- 文学知识体系: [references/literature-knowledge-system.md](references/literature-knowledge-system.md)
- 管理学知识体系: [references/management-knowledge-system.md](references/management-knowledge-system.md)
- 艺术学知识体系: [references/arts-knowledge-system.md](references/arts-knowledge-system.md)
- 农学知识体系: [references/agriculture-knowledge-system.md](references/agriculture-knowledge-system.md)

## 注意事项
- 仅在需要时读取特定学科的参考文档，保持上下文简洁
- 充分利用智能体的知识库和推理能力，设计符合教育规律的教学方案
- 根据用户反馈动态调整助理配置，确保个性化适配
- 避免过度设计，聚焦核心教学价值

## 使用示例

### 示例 1: 创建高中数学学习助理
- **用户需求**: "帮我创建一个针对高一数学的学习助理，重点是函数部分"
- **执行方式**: 智能体主导
- **关键步骤**:
  1. 确认年级为高一，重点模块为函数
  2. 读取 math-knowledge-system.md 了解函数知识点
  3. 设计严谨逻辑型助理，强调概念理解和应用能力
  4. 生成函数章节的学习路径（定义→性质→图像→应用）

### 示例 2: 设计初中英语学习路径
- **用户需求**: "需要为初一学生设计英语学习路径，重点是词汇和语法"
- **执行方式**: 智能体主导
- **关键步骤**:
  1. 确认学科为英语，年级初一，重点词汇和语法
  2. 读取 english-knowledge-system.md 获取初一知识模块
  3. 设计趣味互动型助理，注重听说读写综合能力
  4. 规划词汇记忆策略和语法练习方法

### 示例 3: 创建高考备考历史助理
- **用户需求**: "创建一个历史学习助理，帮助学生备考高考"
- **执行方式**: 智能体主导
- **关键步骤**:
  1. 确认学科为历史，目标为高考备考
  2. 读取 history-knowledge-system.md 了解高考考点
  3. 设计时间线索型助理，强调时空观念和因果关系
  4. 生成按时间轴和主题的复习路径

### 示例 4: 创建大学计算机科学学习助理
- **用户需求**: "帮我创建一个计算机科学学习助理，重点是数据结构与算法"
- **执行方式**: 智能体主导
- **关键步骤**:
  1. 确认学科为计算机科学，学习阶段为大学
  2. 读取 computer-science-knowledge-system.md 获取算法与数据结构模块
  3. 设计逻辑推理型助理，强调代码实践和调试能力
  4. 规划从基础数据结构到高级算法的学习路径，包含项目实践

### 示例 5: 设计职业培训医学学习路径
- **用户需求**: "需要为医学职业培训设计学习助理，重点是临床技能"
- **执行方式**: 智能体主导
- **关键步骤**:
  1. 确认学科为医学，学习阶段为职业培训
  2. 读取 medicine-knowledge-system.md 了解临床技能模块
  3. 设计实践导向型助理，注重理论与实践结合、临床思维训练
  4. 规划从基础医学到临床实践的学习路径，包含病例分析和模拟训练
