#!/usr/bin/env python3
"""
Feishu Bitable Attachment Upload Skill - Main Entry Point

Usage:
    python scripts/main.py --input payload.json

This script orchestrates the full upload flow:
1. Resolve target (table/field/record)
2. Fetch source file (local/url/feishu_message)
3. Upload to Bitable (direct or chunked)
4. Update/Create record with attachment

Environment Variables Required:
    FEISHU_APP_ID       - Feishu app ID
    FEISHU_APP_SECRET   - Feishu app secret
    FEISHU_BASE_URL     - Optional, default https://open.feishu.cn
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (
    log,
    print_json,
    get_env_required,
    SkillError,
    SkillInputError,
    SkillFileNotFoundError,
    SkillDownloadError,
    FeishuAuthError,
    FeishuUploadError,
    BitableResolveError,
    BitableUpdateError,
)
from fetch_source_file import fetch_source_file, cleanup_temp_file
from resolve_bitable_target import resolve_bitable_target
from upload_to_bitable import upload_to_bitable
from update_bitable_record import update_bitable_record


def load_input(input_path: str) -> Dict[str, Any]:
    """Load input JSON from file."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_input(data: Dict[str, Any]) -> None:
    """
    Validate input structure.

    Raises:
        SkillInputError: If input is invalid
    """
    if "target" not in data:
        raise SkillInputError("Missing required field: target")
    if "source" not in data:
        raise SkillInputError("Missing required field: source")

    target = data["target"]
    source = data["source"]

    # Validate target
    if not target.get("app_token"):
        raise SkillInputError("target.app_token is required")

    # Need either table_id or table_name
    if not target.get("table_id") and not target.get("table_name"):
        raise SkillInputError("Either target.table_id or target.table_name must be provided")

    # Need either field_id or field_name
    if not target.get("field_id") and not target.get("field_name"):
        raise SkillInputError("Either target.field_id or target.field_name must be provided")

    # Validate source
    if not source.get("type"):
        raise SkillInputError("source.type is required")
    if source.get("ref") is None:
        raise SkillInputError("source.ref is required")

    if source["type"] == "local":
        if not isinstance(source["ref"], str):
            raise SkillInputError("source.ref must be a file path string for type=local")
    elif source["type"] == "url":
        if not isinstance(source["ref"], str):
            raise SkillInputError("source.ref must be a URL string for type=url")
    elif source["type"] == "feishu_message":
        if not isinstance(source["ref"], (str, dict)):
            raise SkillInputError("source.ref must be a file_key string or dict for type=feishu_message")
    else:
        raise SkillInputError(
            f"Invalid source.type: '{source['type']}'. Must be one of: local, url, feishu_message"
        )


def build_result(target: Dict, target_result=None, upload_result=None, record_result=None, filename=None) -> Dict[str, Any]:
    """Build result dictionary."""
    result = {
        "app_token": target.get("app_token", ""),
        "table_id": target_result.table_id if target_result else "",
        "table_name": target_result.table_name if target_result else "",
        "record_id": "",
        "field_name": target_result.field_name if target_result else (target.get("field_name") or target.get("field_id", "")),
        "field_id": target_result.field_id if target_result else "",
        "file_token": upload_result.file_token if upload_result else "",
        "upload_type": upload_result.upload_type if upload_result else "",
        "message": ""
    }

    if target_result:
        result["record_id"] = target_result.record_id or ""

    if record_result:
        result["record_id"] = record_result.get("record_id", result["record_id"])
        result["attachment_count"] = record_result.get("attachment_count", 0)
        result["mode"] = record_result.get("mode", "")

    return result


