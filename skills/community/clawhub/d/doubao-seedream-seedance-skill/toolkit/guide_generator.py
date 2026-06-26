"""
Guide generator for Volcengine API Skill.

Provides contextual guidance for users.
"""

from typing import List, Dict, Any, Optional
from toolkit.models.base import TaskType
from toolkit.state_manager import StateManager


class GuideGenerator:
    """
    Generates contextual guidance for users.
    
    Features:
    - Initial welcome guide
    - Post-operation suggestions
    - Context-aware recommendations
    - User preference learning
    """
    
    @staticmethod
    def get_welcome_guide() -> str:
        """
        Get initial welcome guide.
        
        Returns:
            Welcome message with available features
        """
        return """
🎨 火山引擎API助手已就绪！

我可以帮您：

1. 生成图像
   - 文本生成图片（Seedream 4.0）
   - 图片编辑
   - 图生图

2. 生成视频
   - 文本生成视频（Seedance 1.5）
   - 图片生成视频
   - 控制镜头运动

3. 视觉理解
   - 图像内容分析
   - 对象检测

4. 任务管理
   - 查看生成进度
   - 下载结果
   - 管理历史记录

5. 配置设置
   - 设置API Key
   - 调整默认参数
   - 查看配置

请告诉我您想要做什么？
"""
    
    @staticmethod
    def get_post_operation_guide(
        task_type: TaskType,
        result: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get guide after completing an operation.
        
        Args:
            task_type: Type of completed task
            result: Task result data
            
        Returns:
            Post-operation suggestions
        """
        guides = {
            TaskType.IMAGE_GENERATION: GuideGenerator._get_image_post_guide(result),
            TaskType.IMAGE_EDIT: GuideGenerator._get_image_post_guide(result),
            TaskType.VIDEO_T2V: GuideGenerator._get_video_post_guide(result),
            TaskType.VIDEO_I2V: GuideGenerator._get_video_post_guide(result),
            TaskType.VISION_DETECTION: GuideGenerator._get_vision_post_guide(result),
        }
        
        
        return guides.get(task_type, "✅ 操作完成！\n\n还需要其他帮助吗？")
    
    @staticmethod
    @staticmethod
    def _get_image_post_guide(result: Optional[Dict[str, Any]]) -> str:
        """Get guide after image operation."""
        message = """✅ 图片生成成功！

🎬 接下来您可以用这张图片：

┌─────────────────────────────────────────┐
│  📹 图生视频 (Image-to-Video)            │
├─────────────────────────────────────────┤
│  "用这张图片生成视频，镜头缓缓推进"         │
│  "让图片动起来，添加镜头运动效果"          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🎞️ 首尾帧视频 (Frame-to-Frame)          │
├─────────────────────────────────────────┤
│  "以这张图片为首帧，生成过渡到[描述]的视频" │
│  "从这张图片过渡到另一张图片"              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🎨 图生图 (Image-to-Image)              │
├─────────────────────────────────────────┤
│  "把这张图片转换成油画风格"               │
│  "在这张图片基础上修改[描述]"             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  ✏️ 图片编辑 (Image Edit)                │
├─────────────────────────────────────────┤
│  "编辑这张图片，[描述修改内容]"            │
│  "移除图片中的[对象]"                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  👁️ 视觉理解 (Vision Understanding)      │
├─────────────────────────────────────────┤
│  "分析这张图片的内容"                    │
│  "识别图片中的物体"                      │
└─────────────────────────────────────────┘

"""
        
        # 如果有图片URL，添加链接
        if result and result.get("url"):
            message += f"📷 图片链接: {result['url']}\n"
            message += "⚠️  链接有效期24小时，请及时保存\n\n"
        
        message += """💡 提示：直接告诉我您想做什么即可，例如：
   "用这张图生成一个5秒的视频"
   "把这张图转成水彩画风格"
   "分析这张图片里有什么"

您想继续做什么？"""
        
        return message
    @staticmethod
    def _get_video_post_guide(result: Optional[Dict[str, Any]]) -> str:
        """Get guide after video operation."""
        message = """✅ 视频生成成功！

🎬 接下来您可以用这个视频：

┌─────────────────────────────────────────┐
│  ✂️ 视频编辑 (Video Edit)                 │
├─────────────────────────────────────────┤
│  "裁剪视频，保留前3秒"                    │
│  "合并多个视频片段"                   │
│  "添加背景音乐"                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🖼️ 提取视频帧 (Extract Frames)             │
├─────────────────────────────────────────┤
│  "提取视频的关键帧作为图片"              │
│  "从视频中截取某一帧"                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🎞 图生视频 (Image-to-Video)             │
├─────────────────────────────────────────┤
│  "用视频帧生成新视频"                   │
│  "从视频中提取帧，生成新视频"            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🔄 继续创作 (Continue Creating)             │
├─────────────────────────────────────────┤
│  "生成更多类似风格的视频"                │
│  "调整参数，生成不同效果"              │
└─────────────────────────────────────────┘

"""
        
        if result and result.get("url"):
            message += f"🎬 视频链接: {result['url']}\n"
            message += "⚠️  链接有效期24小时，请及时保存\n\n"
        
        message += """💡 提示：直接告诉我您想做什么即可。

您想继续做什么？"""
        
        return message
    
    @staticmethod
    def _get_vision_post_guide(result: Optional[Dict[str, Any]]) -> str:
        message = """✅ 图像分析完成！

👁️ 接下来您可以用这个分析结果：

┌─────────────────────────────────────────┐
│  🎨 生成相关图片 (Generate Related Images)   │
├─────────────────────────────────────────┤
│  "根据分析内容生成类似图片"             │
│  "生成与图片风格一致的新图"             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🎬 生成描述视频 (Generate Description Video)  │
├─────────────────────────────────────────┤
│  "把图片内容转换成视频"                │
│  "用图片作为视频首帧"                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🔄 继续分析 (Continue Analysis)           │
├─────────────────────────────────────────┤
│  "分析更多图片"                        │
│  "深入分析某个特定区域"                 │
└─────────────────────────────────────────┘

"""
        
        message += """💡 提示：直接告诉我您想做什么即可。

您想继续做什么？"""
        
        return message
    
    @staticmethod
    def get_contextual_suggestions(
        state_manager: StateManager,
        current_context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Get contextual suggestions based on user history.
        
        Args:
            state_manager: State manager with user history
            current_context: Current operation context
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        # Get user preferences
        default_model = state_manager.get_preference("default_model")
        if default_model:
            suggestions.append(f"使用默认模型: {default_model}")
        
        # Get recent operations
        recent_ops = state_manager.get_history(limit=5)
        if recent_ops:
            op_types = [op["operation"] for op in recent_ops]
            most_common = max(set(op_types), key=op_types.count)
            suggestions.append(f"继续{most_common}操作")
        
        # Context-specific suggestions
        if current_context:
            if current_context.get("has_image"):
                suggestions.append("用此图片生成视频")
            if current_context.get("has_video"):
                suggestions.append("提取视频帧")
        
        return suggestions[:3]  # Limit to top 3
