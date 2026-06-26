#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Duwi 智能家居命令行工具
支持所有 API 功能
"""

import sys
import os
import json
import argparse
import getpass
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from duwi_client import DuwiClient, DuwiAPIError
from device_handlers import DeviceHandlerFactory

TOKEN_FILE = os.path.join(script_dir, 'token_cache.json')
CONFIG_FILE = os.path.join(script_dir, 'config.json')
APP_CONFIG_FILE = os.path.join(script_dir, 'app_config.json')

APPKEY = None
SECRET = None

def _set_file_permissions(filepath: str):
    """设置文件权限为仅所有者可读写"""
    try:
        os.chmod(filepath, 0o600)
    except Exception:
        pass

def _load_app_credentials():
    """
    从配置文件加载应用凭证

    Returns:
        tuple: (appkey, secret)，如果配置不存在则返回 (None, None)
    """
    if not os.path.exists(APP_CONFIG_FILE):
        print("❌ 未找到应用配置文件 app_config.json")
        print()
        print("💡 请先完成应用凭证配置（二选一）：")
        print("   方式 1（推荐）：python init_config.py --appkey <APPKEY> --secret <SECRET>")
        print("   方式 2（交互）：python init_config.py")
        return None, None

    with open(APP_CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    appkey = config.get('appkey')
    secret = config.get('secret')

    if not appkey or not secret:
        print("❌ 配置文件中缺少 appkey 或 secret")
        print()
        print("💡 请重新配置：python init_config.py --force")
        return None, None

    return appkey, secret

def _save_token(token_info: dict):
    """保存 token 信息"""
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(token_info, f, indent=2, ensure_ascii=False)
    _set_file_permissions(TOKEN_FILE)

def _load_token() -> Optional[dict]:
    """加载 token 信息"""
    if not os.path.exists(TOKEN_FILE):
        return None
    
    try:
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            token_info = json.load(f)
        return token_info
    except json.JSONDecodeError:
        return None
    except Exception:
        return None

def _save_config(config: dict):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    _set_file_permissions(CONFIG_FILE)

def _load_config() -> dict:
    """加载配置"""
    if not os.path.exists(CONFIG_FILE):
        return {}
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def _get_client() -> Optional[DuwiClient]:
    """获取已登录的客户端"""
    if not APPKEY or not SECRET:
        print("❌ 应用凭证未配置")
        print()
        print("💡 请先完成应用凭证配置：")
        print("   python init_config.py --appkey <APPKEY> --secret <SECRET>")
        return None
    
    token_info = _load_token()
    if not token_info:
        print("❌ 未登录或登录已过期")
        print()
        print("💡 请先登录账户：")
        print("   python duwi_cli.py login <手机号> <密码>")
        return None
    
    client = DuwiClient(
        APPKEY, 
        SECRET,
        access_token=token_info.get('access_token'),
        refresh_token=token_info.get('refresh_token'),
        token_expire_time=token_info.get('access_token_expire'),
        token_file=TOKEN_FILE,
    )
    return client

def _get_room_map(client: DuwiClient, house_no: str) -> Dict[str, str]:
    """获取房间映射表（使用客户端缓存）"""
    rooms = client.get_rooms(house_no)  # 自动实时获取并缓存
    room_map = {r['roomName'].lower(): r['roomNo'] for r in rooms}
    return room_map

def _get_floor_map(client: DuwiClient, house_no: str) -> Dict[str, str]:
    """获取楼层映射表（使用客户端缓存）"""
    floors = client.get_floors(house_no)  # 自动实时获取并缓存
    floor_map = {f['floorName'].lower(): f['floorNo'] for f in floors}
    return floor_map

def _get_rooms_by_floor(client: DuwiClient, house_no: str, floor_no: str) -> List[Dict]:
    """获取指定楼层的所有房间"""
    rooms = client.get_rooms(house_no)
    return [r for r in rooms if r.get('floorNo') == floor_no]

def _find_items(
    client: DuwiClient,
    house_no: str,
    items: List[Dict[str, Any]],
    room_name: Optional[str] = None,
    item_name: Optional[str] = None,
    floor_name: Optional[str] = None,
    name_key: str = 'deviceName',
    room_key: str = 'roomNo',
) -> List[Dict[str, Any]]:
    """
    查找设备或场景（支持楼层 + 房间 + 名称组合查找）
    
    Returns:
        匹配的列表
    """
    floors_rooms = client.get_floors_and_rooms(house_no, False)
    rooms_list = floors_rooms.get('rooms', [])
    floors_list = floors_rooms.get('floors', [])

    room_map = {r['roomName'].lower(): r['roomNo'] for r in rooms_list}
    floor_map = {f['floorName'].lower(): f['floorNo'] for f in floors_list}

    target_room_no = room_map.get(room_name.lower()) if room_name else None
    target_floor_no = floor_map.get(floor_name.lower()) if floor_name else None

    floor_room_nos = []
    if target_floor_no:
        floor_room_nos = [r['roomNo'] for r in rooms_list if r.get('floorNo') == target_floor_no]

    exact_matches = []
    if item_name:
        exact_matches = [
            item for item in items 
            if item.get(name_key, '').lower() == item_name.lower()
        ]

    search_items = exact_matches if exact_matches else items
    candidates = []

    for item in search_items:
        item_name_val = item.get(name_key, '')
        item_room_no = item.get(room_key, '')

        name_match = False
        if item_name:
            if exact_matches:
                name_match = True
            else:
                name_match = (
                    item_name.lower() in item_name_val.lower() or
                    item_name_val.lower() in item_name.lower()
                )
                if room_name and room_name in item_name_val:
                    name_match = True
                if floor_name and floor_name in item_name_val:
                    name_match = True
        else:
            name_match = True

        room_match = (target_room_no is None) or (item_room_no == target_room_no)

        floor_match = True
        if target_floor_no and floor_room_nos:
            floor_match = item_room_no in floor_room_nos

        if name_match and room_match and floor_match:
            candidates.append(item)

    return candidates


def _find_devices(
    client: DuwiClient,
    house_no: str,
    room_name: Optional[str] = None,
    device_name: Optional[str] = None,
    floor_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """查找设备"""
    devices = client.get_devices(house_no, False)
    return _find_items(client, house_no, devices, room_name, device_name, floor_name, 'deviceName', 'roomNo')

def _find_scenes(
    client: DuwiClient,
    house_no: str,
    room_name: Optional[str] = None,
    scene_name: Optional[str] = None,
    floor_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """查找场景"""
    scenes = client.get_scenes(house_no, False)
    return _find_items(client, house_no, scenes, room_name, scene_name, floor_name, 'sceneName', 'roomNo')

def _resolve_devices(
    client: DuwiClient,
    house_no: str,
    args: argparse.Namespace,
    device_type_desc: str = "设备",
) -> List[Dict[str, Any]]:
    """解析设备参数"""
    device_no = getattr(args, 'device_no', None)

    if device_no:
        dev = client.get_device_info(device_no)
        if not dev:
            print(f"❌ 未找到{device_type_desc}：{device_no}")
            return []
        return [dev]

    floor_name = getattr(args, 'floor', None)
    room_name = getattr(args, 'room', None)
    device_name = getattr(args, 'device_name', None)

    if floor_name and room_name and device_name:
        devs = _find_devices(client, house_no, room_name, device_name, floor_name)
        if not devs:
            print(f"❌ 未找到{device_type_desc}：{floor_name} - {room_name} - {device_name}")
        return devs

    if room_name and device_name:
        devs = _find_devices(client, house_no, room_name, device_name, None)
        if not devs:
            print(f"❌ 未找到{device_type_desc}：{room_name} - {device_name}")
        return devs

    if device_name:
        devs = _find_devices(client, house_no, None, device_name, None)
        if not devs:
            print(f"❌ 未找到{device_type_desc}：{device_name}")
        return devs

    print(f"❌ 请指定{device_type_desc}名称或编号")
    return []

def _resolve_scenes(
    client: DuwiClient,
    house_no: str,
    args: argparse.Namespace,
    scene_type_desc: str = "场景",
) -> List[Dict[str, Any]]:
    """解析场景参数"""
    scene_no = getattr(args, 'scene_no', None)
    
    if scene_no:
        scenes = client.get_scenes(house_no)
        matched = [s for s in scenes if s.get('sceneNo') == scene_no]
        if not matched:
            print(f"❌ 未找到{scene_type_desc}：{scene_no}")
            return []
        return matched

    scene_name = getattr(args, 'scene_name', None)
    floor_name = getattr(args, 'floor', None)
    room_name = getattr(args, 'room', None)

    if floor_name and room_name and scene_name:
        scenes = _find_scenes(client, house_no, room_name, scene_name, floor_name)
        if not scenes:
            print(f"❌ 未找到{scene_type_desc}：{floor_name} - {room_name} - {scene_name}")
        return scenes

    if room_name and scene_name:
        scenes = _find_scenes(client, house_no, room_name, scene_name, None)
        if not scenes:
            print(f"❌ 未找到{scene_type_desc}：{room_name} - {scene_name}")
        return scenes

    if scene_name:
        scenes = _find_scenes(client, house_no, None, scene_name, None)
        if not scenes:
            print(f"❌ 未找到{scene_type_desc}：{scene_name}")
        return scenes

    print(f"❌ 请指定{scene_type_desc}名称或编号")
    return []

# 命令

def cmd_login(args):
    """登录"""
    if not APPKEY or not SECRET:
        print("❌ 应用凭证未配置")
        print()
        print("💡 请先完成应用凭证配置：")
        print("   python init_config.py --appkey <APPKEY> --secret <SECRET>")
        return
    
    # 处理密码输入
    password = args.password
    if not password:
        password = getpass.getpass("请输入密码：").strip()
    
    client = DuwiClient(APPKEY, SECRET, token_file=TOKEN_FILE)
    try:
        result = client.login(args.phone, password)
        print(f"\n✅ 登录成功！")
        print(f"手机号：{args.phone}")
        print(f"Token 过期时间：{result.get('accessTokenExpireTime', '未知')}")
    except DuwiAPIError as e:
        print(f"\n❌ 登录失败：{e}")
        print()
        print("💡 可能原因：")
        print("   - 手机号或密码错误")
        print("   - 账户不存在或未开通")
        print("   - 网络连接问题")

def cmd_logout(args):
    """退出登录"""
    client = _get_client()
    if client:
        try:
            client.logout()
        except Exception:
            pass
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    from cache import clear
    clear()
    print("✅ 已退出登录")

def cmd_houses(args):
    """获取房屋列表"""
    client = _get_client()
    if not client:
        return
    houses = client.get_houses()
    if not houses:
        print("❌ 没有找到房屋")
        print()
        print("💡 可能原因：")
        print("   - 账户下还没有房屋，请联系迪惟研发中心添加")
        print("   - 登录的手机号不正确")
        return

    config = _load_config()
    selected = config.get('selected_house_no', '')

    print(f"\n房屋列表 (当前选择：{selected if selected else '未选择'}):\n")
    for i, house in enumerate(houses, 1):
        mark = "👉 " if house['houseNo'] == selected else ""
        print(f"{mark}{i}. {house['houseName']}")
        print(f"   房屋编号：{house['houseNo']}")
        print(f"   房屋地址：{house.get('address', '-')}")
        print(f"   设备总数：{house.get('deviceCount', 0)}")
        print()
    
    if not selected:
        print("💡 提示：请先选择房屋")
        print("   python duwi_cli.py choose-house")
        print("   或：python duwi_cli.py choose-house --house_no <房屋编号>")

def cmd_floors(args):
    """获取楼层列表"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("❌ 请先选择房屋")
        print()
        print("💡 命令：")
        print("   python duwi_cli.py choose-house")
        print("   或：python duwi_cli.py choose-house --house_no <房屋编号>")
        return

    floors = client.get_floors(house_no)

    if not floors:
        print("❌ 没有找到楼层")
        print()
        print("💡 可能原因：")
        print("   - 房屋尚未配置楼层")
        print("   - 楼层信息未同步")
        return

    print(f"\n楼层列表 (共 {len(floors)} 个):\n")
    for i, floor in enumerate(floors, 1):
        print(f"{i}. {floor['floorName']}")
        print(f"   编号：{floor['floorNo']}")
        print()

