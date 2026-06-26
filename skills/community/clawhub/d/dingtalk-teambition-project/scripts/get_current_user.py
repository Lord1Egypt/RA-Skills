#!/usr/bin/env python3
"""
获取当前用户信息
用法: uv run scripts/get_current_user.py

调用 /users/me 接口，返回当前登录用户的基本信息。
"""

import json
import sys

import call_api


def get_current_user() -> dict:
    """
    获取当前用户信息。
    
    Returns:
        用户信息字典，包含 userId 和 name，失败返回 None
    """
    print("正在获取当前用户信息...")
    
    try:
        data = call_api.get("users/me")
        user_info = data.get("result", {})
        
        if not user_info:
            print("\n" + "="*50)
            print("❌ 未获取到用户信息")
            print("="*50)
            return None
        
        # 提取关键信息
        user_data = {
            "userId": user_info.get("userId"),
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "phone": user_info.get("phone"),
            "role": user_info.get("role"),
            "isDisabled": user_info.get("isDisabled"),
            "employeeNumber": user_info.get("employeeNumber")
        }
        
        # 输出格式化的结果
        print("\n" + "="*50)
        print("✅ 获取用户信息成功！")
        print("="*50)
        print(f"用户 ID: {user_data['userId']}")
        print(f"用户名称: {user_data['name']}")
        if user_data['email']:
            print(f"邮箱: {user_data['email']}")
        if user_data['phone']:
            print(f"电话: {user_data['phone']}")
        if user_data['employeeNumber']:
            print(f"工号: {user_data['employeeNumber']}")
        
        role_map = {
            -1: "外部成员",
            0: "成员",
            1: "管理员",
            2: "拥有者"
        }
        role_name = role_map.get(user_data['role'], "未知")
        print(f"角色: {role_name}")
        print(f"账号状态: {'停用' if user_data['isDisabled'] == 1 else '启用'}")
        
        print("\n完整信息:")
        print(json.dumps(user_data, ensure_ascii=False, indent=2))
        
        return user_data
        
    except Exception as e:
        print(f"\n❌ 获取用户信息失败: {str(e)}", file=sys.stderr)
        return None


def main():
    """主函数 - 命令行入口"""
    if "--help" in sys.argv:
        print("""用法: uv run scripts/get_current_user.py

说明:
  获取当前用户在企业中的基本成员信息
  该接口只适用于 User Token 认证

返回信息:
  - userId: 用户 ID
  - name: 用户名称
  - email: 电子邮箱
  - phone: 联系电话
  - role: 成员角色（-1: 外部成员, 0: 成员, 1: 管理员, 2: 拥有者）
  - isDisabled: 账号状态（0: 启用, 1: 停用）
  - employeeNumber: 员工工号

示例:
  # 获取当前用户信息
  uv run scripts/get_current_user.py""")
        sys.exit(0)
    
    # 执行查询
    user_info = get_current_user()
    
    # 根据结果退出
    if user_info:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
