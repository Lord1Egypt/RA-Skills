from __future__ import annotations

from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "utm_id",
    "gclid",
    "fbclid",
    "mc_cid",
    "mc_eid",
    "spm",
    "from",
    "ref",
    "ref_src",
}


def normalize_url(url: str | None) -> str:
    """
    归一化 URL，尽量把“同一链接不同写法”收敛成一个形式。
    """
    if not url:
        return ""

    url = url.strip()
    if not url:
        return ""

    try:
        parsed = urlparse(url)

        scheme = (parsed.scheme or "https").lower()
        netloc = parsed.netloc.lower()

        # 去掉默认端口
        if netloc.endswith(":80") and scheme == "http":
            netloc = netloc[:-3]
        if netloc.endswith(":443") and scheme == "https":
            netloc = netloc[:-4]

        # path 去尾部斜杠（根路径除外）
        path = parsed.path or ""
        if path != "/" and path.endswith("/"):
            path = path[:-1]

        # 去 tracking query 参数，并按 key 排序
        query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
        filtered_pairs = [
            (k, v) for k, v in query_pairs
            if k.lower() not in TRACKING_PARAMS
        ]
        filtered_pairs.sort(key=lambda x: (x[0], x[1]))
        query = urlencode(filtered_pairs, doseq=True)

        # fragment 去掉
        fragment = ""

        normalized = urlunparse((scheme, netloc, path, "", query, fragment))
        return normalized
    except Exception:
        return url