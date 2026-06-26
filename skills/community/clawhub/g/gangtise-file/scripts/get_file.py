import os
import sys
import requests
from urllib.parse import unquote
from io import TextIOWrapper
from typing import List
from typing import Optional
import locale

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import (
    GTS_AUTHORIZATION,
    FILE_URL,
    SUMMARY_DOWNLOAD_URL,
    COMPANY_ANNOUNCEMENT_DOWNLOAD_URL,
    REPORT_DOWNLOAD_URL,
    FOREIGN_REPORT_DOWNLOAD_URL,
    FILE_TYPE_MAP,
    file_dir,
    gangtise_workspace_path,
    check_version,
)

def safe_file_title(file_item):
    title = file_item["title"]
    not_allow_title_symbol = [
        "\\", ":", "*", "?", "\"", "<", ">", "|", 
        "=", "&", "\0"
    ]
    for symbol in not_allow_title_symbol:
        title = title.replace(symbol, "")
    title = title.replace(" ", "_")
    return title

def get_file(
    file_id: str,
    file_type: str,
    output: str = None,
    download_type: str = "pdf", # pdf, markdown
    output_dir: str = None, # 该参数仅在download_files中使用
    title: str = None, # 该参数仅在download_files中使用
):
    title = title.replace("/", "_") if title else None
    try:
        try:
            if not check_version():
                print(f"[WARNING] 存在 Gangtise skills 版本更新，请与用户确认是否更新\n")
        except Exception:
            print(f"[WARNING] 检查 Gangtise skills 版本失败\n")
        headers = {
            "Authorization": GTS_AUTHORIZATION,
        }
        task_status = False

        # 使用对应接口下载文件
        url_map = {
            "会议纪要": SUMMARY_DOWNLOAD_URL,
            "公司公告": COMPANY_ANNOUNCEMENT_DOWNLOAD_URL,
            "研究报告": REPORT_DOWNLOAD_URL,
            "外资研报": FOREIGN_REPORT_DOWNLOAD_URL,
        }
        download_type_map = {
            "pdf": 1,
            "markdown": 2,
        }
        params_map = {
            "会议纪要": {
                "summaryId": file_id,
            },
            "研究报告": {
                "reportId": file_id,
                "fileType": download_type_map[download_type],
            },
            "外资研报": {
                "reportId": file_id,
                "fileType": download_type_map[download_type],
            },
            "公司公告": {
                "announcementId": file_id,
                "fileType": download_type_map[download_type],
            },
        }
        if file_type in url_map:
            response = requests.get(url_map[file_type], headers=headers, params=params_map[file_type], timeout=300)
            if response.status_code != 200:
                return f"获取文件失败：{response.status_code} {response.text}"
            return_message = ""
            if response.headers.get("Content-Type") == "application/json":
                return f"不存在文件，为网络地址：{response.json()['url']}"

        # 如果不行，尝试FILE_URL
        else:
            params = {
                "sourceId": file_id,
                "resourceType": FILE_TYPE_MAP[file_type],
            }
            response = requests.get(FILE_URL, headers=headers, params=params, timeout=300)
            if response.status_code != 200:
                return f"获取文件失败：{response.status_code} {response.text}"
            return_message = ""
            if response.headers.get("Content-Type") == "application/json":
                return f"不存在文件，为网络地址：{response.json()['url']}"
        if output:
            if output.split(".")[-1] != response.headers["Content-Disposition"].split("filename=")[1].split(".")[-1]:
                if len(response.headers["Content-Disposition"].split("filename=")) > 1:
                    output = ".".join(output.split(".")[:-1]) + "." + unquote(response.headers["Content-Disposition"].split("filename=")[1]).split(".")[-1]
                else:
                    output = ".".join(output.split(".")[:-1]) + "." + unquote(response.headers["Content-Disposition"].split("filename*=utf-8''")[1]).split(".")[-1]
            output = safe_file_title({"title": output, "url": "."+output.split(".")[-1]})
            return_message = f"文件保存路径已自动修正，并保存到：{output}"
        elif output_dir:
            if len(response.headers["Content-Disposition"].split("filename=")) > 1:
                file_name = unquote(response.headers["Content-Disposition"].split("filename=")[1])
            else:
                file_name = unquote(response.headers["Content-Disposition"].split("filename*=utf-8''")[1])
            file_name = os.path.basename(file_name)
            if title:
                file_name = title + "." + file_name.split(".")[-1]
            output = os.path.join(output_dir, file_name)
            if output.startswith("\""):
                output = output[1:]
            if output.endswith("\""):
                output = output[:-1]
            output = safe_file_title({"title": output, "url": "."+output.split(".")[-1]})
            return_message = f"文件已保存到：{output}"
        else:
            if len(response.headers["Content-Disposition"].split("filename=")) > 1:
                file_name = unquote(response.headers["Content-Disposition"].split("filename=")[1])
            else:
                file_name = unquote(response.headers["Content-Disposition"].split("filename*=utf-8''")[1])
            file_name = os.path.basename(file_name)
            output = os.path.join(file_dir, file_name)
            if output.startswith("\""):
                output = output[1:-1]
            output = safe_file_title({"title": output, "url": "."+output.split(".")[-1]})
            return_message = f"文件已保存到：{output}"
        with open(output, "wb") as f:
            f.write(response.content)
        return return_message
    except Exception as e:
        return f"获取文件失败：{str(e)}"

