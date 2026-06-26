# 🎭 执行师 (Maker) - 图片生成执行

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
        self.tools_config = self._load_tools_config()
        self.generated_params = []  # 记录生成参数
    
    def _load_tools_config(self) -> Dict:
        """加载工具配置"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '../config/tools_config.json')
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
            "future_tools": []
        }
    
    def generate(self, brief: Dict) -> Dict:
        """
        根据创意简报生成图片
        
        Args:
            brief: 策划师生成的创意简报
            
        Returns:
            生成结果（图片路径 + 参数记录）
        """
        if brief.get("type") != "brief":
            return {"error": "无效的创意简报"}
        
        # 获取工具选择
        tool_id = brief["creative_brief"]["recommended_tool"]
        
        # 检查工具是否可用
        if not self._is_tool_enabled(tool_id):
            # 尝试切换到备用工具
            tool_id = self._get_fallback_tool()
            if not tool_id:
                return {"error": "没有可用的生成工具"}
        
        # 获取生成参数
        prompt = brief["creative_brief"]["prompt"]
        negative_prompt = brief["creative_brief"]["negative_prompt"]
        quantity = brief["creative_brief"]["quantity"]
        
        # 调用工具生成
        result = self._call_tool(tool_id, prompt, negative_prompt, quantity, brief)
        
        return result
    
    def _is_tool_enabled(self, tool_id: str) -> bool:
        """检查工具是否启用"""
        for tool in self.tools_config.get("image_tools", []):
            if tool["id"] == tool_id:
                return tool.get("enabled", False)
        return False
    
    def _get_fallback_tool(self) -> Optional[str]:
        """获取备用工具"""
        for tool in self.tools_config.get("image_tools", []):
            if tool.get("enabled", False):
                return tool["id"]
        return None
    
    def _call_tool(self, tool_id: str, prompt: str, negative_prompt: str, 
                   quantity: int, brief: Dict) -> Dict:
        """
        调用具体工具生成图片
        
        实际实现需要调用即梦或 Liblib 的 API/脚本
        这里是框架实现
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if tool_id == "jimeng":
            result = self._call_jimeng(prompt, negative_prompt, quantity, brief, timestamp)
        elif tool_id == "liblib":
            result = self._call_liblib(prompt, negative_prompt, quantity, brief, timestamp)
        else:
            result = {"error": f"未知工具：{tool_id}"}
        
        # 记录生成参数
        if "images" in result:
            self._record_params(tool_id, prompt, negative_prompt, quantity, result)
        
        return result
    
    def _call_jimeng(self, prompt: str, negative_prompt: str, 
                     quantity: int, brief: Dict, timestamp: str) -> Dict:
        """
        调用即梦生成图片
        
        实际实现：
        1. 调用 skills/jimeng/scripts/jimeng_auto.py
        2. 或使用即梦 API
        """
        # TODO: 实际调用即梦脚本
        # 这里是模拟返回
        output_dir = f"output/jimeng/{timestamp}"
        
        return {
            "tool": "jimeng",
            "tool_name": "即梦",
            "status": "success",
            "images": [
                {
                    "path": f"{output_dir}/image_1.png",
                    "thumbnail": f"{output_dir}/thumb_1.png"
                }
                # 实际会根据 quantity 生成多张
            ],
            "message": f"已使用即梦生成 {quantity} 张图片",
            "note": "即梦擅长海报和创意图，生成结果具有较强视觉冲击力"
        }
    
    def _call_liblib(self, prompt: str, negative_prompt: str, 
                     quantity: int, brief: Dict, timestamp: str) -> Dict:
        """
        调用 LiblibAI 生成图片
        
        实际实现：
        1. 调用 skills/liblib/scripts/liblib_auto.py
        2. 或使用 Liblib API
        """
        # TODO: 实际调用 Liblib 脚本
        # 这里是模拟返回
        output_dir = f"output/liblib/{timestamp}"
        
        # 根据产品类型推荐模型
        product_type = brief.get("product_info", {}).get("type", "")
        recommended_model = self._recommend_liblib_model(product_type)
        
        return {
            "tool": "liblib",
            "tool_name": "LiblibAI",
            "status": "success",
            "images": [
                {
                    "path": f"{output_dir}/image_1.png",
                    "thumbnail": f"{output_dir}/thumb_1.png"
                }
            ],
            "model_used": recommended_model,
            "message": f"已使用 LiblibAI 生成 {quantity} 张图片",
            "note": f"使用 {recommended_model} 模型，适合{product_type}类产品精修"
        }
    
    def _recommend_liblib_model(self, product_type: str) -> str:
        """根据产品类型推荐 Liblib 模型"""
        model_map = {
            "服装": "服装展示专用模型",
            "食品": "美食摄影模型",
            "数码": "产品精修模型",
            "美妆": "美妆商业摄影模型",
            "家居": "室内场景模型"
        }
        return model_map.get(product_type, "通用商业摄影模型")
    
    def _record_params(self, tool_id: str, prompt: str, negative_prompt: str, 
                       quantity: int, result: Dict):
        """记录生成参数，便于复现和迭代"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_id,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "quantity": quantity,
            "output_paths": [img["path"] for img in result.get("images", [])],
            "model_used": result.get("model_used", "default")
        }
        
        self.generated_params.append(record)
        
        # 保存到文件
        self._save_params_history(record)
    
    def _save_params_history(self, record: Dict):
        """保存参数历史到文件"""
        history_path = os.path.join(os.path.dirname(__file__), '../memory/generation_history.json')
        
        try:
            os.makedirs(os.path.dirname(history_path), exist_ok=True)
            
            # 读取现有历史
            if os.path.exists(history_path):
                with open(history_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            # 添加新记录
            history.append(record)
            
            # 保留最近 100 条
            history = history[-100:]
            
            # 保存
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存参数历史失败：{e}")
    
    def regenerate(self, original_params: Dict, adjustments: str) -> Dict:
        """
        根据调整建议重新生成
        
        Args:
            original_params: 原始生成参数
            adjustments: 调整建议（来自质检师）
            
        Returns:
            重新生成的结果
        """
        # 基于原始参数，应用调整
        new_prompt = self._apply_adjustments(
            original_params.get("prompt", ""), 
            adjustments
        )
        
        # 重新调用工具
        return self._call_tool(
            original_params.get("tool", "jimeng"),
            new_prompt,
            original_params.get("negative_prompt", ""),
            original_params.get("quantity", 2),
            {"product_info": {}}
        )
    
    def _apply_adjustments(self, original_prompt: str, adjustments: str) -> str:
        """应用调整建议到 Prompt"""
        # 简单实现：将调整建议添加到原 Prompt
        return f"{original_prompt}，{adjustments}"


# 使用示例
if __name__ == "__main__":
    maker = MakerAgent()
    
    # 模拟创意简报
    test_brief = {
        "type": "brief",
        "product_info": {
            "type": "服装",
            "name": "女士连衣裙"
        },
        "creative_brief": {
            "prompt": "女士连衣裙，白色雪纺材质，风格简约优雅",
            "negative_prompt": "模糊，变形，低质量",
            "recommended_tool": "liblib",
            "quantity": 2
        }
    }
    
    result = maker.generate(test_brief)
    print(json.dumps(result, ensure_ascii=False, indent=2))
