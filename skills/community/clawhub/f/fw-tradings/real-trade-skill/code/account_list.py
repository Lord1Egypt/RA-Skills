"""账户：查询账户列表  POST /api/v1/account/Accounts

副作用：成功调用后会把账户按 mock / real_stock / real_option 分类，
写回共享 fosun.env 的 FSOPENAPI_ACCOUNT_INDEX，供后续脚本零接口消耗解析。

输出会带 `next_action`：明确告诉模型本脚本是 meta 查询，跑完必须停手汇报，
禁止自动连环 cash_summary / holdings / order_*（治本：这条流程纪律不再依赖 SKILL.md 自觉）。
"""
import argparse

from _client import build_client, dump_with_directive, refresh_account_index, run

EPILOG = """\
何时调用：
  - 用户明确问"我有哪些账户"
  - 第一次接入 / 用户说账户有变更
  - **不要每次查余额/持仓前都先调它**：业务脚本会按需自动解析

示例：
  account_list.py

输出结构（顶层平铺）：
  {
    "ok": true,
    "next_action": "...",                 // 模型必须读这一条再决定下一步
    "real_stock_account_available": true|false, // 实盘证券账户是否可直接用，false 时禁止跑实盘业务脚本
    "accounts_summary": {"mock": 1, ...}, // 各桶数量速览
    "refreshedAt": <unix-ts>,
    "mock":        [{"subAccountId": "8", "subAccountType": 2, ...}],
    "real_stock":  [{"subAccountId": "388230258", ...}],
    "real_option": [...]
  }

读懂结果（重要）：
  - 看清楚一个账户落在哪个桶里，桶名 == 账户类型
  - **real_stock_account_available=false** 表示该共享凭证下没有实盘证券账户，实盘业务脚本会拒绝执行
  - subAccountId 一律是字符串
"""

NEXT_ACTION_HAS_REAL_STOCK = (
    "把账户清单完整念给用户，等用户明确具体业务请求（查余额/查持仓/下单等）后再调相应脚本；"
    "禁止自动连环跑 cash_summary / holdings / cash_flows / order_*。"
)
NEXT_ACTION_NO_REAL_STOCK = (
    "当前共享凭证下没有实盘证券账户（subAccountType=0）。立即把可见账户清单转告用户并停手，"
    "等用户决定是否确认实盘证券账户已开通 / 是否显式 --sub-account-id 指定调试；"
    "禁止私自切模拟盘 skill，禁止挑选其他账户继续实盘业务。"
)


def main():
    argparse.ArgumentParser(
        description="查询并刷新账户索引（mock / real_stock / real_option）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    ).parse_args()

    client = build_client()
    index = refresh_account_index(client)
    mock = index.get("mock") or []
    real_stock = index.get("real_stock") or []
    real_option = index.get("real_option") or []
    real_stock_available = bool(real_stock)

    dump_with_directive(
        {
            "refreshedAt": index.get("refreshedAt"),
            "mock": mock,
            "real_stock": real_stock,
            "real_option": real_option,
        },
        next_action=NEXT_ACTION_HAS_REAL_STOCK if real_stock_available else NEXT_ACTION_NO_REAL_STOCK,
        real_stock_account_available=real_stock_available,
        accounts_summary={
            "mock": len(mock),
            "real_stock": len(real_stock),
            "real_option": len(real_option),
        },
    )


if __name__ == "__main__":
    run(main)
