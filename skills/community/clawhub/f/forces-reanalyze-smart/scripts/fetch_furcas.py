#!/usr/bin/env python3
"""
Furcas 工单数据获取脚本

从 furcas.shouqianba.com 系统获取指定时间范围内的工单数据，导出为 CSV。

用法:
    python scripts/fetch_furcas.py -s "2026-04-01" -n "2026-04-30"

前置条件:
    需要在脚本内设置有效的 cookie（从浏览器Furcas页面拷贝）
"""

import requests
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
import time
import argparse
import csv
import os
import sys


@dataclass
class Furcas:
    content: str = field(default="")
    fur_url: str = field(default="")
    fur_status: str = field(default="")
    fur_reason: str = field(default="")
    fur_author: str = field(default="")
    solving_category: str = field(default="")
    solving_modules: str = field(default="")
    overtime: str = field(default="")
    overtime_remark: str = field(default="")


# 解决模块
solving_modules = [
    {"name": "久久折营销", "id": 33},
    {"name": "打印机", "id": 34},
    {"name": "扫码点单", "id": 35},
    {"name": "自营外卖", "id": 117},
    {"name": "收银系统-餐饮", "id": 125},
    {"name": "餐饮版app", "id": 126},
    {"name": "商户运营", "id": 158},
    {"name": "营销门店码", "id": 159},
    {"name": "美/饿外", "id": 171},
    {"name": "校园外卖", "id": 173},
    {"name": "移动点单", "id": 205},
    {"name": "商家小程序", "id": 220},
    {"name": "收银系统-零售", "id": 253},
    {"name": "美/饿/抖外卖", "id": 172},
    {"name": "外部平台授权-团购业务", "id": 232},
    {"name": "极速开票", "id": 261},
    {"name": "对账单", "id": 302},
]

t_component = str([i["id"] for i in solving_modules]).strip("[").strip("]")

# 解决类别（工单复盘拉取用）
solving_category = [
    {"name": "设计如此-无需优化", "id": "1"},
    {"name": "外部原因-无需优化", "id": "2"},
    {"name": "内部原因-已解决", "id": "3"},
    {"name": "内部原因-延期处理", "id": "4"},
    {"name": "内部原因-无法重现", "id": "5"},
]

CATEGORY_NAME_MAP = {
    "设计如此-无需优化": "无需优化-技术介入",
    "外部原因-无需优化": "无需优化-技术介入",
    "内部原因-已解决": "内部原因-已解决",
    "内部原因-延期处理": "内部原因-延期处理",
    "内部原因-无法重现": "内部原因-无法重现",
}

fur_status = [
    {"name": "已创建", "value": "1", "alias": "已创建"},
    {"name": "已解决", "value": "2", "alias": "已关闭"},
    {"name": "已关闭", "value": "3", "alias": "已关闭"},
    {"name": "处理中", "value": "4", "alias": "处理中"},
    {"name": "已回访", "value": "6", "alias": "已关闭"},
]

# !!! 必须设置 FURCAS_COOKIE 环境变量 !!!
# 获取方式：登录 https://furcas.shouqianba.com → F12 Network → 复制完整 Cookie 请求头
# 设置方式：export FURCAS_COOKIE="showStep=true; furcas=xxx; acw_tc=xxx"
cookie = os.environ.get("FURCAS_COOKIE", "")
if not cookie:
    print("错误: 请先设置 FURCAS_COOKIE 环境变量")
    print("export FURCAS_COOKIE='showStep=true; furcas=xxx; acw_tc=xxx'")
    sys.exit(1)


def get_furcas_list(start, end, resolved_reason, need_tag=False):
    url = (
        "https://furcas.shouqianba.com/api/v2/ticket/search?content=&object_sn=&page=1&page_size=300&status=&deleted=0&start="
        + start
        + "&end="
        + end
        + "&follow=false&overtime=false&aggravate=false&c_component=&t_component="
        + t_component
        + "&resolved_reason="
        + resolved_reason
        + "&assignee=&cc2me=false&start_fix_time=&end_fix_time="
    )
    if need_tag:
        url = url + "&tag=a67bc09d-e7e5-4473-a220-03b7e1893b88"
    head = {"Cookie": cookie}
    res = requests.get(url, headers=head)
    return json.loads(res.text)


