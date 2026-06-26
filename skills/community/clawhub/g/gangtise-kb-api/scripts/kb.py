import os
import sys
from typing import List, Optional
import requests
import datetime
from io import TextIOWrapper
import locale

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import (
    GTS_AUTHORIZATION,
    RAG_URL,
    FILE_TYPE_MAP_REVERSE,
    FILE_TYPE_MAP,
    format_response,
    check_version,
)

from get_file import download_files

def _normalize_file_types(raw: Optional[str]) -> Optional[List[str]]:
    if not raw:
        return None
    result: List[str] = []
    for item in raw.replace("，", ",").split(","):
        if item.strip() and item.strip() not in result:
            result.append(item.strip())
    return result or None

def _format_rag_result(result: dict):
    _result = [
        {
            "标题": result["title"],
            "文件时间": result["time"],
            "摘要": result["content"],
            "类型": FILE_TYPE_MAP_REVERSE[result["resourceType"]],
            "类型中ID": result["sourceId"],
        }
        for result in result["data"]
    ]
    _result = {
        "state": "success" if result["code"] in [200, "000000"] or result["status"] == True else "error",
        "message": result["msg"],
        "data": [{"data": _result, "module": "kb", "type": "files"}],
    }
    return _result


def rag_files_finder(
    query: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    file_types: Optional[List[str]] = None,
    limit: Optional[int] = None,
    output: Optional[str] = None,
    download: bool = False,
    output_dir: Optional[str] = None,
    download_types: Optional[List[str]] = None,
):
    try:
        try:
            if not check_version():
                update_sh = os.path.join(script_dir, "update.sh")
                print(f"[WARNING] 存在 Gangtise skills 版本更新，可以执行 {update_sh} 更新，请与用户确认是否更新\n")
        except Exception as e:
            print(f"[WARNING] 检查 Gangtise skills 版本失败\n")
        headers = {
            "Authorization": GTS_AUTHORIZATION,
        }

        payload = {
            "query": query,
            "startTime": datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000 if start_date else None,
            "endTime": datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000 if end_date else None,
            "resourceTypes": [FILE_TYPE_MAP[file_type] for file_type in file_types] if file_types else None,
            "top": limit,
        }
        response = requests.post(RAG_URL, headers=headers, json=payload, timeout=300)
        if response.status_code != 200:
            return format_response({"state": "error", "message": response.text}, "rag")
        response = response.json()
        response = _format_rag_result(response)
        additional_message = None
        if download:
            additional_message = download_files(
                response.get("data", [{}])[0].get("data", []),
                "kb",
                output_dir=output_dir,
                download_types=download_types or ["pdf"],
            )
        return format_response(response, "rag", output=output, additional_message=additional_message or "")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            "rag",
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="RAG 文件检索命令行：按查询语句检索相关文件。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-q", "--query", default="", help="检索查询语句")
    parser.add_argument("-sd", "--start-date", default=None, help="开始日期，如 2026-01-01")
    parser.add_argument("-ed", "--end-date", default=None, help="结束日期，如 2026-12-31")
    parser.add_argument(
        "--file-types",
        default=None,
        help="文件类型，逗号分隔，可选：研究报告,外资研报,内部报告,AI云盘,首席观点,公司公告,产业公众号,会议纪要,调研纪要,网络纪要",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=None,
        type=int,
        help="结果数量限制",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="结果保存路径（当前版本由后端统一管理，本参数暂不生效）",
    )
    parser.add_argument(
        "-d",
        "--download",
        default=False,
        type=bool,
        help="是否在检索后自动下载对应文件，默认不下载",
    )
    parser.add_argument(
        "-od",
        "--output_dir",
        default=None,
        help="下载文件保存路径，建议使用绝对路径",
    )
    parser.add_argument(
        "-dt",
        "--download-types",
        default="pdf",
        help="下载的文件类型，逗号分隔，可选值：pdf, markdown",
    )
    args = parser.parse_args()

    query = args.query.strip()
    if not query:
        parser.error("必须提供查询语句：-q/--query")

    start_date = args.start_date
    end_date = args.end_date
    file_types = _normalize_file_types(args.file_types)

    limit = args.limit

    download = args.download or False
    output_dir = args.output_dir or None
    if not download and output_dir:
        print(f"[WARNING] 参数 -od/--output_dir 仅在下载文件时有效，已忽略\n")
        output_dir = None
    download_types = _normalize_file_types(args.download_types) or ["pdf"]

    out = rag_files_finder(
        query=query,
        start_date=start_date,
        end_date=end_date,
        file_types=file_types,
        limit=limit,
        output=args.output,
        download=download,
        output_dir=output_dir,
        download_types=download_types,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()