"""账户：重置模拟账户  POST /api/v1/account/SimAccountReset"""
import argparse

from _client import (
    build_client,
    dump_with_directive,
    ensure_user_confirmed,
    refresh_account_index,
    run,
    sim_account_reset,
)

EPILOG = """\
何时调用：
  - 用户明确要求重置某个模拟盘证券账户

接口行为：
  - 禁用旧模拟证券账户，并创建新的模拟证券账户
  - HKD/USD 各初始化 100 万现金
  - 重置需要间隔 7 天
  - 成功后脚本会刷新账户索引缓存，避免后续业务继续使用旧账户

强制规则：
  - 必须显式传 `--sub-account-id <旧模拟账户ID>`，禁止模型自动挑一个账户重置
  - 必须先向用户说明“旧账户会被禁用，并创建新账户”，再反问确认
  - 必须传 `--confirm`；未传直接 NEED_CONFIRMATION 拦截
"""


def _refresh_index_safely(client):
    try:
        index = refresh_account_index(client)
        return {
            "refreshed": True,
            "accounts_summary": {
                "mock": len(index.get("mock") or []),
                "real_stock": len(index.get("real_stock") or []),
                "real_option": len(index.get("real_option") or []),
            },
            "refreshedAt": index.get("refreshedAt"),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "refreshed": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def main():
    parser = argparse.ArgumentParser(
        description="重置模拟盘证券账户（禁用旧账户并创建新账户）",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sub-account-id", required=True, help="旧模拟证券账户 ID（必填）")
    parser.add_argument(
        "--intent",
        required=True,
        help=(
            "**必传**：用一段中文复述本次重置模拟账户意图，必须包含旧 subAccountId。"
            "例：『重置旧模拟账户 8：禁用旧账户并创建新模拟账户，HKD/USD 各初始化 100 万现金』。"
        ),
    )
    parser.add_argument("--confirm", action="store_true",
                        help="必传：用户已明确确认重置模拟账户后再加这个 flag")
    parser.add_argument("--confirm-token",
                        help="二次确认令牌：先触发一次 NEED_CONFIRMATION 后，从返回信息复制 token，再与 --confirm 一起提交")
    args = parser.parse_args()
    ensure_user_confirmed(
        args.confirm,
        action="重置模拟账户",
        intent_summary=args.intent,
        confirm_token=args.confirm_token,
    )

    client = build_client()
    result = sim_account_reset(client, args.sub_account_id)
    index_refresh = _refresh_index_safely(client)

    dump_with_directive(
        {
            "intent": args.intent,
            "oldSubAccountId": args.sub_account_id,
            "result": result,
            "account_index_refresh": index_refresh,
        },
        next_action=(
            "模拟账户重置请求已发送。先把旧 subAccountId、新 subAccountId、重置次数、账户状态、HKD/USD 初始现金和缓存刷新结果汇报给用户，然后停手。"
            "汇报时不能只说 code 数字，必须同时说明对应文字状态（如 code=0 表示接口返回成功）。"
            "禁止自动接 cash_summary / holdings / order_*；等用户明确下一步业务请求。"
        ),
    )


if __name__ == "__main__":
    run(main)
