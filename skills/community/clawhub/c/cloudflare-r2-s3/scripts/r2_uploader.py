#!/usr/bin/env python3
"""
Cloudflare R2 S3 上传工具
支持上传本地文件到 R2 存储桶并生成公开访问地址
"""

import os
import sys
import argparse
import boto3
from botocore.config import Config
from dotenv import load_dotenv
from typing import Optional, Dict, List


class R2Uploader:
    """Cloudflare R2 S3 兼容存储上传器"""
    
    def __init__(
        self,
        account_id: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        bucket_name: Optional[str] = None,
        public_domain: Optional[str] = None,
        default_public: bool = True,
        config_file: Optional[str] = None
    ):
        """
        初始化 R2 上传器
        
        Args:
            account_id: Cloudflare 账户 ID，如果不传入则从环境变量读取
            access_key_id: S3 访问密钥 ID
            secret_access_key: S3 秘密访问密钥
            bucket_name: 存储桶名称
            public_domain: 自定义公开域名
            default_public: 是否默认公开可读
            config_file: 配置文件路径，默认为 ~/.openclaw/config/cloudflare-r2.env
        """
        # 加载配置
        if config_file is None:
            config_file = os.path.expanduser("~/.openclaw/config/cloudflare-r2.env")
        
        if os.path.exists(config_file):
            load_dotenv(config_file)
        
        # 从参数或环境变量获取配置
        self.account_id = account_id or os.getenv("CLOUDFLARE_R2_ACCOUNT_ID")
        self.access_key_id = access_key_id or os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
        self.secret_access_key = secret_access_key or os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        self.bucket_name = bucket_name or os.getenv("CLOUDFLARE_R2_BUCKET_NAME")
        self.public_domain = public_domain or os.getenv("CLOUDFLARE_R2_PUBLIC_DOMAIN")
        self.default_public = default_public if default_public is not None else \
            os.getenv("CLOUDFLARE_R2_DEFAULT_PUBLIC", "true").lower() == "true"
        
        # 验证配置
        self._validate_config()
        
        # 初始化 S3 客户端
        self.s3_client = self._init_s3_client()
    
    def _validate_config(self):
        """验证配置是否完整"""
        missing = []
        if not self.account_id:
            missing.append("CLOUDFLARE_R2_ACCOUNT_ID")
        if not self.access_key_id:
            missing.append("CLOUDFLARE_R2_ACCESS_KEY_ID")
        if not self.secret_access_key:
            missing.append("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        if not self.bucket_name:
            missing.append("CLOUDFLARE_R2_BUCKET_NAME")
        
        if missing:
            raise ValueError(
                f"缺少必要配置: {', '.join(missing)}\n"
                "请在 ~/.openclaw/config/cloudflare-r2.env 中配置，或者通过参数传入。"
                "参考: https://github.com/openclaw/openclaw/blob/main/skills/cloudflare-r2-s3/references/config_example.env"
            )
    
    def _init_s3_client(self) -> boto3.client:
        """初始化 S3 客户端"""
        endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
        
        config = Config(
            region_name='auto',
            signature_version='s3v4',
        )
        
        s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            config=config
        )
        
        return s3
    
    def get_public_url(self, object_name: str) -> str:
        """
        获取对象的公开访问 URL
        
        Args:
            object_name: 对象名称
            
        Returns:
            公开访问 URL
        """
        if self.public_domain:
            # 使用自定义域名
            if self.public_domain.startswith(('http://', 'https://')):
                base_url = self.public_domain.rstrip('/')
            else:
                base_url = f"https://{self.public_domain}"
            return f"{base_url}/{object_name}"
        else:
            # 使用 Cloudflare 默认公开域名
            return f"https://pub-{self.bucket_name}.r2.dev/{object_name}"
    
    def upload_file(
        self,
        local_path: str,
        object_name: Optional[str] = None,
        public: Optional[bool] = None,
        content_type: Optional[str] = None
    ) -> Dict:
        """
        上传本地文件到 R2 存储桶
        
        Args:
            local_path: 本地文件路径
            object_name: 存储桶中的对象名称，不传入则使用文件名
            public: 是否公开可读，默认使用配置中的 default_public
            content_type: Content-Type，不传入则自动检测
            
        Returns:
            包含上传结果和公开 URL 的字典
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"文件不存在: {local_path}")
        
        if object_name is None:
            object_name = os.path.basename(local_path)
        
        if public is None:
            public = self.default_public
        
        # 上传参数
        extra_args = {}
        if public:
            extra_args['ACL'] = 'public-read'
        
        if content_type:
            extra_args['ContentType'] = content_type
        
        # 执行上传
        self.s3_client.upload_file(
            local_path,
            self.bucket_name,
            object_name,
            ExtraArgs=extra_args
        )
        
        public_url = self.get_public_url(object_name)
        
        return {
            'success': True,
            'local_path': local_path,
            'object_name': object_name,
            'bucket': self.bucket_name,
            'public_url': public_url,
            'public': public
        }
    
    def list_files(self) -> List[Dict]:
        """列出存储桶中的所有文件"""
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'public_url': self.get_public_url(obj['Key'])
                })
        
        return files
    
    def delete_file(self, object_name: str) -> Dict:
        """删除存储桶中的文件"""
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=object_name
        )
        
        return {
            'success': True,
            'object_name': object_name,
            'bucket': self.bucket_name
        }
    
    def test_connection(self) -> bool:
        """测试连接是否正常"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception as e:
            print(f"连接测试失败: {e}")
            return False


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='Cloudflare R2 S3 文件上传工具'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # upload 命令
    upload_parser = subparsers.add_parser('upload', help='上传文件')
    upload_parser.add_argument('file_path', help='本地文件路径')
    upload_parser.add_argument('object_name', nargs='?', help='存储桶对象名称，默认使用文件名')
    upload_parser.add_argument('--private', action='store_true', help='设为私有，不公开')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出存储桶中文件')
    
    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除文件')
    delete_parser.add_argument('object_name', help='要删除的对象名称')
    
    # test 命令
    test_parser = subparsers.add_parser('test', help='测试连接')
    
    args = parser.parse_args()
    
    try:
        uploader = R2Uploader()
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    if args.command == 'upload':
        try:
            result = uploader.upload_file(
                args.file_path,
                args.object_name,
                public=not args.private
            )
            print("✅ 上传成功!")
            print(f"📁 本地文件: {result['local_path']}")
            print(f"📦 存储桶对象: {result['object_name']}")
            print(f"🔗 公开地址: {result['public_url']}")
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            sys.exit(1)
    
    elif args.command == 'list':
        files = uploader.list_files()
        if not files:
            print("📭 存储桶为空")
            return
        
        print(f"📂 存储桶 {uploader.bucket_name} 中的文件 ({len(files)}):\n")
        for i, f in enumerate(files, 1):
            size_kb = f['size'] / 1024
            print(f"{i}. {f['key']}")
            print(f"   大小: {size_kb:.1f} KB")
            print(f"   地址: {f['public_url']}")
            print()
    
    elif args.command == 'delete':
        try:
            result = uploader.delete_file(args.object_name)
            print(f"✅ 删除成功: {result['object_name']}")
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            sys.exit(1)
    
    elif args.command == 'test':
        if uploader.test_connection():
            print("✅ 连接成功！配置正确。")
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
