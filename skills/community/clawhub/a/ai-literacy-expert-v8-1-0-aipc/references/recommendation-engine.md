> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

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

### 4.4 增强推荐算法（V7 新增）

> 在基础规则匹配之上，引入三大增强机制，使推荐从"静态规则"升级为"动态自适应"。

#### 4.4.1 表现加权评分（Performance-Weighted Scoring）

追踪学生在每个模块的实际表现，用得分率动态调整推荐优先级。

```javascript
// 每个模块维护一个表现记录
const performanceLog = {
  'A1': { attempts: 3, avgScore: 0.85, lastScore: 0.90 },
  'C1': { attempts: 2, avgScore: 0.45, lastScore: 0.40 },
  // ...
};

// 计算推荐优先级分数（越高越需要推荐学习）
function calcPriorityScore(moduleId) {
  const perf = performanceLog[moduleId];
  if (!perf) return 1.0; // 未学过，默认高优先级
  
  const scoreRate = perf.avgScore;
  const trend = perf.lastScore - perf.avgScore; // 正=在进步，负=在退步
  
  // 得分率越低，优先级越高；退步趋势进一步提升优先级
  let priority = (1 - scoreRate) * 0.7;
  if (trend < -0.1) priority += 0.2; // 退步中，额外加权
  if (trend > 0.1) priority -= 0.1;  // 进步中，适当降低
  
  return Math.max(0, Math.min(1, priority));
}
```

#### 4.4.2 间隔重复整合（Spaced Repetition Integration）

基于艾宾浩斯遗忘曲线，在学习后特定时间点触发复习推荐。

```javascript
// 艾宾浩斯遗忘曲线参数
const forgettingCurve = {
  // 复习间隔（天）：1, 3, 7, 14, 30
  intervals: [1, 3, 7, 14, 30],
  // 对应记忆保持率阈值
  retentionThresholds: [0.9, 0.8, 0.7, 0.6, 0.5]
};

// 计算每个模块的记忆衰减度
function calcRetention(moduleId) {
  const lastStudied = getLastStudiedDate(moduleId); // 上次学习日期
  const daysSince = daysBetween(lastStudied, today());
  const reviewCount = getReviewCount(moduleId); // 已复习次数
  
  // 基础衰减率（艾宾浩斯公式简化版）
  const stability = 1 + reviewCount * 0.5; // 复习次数越多，记忆越稳定
  const retention = Math.exp(-daysSince / (stability * 2));
  
  return {
    retention: retention,           // 当前记忆保持率 (0-1)
    daysSince: daysSince,           // 距上次学习天数
    nextReviewDue: isReviewDue(moduleId, daysSince, reviewCount),
    urgency: 1 - retention          // 遗忘紧迫度（越高越需要复习）
  };
}

// 判断是否需要复习
function isReviewDue(moduleId, daysSince, reviewCount) {
  const intervalIndex = Math.min(reviewCount, forgettingCurve.intervals.length - 1);
  const targetInterval = forgettingCurve.intervals[intervalIndex];
  return daysSince >= targetInterval;
}
```

#### 4.4.3 学习风格适配（Learning Style Adaptation）

追踪学生的学习偏好，自动调整推荐资源的格式。

```javascript
// 学习风格追踪
const learningStyleProfile = {
  preferredFormat: {
    'courseware': 0,   // 课件得分
    'game': 0,         // 游戏得分
    'reading': 0,      // 阅读材料得分
    'video': 0         // 视频得分
  },
  engagementScores: {},  // 每种格式的实际参与度
  completionRates: {}    // 每种格式的完成率
};

// 根据历史表现更新学习风格
function updateLearningStyle(moduleId, format, score, engagement, completed) {
  const profile = learningStyleProfile;
  // 加权移动平均（新数据权重 0.3）
  profile.preferredFormat[format] = 
    profile.preferredFormat[format] * 0.7 + score * 0.3;
  
  if (completed) {
    profile.completionRates[format] = 
      (profile.completionRates[format] || 0) * 0.7 + 1.0 * 0.3;
  }
}

// 获取推荐资源格式
function getRecommendedFormat(moduleId) {
  const profile = learningStyleProfile;
  const formats = Object.entries(profile.preferredFormat);
  
  // 如果某格式完成率低，尝试切换（避免"只看不练"）
  const lowCompletion = formats.find(([f, s]) => 
    (profile.completionRates[f] || 1) < 0.5
  );
  if (lowCompletion) return lowCompletion[0];
  
  // 否则推荐得分最高的格式
  formats.sort((a, b) => b[1] - a[1]);
  return formats[0][0];
}
```

