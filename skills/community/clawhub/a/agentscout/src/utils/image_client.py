"""图片生成 API 封装 - OpenAI 兼容协议，可切换服务商"""

import os
import httpx
from pathlib import Path
from openai import OpenAI

from src.config import ImageConfig


class ImageClient:
    """OpenAI 兼容的图片生成客户端，可指向任意服务商"""

    def __init__(self, config: ImageConfig):
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )
        self.model = config.model
        self.default_size = config.size
        self.style_prefix = config.style_prefix

    def generate(
        self,
        prompt: str,
        output_path: str,
        size: str = "",
        add_style_prefix: bool = True,
    ) -> str:
        """
        生成图片并保存到本地。

        Args:
            prompt: 图片描述
            output_path: 保存路径
            size: 图片尺寸，默认使用配置值
            add_style_prefix: 是否添加风格前缀

        Returns:
            保存的文件路径
        """
        full_prompt = f"{self.style_prefix}{prompt}" if add_style_prefix else prompt

        response = self.client.images.generate(
            model=self.model,
            prompt=full_prompt,
            size=size or self.default_size,
            n=1,
        )

        image_url = response.data[0].url
        if not image_url:
            # 某些 API 返回 b64_json
            import base64
            b64 = response.data[0].b64_json
            image_data = base64.b64decode(b64)
        else:
            # 下载图片
            resp = httpx.get(image_url, timeout=60)
            resp.raise_for_status()
            image_data = resp.content

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_data)

        return output_path
