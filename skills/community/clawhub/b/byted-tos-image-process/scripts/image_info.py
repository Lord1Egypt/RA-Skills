# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3
"""Example script: get image information from TOS using the Python SDK.

Calls TOS image processing with `process="image/info"` and prints the JSON result.

Environment variables:
  - TOS_ACCESS_KEY        Access key ID (AK) or STS AccessKeyId
  - TOS_SECRET_KEY        Secret access key (SK) or STS SecretAccessKey
  - TOS_SECURITY_TOKEN    (optional) STS session token
  - TOS_ENDPOINT          TOS endpoint, e.g. https://tos-cn-beijing.volces.com
  - TOS_REGION            TOS region, e.g. cn-beijing
  - TOS_BUCKET            Bucket name that stores the image
  - TOS_OBJECT_KEY        Object key of the image file in the bucket

Optional:
  - MAX_OBJECT_SIZE       Maximum allowed local output size in bytes (default: 262144)

This script supports:
  - local save: via `get_object_to_file` when `--output` is provided
  - save back to TOS: via `get_object(..., save_bucket=..., save_object=...)`

Note: The exact response schema is subject to the official TOS documentation.
"""

import argparse
import json
import os
import sys
from typing import Optional

import tos
from tos.exceptions import TosClientError, TosServerError


def get_env(name: str, required: bool = True, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if required and not value:
        print(f"[ERROR] Environment variable {name} is required.", file=sys.stderr)
        sys.exit(1)
    return value  # type: ignore[return-value]


def create_client() -> tos.TosClientV2:
    ak = get_env("TOS_ACCESS_KEY")
    sk = get_env("TOS_SECRET_KEY")
    endpoint = get_env("TOS_ENDPOINT")
    region = get_env("TOS_REGION")
    security_token = os.getenv("TOS_SECURITY_TOKEN")

    print(f"[INFO] Initializing TOS client for endpoint={endpoint}, region={region} ...")
    return tos.TosClientV2(
        ak=ak,
        sk=sk,
        endpoint=endpoint,
        region=region,
        security_token=security_token,
    )


def load_json_file(path: str) -> object:
    with open(path, "rb") as f:
        raw = f.read()
    return json.loads(raw.decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Get image info via TOS process=image/info")
    parser.add_argument("--bucket", type=str, default=None, help="Override TOS_BUCKET")
    parser.add_argument("--key", type=str, default=None, help="Override TOS_OBJECT_KEY")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="If set, save the JSON response locally using get_object_to_file",
    )
    parser.add_argument("--saveas-bucket", type=str, default=None, help="Persist result to this bucket")
    parser.add_argument("--saveas-object", type=str, default=None, help="Persist result as this object key")
    args = parser.parse_args()

    client = create_client()
    bucket = args.bucket or get_env("TOS_BUCKET")
    key = args.key or get_env("TOS_OBJECT_KEY")

    save_bucket = args.saveas_bucket
    save_object = args.saveas_object
    persist_to_tos = bool(save_bucket or save_object)

    if persist_to_tos:
        save_bucket = save_bucket or bucket
        if not save_object:
            base = os.path.basename(key).replace("/", "_")
            save_object = f"image_info_{base}.json"

        print(f"[INFO] Requesting image info for {bucket}/{key} -> {save_bucket}/{save_object}")
        print("[INFO] process = image/info")

        try:
            output = client.get_object(
                bucket=bucket,
                key=key,
                process="image/info",
                save_bucket=save_bucket,
                save_object=save_object,
            )
            raw = output.read()
        except TosServerError as e:
            print(
                f"[ERROR] TOS server error: code={e.code}, status={e.status_code}, "
                f"request_id={e.request_id}, message={e.message}",
                file=sys.stderr,
            )
            sys.exit(1)
        except TosClientError as e:
            print(f"[ERROR] TOS client error: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            print("[ERROR] Failed to parse response as JSON:", file=sys.stderr)
            print(exc, file=sys.stderr)
            print(raw[:200], file=sys.stderr)
            sys.exit(1)

        print("[OK] Image info saved to TOS:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if args.output:
        output_path = args.output
        print(f"[INFO] Requesting image info for {bucket}/{key} -> {output_path}")
        print("[INFO] process = image/info")

        try:
            client.get_object_to_file(bucket=bucket, key=key, file_path=output_path, process="image/info")
        except TosServerError as e:
            print(
                f"[ERROR] TOS server error: code={e.code}, status={e.status_code}, "
                f"request_id={e.request_id}, message={e.message}",
                file=sys.stderr,
            )
            sys.exit(1)
        except TosClientError as e:
            print(f"[ERROR] TOS client error: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            data = load_json_file(output_path)
        except Exception as exc:  # noqa: BLE001
            print("[ERROR] Failed to parse local file as JSON:", file=sys.stderr)
            print(exc, file=sys.stderr)
            sys.exit(1)

        max_object_size = int(os.getenv("MAX_OBJECT_SIZE", "262144"))
        size = os.path.getsize(output_path)
        if size > max_object_size:
            print(
                f"[ERROR] Output size ({size} bytes) exceeds MAX_OBJECT_SIZE={max_object_size}.",
                file=sys.stderr,
            )
            sys.exit(1)

        print("[OK] Image info:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    print(f"[INFO] Requesting image info for {bucket}/{key} ...")
    print("[INFO] process = image/info")

    try:
        output = client.get_object(bucket=bucket, key=key, process="image/info")
        raw = output.read()
    except TosServerError as e:
        print(
            f"[ERROR] TOS server error: code={e.code}, status={e.status_code}, "
            f"request_id={e.request_id}, message={e.message}",
            file=sys.stderr,
        )
        sys.exit(1)
    except TosClientError as e:
        print(f"[ERROR] TOS client error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        print("[ERROR] Failed to parse response as JSON:", file=sys.stderr)
        print(exc, file=sys.stderr)
        print(raw[:200], file=sys.stderr)
        sys.exit(1)

    print("[OK] Image info:")
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