def cmd_rooms(args):
    """房间列表"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("❌ 请先选择房屋")
        print()
        print("💡 命令：")
        print("   python duwi_cli.py choose-house")
        return

    rooms = client.get_rooms(house_no)

    if hasattr(args, 'floor') and args.floor:
        floor_map = _get_floor_map(client, house_no)
        target_floor_no = floor_map.get(args.floor.lower())
        if target_floor_no:
            rooms = [r for r in rooms if r.get('floorNo') == target_floor_no]
        else:
            print(f"❌ 未找到楼层：{args.floor}")
            print()
            print("💡 可用楼层：")
            floors = client.get_floors(house_no)
            for f in floors:
                print(f"   - {f['floorName']}")
            return

    if not rooms:
        filter_info = f"（楼层：{args.floor}）" if hasattr(args, 'floor') and args.floor else ""
        print(f"❌ 没有找到房间{filter_info}")
        if filter_info:
            print()
            print("💡 可能原因：")
            print("   - 该楼层尚未配置房间")
            print("   - 楼层名称不正确")
        return

    filter_info = f"（楼层：{args.floor}）" if hasattr(args, 'floor') and args.floor else ""
    print(f"\n房间列表{filter_info} (共 {len(rooms)} 个):\n")
    for i, room in enumerate(rooms, 1):
        print(f"{i}. {room['roomName']}")
        print(f"   编号：{room['roomNo']}")
        print(f"   楼层：{room.get('floorNo', '-')}")
        print()

def cmd_choose_house(args):
    """选择房屋"""
    client = _get_client()
    if not client:
        return
    houses = client.get_houses()

    if not houses:
        print("❌ 没有找到房屋")
        print()
        print("💡 可能原因：")
        print("   - 账户下还没有房屋，请联系迪惟研发中心添加")
        print("   - 登录的手机号不正确")
        return

    # 支持命令行直接指定房屋编号或名称
    if hasattr(args, 'house_no') and args.house_no:
        selected_house = None
        for house in houses:
            if house['houseNo'] == args.house_no or house['houseName'] == args.house_no:
                selected_house = house
                break
        
        if selected_house:
            config = _load_config()
            config['selected_house_no'] = selected_house['houseNo']
            _save_config(config)
            print(f"✅ 已选择：{selected_house['houseName']}")
        else:
            print(f"❌ 未找到房屋：{args.house_no}")
            print()
            print("💡 可用房屋：")
            for i, house in enumerate(houses, 1):
                print(f"   {i}. {house['houseName']} ({house['houseNo']})")
        return

    # 交互模式：显示列表并提示输入
    print("\n房屋列表:")
    for i, house in enumerate(houses, 1):
        print(f"{i}. {house['houseName']} - {house['houseNo']}")

    print()
    print("💡 提示：也可以使用 --house_no 参数直接指定房屋，避免交互：")
    print("   python duwi_cli.py choose-house --house_no <房屋编号或名称>")
    print()
    print("请选择房屋 (输入编号 1-{len(houses)} 或直接输入房屋名称):")
    choice = input("> ").strip()

    selected_house = None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(houses):
            selected_house = houses[idx]
    except ValueError:
        for house in houses:
            if house['houseName'] == choice or house['houseNo'] == choice:
                selected_house = house
                break

    if selected_house:
        config = _load_config()
        config['selected_house_no'] = selected_house['houseNo']
        _save_config(config)
        print(f"✅ 已选择：{selected_house['houseName']}")
    else:
        print("❌ 无效选择")

def cmd_devices(args):
    """获取设备列表"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("❌ 请先选择房屋")
        print()
        print("💡 命令：")
        print("   python duwi_cli.py choose-house")
        return

    devices = client.get_devices(house_no)

    if hasattr(args, 'online') and args.online:
        devices = [d for d in devices if d.get('isOnline', True)]
        if not devices:
            print("❌ 没有找到在线设备")
            print()
            print("💡 可能原因：")
            print("   - 设备未通电")
            print("   - 设备未连接到网络")
            print("   - 网关离线")
            return

    if hasattr(args, 'type') and args.type:
        devices = [d for d in devices if d.get('deviceTypeNo', '').startswith(args.type)]
        if not devices:
            print(f"❌ 没有找到类型为 '{args.type}' 的设备")
            print()
            print("💡 使用以下命令查看所有设备：")
            print("   python duwi_cli.py devices")
            return

    if hasattr(args, 'floor') and args.floor:
        floor_map = _get_floor_map(client, house_no)
        target_floor_no = floor_map.get(args.floor.lower())
        if target_floor_no:
            floor_rooms = _get_rooms_by_floor(client, house_no, target_floor_no)
            floor_room_nos = [r['roomNo'] for r in floor_rooms]
            devices = [d for d in devices if d.get('roomNo') in floor_room_nos]
        else:
            print(f"❌ 未找到楼层：{args.floor}")
            print()
            print("💡 可用楼层：")
            floors = client.get_floors(house_no)
            for f in floors:
                print(f"   - {f['floorName']}")
            return

    if hasattr(args, 'room') and args.room:
        room_map = _get_room_map(client, house_no)
        target_room_no = room_map.get(args.room.lower())
        if target_room_no:
            devices = [d for d in devices if d.get('roomNo') == target_room_no]
        else:
            print(f"❌ 未找到房间：{args.room}")
            print()
            print("💡 可用房间：")
            rooms = client.get_rooms(house_no)
            for r in rooms:
                print(f"   - {r['roomName']}")
            return

    if not devices:
        print("❌ 没有找到设备")
        print()
        print("💡 可能原因：")
        print("   - 该房屋/位置尚未添加设备")
        print("   - 选择了错误的房屋")
        return

    print(f"\n设备列表 (共 {len(devices)} 个):\n")
    for i, dev in enumerate(devices, 1):
        online = "🟢" if dev.get('isOnline', False) else "🔴"
        print(f"{online} {i}. {dev['deviceName']}")
        print(f"   编号：{dev['deviceNo']}")
        print(f"   类型：{dev['deviceTypeNo']} - {dev.get('deviceSubTypeNo', '-')}")
        if dev.get('roomNo'):
            print(f"   房间：{dev['roomNo']}")
        if dev.get('value'):
            print(f"   状态：{dev['value']}")
        print()

