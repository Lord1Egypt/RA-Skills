# 菲菲老师知识网络总控数据库 / Knowledge Network Control Database

*菲菲老师 v3.5 · 学来学去学习社出品*

---

## 📚 全科知识网络总览 / Complete Knowledge Network Overview

### 1.1 学科知识网络架构 / Subject Knowledge Architecture

```
                    ┌─────────────────────────────────────┐
                    │         菲菲老师总指挥中枢            │
                    │    Feifei Commander Center          │
                    └─────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│   理科网络    │◄─────────►│   跨学科枢纽   │◄─────────►│   文科网络    │
│Science Network│           │Interdisciplinary│          │ Liberal Arts  │
└───────────────┘           └───────────────┘           └───────────────┘
        │                             │                             │
   ┌────┴────┐                   ┌────┴────┐                   ┌────┴────┐
   │         │                   │         │                   │         │
   ▼         ▼                   ▼         ▼                   ▼         ▼
┌─────┐  ┌─────┐            ┌─────┐  ┌─────┐            ┌─────┐  ┌─────┐
│数学 │  │物理 │            │数学 │  │化学 │            │语文 │  │英语 │
│Math │  │Phys │            │思维 │  │应用 │            │Chin │  │Eng  │
└─────┘  └─────┘            └─────┘  └─────┘            └─────┘  └─────┘
   │         │                   │         │                   │         │
   ▼         ▼                   ▼         ▼                   ▼         ▼
┌─────┐  ┌─────┐            ┌─────┐  ┌─────┐            ┌─────┐  ┌─────┐
│化学 │  │生物 │            │数据 │  │实验 │            │历史 │  │地理 │
│Chem │  │Bio  │            │分析 │  │报告 │            │Hist │  │Geo  │
└─────┘  └─────┘            └─────┘  └─────┘            └─────┘  └─────┘
```

### 1.2 跨学科连接点汇总表 / Interdisciplinary Connection Points

| 连接类型 / Type | 学科A / Subject A | 知识点 / Topic A | 学科B / Subject B | 知识点 / Topic B | 连接强度 / Strength |
|----------------|------------------|-----------------|------------------|-----------------|-------------------|
| 数学→物理 | 数学 Math | 函数与图像 Functions | 物理 Physics | 运动学图像 Kinematics | ⭐⭐⭐⭐⭐ |
| 数学→物理 | 数学 Math | 三角函数 Trigonometry | 物理 Physics | 力的分解 Force Resolution | ⭐⭐⭐⭐⭐ |
| 数学→化学 | 数学 Math | 比例与方程 Ratios | 化学 Chemistry | 化学计量 Stoichiometry | ⭐⭐⭐⭐ |
| 数学→化学 | 数学 Math | 对数运算 Logarithms | 化学 Chemistry | pH计算 pH Calculation | ⭐⭐⭐⭐ |
| 语文→历史 | 语文 Chinese | 古诗词鉴赏 Poetry | 历史 History | 朝代背景 Dynasties | ⭐⭐⭐⭐⭐ |
| 语文→政治 | 语文 Chinese | 议论文写作 Essays | 政治 Politics | 哲学原理 Philosophy | ⭐⭐⭐⭐ |
| 英语→地理 | 英语 English | 阅读理解 Reading | 地理 Geography | 国家文化 Countries | ⭐⭐⭐⭐ |
| 物理→化学 | 物理 Physics | 分子运动 Molecular Motion | 化学 Chemistry | 化学反应 Reactions | ⭐⭐⭐⭐⭐ |
| 生物→化学 | 生物 Biology | 细胞代谢 Metabolism | 化学 Chemistry | 有机化学 Organic Chem | ⭐⭐⭐⭐ |
| 物理→地理 | 物理 Physics | 光学 Optics | 地理 Geography | 天文 Astronomy | ⭐⭐⭐⭐ |

---

## 👤 学生画像模板 / Student Profile Template

### 2.1 基础画像 / Basic Profile

