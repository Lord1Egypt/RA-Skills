#!/usr/bin/env python3
import os
import stat
import json

def check_permissions(path, max_allowed_mode):
    """检查路径权限，如果超过 max_allowed_mode 则返回风险信息"""
    if not os.path.exists(path):
        return None
    
    st = os.stat(path)
    # 取权限的后三位八进制数字
    current_mode = stat.S_IMODE(st.st_mode) 
    
    # 检查 Group 和 Other 权限
    # 0o077 代表是否有任何组(Group)或其他人(Other)的读/写/执行权限
    if (current_mode & 0o077) != 0:
        return f"{path} (当前权限: {oct(current_mode)}, 建议收紧为: {oct(max_allowed_mode)})"
    return None

def main():
    base_dir = os.path.expanduser("~/.openclaw")
    result = {"status": "unknown", "vulnerable_files": []}
    
    if not os.path.exists(base_dir):
        result["status"] = "clean"
        result["vulnerable_files"] = ["OpenClaw 根目录不存在，跳过检查。"]
        print(json.dumps(result, ensure_ascii=False))
        return

    vulnerable_list = []
    
    # 1. 检查根目录必须是 700 (drwx------)
    res = check_permissions(base_dir, 0o700)
    if res: vulnerable_list.append(f"[根目录暴露] {res}")

    # 2. 检查凭证和配置目录
    sensitive_subdirs = ["credentials", "agents", "openclaw.json"]
    for sub in sensitive_subdirs:
        target_path = os.path.join(base_dir, sub)
        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                # 遍历目录下的敏感文件
                for root, _, files in os.walk(target_path):
                    for f in files:
                        if f.endswith(('.json', '.jsonl', '.yml', '.yaml')):
                            file_res = check_permissions(os.path.join(root, f), 0o600)
                            if file_res: vulnerable_list.append(f"[凭证/日志泄露] {file_res}")
            else:
                file_res = check_permissions(target_path, 0o600)
                if file_res: vulnerable_list.append(f"[配置暴露] {file_res}")

    if vulnerable_list:
        result["status"] = "risks_found"
        result["vulnerable_files"] = vulnerable_list
    else:
        result["status"] = "clean"
        result["vulnerable_files"] = ["所有敏感配置和会话目录均已正确收紧权限 (700/600)。"]

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()