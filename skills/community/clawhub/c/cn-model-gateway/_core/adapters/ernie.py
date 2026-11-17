"""文心（百度 ERNIE）适配器：推荐走 OpenAI 兼容通道，保留原生 OAuth2 兜底。

v2.5 精简：ernie 实际走 openai_compat 兼容通道，本类保留为薄封装。
- 优先走 Qianfan OpenAI 兼容端点（ERNIE_OPENAI_KEY）→ 直接委托 OpenAICompatAdapter
- 兜底走经典 OAuth2（ERNIE_API_KEY=AK + ERNIE_SECRET_KEY=SK）→ 原生签名路径
- 推荐用户配置 ERNIE_OPENAI_KEY，原生路径仅作向后兼容

models.yaml 中 ernie 可配置为：
  ernie:
    display: 百度文心
    adapter: openai_compat      # ← 推荐：走兼容通道
    base_url: https://qianfan.baidubce.com/v2
    env_hint: ERNIE_OPENAI_KEY
    ...

如需使用原生 OAuth2 路径，在 config 中保留 adapter: ernie 即可。
"""

import json
import urllib.parse
from .base import AdapterBase, AdapterError, http_post_json, _estimate_tokens
from .openai_compat import OpenAICompatAdapter


class ErnieAdapter(AdapterBase):
    adapter_type = "ernie"

    def chat(self, messages, model, stream=False, timeout=60):
        openai_key = self.cfg.get("api_key_openai")
        if openai_key:
            # 推荐路径：委托 OpenAICompatAdapter（零额外代码）
            sub = OpenAICompatAdapter({
                "base_url": self.cfg.get("base_url_openai") or "https://qianfan.baidubce.com/v2",
                "api_key": openai_key,
            })
            return sub.chat(messages, model, stream=stream, timeout=timeout)

        # 兼容路径：原生 OAuth2（仅作兜底，不推荐新用户使用）
        ak = self.cfg.get("ak")
        sk = self.cfg.get("sk")
        if not (ak and sk):
            raise AdapterError(
                "未检测到文心密钥。推荐设置 ERNIE_OPENAI_KEY（Qianfan 兼容），"
                "或同时设置 ERNIE_API_KEY(AK) 与 ERNIE_SECRET_KEY(SK)。"
            )
        token = self._get_token(ak, sk, timeout)
        endpoint = self.cfg.get("base_url")
        if not endpoint:
            raise AdapterError("缺少文心 chat 端点 base_url")
        url = endpoint.rstrip("/") + "?access_token=" + token

        headers = {"Content-Type": "application/json"}
        payload = {"messages": messages, "stream": bool(stream)}
        if model:
            payload["model"] = model

        if not stream:
            status, data = http_post_json(url, headers, payload, timeout)
            if status != 200:
                raise AdapterError("文心调用失败: %s" % str(data)[:300])
            result = data.get("result", "")
            it = int((data.get("usage") or {}).get("prompt_tokens", 0) or 0)
            ot = int((data.get("usage") or {}).get("completion_tokens", 0) or 0)
            return {"content": result, "in_tokens": it, "out_tokens": ot}
        else:
            return self._stream(url, headers, payload, timeout)

    def _get_token(self, ak, sk, timeout):
        token_url = (
            "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"
            "&client_id=%s&client_secret=%s" % (urllib.parse.quote(ak), urllib.parse.quote(sk))
        )
        import urllib.request
        req = urllib.request.Request(token_url, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8", "replace"))
        except Exception as e:
            raise AdapterError("获取文心 access_token 失败: %s" % e)
        if "access_token" not in body:
            raise AdapterError("文心鉴权失败（检查 AK/SK）: %s" % str(body)[:200])
        return body["access_token"]

    def _stream(self, url, headers, payload, timeout):
        import urllib.request
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
        except Exception as e:
            raise AdapterError("文心流式请求失败: %s" % e)

        def gen():
            try:
                full_content = []
                for raw in resp:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    text = obj.get("result") or ""
                    if text:
                        full_content.append(text)
                        yield text
                yield ""
                # 流式结束时若 usage 为空，用文本估算兜底（ernie 原生端点流式可能不返回 usage）
            except Exception as e:
                raise AdapterError("文心流式读取中断: %s" % e)
            finally:
                try:
                    resp.close()
                except Exception:
                    pass

        return gen()
