#!/usr/bin/env python3
"""
腾讯混元大模型 (Hunyuan) 客户端封装。

调用 ChatCompletions 接口（非流式），默认使用 hunyuan-lite 模型。
统一输出文本内容，并对常见错误（未开通服务、欠费、资源包耗尽等）给出明确指引。

用法：
    from llm_client import HunyuanClient
    client = HunyuanClient(model="hunyuan-lite")
    reply = client.chat([
        {"Role": "system", "Content": "..."},
        {"Role": "user", "Content": "..."},
    ])
"""

import json
import os
import subprocess
import sys

from env_loader import validate_env

HUNYUAN_ENDPOINT = "hunyuan.tencentcloudapi.com"
DEFAULT_MODEL = "hunyuan-lite"
MAX_RETRY = 2


def ensure_dependencies():
    """确保 tencentcloud-sdk-python-hunyuan 已安装，缺失时自动安装。"""
    try:
        from tencentcloud.hunyuan.v20230901 import hunyuan_client, models  # noqa: F401
    except (ImportError, ModuleNotFoundError):
        print("[INFO] tencentcloud-sdk-python-hunyuan 未安装，正在安装...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "tencentcloud-sdk-python-hunyuan", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] 依赖安装完成。", file=sys.stderr)


class HunyuanClient:
    """腾讯混元大模型非流式对话客户端。"""

    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 0.7, max_tokens: int = 4096):
        ensure_dependencies()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None

    def _get_client(self):
        """懒加载混元客户端。"""
        if self._client is not None:
            return self._client
        secret_id, secret_key = validate_env()

        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.hunyuan.v20230901 import hunyuan_client

        cred = credential.Credential(secret_id, secret_key)
        http_profile = HttpProfile()
        http_profile.endpoint = HUNYUAN_ENDPOINT
        http_profile.reqTimeout = 120
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        self._client = hunyuan_client.HunyuanClient(cred, "", client_profile)
        return self._client

    def chat(self, messages: list, model: str = None) -> str:
        """
        调用混元 ChatCompletions（非流式）。

        messages: [{"Role": "system"|"user"|"assistant", "Content": "..."}]
        返回: 模型回复文本。
        失败时抛出 RuntimeError（已带用户可读的中文错误说明）。
        """
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
            TencentCloudSDKException,
        )
        from tencentcloud.hunyuan.v20230901 import models

        client = self._get_client()
        req = models.ChatCompletionsRequest()
        params = {
            "Model": model or self.model,
            "Messages": messages,
            "Stream": False,
            "Temperature": self.temperature,
        }
        req.from_json_string(json.dumps(params))

        last_err = None
        for attempt in range(MAX_RETRY + 1):
            try:
                resp = client.ChatCompletions(req)
                resp_json = json.loads(resp.to_json_string())
                choices = resp_json.get("Choices", [])
                if not choices:
                    raise RuntimeError("模型未返回内容（Choices 为空）。")
                content = choices[0].get("Message", {}).get("Content", "")
                if not content:
                    raise RuntimeError("模型回复内容为空。")
                return content
            except TencentCloudSDKException as e:
                last_err = self._friendly_error(e)
                if attempt < MAX_RETRY:
                    continue
            except RuntimeError:
                raise
            except Exception as e:  # noqa: BLE001
                last_err = f"调用混元大模型失败: {e}"
                if attempt < MAX_RETRY:
                    continue
        raise RuntimeError(last_err or "调用混元大模型失败。")

    @staticmethod
    def _friendly_error(e) -> str:
        """将腾讯云 SDK 异常转换为用户可读的中文说明。"""
        code = getattr(e, "code", "") or ""
        message = getattr(e, "message", "") or ""
        guide = ""

        if "UnauthorizedOperation" in code:
            guide = (
                "子账号权限不足。请在 CAM 策略中为当前账号授予混元服务权限，"
                "或使用主账号密钥：https://console.cloud.tencent.com/cam/capi"
            )
        elif "UnsupportedOperation" in code or "UnOpenError" in code or "not opened" in message.lower():
            guide = (
                "混元大模型服务尚未开通。请前往控制台开通：\n"
                "  https://console.cloud.tencent.com/hunyuan\n"
                "开通后在 [密钥管理] 确认 SecretId/SecretKey 可用。"
            )
        elif "ResourcePackExhausted" in code or "ResourceInsufficient" in code:
            guide = "资源包余量用尽或资源不足。请在混元控制台购买/充值资源包。"
        elif "ServiceStopArrears" in code or "InvalidCredential" in code:
            guide = "账号欠费或凭证无效，请检查账户余额与密钥状态。"
        elif "FailedOperation" in code:
            guide = "服务内部错误，请稍后重试；若持续失败请检查控制台服务状态。"

        return f"混元大模型调用失败 [{code}]: {message}\n{guide}".strip()


def extract_json(text: str) -> dict:
    """
    从模型回复中稳健提取 JSON 对象。

    优先尝试整体解析；失败则截取首个 { 到最后一个 } 之间的内容再解析。
    """
    if not text:
        raise ValueError("模型回复为空，无法解析 JSON。")
    try:
        return json.loads(text)
    except (ValueError, json.JSONDecodeError):
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"模型回复中未找到 JSON 对象。原始回复:\n{text[:500]}")

    candidate = text[start : end + 1]
    try:
        return json.loads(candidate)
    except (ValueError, json.JSONDecodeError):
        # 兼容 markdown 代码块 ```json ... ``` 包裹
        if "```" in text:
            block = text.split("```")
            for part in block:
                cleaned = part.strip()
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:].strip()
                if cleaned.startswith("{") and cleaned.endswith("}"):
                    try:
                        return json.loads(cleaned)
                    except (ValueError, json.JSONDecodeError):
                        continue
        raise ValueError(f"模型回复中包含 JSON 但解析失败。原始回复:\n{text[:500]}")