```json
{
  "student_id": "SAMPLE_001",
  "version": "3.5",
  "last_updated": "2026-04-16",
  
  "basic": {
    "name": "示例学生",
    "name_en": "Sample Student",
    "grade": "八年级 / Grade 8",
    "school": "示例中学",
    "region": "北京市",
    "semester": "2026春季学期",
    
    "textbooks": {
      "math": "人教版A版 / RJ-A",
      "chinese": "统编版 / Unified",
      "english": "人教版 / RJ",
      "physics": "人教版 / RJ",
      "chemistry": "人教版 / RJ",
      "biology": "人教版 / RJ",
      "history": "统编版 / Unified",
      "geography": "人教版 / RJ",
      "politics": "统编版 / Unified"
    }
  },
  
  "mastery": {
    "math": {
      "algebra_basics": 0.85,
      "linear_functions": 0.72,
      "quadratic_equations": 0.60,
      "geometry_basics": 0.78,
      "triangles": 0.65,
      "circles": 0.45,
      "statistics": 0.80,
      "probability": 0.70
    },
    "chinese": {
      "classical_chinese": 0.68,
      "modern_reading": 0.82,
      "writing": 0.75,
      "poetry": 0.60,
      "language_use": 0.85
    },
    "english": {
      "vocabulary": 0.75,
      "grammar": 0.70,
      "reading": 0.78,
      "writing": 0.65,
      "listening": 0.72,
      "speaking": 0.60
    },
    "physics": {
      "mechanics": 0.55,
      "thermodynamics": 0.70,
      "electricity": 0.40,
      "optics": 0.65,
      "waves": 0.50
    },
    "chemistry": {
      "atomic_structure": 0.60,
      "chemical_bonds": 0.55,
      "stoichiometry": 0.45,
      "organic_basics": 0.30
    }
  },
  
  "mastery_summary": {
    "overall": 0.68,
    "strongest_subject": "chinese",
    "weakest_subject": "chemistry",
    "trend": "improving"
  },
  
  "learning_style": {
    "primary": "视觉型 / Visual",
    "secondary": "动手型 / Kinesthetic",
    "visual_score": 0.75,
    "auditory_score": 0.45,
    "kinesthetic_score": 0.65,
    "reading_score": 0.60,
    "preferences": ["图表", "思维导图", "实验操作", "视频讲解"]
  },
  
  "schedule": {
    "weekday_available": "19:00-21:30",
    "weekend_available": "09:00-12:00, 14:00-17:00",
    "preferred_sessions": ["晚间时段", "周末上午"],
    "avg_daily_study_time": 90,
    "max_focus_duration": 35,
    "optimal_break_interval": 25,
    "habits": {
      "morning_review": false,
      "evening_summary": true,
      "weekend_preview": true
    }
  },
  
  "goals": {
    "short_term": {
      "target": "期中考试班级前15名",
      "deadline": "2026-04-25",
      "focus_subjects": ["math", "physics"],
      "target_score_improvement": 15
    },
    "mid_term": {
      "target": "期末考试班级前10名",
      "deadline": "2026-07-10",
      "focus_subjects": ["math", "physics", "chemistry"],
      "target_score_improvement": 25
    },
    "long_term": {
      "target": "中考进入重点高中",
      "deadline": "2027-06",
      "target_school": "市重点高中",
      "target_score": 580
    }
  },
  
  "weakness_alerts": [
    {
      "subject": "physics",
      "topic": "electricity",
      "mastery": 0.40,
      "risk_level": "high",
      "suggested_action": "前置知识检查 → 基础电路原理补习"
    },
    {
      "subject": "chemistry",
      "topic": "stoichiometry",
      "mastery": 0.45,
      "risk_level": "medium",
      "suggested_action": "数学基础检查 → 化学计量专项训练"
    }
  ],
  
  "recent_achievements": [
    {
      "date": "2026-04-10",
      "subject": "math",
      "topic": "linear_functions",
      "improvement": "从0.65提升至0.72",
      "note": "一次函数图像掌握度明显提升"
    }
  ]
}
```

### 2.2 掌握度等级定义 / Mastery Level Definitions

| 等级 / Level | 数值范围 / Range | 状态 / Status | 学习建议 / Recommendation |
|-------------|-----------------|--------------|-------------------------|
| 🔴 薄弱 / Weak | 0.00 - 0.40 | 需要紧急补习 | 前置知识检查 + 基础强化训练 |
| 🟡 一般 / Fair | 0.41 - 0.60 | 需要巩固提升 | 专项练习 + 错题回顾 |
| 🟢 良好 / Good | 0.61 - 0.80 | 保持稳定 | 综合应用 + 适度拓展 |
| 🔵 优秀 / Excellent | 0.81 - 0.95 | 准备进阶 | 难题挑战 + 跨学科整合 |
| ⭐ 精通 / Master | 0.96 - 1.00 | 可以教学 | 费曼输出 + 辅导他人 |

---

## 📖 教材版本对应表 / Textbook Version Mapping

### 3.1 数学 / Mathematics

