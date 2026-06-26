#!/usr/bin/env python3
"""
设备默认密码匹配器
自动识别设备类型并匹配默认密码数据库
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List

class DeviceMatcher:
    """设备默认密码匹配器"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "references" / "device_passwords.json"
        
        self.db_path = Path(db_path)
        self.database = self._load_database()
    
    def _load_database(self) -> Dict:
        """加载设备密码数据库"""
        if not self.db_path.exists():
            print(f"[!] 数据库文件不存在: {self.db_path}")
            return self._get_default_database()
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] 加载数据库失败: {e}")
            return self._get_default_database()
    
    def _get_default_database(self) -> Dict:
        """获取默认的设备密码数据库"""
        return {
            "routers": {
                "Cisco": [{"model": "General", "username": "admin", "password": "admin"}],
                "TP-Link": [{"model": "General", "username": "admin", "password": "admin"}],
                "D-Link": [{"model": "General", "username": "admin", "password": "admin"}],
            },
            "cameras": {
                "Hikvision": [{"model": "General", "username": "admin", "password": "12345"}],
                "Dahua": [{"model": "General", "username": "admin", "password": "admin"}],
            }
        }
    
    def get_device_types(self) -> List[str]:
        """获取支持的设备类型列表"""
        return list(self.database.keys())
    
    def get_brands(self, device_type: str) -> List[str]:
        """获取指定设备类型的品牌列表"""
        if device_type in self.database:
            return list(self.database[device_type].keys())
        return []
    
    def get_default_passwords(self, device_type: str, brand: str = None) -> List[Dict]:
        """获取设备的默认密码"""
        if device_type not in self.database:
            print(f"[-] 不支持的设备类型: {device_type}")
            return []
        
        if brand:
            if brand not in self.database[device_type]:
                print(f"[-] 设备类型 '{device_type}' 不支持品牌 '{brand}'")
                return []
            return self.database[device_type][brand]
        
        # 如果没有指定品牌，返回所有品牌的默认密码
        all_passwords = []
        for brand_name, passwords in self.database[device_type].items():
            for pwd in passwords:
                pwd_copy = pwd.copy()
                pwd_copy['brand'] = brand_name
                all_passwords.append(pwd_copy)
        
        return all_passwords
    
    def list_all_devices(self):
        """列出所有支持的设备和品牌"""
        print("\n支持的设备类型和品牌:")
        print("="*60)
        
        for device_type, brands in self.database.items():
            print(f"\n[+] {device_type.upper()}")
            for brand in brands.keys():
                print(f"    - {brand}")
        
        print("\n使用示例:")
        print("  python device_matcher.py --device-type router --brand Cisco")
        print("  python device_matcher.py --device-type camera --brand Hikvision")


def main():
    parser = argparse.ArgumentParser(description="设备默认密码匹配器")
    
    parser.add_argument('--device-type', '-t', help='设备类型')
    parser.add_argument('--brand', '-b', help='设备品牌')
    parser.add_argument('--list-devices', '-l', action='store_true', help='列出所有支持的设备')
    parser.add_argument('--output', '-o', help='输出文件路径（JSON格式）')
    
    args = parser.parse_args()
    
    matcher = DeviceMatcher()
    
    if args.list_devices:
        matcher.list_all_devices()
        return
    
    if args.device_type:
        passwords = matcher.get_default_passwords(args.device_type, args.brand)
        
        if passwords:
            print(f"\n找到 {len(passwords)} 个默认凭证:")
            for i, pwd in enumerate(passwords, 1):
                brand = pwd.get('brand', args.brand if args.brand else 'N/A')
                print(f"{i}. 品牌: {brand}, 用户名: {pwd.get('username')}, 密码: {pwd.get('password')}")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(passwords, f, indent=2, ensure_ascii=False)
                print(f"\n[+] 结果已保存到: {args.output}")
        else:
            print("[!] 未找到匹配的默认密码")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
