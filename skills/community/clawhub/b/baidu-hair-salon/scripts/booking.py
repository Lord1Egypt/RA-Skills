#!/usr/bin/env python3
"""
理发店预约工具
支持：查看发型师、获取日期、获取时间段、提交预约、查询预约记录
"""

import os
import json as json_module
import requests
import json
import sys
from datetime import datetime, timedelta

BASE_URL = "http://goldsalon999.fun:8888/hair-salon/salon/serve"

# 从 openclaw.json 读取偏好
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")

def load_prefs():
    """从 openclaw.json 加载用户偏好"""
    try:
        with open(OPENCLAW_CONFIG, "r") as f:
            config = json_module.load(f)
        entries = config.get("skills", {}).get("entries", {})
        hair = entries.get("baidu-hair-salon", {})
        return {
            "phone": hair.get("default_phone", ""),
            "person": hair.get("default_person", ""),
            "shop_id": hair.get("last_shop_id", ""),
            "shop_name": hair.get("last_shop_name", ""),
            "staff_id": hair.get("last_staff_id", ""),
            "staff_name": hair.get("last_staff_name", ""),
            "service": hair.get("last_service", ""),
        }
    except Exception:
        return {
            "phone": "",
            "person": "",
            "shop_id": "",
            "shop_name": "",
            "staff_id": "",
            "staff_name": "",
            "service": "",
        }

def save_prefs(prefs):
    """保存用户偏好到 openclaw.json"""
    try:
        with open(OPENCLAW_CONFIG, "r") as f:
            config = json_module.load(f)
    except Exception:
        config = {}

    if "skills" not in config:
        config["skills"] = {}
    if "entries" not in config["skills"]:
        config["skills"]["entries"] = {}
    config["skills"]["entries"]["baidu-hair-salon"] = prefs

    with open(OPENCLAW_CONFIG, "w") as f:
        json_module.dump(config, f, ensure_ascii=False, indent=2)

DEFAULT_PHONE = ""
DEFAULT_PERSON = ""
DEFAULT_SHOP_ID = ""
SHOP_NAME = ""
SHOP_PHONE = ""

HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Origin": "http://goldsalon999.fun:9008",
    "Pragma": "no-cache",
    "Referer": "http://goldsalon999.fun:9008/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5) AppleWebKit/537.36"
}


