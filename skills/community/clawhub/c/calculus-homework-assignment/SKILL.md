# calculus-homework-assignment - 高等数学智能作业布置Skill

## 概述
基于学生能力画像的智能作业布置系统，专门针对高等数学课程设计。支持自适应作业生成、分层难度设计、多模态题目组装和定时发布。

## 核心功能

### 1. 自适应作业生成
根据学生历史表现和知识点掌握度，智能生成个性化作业：
- **能力画像分析**：评估学生概念理解、计算能力、逻辑推理三大维度
- **难度自适应**：动态调整基础/提高/拓展题目比例
- **知识点覆盖**：确保教学进度的全面覆盖

### 2. 多模态题目支持
- **LaTeX公式**：完美支持高等数学公式编辑
- **GeoGebra交互**：嵌入几何可视化题目
- **图像题目**：支持图表、函数图像
- **语音讲解**：为复杂题目提供语音提示

### 3. 智能工作流
```
学生能力分析 → 知识点匹配 → 题目筛选 → 难度调整 → 作业组装 → 发布
```

## 工具定义

### generate_adaptive_homework
基于学生能力画像生成自适应作业

**参数**：
- `topic` (string): 知识点主题，如"定积分应用"、"多元函数微分"
- `difficulty_distribution` (array): 难度分布，如[40, 40, 20]表示基础40%、提高40%、拓展20%
- `student_level` (string): 学生水平，可选"初级"、"中等"、"高级"或具体分数段
- `estimated_time` (number): 预计完成时间（分钟）
- `question_count` (number): 题目数量，默认10题

**返回**：
```json
{
  "homework_id": "hw_20260416_001",
  "topic": "定积分应用",
  "questions": [
    {
      "id": "q1",
      "type": "calculation",
      "difficulty": "基础",
      "content": "计算∫₀¹ x² dx",
      "latex": "\\int_0^1 x^2 dx",
      "estimated_time": 5
    }
  ],
  "total_time": 60,
  "difficulty_summary": {
    "basic": 4,
    "intermediate": 4, 
    "advanced": 2
  }
}
```

### schedule_release
定时发布作业并设置提醒

**参数**：
- `release_time` (string): 发布时间，ISO格式"2026-04-16T18:00:00"
- `deadline` (string): 截止时间，ISO格式"2026-04-17T23:59:00"
- `reminder_hours` (number): 提前提醒小时数，默认2小时
- `class_id` (string): 班级ID
- `batch_release` (boolean): 是否分批发布

**返回**：
```json
{
  "schedule_id": "sch_001",
  "release_time": "2026-04-16T18:00:00",
  "deadline": "2026-04-17T23:59:00",
  "reminder_set": true,
  "reminder_time": "2026-04-17T21:59:00"
}
```

### analyze_student_profile
分析学生能力画像

**参数**：
- `student_id` (string): 学生ID
- `history_range` (string): 历史数据范围，如"last_month"、"all"
- `include_topics` (array): 包含的知识点列表

**返回**：
```json
{
  "student_id": "stu001",
  "overall_level": "中等",
  "dimension_scores": {
    "concept_understanding": 75,
    "computation_ability": 82,
    "logical_reasoning": 68
  },
  "weak_topics": ["微分中值定理", "泰勒公式"],
  "strong_topics": ["导数计算", "不定积分"],
  "recommended_difficulty": [30, 50, 20]
}
```

## 使用示例

### 示例1：生成个性化作业
```bash
# 为中等水平学生生成定积分应用作业
openclaw skill calculus-homework-assignment generate_adaptive_homework \
  --topic "定积分应用" \
  --difficulty-distribution "[40,40,20]" \
  --student-level "中等" \
  --estimated-time 60 \
  --question-count 8
```

### 示例2：定时发布作业
```bash
# 安排作业发布
openclaw skill calculus-homework-assignment schedule_release \
  --release-time "2026-04-16T18:00:00" \
  --deadline "2026-04-17T23:59:00" \
  --reminder-hours 2 \
  --class-id "math2024-01" \
  --batch-release true
```

### 示例3：分析学生能力
```bash
# 分析学生能力画像
openclaw skill calculus-homework-assignment analyze_student_profile \
  --student-id "stu001" \
  --history-range "last_month" \
  --include-topics "['导数','积分','微分方程']"
```

