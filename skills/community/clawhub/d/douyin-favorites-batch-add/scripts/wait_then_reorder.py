#!/usr/bin/env python3
"""等当前入夹批次结束（.run.lock 消失且持锁进程已退出）后，按最新表格重排 state 顺序。

用法: python wait_then_reorder.py "C:/path/MyLike_分类结果_YYYY-MM-DD.xlsx"
"""
import ctypes
import json
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.join(BASE, "douyin-queue", ".run.lock")
STILL_ACTIVE = 259


def alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    code = ctypes.c_ulong()
    ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
    ctypes.windll.kernel32.CloseHandle(h)
    return bool(ok) and code.value == STILL_ACTIVE


def main(xlsx):
    deadline = time.time() + 3 * 3600
    while time.time() < deadline:
        if not os.path.exists(LOCK):
            print("%s lock gone" % time.strftime("%H:%M:%S"))
            break
        try:
            st = json.load(open(LOCK, encoding="utf-8"))
        except Exception:
            st = {}
        pid = st.get("pid")
        if pid and not alive(pid):
            time.sleep(120)
            if not os.path.exists(LOCK):
                print("%s lock released" % time.strftime("%H:%M:%S"))
                break
            try:
                st2 = json.load(open(LOCK, encoding="utf-8"))
            except Exception:
                st2 = {}
            if st2.get("pid") == pid and not alive(pid):
                print("%s stale lock from dead pid %s" % (time.strftime("%H:%M:%S"), pid))
                break
        time.sleep(30)
    else:
        print("%s wait timeout, reorder anyway" % time.strftime("%H:%M:%S"))

    time.sleep(15)
    r = subprocess.run([sys.executable, os.path.join(BASE, "reorder_state.py"), xlsx],
                       capture_output=True, text=True)
    print("%s reorder rc=%s %s %s" % (time.strftime("%H:%M:%S"), r.returncode,
                                      r.stdout.strip(), r.stderr.strip()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
