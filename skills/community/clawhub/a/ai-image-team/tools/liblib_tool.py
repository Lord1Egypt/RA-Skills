# 🎨 LiblibAI 工具封装 (Liblib Tool)

"""
LiblibAI 工具封装
- 网页版：https://www.liblib.art/
- 擅长：产品精修、ControlNet 控制、多模型选择
- 脚本：skills/liblib/scripts/liblib_auto.py

本文件提供 LiblibAI 工具的统一调用接口
"""

from typing import Dict, List, Optional
import subprocess
import os
import json
from datetime import datetime


class LiblibTool:
    """LiblibAI 工具封装"""
    
    def __init__(self):
        self.name = "LiblibAI"
        self.script_path = self._find_script()
        self.output_dir = "output/liblib"
        self.default_model = "通用商业摄影模型"
    
    def _find_script(self) -> Optional[str]:
        """查找 Liblib 自动化脚本"""
        possible_paths = [
            # 工作区技能目录
            os.path.join(os.path.dirname(__file__), '../../liblib/scripts/liblib_auto.py'),
            # 用户技能目录
            os.path.expanduser('~/.openclaw/workspace/skills/liblib/scripts/liblib_auto.py'),
            # 当前工作目录
            'skills/liblib/scripts/liblib_auto.py'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return None
    
    def generate(self, prompt: str, negative_prompt: str = "", 
                 quantity: int = 1, model: str = None, **kwargs) -> Dict:
        """
        调用 LiblibAI 生成图片
        
        Args:
            prompt: 正向提示词
            negative_prompt: 负面提示词
            quantity: 生成数量
            model: 模型名称（可选，自动推荐）
            **kwargs: 其他参数（如尺寸、采样器等）
            
        Returns:
            生成结果
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, timestamp)
        
        # 确保输出目录存在
        os.makedirs(output_path, exist_ok=True)
        
        # 根据产品类型推荐模型
        if not model:
            model = self._recommend_model(kwargs.get("product_type", ""))
        
        # 检查脚本是否存在
        if not self.script_path:
            return self._mock_generate(prompt, negative_prompt, quantity, output_path, model)
        
        # 调用脚本
        try:
            result = self._call_script(prompt, negative_prompt, quantity, output_path, model, kwargs)
            return result
        except Exception as e:
            return {
                "tool": "liblib",
                "tool_name": "LiblibAI",
                "status": "error",
                "message": f"调用 LiblibAI 失败：{str(e)}",
                "fallback": self._mock_generate(prompt, negative_prompt, quantity, output_path, model)
            }
    
    def _recommend_model(self, product_type: str) -> str:
        """根据产品类型推荐模型"""
        model_map = {
            "服装": "服装展示专用模型",
            "食品": "美食摄影模型",
            "数码": "产品精修模型",
            "美妆": "美妆商业摄影模型",
            "家居": "室内场景模型",
            "人物": "人像摄影模型",
            "动漫": "二次元模型"
        }
        return model_map.get(product_type, self.default_model)
    
    def _call_script(self, prompt: str, negative_prompt: str, quantity: int,
                     output_path: str, model: str, kwargs: Dict) -> Dict:
        """调用 Liblib 自动化脚本"""
        # 构建命令
        cmd = [
            "python", self.script_path,
            "--prompt", prompt,
            "--output", output_path,
            "--count", str(quantity),
            "--model", model
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
            "tool": "liblib",
            "tool_name": "LiblibAI",
            "status": "success",
            "images": output.get("images", []),
            "model_used": model,
            "message": f"已使用 LiblibAI 生成 {quantity} 张图片",
            "note": f"使用 {model} 模型，适合精细化的产品图生成"
        }
    
    def _mock_generate(self, prompt: str, negative_prompt: str, 
                       quantity: int, output_path: str, model: str) -> Dict:
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
                "negative_prompt": negative_prompt,
                "model": model
            })
        
        return {
            "tool": "liblib",
            "tool_name": "LiblibAI",
            "status": "success",
            "images": images,
            "model_used": model,
            "message": f"[模拟] 已生成 {quantity} 张图片（脚本未就绪）",
            "note": "请确保 Liblib 脚本可用：skills/liblib/scripts/liblib_auto.py"
        }
    
    def controlnet(self, image_path: str, prompt: str, 
                   control_type: str = "canny", **kwargs) -> Dict:
        """
        ControlNet 控制生成
        
        Args:
            image_path: 参考图路径
            prompt: 提示词
            control_type: 控制类型（canny/depth/pose/openpose 等）
            **kwargs: 其他参数
            
        Returns:
            生成结果
        """
        # Liblib 支持多种 ControlNet 模式
        control_types = {
            "canny": "边缘检测",
            "depth": "深度图",
            "pose": "人体姿态",
            "openpose": "OpenPose 姿态",
            "tile": "细节增强",
            "inpaint": "局部重绘"
        }
        
        if control_type not in control_types:
            return {
                "tool": "liblib",
                "status": "error",
                "message": f"不支持的 ControlNet 类型：{control_type}",
                "supported": list(control_types.keys())
            }
        
        # 调用脚本（如支持）
        if self.script_path:
            try:
                cmd = [
                    "python", self.script_path,
                    "--controlnet",
                    "--reference", image_path,
                    "--prompt", prompt,
                    "--control-type", control_type
                ]
                
                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if process.returncode != 0:
                    raise Exception(f"脚本执行失败：{process.stderr}")
                
                output = json.loads(process.stdout) if process.stdout else {}
                
                return {
                    "tool": "liblib",
                    "tool_name": "LiblibAI",
                    "status": "success",
                    "control_type": control_type,
                    "control_type_name": control_types[control_type],
                    "images": output.get("images", []),
                    "message": f"已使用 ControlNet ({control_types[control_type]}) 生成图片"
                }
            except Exception as e:
                return {
                    "tool": "liblib",
                    "status": "error",
                    "message": f"ControlNet 调用失败：{str(e)}"
                }
        
        # 脚本不可用时的提示
        return {
            "tool": "liblib",
            "status": "not_ready",
            "message": "ControlNet 功能需要 Liblib 脚本支持",
            "control_type": control_type,
            "control_type_name": control_types[control_type]
        }
    
    def inpaint(self, image_path: str, mask_path: str, prompt: str, **kwargs) -> Dict:
        """
        局部重绘
        
        Args:
            image_path: 原图路径
            mask_path: 蒙版图路径
            prompt: 重绘区域提示词
            **kwargs: 其他参数
            
        Returns:
            重绘结果
        """
        return self.controlnet(image_path, prompt, control_type="inpaint", mask_path=mask_path, **kwargs)
    
    def get_capabilities(self) -> Dict:
        """获取工具能力说明"""
        return {
            "name": "LiblibAI",
            "url": "https://www.liblib.art/",
            "strengths": ["产品精修", "ControlNet 控制", "多模型选择", "细节调整"],
            "weaknesses": ["创意发散", "海报设计"],
            "supported_features": [
                "文生图",
                "图生图",
                "ControlNet (多种类型)",
                "局部重绘",
                "模型选择",
                "参数精细调整"
            ],
            "controlnet_types": [
                "canny (边缘检测)",
                "depth (深度图)",
                "pose (人体姿态)",
                "openpose (OpenPose)",
                "tile (细节增强)",
                "inpaint (局部重绘)"
            ]
        }


# 使用示例
if __name__ == "__main__":
    tool = LiblibTool()
    
    # 测试生成
    result = tool.generate(
        prompt="女士连衣裙，白色雪纺材质，风格简约优雅，背景干净",
        negative_prompt="模糊，变形，低质量",
        quantity=2,
        product_type="服装"
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
