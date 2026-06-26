#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


TEXT_COLOR_RED = 4


class ToolError(RuntimeError):
    pass


def token_from_input(value: str) -> str:
    value = value.strip()
    if not value:
        raise ToolError("missing Feishu URL or token")
    for pattern in [
        r"/docx/([A-Za-z0-9_-]+)",
        r"/doc/([A-Za-z0-9_-]+)",
        r"/wiki/([A-Za-z0-9_-]+)",
        r"/sheets/([A-Za-z0-9_-]+)",
        r"/base/([A-Za-z0-9_-]+)",
    ]:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return value.split("?")[0].rstrip("/").split("/")[-1]


def json_arg(value: str, *, default: Any = None) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid JSON argument: {value[:120]}") from exc


def to_jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        out: dict[str, Any] = {}
        for field in dataclasses.fields(value):
            if field.name == "raw":
                continue
            out[field.name] = to_jsonable(getattr(value, field.name))
        return out
    if isinstance(value, dict):
        return {
            str(key): to_jsonable(item)
            for key, item in value.items()
            if key != "raw"
        }
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def emit(value: Any) -> None:
    print(json.dumps(to_jsonable(value), ensure_ascii=False, indent=2))


def configure_env(args: argparse.Namespace) -> None:
    if args.env_file:
        os.environ["FEISHU_ENV_FILE"] = str(Path(args.env_file).expanduser())


def docs_service(args: argparse.Namespace):
    from feishu_api.services import DocsService
    use_user_token = bool(getattr(args, "user_token", False))
    if hasattr(args, "allow_app_owned"):
        use_user_token = not getattr(args, "allow_app_owned", False)
    return DocsService(use_user_token=use_user_token)


def command_doc_create(args: argparse.Namespace) -> dict[str, Any]:
    result = docs_service(args).create_document(args.title, args.folder_token)
    return {"document": result, "url": f"https://feishu.cn/docx/{result.document_id}"}


def command_doc_read(args: argparse.Namespace) -> Any:
    service = docs_service(args)
    doc = token_from_input(args.doc)
    if args.blocks:
        return service.read_document(doc)
    return service.get_document(doc)


def command_doc_append_text(args: argparse.Namespace) -> Any:
    service = docs_service(args)
    doc = token_from_input(args.doc)
    if args.red:
        return service.append_rich_text(doc, args.text, text_color=TEXT_COLOR_RED)
    return service.append_text(doc, args.text)


def command_doc_update_block_text(args: argparse.Namespace) -> dict[str, Any]:
    service = docs_service(args)
    doc = token_from_input(args.doc)
    service.update_block_text(doc, args.block_id, args.text, text_color=TEXT_COLOR_RED if args.red else None)
    return {"ok": True, "document_id": doc, "block_id": args.block_id}


def command_doc_replace_section(args: argparse.Namespace) -> Any:
    service = docs_service(args)
    doc = token_from_input(args.doc)
    paragraphs = args.paragraph or []
    if args.paragraphs_json:
        parsed = json_arg(args.paragraphs_json, default=[])
        if not isinstance(parsed, list):
            raise ToolError("--paragraphs-json must be a JSON array of strings")
        paragraphs.extend(str(item) for item in parsed)
    if not paragraphs:
        raise ToolError("provide --paragraph or --paragraphs-json")
    return service.replace_section_text_by_heading(doc, args.heading, paragraphs, exact=not args.fuzzy)


def command_sheet_create(args: argparse.Namespace) -> Any:
    from feishu_api.services import SheetsService
    return SheetsService().create_spreadsheet(args.title, folder_token=args.folder_token)


def command_sheet_get(args: argparse.Namespace) -> Any:
    from feishu_api.services import SheetsService
    return SheetsService().get_spreadsheet(token_from_input(args.spreadsheet))


def command_sheet_query(args: argparse.Namespace) -> Any:
    from feishu_api.services import SheetsService
    return SheetsService().query_sheets(token_from_input(args.spreadsheet))


def command_sheet_find(args: argparse.Namespace) -> Any:
    from feishu_api.services import SheetsService
    return SheetsService().find_in_sheet(
        token_from_input(args.spreadsheet),
        args.sheet_id,
        args.text,
        cell_range=args.range,
    )


def command_sheet_replace(args: argparse.Namespace) -> Any:
    from feishu_api.services import SheetsService
    return SheetsService().replace_in_sheet(
        token_from_input(args.spreadsheet),
        args.sheet_id,
        args.find,
        args.replacement,
        cell_range=args.range,
    )


def command_base_create(args: argparse.Namespace) -> Any:
    from feishu_api.services import BaseAppService
    return BaseAppService().create_base(args.name, folder_token=args.folder_token, time_zone=args.time_zone)


