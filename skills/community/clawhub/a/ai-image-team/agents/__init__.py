# AI 电商图片创作 Agent 团队

"""
AI 电商图片创作 Agent 团队 - 主入口

团队架构：
- 🧠 策划师 (Planner) - 需求分析与创意构思
- 🎭 执行师 (Maker) - 图片生成执行
- ✅ 质检师 (Reviewer) - 质量评估与迭代建议

使用方式：
1. 接收用户中文需求
2. 策划师分析需求，生成创意简报
3. 执行师调用工具生成图片
4. 质检师把关质量
5. 交付最终成品
"""

from .planner import PlannerAgent
from .maker import MakerAgent
from .reviewer import ReviewerAgent


class AIImageTeam:
    """AI 电商图片创作团队"""
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.maker = MakerAgent()
        self.reviewer = ReviewerAgent()
    
    def create(self, user_input: str) -> dict:
        """
        完整创作流程
        
        Args:
            user_input: 用户中文需求描述
            
        Returns:
            最终交付结果
        """
        # 阶段 1：策划师分析
        brief = self.planner.analyze(user_input)
        
        if brief.get("type") == "clarification":
            # 需要进一步询问
            return {
                "status": "need_clarification",
                "questions": brief.get("questions", []),
                "message": "需要进一步了解您的需求"
            }
        
        # 阶段 2：执行师生成
        generation_result = self.maker.generate(brief)
        
        if generation_result.get("status") == "error":
            return {
                "status": "error",
                "message": generation_result.get("message", "生成失败")
            }
        
        # 阶段 3：质检师把关
        images = generation_result.get("images", [])
        review_result = self.reviewer.review(images, brief)
        
        # 阶段 4：根据质检结果决策
        overall = review_result.get("overall", {})
        
        if overall.get("verdict") == "pass":
            # 通过，直接交付
            return {
                "status": "delivered",
                "message": "✅ 质检通过，已交付",
                "images": images,
                "review": review_result,
                "brief": brief
            }
        
        elif overall.get("verdict") == "minor_revision":
            # 微调
            iteration_plan = self.reviewer.get_iteration_plan(review_result["image_reports"])
            return {
                "status": "need_minor_revision",
                "message": "⚠️ 需要微调",
                "suggestions": iteration_plan.get("suggestions", []),
                "images": images,
                "review": review_result
            }
        
        else:
            # 返工，重新规划
            return {
                "status": "need_major_revision",
                "message": "❌ 需要重新规划",
                "issues": review_result.get("summary", ""),
                "brief": brief
            }


# 快捷函数
def create_image(user_input: str) -> dict:
    """快捷创建图片"""
    team = AIImageTeam()
    return team.create(user_input)


# 导出
__all__ = ["AIImageTeam", "PlannerAgent", "MakerAgent", "ReviewerAgent", "create_image"]
