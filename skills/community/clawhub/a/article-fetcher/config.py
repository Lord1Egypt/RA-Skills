"""
配置管理
"""
import os
from dotenv import load_dotenv

# .env 加载策略：$AGENT_HOME > $HERMES_HOME > 当前目录
_agent_home = os.getenv('AGENT_HOME', os.getenv('HERMES_HOME', ''))
if _agent_home:
    load_dotenv(os.path.join(_agent_home, '.env'))
else:
    load_dotenv()


class ConfigManager:
    """集中管理所有环境变量"""

    def __init__(self):
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'

        # 阿里云 OSS（必需）
        self.aliyun_oss_ak = os.getenv('ALIYUN_OSS_AK')
        self.aliyun_oss_sk = os.getenv('ALIYUN_OSS_SK')
        self.aliyun_oss_bucket_id = os.getenv('ALIYUN_OSS_BUCKET_ID')
        self.aliyun_oss_endpoint = os.getenv('ALIYUN_OSS_ENDPOINT')

        # Obsidian 本地存档（推荐，默认适配知识库路径）
        self.obsidian_vault_path = os.getenv(
            'OBSIDIAN_VAULT_PATH',
            os.path.expanduser('D:/GitRepo/AjayObsidianVault')
        ).rstrip('/\\')

        # Notion 云端存档（可选）
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        self.notion_article_database_id = os.getenv('NOTION_ARTICLE_DATABASE_ID')

        # LLM 关键词提取（OpenAI 兼容接口，复用 video-summarizer 配置）
        self.llm_api_key = os.getenv('LLM_API_KEY', '').strip()
        self.llm_base_url = os.getenv('LLM_BASE_URL', '').strip()
        self.llm_model = os.getenv('LLM_MODEL', '').strip()

        # 可选：Cookies（默认路径 ~/.cookies/<platform>_cookies.txt）
        self.wechat_cookies = os.getenv('WECHAT_COOKIES_FILE', os.path.expanduser('~/.cookies/wechat_cookies.txt'))
        self.zhihu_cookies = os.getenv('ZHIHU_COOKIES_FILE', os.path.expanduser('~/.cookies/zhihu_cookies.txt'))

        self._validate()

    @property
    def obsidian_available(self) -> bool:
        """Obsidian 存档是否可用（路径存在即可）"""
        return bool(self.obsidian_vault_path and os.path.isdir(self.obsidian_vault_path))

    @property
    def notion_available(self) -> bool:
        """Notion 存档是否可用（需 API Key + Database ID）"""
        return bool(self.notion_api_key and self.notion_article_database_id)

    @property
    def llm_available(self) -> bool:
        """LLM 关键词提取是否可用"""
        return bool(self.llm_api_key and self.llm_base_url and self.llm_model)

    @property
    def archive_available(self) -> bool:
        """至少有一种存档方式可用"""
        return self.obsidian_available or self.notion_available

    def _validate(self):
        """仅校验 OSS（必需），Notion/Obsidian 为可选"""
        required = [
            ('ALIYUN_OSS_AK', self.aliyun_oss_ak),
            ('ALIYUN_OSS_SK', self.aliyun_oss_sk),
            ('ALIYUN_OSS_BUCKET_ID', self.aliyun_oss_bucket_id),
            ('ALIYUN_OSS_ENDPOINT', self.aliyun_oss_endpoint),
        ]
        missing = [name for name, val in required if not val]
        if missing:
            raise ValueError(f"缺少必要的环境变量：{', '.join(missing)}")


config = ConfigManager()
