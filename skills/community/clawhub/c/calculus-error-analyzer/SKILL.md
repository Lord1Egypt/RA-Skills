# calculus-error-analyzer - 高等数学错题深度分析Skill

## 概述
专门针对高等数学错题的深度分析系统，通过错误模式识别、知识点关联分析、学习路径优化，实现从错题到学习改进的智能转化。

## 核心功能

### 1. 错误模式深度挖掘
- **错误类型分类**: 概念错误、计算错误、逻辑错误、理解偏差
- **错误根源分析**: 追溯错误的知识点根源和思维误区
- **错误模式聚类**: 发现学生个性化的错误模式
- **错误演变追踪**: 分析错误随时间的演变规律

### 2. 个性化错题本生成
- **智能错题归类**: 按知识点、错误类型、难度自动分类
- **错题标签系统**: 多维标签标记错题特征
- **错题难度评估**: 评估错题的典型性和重要性
- **错题复习计划**: 基于遗忘曲线的智能复习安排

### 3. 学习路径优化
- **薄弱点诊断**: 精准定位知识体系中的薄弱环节
- **学习路径推荐**: 基于错误分析的个性化学习路径
- **干预策略生成**: 针对不同错误类型的教学干预
- **进步预测**: 基于错误纠正的进步可能性预测

## 工具定义

### analyze_error_patterns
深度分析错误模式

**参数**：
- `error_data` (array): 错误数据列表
- `analysis_level` (string): 分析级别，"basic"、"standard"、"deep"
- `include_causes` (boolean): 是否包含错误原因分析
- `generate_solutions` (boolean): 是否生成解决方案

**返回**：
```json
{
  "analysis_id": "ea_001",
  "summary": {
    "total_errors": 24,
    "unique_error_types": 8,
    "most_common_error": "积分公式记错",
    "error_frequency": 6
  },
  "error_categories": [
    {
      "category": "概念理解错误",
      "count": 10,
      "percentage": 41.7,
      "subtypes": [
        {
          "subtype": "定理条件混淆",
          "examples": ["误用罗尔定理条件", "拉格朗日定理应用错误"],
          "root_cause": "对定理成立条件理解不深",
          "recommendation": "重点复习定理的几何意义和适用条件"
        }
      ]
    },
    {
      "category": "计算执行错误",
      "count": 8,
      "percentage": 33.3,
      "subtypes": [
        {
          "subtype": "符号运算错误",
          "examples": ["正负号错误", "括号展开错误"],
          "root_cause": "计算粗心，检查习惯不好",
          "recommendation": "建立计算检查清单，放慢计算速度"
        }
      ]
    }
  ],
  "knowledge_gaps": [
    {
      "topic": "微分中值定理",
      "gap_level": "严重",
      "affected_questions": 5,
      "prerequisite_topics": ["函数连续性", "导数概念"],
      "remediation_path": [
        "第一步：复习函数连续性定义",
        "第二步：理解导数几何意义",
        "第三步：学习中值定理证明",
        "第四步：练习典型应用题"
      ]
    }
  ],
  "personalized_insights": {
    "learning_style_issues": "倾向于记忆公式而非理解推导",
    "thinking_patterns": "在证明题中容易跳过关键步骤",
    "time_management": "复杂题目后期容易出现计算错误",
    "confidence_level": "中等偏下，需要成功体验提升"
  }
}
```

### generate_personalized_error_book
生成个性化错题本

**参数**：
- `student_id` (string): 学生ID
- `time_range` (string): 时间范围，"week"、"month"、"all"
- `organization_method` (string): 组织方式，"by_topic"、"by_error_type"、"by_difficulty"
- `include_explanations` (boolean): 是否包含详细解析

