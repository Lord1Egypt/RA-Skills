# calculus-learning-analytics - 高等数学学情数据分析Skill

## 概述
基于作业批改数据的学情分析系统，构建学生能力画像、班级整体表现看板、教学建议引擎。实现从数据收集到教学决策的完整闭环。

## 核心功能

### 1. 多维度数据看板
- **班级概览**: 提交率、平均分、知识点掌握热力图
- **学生画像**: 个人能力雷达图、进步趋势、薄弱点分析
- **教学洞察**: 错误模式聚类、教学效果评估、资源使用分析

### 2. 智能分析引擎
- **能力维度建模**: 概念理解、计算能力、逻辑推理三大维度
- **知识点关联分析**: 发现知识点之间的依赖关系
- **预测模型**: 预测学生未来表现和风险预警
- **个性化推荐**: 基于薄弱点的针对性练习推荐

### 3. 教学决策支持
- **课堂重点建议**: 基于错误集中度推荐讲解重点
- **分层教学方案**: 为不同水平学生设计教学策略
- **资源优化分配**: 智能推荐教学资源和辅导时间

## 工具定义

### generate_class_dashboard
生成班级学情数据看板

**参数**：
- `class_id` (string): 班级ID
- `time_range` (string): 时间范围，"week"、"month"、"semester"
- `include_metrics` (array): 包含的指标列表
- `visualization_type` (string): 可视化类型，"summary"、"detailed"、"export"

**返回**：
```json
{
  "dashboard_id": "db_20260416_001",
  "class_info": {
    "class_id": "math2024-01",
    "student_count": 45,
    "time_range": "2026-04-01 至 2026-04-15"
  },
  "overview_metrics": {
    "submission_rate": 92.3,
    "average_score": 78.5,
    "completion_rate": 85.7,
    "improvement_rate": 12.3
  },
  "knowledge_heatmap": [
    {
      "topic": "导数计算",
      "mastery_rate": 88.2,
      "common_errors": ["链式法则", "隐函数求导"]
    },
    {
      "topic": "定积分应用",
      "mastery_rate": 72.5,
      "common_errors": ["积分上下限", "面积计算"]
    }
  ],
  "ability_radar": {
    "concept_understanding": 75.3,
    "computation_ability": 82.1,
    "logical_reasoning": 68.7,
    "problem_solving": 71.2,
    "mathematical_modeling": 65.4
  },
  "visualizations": {
    "heatmap_url": "https://example.com/heatmap.png",
    "radar_chart_url": "https://example.com/radar.png",
    "trend_chart_url": "https://example.com/trend.png"
  }
}
```

### analyze_student_profile
深度分析学生个人学习画像

**参数**：
- `student_id` (string): 学生ID
- `analysis_depth` (string): 分析深度，"basic"、"standard"、"deep"
- `include_comparison` (boolean): 是否包含班级对比
- `generate_recommendations` (boolean): 是否生成学习建议

**返回**：
```json
{
  "student_id": "stu001",
  "basic_info": {
    "name": "张三",
    "class": "math2024-01",
    "total_assignments": 24,
    "average_score": 81.5
  },
  "learning_trend": {
    "score_trend": [75, 78, 82, 85, 81, 83, 86],
    "submission_trend": [1, 1, 1, 1, 0, 1, 1],  # 1=提交，0=未提交
    "time_spent_trend": [45, 50, 48, 52, 0, 55, 53]  # 分钟
  },
  "knowledge_mastery": {
    "strong_topics": [
      {"topic": "导数计算", "mastery": 92, "rank": "top10%"},
      {"topic": "函数极限", "mastery": 88, "rank": "top20%"}
    ],
    "weak_topics": [
      {"topic": "微分中值定理", "mastery": 62, "rank": "bottom30%"},
      {"topic": "泰勒公式", "mastery": 58, "rank": "bottom25%"}
    ],
    "improving_topics": [
      {"topic": "不定积分", "from": 65, "to": 78, "improvement": 13}
    ]
  },
  "error_patterns": {
    "most_common": "计算粗心错误",
    "frequency": 8,
    "contexts": ["积分计算", "导数运算"],
    "time_pattern": "作业后半段出现较多"
  },
  "personalized_recommendations": {
    "immediate": [
      "重点复习微分中值定理的应用场景",
      "完成泰勒公式专项练习5题"
    ],
    "short_term": [
      "每周增加30分钟证明题练习",
      "建立错题本，记录计算粗心错误"
    ],
    "long_term": [
      "参加数学建模兴趣小组",
      "阅读《微积分的历程》拓展视野"
    ]
  },
  "comparison_with_class": {
    "score_percentile": 75.3,
    "submission_rank": "前30%",
    "improvement_rank": "前20%"
  }
}
```

### generate_teaching_recommendations
生成教学建议和课堂优化方案

**参数**：
- `class_id` (string): 班级ID
- `focus_topics` (array): 重点关注知识点
- `time_constraint` (number): 课堂时间约束（分钟）
- `teaching_style` (string): 教学风格，"traditional"、"interactive"、"flipped"

