"""
数据模型定义
定义用户档案、训练计划、训练记录的数据结构
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class GoalType(Enum):
    """目标类型"""
    FAT_LOSS = "减脂"
    MUSCLE_GAIN = "增肌"
    MAINTENANCE = "保持"
    STRENGTH = "力量"


class ExperienceLevel(Enum):
    """训练经验"""
    BEGINNER = "新手"
    INTERMEDIATE = "进阶"
    ADVANCED = "高级"


@dataclass
class BodyMetrics:
    """身体指标"""
    height: float  # cm
    weight: float  # kg
    body_fat: Optional[float] = None  # %
    estimated_body_fat: Optional[float] = None  # 估算的体脂率


@dataclass
class UserProfile:
    """用户档案"""
    user_id: str
    name: Optional[str] = None
    body_metrics: Optional[BodyMetrics] = None
    target_weight: Optional[float] = None
    exercise_frequency: Optional[int] = None  # 每周次数
    diet_preference: Optional[str] = None
    goal_type: GoalType = GoalType.MAINTENANCE
    experience_level: ExperienceLevel = ExperienceLevel.BEGINNER

    # 个性化洞察
    personality_insights: Dict = field(default_factory=dict)

    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Exercise:
    """单个动作"""
    name: str
    sets: int
    reps: int
    weight: Optional[float] = None  # kg
    rest_time: Optional[int] = None  # 秒
    notes: Optional[str] = None


@dataclass
class TrainingSession:
    """训练计划单次"""
    focus: str  # 胸/背/腿/肩/手/核心
    exercises: List[Exercise]
    warmup: Optional[str] = None
    duration_estimate: Optional[int] = None  # 分钟


@dataclass
class TrainingPlan:
    """训练计划"""
    plan_id: str
    user_id: str
    name: str
    goal_type: GoalType
    sessions: List[TrainingSession]
    schedule: List[str]  # ["周一", "周三", "周五"]

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: str = "进行中"


@dataclass
class WorkoutLog:
    """训练记录"""
    log_id: str
    user_id: str
    training_date: datetime

    # 训练内容
    exercises: List[Exercise]
    focus: str

    # 完成情况
    completion_rate: float = 100.0  # %
    user_feedback: Optional[str] = None
    feeling_score: Optional[int] = None  # 1-5

    # 数据记录
    weight_logged: Optional[float] = None
    notes: Optional[str] = None

    # 日报
    daily_report: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProgressTracker:
    """进度追踪"""
    user_id: str

    # 训练统计
    total_sessions: int = 0
    current_streak: int = 0  # 连续天数
    longest_streak: int = 0

    # 进度数据
    weight_history: List[Dict] = field(default_factory=list)  # [{"date": ..., "weight": ...}]
    last_workout_date: Optional[datetime] = None
    next_workout_date: Optional[datetime] = None

    # 成就
    achievements: List[str] = field(default_factory=list)


@dataclass
class ConversationMemory:
    """对话记忆"""
    user_id: str
    short_term: List[Dict] = field(default_factory=list)  # 最近10轮对话
    long_term_insights: List[str] = field(default_factory=list)  # 长期洞察

    # 情感记忆
    motivation_events: List[Dict] = field(default_factory=list)  # 激励事件
    frustration_points: List[str] = field(default_factory=list)  # 挫折点
