"""
HTTP 客户端工具模块
提供带重试机制的 HTTP 请求功能（Session 单例复用 TCP 连接）
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import logger

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# 模块级 Session 单例，复用 TCP 连接
_shared_session = None


def _get_shared_session() -> requests.Session:
    """获取或创建模块级共享 Session（懒初始化）"""
    global _shared_session
    if _shared_session is None:
        _shared_session = requests.Session()
        _shared_session.headers.update({
            'User-Agent': DEFAULT_USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
        _shared_session.mount("https://", adapter)
        _shared_session.mount("http://", adapter)
    return _shared_session


def get_with_retry(url: str, headers: dict = None, timeout: int = 30) -> requests.Response:
    """
    发送 GET 请求（带重试，复用 Session 连接池）

    Args:
        url (str): 请求 URL
        headers (dict): 自定义请求头
        timeout (int): 超时时间（秒）

    Returns:
        requests.Response: 响应对象

    Raises:
        requests.exceptions.RequestException: 请求失败
    """
    session = _get_shared_session()

    # 每次请求前重置 session 级别 headers 为默认值
    session.headers.update({
        'User-Agent': DEFAULT_USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    # 清除之前可能残留的 Cookie / Referer
    session.headers.pop('Cookie', None)
    session.headers.pop('Referer', None)

    if headers:
        session.headers.update(headers)

    logger.info(f"GET {url}")

    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        logger.debug(f"响应状态码：{response.status_code}")
        return response
    except requests.exceptions.Timeout:
        logger.error(f"请求超时：{url}")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP 错误：{e.response.status_code} - {url}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败：{str(e)}")
        raise
