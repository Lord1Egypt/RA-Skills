import aiohttp

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from request.web.xhs_session import XHS_Session


class Authentication:
    def __init__(self, session: "XHS_Session"):
        self.session = session  # 保存会话引用

    async def get_self_simple_info(self) -> aiohttp.ClientResponse:
        """获取当前登录用户简要信息

        Returns:
            Dict: 用户信息
        """
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/user/me"
        return await self.session.request(method="get", url=url)