**返回**：
```json
{
  "error_book_id": "eb_001",
  "student_info": {
    "student_id": "stu001",
    "name": "张三",
    "total_errors_collected": 42,
    "time_period": "2026-03-01 至 2026-04-15"
  },
  "error_book_structure": {
    "sections": [
      {
        "section_title": "第一章 函数与极限",
        "error_count": 8,
        "priority": "高",
        "topics": [
          {
            "topic": "函数极限计算",
            "error_examples": [
              {
                "original_question": "求lim(x→0) (sinx/x)",
                "student_answer": "0",
                "correct_answer": "1",
                "error_type": "重要极限记错",
                "detailed_explanation": "这是第一个重要极限，值为1...",
                "similar_questions": [
                  "lim(x→0) (tanx/x)",
                  "lim(x→0) (arcsinx/x)"
                ],
                "learning_resources": [
                  {
                    "type": "video",
                    "title": "重要极限的几何解释",
                    "url": "https://example.com/video1"
                  }
                ]
              }
            ],
            "mastery_exercises": [
              {
                "exercise": "计算lim(x→0) (1-cosx)/x²",
                "hint": "使用半角公式或洛必达法则",
                "answer": "1/2"
              }
            ]
          }
        ]
      }
    ]
  },
  "review_schedule": {
    "spaced_repetition": [
      {
        "review_date": "2026-04-16",
        "topics": ["函数极限", "导数定义"],
        "estimated_time": 30
      },
      {
        "review_date": "2026-04-20",
        "topics": ["微分中值定理"],
        "estimated_time": 45
      }
    ],
    "review_strategies": {
      "immediate": "24小时内复习新错题",
      "short_term": "3天后第二次复习",
      "long_term": "每周系统性回顾"
    }
  },
  "progress_tracking": {
    "error_reduction_rate": 35.2,
    "mastery_improvement": [
      {"topic": "导数计算", "from": 65, "to": 82},
      {"topic": "积分应用", "from": 58, "to": 71}
    ],
    "confidence_change": "显著提升"
  }
}
```

### recommend_intervention_strategies
推荐教学干预策略

**参数**：
- `error_analysis` (object): 错误分析结果
- `student_profile` (object): 学生画像
- `intervention_type` (string): 干预类型，"immediate"、"short_term"、"long_term"
- `available_resources` (array): 可用教学资源

**返回**：
```json
{
  "intervention_plan_id": "ip_001",
  "student_profile_summary": {
    "learning_style": "视觉型学习者",
    "motivation_level": "中等",
    "self_efficacy": "需要提升",
    "time_availability": "每周5-7小时"
  },
  "immediate_interventions": [
    {
      "strategy": "概念澄清会议",
      "description": "一对一讲解微分中值定理的几何意义",
      "duration": 30,
      "materials": [
        "GeoGebra动态演示文件",
        "定理证明动画视频"
      ],
      "expected_outcome": "理解定理条件和几何解释"
    },
    {
      "strategy": "计算规范化训练",
      "description": "建立标准计算步骤检查表",
      "duration": 20,
      "materials": ["计算检查清单", "典型错误案例集"],
      "expected_outcome": "减少符号运算错误50%"
    }
  ],
  "short_term_strategies": [
    {
      "strategy": "错题重做计划",
      "description": "系统性重做最近10个错题",
      "schedule": "每天2题，连续5天",
      "monitoring": "每天提交重做结果",
      "success_criteria": "正确率达到90%"
    },
    {
      "strategy": "同伴学习小组",
      "description": "与同水平同学组成学习小组",
      "activities": ["互相批改作业", "讨论解题思路", "分享学习资源"],
      "frequency": "每周2次，每次60分钟"
    }
  ],
  "long_term_development": [
    {
      "strategy": "数学思维训练",
      "description": "培养严谨的数学推理习惯",
      "activities": [
        "每周完成1道证明题",
        "学习数学证明写作规范",
        "阅读数学史相关材料"
      ],
      "timeline": "8周计划",
      "milestones": [
        "第2周：掌握基本证明结构",
        "第4周：能独立完成中等难度证明",
        "第8周：形成系统的数学思维"
      ]
    }
  ],
  "resource_recommendations": {
    "targeted_practice": [
      {
        "resource_type": "练习册",
        "name": "微分中值定理专项练习",
        "difficulty": "基础到提高",
        "estimated_time": "4小时"
      }
    ],
    "conceptual_understanding": [
      {
        "resource_type": "视频课程",
        "name": "微积分核心概念可视化",
        "duration": "3小时",
        "focus": "几何直观理解"
      }
    ],
    "motivational": [
      {
        "resource_type": "阅读材料",
        "name": "数学之美：从微积分看世界",
        "purpose": "激发学习兴趣，理解数学应用"
      }
    ]
  },
  "monitoring_and_evaluation": {
    "key_metrics": [
      "错题重做正确率",
      "同类错误重复率",
      "学习时间投入",
      "自我效能感变化"
    ],
    "evaluation_schedule": [
      {"time": "1周后", "focus": "计算错误减少情况"},
      {"time": "2周后", "focus": "概念理解提升"},
      {"time": "1月后", "focus": "综合能力进步"}
    ],
    "adjustment_criteria": "如果2周后进步小于20%，调整干预策略"
  }
}
```

