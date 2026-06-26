#!/usr/bin/env python3
"""
DMP洞察API集成脚本 - v3.0 (MD5签名 + 4位随机数)

支持与明日DMP平台的API集成：
- 使用AK/SK生成MD5签名（正确的鉴权方式）
- 查询洞察任务状态
- 获取洞察任务结果
- 处理特征数据

【重要更新】
- 鉴权方式：SHA1 → MD5（hash(ts + randStr + SK).upper()）
- 随机数：32位字母数字 → 4位纯数字
- API域名：https://open.mingdata.com/api/open-api（兼容性最优）
"""

import os
import json
import requests
import hashlib
import random
import time
from typing import Dict, List, Any, Optional
from enum import Enum


class InsightStatus(Enum):
    """洞察任务状态枚举"""
    FAILED = 0      # 失败
    SUCCESS = 1     # 成功
    WAITING = 2     # 等待中
    COMPUTING = 3   # 计算中


class InsightAPI:
    """DMP洞察API客户端 - 支持正确的MD5签名认证"""
    
    def __init__(self, ak: Optional[str] = None, sk: Optional[str] = None):
        """初始化API客户端
        
        Args:
            ak: 明日DMP Access Key
            sk: 明日DMP Secret Key
            
        Example:
            >>> api = InsightAPI(ak='your_access_key', sk='your_secret_key')
            >>> result = api.get_insight_result(task_id)
        """
        # 优先使用 AK/SK，其次使用环境变量
        self.ak = ak or os.environ.get('DMP_AK')
        self.sk = sk or os.environ.get('DMP_SK')
        
        # 正确的API基础URL
        self.base_url = "https://open.mingdata.com/api/open-api"
        
        # 禁用SSL警告（开发/测试环境）
        self.verify_ssl = False
        
        if not self.ak or not self.sk:
            print("⚠️  警告：未检测到凭证")
            print("   需要配置以下任一方式：")
            print("   1. 传入 ak 和 sk 参数")
            print("   2. 设置环境变量 DMP_AK 和 DMP_SK")
    
    def _generate_sign(self, ts: str, rand_str: str) -> str:
        """生成MD5签名（正确的鉴权方式）
        
        Args:
            ts: 时间戳（10位秒级）
            rand_str: 4位随机数
            
        Returns:
            MD5签名（大写）
            
        Algorithm:
            sign = MD5(ts + randStr + SK).upper()
        """
        sign_str = f'{ts}{rand_str}{self.sk}'
        return hashlib.md5(sign_str.encode()).hexdigest().upper()
    
    def _generate_rand_str(self) -> str:
        """生成4位随机数字（正确的方式）
        
        Returns:
            4位纯数字随机字符串 (1000-9999)
        """
        return str(random.randint(1000, 9999))
    
    def _build_auth_params(self) -> Dict:
        """构建认证参数（MD5签名方式）
        
        Returns:
            包含认证信息的参数字典
            
        Format:
            {
                'ts': '1774580142',           # 10位秒级时间戳
                'randStr': '8165',            # 4位数字
                'accessKey': 'your_access_key',     # AK
                'sign': 'MD5_HASH_UPPERCASE'  # MD5签名（大写）
            }
        """
        ts = str(int(time.time()))        # 10位秒级时间戳
        rand_str = self._generate_rand_str()  # 4位随机数
        
        # 根据MD5(ts + randStr + SK)生成签名
        sign = self._generate_sign(ts, rand_str)
        
        return {
            'ts': ts,
            'randStr': rand_str,
            'accessKey': self.ak,
            'sign': sign
        }
    
    def query_insight_status(self, task_ids: List[int]) -> List[Dict[str, Any]]:
        """查询洞察任务状态
        
        Args:
            task_ids: 任务ID列表
            
        Returns:
            任务状态信息列表
        """
        if not self.ak or not self.sk:
            print("❌ 错误：未配置 DMP_AK/DMP_SK")
            return []
        
        print(f"📊 查询任务状态...")
        print(f"   任务ID: {task_ids}")
        print(f"   API: /audience/insight/list")
        
        url = f"{self.base_url}/audience/insight/list"
        auth_params = self._build_auth_params()
        
        payload = {
            'taskIds': task_ids
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                params=auth_params,
                timeout=30,
                verify=self.verify_ssl
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"✅ 查询成功")
                    return data.get('data', [])
                else:
                    print(f"❌ API错误：{data.get('msg')}")
                    return []
            else:
                print(f"❌ HTTP错误：{response.status_code}")
                print(f"   {response.text[:200]}")
                return []
        
        except Exception as e:
            print(f"❌ 请求失败：{str(e)[:100]}")
            return []
    
    def get_insight_result(self, task_id: int) -> Dict[str, Any]:
        """获取洞察任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            洞察结果数据
        """
        if not self.ak or not self.sk:
            print("❌ 错误：未配置 DMP_AK/DMP_SK")
            return {}
        
        print(f"📥 获取任务结果...")
        print(f"   任务ID: {task_id}")
        print(f"   API: /audience/insight/result")
        
        url = f"{self.base_url}/audience/insight/result"
        auth_params = self._build_auth_params()
        auth_params['taskId'] = str(task_id)
        
        try:
            response = requests.get(
                url,
                params=auth_params,
                timeout=30,
                verify=self.verify_ssl
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"✅ 获取成功")
                    return data.get('data', {})
                else:
                    print(f"❌ API错误：{data.get('msg')}")
                    return {}
            else:
                print(f"❌ HTTP错误：{response.status_code}")
                print(f"   {response.text[:200]}")
                return {}
        
        except Exception as e:
            print(f"❌ 请求失败：{str(e)[:100]}")
            return {}
    
    def parse_features(self, result_data: Dict) -> List[Dict]:
        """解析特征数据
        
        Args:
            result_data: API返回的原始数据
            
        Returns:
            解析后的特征列表
        """
        features = []
        
        if not result_data or not isinstance(result_data, dict):
            return features
        
        # 递归提取特征
        def extract_features(node, depth=0):
            if isinstance(node, dict):
                feature = {
                    'name': node.get('name', ''),
                    'coverage_rate': node.get('coverageRate', 0),
                    'tgi': node.get('tgi', 0),
                    'depth': depth
                }
                features.append(feature)
                
                # 递归处理子特征
                if 'children' in node and node['children']:
                    for child in node['children']:
                        extract_features(child, depth + 1)
        
        extract_features(result_data)
        return features


if __name__ == '__main__':
    # 使用示例
    import warnings
    warnings.filterwarnings('ignore')
    
    # 初始化API
    api = InsightAPI(ak='your_ak', sk='your_sk')
    
    # 查询任务状态
    print("查询任务状态示例：")
    status = api.query_insight_status([your_task_id])
    print(f"结果: {json.dumps(status, ensure_ascii=False, indent=2)}\n")
    
    # 获取任务结果
    print("获取任务结果示例：")
    result = api.get_insight_result(your_task_id)
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}\n")
