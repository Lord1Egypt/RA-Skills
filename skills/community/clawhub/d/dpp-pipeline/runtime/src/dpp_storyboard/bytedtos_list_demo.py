from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any

from dpp_storyboard.bytedtos_upload_demo import (
    BytedTosDemoError,
    BytedTosDependencyError,
    TosUploadDemoConfig,
    create_client,
)


@dataclass(frozen=True, slots=True)
class ListObjectsOptions:
    prefix: str = ""
    delimiter: str = ""
    start_after: str = ""
    max_keys: int = 100


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List objects in a TOS bucket using TOS_BUCKET/TOS_AK/TOS_SK/TOS_ENDPOINT/TOS_REGION from the environment."
    )
    parser.add_argument("--prefix", default="", help="Only list keys under this prefix.")
    parser.add_argument("--delimiter", default="", help="Optional delimiter, such as '/'.")
    parser.add_argument("--start-after", default="", help="Only return keys after this marker.")
    parser.add_argument("--max-keys", type=int, default=100, help="Maximum number of objects to return.")
    return parser.parse_args(argv)


def make_list_request_kwargs(options: ListObjectsOptions) -> dict[str, Any]:
    return {
        "prefix": options.prefix,
        "delimiter": options.delimiter,
        "start_after": options.start_after,
        "max_keys": options.max_keys,
    }


def list_objects(client: Any, config: TosUploadDemoConfig, options: ListObjectsOptions) -> Any:
    return client.list_objects_type2(
        bucket=config.bucket,
        prefix=options.prefix or None,
        delimiter=options.delimiter or None,
        start_after=options.start_after or None,
        max_keys=options.max_keys,
    )


def extract_listed_keys(payload: Any) -> list[str]:
    objects = getattr(payload, "contents", None) or []
    keys: list[str] = []
    for item in objects:
        key = getattr(item, "key", None)
        if isinstance(key, str) and key:
            keys.append(key)
    return keys


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        config = TosUploadDemoConfig.from_env()
        options = ListObjectsOptions(
            prefix=args.prefix,
            delimiter=args.delimiter,
            start_after=args.start_after,
            max_keys=args.max_keys,
        )

        client = create_client(config)
        payload = list_objects(client, config, options)
        keys = extract_listed_keys(payload)

        print(f"bucket={config.bucket}")
        print(f"endpoint={config.endpoint}")
        print(f"prefix={options.prefix}")
        print(f"listed_count={len(keys)}")
        for key in keys:
            print(key)

        return 0
    except (BytedTosDemoError, BytedTosDependencyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
