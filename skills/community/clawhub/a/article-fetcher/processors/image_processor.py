import oss2
import os
import requests
from urllib.parse import urlparse
from config import config
from utils.logger import logger


class ImageProcessor:
    """
    图片处理器，负责将图片上传到阿里云OSS
    """

    def __init__(self):
        auth = oss2.Auth(config.aliyun_oss_ak, config.aliyun_oss_sk)
        self.bucket = oss2.Bucket(auth, f'https://{config.aliyun_oss_endpoint}', config.aliyun_oss_bucket_id)

    def upload_images(self, image_urls: list, platform: str, article_id: str) -> dict:
        """
        批量上传图片到OSS，按 article-001.jpg, article-002.jpg... 命名

        Args:
            image_urls (list): 图片URL列表
            platform (str): 平台标识符 (wechat, xhs, douban, zhihu)
            article_id (str): 文章唯一标识

        Returns:
            dict: 原始URL到OSS URL的映射字典
        """
        url_mapping = {}

        # 平台 Referer 映射（防盗链图片需要设置 Referer）
        platform_referers = {
            'douban': 'https://www.douban.com/',
            'zhihu': 'https://www.zhihu.com/',
            'wechat': 'https://mp.weixin.qq.com/',
            'xhs': 'https://www.xiaohongshu.com/',
        }
        headers = {'Referer': platform_referers.get(platform, '')}

        for idx, img_url in enumerate(image_urls, start=1):
            try:
                # 解析原始图片URL，获取文件扩展名
                parsed_url = urlparse(img_url)
                ext = os.path.splitext(parsed_url.path)[1]
                if not ext:
                    ext = '.jpg'

                # 按 article-001.jpg 格式命名
                oss_filename = f"article-{idx:03d}{ext}"
                oss_path = f"articles/{platform}/{article_id}/{oss_filename}"

                # 下载图片内容（带 Referer 绕过防盗链）
                response = requests.get(img_url, headers=headers, timeout=30)
                response.raise_for_status()

                # 上传到OSS
                result = self.bucket.put_object(oss_path, response.content)

                if result.status == 200:
                    oss_url = f"https://{config.aliyun_oss_bucket_id}.{config.aliyun_oss_endpoint}/{oss_path}"
                    url_mapping[img_url] = oss_url
                    logger.debug(f"图片上传成功 [{idx}/{len(image_urls)}]: {oss_filename}")
                else:
                    logger.warning(f"图片上传失败 [{idx}]: {img_url}, 状态码: {result.status}")

            except Exception as e:
                logger.warning(f"图片上传失败 [{idx}]: {img_url}, 错误: {str(e)}")
                continue

        return url_mapping
