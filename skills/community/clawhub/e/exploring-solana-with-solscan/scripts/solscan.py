import argparse
import sys
import json
import os
import requests

BASE_URL = "https://pro-api.solscan.io/v2.0"

def get_api_key():
    api_key = os.environ.get("SOLSCAN_API_KEY")
    if not api_key:
        print("Error: SOLSCAN_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return api_key

def make_request(endpoint, params=None):
    api_key = get_api_key()
    headers = {
        "token": api_key,
        "User-Agent": "Agent-Skill/1.0"
    }
    url = f"{BASE_URL}{endpoint}"
    # Remove None values
    if params:
        params = {k: v for k, v in params.items() if v is not None}
        
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response Body: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def print_result(data):
    print(json.dumps(data, indent=2))

# --- Account Commands ---
def setup_account_parser(subparsers):
    parser = subparsers.add_parser('account', help='Account operations')
    sp = parser.add_subparsers(dest='action', required=True)

    sp.add_parser('detail', help='Get account details').add_argument('--address', required=True)
    sp.add_parser('data-decoded', help='Get decoded data').add_argument('--address', required=True)
    
    p_tokens = sp.add_parser('tokens', help='Get token accounts')
    p_tokens.add_argument('--address', required=True)
    p_tokens.add_argument('--type', required=True, choices=['token', 'nft'], help='Type of token: token or nft')
    p_tokens.add_argument('--page', type=int, default=1)
    p_tokens.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40], help='Items per page: 10, 20, 30, or 40')
    p_tokens.add_argument('--hide-zero', action='store_true', help='Filter tokens with zero amount')

    p_txs = sp.add_parser('transactions', help='Get account transactions')
    p_txs.add_argument('--address', required=True)
    p_txs.add_argument('--before', help='Cursor for pagination (transaction signature)')
    p_txs.add_argument('--limit', type=int, default=10, choices=[10, 20, 30, 40], help='Number of transactions')
    
    p_transfers = sp.add_parser('transfer', help='Get transfers')
    p_transfers.add_argument('--address', required=True)
    p_transfers.add_argument('--activity-type', help='Activity type (comma-separated): ACTIVITY_SPL_TRANSFER,ACTIVITY_SPL_BURN,ACTIVITY_SPL_MINT,etc')
    p_transfers.add_argument('--token-account', help='Filter by specific token account address')
    p_transfers.add_argument('--from', help='Filter from address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--exclude-from', help='Exclude from address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--to', help='Filter to address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--exclude-to', help='Exclude to address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--token', help='Filter by token address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--amount', nargs=2, type=float, help='Amount range (min max)')
    p_transfers.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_transfers.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_transfers.add_argument('--exclude-amount-zero', action='store_true', help='Exclude zero amount transfers')
    p_transfers.add_argument('--flow', choices=['in', 'out'], help='Transfer direction: in or out')
    p_transfers.add_argument('--page', type=int, default=1)
    p_transfers.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100], help='Items per page')
    p_transfers.add_argument('--sort-order', choices=['asc', 'desc'], default='desc', help='Sort order')
    p_transfers.add_argument('--value', nargs=2, type=float, help='Value range in USD (min max)')

    p_stake = sp.add_parser('stake', help='Get stake accounts')
    p_stake.add_argument('--address', required=True)
    p_stake.add_argument('--page', type=int, default=1)
    p_stake.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40], help='Items per page')
    p_stake.add_argument('--sort-by', default='active_stake', choices=['active_stake', 'delegated_stake'], help='Sort by field')
    p_stake.add_argument('--sort-order', choices=['asc', 'desc'], help='Sort order: asc or desc')
    p_portfolio = sp.add_parser('portfolio', help='Get portfolio')
    p_portfolio.add_argument('--address', required=True)
    p_portfolio.add_argument('--exclude-low-score-tokens', action='store_true', help='Exclude low score tokens')

    p_defi = sp.add_parser('defi', help='Get DeFi activities')
    p_defi.add_argument('--address', required=True)
    p_defi.add_argument('--activity-type', help='Filter by activity type(s) (comma-separated): ACTIVITY_TOKEN_SWAP,ACTIVITY_AGG_TOKEN_SWAP,etc')
    p_defi.add_argument('--from', help='Filter from address')
    p_defi.add_argument('--platform', help='Filter by platform(s) (comma-separated, max 5)')
    p_defi.add_argument('--source', help='Filter by source(s) (comma-separated, max 5)')
    p_defi.add_argument('--token', help='Filter by token address')
    p_defi.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_defi.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_defi.add_argument('--page', type=int, default=1)
    p_defi.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    p_defi.add_argument('--sort-by', default='block_time', choices=['block_time'], help='Sort by field (default: block_time)')
    p_defi.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order: asc or desc (default: desc)')

    p_defi_export = sp.add_parser('defi-export', help='Export DeFi activities')
    p_defi_export.add_argument('--address', required=True)
    p_defi_export.add_argument('--activity-type', help='Activity type filter (comma-separated): ACTIVITY_TOKEN_SWAP,ACTIVITY_AGG_TOKEN_SWAP,etc')
    p_defi_export.add_argument('--from', help='Filter activities from an address')
    p_defi_export.add_argument('--platform', help='Filter by platform(s) (comma-separated, max 5)')
    p_defi_export.add_argument('--source', help='Filter by source(s) (comma-separated, max 5)')
    p_defi_export.add_argument('--token', help='Filter by token address')
    p_defi_export.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_defi_export.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_defi_export.add_argument('--sort-by', default='block_time', choices=['block_time'], help='Sort by field (default: block_time)')
    p_defi_export.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order: asc or desc (default: desc)')

    p_balance = sp.add_parser('balance-change', help='Get balance changes')
    p_balance.add_argument('--address', required=True)
    p_balance.add_argument('--token-account', help='Filter by token account address')
    p_balance.add_argument('--token', help='Filter by token address')
    p_balance.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_balance.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_balance.add_argument('--amount', nargs=2, type=float, help='Amount range (min max)')
    p_balance.add_argument('--flow', choices=['in', 'out'], help='Transfer direction: in or out')
    p_balance.add_argument('--remove-spam', choices=['true', 'false'], help='Remove spam transactions')
    p_balance.add_argument('--page', type=int, default=1)
    p_balance.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    p_balance.add_argument('--sort-by', default='block_time', choices=['block_time'], help='Sort by field (default: block_time)')
    p_balance.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order: asc or desc (default: desc)')

    p_reward_export = sp.add_parser('reward-export', help='Export stake rewards (max 5000 items, max 1 req/min)')
    p_reward_export.add_argument('--address', required=True)
    p_reward_export.add_argument('--time-from', type=int, help='Start time (Unix timestamp in seconds, default: 1 month before time-to)')
    p_reward_export.add_argument('--time-to', type=int, help='End time (Unix timestamp in seconds, default: current time)')

    p_transfer_export = sp.add_parser('transfer-export', help='Export transfers (max 5000 items, max 1 req/min)')
    p_transfer_export.add_argument('--address', required=True)
    p_transfer_export.add_argument('--activity-type', help='Activity type filter (comma-separated): ACTIVITY_SPL_TRANSFER,ACTIVITY_SPL_BURN,etc')
    p_transfer_export.add_argument('--token-account', help='Filter by specific token account address')
    p_transfer_export.add_argument('--from', help='Filter from address')
    p_transfer_export.add_argument('--to', help='Filter to address')
    p_transfer_export.add_argument('--token', help='Filter by token address')
    p_transfer_export.add_argument('--amount', nargs=2, type=float, help='Amount range (min max)')
    p_transfer_export.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_transfer_export.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_transfer_export.add_argument('--exclude-amount-zero', action='store_true', help='Exclude zero amount transfers')
    p_transfer_export.add_argument('--flow', choices=['in', 'out'], help='Transfer direction: in or out')
    
    sp.add_parser('metadata', help='Get metadata').add_argument('--address', required=True)
    sp.add_parser('metadata-multi', help='Get multiple metadata').add_argument('--addresses', required=True, help='Comma separated addresses')

    p_leader = sp.add_parser('leaderboard', help='Get leaderboard')
    p_leader.add_argument('--sort-by', default='total_values', choices=['sol_values', 'stake_values', 'token_values', 'total_values'], help='Sort by field (default: total_values)')
    p_leader.add_argument('--sort-order', choices=['asc', 'desc'], help='Sort order: asc or desc')
    p_leader.add_argument('--page', type=int, default=1)
    p_leader.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])

