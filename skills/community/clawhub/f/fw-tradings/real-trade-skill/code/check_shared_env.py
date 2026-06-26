"""检查共享凭证是否存在且可用。

副作用：成功时顺带把账户列表分门别类写入共享 fosun.env 的 FSOPENAPI_ACCOUNT_INDEX，
让后续所有交易脚本零额外接口消耗即可解析 subAccountId。
"""

from __future__ import annotations

import argparse
import json
import sys

from _client import build_client, refresh_account_index, shared_env_path

EPILOG = """\
何时调用：
  - 任何实盘操作前的"体检"，特别是用户怀疑凭证失效时
  - install.sh 完成后第一次跑

示例：
  check_shared_env.py

输出（status=valid 表示凭证可用 + 账户索引已刷新；status=invalid 写入 stderr）：
  {
    "status": "valid",
    "next_action": "...",                 // 模型必须读这一条再决定下一步
    "real_stock_account_available": true|false, // 实盘证券账户是否可直接用
    "env_path": "/path/to/fosun.env",
    "counts": {"mock": 1, "real_stock": 1, "real_option": 0}
  }

读懂结果（重要）：
  - real_stock_account_available=false → 共享凭证下没有实盘证券账户，实盘脚本会拒绝执行
  - status=invalid → 先通过 fosun-env-setup 修复或重新生成共享凭证
"""

NEXT_ACTION_VALID_HAS_REAL_STOCK = (
    "凭证有效且实盘证券账户可用。把体检结果汇报给用户，等用户明确具体业务请求后再调对应脚本；"
    "禁止自动连环跑业务脚本。"
)
NEXT_ACTION_VALID_NO_REAL_STOCK = (
    "凭证有效，但共享凭证下没有实盘证券账户（subAccountType=0）。把这一情况转告用户并停手，"
    "等用户确认实盘证券账户是否已开通；禁止私自切模拟盘 skill。"
)
NEXT_ACTION_INVALID = (
    "共享凭证不可用。请先通过 fosun-env-setup 生成或修复有效的 fosun.env；"
    "禁止在凭证未恢复前调任何实盘业务脚本。"
)


def main():
    argparse.ArgumentParser(
        description="体检：共享凭证是否可用 + 刷新账户索引缓存",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    ).parse_args()

    try:
        client = build_client()
        index = refresh_account_index(client)
        counts = {
            "mock": len(index.get("mock") or []),
            "real_stock": len(index.get("real_stock") or []),
            "real_option": len(index.get("real_option") or []),
        }
        real_stock_available = counts["real_stock"] > 0
        payload = {
            "status": "valid",
            "next_action": NEXT_ACTION_VALID_HAS_REAL_STOCK if real_stock_available else NEXT_ACTION_VALID_NO_REAL_STOCK,
            "real_stock_account_available": real_stock_available,
            "env_path": str(shared_env_path()),
            "message": "共享凭证可用，已刷新账户索引",
            "refreshedAt": index.get("refreshedAt"),
            "counts": counts,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except Exception as exc:  # noqa: BLE001
        payload = {
            "status": "invalid",
            "next_action": NEXT_ACTION_INVALID,
            "env_path": str(shared_env_path()),
            "message": f"{type(exc).__name__}: {exc}",
            "action": "请先通过 fosun-env-setup 确保 FOSUN_ENV_PATH 指向的共享凭证文件已生成且有效",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
