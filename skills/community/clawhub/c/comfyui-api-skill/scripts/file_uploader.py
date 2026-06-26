#!/usr/bin/env python3
"""
ComfyUI 文件上传器

功能：
1. 上传多种类型文件到 ComfyUI（图像、视频、音频、模型等）
2. 支持蒙版上传
3. 支持从配置文件读取配置
4. 自动检测文件类型并设置正确的 MIME 类型

使用示例：
    python file_uploader.py --file ./reference.png
    python file_uploader.py --file ./video.mp4 --subfolder input
    python file_uploader.py --type mask --file ./mask.png
    python file_uploader.py --file ./model.glb --type model
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

try:
    import requests
except ImportError:
    print("错误：缺少 requests 库，请运行：pip install requests>=2.28.0")
    sys.exit(1)

# 导入配置加载器
try:
    from config_loader import get_config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import get_config


class FileUploader:
    """ComfyUI 文件上传器"""
    
    # 文件类型映射：扩展名 -> (MIME类型, 字段名)
    FILE_TYPE_MAP = {
        # 图像格式
        '.png': ('image/png', 'image'),
        '.jpg': ('image/jpeg', 'image'),
        '.jpeg': ('image/jpeg', 'image'),
        '.webp': ('image/webp', 'image'),
        '.gif': ('image/gif', 'image'),
        '.bmp': ('image/bmp', 'image'),
        '.tiff': ('image/tiff', 'image'),
        '.tif': ('image/tiff', 'image'),
        '.exr': ('image/x-exr', 'image'),
        
        # 视频格式
        '.mp4': ('video/mp4', 'video'),
        '.avi': ('video/x-msvideo', 'video'),
        '.mov': ('video/quicktime', 'video'),
        '.mkv': ('video/x-matroska', 'video'),
        '.webm': ('video/webm', 'video'),
        '.flv': ('video/x-flv', 'video'),
        
        # 音频格式
        '.mp3': ('audio/mpeg', 'audio'),
        '.wav': ('audio/wav', 'audio'),
        '.ogg': ('audio/ogg', 'audio'),
        '.flac': ('audio/flac', 'audio'),
        '.aac': ('audio/aac', 'audio'),
        '.m4a': ('audio/mp4', 'audio'),
        
        # 3D 模型格式
        '.obj': ('model/obj', 'model'),
        '.gltf': ('model/gltf+json', 'model'),
        '.glb': ('model/gltf-binary', 'model'),
        '.fbx': ('model/fbx', 'model'),
        '.stl': ('model/stl', 'model'),
        
        # 其他格式
        '.json': ('application/json', 'file'),
        '.txt': ('text/plain', 'file'),
        '.csv': ('text/csv', 'file'),
    }
    
    def __init__(self, server_url: str = None, api_key: str = None):
        """
        初始化文件上传器
        
        Args:
            server_url: ComfyUI 服务地址
            api_key: API 密钥（可选）
        """
        # 加载配置
        config = get_config()
        
        # 使用配置优先级
        self.server_url = config.get_server_url(cli_value=server_url)
        self.api_key = config.get_api_key(cli_value=api_key)
        self.session = requests.Session()
        
        # 设置请求头
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
    
    def detect_file_type(self, file_path: str) -> Tuple[str, str, str]:
        """
        检测文件类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            (MIME类型, 字段名, 类型标签)
        """
        ext = Path(file_path).suffix.lower()
        
        if ext in self.FILE_TYPE_MAP:
            mime_type, field_name = self.FILE_TYPE_MAP[ext]
        else:
            # 默认作为普通文件
            mime_type = 'application/octet-stream'
            field_name = 'file'
        
        # 确定类型标签
        type_labels = {
            'image': '图像',
            'video': '视频',
            'audio': '音频',
            'model': '3D模型',
            'file': '文件'
        }
        type_label = type_labels.get(field_name, '文件')
        
        return mime_type, field_name, type_label
    
    def upload_file(
        self,
        file_path: str,
        file_type: str = None,
        subfolder: str = "",
        overwrite: bool = True,
        image_type: str = None
    ) -> Dict[str, Any]:
        """
        上传文件到 ComfyUI（支持多种类型）
        
        Args:
            file_path: 文件路径
            file_type: 文件类型（image/mask/video/audio/model/file），不指定则自动检测
            subfolder: 子文件夹路径
            overwrite: 是否覆盖已存在的文件
            image_type: 图像类型（仅用于图像文件，如 'input', 'output'）
            
        Returns:
            上传结果，包含文件名、子文件夹等信息
            
        Raises:
            Exception: 上传失败时抛出异常
        """
        # 检查文件是否存在
        path = Path(file_path)
        if not path.exists():
            raise Exception(f"文件不存在: {file_path}")
        
        # 检测或使用指定的文件类型
        mime_type, detected_field, type_label = self.detect_file_type(file_path)
        
        if file_type:
            field_name = file_type
            # 如果明确指定了 mask 类型
            if file_type == 'mask':
                field_name = 'mask'
                mime_type = 'image/png'
                type_label = '蒙版'
        else:
            field_name = detected_field
        
        # 确定上传端点
        # ComfyUI 的 /upload/image 端点可以处理多种文件类型
        # 但 mask 需要使用专门的 /upload/mask 端点
        if field_name == 'mask':
            upload_url = f"{self.server_url}/upload/mask"
        else:
            upload_url = f"{self.server_url}/upload/image"
        
        # 准备上传数据
        files = {
            field_name: (path.name, open(path, "rb"), mime_type)
        }
        
        data = {
            "overwrite": "true" if overwrite else "false"
        }
        
        if subfolder:
            data["subfolder"] = subfolder
        
        if image_type:
            data["type"] = image_type
        
        try:
            print(f"⏳ 正在上传 [{type_label}]: {path.name}")
            
            response = self.session.post(
                upload_url,
                files=files,
                data=data,
                timeout=120  # 增加超时时间以适应大文件
            )
            
            if response.status_code >= 400:
                raise Exception(f"上传失败: HTTP {response.status_code}, {response.text}")
            
            result = response.json()
            
            # 添加额外信息
            result['file_type'] = field_name
            result['mime_type'] = mime_type
            result['size'] = path.stat().st_size
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        finally:
            files[field_name][1].close()
    
    def upload_image(
        self,
        file_path: str,
        subfolder: str = "",
        overwrite: bool = True
    ) -> Dict[str, Any]:
        """
        上传图片（兼容旧接口）
        
        Args:
            file_path: 图片文件路径
            subfolder: 子文件夹路径
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            上传结果
        """
        return self.upload_file(
            file_path=file_path,
            file_type='image',
            subfolder=subfolder,
            overwrite=overwrite
        )
    
    def upload_mask(
        self,
        file_path: str,
        subfolder: str = "",
        overwrite: bool = True
    ) -> Dict[str, Any]:
        """
        上传蒙版（兼容旧接口）
        
        Args:
            file_path: 蒙版文件路径
            subfolder: 子文件夹路径
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            上传结果
        """
        return self.upload_file(
            file_path=file_path,
            file_type='mask',
            subfolder=subfolder,
            overwrite=overwrite
        )
    
    def format_size(self, size: int) -> str:
        """
        格式化文件大小
        
        Args:
            size: 文件大小（字节）
            
        Returns:
            格式化的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="ComfyUI 文件上传器（支持多种文件类型）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的文件类型：
  图像：PNG, JPG, WebP, GIF, BMP, TIFF, EXR
  视频：MP4, AVI, MOV, MKV, WebM, FLV
  音频：MP3, WAV, OGG, FLAC, AAC, M4A
  模型：OBJ, GLTF, GLB, FBX, STL
  其他：JSON, TXT, CSV 等

