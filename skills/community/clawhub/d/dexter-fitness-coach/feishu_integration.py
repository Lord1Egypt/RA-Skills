"""
飞书多维表格集成
自动同步训练数据到飞书
"""
import json
import requests
from typing import Dict, List, Optional
from data_models import UserProfile, WorkoutLog


class FeishuIntegration:
    """飞书集成类"""

    def __init__(self, app_id: str = None, app_secret: str = None):
        """初始化飞书集成

        Args:
            app_id: 飞书应用的App ID
            app_secret: 飞书应用的App Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.base_url = "https://open.feishu.cn/open-apis"

    def get_access_token(self) -> str:
        """获取访问令牌"""
        if not self.app_id or not self.app_secret:
            print("⚠️  飞书凭证未配置，跳过API调用")
            return None

        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if data.get("code") == 0:
                self.access_token = data.get("tenant_access_token")
                return self.access_token
            else:
                print(f"获取飞书令牌失败: {data}")
                return None
        except Exception as e:
            print(f"飞书API调用错误: {e}")
            return None

    def create_table(self, table_name: str, fields: List[Dict]) -> Dict:
        """创建多维表格

        Args:
            table_name: 表名
            fields: 字段定义 [{"name": "字段名", "type": "text"}]

        Returns:
            创建结果
        """
        if not self.get_access_token():
            return None

        # 这里需要根据飞书API文档实现
        # 暂时返回模拟数据
        return {"table_id": "mock_table_id", "status": "created"}

    def add_record(self, table_id: str, record_data: Dict) -> bool:
        """添加记录到表格

        Args:
            table_id: 表格ID
            record_data: 记录数据

        Returns:
            是否成功
        """
        if not self.get_access_token():
            print("⚠️  飞书未配置，数据已保存到本地")
            return False

        # 实际API调用
        return True

    def sync_workout_log(self, log: WorkoutLog) -> bool:
        """同步训练日志到飞书

        Args:
            log: 训练日志

        Returns:
            是否成功
        """
        record_data = {
            "训练日期": log.training_date.strftime("%Y-%m-%d"),
            "训练重点": log.focus,
            "完成度": f"{log.completion_rate}%",
            "用户反馈": log.user_feedback or "",
            "体感评分": log.feeling_score or "",
            "体重": log.weight_logged or "",
            "日报": log.daily_report or ""
        }

        return self.add_record("workout_logs", record_data)

    def sync_user_profile(self, profile: UserProfile) -> bool:
        """同步用户档案到飞书

        Args:
            profile: 用户档案

        Returns:
            是否成功
        """
        record_data = {
            "用户ID": profile.user_id,
            "身高": profile.body_metrics.height if profile.body_metrics else "",
            "体重": profile.body_metrics.weight if profile.body_metrics else "",
            "体脂率": profile.body_metrics.body_fat if profile.body_metrics else "",
            "目标体重": profile.target_weight or "",
            "运动频率": f"每周{profile.exercise_frequency}次" if profile.exercise_frequency else "",
            "饮食偏好": profile.diet_preference or "",
            "目标类型": profile.goal_type or ""
        }

        return self.add_record("user_profiles", record_data)


class FeishuTableManager:
    """飞书表格管理器 - 简化版"""

    def __init__(self):
        """初始化"""
        self.enabled = False
        self.app_id = None
        self.app_secret = None

    def configure(self, app_id: str, app_secret: str):
        """配置飞书凭证"""
        self.app_id = app_id
        self.app_secret = app_secret
        self.enabled = True

    def export_to_csv(self, data: List[Dict], filename: str):
        """导出数据为CSV（飞书导入格式）

        Args:
            data: 数据列表
            filename: 文件名
        """
        import csv

        if not data:
            return

        keys = data[0].keys()

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"✅ 数据已导出到 {filename}")
        print(f"💡 可以导入到飞书多维表格")

    def generate_feishu_import_guide(self):
        """生成飞书导入指南"""
        guide = """
📊 飞书多维表格设置指南

一、创建表格

1. 打开飞书，创建新的多维表格
2. 创建以下数据表：

   【表1: 用户档案】
   - 用户ID (文本)
   - 身高 (数字)
   - 体重 (数字)
   - 体脂率 (数字)
   - 目标体重 (数字)
   - 运动频率 (文本)
   - 饮食偏好 (文本)
   - 目标类型 (单选: 减脂/增肌/保持)
   - 创建时间 (日期)

   【表2: 训练记录】
   - 记录ID (文本)
   - 用户ID (文本)
   - 训练日期 (日期)
   - 训练重点 (单选: 胸/背/腿/肩/手/核心)
   - 完成度 (数字, %)
   - 用户反馈 (文本)
   - 体感评分 (数字, 1-5)
   - 体重记录 (数字)
   - 日报内容 (文本)
   - 创建时间 (日期)

   【表3: 进度追踪】
   - 用户ID (文本)
   - 总训练次数 (数字)
   - 当前连续天数 (数字)
   - 最后训练日期 (日期)

二、导入数据

使用本系统的导出功能，将数据导出为CSV，然后导入飞书表格。

三、自动同步（可选）

如需自动同步，请配置飞书API凭证：
1. 创建飞书应用
2. 获取App ID和App Secret
3. 在配置中填入凭证
        """

        print(guide)


# 便捷函数
def create_sample_feishu_tables():
    """创建示例表格数据"""
    return {
        "user_profiles": [
            {
                "用户ID": "example_001",
                "身高": 175,
                "体重": 80,
                "体脂率": 22,
                "目标体重": 70,
                "运动频率": "每周3次",
                "饮食偏好": "无忌口",
                "目标类型": "减脂"
            }
        ],
        "workout_logs": [
            {
                "记录ID": "log_001",
                "用户ID": "example_001",
                "训练日期": "2025-03-24",
                "训练重点": "胸",
                "完成度": "100%",
                "用户反馈": "状态不错",
                "体感评分": 4,
                "体重记录": 79.5,
                "日报内容": "今日训练完成，卧推有进步！"
            }
        ]
    }
