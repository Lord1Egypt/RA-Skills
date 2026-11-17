#!/usr/bin/env python3
"""
API Balance Checker
查询 API 余额和使用情况
"""

import requests
from typing import Dict, Optional
from datetime import datetime

class BalanceChecker:
    def __init__(self):
        """初始化余额查询器"""
        pass
    
    def check_openai(self, api_key: str, base_url: str = "https://api.openai.com") -> Dict:
        """查询 OpenAI 余额"""
        try:
            # 查询订阅信息
            response = requests.get(
                f"{base_url}/v1/dashboard/billing/subscription",
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'provider': 'openai',
                    'status': 'success',
                    'balance': data.get('hard_limit_usd', 'N/A'),
                    'used': data.get('soft_limit_usd', 'N/A'),
                    'plan': data.get('plan', {}).get('title', 'Unknown'),
                    'raw': data
                }
            else:
                return {
                    'provider': 'openai',
                    'status': 'error',
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
        
        except Exception as e:
            return {
                'provider': 'openai',
                'status': 'error',
                'error': str(e)
            }
    
    def check_anthropic(self, api_key: str, base_url: str = "https://api.anthropic.com") -> Dict:
        """查询 Anthropic 余额"""
        try:
            # 查询使用情况
            response = requests.get(
                f"{base_url}/v1/organization/usage",
                headers={'x-api-key': api_key},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'provider': 'anthropic',
                    'status': 'success',
                    'balance': data.get('balance', 'N/A'),
                    'used': data.get('usage', 'N/A'),
                    'raw': data
                }
            else:
                return {
                    'provider': 'anthropic',
                    'status': 'error',
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
        
        except Exception as e:
            return {
                'provider': 'anthropic',
                'status': 'error',
                'error': str(e)
            }
    
    def check_balance(self, provider: str, api_key: str, base_url: str, protocol: str) -> Dict:
        """根据协议类型查询余额"""
        if protocol == 'anthropic-messages':
            return self.check_anthropic(api_key, base_url)
        
        elif protocol in ['openai-chat', 'openai-compatible', 'openai-completions']:
            return self.check_openai(api_key, base_url)
        
        else:
            return {
                'provider': provider,
                'status': 'unsupported',
                'error': f'Balance check not supported for protocol: {protocol}'
            }
    
    def format_balance_result(self, result: Dict) -> str:
        """格式化余额查询结果"""
        if result['status'] == 'success':
            output = f"**{result['provider']}**\n"
            output += f"余额: ${result['balance']}\n"
            output += f"已用: ${result['used']}\n"
            
            if 'plan' in result:
                output += f"计划: {result['plan']}\n"
            
            # 余额警告
            try:
                balance = float(result['balance'])
                if balance < 5:
                    output += "⚠️ 余额不足 $5\n"
                elif balance < 10:
                    output += "⚠️ 余额较低\n"
            except:
                pass
            
            return output
        
        elif result['status'] == 'error':
            return f"**{result['provider']}**: ❌ {result['error']}\n"
        
        elif result['status'] == 'unsupported':
            return f"**{result['provider']}**: ⚠️ {result['error']}\n"
        
        else:
            return f"**{result['provider']}**: Unknown status\n"

def main():
    """测试"""
    checker = BalanceChecker()
    
    # 测试 OpenAI（需要真实 API Key）
    # result = checker.check_openai('sk-xxx')
    # print(checker.format_balance_result(result))
    
    print("Balance checker initialized")

if __name__ == '__main__':
    main()