def download_files(files: List[dict], method_name: str, output_dir: Optional[str] = None, download_types: Optional[List[str]] = None):
    target_dir = output_dir or os.path.join(gangtise_workspace_path, method_name)
    os.makedirs(target_dir, exist_ok=True)
    failed_message = []

    # 基于 (类型, 类型中ID) 去重，避免重复下载同一文件
    unique_files: List[dict] = []
    seen: set[tuple[str, str]] = set()
    for file in files or []:
        file_type = str(file.get("类型", "") or "").strip()
        file_id = str(file.get("类型中ID", "") or "").strip()
        if not file_type or not file_id:
            continue
        key = (file_type, file_id)
        if key in seen:
            continue
        seen.add(key)
        unique_files.append(file)

    for file in unique_files:
        for download_type in (download_types or ["pdf"]):
            return_message = get_file(
                file["类型中ID"],
                file["类型"],
                output=None,
                output_dir=target_dir,
                title=file.get("标题"),
                download_type=download_type,
            )
            if "文件已保存到" not in return_message:
                failed_message.append({"title": file["标题"], "message": return_message, "download_type": download_type, "web_file": True if file.get("网络连接", "") else False})
    if len(failed_message) == len(unique_files) and unique_files:
        return_message = "\n".join([f"- {x['title']}({x['download_type']})：{'是网络文件' if x['web_file'] else x['message']}" for x in failed_message])
    elif len(failed_message) > 0:
        return_message = f"部分文件下载成功，并保存到：{target_dir}"
        return_message += "; 其中有下载失败的文件：\n" + "\n".join([f"- {x['title']}({x['download_type']})：{'是网络文件' if x['web_file'] else x['message']}" for x in failed_message])
    else:
        return_message = f"文件全部下载成功，并保存到：{target_dir}"
    return return_message

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="RAG 文件检索命令行：按查询语句检索相关文件。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-id", "--file-id", default="", help="文件ID")
    parser.add_argument("-type", "--file-type", default="", help="文件类型")
    parser.add_argument("-o", "--output", default="", help="输出文件路径")
    parser.add_argument("-dt", "--download-type", default="pdf", help="下载类型")

    args = parser.parse_args()

    file_id = args.file_id.strip()
    if not file_id:
        parser.error("必须提供文件ID：-id/--file-id")

    file_type = args.file_type.strip()
    if not file_type:
        parser.error("必须提供文件类型：-type/--file-type")

    out = get_file(
        file_id=file_id,
        file_type=file_type,
        output=args.output,
        download_type=args.download_type,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors='ignore')
    main()