#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云 ECS 与 百度智能云 BCC 价格对比脚本

凭证来源（优先级：环境变量 > 配置文件）:
  阿里云: ALICLOUD_ACCESS_KEY_ID / ALICLOUD_ACCESS_KEY_SECRET
         或 ~/.config/openclaw/alicloud-ecs-price/credentials.json
  百度云: BCE_ACCESS_KEY_ID / BCE_SECRET_ACCESS_KEY / BCE_BCC_REGION
         或 ~/.config/openclaw/baidu-bcc-price/credentials.json

用法示例:
  # 按实例族和核数自动映射（推荐，默认Intel最新代）
  python3 compare_price.py --region 北京 --family g --vcpu 4 \\
      --disk-size 100 --disk-type SSD云盘 --bandwidth 5

  # 按实例族和核数自动映射（AMD系列）
  python3 compare_price.py --region 北京 --family ga --vcpu 4 \\
      --disk-size 100 --disk-type ESSD_PL1 --bandwidth 5

  # 直接指定两家云实例规格
  python3 compare_price.py --region 北京 \\
      --ali-spec ecs.g8i.xlarge --bcc-spec bcc.g7.c4m16 \\
      --disk-size 100 --disk-type SSD云盘 --bandwidth 5 --bandwidth-type ByBandwidth

  # 不含公网IP
  python3 compare_price.py --region 广州 --family c --vcpu 8 \\
      --disk-size 200 --disk-type ESSD_PL1

