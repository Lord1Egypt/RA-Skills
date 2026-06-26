"""
智能助手 - 提供更好的用户体验
"""

from typing import Dict, Any
from toolkit.error_handler import (
    VolcengineError,
    AuthenticationError,
    RateLimitError,
    InvalidInputError
)


class SmartHelper:
    """智能助手 - 提供友好的错误提示和建议"""
    
    @staticmethod
    def suggest_fix(error: Exception) -> Dict[str, str]:
        """
        根据错误类型提供修复建议
        
        Args:
            error: 异常对象
            
        Returns:
            修复建议字典
        """
        suggestions = {
            "issue": None,
            "cause": None,
            "solutions": []
        }
        
        if isinstance(error, AuthenticationError):
            suggestions = {
                "issue": "API Key认证失败",
                "cause": "API Key无效或未配置",
                "solutions": [
                    "检查API Key是否正确设置",
                    "确认API Key是否过期",
                    "验证账户是否有足够权限",
                    "查看服务是否已开通"
                ]
            }
        elif isinstance(error, RateLimitError):
            suggestions = {
                "issue": "请求频率超限",
                "cause": "短时间内请求过多",
                "solutions": [
                    "等待一段时间后重试",
                    "减少请求频率",
                    "检查账户配额",
                    "考虑升级套餐"
                ]
            }
        elif isinstance(error, InvalidInputError):
            suggestions = {
                "issue": "参数验证失败",
                "cause": "输入参数不符合要求",
                "solutions": [
                    "检查参数格式是否正确",
                    "确认必填参数是否提供",
                    "验证参数值是否在有效范围内",
                    "参考API文档确认参数要求"
                ]
            }
        elif isinstance(error, VolcengineError):
            suggestions = {
                "issue": "API调用失败",
                "cause": "服务端错误或网络问题",
                "solutions": [
                    "检查网络连接",
                    "确认API端点是否正确",
                    "查看服务状态",
                    "稍后重试或联系客服"
                ]
            }
        else:
            suggestions = {
                "issue": "未知错误",
                "cause": "未预期的异常",
                "solutions": [
                    "查看详细错误信息",
                    "检查代码逻辑",
                    "查看日志输出",
                    "联系技术支持"
                ]
            }
        
        return suggestions
    
    @staticmethod
    def get_quick_guide(task_type: str) -> str:
        """
        获取快速使用指南
        
        Args:
            task_type: 任务类型 (image/video/vision)
            
        Returns:
            使用指南字符串
        """
        guides = {
            "image": """
🖼️ 图像生成快速指南:
1. 准备提示词: 详细描述想要的图片内容
2. 选择尺寸: 1024x1024 (默认) 或其他尺寸
3. 调用API: 使用 /images/generations 端点
4. 获取结果: 从响应中提取图片URL

示例:
```python
result = client.post("/images/generations", json={
    "model": "doubao-seedream-4-0-250828",
    "prompt": "一只可爱的橘猫",
    "size": "1024x1024",
    "response_format": "url",
    "n": 1
})
image_url = result["data"][0]["url"]
```
""",
            "video": """
🎬 视频生成快速指南:
1. 准备提示词: 描述视频内容和动作
2. 指定参数: --duration 5 --resolution 720p
3. 创建任务: 使用 /contents/generations/tasks 端点
4. 轮询状态: 使用返回的任务ID轮询
5. 获取结果: 任务完成后下载视频

示例:
```python
# 创建任务
result = client.post("/contents/generations/tasks", json={
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
        {"type": "text", "text": "镜头缓缓移动 --duration 5"}
    ]
}
task_id = result["id"]

# 查询状态
status = client.get(f"/contents/generations/tasks/{task_id}")
if status["status"] == "succeeded":
    video_url = status["content"]["video_url"]
```
""",
            "vision": """
👁️ 视觉理解快速指南:
1. 准备图片: 图片URL或本地路径
2. 准备问题: 想要了解的内容
3. 调用API: 使用 /responses 端点
4. 解析结果: 从output中提取分析内容

示例:
```python
result = client.post("/responses", json={
    "model": "doubao-seed-1-6-vision-250815",
    "input": [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "描述这张图片"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg"}
            ]
        }
    ]
}
# 解析响应
for item in result["output"]:
    if item["type"] == "summary_text":
        print(item["text"])
```
"""
        }
        
        return guides.get(task_type, "暂不支持的任务类型")
    
    @staticmethod
    def estimate_cost(task_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        估算任务成本
        
        Args:
            task_type: 任务类型
            params: 任务参数
            
        Returns:
            成本估算
        """
        # 基于官方定价估算
        costs = {
            "image": {
                "base": 0.02,  # 每张图片基础价格
                "unit": "张"
            },
            "video": {
                "base": 0.10,  # 每秒视频基础价格
                "unit": "秒"
            },
            "vision": {
                "base": 0.001,  # 每次请求基础价格
                "unit": "次"
            }
        }
        
        if task_type in costs:
            base_cost = costs[task_type]["base"]
            
            if task_type == "image":
                count = params.get("n", 1)
                return {
                    "estimated_cost": base_cost * count,
                    "unit": f"{count} {costs[task_type]['unit']}",
                    "note": "实际费用可能因模型和复杂度而异"
                }
            elif task_type == "video":
                duration = params.get("duration", 5)
                return {
                    "estimated_cost": base_cost * duration,
                    "unit": f"{duration} {costs[task_type]['unit']}",
                    "note": "视频生成是异步的，可能需要额外时间"
                }
            elif task_type == "vision":
                return {
                    "estimated_cost": base_cost,
                    "unit": costs[task_type]["unit"],
                    "note": "复杂分析可能产生额外费用"
                }
        
        return {
            "estimated_cost": 0,
            "unit": "未知",
            "note": "无法估算此任务类型的成本"
        }