def command_base_list_tables(args: argparse.Namespace) -> Any:
    from feishu_api.services import BaseAppService
    return BaseAppService().list_tables(token_from_input(args.app))


def command_base_create_table(args: argparse.Namespace) -> Any:
    from feishu_api.services import BaseAppService
    fields = json_arg(args.fields_json, default=[])
    if not isinstance(fields, list):
        raise ToolError("--fields-json must be a JSON array")
    return BaseAppService().create_table(token_from_input(args.app), args.name, fields)


def command_base_list_fields(args: argparse.Namespace) -> Any:
    from feishu_api.services import BaseAppService
    return BaseAppService().list_fields(token_from_input(args.app), args.table_id)


def command_base_list_records(args: argparse.Namespace) -> Any:
    from feishu_api.services import BaseAppService
    return BaseAppService().list_records(token_from_input(args.app), args.table_id, page_size=args.page_size)


def command_base_create_record(args: argparse.Namespace) -> Any:
    from feishu_api.services import BaseAppService
    fields = json_arg(args.fields_json, default={})
    if not isinstance(fields, dict):
        raise ToolError("--fields-json must be a JSON object")
    return BaseAppService().create_record(token_from_input(args.app), args.table_id, fields)


def command_base_update_record(args: argparse.Namespace) -> Any:
    from feishu_api.services import BaseAppService
    fields = json_arg(args.fields_json, default={})
    if not isinstance(fields, dict):
        raise ToolError("--fields-json must be a JSON object")
    return BaseAppService().update_record(token_from_input(args.app), args.table_id, args.record_id, fields)


def command_wiki_list_spaces(args: argparse.Namespace) -> Any:
    from feishu_api.services import WikiService
    return WikiService().list_spaces(page_size=args.page_size)


def command_wiki_list_nodes(args: argparse.Namespace) -> Any:
    from feishu_api.services import WikiService
    return WikiService().list_nodes(args.space_id, parent_node_token=args.parent_node_token, page_size=args.page_size)


def command_wiki_get_node(args: argparse.Namespace) -> Any:
    from feishu_api.services import WikiService
    return WikiService().get_node_info(token_from_input(args.token), obj_type=args.obj_type)


def command_drive_list_files(args: argparse.Namespace) -> Any:
    from feishu_api.services import DriveService
    return DriveService().list_files(page_size=args.page_size)


def command_drive_find_token(args: argparse.Namespace) -> Any:
    from feishu_api.services import DriveService
    return DriveService().find_file_by_token(token_from_input(args.token), page_size=args.page_size)


def command_im_send_text(args: argparse.Namespace) -> Any:
    from feishu_api.services import IMService
    return IMService().send_text(args.receive_id, args.text, receive_id_type=args.receive_id_type)


def command_im_get_message(args: argparse.Namespace) -> Any:
    from feishu_api.services import IMService
    return IMService().get_message(args.message_id)


def command_im_list_messages(args: argparse.Namespace) -> Any:
    from feishu_api.services import IMService
    return IMService().list_messages(
        args.chat_id,
        start_time=args.start_time,
        end_time=args.end_time,
        page_size=args.page_size,
    )


