# 🎭 AI 执行师 Agent

"""
执行师职责：
1. 接收策划师的创意简报
2. 调用 AI 工具生成图片（即梦/LiblibAI）
3. 参数调优与多方案生成
4. 记录生成参数（便于复现/迭代）

输出：1-4 张初稿图片 + 生成参数记录
"""

from typing import Dict, List, Optional
import json
import os
from datetime import datetime


class MakerAgent:
    """执行师 Agent"""
    
    def __init__(self):
        self.name = "🎭 执行师"
        self.config = self._load_config()
        self.tools = self._init_tools()
    
    def _load_config(self) -> Dict:
        """加载工具配置"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config/tools_config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认工具配置"""
        return {
            "image_tools": [
                {"id": "jimeng", "name": "即梦", "enabled": True, "strengths": ["海报", "创意图"]},
                {"id": "liblib", "name": "LiblibAI", "enabled": True, "strengths": ["产品精修", "ControlNet"]}
            ],
            "video_tools": [
                {"id": "jimeng_video", "name": "即梦视频", "enabled": False},
                {"id": "kling", "name": "可灵", "enabled": False}
            ],
            "fallback_strategy": {"enabled": True, "order": ["jimeng", "liblib"]}
        }
    
    def _init_tools(self) -> Dict:
        """初始化工具"""
        return {
            "jimeng": self._call_jimeng,
            "liblib": self._call_liblib
        }
    
    def generate(self, brief: Dict) -> Dict:
        """
        根据创意简报生成图片
        
        Args:
            brief: 策划师生成的创意简报
            
        Returns:
            生成结果
        """
        if brief.get("type") != "brief":
            return {"error": "无效的创意简报", "agent": "maker"}
        
        tool_id = brief["creative_brief"]["recommended_tool"]
        if not self._is_tool_enabled(tool_id):
            tool_id = self._get_fallback_tool()
            if not tool_id:
                return {"error": "没有可用的生成工具", "agent": "maker"}
        
        prompt = brief["creative_brief"]["prompt"]
        negative_prompt = brief["creative_brief"]["negative_prompt"]
        quantity = brief["creative_brief"]["quantity"]
        
        result = self._call_tool(tool_id, prompt, negative_prompt, quantity, brief)
        
        if result.get("status") == "success":
            self._record_generation(result, brief)
        
        return result
    
    def _is_tool_enabled(self, tool_id: str) -> bool:
        """检查工具是否启用"""
        for tool in self.config.get("image_tools", []):
            if tool["id"] == tool_id:
                return tool.get("enabled", False)
        return False
    
    def _get_fallback_tool(self) -> Optional[str]:
        """获取备用工具"""
        fallback = self.config.get("fallback_strategy", {})
        if fallback.get("enabled"):
            for tool_id in fallback.get("order", ["jimeng", "liblib"]):
                if self._is_tool_enabled(tool_id):
                    return tool_id
        return None
    
    def _call_tool(self, tool_id: str, prompt: str, negative_prompt: str, 
                   quantity: int, brief: Dict) -> Dict:
        """调用具体工具"""
        if tool_id in self.tools:
            return self.tools[tool_id](prompt, negative_prompt, quantity, brief)
        return {"error": f"未知工具：{tool_id}", "agent": "maker"}
    
    def _call_jimeng(self, prompt: str, negative_prompt: str, 
                     quantity: int, brief: Dict) -> Dict:
        """调用即梦生成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"output/jimeng/{timestamp}"
        
        # TODO: 实际调用即梦脚本
        images = []
        for i in range(quantity):
            images.append({
                "path": f"{output_dir}/image_{i+1}.png",
                "thumbnail": f"{output_dir}/thumb_{i+1}.png"
            })
        
        return {
            "agent": "maker",
            "tool": "jimeng",
            "tool_name": "即梦",
            "status": "success",
            "images": images,
            "message": f"已使用即梦生成 {quantity} 张图片",
            "note": "即梦擅长海报和创意图，生成结果具有较强视觉冲击力"
        }
    
    def _call_liblib(self, prompt: str, negative_prompt: str, 
                     quantity: int, brief: Dict) -> Dict:
        """调用 Liblib 生成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"output/liblib/{timestamp}"
        
        product_type = brief.get("product_info", {}).get("type", "")
        model = self._recommend_liblib_model(product_type)
        
        # TODO: 实际调用 Liblib 脚本
        images = []
        for i in range(quantity):
            images.append({
                "path": f"{output_dir}/image_{i+1}.png",
                "thumbnail": f"{output_dir}/thumb_{i+1}.png"
            })
        
        return {
            "agent": "maker",
            "tool": "liblib",
            "tool_name": "LiblibAI",
            "status": "success",
            "images": images,
            "model_used": model,
            "message": f"已使用 LiblibAI 生成 {quantity} 张图片",
            "note": f"使用 {model} 模型，适合{product_type}类产品精修"
        }
    
    def _recommend_liblib_model(self, product_type: str) -> str:
        """推荐 Liblib 模型"""
        model_map = {
            "服装": "服装展示专用模型",
            "食品": "美食摄影模型",
            "数码": "产品精修模型",
            "美妆": "美妆商业摄影模型",
            "家居": "室内场景模型"
        }
        return model_map.get(product_type, "通用商业摄影模型")
    
    def _record_generation(self, result: Dict, brief: Dict):
        """记录生成历史"""
        history_path = os.path.join(os.path.dirname(__file__), 'memory/generation_history.md')
        
        try:
            os.makedirs(os.path.dirname(history_path), exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tool = result.get("tool_name", "unknown")
            product_type = brief.get("product_info", {}).get("type", "unknown")
            
            with open(history_path, 'a', encoding='utf-8') as f:
                f.write(f"\n## [{timestamp}] {product_type} - {tool}\n")
                f.write(f"- 工具：{tool}\n")
                f.write(f"- Prompt: {brief.get('creative_brief', {}).get('prompt', 'N/A')[:50]}...\n")
                f.write(f"- 数量：{len(result.get('images', []))}\n")
                f.write(f"- 输出：{result.get('images', [{}])[0].get('path', 'N/A')}\n")
                f.write("---\n")
        except Exception as e:
            print(f"记录生成历史失败：{e}")
    
    def regenerate(self, original_params: Dict, adjustments: str) -> Dict:
        """根据调整建议重新生成"""
        new_prompt = f"{original_params.get('prompt', '')}，{adjustments}"
        
        return self._call_tool(
            original_params.get("tool", "jimeng"),
            new_prompt,
            original_params.get("negative_prompt", ""),
            original_params.get("quantity", 2),
            {"product_info": {}}
        )


# 快捷函数
def generate_image(brief: Dict) -> Dict:
    """快捷生成图片"""
    agent = MakerAgent()
    return agent.generate(brief)


if __name__ == "__main__":
    test_brief = {
        "type": "brief",
        "product_info": {"type": "服装", "name": "女士连衣裙"},
        "creative_brief": {
            "prompt": "女士连衣裙，白色雪纺材质，风格简约优雅",
            "negative_prompt": "模糊，变形，低质量",
            "recommended_tool": "liblib",
            "quantity": 2
        }
    }
    result = generate_image(test_brief)
    print(json.dumps(result, ensure_ascii=False, indent=2))
