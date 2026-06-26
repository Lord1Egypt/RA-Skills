"""Cookie 健康检查与过期告警模块"""

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CookieStatus:
    valid: bool
    last_check: str
    expires_in_days: int | None
    error_message: str | None = None


class CookieManager:
    """管理 B站 Cookie 的健康检查和过期提醒"""

    def __init__(self, env_path: Path | None = None):
        if env_path is None:
            env_path = Path(__file__).parent.parent / ".env"
        self.env_path = Path(env_path)
        self.cookies = self._load_cookies()

    def _load_cookies(self) -> dict:
        """从 .env 文件加载 Cookie"""
        cookies = {}
        if self.env_path.exists():
            for line in self.env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key == "BILIBILI_SESSDATA":
                        cookies["SESSDATA"] = value
                    elif key == "BILIBILI_BILI_JCT":
                        cookies["bili_jct"] = value
                    elif key == "BILIBILI_BUVID3":
                        cookies["buvid3"] = value
        return cookies

    def check_health(self) -> CookieStatus:
        """检查 Cookie 是否有效"""
        if not self.cookies.get("SESSDATA"):
            return CookieStatus(
                valid=False,
                last_check=datetime.now().isoformat(),
                expires_in_days=None,
                error_message="BILIBILI_SESSDATA 未配置或为空",
            )

        try:
            from .bilibili_api import BilibiliAPI

            api = BilibiliAPI(
                sessdata=self.cookies["SESSDATA"],
                bili_jct=self.cookies.get("bili_jct", ""),
                buvid3=self.cookies.get("buvid3", ""),
            )
            api.get_user_mid()
            return CookieStatus(
                valid=True,
                last_check=datetime.now().isoformat(),
                expires_in_days=None,
            )
        except Exception as e:
            error_msg = str(e)
            return CookieStatus(
                valid=False,
                last_check=datetime.now().isoformat(),
                expires_in_days=None,
                error_message=error_msg,
            )

    def warn_if_expiring(self) -> bool:
        """
        每次启动时调用。
        返回 True 表示正常，False 表示有问题（已打印警告后返回 False）。
        """
        status = self.check_health()
        if status.valid:
            return True

        print("=" * 55)
        print("  ⚠️  B站登录状态异常")
        print(f"  错误信息：{status.error_message}")
        print("=" * 55)
        print("  请重新获取 Cookie：")
        print("  1. 登录 https://www.bilibili.com")
        print("  2. 按 F12 打开开发者工具 → Application → Cookies → bilibili.com")
        print("  3. 复制 SESSDATA、BILI_JCT、BUVID3 的值")
        print("  4. 更新项目根目录的 .env 文件")
        print("=" * 55)
        return False

    def reload(self):
        """重新从 .env 加载 Cookie（用户手动更新后调用）"""
        self.cookies = self._load_cookies()
        return self.check_health()

    @property
    def is_configured(self) -> bool:
        """检查是否已配置 Cookie"""
        return bool(self.cookies.get("SESSDATA"))

    def get_api(self):
        """获取已配置 Cookie 的 BilibiliAPI 实例"""
        from .bilibili_api import BilibiliAPI

        return BilibiliAPI(
            sessdata=self.cookies.get("SESSDATA", ""),
            bili_jct=self.cookies.get("bili_jct", ""),
            buvid3=self.cookies.get("buvid3", ""),
        )
