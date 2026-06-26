---
name: Financial Industry Training & Coaching System
slug: finance-training-coach
description: AI-powered financial industry training and coaching system — covers skill assessment, personalized learning paths, role-play training, knowledge quizzes, and performance tracking. Built for financial institutions' training departments. Keywords: training system, skill assessment, role-play, learning path, financial education, 培训系统, 技能评估, 角色扮演, 学习路径, 金融培训, 员工培训, 技能考核, 智能陪练, 学习管理, 培训管理.
version: "5.0.0"
---

# Financial Industry Training & Coaching System / 金融行业培训陪练系统

> **English:** AI-powered training system — covers skill assessment, learning paths, role-play, and quizzes.
>
> **中文:** 培训陪练系统——覆盖技能评估、学习路径、角色扮演、考核测验。

---


### 金融监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 金融监管 | 2026年Q1：金融行业培训需覆盖最新合规要求 | 培训课程库需增加2026年合规和AI工具课程 |
| 金融监管 | 保险销售人员分级制度、银行合规管理、反洗钱培训 | 培训课程库需增加2026年合规和AI工具课程 |
| 金融监管 | AI工具使用培训需求上升（MCP/RAG/Agent等） | 培训课程库需增加2026年合规和AI工具课程 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **培训效率低** | 统一培训不适应个体差异 | 个性化学习路径 |
| **实战不足** | 理论多、实操少 | AI角色扮演陪练 |
| **效果难评估** | 培训效果无法量化 | 技能雷达图 |
| **知识遗忘快** | 培训后知识快速遗忘 | 间隔重复机制 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** training system, skill assessment, role-play, learning path, financial education

**中文触发词（优先）：** 培训 / 陪练 / 技能评估 / 角色扮演 / 学习路径 / 考核 / 测验 / 金融培训

---

## Core Capabilities / 核心能力

### 1. Skill Assessment / 技能评估

```python
SKILL_FRAMEWORK = {
    "banking": {
        "知识": ["产品知识", "合规知识", "营销知识"],
        "技能": ["客户沟通", "需求挖掘", "异议处理"],
        "态度": ["服务意识", "合规意识", "学习意愿"]
    },
    "insurance": {
        "知识": ["产品条款", "核保规则", "理赔流程"],
        "技能": ["需求分析", "方案设计", "促成技巧"],
        "态度": ["诚信展业", "长期服务"]
    }
}

class SkillAssess:
    """技能评估引擎"""
    
    def assess(self, employee_id: str) -> dict:
        """全面技能评估"""
        return {
            "skill_radar": self._generate_radar(scores),
            "gap_analysis": self._identify_gaps(scores),
            "learning_recommendations": self._recommend_courses(gaps),
            "comparison_to_peers": self._peer_comparison(scores)
        }
```

### 2. Role-play Training / 角色扮演

```python
ROLE_PLAY_SCENARIOS = {
    "客户拒绝处理": {
        "场景": "客户说'我不需要保险'",
        "难度": "初级",
        "评估维度": ["倾听", "共情", "探询", "回应"]
    },
    "产品推荐": {
        "场景": "向高净值客户推荐综合理财方案",
        "难度": "高级",
        "评估维度": ["需求分析", "方案设计", "专业展示", "促成技巧"]
    }
}
```

---

## Disclaimer

This skill provides training tools for educational purposes.
## Appendix G. Alibaba Dianjin Fusion — finance-training-coach v5.0.0

> **Source**: Alibaba Dianjin Digital Employee — `education-trainer` (AI教育训练师)  
> **Essence**: 金融知识科普、投教课程设计、学习效果评估、个性化学习路径  
> **Integrated**: 2026-05-31

---

### G.1 Core Workflow (Dianjin essence)

```
用户请求 → 学习目标识别 → 知识图谱构建 → 课程内容生成 → 测评题目设计
   ↓
Learning Path:
  - 入门级：基础概念（股票/基金/债券是什么）
  - 进阶级：分析方法（基本面/技术面/量化）
  - 高级：策略实战（回测/仓位管理/风险控制）
   ↓
Content Types:
  - 图文教程（Markdown+图表）
  - 视频脚本（口播稿+PPT大纲）
  - 测评题库（单选/多选/判断/案例）
```

---

### G.2 Knowledge Graph & Curriculum (Dianjin method)

