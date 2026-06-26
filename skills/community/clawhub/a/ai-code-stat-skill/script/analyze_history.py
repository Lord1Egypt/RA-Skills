import subprocess
import re
from collections import defaultdict

def get_logs():
    return subprocess.check_output(
        ["git", "log", "--pretty=format:%B||END||"],
        text=True,
        errors="ignore"
    ).split("||END||")

def parse(msg):
    data = {}
    patterns = {
        "author": r"提交人：(.*)",
        "version": r"版本：(.*)",
        "total": r"代码总行数：(\\d+)",
        "ai": r"AI代码总行数：(\\d+)",
        "type": r"^(feat|bug|enhance|test|docs|other)"
    }
    for k, p in patterns.items():
        m = re.search(p, msg, re.MULTILINE)
        if m:
            data[k] = m.group(1)
    return data