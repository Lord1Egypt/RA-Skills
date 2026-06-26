# 🏋️ AI健身教练 - 完整设计文档

> 24/7陪伴的个性化健身指导智能体

**版本**: 1.0.2
**作者**: @dexterqiu-collab
**ClawHub ID**: k973az9cyysxhp04wezy0hvj1x83hxms
**GitHub**: https://github.com/dexterqiu-collab/fitness-coach

---

## 目录

- [1. 项目概述](#1-项目概述)
- [2. 核心功能](#2-核心功能)
- [3. 技术架构](#3-技术架构)
- [4. 数据模型设计](#4-数据模型设计)
- [5. 核心模块](#5-核心模块)
- [6. 部署方案](#6-部署方案)
- [7. 使用流程](#7-使用流程)
- [8. 开发路线](#8-开发路线)
- [9. 安全声明](#9-安全声明)

---

## 1. 项目概述

### 1.1 愿景

打造一个**24/7陪伴的个性化健身教练**，具备：

- 🧠 **记忆系统** - 记住训练历史、偏好、目标
- 📋 **计划生成** - 根据数据生成个性化训练计划
- 📊 **进度追踪** - 自动记录训练，同步飞书表格
- ❤️ **情绪陪伴** - 不只是冷冰冰的计划，更是懂你的教练

### 1.2 差异化优势

| 特性 | 传统方法 | AI健身教练 |
|------|----------|------------|
| 随时陪伴 | ❌ 需预约 | ✅ 24/7在线 |
| 记录方式 | 📝 备忘录/表格 | ✅ 对话即记录 |
| 个性化 | 📋 固定模板 | ✅ 越用越懂你 |
| 情绪价值 | ❌ 无 | ✅ 陪伴式教练 |
| 数据同步 | 🔄 手动导入 | ✅ 自动同步飞书 |

### 1.3 目标用户

- 健身新手 - 需要指导和陪伴
- 增肌减脂者 - 需要计划和追踪
- 忙碌白领 - 需要高效记录
- 数据控 - 喜欢可视化进度

---

## 2. 核心功能

### 2.1 MVP功能（已实现）

#### 功能1：用户档案管理
```python
# 收集的信息
- 身体数据：身高、体重、体脂率（估算）
- 目标设定：减脂 / 增肌 / 保持
- 训练频率：每周2-5次
- 饮食偏好：记录备注
```

#### 功能2：个性化训练计划
```python
# 根据目标生成
减脂目标 → 全身训练为主，高次数
增肌目标 → 分化训练为主，渐进负荷
保持目标 → 综合训练

# 训练频率支持
2次/周 → 全身A/B
3次/周 → 全身+上下肢
4-5次/周 → 推拉腿分化
```

#### 功能3：训练记录
```python
# 对话式记录
用户: "今天练了胸，卧推4组12次，引体向上4组10次"
AI: 自动解析并记录

# 自动生成
- 训练日报
- 完成度统计
- 连续打卡天数
```

#### 功能4：进度追踪
```python
# 统计数据
- 总训练次数
- 连续打卡天数
- 体重变化曲线
- 本周训练频率

# 可视化输出
📈 你的训练进度
- 训练次数：15次
- 连续打卡：7天 🔥
- 体重：80kg → 78kg (-2kg)
```

#### 功能5：飞书集成
```python
# 数据同步
- 自动导出CSV（可导入飞书多维表格）
- API集成（可选）
- 训练记录表
- 用户档案表
- 进度统计表
```

### 2.2 规划功能（待实现）

#### 功能6：智能内容解析
```python
# 使用LLM解析训练内容
支持自然语言输入：
- "今天做了5个引体向上，感觉很轻松"
- "深蹲100kg，5组5次，最后一组有点吃力"

自动提取：
- 动作名称
- 组数次数
- 重量
- 体感评分
```

#### 功能7：个性化日报
```python
# AI生成训练日报
根据当日训练内容：
- 总结训练亮点
- 分析进步趋势
- 提供改进建议
- 情绪化鼓励
```

#### 功能8：情绪陪伴系统
```python
# 教练个性
style: encouraging（鼓励型）/ strict（严格型）/ humorous（幽默型）

# 对话场景
- 训练前：激励和提醒
- 训练后：祝贺和总结
- 偷懒时：温和督促
- 成功时：一起庆祝
```

---

## 3. 技术架构

### 3.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      用户交互层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  飞书客户端  │  │  Claude Code │  │  OpenClaw    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   AI健身教练核心层                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              FitnessCoach (主程序)                   │   │
│  │  - 对话管理  - 流程控制  - 意图识别                  │   │
│  └──────────────────────────────────────────────────────┘   │
│           ↓            ↓            ↓                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ 记忆管理 │  │ 计划生成 │  │ 飞书集成 │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据存储层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  JSON文件    │  │  飞书表格    │  │  对话记忆    │      │
│  │  用户档案    │  │  训练记录    │  │  上下文      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      外部服务层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  智谱GLM API │  │  飞书 API    │  │  ClawHub     │      │
│  │  (LLM服务)   │  │  (数据同步)  │  │  (技能分发)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **语言** | Python 3.8+ | 核心开发语言 |
| **数据存储** | JSON | 本地文件存储 |
| **LLM服务** | 智谱GLM | 智能内容解析和生成 |
| **LLM备选** | Claude / DeepSeek | 可选的其他大模型 |
| **数据同步** | 飞书多维表格API | 云端数据存储 |
| **技能分发** | OpenClaw + ClawHub | 智能体部署平台 |
| **配置管理** | YAML | 配置文件格式 |

### 3.3 项目结构

```
fitness-coach/
├── skill.md                 # Claude Code技能定义
├── openclaw.yaml            # OpenClaw技能配置
├── openclaw.sh              # OpenClaw入口脚本
├── config.yaml              # 全局配置文件
├── README.md                # 使用说明
├── DESIGN.md                # 本设计文档
│
├── data_models.py           # 数据模型定义
├── memory_manager.py        # 记忆管理系统
├── training_planner.py      # 训练计划生成器
├── feishu_integration.py    # 飞书集成
├── fitness_coach.py         # 主程序
│
├── auto-deploy.sh           # 自动部署脚本
└── data/                    # 数据存储目录
    ├── users/               # 用户档案
    │   └── {user_id}.json
    └── logs/                # 训练日志
        └── {user_id}_logs.json
```

---

## 4. 数据模型设计

### 4.1 核心数据模型

#### 4.1.1 用户档案 (UserProfile)

```python
@dataclass
class UserProfile:
    """用户档案"""
    user_id: str                          # 用户唯一ID
    name: Optional[str] = None            # 姓名
    body_metrics: Optional[BodyMetrics] = None  # 身体指标
    target_weight: Optional[float] = None # 目标体重
    exercise_frequency: Optional[int] = None  # 每周训练次数
    diet_preference: Optional[str] = None     # 饮食偏好
    goal_type: GoalType = GoalType.MAINTENANCE  # 目标类型
    personality_insights: Dict = field(default_factory=dict)  # 个性化洞察
    created_at: datetime = field(default_factory=datetime.now)
```

#### 4.1.2 身体指标 (BodyMetrics)

```python
@dataclass
class BodyMetrics:
    """身体指标"""
    height: Optional[float] = None     # 身高(cm)
    weight: Optional[float] = None     # 体重(kg)
    body_fat: Optional[float] = None   # 体脂率(%)
    estimated_body_fat: Optional[float] = None  # 估算体脂率
    updated_at: datetime = field(default_factory=datetime.now)
```

#### 4.1.3 训练计划 (TrainingPlan)

```python
@dataclass
class TrainingPlan:
    """训练计划"""
    plan_id: str                       # 计划ID
    user_id: str                       # 用户ID
    name: str                          # 计划名称
    goal_type: GoalType                # 目标类型
    sessions: List[TrainingSession]    # 训练课程列表
    schedule: List[str]                # 训练时间表
    created_at: datetime = field(default_factory=datetime.now)
```

#### 4.1.4 训练课程 (TrainingSession)

```python
@dataclass
class TrainingSession:
    """单次训练课程"""
    focus: str                         # 训练重点（胸/背/腿/等）
    exercises: List[Exercise]          # 动作列表
    warmup: str                        # 热身内容
    cooldown: Optional[str] = None     # 放松内容
    duration_estimate: int = 45        # 预计时长(分钟)
    rest_between_sets: int = 90        # 组间休息(秒)
```

#### 4.1.5 训练动作 (Exercise)

```python
@dataclass
class Exercise:
    """训练动作"""
    name: str                          # 动作名称
    sets: int                          # 组数
    reps: Union[int, str]              # 次数（支持 "8-12"）
    weight: Optional[float] = None     # 重量(kg)
    rest_seconds: Optional[int] = None # 休息时间
    notes: Optional[str] = None        # 备注
```

#### 4.1.6 训练日志 (WorkoutLog)

```python
@dataclass
class WorkoutLog:
    """训练记录"""
    log_id: str                        # 日志ID
    user_id: str                       # 用户ID
    training_date: datetime            # 训练日期
    exercises: List[Exercise]          # 完成的动作
    focus: str                         # 训练重点
    completion_rate: float = 100.0     # 完成度
    user_feedback: Optional[str] = None     # 用户反馈
    feeling_score: Optional[int] = None     # 体感评分(1-5)
    weight_logged: Optional[float] = None   # 当日体重
    daily_report: Optional[str] = None      # 日报内容
    created_at: datetime = field(default_factory=datetime.now)
```

#### 4.1.7 进度追踪 (ProgressTracker)

```python
@dataclass
class ProgressTracker:
    """进度统计"""
    user_id: str                       # 用户ID
    total_sessions: int = 0            # 总训练次数
    current_streak: int = 0            # 当前连续天数
    longest_streak: int = 0            # 最长连续天数
    weight_history: List[Dict] = field(default_factory=list)  # 体重历史
    last_training_date: Optional[datetime] = None  # 最后训练日期
```

#### 4.1.8 对话记忆 (ConversationMemory)

```python
@dataclass
class ConversationMemory:
    """对话记忆"""
    user_id: str                       # 用户ID
    messages: List[Dict] = field(default_factory=list)  # 消息列表
    context_summary: Optional[str] = None   # 上下文摘要
    last_updated: datetime = field(default_factory=datetime.now)
```

### 4.2 数据存储格式

#### 4.2.1 用户档案文件

```json
{
  "user_id": "user_abc123",
  "name": "张三",
  "body_metrics": {
    "height": 175,
    "weight": 80,
    "body_fat": 22.0
  },
  "target_weight": 75,
  "exercise_frequency": 3,
  "goal_type": "减脂",
  "created_at": "2026-03-24T10:00:00"
}
```

#### 4.2.2 训练日志文件

```json
{
  "logs": [
    {
      "log_id": "log_001",
      "user_id": "user_abc123",
      "training_date": "2026-03-24T15:00:00",
      "exercises": [
        {"name": "卧推", "sets": 4, "reps": 12, "weight": 60},
        {"name": "引体向上", "sets": 4, "reps": 10, "weight": null}
      ],
      "focus": "胸",
      "daily_report": "今日训练表现优秀！"
    }
  ]
}
```

---

## 5. 核心模块

### 5.1 记忆管理模块 (MemoryManager)

**职责**：数据的持久化存储和检索

**核心方法**：

```python
class MemoryManager:
    def __init__(self, data_dir: str = None):
        """初始化，设置数据目录"""

    # 用户档案管理
    def create_user_profile(self, user_id: str) -> UserProfile:
        """创建新用户档案"""

    def load_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """加载用户档案"""

    def save_user_profile(self, profile: UserProfile) -> bool:
        """保存用户档案"""

    # 训练日志管理
    def add_workout_log(self, log: WorkoutLog) -> bool:
        """添加训练日志"""

    def get_user_logs(self, user_id: str, limit: int = 50) -> List[WorkoutLog]:
        """获取用户训练日志"""

    def get_recent_logs(self, user_id: str, days: int = 7) -> List[WorkoutLog]:
        """获取最近N天的日志"""

    # 进度统计
    def get_progress_stats(self, user_id: str) -> Dict:
        """获取进度统计"""
        return {
            "total_sessions": 15,
            "current_streak": 7,
            "longest_streak": 14,
            "weight_history": [...]
        }

    # 对话管理
    def add_conversation(self, user_id: str, role: str, content: str):
        """添加对话记录"""

    def get_conversation_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """获取对话历史"""
```

**数据目录结构**：

```
data/
├── users/
│   ├── user_abc123.json
│   └── user_def456.json
└── logs/
    ├── user_abc123_logs.json
    └── user_def456_logs.json
```

---

### 5.2 训练计划生成模块 (TrainingPlanner)

**职责**：根据用户目标生成个性化训练计划

**训练动作库**：

```python
EXERCISE_LIBRARY = {
    "胸": {
        "compound": ["卧推", "杠铃卧推", "哑铃卧推", "俯卧撑"],
        "isolation": ["哑铃飞鸟", "蝴蝶机夹胸", "绳索夹胸"],
        "bodyweight": ["俯卧撑", "钻石俯卧撑"]
    },
    "背": {
        "compound": ["引体向上", "高位下拉", "杠铃划船", "哑铃划船"],
        "isolation": ["直臂下压", "坐姿划船", "单臂哑铃划船"],
        "lower_back": ["硬拉", "山羊挺身"]
    },
    "腿": {
        "compound": ["深蹲", "腿举", "箭步蹲"],
        "quads": ["腿屈伸", "深蹲"],
        "hamstrings": ["腿弯举", "罗马尼亚硬拉"],
        "calves": ["提踵"]
    },
    # ... 更多部位
}
```

**计划生成逻辑**：

```python
class TrainingPlanner:
    def generate_plan(self, profile: UserProfile) -> TrainingPlan:
        """生成训练计划"""
        # 1. 确定目标类型
        goal = profile.goal_type  # 减脂/增肌/保持

        # 2. 根据目标和频率创建课程
        sessions = self._create_sessions(profile)

        # 3. 生成时间表
        schedule = self._create_schedule(profile.exercise_frequency)

        return TrainingPlan(...)

    def _create_fat_loss_sessions(self, frequency: int):
        """减脂期：全身训练为主"""
        if frequency == 2:
            return [全身A, 全身B]
        elif frequency == 3:
            return [全身, 上肢, 下肢]
        else:
            return [推, 拉, 腿, 全身]

    def _create_muscle_gain_sessions(self, frequency: int):
        """增肌期：分化训练为主"""
        if frequency == 3:
            return [推, 拉, 腿]
        else:
            return [胸+三头, 背+二头, 腿+肩, 弱项]
```

**计划示例**：

```python
# 减脂 - 3次/周
周一: 全身训练（深蹲、卧推、划船、推举、平板支撑）
周三: 上肢训练（卧推、划船、推举、弯举、下压）
周五: 下肢训练（深蹲、腿举、腿弯举、提踵）

# 增肌 - 4次/周
周一: 推（胸+三头）- 4个动作
周三: 拉（背+二头）- 5个动作
周五: 腿+肩 - 5个动作
周日: 弱项强化 - 自定义
```

---

### 5.3 飞书集成模块 (FeishuIntegration)

**职责**：数据同步到飞书多维表格

**核心方法**：

```python
class FeishuIntegration:
    def __init__(self, app_id: str, app_secret: str):
        """初始化飞书API"""

    def get_access_token(self) -> str:
        """获取访问令牌"""

    def create_table(self, table_name: str, fields: List[Dict]) -> Dict:
        """创建多维表格"""

    def add_record(self, table_id: str, record_data: Dict) -> bool:
        """添加记录"""

    def sync_workout_log(self, log: WorkoutLog) -> bool:
        """同步训练日志"""
        record_data = {
            "训练日期": log.training_date.strftime("%Y-%m-%d"),
            "训练重点": log.focus,
            "完成度": f"{log.completion_rate}%",
            "用户反馈": log.user_feedback or "",
            "体感评分": log.feeling_score or "",
            "日报": log.daily_report or ""
        }
        return self.add_record("workout_logs", record_data)

    def sync_user_profile(self, profile: UserProfile) -> bool:
        """同步用户档案"""
```

**表格结构设计**：

##### 表1：用户档案 (user_profiles)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 用户ID | 文本 | 唯一标识 |
| 身高 | 数字 | cm |
| 体重 | 数字 | kg |
| 体脂率 | 数字 | % |
| 目标体重 | 数字 | kg |
| 运动频率 | 文本 | "每周3次" |
| 目标类型 | 单选 | 减脂/增肌/保持 |
| 创建时间 | 日期 | - |

##### 表2：训练记录 (workout_logs)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 记录ID | 文本 | 唯一标识 |
| 用户ID | 文本 | 关联用户 |
| 训练日期 | 日期 | - |
| 训练重点 | 单选 | 胸/背/腿/肩/手/核心 |
| 完成度 | 数字 | % |
| 用户反馈 | 文本 | 自然语言 |
| 体感评分 | 数字 | 1-5 |
| 日报内容 | 文本 | AI生成 |

**CSV导出功能**：

```python
def export_to_csv(self, data: List[Dict], filename: str):
    """导出为CSV，可导入飞书"""
    import csv
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
```

---

### 5.4 主程序模块 (FitnessCoach)

**职责**：整合所有模块，管理对话流程

**对话状态机**：

```
┌──────────┐
│ initial  │ ← 初始状态
└────┬─────┘
     │ 用户首次交互
     ↓
┌──────────┐
│collecting│ ← 收集信息
└────┬─────┘
     │ 信息完整
     ↓
┌──────────┐
│  active  │ ← 活跃使用
└──────────┘
```

**核心方法**：

```python
class FitnessCoach:
    def __init__(self, user_id: str = None):
        self.user_id = user_id or f"user_{uuid.uuid4().hex[:8]}"
        self.memory = MemoryManager()
        self.planner = TrainingPlanner()
        self.feishu = FeishuTableManager()
        self.conversation_stage = "initial"

    # 对话流程
    def start_onboarding(self) -> str:
        """开始用户引导"""
        return """
        ✨ 欢迎来到你的健身之旅！✨

        为了给你制定最适合的训练计划，我需要了解几个信息：

        **1️⃣ 身体数据**
        请告诉我你的：
        - 身高（cm）
        - 体重（kg）
        - 体脂率（不知道的话说"不清楚"就行）

        例如：我身高175，体重80，体脂率不清楚
        """

    def process_input(self, user_input: str) -> str:
        """处理用户输入"""
        # 保存对话
        self.memory.add_conversation(self.user_id, "user", user_input)

        # 根据阶段处理
        if self.conversation_stage == "initial":
            response = self.start_onboarding()
        elif self.conversation_stage == "collecting":
            response = self._collect_info(user_input)
        elif self.conversation_stage == "active":
            response = self._active_coaching(user_input)

        # 保存回复
        self.memory.add_conversation(self.user_id, "coach", response)
        return response

    # 训练记录
    def _process_workout_log(self, user_input: str) -> str:
        """处理训练记录"""
        # 解析训练内容（TODO: 用LLM）
        exercises = self._parse_workout_input(user_input)

        # 创建日志
        log = WorkoutLog(
            log_id=f"log_{uuid.uuid4().hex[:8]}",
            user_id=self.user_id,
            training_date=datetime.now(),
            exercises=exercises,
            focus=exercises[0].name if exercises else "综合",
            user_feedback=user_input,
            daily_report=self._generate_daily_report(exercises)
        )

        # 保存并同步
        self.memory.add_workout_log(log)
        self.feishu.sync_workout_log(log)

        # 生成回复
        return self._format_workout_response(log)

    # 进度查询
    def _show_progress(self) -> str:
        """显示进度"""
        stats = self.memory.get_progress_stats(self.user_id)
        return f"""
        📈 你的训练进度

        - 总训练次数：{stats['total_sessions']}次
        - 连续打卡：{stats['current_streak']}天 🔥
        """
```

---

## 6. 部署方案

### 6.1 部署平台

#### 平台1：Claude Code Skill

**用途**：开发测试阶段使用

**配置文件**：`skill.md`

```yaml
---
name: fitness-coach
description: AI健身教练 - 24/7陪伴的个性化健身指导智能体
disable-model-invocation: false
user-invocable: true
---
```

**安装位置**：`~/.claude/skills/fitness-coach/`

**使用方式**：在Claude Code中输入 `/fitness-coach`

---

#### 平台2：OpenClaw + ClawHub

**用途**：生产环境，飞书集成

**配置文件**：`openclaw.yaml`

```yaml
name: "AI健身教练"
slug: "fitness-coach"
version: "1.0.1"
description: "24/7陪伴的个性化健身指导智能体"

type: "assistant"
author:
  name: "dexterqiu-collab"

main:
  python: "fitness_coach.py"
  class: "FitnessCoach"

capabilities:
  - "训练计划生成"
  - "进度追踪"
  - "智能日报"
  - "情绪陪伴"
  - "飞书同步"

tags:
  - "健身"
  - "训练"
  - "健康"
```

**发布步骤**：

```bash
# 1. 复制到OpenClaw工作区
cp -r ~/.claude/skills/fitness-coach ~/.openclaw/workspace/skills/

# 2. 发布到ClawHub
cd ~/.openclaw/workspace/skills/fitness-coach
clawhub publish . \
  --slug dexter-fitness-coach \
  --name "AI健身教练" \
  --version "1.0.1" \
  --tags "fitness,workout,training,health"

# 3. 等待安全扫描完成（5-10分钟）
```

**安装方式**：

在飞书OpenClaw中：
```
/install dexter-fitness-coach
```

或搜索：`健身` / `fitness`

---

#### 平台3：GitHub仓库

**用途**：代码托管和备份

**仓库地址**：https://github.com/dexterqiu-collab/fitness-coach

**自动部署脚本**：`auto-deploy.sh`

```bash
#!/bin/bash
# 自动化部署到GitHub和ClawHub

# 1. 创建GitHub仓库
curl -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/user/repos" \
  -d '{"name":"fitness-coach","private":false}'

# 2. 推送代码
git remote add origin "https://github.com/${GITHUB_USERNAME}/fitness-coach.git"
git push -u origin main

# 3. 发布到ClawHub
clawhub publish . --slug dexter-fitness-coach --name "AI健身教练" --version "1.0.2"
```

---

### 6.2 配置管理

**配置文件**：`config.yaml`

```yaml
# 大模型配置
llm:
  provider: "zhipu"  # 智谱GLM / claude / deepseek
  api_key: ""  # 在这里填入你的API密钥
  model: "glm-4-flash"
  temperature: 0.8
  max_tokens: 2000

# 飞书配置
feishu:
  enabled: false
  app_id: ""  # 飞书应用ID
  app_secret: ""  # 飞书应用Secret
  base_url: "https://open.feishu.cn/open-apis"

# 数据存储配置
storage:
  data_dir: "~/.claude/skills/fitness-coach/data"
  backup_enabled: true
  backup_interval: 86400  # 秒

# 教练个性配置
personality:
  style: "encouraging"  # encouraging（鼓励型） / strict（严格型） / humorous（幽默型）
  motivation_frequency: "medium"  # low / medium / high
  reminder_enabled: true

# 训练计划配置
training:
  default_frequency: 3  # 默认每周训练次数
  rest_days: ["周日"]  # 默认休息日
  session_duration: 45  # 默认训练时长（分钟）
```

---

## 7. 使用流程

### 7.1 首次使用流程

```
用户
 ↓
"你好，我是新来的，想开始健身"
 ↓
AI教练：欢迎！开始引导流程
 ↓
┌─────────────────────────────────────┐
│ 1️⃣ 收集身体数据                      │
│ - 身高、体重、体脂率                  │
│ - 目标体重                           │
│ - 训练频率                           │
└─────────────────────────────────────┘
 ↓
┌─────────────────────────────────────┐
│ 2️⃣ 生成训练计划                      │
│ - 根据目标（减脂/增肌）                │
│ - 根据频率（2-5次/周）                │
│ - 生成个性化课程                      │
└─────────────────────────────────────┘
 ↓
┌─────────────────────────────────────┐
│ 3️⃣ 完成设置                          │
│ - 保存用户档案                        │
│ - 进入活跃状态                        │
└─────────────────────────────────────┘
 ↓
"✅ 档案建立完成！现在可以开始训练了"
```

### 7.2 日常使用流程

```
用户：今天的训练计划是什么？
 ↓
AI教练：显示今日计划
 - 热身内容
 - 训练动作（组数、次数）
 - 预计时长
 ↓
[用户去训练...]
 ↓
用户：今天练了胸，卧推4组12次，引体向上4组10次
 ↓
AI教练：
 1. 解析训练内容
 2. 保存训练日志
 3. 同步到飞书
 4. 生成日报
 5. 显示进度统计
 ↓
"📊 已记录今日训练
  ✅ 训练内容：胸
  ✅ 完成动作数：2个
  💪 连续打卡：7天 🔥"
```

### 7.3 进度查看流程

```
用户：我的进度怎么样？
 ↓
AI教练：
 1. 从记忆系统读取统计
 2. 查询最近训练记录
 3. 计算连续天数
 4. 生成可视化报告
 ↓
"📈 你的训练进度
  - 本周训练：3次
  - 总训练次数：15次
  - 连续打卡：7天 🔥
  - 体重变化：80kg → 78kg"
```

---

## 8. 开发路线

### 8.1 已完成 ✅

| 功能 | 状态 | 说明 |
|------|------|------|
| 数据模型设计 | ✅ | 完整的数据结构定义 |
| 记忆管理系统 | ✅ | JSON文件存储 |
| 训练计划生成 | ✅ | 支持减脂/增肌/保持 |
| 基础对话流程 | ✅ | onboarding → active |
| 飞书集成框架 | ✅ | CSV导出 + API接口 |
| ClawHub发布 | ✅ | 技能已发布 |
| GitHub仓库 | ✅ | 代码已托管 |

### 8.2 进行中 🚧

| 功能 | 状态 | 优先级 |
|------|------|--------|
| LLM集成（智谱GLM） | 🔨 | P0 |
| 智能训练内容解析 | 🔨 | P0 |
| 个性化日报生成 | 🔨 | P1 |
| 情绪陪伴系统 | 🔨 | P1 |

### 8.3 计划中 📋

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 飞书机器人部署 | 在飞书中直接使用 | P0 |
| 多用户支持 | 支持多个用户独立使用 | P1 |
| 数据可视化 | 图表展示进度 | P1 |
| 饮食记录集成 | 记录饮食，计算卡路里 | P2 |
| 穿戴设备集成 | Apple Health / Google Fit | P2 |
| 语音交互 | 支持语音输入输出 | P3 |
| 视频演示 | 动作示范视频 | P3 |

---

## 9. 安全声明

### 9.1 使用限制

⚠️ **重要提醒**：

- 本AI教练提供的是**参考建议**，不能替代专业医疗建议
- 如有身体不适，请立即停止训练并咨询医生
- 训练请量力而行，循序渐进
- 孕妇、老年人、有慢性病者请先咨询医生

### 9.2 数据隐私

- **本地存储**：用户数据默认存储在本地JSON文件
- **数据所有权**：用户拥有自己的数据完全控制权
- **飞书同步**：启用飞书集成后，数据将同步到飞书（需用户授权）
- **不收集敏感信息**：不收集身份证号、银行卡等敏感信息

### 9.3 免责声明

```
本AI健身教练提供的建议仅供参考，不构成医疗建议。
使用本系统产生的任何后果，开发者不承担责任。
请根据自身情况合理使用，如有不适请及时就医。
```

---

## 附录

### A. 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/dexterqiu-collab/fitness-coach.git
cd fitness-coach

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置API密钥
cp config.yaml.example config.yaml
# 编辑config.yaml，填入智谱API密钥

# 4. 运行
python fitness_coach.py
```

### B. 依赖安装

```bash
# requirements.txt
requests>=2.28.0
pyyaml>=6.0
zhipuai>=4.0.0  # 智谱AI SDK
```

### C. API参考

#### 智谱GLM API

```python
# 安装
pip install zhipuai

# 使用
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {"role": "user", "content": "分析训练内容：今天练了胸，卧推4组12次"}
    ]
)
```

#### 飞书API

```python
# 获取访问令牌
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
{
  "app_id": "your-app-id",
  "app_secret": "your-app-secret"
}

# 添加记录
POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records
```

### D. 常见问题

**Q1: 如何获取智谱API密钥？**
A: 访问 https://open.bigmodel.cn/ 注册并创建API密钥

**Q2: 飞书集成如何配置？**
A: 在飞书开放平台创建应用，获取App ID和App Secret，填入config.yaml

**Q3: 数据存储在哪里？**
A: 默认存储在 `~/.claude/skills/fitness-coach/data/` 目录

**Q4: 如何导出数据？**
A: 使用飞书集成的CSV导出功能，或直接复制data目录

**Q5: 支持多用户吗？**
A: 当前版本支持多用户，每个用户有独立的user_id和数据文件

---

## 联系方式

- **GitHub**: https://github.com/dexterqiu-collab/fitness-coach
- **ClawHub**: https://clawhub.dev/skills/dexter-fitness-coach
- **作者**: @dexterqiu-collab

---

## 许可证

MIT-0 License

**No attribution required. Free to use, modify, and redistribute.**

---

*记住：坚持 > 完美，进步 > 速度*