def cmd_device_info(args):
    """获取设备详情"""
    client = _get_client()
    if not client:
        return
    info = client.get_device_info(args.device_no)

    if not info:
        print(f"❌ 未找到设备：{args.device_no}")
        print()
        print("💡 建议：")
        print("   - 检查设备编号是否正确")
        print("   - 使用 'python duwi_cli.py devices' 查看可用设备")
        return

    print(f"\n✅ 设备信息:")
    print(f"名称：{info.get('deviceName', '')}")
    print(f"编号：{info.get('deviceNo', '')}")
    print(f"类型：{info.get('deviceTypeNo', '')} - {info.get('deviceSubTypeNo', '')}")
    print(f"在线：{'🟢 是' if info.get('isOnline', False) else '🔴 否'}")
    print(f"启用：{'是' if info.get('isUse', 0) else '否'}")
    if info.get('value'):
        print(f"状态：{info['value']}")

def cmd_device_value(args):
    """获取设备状态值"""
    client = _get_client()
    if not client:
        return
    value = client.get_device_value(args.device_no)
    print(f"设备 {args.device_no} 状态:")
    print(json.dumps(value, indent=2, ensure_ascii=False))

def cmd_operate(args):
    """设备操作（使用策略模式）"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("❌ 请先选择房屋")
        print()
        print("💡 命令：")
        print("   python duwi_cli.py choose-house")
        return

    devices = _resolve_devices(client, house_no, args, "设备")
    if not devices:
        return

    action = args.action
    value = args.value

    success_count = 0
    for device in devices:
        if not device.get('isOnline', False):
            print(f"⚠️ 设备 {device.get('deviceName')} ({device.get('deviceNo')}): 设备未在线")
            print("💡 请检查设备是否通电并连接到网络")
            continue

        device_type_no = device.get('deviceTypeNo', '')
        handler = DeviceHandlerFactory.get_handler(device_type_no)

        if handler:
            try:
                handler.handle(client, house_no, device, action, value)
                success_count += 1
            except DuwiAPIError as e:
                print(f"❌ 操作失败：{e}")
                print()
                print("💡 可能原因：")
                print("   - 设备不支持该操作")
                print("   - 参数值不正确")
                print("   - 设备状态异常")
        else:
            print(f"⚠️ 设备 {device.get('deviceName')} ({device.get('deviceNo')}): 暂不支持 (类型：{device_type_no})")
    
    if success_count > 0:
        print(f"\n✅ 成功操作 {success_count} 个设备")

def cmd_execute_scene(args):
    """执行场景"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("❌ 请先选择房屋")
        print()
        print("💡 命令：")
        print("   python duwi_cli.py choose-house")
        return

    scenes = _resolve_scenes(client, house_no, args, "场景")
    if not scenes:
        return

    if len(scenes) > 1:
        print(f"⚠️ 找到 {len(scenes)} 个匹配的场景，请提供更精确的位置信息：")
        print()
        for i, scene in enumerate(scenes, 1):
            print(f"  {i}. {scene['sceneName']} - 房间：{scene.get('roomNo', '-')}")
        print()
        print("💡 请使用以下命令精确指定：")
        print("   python duwi_cli.py execute-scene --scene_no <场景编号>")
        print("   或：python duwi_cli.py execute-scene --room <房间名> --scene_name <场景名>")
        return

    scene = scenes[0]
    try:
        client.execute_scene(house_no, scene['sceneNo'])
        location_info = ""
        if hasattr(args, 'floor') and args.floor:
            location_info += f"（楼层：{args.floor}）"
        if hasattr(args, 'room') and args.room:
            location_info += f"（房间：{args.room}）"
        print(f"\n✅ 已执行场景：{scene['sceneName']}{location_info}")
    except DuwiAPIError as e:
        print(f"\n❌ 执行失败：{e}")
        print()
        print("💡 可能原因：")
        print("   - 场景配置异常")
        print("   - 场景中的设备不可用")
        print("   - 网络连接问题")

