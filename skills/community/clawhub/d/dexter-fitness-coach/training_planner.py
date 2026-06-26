"""
训练计划生成器
根据用户档案生成个性化训练计划
"""
from typing import List, Dict
from data_models import UserProfile, TrainingPlan, TrainingSession, Exercise, GoalType


class TrainingPlanner:
    """训练计划生成器"""

    # 训练动作库
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
        "肩": {
            "compound": ["推举", "哑铃推举"],
            "front": ["前平举"],
            "side": ["侧平举"],
            "rear": ["面拉", "反向飞鸟"]
        },
        "二头": {
            "exercises": ["杠铃弯举", "哑铃弯举", "锤式弯举", "集中弯举"]
        },
        "三头": {
            "exercises": ["绳索下压", "哑铃颈后臂屈伸", "窄距卧推", "双杠臂屈伸"]
        },
        "核心": {
            "exercises": ["平板支撑", "卷腹", "举腿", "俄罗斯转体"]
        }
    }

    def __init__(self):
        """初始化训练计划生成器"""
        pass

    def generate_plan(self, profile: UserProfile) -> TrainingPlan:
        """生成训练计划"""
        plan_id = f"plan_{profile.user_id}_{int(datetime.now().timestamp())}"

        # 根据目标确定训练重点
        sessions = self._create_sessions(profile)

        # 生成时间表
        schedule = self._create_schedule(profile.exercise_frequency or 3)

        plan = TrainingPlan(
            plan_id=plan_id,
            user_id=profile.user_id,
            name=f"{profile.goal_type}计划",
            goal_type=profile.goal_type,
            sessions=sessions,
            schedule=schedule
        )

        return plan

    def _create_sessions(self, profile: UserProfile) -> List[TrainingSession]:
        """创建训练课程"""
        frequency = profile.exercise_frequency or 3
        goal = profile.goal_type

        if goal == "减脂":
            return self._create_fat_loss_sessions(frequency)
        elif goal == "增肌":
            return self._create_muscle_gain_sessions(frequency)
        else:
            return self._create_maintenance_sessions(frequency)

    def _create_fat_loss_sessions(self, frequency: int) -> List[TrainingSession]:
        """创建减脂期训练（全身训练为主）"""
        sessions = []

        if frequency == 2:
            # 每周2次：全身训练
            sessions.append(self._create_full_body_session("全身A"))
            sessions.append(self._create_full_body_session("全身B"))

        elif frequency == 3:
            # 每周3次：全身+上下肢分化
            sessions.append(self._create_full_body_session("全身"))
            sessions.append(self._create_upper_lower_session("上肢"))
            sessions.append(self._create_upper_lower_session("下肢"))

        else:  # 4+ 次
            # 推拉腿分化
            sessions.append(self._create_ppl_session("推"))
            sessions.append(self._create_ppl_session("拉"))
            sessions.append(self._create_ppl_session("腿"))
            sessions.append(self._create_full_body_session("全身"))

        return sessions

    def _create_muscle_gain_sessions(self, frequency: int) -> List[TrainingSession]:
        """创建增肌期训练（分化训练为主）"""
        sessions = []

        if frequency == 3:
            # 推拉腿
            sessions.append(self._create_ppl_session("推"))
            sessions.append(self._create_ppl_session("拉"))
            sessions.append(self._create_ppl_session("腿"))

        else:  # 4+ 次
            # 更细的分化
            sessions.append(self._create_ppl_session("胸+三头"))
            sessions.append(self._create_ppl_session("背+二头"))
            sessions.append(self._create_ppl_session("腿+肩"))
            sessions.append(self._create_weak_point_session("弱项强化"))

        return sessions

    def _create_maintenance_sessions(self, frequency: int) -> List[TrainingSession]:
        """创建保持期训练"""
        return self._create_fat_loss_sessions(frequency)

    def _create_full_body_session(self, name: str) -> TrainingSession:
        """创建全身训练"""
        exercises = [
            Exercise(name="深蹲", sets=3, reps=12, weight=None),
            Exercise(name="卧推", sets=3, reps=12, weight=None),
            Exercise(name="划船", sets=3, reps=12, weight=None),
            Exercise(name="推举", sets=3, reps=12, weight=None),
            Exercise(name="平板支撑", sets=3, reps=30, weight=None),
        ]

        return TrainingSession(
            focus=name,
            exercises=exercises,
            warmup="5分钟慢跑 + 动态拉伸",
            duration_estimate=45
        )

    def _create_upper_lower_session(self, focus: str) -> TrainingSession:
        """创建上/下肢训练"""
        if focus == "上肢":
            exercises = [
                Exercise(name="卧推", sets=4, reps=10, weight=None),
                Exercise(name="划船", sets=4, reps=10, weight=None),
                Exercise(name="推举", sets=3, reps=12, weight=None),
                Exercise(name="弯举", sets=3, reps=12, weight=None),
                Exercise(name="绳索下压", sets=3, reps=12, weight=None),
            ]
        else:  # 下肢
            exercises = [
                Exercise(name="深蹲", sets=4, reps=10, weight=None),
                Exercise(name="腿举", sets=3, reps=12, weight=None),
                Exercise(name="腿弯举", sets=3, reps=12, weight=None),
                Exercise(name="提踵", sets=3, reps=15, weight=None),
                Exercise(name="平板支撑", sets=3, reps=45, weight=None),
            ]

        return TrainingSession(
            focus=focus,
            exercises=exercises,
            warmup="5分钟慢跑 + 关节活动",
            duration_estimate=50
        )

    def _create_ppl_session(self, focus: str) -> TrainingSession:
        """创建推/拉/腿训练"""
        if focus == "推" or focus == "胸+三头":
            exercises = [
                Exercise(name="卧推", sets=4, reps=8-12, weight=None),
                Exercise(name="推举", sets=3, reps=10, weight=None),
                Exercise(name="侧平举", sets=3, reps=12, weight=None),
                Exercise(name="绳索下压", sets=3, reps=12, weight=None),
                Exercise(name="双杠臂屈伸", sets=3, reps=10, weight=None),
            ]
        elif focus == "拉" or focus == "背+二头":
            exercises = [
                Exercise(name="引体向上", sets=4, reps=8-12, weight=None),
                Exercise(name="杠铃划船", sets=3, reps=10, weight=None),
                Exercise(name="面拉", sets=3, reps=12, weight=None),
                Exercise(name="弯举", sets=3, reps=12, weight=None),
                Exercise(name="锤式弯举", sets=3, reps=12, weight=None),
            ]
        else:  # 腿 或 腿+肩
            exercises = [
                Exercise(name="深蹲", sets=4, reps=8-10, weight=None),
                Exercise(name="腿举", sets=3, reps=10, weight=None),
                Exercise(name="罗马尼亚硬拉", sets=3, reps=10, weight=None),
                Exercise(name="腿弯举", sets=3, reps=12, weight=None),
                Exercise(name="提踵", sets=4, reps=15, weight=None),
            ]

        return TrainingSession(
            focus=focus,
            exercises=exercises,
            warmup="5-10分钟有氧 + 动态拉伸",
            duration_estimate=60
        )

    def _create_weak_point_session(self, focus: str) -> TrainingSession:
        """创建弱项强化训练"""
        exercises = [
            Exercise(name="根据个人情况定制", sets=4, reps=10, weight=None),
        ]

        return TrainingSession(
            focus=focus,
            exercises=exercises,
            warmup="充分热身",
            duration_estimate=45
        )

    def _create_schedule(self, frequency: int) -> List[str]:
        """创建训练时间表"""
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

        if frequency == 2:
            return ["周一", "周四"]
        elif frequency == 3:
            return ["周一", "周三", "周五"]
        elif frequency == 4:
            return ["周一", "周二", "周四", "周五"]
        else:
            return ["周一", "周二", "周三", "周四", "周五"]

    def adjust_intensity(self, exercises: List[Exercise], feedback: str) -> List[Exercise]:
        """根据反馈调整强度"""
        # 简单的强度调整逻辑
        # 可以用LLM来更智能地调整

        feedback_lower = feedback.lower()

        for ex in exercises:
            if "太轻松" in feedback_lower or "太简单" in feedback_lower:
                if ex.reps:
                    ex.reps = max(ex.reps - 2, 6)
            elif "太累" in feedback_lower or "太难" in feedback_lower:
                if ex.reps:
                    ex.reps = ex.reps + 2

        return exercises


# 辅助函数
from datetime import datetime