| 版本 / Version | 适用地区 / Region | 章节索引特点 / Index Features |
|---------------|------------------|-----------------------------|
| 人教版A版 / RJ-A | 全国主流 | 代数→几何→统计→概率 顺序 |
| 人教版B版 / RJ-B | 部分省份 | 螺旋式编排，强调函数主线 |
| 北师大版 / BNU | 北京、广东等 | 数与代数、图形与几何分册 |
| 苏教版 / JS | 江苏 | 注重探究，章节实验活动多 |
| 沪教版 / SH | 上海 | 难度较高，与国际课程接轨 |
| 湘教版 / HN | 湖南 | 强调应用，联系实际生活 |

### 3.2 语文 / Chinese

| 版本 / Version | 适用地区 / Region | 章节索引特点 / Index Features |
|---------------|------------------|-----------------------------|
| 统编版 / Unified | 全国统一 | 人文主题+语文要素双线组元 |

### 3.3 英语 / English

| 版本 / Version | 适用地区 / Region | 单元主题 / Unit Topics |
|---------------|------------------|----------------------|
| 人教版 / RJ | 全国主流 | 话题功能结构任务相结合 |
| 外研社版 / FLTRP | 多地使用 | 模块化设计，强调交际 |
| 北师大版 / BNU | 部分地区 | 语言技能与学习策略并重 |

### 3.4 物理 / Physics

| 版本 / Version | 适用地区 / Region | 章节编排 / Chapter Arrangement |
|---------------|------------------|------------------------------|
| 人教版 / RJ | 全国主流 | 声→光→热→电→力→能量 |
| 沪粤版 / SH-GD | 上海、广东 | 从生活走向物理 |
| 苏科版 / JS-K | 江苏 | 实验探究为主线 |

### 3.5 化学 / Chemistry

| 版本 / Version | 适用地区 / Region | 章节编排 / Chapter Arrangement |
|---------------|------------------|------------------------------|
| 人教版 / RJ | 全国主流 | 原子→分子→化学方程式→酸碱盐 |
| 沪教版 / SH | 上海 | 从化学走进生活 |
| 鲁教版 / SD | 山东 | 活动探究为主线 |

### 3.6 知识点索引编码规范 / Knowledge Index Coding

```
格式：[学科代码]_[类别]_[具体知识点]_[难度级别]

学科代码:
- math = 数学
- chn = 语文
- eng = 英语
- phy = 物理
- chem = 化学
- bio = 生物
- hist = 历史
- geo = 地理
- pol = 政治

类别示例 (数学):
- alg = 代数 (algebra)
- geo = 几何 (geometry)
- func = 函数 (function)
- stat = 统计 (statistics)
- prob = 概率 (probability)

示例:
- math_func_linear_l2 = 数学-函数-一次函数-中等难度
- phy_elec_circuit_l3 = 物理-电学-电路分析-较高难度
- eng_gram_tense_present_l1 = 英语-语法-现在时态-基础难度
```

---

## 🔗 知识网络连接规则 / Knowledge Network Connection Rules

### 4.1 同一学科纵向连接规则 / Intra-subject Vertical Connections

```
 prerequisite(前置) → current(当前) → subsequent(后续)
         ▲                                      │
         └────────── 循环复习 ──────────────────┘
```

**规则1：前置依赖检查 / Prerequisite Check**
```
IF current_mastery < 0.60:
    FOR EACH prerequisite IN current.prerequisites:
        IF prerequisite.mastery < 0.70:
            RETURN "需要先补习前置知识: " + prerequisite.name
            RETURN "推荐路径: " + prerequisite → current
```

**规则2：学习路径生成 / Learning Path Generation**
```
FUNCTION generate_learning_path(target_topic):
    path = []
    to_check = [target_topic]
    
    WHILE to_check NOT EMPTY:
        topic = to_check.pop()
        FOR EACH prereq IN topic.prerequisites:
            IF prereq.mastery < 0.70:
                path.append(prereq)
                to_check.append(prereq)
    
    RETURN reverse(path) + [target_topic]
```

### 4.2 跨学科横向连接规则 / Inter-subject Horizontal Connections

**触发条件 / Trigger Conditions:**
- 当前学科掌握度 ≥ 0.80 时，推荐跨学科拓展
- 前置学科薄弱（< 0.50）时，提示影响范围

**连接类型 / Connection Types:**

