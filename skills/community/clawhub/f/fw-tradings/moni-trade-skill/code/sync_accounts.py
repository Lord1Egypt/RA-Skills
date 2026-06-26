"""账户索引同步：调一次 /v1/account/Accounts，按类型分类写回共享 fosun.env。

用途：
- 用户新增/删除/变更子账户后，主动跑一次刷新缓存
- 也可作为日常体检：确认共享凭证下挂载了哪些 mock / real_stock / real_option 账户

输出会带 `next_action`：明确告诉模型本脚本是 meta 同步，跑完必须停手汇报，
禁止自动连环 cash_summary / holdings / order_*（治本：流程纪律下沉到运行时）。
"""
from __future__ import annotations

import argparse

from _client import build_client, dump_with_directive, refresh_account_index, run

EPILOG = """\
何时调用（仅在以下时机，平时不要主动跑）：
  - 用户明确说"我刚开了新账户 / 账户有变更，刷新一下"
  - 业务脚本反复报账户类错误，怀疑缓存过期

平时业务脚本会自动按需刷新缓存，**不需要先跑这个**。
"""

NEXT_ACTION_HAS_MOCK = (
    "已刷新账户索引到共享凭证。把刷新结果汇报给用户，等用户明确下一步业务请求后再继续；"
    "禁止自动连环跑 cash_summary / holdings / cash_flows / order_*。"
)
NEXT_ACTION_NO_MOCK = (
    "刷新后仍未发现模拟盘账户（subAccountType=2）。立即把可见账户清单转告用户并停手，"
    "等用户决定后续动作；禁止私自切实盘 skill 或挑其他账户继续模拟盘业务。"
)


def main():
    argparse.ArgumentParser(
        description="强制刷新账户索引到共享凭证（账户有变更时再跑）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    ).parse_args()

    client = build_client()
    index = refresh_account_index(client)
    mock = index.get("mock") or []
    real_stock = index.get("real_stock") or []
    real_option = index.get("real_option") or []
    mock_available = bool(mock)

    dump_with_directive(
        {
            "refreshedAt": index.get("refreshedAt"),
            "accounts": {
                "mock": mock,
                "real_stock": real_stock,
                "real_option": real_option,
            },
        },
        next_action=NEXT_ACTION_HAS_MOCK if mock_available else NEXT_ACTION_NO_MOCK,
        mock_account_available=mock_available,
        accounts_summary={
            "mock": len(mock),
            "real_stock": len(real_stock),
            "real_option": len(real_option),
        },
    )


if __name__ == "__main__":
    run(main)
