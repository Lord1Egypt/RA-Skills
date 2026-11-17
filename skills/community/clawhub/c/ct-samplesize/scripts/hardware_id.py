"""hardware_id.py — 稳定、不可逆、硬件绑定的机器标识 (ct-base §8.6 升级).

替代旧的 ``sha256(socket.gethostname())``：主机名不是硬件，在容器 / 云端环境
会随会话或账号变化，导致「同机换账号 / 网页版」SHA 不稳定，且可被改、可重名。

本模块读取真实硬件令牌，按回退链取第一个可用的，再 sha256：

  Windows:  SMBIOS UUID (ctypes 调 kernel32!GetSystemFirmwareTable('RSMB')
            解析 Type 1 结构，纯进程内零子进程，输出与 CIM
            Win32_ComputerSystemProduct.UUID 逐字节一致——本机 2026-10-15
            实证；主板级，换账号 / 改主机名 / 重装系统都不变)
            → 注册表 MachineGuid
  macOS:    IOPlatformUUID (ioreg)
  Linux:    /etc/machine-id (或 /var/lib/dbus/machine-id)
  兜底:     主机名（仅当上述全部失败，保证永不崩）

返回格式保持 ``"sha256:<64 hex>"``，与旧 query_origin 契约完全兼容。

重要边界（务必知悉）：
  - 本机硬件绑定只在「本地桌面端」真正生效——同一台物理电脑，无论切哪个
    Windows 账号、改不改主机名，输出固定。
  - 网页 / 云端版本若把 Python 跑在服务器或临时容器里，服务端代码读不到你
    本机硬件，只能读到「服务端硬件」；临时容器每次重建 machine-id 仍会变。
    那种环境无法做到「同机固定」，只能退而求其次（绑部署实例或账号）。
"""
from __future__ import annotations

import hashlib
import socket
import subprocess
import sys

# ── Windows 子进程无控制台窗口（2026-10-15）─────────────────────────────────
# Windows 上 ioreg（macOS）之外的任何控制台子系统子程序，在父进程无控制台时
# （WorkBuddy 桌面端宿主、pythonw 等 GUI 场景）直接 spawn 会让 Windows 新建
# 控制台 → 屏幕闪出前台弹窗。CREATE_NO_WINDOW（+ STARTF_USESHOWWINDOW /
# SW_HIDE 双保险）令子进程完全后台运行；stdout/stderr 管道捕获不受影响。
# 注：Windows SMBIOS UUID 已改用纯进程内 ctypes 读取（见 _smbios_uuid），
# 本 helper 现仅服务 macOS ioreg（非 Windows 返回 {}，空操作）。
_CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)


def _hidden_kwargs() -> dict:
    """返回抑制控制台弹窗的 subprocess 关键字参数（非 Windows 平台返回 {}）。"""
    if not sys.platform.startswith("win"):
        return {}
    kw = {"creationflags": _CREATE_NO_WINDOW}
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        kw["startupinfo"] = si
    except Exception:
        pass
    return kw


