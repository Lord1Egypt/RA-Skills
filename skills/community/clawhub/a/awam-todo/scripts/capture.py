#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""awam-todo 捕获服务（Windows）。

全局快捷键 → 读取剪贴板 → 分诊（triage）→ 需要确认 / 填写时用系统弹框 → 执行。

由 web/server.py 在启动时拉起（服务必须随 UI 服务运行才能捕获）。
纯标准库实现：RegisterHotKey + GetMessage 消息循环读全局快捷键、CF_UNICODETEXT 读剪贴板、
tkinter 系统弹框 —— 不依赖任何第三方包。非 Windows / 无图形环境时优雅降级（返回原因）。

语言策略：与 CLI 一致，弹框文案固定英文；数据值（状态 / 重要 / 紧急 / 标签 / 任务原文）原样展示。
"""

import ctypes
import datetime as dt
import os
import sys
import threading
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import todo  # noqa: E402

if os.name == "nt":
    import ctypes.wintypes as wt
else:
    wt = None

WM_HOTKEY = 0x0312
WM_QUIT = 0x0012
CF_UNICODETEXT = 13
EXIT_NEEDS_CONFIRM = todo.EXIT_NEEDS_CONFIRM
DIALOG_STATUSES = ("进行中", "待开始", "结束", "维护", "其他")


def tk_available():
    """系统弹框（tkinter）是否可用。"""
    try:
        import tkinter  # noqa: F401
        return True
    except Exception:
        return False


# ---- 剪贴板读取（纯 Win32，64 位安全的句柄类型） ----
def _setup_win32():
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    user32.OpenClipboard.argtypes = [wt.HWND]
    user32.OpenClipboard.restype = wt.BOOL
    user32.IsClipboardFormatAvailable.argtypes = [wt.UINT]
    user32.IsClipboardFormatAvailable.restype = wt.BOOL
    user32.GetClipboardData.argtypes = [wt.UINT]
    user32.GetClipboardData.restype = wt.HANDLE
    user32.CloseClipboard.restype = wt.BOOL
    kernel32.GlobalLock.argtypes = [wt.HGLOBAL]
    kernel32.GlobalLock.restype = wt.LPVOID
    kernel32.GlobalUnlock.argtypes = [wt.HGLOBAL]
    kernel32.GlobalUnlock.restype = wt.BOOL
    return user32, kernel32


def read_clipboard_text():
    """读剪贴板文本（CF_UNICODETEXT）。非文本 / 空 / 失败返回 ""。"""
    if os.name != "nt" or wt is None:
        return ""
    user32, kernel32 = _setup_win32()
    if not user32.OpenClipboard(None):
        return ""
    try:
        if not user32.IsClipboardFormatAvailable(CF_UNICODETEXT):
            return ""
        h = user32.GetClipboardData(CF_UNICODETEXT)
        if not h:
            return ""
        ptr = kernel32.GlobalLock(h)
        if not ptr:
            return ""
        try:
            return ctypes.wstring_at(ptr).strip()
        finally:
            kernel32.GlobalUnlock(h)
    finally:
        user32.CloseClipboard()


# ---- 全局快捷键监听（线程内消息循环） ----
class HotkeyListener:
    """Win32 全局快捷键监听。start() 后独立线程跑消息循环；stop() 退出。"""

    def __init__(self, mods, vk, on_hotkey, on_error=None):
        self.mods = mods
        self.vk = vk
        self.on_hotkey = on_hotkey
        self.on_error = on_error or (lambda msg: None)
        self._id = 1
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True,
                                       name="awam-todo-hotkey")

    def start(self):
        if self.thread.ident is None:
            self.thread.start()

    def _run(self):
        if os.name != "nt" or wt is None:
            self.on_error("Capture requires Windows.")
            return
        user32 = ctypes.windll.user32
        user32.RegisterHotKey.argtypes = [wt.HWND, ctypes.c_int, wt.UINT, wt.UINT]
        user32.RegisterHotKey.restype = wt.BOOL
        user32.GetMessageW.argtypes = [ctypes.POINTER(wt.MSG), wt.HWND, wt.UINT, wt.UINT]
        user32.GetMessageW.restype = ctypes.c_int
        user32.TranslateMessage.argtypes = [ctypes.POINTER(wt.MSG)]
        user32.DispatchMessageW.argtypes = [ctypes.POINTER(wt.MSG)]
        user32.UnregisterHotKey.argtypes = [wt.HWND, ctypes.c_int]
        user32.UnregisterHotKey.restype = wt.BOOL
        user32.PostThreadMessageW.argtypes = [wt.DWORD, wt.UINT, wt.WPARAM, wt.LPARAM]
        user32.PostThreadMessageW.restype = wt.BOOL

        if not user32.RegisterHotKey(None, self._id, self.mods, self.vk):
            self.on_error("Hotkey registration failed (already taken by another app?). "
                          "Change it in the web UI Settings.")
            return
        msg = wt.MSG()
        try:
            while not self._stop.is_set():
                r = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if r <= 0:
                    break
                if msg.message == WM_HOTKEY and msg.wParam == self._id:
                    try:
                        self.on_hotkey()
                    except Exception as e:  # noqa: BLE001
                        self.on_error("Capture error: %s" % e)
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        finally:
            user32.UnregisterHotKey(None, self._id)

    def stop(self):
        self._stop.set()
        if self.thread.ident is not None and os.name == "nt" and wt is not None:
            ctypes.windll.user32.PostThreadMessageW(self.thread.ident, WM_QUIT, 0, 0)


# ---- 系统弹框（全部 tkinter，固定英文文案 + 中文数据值原样） ----
def _new_root():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    return root, tk


def show_toast(title, msg, ms=2600):
    """非阻塞角标提示（自动关闭），用于捕获成功 / 空剪贴板等轻量反馈。"""
    if not tk_available():
        return
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        top = tk.Toplevel(root)
        top.overrideredirect(True)
        top.attributes("-topmost", True)
        top.configure(bg="#2b2b2b")
        tk.Label(top, text=title, bg="#2b2b2b", fg="#ffffff",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(top, text=msg, bg="#2b2b2b", fg="#eeeeee",
                 font=("Segoe UI", 10), wraplength=400, justify="left").pack(anchor="w", padx=14, pady=(0, 10))
        top.update_idletasks()
        w = min(430, top.winfo_reqwidth() + 28)
        h = top.winfo_reqheight() + 12
        sw, sh = top.winfo_screenwidth(), top.winfo_screenheight()
        top.geometry("%dx%d+%d+%d" % (w, h, sw - w - 24, sh - h - 72))
        root.after(ms, lambda: (top.destroy(), root.destroy()))
        root.mainloop()
    except Exception:
        pass


def show_confirm(title, msg, ok_label="OK", cancel_label="Cancel"):
    """阻塞确认框。返回 True / False / None（无法弹框）。"""
    if not tk_available():
        return None
    try:
        import tkinter as tk
        from tkinter import messagebox
        root, _ = _new_root()
        ans = messagebox.askyesno(title, msg, icon="question")
        root.destroy()
        return bool(ans)
    except Exception:
        return None


def show_error(title, msg):
    """错误提示框（阻塞）。"""
    if not tk_available():
        return
    try:
        import tkinter as tk
        from tkinter import messagebox
        root, _ = _new_root()
        messagebox.showerror(title, msg)
        root.destroy()
    except Exception:
        pass


def _verdict_text(proposal):
    action = proposal.get("action")
    reasons = proposal.get("reasons") or []
    t = proposal.get("target")
    if action == "add":
        if t:
            return "Add -> but a duplicate/similar todo exists: %s (%s): %s" % (
                t.get("id"), t.get("kind"), t.get("text"))
        return "Add as a new todo"
    if action == "status":
        if t:
            return "Change status of %s (%s) to %s" % (t.get("id"), t.get("text"),
                                                       proposal.get("status"))
        return "Status change requested, but no matching todo was found"
    if action == "update":
        if t:
            return "Update %s (%s)" % (t.get("id"), t.get("text"))
        return "Update requested, but no matching todo was found"
    if action == "delete":
        if t:
            return "DELETE %s (%s)" % (t.get("id"), t.get("text"))
        return "Delete requested, but no matching todo was found"
    return "Not recognized as a todo action: %s" % ", ".join(reasons or ("unknown",))


def _split_tags(s):
    return [x.strip() for x in re_split_tags(s) if x.strip()]


def re_split_tags(s):
    import re
    return re.split(r"[;；、,，]", s or "")


def show_triage_dialog(proposal, cfg):
    """分诊确认弹框：展示判定，按动作提供可选字段 / 目标选择。

    返回执行参数 dict（choice=execute）或 None（取消）：
      {"choice": "execute", "action": ..., "target_id": ..., "status": ...,
       "text": ..., "fields": {...}, "update_id": ..., "force": ...}
    """
    if not tk_available():
        return None
    import tkinter as tk
    from tkinter import ttk

    action = proposal.get("action") or "unknown"
    reasons = proposal.get("reasons") or []
    target = proposal.get("target")
    candidates = proposal.get("candidates") or []
    fields = proposal.get("fields") or {}

    root = tk.Tk()
    root.title("awam-todo Capture")
    root.attributes("-topmost", True)
    root.resizable(False, False)
    root.configure(bg="#f5f5f5")
    pad = 12
    result = {"choice": "cancel", "action": action}

    tk.Label(root, text="Captured text / 捕获内容:", bg="#f5f5f5", anchor="w",
             font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=pad, pady=(pad, 2))
    txt = tk.Text(root, width=54, height=3, wrap="word", font=("Segoe UI", 10),
                  highlightthickness=1, highlightbackground="#c9c9c9")
    txt.insert("1.0", proposal.get("text") or "")
    txt.grid(row=1, column=0, columnspan=3, sticky="we", padx=pad)

    tk.Label(root, text="Verdict / 判定:", bg="#f5f5f5", anchor="w",
             font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=pad, pady=(8, 2))
    tk.Label(root, text=_verdict_text(proposal), bg="#f5f5f5", fg="#1a56a0", anchor="w",
             justify="left", wraplength=500, font=("Segoe UI", 10)).grid(
        row=3, column=0, columnspan=3, sticky="w", padx=pad)

    row = 4
    vars_ = {}

    def add_row(label, widget, sticky="we"):
        nonlocal row
        tk.Label(root, text=label, bg="#f5f5f5", anchor="w",
                 font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", padx=pad, pady=(6, 2))
        widget.grid(row=row, column=1, columnspan=2, sticky=sticky, padx=(0, pad))
        row += 1

    def entry(default, width=40):
        v = tk.StringVar(value=default or "")
        e = tk.Entry(root, textvariable=v, width=width, font=("Segoe UI", 10))
        return v, e

    def combo(values, default):
        v = tk.StringVar(value=default or (values[0] if values else ""))
        c = ttk.Combobox(root, textvariable=v, values=values, state="readonly", width=44)
        return v, c

    # 目标选择（update / status / delete / duplicate-add 用）
    target_var = None
    if action in ("update", "status", "delete") or (action == "add" and target):
        opts = []
        defs = ""
        if action == "add" and target:
            opts.append(("update:" + target["id"], "Update: %s — %s" % (target["id"], target["text"])))
            defs = opts[0][0]
        if target and action in ("update", "status", "delete"):
            opts.append((target["id"], "%s — %s" % (target["id"], target["text"])))
            defs = target["id"]
        seen = set()
        for c in candidates:
            if c["id"] in seen:
                continue
            seen.add(c["id"])
            opts.append((c["id"], "%s — %s" % (c["id"], c["text"])))
        if action == "add" and target:
            opts.append(("force", "Create anyway (force)"))
        target_var, _ = combo([o[0] for o in opts], defs)
        add_row("Target / 目标:", target_var[1])

    status_var = None
    if action == "status":
        status_var, _ = combo(list(DIALOG_STATUSES), proposal.get("status"))
        add_row("New status / 新状态:", status_var[1])

    due_var = tags_var = note_var = newtext_var = None
    imp_var = urg_var = None
    if action == "add":
        due_var, due_e = entry(fields.get("due"))
        add_row("Deadline / 截止:", due_e)
        sug = proposal.get("suggested_tags") or []
        tags_var, tags_e = entry("; ".join(sug) if sug else "")
        add_row("Tags / 标签 (suggestion only):", tags_e)
        note_var, note_e = entry(fields.get("note"))
        add_row("Note / 备注:", note_e)
        chk = tk.Frame(root, bg="#f5f5f5")
        imp_var = tk.BooleanVar(value=(fields.get("importance") == "重要"))
        urg_var = tk.BooleanVar(value=(fields.get("urgent") == "紧急"))
        tk.Checkbutton(chk, text="重要 / Important", variable=imp_var, bg="#f5f5f5",
                       anchor="w", font=("Segoe UI", 9)).pack(side="left", padx=(0, 16))
        tk.Checkbutton(chk, text="紧急 / Urgent", variable=urg_var, bg="#f5f5f5",
                       anchor="w", font=("Segoe UI", 9)).pack(side="left")
        add_row("Flags / 标记:", chk, sticky="w")
    elif action == "update":
        newtext_var, newtext_e = entry(fields.get("text"))
        add_row("New text / 新内容 (optional):", newtext_e)
        due_var, due_e = entry(fields.get("due"))
        add_row("Deadline / 截止 (optional):", due_e)
        tags_var, tags_e = entry("; ".join(fields.get("tags") or []))
        add_row("Tags / 标签 (optional):", tags_e)
        note_var, note_e = entry(fields.get("note"))
        add_row("Note / 备注 (optional):", note_e)

    if action == "unknown" or ("target_not_found" in reasons and action in ("update", "status", "delete")):
        if action in ("update", "status", "delete"):
            tk.Label(root, text="No matching todo found. Pick an existing one to update, "
                                "or add as a new todo:", bg="#f5f5f5", fg="#8a6d3b", anchor="w",
                     justify="left", wraplength=500, font=("Segoe UI", 9)).grid(
                row=row, column=0, columnspan=3, sticky="w", padx=pad, pady=(8, 2))
            row += 1
            opts = [("", "Add as a new todo / 作为新任务添加")]
            seen = set()
            for c in candidates:
                if c["id"] in seen:
                    continue
                seen.add(c["id"])
                opts.append((c["id"], "Update: %s — %s" % (c["id"], c["text"])))
            target_var, _ = combo([o[0] for o in opts], "")
            add_row("How / 处理方式:", target_var[1])

    foot = tk.Frame(root, bg="#f5f5f5")
    foot.grid(row=row, column=0, columnspan=3, sticky="e", padx=pad, pady=(14, pad))

    def on_ok():
        result["choice"] = "execute"
        result["action"] = action
        result["text"] = txt.get("1.0", "end-1c").strip()
        if target_var is not None:
            pick = target_var.get()
            if action == "add":
                if pick.startswith("update:"):
                    result["update_id"] = pick.split(":", 1)[1]
                elif pick == "force":
                    result["force"] = True
                elif pick:
                    result["update_id"] = pick
            else:
                result["target_id"] = pick or None
        if status_var is not None:
            result["status"] = status_var.get()
        f = {}
        if action == "add":
            f["due"] = due_var.get().strip() or None if due_var else None
            f["tags"] = _split_tags(tags_var.get().strip()) if tags_var else None
            f["note"] = note_var.get().strip() or None if note_var else None
            f["importance"] = ("重要" if imp_var.get() else None) if imp_var else None
            f["urgent"] = ("紧急" if urg_var.get() else None) if urg_var else None
        elif action == "update":
            f["text"] = newtext_var.get().strip() or None if newtext_var else None
            f["due"] = due_var.get().strip() or None if due_var else None
            f["tags"] = _split_tags(tags_var.get().strip()) if tags_var else None
            f["note"] = note_var.get().strip() or None if note_var else None
        result["fields"] = {k: v for k, v in f.items() if v is not None}
        if action in ("update", "status") and "target_not_found" in reasons and target_var is not None:
            # 未锁住目标时选了候选 → 退化为「更新该候选」
            if result.get("target_id"):
                result["action"] = "update"
        root.destroy()

    ok_label = "Delete / 删除" if action == "delete" else ("Execute / 执行")
    ok_btn = tk.Button(foot, text=ok_label, width=12, bg="#d9534f" if action == "delete" else "#337ab7",
                       fg="#ffffff", relief="flat", font=("Segoe UI", 10, "bold"),
                       command=on_ok)
    ok_btn.pack(side="right", padx=(8, 0))
    tk.Button(foot, text="Cancel / 取消", width=10, bg="#e7e7e7", relief="flat",
              font=("Segoe UI", 10), command=root.destroy).pack(side="right")

    root.mainloop()
    return result if result.get("choice") == "execute" else None


# ---- 分诊结果应用配置过滤 ----
def apply_config_filters(proposal, cfg):
    """按 env.json 的 capture.triage_types 过滤：被禁用的动作转为「需确认」，
    并提供 fallback_action=add 让弹框可以按新任务处理。返回新 dict，不改入参。"""
    enabled = (cfg.get("triage_types") or {})
    action = proposal.get("action")
    if action in ("add", "update", "delete", "status") and not enabled.get(action, True):
        p = dict(proposal)
        p["need_confirm"] = True
        p["confidence"] = "low"
        p["reasons"] = list(proposal.get("reasons") or [])
        if "action_disabled" not in p["reasons"]:
            p["reasons"].append("action_disabled")
        p["fallback_action"] = "add"
        return p
    return proposal


# ---- 执行 ----
def _ns(**kw):
    return SimpleNamespace(**kw)


def execute_proposal(proposal, dlg, cfg):
    """执行分诊结果。dlg 为 None 表示无需确认直接执行；否则使用弹框返回的参数。
    返回 (退出码, 动作标识)。退出码 3=仍需确认（守卫冲突），2=参数/目标错误，0=成功。"""
    now = dt.datetime.now()
    action = (dlg or {}).get("action") or proposal.get("action")
    if action == "unknown":
        return 2, "unknown"
    target_id = (dlg or {}).get("target_id") or (proposal.get("target") or {}).get("id")
    fields = dict(proposal.get("fields") or {})
    if dlg and dlg.get("fields"):
        fields.update(dlg["fields"])
    if dlg and dlg.get("text") is not None:
        fields["text"] = dlg["text"]

    if action == "add":
        ns = _ns(
            text=fields.get("text") or proposal.get("text"),
            importance=fields.get("importance"),
            urgent=fields.get("urgent"),
            status=None,
            note=fields.get("note"),
            blocker=None, counter=None,
            workspace=fields.get("workspace"),
            docs=None, links=None, deps=None,
            tags=fields.get("tags"),
            parent=None,
            due=fields.get("due"),
            date="", from_type="capture", from_url=None,
            force=bool((dlg or {}).get("force")),
            update_id=(dlg or {}).get("update_id") or "",
        )
        return todo.cmd_add(ns, now), "add"

    if action == "status":
        if not target_id:
            return 2, "no target"
        status = (dlg or {}).get("status") or proposal.get("status")
        if not status:
            return 2, "no status"
        date, data, t = todo._find_task(target_id)
        if t is None:
            return 2, "task not found"
        if t.get("status") == status:
            return 0, "status"
        return todo._set_status(target_id, status, bool((dlg or {}).get("force"))), "status"

    if action == "update":
        if not target_id:
            return 2, "no target"
        ns = _ns(
            text=fields.get("text"),
            importance=fields.get("importance"),
            urgent=fields.get("urgent"),
            status=None,
            note=fields.get("note"),
            blocker=None, counter=None,
            workspace=fields.get("workspace"),
            docs=None, links=None, deps=None,
            tags=fields.get("tags"),
            parent=None,
            due=fields.get("due"),
            date="", from_type="capture", from_url=None,
            force=bool((dlg or {}).get("force")),
            update_id=target_id,
        )
        return todo._update_existing_task(target_id, ns, now), "update"

    if action == "delete":
        if not target_id:
            return 2, "no target"
        return todo._delete_task(target_id, now, quiet=True), "delete"

    return 2, "unsupported action"


_RESULT_LABELS = {"add": "Todo added", "update": "Todo updated",
                  "status": "Status changed", "delete": "Todo deleted"}


def _run_with_retry(proposal, dlg, cfg):
    """执行并处理结果：守卫冲突（exit 3）时弹框询问是否强制。"""
    rc, what = execute_proposal(proposal, dlg, cfg)
    if rc == EXIT_NEEDS_CONFIRM:
        if show_confirm(
                "awam-todo 需要确认",
                "The operation is blocked (unfinished dependencies / subtasks, or a duplicate).\n"
                "Force it anyway?",
                ok_label="Force / 强制", cancel_label="Cancel / 取消"):
            dlg2 = dict(dlg or {})
            dlg2["force"] = True
            rc, what = execute_proposal(proposal, dlg2, cfg)
    if rc == 0:
        if cfg.get("toast", True):
            show_toast("awam-todo", _RESULT_LABELS.get(what, "Done"))
    elif rc == 2:
        show_error("awam-todo", "Operation failed: %s" % what)
    elif rc == EXIT_NEEDS_CONFIRM:
        show_toast("awam-todo", "Cancelled (guarded operation)")
    return rc


def capture_flow(cfg):
    """一次完整捕获：读剪贴板 → 分诊 →（需确认则弹框）→ 执行 → 结果提示。"""
    text = read_clipboard_text()
    if not text:
        show_toast("awam-todo",
                   "Clipboard is empty or not text.\nCopy something first, then press the hotkey again.")
        return
    proposal = todo.triage_text(text)
    proposal = apply_config_filters(proposal, cfg)

    action = proposal.get("action")
    # 删除且配置为「不确认」时直接执行
    if action == "delete" and not cfg.get("confirm_delete", True):
        _run_with_retry(proposal, None, cfg)
        return
    # 高置信：直接执行
    if not proposal.get("need_confirm"):
        _run_with_retry(proposal, None, cfg)
        return
    # 需要确认 / 填写：系统弹框
    dlg = show_triage_dialog(proposal, cfg)
    if not dlg:
        return
    _run_with_retry(proposal, dlg, cfg)