def main(input_path: str) -> Dict[str, Any]:
    """
    Main execution flow.

    Args:
        input_path: Path to input JSON file

    Returns:
        Result dictionary with ok=true/false
    """
    log.info("=" * 60)
    log.info("Feishu Bitable Attachment Upload")
    log.info("=" * 60)

    # Load and validate input
    log.info(f"Loading input from: {input_path}")
    input_data = load_input(input_path)
    validate_input(input_data)

    target = input_data["target"]
    source = input_data["source"]
    append = input_data.get("append", True)

    # Get credentials from environment
    app_id = get_env_required("FEISHU_APP_ID")
    app_secret = get_env_required("FEISHU_APP_SECRET")

    log.info(f"App ID: {app_id[:8]}...")

    target_result = None
    upload_result = None
    record_result = None
    fetch_result = None

    try:
        # Step 1: Resolve target
        log.info("Step 1/4: Resolving Bitable target...")
        target_result = resolve_bitable_target(target, app_id, app_secret)

        log.info(f"  App Token: {target_result.app_token}")
        log.info(f"  Table: {target_result.table_name} ({target_result.table_id})")
        log.info(f"  Field: {target_result.field_name} ({target_result.field_id})")
        log.info(f"  Record: {target_result.record_id or 'NEW (will create)'}")

        # Step 2: Fetch source file
        log.info("Step 2/4: Fetching source file...")
        fetch_result = fetch_source_file(source, app_id, app_secret)

        log.info(f"  Filename: {fetch_result.filename}")
        log.info(f"  Size: {fetch_result.file_size} bytes")
        log.info(f"  MIME: {fetch_result.mime_type}")
        log.info(f"  Temp path: {fetch_result.local_file_path}")

        # Step 3: Upload to Bitable
        log.info("Step 3/4: Uploading to Bitable...")
        upload_result = upload_to_bitable(
            fetch_result.local_file_path,
            target_result.app_token,
            app_id,
            app_secret,
            fetch_result.filename
        )

        log.info(f"  File token: {upload_result.file_token}")
        log.info(f"  Upload type: {upload_result.upload_type}")

        # Step 4: Update/Create record
        log.info("Step 4/4: Updating Bitable record...")
        record_result = update_bitable_record(
            app_token=target_result.app_token,
            table_id=target_result.table_id,
            field_id=target_result.field_id,
            field_name=target_result.field_name,
            file_token=upload_result.file_token,
            app_id=app_id,
            app_secret=app_secret,
            record_id=target_result.record_id,
            append=append,
            fields=None
        )

        log.info(f"  Record ID: {record_result['record_id']}")
        log.info(f"  Attachment count: {record_result['attachment_count']}")
        log.info(f"  Mode: {record_result['mode']}")

        # Cleanup temp file
        log.info("Cleaning up temporary file...")
        cleanup_temp_file(fetch_result.local_file_path)

        # Build success result
        result = build_result(target, target_result, upload_result, record_result, fetch_result.filename)
        result["message"] = (
            f"Successfully uploaded '{fetch_result.filename}' to Bitable "
            f"'{target_result.table_name}' field '{target_result.field_name}' "
            f"({record_result['mode']} mode)"
        )

        log.info("=" * 60)
        log.info("SUCCESS")
        log.info("=" * 60)

        return {"ok": True, **result}

    except SkillFileNotFoundError as e:
        log.error(f"File not found: {e.message}")
        return {"ok": False, "error": e.message, "error_type": "file_not_found", **e.details}

    except SkillDownloadError as e:
        log.error(f"Download failed: {e.message}")
        return {"ok": False, "error": e.message, "error_type": "download_failed", **e.details}

    except SkillInputError as e:
        log.error(f"Input error: {e.message}")
        return {"ok": False, "error": e.message, "error_type": "input_error", **e.details}

    except FeishuAuthError as e:
        log.error(f"Authentication failed: {e.message}")
        return {"ok": False, "error": e.message, "error_type": "auth_error", **e.details}

    except FeishuUploadError as e:
        log.error(f"Upload failed: {e.message}")
        return {"ok": False, "error": e.message, "error_type": "upload_error", **e.details}

    except BitableResolveError as e:
        log.error(f"Target resolution failed: {e.message}")
        return {"ok": False, "error": e.message, "error_type": "resolve_error", **e.details}

    except BitableUpdateError as e:
        log.error(f"Record update failed: {e.message}")
        return {"ok": False, "error": e.message, "error_type": "update_error", **e.details}

    except FileNotFoundError as e:
        log.error(f"File not found: {e}")
        return {"ok": False, "error": str(e), "error_type": "file_not_found"}

    except Exception as e:
        log.error(f"Unexpected error: {e}")
        import traceback
        log.error(traceback.format_exc())
        return {"ok": False, "error": f"Unexpected error: {str(e)}", "error_type": "unexpected_error"}


def cli_main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Feishu Bitable Attachment Upload Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/main.py --input payload.local.json
    python scripts/main.py --input payload.url.json
    python scripts/main.py --input payload.feishu_message.json
    python scripts/main.py --input payload.table_name.json
    python scripts/main.py --input payload.lookup.json
    python scripts/main.py --input payload.create_record.json

Environment variables required:
    FEISHU_APP_ID       - Feishu app ID
    FEISHU_APP_SECRET   - Feishu app secret
    FEISHU_BASE_URL     - Optional, default https://open.feishu.cn
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input JSON file"
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only output final JSON result"
    )

    args = parser.parse_args()

    if args.quiet:
        # Suppress logging
        import logging
        logging.getLogger().setLevel(logging.CRITICAL)

    # Run main
    result = main(args.input)

    # Output result
    print_json(result)

    # Exit code
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    cli_main()
