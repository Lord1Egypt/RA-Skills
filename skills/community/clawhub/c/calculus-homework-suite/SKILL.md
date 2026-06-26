# calculus-homework-suite - 高等数学作业全生命周期管理套件

## 概述
这是一个完整的高等数学作业管理系统，包含作业布置、智能批改、学情分析和错题分析四大模块，专门针对高等数学的公式、推导、证明等特色需求设计。

## 系统架构
```
┌─────────────────────────────────────────────────────────────┐
│ 作业管理中枢 (Homework Hub)                                 │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│ │ 作业布置Skill │ │ 智能批改Skill │ │ 学情数据Skill     │ │
│ │ (Assignment)│ │ (Grading)   │ │ (Analytics)       │ │
│ └──────┬──────┘ └──────┬──────┘ └──────────┬──────────┘ │
│        └─────────────────┼────────────────────┘          │
│                         ▼                                 │
│              ┌─────────────────────────┐                 │
│              │ 错题分析Skill           │                 │
│              │ (Error Analysis)        │                 │
│              └─────────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

## 包含的子Skill
1. **calculus-homework-assignment** - 智能作业布置
2. **calculus-intelligent-grading** - 多模态智能批改  
3. **calculus-learning-analytics** - 学情数据分析
4. **calculus-error-analyzer** - 错题深度分析

## 核心功能

### 1. 作业布置功能
- 自适应作业生成（基于学生能力画像）
- 分层难度设计（基础/提高/拓展）
- 多模态支持（LaTeX公式、GeoGebra交互、图像上传）
- 定时发布与提醒

### 2. 智能批改功能
- LaTeX公式符号计算验证
- 推导过程步骤检查
- 多模态批注（文字、语音、视频）
- AI助教+人工复核双模式

### 3. 学情分析功能
- 班级作业概览看板
- 学生个人能力画像
- 错误类型分布分析
- 教学建议引擎

### 4. 错题分析功能
- 薄弱知识点定位
- 个性化错题本生成
- 针对性练习推荐
- 学习路径优化

## 与现有Skill集成
- **calculus-concept-visualizer** - 作业中嵌入概念可视化
- **calculus-problem-generator** - 作业题库来源
- **question-type-generator** - 题目生成引擎
- **math-edu-assistant** - 数学教育支持

## 使用示例

### 完整作业流程
```bash
# 1. 生成自适应作业
openclaw skill calculus-homework-assignment generate \
  --topic "定积分应用" \
  --difficulty "基础40%,提高40%,拓展20%" \
  --student-level "中等"

# 2. 批改学生作业
openclaw skill calculus-intelligent-grading grade \
  --submission-type "image" \
  --image-path "student_work.jpg" \
  --reference-answer "标准答案"

# 3. 生成学情报告
openclaw skill calculus-learning-analytics report \
  --class-id "math2024-01" \
  --time-range "本周"

# 4. 错题分析
openclaw skill calculus-error-analyzer analyze \
  --student-id "stu001" \
  --knowledge-point "微分中值定理"
```

### 快速开始
```bash
# 安装所有子Skill
clawhub install calculus-homework-assignment
clawhub install calculus-intelligent-grading
clawhub install calculus-learning-analytics
clawhub install calculus-error-analyzer

# 运行完整作业流程
openclaw skill calculus-homework-suite run-full-workflow \
  --class "高等数学A班" \
  --topic "多元函数微分学" \
  --deadline "2026-04-18 23:59"
```

## 技术架构
- **后端**: Python + FastAPI
- **AI引擎**: Claude/DeepSeek + SymPy符号计算
- **存储**: PostgreSQL + Redis缓存
- **前端**: Vue3数据看板（可选）
- **部署**: OpenClaw Skill标准格式

## 配置说明

### 环境变量
```bash
# 数据库配置
export HOMEWORK_DB_HOST=localhost
export HOMEWORK_DB_PORT=5432
export HOMEWORK_DB_NAME=calculus_homework

# AI服务配置
export LLM_API_KEY=your_llm_key
export OCR_SERVICE_URL=http://localhost:8001

# 定时任务配置
export SCHEDULER_ENABLED=true
export REMINDER_HOURS_BEFORE=2
```

### 技能配置
```yaml
# config/skill-config.yaml
assignment:
  default_difficulty: [40, 40, 20]  # 基础,提高,拓展
  max_questions: 10
  time_estimate: 60  # 分钟

grading:
  llm_model: "deepseek/deepseek-chat"
  step_validation: true
  voice_feedback: true

analytics:
  dashboard_refresh: 300  # 秒
  report_generation: "daily"
```

## 开发指南

### 项目结构
```
calculus-homework-suite/
├── SKILL.md                    # 主技能文档
├── package.json               # 技能配置
├── src/
│   ├── assignment/           # 作业布置模块
│   ├── grading/             # 智能批改模块
│   ├── analytics/           # 学情分析模块
│   ├── error_analysis/      # 错题分析模块
│   └── shared/              # 共享工具
├── config/                   # 配置文件
├── examples/                 # 使用示例
└── tests/                    # 测试用例
```

### 扩展开发
要添加新的批改算法或分析维度：
1. 在对应模块创建新的Python类
2. 实现标准接口
3. 更新技能配置
4. 添加测试用例

## 版本历史
- v1.0.0 (2026-04-16): 初始版本发布
  - 四大核心模块
  - 多模态作业支持
  - 智能批改引擎
  - 学情数据看板

## 作者
代国兴 - 高等数学智慧课程系统设计

## 许可证
MIT License