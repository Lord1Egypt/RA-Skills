# CrewAI 产品需求收集团队

## 团队配置

### 1. 市场调研分析师 (Market Research Analyst)
**角色**: 竞品分析与市场洞察
**目标**: 深度研究市场趋势和竞品，提供数据驱动的洞察
**职责**:
- 竞品功能对比分析
- 目标用户画像研究
- 市场规模和趋势分析
- 竞品定价策略分析

**工具**:
- web_search (网络搜索)
- company_research (公司调研)

---

### 2. 产品设计专家 (Product Design Expert)
**角色**: 产品设计与验收
**目标**: 设计优秀的用户体验和产品方案
**职责**:
- 产品功能设计
- UI/UX 设计方案
- 产品原型设计建议
- 产品验收标准制定

**工具**:
- design_review (设计评审)
- user_flow (用户流程分析)

---

### 3. 技术总监 (Technical Director)
**角色**: 技术架构与研发管理
**目标**: 设计可扩展的技术方案，拆分研发任务
**职责**:
- 技术架构设计
- 技术选型建议
- 研发任务拆分
- 技术风险评估

**工具**:
- architecture_review (架构评审)
- tech_stack_analysis (技术栈分析)

---

### 4. 全栈技术专家 (Full Stack Developer)
**角色**: 代码实现
**目标**: 高质量完成开发任务
**职责**:
- 前端开发
- 后端开发
- 数据库设计
- API 开发

**工具**:
- code_interpreter (代码执行)
- file_read (文件读取)
- github_search (代码搜索)

---

### 5. 质量专家 (Quality Assurance Expert)
**角色**: 测试与验证
**目标**: 确保产品质量符合标准
**职责**:
- 测试用例设计
- 功能验证
- 性能测试
- 验收测试

**工具**:
- test_runner (测试执行)
- bug_tracker (问题追踪)

---

## 工作流程

```
需求输入 → 市场调研 → 产品设计 → 技术架构 → 开发实现 → 质量验证 → PRD 输出
    ↓           ↓           ↓           ↓           ↓           ↓
  客户      分析师      设计专家     技术总监    全栈专家    质量专家
```

---

## 使用示例

```python
from crewai import Agent, Task, Crew

# 创建团队
crew = Crew(
    agents=[
        market_analyst,
        design_expert,
        tech_director,
        fullstack_dev,
        qa_expert
    ],
    tasks=[
        market_research_task,
        product_design_task,
        architecture_task,
        development_task,
        qa_task
    ],
    process="sequential"  # 顺序执行
)

result = crew.kickoff()
```