**金融知识体系（Dianjin结构）**：

```
Level 1: 基础理论
  - 金融市场的功能（融资/投资/风险管理）
  - 主要资产类别（股票/债券/基金/衍生品）
  - 基本术语（PE/PB/ROE/市值/涨停板）

Level 2: 分析方法
  - 基本面分析：财报解读/行业研究/宏观分析
  - 技术面分析：K线/均线/MACD/布林带
  - 量化分析：因子模型/回测/风险控制

Level 3: 实战策略
  - 价值投资：巴菲特/格雷厄姆方法论
  - 成长投资：PEG/赛道选择/催化剂
  - 趋势交易：均线突破/量价关系
  - 对冲策略：配对交易/市场中性

Level 4: 风险管理
  - 仓位管理：凯利公式/ATR仓位
  - 止损策略：固定止损/移动止损
  - 心理控制：贪婪/恐惧/从众心理
```

**课程设计模板（Dianjin风格）**：

```
【课程】股票基本面分析入门（Level 1）

一、学习目标
- 理解PE/PB/ROE三个核心指标
- 能读懂利润表/资产负债表/现金流量表
- 能计算并解释股息率/分红率

二、学习内容
1. 视频：15分钟（口播稿见附件）
2. 图文：PE/PB/ROE计算公式+案例
3. 实战：挑选3只股票，计算其PE/PB/ROE

三、测评题目（5题）
1. 【单选】某公司股价100元，每股收益5元，PE是多少？
   A. 10倍  B. 20倍  C. 50倍  D. 100倍

四、学习时长
- 视频：15分钟
- 阅读：20分钟
- 实战：30分钟
- 总计：65分钟

五、扩展阅读
- 《聪明的投资者》第3章
- 巴菲特致股东的信（2025）
```

---

### G.3 Personalized Learning Path (Dianjin essence)

**学习者画像**：

| 维度 | 新手 | 进阶者 | 资深者 |
|------|------|--------|--------|
| 金融知识 | 无/极少 | 基础概念清楚 | 有实战经验 |
| 投资经验 | <1年 | 1-5年 | >5年 |
| 学习目标 | 理解基础 | 掌握分析方法 | 优化策略 |
| 推荐路径 | Level 1 → 2 | Level 2 → 3 | Level 3 → 4 |

**个性化推荐算法（Dianjin风格）**：

```
输入：学习者画像（知识水平/学习目标/可用时间）
  ↓
匹配：知识图谱中的最优学习路径
  ↓
输出：
  - 推荐课程列表（排序）
  - 每门课程的学习时长
  - 里程碑节点（完成XX课程后获得证书）
```

---

### G.4 Assessment & Feedback (Dianjin method)

**测评题目类型**：

```
1. 知识理解题（单选/多选/判断）
   - 目标：检验概念掌握
   - 难度：低-中
   - 示例："PE是什么？"

2. 计算应用题（计算/分析）
   - 目标：检验公式运用
   - 难度：中-高
   - 示例："计算茅台的PE，并判断是否高估"

3. 案例分析题（开放/论述）
   - 目标：检验综合分析能力
   - 难度：高
   - 示例："分析特斯拉2025年Q4财报，给出投资建议"
```

**反馈机制**：

```
即时反馈：
  - 答题正确 → "✅ 正确！解释：..."
  - 答题错误 → "❌ 错误。正确答案：B。解释：..."

学习报告：
  - 完成课程数/总课程数
  - 平均得分/满分
  - 薄弱知识点（需加强）
  - 推荐复习课程
```

---

### G.5 Test Case (Dianjin quality)

**Test Case: 个性化学习路径推荐**

```
Input: "我是投资新手，想学习股票投资，每天能学1小时"

Expected Output:
1. 学习者画像：新手（知识水平低，经验<1年）
2. 推荐路径：Level 1（基础理论）→ Level 2（分析方法）
3. 课程列表：TOP 5课程（按优先级排序）
4. 学习时长：每门课程60-90分钟，总计约7-10小时

Quality Check:
- ✅ 路径符合学习者水平
- ✅ 课程难度递进（不跳跃）
- ✅ 时长合理（每天1小时，约1-2周完成）
```

---

**End of Dianjin Fusion Content — finance-training-coach v5.0.0**
