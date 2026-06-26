#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产验证器 - GEP 1.6.0 规范验证
2026-04-06 更新：
1. 添加 Hub validate 接口验证哈希
2. 添加 sha256: 前缀确保
3. 添加 asset_id 剔除逻辑
"""

from typing import Dict, List, Tuple, Optional
import json
import hashlib
import requests
import copy


class AssetValidator:
    """资产验证器"""
    
    def __init__(self, schema_version: str = "1.6.0"):
        self.schema_version = schema_version
        self.required_fields = {
            'Gene': ['type', 'schema_version', 'category', 'signals_match', 'summary', 'strategy'],
            'Capsule': ['type', 'schema_version', 'trigger', 'gene', 'summary', 'content', 'confidence']
        }
    
    def validate(self, asset: Dict, asset_type: str) -> Tuple[bool, str, List[str]]:
        """验证资产"""
        errors = []
        
        # 检查必填字段
        required = self.required_fields.get(asset_type, [])
        for field in required:
            if field not in asset:
                errors.append(f"缺少必填字段：{field}")
        
        # 检查 schema_version
        if asset.get('schema_version') != self.schema_version:
            errors.append(f"schema_version 不匹配：期望 {self.schema_version}, 实际 {asset.get('schema_version')}")
        
        # 检查信号数量
        signals = asset.get('signals_match', asset.get('trigger', []))
        if len(signals) < 2:
            errors.append("信号数量不足：至少需要 2 个信号")
        elif len(signals) > 10:
            errors.append("信号数量过多：最多 10 个信号")
        
        # 检查内容长度
        summary = asset.get('summary', '')
        if len(summary) < 100:
            errors.append(f"summary 长度不足：{len(summary)} < 100")
        
        valid = len(errors) == 0
        message = "验证通过" if valid else f"验证失败：{len(errors)} 个错误"
        
        return valid, message, errors
    
    def validate_gene(self, gene: Dict) -> Tuple[bool, str, List[str]]:
        """验证 Gene"""
        return self.validate(gene, 'Gene')
    
    def validate_capsule(self, capsule: Dict) -> Tuple[bool, str, List[str]]:
        """验证 Capsule"""
        return self.validate(capsule, 'Capsule')
    
    # ==================== 2026-04-06 新增方法 ====================
    
    def ensure_sha256_prefix(self, asset_id: str) -> str:
        """确保 asset_id 带有 sha256: 前缀"""
        if not asset_id:
            return ""
        if asset_id.startswith('sha256:'):
            return asset_id
        return f"sha256:{asset_id}"
    
    def remove_asset_id(self, asset: Dict) -> Dict:
        """剔除 asset_id 字段（哈希计算前必须）"""
        asset_copy = copy.deepcopy(asset)
        if 'asset_id' in asset_copy:
            del asset_copy['asset_id']
        return asset_copy
    
    def compute_asset_hash(self, asset: Dict) -> str:
        """计算资产哈希（剔除 asset_id 后）"""
        # 剔除 asset_id
        clean_asset = self.remove_asset_id(asset)
        # Canonicalize（键值排序）
        canonical_json = json.dumps(clean_asset, sort_keys=True, separators=(',', ':'))
        # SHA256 计算
        hash_value = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
        return self.ensure_sha256_prefix(hash_value)
    
    def validate_with_hub(self, asset: Dict, auth_token: str, asset_type: str = 'Gene') -> Tuple[bool, str, Optional[str]]:
        """
        使用 Hub validate 接口验证哈希（官方外挂）
        
        Args:
            asset: 资产对象（Gene 或 Capsule）
            auth_token: Authorization Token
            asset_type: 资产类型
            
        Returns:
            (success, message, computed_asset_id)
        """
        url = "https://evomap.ai/a2a/validate"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        # 构建验证请求（7 要素信封）
        payload = {
            "payload": {
                "assets": [asset]
            }
        }
        
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            data = resp.json()
            
            if resp.status_code == 200 and data.get('status') == 'ok':
                # 提取 Hub 计算的正確哈希
                computed_assets = data.get('computed_assets', [])
                if computed_assets:
                    computed_id = computed_assets[0].get('computed_asset_id')
                    return True, "Hub 验证通过", self.ensure_sha256_prefix(computed_id)
                else:
                    return False, "Hub 未返回 computed_assets", None
            else:
                error_msg = data.get('msg', data.get('error', '未知错误'))
                return False, f"Hub 验证失败：{error_msg}", None
                
        except requests.exceptions.Timeout:
            return False, "Hub 验证超时", None
        except Exception as e:
            return False, f"Hub 验证异常：{str(e)}", None
    
    def fix_asset_hash(self, asset: Dict, auth_token: str) -> Tuple[bool, str, Dict]:
        """
        自动修复资产哈希（偷梁换柱法）
        
        流程：
        1. 调用 validate 接口获取正确的 computed_asset_id
        2. 替换 asset 中的 asset_id
        3. 返回修复后的资产
        
        Args:
            asset: 原始资产对象
            auth_token: Authorization Token
            
        Returns:
            (success, message, fixed_asset)
        """
        # 调用 Hub 验证
        success, msg, computed_id = self.validate_with_hub(asset, auth_token)
        
        if not success:
            return False, msg, asset
        
        # 偷梁换柱：替换 asset_id
        fixed_asset = copy.deepcopy(asset)
        fixed_asset['asset_id'] = computed_id
        
        return True, f"哈希已修复：{computed_id}", fixed_asset
    validator = AssetValidator()
    
    # 测试验证
    gene = {
        'type': 'Gene',
        'schema_version': '1.6.0',
        'category': 'optimize',
        'signals_match': ['optimization', 'performance'],
        'summary': 'A' * 100,
        'strategy': ['Step 1', 'Step 2', 'Step 3']
    }
    
    valid, message, errors = validator.validate_gene(gene)
    print(f"验证结果：{message}")
    if errors:
        print(f"错误：{errors}")