def get_furcas_operations(ticket_id):
    url = "https://furcas.shouqianba.com/api/v2/ticket/operations?id=" + ticket_id
    head = {"Cookie": cookie}
    res = requests.get(url, headers=head)
    return json.loads(res.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", "-s", required=True, type=str, help="开始时间，如 2026-04-01")
    parser.add_argument("--end", "-n", required=True, type=str, help="结束时间，如 2026-04-30")
    parser.add_argument("--output", "-o", default="furcas.csv", type=str, help="输出CSV路径")
    args = parser.parse_args()

    start_time_str = args.start + " 00:00:00"
    start_seconds = time.mktime(time.strptime(start_time_str, "%Y-%m-%d %H:%M:%S"))
    end_time_str = args.end + " 23:59:59"
    end_seconds = time.mktime(time.strptime(end_time_str, "%Y-%m-%d %H:%M:%S"))

    start = str(int(start_seconds))
    end = str(int(end_seconds))

    csv_headers = [
        "问题描述", "问题链接", "工单状态/修复情况", "问题原因",
        "责任人", "解决类别", "解决模块", "超时时间", "超时备注",
    ]

    with open(args.output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        csv_list = []

        for j in solving_category:
            if j["id"] in ("1", "2"):
                res = get_furcas_list(start, end, j["id"], True)
            else:
                res = get_furcas_list(start, end, j["id"])

            tmp_name = CATEGORY_NAME_MAP.get(j["name"], j["name"])

            for i in res["data"]["list"]:
                operations_res = get_furcas_operations(i["id"])
                reasons = [x for x in operations_res["data"] if "问题原因及解决方式" in x["context"]]
                over_list = [x for x in operations_res["data"] if "更新了工单处理人" in x["context"]]
                overtime_remark = ""
                for detail in reversed(over_list):
                    overtime_remark += (
                        detail["User"]["ding_name"]
                        + "->"
                        + detail["context"].replace("更新了工单处理人：", "")
                        + ": "
                        + detail["ctime"][5:-9].replace("T", " ")
                        + "；"
                    )
                if len(reasons) > 0:
                    fur = Furcas(
                        content=i["content"].replace("\n", " "),
                        fur_url="https://furcas.shouqianba.com/workdetail?id=" + str(i["id"]),
                        fur_status=[a for a in fur_status if a["value"] == str(i["status"])][0]["alias"] if i["status"] else "",
                        fur_reason=[x for x in operations_res["data"] if "问题原因及解决方式" in x["context"]][0]["context"].strip("问题原因及解决方式：").replace("\n", " "),
                        fur_author=[x for x in operations_res["data"] if "问题原因及解决方式" in x["context"]][0]["User"]["ding_name"],
                        solving_category=tmp_name,
                        solving_modules=[a for a in solving_modules if i["t_component"] == a["id"]][0]["name"],
                        overtime=i["overtime"],
                        overtime_remark=overtime_remark,
                    )
                else:
                    fur = Furcas(
                        content=i["content"].replace("\n", " "),
                        fur_url="https://furcas.shouqianba.com/workdetail?id=" + str(i["id"]),
                        fur_status=[a for a in fur_status if a["value"] == str(i["status"])][0]["alias"] if i["status"] else "",
                        solving_category=tmp_name,
                        solving_modules=[a for a in solving_modules if i["t_component"] == a["id"]][0]["name"],
                        overtime=i["overtime"],
                        overtime_remark=overtime_remark,
                    )
                csv_list.append(list(asdict(fur).values()))

        writer.writerow(csv_headers)
        for row in csv_list:
            writer.writerow(row)

    print(f"Done: {len(csv_list)} records written to {args.output}")