示例：
  python file_uploader.py --file ./reference.png
  python file_uploader.py --file ./video.mp4 --subfolder input
  python file_uploader.py --type mask --file ./mask.png
  python file_uploader.py --file ./model.glb --type model
  python file_uploader.py --file ./audio.mp3
        """
    )
    
    parser.add_argument(
        "--file",
        required=True,
        help="文件路径"
    )
    
    parser.add_argument(
        "--type",
        choices=["image", "mask", "video", "audio", "model", "file"],
        help="文件类型（不指定则自动检测）"
    )
    
    parser.add_argument(
        "--subfolder",
        default="",
        help="子文件夹路径（默认：空）"
    )
    
    parser.add_argument(
        "--image-type",
        help="图像类型（input/output/temp，仅用于图像文件）"
    )
    
    parser.add_argument(
        "--server-url",
        help="ComfyUI 服务地址（默认：使用配置文件中的值）"
    )
    
    parser.add_argument(
        "--api-key",
        help="API 密钥（可选）"
    )
    
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="不覆盖已存在的文件"
    )
    
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="以 JSON 格式输出结果"
    )
    
    args = parser.parse_args()
    
    # 创建文件上传器
    uploader = FileUploader(
        server_url=args.server_url,
        api_key=args.api_key
    )
    
    try:
        result = uploader.upload_file(
            file_path=args.file,
            file_type=args.type,
            subfolder=args.subfolder,
            overwrite=not args.no_overwrite,
            image_type=args.image_type
        )
        
        if args.output_json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("\n✓ 文件上传成功")
            print(f"文件名: {result.get('name', 'N/A')}")
            print(f"类型: {result.get('file_type', 'N/A')}")
            print(f"子文件夹: {result.get('subfolder', 'N/A')}")
            print(f"大小: {uploader.format_size(result.get('size', 0))}")
            
            # 显示在工作流中如何使用
            filename = result.get('name', '')
            subfolder = result.get('subfolder', '')
            if filename:
                print(f"\n在工作流中使用：")
                if subfolder:
                    print(f'  路径: {subfolder}/{filename}')
                else:
                    print(f'  路径: {filename}')
        
    except Exception as e:
        print(f"\n✗ 上传失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