磁盘类型可选: 高效云盘, SSD云盘, ESSD_PL1, ESSD_PL2, ESSD_PL3
带宽计费方式: ByBandwidth(按带宽，默认), ByTraffic(按流量)
"""

import argparse
import hashlib
import hmac
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────── 常量与映射表 ────────────────────────────

ALI_CRED_PATH = Path.home() / ".config" / "openclaw" / "alicloud-ecs-price" / "credentials.json"
BCC_CRED_PATH = Path.home() / ".config" / "openclaw" / "baidu-bcc-price" / "credentials.json"

# 地域映射: 通用名 → (ali_region, bcc_host, bcc_default_zone, cn_name)
REGION_MAP = {
    "北京":        ("cn-beijing",   "bcc.bj.baidubce.com",  "cn-bj-d",  "北京"),
    "beijing":     ("cn-beijing",   "bcc.bj.baidubce.com",  "cn-bj-d",  "北京"),
    "bj":          ("cn-beijing",   "bcc.bj.baidubce.com",  "cn-bj-d",  "北京"),
    "广州":        ("cn-shenzhen",  "bcc.gz.baidubce.com",  "cn-gz-c",  "广州/深圳"),
    "深圳":        ("cn-shenzhen",  "bcc.gz.baidubce.com",  "cn-gz-c",  "广州/深圳"),
    "guangzhou":   ("cn-shenzhen",  "bcc.gz.baidubce.com",  "cn-gz-c",  "广州/深圳"),
    "gz":          ("cn-shenzhen",  "bcc.gz.baidubce.com",  "cn-gz-c",  "广州/深圳"),
    "成都":        ("cn-chengdu",   "bcc.cd.baidubce.com",  "cn-cd-a",  "成都"),
    "chengdu":     ("cn-chengdu",   "bcc.cd.baidubce.com",  "cn-cd-a",  "成都"),
    "cd":          ("cn-chengdu",   "bcc.cd.baidubce.com",  "cn-cd-a",  "成都"),
    "香港":        ("cn-hongkong",  "bcc.hkg.baidubce.com", "cn-hkg-a", "香港"),
    "hongkong":    ("cn-hongkong",  "bcc.hkg.baidubce.com", "cn-hkg-a", "香港"),
    "hk":          ("cn-hongkong",  "bcc.hkg.baidubce.com", "cn-hkg-a", "香港"),
    "苏州":        ("cn-shanghai",  "bcc.su.baidubce.com",  "cn-su-a",  "苏州"),
    "su":          ("cn-shanghai",  "bcc.su.baidubce.com",  "cn-su-a",  "苏州"),
    "保定":        ("cn-beijing",   "bcc.bd.baidubce.com",  "cn-bd-a",  "保定"),
    "bd":          ("cn-beijing",   "bcc.bd.baidubce.com",  "cn-bd-a",  "保定"),
    # 支持直接传入阿里云 region code
    "cn-beijing":  ("cn-beijing",   "bcc.bj.baidubce.com",  "cn-bj-d",  "北京"),
    "cn-shenzhen": ("cn-shenzhen",  "bcc.gz.baidubce.com",  "cn-gz-c",  "广州/深圳"),
    "cn-chengdu":  ("cn-chengdu",   "bcc.cd.baidubce.com",  "cn-cd-a",  "成都"),
    "cn-hongkong": ("cn-hongkong",  "bcc.hkg.baidubce.com", "cn-hkg-a", "香港"),
    "cn-shanghai": ("cn-shanghai",  "bcc.su.baidubce.com",  "cn-su-a",  "苏州"),
}

# 磁盘类型映射: user_input → (ali_category, bcc_display_name, ali_display_name)
DISK_TYPE_MAP = {
    "高效云盘":      ("cloud_efficiency", "高性能云磁盘",  "高效云盘"),
    "高效":          ("cloud_efficiency", "高性能云磁盘",  "高效云盘"),
    "SSD云盘":       ("cloud_ssd",        "通用型SSD",     "SSD云盘"),
    "SSD":           ("cloud_ssd",        "通用型SSD",     "SSD云盘"),
    "通用型SSD":     ("cloud_ssd",        "通用型SSD",     "SSD云盘"),
    "ESSD":          ("cloud_essd",       "增强型SSD_PL1", "ESSD云盘(PL1)"),
    "ESSD_PL1":      ("cloud_essd",       "增强型SSD_PL1", "ESSD云盘(PL1)"),
    "增强型SSD_PL1": ("cloud_essd",       "增强型SSD_PL1", "ESSD云盘(PL1)"),
    "ESSD PL1":      ("cloud_essd",       "增强型SSD_PL1", "ESSD云盘(PL1)"),
    "ESSD_PL2":      ("cloud_essd_pl2",   "增强型SSD_PL2", "ESSD云盘(PL2)"),
    "增强型SSD_PL2": ("cloud_essd_pl2",   "增强型SSD_PL2", "ESSD云盘(PL2)"),
    "ESSD PL2":      ("cloud_essd_pl2",   "增强型SSD_PL2", "ESSD云盘(PL2)"),
    "ESSD_PL3":      ("cloud_essd_pl3",   "增强型SSD_PL3", "ESSD云盘(PL3)"),
    "增强型SSD_PL3": ("cloud_essd_pl3",   "增强型SSD_PL3", "ESSD云盘(PL3)"),
    "ESSD PL3":      ("cloud_essd_pl3",   "增强型SSD_PL3", "ESSD云盘(PL3)"),
}

# BCC 磁盘类型 display name → API storage type
BCC_DISK_API_MAP = {
    "通用型SSD":     "cloud_hp1",
    "高性能云磁盘":   "hp1",
    "增强型SSD_PL1": "enhanced_ssd_pl1",
    "增强型SSD_PL2": "enhanced_ssd_pl2",
    "增强型SSD_PL3": "enhanced_ssd_pl3",
}

# vCPU 数量 → 阿里云规格后缀
VCPU_TO_SIZE = {
    2:  "large",
    4:  "xlarge",
    8:  "2xlarge",
    16: "4xlarge",
    32: "8xlarge",
    64: "16xlarge",
}

# 实例族映射（Intel 系列 — 最新代）
ALI_FAMILY_MAP = {
    "g": "g8i",    # 通用型
    "c": "c8ine",  # 计算型
    "r": "r8i",    # 内存型
    "m": "r8i",    # 内存型 alias
}

BCC_FAMILY_MAP = {
    "g": "g7",  # 通用型
    "c": "c7",  # 计算型
    "r": "m7",  # 内存型
    "m": "m7",  # 内存型 alias
}

# 实例族映射（AMD 系列 — 最新代）
ALI_FAMILY_MAP_AMD = {
    "ga": "g8a",  # 通用型 AMD
    "ca": "c8a",  # 计算型 AMD
    "ra": "r8a",  # 内存型 AMD
    "ma": "r8a",  # 内存型 AMD alias
}

BCC_FAMILY_MAP_AMD = {
    "ga": "ga3",  # 通用型 AMD
    "ca": "ca3",  # 计算型 AMD
    "ra": "ma3",  # 内存型 AMD
    "ma": "ma3",  # 内存型 AMD alias
}

MEMORY_RATIO = {"g": 4, "c": 2, "r": 8, "m": 8, "ga": 4, "ca": 2, "ra": 8, "ma": 8}

FAMILY_CN_NAME = {
    "g": "通用型Intel", "c": "计算型Intel", "r": "内存型Intel", "m": "内存型Intel",
    "ga": "通用型AMD", "ca": "计算型AMD", "ra": "内存型AMD", "ma": "内存型AMD",
}


# ──────────────────────────── 凭证加载 ────────────────────────────

def load_ali_credentials():
    """返回 (ak, sk) 元组，缺失时返回 (None, None)"""
    file_cred = {}
    if ALI_CRED_PATH.exists():
        try:
            file_cred = json.loads(ALI_CRED_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    ak = os.environ.get("ALICLOUD_ACCESS_KEY_ID") or file_cred.get("access_key_id")
    sk = os.environ.get("ALICLOUD_ACCESS_KEY_SECRET") or file_cred.get("access_key_secret")
    return ak, sk


def load_bcc_credentials():
    """返回 (ak, sk) 元组，缺失时返回 (None, None)"""
    file_cred = {}
    if BCC_CRED_PATH.exists():
        try:
            file_cred = json.loads(BCC_CRED_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    ak = os.environ.get("BCE_ACCESS_KEY_ID") or file_cred.get("accessKeyId")
    sk = os.environ.get("BCE_SECRET_ACCESS_KEY") or file_cred.get("secretAccessKey")
    return ak, sk


# ──────────────────────────── 规格自动推导 ────────────────────────────

def build_ali_spec(family, vcpu):
    """根据实例族和 vCPU 数量生成阿里云实例规格"""
    ali_map = ALI_FAMILY_MAP_AMD if family in ALI_FAMILY_MAP_AMD else ALI_FAMILY_MAP
    family_code = ali_map.get(family)
    if not family_code:
        raise ValueError(f"不支持的实例族: '{family}'，可选: g/ga(通用型) / c/ca(计算型) / r/ra(内存型)")
    size = VCPU_TO_SIZE.get(vcpu)
    if not size:
        raise ValueError(f"不支持的 vCPU 数量: {vcpu}，可选: {sorted(VCPU_TO_SIZE.keys())}")
    return f"ecs.{family_code}.{size}"


def build_bcc_spec(family, vcpu):
    """根据实例族和 vCPU 数量生成百度云实例规格"""
    bcc_map = BCC_FAMILY_MAP_AMD if family in BCC_FAMILY_MAP_AMD else BCC_FAMILY_MAP
    family_code = bcc_map.get(family)
    if not family_code:
        raise ValueError(f"不支持的实例族: '{family}'")
    memory = vcpu * MEMORY_RATIO[family]
    return f"bcc.{family_code}.c{vcpu}m{memory}"


# ──────────────────────────── 阿里云 API ────────────────────────────

def _get_ali_client(ak, sk, region):
    try:
        from alibabacloud_ecs20140526.client import Client as EcsClient
        from alibabacloud_tea_openapi import models as open_api_models
    except ImportError:
        raise RuntimeError(
            "阿里云SDK未安装。请先运行阿里云ECS价格查询技能的 setup.sh，"
            "或手动执行: pip install alibabacloud_ecs20140526"
        )
    config = open_api_models.Config(
        access_key_id=ak,
        access_key_secret=sk,
        region_id=region,
        endpoint=f"ecs.{region}.aliyuncs.com"
    )
    return EcsClient(config)


def _parse_ali_price(response_map):
    """从阿里云 SDK response.to_map() 中提取价格，兼容 snake_case 和 PascalCase"""
    price_info = (
        response_map.get("price_info") or
        response_map.get("PriceInfo") or
        response_map.get("body", {}).get("PriceInfo") or
        {}
    )
    price = price_info.get("price") or price_info.get("Price") or {}
    trade = price.get("trade_price") or price.get("TradePrice") or 0
    original = price.get("original_price") or price.get("OriginalPrice") or trade
    return float(trade), float(original)


def _parse_ali_instance_price(response_map):
    """从阿里云 SDK response.to_map() 中提取实例价格（不包含系统盘）"""
    price_info = (
        response_map.get("price_info") or
        response_map.get("PriceInfo") or
        response_map.get("body", {}).get("PriceInfo") or
        {}
    )
    price = price_info.get("price") or price_info.get("Price") or {}
    
    # 尝试从 DetailInfos 中提取 instanceType 价格
    detail_infos = price.get("detail_infos") or price.get("DetailInfos") or {}
    detail_list = detail_infos.get("detail_info") or detail_infos.get("DetailInfo") or []
    
    if detail_list:
        # 从明细中提取 instanceType 的价格
        for detail in detail_list:
            resource = detail.get("resource") or detail.get("Resource") or ""
            if resource == "instanceType":
                trade = detail.get("trade_price") or detail.get("TradePrice") or 0
                original = detail.get("original_price") or detail.get("OriginalPrice") or trade
                return float(trade), float(original)
    
    # 如果没有明细信息，返回总价
    trade = price.get("trade_price") or price.get("TradePrice") or 0
    original = price.get("original_price") or price.get("OriginalPrice") or trade
    return float(trade), float(original)


def query_ali_prices(ak, sk, ali_region, ali_spec, disk_category, disk_size, bandwidth, bandwidth_type):
    """查询阿里云各项价格，返回结果 dict"""
    result = {"spec": ali_spec, "region": ali_region}

    try:
        client = _get_ali_client(ak, sk, ali_region)
    except Exception as e:
        return {"spec": ali_spec, "region": ali_region, "fatal_error": str(e)}

    try:
        from alibabacloud_ecs20140526 import models as ecs_models
    except ImportError as e:
        return {"spec": ali_spec, "region": ali_region, "fatal_error": str(e)}

    # 实例价格和磁盘价格（一次查询同时获取）
    try:
        # 使用实例查询API，包含系统盘参数，同时获取实例和磁盘的包年包月价格
        system_disk = ecs_models.DescribePriceRequestSystemDisk(
            category=disk_category,
            size=disk_size
        )
        request = ecs_models.DescribePriceRequest(
            region_id=ali_region,
            resource_type="instance",
            instance_type=ali_spec,
            price_unit="Month",
            period=1,
            system_disk=system_disk
        )
        response = client.describe_price(request)
        result_map = response.to_map()
        
        # 提取价格明细
        price_info = result_map.get("body", {}).get("PriceInfo", {})
        price = price_info.get("Price", {})
        detail_infos = price.get("DetailInfos", {}).get("DetailInfo", [])
        
        # 从明细中提取实例价格和磁盘价格
        instance_price = None
        disk_price = None
        
        for detail in detail_infos:
            resource = detail.get("Resource", "")
            trade = detail.get("TradePrice", 0)
            
            if resource == "instanceType":
                instance_price = trade
            elif resource == "systemDisk":
                disk_price = trade
        
        # 设置实例价格
        if instance_price is not None:
            result["instance_monthly"] = float(instance_price)
            result["instance_original_monthly"] = float(instance_price)
        else:
            # 如果无法从明细提取，尝试从总价提取
            total_trade = price.get("TradePrice", 0)
            if disk_price is not None:
                result["instance_monthly"] = float(total_trade - disk_price)
            else:
                result["instance_error"] = "无法从API响应中提取实例价格"
        
        # 设置磁盘价格
        if disk_price is not None:
            result["disk_monthly"] = float(disk_price)
            result["disk_note"] = "包年包月价格（通过实例API获取）"
        else:
            result["disk_error"] = "无法从API响应中提取磁盘价格"
            
    except Exception as e:
        err_str = str(e)
        result["instance_error"] = err_str
        result["disk_error"] = err_str
        # 检测售罄相关错误码
        if any(code in err_str for code in ["InventoryExceeded", "NotSupportedWithSoldOut"]):
            result["sold_out"] = True

    # 带宽价格（包年包月）
    if bandwidth > 0:
        if bandwidth_type == "ByTraffic":
            try:
                request = ecs_models.DescribePriceRequest(
                    region_id=ali_region,
                    resource_type="bandwidth",
                )
                response = client.describe_price(request)
                trade, _ = _parse_ali_price(response.to_map())
                result["bandwidth_per_gb"] = trade
                result["bandwidth_type"] = "ByTraffic"
            except Exception as e:
                result["bandwidth_error"] = str(e)
        else:  # ByBandwidth
            # 阿里云带宽包年包月定价规则（华北2北京等指定地域）：
            # 1 Mbps = 23元, 2 Mbps = 46元, 3 Mbps = 71元, 4 Mbps = 96元, 5 Mbps = 125元
            # 6 Mbps及以上：125.0 + (n - 5) × 80
            # 参考：https://help.aliyun.com/zh/eip/subscription
            bandwidth_prices = {
                1: 23.0,
                2: 46.0,
                3: 71.0,
                4: 96.0,
                5: 125.0
            }
            
            if bandwidth <= 5:
                bandwidth_monthly = bandwidth_prices.get(bandwidth, 125.0)
            else:
                # 6 Mbps及以上：125.0 + (n - 5) × 80
                bandwidth_monthly = 125.0 + (bandwidth - 5) * 80.0
            
            result["bandwidth_monthly"] = round(bandwidth_monthly, 2)
            result["bandwidth_type"] = "ByBandwidth"
            result["bandwidth_note"] = "包年包月价格（按官方定价计算）"

    return result


# ──────────────────────────── 百度云 API (原生 Python) ────────────────────────────

def _bcc_sign(method, uri, timestamp, ak, sk, host):
    """生成百度云 bce-auth-v1 签名"""
    auth_prefix = f"bce-auth-v1/{ak}/{timestamp}/3600"
    canonical_uri = urllib.parse.quote(uri, safe="/")
    canonical_headers = f"host:{urllib.parse.quote(host, safe='')}"
    canonical_request = f"{method}\n{canonical_uri}\n\n{canonical_headers}"
    signing_key = hmac.new(sk.encode(), auth_prefix.encode(), hashlib.sha256).hexdigest()
    signature = hmac.new(signing_key.encode(), canonical_request.encode(), hashlib.sha256).hexdigest()
    return f"{auth_prefix}/host/{signature}"


def _bcc_http_post(host, path, payload, ak, sk):
    """向百度云发起签名 POST，返回解析后的 JSON"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    headers = {
        "Host": host,
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": _bcc_sign("POST", path, timestamp, ak, sk, host),
    }
    req = urllib.request.Request(
        f"https://{host}{path}",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    ctx = ssl._create_unverified_context()
    return json.loads(urllib.request.urlopen(req, timeout=15, context=ctx).read().decode())


def query_bcc_prices(ak, sk, bcc_host, bcc_spec, bcc_zone, bcc_disk_display, disk_size, bandwidth, bandwidth_type):
    """查询百度智能云各项价格，返回结果 dict"""
    result = {"spec": bcc_spec, "host": bcc_host, "zone": bcc_zone}
    total = 0.0

    # 实例价格（Prepaid 1个月）
    try:
        payload = {
            "purchaseCount": 1,
            "purchaseLength": 1,
            "spec": bcc_spec,
            "paymentTiming": "Prepaid",
            "zoneName": bcc_zone,
        }
        data = _bcc_http_post(bcc_host, "/v2/instance/price", payload, ak, sk)
        found = False
        for item in data.get("price", []):
            for pi in item.get("specPrices", []):
                if pi.get("spec") == bcc_spec:
                    if pi.get("status") != "available":
                        result["instance_error"] = f"匹配对应实例规格售罄（可用区 {bcc_zone}），请更换可用区（--bcc-zone）"
                        result["sold_out"] = True
                    else:
                        result["instance_monthly"] = float(pi["specPrice"])
                        total += result["instance_monthly"]
                    found = True
                    break
            if found:
                break
        if not found:
            result["instance_error"] = f"未找到规格 {bcc_spec}（请检查规格名称和可用区 {bcc_zone}）"
    except Exception as e:
        result["instance_error"] = str(e)

    # 磁盘价格（Prepaid 1个月）
    try:
        storage_type = BCC_DISK_API_MAP.get(bcc_disk_display, bcc_disk_display)
        payload = {
            "purchaseCount": 1,
            "purchaseLength": 1,
            "cdsSizeInGB": disk_size,
            "storageType": storage_type,
            "paymentTiming": "Prepaid",
            "zoneName": bcc_zone,
        }
        data = _bcc_http_post(bcc_host, "/v2/volume/getPrice", payload, ak, sk)
        found_disk = False
        for item in data.get("price", []):
            if item.get("storageType") == storage_type and item.get("cdsSizeInGB") == disk_size:
                result["disk_monthly"] = float(item["price"])
                total += result["disk_monthly"]
                found_disk = True
                break
        if not found_disk:
            result["disk_error"] = f"未找到云盘规格（类型: {storage_type}, 大小: {disk_size}GB）"
    except Exception as e:
        result["disk_error"] = str(e)

    # 带宽/EIP 价格
    if bandwidth > 0:
        try:
            eip_host = bcc_host.replace("bcc.", "eip.")
            if bandwidth_type == "ByTraffic":
                payload = {
                    "bandwidthInMbps": bandwidth,
                    "count": 1,
                    "billing": {
                        "paymentTiming": "Postpaid",
                        "billingMethod": "ByTraffic",
                    },
                }
                data = _bcc_http_post(eip_host, "/v1/eip/price", payload, ak, sk)
                prices = data.get("prices", {})
                config_price = prices.get("configPrice")
                # 确保转换为 float
                if config_price is not None:
                    try:
                        result["bandwidth_per_gb"] = float(config_price)
                    except (ValueError, TypeError):
                        result["bandwidth_per_gb"] = 0.76  # 默认值
                else:
                    result["bandwidth_per_gb"] = 0.76  # 默认值
                result["bandwidth_type"] = "ByTraffic"
            else:  # ByBandwidth
                payload = {
                    "bandwidthInMbps": bandwidth,
                    "count": 1,
                    "billing": {
                        "paymentTiming": "Prepaid",
                        "reservation": {
                            "reservationLength": 1,
                            "reservationTimeUnit": "month",
                        },
                    },
                }
                data = _bcc_http_post(eip_host, "/v1/eip/price", payload, ak, sk)
                prices = data.get("prices", {})
                purchase_price = prices.get("purchasePrice")
                if purchase_price is not None:
                    result["bandwidth_monthly"] = float(purchase_price)
                    total += result["bandwidth_monthly"]
                    result["bandwidth_type"] = "ByBandwidth"
                else:
                    result["bandwidth_error"] = f"未获取到 EIP 价格（响应: {data}）"
        except Exception as e:
            result["bandwidth_error"] = str(e)

    result["total_monthly"] = round(total, 2)
    return result


# ──────────────────────────── 输出格式化 ────────────────────────────

def _display_width(s):
    return sum(2 if ord(c) > 127 else 1 for c in str(s))

def _pad(s, width):
    s = str(s)
    dw = _display_width(s)
    return s + " " * max(0, width - dw)

def _fmt_price(val, suffix="/月"):
    if val is None:
        return "N/A"
    return f"¥{val:.2f}{suffix}"

def _fmt_err(msg):
    return f"[错误] {msg[:30]}..." if len(str(msg)) > 30 else f"[错误] {msg}"


def get_processor_generation(spec):
    """从实例规格中提取处理器代数信息"""
    # 阿里云规格处理
    if spec.startswith("ecs."):
        family = spec.split(".")[1] if "." in spec else ""
        
        # Intel 处理器
        if "9i" in family or "9a" in family:
            return "Intel 9代 / AMD 4代+"
        elif "8i" in family or "8a" in family or "8ine" in family:
            return "Intel 5代 / AMD 3代"
        elif "7" in family and ("i" not in family and "a" not in family):
            return "Intel 3代"
        elif family.startswith("c6") or family.startswith("g6") or family.startswith("r6"):
            return "Intel 2代"
        elif family.startswith("c5") or family.startswith("g5") or family.startswith("r5"):
            return "Intel 2代"
        else:
            return "Intel 2代"
    
    # 百度云规格处理
    elif spec.startswith("bcc."):
        parts = spec.split(".")
        if len(parts) >= 2:
            family = parts[1]
            
            # 根据规格族判断
            if family in ["g8", "c8", "m8"]:
                return "Intel 9代"
            elif family in ["g7", "c7", "m7", "ga3", "ca3", "ma3"]:
                return "Intel 5代 / AMD 3代"
            elif family in ["g5", "c5", "m5"]:
                return "Intel 3代"
            elif family in ["g4", "c4", "m4", "e1"]:
                return "Intel 2代"
            elif family in ["ga2", "ca2", "ma2"]:
                return "AMD 2代"
            elif family in ["ga1", "ca1", "ma1", "e2"]:
                return "AMD 1代"
            else:
                return "Intel 2代"
        else:
            return "Intel 2代"
    
    else:
        return "未知"


def print_comparison(args, region_info, ali_spec, bcc_spec, disk_info, ali_result, bcc_result):
    """打印格式化的价格对比表格"""
    ali_region, bcc_host, bcc_zone, region_cn = region_info
    ali_disk_name = disk_info[2]
    bcc_disk_name = disk_info[1]
    bw = args.bandwidth
    bw_type = args.bandwidth_type
    bw_type_cn = "按带宽计费" if bw_type == "ByBandwidth" else "按流量计费"
    family_cn = FAMILY_CN_NAME.get(args.family, "") if args.family else ""

    SEP = "=" * 64
    print(f"\n{SEP}")
    print(f"  云主机价格对比（包年包月 · 1个月）")
    print(SEP)
    print(f"  地  域: {region_cn}（阿里云: {ali_region} | 百度智能云: {bcc_host}）")
    print(f"  实  例: {ali_spec}  vs  {bcc_spec}")
    if family_cn:
        print(f"  族  型: {family_cn}")
    print(f"  磁  盘: {args.disk_size}GB  "
          f"阿里云({ali_disk_name}) | 百度智能云({bcc_disk_name})")
    if bw > 0:
        print(f"  带  宽: {bw}Mbps（{bw_type_cn}）")
    print(SEP)

    # 若任一方有 fatal_error
    if "fatal_error" in ali_result:
        print(f"  阿里云查询失败: {ali_result['fatal_error']}")
    if "fatal_error" in bcc_result:
        print(f"  百度云查询失败: {bcc_result['fatal_error']}")
    if "fatal_error" in ali_result or "fatal_error" in bcc_result:
        print(f"{SEP}\n")
        return

    # 售罄提示
    if ali_result.get("sold_out"):
        print(f"  [!] 阿里云: 匹配对应实例规格售罄")
    if bcc_result.get("sold_out"):
        print(f"  [!] 百度智能云: 匹配对应实例规格售罄")

    C0, C1, C2 = 14, 24, 24
    line = f"{'对比项目':{C0}}" + _pad("阿里云 ECS", C1) + _pad("百度智能云 BCC", C2)
    print(line)
    print(f"{'-'*C0}{'-'*C1}{'-'*C2}")

    def row(label, ali_val, bcc_val):
        print(f"{_pad(label, C0)}{_pad(ali_val, C1)}{_pad(bcc_val, C2)}")

    row("实例规格", ali_spec, bcc_spec)
    
    # 添加处理器代数对比
    ali_gen = get_processor_generation(ali_spec)
    bcc_gen = get_processor_generation(bcc_spec)
    row("处理器代数", ali_gen, bcc_gen)

    ali_inst = (_fmt_price(ali_result.get("instance_monthly"))
                if "instance_monthly" in ali_result
                else _fmt_err(ali_result.get("instance_error", "未查询")))
    bcc_inst = (_fmt_price(bcc_result.get("instance_monthly"))
                if "instance_monthly" in bcc_result
                else _fmt_err(bcc_result.get("instance_error", "未查询")))
    row("实例月费", ali_inst, bcc_inst)

    row("磁盘类型", ali_disk_name, bcc_disk_name)

    ali_disk = (_fmt_price(ali_result.get("disk_monthly"))
                if "disk_monthly" in ali_result
                else _fmt_err(ali_result.get("disk_error", "未查询")))
    bcc_disk = (_fmt_price(bcc_result.get("disk_monthly"))
                if "disk_monthly" in bcc_result
                else _fmt_err(bcc_result.get("disk_error", "未查询")))
    row(f"磁盘月费({args.disk_size}G)", ali_disk, bcc_disk)

    if bw > 0:
        if bw_type == "ByBandwidth":
            ali_bw = (_fmt_price(ali_result.get("bandwidth_monthly"))
                      if "bandwidth_monthly" in ali_result
                      else _fmt_err(ali_result.get("bandwidth_error", "未查询")))
            bcc_bw = (_fmt_price(bcc_result.get("bandwidth_monthly"))
                      if "bandwidth_monthly" in bcc_result
                      else _fmt_err(bcc_result.get("bandwidth_error", "未查询")))
            row(f"带宽月费({bw}Mbps)", ali_bw, bcc_bw)
        else:
            ali_bw = (_fmt_price(ali_result.get("bandwidth_per_gb"), suffix="/GB")
                      if "bandwidth_per_gb" in ali_result
                      else _fmt_err(ali_result.get("bandwidth_error", "未查询")))
            bcc_bw = (_fmt_price(bcc_result.get("bandwidth_per_gb"), suffix="/GB")
                      if "bandwidth_per_gb" in bcc_result
                      else _fmt_err(bcc_result.get("bandwidth_error", "未查询")))
            row("流量单价", ali_bw, bcc_bw)

    ali_total = (
        ali_result.get("instance_monthly", 0) +
        ali_result.get("disk_monthly", 0) +
        (ali_result.get("bandwidth_monthly", 0) if bw_type == "ByBandwidth" else 0)
    )
    bcc_total = bcc_result.get("total_monthly", 0)

    print(f"{'=' * C0}{'=' * C1}{'=' * C2}")
    ali_total_str = _fmt_price(ali_total) if ali_total > 0 else "计算失败"
    bcc_total_str = _fmt_price(bcc_total) if bcc_total > 0 else "计算失败"
    row("合计月费", ali_total_str, bcc_total_str)

    if ali_total > 0 and bcc_total > 0:
        diff = ali_total - bcc_total
        pct = abs(diff) / ali_total * 100
        if diff > 0:
            print(f"\n  百度智能云比阿里云便宜  ¥{abs(diff):.2f}/月 ({pct:.1f}%)")
        elif diff < 0:
            print(f"\n  阿里云比百度智能云便宜  ¥{abs(diff):.2f}/月 ({pct:.1f}%)")
        else:
            print(f"\n  两家价格相同")

    notes = []
    if bw > 0 and bw_type == "ByTraffic":
        notes.append("按流量计费：合计未含带宽费用（实际费用取决于流量消耗）")
    if "disk_monthly" in ali_result:
        notes.append("阿里云磁盘价格为包年包月价格（通过实例API获取）")
    if "bandwidth_monthly" in ali_result and ali_result.get("bandwidth_monthly", 0) > 0:
        notes.append("阿里云带宽价格为包年包月价格（按官方定价计算）")
    if notes:
        print(f"\n  说明:")
        for n in notes:
            print(f"     * {n}")

    print(f"\n{SEP}\n")


# ──────────────────────────── 主函数 ────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="阿里云 ECS vs 百度智能云 BCC 价格对比",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 compare_price.py --region 北京 --family g --vcpu 4 --disk-size 100 --disk-type SSD云盘 --bandwidth 5
  python3 compare_price.py --region 广州 --ali-spec ecs.g8i.xlarge --bcc-spec bcc.g7.c4m16 --disk-size 200 --disk-type ESSD_PL1
  python3 compare_price.py --region 北京 --family ga --vcpu 8 --disk-size 200 --disk-type ESSD_PL1 --bandwidth 10
        """,
    )

    parser.add_argument(
        "--region", required=True,
        help="地域：北京 / 广州 / 成都 / 香港 / 苏州 / 保定，或 cn-beijing 等",
    )

    spec_group = parser.add_argument_group("实例规格（A/B 二选一）")
    spec_group.add_argument(
        "--family",
        choices=["g", "c", "r", "m", "ga", "ca", "ra", "ma"],
        help="A: 实例族  g/ga(通用型) / c/ca(计算型) / r/ra(内存型)",
    )
    spec_group.add_argument("--vcpu", type=int, help="A: vCPU 数量  2 / 4 / 8 / 16 / 32 / 64")
    spec_group.add_argument("--ali-spec", help="B: 直接指定阿里云实例规格，如 ecs.g8i.xlarge")
    spec_group.add_argument("--bcc-spec", help="B: 直接指定百度云实例规格，如 bcc.g7.c4m16")

    parser.add_argument("--disk-size", type=int, default=100, help="磁盘大小 (GB)，默认 100")
    parser.add_argument(
        "--disk-type", default="SSD云盘",
        help="磁盘类型：高效云盘 / SSD云盘 / ESSD_PL1 / ESSD_PL2 / ESSD_PL3，默认 SSD云盘",
    )
    parser.add_argument("--bandwidth", type=int, default=0, help="公网带宽 (Mbps)，0=不含公网IP，默认 0")
    parser.add_argument(
        "--bandwidth-type", default="ByBandwidth",
        choices=["ByBandwidth", "ByTraffic"],
        help="带宽计费方式：ByBandwidth(按带宽，默认) / ByTraffic(按流量)",
    )
    parser.add_argument("--bcc-zone", help="百度云可用区，如 cn-bj-d（不指定则使用各地域默认可用区）")

    args = parser.parse_args()

    # ── 解析地域 ──
    region_key = args.region.strip()
    if region_key not in REGION_MAP:
        valid = list(set(REGION_MAP.keys()) - set(["beijing", "bj", "guangzhou", "gz", "chengdu", "cd", "hongkong", "hk", "su", "bd"]))
        parser.error(f"不支持的地域 '{region_key}'，可选: {valid}")

    region_info = REGION_MAP[region_key]
    ali_region, bcc_host_default, bcc_zone_default, _ = region_info
    bcc_host = bcc_host_default
    bcc_zone = args.bcc_zone or bcc_zone_default

    # ── 解析实例规格 ──
    if args.ali_spec and args.bcc_spec:
        ali_spec = args.ali_spec.strip()
        bcc_spec = args.bcc_spec.strip()
    elif args.family and args.vcpu:
        try:
            ali_spec = build_ali_spec(args.family, args.vcpu)
            bcc_spec = build_bcc_spec(args.family, args.vcpu)
        except ValueError as e:
            parser.error(str(e))
    else:
        parser.error(
            "请提供实例规格，二选一:\n"
            "  A) --family <g|ga|c|ca|r|ra> --vcpu <核数>  （自动映射最新代规格）\n"
            "  B) --ali-spec <规格> --bcc-spec <规格>  （直接指定）"
        )

    # ── 解析磁盘类型 ──
    disk_type_key = args.disk_type.strip()
    if disk_type_key not in DISK_TYPE_MAP:
        valid_disks = " / ".join(["高效云盘", "SSD云盘", "ESSD_PL1", "ESSD_PL2", "ESSD_PL3"])
        parser.error(f"不支持的磁盘类型 '{disk_type_key}'，可选: {valid_disks}")
    disk_info = DISK_TYPE_MAP[disk_type_key]
    ali_disk_category = disk_info[0]
    bcc_disk_display = disk_info[1]

    # ── 加载凭证 ──
    ali_ak, ali_sk = load_ali_credentials()
    bcc_ak, bcc_sk = load_bcc_credentials()

    missing = []
    if not ali_ak or not ali_sk:
        missing.append("阿里云（请先运行 alicloud_ecs_price-1.0.0/scripts/setup.sh）")
    if not bcc_ak or not bcc_sk:
        missing.append("百度智能云（请先运行 baidu-bcc-price-1.0.1/scripts/setup.sh）")
    if missing:
        for m in missing:
            print(f"[!] {m} 凭证未配置", file=sys.stderr)
        if len(missing) == 2:
            sys.exit(1)

    # ── 输出查询信息 ──
    bw_type_cn = "按带宽计费" if args.bandwidth_type == "ByBandwidth" else "按流量计费"
    print(f"\n正在查询价格，请稍候...")
    print(f"   阿里云: {ali_spec} @ {ali_region}  磁盘: {args.disk_size}GB {disk_info[2]}", end="")
    print(f"  带宽: {args.bandwidth}Mbps({bw_type_cn})" if args.bandwidth > 0 else "")
    print(f"   百度云: {bcc_spec} @ {bcc_host} ({bcc_zone})  磁盘: {args.disk_size}GB {bcc_disk_display}", end="")
    print(f"  带宽: {args.bandwidth}Mbps({bw_type_cn})" if args.bandwidth > 0 else "")

    # ── 执行查询 ──
    ali_result = {}
    bcc_result = {}

    if ali_ak and ali_sk:
        print("   正在查询阿里云价格...")
        ali_result = query_ali_prices(
            ali_ak, ali_sk, ali_region, ali_spec,
            ali_disk_category, args.disk_size,
            args.bandwidth, args.bandwidth_type,
        )

    if bcc_ak and bcc_sk:
        print("   正在查询百度智能云价格...")
        bcc_result = query_bcc_prices(
            bcc_ak, bcc_sk, bcc_host, bcc_spec, bcc_zone,
            bcc_disk_display, args.disk_size,
            args.bandwidth, args.bandwidth_type,
        )

    # ── 输出对比 ──
    print_comparison(args, region_info, ali_spec, bcc_spec, disk_info, ali_result, bcc_result)


if __name__ == "__main__":
    main()
