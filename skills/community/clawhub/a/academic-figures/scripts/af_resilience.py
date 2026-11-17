# -*- coding: utf-8 -*-
"""af_resilience：v6.2.0 渲染稳定性层——瞬时失败自动重试 + 看门狗预算放宽。

设计要点（为何进程级重试）：看门狗超时由守护线程 os._exit 强杀，Python 层
try/except 拦截不到；且渲染主流程持有大量模块级状态（matplotlib 全局、字体
注册），进程内重入不干净。故重试=以原 argv 重跑本脚本（状态零残留，等价于
自动化的"再跑一次"），成功即透传其退出码（exit 0=最终成功）。
只重试资源类瞬时失败（超时/内存）；重叠/数据/环境等确定性错误重跑无意义。
"""
import os
import subprocess
import sys

# 看门狗超时(exit 5)/内存耗尽(exit 6)=资源类瞬时失败；1/2/3/4=确定性错误不重试
RETRYABLE_CODES = {5, 6}


def wd_scale(budget):
    """重试代看门狗预算放宽系数（AF_WD_BUDGET_SCALE=1.5^N，由重试层写入）。"""
    try:
        s = float(os.environ.get("AF_WD_BUDGET_SCALE", "1") or 1)
    except ValueError:
        s = 1.0
    return budget * (s if s >= 1.0 else 1.0)


def spawn_retry(code):
    """瞬时失败自动重试。返回重试进程最终退出码；不重试返回 None。

    可重试=code in RETRYABLE_CODES 且未达上限（AF_RETRY_N < AF_RETRIES_MAX，
    上限由 main() 参数解析后写入环境、子进程经继承获得；--retries 0=关闭）。
    AF_DEBUG 模式不重试（维护者/反馈通道保持完整 traceback 直出）。
    重跑目标=调用方主脚本自身（sys.argv[0]，即 gen_figure.py），原 argv 原样继承。
    """
    if os.environ.get("AF_DEBUG"):
        return None
    if code not in RETRYABLE_CODES:
        return None
    try:
        gen = int(os.environ.get("AF_RETRY_N", "0") or 0)
        allowed = int(os.environ.get("AF_RETRIES_MAX", "1") or 0)
    except ValueError:
        return None
    if gen >= allowed:
        return None
    env = dict(os.environ)
    env["AF_RETRY_N"] = str(gen + 1)
    env["AF_WD_BUDGET_SCALE"] = f"{1.5 ** (gen + 1):.6f}"
    print(f"WARNING: 瞬时失败（exit {code}）——自动重试第 {gen + 1}/{allowed} 次"
          f"（看门狗预算放宽 ×{1.5 ** (gen + 1):.2f}；--retries 0 可关闭）",
          file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()
    script = os.path.abspath(sys.argv[0])
    proc = subprocess.Popen([sys.executable, script] + sys.argv[1:], env=env)
    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        return 130
