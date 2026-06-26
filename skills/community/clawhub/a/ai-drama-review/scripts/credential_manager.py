"""
凭证安全管理模块 - ai-drama-review

安全原则：
- 所有凭证仅通过环境变量读取
- 零持久化：不写文件、不缓存、不打印
- 不通过命令行参数传递（避免进程列表泄露）
- 统一通过 get_credential() 函数访问
"""

import os
import sys

# AI 分析 Provider 密钥映射
_AI_PROVIDER_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}

_ALL_KEYS = {**_AI_PROVIDER_KEYS}


def get_credential(provider: str) -> str:
    """
    从环境变量获取指定 provider 的 API 密钥。

    Args:
        provider: Provider 名称（如 "openai", "anthropic"）

    Returns:
        API 密钥字符串

    Raises:
        ValueError: 未知的 provider 名称
        EnvironmentError: 环境变量未设置
    """
    env_var = _ALL_KEYS.get(provider.lower())
    if not env_var:
        raise ValueError(
            f"未知的 provider: '{provider}'\n"
            f"支持的 provider: {', '.join(sorted(_ALL_KEYS.keys()))}"
        )

    value = os.environ.get(env_var)
    if not value:
        raise EnvironmentError(
            f"缺少凭证: 请设置环境变量 {env_var}\n"
            f"Windows:  set {env_var}=your_key_here\n"
            f"Linux/macOS: export {env_var}=your_key_here"
        )

    return value


def list_available_providers() -> list:
    """
    列出所有已配置凭证的 AI provider。

    Returns:
        已配置凭证的 provider 名称列表
    """
    return [
        provider for provider, env_var in _AI_PROVIDER_KEYS.items()
        if os.environ.get(env_var)
    ]


def check_credential_status() -> str:
    """
    检查所有凭证的配置状态。

    Returns:
        格式化的状态报告字符串（不包含任何密钥值）
    """
    lines = ["=== 凭证配置状态 ===", ""]

    lines.append("AI 分析 Provider:")
    for provider, env_var in _AI_PROVIDER_KEYS.items():
        status = "已配置" if os.environ.get(env_var) else "未配置"
        lines.append(f"  {provider:12s} ({env_var}): {status}")

    available = list_available_providers()
    lines.append("")
    if available:
        lines.append(f"运行模式: 混合模式 (本地 + AI 深度分析)")
    else:
        lines.append(f"运行模式: 仅本地模式 (关键词匹配)")
        lines.append(f"提示: 配置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 可启用 AI 深度分析")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        print(check_credential_status())
    elif len(sys.argv) > 1 and sys.argv[1] == "--available":
        import json
        print(json.dumps(list_available_providers(), indent=2, ensure_ascii=False))
    else:
        print("用法:")
        print("  python credential_manager.py --status    查看凭证配置状态")
        print("  python credential_manager.py --available 列出可用 provider")
