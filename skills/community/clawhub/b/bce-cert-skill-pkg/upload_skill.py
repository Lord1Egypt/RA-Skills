#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""上传技能包到 Gitee"""
import base64
import requests
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GITEE_TOKEN = "b843f832f3a292de904b9fb9eb0a35fb"
USERNAME = "x-hower"
REPO_NAME = "bce-cert-skill"
REPO_FULL = f"{USERNAME}/{REPO_NAME}"

def upload_file(fname, message=None):
    """上传文件"""
    from pathlib import Path
    fpath = Path(fname)
    if not fpath.exists():
        return None, "文件不存在"
    
    content = fpath.read_bytes()
    content_b64 = base64.b64encode(content).decode()
    
    headers = {"Authorization": f"token {GITEE_TOKEN}", "Content-Type": "application/json"}
    
    # 检查是否存在
    r = requests.get(
        f'https://gitee.com/api/v5/repos/{REPO_FULL}/contents/{fname}',
        params={'ref': 'master'},
        headers=headers, verify=False
    )
    sha = None
    if r.status_code == 200 and isinstance(r.json(), dict):
        sha = r.json().get("sha")
    
    data = {
        "message": message or f"Add {fname}",
        "content": content_b64,
    }
    if sha:
        data["sha"] = sha
    
    time.sleep(1)
    
    if sha:
        r = requests.put(
            f'https://gitee.com/api/v5/repos/{REPO_FULL}/contents/{fname}',
            json=data, headers=headers, verify=False, timeout=30
        )
    else:
        r = requests.post(
            f'https://gitee.com/api/v5/repos/{REPO_FULL}/contents/{fname}',
            json=data, headers=headers, verify=False, timeout=30
        )
    
    return r.status_code, r.json() if r.status_code in (200, 201) else r.text[:200]

# 创建仓库
print("创建仓库...")
headers = {"Authorization": f"token {GITEE_TOKEN}", "Content-Type": "application/json"}
r = requests.post('https://gitee.com/api/v5/user/repos', json={
    "name": REPO_NAME,
    "description": "OpenClaw技能包：百度智能云DNS自动申请SSL证书",
    "private": False,
    "auto_init": True,
}, headers=headers, verify=False)

if r.status_code == 201:
    print("✅ 仓库创建成功")
elif r.status_code == 400 and "already exists" in r.text:
    print("仓库已存在")
else:
    print(f"创建仓库: {r.status_code} {r.text[:100]}")

time.sleep(3)

# 上传文件
print("\n上传文件...")
from pathlib import Path

# 上传 SKILL.md
code, result = upload_file("SKILL.md", "Add SKILL.md")
print(f"{'✅' if code in (200,201) else '❌'} SKILL.md")

# 上传 README.md
code, result = upload_file("README.md", "Add README.md")
print(f"{'✅' if code in (200,201) else '❌'} README.md")

# 上传 bce-cert 子目录的文件
skill_dir = Path("bce-cert")
for fname in sorted(skill_dir.glob("*")):
    if fname.is_file():
        rel_path = f"bce-cert/{fname.name}"
        code, result = upload_file(rel_path, f"Add {fname.name}")
        print(f"{'✅' if code in (200,201) else '❌'} {rel_path}")

print(f"\n🎉 完成！https://gitee.com/{REPO_FULL}")