| 类型 / Type | 描述 / Description | 示例 / Example |
|------------|-------------------|---------------|
| 工具依赖 Tool Dependency | A学科作为B学科的工具 | 数学→物理计算 |
| 概念映射 Concept Mapping | 相同概念在不同学科 | 能量守恒(物理/化学) |
| 背景知识 Background | A为B提供历史/文化背景 | 历史→古诗词理解 |
| 应用实例 Application | B是A的实际应用 | 数学→金融计算 |

### 4.3 前置知识判断规则 / Prerequisite Judgment Rules

| 当前掌握度 / Current Mastery | 前置要求 / Prerequisite Requirement | 行动 / Action |
|---------------------------|----------------------------------|--------------|
| < 0.40 | 前置 ≥ 0.80 | 🔴 立即补前置基础 |
| 0.40 - 0.55 | 前置 ≥ 0.70 | 🟡 同步补前置 + 当前基础 |
| 0.56 - 0.70 | 前置 ≥ 0.60 | 🟢 可以快速过前置，主攻当前 |
| > 0.70 | 前置 ≥ 0.50 | 🔵 直接进入当前学习 |

---

## 📅 考试日历与复习规划 / Exam Calendar & Review Planning

### 5.1 常规考试周期 / Regular Exam Cycle

```
时间线 Timeline:

9月      10月      11月      12月      1月       3月       4月       5月       6月       7月
 │        │         │         │         │         │         │         │         │         │
 ├────────┼─────────┼─────────┼─────────┤         ├─────────┼─────────┼─────────┼─────────┤
 │ 学期初   │         │         │ 期末复习  │ 寒假     │ 学期初   │         │ 期中复习  │         │ 期末复习  │
 │ 基础夯实 │         │         │ 1-2周   │        │ 基础夯实 │         │ 1-2周   │         │ 2-3周   │
 │        │         │         │ ▼       │        │        │         │ ▼       │         │ ▼       │
 │        │         │         │ 期末考试  │        │        │         │ 期中考试  │         │ 期末考试  │
 │        │         │         │         │        │        │         │         │         │         │
 │        │         │ 期中复习  │         │        │        │         │         │         │         │
 │        │         │ 1-2周    │         │        │        │         │         │         │         │
 │        │         │ ▼       │         │        │        │         │         │         │         │
 │        │         │ 期中考试  │         │        │        │         │         │         │         │
```

### 5.2 中考备考时间线 / High School Entrance Exam Timeline

| 阶段 / Phase | 时间 / Time | 知识目标 / Knowledge Goals | 重点任务 / Key Tasks |
|-------------|------------|--------------------------|-------------------|
| 基础夯实期 | 9月-12月 | 完成全部新知学习 | 建立完整知识网络 |
| 系统复习期 | 1月-3月 | 第一轮全面复习 | 薄弱点诊断与强化 |
| 专题突破期 | 4月-5月 | 重难点专题攻克 | 跨学科整合训练 |
| 冲刺模拟期 | 5月-6月 | 模拟实战演练 | 应试技巧+心态调整 |

### 5.3 复习优先级算法 / Review Priority Algorithm

```
优先级分数 = w1×遗忘系数 + w2×薄弱系数 + w3×考试接近度

其中:
- 遗忘系数 = 1 - exp(-t/T)  (t=距上次复习天数, T=半衰期)
- 薄弱系数 = 1 - mastery_score
- 考试接近度 = 1 / (距考试天数 + 7)
- w1=0.3, w2=0.4, w3=0.3 (默认权重)

优先级 > 0.7: 🔴 紧急复习
优先级 0.5-0.7: 🟡 重点复习  
优先级 0.3-0.5: 🟢 常规复习
优先级 < 0.3: ⚪ 延后复习
```

---

## 💬 家长沟通话术库 / Parent Communication Scripts

### 6.1 成绩提升场景 / Score Improvement Scenario

**开场 / Opening:**
> 家长您好！好消息，孩子这次[数学]进步了[8分]！这和孩子最近坚持每天[25分钟]的专项训练分不开。
> Hi! Good news - [math] score improved by [8 points]! This comes from consistent [25-min] daily practice.

**数据展示 / Data Presentation:**
> 从知识网络来看，[一次函数]的掌握度从[65%]提升到了[82%]，已经进入了"良好"区间。
> From the knowledge map, [linear functions] mastery improved from [65%] to [82%], now in "Good" range.

**下一步 / Next Steps:**
> 建议继续保持这个节奏，同时我们可以开始攻克下一个目标[二次函数]，预计[3周]后能见到效果。
> Let's maintain this pace and start [quadratic functions]. Expected improvement in [3 weeks].

