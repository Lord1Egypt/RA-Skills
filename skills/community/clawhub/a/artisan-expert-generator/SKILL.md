---
name: artisan-expert-generator
description: 基于职业身份知识结构自动生成专家Skill；支持6维度采集、用户私有知识融合、框架提炼、质量验证与双Agent精炼。当用户需要创建职业专家助手、构建领域专业视角或生成标准化专业知识输出时使用此工具即可
dependency:
  python:
    - pypdf==3.17.4
    - python-docx==1.1.0
    - PyYAML==6.0.1
    - markdown==3.5.2
---

# 职业专家Skill生成器

## 核心理念

Artisan 不是复制职业知识，是**提炼专业视角**。

一个好的职业专家 Skill 是一套可运行的**专业认知操作系统**：
- 他用什么**专业视角内核**看问题？（方法论核心）
- 他用什么**分析框架**做判断？（步骤和流程）
- 他怎么**表达**？（专业语言规范和风格）
- 他**绝对不会**做什么？（职业伦理边界）
- 什么是这个专家**做不到的**？（能力边界）

**关键区分**：捕捉的是职业视角的本质，不是职业知识的堆砌。

### 职业身份 vs 人物身份

| 维度 | 人物 Skill（女娲） | 职业专家 Skill（Artisan） |
|------|------------------|------------------------|
| 蒸馏对象 | 具体个人的思维框架 | 职业身份的专业视角 |
| 知识来源 | 个人著作、访谈、演讲 | 专业文献、法规、案例、标准 |
| 思维框架 | 个人独创的心智模型 | 职业共识方法论 + 行业实践 |
| 表达风格 | 模仿个人的语言特征 | 遵循职业表达规范 |
| 可验证性 | 对比个人公开表态 | 对比行业标准和专业共识 |
| 时效性 | 需跟踪个人最新动态 | 更新专业法规和行业实践 |

---

## 任务目标
- 本 Skill 用于：根据用户提供的职业身份信息，生成符合规范的职业专家Skill
- 能力包含：信息采集引导、框架提炼指导、Skill结构生成、质量验证
- 触发条件：用户说"创建XX专家"、"生成XX职业Skill"、"我需要一个XX领域的顾问"

## 前置准备
- 依赖说明：scripts依赖pypdf、python-docx、PyYAML、markdown
- 用户准备：
  - 明确职业身份（如"刑法律师"、"明史专家"）
  - 可选：上传私有知识文件（PDF/Word/Markdown）
  - 可选：提供应用场景偏好（如"合同审查"、"风险评估"）

## 操作步骤

### Phase 0: 入口分流
- 识别输入类型（明确职业/模糊需求）
- 确认专家身份定义
- 收集用户私有知识（可选）
- 收集用户偏好配置（可选）

### Phase 1: 六维度信息采集
- 维度1: 学科基础（核心概念、理论框架）
- 维度2: 法规规范（法律法规、行业规范）
- 维度3: 方法论（分析框架、决策流程）
- 维度4: 典型案例（经典案例、解决方案）
- 维度5: 行业实践（实务技巧、行业惯例）
- 维度6: 表达规范（专业术语、文书格式）

用户私有知识处理：
- 调用 `python scripts/parse_document.py --file_path <路径>` 解析文件
- 将内容归入对应维度

详见：[6维度采集详细指南](references/collection-dimensions.md)

### Phase 1.5: 采集确认检查点（必须用户确认）
展示内容：
- 各维度采集数量和关键发现
- 信息源类型占比（一手/学术/实务）
- 矛盾点和信息缺口
- 用户知识贡献度

用户操作：
- [确认] 信息准确完整，继续构建专家Skill
- [补充] 添加更多资料或方向 → 增量采集
- [修改] 调整采集方向 → 重新采集
- [重新采集] 从头开始

### Phase 2: 专家框架提炼
- 提取知识体系（核心概念、理论框架）
- 构建分析框架（分析步骤、决策流程）
- 提炼决策启发式（快速规则）
- 定义伦理边界（职业禁忌、能力边界）
- 融合用户偏好（风格配置、关注重点）

