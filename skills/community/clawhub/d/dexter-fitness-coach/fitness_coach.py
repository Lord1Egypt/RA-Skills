"""
AI健身教练主程序
整合所有模块，提供完整的健身指导功能
"""
import os
import sys
import uuid
from datetime import datetime
from typing import Dict, List, Optional

# 添加当前目录到路径，以便导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_models import (
    UserProfile, WorkoutLog, Exercise, GoalType,
    BodyMetrics, TrainingPlan
)
from memory_manager import MemoryManager
from training_planner import TrainingPlanner
from feishu_integration import FeishuTableManager


class FitnessCoach:
    """AI健身教练主类"""

    def __init__(self, user_id: str = None, data_dir: str = None):
        """初始化健身教练

        Args:
            user_id: 用户ID（可选，首次使用时创建）
            data_dir: 数据存储目录
        """
        self.user_id = user_id or f"user_{uuid.uuid4().hex[:8]}"
        self.memory = MemoryManager(data_dir)
        self.planner = TrainingPlanner()
        self.feishu = FeishuTableManager()

        # 状态管理
        self.profile = None
        self.current_plan = None
        self.conversation_stage = "initial"  # initial, collecting, active

        # 加载用户数据
        self._load_user_data()

    def _load_user_data(self):
        """加载用户数据"""
        self.profile = self.memory.load_user_profile(self.user_id)

        if self.profile:
            print(f"✅ 欢迎回来，{self.profile.name or '朋友'}！")
            print(f"📊 你的目标：{self.profile.goal_type}")
            self.conversation_stage = "active"
        else:
            print("👋 你好！我是你的AI健身教练 🏋️")
            print("让我先了解一下你的情况...")

    # ========== 对话流程 ==========

    def start_onboarding(self) -> str:
        """开始用户引导流程"""
        self.conversation_stage = "collecting"

        message = """
✨ **欢迎来到你的健身之旅！** ✨

为了给你制定最适合的训练计划，我需要了解几个信息：

---

**1️⃣ 身体数据**
请告诉我你的：
- 身高（cm）
- 体重（kg）
- 体脂率（不知道的话说"不清楚"就行，我会帮你估算）

例如：我身高175，体重80，体脂率不清楚

---

你可以一次性回答所有问题，也可以一个一个来 💪
        """

        return message.strip()

    def process_input(self, user_input: str) -> str:
        """处理用户输入

        Args:
            user_input: 用户输入的文本

        Returns:
            教练的回复
        """
        # 保存对话
        self.memory.add_conversation(self.user_id, "user", user_input)

        # 根据当前阶段处理
        if self.conversation_stage == "initial":
            response = self.start_onboarding()

        elif self.conversation_stage == "collecting":
            response = self._collect_info(user_input)

        elif self.conversation_stage == "active":
            response = self._active_coaching(user_input)

        else:
            response = "我该怎么帮助你？"

        # 保存回复
        self.memory.add_conversation(self.user_id, "coach", response)

        return response

    def _collect_info(self, user_input: str) -> str:
        """收集用户信息"""
        # 简单的信息提取（实际应用中可以用LLM）
        info = self._extract_user_info(user_input)

        # 检查是否收集了必要信息
        if not self.profile:
            self.profile = UserProfile(user_id=self.user_id)

        # 更新档案
        if "height" in info and "weight" in info:
            from data_models import BodyMetrics

            # 估算体脂率（如果用户不知道）
            body_fat = info.get("body_fat")
            if not body_fat and info.get("height") and info.get("weight"):
                body_fat = self._estimate_body_fat(
                    info["height"], info["weight"], info.get("gender", "male")
                )

            self.profile.body_metrics = BodyMetrics(
                height=info["height"],
                weight=info["weight"],
                body_fat=info.get("body_fat"),
                estimated_body_fat=body_fat if not info.get("body_fat") else None
            )

        if "target_weight" in info:
            self.profile.target_weight = info["target_weight"]

        if "frequency" in info:
            self.profile.exercise_frequency = info["frequency"]

        # 检查是否完整
        if self._is_profile_complete():
            return self._complete_onboarding()
        else:
            return self._ask_missing_info()

    def _active_coaching(self, user_input: str) -> str:
        """活跃期的教练对话"""
        input_lower = user_input.lower()

        # 记录训练
        if any(keyword in input_lower for keyword in ["练了", "训练", "完成", "做了"]):
            return self._process_workout_log(user_input)

        # 查看进度
        elif any(keyword in input_lower for keyword in ["进度", "怎么样", "统计", "记录"]):
            return self._show_progress()

        # 请求计划
        elif any(keyword in input_lower for keyword in ["计划", "今天练什么", "训练"]):
            return self._get_training_plan()

        # 其他
        else:
            return self._general_chat(user_input)

    # ========== 训练记录处理 ==========

    def _process_workout_log(self, user_input: str) -> str:
        """处理训练记录"""
        # 解析训练内容
        exercises = self._parse_workout_input(user_input)

        if not exercises:
            return "抱歉，我没太理解你的训练内容。能详细说说吗？"

        # 创建训练日志
        log = WorkoutLog(
            log_id=f"log_{uuid.uuid4().hex[:8]}",
            user_id=self.user_id,
            training_date=datetime.now(),
            exercises=exercises,
            focus=exercises[0].name if exercises else "综合",
            user_feedback=user_input,
            daily_report=self._generate_daily_report(exercises)
        )

        # 保存日志
        self.memory.add_workout_log(log)

        # 同步到飞书
        # self.feishu.sync_workout_log(log)

        # 生成回复
        return self._format_workout_response(log, exercises)

    def _parse_workout_input(self, text: str) -> List[Exercise]:
        """解析训练输入"""
        exercises = []

        # 简单的解析逻辑（实际应该用LLM）
        lines = text.split('\n')
        for line in lines:
            if any(char.isdigit() for char in line):
                # 提取动作信息
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[0]
                    exercises.append(Exercise(name=name, sets=3, reps=10))

        return exercises

    def _generate_daily_report(self, exercises: List[Exercise]) -> str:
        """生成日报"""
        return f"完成了{len(exercises)}个动作，训练时长约45分钟"

    def _format_workout_response(self, log: WorkoutLog, exercises: List[Exercise]) -> str:
        """格式化训练回复"""
        # 获取进度
        stats = self.memory.get_progress_stats(self.user_id)

        response = f"""
📊 **已记录今日训练**

✅ 训练内容：{log.focus}
✅ 完成动作数：{len(exercises)}

💪 **你的进度**：
- 总训练次数：{stats['total_sessions']}次
- 连续打卡：{stats['current_streak']}天 🔥

💡 **建议**：
- 训练完成得很好！
- 记得补充蛋白质
- 好好休息，明天继续

（数据已保存，可随时查看进度）
        """

        return response.strip()

    # ========== 进度查询 ==========

    def _show_progress(self) -> str:
        """显示进度"""
        stats = self.memory.get_progress_stats(self.user_id)
        logs = self.memory.get_recent_logs(self.user_id, days=7)

        response = f"""
📈 **你的训练进度**

**📊 本周统计**
- 训练次数：{len(logs)}次
- 总训练次数：{stats['total_sessions']}次
- 连续打卡：{stats['current_streak']}天 {'🔥' if stats['current_streak'] > 3 else ''}
"""

        if stats.get('weight_history'):
            latest_weight = stats['weight_history'][-1]['weight']
            if self.profile and self.profile.target_weight:
                progress = latest_weight - self.profile.target_weight
                response += f"\n- 当前体重：{latest_weight}kg"
                response += f"\n- 距离目标：还有{abs(progress):.1f}kg"

        response += "\n\n💪 继续保持，你做得很好！"

        return response.strip()

    # ========== 训练计划 ==========

    def _get_training_plan(self) -> str:
        """获取训练计划"""
        if not self.current_plan and self.profile:
            self.current_plan = self.planner.generate_plan(self.profile)

        if not self.current_plan:
            return "请先完善你的档案信息"

        plan = self.current_plan
        session = plan.sessions[0]  # 简化，只返回第一个session

        response = f"""
📋 **今日训练计划：{session.focus}**

⏱️ 预计时长：{session.duration_estimate}分钟

🔥 **热身**：
{session.warmup}

💪 **训练动作**：
"""

        for i, ex in enumerate(session.exercises, 1):
            response += f"\n{i}. **{ex.name}**"
            response += f"\n   - {ex.sets}组 × {ex.reps}次"
            if ex.weight:
                response += f" × {ex.weight}kg"

        response += "\n\n💡 记得训练完告诉我，我来帮你记录！"

        return response.strip()

    # ========== 辅助方法 ==========

    def _extract_user_info(self, text: str) -> Dict:
        """从文本中提取用户信息（简化版）"""
        info = {}
        text_lower = text.lower()

        # 提取数字
        import re
        numbers = re.findall(r'\d+\.?\d*', text)

        if numbers:
            if "身高" in text_lower or "cm" in text_lower or "厘米" in text_lower:
                info["height"] = float(numbers[0])
            elif "体重" in text_lower or "kg" in text_lower or "公斤" in text_lower:
                if len(numbers) >= 2:
                    info["height"] = float(numbers[0])
                    info["weight"] = float(numbers[1])
                else:
                    info["weight"] = float(numbers[0])

            if "目标" in text_lower:
                info["target_weight"] = float(numbers[-1])

        # 提取运动频率
        if "每周" in text_lower or "次" in text_lower:
            freq_match = re.search(r'每[周天][\s]*(\d+)[\s]*次', text_lower)
            if freq_match:
                info["frequency"] = int(freq_match.group(1))

        return info

    def _estimate_body_fat(self, height: float, weight: float, gender: str = "male") -> float:
        """估算体脂率（简化版BMI公式）"""
        bmi = weight / ((height / 100) ** 2)

        # 简化的估算公式
        if gender == "male":
            return (1.20 * bmi) + 0.23 * 30 - 10.8  # 假设30岁
        else:
            return (1.20 * bmi) + 0.23 * 30 - 5.4

    def _is_profile_complete(self) -> bool:
        """检查档案是否完整"""
        if not self.profile:
            return False
        if not self.profile.body_metrics:
            return False
        if not self.profile.body_metrics.height or not self.profile.body_metrics.weight:
            return False

        return True

    def _ask_missing_info(self) -> str:
        """询问缺失信息"""
        missing = []

        if not self.profile.body_metrics:
            missing.append("身高和体重")
        elif not self.profile.target_weight:
            missing.append("目标体重")
        elif not self.profile.exercise_frequency:
            missing.append("每周运动几次")

        if missing:
            return f"还需要知道：{', '.join(missing)}\n\n请告诉我这些信息 💪"

        return self._complete_onboarding()

    def _complete_onboarding(self) -> str:
        """完成引导"""
        # 生成训练计划
        self.current_plan = self.planner.generate_plan(self.profile)

        # 保存档案
        self.memory.save_user_profile(self.profile)

        # 更新状态
        self.conversation_stage = "active"

        # 推断目标类型
        if self.profile.body_metrics and self.profile.target_weight:
            if self.profile.target_weight < self.profile.body_metrics.weight:
                self.profile.goal_type = "减脂"
            else:
                self.profile.goal_type = "增肌"

        response = f"""
✅ **档案建立完成！**

📋 **你的信息**：
- 身高：{self.profile.body_metrics.height}cm
- 体重：{self.profile.body_metrics.weight}kg
- 目标：{self.profile.target_weight}kg
- 目标类型：{self.profile.goal_type}

🎯 **为你生成了{self.profile.goal_type}训练计划！**

---

💪 **现在你可以：**
1. 说"今天的计划" - 查看训练内容
2. 训练完后告诉我 - 我会帮你记录
3. 随时问"进度怎么样" - 查看统计

**准备好开始了吗？** 🚀
        """

        return response.strip()

    def _general_chat(self, user_input: str) -> str:
        """一般对话"""
        responses = [
            "我在这里！需要什么帮助吗？\n- 查看训练计划\n- 记录训练\n- 查看进度",
            "随时可以帮你：\n1. 制定训练计划\n2. 记录训练数据\n3. 查看进度统计",
            "今天训练了吗？练完记得告诉我哦 💪"
        ]
        import random
        return random.choice(responses)


# 便捷函数
def create_coach(user_id: str = None) -> FitnessCoach:
    """创建健身教练实例"""
    return FitnessCoach(user_id=user_id)


if __name__ == "__main__":
    # 测试代码
    coach = create_coach()

    print("=" * 50)
    print(coach.start_onboarding())
    print("=" * 50)
