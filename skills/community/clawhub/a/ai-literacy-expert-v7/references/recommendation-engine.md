# 智能课程推荐引擎指南（V5 新增）

> 本文是 V5 能力五「智能课程推荐引擎」的设计与实现手册。

## 一、核心理念

- **目标导向**：从学习目标反推课程路径
- **个性化**：基于受众特征匹配最优学习顺序
- **可解释**：每个推荐都有清晰的理由
- **动态调整**：根据学习表现持续优化推荐

## 二、能力触发

### 2.1 触发词
- 「帮我设计课程」「推荐学习路径」
- 「课程规划」「学习建议」「从哪里开始」
- 「我要学 AI」「AI 学习路线」「零基础学 AI」

### 2.2 输入参数

| 参数 | 类型 | 说明 |
|------|------|------|
| audience | enum | 中学生 / 大学生 / 教师 / 企业 |
| goal | string | 学习目标描述 |
| time_available | string | 可用时间：碎片化/每天1h/每天2h/全职学习 |
| current_level | enum | 零基础/入门/进阶/高级 |
| special_needs | string[] | 特殊需求：考试/工作/兴趣/科研 |

## 三、推荐流程

### Phase 1 · 目标确认
```
用户：帮我设计 AI 学习路线
AI：请告诉我你的学习目标是什么？
     ① 应对考试（高考/考研/考证）
     ② 工作提效（职场技能）
     ③ 深入研究（科研/开发）
     ④ 兴趣爱好
     ⑤ 综合提升
```

### Phase 2 · 现状评估
```
AI：请评估你的 AI 基础：
     ① 完全不了解（零基础）
     ② 知道一些概念
     ③ 日常使用过 ChatGPT 等工具
     ④ 有一定编程基础
     ⑤ 已深入学习和实践
```

### Phase 3 · 时间投入
```
AI：你每周能投入多少时间学习？
     ① 碎片时间（每天<30min）
     ② 轻松学习（每天1h）
     ③ 系统学习（每天2-3h）
     ④ 强化训练（每天4h+）
```

### Phase 4 · 生成推荐
- AI 分析输入 → 匹配知识图谱 → 生成个性化路径
- 输出：课程大纲 + 学习计划 + 里程碑

## 四、推荐算法

### 4.1 知识图谱

```javascript
const knowledgeGraph = {
  modules: {
    'A1': { name: 'AI进化历程', prerequisites: [], duration: '2h', difficulty: 1 },
    'A2': { name: 'AI是什么', prerequisites: ['A1'], duration: '3h', difficulty: 1 },
    'A3': { name: '协作哲学', prerequisites: ['A2'], duration: '2h', difficulty: 2 },
    'B1': { name: 'TRAE IDE', prerequisites: ['A2'], duration: '4h', difficulty: 2 },
    'B2': { name: 'SOLO工具', prerequisites: ['B1'], duration: '4h', difficulty: 2 },
    'C1': { name: 'Prompt基础', prerequisites: ['A3'], duration: '3h', difficulty: 2 },
    'C2': { name: '需求拆解', prerequisites: ['C1'], duration: '4h', difficulty: 3 },
    'C3': { name: '验证闭环', prerequisites: ['C2'], duration: '3h', difficulty: 3 },
    'C4': { name: '多Agent', prerequisites: ['C3'], duration: '5h', difficulty: 4 },
    'C5': { name: '沉淀飞轮', prerequisites: ['C4'], duration: '4h', difficulty: 4 },
    'D1': { name: '数据分析', prerequisites: ['C1'], duration: '5h', difficulty: 3 },
    'D2': { name: 'Vibe Coding', prerequisites: ['D1', 'B1'], duration: '6h', difficulty: 4 },
    'E1-E5': { name: '专业应用', prerequisites: ['A3', 'C1'], duration: '10h', difficulty: 4 },
    'F1-F4': { name: '安全伦理', prerequisites: ['A2'], duration: '4h', difficulty: 2 },
    'G1-G3': { name: '最新发展', prerequisites: ['A3', 'E1'], duration: '6h', difficulty: 3 },
  }
};
```

### 4.2 目标-模块映射

