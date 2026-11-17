#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claude 模型切换器 —— 点哪个模型，就把 ~/.claude/settings.json 切到那个 profile，
并自动拉起对应的本地代理。双击「Claude模型切换器.cmd」启动。

本文件为可移植版本：python 取运行本脚本的解释器（pythonw），
ccproxy 网关取与本脚本同目录的 ccproxy.py，无需写死机器路径。

注意：StepFun 的 API Key 不写死在脚本里，运行时从环境变量 STEPFUN_API_KEY 读取
（或在下方 STEPFUN_KEY_FALLBACK 写占位符）。这样既能在你本机用，也不会把密钥
随技能发布出去。
"""
import os
import sys
import json
import socket
import subprocess
import tkinter as tk
from tkinter import messagebox

HOME = os.path.expanduser("~")
PY = sys.executable  # 运行本脚本的 pythonw，自动适配本机
CC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ccproxy.py")

# StepFun key：优先环境变量，其次下方占位符（发布版留空，使用者自己填）
STEPFUN_KEY_FALLBACK = os.environ.get("STEPFUN_API_KEY", "")


# name=显示名, profile=profiles 下文件名(无后缀), port=需要的本地代理端口(None=直连), args=代理启动参数
# 含 __STEPFUN_KEY__ 的 args 会在启动时替换为真实 key
MODELS = [
    # 锁定具体模型优于 kilo-auto/free 随机路由：后者会抽到重推理模型（实测 7min/161token）
    ("Kilo LFM2.5（免费·agent首选）", "kilo-fast", 3461,
     "--upstream https://api.kilo.ai/api/gateway/v1/chat/completions --model liquid/lfm-2.5-2.6b:free --key anonymous"),
    ("Kilo 随机轮换（免费·可能很慢）", "spacebunny", 3457,
     "--upstream https://api.kilo.ai/api/gateway/v1/chat/completions --model kilo-auto/free --key anonymous"),
    ("Kilo 随机轮换+读图桥接（免费）", "kilo-bridge", 3457,
     "--upstream https://api.kilo.ai/api/gateway/v1/chat/completions --model kilo-auto/free --key anonymous"),
    ("读图 Vision（免费·可看图）", "vision", 3458,
     "--upstream https://api.kilo.ai/api/gateway/v1/chat/completions --model nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free --key anonymous"),
    ("DeepSeek-V4 (付费)", "deepseek", None, ""),
    ("GLM-4.7", "glm", None, ""),
    ("GLM-4-Flash（免费·稳定）", "glm4", None, ""),
    ("GLM-4-Flash + 读图桥接（免费）", "glm4-bridge", None, ""),
    ("StepFun Step 5 (推理·限时免费)", "stepfun", 3459,
     "--upstream https://api.stepfun.com/v1/chat/completions --model step-5-preview --key __STEPFUN_KEY__"),
    ("StepFun Step 5 (无推理·限时免费)", "stepfun-nothink", 3460,
     "--upstream https://api.stepfun.com/v1/chat/completions --model step-5-preview --key __STEPFUN_KEY__ --no-reasoning"),
]

DETACHED = 0x00000008  # DETACHED_PROCESS


def port_open(port):
    s = socket.socket()
    s.settimeout(0.4)
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def _resolve_args(args):
    """把 __STEPFUN_KEY__ 占位符替换成真实 key（来自环境变量/占位符）。"""
    if "__STEPFUN_KEY__" not in args:
        return args
    key = STEPFUN_KEY_FALLBACK
    if not key:
        # 仍未配置：保留占位符，ccproxy 会拿它当 key 调 StepFun → 401，
        # 由下方 on_click 的提示引导用户设置环境变量。
        return args
    return args.replace("__STEPFUN_KEY__", key)


def ensure_proxy(port, args):
    if port is None:
        return "（直连，无需代理）"
    if port_open(port):
        return "代理已在运行"
    log = os.path.join(HOME, ".claude", f"ccproxy-{port}.log")
    with open(log, "ab"):
        pass
    with open(log, "ab") as lf:
        subprocess.Popen([PY, CC, "--port", str(port)] + _resolve_args(args).split(),
                         stdout=lf, stderr=subprocess.STDOUT,
                         creationflags=DETACHED, close_fds=True)
    return "已启动代理"


def current_model():
    try:
        s = json.load(open(os.path.join(HOME, ".claude", "settings.json"), encoding="utf-8"))
        env = s.get("env", {})
        base = env.get("ANTHROPIC_BASE_URL", "")
        model = s.get("model") or env.get("ANTHROPIC_MODEL", "")
        return base, model
    except Exception:
        return "", ""


def switch(profile, port, args):
    pf = os.path.join(HOME, ".claude", "profiles", profile + ".json")
    prof = json.load(open(pf, encoding="utf-8"))
    sp = os.path.join(HOME, ".claude", "settings.json")
    settings = json.load(open(sp, encoding="utf-8"))
    settings["env"] = prof.get("env", {})
    settings["model"] = prof.get("model")
    if "modelSettings" in prof:
        settings["modelSettings"] = prof["modelSettings"]
    # 读图桥接：profile 带 mcpServers 就注入，否则清掉（避免非桥接 profile 残留 MCP）
    if "mcpServers" in prof:
        settings["mcpServers"] = prof["mcpServers"]
    else:
        settings.pop("mcpServers", None)
    tmp = sp + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    os.replace(tmp, sp)
    proxy_msg = ensure_proxy(port, args)
    return proxy_msg


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Claude 模型切换器")
        self.geometry("420x820")
        self.resizable(False, False)
        tk.Label(self, text="点哪个模型，就切到哪个\n切完重启 Claude Code 即可",
                 font=("Microsoft YaHei", 11), pady=6).pack()

        self.status = tk.Label(self, text="", fg="green", font=("Microsoft YaHei", 9),
                               wraplength=380, justify="left", height=2)
        self.status.pack(pady=4)

        for disp, prof, port, args in MODELS:
            b = tk.Button(self, text=disp, height=2,
                          font=("Microsoft YaHei", 11),
                          command=lambda d=disp, p=prof, pt=port, a=args: self.on_click(d, p, pt, a))
            b.pack(fill="x", padx=28, pady=6)

        self.refresh()

    def refresh(self):
        cur_base, cur_model = current_model()
        try:
            s = json.load(open(os.path.join(HOME, ".claude", "settings.json"), encoding="utf-8"))
            has_bridge = "vision-bridge" in s.get("mcpServers", {})
        except Exception:
            has_bridge = False
        cur_disp = "未知"
        for disp, prof, port, args in MODELS:
            try:
                p = json.load(open(os.path.join(HOME, ".claude", "profiles", prof + ".json"), encoding="utf-8"))
            except Exception:
                continue
            pbase = p["env"]["ANTHROPIC_BASE_URL"]
            pmodel = p.get("model") or p["env"].get("ANTHROPIC_MODEL", "")
            pbridge = "vision-bridge" in p.get("mcpServers", {})
            if pbase == cur_base and pmodel == cur_model and pbridge == has_bridge:
                cur_disp = disp
                break
        self.status.config(text=f"当前：{cur_disp}\n切换后请重启 Claude Code", fg="blue")

    def on_click(self, disp, prof, port, args):
        try:
            if "__STEPFUN_KEY__" in args and not STEPFUN_KEY_FALLBACK:
                messagebox.showwarning(
                    "需要 StepFun Key",
                    "StepFun 按钮需要 API Key。请先设置环境变量：\n"
                    "  set STEPFUN_API_KEY=你的key   （Windows）\n"
                    "  export STEPFUN_API_KEY=你的key   （Linux/macOS）\n"
                    "然后在 Claude Code 的 profile / models.json 里同样填该 key。")
                return
            msg = switch(prof, port, args)
            messagebox.showinfo("已切换", f"已切换到：{disp}\n{msg}\n\n请重启 Claude Code。")
            self.refresh()
        except Exception as e:
            messagebox.showerror("失败", str(e))


if __name__ == "__main__":
    try:
        App().mainloop()
    except Exception:
        import traceback
        log = os.path.join(HOME, ".claude", "switcher-error.log")
        with open(log, "a", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        try:
            messagebox.showerror("切换器出错", "详情见 " + log)
        except Exception:
            pass