## 配置说明

### 难度等级定义
```yaml
difficulty_levels:
  basic:     # 基础题（40%）
    description: "直接应用公式和基本方法"
    example: "计算简单导数或积分"
    
  intermediate:  # 提高题（40%）
    description: "需要多步推导或综合应用"
    example: "应用题、证明题前几步"
    
  advanced:      # 拓展题（20%）
    description: "创新性、开放性题目"
    example: "综合证明、实际建模问题"
```

### 知识点库配置
```yaml
knowledge_topics:
  - id: "derivative"
    name: "导数与微分"
    sub_topics: ["基本求导", "高阶导数", "隐函数求导", "参数方程求导"]
    
  - id: "integral"  
    name: "积分"
    sub_topics: ["不定积分", "定积分", "反常积分", "重积分"]
    
  - id: "series"
    name: "级数"
    sub_topics: ["数项级数", "幂级数", "傅里叶级数"]
```

## 与现有Skill集成

### 调用question-type-generator
```python
# 从题目生成器获取题目
from question_type_generator import generate_math_problem

problem = generate_math_problem(
    topic="定积分",
    difficulty="中等",
    type="calculation"
)
```

### 集成calculus-concept-visualizer
```python
# 为题目添加可视化
from calculus_concept_visualizer import create_visualization

visualization = create_visualization(
    concept="定积分的几何意义",
    type="area_under_curve"
)
```

## 实现细节

### 核心算法
```python
class AdaptiveHomeworkGenerator:
    def __init__(self):
        self.question_bank = QuestionBank()
        self.student_analyzer = StudentAnalyzer()
        
    def generate_homework(self, topic, student_profile):
        # 1. 分析学生能力
        ability_scores = self.student_analyzer.analyze(student_profile)
        
        # 2. 确定难度分布
        difficulty_dist = self.calculate_difficulty_distribution(ability_scores)
        
        # 3. 筛选题目
        questions = self.question_bank.filter_questions(
            topic=topic,
            difficulty_dist=difficulty_dist,
            count=10
        )
        
        # 4. 组装作业
        homework = self.assemble_homework(questions, topic)
        
        return homework
```

### 多模态支持
```python
class MultimediaQuestion:
    def __init__(self, base_question):
        self.base = base_question
        
    def add_latex(self, latex_content):
        """添加LaTeX公式"""
        self.latex = latex_content
        
    def add_geogebra(self, geogebra_url):
        """添加GeoGebra交互"""
        self.geogebra = geogebra_url
        
    def add_voice_hint(self, hint_text):
        """添加语音提示"""
        self.voice_hint = text_to_speech(hint_text)
```

## 测试用例

### 单元测试
```python
def test_adaptive_homework_generation():
    generator = AdaptiveHomeworkGenerator()
    
    # 测试中等水平学生
    homework = generator.generate_homework(
        topic="定积分应用",
        student_level="中等"
    )
    
    assert len(homework.questions) == 10
    assert homework.difficulty_summary["basic"] == 4
    assert homework.total_time <= 60
```

### 集成测试
```bash
# 测试完整作业流程
python test_full_workflow.py \
  --student "stu001" \
  --topic "多元函数微分" \
  --output "test_report.json"
```

## 部署说明

### 环境要求
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- LaTeX编译环境

### 安装步骤
```bash
# 1. 克隆代码
git clone https://github.com/yourrepo/calculus-homework-assignment.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置数据库
python setup_database.py

# 4. 启动服务
python main.py --port 8000
```

## 性能优化

### 缓存策略
- 题目库缓存：Redis缓存常用题目
- 学生画像缓存：内存缓存活跃学生数据
- 作业模板缓存：预生成常用作业模板

### 并发处理
- 异步题目生成：使用asyncio提高并发
- 批量作业发布：支持同时发布多个班级作业
- 分布式处理：支持多节点部署

## 版本历史
- v1.0.0 (2026-04-16): 初始版本
  - 自适应作业生成
  - 多模态题目支持
  - 定时发布功能
  - 学生能力分析

## 作者
代国兴 - 高等数学智慧课程系统

## 许可证
MIT License