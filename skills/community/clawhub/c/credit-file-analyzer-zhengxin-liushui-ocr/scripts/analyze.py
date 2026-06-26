"""
信贷文件分析脚本

用法:
    python analyze.py --url "<文件URL>" --type "简版征信"
    python analyze.py --url "<文件URL>" --type "详版征信" --password "abc123"
    python analyze.py --url "<URL1>,<URL2>" --type "流水" --file-type img
"""

import argparse
import json
import sys
import time
import uuid
from datetime import datetime

import requests

BASE_URL = "https://www.ipipei.com/prod-api"
ENTERPRISE_KEY = "26b22ed9a21c42ec89b07b6299cdceb5"

VALID_TYPES = ["详版征信", "简版征信", "企业征信", "流水"]
VALID_FILE_TYPES = ["pdf", "img", "excel"]


def now_text():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def request_code():
    return uuid.uuid4().hex


def post(path, payload, token=None, timeout=20):
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    if token:
        headers["Authorization"] = token
    url = f"{BASE_URL}/{path.lstrip('/')}"
    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_token():
    payload = {"enterpriseKey": ENTERPRISE_KEY, "dateTime": now_text()}
    data = post("enterpriseApi/getToken", payload)
    if str(data.get("code")) != "200":
        print(f"[错误] 获取 Token 失败: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)
    return data["data"]


def upload_file(token, file_url, analysis_type, file_type, file_name=None, password=None):
    payload = {
        "requestCode": request_code(),
        "analysisType": analysis_type,
        "fileType": file_type,
        "filePackage": file_url,
    }
    if file_name:
        payload["fileName"] = file_name
    if password:
        payload["passWord"] = password

    data = post("enterpriseApi/fileUpload", payload, token=token)
    if str(data.get("code")) != "200":
        print(f"[错误] 上传失败: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)
    return data["data"]


def poll_result(token, result_id, interval=3, max_wait=60):
    elapsed = 0
    attempt = 0
    while elapsed < max_wait:
        attempt += 1
        payload = {"requestCode": request_code(), "resultId": result_id}
        result = post("enterpriseApi/fileResult", payload, token=token)
        data = result.get("data") or {}
        status = str(data.get("isSuccess", ""))

        print(f"[轮询 {attempt}] isSuccess={status} (已等待 {elapsed}s)", file=sys.stderr)

        if status == "1":
            return data
        if status == "2":
            return data

        time.sleep(interval)
        elapsed += interval

    print(f"[警告] 轮询超时({max_wait}s)，返回最后状态", file=sys.stderr)
    return data


def extract_key_fields(data):
    """提取关键字段，输出简洁结果"""
    output = {
        "状态": "成功" if str(data.get("isSuccess")) == "1" else "失败" if str(data.get("isSuccess")) == "2" else "未知",
        "报告地址": data.get("reportAddress", ""),
        "文件名": data.get("fileName", ""),
        "页数": data.get("pageCount", ""),
        "错误信息": data.get("errorMessage", ""),
    }

    if data.get("creditMessage_new"):
        output["征信数据(详版/简版)"] = data["creditMessage_new"]
    if data.get("creditMessage"):
        output["征信数据(流水/企业)"] = data["creditMessage"]
    if data.get("analysisReport"):
        output["AI分析报告"] = data["analysisReport"]
    if data.get("actualFileType"):
        output["实际文件类型(与上传不一致)"] = data["actualFileType"]

    return output


def main():
    parser = argparse.ArgumentParser(
        description="信贷文件分析工具 — 解析征信报告、银行流水等文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python analyze.py --url "https://example.com/credit.pdf" --type "简版征信"
  python analyze.py --url "https://example.com/detail.pdf" --type "详版征信" --password "abc"
  python analyze.py --url "https://a.com/1.png,https://a.com/2.png" --type "流水" --file-type img
        """,
    )
    parser.add_argument("--url", required=True, help="文件公网 URL（图片可用英文逗号分隔多个）")
    parser.add_argument("--type", required=True, choices=VALID_TYPES, help="分析类型: 详版征信/简版征信/企业征信/流水")
    parser.add_argument("--file-type", default="pdf", choices=VALID_FILE_TYPES, help="文件格式 (默认: pdf)")
    parser.add_argument("--password", default=None, help="PDF 密码（如有）")
    parser.add_argument("--timeout", type=int, default=60, help="轮询超时秒数 (默认: 60)")

    args = parser.parse_args()

    # 1. 获取 Token
    print("[1/3] 获取 Token...", file=sys.stderr)
    token = get_token()
    print("[1/3] Token 获取成功", file=sys.stderr)

    # 2. 上传文件
    print(f"[2/3] 上传文件: {args.type} ({args.file_type})", file=sys.stderr)
    file_name = None
    if args.file_type == "pdf" and not "," in args.url:
        file_name = args.url.rsplit("/", 1)[-1] if "/" in args.url else None
    result_id = upload_file(token, args.url, args.type, args.file_type, file_name, args.password)
    print(f"[2/3] 上传成功, resultId={result_id}", file=sys.stderr)

    # 3. 轮询结果
    print("[3/3] 等待解析结果...", file=sys.stderr)
    data = poll_result(token, result_id, max_wait=args.timeout)

    # 输出结果
    output = extract_key_fields(data)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
