#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preflight_check.py

前置校验脚本 - 代码级硬拦截。
检查项：
1. Python版本 >= 3.8
2. 凭证文件是否存在且有效
3. 标签指标表是否存在
4. 技能脚本目录完整性

用法：
    python3 preflight_check.py [--action run]

返回 JSON：
    {"status": "ok", ...}  - 通过
    {"status": "error", "blockers": [...]}  - 被拦截
"""

import json
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CRED_FILE = Path.home() / ".mingdata_dmp_credentials"
ASSETS_DIR = SKILL_DIR / "assets"


def check_python_version():
    if sys.version_info < (3, 8):
        return False, f"Python版本过低: {sys.version}，需要 >= 3.8"
    return True, f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def check_auth_skill():
    """检查鉴权技能是否安装（与批量打通圈包技能一致）"""
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        from find_auth_skill import find_auth_skill_path
        path = find_auth_skill_path()
        if path:
            return True, f"鉴权技能已安装（{path}）"
        return False, "鉴权技能未安装"
    except ImportError:
        # find_auth_skill.py 不存在，用内联逻辑检查
        possible_paths = [
            Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
            Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
            Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        ]
        for p in possible_paths:
            if p.exists():
                return True, f"鉴权技能已安装（{p}）"
        return False, "鉴权技能未安装"


def check_credentials():
    """检查凭证文件存在且完整"""
    if not CRED_FILE.exists():
        return False, f"凭证文件不存在: {CRED_FILE}（请运行 python3 scripts/setup_credentials.py <AK> <SK>）"
    try:
        with open(CRED_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
        if not creds.get("access_key") or not creds.get("secret_key"):
            return False, "凭证不完整（缺少 access_key 或 secret_key）"
        base_url = creds.get("base_url", "https://open.mingdata.com")
        return True, f"凭证文件有效（base_url={base_url}）", creds
    except Exception as e:
        return False, f"凭证读取失败: {e}", None


def check_api_connectivity():
    """实际调用tag/list接口验证AK/SK能连通DMP API（签名+网络+权限均验证）。
    强制重新import以避免模块缓存读到旧凭证。"""
    try:
        # 清除模块缓存，强制重新加载以读取最新凭证文件
        for mod in list(sys.modules.keys()):
            if mod in ('auth', 'dmp_api_client') or mod.startswith('auth.') or mod.startswith('dmp_api_client.'):
                del sys.modules[mod]
        sys.path.insert(0, str(SCRIPT_DIR))
        from dmp_api_client import DmpClient
        client = DmpClient.from_config(timeout=10)
        resp = client.get("/tag/list", params={"tagType": 1})
        if str(resp.get("code")) != "0":
            return False, f"API返回错误: code={resp.get('code')}, msg={resp.get('msg')}"
        data = resp.get("data") or []
        return True, f"API连通正常（tag/list返回{len(data)}个明略标签）"
    except RuntimeError as e:
        return False, f"API连接/鉴权失败: {e}"
    except Exception as e:
        return False, f"API验证异常: {type(e).__name__}: {e}"


def check_assets():
    xlsx = ASSETS_DIR / "标签指标表.xlsx"
    if not xlsx.exists():
        return False, f"标签指标表不存在: {xlsx}"
    return True, f"标签指标表存在（{xlsx.stat().st_size} bytes）"


def check_scripts():
    required = [
        # 基础设施
        "dmp_api_client.py", "auth.py", "setup_credentials.py",
        "find_auth_skill.py", "check_task_logger.py",
        # Step 3-6: 标签池→召回→兜底→画像→分组排序
        "query_tag_list.py",
        "coverage_matrix.py", "capability_probe.py",
        "build_queries_generic.py", "build_queries.py",  # 兼容旧版与通用版
        "tag_semantic_search.py", "fallback_key_dimensions.py",
        "tag_profile_enrich.py", "rank_candidates.py",
        "requirement_audit.py",
        # 鉴权技能安装对齐（可选，但用于对话层一致性）
        "install_auth_skill.py",
        # Step 8-12: 层级→基准→Overlap→扩缩量→方案生成
        "tag_hierarchy.py", "create_must_baseline.py",
        "analyze_overlap.py", "analyze_scale.py", "generate_plans.py",
        # Step 14: 创建+查询
        "create_combined_crowd.py", "query_crowd_task.py",
    ]
    missing = []
    for s in required:
        if not (SCRIPT_DIR / s).exists():
            missing.append(s)
    if missing:
        return False, f"脚本缺失: {', '.join(missing)}"
    return True, f"所有必需脚本存在（{len(required)}个）"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="tp圈人-组合人群 前置校验")
    parser.add_argument("--action", default="run", choices=["run"])
    args = parser.parse_args()

    blockers = []
    checks = {}

    for name, fn in [
        ("python_version", check_python_version),
        ("auth_skill", check_auth_skill),
        ("credentials", check_credentials),
        ("assets", check_assets),
        ("scripts", check_scripts),
        ("api_connectivity", check_api_connectivity),
    ]:
        result = fn()
        ok, msg = result[0], result[1]
        checks[name] = {"ok": ok, "message": msg}
        if not ok:
            blockers.append(f"[{name}] {msg}")

    if blockers:
        result = {
            "status": "error",
            "message": "前置校验失败，请修复阻塞项后重试",
            "blockers": blockers,
            "checks": checks,
            "help": {
                "setup_credentials": f"python3 {SCRIPT_DIR}/setup_credentials.py <AK> <SK> [BASE_URL]",
                "credential_guide": str(SKILL_DIR / "references" / "凭证获取指南.md"),
                "install_guide": str(SKILL_DIR / "references" / "技能安装与环境检查.md"),
            }
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    else:
        result = {
            "status": "ok",
            "message": "前置校验通过，可以执行圈人流程",
            "checks": checks,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)


if __name__ == "__main__":
    main()