def _smbios_uuid() -> str | None:
    """纯进程内读取 SMBIOS System Information (Type 1) 的 UUID（零子进程）。

    走 kernel32!GetSystemFirmwareTable('RSMB') 取原始 SMBIOS 表，遍历结构
    定位 Type 1，读 offset 0x08 起 16 字节 UUID，按 WMI/CIM 口径格式化
    （time_low / time_mid / time_hi_version 三组按小端反转，输出大写
    8-4-4-4-12）——与 ``(Get-CimInstance Win32_ComputerSystemProduct).UUID``
    逐字节一致（本机 2026-10-15 三方交叉实证），故 hardware_id 输出值不变。
    任何环节失败返回 None，由调用方回退下一级来源（保证永不崩）。
    """
    try:
        import ctypes
        from ctypes import wintypes
    except Exception:
        return None
    try:
        get_fw_tbl = ctypes.windll.kernel32.GetSystemFirmwareTable
        get_fw_tbl.argtypes = [wintypes.DWORD, wintypes.DWORD,
                               ctypes.c_void_p, wintypes.DWORD]
        get_fw_tbl.restype = wintypes.DWORD
        RSMB = 0x52534D42  # 'RSMB' — Raw SMBIOS provider
        size = get_fw_tbl(RSMB, 0, None, 0)
        if not size:
            return None
        buf = ctypes.create_string_buffer(size)
        if get_fw_tbl(RSMB, 0, buf, size) != size:
            return None
        data = buf.raw[:size]
        if len(data) < 9:
            return None
        off = 8  # RawSMBIOSData 头 8 字节（Used20CallingMethod/Major/Minor/
        #         DmiRevision/Length）之后即 SMBIOS 表数据
        while off + 4 <= len(data):
            stype, slen = data[off], data[off + 1]
            if slen < 4 or off + slen > len(data):
                return None
            if stype == 1 and slen >= 0x19:  # Type 1，SMBIOS 2.6+ 含 16B UUID
                u = data[off + 0x08: off + 0x18]
                if len(u) == 16:
                    b = bytes([u[3], u[2], u[1], u[0],
                               u[5], u[4], u[7], u[6]]) + u[8:16]
                    s = "%02X%02X%02X%02X-%02X%02X-%02X%02X-%02X%02X-%s" % (
                        b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7],
                        b[8], b[9], b[10:16].hex().upper())
                    if s not in ("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF",
                                 "00000000-0000-0000-0000-000000000000"):
                        return "win:smbios:" + s
                return None
            # 跳到下一结构：formatted 区之后是 NUL 结尾字符串区（双 NUL 收尾）
            p = off + slen
            while p + 1 < len(data) and not (data[p] == 0 and data[p + 1] == 0):
                p += 1
            off = p + 2
    except Exception:
        return None
    return None


def _raw_hw_token() -> str:
    """返回未哈希的硬件令牌字符串；任一来源失败即回退到下一项，最后兜底主机名。"""
    # Windows
    if sys.platform.startswith("win"):
        # 1) SMBIOS UUID（最硬，主板级，跨账号 / 主机名 / 重装都不变）
        #    纯进程内 ctypes 读取（2026-10-15 起零子进程）——原 powershell.exe
        #    方案在无控制台父进程下闪弹窗；输出与 CIM 逐字节一致（本机实证），
        #    无理由再起外部进程。失败（极老系统 / 无 SMBIOS）自动回退下一级。
        s = _smbios_uuid()
        if s:
            return s
        # 2) 注册表 MachineGuid（跨账号 / 主机名稳定，仅重装系统变）
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
            ) as k:
                return "win:machineguid:" + winreg.QueryValueEx(k, "MachineGuid")[0]
        except Exception:
            pass
    # macOS
    elif sys.platform == "darwin":
        try:
            out = subprocess.check_output(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                stderr=subprocess.DEVNULL, text=True, timeout=10,
                **_hidden_kwargs())
            for line in out.splitlines():
                if "IOPlatformUUID" in line:
                    # 形如:   "IOPlatformUUID" = "XXXXXXXX-XXXX-..."
                    parts = line.split('"')
                    if len(parts) >= 4 and parts[3].strip():
                        return "mac:platformuuid:" + parts[3].strip()
        except Exception:
            pass
    # Linux（及其他类 Unix）
    else:
        for p in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
            try:
                with open(p, encoding="utf-8") as f:
                    s = f.read().strip()
                if s:
                    return "linux:machine-id:" + s
            except Exception:
                pass
    # 兜底：主机名（旧行为；容器里仍会变，但保证永不抛异常）
    try:
        return "host:" + socket.gethostname()
    except Exception:
        return "host:unknown"


def hardware_id() -> str:
    """返回稳定、不可逆、硬件绑定的机器标识：``"sha256:<64 hex>"``。"""
    return "sha256:" + hashlib.sha256(_raw_hw_token().encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print(hardware_id())
