#!/usr/bin/env python3
"""
AI视觉识别技能 v1.1
安全的图片和视频识别工具
支持：智谱AI、OpenAI、Anthropic、DeepSeek、通义千问等
"""

import os
import base64
import mimetypes
from pathlib import Path
from typing import Optional, Dict, List
import json

# 导入LLM配置
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_config import LLMConfig


class AISecurityError(Exception):
    """安全异常"""
    pass


class FileValidator:
    """文件安全验证器"""

    # 允许的文件类型
    ALLOWED_TYPES = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/webp': '.webp',
        'image/gif': '.gif'
    }

    # 最大文件大小 (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    @classmethod
    def validate_file(cls, file_path: str) -> Dict:
        """
        验证文件安全性

        Returns:
            包含文件信息的字典
        """
        path = Path(file_path)

        # 检查文件是否存在
        if not path.exists():
            raise AISecurityError("文件不存在")

        # 检查文件大小
        file_size = path.stat().st_size
        if file_size > cls.MAX_FILE_SIZE:
            raise AISecurityError(f"文件过大 ({file_size} > {cls.MAX_FILE_SIZE})")

        if file_size == 0:
            raise AISecurityError("文件为空")

        # 检查文件类型
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type not in cls.ALLOWED_TYPES:
            raise AISecurityError(f"不支持的文件类型: {mime_type}")

        # 检查扩展名
        ext = cls.ALLOWED_TYPES[mime_type]
        if path.suffix.lower() not in [ext, ext[1:]]:
            raise AISecurityError("文件扩展名与类型不匹配")

        return {
            'path': str(path),
            'size': file_size,
            'mime_type': mime_type,
            'extension': path.suffix
        }

    @classmethod
    def validate_directory(cls, directory: str) -> List[Dict]:
        """验证目录中的所有图片文件"""
        path = Path(directory)

        if not path.is_dir():
            raise AISecurityError("不是有效的目录")

        valid_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            for file_path in path.glob(f"**/*{ext}"):
                try:
                    info = cls.validate_file(str(file_path))
                    valid_files.append(info)
                except AISecurityError:
                    continue

        return valid_files


class LocalVisionAI:
    """本地视觉AI（使用本地模型）"""

    def __init__(self):
        """初始化本地视觉AI"""
        self.model = None
        self._load_model()

    def _load_model(self):
        """加载本地模型"""
        try:
            import torch
            from transformers import BlipProcessor, BlipForConditionalGeneration

            print("加载本地视觉模型...")
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            print("✓ 模型加载成功")

        except ImportError:
            print("提示: 安装 torch transformers 以使用本地模型")
            print("命令: pip install torch transformers pillow")
        except Exception as e:
            print(f"模型加载失败: {e}")

    def analyze_image(self, image_path: str) -> Dict:
        """
        分析本地图片

        Args:
            image_path: 图片路径

        Returns:
            分析结果
        """
        # 文件验证
        file_info = FileValidator.validate_file(image_path)

        if self.model is None:
            return {
                'error': '本地模型未加载',
                'suggestion': '请使用API模式或安装本地模型依赖'
            }

        try:
            from PIL import Image

            image = Image.open(image_path).convert('RGB')

            # 生成描述
            inputs = self.processor(image, return_tensors="pt")
            out = self.model.generate(**inputs)
            description = self.processor.decode(out[0], skip_special_tokens=True)

            return {
                'file': file_info['path'],
                'size': file_info['size'],
                'description': description,
                'confidence': 'N/A'
            }

        except Exception as e:
            return {
                'error': f'分析失败: {str(e)}'
            }


