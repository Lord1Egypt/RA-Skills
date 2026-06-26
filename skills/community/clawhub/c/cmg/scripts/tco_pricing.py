#!/usr/bin/env python3
"""
CMG TCO 一站式询价工具
用法:
  # 方式1: 提供 AKSK 自动扫描阿里云资源并询价
  python3 tco_pricing.py --source aliyun --ak <AK> --sk <SK> --region cn-hangzhou

  # 方式2: 从已有的扫描 JSON 文件询价
  python3 tco_pricing.py --from-scan scan_result.json

  # 方式3: 手动指定资源配置
  python3 tco_pricing.py --from-config resources.json

功能:
  1. 扫描源端资源 (可选, 目前支持阿里云)
  2. 批量调用源端 DescribePrice API 获取价格
  3. 自动映射目标端腾讯云规格 + 地域
  4. 批量调用腾讯云询价 API
  5. 生成 pricing_data.json
  6. 调用 tco_report.py 生成 Excel + HTML 报告
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any

# ---------------------------------------------------------------------------
# 常量: 地域映射
# ---------------------------------------------------------------------------

# 阿里云 -> 腾讯云 地域映射
REGION_MAP_ALIYUN_TO_TENCENT: dict[str, str] = {
    "cn-hangzhou": "ap-shanghai",       # 杭州 -> 上海 (腾讯云无杭州)
    "cn-shanghai": "ap-shanghai",
    "cn-beijing": "ap-beijing",
    "cn-shenzhen": "ap-guangzhou",
    "cn-guangzhou": "ap-guangzhou",
    "cn-zhangjiakou": "ap-beijing",     # 张家口 -> 北京
    "cn-huhehaote": "ap-beijing",       # 呼和浩特 -> 北京
    "cn-chengdu": "ap-chengdu",
    "cn-nanjing": "ap-nanjing",
    "cn-qingdao": "ap-shanghai",        # 青岛 -> 上海
    "cn-wulanchabu": "ap-beijing",      # 乌兰察布 -> 北京
    "cn-hongkong": "ap-hongkong",
    "ap-southeast-1": "ap-singapore",   # 新加坡
    "ap-southeast-2": "ap-sydney",      # 悉尼 (不确定时 fallback 到新加坡)
    "ap-southeast-3": "ap-bangkok",     # 吉隆坡 -> 曼谷
    "ap-southeast-5": "ap-jakarta",     # 雅加达
    "ap-northeast-1": "ap-tokyo",       # 东京
    "ap-south-1": "ap-mumbai",          # 孟买
    "eu-central-1": "eu-frankfurt",     # 法兰克福
    "eu-west-1": "eu-frankfurt",        # 伦敦 -> 法兰克福
    "us-west-1": "na-siliconvalley",   # 硅谷
    "us-east-1": "na-ashburn",         # 弗吉尼亚
}

# 阿里云 -> 腾讯云 地域中文名映射 (用于显示)
REGION_DISPLAY: dict[str, str] = {
    "cn-hangzhou": "杭州→上海",
    "cn-shanghai": "上海",
    "cn-beijing": "北京",
    "cn-shenzhen": "深圳→广州",
    "cn-guangzhou": "广州",
    "cn-chengdu": "成都",
    "cn-nanjing": "南京",
    "cn-hongkong": "中国香港",
}

# ---------------------------------------------------------------------------
# 常量: 磁盘类型映射 (阿里云 -> 腾讯云)
# ---------------------------------------------------------------------------

DISK_TYPE_MAP: dict[str, str] = {
    "cloud_efficiency": "CLOUD_PREMIUM",      # 高效云盘 -> 高性能云盘
    "cloud_ssd": "CLOUD_SSD",                 # SSD云盘 -> SSD云盘
    "cloud_essd": "CLOUD_BSSD",               # ESSD -> 通用型SSD (简化, PL0/PL1)
    "cloud_essd_entry": "CLOUD_BSSD",         # ESSD Entry -> 通用型SSD
    "cloud_auto": "CLOUD_BSSD",               # ESSD AutoPL -> 通用型SSD
    "cloud": "CLOUD_PREMIUM",                 # 普通云盘 -> 高性能云盘
}

# ---------------------------------------------------------------------------
# 常量: 规格映射 (阿里云 -> 腾讯云)
# ---------------------------------------------------------------------------

# 直接按 CPU/内存 比例映射到腾讯云 S5 系列
def map_instance_type(ali_type: str, cpu: int, mem_gb: int) -> str:
    """
    阿里云实例规格 -> 腾讯云实例规格映射
    简化策略: 按 CPU/内存 映射到腾讯云 S5 标准系列
    """
    # 腾讯云 S5 命名规则: S5.{size}
    # SMALL1=1C1G, SMALL2=1C2G, MEDIUM2=2C2G, MEDIUM4=2C4G,
    # LARGE4=4C4G, LARGE8=4C8G, XLARGE8=4C8G, 2XLARGE16=8C16G...

    size_map: dict[tuple[int, int], str] = {
        (1, 1): "S5.SMALL1",
        (1, 2): "S5.SMALL2",
        (1, 4): "S5.SMALL4",
        (2, 2): "S5.MEDIUM2",
        (2, 4): "S5.MEDIUM4",
        (2, 8): "S5.MEDIUM8",
        (4, 4): "S5.LARGE4",
        (4, 8): "S5.LARGE8",
        (4, 16): "S5.LARGE16",
        (8, 8): "S5.XLARGE8",
        (8, 16): "S5.XLARGE16",
        (8, 32): "S5.XLARGE32",
        (16, 16): "S5.2XLARGE16",
        (16, 32): "S5.2XLARGE32",
        (16, 64): "S5.2XLARGE64",
        (32, 64): "S5.4XLARGE64",
        (32, 128): "S5.4XLARGE128",
        (64, 128): "S5.8XLARGE128",
        (64, 256): "S5.8XLARGE256",
    }

    key = (cpu, mem_gb)
    if key in size_map:
        return size_map[key]

    # Fallback: 根据 CPU/mem 比例找最近的
    best = None
    best_diff = float("inf")
    for (c, m), name in size_map.items():
        diff = abs(c - cpu) + abs(m - mem_gb)
        if diff < best_diff:
            best_diff = diff
            best = name
    return best or "S5.MEDIUM4"


# ---------------------------------------------------------------------------
# 阿里云 API 调用
# ---------------------------------------------------------------------------

class AliyunClient:
    """阿里云 API 客户端 (内置签名)"""

    def __init__(self, ak: str, sk: str, region: str):
        self.ak = ak
        self.sk = sk
        self.region = region
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    @staticmethod
    def _percent_encode(s: str) -> str:
        return urllib.parse.quote(str(s), safe="~").replace("+", "%20").replace("*", "%2A")

    def call(self, endpoint: str, action: str, version: str, extra: dict[str, str] | None = None) -> dict:
        params: dict[str, str] = {
            "Action": action,
            "RegionId": self.region,
            "Format": "JSON",
            "Version": version,
            "AccessKeyId": self.ak,
            "SignatureMethod": "HMAC-SHA1",
            "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "SignatureVersion": "1.0",
            "SignatureNonce": str(uuid.uuid4()),
        }
        if extra:
            params.update(extra)

        sorted_params = sorted(params.items())
        canonicalized = "&".join(
            f"{self._percent_encode(k)}={self._percent_encode(v)}" for k, v in sorted_params
        )
        string_to_sign = f"GET&{self._percent_encode('/')}&{self._percent_encode(canonicalized)}"
        h = hmac.new(
            (self.sk + "&").encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        )
        params["Signature"] = base64.b64encode(h.digest()).decode("utf-8")

        url = f"https://{endpoint}/?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
        try:
            resp = urllib.request.urlopen(req, timeout=30, context=self.ctx)
            return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode("utf-8"))

    # --- 便捷方法 ---

    def describe_instances(self, page_size: int = 100) -> list[dict]:
        """获取 ECS 实例列表"""
        data = self.call("ecs.aliyuncs.com", "DescribeInstances", "2014-05-26", {"PageSize": str(page_size)})
        return data.get("Instances", {}).get("Instance", [])

    def describe_disks(self, instance_id: str) -> list[dict]:
        """获取某实例的磁盘列表"""
        data = self.call("ecs.aliyuncs.com", "DescribeDisks", "2014-05-26", {"InstanceId": instance_id})
        return data.get("Disks", {}).get("Disk", [])

    def describe_eip(self, alloc_id: str) -> dict | None:
        """获取 EIP 详情"""
        data = self.call("vpc.aliyuncs.com", "DescribeEipAddresses", "2016-04-28", {"AllocationId": alloc_id})
        eips = data.get("EipAddresses", {}).get("EipAddress", [])
        return eips[0] if eips else None

    def describe_price(self, params: dict[str, str]) -> dict:
        """ECS 询价"""
        return self.call("ecs.aliyuncs.com", "DescribePrice", "2014-05-26", params)


# ---------------------------------------------------------------------------
# 腾讯云 tccli 调用
# ---------------------------------------------------------------------------

def tccli_call(service: str, action: str, region: str, params: dict) -> dict:
    """调用腾讯云 tccli，返回 JSON 响应"""
    # 将 params 中的复杂对象转为 CLI 参数
    args = ["tccli", service, action, "--region", region]
    for k, v in params.items():
        if isinstance(v, (dict, list)):
            args.extend([f"--{k}", json.dumps(v, ensure_ascii=False)])
        else:
            args.extend([f"--{k}", str(v)])

    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"  ⚠️ tccli 错误: {result.stderr.strip()}")
            return {"Error": result.stderr.strip()}
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("  ❌ tccli 未安装，请先执行: pip3 install tccli && tccli auth login")
        return {"Error": "tccli not found"}
    except subprocess.TimeoutExpired:
        print("  ⚠️ tccli 调用超时")
        return {"Error": "timeout"}
    except json.JSONDecodeError:
        print(f"  ⚠️ tccli 返回非 JSON: {result.stdout[:200]}")
        return {"Error": "invalid json"}


def tccli_inquiry_price_cvm(
    region: str, zone: str, instance_type: str,
    disk_type: str, disk_size: int,
    bandwidth: int = 0,
) -> dict:
    """腾讯云 CVM 包月询价"""
    params = {
        "Placement": {"Zone": zone},
        "InstanceChargeType": "PREPAID",
        "InstanceChargePrepaid": {"Period": 1},
        "InstanceType": instance_type,
        "ImageId": "img-487zeit5",  # CentOS 通用镜像
        "SystemDisk": {"DiskType": disk_type, "DiskSize": disk_size},
        "InternetAccessible": {
            "InternetChargeType": "TRAFFIC_POSTPAID_BY_HOUR",
            "InternetMaxBandwidthOut": bandwidth,
        },
        "InstanceCount": 1,
    }
    return tccli_call("cvm", "InquiryPriceRunInstances", region, params)


def get_tencent_zone(region: str) -> str:
    """获取腾讯云地域的第一个可用区"""
    data = tccli_call("cvm", "DescribeZones", region, {})
    zones = data.get("ZoneSet", [])
    for z in zones:
        if z.get("ZoneState") == "AVAILABLE":
            return z["Zone"]
    # fallback: region + "-2"
    return f"{region}-2"


# ---------------------------------------------------------------------------
# 扫描 + 标准化
# ---------------------------------------------------------------------------

def scan_aliyun_ecs(client: AliyunClient) -> list[dict]:
    """扫描阿里云 ECS 并标准化为内部格式"""
    print("\n📡 正在扫描阿里云 ECS 实例...")
    instances = client.describe_instances()
    print(f"   找到 {len(instances)} 台 ECS 实例")

    resources: list[dict] = []
    for inst in instances:
        instance_id = inst["InstanceId"]
        print(f"   📦 {instance_id} ({inst.get('InstanceName', '')}) - {inst['InstanceType']}")

        # 获取磁盘
        disks = client.describe_disks(instance_id)
        sys_disk = None
        data_disks: list[dict] = []
        for d in disks:
            if d["Type"] == "system":
                sys_disk = d
            else:
                data_disks.append(d)

        # 获取 EIP (如果有)
        eip_list = inst.get("EipAddress", {})
        eip_id = eip_list.get("AllocationId", "")
        eip_bandwidth = eip_list.get("Bandwidth", 0)

        # CPU / 内存
        cpu = inst.get("Cpu", 0)
        mem_mb = inst.get("Memory", 0)
        mem_gb = mem_mb // 1024 if mem_mb > 100 else mem_mb  # 兼容 MB 和 GB

        # 带宽
        bw_out = inst.get("InternetMaxBandwidthOut", 0)
        bw_charge = inst.get("InternetChargeType", "PayByTraffic")

        resource = {
            "source_vendor": "aliyun",
            "product": "ECS",
            "instance_id": instance_id,
            "instance_name": inst.get("InstanceName", ""),
            "instance_type": inst["InstanceType"],
            "cpu": cpu,
            "memory_gb": mem_gb,
            "os_type": inst.get("OSType", "linux"),
            "region": inst.get("RegionId", client.region),
            "zone": inst.get("ZoneId", ""),
            "system_disk": {
                "category": sys_disk["Category"] if sys_disk else "cloud_efficiency",
                "size_gb": sys_disk["Size"] if sys_disk else 40,
            },
            "data_disks": [{"category": d["Category"], "size_gb": d["Size"]} for d in data_disks],
            "bandwidth_out": bw_out,
            "bandwidth_charge": bw_charge,
            "eip_id": eip_id,
            "eip_bandwidth": eip_bandwidth,
            "charge_type": inst.get("InstanceChargeType", "PostPaid"),
        }
        resources.append(resource)

    return resources


# ---------------------------------------------------------------------------
# 阿里云批量询价
# ---------------------------------------------------------------------------

def price_aliyun_ecs(client: AliyunClient, resource: dict) -> dict:
    """对单台阿里云 ECS 询价 (包月)"""
    params: dict[str, str] = {
        "ResourceType": "instance",
        "InstanceType": resource["instance_type"],
        "SystemDisk.Category": resource["system_disk"]["category"],
        "SystemDisk.Size": str(resource["system_disk"]["size_gb"]),
        "InternetChargeType": "PayByTraffic",
        "InternetMaxBandwidthOut": str(resource["bandwidth_out"] if resource["bandwidth_charge"] != "PayByTraffic" else resource["bandwidth_out"]),
        "Period": "1",
        "PriceUnit": "Month",
        "InstanceChargeType": "PrePaid",
        "Amount": "1",
    }
    # 数据盘
    for i, dd in enumerate(resource.get("data_disks", []), 1):
        params[f"DataDisk.{i}.Category"] = dd["category"]
        params[f"DataDisk.{i}.Size"] = str(dd["size_gb"])

    result = client.describe_price(params)

    price_info = result.get("PriceInfo", {}).get("Price", {})
    original = price_info.get("OriginalPrice", 0)
    trade = price_info.get("TradePrice", 0)
    discount = price_info.get("DiscountPrice", 0)

    return {
        "original_price": float(original),
        "trade_price": float(trade),
        "discount": float(discount),
        "detail_prices": result.get("PriceInfo", {}).get("Price", {}).get("DetailPrices", {}).get("ResourcePriceModel", []),
    }


def price_aliyun_batch(client: AliyunClient, resources: list[dict]) -> list[dict]:
    """批量阿里云 ECS 询价 (并行)"""
    print("\n💰 阿里云批量询价中...")
    results: list[dict] = []

    def _price_one(res: dict) -> tuple[dict, dict]:
        p = price_aliyun_ecs(client, res)
        return res, p

    with ThreadPoolExecutor(max_workers=min(5, len(resources))) as executor:
        futures = {executor.submit(_price_one, r): r for r in resources}
        for future in as_completed(futures):
            try:
                res, price = future.result()
                res["price"] = price
                results.append(res)
                print(f"   ✅ {res['instance_id']} ({res['instance_type']}): "
                      f"¥{price['trade_price']:.2f}/月 (原价 ¥{price['original_price']:.2f})")
            except Exception as e:
                r = futures[future]
                print(f"   ❌ {r['instance_id']}: {e}")
                r["price"] = {"original_price": 0, "trade_price": 0, "discount": 0, "detail_prices": []}
                results.append(r)

    return results


# ---------------------------------------------------------------------------
# 腾讯云批量询价
# ---------------------------------------------------------------------------

def price_tencent_batch(resources: list[dict]) -> list[dict]:
    """批量腾讯云 CVM 询价"""
    print("\n💰 腾讯云批量询价中...")
    results: list[dict] = []

    # 预缓存地域的可用区
    zone_cache: dict[str, str] = {}

    for res in resources:
        ali_region = res["region"]
        tc_region = REGION_MAP_ALIYUN_TO_TENCENT.get(ali_region, "ap-shanghai")

        # 获取可用区 (缓存)
        if tc_region not in zone_cache:
            zone_cache[tc_region] = get_tencent_zone(tc_region)
        tc_zone = zone_cache[tc_region]

        # 映射规格
        tc_type = map_instance_type(res["instance_type"], res["cpu"], res["memory_gb"])

        # 映射磁盘类型
        tc_disk_type = DISK_TYPE_MAP.get(res["system_disk"]["category"], "CLOUD_PREMIUM")
        tc_disk_size = res["system_disk"]["size_gb"]

        # 映射带宽
        tc_bw = res["bandwidth_out"] if res["bandwidth_charge"] != "PayByTraffic" else res["bandwidth_out"]

        print(f"   🔍 {res['instance_id']}: {res['instance_type']} → {tc_type} @ {tc_region}/{tc_zone}")

        # 调用询价 API
        result = tccli_inquiry_price_cvm(tc_region, tc_zone, tc_type, tc_disk_type, tc_disk_size, tc_bw)

        if "Error" in result:
            print(f"   ❌ 询价失败: {result['Error']}")
            res["target"] = {
                "vendor": "tencent",
                "instance_type": tc_type,
                "region": tc_region,
                "zone": tc_zone,
                "disk_type": tc_disk_type,
                "disk_size": tc_disk_size,
                "price": 0,
            }
        else:
            price = result.get("Price", {})
            instance_price = price.get("InstancePrice", {})
            bandwidth_price = price.get("BandwidthPrice", {})

            # 包月总价 = 实例 + 带宽 (系统盘包含在实例价格中)
            total = float(instance_price.get("OriginalPrice", 0)) + float(bandwidth_price.get("OriginalPrice", 0))
            discount_total = float(instance_price.get("DiscountPrice", 0)) + float(bandwidth_price.get("DiscountPrice", 0))

            res["target"] = {
                "vendor": "tencent",
                "instance_type": tc_type,
                "region": tc_region,
                "zone": tc_zone,
                "disk_type": tc_disk_type,
                "disk_size": tc_disk_size,
                "price": discount_total or total,
                "original_price": total,
                "instance_price": float(instance_price.get("DiscountPrice", 0) or instance_price.get("OriginalPrice", 0)),
                "bandwidth_price": float(bandwidth_price.get("DiscountPrice", 0) or bandwidth_price.get("OriginalPrice", 0)),
            }
            print(f"   ✅ {tc_type}: ¥{res['target']['price']:.2f}/月")

        results.append(res)

    return results


# ---------------------------------------------------------------------------
# 生成 pricing_data.json
# ---------------------------------------------------------------------------

def build_pricing_json(resources: list[dict], title: str) -> dict:
    """将询价结果转为 tco_report.py 需要的 pricing_data.json 格式"""
    today = datetime.now().strftime("%Y-%m-%d")
    items: list[dict] = []

    for res in resources:
        # 源端条目
        price = res.get("price", {})
        spec = f"{res['instance_type']} ({res['cpu']}C{res['memory_gb']}G)"
        disk_desc = f" + {res['system_disk']['size_gb']}G {res['system_disk']['category']}"
        if res.get("data_disks"):
            for dd in res["data_disks"]:
                disk_desc += f" + {dd['size_gb']}G {dd['category']}"

        source_monthly = price.get("trade_price", 0)
        items.append({
            "side": "source",
            "vendor": "aliyun",
            "product": "ECS",
            "resource_id": res["instance_id"],
            "resource_name": res["instance_name"],
            "region": res["region"],
            "spec_summary": spec + disk_desc,
            "billing_mode": "monthly",
            "unit_price_monthly": source_monthly,
            "quantity": 1,
            "subtotal_monthly": source_monthly,
            "subtotal_yearly": source_monthly * 12,
            "currency": "CNY",
            "price_source": "阿里云 DescribePrice API",
            "query_time": today,
            "notes": f"原价 ¥{price.get('original_price', 0):.2f}" if price.get("discount", 0) > 0 else "",
        })

        # 目标端条目
        target = res.get("target", {})
        if target:
            tc_spec = f"{target['instance_type']} ({res['cpu']}C{res['memory_gb']}G)"
            tc_disk_desc = f" + {target['disk_size']}G {target['disk_type']}"
            target_monthly = target.get("price", 0)
            items.append({
                "side": "target",
                "vendor": "tencent",
                "product": "CVM",
                "resource_id": "",
                "resource_name": f"{res['instance_name']} (推荐)",
                "region": target["region"],
                "spec_summary": tc_spec + tc_disk_desc,
                "billing_mode": "monthly",
                "unit_price_monthly": target_monthly,
                "quantity": 1,
                "subtotal_monthly": target_monthly,
                "subtotal_yearly": target_monthly * 12,
                "currency": "CNY",
                "price_source": "腾讯云 InquiryPriceRunInstances API",
                "query_time": today,
                "notes": f"对标 {res['instance_type']}",
            })

    return {
        "project_name": title,
        "analysis_date": today,
        "source_vendor": "aliyun",
        "target_vendor": "tencent",
        "currency": "CNY",
        "pricing_items": items,
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="CMG TCO 一站式询价工具")
    parser.add_argument("--source", default="aliyun", choices=["aliyun", "aws", "huawei"],
                        help="源端云厂商 (目前支持 aliyun)")
    parser.add_argument("--ak", help="源端 AccessKey ID")
    parser.add_argument("--sk", help="源端 AccessKey Secret")
    parser.add_argument("--region", default="cn-hangzhou", help="源端地域 (默认 cn-hangzhou)")
    parser.add_argument("--from-scan", help="从已有的扫描 JSON 文件加载 (跳过扫描步骤)")
    parser.add_argument("--from-config", help="从手动配置的资源 JSON 文件加载")
    parser.add_argument("--title", default="云迁移 TCO 分析", help="报告标题")
    parser.add_argument("--output-dir", default=".", help="输出目录")
    parser.add_argument("--skip-report", action="store_true", help="只生成 pricing_data.json, 不生成报告")
    args = parser.parse_args()

    start_time = time.time()

    # Step 1: 获取资源列表
    resources: list[dict] = []

    if args.from_scan:
        print(f"📂 从文件加载扫描结果: {args.from_scan}")
        with open(args.from_scan, "r", encoding="utf-8") as f:
            resources = json.load(f)
        print(f"   加载了 {len(resources)} 条资源")

    elif args.from_config:
        print(f"📂 从文件加载资源配置: {args.from_config}")
        with open(args.from_config, "r", encoding="utf-8") as f:
            resources = json.load(f)
        print(f"   加载了 {len(resources)} 条资源")

    elif args.ak and args.sk:
        client = AliyunClient(args.ak, args.sk, args.region)
        resources = scan_aliyun_ecs(client)

        if not resources:
            print("⚠️ 未扫描到 ECS 实例")
            sys.exit(1)

        # 保存扫描结果 (方便下次直接 --from-scan)
        scan_path = os.path.join(args.output_dir, "scan_result.json")
        os.makedirs(args.output_dir, exist_ok=True)
        with open(scan_path, "w", encoding="utf-8") as f:
            json.dump(resources, f, indent=2, ensure_ascii=False)
        print(f"\n💾 扫描结果已保存: {scan_path}")
    else:
        print("❌ 请提供 --ak/--sk 或 --from-scan 或 --from-config")
        parser.print_help()
        sys.exit(1)

    # Step 2: 源端 (阿里云) 批量询价
    if args.source == "aliyun" and args.ak and args.sk:
        client = AliyunClient(args.ak, args.sk, args.region)
        resources = price_aliyun_batch(client, resources)
    elif args.from_scan or args.from_config:
        # 如果从文件加载且已有价格信息，跳过源端询价
        if resources and "price" not in resources[0]:
            if not (args.ak and args.sk):
                print("⚠️ 从文件加载的资源无价格信息, 需要提供 --ak/--sk 进行源端询价")
                sys.exit(1)
            client = AliyunClient(args.ak, args.sk, args.region)
            resources = price_aliyun_batch(client, resources)

    # Step 3: 目标端 (腾讯云) 批量询价
    resources = price_tencent_batch(resources)

    # Step 4: 生成 pricing_data.json
    os.makedirs(args.output_dir, exist_ok=True)
    pricing_data = build_pricing_json(resources, args.title)
    pricing_path = os.path.join(args.output_dir, "pricing_data.json")
    with open(pricing_path, "w", encoding="utf-8") as f:
        json.dump(pricing_data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 询价数据已保存: {pricing_path}")

    # Step 5: 生成报告
    if not args.skip_report:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        report_script = os.path.join(script_dir, "tco_report.py")
        if os.path.isfile(report_script):
            print("\n📊 生成 TCO 报告...")
            cmd = [
                sys.executable, report_script, pricing_path,
                "--title", args.title,
                "--output-dir", args.output_dir,
            ]
            subprocess.run(cmd, check=True)
        else:
            print(f"⚠️ 报告脚本未找到: {report_script}")

    elapsed = time.time() - start_time
    print(f"\n🎉 全部完成! 耗时 {elapsed:.1f}s")

    # 汇总
    src_total = sum(r.get("price", {}).get("trade_price", 0) for r in resources)
    tgt_total = sum(r.get("target", {}).get("price", 0) for r in resources)
    diff_pct = ((src_total - tgt_total) / src_total * 100) if src_total > 0 else 0

    print(f"\n{'='*50}")
    print(f"  源端月度总成本:  ¥{src_total:,.2f}")
    print(f"  目标端月度总成本: ¥{tgt_total:,.2f}")
    if diff_pct >= 0:
        print(f"  预计节省:       {diff_pct:.1f}% (¥{src_total - tgt_total:,.2f}/月)")
    else:
        print(f"  预计增加:       {abs(diff_pct):.1f}% (¥{tgt_total - src_total:,.2f}/月)")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
