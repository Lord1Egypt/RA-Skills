#!/usr/bin/env python3
# Copyright 2024 ByteDance, Inc.
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
from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field, asdict
import logging
import json
import os
import re
import datetime
import hashlib
import hmac
import requests

from six.moves.urllib.parse import quote, urlencode
from typing import Any, Dict, Optional
from requests_toolbelt.multipart.encoder import MultipartEncoder


DEFAULT_API_HOST = "data-agent.volcengineapi.com"
DEFAULT_API_PATH = "/"
DEFAULT_SERVICE = "data_agent"
DEFAULT_REGION = "cn-beijing"
DEFAULT_VERSION = "2025-05-13"
MIN_VOLC_SDK_VERSION = "4.0.43"


class SignerV4(object):

    @staticmethod
    def sign(path, method, headers, body, post_params, query, ak, sk, region, service,
             session_token=None):
        if path == '':
            path = '/'
        if method != 'GET' and not ('Content-Type' in headers):
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
        format_date = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        headers['X-Date'] = format_date

        if (method == 'POST' and headers.get('Content-Type').startswith('application/x-www-form-urlencoded')
                and post_params):
            body = urlencode(post_params)

        body_hash = hashlib.sha256(body.encode('utf-8') if isinstance(body, str) else body).hexdigest()
        headers['X-Content-Sha256'] = body_hash
        if session_token:
            headers['X-Security-Token'] = session_token

        signed_headers = dict()
        for key in headers:
            if key in ['Content-Type', 'Content-Md5', 'Host'] or key.startswith('X-'):
                signed_headers[key.lower()] = headers[key]

        if 'host' in signed_headers:
            v = signed_headers['host']
            if v.find(':') != -1:
                split = v.split(':')
                port = split[1]
                if str(port) == '80' or str(port) == '443':
                    signed_headers['host'] = split[0]

        signed_str = ''
        for key in sorted(signed_headers.keys()):
            signed_str += key + ':' + signed_headers[key] + '\n'

        signed_headers_string = ';'.join(sorted(signed_headers.keys()))

        canonical_request = '\n'.join(
            [method, path, SignerV4.canonical_query(dict(query)), signed_str, signed_headers_string, body_hash])
        credential_scope = '/'.join([format_date[:8], region, service, 'request'])
        signing_str = '\n'.join(['HMAC-SHA256', format_date, credential_scope,
                                 hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()])
        signing_key = SignerV4.get_signing_secret_key_v4(sk, format_date[:8], region, service)

        signature = hmac.new(signing_key, signing_str.encode('utf-8'), hashlib.sha256).hexdigest()

        credential = ak + '/' + credential_scope
        headers[
            'Authorization'] = 'HMAC-SHA256' + ' Credential=' + credential + ', SignedHeaders=' + \
                               signed_headers_string + ', Signature=' + signature
        return

    @staticmethod
    def canonical_query(query):
        res = []
        for key in query:
            value = str(query[key])
            res.append((quote(key, safe='-_.~'), quote(value, safe='-_.~')))
        sorted_key_vals = []
        for key, value in sorted(res):
            sorted_key_vals.append('%s=%s' % (key, value))
        return '&'.join(sorted_key_vals)

    @staticmethod
    def get_signing_secret_key_v4(sk, date, region, service):
        kdate = SignerV4.hmac_sha256(sk.encode('utf-8'), date)
        kregion = SignerV4.hmac_sha256(kdate, region)
        kservice = SignerV4.hmac_sha256(kregion, service)
        return SignerV4.hmac_sha256(kservice, 'request')

    @staticmethod
    def hmac_sha256(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    @staticmethod
    def sign_url(path, method, query, ak, sk, region, service, session_token=None, host=None):
        """
        Generate presigned URL query string (AWS Signature V4)

        :param path: Request path
        :param method: HTTP method (GET, POST, etc.)
        :param query: Query parameters dict
        :param ak: Access Key
        :param sk: Secret Key
        :param region: Service region
        :param service: Service name
        :param session_token: Optional session token
        :param host: Optional host header to sign
        :return: Query string with signature
        """
        format_date = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date = format_date[:8]

        # Build credential scope
        credential_scope = '/'.join([date, region, service, 'request'])

        # Determine if host header should be signed
        sign_host = host is not None and host != ''

        # Add required query parameters
        query = dict(query)  # Make a copy to avoid modifying original
        query['X-Date'] = format_date
        query['X-NotSignBody'] = ''
        query['X-Credential'] = ak + '/' + credential_scope
        query['X-Algorithm'] = 'HMAC-SHA256'
        query['X-SignedHeaders'] = 'host' if sign_host else ''
        query['X-SignedQueries'] = ''

        # Generate X-SignedQueries BEFORE adding X-Security-Token
        query['X-SignedQueries'] = ';'.join(sorted(query.keys()))
        signed_query_keys = set(query.keys())

        # X-Security-Token must be added AFTER X-SignedQueries calculation
        if session_token:
            query['X-Security-Token'] = session_token

        # Build canonical request
        body_hash = hashlib.sha256(b'').hexdigest()
        canonical_query_params = {k: v for k, v in query.items() if k in signed_query_keys}

        if sign_host:
            canonical_request = '\n'.join([
                method,
                path,
                SignerV4.canonical_query(canonical_query_params),
                'host:' + host + '\n',
                'host',
                body_hash
            ])
        else:
            canonical_request = '\n'.join([
                method,
                path,
                SignerV4.canonical_query(canonical_query_params),
                '\n',
                '',
                body_hash
            ])

        # Build string to sign
        signing_str = '\n'.join([
            'HMAC-SHA256',
            format_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        ])

        # Calculate signature
        signing_key = SignerV4.get_signing_secret_key_v4(sk, date, region, service)
        signature = hmac.new(signing_key, signing_str.encode('utf-8'), hashlib.sha256).hexdigest()

        # Add signature to query
        query['X-Signature'] = signature

        # Return encoded query string
        return urlencode(sorted(query.items()))


class Actions:
    """
    |Action|操作类型|接口说明|
    |--|--|--|
    |ArkClawDataAgentDeepresearchExecuteTask|POST|执行深度研究任务|
    |ArkClawDataAgentDeepresearchGetTaskStatus|GET|获取深度研究任务状态|
    |ArkClawDataAgentDeepresearchGetTaskDetail|GET|获取深度研究任务详情|
    |ArkClawDataAgentDeepresearchUploadFile|POST|上传数据文件|
    """

    ACTION_EXECUTE_TASK = "ArkClawDataAgentDeepresearchExecuteTask"
    ACTION_GET_TASK_STATUS = "ArkClawDataAgentDeepresearchGetTaskStatus"
    ACTION_GET_TASK_DETAIL = "ArkClawDataAgentDeepresearchGetTaskDetail"
    ACTION_UPLOAD_FILE = "ArkClawDataAgentDeepresearchUploadFile"


@dataclass
class TaskMetadata:
    agent_id: int = 0
    file_list: list[str] = field(default_factory=list)
    enable_running_step_output: bool = False

@dataclass
class Data2DocTaskRequest:
    stream: bool = True
    content: str = ""
    metadata: TaskMetadata = field(default_factory=TaskMetadata)


def _env(name: str) -> Optional[str]:
    v = os.environ.get(name)
    if v is None:
        return None
    v = v.strip()
    return v or None


def _parse_version(v: str) -> tuple[int, int, int]:
    parts = (v or "").strip().split(".")
    nums: list[int] = []
    for p in parts[:3]:
        try:
            nums.append(int(re.sub(r"\D.*$", "", p)))
        except Exception:
            nums.append(0)
    while len(nums) < 3:
        nums.append(0)
    return nums[0], nums[1], nums[2]


def _get_volc_sdk_version() -> Optional[str]:
    try:
        from importlib.metadata import version  # py3.8+
    except Exception:
        try:
            from importlib_metadata import version  # type: ignore
        except Exception:
            return None
    try:
        return version("volcengine-python-sdk")
    except Exception:
        return None


def _ensure_volc_sdk_min_version(min_version: str = MIN_VOLC_SDK_VERSION) -> Optional[str]:
    cur = _get_volc_sdk_version()
    if not cur:
        return "未安装 volcengine-python-sdk。请先安装 volcengine-python-sdk>=4.0.43。"
    if _parse_version(cur) < _parse_version(min_version):
        return f"volcengine-python-sdk 版本过低（当前 {cur}，要求 >= {min_version}）。请升级以避免历史版本重试缺陷。"
    return None


def _build_api_client(ak_override: Optional[str] = None, sk_override: Optional[str] = None) -> tuple[Any, str]:
    """构建已配置签名的 volcenginesdkcore.ApiClient，返回 (client, api_path)。"""
    ver_err = _ensure_volc_sdk_min_version()
    if ver_err:
        raise RuntimeError(ver_err)

    try:
        import volcenginesdkcore  # type: ignore
    except ImportError:
        raise RuntimeError(
            "未安装 volcengine-python-sdk（缺少 volcenginesdkcore）。请先安装 volcengine-python-sdk>=4.0.43。"
        )

    ak = ak_override or _env("VOLCENGINE_ACCESS_KEY")
    sk = sk_override or _env("VOLCENGINE_SECRET_KEY")

    if not (ak and sk):
        raise RuntimeError("未配置 Volcengine 凭证（需要同时设置 VOLCENGINE_ACCESS_KEY / VOLCENGINE_SECRET_KEY）。")


    # service / region / host 均有内置默认值，环境变量可覆盖（用于调试）
    service = _env("VOLC_SERVICE") or DEFAULT_SERVICE
    region = _env("VOLCENGINE_REGION") or DEFAULT_REGION

    custom_url = _env("PUBLIC_INSIGHT_API_URL")
    if custom_url:
        from urllib.parse import urlsplit
        p = urlsplit(custom_url)
        host = p.netloc or DEFAULT_API_HOST
        api_path = p.path or DEFAULT_API_PATH
        scheme = p.scheme or "https"
    else:
        host = DEFAULT_API_HOST
        api_path = DEFAULT_API_PATH
        scheme = "https"

    configuration = volcenginesdkcore.Configuration()
    # 默认关闭 SDK 的日志输出（避免干扰用户输出）。
    # 调试时可通过 OPENCLAW_DEBUG=1 打开。
    configuration.logger["package_logger"].setLevel(logging.ERROR)
    configuration.logger["urllib3_logger"].setLevel(logging.ERROR)
    configuration.ak = ak
    configuration.sk = sk
    configuration.region = region
    configuration.host = host
    if scheme != "https":
        configuration.scheme = scheme
    if hasattr(configuration, "service"):
        configuration.service = service

    return volcenginesdkcore.ApiClient(configuration), api_path


def _do_call(
        api_client: Any,
        params: Dict[str, Any],
        action: str,
        payload: Dict[str, Any] | str,
        headers: dict[str, Any] = None,
        stream: bool = False,
        stream_callback: callable[str, Any] = None
) -> Optional[Dict[str, Any]]:
    """通过 SDK ApiClient 向火山 OpenAPI 发起签名 POST 请求。"""
    cfg = api_client.configuration
    scheme = getattr(cfg, "scheme", "https") or "https"
    service = getattr(cfg, "service", DEFAULT_SERVICE) or DEFAULT_SERVICE
    url = f"{scheme}://{cfg.host}"
    if not params:
        params = {}
    params.update({
        "Action": action, 
        "Version": DEFAULT_VERSION
    })
    if not headers:
        headers = {}
    headers.update({
        "Accept": "application/json",
        "Host": cfg.host
    })
    method = "POST"
    if isinstance(payload, dict):
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        headers["Content-Type"] = "application/json"
    elif isinstance(payload, (str | bytes)) and len(payload) > 0:
        data = payload
    else:
        data = ""
        method = "GET"
    
    SignerV4.sign("", method, headers, data, None, params,
                    cfg.ak, cfg.sk, cfg.region, service, None)
    if method == "POST":
        http_resp = requests.post(url, params=params, headers=headers, data=data, timeout=3600, stream=stream)
    else:
        http_resp = requests.get(url, params=params, headers=headers, timeout=3600, stream=stream)
    if stream:
        for line in http_resp.iter_lines():
            if line and stream_callback:
                stream_callback(line.decode("utf-8"))
        http_resp.raise_for_status()
    else:
        http_resp.raise_for_status()
        return http_resp.content
    return None


def api_call(
        action: str,
        params: Dict[str, Any] = None,
        payload: dict[str, Any] | str = None,
        headers: dict[str, Any] = None,
        ak: Optional[str] = None,
        sk: Optional[str] = None,
        stream: bool = False,
        stream_callback: callable[str, Any] = None
) -> Dict[str, Any]:
    """封装单次API调用"""
    api_client, api_path = _build_api_client(ak_override=ak, sk_override=sk)

    try:
        return _do_call(
            api_client,
            params=params,
            action=action,
            payload=payload,
            headers=headers,
            stream=stream,
            stream_callback=stream_callback
        )
    except requests.exceptions.HTTPError as e:
        print(e.response.content)
        raise e


def execute_task(task_request: Data2DocTaskRequest, ak: Optional[str] = None, sk: Optional[str] = None) -> Dict[str, Any]:
    """执行深度研究任务"""
    return api_call(Actions.ACTION_EXECUTE_TASK, payload=asdict(task_request), ak=ak, sk=sk)


def upload_files(file_list: list[str], ak: Optional[str] = None, sk: Optional[str] = None) -> list[str]:
    """上传数据文件"""

    obj_store_keys = []
    for file in file_list:
        with open(file, "rb") as f:
            filename = os.path.basename(file)
            filesize = os.path.getsize(file)

            if filename.endswith(".csv"):
                filetype = "csv"
            elif filename.endswith(".xlsx"):
                filetype = "xlsx"
            elif filename.endswith(".xls"):
                filetype = "xls"
            else:
                raise Exception(f"暂时不支持该文件类型: {filename}")

            m = MultipartEncoder(
                fields={
                    'fileType': filetype,
                    'fileName': filename,
                    'fileSize': str(filesize),
                    'file': (filename, f)
                }
            )
            data = m.to_string()
            response = api_call(Actions.ACTION_UPLOAD_FILE, payload=data, headers={"Content-Type": m.content_type}, ak=ak, sk=sk)
            result = json.loads(response)
            obj_store_keys.append(result["data"]["storageKey"])
    return obj_store_keys


def main() -> int:
    ap = argparse.ArgumentParser(description="Aida OpenAPI Client (volcengine-sdk)")
    ap.add_argument("--ak", default=None, help="Volcengine AccessKey（优先级高于环境变量和 .env 文件）")
    ap.add_argument("--sk", default=None, help="Volcengine SecretKey（优先级高于环境变量和 .env 文件）")
    ap.add_argument("--debug", default=False, action="store_true", help="输出完整错误信息（也可用 OPENCLAW_DEBUG=1）")
    ap.add_argument("--files", required=True, help="用户待处理的excel/csv文件路径，绝对路径, 多个文件用逗号分隔")
    # ap.add_argument("--question", required=True, help="用户的问题")
    ap.add_argument("--output", required=True, help="输出文件路径，绝对路径")

    args = ap.parse_args()

    start = time.time()

    if args.debug:
        os.environ["OPENCLAW_DEBUG"] = "1"

    task_request = Data2DocTaskRequest(
        stream=True,
        content="请帮我分析并产出文档",
        metadata=TaskMetadata(
            agent_id=1,
            file_list=upload_files(args.files.split(","), ak=args.ak, sk=args.sk),
            enable_running_step_output=True,
        ),
    )

    output_file = args.output
    with open(output_file, "w+", encoding="utf-8") as out:

        def stream_callback(content: str) -> None:
            content = content.lstrip("data:").strip()
            try:
                event = json.loads(content)
            except Exception as _:
                return
            if not isinstance(event, dict):
                return
            artifact_update = event.get("artifactUpdate")
            if not isinstance(artifact_update, dict):
                return
            artifact = artifact_update.get("artifact")
            if not isinstance(artifact, dict):
                return
            metadata = artifact.get("metadata")
            if not isinstance(metadata, dict):
                return
            parts = artifact.get("parts", [])
            if not isinstance(parts, list):
                return

            artifact_type = metadata.get("type")
            if "deep_research_markdown_report" == artifact_type:
                for part in parts:
                    if not isinstance(part, dict):
                        continue
                    text = part.get("text")
                    if not text:
                        continue
                    out.write(text)
            else:
                if args.debug:
                    print(f"任务正常运行中, 当前运行时间{int(time.time() - start)}秒, 请耐心等待~")

        # run deepresearch task
        api_call(Actions.ACTION_EXECUTE_TASK, payload=asdict(task_request), ak=args.ak, sk=args.sk, stream=True, stream_callback=stream_callback)

    print(f"报告已生成, 存储于文件{output_file}中. 耗时: {int(time.time() - start)}秒")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
