#!/usr/bin/env python3
"""
UUID 生成器
支持 v1/v4/v5 UUID 和短UUID生成
"""

import argparse
import sys
import json
import uuid
import base64
import hashlib

def uuid_to_short(uuid_str: str) -> str:
    """
    将UUID转换为短格式(Base62)
    """
    # 移除连字符
    hex_str = uuid_str.replace('-', '')
    # 转为整数
    num = int(hex_str, 16)
    
    # Base62 字符集
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    
    result = []
    while num > 0:
        result.append(chars[num % 62])
        num //= 62
    
    return ''.join(reversed(result))

def generate_uuid(version: int = 4, namespace: str = None, name: str = None) -> str:
    """
    生成UUID
    
    Args:
        version: UUID版本 (1/4/5)
        namespace: v5命名空间 (DNS/URL/OID/X500)
        name: v5名称
    
    Returns:
        UUID字符串
    """
    if version == 1:
        return str(uuid.uuid1())
    elif version == 4:
        return str(uuid.uuid4())
    elif version == 5:
        if not namespace or not name:
            raise ValueError("v5需要namespace和name参数")
        
        # 命名空间映射
        ns_map = {
            'DNS': uuid.NAMESPACE_DNS,
            'URL': uuid.NAMESPACE_URL,
            'OID': uuid.NAMESPACE_OID,
            'X500': uuid.NAMESPACE_X500,
        }
        
        ns = ns_map.get(namespace.upper(), uuid.NAMESPACE_DNS)
        return str(uuid.uuid5(ns, name))
    else:
        raise ValueError(f"不支持的UUID版本: {version}")

def main():
    parser = argparse.ArgumentParser(description="UUID生成器")
    parser.add_argument("-c", "--count", type=int, default=1, help="生成数量")
    parser.add_argument("-v", "--version", type=int, default=4, choices=[1, 4, 5],
                        help="UUID版本: 1基于时间戳, 4随机(默认), 5基于命名空间")
    parser.add_argument("-n", "--namespace", help="v5命名空间 (DNS/URL/OID/X500)")
    parser.add_argument("--name", help="v5名称")
    parser.add_argument("-s", "--short", action="store_true", help="生成短UUID")
    parser.add_argument("-j", "--json", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    uuids = []
    for i in range(args.count):
        try:
            uid = generate_uuid(args.version, args.namespace, args.name)
            if args.short:
                uid = uuid_to_short(uid)
            uuids.append(uid)
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
    
    if args.json:
        output = {
            "success": True,
            "version": args.version,
            "count": args.count,
            "short": args.short,
            "uuids": uuids
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        for uid in uuids:
            print(uid)

if __name__ == "__main__":
    main()
