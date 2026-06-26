# ComfyUI Running Skill - Python Package Init
"""
ComfyUI 全自动运行技能包

用法：
    from comfyui_automation import quick_generate, ComfyUIAutomation
    
    # 一句话生成
    result = quick_generate("a cute cat")
    
    # 完整控制
    automation = ComfyUIAutomation()
    result = automation.generate("a cat", steps=25)
"""

from .comfyui_automation import (
    ComfyUIAutomation,
    quick_generate,
    _ensure_dependencies,
)

__all__ = [
    'ComfyUIAutomation',
    'quick_generate',
    '_ensure_dependencies',
]

# 版本信息
__version__ = '2.0.0'