## 使用示例

### 示例1：深度错误模式分析
```bash
# 分析学生错误模式
openclaw skill calculus-error-analyzer analyze_error_patterns \
  --error-data '[{"question":"求导数","error":"链式法则应用错误"},{"question":"计算积分","error":"积分公式记错"}]' \
  --analysis-level "deep" \
  --include-causes true \
  --generate-solutions true
```

### 示例2：生成个性化错题本
```bash
# 为学生生成月度错题本
openclaw skill calculus-error-analyzer generate_personalized_error_book \
  --student-id "stu001" \
  --time-range "month" \
  --organization-method "by_topic" \
  --include-explanations true
```

### 示例3：推荐干预策略
```bash
# 基于错误分析推荐教学干预
openclaw skill calculus-error-analyzer recommend_intervention_strategies \
  --error-analysis '{"error_categories":[{"category":"概念错误","count":10}]}' \
  --student-profile '{"learning_style":"visual","motivation":"medium"}' \
  --intervention-type "comprehensive" \
  --available-resources '["geogebra","video_course","practice_sheets"]'
```

## 错误分析模型

### 错误分类体系
```python
class ErrorTaxonomy:
    """高等数学错误分类体系"""
    
    def __init__(self):
        self.categories = {
            'conceptual_errors': {
                'definition_misunderstanding': {
                    'description': '概念定义理解错误',
                    'examples': ['极限定义混淆', '导数概念误解'],
                    'severity': '高'
                },
                'theorem_misapplication': {
                    'description': '定理条件或应用错误',
                    'examples': ['误用中值定理', '洛必达法则滥用'],
                    'severity': '高'
                },
                'logical_fallacies': {
                    'description': '逻辑推理错误',
                    'examples': ['循环论证', '充分必要条件混淆'],
                    'severity': '中'
                }
            },
            'computational_errors': {
                'algebraic_mistakes': {
                    'description': '代数运算错误',
                    'examples': ['符号错误', '因式分解错误'],
                    'severity': '中'
                },
                'formula_misremembering': {
                    'description': '公式记忆错误',
                    'examples': ['积分公式记错', '导数公式错误'],
                    'severity': '中'
                },
                'procedural_errors': {
                    'description': '计算步骤错误',
                    'examples': ['积分上下限错误', '变量替换错误'],
                    'severity': '低'
                }
            },
            'strategic_errors': {
                'method_selection': {
                    'description': '解题方法选择不当',
                    'examples': ['复杂方法代替简单方法', '方法不适用'],
                    'severity': '中'
                },
                'problem_analysis': {
                    'description': '问题分析不充分',
                    'examples': ['未识别关键条件', '误解问题要求'],
                    'severity': '高'
                }
            }
        }
    
    def classify_error(self, error_description, context):
        """分类错误类型"""
        for category, subcategories in self.categories.items():
            for subtype, config in subcategories.items():
                if self.matches_pattern(error_description, config['examples']):
                    return {
                        'category': category,
                        'subtype': subtype,
                        'description': config['description'],
                        'severity': config['severity'],
                        'confidence': self.calculate_confidence(error_description, config)
                    }
        return {'category': 'unknown', 'subtype': 'other'}
```

