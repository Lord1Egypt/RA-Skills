import os
import re
from typing import Dict, List, Any, Optional
# import logging
# from logging.handlers import TimedRotatingFileHandler
import pandas as pd
import datetime
import json
import requests


GTS_AUTHORIZATION_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".authorization")
GTS_ACCESS_KEY = os.getenv("GTS_ACCESS_KEY", None)
GTS_SECRET_KEY = os.getenv("GTS_SECRET_KEY", None)

# 通过 ak/sk 获取 临时 authorization

AUTHORIZATION_URL = f"https://open.gangtise.com/application/auth/oauth/open/loginV2"

def get_authorization(ak: str, sk: str):
    payload = {
        "accessKey": ak,
        "secretAccessKey": sk
    }
    response = requests.post(AUTHORIZATION_URL, json=payload)
    if response.status_code != 200:
        return None
    try:
        return response.json()["data"]["accessToken"]
    except Exception as e:
        return None

GTS_AUTHORIZATION = None
if GTS_ACCESS_KEY and GTS_SECRET_KEY:
    GTS_AUTHORIZATION = get_authorization(GTS_ACCESS_KEY, GTS_SECRET_KEY)
elif os.path.exists(GTS_AUTHORIZATION_PATH):
    with open(GTS_AUTHORIZATION_PATH, "r", encoding="utf-8") as f:
        content = json.load(f)
        if content.get("accessKey", None) and content.get("secretAccessKey", None):
            GTS_AUTHORIZATION = get_authorization(content["accessKey"], content["secretAccessKey"])
        else:
            GTS_AUTHORIZATION = None

GTS_SAVE_FILE = os.getenv("GTS_SAVE_FILE", False)
GTS_SAVE_EXTENSION = os.getenv("GTS_SAVE_EXTENSION", "md")

GANGTISE_DATA_DOMAIN = os.getenv("GANGTISE_DOMAIN", "https://open.gangtise.com/application/open-data")
GANGTISE_INSIGHT_DOMAIN = os.getenv("GANGTISE_INSIGHT_DOMAIN", "https://open.gangtise.com/application/open-insight")

RAG_URL = f"{GANGTISE_DATA_DOMAIN}/ai/search/knowledge_base"
FILE_URL = f"{GANGTISE_DATA_DOMAIN}/ai/resource/download"
SUMMARY_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/summary/v2/download/file"
COMPANY_ANNOUNCEMENT_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/announcement/download/file"
REPORT_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/broker-report/download/file"
FOREIGN_REPORT_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/foreign-report/download/file"

def _find_openclaw_root():
    """向上遍历目录直到找到 .openclaw，返回其上级目录作为执行目录"""
    path = os.path.abspath(os.path.dirname(__file__))
    openclaw_dir_got = False
    while path != os.path.dirname(path):
        dir_name = os.path.basename(path)
        if dir_name in (".openclaw"):
            openclaw_dir_got = True
            return os.path.abspath(path)
        path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in (".agent"):
                openclaw_dir_got = True
                return os.path.abspath(path)
            path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in ("workspace"):
                openclaw_dir_got = True
                return os.path.abspath(path)
            path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in ("skills"):
                openclaw_dir_got = True
                return os.path.abspath(os.path.dirname(path))
            path = os.path.dirname(path)
    return os.path.abspath(os.getcwd())

openclaw_root = _find_openclaw_root()
if openclaw_root.endswith("workspace"):
    gangtise_workspace_path = os.path.join(openclaw_root, "gangtise")
else:
    gangtise_workspace_path = os.path.join(openclaw_root, "workspace", "gangtise")
if not os.path.exists(gangtise_workspace_path):
    os.makedirs(gangtise_workspace_path, exist_ok=True)

usage_dir = os.path.join(gangtise_workspace_path, ".usage")
if not os.path.exists(usage_dir):
    os.makedirs(usage_dir, exist_ok=True)

file_dir = os.path.join(gangtise_workspace_path, "files")
if not os.path.exists(file_dir):
    os.makedirs(file_dir, exist_ok=True)

FILE_TYPE_MAP = {
    "研究报告": 10,
    "外资研报": 11,
    "内部报告": 20,
    "AI云盘": 30,
    "首席观点": 40,
    "公司公告": 50,
    "港股公告": 51,
    "会议纪要": 60,
    "调研纪要": 70,
    "网络纪要": 80,
    "产业公众号": 90,
}

