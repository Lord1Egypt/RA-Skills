"""前置环境变量检查，收到 Amazon 铺货请求后必须最先执行。"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import env, load_env
from scripts.process_images import _decode_ak


load_env()


REQUIRED = [
    (("DXB_USER_ID",), "DXB_USER_ID", "店小宝用户 ID，用于查询已绑定 Amazon 店铺"),
    (
        ("ALPHASHOP_ACCESS_KEY", "ACCESS_KEY"),
        "ALPHASHOP_ACCESS_KEY",
        "遨虾网关 AK，用于 1688 商品、类目和 CPV 映射接口；可用 ACCESS_KEY alias",
    ),
    (
        ("ALPHASHOP_SECRET_KEY", "SECRET_KEY"),
        "ALPHASHOP_SECRET_KEY",
        "遨虾网关 SK，与 AK 配合生成 JWT；可用 SECRET_KEY alias",
    ),
    (("ALI_1688_AK",), "ALI_1688_AK", "源舟网关 AK，用于 Amazon 主图白底、裁剪和翻译处理"),
]


def missing_env() -> list[tuple[str, str]]:
    missing = []
    for names, display_name, desc in REQUIRED:
        if not any(env(name) for name in names):
            missing.append((display_name, desc))
    return missing


def invalid_env() -> list[tuple[str, str]]:
    raw_ak = env("ALI_1688_AK")
    if not raw_ak:
        return []
    try:
        _decode_ak(raw_ak)
    except RuntimeError:
        return [("ALI_1688_AK", "源舟网关 AK 格式无效，需满足图片网关 AK 的长度/编码规则")]
    return []


def env_errors() -> list[tuple[str, str]]:
    return missing_env() + invalid_env()


def main() -> int:
    errors = env_errors()
    if errors:
        print("环境变量检查失败，请逐项提供或修正后重试：")
        for key, desc in errors:
            print(f"  - {key}  ({desc})")
        return 1
    print("环境变量检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
