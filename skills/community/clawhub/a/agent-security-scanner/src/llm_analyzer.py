#!/usr/bin/env python3
"""
LLM 二次判定模块 - 用于边界样本的深度分析

触发条件:
- 风险分数 15-35 (边界区域)
- 意图分析结果不确定
- 包含可疑但常见代码模式

使用场景:
- 白名单样本但有可疑行为
- 规则匹配但意图不明
- 用户要求深度分析
"""

import os
import json
from typing import Optional, Dict

class LLMAnalyzer:
    """LLM 深度分析器"""
    
    def __init__(self):
        self.enabled = os.getenv('ENABLE_LLM_ANALYSIS', 'false').lower() == 'true'
        self.api_key = os.getenv('LLM_API_KEY', '')
        self.api_url = os.getenv('LLM_API_URL', '')
    
    def analyze(self, code: str, context: Dict) -> Optional[Dict]:
        """
        使用 LLM 分析代码意图
        
        Args:
            code: 源代码
            context: 上下文信息 (风险分数、behaviors、语言等)
        
        Returns:
            LLM 分析结果，或 None (LLM 不可用/跳过)
        """
        if not self.enabled:
            return None
        
        # 构建分析提示
        prompt = self._build_prompt(code, context)
        
        try:
            # 调用 LLM API
            # result = self._call_llm_api(prompt)
            # return self._parse_result(result)
            
            # 临时返回 (实际使用时替换为真实 API 调用)
            return {
                'is_malicious': False,
                'confidence': 0.8,
                'reason': '代码模式常见，无明显恶意意图',
                'suggestions': ['建议人工审核']
            }
        except Exception as e:
            # LLM 失败不影响主流程
            return None
    
    def _build_prompt(self, code: str, context: Dict) -> str:
        """构建 LLM 分析提示"""
        return f"""
请分析以下代码的恶意性：

【代码内容】
{code[:2000]}  # 限制长度

【上下文信息】
- 风险分数：{context.get('risk_score', 0)}
- 检测到的行为：{context.get('behaviors', [])}
- 编程语言：{context.get('language', 'unknown')}
- 文件路径：{context.get('path', '')}

【分析要求】
1. 判断代码是否有恶意意图
2. 说明判断理由
3. 给出置信度 (0-1)

【输出格式】
{{
    "is_malicious": true/false,
    "confidence": 0.0-1.0,
    "reason": "判断理由",
    "risk_level": "safe/low/medium/high/critical"
}}
"""
    
    def _call_llm_api(self, prompt: str) -> str:
        """调用 LLM API"""
        # 实现 LLM API 调用
        # 可以使用 OpenAI/Claude/本地模型等
        pass
    
    def _parse_result(self, result: str) -> Dict:
        """解析 LLM 返回结果"""
        try:
            return json.loads(result)
        except:
            return None


def should_trigger_llm(risk_score: float, behaviors: list, intent_result: Optional[Dict]) -> bool:
    """
    判断是否应该触发 LLM 分析
    
    触发条件:
    1. 风险分数在边界区域 (15-35)
    2. 包含可疑但常见行为 (subprocess, base64 等)
    3. 意图分析结果不确定
    """
    # 条件 1: 边界风险分数
    if 15 <= risk_score <= 35:
        return True
    
    # 条件 2: 可疑但常见行为
    suspicious_common = [
        'subprocess', 'base64', 'eval', 'exec',
        'urllib', 'socket', 'requests'
    ]
    for b in behaviors:
        if any(s in b.lower() for s in suspicious_common):
            return True
    
    # 条件 3: 意图不确定
    if intent_result and intent_result.get('intent') == 'unclear':
        return True
    
    return False


# 使用示例
if __name__ == '__main__':
    analyzer = LLMAnalyzer()
    
    # 示例代码
    code = """
import subprocess
import base64

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return base64.b64encode(result.stdout).decode()
"""
    
    context = {
        'risk_score': 25,
        'behaviors': ['high:subprocess.run(', 'py:base64_decode'],
        'language': 'python',
        'path': 'test.py'
    }
    
    if should_trigger_llm(context['risk_score'], context['behaviors'], None):
        result = analyzer.analyze(code, context)
        print(f"LLM 分析结果：{result}")
    else:
        print("不需要 LLM 分析")