def handle_account(args):
    if args.action == 'detail': return make_request("/account/detail", {"address": args.address})
    elif args.action == 'data-decoded': return make_request("/account/data-decoded", {"address": args.address})
    elif args.action == 'tokens': return make_request("/account/token-accounts", {"address": args.address, "type": args.type, "page": args.page, "page_size": args.page_size, "hide_zero": args.hide_zero})
    elif args.action == 'transactions':
        params = {"address": args.address, "limit": args.limit}
        if args.before: params["before"] = args.before
        return make_request("/account/transactions", params)
    elif args.action == 'transfer':
        params = {
            "address": args.address,
            "page": args.page,
            "page_size": args.page_size,
            "sort_order": args.sort_order
        }
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if args.token_account: params["token_account"] = args.token_account
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.exclude_from: params["exclude_from"] = args.exclude_from
        if getattr(args, 'to'): params["to"] = getattr(args, 'to')
        if args.exclude_to: params["exclude_to"] = args.exclude_to
        if args.token: params["token"] = args.token
        if args.amount: params["amount"] = args.amount
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        if args.exclude_amount_zero: params["exclude_amount_zero"] = args.exclude_amount_zero
        if args.flow: params["flow"] = args.flow
        if args.value: params["value"] = args.value
        return make_request("/account/transfer", params)
    elif args.action == 'stake':
        params = {
            "address": args.address,
            "page": args.page,
            "page_size": args.page_size,
            "sort_by": args.sort_by
        }
        if args.sort_order: params["sort_order"] = args.sort_order
        return make_request("/account/stake", params)
    elif args.action == 'portfolio':
        params = {"address": args.address}
        if args.exclude_low_score_tokens: params["exclude_low_score_tokens"] = args.exclude_low_score_tokens
        return make_request("/account/portfolio", params)
    elif args.action == 'defi':
        params = {"address": args.address, "page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.platform: params["platform"] = args.platform.split(',')
        if args.source: params["source"] = args.source.split(',')
        if args.token: params["token"] = args.token
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/account/defi/activities", params)
    elif args.action == 'defi-export':
        params = {"address": args.address, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.platform: params["platform"] = args.platform.split(',')
        if args.source: params["source"] = args.source.split(',')
        if args.token: params["token"] = args.token
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/account/defi/activities/export", params)
    elif args.action == 'balance-change':
        params = {"address": args.address, "page": args.page, "page_size": args.page_size, "sort_order": args.sort_order}
        if args.token_account: params["token_account"] = args.token_account
        if args.token: params["token"] = args.token
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        if args.amount: params["amount"] = args.amount
        if args.flow: params["flow"] = args.flow
        if args.remove_spam: params["remove_spam"] = args.remove_spam
        params["sort_by"] = args.sort_by
        return make_request("/account/balance_change", params)
    elif args.action == 'reward-export':
        params = {"address": args.address}
        if args.time_from: params["time_from"] = args.time_from
        if args.time_to: params["time_to"] = args.time_to
        return make_request("/account/reward/export", params)
    elif args.action == 'transfer-export':
        params = {"address": args.address}
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if args.token_account: params["token_account"] = args.token_account
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if getattr(args, 'to'): params["to"] = getattr(args, 'to')
        if args.token: params["token"] = args.token
        if args.amount: params["amount"] = args.amount
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        if args.exclude_amount_zero: params["exclude_amount_zero"] = args.exclude_amount_zero
        if args.flow: params["flow"] = args.flow
        return make_request("/account/transfer/export", params)
    elif args.action == 'metadata': return make_request("/account/metadata", {"address": args.address})
    elif args.action == 'metadata-multi': return make_request("/account/metadata/multi", {"address": args.addresses})
    elif args.action == 'leaderboard':
        params = {"page": args.page, "page_size": args.page_size, "sort_by": args.sort_by}
        if args.sort_order: params["sort_order"] = args.sort_order
        return make_request("/account/leaderboard", params)

# --- Token Commands ---
def setup_token_parser(subparsers):
    parser = subparsers.add_parser('token', help='Token operations')
    sp = parser.add_subparsers(dest='action', required=True)

    sp.add_parser('meta', help='Get metadata').add_argument('--address', required=True)
    sp.add_parser('meta-multi', help='Get multiple metadata').add_argument('--addresses', required=True)
    
    p_holders = sp.add_parser('holders', help='Get holders')
    p_holders.add_argument('--address', required=True)
    p_holders.add_argument('--page', type=int, default=1)
    p_holders.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40])
    p_holders.add_argument('--from-amount', help='Minimum token holding amount (string format)')
    p_holders.add_argument('--to-amount', help='Maximum token holding amount (string format)')
    
    p_price = sp.add_parser('price', help='[DEPRECATED] Get price (use historical instead)')
    p_price.add_argument('--address', required=True)
    p_price.add_argument('--from-time', help='Start time in YYYYMMDD format')
    p_price.add_argument('--to-time', help='End time in YYYYMMDD format')

    p_price_multi = sp.add_parser('price-multi', help='[DEPRECATED] Get multiple prices (use price-history instead)')
    p_price_multi.add_argument('--addresses', required=True, help='Token addresses, comma-separated (max 50)')
    p_price_multi.add_argument('--from-time', help='Start time in YYYYMMDD format')
    p_price_multi.add_argument('--to-time', help='End time in YYYYMMDD format')

    p_price_latest = sp.add_parser('price-latest', help='Get latest prices for multiple tokens')
    p_price_latest.add_argument('--addresses', required=True, help='Token addresses, comma-separated (max 50)')

    p_price_history = sp.add_parser('price-history', help='Get historical prices for multiple tokens')
    p_price_history.add_argument('--addresses', required=True, help='Token addresses, comma-separated (max 50)')
    p_price_history.add_argument('--from-time', help='Start time in YYYYMMDD format')
    p_price_history.add_argument('--to-time', help='End time in YYYYMMDD format')

    p_market = sp.add_parser('markets', help='Get markets')
    p_market.add_argument('--token', required=True, help='Token address(es): 1 token for all markets, 2 tokens (comma-separated) for pair search')
    p_market.add_argument('--sort-by', choices=['volume', 'trade', 'tvl', 'trader'], help='Sort by field')
    p_market.add_argument('--program', help='Filter by program address(es) (comma-separated, max 5)')
    p_market.add_argument('--page', type=int, default=1)
    p_market.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    
    sp.add_parser('trending', help='Get trending').add_argument('--limit', type=int, default=10)

    p_list = sp.add_parser('list', help='List tokens')
    p_list.add_argument('--page', type=int, default=1)
    p_list.add_argument('--page-size', type=int, default=10)
    p_list.add_argument('--sort-by', default='holder', choices=['holder', 'market_cap', 'created_time'], help='Sort field')
    p_list.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order')

    sp.add_parser('top', help='Get top tokens')
    p_latest = sp.add_parser('latest', help='Get latest tokens')
    p_latest.add_argument('--platform-id', help='Filter by platform', choices=['jupiter','lifinity','meteora','orca','raydium','phoenix','sanctum','kamino','pumpfun','openbook','apepro','stabble','jupiterdca','jupiter_limit_order','solfi','zerofi','letsbonkfun_launchpad','raydium_launchlab','believe_launchpad','moonshot_launchpad','jup_studio_launchpad','bags_launchpad'])
    p_latest.add_argument('--page', type=int, default=1)
    p_latest.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    
    p_transfer = sp.add_parser('transfers', help='Get token transfers')
    p_transfer.add_argument('--address', required=True)
    p_transfer.add_argument('--activity-type', help='Transfer type filter (comma-separated): ACTIVITY_SPL_TRANSFER,ACTIVITY_SPL_BURN,ACTIVITY_SPL_MINT,etc')
    p_transfer.add_argument('--from', help='Filter from address(es) (max 5, comma-separated)')
    p_transfer.add_argument('--exclude-from', help='Exclude from address(es) (max 5, comma-separated)')
    p_transfer.add_argument('--to', help='Filter to address(es) (max 5, comma-separated)')
    p_transfer.add_argument('--exclude-to', help='Exclude to address(es) (max 5, comma-separated)')
    p_transfer.add_argument('--amount', nargs=2, type=float, help='Amount range (min max)')
    p_transfer.add_argument('--exclude-amount-zero', action='store_true', help='Exclude zero amount transfers')
    p_transfer.add_argument('--value', nargs=2, type=float, help='Value range in USD (min max)')
    p_transfer.add_argument('--page', type=int, default=1)
    p_transfer.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    p_transfer.add_argument('--sort-by', default='block_time', choices=['block_time'], help='Sort by field (default: block_time)')
    p_transfer.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order: asc or desc (default: desc)')

    p_defi = sp.add_parser('defi', help='Get DeFi activities')
    p_defi.add_argument('--address', required=True)
    p_defi.add_argument('--from', help='Filter activities from an address')
    p_defi.add_argument('--platform', help='Filter by platform(s) (comma-separated, max 5)')
    p_defi.add_argument('--source', help='Filter by source(s) (comma-separated, max 5)')
    p_defi.add_argument('--activity-type', help='Activity type filter (comma-separated): ACTIVITY_TOKEN_SWAP,ACTIVITY_AGG_TOKEN_SWAP,etc')
    p_defi.add_argument('--token', help='Filter by token address')
    p_defi.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_defi.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_defi.add_argument('--page', type=int, default=1)
    p_defi.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    p_defi.add_argument('--sort-by', default='block_time', choices=['block_time'], help='Sort by field (default: block_time)')
    p_defi.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order: asc or desc (default: desc)')

    p_defi_export = sp.add_parser('defi-export', help='Export DeFi activities')
    p_defi_export.add_argument('--address', required=True)
    p_defi_export.add_argument('--from', help='Filter activities from an address')
    p_defi_export.add_argument('--platform', help='Filter by platform(s) (comma-separated, max 5)')
    p_defi_export.add_argument('--source', help='Filter by source(s) (comma-separated, max 5)')
    p_defi_export.add_argument('--activity-type', help='Activity type filter (comma-separated): ACTIVITY_TOKEN_SWAP,ACTIVITY_AGG_TOKEN_SWAP,etc')
    p_defi_export.add_argument('--token', help='Filter by token address')
    p_defi_export.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_defi_export.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_defi_export.add_argument('--sort-by', default='block_time', choices=['block_time'], help='Sort by field (default: block_time)')
    p_defi_export.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order: asc or desc (default: desc)')
    
    p_hist = sp.add_parser('historical', help='Get historical price data')
    p_hist.add_argument('--address', required=True)
    p_hist.add_argument('--range', type=int, default=7, choices=[7, 30], help='Time range in days (7 or 30, default: 7)')

    p_search = sp.add_parser('search', help='Search tokens')
    p_search.add_argument('--keyword', required=True)
    p_search.add_argument('--search-mode', default='exact', choices=['exact', 'fuzzy'], help='Search mode (default: exact)')
    p_search.add_argument('--search-by', default='combination', choices=['combination', 'address', 'name', 'symbol'], help='Search field (default: combination)')
    p_search.add_argument('--exclude-unverified-token', action='store_true', help='Exclude unverified tokens')
    p_search.add_argument('--sort-by', default='reputation', choices=['reputation', 'market_cap', 'volume_24h'], help='Sort by field (default: reputation)')
    p_search.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order (default: desc)')
    p_search.add_argument('--page', type=int, default=1)
    p_search.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40])

