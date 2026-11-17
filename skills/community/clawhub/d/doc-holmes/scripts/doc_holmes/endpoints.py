"""翻译端点配置层。

优先级：DOC_HOLMES_* 环境变量 > ~/.config/doc-holmes/env > 无默认。

分发安全（v1.0.1，机制层）：
  - 出厂不内置任何端点与密钥：用户必须显式配置【自己的】OpenAI 兼容端点 + 自己的 key；
  - GLM Coding Plan 订阅端点（/coding/）默认拒绝：订阅服务面向编码工具场景，
    第三方翻译工具接入违反服务条款、有封号风险——保护用户就是保护发布者；
    知情用户可用 DOC_HOLMES_ALLOW_CODING_ENDPOINT=1 显式解锁（自担风险）；
  - 官方开放平台 /api/paas/v4（自有 key，glm-4.5-flash 等免费档）是合法通道，不拦。
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_BASE_URL = ""
DEFAULT_MODEL = "glm-4.5-flash"
DEFAULT_QPS = 4
DEFAULT_OPENAI_TIMEOUT = 180   # 密集页大段落实测 60s 不够（STTT 案例）
ENV_FILE = os.path.expanduser("~/.config/doc-holmes/env")

GUIDE_LINES = (
    "缺少端点/API key 配置。doc-holmes 不内置任何端点——请配置【你自己的】"
    "OpenAI 兼容端点 + key（三选一）：\n"
    "  A) 智谱开放平台官方 API（推荐）：https://open.bigmodel.cn/api/paas/v4\n"
    "     glm-4.5-flash 免费档；在 open.bigmodel.cn 注册并创建你自己的 key\n"
    "  B) SiliconFlow 等聚合平台免费档（https://api.siliconflow.cn/v1）\n"
    "  C) 任意 OpenAI 兼容端点\n"
    "设置方式（二选一）：\n"
    "  1) 环境变量：\n"
    "     export DOC_HOLMES_OPENAI_BASE_URL=<上面选的端点>\n"
    "     export DOC_HOLMES_OPENAI_API_KEY=<你的key>\n"
    "  2) 配置文件 ~/.config/doc-holmes/env 写入同样两行\n"
    "⚠️ GLM Coding Plan 订阅端点（/coding/）不适用：官方 FAQ 明确套餐仅限指定\n"
    "     编码工具，其他工具调用不享套餐额度、按量扣除账户余额。")


class EndpointError(RuntimeError):
    """端点配置错误（含用户可操作的修复指引）。"""


class PaidEndpointError(EndpointError):
    """分发安全断言触发（基类）。"""


class CodingPlanEndpointError(PaidEndpointError):
    """配置指向 GLM Coding Plan 订阅端点（默认拒绝，防封号）。"""


@dataclass
class EndpointConfig:
    base_url: str = DEFAULT_BASE_URL
    api_key: str = ""
    model: str = DEFAULT_MODEL
    qps: int = DEFAULT_QPS
    timeout: int = DEFAULT_OPENAI_TIMEOUT


def _parse_env_file(path: str) -> dict:
    data = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                val = val.split(" #", 1)[0]          # 剥行内注释
                data[key.strip()] = val.strip().strip('"').strip("'")
    except OSError:
        pass
    return data


def assert_distribution_safe(base_url: str, allow_coding: bool = False) -> None:
    """订阅端点知情确认（依据智谱官方 FAQ，2026-09 查证）。

    Coding Plan 仅限官方指定编码工具使用；在此外的调用不享套餐额度、
    按量扣除账户余额；多人共用同一订阅会被视为不当使用、限制订阅权益。
    个人知情使用不干涉——设 DOC_HOLMES_ALLOW_CODING_ENDPOINT=1 一次性确认。
    """
    url = (base_url or "").strip().lower()
    if "/coding/" in url and not allow_coding:
        raise CodingPlanEndpointError(
            "检测到 GLM Coding Plan 订阅端点：%s\n"
            "官方 FAQ 明确：该套餐仅限指定编码工具使用；在此外调用【不享套餐额度，"
            "按量扣除账户余额】；多人共用同一订阅会被视为不当使用并限制订阅权益。\n"
            "推荐改用官方开放平台 https://open.bigmodel.cn/api/paas/v4"
            "（glm-4.5-flash 免费档，同样用自己的 key）。\n"
            "确认知晓以上计费后果、仍要将本工具接入你的订阅：设 "
            "DOC_HOLMES_ALLOW_CODING_ENDPOINT=1 后重试（写入 env 文件即可永久生效）。"
            % base_url)


def load_endpoint_config(environ=None, env_file: str = ENV_FILE,
                         allow_custom: bool = False) -> EndpointConfig:
    """加载端点配置；缺配置/订阅端点时抛出带修复指引的错误。"""
    environ = os.environ if environ is None else environ
    filedata = _parse_env_file(env_file)

    def pick(key: str, default: str = "") -> str:
        return environ.get(key) or filedata.get(key) or default

    base_url = pick("DOC_HOLMES_OPENAI_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    allow_coding = (allow_custom
                    or environ.get("DOC_HOLMES_ALLOW_CODING_ENDPOINT") == "1"
                    or filedata.get("DOC_HOLMES_ALLOW_CODING_ENDPOINT") == "1")
    if not base_url:
        raise EndpointError(GUIDE_LINES)
    assert_distribution_safe(base_url, allow_coding=allow_coding)

    cfg = EndpointConfig(
        base_url=base_url,
        api_key=pick("DOC_HOLMES_OPENAI_API_KEY"),
        model=pick("DOC_HOLMES_MODEL", DEFAULT_MODEL),
        qps=_to_int(pick("DOC_HOLMES_QPS"), DEFAULT_QPS),
        timeout=_to_int(pick("DOC_HOLMES_OPENAI_TIMEOUT"), DEFAULT_OPENAI_TIMEOUT),
    )
    if not cfg.api_key:
        raise EndpointError(
            "已配置端点 %s，但缺少 API key。请任选其一设置：\n"
            "  1) 环境变量：export DOC_HOLMES_OPENAI_API_KEY=<你的key>\n"
            "  2) 配置文件：%s\n"
            "     写入一行：DOC_HOLMES_OPENAI_API_KEY=<你的key>\n"
            "     （建议把该文件权限设为仅本人可读）" % (cfg.base_url, env_file)
        )
    return cfg


def _to_int(val, default: int) -> int:
    try:
        return int(str(val))
    except (TypeError, ValueError):
        return default
