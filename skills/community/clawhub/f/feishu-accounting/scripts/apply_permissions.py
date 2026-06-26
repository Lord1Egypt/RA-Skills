#!/usr/bin/env python3
"""
飞书应用一键权限申请脚本
1. 生成「一键授权链接」— 把所有 base 相关权限打包在一个 URL 里
2. 调用 scopes/apply API 提交管理员审批请求
用户只需：点链接 → 确认 → 审批 → 发布

用法：
    python3 apply_permissions.py --app-id cli_xxx --app-secret xxx
"""

import argparse
import json
import urllib.request
import urllib.error

FEISHU_HOST = "https://open.feishu.cn"


def get_tenant_token(app_id: str, app_secret: str) -> str:
    """获取 Tenant Access Token"""
    url = f"{FEISHU_HOST}/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"获取 Tenant Token 失败: {result}")
    return result["tenant_access_token"]


# 记账系统需要的所有 base 权限
REQUIRED_SCOPES = [
    "base:app:read",
    "base:app:update",
    "base:app:create",
    "base:table:read",
    "base:table:create",
    "base:table:update",
    "base:table:delete",
    "base:field:read",
    "base:field:create",
    "base:field:update",
    "base:field:delete",
    "base:record:read",
    "base:record:create",
    "base:record:update",
    "base:record:delete",
    "base:view:read",
    "base:view:write_only",
    "bitable:app:readonly",
    "bitable:app",
]


def build_auth_url(app_id: str) -> str:
    """生成一键授权链接"""
    scopes_str = ",".join(REQUIRED_SCOPES)
    return (
        f"{FEISHU_HOST}/app/{app_id}/auth"
        f"?q={scopes_str}"
        f"&op_from=openapi&token_type=tenant"
    )


def call_scopes_apply(app_id: str, token: str) -> dict:
    """调用 scopes/apply API 提交审批"""
    url = f"{FEISHU_HOST}/open-apis/application/v6/scopes/apply"
    data = json.dumps({}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        return body


def main():
    parser = argparse.ArgumentParser(description="飞书应用一键权限申请")
    parser.add_argument("--app-id", required=True, help="飞书应用 App ID")
    parser.add_argument("--app-secret", required=True, help="飞书应用 App Secret")
    args = parser.parse_args()

    print("🚀 开始申请飞书记账系统权限...")

    # Step 1: 获取 Token
    token = get_tenant_token(args.app_id, args.app_secret)
    print("✅ 获取 Tenant Token 成功")

    # Step 2: 生成一键授权链接
    auth_url = build_auth_url(args.app_id)
    print(f"\n🔗 一键授权链接（点击后确认即可批量开通所有权限）：")
    print(f"{auth_url}")
    print()

    # Step 3: 打印需要用户后续操作的提示
    print("=" * 60)
    print("📋 操作步骤：")
    print("  1️⃣  点击上面的链接，跳转到飞书权限管理页面")
    print("  2️⃣  页面会列出所有需要的权限，点击「确认开通权限」")
    print("  3️⃣  返回后告诉我「权限已开通」")
    print("  4️⃣  我会调用 scopes/apply API 提交审批申请")
    print("  5️⃣  去 飞书开放平台 → 版本管理与发布 → 创建版本并发布")
    print("=" * 60)

    # Step 4: 尝试调用 scopes/apply（用户确认权限后可调用）
    print("\n📡 尝试调用 scopes/apply...")
    result = call_scopes_apply(args.app_id, token)
    code = result.get("code", -1)
    if code == 0:
        print("✅ scopes/apply 调用成功！请去飞书审批中确认")
    elif code == 212002:
        print("ℹ️  所有权限已授权，无需重复审批")
    elif code == 212003:
        print("ℹ️  审批次数超过限制（同一版本最多申请 10 次）")
    elif code == 212004:
        print("ℹ️  重复申请，审批单已存在")
    else:
        msg = result.get("msg", "未知错误")
        print(f"ℹ️  待用户确认权限后再调用 scopes/apply（code={code}: {msg}）")
        print("   用户确认权限后，agent 会重新调用 scopes/apply")


if __name__ == "__main__":
    main()