def cmd_scenes(args):
    """场景列表"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("请先选择房屋：duwi choose-house")
        return

    scenes = client.get_scenes(house_no)

    if hasattr(args, 'floor') and args.floor:
        floor_map = _get_floor_map(client, house_no)
        target_floor_no = floor_map.get(args.floor.lower())
        if target_floor_no:
            floor_rooms = _get_rooms_by_floor(client, house_no, target_floor_no)
            floor_room_nos = [r['roomNo'] for r in floor_rooms]
            scenes = [s for s in scenes if s.get('roomNo') in floor_room_nos]
        else:
            print(f"⚠️ 未找到楼层：{args.floor}")
            return

    if hasattr(args, 'room') and args.room:
        room_map = _get_room_map(client, house_no)
        target_room_no = room_map.get(args.room.lower())
        if target_room_no:
            scenes = [s for s in scenes if s.get('roomNo') == target_room_no]
        else:
            print(f"⚠️ 未找到房间：{args.room}")
            return

    if hasattr(args, 'scene_name') and args.scene_name:
        scenes = [
            s for s in scenes
            if args.scene_name.lower() in s.get('sceneName', '').lower()
        ]
        if not scenes:
            print(f"⚠️ 未找到包含关键词\"{args.scene_name}\"的场景")
            return

    if not scenes:
        filter_info = ""
        if hasattr(args, 'floor') and args.floor:
            filter_info += f"（楼层：{args.floor}）"
        if hasattr(args, 'room') and args.room:
            filter_info += f"（房间：{args.room}）"
        if hasattr(args, 'scene_name') and args.scene_name:
            filter_info += f"（名称：{args.scene_name}）"
        print(f"没有找到场景{filter_info}")
        return

    filter_info = ""
    if hasattr(args, 'floor') and args.floor:
        filter_info += f"（楼层：{args.floor}）"
    if hasattr(args, 'room') and args.room:
        filter_info += f"（房间：{args.room}）"
    if hasattr(args, 'scene_name') and args.scene_name:
        filter_info += f"（名称：{args.scene_name}）"

    print(f"\n场景列表{filter_info} (共 {len(scenes)} 个):\n")
    for i, scene in enumerate(scenes, 1):
        print(f"{i}. {scene['sceneName']}")
        print(f"   编号：{scene['sceneNo']}")
        print(f"   房间：{scene.get('roomNo', '-')}")
        print(f"   启用：{'是' if scene.get('isUse', False) else '否'}")
        print(f"   收藏：{'是' if scene.get('isFavorite', False) else '否'}")
        print()

def cmd_elec_stats(args):
    """电量统计"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("请先选择房屋：duwi choose-house")
        return

    end_time = datetime.now()
    start_time = end_time - timedelta(days=args.days)
    record_type = 3
    start_str = start_time.strftime("%Y-%m-%d")
    end_str = end_time.strftime("%Y-%m-%d")

    device_no = getattr(args, 'device_no', None)
    data = client.get_elec_stats(house_no, record_type, start_str, end_str, device_no)

    print(f"\n电量统计 (过去 {args.days} 天):")
    elec_infos = data.get('elecInfos', [])

    total = 0
    for info in elec_infos:
        value = info.get('value', 0)
        total += value
        date = f"{info.get('year')}-{info.get('month', 0):02d}-{info.get('day', 0):02d}"
        print(f"  {date}: {value} kWh, 电费：¥{info.get('elecTotalFee', 0)}")

    print(f"\n总计：{total} kWh")