FILE_TYPE_MAP_REVERSE = {
    v: k for k, v in FILE_TYPE_MAP.items()
}

def data_to_md(data: pd.DataFrame, range: List[int]=None, max_cell_length: int=None):
    data_copy = data.copy()
    if "metadata" in data_copy.columns:
        data_copy = data_copy.drop(columns=["metadata"])
    content = "| " + " | ".join(data_copy.columns) + " |\n"
    content += "| " + " | ".join(["-" for _ in data_copy.columns]) + " |\n"
    omitted = False
    for i, row in enumerate(data_copy.to_dict(orient="records")):
        if range:
            if i in range:
                if max_cell_length:
                    content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "")[:max_cell_length]+"..." if len(re.sub(r"\s+", " ", str(row[key])).replace("|", "")) > max_cell_length else re.sub(r"\s+", " ", str(row[key])).replace("|", "") for key in row.keys()]) + " |\n"
                else:
                    content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "") for key in row.keys()]) + " |\n"
            elif not omitted:
                content += "| ... |\n"
                omitted = True
        else:
            if max_cell_length:
                content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "")[:max_cell_length]+"..." if len(re.sub(r"\s+", " ", str(row[key])).replace("|", "")) > max_cell_length else re.sub(r"\s+", " ", str(row[key])).replace("|", "") for key in row.keys()]) + " |\n"
            else:
                content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "") for key in row.keys()]) + " |\n"
    content = content[:-1]
    return content.strip()

def add_usages(usages_list: List[Dict[str, Any]]):
    usages = {}
    for usages_item in usages_list:
        if len(usages_item) == 0:
            continue
        for k,v in usages_item.items():
            if k not in usages:
                usages[k] = v
            else:
                usages[k] = usages[k] + v
    return usages

def format_response(response: dict, method_name: str, output: Optional[str] = None, additional_message: str = ""):
    
    # 保存usage
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H%M%S")
    usage_path = os.path.join(usage_dir, f"{today}.json")
    if response.get("usage", None):
        if os.path.exists(usage_path):
            with open(usage_path, "r", encoding="utf-8") as f:
                usage = json.load(f)
            if now in usage:
                now_usage = add_usages([response["usage"], usage[now]])
            else:
                now_usage = response["usage"]
            usage.update({now: now_usage})
        else:
            usage = {now: response["usage"]}
        with open(usage_path, "w", encoding="utf-8") as f:
            json.dump(usage, f, ensure_ascii=False)

    # 保存结果
    return_message = ""
    method_name_map = {
        "block_component": "板块成分信息",
        "financial": "财务数据",
        "industry_indicator": "行业指标数据",
        "main_business": "主营业务数据",
        "quote": "行情数据",
        "security": "证券信息",
        "shareholder": "股东数据",
        "valuation": "估值数据",
        "rag": "知识库检索",
    }
    if response["state"] == "success":
        for item in response["data"]:
            module_name = item["module"]
            data = item["data"]
            if GTS_SAVE_FILE:
                if output:
                    process_path = output
                    if os.path.exists(process_path):
                        return_message = "错误信息：文件已存在"
                        return return_message
                else:
                    extension = GTS_SAVE_EXTENSION
                    process_dir = os.path.join(gangtise_workspace_path, method_name)
                    if not os.path.exists(process_dir):
                        os.makedirs(process_dir, exist_ok=True)
                    # now = datetime.datetime.now().strftime("%H%M%S")
                    now = 1
                    process_path = os.path.join(process_dir, f"{module_name}_{now}.{extension}")
                    max_retries = 10
                    for file in os.listdir(process_dir):
                        if file.startswith(f"{module_name}_") and file.endswith(f".{extension}"):
                            max_retries = max(max_retries, int(file.split("_")[-1].split(".")[0])+10)
                    while os.path.exists(process_path) and max_retries > 0:
                        # now = datetime.datetime.now().strftime("%H%M%S")
                        now += 1
                        process_path = os.path.join(process_dir, f"{module_name}_{now}.{extension}")
                        max_retries -= 1
                        # sleep(1)
                    if max_retries == 0:
                        return_message = "错误信息：文件存储系统繁忙，请稍后再试"
                        return return_message
                if GTS_SAVE_EXTENSION == "md":
                    with open(process_path, "w", encoding="utf-8") as f:
                        for i, file in enumerate(data):
                            f.write(f"### 查询结果 {i+1}\n\n")
                            f.write(f"标题：{file['标题']}\n")
                            f.write(f"文件时间：{file['文件时间']}\n")
                            f.write(f"内容：\"\"\"\n{file['摘要']}\n\"\"\"\n")
                            f.write(f"file-type：{file['类型']}\n")
                            f.write(f"file-id：{file['类型中ID']}")
                            if i < len(data) - 1:
                                f.write("\n\n---\n\n")
                elif GTS_SAVE_EXTENSION == "json":
                    with open(process_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False)
                sample_data = ""
                for file in data:
                    sample_data += f"标题：{file['标题']}\n"
                    sample_data += f"文件时间：{file['文件时间']}\n"
                    sample_data += f"内容：\"\"\"\n{file['摘要']}\n\"\"\"\n"
                    sample_data += f"file-type：{file['类型']}\n"
                    sample_data += f"file-id：{file['类型中ID']}"
                    sample_data += "\n\n---\n\n"
                return_message += "### " + method_name_map[method_name] + " 查询结果:\n\n---\n\n" + sample_data + f"所有查询结果已保存到{GTS_SAVE_EXTENSION}：\"" + os.path.abspath(process_path) + "\""
                return_message += f"\n\n查询结果共计{len(data)}条"
            else:
                sample_data = ""
                for i, file in enumerate(data):
                    sample_data += f"标题：{file['标题']}\n"
                    sample_data += f"文件时间：{file['文件时间']}\n"
                    if file.get("摘要", None):
                        sample_data += f"摘要：\"\"\"\n{file['摘要']}\n\"\"\"\n"
                    sample_data += f"file-type：{file['类型']}\n"
                    sample_data += f"file-id：{file['类型中ID']}"
                    sample_data += "\n\n---\n\n"
                return_message += "### " + method_name_map[method_name] + "查询结果:\n\n---\n\n" + sample_data
                return_message += f"查询结果共计{len(data)}条"
    else:
        return_message = "调用gangtise服务端失败，错误信息：" + response["message"]
    if additional_message:
        return_message += "\n" + additional_message
    return return_message

