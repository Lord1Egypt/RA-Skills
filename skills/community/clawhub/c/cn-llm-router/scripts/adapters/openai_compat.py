"""OpenAI 兼容适配器：覆盖 DeepSeek / 通义 / 智谱 / Kimi / 混元 / 豆包 /
MiniMax / 零一万物 Yi / 百川 / 阶跃星辰 Step 等厂商。

以上厂商均提供 OpenAI 格式的 /chat/completions 端点，统一用 Bearer Token 调用，
因此一个适配器（纯标准库 urllib）即可复用于所有 OpenAI 兼容厂商，零额外依赖；
新增同类厂商时只需在 models.yaml 增配 base_url + env_hint，无需改动本文件。
"""

import json
from .base import AdapterBase, AdapterError, http_post_json, _short, _estimate_tokens


class OpenAICompatAdapter(AdapterBase):
    adapter_type = "openai_compat"

    def chat(self, messages, model, stream=False, timeout=60):
        base_url = self.cfg.get("base_url")
        api_key = self.cfg.get("api_key")
        if not base_url:
            raise AdapterError("缺少 base_url，请检查 models.yaml 中该厂商配置")
        if not api_key:
            raise AdapterError(
                "未检测到 API Key（环境变量 %s）。请先配置后再调用。"
                % self.cfg.get("env_hint", "")
            )

        url = base_url.rstrip("/") + "/chat/completions"
        headers = {
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        }
        payload = {"model": model, "messages": messages, "stream": bool(stream)}

        if not stream:
            status, data = http_post_json(url, headers, payload, timeout)
            if status != 200:
                raise AdapterError("调用返回非 200: %s" % _short(data))
            if isinstance(data, str):
                raise AdapterError("响应非 JSON: %s" % _short(data))
            content = data["choices"][0]["message"]["content"]
            it, ot = self._extract_usage(data)
            return {"content": content, "in_tokens": it, "out_tokens": ot}
        else:
            return self._stream(url, headers, payload, timeout)

    def embed(self, texts, model=None, timeout=60):
        """文本向量嵌入（OpenAI 兼容 /embeddings 端点）。"""
        base_url = self.cfg.get("base_url")
        api_key = self.cfg.get("api_key")
        if not base_url or not api_key:
            raise AdapterError("缺少 base_url 或 api_key，无法调用 embedding")
        embed_model = model or self.cfg.get("default_embed_model", "text-embedding-3-small")
        url = base_url.rstrip("/") + "/embeddings"
        headers = {
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        }
        payload = {"model": embed_model, "input": texts}
        status, data = http_post_json(url, headers, payload, timeout)
        if status != 200:
            raise AdapterError("embedding 调用失败: %s" % _short(data))
        if isinstance(data, str):
            raise AdapterError("embedding 响应非 JSON: %s" % _short(data))
        embeddings = [item["embedding"] for item in data.get("data", [])]
        usage = data.get("usage", {})
        return {
            "embeddings": embeddings,
            "model": embed_model,
            "dim": len(embeddings[0]) if embeddings else 0,
            "tokens": usage.get("total_tokens", 0),
        }

    def rerank(self, query, documents, model=None, timeout=60):
        """文档重排序（OpenAI 兼容 /rerank 端点，部分厂商支持）。"""
        base_url = self.cfg.get("base_url")
        api_key = self.cfg.get("api_key")
        if not base_url or not api_key:
            raise AdapterError("缺少 base_url 或 api_key，无法调用 rerank")
        rerank_model = model or self.cfg.get("default_rerank_model", "bge-reranker-v2-m3")
        url = base_url.rstrip("/") + "/reranking"
        headers = {
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        }
        payload = {"model": rerank_model, "query": query, "documents": documents}
        status, data = http_post_json(url, headers, payload, timeout)
        if status != 200:
            raise AdapterError("rerank 调用失败: %s" % _short(data))
        if isinstance(data, str):
            raise AdapterError("rerank 响应非 JSON: %s" % _short(data))
        results = data.get("results", [])
        return {
            "results": results,
            "model": rerank_model,
        }

    def _stream(self, url, headers, payload, timeout):
        import urllib.request
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
        except Exception as e:
            raise AdapterError("流式请求失败: %s" % e)
        # 生成器：逐行解析 SSE
        def gen():
            buf = b""
            it = ot = 0
            full_content = []  # 累积完整文本，用于无 usage 时估算
            try:
                for raw in resp:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line or not line.startswith("data:"):
                        continue
                    chunk = line[len("data:"):].strip()
                    if chunk == "[DONE]":
                        break
                    try:
                        obj = json.loads(chunk)
                    except json.JSONDecodeError:
                        continue
                    delta = obj.get("choices", [{}])[0].get("delta", {})
                    text = delta.get("content") or ""
                    if text:
                        full_content.append(text)
                        yield text
                    u = obj.get("usage")
                    if u:
                        it, ot = self._extract_usage(obj)
                # 流式结束时，若厂商未返回 usage，用文本估算兜底并标注
                if ot == 0 and full_content:
                    ot = _estimate_tokens("".join(full_content))
                yield ""  # 结束哨兵
            except Exception as e:
                raise AdapterError("流式读取中断: %s" % e)
            finally:
                try:
                    resp.close()
                except Exception:
                    pass

        return gen()
