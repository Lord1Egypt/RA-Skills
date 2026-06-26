#!/usr/bin/env python3
"""
BLS Query Script - Query Baidu Log Service via API.

AK/SK Resolution Order:
    1. Command line args: --ak / --sk
    2. Environment variables: BCE_BLS_ACCESS_KEY / BCE_BLS_SECRET_KEY
    3. Config file: ~/.bce_bls/credentials (INI format)

Usage:
    python3 bls_query.py --region <region> <command> [options]

Commands:
    list-projects    List all projects
    list-logstores   List logstores in a project
    describe-index   Get index details for a logstore
    query            Query log records

Examples:
    # Using environment variables (recommended)
    export BCE_BLS_ACCESS_KEY=xxx BCE_BLS_SECRET_KEY=xxx
    python3 bls_query.py --region bj list-logstores --project default

    # Using command line args
    python3 bls_query.py --ak xxx --sk xxx --region bj list-logstores --project default

    # Query logs (SQL)
    python3 bls_query.py --region bj query --project default --logstore my-logstore \\
        --start "2024-01-01T00:00:00Z" --end "2024-01-01T01:00:00Z" \\
        --query "select level, count(*) as cnt group by level order by cnt desc limit 10"
"""

import argparse
import configparser
import hashlib
import hmac
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


ENDPOINTS = {
    "bj": "bls-log.bj.baidubce.com",
    "gz": "bls-log.gz.baidubce.com",
    "su": "bls-log.su.baidubce.com",
    "bd": "bls-log.bd.baidubce.com",
    "fwh": "bls-log.fwh.baidubce.com",
    "hkg": "bls-log.hkg.baidubce.com",
    "cd": "bls-log.cd.baidubce.com",
    "nj": "bls-log.nj.baidubce.com",
    "yq": "bls-log.yq.baidubce.com",
}

ERROR_HINTS = {
    401: "鉴权失败。请检查：\n"
         "  1. AK/SK 是否正确且未过期\n"
         "  2. IAM 子用户是否有 BLS 访问权限\n"
         "  3. AK/SK 来源：--ak/--sk 参数 > BCE_BLS_ACCESS_KEY/BCE_BLS_SECRET_KEY 环境变量 > ~/.bce_bls/credentials 文件",
    403: "权限不足。当前 AK/SK 对应的用户没有该资源的操作权限，请检查 IAM 策略配置。",
    404: "资源不存在。请检查 project、logstore 名称是否正确。",
    400: "请求参数错误。请检查查询语句语法、时间格式等。",
}


def resolve_credentials(args):
    """Resolve AK/SK credentials from multiple sources.

    Resolution order:
        1. Command line args (--ak / --sk)
        2. Environment variables (BCE_BLS_ACCESS_KEY / BCE_BLS_SECRET_KEY)
        3. Config file (~/.bce_bls/credentials)

    Args:
        args: Parsed argparse namespace containing optional ak/sk attributes.

    Returns:
        A tuple of (access_key, secret_key).

    Exits:
        Prints error message and exits with code 1 if no credentials found.
    """
    ak = getattr(args, "ak", None)
    sk = getattr(args, "sk", None)

    # 1. Command line args
    if ak and sk:
        return ak, sk

    # 2. Environment variables
    ak = ak or os.environ.get("BCE_BLS_ACCESS_KEY")
    sk = sk or os.environ.get("BCE_BLS_SECRET_KEY")
    if ak and sk:
        return ak, sk

    # 3. Config file ~/.bce_bls/credentials
    cred_file = Path.home() / ".bce_bls" / "credentials"
    if cred_file.exists():
        config = configparser.ConfigParser()
        config.read(str(cred_file))
        profile = os.environ.get("BCE_BLS_PROFILE", "default")
        if config.has_section(profile):
            ak = ak or config.get(profile, "bce_access_key_id", fallback=None)
            sk = sk or config.get(profile, "bce_secret_access_key", fallback=None)
            if ak and sk:
                return ak, sk

    # Failed
    print(
        "错误：未找到 AK/SK。请通过以下方式之一提供：\n"
        "  1. 命令行参数：--ak <AK> --sk <SK>\n"
        "  2. 环境变量：export BCE_BLS_ACCESS_KEY=xxx BCE_BLS_SECRET_KEY=xxx\n"
        "  3. 配置文件：~/.bce_bls/credentials (INI 格式，包含 bce_access_key_id 和 bce_secret_access_key)",
        file=sys.stderr,
    )
    sys.exit(1)


