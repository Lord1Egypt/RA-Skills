from urllib.parse import urlparse
from typing import Optional

# 平台 → 允许的域名（严格白名单，拒绝路径拼接攻击）
ALLOWED_HOSTS = {
    'wechat': {'mp.weixin.qq.com', 'weixin.qq.com'},
    'xhs': {'www.xiaohongshu.com', 'xhslink.com', 'www.xhslink.com'},
    'douban': {'www.douban.com', 'm.douban.com', 'douban.com'},
    'zhihu': {'www.zhihu.com', 'zhuanlan.zhihu.com', 'zhihu.com'},
}


def detect_platform(url: str) -> Optional[str]:
    """
    根据URL识别文章所属平台

    安全策略：严格校验 hostname，拒绝路径中包含平台域名的恶意 URL。

    Args:
        url (str): 文章链接

    Returns:
        Optional[str]: 平台标识符 (wechat, xhs, douban, zhihu) 或 None
    """
    if not url:
        return None

    try:
        parsed = urlparse(url)
    except Exception:
        return None

    hostname = parsed.hostname
    if not hostname:
        return None

    hostname = hostname.lower()

    # 白名单匹配
    for platform, hosts in ALLOWED_HOSTS.items():
        if hostname in hosts:
            return platform

    return None