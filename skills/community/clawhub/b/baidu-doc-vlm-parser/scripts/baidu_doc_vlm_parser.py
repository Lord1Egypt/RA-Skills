#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baidu Document Parser (PaddleOCR-VL) Client
API Documentation: https://ai.baidu.com/ai-doc/OCR/3mi73at9o
"""

import base64
import json
import os
import time
import requests
import argparse
from typing import Optional, Dict, Any, Union
from urllib.parse import urlencode, urlparse


class BaiduDocVLMParser:
    """Baidu Document Parser (PaddleOCR-VL) Client"""

    OAUTH_URL = "https://aip.baidubce.com/oauth/2.0/token"
    SUBMIT_URL = "https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task"
    QUERY_URL = "https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task/query"

    DEFAULT_POLL_INTERVAL = 5
    DEFAULT_MAX_POLL_TIME = 300

    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, access_token: Optional[str] = None):
        self.api_key = api_key or os.getenv("BAIDU_DOC_AI_API_KEY")
        self.secret_key = secret_key or os.getenv("BAIDU_DOC_AI_SECRET_KEY")
        self.access_token = access_token

        if not self.access_token and (self.api_key and self.secret_key):
            self.access_token = self._fetch_auth_credential()

        if not self.access_token:
            raise ValueError("Must provide access_token or api_key+secret_key")

    def _fetch_auth_credential(self) -> str:
        params = {'grant_type': 'client_credentials', 'client_id': self.api_key, 'client_secret': self.secret_key}
        response = requests.post(self.OAUTH_URL, params=params)
        result = response.json()
        if 'access_token' not in result:
            raise Exception(f"Failed to get access_token: {result}")
        return result['access_token']

    def _extract_filename_from_url(self, file_url: str) -> str:
        parsed = urlparse(file_url)
        filename = os.path.basename(parsed.path)
        return filename if filename else "document.pdf"

    def _bool_to_str(self, value: Union[bool, str, None]) -> str:
        if value is None:
            return "False"
        if isinstance(value, bool):
            return str(value)
        return value

    def submit_task(
        self,
        file_data: Optional[str] = None,
        file_url: Optional[str] = None,
        file_name: Optional[str] = None,
        analysis_chart: Union[bool, str, None] = None,
        merge_tables: Union[bool, str, None] = None,
        relevel_titles: Union[bool, str, None] = None,
        recognize_seal: Union[bool, str, None] = None,
        return_span_boxes: Union[bool, str, None] = None,
        return_doc_chunks: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        url = f"{self.SUBMIT_URL}?access_token={self.access_token}"

        if not file_data and not file_url:
            raise ValueError("Must provide file_data or file_url")

        if not file_name:
            if file_url:
                file_name = self._extract_filename_from_url(file_url)
            else:
                raise ValueError("Must provide file_name when using file_data")

        params = {'file_name': file_name}

        if file_data:
            params['file_data'] = file_data
        elif file_url:
            params['file_url'] = file_url

        if analysis_chart is not None:
            params['analysis_chart'] = self._bool_to_str(analysis_chart)
        if merge_tables is not None:
            params['merge_tables'] = self._bool_to_str(merge_tables)
        if relevel_titles is not None:
            params['relevel_titles'] = self._bool_to_str(relevel_titles)
        if recognize_seal is not None:
            params['recognize_seal'] = self._bool_to_str(recognize_seal)
        if return_span_boxes is not None:
            params['return_span_boxes'] = self._bool_to_str(return_span_boxes)

        if return_doc_chunks is not None:
            if isinstance(return_doc_chunks, dict):
                params['return_doc_chunks'] = json.dumps(return_doc_chunks)
            elif isinstance(return_doc_chunks, str):
                params['return_doc_chunks'] = return_doc_chunks

        params.update(kwargs)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=params)
        result = response.json()

        if result.get('error_code', 0) != 0:
            raise Exception(f"Submit task failed: {result.get('error_msg', 'Unknown error')}")

        return result

    def query_task(self, task_id: str) -> Dict[str, Any]:
        url = f"{self.QUERY_URL}?access_token={self.access_token}"
        payload = {'task_id': task_id}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=payload)
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
        task_id = submit_result['result']['task_id']
        print(f"Task submitted: {task_id}")

        time.sleep(5)

        start_time = time.time()
        while time.time() - start_time < max_poll_time:
            result = self.query_task(task_id)

            if result.get('error_code') == 0:
                status = result.get('result', {}).get('status')

                if status == 'success':
                    print("Document parsing completed")
                    if download_result:
                        parse_result_url = result.get('result', {}).get('parse_result_url')
                        if parse_result_url:
                            parse_response = requests.get(parse_result_url)
                            parse_response.encoding = 'utf-8'
                            result['parse_result'] = parse_response.json()
                    return result
                elif status == 'failed':
                    task_error = result.get('result', {}).get('task_error', 'Unknown error')
                    raise Exception(f"Document parsing failed: {task_error}")
                elif status in ('pending', 'processing'):
                    print(f"Status: {status} (waited {int(time.time() - start_time)}s)")
                    time.sleep(poll_interval)
                else:
                    print(f"Unknown status: {status}")
                    time.sleep(poll_interval)
            else:
                raise Exception(f"Query failed: {result.get('error_msg')}")

        raise Exception(f"Timeout: Document parsing exceeded {max_poll_time} seconds")


def _str_to_bool(value):
    if value.lower() in ('true', '1', 'yes'):
        return True
    elif value.lower() in ('false', '0', 'no'):
        return False
    raise argparse.ArgumentTypeError(f"Boolean value expected, got '{value}'")


def main():
    parser = argparse.ArgumentParser(description="Baidu Document Parser (PaddleOCR-VL)")
    parser.add_argument("--file_url", help="Document URL")
    parser.add_argument("--file_data", help="Base64-encoded file data")
    parser.add_argument("--file_name", help="File name with extension")
    parser.add_argument("--api_key", help="API Key (optional, uses env var BAIDU_DOC_AI_API_KEY)")
    parser.add_argument("--secret_key", help="Secret Key (optional, uses env var BAIDU_DOC_AI_SECRET_KEY)")
    parser.add_argument("--analysis_chart", type=_str_to_bool, help="Analyze charts (True/False)")
    parser.add_argument("--merge_tables", type=_str_to_bool, help="Merge cross-page tables (True/False)")
    parser.add_argument("--relevel_titles", type=_str_to_bool, help="Level paragraph titles (True/False)")
    parser.add_argument("--recognize_seal", type=_str_to_bool, help="Recognize seals (True/False)")
    parser.add_argument("--return_span_boxes", type=_str_to_bool, help="Return line coordinates (True/False)")
    parser.add_argument("--poll_interval", type=int, default=5, help="Polling interval (seconds)")
    parser.add_argument("--max_poll_time", type=int, default=300, help="Max polling time (seconds)")
    parser.add_argument("--no_download", action="store_true", help="Do not download parse_result_url content")

    args = parser.parse_args()

    if not args.file_url and not args.file_data:
        parser.error("Must provide --file_url or --file_data")

    if args.file_data and not args.file_name:
        parser.error("Must provide --file_name when using --file_data")

    try:
        client = BaiduDocVLMParser(api_key=args.api_key, secret_key=args.secret_key)

        result = client.parse(
            file_url=args.file_url,
            file_data=args.file_data,
            file_name=args.file_name,
            analysis_chart=args.analysis_chart,
            merge_tables=args.merge_tables,
            relevel_titles=args.relevel_titles,
            recognize_seal=args.recognize_seal,
            return_span_boxes=args.return_span_boxes,
            poll_interval=args.poll_interval,
            max_poll_time=args.max_poll_time,
            download_result=not args.no_download
        )

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
