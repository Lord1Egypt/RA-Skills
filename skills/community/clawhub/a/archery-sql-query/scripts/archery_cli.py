#!/usr/bin/env python3
import argparse
import json
import sys

from archery_client import ArcheryClient, ArcheryError


DEFAULT_SESSION_FILE = "~/.archery/cache/session.json"


def add_common_connection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--base-url",
        default="http://your-archery-server:9123",
        help="Archery base URL",
    )
    parser.add_argument(
        "--session-file",
        default=DEFAULT_SESSION_FILE,
        help="Session cookie file used by all commands",
    )
    parser.add_argument(
        "--timeout", type=int, default=15, help="HTTP timeout in seconds"
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification for https URLs",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )


def client_from_args(args: argparse.Namespace) -> ArcheryClient:
    client = ArcheryClient(
        base_url=args.base_url,
        timeout=args.timeout,
        verify=not args.insecure,
        session_file=args.session_file,
    )
    client.load_session()
    return client


def dump(data, pretty: bool) -> None:
    if pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Archery query helper CLI for login, metadata lookup, and query execution."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    login = subparsers.add_parser("login", help="Login and save session cookies")
    add_common_connection_args(login)
    login.add_argument("--username", required=True)
    login.add_argument("--password", required=True)
    login.add_argument("--otp")
    login.add_argument("--auth-type", choices=["totp", "sms"], default="totp")
    login.add_argument("--phone", default="")
    login.add_argument("--key", default="")

    whoami = subparsers.add_parser("cookies", help="Show current saved cookies")
    add_common_connection_args(whoami)

    list_instances = subparsers.add_parser(
        "list-instances", help="List instances available to the current user"
    )
    add_common_connection_args(list_instances)
    list_instances.add_argument(
        "--tag-code",
        action="append",
        default=[],
        help="Repeatable tag code filter, e.g. --tag-code can_read",
    )
    list_instances.add_argument(
        "--db-type",
        action="append",
        default=[],
        help="Repeatable db_type filter",
    )
    list_instances.add_argument("--type-name", default=None)

    list_resources = subparsers.add_parser(
        "list-resources", help="List database/schema/table/column resources"
    )
    add_common_connection_args(list_resources)
    list_resources.add_argument("--instance-name", required=True)
    list_resources.add_argument("--db-name", default="")
    list_resources.add_argument("--schema-name", default="")
    list_resources.add_argument("--tb-name", default="")
    list_resources.add_argument(
        "--resource-type",
        required=True,
        choices=["database", "schema", "table", "column"],
    )

    describe = subparsers.add_parser("describe-table", help="Describe a table")
    add_common_connection_args(describe)
    describe.add_argument("--instance-name", required=True)
    describe.add_argument("--db-name", required=True)
    describe.add_argument("--tb-name", required=True)
    describe.add_argument("--schema-name", default="")

    query = subparsers.add_parser("query", help="Execute a SQL query")
    add_common_connection_args(query)
    query.add_argument("--instance-name", required=True)
    query.add_argument("--db-name", required=True)
    query.add_argument("--sql", required=True, help="SQL to execute")
    query.add_argument("--tb-name", default="")
    query.add_argument("--schema-name", default="")
    query.add_argument("--limit-num", type=int, default=100)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        client = client_from_args(args)

        if args.command == "login":
            result = client.login(
                args.username,
                args.password,
                otp=args.otp,
                auth_type=args.auth_type,
                phone=args.phone,
                key=args.key,
            )
            dump(result, args.pretty)
            return 0

        if args.command == "cookies":
            client.ensure_session()
            dump(
                {"base_url": client.base_url, "cookies": client._cookie_dict()},
                args.pretty,
            )
            return 0

        if args.command == "list-instances":
            result = client.list_instances(
                tag_codes=args.tag_code,
                type_name=args.type_name,
                db_types=args.db_type,
            )
            dump(result, args.pretty)
            return 0

        if args.command == "list-resources":
            result = client.list_resources(
                instance_name=args.instance_name,
                db_name=args.db_name,
                schema_name=args.schema_name,
                tb_name=args.tb_name,
                resource_type=args.resource_type,
            )
            dump(result, args.pretty)
            return 0

        if args.command == "describe-table":
            result = client.describe_table(
                instance_name=args.instance_name,
                db_name=args.db_name,
                tb_name=args.tb_name,
                schema_name=args.schema_name,
            )
            dump(result, args.pretty)
            return 0

        if args.command == "query":
            result = client.query(
                instance_name=args.instance_name,
                db_name=args.db_name,
                sql_content=args.sql,
                tb_name=args.tb_name,
                schema_name=args.schema_name,
                limit_num=args.limit_num,
            )
            dump(result, args.pretty)
            return 0
    except ArcheryError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