### Phase 2.5: 提炼确认检查点（必须用户确认）
展示内容：
- 知识体系（核心概念列表）
- 分析框架（分析步骤）
- 决策启发式（快速规则列表）
- 伦理边界与禁忌
- 表达风格配置选项

用户操作：
- [确认] 框架准确，继续构建Skill
- [修改] 调整已有内容
- [添加] 添加自定义内容
- [重新提炼] 放弃当前提炼，重新分析

### Phase 3: Skill构建
调用脚本生成SKILL.md文件：
```bash
python scripts/generate_skill.py \
  --expert_name "刑法律师" \
  --knowledge_system '{"core_concepts":["犯罪构成要件","刑罚种类"],"theories":["四要件说"]}' \
  --analysis_framework '{"steps":["问题定性","构成要件分析","量刑分析","辩护策略"]}' \
  --decision_rules '[{"condition":"不符合构成要件","action":"判断无罪"}]' \
  --ethics '{"must":["保守当事人秘密"],"must_not":["不教唆作伪证"]}' \
  --expression_style '{"language":"正式专业","format":"正式报告","detail":"适中"}' \
  --output_path "/workspace/projects/criminal-law-expert/SKILL.md"
```

### Phase 4: 质量验证
调用脚本验证Skill结构：
```bash
python scripts/validate_structure.py --skill_path "/workspace/projects/criminal-law-expert"
```

验证维度：
- 专业准确性（对比行业标准）
- 边界测试（边缘案例响应）
- 风格测试（表达是否符合预期）

### Phase 5: 双Agent精炼（可选）
- Agent A: 结构评估与改进建议
- Agent B: 可操作性评审

### 跨学科专家生成流程（可选）

#### Phase 0-Cross: 跨学科专家入口分流
- 识别用户需求类型（单一领域/跨学科）
- 配置跨学科知识结构：
  - 选择主领域（T型竖线，深度专业，权重70%）
  - 选择辅助领域（T型横线，广度拓展，各10-15%）
  - 配置知识融合策略
- 收集用户私有知识（可选）
- 配置表达能力要求（可选）

详见：[跨学科专家专项指南](references/cross-disciplinary-guide.md)

#### Phase 1-Cross: 多领域并行采集
- 并行启动多个领域的6维度采集Agent
- 主领域：完整深度采集（学科基础、法规规范、方法论、典型案例、行业实践、表达规范）
- 辅助领域：关键点采集（聚焦融合点）
- 调用 `python scripts/parse_document.py --file_path <路径>` 解析用户私有知识

#### Phase 1.5-Cross: 采集确认检查点（必须用户确认）
展示内容：
- 各领域采集结果（主领域+辅助领域）
- 知识交叉点识别
- 融合方向建议
- 用户知识贡献度

用户操作：
- [确认] 采集结果准确，继续知识融合
- [补充] 添加更多领域或内容 → 增量采集
- [修改] 调整领域权重或采集深度 → 重新采集
- [重新采集] 从头开始

#### Phase 2-Cross: 跨学科知识融合
详见：[知识融合方法指南](references/knowledge-fusion-methods.md)

- 构建跨学科知识图谱
  - 提取各领域核心概念
  - 识别概念映射关系
  - 构建领域内和跨领域关系
  - 标注融合点、冲突点、创新点
- 提取融合规则
  - 主领域优先原则
  - 概念冲突标注原则
  - 关键点聚焦原则
- 生成融合框架
  - 统一概念体系
  - 跨学科分析方法
  - 创新解决方案

#### Phase 2.5-Cross: 融合确认检查点（必须用户确认）
展示内容：
- 跨学科知识图谱
- 融合后的知识体系
- 跨学科分析框架
- 融合规则列表

用户操作：
- [确认] 融合结果准确，继续表达能力增强
- [修改] 调整融合规则或权重
- [添加] 添加自定义融合规则
- [重新融合] 放弃当前融合，重新分析

