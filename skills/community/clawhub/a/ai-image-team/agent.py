# 🎨 AI 电商图片创作团队协调器

"""
协调 🧠 策划师、🎭 执行师、✅ 质检师 三个独立技能
形成完整的电商图片创作工作流
"""

from typing import Dict, List, Optional
import json
import os
from datetime import datetime

# 导入各成员 Agent
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../ai-planner'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../ai-maker'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../ai-reviewer'))

from planner import PlannerAgent
from maker import MakerAgent
from reviewer import ReviewerAgent


class AIImageTeam:
    """AI 电商图片创作团队协调器"""
    
    def __init__(self):
        self.name = "🎨 AI 电商图片创作团队"
        self.config = self._load_config()
        
        # 初始化成员 Agent
        self.planner = PlannerAgent() if self.config["members"]["planner"]["enabled"] else None
        self.maker = MakerAgent() if self.config["members"]["maker"]["enabled"] else None
        self.reviewer = ReviewerAgent() if self.config["members"]["reviewer"]["enabled"] else None
    
    def _load_config(self) -> Dict:
        """加载团队配置"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config/team_config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "members": {
                "planner": {"enabled": True, "skill": "ai-planner"},
                "maker": {"enabled": True, "skill": "ai-maker"},
                "reviewer": {"enabled": True, "skill": "ai-reviewer"}
            },
            "quality_threshold": 0.8,
            "max_iterations": 3,
            "auto_mode": True
        }
    
    def create(self, user_input: str) -> Dict:
        """
        完整创作流程
        
        Args:
            user_input: 用户中文需求描述
            
        Returns:
            最终交付结果
        """
        iteration_count = 0
        max_iterations = self.config.get("max_iterations", 3)
        current_brief = None
        
        while iteration_count < max_iterations:
            iteration_count += 1
            
            # 阶段 1：策划师分析
            if self.planner:
                brief = self.planner.analyze(user_input)
                
                if brief.get("type") == "clarification":
                    return {
                        "status": "need_clarification",
                        "agent": "team",
                        "questions": brief.get("questions", []),
                        "message": "需要进一步了解您的需求"
                    }
                
                current_brief = brief
            else:
                return {"error": "策划师未启用"}
            
            # 阶段 2：执行师生成
            if self.maker:
                generation_result = self.maker.generate(current_brief)
                
                if generation_result.get("status") == "error":
                    return {
                        "status": "error",
                        "agent": "team",
                        "message": generation_result.get("message", "生成失败")
                    }
                
                images = generation_result.get("images", [])
            else:
                return {"error": "执行师未启用"}
            
            # 阶段 3：质检师把关
            if self.reviewer:
                review_result = self.reviewer.review(images, current_brief)
                overall = review_result.get("overall", {})
                
                if overall.get("verdict") == "pass":
                    # 通过，交付
                    return self._deliver(current_brief, generation_result, review_result)
                
                elif overall.get("verdict") == "minor_revision":
                    # 微调
                    iteration_plan = self.reviewer.get_iteration_plan(review_result["image_reports"])
                    suggestions = iteration_plan.get("suggestions", [])
                    
                    if suggestions:
                        # 调整 Prompt 后重新生成
                        adjustment = "，".join(suggestions[:2])
                        user_input = f"{user_input}，{adjustment}"
                        continue
                    else:
                        return self._deliver(current_brief, generation_result, review_result)
                
                else:
                    # 返工，重新规划
                    return {
                        "status": "need_major_revision",
                        "agent": "team",
                        "message": "需要重新规划",
                        "review": review_result,
                        "iteration": iteration_count
                    }
            else:
                # 无质检师，直接交付
                return self._deliver(current_brief, generation_result, None)
        
        # 达到最大迭代次数
        return {
            "status": "max_iterations_reached",
            "agent": "team",
            "message": f"已达到最大迭代次数 ({max_iterations})",
            "current_brief": current_brief
        }
    
    def _deliver(self, brief: Dict, generation: Dict, review: Optional[Dict]) -> Dict:
        """交付结果"""
        result = {
            "status": "delivered",
            "agent": "team",
            "timestamp": datetime.now().isoformat(),
            "brief": brief,
            "generation": generation,
            "images": generation.get("images", [])
        }
        
        if review:
            result["review"] = review
        
        # 保存项目历史
        self._save_project_history(result)
        
        return result
    
    def _save_project_history(self, result: Dict):
        """保存项目历史"""
        history_path = os.path.join(os.path.dirname(__file__), 'memory/project_history.md')
        
        try:
            os.makedirs(os.path.dirname(history_path), exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            product_type = result.get("brief", {}).get("product_info", {}).get("type", "未知")
            tool = result.get("generation", {}).get("tool_name", "未知")
            status = result.get("status", "未知")
            
            with open(history_path, 'a', encoding='utf-8') as f:
                f.write(f"\n## [{timestamp}] {product_type} - {tool}\n")
                f.write(f"- 状态：{status}\n")
                f.write(f"- 工具：{tool}\n")
                f.write(f"- 图片数：{len(result.get('images', []))}\n")
                f.write("---\n")
        except Exception as e:
            print(f"保存项目历史失败：{e}")


# 快捷函数
def create_image(user_input: str) -> Dict:
    """快捷创建图片"""
    team = AIImageTeam()
    return team.create(user_input)


if __name__ == "__main__":
    test_input = "帮我生成一张电商海报，产品是新款运动鞋，风格科技感"
    result = create_image(test_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))
