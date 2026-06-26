#!/usr/bin/env python3
"""
api_paths.py
DeepSOP humabot 技能的 **API 路径权威清单（代码侧单一来源）**。

此文件必须与 `SKILL.md` 顶部「📋 API 路径权威清单」的 20 条路径**完全一致**。
任何脚本需要发起 HTTP 请求时，**必须**：
  1. 从本模块导入对应的常量或调用 `build_url(name, **query)`；
  2. 严禁在脚本中拼接、改写、私加 query 参数；
  3. 若 SKILL.md 增删改路径，必须同步更新本文件，否则视为 bug。

为什么要在代码侧再设一份：
  - SKILL.md 的清单约束的是 LLM/Agent 的行为；
  - api_paths.py 约束的是脚本（Python）行为；
  - 二者构成"双轨强约束"，避免任一侧偷偷绕过。

校验：本模块自带 `verify_against_skill_md()`，可在 CI 或 dev 环境中比对
SKILL.md 中的路径表是否漂移。
"""
from __future__ import annotations

from typing import Final


BASE_URL: Final[str] = "https://ai.deepsop.com/prod-api"


# 与 SKILL.md「📋 API 路径权威清单」编号一致 —— 任何修改必须同步两侧
API_PATHS: Final[dict[str, str]] = {
    # 1
    "preset_employee_list":            "/ai/presetEmployee/list",
    # 1.1
    "signup_package_list":             "/ai/setting/list?packageType=3",
    # 1.2
    "kcoin_rate_config":               "/system/config/configKey/CNY_TO_KCOIN",
    # 1.3
    "kcoin_balance":                   "/ai/vip/balance",
    # 1.4
    "purchase_package_by_ktoken":      "/ai/order/purchaseIndependentPackageByKToken",
    # 2
    "preset_employee_submit_task":     "/ai/presetEmployee/submitTask",
    # 3
    "outbound_describe_instance":      "/ai/outBound/describeInstance",
    # 4
    "outbound_caller_number_list":     "/ai/outBound/callerNumber/list",
    # 5
    "outbound_list_scripts":           "/ai/outBound/listScripts",
    # 5.1 创建/修改场景并提交审核（场景+TTS+机器人设定 三合一）
    "outbound_create_or_modify_script": "/ai/outBound/createOrModifyScriptAndSubmitScriptReview",
    # 5.2 查询场景库详情（轮询审核状态）
    "outbound_describe_script":         "/ai/outBound/describeScript",
    # 5.3 查询机器人设定详情（修改场景时回填）
    "outbound_get_agent_profile":       "/ai/outBound/getAgentProfile",
    # 5.4 单独提交既有草稿/已发布场景重新进入审核
    "outbound_submit_script_review":    "/ai/outBound/submitScriptReview",
    # 5.5 撤销正在审核中的场景
    "outbound_withdraw_script_review":  "/ai/outBound/withdrawScriptReview",
    # 6
    "emailconfig_list":                "/ai/emailconfig/list",
    # 7
    "user_profile":                    "/ai/user/profile",
    # 8
    "sms_query_template_list":         "/ai/sms/querySmsTemplateList",
    # 9（已迁移到 deepsop-tiktokflow）— Toby/TikTok 相关接口已移除
    # 12
    "preset_employee_pool_detail":     "/ai/presetEmployee/getCustomerPoolDetail",
    # 13
    "email_get_task_email_count":      "/ai/email/getTaskEmailCount",
    # 14
    "email_task_list":                 "/ai/email/taskList",
    # 15
    "preset_employee_collab_stat":     "/ai/presetEmployee/collaborationTaskStatistics",
    # 16
    "preset_employee_collab_call":     "/ai/presetEmployee/collaborationCallResult",
    # 17
    "sms_get_task_sms_count":          "/ai/sms/getTaskSmsCount",
    # 18
    "sms_get_sms_result_list":         "/ai/sms/getSmsResultList",
    # 21
    "customer_search_list":            "/ai/customer/customerList",
    # 22
    "system_file_upload":              "/system/fileUpload/upload",
    # 23 公司导入模板下载（POST, application/x-www-form-urlencoded, blob 响应）
    "customer_import_template":        "/ai/customer/template",
    # 24 地址簿导入模板下载（POST, application/x-www-form-urlencoded, blob 响应）
    "contact_import_template":         "/ai/customer/contactImportTemplate",
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
    （供 CI / 排查使用，不在运行时调用。）
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
