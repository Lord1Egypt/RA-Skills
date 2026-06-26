"""
凭证安全管理模块

安全原则：
- 所有凭证仅通过环境变量读取
- 零持久化：不写文件、不缓存、不打印
- 不通过命令行参数传递（避免进程列表泄露）
- 统一通过 get_credential() 函数访问
"""

import os
import sys

# 视频生成 Provider 密钥映射
_VIDEO_PROVIDER_KEYS = {
    "lumaai": "LUMAAI_API_KEY",
    "runway": "RUNWAY_API_KEY",
    "replicate": "REPLICATE_API_TOKEN",
    "openai": "OPENAI_API_KEY",
    "kling": "KLING_API_KEY",
}

# 平台发布密钥映射
_PLATFORM_KEYS = {
    "weibo": "WEIBO_ACCESS_TOKEN",
    "xiaohongshu": "XHS_COOKIE",
    "douyin": "DOUYIN_ACCESS_TOKEN",
}

# 云存储密钥映射
_CLOUD_KEYS = {
    "aliyun_oss": ["ALIYUN_ACCESS_KEY_ID", "ALIYUN_ACCESS_KEY_SECRET", "ALIYUN_OSS_BUCKET"],
    "tencent_cos": ["TENCENT_SECRET_ID", "TENCENT_SECRET_KEY", "TENCENT_COS_BUCKET"],
    "aws_s3": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_S3_BUCKET"],
}

# 合并所有单值密钥
_ALL_KEYS = {**_VIDEO_PROVIDER_KEYS, **_PLATFORM_KEYS}


def get_credential(provider: str) -> str:
    """
    从环境变量获取指定 provider 的 API 密钥。

    安全保证：
    - 仅从 os.environ 读取，不做任何持久化
    - 不记录、不打印密钥值
    - 每次调用都重新读取（不缓存）

    Args:
        provider: Provider 名称（如 "lumaai", "runway", "weibo"）

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
            f"Linux/macOS: export {env_var}=your_key_here\n"
            f"OpenClaw 配置: 在 openclaw.json 中设置 skills.entries.ai-video-pro.apiKey"
        )

    return value


def get_cloud_credentials(cloud_provider: str) -> dict:
    """
    获取云存储 provider 的多个凭证。

    Args:
        cloud_provider: 云存储名称（如 "aliyun_oss", "tencent_cos", "aws_s3"）

    Returns:
        凭证字典 {env_var_name: value}

    Raises:
        ValueError: 未知的云存储 provider
        EnvironmentError: 缺少必需的环境变量
    """
    env_vars = _CLOUD_KEYS.get(cloud_provider.lower())
    if not env_vars:
        raise ValueError(
            f"未知的云存储: '{cloud_provider}'\n"
            f"支持的云存储: {', '.join(sorted(_CLOUD_KEYS.keys()))}"
        )

    credentials = {}
    missing = []
    for var in env_vars:
        value = os.environ.get(var)
        if not value:
            missing.append(var)
        else:
            credentials[var] = value

    if missing:
        raise EnvironmentError(
            f"缺少云存储凭证，请设置以下环境变量:\n"
            + "\n".join(f"  - {var}" for var in missing)
        )

    return credentials


def list_available_providers() -> dict:
    """
    列出所有已配置凭证的 provider。

    Returns:
        字典 {"video": [...], "platform": [...], "cloud": [...]}
        每个列表包含已配置凭证的 provider 名称
    """
    result = {"video": [], "platform": [], "cloud": []}

    for provider, env_var in _VIDEO_PROVIDER_KEYS.items():
        if os.environ.get(env_var):
            result["video"].append(provider)

    for provider, env_var in _PLATFORM_KEYS.items():
        if os.environ.get(env_var):
            result["platform"].append(provider)

    for provider, env_vars in _CLOUD_KEYS.items():
        if all(os.environ.get(var) for var in env_vars):
            result["cloud"].append(provider)

    return result


def check_credential_status() -> str:
    """
    检查所有凭证的配置状态，输出人类可读的报告。

    Returns:
        格式化的状态报告字符串（不包含任何密钥值）
    """
    lines = ["=== 凭证配置状态 ===", ""]

    lines.append("视频生成 Provider:")
    for provider, env_var in _VIDEO_PROVIDER_KEYS.items():
        status = "✓ 已配置" if os.environ.get(env_var) else "✗ 未配置"
        lines.append(f"  {provider:12s} ({env_var}): {status}")

    lines.append("")
    lines.append("发布平台:")
    for provider, env_var in _PLATFORM_KEYS.items():
        status = "✓ 已配置" if os.environ.get(env_var) else "✗ 未配置 (可选)"
        lines.append(f"  {provider:12s} ({env_var}): {status}")

    lines.append("")
    lines.append("云存储:")
    for provider, env_vars in _CLOUD_KEYS.items():
        configured = all(os.environ.get(var) for var in env_vars)
        status = "✓ 已配置" if configured else "✗ 未配置 (可选)"
        lines.append(f"  {provider:12s}: {status}")

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
