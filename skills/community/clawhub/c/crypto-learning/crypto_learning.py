#!/usr/bin/env python3
"""
加密货币学习计划 - Crypto Learning Plan
为 hmzo 提供每日加密货币学习内容推送
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path

# 文件路径
SCRIPT_DIR = Path(__file__).parent
CONTENT_FILE = SCRIPT_DIR / "content.json"
PROGRESS_FILE = SCRIPT_DIR / "progress.json"


class CryptoLearning:
    def __init__(self):
        self.content = self._load_content()
        self.progress = self._load_progress()

    def _load_content(self):
        """加载学习内容"""
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_progress(self):
        """加载学习进度"""
        if not PROGRESS_FILE.exists():
            return self._init_progress()
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_progress(self):
        """保存学习进度"""
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)

    def _init_progress(self):
        """初始化进度"""
        return {
            "user_id": "hmzo",
            "started_at": None,
            "current_stage": "beginner",
            "current_topic_index": 0,
            "current_subtopic_index": 0,
            "completed_subtopics": [],
            "skipped_dates": [],
            "last_push_date": None,
            "total_days_completed": 0,
            "enabled": False
        }

    def start(self):
        """开始学习计划"""
        if self.progress["enabled"]:
            return "学习计划已经在进行中！使用 'status' 查看进度。"

        self.progress["enabled"] = True
        self.progress["started_at"] = datetime.now().isoformat()
        self.progress["last_push_date"] = date.today().isoformat()
        self._save_progress()

        return "🎉 加密货币学习计划已启动！明天早上9点将收到第一课。"

    def stop(self):
        """停止学习计划"""
        if not self.progress["enabled"]:
            return "学习计划未启动。"

        self.progress["enabled"] = False
        self._save_progress()
        return "⏸️ 学习计划已暂停。使用 'start' 重新开始。"

    def reset(self):
        """重置学习计划"""
        self.progress = self._init_progress()
        self._save_progress()
        return "🔄 学习计划已重置。使用 'start' 重新开始。"

    def skip_today(self):
        """跳过今天的学习"""
        if not self.progress["enabled"]:
            return "学习计划未启动。"

        today = date.today().isoformat()
        if today in self.progress["skipped_dates"]:
            return "今天已经跳过了。"

        self.progress["skipped_dates"].append(today)
        self._save_progress()
        return "⏭️ 已跳过今天的学习。"

    def get_status(self):
        """获取学习状态"""
        if not self.progress["started_at"]:
            return "📊 学习计划尚未开始。使用 'start' 开始学习。"

        stage = self.progress["current_stage"]
        stage_info = self.content["stages"][stage]
        topic_idx = self.progress["current_topic_index"]
        subtopic_idx = self.progress["current_subtopic_index"]

        if topic_idx < len(stage_info["topics"]):
            topic = stage_info["topics"][topic_idx]
            if subtopic_idx < len(topic["subtopics"]):
                subtopic = topic["subtopics"][subtopic_idx]
                current = f"{stage_info['name']} - {topic['name']} - {subtopic['title']}"
            else:
                current = f"{stage_info['name']} - {topic['name']}（已完成）"
        else:
            current = f"{stage_info['name']}（已完成）"

        status = f"""📊 学习进度

当前阶段：{stage_info['name']}
当前学习：{current}
已完成天数：{self.progress['total_days_completed']}
状态：{'进行中 🟢' if self.progress['enabled'] else '已暂停 🔴'}

使用 'next' 获取今日学习内容
使用 'start' 开始/继续
使用 'stop' 暂停
使用 'reset' 重置
"""
        return status

    def get_next_content(self):
        """获取下一个学习内容"""
        if not self.progress["enabled"]:
            return "学习计划未启动。使用 'start' 开始。"

        stage_key = self.progress["current_stage"]
        stage = self.content["stages"][stage_key]
        topic_idx = self.progress["current_topic_index"]
        subtopic_idx = self.progress["current_subtopic_index"]

        # 检查是否完成当前阶段
        if topic_idx >= len(stage["topics"]):
            # 进入下一阶段
            next_stage = self._get_next_stage(stage_key)
            if next_stage:
                self.progress["current_stage"] = next_stage
                self.progress["current_topic_index"] = 0
                self.progress["current_subtopic_index"] = 0
                return self.get_next_content()
            else:
                return "🎊 恭喜！你已经完成了所有学习内容！"

        topic = stage["topics"][topic_idx]

        # 检查是否完成当前主题
        if subtopic_idx >= len(topic["subtopics"]):
            # 进入下一个主题
            self.progress["current_topic_index"] += 1
            self.progress["current_subtopic_index"] = 0
            return self.get_next_content()

        subtopic = topic["subtopics"][subtopic_idx]

        # 更新进度
        self.progress["current_subtopic_index"] += 1
        self.progress["total_days_completed"] += 1
        self.progress["last_push_date"] = date.today().isoformat()
        self._save_progress()

        # 格式化消息
        message = f"""📚 加密货币学习计划 - 第 {self.progress['total_days_completed']} 天

【{stage['name']}】{topic['name']}
📖 {subtopic['title']}

{subtopic['content']}

---
💡 每天进步一点点，坚持就是胜利！
使用 'status' 查看进度
"""
        return message

    def _get_next_stage(self, current_stage):
        """获取下一个阶段"""
        stages_order = ["beginner", "investment", "advanced"]
        try:
            idx = stages_order.index(current_stage)
            if idx + 1 < len(stages_order):
                return stages_order[idx + 1]
        except ValueError:
            pass
        return None

    def get_all_content_summary(self):
        """获取所有内容概览"""
        summary = "📖 学习内容概览\n\n"

        for stage_key, stage in self.content["stages"].items():
            summary += f"【{stage['name']}】{stage['description']}（{stage['duration_days']}天）\n"
            for topic in stage["topics"]:
                summary += f"  • {topic['name']}\n"
                for subtopic in topic["subtopics"]:
                    summary += f"    - {subtopic['title']}\n"
            summary += "\n"

        total_days = sum(s["duration_days"] for s in self.content["stages"].values())
        summary += f"总计：{total_days} 天学习内容\n"

        return summary


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python crypto_learning.py start     - 开始学习计划")
        print("  python crypto_learning.py stop      - 停止学习计划")
        print("  python crypto_learning.py reset     - 重置学习计划")
        print("  python crypto_learning.py status    - 查看进度")
        print("  python crypto_learning.py next      - 获取今日学习内容")
        print("  python crypto_learning.py skip      - 跳过今天")
        print("  python crypto_learning.py summary   - 查看所有内容")
        return

    learning = CryptoLearning()
    command = sys.argv[1].lower()

    if command == "start":
        print(learning.start())
    elif command == "stop":
        print(learning.stop())
    elif command == "reset":
        print(learning.reset())
    elif command == "status":
        print(learning.get_status())
    elif command == "next":
        print(learning.get_next_content())
    elif command == "skip":
        print(learning.skip_today())
    elif command == "summary":
        print(learning.get_all_content_summary())
    else:
        print(f"未知命令: {command}")
        print("使用 'python crypto_learning.py' 查看帮助")


if __name__ == "__main__":
    main()