**返回**：
```json
{
  "recommendation_id": "rec_001",
  "class_analysis": {
    "overall_level": "中等偏上",
    "main_challenges": ["抽象概念理解", "证明题逻辑"],
    "learning_characteristics": "计算能力强，逻辑推理需加强"
  },
  "next_class_focus": {
    "primary_topic": "微分中值定理应用",
    "time_allocation": {
      "concept_explanation": 20,
      "example_demonstration": 15,
      "student_practice": 25,
      "qna_discussion": 10
    },
    "key_points": [
      "罗尔定理与拉格朗日定理的联系",
      "中值定理的几何解释",
      "典型应用场景分析"
    ]
  },
  "differentiated_instruction": {
    "advanced_students": [
      "挑战题：中值定理的推广形式",
      "阅读材料：《微积分发展史》相关章节"
    ],
    "average_students": [
      "巩固练习：标准题型训练",
      "小组讨论：定理应用实例"
    ],
    "struggling_students": [
      "基础回顾：定理条件理解",
      "一对一辅导：具体问题解答"
    ]
  },
  "resource_recommendations": {
    "videos": [
      {
        "title": "微分中值定理直观解释",
        "url": "https://example.com/video1",
        "duration": 8,
        "suitable_for": "all"
      }
    ],
    "interactive_tools": [
      {
        "name": "GeoGebra中值定理演示",
        "url": "https://geogebra.org/...",
        "activity": "拖动观察定理条件变化"
      }
    ],
    "practice_sets": [
      {
        "name": "中值定理基础练习",
        "difficulty": "基础",
        "count": 6,
        "estimated_time": 30
      }
    ]
  },
  "assessment_suggestions": {
    "formative": [
      "课堂小测：定理条件判断",
      "小组展示：应用实例分享"
    ],
    "summative": [
      "单元测试：包含证明和应用题",
      "项目作业：实际问题建模"
    ]
  }
}
```

## 使用示例

### 示例1：生成班级数据看板
```bash
# 生成月度班级学情看板
openclaw skill calculus-learning-analytics generate_class_dashboard \
  --class-id "math2024-01" \
  --time-range "month" \
  --include-metrics "['submission_rate','average_score','knowledge_mastery']" \
  --visualization-type "detailed"
```

### 示例2：深度分析学生画像
```bash
# 深度分析学生学习情况
openclaw skill calculus-learning-analytics analyze_student_profile \
  --student-id "stu001" \
  --analysis-depth "deep" \
  --include-comparison true \
  --generate-recommendations true
```

### 示例3：生成教学建议
```bash
# 为下周课堂生成教学方案
openclaw skill calculus-learning-analytics generate_teaching_recommendations \
  --class-id "math2024-01" \
  --focus-topics "['微分中值定理','泰勒公式']" \
  --time-constraint 90 \
  --teaching-style "interactive"
```

## 数据分析模型

### 能力维度建模
```python
class AbilityModel:
    """学生能力多维度建模"""
    
    def __init__(self):
        self.dimensions = {
            'concept_understanding': {
                'indicators': ['定义记忆', '定理理解', '概念应用'],
                'weight': 0.3
            },
            'computation_ability': {
                'indicators': ['计算速度', '计算准确率', '复杂计算'],
                'weight': 0.25
            },
            'logical_reasoning': {
                'indicators': ['证明逻辑', '问题分析', '推理能力'],
                'weight': 0.25
            },
            'problem_solving': {
                'indicators': ['策略选择', '方法创新', '结果验证'],
                'weight': 0.2
            }
        }
    
    def calculate_ability_scores(self, student_data):
        """计算各维度能力分数"""
        scores = {}
        
        for dim_name, dim_config in self.dimensions.items():
            dimension_score = 0
            total_weight = 0
            
            for indicator in dim_config['indicators']:
                # 从学生数据中提取指标分数
                indicator_score = self.extract_indicator_score(
                    student_data, dim_name, indicator
                )
                dimension_score += indicator_score
                total_weight += 1
            
            scores[dim_name] = dimension_score / total_weight
        
        return scores
```

### 知识点关联分析
```python
class KnowledgeGraphAnalyzer:
    """知识点关联关系分析"""
    
    def __init__(self):
        self.graph = KnowledgeGraph()
        
    def analyze_prerequisites(self, weak_topic):
        """分析薄弱知识点的前置依赖"""
        prerequisites = self.graph.get_prerequisites(weak_topic)
        
        # 检查学生是否掌握前置知识点
        missing_prereqs = []
        for prereq in prerequisites:
            if not self.check_mastery(prereq):
                missing_prereqs.append({
                    'topic': prereq,
                    'mastery_level': self.get_mastery_level(prereq),
                    'recommendation': f'先复习{prereq}'
                })
        
        return missing_prereqs
    
    def find_related_errors(self, error_type):
        """发现关联错误模式"""
        related_errors = []
        
        # 基于知识图谱查找关联错误
        for topic in self.graph.get_related_topics(error_type):
            similar_errors = self.find_similar_errors(topic, error_type)
            if similar_errors:
                related_errors.append({
                    'topic': topic,
                    'error_count': len(similar_errors),
                    'common_pattern': self.extract_pattern(similar_errors)
                })
        
        return related_errors
```

