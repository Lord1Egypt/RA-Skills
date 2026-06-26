# -*- coding: utf-8 -*-
"""
蛋叔商城 MCP Server 调用脚本
解决 Windows PowerShell/cmd 下 curl 中文编码问题
"""
import requests
import json
import sys
import os

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

def call_dangaoss(tool_name, arguments):
    """调用蛋叔商城 MCP Server"""
    url = "https://www.dangaoss.com/dsapi/workbuddy/mcp_server"

    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=60
        )
        result = response.json()

        # 解析业务数据
        if 'result' in result and 'content' in result['result']:
            business_text = result['result']['content'][0]['text']
            return json.loads(business_text)
        return result

    except Exception as e:
        return {"code": 500, "msg": "系统繁忙，请稍后重试", "data": None}


def get_addr_list(user_token, city_name):
    """获取地址列表"""
    return call_dangaoss("getAddrList", {
        "user_token": user_token,
        "city_name": city_name
    })


def search_products(user_token, aid, keyword, cat_id, page=1):
    """搜索商品"""
    return call_dangaoss("sweets_lst", {
        "user_token": user_token,
        "aid": aid,
        "keyword": keyword,
        "cat_id": cat_id,
        "page": page
    })


def get_order_url(user_token, aid, spec_id, city_name, quantitys=1):
    """生成下单链接"""
    return call_dangaoss("getOrderaddr", {
        "user_token": user_token,
        "aid": aid,
        "spec_id": spec_id,
        "city_name": city_name,
        "quantitys": quantitys
    })


def add_addr(user_token, province, city, area, addr, name, phone):
    """添加收货地址"""
    return call_dangaoss("addAddrList", {
        "user_token": user_token,
        "province": province,
        "city": city,
        "area": area,
        "addr": addr,
        "name": name,
        "phone": phone
    })


def get_order_status(user_token, scene):
    """订单状态查询"""
    return call_dangaoss("getOrderStatus", {
        "user_token": user_token,
        "scene": scene
    })


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python dgss.py <命令> <参数JSON>")
        print("示例: python dgss.py getAddrList '{\"user_token\":\"xxx\",\"city_name\":\"北京市\"}'")
        sys.exit(1)

    command = sys.argv[1]
    # 处理 Windows cmd 引号问题：去除首尾的单引号或双引号
    raw_args = sys.argv[2]
    if raw_args.startswith("'") and raw_args.endswith("'"):
        raw_args = raw_args[1:-1]
    elif raw_args.startswith('"') and raw_args.endswith('"'):
        raw_args = raw_args[1:-1]
    args = json.loads(raw_args)

    if command == "getAddrList":
        result = get_addr_list(args["user_token"], args["city_name"])
    elif command == "sweets_lst":
        result = search_products(args["user_token"], args["aid"], args["keyword"], args["cat_id"], args.get("page", 1))
    elif command == "getOrderaddr":
        result = get_order_url(args["user_token"], args["aid"], args["spec_id"], args["city_name"], args.get("quantitys", 1))
    elif command == "addAddrList":
        result = add_addr(args["user_token"], args["province"], args["city"], args["area"], args["addr"], args["name"], args["phone"])
    elif command == "getOrderStatus":
        result = get_order_status(args["user_token"], args["scene"])
    else:
        print(json.dumps({"code": 400, "msg": f"未知命令: {command}"}))
        sys.exit(1)

    # 输出结果（UTF-8）
    print(json.dumps(result, ensure_ascii=False, indent=2))
