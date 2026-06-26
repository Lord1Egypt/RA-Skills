#!/usr/bin/env python3
import os
import json

def main():
    workspace_dir = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    result = {"status": "unknown", "scanned_dir": workspace_dir, "dangerous_symlinks": []}

    if not os.path.exists(workspace_dir):
        result["status"] = "error"
        result["dangerous_symlinks"] = [f"工作区目录不存在: {workspace_dir}"]
        print(json.dumps(result, ensure_ascii=False))
        return

    dangerous_links = []
    
    # 遍历工作区目录
    for root, dirs, files in os.walk(workspace_dir):
        for name in dirs + files:
            file_path = os.path.join(root, name)
            # 检查是否为符号链接
            if os.path.islink(file_path):
                try:
                    # 获取该链接真实指向的绝对路径
                    target_path = os.path.realpath(file_path)
                    
                    # 核心校验：如果真实路径不是以 workspace_dir 开头，说明发生了目录逃逸
                    if not target_path.startswith(os.path.realpath(workspace_dir)):
                        dangerous_links.append(f"{file_path} -> [逃逸指向] -> {target_path}")
                except Exception:
                    pass

    if dangerous_links:
        result["status"] = "risks_found"
        result["dangerous_symlinks"] = dangerous_links
    else:
        result["status"] = "clean"
        result["dangerous_symlinks"] = ["未发现指向工作区外部的危险符号链接。"]

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()