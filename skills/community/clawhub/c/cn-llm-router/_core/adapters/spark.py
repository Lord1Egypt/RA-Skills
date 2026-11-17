"""讯飞星火适配器：WebSocket 协议（官方仅提供 WS 接入）。

标准库没有 WebSocket 客户端，本适配器在调用时按需 import 可选的 `websocket-client`
包做传输，而**签名用纯标准库（hmac / hashlib / base64）自研**，不依赖任何签名库。
若未安装 websocket-client，给出清晰中文指引，绝不静默失败。

可选依赖安装（用户自行决定，非核心依赖）：pip install websocket-client
其余 7 家厂商（DeepSeek / 通义 / 智谱 / Kimi / 混元 / 豆包 / 文心）均为纯标准库，无需此依赖。
"""

import base64
import hashlib
import hmac
import json
import time
import urllib.parse
from datetime import datetime, timezone

from .base import AdapterBase, AdapterError


# 不同版本对应的 host / path
SPARK_ENDPOINTS = {
    "v3.1": ("spark-api.xf-yun.com", "/v3.1/chat"),
    "v3.5": ("spark-api.xf-yun.com", "/v3.5/chat"),
    "v4.0": ("spark-api.xf-yun.com", "/v4.0/chat"),
}


def _build_ws_url(host, path, api_key, api_secret):
    """按讯飞规范构造带鉴权的 wss URL（纯标准库签名）。"""
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %Z")
    # 时区字段讯飞要求 GMT，替换 UTC→GMT
    now = now.replace("UTC", "GMT")
    signature_origin = "host: %s\ndate: %s\nGET %s HTTP/1.1" % (host, now, path)
    signature_sha = hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    signature = base64.b64encode(signature_sha).decode("utf-8")
    auth_origin = (
        'api_key="%s", algorithm="hmac-sha256", headers="host date request-line", signature="%s"'
        % (api_key, signature)
    )
    return (
        "wss://%s%s?authorization=%s&date=%s&host=%s"
        % (
            host,
            path,
            urllib.parse.quote(auth_origin, safe=""),
            urllib.parse.quote(now, safe=""),
            host,
        )
    )


class SparkAdapter(AdapterBase):
    adapter_type = "spark"

    def chat(self, messages, model, stream=False, timeout=60):
        app_id = self.cfg.get("app_id")
        api_key = self.cfg.get("api_key")
        api_secret = self.cfg.get("api_secret")
        if not (app_id and api_key and api_secret):
            raise AdapterError(
                "未检测到讯飞星火密钥。请设置 SPARK_APP_ID / SPARK_API_KEY / SPARK_API_SECRET 三个环境变量。"
            )
        try:
            import websocket  # websocket-client
        except ImportError:
            raise AdapterError(
                "讯飞星火需要可选依赖 websocket-client（其余厂商无需此依赖）。"
                "请运行 `pip install websocket-client` 后重试；"
                "若不想装依赖，可改用通义 / 智谱 / DeepSeek 等纯标准库支持的厂商。"
            )

        version = self.cfg.get("version", "v3.5")
        if version not in SPARK_ENDPOINTS:
            version = "v3.5"
        host, path = SPARK_ENDPOINTS[version]
        ws_url = _build_ws_url(host, path, api_key, api_secret)

        # 将 OpenAI messages 转为讯飞 payload 文本（拼接多轮）
        text_parts = []
        for m in messages:
            role = m.get("role")
            content = m.get("content", "")
            if role == "system":
                text_parts.append("系统设定：" + content)
            else:
                text_parts.append(content)
        prompt_text = "\n".join(text_parts)

        frame = {
            "header": {"app_id": app_id, "uid": "cn-llm-router"},
            "parameter": {
                "chat": {
                    "domain": self.cfg.get("domain", "generalv3.5"),
                    "temperature": 0.7,
                    "max_tokens": 2048,
                }
            },
            "payload": {"message": {"text": [{"role": "user", "content": prompt_text}]}},
        }

        result = self._ws_chat(ws_url, frame, timeout)
        if not stream:
            return result
        # 讯飞 WS 不提供逐字流式，兼容上层协议：把完整结果作为单段生成器返回
        def gen():
            yield result["content"]
            yield ""
        return gen()

    def _ws_chat(self, ws_url, frame, timeout):
        result_text = []
        it = ot = 0
        try:
            ws = websocket.create_connection(ws_url, timeout=timeout)
            ws.send(json.dumps(frame))
            while True:
                raw = ws.recv()
                if not raw:
                    continue
                obj = json.loads(raw)
                code = obj.get("header", {}).get("code")
                if code != 0:
                    raise AdapterError("讯飞返回错误码 %s: %s" % (code, obj.get("header", {}).get("message")))
                text = obj.get("payload", {}).get("choices", {}).get("text", [{}])[0].get("content", "")
                if text:
                    result_text.append(text)
                usage = obj.get("payload", {}).get("usage", {}).get("text", {})
                it = int(usage.get("prompt_tokens", it))
                ot = int(usage.get("completion_tokens", ot))
                if obj.get("header", {}).get("status") == 2:
                    break
            ws.close()
        except AdapterError:
            raise
        except Exception as e:
            raise AdapterError("讯飞星火 WebSocket 通信失败: %s" % e)
        return {"content": "".join(result_text), "in_tokens": it, "out_tokens": ot}
