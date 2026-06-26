#!/usr/bin/env python3
"""
智能路由系统核心
根据问题复杂度自动选择模型，集成成本优化
"""

import re
import json
from typing import Dict, Any, Optional

# 尝试导入requests，如果失败则使用备用方案
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[警告] requests库未安装，将使用纯关键词匹配模式")

# 导入模型管理器
try:
    from model_manager import model_manager
    MODEL_MANAGER_AVAILABLE = True
except ImportError:
    MODEL_MANAGER_AVAILABLE = False
    print("[警告] 模型管理器不可用，将使用默认模型选择")

class SmartRouter:
    def __init__(self, ollama_host: str = "http://192.168.10.14:11434"):
        self.ollama_host = ollama_host
        self.judge_model = "deepseek-r1:1.5b"
        
        # 初始化模型管理器
        if MODEL_MANAGER_AVAILABLE:
            # 自动检测并更新模型配置
            model_manager.update_config_from_detection()
            print("[智能路由] 模型管理器已初始化")
        else:
            print("[智能路由] 警告: 使用默认模型配置")
        
        # 缓存判断结果，提高性能
        self.cache = {}
        
        # 预定义简单请求模式（快速判断）
        self.simple_patterns = [
            r'^(hi|hello|hey|你好|嗨)',
            r'^(what.*time|几点了|现在几点|时间)',
            r'^(weather|天气)',
            r'^(remind|提醒)',
            r'^(note|笔记)',
            r'^(list|列出|显示|查看)',
            r'^(search|搜索|查找)',
            r'^(file|文件)',
            r'^(read|读取|打开)',
            r'^(copy|复制)',
            r'^(move|移动)',
            r'^(delete|删除)',
            r'^(rename|重命名)',
            r'^[0-9\+\-\*\/\s]+[=?]$',  # 简单数学计算
            r'^(yes|no|ok|好的|不行|可以)',
            r'^.{1,50}$',  # 非常短的请求
            r'(status|状态|检查)',
            r'(pwd|ls|cd|cat|echo)',
            r'(简单|基础|快速)',
        ]
        
        # 预定义复杂请求模式
        self.complex_patterns = [
            r'(explain|解释)',
            r'(analyze|分析|解析)',
            r'(compare|比较|对比)',
            r'(write|编写|创作).*(code|代码|程序|文章)',
            r'(debug|调试|排错)',
            r'(design|设计|规划)',
            r'(philosophy|哲学|思考)',
            r'(creative|创意|创作)',
            r'(long|长篇|详细)',
            r'(summary|总结|概括)',
            r'(translate|翻译).{20,}',  # 长文本翻译
            r'(how to|如何|怎样).*(step|步骤|流程)',
            r'(复杂|困难|难题)',
            r'(架构|系统|框架)',
            r'(算法|数据结构)',
            r'(机器学习|人工智能|AI)',
            r'(项目|工程|开发)',
            r'(代码|编程|开发)',  # 添加代码相关关键词
            r'(原理|理论|机制)',  # 添加原理相关关键词
        ]
    
    def quick_check(self, prompt: str) -> Optional[str]:
        """快速检查，使用预定义模式"""
        prompt_lower = prompt.lower().strip()
        
        # 检查缓存
        cache_key = f"quick_{hash(prompt_lower)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 先检查是否明确复杂（优先级更高）
        for pattern in self.complex_patterns:
            if re.search(pattern, prompt_lower, re.IGNORECASE):
                self.cache[cache_key] = "complex"
                return "complex"
        
        # 再检查是否明确简单
        for pattern in self.simple_patterns:
            if re.match(pattern, prompt_lower, re.IGNORECASE):
                self.cache[cache_key] = "simple"
                return "simple"
        
        # 无法快速判断，需要小模型判断
        return None
    
    def judge_with_model(self, prompt: str) -> str:
        """使用小模型判断复杂度"""
        if not REQUESTS_AVAILABLE:
            # 如果没有requests库，使用扩展的关键词匹配
            return self._fallback_judge(prompt)
        
        try:
            cache_key = f"model_{hash(prompt)}"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.judge_model,
                    "prompt": f"""请判断以下用户请求是简单请求还是复杂请求：

用户请求：{prompt}

简单请求通常包括：问候、简单查询、文件操作、提醒设置、简短回答等。
复杂请求通常包括：代码编写、复杂分析、创意写作、详细解释、逻辑推理等。

请只回答一个字："简单" 或 "复杂"，不要其他任何内容。""",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "max_tokens": 10
                    }
                },
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()["response"].strip()
                if "复杂" in result:
                    self.cache[cache_key] = "complex"
                    return "complex"
                else:
                    self.cache[cache_key] = "simple"
                    return "simple"
        except Exception as e:
            print(f"[智能路由] 小模型判断失败: {e}")
            # 失败时使用备用方案
            return self._fallback_judge(prompt)
        
        # 默认返回简单（保守策略）
        return "simple"
    
    def _fallback_judge(self, prompt: str) -> str:
        """备用判断方案：扩展关键词匹配"""
        prompt_lower = prompt.lower()
        
        # 扩展的复杂关键词
        complex_keywords = [
            '代码', '编程', '开发', '算法', '数据结构',
            '解释', '分析', '解析', '原理', '理论',
            '设计', '架构', '系统', '框架',
            '比较', '对比', '差异',
            '如何', '怎样', '步骤', '流程',
            '机器学习', '人工智能', 'AI', '深度学习',
            '项目', '工程', '应用', '实现'
        ]
        
        # 检查是否包含复杂关键词
        for keyword in complex_keywords:
            if keyword in prompt_lower:
                return "complex"
        
        # 检查长度 - 长文本更可能是复杂请求
        if len(prompt) > 100:
            return "complex"
        
        return "simple"
    
    def route_request(self, prompt: str) -> Dict[str, Any]:
        """路由请求，返回模型选择建议（集成成本优化）"""
        # 先尝试快速检查
        quick_result = self.quick_check(prompt)
        
        if quick_result:
            complexity = quick_result
            method = "pattern"
        else:
            # 使用小模型判断
            complexity = self.judge_with_model(prompt)
            method = "model"
        
        # 根据复杂度和成本优化选择模型
        if MODEL_MANAGER_AVAILABLE:
            # 使用模型管理器进行成本优化选择
            model = model_manager.get_cost_effective_model(complexity)
            
            # 获取模型详细信息
            model_info = model_manager.models.get(model, {})
            model_name = model_info.get("name", model)
            model_type = model_info.get("type", "unknown")
            model_priority = model_info.get("model_priority", "normal")
            
            if complexity == "simple":
                reason = f"简单请求，使用{model_type}模型处理（{model_name}）"
            else:
                reason = f"复杂请求，使用{model_type}模型处理（{model_name}，优先级：{model_priority}）"
            
            cost_weight = model_info.get("cost_weight", 1.0)
            
        else:
            # 回退到默认逻辑
            if complexity == "simple":
                model = "ollama-local/deepseek-r1-7b"
                reason = "简单请求，使用本地模型处理"
                model_type = "local"
                cost_weight = 0.3
            else:
                model = "deepseek/deepseek-chat"
                reason = "复杂请求，使用云端模型处理"
                model_type = "cloud"
                cost_weight = 1.0
        
        return {
            "complexity": complexity,
            "model": model,
            "model_type": model_type,
            "cost_weight": cost_weight,
            "reason": reason,
            "method": method,
            "prompt_length": len(prompt),
            "cost_optimized": MODEL_MANAGER_AVAILABLE
        }
    
    def get_recommended_model(self, prompt: str) -> str:
        """获取推荐的模型"""
        route_info = self.route_request(prompt)
        return route_info["model"]
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """获取当前可用的模型配置"""
        if MODEL_MANAGER_AVAILABLE:
            return model_manager.models
        else:
            # 返回默认配置
            return {
                "ollama-local/deepseek-r1-7b": {
                    "enable": True,
                    "type": "local",
                    "name": "DeepSeek R1 7B (本地任务处理)",
                    "model_priority": "normal",
                    "description": "本地中等模型，适合大多数任务",
                    "cost_weight": 0.3
                },
                "deepseek/deepseek-chat": {
                    "enable": True,
                    "type": "cloud",
                    "name": "DeepSeek Chat (云端复杂任务)",
                    "model_priority": "max",
                    "description": "云端大模型，适合复杂任务",
                    "cost_weight": 1.0
                }
            }

# 单例实例
router = SmartRouter()

if __name__ == "__main__":
    # 测试函数
    test_cases = [
        "现在几点了",
        "帮我列出桌面上的文件",
        "提醒我下午3点开会",
        "请解释量子纠缠的基本原理",
        "帮我写一个Flutter的登录页面代码",
        "比较React和Vue的优缺点",
        "2+2等于多少？",
        "请详细分析Android内存泄漏的常见原因和解决方案",
    ]
    
    print("=== 智能路由测试 ===\n")
    for i, prompt in enumerate(test_cases, 1):
        print(f"测试 {i}: {prompt}")
        result = router.route_request(prompt)
        print(f"  复杂度: {result['complexity']} ({result['method']})")
        print(f"  推荐模型: {result['model']}")
        print(f"  理由: {result['reason']}")
        print()