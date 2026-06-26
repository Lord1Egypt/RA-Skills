#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CompShare API 客户端脚本

用于管理优云智算CompShare平台的GPU实例全生命周期

配置文件: assets/config.yaml
"""

import os
import sys
import json
import base64
import argparse
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from ucloud.core import exc
    from ucloud.client import Client
except ImportError:
    print("Error: ucloud-sdk-python3 is required. Install with: pip install ucloud-sdk-python3")
    sys.exit(1)

# 支持的GPU类型
GPU_TYPES = ["P40", "2080", "3090", "3080Ti", "4090", "A800", "A100", "H20"]

# 默认配置
DEFAULT_REGION = "cn-wlcb"
DEFAULT_ZONE = "cn-wlcb-01"
DEFAULT_BASE_URL = "https://api.compshare.cn"
DEFAULT_IMAGE_ID = "500WHhII1fnz"


def get_config_path() -> Path:
    """
    获取配置文件路径
    
    优先级：
    1. 命令行参数 --config
    2. 默认路径 assets/config.yaml（Skill目录下）
    """
    # 默认路径（Skill目录下的assets/config.yaml）
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / "assets" / "config.yaml"
    
    return config_path


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径，为空则自动查找
    
    Returns:
        配置字典
    """
    if config_path is None:
        config_path = get_config_path()
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {config_path}\n"
            f"请将 assets/config.yaml.example 复制为 assets/config.yaml 并填入API凭证信息。"
        )
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    if not config:
        raise ValueError(f"配置文件为空: {config_path}")
    
    return config


def get_client(config: Optional[Dict[str, Any]] = None) -> Client:
    """
    获取CompShare API客户端
    
    Args:
        config: 配置字典，为空则自动加载
    
    Returns:
        ucloud Client实例
    """
    if config is None:
        config = load_config()
    
    compshare_config = config.get("compshare", {})
    
    public_key = compshare_config.get("public_key")
    private_key = compshare_config.get("private_key")
    
    if not public_key or not private_key:
        raise ValueError(
            "凭证配置不完整，请在assets/config.yaml中配置public_key和private_key\n"
            "获取凭证: https://console.compshare.cn/uaccount/api_manage"
        )
    
    client = Client({
        "region": compshare_config.get("region", DEFAULT_REGION),
        "public_key": public_key,
        "private_key": private_key,
        "base_url": compshare_config.get("base_url", DEFAULT_BASE_URL)
    })
    
    return client


def get_zone(config: Optional[Dict[str, Any]] = None) -> str:
    """获取配置的可用区"""
    if config is None:
        config = load_config()
    return config.get("compshare", {}).get("zone", DEFAULT_ZONE)


