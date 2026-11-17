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

    def upload_images(self, image_urls: list, platform: str, article_id: str, article_url: str = '') -> dict:
        """
        批量上传图片到OSS，按 article-001.jpg, article-002.jpg... 命名

        Args:
            image_urls (list): 图片URL列表
            platform (str): 平台标识符 (wechat, xhs, douban, zhihu)
            article_id (str): 文章唯一标识
            article_url (str): 原文链接（用于动态生成 Referer，兼容第三方CDN）

        Returns:
            dict: 原始URL到OSS URL的映射字典
        """
        url_mapping = {}

        # 平台 Referer（仅作回退用）
        platform_referer = self._build_referer(article_url, platform)

        for idx, img_url in enumerate(image_urls, start=1):
            try:
                parsed_url = urlparse(img_url)
                ext = os.path.splitext(parsed_url.path)[1]
                if not ext:
                    ext = '.jpg'

                oss_filename = f"article-{idx:03d}{ext}"
                oss_path = f"articles/{platform}/{article_id}/{oss_filename}"

                # 下载：优先空 Referer，403 时降级回退平台 Referer
                response = self._download_image(img_url, platform_referer)

                result = self.bucket.put_object(oss_path, response.content)

                if result.status == 200:
                    endpoint = config.aliyun_oss_endpoint.lstrip('https://').lstrip('http://')
                    oss_url = f"https://{config.aliyun_oss_bucket_id}.{endpoint}/{oss_path}"
                    url_mapping[img_url] = oss_url
                    logger.debug(f"图片上传成功 [{idx}/{len(image_urls)}]: {oss_filename}")
                else:
                    logger.warning(f"图片上传失败 [{idx}]: {img_url}, 状态码: {result.status}")

            except Exception as e:
                logger.warning(f"图片上传失败 [{idx}]: {img_url}, 错误: {str(e)}")
                continue

        return url_mapping

    @staticmethod
    def _download_image(img_url: str, fallback_referer: str):
        """下载图片：空 Referer 优先，403 时回退平台 Referer"""
        # ① 空 Referer
        try:
            resp = requests.get(img_url, timeout=30)
            if resp.status_code != 403:
                resp.raise_for_status()
                return resp
        except requests.HTTPError:
            pass

        # ② 回退：平台 Referer
        if fallback_referer:
            logger.debug(f"空 Referer 失败，回退平台 Referer: {fallback_referer}")
            resp = requests.get(img_url, headers={'Referer': fallback_referer}, timeout=30)
            resp.raise_for_status()
            return resp

        raise RuntimeError(f"图片下载失败: {img_url}")

    @staticmethod
    def _build_referer(article_url: str, platform: str) -> str:
        """构建 Referer：优先从原文链接动态提取，回退平台默认值"""
        if article_url:
            parsed = urlparse(article_url)
            return f"{parsed.scheme}://{parsed.hostname}/"

        # 平台默认值
        platform_referers = {
            'douban': 'https://www.douban.com/',
            'zhihu': 'https://www.zhihu.com/',
            'wechat': 'https://mp.weixin.qq.com/',
            'xhs': 'https://www.xiaohongshu.com/',
        }
        return platform_referers.get(platform, '')