def sign_request(ak, sk, method, path, headers, params, timestamp, expiration=1800):
    """Generate BCE auth v1 signature for API request.

    Args:
        ak: Access Key ID.
        sk: Secret Access Key.
        method: HTTP method (e.g. "GET", "POST").
        path: Request URI path.
        headers: Dict of HTTP headers.
        params: Dict of query parameters.
        timestamp: ISO8601 UTC timestamp string.
        expiration: Signature expiration time in seconds, defaults to 1800.

    Returns:
        Authorization header string in BCE auth v1 format.
    """
    auth_string_prefix = f"bce-auth-v1/{ak}/{timestamp}/{expiration}"
    signing_key = hmac.new(
        sk.encode("utf-8"), auth_string_prefix.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    canonical_uri = urllib.parse.quote(path, safe="/")

    sorted_params = sorted(params.items())
    canonical_querystring = "&".join(
        f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(str(v), safe='')}"
        for k, v in sorted_params
    )

    headers_to_sign = {}
    for k, v in headers.items():
        key_lower = k.lower().strip()
        if key_lower in ("host", "content-type") or key_lower.startswith("x-bce-"):
            headers_to_sign[key_lower] = v.strip()

    sorted_headers = sorted(headers_to_sign.items())
    canonical_headers = "\n".join(
        f"{urllib.parse.quote(k, safe='')}:{urllib.parse.quote(v, safe='')}"
        for k, v in sorted_headers
    )
    signed_headers = ";".join(k for k, _ in sorted_headers)

    canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}"
    signature = hmac.new(
        signing_key.encode("utf-8"),
        canonical_request.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return f"bce-auth-v1/{ak}/{timestamp}/{expiration}/{signed_headers}/{signature}"


def make_request(ak, sk, endpoint, method, path, params=None, body=None):
    """Make an authenticated HTTP request to the BLS API.

    Args:
        ak: Access Key ID.
        sk: Secret Access Key.
        endpoint: BLS API endpoint hostname.
        method: HTTP method (e.g. "GET", "POST").
        path: Request URI path.
        params: Optional dict of query parameters.
        body: Optional dict to send as JSON request body (for POST requests).

    Returns:
        Parsed JSON response as a dict.

    Exits:
        Prints error message and exits with code 1 on HTTP or network errors.
    """
    if params is None:
        params = {}

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    headers = {
        "Host": endpoint,
        "x-bce-date": timestamp,
        "Content-Type": "application/json; charset=utf-8",
    }

    auth = sign_request(ak, sk, method, path, headers, params, timestamp)
    headers["Authorization"] = auth

    query_string = "&".join(
        f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(str(v), safe='')}"
        for k, v in params.items()
    )
    url = f"https://{endpoint}{path}"
    if query_string:
        url += f"?{query_string}"

    req = urllib.request.Request(url, headers=headers, method=method)
    if body is not None:
        req.data = json.dumps(body).encode("utf-8")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        hint = ERROR_HINTS.get(e.code, "")
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        if hint:
            print(f"\n提示：{hint}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误：{e.reason}", file=sys.stderr)
        print(f"请检查网络连接和 endpoint: {endpoint}", file=sys.stderr)
        sys.exit(1)


