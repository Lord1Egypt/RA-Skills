"""端到端演示：造一个"文档写了 9/9 PASS、实际只跑出 1/2"的包，看审计器能不能抓出来。

跑法：python demo/run_demo.py
输出：审计表 + 该包的退出码（1 表示有声明对不上）
"""
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "..", "scripts", "audit.py")


def w(root, rel, text):
    p = os.path.join(root, rel)
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    root = tempfile.mkdtemp(prefix="demo-")
    w(root, "SKILL.md", "本包自检 9/9 PASS，共 12 个文件。\n")
    w(root, "tests/run_golden.py", 'print("PASS T1")\nprint("--- 1/2 PASS ---")\n')
    r = subprocess.run([sys.executable, AUDIT, "check", root],
                       capture_output=True, text=True, encoding="utf-8")
    print(r.stdout)
    print("退出码：", r.returncode, "（1 = 有声明对不上）")
    return 0 if r.returncode == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
