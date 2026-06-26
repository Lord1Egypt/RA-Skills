#!/usr/bin/env python3
"""
FortiGate 配置 Skill - 工控增强版
支持基础防火墙配置及工控协议（Modbus、IEC104、S7等）的安全策略管理。
"""

import os
import sys
import json
import argparse
import requests
import urllib3

# 尝试导入 tabulate，用于美化输出
try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

# 禁用 SSL 证书警告（如果使用自签名证书）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------- 配置读取 ----------
FGT_HOST = os.environ.get("FORTIGATE_HOST")
FGT_TOKEN = os.environ.get("FORTIGATE_TOKEN")
FGT_PORT = os.environ.get("FORTIGATE_PORT", "443")
FGT_VERIFY_SSL = os.environ.get("FORTIGATE_VERIFY_SSL", "false").lower() == "true"

if not FGT_HOST or not FGT_TOKEN:
    print("错误：必须设置环境变量 FORTIGATE_HOST 和 FORTIGATE_TOKEN")
    sys.exit(1)

BASE_URL = f"https://{FGT_HOST}:{FGT_PORT}/api/v2"
HEADERS = {
    "Authorization": f"Bearer {FGT_TOKEN}",
    "Content-Type": "application/json"
}


# ---------- API 调用工具 ----------
def call_api(method, path, data=None, params=None):
    """发送 API 请求并返回解析后的 JSON 响应，出错时返回包含 error 字段的字典"""
    url = f"{BASE_URL}/{path.lstrip('/')}"
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=HEADERS,
            json=data,
            params=params,
            verify=FGT_VERIFY_SSL,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        if response is not None and response.text:
            try:
                error_json = response.json()
                error_detail = error_json.get("error", {}).get("message", response.text)
            except:
                error_detail = response.text
        return {"error": f"HTTP {response.status_code}: {error_detail}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"网络请求失败: {e}"}
    except json.JSONDecodeError:
        return {"error": "API 返回了非 JSON 格式的响应"}


# ---------- 对象存在性检查 ----------
def address_exists(name):
    """检查地址对象是否存在，返回布尔值"""
    result = call_api("GET", f"cmdb/firewall/address/{name}")
    if "error" in result or result.get("http_status") == 404:
        return False
    return bool(result.get("results"))


def policy_exists(policy_id):
    """检查策略是否存在，返回布尔值"""
    result = call_api("GET", "cmdb/firewall/policy/", params={"policyid": policy_id})
    if "error" in result:
        return False
    results = result.get("results", [])
    return len(results) > 0


def service_exists(name):
    """检查自定义服务对象是否存在"""
    result = call_api("GET", f"cmdb/firewall.service/custom/{name}")
    return not ("error" in result) and bool(result.get("results"))


def ips_sensor_exists(name):
    """检查 IPS 传感器是否存在"""
    result = call_api("GET", f"cmdb/ips/sensor/{name}")
    return not ("error" in result) and bool(result.get("results"))


# ---------- 基础操作函数 ----------
def list_policies():
    """列出所有防火墙策略，并使用表格输出"""
    result = call_api("GET", "cmdb/firewall/policy/")
    if "error" in result:
        print(f"错误: {result['error']}")
        return 1

    policies = result.get("results", [])
    if not policies:
        print("没有找到任何防火墙策略。")
        return 0

    table_data = []
    for p in policies:
        table_data.append([
            p.get("policyid"),
            p.get("name", ""),
            p.get("action"),
            p.get("status"),
            p.get("srcintf", [{}])[0].get("name") if p.get("srcintf") else "",
            p.get("dstintf", [{}])[0].get("name") if p.get("dstintf") else "",
        ])

    headers = ["ID", "名称", "动作", "状态", "源接口", "目的接口"]
    if TABULATE_AVAILABLE:
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        # 降级输出：简单的文本对齐
        print("\t".join(headers))
        for row in table_data:
            print("\t".join(str(cell) for cell in row))
    return 0


def add_address(name, subnet):
    """添加地址对象，添加前检查是否存在"""
    if address_exists(name):
        print(f"警告: 地址对象 '{name}' 已存在，跳过创建。")
        return 0

    # 处理 CIDR 格式
    if "/" in subnet:
        ip, mask = subnet.split("/")
        # 简单映射常见掩码，生产环境建议使用 ipaddress 库
        cidr_to_mask = {
            "24": "255.255.255.0",
            "32": "255.255.255.255",
            "16": "255.255.0.0",
            "8": "255.0.0.0"
        }
        netmask = cidr_to_mask.get(mask, "255.255.255.0")
        subnet_list = [ip, netmask]
    else:
        subnet_list = subnet.split()

    data = {
        "name": name,
        "subnet": subnet_list
    }
    result = call_api("POST", "cmdb/firewall/address/", data=data)
    if "error" in result:
        print(f"错误: 添加地址对象失败: {result['error']}")
        return 1
    print(f"成功: 地址对象 '{name}' 已添加。")
    return 0


def delete_address(name):
    """删除地址对象，删除前检查是否存在"""
    if not address_exists(name):
        print(f"错误: 地址对象 '{name}' 不存在，无法删除。")
        return 1

    result = call_api("DELETE", f"cmdb/firewall/address/{name}")
    if "error" in result:
        print(f"错误: 删除地址对象失败: {result['error']}")
        return 1
    print(f"成功: 地址对象 '{name}' 已删除。")
    return 0


def add_policy(params):
    """添加防火墙策略，添加前检查名称或ID是否已存在"""
    # 解析参数
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            print("错误: 添加策略需要有效的 JSON 参数")
            return 1

    # 构建策略数据
    data = {
        "name": params.get("name"),
        "srcintf": [{"name": params.get("srcintf")}] if params.get("srcintf") else [],
        "dstintf": [{"name": params.get("dstintf")}] if params.get("dstintf") else [],
        "srcaddr": [{"name": params.get("srcaddr")}] if params.get("srcaddr") else [],
        "dstaddr": [{"name": params.get("dstaddr")}] if params.get("dstaddr") else [],
        "action": params.get("action", "accept"),
        "status": params.get("status", "enable")
    }
    # 可选字段
    if params.get("schedule"):
        data["schedule"] = params.get("schedule")
    if params.get("service"):
        data["service"] = [{"name": params.get("service")}]

    # 简单检查同名策略（仅作提示，不阻止创建）
    policy_name = params.get("name")
    if policy_name:
        check = call_api("GET", "cmdb/firewall/policy/", params={"filter": f"name=@{policy_name}"})
        if not check.get("error") and check.get("results"):
            print(f"注意: 存在同名策略 '{policy_name}'，将创建新策略（名称可能重复）。")

    result = call_api("POST", "cmdb/firewall/policy/", data=data)
    if "error" in result:
        print(f"错误: 添加策略失败: {result['error']}")
        return 1
    print(f"成功: 策略 '{policy_name}' 已添加。")
    return 0


def update_policy(policy_id, updates):
    """更新防火墙策略"""
    if not policy_exists(policy_id):
        print(f"错误: 策略 ID {policy_id} 不存在，无法更新。")
        return 1

    result = call_api("PUT", f"cmdb/firewall/policy/{policy_id}", data=updates)
    if "error" in result:
        print(f"错误: 更新策略失败: {result['error']}")
        return 1
    print(f"成功: 策略 ID {policy_id} 已更新。")
    return 0


# ---------- 工控协议操作函数 ----------
def configure_icond(params):
    """
    配置 Industrial Connectivity 服务（协议转换）
    注意：此功能仅适用于 FortiGate Rugged 系列，API 路径可能因版本而异。
    此处使用接口的 allowaccess 配置，实际 icond 配置可能需要通过 CLI 或特定 API。
    """
    interface = params.get("interface")
    protocol_type = params.get("protocol_type")
    tty_device = params.get("tty_device")

    if not interface or not protocol_type or not tty_device:
        print("错误: configure-icond 需要提供 interface, protocol_type, tty_device 参数")
        return 1

    # 1. 启用接口的 icond 访问权限
    interface_data = {
        "allowaccess": "ping https ssh http icond"
    }
    iface_result = call_api("PUT", f"cmdb/system/interface/{interface}", data=interface_data)
    if "error" in iface_result:
        print(f"错误: 配置接口 {interface} 失败: {iface_result['error']}")
        return 1

    # 2. 配置 icond（假设 API 路径为 cmdb/system/icond）
    # 如果此 API 不存在，用户需通过 CLI 手动配置。这里仅给出框架。
    icond_data = {
        "status": "enable",
        "type": protocol_type,
        "tty-device": tty_device
    }
    icond_result = call_api("PUT", "cmdb/system/icond", data=icond_data)
    if "error" in icond_result:
        # 如果 API 不可用，给出提示
        print(f"警告: 无法通过 API 配置 icond（{icond_result['error']}），请手动在 CLI 下执行：")
        print(f"config system icond")
        print(f"    set status enable")
        print(f"    set type {protocol_type}")
        print(f"    set tty-device {tty_device}")
        print(f"end")
        return 0
    print(f"成功: 已启用 {protocol_type} 协议转换，使用串口 {tty_device}")
    return 0


def create_industrial_service(params):
    """创建工控协议服务对象"""
    name = params.get("name")
    protocol = params.get("protocol", "TCP").upper()
    port = params.get("port")

    if not name or not port:
        print("错误: create-industrial-service 需要提供 name 和 port 参数")
        return 1

    if service_exists(name):
        print(f"警告: 服务对象 '{name}' 已存在，跳过创建。")
        return 0

    data = {
        "name": name,
        "protocol": protocol,
        "tcp-portrange": str(port) if protocol == "TCP" else "",
        "udp-portrange": str(port) if protocol == "UDP" else ""
    }
    result = call_api("POST", "cmdb/firewall.service/custom", data=data)
    if "error" in result:
        print(f"错误: 创建服务对象失败: {result['error']}")
        return 1
    print(f"成功: 服务对象 '{name}' 已创建。")
    return 0


def create_industrial_ips(params):
    """创建针对工控协议的 IPS 配置文件"""
    name = params.get("name")
    protocols = params.get("protocols", [])
    action = params.get("action", "monitor")  # 默认监控模式，避免影响业务

    if not name or not protocols:
        print("错误: create-industrial-ips 需要提供 name 和 protocols 列表")
        return 1

    if ips_sensor_exists(name):
        print(f"警告: IPS 传感器 '{name}' 已存在，跳过创建。")
        return 0

    # 构建过滤器
    filters = []
    for proto in protocols:
        filters.append({
            "name": f"industrial.{proto.lower()}",
            "action": action
        })

    data = {
        "name": name,
        "filters": filters
    }
    result = call_api("POST", "cmdb/ips/sensor", data=data)
    if "error" in result:
        print(f"错误: 创建 IPS 传感器失败: {result['error']}")
        return 1
    print(f"成功: IPS 传感器 '{name}' 已创建，动作为 {action}。")
    return 0


def add_industrial_policy(params):
    """添加工控协议防火墙策略（带安全配置文件）"""
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            print("错误: add-industrial-policy 需要有效的 JSON 参数")
            return 1

    # 检查必须参数
    required = ["name", "srcintf", "dstintf", "srcaddr", "dstaddr", "service"]
    for r in required:
        if r not in params:
            print(f"错误: 缺少必要参数 '{r}'")
            return 1

    # 构建策略数据
    data = {
        "name": params.get("name"),
        "srcintf": [{"name": params.get("srcintf")}],
        "dstintf": [{"name": params.get("dstintf")}],
        "srcaddr": [{"name": params.get("srcaddr")}],
        "dstaddr": [{"name": params.get("dstaddr")}],
        "service": [{"name": params.get("service")}],
        "action": params.get("action", "accept"),
        "status": params.get("status", "enable")
    }

    # 关联安全配置文件（可选）
    if params.get("ips_profile"):
        # 检查 IPS 传感器是否存在
        if not ips_sensor_exists(params["ips_profile"]):
            print(f"警告: IPS 传感器 '{params['ips_profile']}' 不存在，策略将不关联 IPS。")
        else:
            data["ips-sensor"] = params["ips_profile"]

    if params.get("app_profile"):
        data["application-list"] = params["app_profile"]

    # 检查同名策略（可选）
    policy_name = params.get("name")
    if policy_name:
        check = call_api("GET", "cmdb/firewall/policy/", params={"filter": f"name=@{policy_name}"})
        if not check.get("error") and check.get("results"):
            print(f"注意: 存在同名策略 '{policy_name}'，将创建新策略。")

    result = call_api("POST", "cmdb/firewall/policy/", data=data)
    if "error" in result:
        print(f"错误: 添加工控策略失败: {result['error']}")
        return 1
    print(f"成功: 工控策略 '{data['name']}' 已添加。")
    return 0


# ---------- 主入口 ----------
def main():
    parser = argparse.ArgumentParser(description="FortiGate 配置技能（工控增强版）")
    parser.add_argument("action", help="操作")
    parser.add_argument("params", nargs="?", default="{}", help="操作所需的参数（JSON 格式）")

    args = parser.parse_args()
    action = args.action
    params_str = args.params

    # 尝试解析 params 为 JSON
    try:
        params = json.loads(params_str) if params_str else {}
    except json.JSONDecodeError:
        print("错误: params 必须是有效的 JSON 字符串")
        return 1

    # 操作映射
    actions = {
        # 基础操作
        "list-policies": lambda: list_policies(),
        "add-address": lambda: add_address(params.get("name"), params.get("subnet")),
        "delete-address": lambda: delete_address(params.get("name")),
        "add-policy": lambda: add_policy(params),
        "update-policy": lambda: update_policy(params.get("policyid"), {k: v for k, v in params.items() if k != "policyid"}),

        # 工控操作
        "configure-icond": lambda: configure_icond(params),
        "create-industrial-service": lambda: create_industrial_service(params),
        "create-industrial-ips": lambda: create_industrial_ips(params),
        "add-industrial-policy": lambda: add_industrial_policy(params),
    }

    if action not in actions:
        print(f"错误: 未知操作 '{action}'")
        print("支持的操作: " + ", ".join(actions.keys()))
        return 1

    return actions[action]()


if __name__ == "__main__":
    sys.exit(main())