"""适配器基类：统一 chat() 接口，归一请求 / 响应 / 错误 / 重试 / 限流。

所有适配器：
- 只通过 https 调用，设置超时，失败后抛 AdapterError（中文）。
- 响应统一返回 dict：{ "content": str, "in_tokens": int, "out_tokens": int }
- 流式：yield 文本片段（生成器）。
- 密钥仅从环境变量读取，绝不落盘。
"""

import time
import json
import re
import urllib.request
import urllib.error


class AdapterError(Exception):
    """所有适配器错误的统一类型（中文提示）。"""


class AdapterTimeoutError(AdapterError):
    """调用超时错误（用于触发故障转移，与鉴权/限流等错误区分）。"""

    def __init__(self, provider, model, timeout_sec, cause=None):
        self.provider = provider
        self.model = model
        self.timeout_sec = timeout_sec
        self.cause = cause
        msg = "调用超时（%s / %s，%ds），模型可能过载或网络不畅" % (provider, model, timeout_sec)
        super().__init__(msg)


def http_post_json(url, headers, payload, timeout=60):
    """发送 JSON POST，返回 (status_code, parsed_json_or_text)。"""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace")
            try:
                return resp.status, json.loads(body)
            except json.JSONDecodeError:
                return resp.status, body
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise AdapterError("HTTP %s 调用失败: %s" % (e.code, _short(detail)))
    except urllib.error.URLError as e:
        raise AdapterError("网络错误（无法连接 %s）: %s" % (url, e.reason))
    except TimeoutError:
        raise AdapterError("请求超时（%s 秒），模型可能过载或网络不畅" % timeout)


def _short(text, n=300):
    text = (text or "").replace("\n", " ")
    return text[:n] + ("…" if len(text) > n else "")


def _estimate_tokens(text):
    """根据文本粗略估算 token 数（用于流式输出无 usage 字段时的兜底）。
    规则：中文/全角字符 ≈ 1.5 tokens/字，英文单词 ≈ 1.3 tokens/词，标点/空白折半。
    """
    if not text:
        return 0
    cn_chars = len(re.findall(r"[\u4e00-\u9fff\uff00-\uffef]", text))
    en_matches = re.findall(r"[a-zA-Z]+", text)
    en_words = len(en_matches)
    en_chars = sum(len(m) for m in en_matches)  # 英文字符总长度（用于计算 other）
    other = len(text) - cn_chars - en_chars
    return int(cn_chars * 1.5 + en_words * 1.3 + other * 0.5)


class AdapterBase:
    adapter_type = "base"

    def __init__(self, provider_cfg):
        # provider_cfg: models.yaml 中该厂商的配置片段
        self.cfg = provider_cfg or {}

    def chat(self, messages, model, stream=False, timeout=60):
        raise NotImplementedError

    def embed(self, texts, model=None, timeout=60):
        """文本向量嵌入。子类实现，不支持的厂商抛 NotImplementedError。"""
        raise NotImplementedError("该适配器不支持 embedding")

    def rerank(self, query, documents, model=None, timeout=60):
        """文档重排序。子类实现，不支持的厂商抛 NotImplementedError。"""
        raise NotImplementedError("该适配器不支持 rerank")

    def _extract_usage(self, data):
        """从响应里取 token 用量，兼容多种字段名。"""
        usage = (data or {}).get("usage") or {}
        it = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
        ot = usage.get("completion_tokens") or usage.get("output_tokens") or 0
        return int(it), int(ot)

    def _retry(self, func, max_retries=2, backoff=1.5):
        """简单指数退避重试（应对 429 / 临时 5xx）。"""
        last = None
        for i in range(max_retries + 1):
            try:
                return func()
            except AdapterError as e:
                last = e
                msg = str(e)
                if "429" in msg or "500" in msg or "502" in msg or "503" in msg:
                    if i < max_retries:
                        time.sleep(backoff * (i + 1))
                        continue
                raise
        raise last
