#!/usr/bin/env python3
"""
飞书文档所有权转移工具
支持文档/表格/多维表格/文件的所有权转移
"""
import requests
import sys
import json

def transfer_owner(tenant_token, file_token, owner_id, member_type="openid", file_type="doc", remove_old=False, cancel_notify=False):
    """
    转移飞书文档所有权
    
    Args:
        tenant_token: 租户Token (t-xxx开头)
        file_token: 文档Token (从URL提取，如 doxcnxxx)
        owner_id: 新所有者的 open_id/user_id/union_id
        member_type: 成员类型 (openid/userid/unionid)
        file_type: 文档类型 (doc/sheet/bitable/file)
        remove_old: 是否移除原所有者权限
        cancel_notify: 是否取消通知
    
    Returns:
        dict: {"ok": True/False, "msg": "..."}
    """
    url = "https://open.feishu.cn/open-apis/drive/permission/member/transfer"
    
    headers = {
        "Authorization": f"Bearer {tenant_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "type": file_type,
        "token": file_token,
        "owner": {
            "member_type": member_type,
            "member_id": owner_id
        },
        "remove_old_owner": remove_old,
        "cancel_notify": cancel_notify
    }
    
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        result = resp.json()
        
        if resp.status_code == 200 and result.get("code") == 0:
            return {"ok": True, "msg": "所有权转移成功", "data": result.get("data")}
        else:
            return {"ok": False, "msg": f"转移失败: {result.get('msg')}", "raw": result}
    
    except Exception as e:
        return {"ok": False, "msg": f"请求异常: {str(e)}"}

def main():
    """命令行入口"""
    if len(sys.argv) < 5:
        print("用法: transfer_owner.py <tenant_token> <file_token> <owner_id> <member_type> [file_type]")
        print("示例: transfer_owner.py t-xxx doxcnxxx ou_xxx openid doc")
        sys.exit(1)
    
    tenant_token = sys.argv[1]
    file_token = sys.argv[2]
    owner_id = sys.argv[3]
    member_type = sys.argv[4]
    file_type = sys.argv[5] if len(sys.argv) > 5 else "doc"
    
    result = transfer_owner(tenant_token, file_token, owner_id, member_type, file_type)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
