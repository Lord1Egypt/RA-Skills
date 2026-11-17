#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baidu Document Parser (Unlimited-OCR) Client
API Documentation: https://cloud.baidu.com/doc/OCR/s/fmr1p39gb
"""

import base64
import json
import os
import time
import argparse
from typing import Optional, Dict, Any
from urllib.parse import urlparse

import requests


class BaiduDocUnlimitedOCRParser:
    """Baidu Document Parser (Unlimited-OCR) Client"""

    OAUTH_URL = "https://aip.baidubce.com/oauth/2.0/token"
    SUBMIT_URL = "https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task"
    QUERY_URL = "https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task/query"

    DEFAULT_POLL_INTERVAL = 5
    DEFAULT_MAX_POLL_TIME = 300

    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("BAIDU_DOC_AI_API_KEY")
        self.secret_key = secret_key or os.getenv("BAIDU_DOC_AI_SECRET_KEY")
        self.access_token = access_token

        if not self.access_token and (self.api_key and self.secret_key):
            self.access_token = self._fetch_auth_credential()

        if not self.access_token:
            raise ValueError("Must provide access_token or api_key+secret_key")

    def _fetch_auth_credential(self) -> str:
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
        }
        response = requests.post(self.OAUTH_URL, params=params, timeout=30)
        result = response.json()
        if "access_token" not in result:
            raise Exception(f"Failed to get access_token: {result}")
        return result["access_token"]

    def _extract_filename_from_url(self, file_url: str) -> str:
        parsed = urlparse(file_url)
        filename = os.path.basename(parsed.path)
        return filename if filename else "document.pdf"

    def submit_task(
        self,
        file_data: Optional[str] = None,
        file_url: Optional[str] = None,
        file_name: Optional[str] = None,
        angle_adjust: Optional[bool] = None,
        angle_mode: Optional[str] = None,
        erase_seal: Optional[bool] = None,
        erase_watermark: Optional[bool] = None,
        unwarp: Optional[bool] = None,
    ) -> Dict[str, Any]:
        url = f"{self.SUBMIT_URL}?access_token={self.access_token}"

        if not file_data and not file_url:
            raise ValueError("Must provide file_data or file_url")

        if not file_name:
            if file_url:
                file_name = self._extract_filename_from_url(file_url)
            else:
                raise ValueError("Must provide file_name when using file_data")

        params = {"file_name": file_name}
        if file_data:
            params["file_data"] = file_data
        elif file_url:
            params["file_url"] = file_url

        if angle_adjust is not None:
            params["angle_adjust"] = str(angle_adjust)
        if angle_mode is not None:
            params["angle_mode"] = angle_mode
        if erase_seal is not None:
            params["erase_seal"] = str(erase_seal)
        if erase_watermark is not None:
            params["erase_watermark"] = str(erase_watermark)
        if unwarp is not None:
            params["unwarp"] = str(unwarp)

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, headers=headers, data=params, timeout=120)
        result = response.json()

        if result.get("error_code", 0) != 0:
            raise Exception(f"Submit task failed: {result.get('error_msg', 'Unknown error')}")

        return result

    def query_task(self, task_id: str) -> Dict[str, Any]:
        url = f"{self.QUERY_URL}?access_token={self.access_token}"
        payload = {"task_id": task_id}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url, headers=headers, data=payload, timeout=60)
        return response.json()

    def parse(
        self,
        file_url: Optional[str] = None,
        file_data: Optional[str] = None,
        file_name: Optional[str] = None,
        poll_interval: int = DEFAULT_POLL_INTERVAL,
        max_poll_time: int = DEFAULT_MAX_POLL_TIME,
        download_result: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        submit_result = self.submit_task(
            file_url=file_url,
            file_data=file_data,
            file_name=file_name,
            **kwargs
        )
        task_id = submit_result["result"]["task_id"]
        print(f"Task submitted: {task_id}")

        time.sleep(5)

        start_time = time.time()
        while time.time() - start_time < max_poll_time:
            result = self.query_task(task_id)

            if result.get("error_code") == 0:
                status = result.get("result", {}).get("status")

                if status == "success":
                    print("Document parsing completed")
                    if download_result:
                        markdown_url = result.get("result", {}).get("markdown_url")
                        if markdown_url:
                            md_resp = requests.get(markdown_url, timeout=60)
                            md_resp.encoding = "utf-8"
                            result["markdown"] = md_resp.text
                        parse_result_url = result.get("result", {}).get("parse_result_url")
                        if parse_result_url:
                            try:
                                pr_resp = requests.get(parse_result_url, timeout=60)
                                pr_resp.encoding = "utf-8"
                                result["parse_result"] = pr_resp.json()
                            except Exception:
                                pass
                    return result
                elif status == "failed":
                    task_error = result.get("result", {}).get("task_error", "Unknown error")
                    raise Exception(f"Document parsing failed: {task_error}")
                elif status in ("pending", "running", "processing"):
                    print(f"Status: {status} (waited {int(time.time() - start_time)}s)")
                    time.sleep(poll_interval)
                else:
                    print(f"Unknown status: {status}")
                    time.sleep(poll_interval)
            else:
                raise Exception(f"Query failed: {result.get('error_msg')}")

        raise Exception(f"Timeout: Document parsing exceeded {max_poll_time} seconds")


def _str_to_bool(value):
    if value.lower() in ("true", "1", "yes"):
        return True
    elif value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Boolean value expected, got '{value}'")


def main():
    parser = argparse.ArgumentParser(description="Baidu Document Parser (Unlimited-OCR)")
    parser.add_argument("--file_url", help="Document URL")
    parser.add_argument("--file_data", help="Base64-encoded file data")
    parser.add_argument("--file_name", help="File name with extension")
    parser.add_argument("--api_key", help="API Key (defaults to env BAIDU_DOC_AI_API_KEY)")
    parser.add_argument("--secret_key", help="Secret Key (defaults to env BAIDU_DOC_AI_SECRET_KEY)")
    parser.add_argument("--angle_adjust", type=_str_to_bool, help="Angle correction (True/False, default True)")
    parser.add_argument("--angle_mode", choices=["direction", "arbitrary"], help="Angle correction mode")
    parser.add_argument("--erase_seal", type=_str_to_bool, help="Erase seals (True/False)")
    parser.add_argument("--erase_watermark", type=_str_to_bool, help="Erase watermarks (True/False)")
    parser.add_argument("--unwarp", type=_str_to_bool, help="Image dewarping (True/False)")
    parser.add_argument("--poll_interval", type=int, default=5, help="Polling interval (seconds)")
    parser.add_argument("--max_poll_time", type=int, default=300, help="Max polling time (seconds)")
    parser.add_argument("--no_download", action="store_true", help="Do not download markdown/parse_result content")
    parser.add_argument("--task_id", help="If set, only query the given task_id (skip submit)")

    args = parser.parse_args()

    try:
        client = BaiduDocUnlimitedOCRParser(api_key=args.api_key, secret_key=args.secret_key)

        if args.task_id:
            result = client.query_task(args.task_id)
        else:
            if not args.file_url and not args.file_data:
                parser.error("Must provide --file_url or --file_data (or --task_id)")
            if args.file_data and not args.file_name:
                parser.error("Must provide --file_name when using --file_data")

            preprocess = {}
            if args.angle_adjust is not None:
                preprocess["angle_adjust"] = args.angle_adjust
            if args.angle_mode is not None:
                preprocess["angle_mode"] = args.angle_mode
            if args.erase_seal is not None:
                preprocess["erase_seal"] = args.erase_seal
            if args.erase_watermark is not None:
                preprocess["erase_watermark"] = args.erase_watermark
            if args.unwarp is not None:
                preprocess["unwarp"] = args.unwarp

            result = client.parse(
                file_url=args.file_url,
                file_data=args.file_data,
                file_name=args.file_name,
                poll_interval=args.poll_interval,
                max_poll_time=args.max_poll_time,
                download_result=not args.no_download,
                **preprocess,
            )

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