### 错误根源分析
```python
class RootCauseAnalyzer:
    """错误根源分析引擎"""
    
    def analyze_root_cause(self, error_instance, student_history):
        """分析错误根本原因"""
        causes = []
        
        # 1. 知识点缺陷分析
        knowledge_gaps = self.identify_knowledge_gaps(error_instance)
        if knowledge_gaps:
            causes.append({
                'type': 'knowledge_gap',
                'description': '相关知识点掌握不足',
                'specific_gaps': knowledge_gaps,
                'evidence': self.find_evidence(student_history, knowledge_gaps)
            })
        
        # 2. 思维习惯分析
        thinking_patterns = self.analyze_thinking_patterns(error_instance, student_history)
        if thinking_patterns:
            causes.append({
                'type': 'thinking_habit',
                'description': '不良思维习惯',
                'patterns': thinking_patterns,
                'frequency': self.calculate_frequency(student_history, thinking_patterns)
            })
        
        # 3. 心理因素分析
        psychological_factors = self.assess_psychological_factors(student_history)
        if psychological_factors:
            causes.append({
                'type': 'psychological',
                'description': '心理因素影响',
                'factors': psychological_factors,
                'impact_level': self.estimate_impact(psychological_factors)
            })
        
        # 4. 学习策略分析
        strategy_issues = self.evaluate_learning_strategies(student_history)
        if strategy_issues:
            causes.append({
                'type': 'strategy',
                'description': '学习策略不当',
                'issues': strategy_issues,
                'recommendations': self.suggest_strategy_improvements(strategy_issues)
            })
        
        return {
            'primary_cause': self.identify_primary_cause(causes),
            'contributing_factors': causes,
            'interdependencies': self.analyze_interdependencies(causes)
        }
```

### 错题本智能生成
```python
class ErrorBookGenerator:
    """个性化错题本生成器"""
    
    def __init__(self):
        self.organizers = {
            'by_topic': TopicOrganizer(),
            'by_error_type': ErrorTypeOrganizer(),
            'by_difficulty': DifficultyOrganizer(),
            'by_priority': PriorityOrganizer()
        }
        
    def generate_error_book(self, student_errors, organization_method='by_topic'):
        """生成错题本"""
        organizer = self.organizers.get(organization_method, self.organizers['by_topic'])
        
        # 1. 错题分类组织
        organized_errors = organizer.organize(student_errors)
        
        # 2. 添加详细解析
        enriched_errors = self.enrich_with_explanations(organized_errors)
        
        # 3. 生成学习资源链接
        errors_with_resources = self.link_learning_resources(enriched_errors)
        
        # 4. 设计复习计划
        review_plan = self.create_review_plan(errors_with_resources)
        
        # 5. 生成错题本文档
        error_book = self.compile_error_book(
            errors_with_resources, 
            review_plan
        )
        
        return error_book
    
    def create_review_plan(self, errors, algorithm='spaced_repetition'):
        """基于遗忘曲线创建复习计划"""
        if algorithm == 'spaced_repetition':
            plan = SpacedRepetitionScheduler().schedule(errors)
        elif algorithm == 'adaptive':
            plan = AdaptiveScheduler().schedule(errors)
        else:
            plan = FixedIntervalScheduler().schedule(errors)
        
        return {
            'schedule': plan['intervals'],
            'estimated_time': plan['total_time'],
            'success_criteria': self.define_success_criteria(errors),
            'adjustment_rules': self.get_adjustment_rules()
        }
```

## 与现有Skill集成

### 集成calculus-learning-anal