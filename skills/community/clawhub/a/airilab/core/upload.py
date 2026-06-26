#!/usr/bin/env python3
"""
AiriLab 图片上传

整合原 airi-upload 技能的功能：
1. 上传图片到 S3
2. 支持多种图片类型（base-image, reference-image 等）
"""

import requests
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from .config import AiriLabConfig
except ImportError:  # pragma: no cover
    from config import AiriLabConfig

# API 端点
UPLOAD_URL = "https://cn.airilab.com/api/Workflow/UploadMedia"


class AiriLabUpload:
    """AiriLab 图片上传器"""
    
    def __init__(self, config: AiriLabConfig = None):
        """
        初始化上传器
        
        参数:
            config: 配置管理器实例
        """
        self.config = config or AiriLabConfig()
    
    def upload_image(self, file_path: str, image_part: str = "base-image", 
                     team_id: int = 0) -> Dict[str, Any]:
        """
        上传图片到 S3
        
        参数:
            file_path: 图片文件路径
            image_part: 图片类型 (base-image, reference-image, mask-image 等)
            team_id: 团队 ID
        
        返回:
            dict: {
                'success': bool,
                'url': str | None,
                'message': str
            }
        """
        token = self.config.get_token()
        
        if not token:
            return {
                'success': False,
                'url': None,
                'message': 'Token 不存在，请先登录'
            }
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {
                'success': False,
                'url': None,
                'message': f'文件不存在：{file_path}'
            }
        
        try:
            with open(file_path, 'rb') as f:
                files = {'myFile': (file_path.name, f, 'image/jpeg')}
                data = {
                    'imagePart': image_part,
                    'teamId': str(team_id)
                }
                
                response = requests.post(
                    UPLOAD_URL,
                    headers={'Authorization': f'Bearer {token}'},
                    files=files,
                    data=data,
                    timeout=60
                )
                
                result = response.json()
                
                if result.get('status') == 200:
                    url = result.get('data', {}).get('path', '')
                    return {
                        'success': True,
                        'url': url,
                        'message': f'上传成功：{url}'
                    }
                else:
                    return {
                        'success': False,
                        'url': None,
                        'message': f'上传失败：{result}'
                    }
                    
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'url': None,
                'message': f'网络错误：{str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'url': None,
                'message': f'上传错误：{str(e)}'
            }


# ==================== 命令行入口 ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AiriLab 图片上传")
    parser.add_argument("file", help="图片文件路径")
    parser.add_argument("--type", dest="image_type", default="base-image",
                       choices=["base-image", "reference-image", "mask-image", "video-thumbnail"],
                       help="图片类型")
    parser.add_argument("--team-id", type=int, default=0, help="团队 ID")
    
    args = parser.parse_args()
    
    config = AiriLabConfig()
    upload = AiriLabUpload(config)
    
    result = upload.upload_image(args.file, args.image_type, args.team_id)
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")