```javascript
const goalMapping = {
  '考试': {
    core: ['A1', 'A2', 'A3', 'C1', 'C2', 'F1', 'F2'],
    weight: { '概念类': 1.5, '实践类': 1.0 }
  },
  '工作提效': {
    core: ['A2', 'A3', 'B1', 'B2', 'C1', 'C2'],
    weight: { '实操类': 1.5, '理论类': 0.8 }
  },
  '深入研究': {
    core: ['A1', 'A2', 'A3', 'C1-C5', 'D1', 'D2', 'E1', 'G1-G3'],
    weight: { '深度类': 1.5, '广度类': 1.0 }
  },
  '兴趣爱好': {
    core: ['A1', 'A2', 'A3', 'B1', 'C1', 'F1'],
    weight: { '趣味类': 1.5, '严肃类': 0.8 }
  },
  '综合提升': {
    core: ['A1', 'A2', 'A3', 'B1', 'C1-C5', 'D1', 'F1', 'G1'],
    weight: { '均衡': 1.0 }
  }
};
```

### 4.3 学习计划生成

```javascript
function generatePlan(input) {
  // 1. 确定核心模块
  const coreModules = goalMapping[input.goal].core;
  
  // 2. 计算总时长
  const totalHours = coreModules.reduce(
    (sum, m) => sum + knowledgeGraph.modules[m].duration, 0
  );
  
  // 3. 分配周计划
  const weeklyHours = {
    '碎片时间': 2,
    '轻松学习': 7,
    '系统学习': 15,
    '强化训练': 28
  }[input.time_available];
  
  const weeks = Math.ceil(totalHours / weeklyHours);
  
  // 4. 生成里程碑
  const milestones = [
    { week: 1, modules: ['A1', 'A2'], goal: '理解AI基础' },
    { week: 2, modules: ['A3', 'B1'], goal: '掌握协作思维' },
    // ...
  ];
  
  return { coreModules, totalHours, weeks, milestones };
}
```

## 五、输出格式

### 5.1 课程大纲（Markdown）

```markdown
# 🎯 AI 学习路线图
## 学习者画像
- 目标：工作提效
- 基础：日常使用过 ChatGPT
- 时间：每天 1 小时
- 预计完成：8 周

## 📅 学习计划

### 第一阶段：认知奠基（第 1-2 周）
| 周次 | 模块 | 内容 | 预计时长 | 产出 |
|------|------|------|----------|------|
| Week 1 | A1 AI进化历程 | AI发展史时间轴 | 2h | 课件 |
| Week 1 | A2 AI是什么 | 核心概念辨析 | 3h | 课件 |
| Week 2 | A3 协作哲学 | 人机协作思维 | 2h | 游戏 |

### 第二阶段：工具掌握（第 3-4 周）
| 周次 | 模块 | 内容 | 预计时长 | 产出 |
|------|------|------|----------|------|
| Week 3 | B1 TRAE IDE | 开发环境使用 | 4h | 实操 |
| Week 4 | B2 SOLO工具 | 效率工具实战 | 4h | 项目 |

### 第三阶段：方法进阶（第 5-7 周）
...

## 🏆 里程碑
- [ ] Week 2 完成 AI 认知测试
- [ ] Week 4 完成工具使用测评
- [ ] Week 8 完成综合能力评估

## 📚 推荐资源
- 课件：能力一「p5.js 互动课件」
- 游戏：能力二「冒险闯关」
- 测评：能力四「学习评估」
```

### 5.2 可视化路径图（HTML）

```html
<div id="roadmap">
  <svg viewBox="0 0 800 600">
    <!-- 模块节点 -->
    <circle cx="100" cy="100" r="30" class="module" data-module="A1"/>
    <circle cx="200" cy="100" r="30" class="module" data-module="A2"/>
    <!-- 连线 -->
    <line x1="130" y1="100" x2="170" y2="100" class="edge"/>
    <!-- 里程碑 -->
    <rect x="50" y="200" width="200" height="60" class="milestone"/>
  </svg>
</div>
```

## 六、与能力一/二/三/四联动

| 联动场景 | 说明 |
|----------|------|
| 推荐 → 课件 | 每个模块推荐对应的 p5.js 课件 |
| 推荐 → 游戏 | 推荐与学习阶段匹配的游戏强化 |
| 推荐 → 备课 | 推荐后可一键生成备课包（能力三） |
| 推荐 → 评估 | 完成学习后推荐测评验证效果（能力四） |
