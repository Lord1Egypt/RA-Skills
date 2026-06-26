#!/usr/bin/env python3
"""
api_paths.py
DeepSOP TikTokFlow 技能的 **API 路径权威清单（代码侧单一来源）**。

此文件必须与 `SKILL.md` 顶部「📋 API 路径权威清单」**完全一致**。
任何脚本需要发起 HTTP 请求时，**必须**：
  1. 从本模块导入对应的常量或调用 `build_url(name)`；
  2. 严禁在脚本中拼接、改写、私加 query 参数；
  3. 若 SKILL.md 增删改路径，必须同步更新本文件，否则视为 bug。

为什么要在代码侧再设一份：
  - SKILL.md 的清单约束 LLM/Agent 行为；
  - api_paths.py 约束脚本（Python）行为；
  - 二者构成"双轨强约束"，避免任一侧偷偷绕过。

校验：本模块自带 `verify_against_skill_md()`，可在 CI 或 dev 环境中比对
SKILL.md 中的路径表是否漂移。
"""
from __future__ import annotations

from typing import Final


BASE_URL: Final[str] = "https://ai.deepsop.com/prod-api"


# 与 SKILL.md「📋 API 路径权威清单」一致 —— 任何修改必须同步两侧
API_PATHS: Final[dict[str, str]] = {
    # 1：数字员工可用性
    "preset_employee_list":            "/ai/presetEmployee/list",
    # 1.1：签约套餐列表
    "signup_package_list":             "/ai/setting/list?packageType=3",
    # 1.2：人民币→K币汇率
    "kcoin_rate_config":               "/system/config/configKey/CNY_TO_KCOIN",
    # 1.3：K币余额查询
    "kcoin_balance":                   "/ai/vip/balance",
    # 1.4：提交签约（扣K币）
    "purchase_package_by_ktoken":      "/ai/order/purchaseIndependentPackageByKToken",
    # 1.5：用户 Profile（取 userId）
    "user_profile":                    "/ai/user/profile",
    # 2：提交任务
    "preset_employee_submit_task":     "/ai/presetEmployee/submitTask",
    # 3：TikTok 账号列表
    "authaccount_list":                "/ai/authaccount/list",
    # 4：TikTok 账号权限
    "tiktok_get_creator_info":         "/ai/auth/tiktok/getCreatorInfo",
    # 5：视频模型列表
    "consume_source_list":             "/ai/consumeSource/list",
    # 6：视频统计
    "data_count":                      "/ai/data/count",
    # 7：视频列表
    "data_list":                       "/ai/data/list",
}


def build_url(name: str) -> str:
    """根据清单 key 取得不带 query 的完整 URL。"""
    if name not in API_PATHS:
        raise KeyError(
            f"未知 API 名称：{name!r}。可用 key 列表见 api_paths.API_PATHS；"
            f"如确需新增接口，请先在 SKILL.md 中加入清单后再同步本文件。"
        )
    return BASE_URL + API_PATHS[name]


def assert_url_matches(url: str, name: str) -> None:
    """
    在脚本里硬编码 URL 时，用本函数自检：URL 必须严格等于 build_url(name)
    或以 build_url(name) 开头（仅允许追加 ?query=...）。
    校验失败立刻抛 AssertionError，阻止误用。
    """
    expected = build_url(name)
    if url != expected and not url.startswith(expected + "?"):
        raise AssertionError(
            f"[api_paths] URL 与 SKILL.md 清单不一致：\n"
            f"  传入：{url}\n"
            f"  期望：{expected}（允许追加 ?query=...）\n"
            f"  对照 SKILL.md「📋 API 路径权威清单」中的 {name!r} 条目。"
        )


def verify_against_skill_md(skill_md_path: str | None = None) -> list[str]:
    """
    对照 SKILL.md 中所有形如 https://ai.deepsop.com/prod-api/... 的路径，
    检查它们是否都出现在本文件 API_PATHS 的值集合中。返回不一致项列表。
    """
    import re
    from pathlib import Path

    if skill_md_path is None:
        skill_md_path = str(Path(__file__).resolve().parent.parent / "SKILL.md")
    text = Path(skill_md_path).read_text(encoding="utf-8")

    pattern = re.compile(r"https://ai\.deepsop\.com/prod-api(/[A-Za-z0-9_/]+)")
    found_paths = {m.group(1) for m in pattern.finditer(text)}
    # 去除 query string，path 才是 drift 比对单位
    known_paths = {v.split("?", 1)[0] for v in API_PATHS.values()}
    drift = sorted(found_paths - known_paths)
    return drift


if __name__ == "__main__":
    import sys

    drift = verify_against_skill_md()
    if drift:
        sys.stderr.write(
            "[api_paths] ⚠️ SKILL.md 中出现未在 api_paths.API_PATHS 登记的路径：\n"
        )
        for p in drift:
            sys.stderr.write(f"  - {p}\n")
        sys.exit(1)
    print(f"[api_paths] OK：SKILL.md 中所有 prod-api 路径均已登记，共 {len(API_PATHS)} 条。")
