"""
记忆管理系统
管理用户的短期记忆、长期记忆和情感记忆
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
from data_models import UserProfile, WorkoutLog, ConversationMemory, ProgressTracker


class MemoryManager:
    """记忆管理器"""

    def __init__(self, data_dir: str = None):
        """初始化记忆管理器"""
        if data_dir is None:
            data_dir = Path.home() / ".claude" / "skills" / "fitness-coach" / "data"
        self.data_dir = Path(data_dir)
        self.users_dir = self.data_dir / "users"
        self.logs_dir = self.data_dir / "logs"

        # 创建目录
        self.users_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def _get_user_file(self, user_id: str) -> Path:
        """获取用户档案文件路径"""
        return self.users_dir / f"{user_id}.json"

    def _get_logs_file(self, user_id: str) -> Path:
        """获取用户日志文件路径"""
        return self.logs_dir / f"{user_id}_logs.json"

    # ========== 用户档案管理 ==========

    def create_user_profile(self, user_id: str, profile_data: Dict) -> UserProfile:
        """创建新用户档案"""
        profile = UserProfile(user_id=user_id)

        # 更新基本信息
        if "height" in profile_data:
            from data_models import BodyMetrics
            profile.body_metrics = BodyMetrics(
                height=profile_data["height"],
                weight=profile_data["weight"],
                body_fat=profile_data.get("body_fat")
            )
        if "target_weight" in profile_data:
            profile.target_weight = profile_data["target_weight"]
        if "exercise_frequency" in profile_data:
            profile.exercise_frequency = profile_data["exercise_frequency"]
        if "diet_preference" in profile_data:
            profile.diet_preference = profile_data["diet_preference"]

        # 自动推断目标类型
        if profile.body_metrics and profile.target_weight:
            if profile.target_weight < profile.body_metrics.weight:
                profile.goal_type = "减脂"
            elif profile.target_weight > profile.body_metrics.weight:
                profile.goal_type = "增肌"

        # 保存
        self.save_user_profile(profile)
        return profile

    def load_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """加载用户档案"""
        file_path = self._get_user_file(user_id)
        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 重建UserProfile对象
        profile = UserProfile(user_id=user_id)
        profile.name = data.get("name")
        profile.target_weight = data.get("target_weight")
        profile.exercise_frequency = data.get("exercise_frequency")
        profile.diet_preference = data.get("diet_preference")
        profile.goal_type = data.get("goal_type", "减脂")
        profile.personality_insights = data.get("personality_insights", {})

        # 重建body_metrics
        if "body_metrics" in data:
            from data_models import BodyMetrics
            bm = data["body_metrics"]
            profile.body_metrics = BodyMetrics(
                height=bm["height"],
                weight=bm["weight"],
                body_fat=bm.get("body_fat"),
                estimated_body_fat=bm.get("estimated_body_fat")
            )

        return profile

    def save_user_profile(self, profile: UserProfile):
        """保存用户档案"""
        file_path = self._get_user_file(profile.user_id)

        data = {
            "user_id": profile.user_id,
            "name": profile.name,
            "target_weight": profile.target_weight,
            "exercise_frequency": profile.exercise_frequency,
            "diet_preference": profile.diet_preference,
            "goal_type": profile.goal_type,
            "personality_insights": profile.personality_insights,
            "created_at": profile.created_at.isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        if profile.body_metrics:
            data["body_metrics"] = {
                "height": profile.body_metrics.height,
                "weight": profile.body_metrics.weight,
                "body_fat": profile.body_metrics.body_fat,
                "estimated_body_fat": profile.body_metrics.estimated_body_fat
            }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ========== 训练日志管理 ==========

    def add_workout_log(self, log: WorkoutLog):
        """添加训练日志"""
        logs = self.load_workout_logs(log.user_id)
        logs.append({
            "log_id": log.log_id,
            "user_id": log.user_id,
            "training_date": log.training_date.isoformat(),
            "focus": log.focus,
            "exercises": [
                {
                    "name": ex.name,
                    "sets": ex.sets,
                    "reps": ex.reps,
                    "weight": ex.weight
                }
                for ex in log.exercises
            ],
            "completion_rate": log.completion_rate,
            "user_feedback": log.user_feedback,
            "feeling_score": log.feeling_score,
            "weight_logged": log.weight_logged,
            "daily_report": log.daily_report,
            "created_at": log.created_at.isoformat()
        })

        file_path = self._get_logs_file(log.user_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def load_workout_logs(self, user_id: str) -> List[Dict]:
        """加载训练日志"""
        file_path = self._get_logs_file(user_id)
        if not file_path.exists():
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_recent_logs(self, user_id: str, days: int = 7) -> List[Dict]:
        """获取最近N天的训练日志"""
        logs = self.load_workout_logs(user_id)
        cutoff_date = datetime.now() - timedelta(days=days)

        recent = []
        for log in logs:
            log_date = datetime.fromisoformat(log["training_date"])
            if log_date >= cutoff_date:
                recent.append(log)

        return recent

    # ========== 进度追踪 ==========

    def get_progress_stats(self, user_id: str) -> Dict:
        """获取进度统计"""
        profile = self.load_user_profile(user_id)
        logs = self.load_workout_logs(user_id)

        total_sessions = len(logs)

        # 计算连续打卡
        streak = 0
        if logs:
            # 按日期排序
            sorted_logs = sorted(logs, key=lambda x: x["training_date"], reverse=True)
            streak = self._calculate_streak(sorted_logs)

        # 体重历史
        weight_history = []
        for log in logs:
            if log.get("weight_logged"):
                weight_history.append({
                    "date": log["training_date"],
                    "weight": log["weight_logged"]
                })

        return {
            "total_sessions": total_sessions,
            "current_streak": streak,
            "weight_history": weight_history,
            "last_workout": logs[-1]["training_date"] if logs else None
        }

    def _calculate_streak(self, sorted_logs: List[Dict]) -> int:
        """计算连续打卡天数"""
        if not sorted_logs:
            return 0

        streak = 1
        last_date = datetime.fromisoformat(sorted_logs[0]["training_date"]).date()

        for i in range(1, len(sorted_logs)):
            current_date = datetime.fromisoformat(sorted_logs[i]["training_date"]).date()
            diff = (last_date - current_date).days

            if diff <= 2:  # 允许间隔1天
                streak += 1
                last_date = current_date
            else:
                break

        return streak

    # ========== 对话记忆 ==========

    def add_conversation(self, user_id: str, role: str, content: str):
        """添加对话记录"""
        memory_file = self.users_dir / f"{user_id}_memory.json"

        memory = {"short_term": []}
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                memory = json.load(f)

        # 添加新对话
        memory["short_term"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # 只保留最近10轮
        if len(memory["short_term"]) > 20:  # 10轮 = 20条（用户+助手）
            memory["short_term"] = memory["short_term"][-20:]

        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)

    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """获取对话历史"""
        memory_file = self.users_dir / f"{user_id}_memory.json"
        if not memory_file.exists():
            return []

        with open(memory_file, 'r', encoding='utf-8') as f:
            memory = json.load(f)

        return memory.get("short_term", [])