def cmd_sensor_stats(args):
    """传感器统计数据"""
    client = _get_client()
    if not client:
        return
    config = _load_config()
    house_no = config.get('selected_house_no')

    if not house_no:
        print("请先选择房屋：duwi choose-house")
        return

    end_time = datetime.now()
    if args.days == 1:
        start_time = end_time - timedelta(days=1)
        record_type = 4
        start_str = start_time.strftime("%Y-%m-%d %H:00")
        end_str = end_time.strftime("%Y-%m-%d %H:00")
    else:
        start_time = end_time - timedelta(days=args.days)
        record_type = 3
        start_str = start_time.strftime("%Y-%m-%d")
        end_str = end_time.strftime("%Y-%m-%d")

    data = client.get_sensor_stats(
        house_no, args.device_no, record_type,
        start_str, end_str, args.type
    )

    sensor_type_names = {1: '温度', 2: '湿度', 3: '光照度', 4: 'CO2', 5: 'PM2.5'}
    print(f"\n传感器统计数据:")
    print(f"类型：{sensor_type_names.get(args.type, '未知')}")
    print(f"单位：{data.get('unit', '')}")
    if data.get('value'):
        print(f"最新值：{data['value']}")

    sensor_infos = data.get('sensorInfos', [])
    if sensor_infos:
        print(f"\n详细数据 (共 {len(sensor_infos)} 条):")
        for info in sensor_infos[:10]:
            print(f"  最大：{info.get('maxValue')}  最小：{info.get('minValue')}  平均：{info.get('avgValue', '-')}")

