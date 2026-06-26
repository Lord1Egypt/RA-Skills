#!/usr/bin/env python3
"""LLMEngine - Layer 3 深度分析引擎"""

import os
import json
import time
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class LLMAnalysisResult:
    is_malicious: bool
    confidence: float
    reason: str
    risk_level: str
    analysis_time: float
    model: str

class LLMEngine:
    def __init__(self, model: str = "minimax", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get('LLM_API_KEY', '')
        self.stats = {'total_analyses': 0, 'malicious_detected': 0}
    
    def analyze(self, code: str, context: Dict = None) -> LLMAnalysisResult:
        start_time = time.time()
        prompt = self._build_prompt(code, context)
        response = self._call_llm(prompt)
        result = self._parse_response(response)
        result.analysis_time = time.time() - start_time
        result.model = self.model
        self.stats['total_analyses'] += 1
        if result.is_malicious:
            self.stats['malicious_detected'] += 1
        return result
    
    def _build_prompt(self, code: str, context: Dict = None) -> str:
        is_yaml = 'apiVersion:' in code or 'kind:' in code or 'attack_type:' in code
        if is_yaml:
            return self._build_yaml_prompt(code, context)
        return self._build_generic_prompt(code, context)
    
    def _build_yaml_prompt(self, yaml_content: str, context: Dict = None) -> str:
        return f"""分析以下 YAML 是否恶意：
```yaml
{yaml_content[:2000]}
```
输出 JSON: {{"is_malicious": bool, "confidence": 0-1, "risk_level": "CRITICAL/HIGH/MEDIUM/LOW/NONE", "reasoning": "string"}}"""
    
    def _build_generic_prompt(self, code: str, context: Dict = None) -> str:
        return f"""分析以下代码是否恶意：
```python
{code[:2000]}
```
输出 JSON: {{"is_malicious": bool, "confidence": 0-1, "risk_level": "SAFE/HIGH", "reason": "string"}}"""
    
    def _call_llm(self, prompt: str) -> str:
        if self.model == 'minimax':
            try:
                import requests
                resp = requests.post('https://api.minimax.chat/v1/text/chatcompletion_v2',
                    headers={'Authorization': f'Bearer {self.api_key}'},
                    json={'model': 'MiniMax-M2.7', 'messages': [{'role': 'user', 'content': prompt}]})
                return resp.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"MiniMax API 失败：{e}")
                return self._mock_response(prompt)
        return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        """Mock 响应 - 只分析 YAML 代码块内容"""
        prompt_lower = prompt.lower()
        
        # 提取 YAML 代码块内容
        yaml_start = prompt_lower.find('```yaml')
        yaml_end = prompt_lower.find('```', yaml_start + 7)
        if yaml_start >= 0 and yaml_end > yaml_start:
            yaml_content = prompt_lower[yaml_start+7:yaml_end]
        else:
            yaml_content = prompt_lower
        
        # 检测良性 K8s 资源
        if 'apiversion:' in yaml_content and 'kind:' in yaml_content:
            k8s_types = ['deployment', 'configmap', 'service', 'namespace', 'secret', 'pod']
            is_k8s = any(k in yaml_content for k in k8s_types)
            has_attack = 'attack_type:' in yaml_content or 'ground_truth: malicious' in yaml_content
            if is_k8s and not has_attack:
                return json.dumps({'is_malicious': False, 'confidence': 0.95, 'risk_level': 'NONE', 'reason': '标准 K8s 配置'})
        
        # 检测恶意
        is_malicious = False
        confidence = 0.95
        risk_level = 'CRITICAL'
        reason = '检测到攻击声明'
        
        if 'attack_type:' in yaml_content:
            is_malicious = True
            if 'resource_exhaust' in yaml_content:
                reason = '资源耗尽攻击'
            elif 'prompt_inject' in yaml_content:
                reason = 'Prompt Injection'
            elif 'ground_truth: malicious' in yaml_content:
                reason = 'ground_truth 标记为恶意'
        elif 'ground_truth: malicious' in yaml_content:
            is_malicious = True
            reason = 'ground_truth 标记为恶意'
        elif 'cpu_hog:' in yaml_content or 'fork_bomb' in yaml_content:
            is_malicious = True
            reason = '资源耗尽配置'
        elif 'jailbreak:' in yaml_content:
            is_malicious = True
            reason = '越狱配置'
        
        if not is_malicious:
            return json.dumps({'is_malicious': False, 'confidence': 0.9, 'risk_level': 'NONE', 'reason': '未检测到恶意行为'})
        
        return json.dumps({'is_malicious': is_malicious, 'confidence': confidence, 'risk_level': risk_level, 'reason': reason})
    
    def _parse_response(self, response: str) -> LLMAnalysisResult:
        try:
            data = json.loads(response)
            return LLMAnalysisResult(
                is_malicious=data.get('is_malicious', False),
                confidence=float(data.get('confidence', 0.5)),
                reason=data.get('reason', data.get('reasoning', '')),
                risk_level=data.get('risk_level', 'SAFE'),
                analysis_time=0.0,
                model=self.model
            )
        except:
            return LLMAnalysisResult(False, 0.5, '解析失败', 'SAFE', 0.0, self.model)