def get_staff_list(shop_id=None):
    """获取发型师列表"""
    shop_id = shop_id or DEFAULT_SHOP_ID
    url = f"{BASE_URL}/userList?shopId={shop_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def get_shop_list():
    """获取店铺列表"""
    url = f"{BASE_URL}/shopList?shopType=1"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def get_service_types(serve_type="hair"):
    """获取服务项目类型"""
    url = f"{BASE_URL}/serviceType?serveType={serve_type}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def get_date_list():
    """获取可预约日期列表"""
    url = f"{BASE_URL}/dateList"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def get_time_slots(staff_id, book_date, serve_type="hair"):
    """获取指定日期和发型师的可预约时间段"""
    url = f"{BASE_URL}/timeSlots?serveType={serve_type}&staffId={staff_id}&bookDate={book_date}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def book_appointment(staff_id, staff_name, book_date, book_time, project="男发精剪",
                     service_time=0.5, book_person=DEFAULT_PERSON,
                     book_phone=DEFAULT_PHONE, serve_type="hair", period=1):
    """提交预约"""
    url = f"{BASE_URL}/book"

    payload = {
        "project": project,
        "serviceTime": service_time,
        "shopName": SHOP_NAME,
        "shopPhone": SHOP_PHONE,
        "staffId": staff_id,
        "staffName": staff_name,
        "bookDate": book_date,
        "bookTime": book_time,
        "bookPerson": book_person,
        "bookPhone": book_phone,
        "shopType": "1",
        "serveType": serve_type,
        "period": period
    }

    headers = HEADERS.copy()
    headers["Content-Type"] = "application/json"

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def get_book_list(phone=DEFAULT_PHONE):
    """查询预约记录"""
    url = f"{BASE_URL}/bookList?bookPhone={phone}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def main():
    # 加载偏好
    prefs = load_prefs()
    global DEFAULT_PHONE, DEFAULT_PERSON, DEFAULT_SHOP_ID, SHOP_NAME, SHOP_PHONE
    DEFAULT_PHONE = prefs["phone"]
    DEFAULT_PERSON = prefs["person"]

    if len(sys.argv) < 2:
        print("用法: python booking.py <命令> [参数]")
        print("")
        print("命令:")
        print("  shops                    获取店铺列表")
        print("  services [serve_type]    获取服务项目列表（默认 hair）")
        print("  staff [shop_id]          获取发型师列表（可选指定店铺）")
        print("  dates                    获取可预约日期")
        print("  slots <staff_id> <date> 获取时间段")
        print("  book <staff_id> <staff_name> <date> <time> <phone> [project]  提交预约")
        print("  list [phone]             查询预约记录")
        print("  pref-get                 查看当前偏好")
        print("  pref-set <phone> <person> [shop_id] [shop_name] [staff_id] [staff_name] [service]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "shops":
        result = get_shop_list()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "services":
        serve_type = sys.argv[2] if len(sys.argv) > 2 else "hair"
        result = get_service_types(serve_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "staff":
        shop_id = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_staff_list(shop_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "dates":
        result = get_date_list()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "slots":
        if len(sys.argv) < 4:
            print("用法: python booking.py slots <staff_id> <date>")
            sys.exit(1)
        staff_id = sys.argv[2]
        date = sys.argv[3]
        result = get_time_slots(staff_id, date)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "book":
        if len(sys.argv) < 6:
            print("用法: python booking.py book <staff_id> <staff_name> <date> <time> <phone> [project]")
            sys.exit(1)
        staff_id = int(sys.argv[2])
        staff_name = sys.argv[3]
        date = sys.argv[4]
        time = sys.argv[5]
        phone = sys.argv[6]
        project = sys.argv[7] if len(sys.argv) > 7 else "男发精剪"
        result = book_appointment(staff_id, staff_name, date, time, project, book_phone=phone)
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 预约成功则保存偏好
        if result.get("code") == 200:
            # 尝试从 booking.py 内部获取店铺信息，这里从参数/环境推断
            save_prefs({
                "default_phone": phone,
                "default_person": prefs.get("person", ""),
                "last_shop_id": prefs.get("shop_id", ""),
                "last_shop_name": prefs.get("shop_name", ""),
                "last_staff_id": str(staff_id),
                "last_staff_name": staff_name,
                "last_service": project,
            })
            print(f"\n[偏好已保存] phone={phone}, staff={staff_name}, project={project}")

    elif cmd == "list":
        phone = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PHONE
        result = get_book_list(phone)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "pref-get":
        print(json.dumps(prefs, ensure_ascii=False, indent=2))

    elif cmd == "pref-set":
        if len(sys.argv) < 4:
            print("用法: python booking.py pref-set <phone> <person> [shop_id] [shop_name] [staff_id] [staff_name] [service]")
            sys.exit(1)
        phone = sys.argv[2]
        person = sys.argv[3]
        shop_id = sys.argv[4] if len(sys.argv) > 4 else ""
        shop_name = sys.argv[5] if len(sys.argv) > 5 else ""
        staff_id = sys.argv[6] if len(sys.argv) > 6 else ""
        staff_name = sys.argv[7] if len(sys.argv) > 7 else ""
        service = sys.argv[8] if len(sys.argv) > 8 else ""
        save_prefs({
            "default_phone": phone,
            "default_person": person,
            "last_shop_id": shop_id,
            "last_shop_name": shop_name,
            "last_staff_id": staff_id,
            "last_staff_name": staff_name,
            "last_service": service,
        })
        print("偏好已保存")
        print(json.dumps(load_prefs(), ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
