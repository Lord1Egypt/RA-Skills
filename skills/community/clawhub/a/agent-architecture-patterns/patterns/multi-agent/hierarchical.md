# 层级模式 (Hierarchical) - 多 Agent 协作

> **版本**: 1.0.0  
> **适用场景**: 大型复杂项目、需要多层协调、有明确组织结构的场景  
> **复杂度**: ⭐⭐⭐⭐（高）

---

## 🧠 核心思想

**层级模式 = 多层管理结构 + 分层决策**

- **分层管理**：CEO → Managers → Teams → Workers
- **分层决策**：战略决策在高层，执行决策在低层
- **信息传递**：自顶向下传递指令，自底向上汇报进度

**与主从模式的区别**：
- 主从模式：单层管理（1 个 Manager + N 个 Worker）
- 层级模式：多层管理（适合大规模系统）

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                      CEO Agent                           │
│  （战略决策、资源分配、跨部门协调）                       │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ Manager A     │ │ Manager B     │ │ Manager C     │
│ （技术部门）   │ │ （产品部门）   │ │ （运营部门）   │
└───────────────┘ └───────────────┘ └───────────────┘
        ↓                 ↓                 ↓
   ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
   ↓         ↓       ↓         ↓       ↓         ↓
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│Team │  │Team │  │Team │  │Team │  │Team │  │Team │
│ A1  │  │ A2  │  │ B1  │  │ B2  │  │ C1  │  │ C2  │
└─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class HierarchicalAgent {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async execute(task, organization) {
    if (this.verbose) {
      console.log(`[Hierarchical] 开始任务：${task}`);
      console.log(`[Hierarchical] 组织结构：${this.describeOrg(organization)}`);
    }
    
    // Phase 1: CEO 制定战略
    const strategy = await organization.ceo.makeStrategy(task);
    
    if (this.verbose) {
      console.log(`[CEO Strategy] ${strategy}`);
    }
    
    // Phase 2: Managers 分解为部门计划
    const departmentPlans = await this.coordinateManagers(organization.managers, strategy);
    
    if (this.verbose) {
      console.log(`[Department Plans] ${departmentPlans.length}个部门计划`);
    }
    
    // Phase 3: Teams 执行具体任务
    const teamResults = await this.coordinateTeams(organization.teams, departmentPlans);
    
    if (this.verbose) {
      console.log(`[Team Results] ${teamResults.length}个团队结果`);
    }
    
    // Phase 4: 整合结果
    const finalResult = await this.integrateResults(task, teamResults);
    
    return finalResult;
  }

  async coordinateManagers(managers, strategy) {
    const plans = await Promise.all(
      managers.map(manager => manager.createPlan(strategy))
    );
    return plans;
  }

  async coordinateTeams(teams, departmentPlans) {
    const results = [];
    
    for (const plan of departmentPlans) {
      const team = teams.find(t => t.department === plan.department);
      if (team) {
        const result = await team.execute(plan);
        results.push(result);
      }
    }
    
    return results;
  }

  async integrateResults(task, results) {
    const prompt = `
任务：${task}

各部门结果：
${results.map((r, i) => `部门 ${i + 1}: ${r}`).join('\n')}

请整合所有结果，生成最终报告。

最终报告：`;
    
    return await this.llm.generate(prompt);
  }

  describeOrg(org) {
    return `CEO: ${org.ceo.id}, Managers: ${org.managers.length}, Teams: ${org.teams.length}`;
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Completed.';
    }
  };
}

/**
 * CEO Agent
 */
class CEOAgent {
  constructor(id) {
    this.id = id;
    this.llm = null;
  }

  async makeStrategy(task) {
    const prompt = `
作为 CEO，请为以下任务制定战略：
${task}

考虑：
1. 总体目标
2. 资源分配
3. 关键里程碑
4. 风险管控

战略：`;
    
    return await this.llm.generate(prompt);
  }
}

/**
 * Manager Agent
 */
class ManagerAgent {
  constructor(id, department) {
    this.id = id;
    this.department = department;
    this.llm = null;
  }

  async createPlan(strategy) {
    const prompt = `
部门：${this.department}

公司战略：
${strategy}

请制定部门计划：
1. 部门目标
2. 具体任务
3. 所需资源
4. 时间表

部门计划：`;
    
    return await this.llm.generate(prompt);
  }
}

/**
 * Team Agent
 */
class TeamAgent {
  constructor(id, department, members) {
    this.id = id;
    this.department = department;
    this.members = members;
    this.llm = null;
  }

  async execute(plan) {
    const prompt = `
团队：${this.id}
部门：${this.department}

部门计划：
${plan}

请执行任务并报告结果。

结果：`;
    
    return await this.llm.generate(prompt);
  }
}
```

---

### 使用示例

```javascript
// 创建组织
const ceo = new CEOAgent('ceo-1');

const managers = [
  new ManagerAgent('mgr-1', '技术部'),
  new ManagerAgent('mgr-2', '产品部'),
  new ManagerAgent('mgr-3', '市场部')
];

const teams = [
  new TeamAgent('team-1', '技术部', ['dev1', 'dev2']),
  new TeamAgent('team-2', '产品部', ['pm1', 'pm2']),
  new TeamAgent('team-3', '市场部', ['marketing1'])
];

const organization = { ceo, managers, teams };

// 创建层级系统
const hierarchical = new HierarchicalAgent({ verbose: true });

// 执行任务
const task = '推出一个新的移动应用';
const result = await hierarchical.execute(task, organization);
console.log(result);
```

---

## 🎯 适用场景

### ✅ 适合的场景

1. **大型项目**：需要多层协调
2. **多部门协作**：有不同专业部门
3. **长期项目**：需要持续管理
4. **复杂决策**：需要分层决策

### ❌ 不适合的场景

1. **小型项目**：过度工程
2. **需要快速响应**：层级太多决策慢
3. **创新导向**：层级抑制创新
4. **资源有限**：管理成本高

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02