### 预测模型
```python
class PerformancePredictor:
    """学生表现预测模型"""
    
    def __init__(self):
        self.model = self.load_prediction_model()
        
    def predict_future_score(self, student_history, upcoming_topic):
        """预测学生在未来知识点上的表现"""
        # 特征工程
        features = self.extract_features(student_history)
        
        # 添加知识点特征
        topic_features = self.get_topic_features(upcoming_topic)
        features.update(topic_features)
        
        # 模型预测
        predicted_score = self.model.predict(features)
        confidence = self.model.predict_proba(features)
        
        return {
            'predicted_score': predicted_score,
            'confidence': confidence,
            'key_factors': self.explain_prediction(features)
        }
    
    def identify_at_risk_students(self, class_data, threshold=60):
        """识别风险学生"""
        at_risk = []
        
        for student in class_data:
            # 预测未来表现
            prediction = self.predict_future_score(
                student['history'], 
                student['next_topic']
            )
            
            if prediction['predicted_score'] < threshold:
                at_risk.append({
                    'student_id': student['id'],
                    'predicted_score': prediction['predicted_score'],
                    'risk_factors': prediction['key_factors'],
                    'intervention_suggested': self.suggest_intervention(student)
                })
        
        return at_risk
```

## 与现有Skill集成

### 集成calculus-error-analyzer
```python
# 获取深度错误分析
from calculus_error_analyzer import get_error_insights

error_insights = get_error_insights(
    class_id="math2024-01",
    time_range="month",
    analysis_depth="deep"
)

# 整合到学情报告
dashboard_data['error_analysis'] = error_insights
```

### 调用question-type-generator
```python
# 基于薄弱点生成练习
from question_type_generator import generate_targeted_practice

practice_set = generate_targeted_practice(
    weak_topics=student_profile['weak_topics'],
    difficulty="adaptive",
    count=10
)
```

## 数据可视化

### 热力图生成
```python
def generate_knowledge_heatmap(self, class_data):
    """生成知识点掌握热力图"""
    heatmap_data = []
    
    for topic in self.knowledge_topics:
        # 计算班级平均掌握率
        mastery_rates = [
            student['knowledge_mastery'].get(topic, 0)
            for student in class_data
        ]
        avg_mastery = sum(mastery_rates) / len(mastery_rates)
        
        # 识别常见错误
        common_errors = self.identify_common_errors(topic, class_data)
        
        heatmap_data.append({
            'topic': topic,
            'mastery_rate': avg_mastery,
            'common_errors': common_errors,
            'color_intensity': self.calculate_color(avg_mastery)
        })
    
    return heatmap_data
```

### 雷达图生成
```python
def generate_ability_radar(self, student_scores, class_average):
    """生成能力维度雷达图"""
    radar_data = {
        'dimensions': list(student_scores.keys()),
        'student_scores': list(student_scores.values()),
        'class_average': list(class_average.values()),
        'max_score': 100
    }
    
    # 计算相对优势
    relative_strengths = []
    for dim in student_scores:
        relative = student_scores[dim] - class_average[dim]
        relative_strengths.append({
            'dimension': dim,
            'difference': relative,
            'strength': '优势' if relative > 5 else '劣势' if relative < -5 else '平均'
        })
    
    radar_data['relative_analysis'] = relative_strengths
    return radar_data
```

## 配置说明

### 分析参数配置
```yaml
analytics_settings:
  scoring_weights:
    concept_understanding: 0.30
    computation_ability: 0.25
    logical_reasoning: 0.25
    problem_solving: 0.20
    
  prediction_settings:
    model: "xgboost"
    features: ["historical_scores", "submission_pattern", "error_types"]
    horizon: 7  # 预测未来7天
    
  visualization:
    color_scheme: "viridis"
    chart_types: ["heatmap", "radar", "line", "bar"]
    export_formats: ["png", "pdf", "html"]
```

### 告警阈值配置
```yaml
alert_thresholds:
  performance:
    at_risk: 60      # 低于60分预警
    significant_drop: 15  # 分数下降15分以上
    
  engagement:
    missing_submissions: 3  # 连续3次未提交
    late_submissions: 5     # 5次以上迟交
    
  progress:
    stagnation: 7    # 7天无进步
    regression: 10   # 退步10分以上
```

## 性能优化

### 数据缓存策略
```python
class AnalyticsCache:
    """学情数据缓存管理"""
    
    def __init__(self):
        self.cache_ttl = {
            'dashboard': 300,      # 5分钟
            'student_profile': 600, # 10分钟
            'predictions': 1800,    # 30分钟
            'recommendations': 3600 # 1小时
        }
        
    async def get_cached_analysis(self, cache_key, analysis_type):
        """获取缓存的分析结果"""
        ttl = self.cache_ttl.get(analysis_type, 300)
        