### 6.2 成绩下降场景 / Score Decline Scenario

**开场 / Opening:**
> 家长您好，我注意到孩子这次[物理]有些波动。我们一起看看是什么原因。
> Hi, I noticed some fluctuation in [physics]. Let's analyze the cause.

**诊断分析 / Diagnosis:**
> 从数据看，主要问题在[电学]章节，这其实是[前置知识-电路基础]不够扎实导致的。就像盖房子，地基不稳上层会晃动。
> Data shows the issue is in [electricity], caused by weak [circuit basics]. Like building a house - weak foundation affects upper floors.

**解决方案 / Solution:**
> 我的建议是：先用[1周]时间回炉[电路基础]，再重新学习[电学]。这样虽然多花一点时间，但后续会顺利很多。
> My suggestion: spend [1 week] reviewing [circuit basics], then redo [electricity]. Takes time but ensures smooth progress later.

### 6.3 学习焦虑场景 / Learning Anxiety Scenario

**共情开场 / Empathy Opening:**
> 我理解您担心孩子[临近考试]的状态。其实从大脑科学角度，适度的紧张是正常的，能提升专注力。
> I understand your concern about the upcoming exam. Moderate stress is normal and can enhance focus.

**数据安抚 / Data Reassurance:**
> 看这份知识网络图，孩子其实[80%]的知识点都掌握得不错，[薄弱点]主要集中在[2-3个]章节，完全来得及。
> Looking at this knowledge map, [80%] topics are solid. [Weak points] focus on just [2-3] chapters - totally manageable.

**具体建议 / Specific Advice:**
> 建议家里这样配合：1) 不再问"复习得怎样"，改说"需要我准备什么" 2) 保证睡眠比熬夜重要 3) 每天留[15分钟]让孩子给您讲一道题（费曼学习法）
> Home support tips: 1) Ask "What do you need?" instead of "How's review?" 2) Sleep beats late-night study 3) 15-min daily teaching time (Feynman method)

### 6.4 升学规划场景 / Academic Planning Scenario

**现状分析 / Current Analysis:**
> 根据孩子目前的[八年级上]知识网络，[语文]和[数学]是优势科目，[物理]还有提升空间。
> Based on current [Grade 8] knowledge map, [Chinese] and [Math] are strengths; [Physics] has room to grow.

**目标路径 / Goal Pathway:**
> 如果要冲刺[市重点高中]，建议这样规划：[本学期]主攻[物理电学] + [数学几何]，[寒假]进行[第一轮全面复习]。
> For [key high school] goal: [This semester] focus on [physics electricity] + [math geometry]; [Winter break] for [first round review].

**资源协调 / Resource Coordination:**
> 数学问题我会派[浩云学长]专门辅导，语文交给[小菲学姐]。我会每周给您汇报进度。
> Math goes to [Haoyun tutor], Chinese to [Xiaofei tutor]. Weekly progress reports to you.

---

## 📊 知识网络更新规则 / Knowledge Network Update Rules

### 7.1 掌握度更新公式 / Mastery Update Formula

```
新掌握度 = α × 旧掌握度 + (1-α) × 新测评得分

其中 α = 0.7 (历史权重)

特殊情况:
- 完全掌握新知识点: 初始值 = 首次测评得分 × 0.6
- 复习后提升: 增益系数 = 1 + (复习次数 × 0.05), 上限1.3
- 长期未复习衰减: 衰减率 = 0.95^(未复习天数/30)
```

### 7.2 触发更新的事件 / Update Triggers

| 事件 / Event | 更新类型 / Update Type | 影响范围 / Scope |
|------------|---------------------|----------------|
| 完成练习题 | mastery值调整 | 单个知识点 |
| 通过单元测试 | mastery值提升 + 解锁后续 | 当前+后续知识点 |
| 费曼输出合格 | mastery值提升 + 稳定性标记 | 单个知识点 |
| 发现知识盲区 | 标记薄弱点 + 影响前置检查 | 相关前置链 |
| 跨学科应用成功 | 双向连接强化 | 相关学科知识点 |

### 7.3 数据持久化规则 / Data Persistence

```
自动保存触发:
- 每次学习会话结束
- 每日23:00
- 重要里程碑(测试通过、阶段完成)

备份策略:
- 本地: 每次更新后立即写入
- 云端: 每日同步一次
- 历史版本: 保留最近30天
```

---

*菲菲老师 v3.5 Knowledge Base | 学来学去学习社出品*
*最后更新 / Last Updated: 2026-04-16*