def list_projects(ak, sk, args):
    """List all projects in the specified region.

    Args:
        ak: Access Key ID.
        sk: Secret Access Key.
        args: Parsed argparse namespace with region, page_no, page_size, and optional name.
    """
    endpoint = ENDPOINTS[args.region]
    body = {"pageNo": args.page_no, "pageSize": args.page_size}
    if args.name:
        body["name"] = args.name
    result = make_request(ak, sk, endpoint, "POST", "/v1/project/list", body=body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def list_logstores(ak, sk, args):
    """List logstores, optionally filtered by project or logstore name.

    Args:
        ak: Access Key ID.
        sk: Secret Access Key.
        args: Parsed argparse namespace with region, page_no, page_size,
              and optional project and logstore_name.
    """
    endpoint = ENDPOINTS[args.region]
    params = {"pageNo": args.page_no, "pageSize": args.page_size}
    if args.project:
        params["project"] = args.project
    if args.logstore_name:
        params["namePattern"] = args.logstore_name
    result = make_request(ak, sk, endpoint, "GET", "/v1/logstore", params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def describe_index(ak, sk, args):
    """Get index configuration details for a logstore.

    Args:
        ak: Access Key ID.
        sk: Secret Access Key.
        args: Parsed argparse namespace with region, logstore, and optional project.
    """
    endpoint = ENDPOINTS[args.region]
    params = {}
    if args.project:
        params["project"] = args.project
    path = f"/v1/logstore/{urllib.parse.quote(args.logstore, safe='')}/index"
    result = make_request(ak, sk, endpoint, "GET", path, params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def query_logs(ak, sk, args):
    """Query log records from a logstore using search or SQL statements.

    If --start and --end are not provided, defaults to the last 1 hour.
    Supports pagination via --marker for search (match) queries.

    Args:
        ak: Access Key ID.
        sk: Secret Access Key.
        args: Parsed argparse namespace with region, logstore, query,
              and optional project, start, end, limit, sort, marker.
    """
    endpoint = ENDPOINTS[args.region]
    now = datetime.now(timezone.utc)
    start_time = args.start if args.start else (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = args.end if args.end else now.strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {
        "query": args.query,
        "startDateTime": start_time,
        "endDateTime": end_time,
    }
    if args.project:
        params["project"] = args.project
    if args.limit:
        params["limit"] = args.limit
    if args.sort:
        params["sort"] = args.sort
    if args.marker:
        params["marker"] = args.marker

    path = f"/v1/logstore/{urllib.parse.quote(args.logstore, safe='')}/logrecord"
    result = make_request(ak, sk, endpoint, "GET", path, params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    """Entry point for the BLS query CLI tool.

    Parses command line arguments and dispatches to the appropriate
    subcommand handler (list-projects, list-logstores, describe-index, query).
    """
    parser = argparse.ArgumentParser(
        description="BLS Query Tool - 百度日志服务查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="AK/SK 解析顺序: --ak/--sk 参数 > BCE_BLS_ACCESS_KEY/BCE_BLS_SECRET_KEY 环境变量 > ~/.bce_bls/credentials 文件",
    )
    parser.add_argument("--ak", help="Access Key ID (也可通过 BCE_BLS_ACCESS_KEY 环境变量设置)")
    parser.add_argument("--sk", help="Secret Access Key (也可通过 BCE_BLS_SECRET_KEY 环境变量设置)")
    parser.add_argument(
        "--region",
        required=True,
        choices=list(ENDPOINTS.keys()),
        help="Region (bj/gz/su/bd/fwh/hkg/nj/yq/cd)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # list-projects
    p_lp = subparsers.add_parser("list-projects", help="List projects")
    p_lp.add_argument("--name", help="Filter by project name")
    p_lp.add_argument("--page-no", type=int, default=1)
    p_lp.add_argument("--page-size", type=int, default=10)

    # list-logstores
    p_ls = subparsers.add_parser("list-logstores", help="List logstores")
    p_ls.add_argument("--project", help="Project name")
    p_ls.add_argument("--logstore-name", help="Filter by logstore name")
    p_ls.add_argument("--page-no", type=int, default=1)
    p_ls.add_argument("--page-size", type=int, default=100)

    # describe-index
    p_di = subparsers.add_parser("describe-index", help="Get index details")
    p_di.add_argument("--project", help="Project name")
    p_di.add_argument("--logstore", required=True, help="LogStore name")

    # query
    p_q = subparsers.add_parser("query", help="Query log records")
    p_q.add_argument("--project", help="Project name")
    p_q.add_argument("--logstore", required=True, help="LogStore name")
    p_q.add_argument("--query", required=True, help="Query statement")
    p_q.add_argument("--start", help="Start time (ISO8601 UTC, default: 1 hour ago)")
    p_q.add_argument("--end", help="End time (ISO8601 UTC, default: now)")
    p_q.add_argument("--limit", type=int, help="Max records (0-1000)")
    p_q.add_argument("--sort", choices=["asc", "desc"], help="Sort order")
    p_q.add_argument("--marker", help="Marker for pagination (only for search queries, from nextMarker in response)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    ak, sk = resolve_credentials(args)

    cmd_map = {
        "list-projects": list_projects,
        "list-logstores": list_logstores,
        "describe-index": describe_index,
        "query": query_logs,
    }
    cmd_map[args.command](ak, sk, args)


if __name__ == "__main__":
    main()
