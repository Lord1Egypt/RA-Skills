"""配置管理 — 从环境变量和.env文件加载配置"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(_env_path)


class Config:
    # B站Cookie（必填）
    BILIBILI_SESSDATA: str = os.getenv("BILIBILI_SESSDATA", "")
    BILIBILI_BILI_JCT: str = os.getenv("BILIBILI_BILI_JCT", "")
    BILIBILI_BUVID3: str = os.getenv("BILIBILI_BUVID3", "")

    # 输出目录
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "./output"))

    # 数据目录
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "./data"))

    # 评论和弹幕数量限制
    MAX_COMMENTS: int = int(os.getenv("MAX_COMMENTS", "10"))
    MAX_DANMAKUS: int = int(os.getenv("MAX_DANMAKUS", "50"))

    # 推送配置
    DELIVERY_PLATFORM: str = os.getenv("DELIVERY_PLATFORM", "none")  # wechat/feishu/telegram/discord/slack/whatsapp/none

    @classmethod
    def validate(cls) -> list[str]:
        """验证必填配置项，返回缺失项列表"""
        missing = []
        if not cls.BILIBILI_SESSDATA:
            missing.append("BILIBILI_SESSDATA")
        if not cls.BILIBILI_BILI_JCT:
            missing.append("BILIBILI_BILI_JCT")
        if not cls.BILIBILI_BUVID3:
            missing.append("BILIBILI_BUVID3")
        return missing

    @classmethod
    def ensure_dirs(cls):
        """确保输出和数据目录存在"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
