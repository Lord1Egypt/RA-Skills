import sys
import json
import requests

BASE_URL = "http://10.168.1.162:9000"

ALLOWED_ENDPOINTS = [
    "bigamountvoutv3e",
    "dailyindsv3e1",
    "dailyindsv3e2",
    "holder3",
    "holder_balance3",
    "realtimeindsv3",
    "rt_bigamountvoutv3e",
    "rt_dailyindsv3e1",
    "rt_dailyindsv3e2",
    "utxos3nd",
    "utxosv3",
    "utxosv4"
]


def call_api(endpoint, field=None, params=None):
    """
    endpoint = 表名
    field = 字段名（可选）
    params = limit / date / dict
    """

    if endpoint not in ALLOWED_ENDPOINTS:
        print(f"Error: endpoint '{endpoint}' not allowed.")
        sys.exit(1)

    # -------- 构建URL --------
    if field:
        url = f"{BASE_URL}/db/btcdb/table/{endpoint}/field/{field}"
    else:
        url = f"{BASE_URL}/db/btcdb/table/{endpoint}"

    # -------- 参数处理 --------
    if params is not None:
        if isinstance(params, dict):
            for k, v in params.items():
                url += f"?{k}={v}" if "?" not in url else f"&{k}={v}"

        elif isinstance(params, int):
            url += f"?limit={params}"

        elif isinstance(params, str):
            url += f"?date={params}"

        else:
            print("Error: params must be dict, int, or date string")
            sys.exit(1)

    # -------- 请求 --------
    try:
        resp = requests.get(url)
        data = resp.json()
    except Exception as e:
        print(f"Error fetching API: {e}")
        sys.exit(1)

    print(json.dumps(data, indent=2, ensure_ascii=False))


# ===================== CLI =====================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python btc_api.py <table>")
        print("  python btc_api.py <table> <limit>")
        print("  python btc_api.py <table> <YYYY-MM-DD>")
        print("  python btc_api.py <table> <field>")
        print("  python btc_api.py <table> <field> <limit|date>")
        sys.exit(1)

    endpoint = sys.argv[1]
    field = None
    params = None

    # -------- 判断参数结构 --------
    if len(sys.argv) == 2:
        pass

    elif len(sys.argv) == 3:
        arg = sys.argv[2]

        # 判断是不是数字
        try:
            params = int(arg)
        except:
            # 可能是字段，也可能是日期
            if "-" in arg:
                params = arg
            else:
                field = arg

    elif len(sys.argv) == 4:
        field = sys.argv[2]
        arg = sys.argv[3]

        try:
            params = int(arg)
        except:
            params = arg

    call_api(endpoint, field, params)