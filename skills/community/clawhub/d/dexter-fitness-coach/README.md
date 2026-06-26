# 🏋️ AI健身教练 - 开发文档

## 当前定位

这个仓库现在以 **标准 skill 包** 为主，根文件是 `SKILL.md`。

- `SKILL.md` / `skill.md`: ClawHub / OpenClaw 主要消费的技能定义
- `fitness_coach.py` 等 Python 文件: 本地原型和参考实现
- `openclaw.yaml`: 补充元数据，不作为已验证的跨平台运行协议

这意味着它现在最可靠的使用方式是作为 **markdown skill** 被安装和调用，而不是依赖 Python 入口被宿主自动执行。

## 项目概述

一个24/7陪伴的个性化健身指导智能体，具备：
- 🧠 记忆系统：记住你的训练历史、偏好、目标
- 📋 计划生成：根据数据生成个性化训练计划
- 📊 进度追踪：自动记录训练，同步飞书表格
- ❤️ 情绪陪伴：不是冷冰冰的计划，而是懂你的教练

---

## 项目结构

```
fitness-coach/
├── skill.md                 # Skill主文件（用户可见）
├── README.md                # 开发文档（本文件）
├── config.yaml              # 配置文件
│
├── data_models.py           # 数据模型定义
├── memory_manager.py        # 记忆管理系统
├── training_planner.py      # 训练计划生成器
├── feishu_integration.py    # 飞书集成
├── fitness_coach.py         # 主程序
│
└── data/                    # 数据存储目录
    ├── users/               # 用户档案
    └── logs/                # 训练日志
```

---

## 核心模块

### 1. 数据模型 (data_models.py)

定义了完整的数据结构：
- `UserProfile`: 用户档案
- `BodyMetrics`: 身体指标
- `TrainingPlan`: 训练计划
- `TrainingSession`: 单次训练
- `Exercise`: 训练动作
- `WorkoutLog`: 训练记录
- `ProgressTracker`: 进度追踪
- `ConversationMemory`: 对话记忆

### 2. 记忆管理 (memory_manager.py)

功能：
- 用户档案的创建/加载/保存
- 训练日志的记录和查询
- 进度统计（总次数、连续天数、体重历史）
- 对话历史管理

### 3. 计划生成 (training_planner.py)

根据用户目标生成训练计划：
- 减脂计划：全身训练为主
- 增肌计划：分化训练为主
- 支持不同训练频率（2-5次/周）

### 4. 飞书集成 (feishu_integration.py)

- 自动同步训练数据到飞书多维表格
- 支持CSV导出（可导入飞书）
- API集成（可选）

### 5. 主程序 (fitness_coach.py)

整合所有功能，提供：
- 用户引导流程
- 对话处理
- 训练记录
- 进度查询
- 计划展示

---

## 使用方法

### 方式1：作为 ClawHub / OpenClaw Skill 使用

安装：
```bash
clawhub install dexter-fitness-coach
```

安装后直接用自然语言发起请求，例如：
```text
我想要一个每周三练的减脂计划，地点是健身房。
```

### 方式2：作为Python模块使用

```python
from fitness_coach import FitnessCoach

# 创建教练实例
coach = FitnessCoach(user_id="user_123")

# 开始对话
response = coach.start_onboarding()
print(response)

# 处理用户输入
user_input = "我身高175，体重80"
response = coach.process_input(user_input)
print(response)
```

---

## 配置

### 大模型配置

在 `config.yaml` 中配置：

```yaml
llm:
  provider: "zhipu"  # 或 "claude" / "deepseek"
  api_key: "your-api-key"
  model: "glm-4-flash"
```

### 飞书配置（可选）

1. 创建飞书应用
2. 获取 App ID 和 App Secret
3. 在 `config.yaml` 中配置：

```yaml
feishu:
  enabled: true
  app_id: "your-app-id"
  app_secret: "your-app-secret"
```

---

## 开发路线

### ✅ 已完成
- [x] 数据模型设计
- [x] 记忆管理系统
- [x] 训练计划生成
- [x] 基础对话流程
- [x] 飞书集成框架

### 🚧 进行中
- [ ] LLM集成（智谱GLM）
- [ ] 智能训练内容解析
- [ ] 个性化日报生成
- [ ] 情绪陪伴系统

### 📋 计划中
- [ ] OpenClaw集成
- [ ] 飞书机器人部署
- [ ] 多用户支持
- [ ] 数据可视化

---

## 技术栈

- **语言**: Python 3.8+
- **数据存储**: JSON（本地文件）
- **大模型**: 智谱GLM（可选Claude/DeepSeek）
- **集成**: 飞书多维表格 API
- **框架**: OpenClaw Agent

---

## 安全声明

⚠️ **重要提醒**：
- 本AI教练提供的是参考建议，不能替代专业医疗建议
- 如有身体不适，请立即停止训练并咨询医生
- 训练请量力而行，循序渐进

---

## 贡献

欢迎提出建议和改进！

---

## 许可

MIT License

---

*记住：坚持 > 完美，进步 > 速度*
