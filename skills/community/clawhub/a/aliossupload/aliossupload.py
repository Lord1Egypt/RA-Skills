#!/usr/bin/env python3
"""
阿里云 OSS 上传工具 - AliOSSUpload
支持单文件上传，自动读取环境变量配置
"""

import os
import sys
import json
import time
import logging
from typing import Optional, Dict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


try:
    import oss2
except ImportError:
    print("错误: 未安装 oss2 库，请运行: pip install oss2")
    sys.exit(1)


class AliOSSUploader:
    """阿里云 OSS 上传器"""
    
    def __init__(self):
        """初始化 OSS 上传器（自动从环境变量读取配置）"""
        self.config = self._load_config_from_env()
        self._validate_config()
        self._init_oss_client()
    
    def _load_config_from_env(self) -> Dict:
        """从环境变量加载配置"""
        config = {
            'access_key_id': os.getenv('ALIYUN_OSS_ACCESS_KEY_ID'),
            'access_key_secret': os.getenv('ALIYUN_OSS_ACCESS_KEY_SECRET'),
            'endpoint': os.getenv('ALIYUN_OSS_ENDPOINT'),
            'bucket_name': os.getenv('ALIYUN_OSS_BUCKET'),
        }
        return config
    
    def _validate_config(self):
        """验证配置"""
        required = ['access_key_id', 'access_key_secret', 'endpoint', 'bucket_name']
        missing = [f for f in required if not self.config.get(f)]
        
        if missing:
            raise ValueError(
                f"配置不完整，缺少: {', '.join(missing)}\n"
                "请设置环境变量:\n"
                "  export ALIYUN_OSS_ACCESS_KEY_ID='your-access-key-id'\n"
                "  export ALIYUN_OSS_ACCESS_KEY_SECRET='your-access-key-secret'\n"
                "  export ALIYUN_OSS_ENDPOINT='oss-cn-beijing.aliyuncs.com'\n"
                "  export ALIYUN_OSS_BUCKET='openclawark'"
            )
    
    def _init_oss_client(self):
        """初始化 OSS 客户端"""
        try:
            auth = oss2.Auth(
                self.config['access_key_id'],
                self.config['access_key_secret']
            )
            self.bucket = oss2.Bucket(
                auth,
                self.config['endpoint'],
                self.config['bucket_name']
            )
            # 测试连接
            self.bucket.get_bucket_info()
            logger.info(f"OSS 客户端初始化成功: {self.config['bucket_name']}")
        except Exception as e:
            raise ConnectionError(f"OSS 客户端初始化失败: {e}")
    
    def upload_file(self, local_file_path: str, object_name: Optional[str] = None) -> Dict:
        """
        上传单个文件到 OSS
        
        Args:
            local_file_path: 本地文件路径
            object_name: OSS 中的对象名称，默认为文件名
        
        Returns:
            包含 url, object_name, size 等信息的字典
        """
        local_file_path = os.path.expanduser(local_file_path)
        
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"文件不存在: {local_file_path}")
        
        if object_name is None:
            object_name = os.path.basename(local_file_path)
        
        file_size = os.path.getsize(local_file_path)
        logger.info(f"开始上传: {local_file_path} -> {object_name} ({self._human_readable_size(file_size)})")
        
        start_time = time.time()
        
        # 上传文件
        self.bucket.put_object_from_file(object_name, local_file_path)
        
        elapsed_time = time.time() - start_time
        url = f"https://{self.config['bucket_name']}.{self.config['endpoint']}/{object_name}"
        
        result = {
            'status': 'success',
            'url': url,
            'object_name': object_name,
            'size': file_size,
            'size_human': self._human_readable_size(file_size),
            'elapsed_time': f"{elapsed_time:.2f}s",
            'speed': f"{self._human_readable_size(file_size/elapsed_time)}/s" if elapsed_time > 0 else 'N/A'
        }
        
        logger.info(f"上传成功: {url}")
        logger.info(f"耗时: {result['elapsed_time']}, 平均速度: {result['speed']}")
        
        return result
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        """将字节大小转换为人类可读格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"


if __name__ == '__main__':
    # 简单测试
    uploader = AliOSSUploader()
    import sys
    test_file = sys.argv[1] if len(sys.argv) > 1 else "/tmp/test.txt"
    
    # 创建测试文件
    if not os.path.exists(test_file):
        with open(test_file, 'w') as f:
            f.write(f"Test file created at {time.time()}")
    
    result = uploader.upload_file(test_file, f"test/{os.path.basename(test_file)}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