def load_securities_from_file(path: str) -> List[str]:
    full_path = path
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"证券文件不存在: {path}")
    df = pd.read_csv(full_path)
    if "security_abbr" in df.columns:
        return [str(x) for x in df["security_abbr"].dropna().tolist()]
    if "security_code" in df.columns:
        return [str(x) for x in df["security_code"].dropna().tolist()]
    raise ValueError("证券文件必须包含 security_code 或 security_abbr 列")

OPENAPI_SKILL_VERSION = "1.4.2"
SKILL_CHECK_URL = "https://open.gangtise.com/application/skills-backend/version?skill=openapi"

def check_version(large_version: bool = True):
    response = requests.get(SKILL_CHECK_URL)
    if response.status_code == 200 and large_version:
        return response.json()["state"] == "success" and response.json()["version"].split(".")[0] == OPENAPI_SKILL_VERSION.split(".")[0] and response.json()["version"].split(".")[1] == OPENAPI_SKILL_VERSION.split(".")[1]
    elif response.status_code == 200 and not large_version:
        return response.json()["state"] == "success" and response.json()["version"] == OPENAPI_SKILL_VERSION
    else:
        return False

if __name__ == "__main__":
    print("检查 gangtise-kb 相关配置")
    if not os.path.exists(GTS_AUTHORIZATION_PATH):
        print("  无法检测到gangtise授权文件, gangtise-kb 无法正常工作")
    elif GTS_AUTHORIZATION is None:
        print("  授权文件存在, 但无法获取gangtise授权, gangtise-kb 无法正常工作")
    else:
        print("  检测到gangtise授权文件, gangtise-kb 可以正常工作")
    if GTS_SAVE_FILE is None:
        print("  环境变量 GTS_SAVE_FILE 未配置, 默认值为 False, gangtise服务端 将不保存查询结果到文件中")
    elif GTS_SAVE_FILE == "True":
        print("  环境变量 GTS_SAVE_FILE 为 True, gangtise服务端 将保存查询结果到文件中")
    else:
        print("  环境变量 GTS_SAVE_FILE 为 False, gangtise服务端 将不保存查询结果到文件中")
    if check_version(large_version=False):
        print("  gangtise-kb 版本为最新")
    else:
        print("  gangtise-kb 版本不是最新, 建议进行更新")
    print(f"  gangtise-kb 工作文件目录: {gangtise_workspace_path}")