def create_instance(
    gpu_type: str,
    gpu_count: int = 1,
    cpu: int = 16,
    memory: int = 64,
    disk_size: int = 200,
    image_id: str = DEFAULT_IMAGE_ID,
    name: Optional[str] = None,
    password: Optional[str] = None,
    charge_type: str = "Spot",
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    创建GPU实例
    
    Args:
        gpu_type: GPU类型 (4090, 3080Ti, 3090, A800, A100, H20等)
        gpu_count: GPU数量
        cpu: CPU核数
        memory: 内存大小(GB)
        disk_size: 系统盘大小(GB)
        image_id: 镜像ID
        name: 实例名称
        password: 登录密码
        charge_type: 计费模式 (Month/Day/Dynamic/Postpay/Spot)
        config: 配置字典
    
    Returns:
        创建结果，包含UHostIds
    """
    if config is None:
        config = load_config()
    
    client = get_client(config)
    zone = get_zone(config)
    
    # 构建请求参数
    params = {
        "Zone": zone,
        "MachineType": "G",
        "CompShareImageId": image_id,
        "GPU": gpu_count,
        "GpuType": gpu_type,
        "CPU": cpu,
        "Memory": memory * 1024,  # 转换为MB
        "Disks": [
            {
                "IsBoot": True,
                "Size": disk_size,
                "Type": "CLOUD_SSD"
            }
        ],
        "ChargeType": charge_type
    }
    
    if name:
        params["Name"] = name
    
    if password:
        # 密码需要base64编码
        params["Password"] = base64.b64encode(password.encode()).decode()
    
    try:
        resp = client.ucompshare().create_comp_share_instance(params)
        return {
            "success": True,
            "uhost_ids": resp.get("UHostIds", []),
            "ips": resp.get("IPs", []),
            "raw_response": resp
        }
    except exc.UCloudException as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_instances(
    instance_ids: Optional[List[str]] = None,
    offset: int = 0,
    limit: int = 20,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    查询实例列表
    
    Args:
        instance_ids: 实例ID列表，为空则查询所有
        offset: 偏移量
        limit: 返回数量限制
        config: 配置字典
    
    Returns:
        实例列表信息
    """
    if config is None:
        config = load_config()
    
    client = get_client(config)
    
    params = {
        "Offset": offset,
        "Limit": limit
    }
    
    if instance_ids:
        params["UHostIds"] = instance_ids
    
    try:
        resp = client.ucompshare().describe_comp_share_instance(params)
        instances = resp.get("UHostSet", [])
        
        # 格式化输出
        formatted_instances = []
        for inst in instances:
            formatted_instances.append({
                "uhost_id": inst.get("UHostId"),
                "name": inst.get("Name"),
                "state": inst.get("State"),
                "ip": inst.get("IP"),
                "gpu_type": inst.get("GPUType"),
                "gpu_count": inst.get("GPU"),
                "cpu": inst.get("CPU"),
                "memory": inst.get("Memory"),
                "zone": inst.get("Zone"),
                "image_name": inst.get("CompShareImageName")
            })
        
        return {
            "success": True,
            "total_count": resp.get("TotalCount", 0),
            "instances": formatted_instances,
            "raw_response": resp
        }
    except exc.UCloudException as e:
        return {
            "success": False,
            "error": str(e)
        }


def start_instance(
    instance_id: str,
    without_gpu: bool = False,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    启动实例
    
    Args:
        instance_id: 实例ID
        without_gpu: 是否无卡启动
        config: 配置字典
    
    Returns:
        操作结果
    """
    if config is None:
        config = load_config()
    
    client = get_client(config)
    zone = get_zone(config)
    
    params = {
        "Zone": zone,
        "UHostId": instance_id
    }
    
    if without_gpu:
        params["WithoutGpu"] = True
    
    try:
        resp = client.ucompshare().start_comp_share_instance(params)
        return {
            "success": True,
            "uhost_id": resp.get("UHostId"),
            "raw_response": resp
        }
    except exc.UCloudException as e:
        return {
            "success": False,
            "error": str(e)
        }


def stop_instance(
    instance_id: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    停止实例
    
    Args:
        instance_id: 实例ID
        config: 配置字典
    
    Returns:
        操作结果
    """
    if config is None:
        config = load_config()
    
    client = get_client(config)
    zone = get_zone(config)
    
    params = {
        "Zone": zone,
        "UHostId": instance_id
    }
    
    try:
        resp = client.ucompshare().stop_comp_share_instance(params)
        return {
            "success": True,
            "uhost_id": resp.get("UHostId"),
            "raw_response": resp
        }
    except exc.UCloudException as e:
        return {
            "success": False,
            "error": str(e)
        }


def reboot_instance(
    instance_id: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    重启实例
    
    Args:
        instance_id: 实例ID
        config: 配置字典
    
    Returns:
        操作结果
    """
    if config is None:
        config = load_config()
    
    client = get_client(config)
    zone = get_zone(config)
    
    params = {
        "Zone": zone,
        "UHostId": instance_id
    }
    
    try:
        resp = client.ucompshare().reboot_comp_share_instance(params)
        return {
            "success": True,
            "uhost_id": resp.get("UHostId"),
            "raw_response": resp
        }
    except exc.UCloudException as e:
        return {
            "success": False,
            "error": str(e)
        }


def reset_password(
    instance_id: str,
    password: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    重置实例密码
    
    Args:
        instance_id: 实例ID
        password: 新密码
        config: 配置字典
    
    Returns:
        操作结果
    """
    if config is None:
        config = load_config()
    
    client = get_client(config)
    zone = get_zone(config)
    
    # 密码需要base64编码
    encoded_password = base64.b64encode(password.encode()).decode()
    
    params = {
        "Zone": zone,
        "UHostId": instance_id,
        "Password": encoded_password
    }
    
    try:
        resp = client.ucompshare().reset_comp_share_instance_password(params)
        return {
            "success": True,
            "uhost_id": resp.get("UHostId"),
            "raw_response": resp
        }
    except exc.UCloudException as e:
        return {
            "success": False,
            "error": str(e)
        }


def delete_instance(
    instance_id: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    删除实例
    
    注意：实例必须处于停止状态才能删除
    
    Args:
        instance_id: 实例ID
        config: 配置字典
    
    Returns:
        操作结果
    """
    if config is None:
        config = load_config()
    
    client = get_client(config)
    zone = get_zone(config)
    
    params = {
        "Zone": zone,
        "UHostId": instance_id
    }
    
    try:
        resp = client.ucompshare().terminate_comp_share_instance(params)
        return {
            "success": True,
            "uhost_id": resp.get("UHostId"),
            "in_recycle": resp.get("InRecycle"),
            "raw_response": resp
        }
    except exc.UCloudException as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description="CompShare GPU实例管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  创建实例:
    python compshare_client.py create --gpu-type 4090 --gpu-count 1 --cpu 16 --memory 64

  查询实例:
    python compshare_client.py list
    python compshare_client.py list --instance-ids "id1,id2"

  启动实例:
    python compshare_client.py start --instance-id uhost-xxx

  停止实例:
    python compshare_client.py stop --instance-id uhost-xxx

  重启实例:
    python compshare_client.py reboot --instance-id uhost-xxx

  重置密码:
    python compshare_client.py reset-password --instance-id uhost-xxx --password newpass

  删除实例:
    python compshare_client.py delete --instance-id uhost-xxx

配置文件:
  默认路径: assets/config.yaml（Skill目录下）
  可通过 --config 参数指定其他路径
        """
    )
    
    parser.add_argument("--config", help="配置文件路径")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建GPU实例")
    create_parser.add_argument("--gpu-type", required=True, choices=GPU_TYPES, help="GPU类型")
    create_parser.add_argument("--gpu-count", type=int, default=1, help="GPU数量 (默认: 1)")
    create_parser.add_argument("--cpu", type=int, default=16, help="CPU核数 (默认: 16)")
    create_parser.add_argument("--memory", type=int, default=64, help="内存大小GB (默认: 64)")
    create_parser.add_argument("--disk-size", type=int, default=200, help="系统盘大小GB (默认: 200)")
    create_parser.add_argument("--image-id", default=DEFAULT_IMAGE_ID, help="镜像ID")
    create_parser.add_argument("--name", help="实例名称")
    create_parser.add_argument("--password", help="登录密码")
    create_parser.add_argument("--charge-type", default="Spot", 
                               choices=["Month", "Day", "Dynamic", "Postpay","Spot"],
                               help="计费模式 (默认: Spot抢占式)")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="查询实例列表")
    list_parser.add_argument("--instance-ids", help="实例ID列表，逗号分隔")
    list_parser.add_argument("--offset", type=int, default=0, help="偏移量 (默认: 0)")
    list_parser.add_argument("--limit", type=int, default=20, help="返回数量 (默认: 20)")
    
    # start 命令
    start_parser = subparsers.add_parser("start", help="启动实例")
    start_parser.add_argument("--instance-id", required=True, help="实例ID")
    start_parser.add_argument("--without-gpu", action="store_true", help="无卡启动")
    
    # stop 命令
    stop_parser = subparsers.add_parser("stop", help="停止实例")
    stop_parser.add_argument("--instance-id", required=True, help="实例ID")
    
    # reboot 命令
    reboot_parser = subparsers.add_parser("reboot", help="重启实例")
    reboot_parser.add_argument("--instance-id", required=True, help="实例ID")
    
    # reset-password 命令
    reset_parser = subparsers.add_parser("reset-password", help="重置实例密码")
    reset_parser.add_argument("--instance-id", required=True, help="实例ID")
    reset_parser.add_argument("--password", required=True, help="新密码")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除实例")
    delete_parser.add_argument("--instance-id", required=True, help="实例ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 加载配置
    config = None
    if args.config:
        config = load_config(Path(args.config))
    
    # 执行对应命令
    result = None
    
    if args.command == "create":
        result = create_instance(
            gpu_type=args.gpu_type,
            gpu_count=args.gpu_count,
            cpu=args.cpu,
            memory=args.memory,
            disk_size=args.disk_size,
            image_id=args.image_id,
            name=args.name,
            password=args.password,
            charge_type=args.charge_type,
            config=config
        )
    
    elif args.command == "list":
        instance_ids = args.instance_ids.split(",") if args.instance_ids else None
        result = list_instances(
            instance_ids=instance_ids,
            offset=args.offset,
            limit=args.limit,
            config=config
        )
    
    elif args.command == "start":
        result = start_instance(
            instance_id=args.instance_id,
            without_gpu=args.without_gpu,
            config=config
        )
    
    elif args.command == "stop":
        result = stop_instance(instance_id=args.instance_id, config=config)
    
    elif args.command == "reboot":
        result = reboot_instance(instance_id=args.instance_id, config=config)
    
    elif args.command == "reset-password":
        result = reset_password(
            instance_id=args.instance_id,
            password=args.password,
            config=config
        )
    
    elif args.command == "delete":
        result = delete_instance(instance_id=args.instance_id, config=config)
    
    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 返回退出码
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