#### Phase 3-Cross: 增强表达能力
详见：[表达能力模块指南](references/expression-capabilities.md)

- 采集写作能力（科普写作、新闻写作、公文写作、学术写作）
- 采集演说能力（公众演讲、专家访谈、沟通技巧、问答应对）
- 配置表达风格（语言风格、结构形式、情感基调）
- 生成表达能力模型

#### Phase 4-Cross: 构建跨学科专家Skill
调用脚本生成SKILL.md文件（扩展参数）：
```bash
python scripts/generate_skill.py \
  --expert_name "智慧城市解决方案专家" \
  --knowledge_system '{"core_concepts":["城市规划","智能技术","数据驱动"],"theories":["系统理论"、"T型知识结构"]}' \
  --analysis_framework '{"steps":["问题定义","跨领域分析","融合方案设计","实施评估"]}' \
  --decision_rules '[{"condition":"技术可行性不足","action":"调整技术方案"}]' \
  --ethics '{"must":["可持续发展","社会公平"],"must_not":["技术至上"]}' \
  --expression_style '{"language":"学术","structure":"逻辑","emotional":"rational"}' \
  --cross_disciplinary_config '{"primary_domain":"城市规划","secondary_domains":["计算机科学","数据科学","社会学"]}' \
  --fusion_method "graph-based" \
  --expression_capabilities '{"writing":["科普写作","学术写作"],"speaking":["公众演讲","专家访谈"]}' \
  --output_path "/workspace/projects/smart-city-expert/SKILL.md"
```

#### Phase 5-Cross: 质量验证与优化
调用脚本验证Skill结构：
```bash
python scripts/validate_structure.py --skill_path "/workspace/projects/smart-city-expert"
```

验证维度：
- 跨学科融合效果（知识融合评估）
- 表达能力验证（写作/演说能力测试）
- 边界测试（跨领域问题响应）
- 用户评估反馈

迭代优化：
- 根据评估结果调整融合规则
- 优化表达能力配置
- 收集用户反馈持续改进

### Phase 5: 双Agent精炼（可选）
- Agent A: 结构评估与改进建议
- Agent B: 可操作性评审

## 使用示例

### 示例1: 明确职业身份
- 场景/输入: "创建一个刑法律师专家Skill"
- 预期产出: 生成包含刑法专业知识、分析框架、伦理边界的专家Skill
- 关键要点:
  - 直接进入Phase 1六维度采集
  - 重点关注法规规范、典型案例维度
  - 输出符合律师职业伦理的表达规范

### 示例2: 模糊需求诊断
- 场景/输入: "我需要帮我看合同风险"
- 预期产出: 建议创建"合同法专家"并引导用户确认
- 关键要点:
  - Phase 0识别需求本质（合同审查）
  - 推荐专家身份（合同法专家）
  - 调整采集重点（合同法相关法规、案例）

### 示例3: 层级扩展
- 场景/输入: "在刑法专家基础上，增加经济犯罪方向"
- 预期产出: 继承刑法专家框架 + 深度扩展经济犯罪知识
- 关键要点:
  - 识别职业身份层级（Level 2 → Level 3）
  - 继承父级框架（刑法通用知识）
  - 深度采集细分方向（经济犯罪案例、法规）

### 示例4: 互联网职业专家
- 场景/输入: "创建一个B端产品经理专家Skill"
- 预期产出: 生成包含需求分析、业务架构、产品规划能力的专家Skill
- 关键要点:
  - 参考[互联网行业专项指南](references/internet-industry-guide.md)
  - 重点采集：需求分析方法论、PRD规范、产品规划流程
  - 核心能力：用户体验地图、需求评审、敏捷开发流程
  - 行业知识：电商、SaaS等B端产品案例

