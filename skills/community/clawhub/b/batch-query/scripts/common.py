#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
common.py — 小递查查技能共用模块

集中存放：
  - 兜底提示文案（会话内自助排查 + 助手协助，不做外部联系渠道）
  - GetUserApiKey 返回 → 批量查询凭据 的映射（已实测确认）
  - 凭据文件写入
  - 统一的中文文案/提示生成

注意（合规约束）：
  技能包内**不内置任何外部联系渠道**——不写第三方即时通讯账号、电子邮箱、
  电话、外部站点地址，也不夹带任何推广。兜底提示一律落在会话内，由助手
  继续协助排查。如需接入部署方自有支持渠道，请自行扩展 cs_hint()，
  不要把这些账号写回本技能包（selftest 的零外部联系渠道扫描会拦截）。
"""

import os
import stat


# --------------------------------------------------------------------------- #
# 兜底提示（统一出口）
#
# 设计原则：只给「下一步做什么」，不给「去哪里找人」。
# 原因：技能发布审核禁止带外部联系渠道；提示里出现即时通讯账号、电子邮箱
# 或外部站点地址会被判为违规内容而驳回。
# --------------------------------------------------------------------------- #
CREDS_KEYS = ("XDCC_PLATFORM_ID", "XDCC_MEMBER_ID", "XDCC_API_KEY")


def cs_hint(reason: str = "") -> str:
    """生成统一的兜底提示。reason 为可选的原因说明。"""
    lines = []
    if reason:
        lines.append(f"⚠️ 遇到问题：{reason}")
    lines.append("建议按以下顺序自助排查：")
    lines.append("  1. 检查凭据文件是否三个键齐全（" + " / ".join(CREDS_KEYS) + "）")
    lines.append("  2. 单独执行 `onboard.py --validate-only` 复核当前凭据是否仍有效")
    lines.append("  3. 把这段报错原文发回会话，助手会带着上下文继续协助处理")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# GetUserApiKey 返回 → 批量查询凭据 映射
# 实测确认：批量查询签名所需的 MemberID 即 GetUserApiKey 返回的 UserID
#   取 UserID 作为 MemberID 调用可成功；若误填 PlatformID 等其他值会返回"用户信息不存在"或"PlatformID错误"
# --------------------------------------------------------------------------- #
def map_apikey_to_creds(data: dict) -> dict:
    """把 GetUserApiKey 的 Data 节点映射为批量查询所需的凭据。"""
    pid = data.get("PlatformID") or data.get("platformId")
    uid = data.get("UserID") or data.get("userID")
    key = data.get("UserApiKey") or data.get("apiKey")
    return {
        "XDCC_PLATFORM_ID": str(pid) if pid is not None else "",
        "XDCC_MEMBER_ID": str(uid) if uid is not None else "",  # = UserID，已实测
        "XDCC_API_KEY": str(key) if key is not None else "",
    }


DEFAULT_TEST_NO = "75012345678901"


def validate_track_creds(creds: dict, test_no: str = DEFAULT_TEST_NO):
    """用真实接口试跑一单，确认凭据可用于批量查询。返回 (ok, message)。

    guided_register 与 onboard 共用此实现，避免同一段校验逻辑出现两份副本。
    """
    try:
        import batch_query as bq  # 纯标准库，可安全导入
        r = bq.query_track(
            creds.get("XDCC_PLATFORM_ID", ""),
            creds.get("XDCC_API_KEY", ""),
            creds.get("XDCC_MEMBER_ID", ""),
            test_no,
        )
        code = r.get("Code")
        if code == 200:
            return True, "鉴权通过（Code=200）"
        if code == 500:
            return False, f"接口返回 500：{r.get('Message')}"
        return False, f"接口返回 Code={code}，Message={r.get('Message')}"
    except Exception as e:
        return False, f"校验请求异常: {e}"


def write_creds(path: str, creds: dict, token: str = None, extra_comment: str = "") -> None:
    """把凭据写入 .env 风格文件（UTF-8）。会保留注释头，便于客户自查。"""
    pid = creds.get("XDCC_PLATFORM_ID", "")
    mid = creds.get("XDCC_MEMBER_ID", "")
    key = creds.get("XDCC_API_KEY", "")
    lines = [
        "# 小递查查（xdccy.com）API 凭据",
        f"# 由「注册引导向导」自动生成。来源：register.html 注册 → GetUserApiKey 返回",
        "# 用途：xdcc-batch-query 技能批量查询快递（签名鉴权）",
        "# 安全提示：本文件含商业凭据，请勿提交到代码仓库或公开渠道",
        "",
        f"XDCC_PLATFORM_ID={pid}",
        f"XDCC_MEMBER_ID={mid}",
        f"XDCC_API_KEY={key}",
    ]
    if token:
        lines.append("")
        lines.append("# 网页登录 token（JWT，可能过期；仅用于 GetUserApiKey 等网页 API，非批量查询必需）")
        lines.append(f"XDCC_USER_TOKEN={token}")
    if extra_comment:
        lines.append("")
        lines.append(f"# {extra_comment}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    _tighten_creds_perm(path)


def _tighten_creds_perm(path: str) -> None:
    """凭据含商业密钥，Unix 下收紧为仅本人可读写；Windows 无该语义，忽略。"""
    try:
        if os.name == "posix":
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def load_creds(path: str) -> dict:
    """从 .env 风格文件读取凭据（仅取 XDCC_ 前缀的键）。"""
    creds = {}
    if not os.path.isfile(path):
        return creds
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k.startswith("XDCC_"):
                creds[k] = v
    return creds
