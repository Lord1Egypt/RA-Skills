import subprocess

def get_git_user():
    try:
        return subprocess.check_output(
            ["git", "config", "user.name"], text=True
        ).strip()
    except:
        return "未知"

def commit(commit_type, message, version, module, total, ai, percent):
    user = get_git_user()

    commit_msg = f"""{commit_type}:{message}

提交人：{user}
版本：{version}
模块名称：{module}
代码总行数：{total}
AI代码总行数：{ai}
AI代码占比：{percent}%"""

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", commit_msg])

    return commit_msg