### 示例5: 互联网开发专家
- 场景/输入: "创建一个前端开发工程师专家Skill，技术栈偏好React"
- 预期产出: 生成包含React技术栈、性能优化、跨平台方案的专家Skill
- 关键要点:
  - 指定技术栈偏好（React、TypeScript）
  - 重点采集：React生态、性能优化方案、工程化实践
  - 核心能力：组件化开发、状态管理、性能优化
  - 行业案例：大型前端项目架构案例

### 示例6: 跨学科专家（T型知识结构）
- 场景/输入: "创建一个智慧城市解决方案专家，主领域是城市规划，辅助领域包括计算机科学、数据科学和社会学"
- 预期产出: 生成具备T型知识结构的跨学科专家Skill，能够融合城市规划、技术和人文视角
- 关键要点:
  - 进入Phase 0-Cross跨学科流程
  - 配置T型知识结构：城市规划（70%）+ 计算机科学（15%）+ 数据科学（10%）+ 社会学（5%）
  - 参考[跨学科专家专项指南](references/cross-disciplinary-guide.md)
  - 构建跨学科知识图谱（识别融合点：城市数据、智能交通、社会公平）
  - 知识融合：城市规划理论 + 智能技术 + 数据驱动 + 社会影响评估
  - 增强表达能力：科普写作（向公众解释智慧城市）、公众演讲（参与城市规划论坛）
  - 详见：[知识融合方法指南](references/knowledge-fusion-methods.md)、[表达能力模块指南](references/expression-capabilities.md)

### 示例7: 跨学科专家（医疗信息化）
- 场景/输入: "创建一个医疗信息化专家，擅长向医疗机构提供数字化转型建议，并能够向公众科普医疗技术"
- 预期产出: 生成融合医疗、技术、管理的跨学科专家，具备强表达能力
- 关键要点:
  - T型知识结构：医学（70%）+ 计算机科学（15%）+ 管理学（10%）+ 传播学（5%）
  - 知识融合点：医疗数据、电子病历、患者隐私、系统安全
  - 融合规则：安全性原则优先于效率原则
  - 表达能力配置：
    * 写作：科普写作（向公众解释AI医疗）、公文写作（医疗合规报告）
    * 演说：公众演讲（医疗科技论坛）、专家访谈（媒体采访）
  - 应用场景：医院数字化转型咨询、医疗技术科普、医疗伦理评估

## 资源索引

### 脚本
- [scripts/generate_skill.py](scripts/generate_skill.py)（用途：Phase 3生成专家SKILL.md文件）
- [scripts/parse_document.py](scripts/parse_document.py)（用途：解析用户上传的PDF/Word/Markdown文件）
- [scripts/validate_structure.py](scripts/validate_structure.py)（用途：Phase 4验证Skill结构完整性）

### 参考
- [references/profession-taxonomy.md](references/profession-taxonomy.md)（何时读取：Phase 0识别职业身份层级时）
- [references/cross-disciplinary-guide.md](references/cross-disciplinary-guide.md)（何时读取：创建跨学科专家时）
- [references/knowledge-fusion-methods.md](references/knowledge-fusion-methods.md)（何时读取：Phase 2-Cross知识融合时）
- [references/expression-capabilities.md](references/expression-capabilities.md)（何时读取：Phase 3-Cross增强表达能力时）
- [references/internet-industry-guide.md](references/internet-industry-guide.md)（何时读取：创建互联网领域专家时）
- [references/skill-template.md](references/skill-template.md)（何时读取：Phase 2提炼框架结构时）
- [references/collection-dimensions.md](references/collection-dimensions.md)（何时读取：Phase 1执行六维度采集时）

### 资产
- [assets/skill-template.md](assets/skill-template.md)（直接用于生成/修饰输出：专家SKILL.md模板文件）

## 注意事项
- 仅在需要时读取参考文档，保持上下文简洁
- Phase 1.5和Phase 2.5必须等待用户确认后才能继续
- 用户私有知识优先级最高，应覆盖公开知识
- 充分利用智能体的网络搜索和内容理解能力，避免为简单任务编写脚本
- 生成的专家Skill必须符合clawhub的规范（SKILL.md + scripts/ + references/ + assets/）