def command_im_reply_text(args: argparse.Namespace) -> Any:
    from feishu_api.services import IMService
    return IMService().reply_text(args.message_id, args.text, reply_in_thread=args.reply_in_thread)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", default="", help="Path to .env with Feishu credentials")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Feishu OpenAPI service wrapper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("doc-create")
    add_common(p)
    p.add_argument("--title", required=True)
    p.add_argument("--folder-token", default="")
    p.add_argument("--allow-app-owned", action="store_true")
    p.set_defaults(func=command_doc_create)

    p = sub.add_parser("doc-read")
    add_common(p)
    p.add_argument("--doc", required=True)
    p.add_argument("--blocks", action="store_true")
    p.add_argument("--user-token", action="store_true")
    p.set_defaults(func=command_doc_read)

    p = sub.add_parser("doc-append-text")
    add_common(p)
    p.add_argument("--doc", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--red", action="store_true")
    p.add_argument("--user-token", action="store_true")
    p.set_defaults(func=command_doc_append_text)

    p = sub.add_parser("doc-update-block-text")
    add_common(p)
    p.add_argument("--doc", required=True)
    p.add_argument("--block-id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--red", action="store_true")
    p.add_argument("--user-token", action="store_true")
    p.set_defaults(func=command_doc_update_block_text)

    p = sub.add_parser("doc-replace-section")
    add_common(p)
    p.add_argument("--doc", required=True)
    p.add_argument("--heading", required=True)
    p.add_argument("--paragraph", action="append")
    p.add_argument("--paragraphs-json", default="")
    p.add_argument("--fuzzy", action="store_true")
    p.add_argument("--user-token", action="store_true")
    p.set_defaults(func=command_doc_replace_section)

    p = sub.add_parser("sheet-create")
    add_common(p)
    p.add_argument("--title", required=True)
    p.add_argument("--folder-token", default="")
    p.set_defaults(func=command_sheet_create)

    p = sub.add_parser("sheet-get")
    add_common(p)
    p.add_argument("--spreadsheet", required=True)
    p.set_defaults(func=command_sheet_get)

    p = sub.add_parser("sheet-query")
    add_common(p)
    p.add_argument("--spreadsheet", required=True)
    p.set_defaults(func=command_sheet_query)

    p = sub.add_parser("sheet-find")
    add_common(p)
    p.add_argument("--spreadsheet", required=True)
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--range", default="")
    p.set_defaults(func=command_sheet_find)

    p = sub.add_parser("sheet-replace")
    add_common(p)
    p.add_argument("--spreadsheet", required=True)
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--find", required=True)
    p.add_argument("--replacement", required=True)
    p.add_argument("--range", default="")
    p.set_defaults(func=command_sheet_replace)

    p = sub.add_parser("base-create")
    add_common(p)
    p.add_argument("--name", required=True)
    p.add_argument("--folder-token", default="")
    p.add_argument("--time-zone", default="Asia/Shanghai")
    p.set_defaults(func=command_base_create)

    p = sub.add_parser("base-list-tables")
    add_common(p)
    p.add_argument("--app", required=True)
    p.set_defaults(func=command_base_list_tables)

    p = sub.add_parser("base-create-table")
    add_common(p)
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--fields-json", required=True)
    p.set_defaults(func=command_base_create_table)

    p = sub.add_parser("base-list-fields")
    add_common(p)
    p.add_argument("--app", required=True)
    p.add_argument("--table-id", required=True)
    p.set_defaults(func=command_base_list_fields)

    p = sub.add_parser("base-list-records")
    add_common(p)
    p.add_argument("--app", required=True)
    p.add_argument("--table-id", required=True)
    p.add_argument("--page-size", type=int, default=200)
    p.set_defaults(func=command_base_list_records)

    p = sub.add_parser("base-create-record")
    add_common(p)
    p.add_argument("--app", required=True)
    p.add_argument("--table-id", required=True)
    p.add_argument("--fields-json", required=True)
    p.set_defaults(func=command_base_create_record)

    p = sub.add_parser("base-update-record")
    add_common(p)
    p.add_argument("--app", required=True)
    p.add_argument("--table-id", required=True)
    p.add_argument("--record-id", required=True)
    p.add_argument("--fields-json", required=True)
    p.set_defaults(func=command_base_update_record)

    p = sub.add_parser("wiki-list-spaces")
    add_common(p)
    p.add_argument("--page-size", type=int, default=50)
    p.set_defaults(func=command_wiki_list_spaces)

    p = sub.add_parser("wiki-list-nodes")
    add_common(p)
    p.add_argument("--space-id", required=True)
    p.add_argument("--parent-node-token", default="")
    p.add_argument("--page-size", type=int, default=200)
    p.set_defaults(func=command_wiki_list_nodes)

    p = sub.add_parser("wiki-get-node")
    add_common(p)
    p.add_argument("--token", required=True)
    p.add_argument("--obj-type", default="docx")
    p.set_defaults(func=command_wiki_get_node)

    p = sub.add_parser("drive-list-files")
    add_common(p)
    p.add_argument("--page-size", type=int, default=50)
    p.set_defaults(func=command_drive_list_files)

    p = sub.add_parser("drive-find-token")
    add_common(p)
    p.add_argument("--token", required=True)
    p.add_argument("--page-size", type=int, default=200)
    p.set_defaults(func=command_drive_find_token)

    p = sub.add_parser("im-send-text")
    add_common(p)
    p.add_argument("--receive-id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--receive-id-type", default="open_id", choices=["open_id", "user_id", "union_id", "email", "chat_id"])
    p.set_defaults(func=command_im_send_text)

    p = sub.add_parser("im-get-message")
    add_common(p)
    p.add_argument("--message-id", required=True)
    p.set_defaults(func=command_im_get_message)

    p = sub.add_parser("im-list-messages")
    add_common(p)
    p.add_argument("--chat-id", required=True)
    p.add_argument("--start-time", required=True, help="Unix timestamp seconds")
    p.add_argument("--end-time", required=True, help="Unix timestamp seconds")
    p.add_argument("--page-size", type=int, default=20)
    p.set_defaults(func=command_im_list_messages)

    p = sub.add_parser("im-reply-text")
    add_common(p)
    p.add_argument("--message-id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--reply-in-thread", action="store_true")
    p.set_defaults(func=command_im_reply_text)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_env(args)
    try:
        emit(args.func(args))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
