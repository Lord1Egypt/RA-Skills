"""
Configuration module for Cloud Storage Manager
云存储管理器配置模块
"""

import os
from typing import Dict, Any


def load_config(provider: str) -> Dict[str, Any]:
    """
    Load configuration from environment variables
    从环境变量加载配置
    
    Args:
        provider: Provider name (e.g., 'aliyun_oss', 'aws_s3')
        
    Returns:
        Configuration dictionary
    """
    config = {}
    
    provider_configs = {
        'aliyun_oss': {
            'access_key_id': 'ALIYUN_ACCESS_KEY_ID',
            'access_key_secret': 'ALIYUN_ACCESS_KEY_SECRET',
            'endpoint': 'ALIYUN_OSS_ENDPOINT',
            'bucket': 'ALIYUN_OSS_BUCKET',
        },
        'aws_s3': {
            'access_key_id': 'AWS_ACCESS_KEY_ID',
            'secret_access_key': 'AWS_SECRET_ACCESS_KEY',
            'region': 'AWS_REGION',
            'bucket': 'AWS_BUCKET',
        },
        'tencent_cos': {
            'secret_id': 'TENCENT_SECRET_ID',
            'secret_key': 'TENCENT_SECRET_KEY',
            'region': 'TENCENT_COS_REGION',
            'bucket': 'TENCENT_COS_BUCKET',
        },
        'azure_blob': {
            'connection_string': 'AZURE_STORAGE_CONNECTION_STRING',
            'container': 'AZURE_CONTAINER',
        },
    }
    
    if provider not in provider_configs:
        raise ValueError(f"Unknown provider: {provider}")
    
    for key, env_var in provider_configs[provider].items():
        value = os.getenv(env_var)
        if value:
            config[key] = value
    
    return config