#### 4.4.4 增强推荐算法伪代码（综合）

```javascript
function enhancedRecommend(input, assessmentResults) {
  // Step 1: 基础推荐（规则匹配，同 §4.2-4.3）
  const basePlan = generatePlan(input);
  
  // Step 2: 表现加权调整
  basePlan.modules.forEach(m => {
    m.priorityScore = calcPriorityScore(m.id);
  });
  
  // Step 3: 间隔重复检查
  basePlan.modules.forEach(m => {
    m.retention = calcRetention(m.id);
    if (m.retention.nextReviewDue) {
      m.priorityScore += m.retention.urgency * 0.3; // 复习需求加权
      m.isReview = true;
    }
  });
  
  // Step 4: 学习风格适配
  basePlan.modules.forEach(m => {
    m.recommendedFormat = getRecommendedFormat(m.id);
    // 根据格式筛选可用资源
    m.resources = filterResourcesByFormat(m.id, m.recommendedFormat);
  });
  
  // Step 5: 综合排序
  basePlan.modules.sort((a, b) => {
    // 前置条件优先
    if (hasPrerequisite(b, a)) return -1;
    if (hasPrerequisite(a, b)) return 1;
    // 综合优先级 = 表现需求(40%) + 遗忘紧迫(30%) + 目标匹配(30%)
    const scoreA = a.priorityScore * 0.4 + (a.retention?.urgency || 0) * 0.3 + a.goalMatch * 0.3;
    const scoreB = b.priorityScore * 0.4 + (b.retention?.urgency || 0) * 0.3 + b.goalMatch * 0.3;
    return scoreB - scoreA;
  });
  
  return basePlan;
}
```

### 4.5 评估闭环联动（V7 新增）

> 推荐引擎消费评估结果，动态调整学习路径。详见 `references/assessment-guide.md` §十一"评估-推荐闭环规范"。

#### 评估结果消费流程

```
评估完成 → 生成诊断报告 → 推荐引擎接收 → 调整路径 → 学习者执行 → 再评估验证
```

| 评估输出 | 推荐引擎动作 | 调整策略 |
|----------|-------------|----------|
| 模块得分率 < 60% | 将该模块插入学习路径前端 | 优先级提升，增加练习量 |
| 特定知识点错误率 > 50% | 推荐该知识点的专项课件 + 游戏 | 精准定位，资源匹配 |
| 认知层次集中在 L1-L2 | 推荐 L3+ 应用类资源 | 提升难度，促进迁移 |
| 答题时间异常短且正确率低 | 推荐基础复习而非进阶内容 | 判断为"假性完成"，回退巩固 |
| 连续两次评估无改善 | 切换推荐资源类型（如课件→游戏） | 尝试不同学习通道 |

#### 闭环数据接口

```javascript
// 推荐引擎接收评估结果的接口
function onAssessmentComplete(assessmentResult) {
  // assessmentResult 结构见 assessment-guide.md §11.5
  const { weakPoints, overallScore, timeProfile, moduleScores } = assessmentResult;
  
  // 1. 更新表现记录
  Object.entries(moduleScores).forEach(([moduleId, score]) => {
    updatePerformanceLog(moduleId, score);
  });
  
  // 2. 生成增强推荐
  const updatedPlan = enhancedRecommend(currentUserInput, assessmentResult);
  
  // 3. 推送新路径
  pushUpdatedPlan(updatedPlan);
  
  // 4. 设置再评估提醒
  scheduleRetest(weakPoints, estimatedCompletionDate(updatedPlan));
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
