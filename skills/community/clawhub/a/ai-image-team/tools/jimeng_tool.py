# 🎭 即梦工具封装 (Jimeng Tool)

"""
即梦 (Jimeng) 工具封装
- 网页版：https://jimeng.jianying.com/
- 擅长：海报、创意图、营销图
- 脚本：skills/jimeng/scripts/jimeng_auto.py

本文件提供即梦工具的统一调用接口
"""

from typing import Dict, List, Optional
import subprocess
import os
import json
from datetime import datetime


class JimengTool:
    """即梦工具封装"""
    
    def __init__(self):
        self.name = "即梦 (Jimeng)"
        self.script_path = self._find_script()
        self.output_dir = "output/jimeng"
    
    def _find_script(self) -> Optional[str]:
        """查找即梦自动化脚本"""
        possible_paths = [
            # 工作区技能目录
            os.path.join(os.path.dirname(__file__), '../../jimeng/scripts/jimeng_auto.py'),
            # 用户技能目录
            os.path.expanduser('~/.openclaw/workspace/skills/jimeng/scripts/jimeng_auto.py'),
            # 当前工作目录
            'skills/jimeng/scripts/jimeng_auto.py'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return None
    
    def generate(self, prompt: str, negative_prompt: str = "", 
                 quantity: int = 1, **kwargs) -> Dict:
        """
        调用即梦生成图片
        
        Args:
            prompt: 正向提示词
            negative_prompt: 负面提示词
            quantity: 生成数量
            **kwargs: 其他参数（如尺寸、风格等）
            
        Returns:
            生成结果
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, timestamp)
        
        # 确保输出目录存在
        os.makedirs(output_path, exist_ok=True)
        
        # 检查脚本是否存在
        if not self.script_path:
            return self._mock_generate(prompt, negative_prompt, quantity, output_path)
        
        # 调用脚本
        try:
            result = self._call_script(prompt, negative_prompt, quantity, output_path, kwargs)
            return result
        except Exception as e:
            return {
                "tool": "jimeng",
                "tool_name": "即梦",
                "status": "error",
                "message": f"调用即梦失败：{str(e)}",
                "fallback": self._mock_generate(prompt, negative_prompt, quantity, output_path)
            }
    
    def _call_script(self, prompt: str, negative_prompt: str, quantity: int,
                     output_path: str, kwargs: Dict) -> Dict:
        """调用即梦自动化脚本"""
        # 构建命令
        cmd = [
            "python", self.script_path,
            "--prompt", prompt,
            "--output", output_path,
            "--count", str(quantity)
        ]
        
        if negative_prompt:
            cmd.extend(["--negative", negative_prompt])
        
        # 添加额外参数
        for key, value in kwargs.items():
            cmd.extend([f"--{key}", str(value)])
        
        # 执行
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 分钟超时
        )
        
        if process.returncode != 0:
            raise Exception(f"脚本执行失败：{process.stderr}")
        
        # 解析输出
        output = json.loads(process.stdout) if process.stdout else {}
        
        return {
            "tool": "jimeng",
            "tool_name": "即梦",
            "status": "success",
            "images": output.get("images", []),
            "message": f"已使用即梦生成 {quantity} 张图片",
            "note": "即梦擅长海报和创意图，生成结果具有较强视觉冲击力"
        }
    
    def _mock_generate(self, prompt: str, negative_prompt: str, 
                       quantity: int, output_path: str) -> Dict:
        """
        模拟生成（当脚本不可用时）
        实际使用时会被真实调用替代
        """
        images = []
        for i in range(quantity):
            images.append({
                "path": os.path.join(output_path, f"image_{i+1}.png"),
                "thumbnail": os.path.join(output_path, f"thumb_{i+1}.png"),
                "prompt": prompt,
                "negative_prompt": negative_prompt
            })
        
        return {
            "tool": "jimeng",
            "tool_name": "即梦",
            "status": "success",
            "images": images,
            "message": f"[模拟] 已生成 {quantity} 张图片（脚本未就绪）",
            "note": "请确保即梦脚本可用：skills/jimeng/scripts/jimeng_auto.py"
        }
    
    def edit(self, image_path: str, prompt: str, **kwargs) -> Dict:
        """
        图像编辑（如即梦支持）
        
        Args:
            image_path: 原图路径
            prompt: 编辑指令
            **kwargs: 其他参数
            
        Returns:
            编辑结果
        """
        # 即梦网页版主要支持生成，编辑功能有限
        # 如需编辑，建议使用 Liblib 的 ControlNet
        return {
            "tool": "jimeng",
            "status": "not_supported",
            "message": "即梦暂不支持图像编辑，建议使用 LiblibAI 的 ControlNet 功能",
            "suggestion": "liblib"
        }
    
    def get_capabilities(self) -> Dict:
        """获取工具能力说明"""
        return {
            "name": "即梦 (Jimeng)",
            "url": "https://jimeng.jianying.com/",
            "strengths": ["海报设计", "创意图", "营销图", "社交媒体配图"],
            "weaknesses": ["产品精修", "细节控制"],
            "supported_features": [
                "文生图",
                "图生图",
                "尺寸选择",
                "风格选择"
            ],
            "not_supported": [
                "ControlNet",
                "局部重绘",
                "批量生成（大量）"
            ]
        }


# 使用示例
if __name__ == "__main__":
    tool = JimengTool()
    
    # 测试生成
    result = tool.generate(
        prompt="女士连衣裙，白色雪纺材质，风格简约优雅，背景干净",
        negative_prompt="模糊，变形，低质量",
        quantity=2
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
