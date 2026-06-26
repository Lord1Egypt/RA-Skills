"""稳健 sina 抓取工具 — 多 UA 轮换 + 5s 退避 + 多次重试

(2026-06-17 立) 解决新浪 hq.sinajs.cn 升级反爬导致 403 的问题。
背景: 2026-06-17 实测发现短 UA "Mozilla/5.0" 会被识别为爬虫, 必须用完整浏览器 UA 字符串。
可靠性数据 (2026-06-17 实测):
  - 短 UA + Referer: 1/3 成功 (不可靠)
  - 完整 UA + Referer: 3/3 成功

使用示例:
    from _sina_fetcher import fetch_sina, sina_get_vix
    body = fetch_sina("sh000300")  # 自动拼 https://hq.sinajs.cn/list=sh000300
    body = fetch_sina("https://hq.sinajs.cn/list=sh000300,sz399001")  # 多字段
    vix = sina_get_vix()  # VIX 专用便捷函数
"""
import urllib.request
import urllib.error
import random
import time
import re
import logging

logger = logging.getLogger(__name__)

# 5 个真实浏览器 UA (2026-06-17 选自 Chrome / Safari / Firefox 主流版本)
UA_POOL = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

REFERER = "https://finance.sina.com.cn/"

# 2026-06-17 设定: delay 5s+, 多次尝试
DEFAULT_RETRIES = 3
DEFAULT_BASE_DELAY = 5.0  # 5 秒 (延迟时长上限)
DEFAULT_TIMEOUT = 8


def fetch_sina(url_or_code, retries=DEFAULT_RETRIES, base_delay=DEFAULT_BASE_DELAY, timeout=DEFAULT_TIMEOUT):
    """稳健 sina 抓取: 多 UA 轮换 + 指数退避 + 多次重试

    Args:
        url_or_code: "sh000300" 自动拼成 https://hq.sinajs.cn/list=sh000300
                     或完整 URL "https://hq.sinajs.cn/list=sh000300,sz399001"
        retries: 重试次数 (默认 3)
        base_delay: 基础退避秒数 (默认 5s, 延迟时长上限)
        timeout: 单次超时秒数 (默认 8s)

    Returns:
        bytes: 原始响应 body (GBK 编码, 需 .decode("gbk", errors="replace"))

    Raises:
        RuntimeError: 全部重试都失败时
    """
    url = url_or_code if url_or_code.startswith("http") else f"https://hq.sinajs.cn/list={url_or_code}"

    last_err = None
    for attempt in range(retries):
        ua = random.choice(UA_POOL)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Referer": REFERER})
            body = urllib.request.urlopen(req, timeout=timeout).read()
            if attempt > 0:
                logger.info(f"[sina_fetcher] 第 {attempt+1} 次重试成功: {url_or_code}")
            return body
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code} {e.reason}"
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"

        # 退避: 第 N 次失败后等 base_delay * 2^N + 随机抖动
        if attempt < retries - 1:
            delay = base_delay * (2 ** attempt) + random.uniform(0, base_delay * 0.5)
            logger.warning(f"[sina_fetcher] 第 {attempt+1} 次失败 ({last_err}), {delay:.1f}s 后重试: {url_or_code}")
            time.sleep(delay)

    raise RuntimeError(f"sina 抓取失败 {retries} 次: {url_or_code} (最后错误: {last_err})")


def sina_get_vix(retries=DEFAULT_RETRIES, base_delay=DEFAULT_BASE_DELAY):
    """便捷函数: 抓 VIX 数据 (新浪 znb_VIX 字段)

    Returns:
        dict: {"value": float, "pct": float, "level": str, "source": str}
               失败时返回空 dict {}
    """
    result = {}
    try:
        body = fetch_sina("znb_VIX", retries=retries, base_delay=base_delay).decode("gbk", errors="replace")
        # 13 字段: 名称,现价,涨跌点,涨跌幅%,昨收,今开,日期,时间,52周高,52周低,成交量,成交额,时间戳
        m = re.search(r'"([^"]+)"', body)
        if m:
            fields = m.group(1).split(",")
            if len(fields) >= 4 and fields[1] and fields[1] != "0.0000":
                vix_val = round(float(fields[1]), 2)
                pct = round(float(fields[3]), 2)
                # 等级: <20 低位, 20-30 中位, >30 高位
                if vix_val < 20:
                    level = "低位"
                elif vix_val <= 30:
                    level = "中位"
                else:
                    level = "高位"
                result = {
                    "value": vix_val,
                    "pct": pct,
                    "level": level,
                    "source": "新浪-VIX"
                }
    except Exception as e:
        logger.warning(f"[sina_get_vix] 失败: {e}")
    return result