class APIVisionAI:
    """API视觉AI（支持多个大模型提供商）"""

    def __init__(self, provider: str = "zhipu", api_key: str = None):
        """
        初始化API视觉AI

        Args:
            provider: 提供商 (zhipu, openai, anthropic, deepseek, qwen等)
            api_key: API密钥（可选，默认从环境变量或配置文件读取）
        """
        try:
            self.llm_config = LLMConfig(provider)
            if api_key:
                self.llm_config.api_key = api_key

            if not self.llm_config.is_available():
                print(f"警告: 未找到{provider} API密钥")
                print(f"请设置环境变量 {self.llm_config.config['api_key_env']}")

            self.provider = provider
            self.model = self.llm_config.get_model('vision')

        except Exception as e:
            print(f"配置错误: {e}")
            self.llm_config = None

    def image_to_base64(self, image_path: str) -> str:
        """将图片转换为base64"""
        file_info = FileValidator.validate_file(image_path)

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_path: str, prompt: str = "请详细描述这张图片的内容") -> Dict:
        """
        使用API分析图片

        Args:
            image_path: 图片路径
            prompt: 分析提示词

        Returns:
            分析结果
        """
        # 文件验证
        file_info = FileValidator.validate_file(image_path)

        if not self.llm_config or not self.llm_config.is_available():
            return {
                'error': '未配置API密钥',
                'suggestion': f'请设置环境变量 {self.llm_config.config["api_key_env"] if self.llm_config else "相关"}'
            }

        try:
            # 检查是否支持视觉能力
            if not self.llm_config.get_model('vision'):
                return {
                    'error': f'{self.llm_config.config["name"]} 暂不支持视觉识别',
                    'suggestion': '请使用其他支持视觉的模型（如zhipu、openai、qwen）'
                }

            # 根据提供商选择调用方式
            library = self.llm_config.get_library()

            if library == 'openai':
                return self._analyze_with_openai_compatible(image_path, prompt)
            elif library == 'anthropic':
                return self._analyze_with_anthropic(image_path, prompt)
            else:
                return {'error': f'暂不支持的库类型: {library}'}

        except Exception as e:
            return {
                'error': f'API调用失败: {str(e)}'
            }

    def _analyze_with_openai_compatible(self, image_path: str, prompt: str) -> Dict:
        """使用OpenAI兼容API（智谱、DeepSeek、通义等）"""
        try:
            from openai import OpenAI

            base64_image = self.image_to_base64(image_path)
            file_info = FileValidator.validate_file(image_path)

            client = OpenAI(
                api_key=self.llm_config.api_key,
                base_url=self.llm_config.get_base_url()
            )

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{file_info['mime_type']};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )

            description = response.choices[0].message.content

            return {
                'file': image_path,
                'size': file_info['size'],
                'description': description,
                'provider': self.llm_config.config['name'],
                'model': self.model
            }

        except ImportError:
            return {'error': '请安装 openai 库: pip install openai'}
        except Exception as e:
            return {'error': f'{self.llm_config.config["name"]} API错误: {str(e)}'}

    def _analyze_with_anthropic(self, image_path: str, prompt: str) -> Dict:
        """使用Anthropic API"""
        try:
            import anthropic

            base64_image = self.image_to_base64(image_path)
            file_info = FileValidator.validate_file(image_path)

            client = anthropic.Anthropic(api_key=self.llm_config.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": file_info['mime_type'],
                                    "data": base64_image
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            description = message.content[0].text

            return {
                'file': image_path,
                'description': description,
                'provider': self.llm_config.config['name'],
                'model': self.model
            }

        except ImportError:
            return {'error': '请安装 anthropic 库: pip install anthropic'}
        except Exception as e:
            return {'error': f'Anthropic API错误: {str(e)}'}


class VisionAI:
    """统一的视觉AI接口"""

    def __init__(self, mode: str = "api", provider: str = "zhipu", api_key: str = None):
        """
        初始化视觉AI

        Args:
            mode: 运行模式 (local, api)
            provider: 提供商 (zhipu, openai, anthropic, deepseek, qwen等)
            api_key: API密钥（API模式需要）
        """
        self.mode = mode
        self.provider = provider

        if mode == "local":
            self.analyzer = LocalVisionAI()
        else:
            self.analyzer = APIVisionAI(provider, api_key)

    def analyze(self, image_path: str, prompt: str = "请详细描述这张图片") -> Dict:
        """
        分析图片

        Args:
            image_path: 图片路径
            prompt: 分析提示词

        Returns:
            分析结果字典
        """
        return self.analyzer.analyze_image(image_path, prompt)

    def batch_analyze(self, directory: str) -> List[Dict]:
        """
        批量分析目录中的图片

        Args:
            directory: 目录路径

        Returns:
            所有图片的分析结果
        """
        files = FileValidator.validate_directory(directory)

        results = []
        for i, file_info in enumerate(files, 1):
            print(f"分析 {i}/{len(files)}: {file_info['path']}")

            result = self.analyze(file_info['path'])
            results.append(result)

        return results


def main():
    """命令行界面"""
    print("=" * 50)
    print("AI视觉识别工具 v1.1")
    print("=" * 50)

    print("\n支持的提供商:")
    providers = LLMConfig.list_providers()
    for key, name in providers.items():
        print(f"  {key}. {name}")

    provider = input("\n请选择提供商 (默认zhipu): ").strip() or "zhipu"

    print("\n选择模式:")
    print("1. API模式 (推荐，支持多个大模型)")
    print("2. 本地模式 (无需API，但需要下载模型)")

    mode_choice = input("\n请选择 (1/2, 默认1): ").strip()

    mode = "local" if mode_choice == "2" else "api"

    if mode == "api":
        vision = VisionAI(mode="api", provider=provider)

        # 检查API配置
        if hasattr(vision.analyzer, 'llm_config') and vision.analyzer.llm_config:
            info = vision.analyzer.llm_config.get_info()
            print(f"\n配置信息:")
            print(f"  提供商: {info['name']}")
            print(f"  API密钥: {'已设置' if info['api_key_set'] else '未设置'}")

            if not info['api_key_set']:
                print(f"\n请设置环境变量: {vision.analyzer.llm_config.config['api_key_env']}")
                print(f"或运行: python ../llm_config.py")
    else:
        vision = VisionAI(mode="local")

    while True:
        print("\n请选择操作:")
        print("1. 分析单张图片")
        print("2. 批量分析目录")
        print("0. 退出")

        choice = input("\n请输入选项: ").strip()

        if choice == "0":
            print("再见！")
            break

        elif choice == "1":
            image_path = input("请输入图片路径: ").strip()

            prompt = input("请输入分析提示 (可选，按回车使用默认): ").strip()
            if not prompt:
                prompt = "请详细描述这张图片的内容"

            result = vision.analyze(image_path, prompt)

            print("\n" + "=" * 50)
            print("分析结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "2":
            directory = input("请输入目录路径: ").strip()

            results = vision.batch_analyze(directory)

            print("\n" + "=" * 50)
            print(f"批量分析完成，共 {len(results)} 张图片")

            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result.get('file', 'N/A')}")
                if 'error' in result:
                    print(f"   错误: {result['error']}")
                else:
                    print(f"   描述: {result.get('description', 'N/A')[:100]}...")


if __name__ == "__main__":
    main()
