#!/usr/bin/env python3
"""
AI Complexity Predictor - 任务复杂度预测
使用免费模型（Qwen 0.5B）预测任务复杂度，替代关键词匹配
"""

import requests
import json
from typing import Literal

ComplexityLevel = Literal["free", "medium", "expensive"]

class AIComplexityPredictor:
    def __init__(self, openrouter_key: str = None):
        """初始化预测器
        
        Args:
            openrouter_key: OpenRouter API key（可选，从环境变量读取）
        """
        import os
        self.api_key = openrouter_key or os.getenv('OPENROUTER_API_KEY', '')
        self.api_base = "https://openrouter.ai/api/v1"
        
        # 免费模型
        self.free_model = "qwen/qwen-2.5-0.5b-instruct"
    
    def predict_complexity(self, task: str) -> ComplexityLevel:
        """预测任务复杂度
        
        Args:
            task: 任务描述
        
        Returns:
            "free" | "medium" | "expensive"
        """
        if not self.api_key:
            # Fallback to keyword matching
            return self._fallback_predict(task)
        
        try:
            # 构建 prompt
            prompt = f"""Analyze this task and rate its complexity from 1-10:

Task: {task}

Consider:
- Simple tasks (1-3): search, weather, translate, time, basic info
- Medium tasks (4-7): code review, summarize, data analysis
- Complex tasks (8-10): architecture design, debug, creative writing

Reply with ONLY a number 1-10:"""

            # 调用 Qwen 0.5B（免费）
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.free_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 10,
                    "temperature": 0.1
                },
                timeout=5
            )
            
            if response.status_code != 200:
                return self._fallback_predict(task)
            
            # 解析结果
            result = response.json()
            score_text = result['choices'][0]['message']['content'].strip()
            
            # 提取数字
            score = int(''.join(c for c in score_text if c.isdigit())[:2])
            
            # 映射到复杂度级别
            if score <= 3:
                return "free"
            elif score <= 7:
                return "medium"
            else:
                return "expensive"
        
        except Exception as e:
            print(f"AI prediction failed: {e}, falling back to keywords")
            return self._fallback_predict(task)
    
    def _fallback_predict(self, task: str) -> ComplexityLevel:
        """关键词匹配（备用方案）"""
        task_lower = task.lower()
        
        # 简单任务关键词
        simple_signals = [
            "search", "weather", "translate", "time", "date", 
            "check", "list", "find", "show", "get"
        ]
        
        # 复杂任务关键词
        complex_signals = [
            "analyze", "write code", "debug", "architect", 
            "design", "implement", "refactor", "optimize"
        ]
        
        if any(s in task_lower for s in simple_signals):
            return "free"
        if any(c in task_lower for c in complex_signals):
            return "expensive"
        
        return "medium"
    
    def predict_with_confidence(self, task: str) -> tuple[ComplexityLevel, float]:
        """预测任务复杂度（带置信度）
        
        Returns:
            (complexity, confidence)
        """
        if not self.api_key:
            return self._fallback_predict(task), 0.5
        
        try:
            # 多次预测取平均
            scores = []
            for _ in range(3):
                complexity = self.predict_complexity(task)
                score_map = {"free": 2, "medium": 5, "expensive": 9}
                scores.append(score_map[complexity])
            
            # 计算平均和标准差
            import statistics
            mean_score = statistics.mean(scores)
            std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
            
            # 置信度：标准差越小，置信度越高
            confidence = max(0.5, 1.0 - std_dev / 5)
            
            # 映射回复杂度
            if mean_score <= 3:
                return "free", confidence
            elif mean_score <= 7:
                return "medium", confidence
            else:
                return "expensive", confidence
        
        except:
            return self._fallback_predict(task), 0.5


def main():
    """CLI 测试"""
    import sys
    
    if len(sys.argv) < 2:
        print("\nUsage: python3 ai_complexity_predictor.py <task>")
        print("\nExamples:")
        print("  python3 ai_complexity_predictor.py 'search weather in Tokyo'")
        print("  python3 ai_complexity_predictor.py 'design a distributed system'")
        return
    
    task = ' '.join(sys.argv[1:])
    predictor = AIComplexityPredictor()
    
    print(f"\nTask: {task}")
    
    # 简单预测
    complexity = predictor.predict_complexity(task)
    print(f"Complexity: {complexity}")
    
    # 带置信度的预测
    complexity, confidence = predictor.predict_with_confidence(task)
    print(f"Complexity (with confidence): {complexity} ({confidence:.2%})")


if __name__ == '__main__':
    main()