def cmd_cache(args):
    """缓存管理"""
    from cache import get_stats, cleanup_expired
    
    if args.action == 'stats':
        stats = get_stats()
        print("\n缓存统计:")
        print(f"  缓存文件数：{stats['count']}")
        print(f"  缓存大小：{stats['size_kb']} KB")
        print(f"  过期文件数：{stats['expired']}")
        if stats['files']:
            print("\n缓存文件列表:")
            for f in stats['files']:
                print(f"  - {f['name']} ({f['size']} bytes)")
    
    elif args.action == 'clean':
        count = cleanup_expired()
        print(f"✅ 已清理 {count} 个过期缓存文件")
    
    elif args.action == 'clear':
        from cache import clear
        clear()
        print("✅ 已清空所有缓存")

def main():
    global APPKEY, SECRET
    
    # 检查配置文件
    APPKEY, SECRET = _load_app_credentials()

    if APPKEY is None or SECRET is None:
        return
    
    parser = argparse.ArgumentParser(
        description='Duwi 智能家居命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='命令')

    p = subparsers.add_parser('login', help='登录')
    p.add_argument('phone', help='手机号')
    p.add_argument('password', nargs='?', help='密码（不提供则提示输入）')
    p.set_defaults(func=cmd_login)

    p = subparsers.add_parser('logout', help='退出登录')
    p.set_defaults(func=cmd_logout)

    p = subparsers.add_parser('houses', help='房屋列表')
    p.set_defaults(func=cmd_houses)

    p = subparsers.add_parser('choose-house', help='选择房屋')
    p.add_argument('--house_no', help='房屋编号或名称（提供此参数则无需交互选择）')
    p.set_defaults(func=cmd_choose_house)

    p = subparsers.add_parser('floors', help='楼层列表')
    p.set_defaults(func=cmd_floors)

    p = subparsers.add_parser('rooms', help='房间列表')
    p.add_argument('--floor', help='楼层名称 (筛选该楼层的房间)')
    p.set_defaults(func=cmd_rooms)

    p = subparsers.add_parser('devices', help='设备列表')
    p.add_argument('--online', action='store_true', help='只显示在线设备')
    p.add_argument('--floor', help='楼层名称 (筛选该楼层的设备)')
    p.add_argument('--room', help='房间名称 (筛选该房间的设备)')
    p.add_argument('--type', help='设备类型前缀 (如 001, 003 等)')
    p.set_defaults(func=cmd_devices)

    p = subparsers.add_parser('device-info', help='设备详情')
    p.add_argument('device_no', help='设备编号')
    p.set_defaults(func=cmd_device_info)

    p = subparsers.add_parser('device-value', help='设备实时状态值')
    p.add_argument('device_no', help='设备编号')
    p.set_defaults(func=cmd_device_value)

    p = subparsers.add_parser('scenes', help='场景列表')
    p.add_argument('--floor', help='楼层名称 (筛选该楼层的场景)')
    p.add_argument('--room', help='房间名称 (筛选该房间的场景)')
    p.add_argument('--scene_name', help='场景名称关键词')
    p.set_defaults(func=cmd_scenes)

    p = subparsers.add_parser('execute-scene', help='执行场景')
    p.add_argument('--scene_no', help='场景编号 (优先使用)')
    p.add_argument('--scene_name', help='场景名称')
    p.add_argument('--floor', help='楼层名称')
    p.add_argument('--room', help='房间名称')
    p.set_defaults(func=cmd_execute_scene)

    p = subparsers.add_parser('device-operate', help='设备操作')
    p.add_argument('action', help='操作动作')
    p.add_argument('value', help='操作值')
    p.add_argument('--device_no', help='设备编号 (优先使用)')
    p.add_argument('--device_name', help='设备名称')
    p.add_argument('--floor', help='楼层名称')
    p.add_argument('--room', help='房间名称')
    p.set_defaults(func=cmd_operate)

    p = subparsers.add_parser('sensor-stats', help='传感器统计')
    p.add_argument('device_no', help='设备编号')
    p.add_argument('--type', type=int, default=1, help='传感器类型 (1=温度，2=湿度...)')
    p.add_argument('--days', type=int, default=1, help='查询天数')
    p.set_defaults(func=cmd_sensor_stats)

    p = subparsers.add_parser('elec-stats', help='电量统计')
    p.add_argument('--device_no', help='设备编号 (不传则为房屋总用电量)')
    p.add_argument('--days', type=int, default=7, help='查询天数')
    p.set_defaults(func=cmd_elec_stats)

    p = subparsers.add_parser('cache', help='缓存管理')
    p.add_argument('action', choices=['stats', 'clean', 'clear'], help='操作：stats(统计), clean(清理过期), clear(清空)')
    p.set_defaults(func=cmd_cache)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        args.func(args)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("💡 建议：按提示完成配置后再使用")
    except DuwiAPIError as e:
        print(f"❌ API 错误：{e.message if hasattr(e, 'message') else e}")
        print("💡 建议：检查网络连接，或联系迪惟技术支持")
    except KeyboardInterrupt:
        print("\n⚠️  操作已取消")
    except Exception as e:
        print(f"❌ 未知错误：{e}")
        print("💡 建议：如问题持续存在，请联系技术支持")

if __name__ == "__main__":
    main()