def handle_token(args):
    if args.action == 'meta': return make_request("/token/meta", {"address": args.address})
    elif args.action == 'meta-multi': return make_request("/token/meta/multi", {"address": args.addresses})
    elif args.action == 'holders':
        params = {"address": args.address, "page": args.page, "page_size": args.page_size}
        if args.from_amount: params["from_amount"] = args.from_amount
        if args.to_amount: params["to_amount"] = args.to_amount
        return make_request("/token/holders", params)
    elif args.action == 'price':
        params = {"address": args.address}
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/token/price", params)
    elif args.action == 'price-multi':
        params = {"address": args.addresses.split(',') if args.addresses else []}
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/token/price/multi", params)
    elif args.action == 'price-latest':
        return make_request("/token/price/latest", {"address": args.addresses.split(',') if args.addresses else []})
    elif args.action == 'price-history':
        params = {"address": args.addresses.split(',') if args.addresses else []}
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/token/price/history", params)
    elif args.action == 'markets':
        params = {
            "token": args.token.split(',') if args.token else [],
            "page": args.page,
            "page_size": args.page_size
        }
        if args.program: params["program"] = args.program.split(',')
        if args.sort_by: params["sort_by"] = args.sort_by
        return make_request("/token/markets", params)
    elif args.action == 'trending': return make_request("/token/trending", {"limit": args.limit})
    elif args.action == 'list': return make_request("/token/list", {"page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order})
    elif args.action == 'top': return make_request("/token/top")
    elif args.action == 'latest':
        params = {"page": args.page, "page_size": args.page_size}
        if args.platform_id: params["platform_id"] = args.platform_id
        return make_request("/token/latest", params)
    elif args.action == 'transfers':
        params = {"address": args.address, "page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.exclude_from: params["exclude_from"] = args.exclude_from
        if getattr(args, 'to'): params["to"] = getattr(args, 'to')
        if args.exclude_to: params["exclude_to"] = args.exclude_to
        if args.amount: params["amount"] = args.amount
        if args.exclude_amount_zero: params["exclude_amount_zero"] = args.exclude_amount_zero
        if args.value: params["value"] = args.value
        return make_request("/token/transfer", params)
    elif args.action == 'defi':
        params = {"address": args.address, "page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.platform: params["platform"] = args.platform.split(',')
        if args.source: params["source"] = args.source.split(',')
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if args.token: params["token"] = args.token
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/token/defi/activities", params)
    elif args.action == 'defi-export':
        params = {"address": args.address, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.platform: params["platform"] = args.platform.split(',')
        if args.source: params["source"] = args.source.split(',')
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if args.token: params["token"] = args.token
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/token/defi/activities/export", params)
    elif args.action == 'historical':
        params = {"address": args.address, "range": args.range}
        return make_request("/token/historical-data", params)
    elif args.action == 'search':
        params = {"keyword": args.keyword, "page": args.page, "page_size": args.page_size, "search_mode": args.search_mode, "search_by": args.search_by, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if args.exclude_unverified_token: params["exclude_unverified_token"] = args.exclude_unverified_token
        return make_request("/token/search", params)


# --- Transaction Commands ---
def setup_transaction_parser(subparsers):
    parser = subparsers.add_parser('transaction', help='Transaction operations')
    sp = parser.add_subparsers(dest='action', required=True)

    sp.add_parser('detail', help='Get transaction details').add_argument('--tx', required=True, help='Transaction signature')

    p_detail_multi = sp.add_parser('detail-multi', help='Get multiple transaction details')
    p_detail_multi.add_argument('--txs', required=True, help='Transaction signatures, comma-separated (max 50)')

    p_last = sp.add_parser('last', help='Get last transactions')
    p_last.add_argument('--limit', type=int, default=10, choices=[10, 20, 30, 40, 60, 100], help='Number of transactions (10, 20, 30, 40, 60, 100, default: 10)')
    p_last.add_argument('--filter', default='exceptVote', choices=['exceptVote', 'all'], help='Filter type (exceptVote, all, default: exceptVote)')

    p_actions = sp.add_parser('actions', help='Get transaction actions/decoded instructions')
    p_actions.add_argument('--tx', required=True, help='Transaction signature')

    p_actions_m = sp.add_parser('actions-multi', help='Get multiple transaction actions')
    p_actions_m.add_argument('--txs', required=True, help='Transaction signatures, comma-separated (max 50)')

    sp.add_parser('fees', help='Get network fees statistics')

def handle_transaction(args):
    if args.action == 'detail': return make_request("/transaction/detail", {"tx": args.tx})
    elif args.action == 'detail-multi': return make_request("/transaction/detail/multi", {"tx": args.txs})
    elif args.action == 'last':
        params = {"limit": args.limit, "filter": args.filter}
        return make_request("/transaction/last", params)
    elif args.action == 'actions': return make_request("/transaction/actions", {"tx": args.tx})
    elif args.action == 'actions-multi': return make_request("/transaction/actions/multi", {"tx": args.txs})
    elif args.action == 'fees': return make_request("/transaction/fees")


# --- NFT Commands ---
def setup_nft_parser(subparsers):
    parser = subparsers.add_parser('nft', help='NFT operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    p_news = sp.add_parser('news', help='Get NFT news/activities')
    p_news.add_argument('--filter', required=True, choices=['created_time'], help='Filter type (default: created_time)')
    p_news.add_argument('--page', type=int, default=1)
    p_news.add_argument('--page-size', type=int, default=12, choices=[12, 24, 36])
    
    p_act = sp.add_parser('activities', help='Get NFT activities')
    p_act.add_argument('--from', help='Filter from address')
    p_act.add_argument('--to', help='Filter to address')
    p_act.add_argument('--source', help='Filter by source address(es) (comma-separated, max 5)')
    p_act.add_argument('--activity-type', help='Filter by activity type (comma-separated): ACTIVITY_NFT_SOLD,ACTIVITY_NFT_LISTING,ACTIVITY_NFT_BIDDING,ACTIVITY_NFT_CANCEL_BID,ACTIVITY_NFT_CANCEL_LIST,ACTIVITY_NFT_REJECT_BID,ACTIVITY_NFT_UPDATE_PRICE,ACTIVITY_NFT_LIST_AUCTION')
    p_act.add_argument('--token', help='Filter by token address')
    p_act.add_argument('--collection', help='Filter by collection')
    p_act.add_argument('--currency-token', help='Currency token address')
    p_act.add_argument('--price', nargs=2, type=float, help='Price range filter (min max, requires currency_token parameter)')
    p_act.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_act.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_act.add_argument('--block-time', nargs=2, type=int, help='[DEPRECATED] Use from-time/to-time instead')
    p_act.add_argument('--page', type=int, default=1)
    p_act.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    
    p_cols = sp.add_parser('collections', help='Get NFT collections')
    p_cols.add_argument('--range', type=int, default=1, choices=[1, 7, 30], help='Days range (1, 7, or 30, default: 1)')
    p_cols.add_argument('--sort-by', default='volumes', choices=['items', 'floor_price', 'volumes'], help='Sort field (default: volumes)')
    p_cols.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order (default: desc)')
    p_cols.add_argument('--collection', help='Filter by collection ID')
    p_cols.add_argument('--page', type=int, default=1)
    p_cols.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40])
    
    p_items = sp.add_parser('items', help='Get NFT collection items')
    p_items.add_argument('--collection', required=True, help='Collection address (required)')
    p_items.add_argument('--sort-by', default='last_trade', choices=['last_trade', 'listing_price'], help='Sort field (default: last_trade)')
    p_items.add_argument('--page', type=int, default=1)
    p_items.add_argument('--page-size', type=int, default=12, choices=[12, 24, 36])

def handle_nft(args):
    if args.action == 'news': return make_request("/nft/news", {"filter": args.filter, "page": args.page, "page_size": args.page_size})
    elif args.action == 'activities':
        params = {"page": args.page, "page_size": args.page_size}
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if getattr(args, 'to'): params["to"] = getattr(args, 'to')
        if args.source: params["source"] = args.source.split(',') if args.source else None
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if args.token: params["token"] = args.token
        if args.collection: params["collection"] = args.collection
        if args.currency_token: params["currency_token"] = args.currency_token
        if args.price: params["price"] = args.price
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        if args.block_time: params["block_time"] = args.block_time
        return make_request("/nft/activities", params)
    elif args.action == 'collections':
        params = {"range": args.range, "sort_by": args.sort_by, "sort_order": args.sort_order, "page": args.page, "page_size": args.page_size}
        if args.collection: params["collection"] = args.collection
        return make_request("/nft/collection/lists", params)
    elif args.action == 'items':
        params = {"collection": args.collection, "sort_by": args.sort_by, "page": args.page, "page_size": args.page_size}
        return make_request("/nft/collection/items", params)


# --- Block Commands ---
def setup_block_parser(subparsers):
    parser = subparsers.add_parser('block', help='Block operations')
    sp = parser.add_subparsers(dest='action', required=True)

    p_last = sp.add_parser('last', help='Get the list of the latest blocks')
    p_last.add_argument('--limit', type=int, default=10, choices=[10, 20, 30, 40, 60, 100], help='Number of blocks to return: 10, 20, 30, 40, 60, or 100 (default: 10)')

    p_detail = sp.add_parser('detail', help='Get the details of a block')
    p_detail.add_argument('--block', required=True, type=int, help='The slot index of a block (required, minimum: 0)')

    p_txs = sp.add_parser('transactions', help='Get the list of transactions of a block')
    p_txs.add_argument('--block', required=True, type=int, help='The slot index of a block (required, minimum: 0)')
    p_txs.add_argument('--page', type=int, default=1, help='Page number for pagination (default: 1)')
    p_txs.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100], help='Number of items per page: 10, 20, 30, 40, 60, or 100 (default: 10)')
    p_txs.add_argument('--exclude-vote', action='store_true', help='Excludes vote transactions from the results')
    p_txs.add_argument('--program', help='The program used to filter transactions that interact with it (optional, string)')

def handle_block(args):
    if args.action == 'last': return make_request("/block/last", {"limit": args.limit})
    elif args.action == 'detail': return make_request("/block/detail", {"block": args.block})
    elif args.action == 'transactions':
        params = {"block": args.block, "page": args.page, "page_size": args.page_size}
        if args.exclude_vote: params["exclude_vote"] = args.exclude_vote
        if args.program: params["program"] = args.program
        return make_request("/block/transactions", params)


# --- Market Commands ---
def setup_market_parser(subparsers):
    parser = subparsers.add_parser('market', help='Market operations')
    sp = parser.add_subparsers(dest='action', required=True)

    p_mlist = sp.add_parser('list', help='List pool/markets')
    p_mlist.add_argument('--page', type=int, default=1, help='Page number (default: 1)')
    p_mlist.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100], help='Number of items per page (default: 10)')
    p_mlist.add_argument('--program', help='Program owner address')
    p_mlist.add_argument('--token-address', help='Token address involved in market')
    p_mlist.add_argument('--sort-by', default='volumes_24h', choices=['created_time', 'volumes_24h', 'trades_24h'], help='Sort field (default: volumes_24h)')
    p_mlist.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order (default: desc)')

    p_info = sp.add_parser('info', help='Get market pool details')
    p_info.add_argument('--address', required=True, help='Market ID/address')

    p_mvol = sp.add_parser('volume', help='Get historical market data')
    p_mvol.add_argument('--address', required=True, help='Market ID/address')
    p_mvol.add_argument('--time', nargs=2, help='Time range in YYYYMMDD format (e.g., 20240701 20240715)')

def handle_market(args):
    if args.action == 'list':
        params = {"page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if args.program: params["program"] = args.program
        if args.token_address: params["token_address"] = args.token_address
        return make_request("/market/list", params)
    elif args.action == 'info': return make_request("/market/info", {"address": args.address})
    elif args.action == 'volume':
        params = {"address": args.address}
        if args.time: params["time"] = args.time
        return make_request("/market/volume", params)

# --- Program Commands ---
def setup_program_parser(subparsers):
    parser = subparsers.add_parser('program', help='Program operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    p_list = sp.add_parser('list', help='List programs active in 90 days')
    p_list.add_argument('--page', type=int, default=1, help='Page number (default: 1)')
    p_list.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40], help='Items per page: 10, 20, 30, or 40 (default: 10)')
    p_list.add_argument('--sort-by', default='num_txs', choices=['num_txs','num_txs_success','interaction_volume','success_rate','active_users_24h'], help='Sort field (default: num_txs)')
    p_list.add_argument('--sort-order', choices=['asc', 'desc'], help='Sort order: asc or desc')

    sp.add_parser('popular-platforms', help='Get popular DeFi platforms')
    
    p_analytics = sp.add_parser('analytics', help='Get comprehensive on-chain analytics for a program')
    p_analytics.add_argument('--address', required=True, help='Program address on Solana blockchain (minimum: 30 characters)')
    p_analytics.add_argument('--range', type=int, required=True, choices=[7, 30], help='Analytics time range in days (7 or 30, required)')

def handle_program(args):
    if args.action == 'list':
        params = {"page": args.page, "page_size": args.page_size, "sort_by": args.sort_by}
        if args.sort_order: params["sort_order"] = args.sort_order
        return make_request("/program/list", params)
    elif args.action == 'popular-platforms': return make_request("/program/popular/platforms")
    elif args.action == 'analytics': return make_request("/program/analytics", {"address": args.address, "range": args.range})

# --- Monitor Commands ---
def setup_monitor_parser(subparsers):
    parser = subparsers.add_parser('monitor', help='Monitor operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    sp.add_parser('usage', help='Get API usage')

def handle_monitor(args):
    if args.action == 'usage': return make_request("/monitor/usage")

def main():
    parser = argparse.ArgumentParser(description="Solscan Pro CLI Tool")
    subparsers = parser.add_subparsers(dest='resource', required=True)

    setup_account_parser(subparsers)
    setup_token_parser(subparsers)
    setup_transaction_parser(subparsers)
    setup_nft_parser(subparsers)
    setup_block_parser(subparsers)
    setup_market_parser(subparsers)
    setup_program_parser(subparsers)
    setup_monitor_parser(subparsers)

    args = parser.parse_args()

    data = {}
    if args.resource == 'account': data = handle_account(args)
    elif args.resource == 'token': data = handle_token(args)
    elif args.resource == 'transaction': data = handle_transaction(args)
    elif args.resource == 'nft': data = handle_nft(args)
    elif args.resource == 'block': data = handle_block(args)
    elif args.resource == 'market': data = handle_market(args)
    elif args.resource == 'program': data = handle_program(args)
    elif args.resource == 'monitor': data = handle_monitor(args)

    print_result(data)

if __name__ == "__main__":
    main()
