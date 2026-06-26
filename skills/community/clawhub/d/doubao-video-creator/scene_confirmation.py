#!/usr/bin/env python3
"""
豆包视频创作助手 - 场景生成方式确认模块
处理每个场景的生成方式选择（文生视频/图生视频）
"""

import json
from typing import Dict, Optional, Tuple
from config_manager import ProjectConfig


class SceneConfirmation:
    """场景生成确认管理"""
    
    def __init__(self, project: ProjectConfig):
        self.project = project
    
    def get_scene_generation_prompt(self, scene_id: int) -> str:
        """获取场景生成方式选择提示"""
        scene = self.project.get_scene(scene_id)
        if not scene:
            return "场景未找到"
        
        prompt = f"""🎬 **场景 {scene_id} 确认** ({scene.get('time', '')})

**场景描述**: {scene.get('description', '')}
**风格**: {scene.get('style', '')}
**文案**: "{scene.get('copy', '')}"

---

**请选择生成方式**:

**A) 文生视频** - 直接用文字提示词生成
   - ✅ 优点：快速，无需生成参考图
   - ✅ 适合：简单场景、抽象画面

**B) 图生视频** - 先生成场景原型图，再基于图片生成视频
   - ✅ 优点：画面更可控，一致性更好
   - ✅ 适合：复杂场景、需要精确控制的画面

请回复 **A** 或 **B** 选择生成方式 📝"""
        
        return prompt
    
    def process_generation_choice(self, scene_id: int, choice: str) -> Tuple[bool, str]:
        """
        处理用户的生成方式选择
        
        Args:
            scene_id: 场景 ID
            choice: 用户选择 ('A' 或 'B')
            
        Returns:
            (success, message): 处理结果和提示信息
        """
        choice = choice.strip().upper()
        
        if choice == 'A':
            mode = 'text_to_video'
            self.project.set_scene_generation_mode(scene_id, mode)
            
            scene = self.project.get_scene(scene_id)
            return True, f"""✅ 已选择 **文生视频** 模式

接下来将生成场景提示词，请确认后再开始生成视频。"""
            
        elif choice == 'B':
            mode = 'image_to_video'
            self.project.set_scene_generation_mode(scene_id, mode)
            
            scene = self.project.get_scene(scene_id)
            return True, f"""✅ 已选择 **图生视频** 模式

接下来将生成场景原型图：
- 描述：{scene.get('description', '')}
- 风格：{scene.get('style', '')}

原型图生成后，请确认是否用于视频生成。"""
        
        else:
            return False, "❌ 无效选择，请回复 **A** 或 **B**"
    
    def get_prototype_confirmation_prompt(self, scene_id: int, prototype_image_path: str) -> str:
        """获取原型图确认提示"""
        scene = self.project.get_scene(scene_id)
        if not scene:
            return "场景未找到"
        
        prompt = f"""🎨 **场景 {scene_id} 原型图已生成**

<qqimg>{prototype_image_path}</qqimg>

**描述**: {scene.get('description', '')}
**风格**: {scene.get('style', '')}

---

请确认：
- **A** - 确认，使用此原型图生成视频
- **B** - 需要调整（请说明调整要求）

请回复 **A** 或 **B** 📝"""
        
        return prompt
    
    def process_prototype_confirmation(self, scene_id: int, confirmed: bool, feedback: str = "") -> Tuple[bool, str]:
        """
        处理原型图确认
        
        Args:
            scene_id: 场景 ID
            confirmed: 是否确认
            feedback: 反馈（如拒绝）
            
        Returns:
            (success, message): 处理结果和提示信息
        """
        if confirmed:
            # 确认原型图
            # TODO: 更新项目配置，标记原型图已确认
            return True, f"""✅ 场景 {scene_id} 原型图已确认！

接下来将生成视频提示词，请确认后再开始生成视频。"""
        else:
            # 拒绝原型图，记录反馈
            # TODO: 更新项目配置，标记需要重新生成
            return True, f"""收到反馈：{feedback}

将重新生成场景原型图，请稍等..."""
    
    def get_prompt_confirmation_prompt(self, scene_id: int, prompt: str) -> str:
        """获取提示词确认提示"""
        scene = self.project.get_scene(scene_id)
        if not scene:
            return "场景未找到"
        
        mode_text = "图生视频" if scene.get('generation_mode') == 'image_to_video' else "文生视频"
        
        # 计算预计成本
        cost_estimate = "¥0.15-0.50"
        
        prompt_text = f"""📝 **场景 {scene_id} 提示词确认** ({mode_text})

【提示词】
```
{prompt}
```

---

这个提示词会生成：
- **时长**: {scene.get('time', '4 秒')}
- **画面**: {scene.get('description', '')}
- **风格**: {scene.get('style', '')}
- **预计成本**: {cost_estimate}

---

⚠️ **重要提醒**：
- 提示词确认后才会开始生成视频
- 生成后如需调整需要重新生成，会产生额外成本
- 请仔细检查提示词是否准确描述您想要的画面

---

请确认：
- **A** - 确认，开始生成视频 ✅
- **B** - 需要修改提示词（请说明修改要求）📝

请回复 **A** 或 **B** 📝"""
        
        return prompt_text
    
    def process_prompt_confirmation(self, scene_id: int, confirmed: bool, modifications: str = "") -> Tuple[bool, str]:
        """
        处理提示词确认
        
        Args:
            scene_id: 场景 ID
            confirmed: 是否确认
            modifications: 修改要求
            
        Returns:
            (success, message): 处理结果和提示信息
        """
        if confirmed:
            # 确认提示词
            self.project.update_scene(scene_id, {
                "prompt_confirmed": True,
                "prompt_confirmed_at": json.dumps({"timestamp": "now"})
            })
            
            return True, f"""✅ 场景 {scene_id} 提示词已确认！

开始生成视频，预计需要 1-2 分钟..."""
        else:
            # 拒绝提示词，记录修改要求
            return True, f"""收到修改要求：{modifications}

将修改提示词后重新确认。"""
    
    def get_video_confirmation_prompt(self, scene_id: int, video_path: str) -> str:
        """获取视频确认提示"""
        scene = self.project.get_scene(scene_id)
        if not scene:
            return "场景未找到"
        
        prompt = f"""🎬 **场景 {scene_id} 视频已生成**

<qqvideo>{video_path}</qqvideo>

**时长**: {scene.get('time', '4 秒')}
**提示词**: {scene.get('prompt', '')[:100]}...

---

请确认：
- **A** - 满意，确认使用此版本
- **B** - 需要重新生成（请说明调整要求）

请回复 **A** 或 **B** 📝"""
        
        return prompt
    
    def process_video_confirmation(self, scene_id: int, confirmed: bool, feedback: str = "") -> Tuple[bool, str]:
        """
        处理视频确认
        
        Args:
            scene_id: 场景 ID
            confirmed: 是否确认
            feedback: 反馈（如拒绝）
            
        Returns:
            (success, message): 处理结果和提示信息
        """
        if confirmed:
            # 确认视频
            self.project.update_scene(scene_id, {
                "video_status": "confirmed",
                "status": "confirmed"
            })
            
            return True, f"""✅ 场景 {scene_id} 已确认！

准备生成下一个场景..."""
        else:
            # 拒绝视频，记录反馈
            self.project.update_scene(scene_id, {
                "video_status": "rejected",
                "feedback": feedback,
                "status": "rejected"
            })
            
            return True, f"""收到反馈：{feedback}

将根据反馈重新生成场景 {scene_id}..."""


