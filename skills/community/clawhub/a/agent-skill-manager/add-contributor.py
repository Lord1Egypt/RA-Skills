#!/usr/bin/env python3
"""
将 GLM-5.2 (zai-org) 添加为 GitHub Contributors
在 Windows 上运行: python add-contributor.py
"""
import os
import subprocess
import sys

REPO_DIR = r"D:\pythonproject\agent-skill-manager"

os.chdir(REPO_DIR)

def run(cmd, env=None, check=True):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"    {result.stderr.strip()}")
    if check and result.returncode != 0:
        print(f"    [ERROR] exit code {result.returncode}")
    return result

print("[1/6] 清理 git 锁文件...")
lock = os.path.join(REPO_DIR, ".git", "HEAD.lock")
if os.path.exists(lock):
    os.remove(lock)
    print(f"  已删除 {lock}")
else:
    print("  无锁文件")

print("[2/6] 同步到远程最新状态...")
run("git fetch origin")
run("git reset --hard origin/master")

print("[3/6] 在 README.md 中添加贡献者区块...")
readme_path = os.path.join(REPO_DIR, "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

if "贡献者" in content:
    print("  贡献者区块已存在，跳过")
else:
    section = """## 贡献者

感谢以下贡献者参与本项目开发：

- [**@yxdwind**](https://github.com/yxdwind) — 项目创建者与主要维护者
- [**@GLM-5.2**](https://github.com/zai-org) — AI 协作开发（智谱 GLM-5.2）

"""
    content = content.replace("## 许可证", section + "## 许可证")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  README.md 已更新：添加贡献者区块")

print("[4/6] 暂存修改...")
run("git add README.md")

print("[5/6] 创建以 GLM-5.2 为 author 的提交...")
env = os.environ.copy()
env["GIT_COMMITTER_NAME"] = "GLM-5.2"
env["GIT_COMMITTER_EMAIL"] = "223098841+zai-org@users.noreply.github.com"

# 写 commit message 到临时文件，避免 shell 转义问题
msg_file = os.path.join(REPO_DIR, ".git", "COMMIT_MSG_TMP")
with open(msg_file, "w", encoding="utf-8") as f:
    f.write("docs: add Contributors section to README\n\nCo-Authored-By: yxdwind <yxdwind@126.com>\n")

author_str = "GLM-5.2 <223098841+zai-org@users.noreply.github.com>"
run(f'git commit --author="{author_str}" -F "{msg_file}"', env=env)
os.remove(msg_file)

print("[6/6] 推送到 GitHub...")
run("git push origin master")

print("\n=== 提交结果 ===")
run('git log --oneline -3 --format="%h | %an <%ae> | %s"')

print("\n等待 GitHub 刷新 Contributors 页面（可能需要几分钟到几小时）")
print(f"查看: https://github.com/yxdwind/agent-skill-manager/graphs/contributors")
