"""
HTTP 客户端工具模块
提供带重试机制的 HTTP 请求功能
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import logger

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def create_session(retries: int = 3, timeout: int = 30) -> requests.Session:
    """
    创建带重试机制的 HTTP Session

    Args:
        retries (int): 重试次数
        timeout (int): 请求超时时间（秒）

    Returns:
        requests.Session: 配置好的 Session 对象
    """
    session = requests.Session()

    # 配置重试策略
    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,  # 重试间隔：1s, 2s, 4s...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # 设置默认请求头
    session.headers.update({
        'User-Agent': DEFAULT_USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    })

    logger.debug(f"创建 HTTP Session | 重试次数：{retries}, 超时：{timeout}s")

    return session

def get_with_retry(url: str, headers: dict = None, timeout: int = 30, retries: int = 3) -> requests.Response:
    """
    发送 GET 请求（带重试）

    Args:
        url (str): 请求 URL
        headers (dict): 自定义请求头
        timeout (int): 超时时间（秒）
        retries (int): 重试次数

    Returns:
        requests.Response: 响应对象

    Raises:
        requests.exceptions.RequestException: 请求失败
    """
    session = create_session(retries=retries, timeout=timeout)

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
    finally:
        session.close()