def format_scene_status(project: ProjectConfig) -> str:
    """格式化场景状态显示"""
    scenes = project.data.get("scenes", [])
    if not scenes:
        return "暂无场景"
    
    output = []
    output.append("📊 **场景生成进度**\n")
    
    for scene in scenes:
        status_icon = {
            "pending": "⏳",
            "generating": "🎬",
            "pending_confirmation": "📝",
            "confirmed": "✅",
            "rejected": "❌"
        }.get(scene.get("status", "pending"), "⏳")
        
        mode_icon = {
            "text_to_video": "📝",
            "image_to_video": "🖼️"
        }.get(scene.get("generation_mode", "text_to_video"), "📝")
        
        output.append(f"{status_icon} **场景 {scene['id']}** ({scene.get('time', '')}) - {scene.get('title', '')}")
        output.append(f"   生成方式：{mode_icon} {scene.get('generation_mode', 'text_to_video')}")
        output.append(f"   状态：{scene.get('status', 'pending')}")
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    # 测试
    from config_manager import get_or_create_project
    
    project = get_or_create_project(theme="测试项目")
    
    # 添加测试场景
    project.add_scene({
        "id": 1,
        "time": "0-4 秒",
        "title": "开场展示",
        "description": "手表特写，镜头从下往上扫过",
        "copy": "创新科技，改变生活",
        "style": "现代科技感"
    })
    
    # 测试场景确认
    confirmation = SceneConfirmation(project)
    print(confirmation.get_scene_generation_prompt(1))
