"""
配置管理
"""
import os
from dotenv import load_dotenv

load_dotenv()


class ConfigManager:
    """集中管理所有环境变量"""

    def __init__(self):
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'

        # 阿里云 OSS
        self.aliyun_oss_ak = os.getenv('ALIYUN_OSS_AK')
        self.aliyun_oss_sk = os.getenv('ALIYUN_OSS_SK')
        self.aliyun_oss_bucket_id = os.getenv('ALIYUN_OSS_BUCKET_ID')
        self.aliyun_oss_endpoint = os.getenv('ALIYUN_OSS_ENDPOINT')

        # Notion
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        self.notion_article_database_id = os.getenv('NOTION_ARTICLE_DATABASE_ID')

        # LLM 关键词提取（OpenAI 兼容接口，复用 video-summarizer 配置）
        self.llm_api_key = os.getenv('LLM_API_KEY', '').strip()
        self.llm_base_url = os.getenv('LLM_BASE_URL', '').strip()
        self.llm_model = os.getenv('LLM_MODEL', '').strip()

        # LLM 可用性标记
        self.llm_available = bool(self.llm_api_key and self.llm_base_url and self.llm_model)

        # 可选：Cookies（默认路径 ~/.cookies/<platform>_cookies.txt）
        self.wechat_cookies = os.getenv('WECHAT_COOKIES_FILE', os.path.expanduser('~/.cookies/wechat_cookies.txt'))
        self.zhihu_cookies = os.getenv('ZHIHU_COOKIES_FILE', os.path.expanduser('~/.cookies/zhihu_cookies.txt'))

        self._validate()

    def _validate(self):
        required = [
            ('ALIYUN_OSS_AK', self.aliyun_oss_ak),
            ('ALIYUN_OSS_SK', self.aliyun_oss_sk),
            ('ALIYUN_OSS_BUCKET_ID', self.aliyun_oss_bucket_id),
            ('ALIYUN_OSS_ENDPOINT', self.aliyun_oss_endpoint),
            ('NOTION_API_KEY', self.notion_api_key),
            ('NOTION_ARTICLE_DATABASE_ID', self.notion_article_database_id),
        ]
        missing = [name for name, val in required if not val]
        if missing:
            raise ValueError(f"缺少必要的环境变量：{', '.join(missing)}")


config = ConfigManager()
