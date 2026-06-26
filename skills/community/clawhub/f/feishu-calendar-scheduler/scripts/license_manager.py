#!/usr/bin/env python3
"""
飞书日历智能调度器 - 许可证管理系统
生成、验证和管理软件许可证
"""

import os
import sys
import json
import hashlib
import hmac
import base64
import time
from datetime import datetime, timedelta
import argparse
import secrets

class LicenseManager:
    """许可证管理器"""
    
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or self.generate_secret_key()
        self.product_id = "feishu-calendar-scheduler"
    
    @staticmethod
    def generate_secret_key(length=32):
        """生成安全密钥"""
        return secrets.token_hex(length)
    
    def generate_license(self, user_id, user_name, plan="professional", months=1):
        """
        生成许可证
        
        参数:
        - user_id: 用户ID（飞书 open_id）
        - user_name: 用户名
        - plan: 套餐类型（trial/professional/enterprise）
        - months: 有效期（月数）
        """
        # 许可证数据
        license_data = {
            "product_id": self.product_id,
            "user_id": user_id,
            "user_name": user_name,
            "plan": plan,
            "issue_date": datetime.now().isoformat(),
            "expiry_date": (datetime.now() + timedelta(days=30*months)).isoformat(),
            "features": self.get_plan_features(plan)
        }
        
        # 序列化数据
        data_json = json.dumps(license_data, separators=(',', ':'))
        data_b64 = base64.b64encode(data_json.encode('utf-8')).decode('ascii')
        
        # 生成签名
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data_b64.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # 组合许可证
        license_key = f"{data_b64}.{signature}"
        
        return {
            "license_key": license_key,
            "license_data": license_data,
            "secret_key": self.secret_key  # 注意：实际使用中不应返回密钥
        }
    
    def verify_license(self, license_key):
        """验证许可证"""
        try:
            # 分割数据和签名
            if '.' not in license_key:
                return {"valid": False, "error": "Invalid license format"}
            
            data_b64, signature = license_key.rsplit('.', 1)
            
            # 验证签名
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                data_b64.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return {"valid": False, "error": "Invalid signature"}
            
            # 解码数据
            data_json = base64.b64decode(data_b64).decode('utf-8')
            license_data = json.loads(data_json)
            
            # 验证产品ID
            if license_data.get("product_id") != self.product_id:
                return {"valid": False, "error": "Invalid product"}
            
            # 检查有效期
            expiry_date = datetime.fromisoformat(license_data["expiry_date"])
            if datetime.now() > expiry_date:
                return {"valid": False, "error": "License expired", "data": license_data}
            
            return {
                "valid": True,
                "data": license_data,
                "days_remaining": (expiry_date - datetime.now()).days
            }
            
        except Exception as e:
            return {"valid": False, "error": f"Verification error: {str(e)}"}
    
    def get_plan_features(self, plan):
        """获取套餐功能"""
        features = {
            "trial": {
                "max_meetings": 10,
                "max_users": 1,
                "features": ["basic_scheduling", "simple_reports"],
                "support_level": "community"
            },
            "professional": {
                "max_meetings": 100,
                "max_users": 10,
                "features": ["smart_scheduling", "batch_management", "advanced_reports", "api_access"],
                "support_level": "email"
            },
            "enterprise": {
                "max_meetings": 1000,
                "max_users": 50,
                "features": ["smart_scheduling", "batch_management", "advanced_reports", "api_access", "custom_integration", "priority_support"],
                "support_level": "priority"
            }
        }
        return features.get(plan, features["trial"])
    
    def save_license_to_file(self, license_info, filename="license.json"):
        """保存许可证到文件"""
        # 不保存密钥
        save_data = {
            "license_key": license_info["license_key"],
            "license_data": license_info["license_data"],
            "generated_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 许可证已保存到: {filename}")
        return filename
    
    def load_secret_key(self, key_file=".license_secret"):
        """从文件加载密钥"""
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                self.secret_key = f.read().strip()
            return True
        return False
    
    def save_secret_key(self, key_file=".license_secret"):
        """保存密钥到文件"""
        with open(key_file, 'w') as f:
            f.write(self.secret_key)
        print(f"🔐 密钥已保存到: {key_file}")
        return key_file

def main():
    parser = argparse.ArgumentParser(description="许可证管理系统")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 生成许可证命令
    gen_parser = subparsers.add_parser("generate", help="生成许可证")
    gen_parser.add_argument("--user-id", required=True, help="用户ID")
    gen_parser.add_argument("--user-name", required=True, help="用户名")
    gen_parser.add_argument("--plan", default="professional", 
                          choices=["trial", "professional", "enterprise"],
                          help="套餐类型")
    gen_parser.add_argument("--months", type=int, default=1, help="有效期（月数）")
    gen_parser.add_argument("--output", "-o", default="license.json", help="输出文件")
    
    # 验证许可证命令
    verify_parser = subparsers.add_parser("verify", help="验证许可证")
    verify_parser.add_argument("--license", help="许可证密钥")
    verify_parser.add_argument("--file", help="许可证文件")
    
    # 初始化命令
    init_parser = subparsers.add_parser("init", help="初始化密钥")
    init_parser.add_argument("--key", help="指定密钥（可选）")
    
    args = parser.parse_args()
    
    if args.command == "init":
        manager = LicenseManager(args.key)
        manager.save_secret_key()
        print(f"✅ 初始化完成")
        print(f"🔑 密钥: {manager.secret_key}")
        
    elif args.command == "generate":
        manager = LicenseManager()
        if not manager.load_secret_key():
            print("⚠️  未找到密钥文件，请先运行 'init' 命令")
            return
        
        license_info = manager.generate_license(
            user_id=args.user_id,
            user_name=args.user_name,
            plan=args.plan,
            months=args.months
        )
        
        manager.save_license_to_file(license_info, args.output)
        
        print(f"\n📋 许可证信息:")
        print(f"   用户: {license_info['license_data']['user_name']}")
        print(f"   套餐: {license_info['license_data']['plan']}")
        print(f"   有效期至: {license_info['license_data']['expiry_date']}")
        print(f"   许可证密钥: {license_info['license_key'][:50]}...")
        
    elif args.command == "verify":
        manager = LicenseManager()
        if not manager.load_secret_key():
            print("⚠️  未找到密钥文件")
            return
        
        if args.license:
            license_key = args.license
        elif args.file:
            with open(args.file, 'r') as f:
                license_data = json.load(f)
                license_key = license_data.get("license_key")
        else:
            print("❌ 请提供许可证密钥或文件")
            return
        
        result = manager.verify_license(license_key)
        
        if result["valid"]:
            print("✅ 许可证有效!")
            print(f"   用户: {result['data']['user_name']}")
            print(f"   套餐: {result['data']['plan']}")
            print(f"   剩余天数: {result['days_remaining']}")
            print(f"   功能: {', '.join(result['data']['features'].get('features', []))}")
        else:
            print(f"❌ 许可证无效: {result['error']}")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()