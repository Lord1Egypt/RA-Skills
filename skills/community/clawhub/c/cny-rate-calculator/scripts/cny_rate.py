#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大草原匯率計算器 - CNY Rate Calculator
自動抓取台銀人民幣匯率並計算優惠價格

Author: HomeClaw
Version: 1.2.0
"""

import requests
import re
import sys
import os
import json
import uuid
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, List


# =========================================================
# 互動式方向鍵選單
# =========================================================

def _enable_ansi_windows():
    """啟用 Windows 10+ ANSI 轉義碼支援"""
    if os.name == 'nt':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass


def menu_select(title: str, options: List[str], hints: List[str] = None,
                subtitle: str = "") -> int:
    """
    方向鍵互動式選單。

    Args:
        title:    選單標題
        options:  選項文字列表
        hints:    每個選項的說明文字（可選，與 options 等長）
        subtitle: 標題下方的說明文字（可選）

    Returns:
        選擇的索引（0-based），-1 代表取消（Esc）
    """
    _enable_ansi_windows()

    if not options:
        return -1

    hints = hints or [''] * len(options)
    while len(hints) < len(options):
        hints.append('')

    current = 0

    # 計算每次重繪需要往上移動的行數
    # 固定行：分隔線 + 標題 + 副標題（若有）+ 分隔線 + 空行 + 空行 + 提示行 = 5 或 6
    FIXED_TOP = 5 if not subtitle else 6
    # 每個選項佔幾行
    option_rows = [2 if h else 1 for h in hints]
    total_lines = FIXED_TOP + sum(option_rows)

    SEP = "=" * 52
    DIM   = "\033[90m"
    GREEN = "\033[32;1m"
    RESET = "\033[0m"

    def render(first: bool):
        if not first:
            # \033[{N}F = 向上移動 N 行並回到行首
            sys.stdout.write(f"\033[{total_lines}F")

        def wline(text=""):
            sys.stdout.write(f"\033[2K{text}\n")

        wline(SEP)
        wline(f"  {title}")
        if subtitle:
            wline(f"  {DIM}{subtitle}{RESET}")
        wline(SEP)
        wline()

        for i, (opt, hint) in enumerate(zip(options, hints)):
            if i == current:
                marker = f"{GREEN}►{RESET}"
                label  = f"{GREEN}{opt}{RESET}"
            else:
                marker = " "
                label  = opt
            wline(f"  {marker} {label}")
            if hint:
                wline(f"      {DIM}{hint}{RESET}")

        wline()
        sys.stdout.write(
            f"\033[2K  {DIM}↑ ↓ 移動選擇   Enter 確認   Esc 取消{RESET}"
        )
        sys.stdout.flush()

    render(first=True)
    print()  # 保留一行讓提示不被截斷

    if os.name == 'nt':
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key in (b'\xe0', b'\x00'):   # 特殊鍵前綴
                key2 = msvcrt.getch()
                if key2 == b'H':            # ↑
                    current = (current - 1) % len(options)
                    render(first=False)
                elif key2 == b'P':          # ↓
                    current = (current + 1) % len(options)
                    render(first=False)
            elif key == b'\r':              # Enter
                print()
                return current
            elif key == b'\x1b':            # Esc
                print()
                return -1
            elif b'1' <= key <= b'9':       # 數字快捷鍵
                idx = int(key.decode()) - 1
                if 0 <= idx < len(options):
                    current = idx
                    render(first=False)
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    nxt = sys.stdin.read(1)
                    if nxt == '[':
                        arrow = sys.stdin.read(1)
                        if arrow == 'A':        # ↑
                            current = (current - 1) % len(options)
                            render(first=False)
                        elif arrow == 'B':      # ↓
                            current = (current + 1) % len(options)
                            render(first=False)
                    else:                       # 單獨 Esc
                        print()
                        return -1
                elif ch in ('\r', '\n'):        # Enter
                    print()
                    return current
                elif '1' <= ch <= '9':
                    idx = int(ch) - 1
                    if 0 <= idx < len(options):
                        current = idx
                        render(first=False)
                elif ch in ('q', 'Q'):
                    print()
                    return -1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return -1


def confirm(question: str) -> bool:
    """
    是/否確認選單（方向鍵版）。

    Returns:
        True = 是，False = 否
    """
    opts = ["是，繼續", "否，跳過"]
    idx  = menu_select(question, opts)
    if idx == -1:
        return False
    return idx == 0


def menu_multiselect(title: str, options: List[str], subtitle: str = "",
                     preselected: List[int] = None) -> Optional[List[int]]:
    """
    多選互動式選單。Space 切換勾選，方向鍵移動，Enter 確認。

    Returns:
        選中的索引列表（已排序），None 代表取消（Esc）
    """
    _enable_ansi_windows()

    if not options:
        return []

    selected = set(preselected or [])
    current  = 0

    FIXED_TOP   = 5 if not subtitle else 6
    total_lines = FIXED_TOP + len(options)

    SEP   = "=" * 52
    DIM   = "\033[90m"
    GREEN = "\033[32;1m"
    CYAN  = "\033[36;1m"
    RESET = "\033[0m"

    def render(first: bool):
        if not first:
            sys.stdout.write(f"\033[{total_lines}F")

        def wline(text=""):
            sys.stdout.write(f"\033[2K{text}\n")

        wline(SEP)
        wline(f"  {title}")
        if subtitle:
            wline(f"  {DIM}{subtitle}{RESET}")
        wline(SEP)
        wline()

        for i, opt in enumerate(options):
            check  = f"{CYAN}[✓]{RESET}" if i in selected else "[ ]"
            if i == current:
                marker = f"{GREEN}►{RESET}"
                label  = f"{GREEN}{opt}{RESET}"
            else:
                marker = " "
                label  = opt
            wline(f"  {marker} {check} {label}")

        sys.stdout.write(
            f"\033[2K  {DIM}↑ ↓ 移動   Space 切換勾選   Enter 確認   Esc 取消{RESET}"
        )
        sys.stdout.flush()

    render(first=True)
    print()

    if os.name == 'nt':
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key in (b'\xe0', b'\x00'):
                key2 = msvcrt.getch()
                if key2 == b'H':        # ↑
                    current = (current - 1) % len(options)
                    render(first=False)
                elif key2 == b'P':      # ↓
                    current = (current + 1) % len(options)
                    render(first=False)
            elif key == b' ':           # Space: toggle
                if current in selected:
                    selected.discard(current)
                else:
                    selected.add(current)
                render(first=False)
            elif key == b'\r':          # Enter: confirm
                print()
                return sorted(selected)
            elif key == b'\x1b':        # Esc: cancel
                print()
                return None
    else:
        import tty
        import termios
        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    nxt = sys.stdin.read(1)
                    if nxt == '[':
                        arrow = sys.stdin.read(1)
                        if arrow == 'A':    # ↑
                            current = (current - 1) % len(options)
                            render(first=False)
                        elif arrow == 'B':  # ↓
                            current = (current + 1) % len(options)
                            render(first=False)
                    else:
                        print()
                        return None
                elif ch == ' ':             # Space: toggle
                    if current in selected:
                        selected.discard(current)
                    else:
                        selected.add(current)
                    render(first=False)
                elif ch in ('\r', '\n'):    # Enter: confirm
                    print()
                    return sorted(selected)
                elif ch in ('q', 'Q'):
                    print()
                    return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return None


# =========================================================
# 例外
# =========================================================

class ConfigError(Exception):
    pass


# =========================================================
# 主類別
# =========================================================

class CNYRateCalculator:
    """人民幣匯率計算器"""

    PRICE_DELTAS = [0.05, 0.03, 0.015]
    PRICE_LABELS = ["基礎成本", "滿萬優惠", "五萬優惠"]
    BOT_URL      = "https://rate.bot.com.tw/xrt"

    OPENCLAW_CONFIG_PATHS = [
        os.path.expanduser("~/.openclaw/openclaw.json"),
        os.path.expanduser("~/.openclaw/config.json"),
        os.path.join(os.environ.get('APPDATA', ''), 'openclaw', 'openclaw.json'),
        os.path.join(os.environ.get('APPDATA', ''), 'openclaw', 'config.json'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'openclaw', 'config.json'),
    ]

    OPENCLAW_CRON_PATHS = [
        os.path.expanduser("~/.openclaw/cron/jobs.json"),
        os.path.join(os.environ.get('APPDATA', ''), 'openclaw', 'cron', 'jobs.json'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'openclaw', 'cron', 'jobs.json'),
    ]

    SKILL_NAME  = "cny-rate-calculator"
    SKILL_EVENT = "執行人民幣匯率計算並發送通知"

    DEFAULT_SCHEDULE = {
        'enabled':        True,
        'days_of_week':   [1, 2, 3, 4, 5],
        'start_time':     '09:00',
        'end_time':       '17:00',
        'interval_hours': 1,
        'schedule_times': [f"{h:02d}:00" for h in range(9, 18)],
        'description':    '週一至週五 09:00–17:00 每小時',
        'cron':           '0 9-17 * * 1,2,3,4,5',
    }

    def __init__(self, config_path: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.config_path = config_path or self._find_skill_config()
        self.config = self._load_config(self.config_path)

    # -------------------------------------------------------
    # 配置管理
    # -------------------------------------------------------

    def _find_skill_config(self) -> Optional[str]:
        candidates = [
            os.path.join(os.path.dirname(__file__), '..', 'config.json'),
            os.path.join(os.path.dirname(__file__), 'config.json'),
            'config.json',
        ]
        for p in candidates:
            if os.path.exists(p):
                return os.path.normpath(p)
        return None

    def _find_openclaw_config(self) -> Optional[str]:
        for p in self.OPENCLAW_CONFIG_PATHS:
            if p and os.path.exists(p):
                return p
        return None

    def _find_cron_jobs_path(self) -> Optional[str]:
        """尋找 OpenClaw cron/jobs.json，找不到則嘗試從 openclaw.json 同層推算"""
        for p in self.OPENCLAW_CRON_PATHS:
            if p and os.path.exists(p):
                return p
        # 從 openclaw.json 路徑往上推算
        oc_path = self._find_openclaw_config()
        if oc_path:
            candidate = os.path.join(os.path.dirname(oc_path), 'cron', 'jobs.json')
            if os.path.exists(candidate):
                return candidate
        return None

    def _register_cron_job(self, cron_expr: str, tz: str = 'Asia/Taipei') -> bool:
        """將排程寫入 OpenClaw cron/jobs.json（存在同名則更新，不存在則新增）"""
        jobs_path = self._find_cron_jobs_path()

        # 若找不到現有檔案，嘗試從 openclaw.json 同層建立目錄
        if not jobs_path:
            oc_path = self._find_openclaw_config()
            if not oc_path:
                print("  ⚠️  找不到 OpenClaw cron 路徑，請手動登記排程。", file=sys.stderr)
                return False
            jobs_path = os.path.join(os.path.dirname(oc_path), 'cron', 'jobs.json')
            os.makedirs(os.path.dirname(jobs_path), exist_ok=True)

        # 讀取現有 jobs
        if os.path.exists(jobs_path):
            try:
                with open(jobs_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                data = {'version': 1, 'jobs': []}
        else:
            data = {'version': 1, 'jobs': []}

        now_ms = int(datetime.now().timestamp() * 1000)

        # 更新既有同名排程，或新增
        existing = next((j for j in data['jobs'] if j.get('name') == self.SKILL_NAME), None)
        if existing:
            existing['schedule']['expr'] = cron_expr
            existing['schedule']['tz']   = tz
            existing['updatedAtMs']      = now_ms
            existing['enabled']          = True
        else:
            data['jobs'].append({
                'id':           str(uuid.uuid4()),
                'agentId':      'main',
                'sessionKey':   'agent:main:main',
                'name':         self.SKILL_NAME,
                'enabled':      True,
                'createdAtMs':  now_ms,
                'updatedAtMs':  now_ms,
                'schedule': {
                    'kind': 'cron',
                    'expr': cron_expr,
                    'tz':   tz,
                },
                'sessionTarget': 'main',
                'wakeMode':      'now',
                'payload': {
                    'kind': 'systemEvent',
                    'text': self.SKILL_EVENT,
                },
                'delivery': {'mode': 'none'},
                'state': {
                    'consecutiveErrors': 0,
                },
            })

        try:
            with open(jobs_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 排程已登記：{cron_expr}（{jobs_path}）")
            return True
        except Exception as e:
            print(f"  ⚠️  無法寫入 cron/jobs.json：{e}", file=sys.stderr)
            return False

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        if not config_path or not os.path.exists(config_path):
            raise ConfigError("❌ 找不到 config.json 配置文件")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_config(self, config: Dict[str, Any]) -> bool:
        if not self.config_path:
            return False
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存配置失敗: {e}", file=sys.stderr)
            return False

    def validate_config(self) -> List[str]:
        """驗證 config.json 完整性，回傳錯誤訊息列表（空列表代表正常）"""
        errors   = []
        channels = self.config.get('channels', [])
        sched    = self.config.get('schedule', {})

        if not channels:
            errors.append("❌ 尚未設定任何通知頻道（channels）")
        else:
            for i, ch in enumerate(channels, 1):
                t   = ch.get('type', '').strip()
                tgt = ch.get('target', '').strip()
                if not t:
                    errors.append(f"❌ 頻道 {i} 缺少 type")
                elif t != 'console' and not tgt:
                    errors.append(f"❌ 頻道 {i}（{t}）缺少 target")

        if not sched.get('enabled', False):
            errors.append("❌ 排程尚未啟用（schedule.enabled）")
        if not sched.get('schedule_times', []):
            errors.append("❌ 缺少排程時間（schedule.schedule_times）")

        return errors

    # -------------------------------------------------------
    # 設定精靈：偵測可用頻道
    # -------------------------------------------------------

    def _detect_channels(self) -> List[Dict[str, Any]]:
        """從 openclaw.json 讀取已啟用的頻道（以 ALL_CHANNELS 為基準，排除 console）"""
        result = []
        path   = self._find_openclaw_config()
        if not path:
            return result
        try:
            with open(path, 'r', encoding='utf-8') as f:
                oc = json.load(f)
        except Exception:
            return result

        oc_channels = oc.get('channels', {})
        for ch_type, ch_name, ch_note in self.ALL_CHANNELS:
            if ch_type == 'console':
                continue
            if oc_channels.get(ch_type, {}).get('enabled', False):
                result.append({'type': ch_type, 'name': ch_name, 'note': ch_note})
        return result

    # -------------------------------------------------------
    # 設定精靈：步驟一 — 多頻道管理
    # -------------------------------------------------------

    ALL_CHANNELS = [
        ('telegram',   'Telegram',    '需要輸入 Chat ID'),
        ('discord',    'Discord',     '需要輸入 Webhook URL'),
        ('signal',     'Signal',      '需要輸入目標電話號碼'),
        ('whatsapp',   'WhatsApp',    '需要輸入目標電話號碼'),
        ('slack',      'Slack',       '需要輸入 Webhook URL'),
        ('imessage',   'iMessage',    '需要輸入聯絡人名稱'),
        ('irc',        'IRC',         '需要輸入頻道名稱'),
        ('googlechat', 'Google Chat', '需要輸入 Webhook URL'),
        ('console',    'Console',     '僅終端輸出，不發送訊息'),
    ]

    CH_PROMPTS = {
        'telegram':   "請輸入 Telegram Chat ID（例：123456789）",
        'discord':    "請輸入 Discord Webhook URL",
        'signal':     "請輸入 Signal 目標電話號碼",
        'whatsapp':   "請輸入 WhatsApp 目標電話號碼",
        'slack':      "請輸入 Slack Webhook URL",
        'imessage':   "請輸入 iMessage 聯絡人名稱",
        'irc':        "請輸入 IRC 頻道名稱",
        'googlechat': "請輸入 Google Chat Webhook URL",
    }

    def _ch_display_name(self, ch_type: str) -> str:
        return next((n for t, n, _ in self.ALL_CHANNELS if t == ch_type), ch_type.title())

    def _wizard_channels(self) -> List[Dict[str, str]]:
        """多頻道管理精靈（新增 / 移除），必須完成才能繼續"""
        channels: List[Dict[str, str]] = list(self.config.get('channels', []))

        while True:
            options: List[str] = []
            hints:   List[str] = []

            for ch in channels:
                name  = self._ch_display_name(ch['type'])
                tgt   = ch.get('target', '')
                label = f"[已加入] {name}" + (f"（{tgt}）" if tgt else "")
                options.append(label)
                hints.append("按 Enter 移除此頻道")

            add_idx  = len(options)
            done_idx = add_idx + 1

            options.append("➕  新增頻道")
            hints.append("加入新的通知頻道")

            options.append("✓   完成，繼續設定排程")
            hints.append("" if channels else "⚠ 請至少加入一個頻道")

            subtitle = (f"已加入 {len(channels)} 個頻道" if channels
                        else "尚未加入任何頻道，請先新增")

            idx = menu_select(
                title    = "📡  步驟 1／2   頻道管理",
                options  = options,
                hints    = hints,
                subtitle = subtitle
            )

            if idx == -1:           # Esc 忽略，留在當前畫面
                continue

            if idx == done_idx:
                if not channels:
                    print("\n  ⚠️  請至少加入一個頻道。")
                    continue
                return channels

            if idx == add_idx:
                new_ch = self._wizard_add_channel()
                if new_ch:
                    channels.append(new_ch)
                    name = self._ch_display_name(new_ch['type'])
                    print(f"\n  ✅ 已加入：{name}")
            else:
                removed = channels.pop(idx)
                print(f"\n  🗑  已移除：{self._ch_display_name(removed['type'])}")

    def _wizard_add_channel(self) -> Optional[Dict[str, str]]:
        """新增單一頻道子精靈"""
        # ALL_CHANNELS 範圍內已啟用的頻道
        detected_types = {ch['type'] for ch in self._detect_channels()}

        # 直接讀 openclaw.json 取得所有啟用頻道（含 ALL_CHANNELS 未涵蓋的新頻道）
        all_oc_enabled: Set[str] = set()
        oc_path = self._find_openclaw_config()
        if oc_path:
            try:
                with open(oc_path, 'r', encoding='utf-8') as f:
                    oc = json.load(f)
                for t, info in oc.get('channels', {}).items():
                    if info.get('enabled', False):
                        all_oc_enabled.add(t)
            except Exception:
                pass

        options:      List[str] = []
        hints:        List[str] = []
        channel_list: List[str] = []

        known_types = {ch_type for ch_type, _, _ in self.ALL_CHANNELS}

        # 已知頻道
        for ch_type, ch_name, ch_note in self.ALL_CHANNELS:
            label = f"{ch_name}（已啟用）" if ch_type in detected_types else ch_name
            options.append(label)
            hints.append(ch_note)
            channel_list.append(ch_type)

        # openclaw.json 裡有啟用、但不在已知清單的新頻道 → 動態加入
        for ch_type in sorted(all_oc_enabled - known_types):
            options.append(f"{ch_type.title()}（已啟用，透過 Gateway 發送）")
            hints.append("OpenClaw 新增頻道，自動使用 Gateway API")
            channel_list.append(ch_type)

        options.append("← 返回")
        hints.append("")

        idx = menu_select(
            title    = "📡  新增頻道   選擇類型",
            options  = options,
            hints    = hints,
            subtitle = "選擇要新增的頻道類型"
        )

        if idx == -1 or idx == len(options) - 1:
            return None

        channel_type = channel_list[idx]

        if channel_type == 'console':
            return {'type': 'console', 'target': ''}

        print(f"\n  {self.CH_PROMPTS.get(channel_type, f'請輸入 {channel_type.title()} 目標（Chat ID / 電話號碼 / Webhook URL 等）')}")
        while True:
            target = input("  > ").strip()
            if target:
                return {'type': channel_type, 'target': target}
            print("  ❌ 不能為空，請重新輸入。")

    # -------------------------------------------------------
    # 設定精靈：步驟二 — 排程設定（完全自訂）
    # -------------------------------------------------------

    DAYS_LABELS = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']
    DAYS_VALUES = [1, 2, 3, 4, 5, 6, 0]

    @staticmethod
    def _parse_time(raw: str) -> Optional[str]:
        """解析時間字串，支援 9、9:00、900、09:00 等格式，回傳 HH:MM 或 None"""
        raw = raw.strip().replace('：', ':').replace(' ', '')
        if re.match(r'^\d{1,2}:\d{2}$', raw):
            h, m = map(int, raw.split(':'))
        elif re.match(r'^\d{3,4}$', raw):
            n = int(raw)
            h, m = divmod(n, 100)
        elif re.match(r'^\d{1,2}$', raw):
            h, m = int(raw), 0
        else:
            return None
        if 0 <= h <= 23 and 0 <= m <= 59:
            return f"{h:02d}:{m:02d}"
        return None

    @staticmethod
    def _generate_times(start: str, end: str,
                        interval: int, unit: str) -> List[str]:
        """依起始、結束、間隔產生通知時間列表"""
        sh, sm = map(int, start.split(':'))
        eh, em = map(int, end.split(':'))
        start_min = sh * 60 + sm
        end_min   = eh * 60 + em
        step      = interval if unit == 'min' else interval * 60
        if step <= 0:
            return [start]
        times, t = [], start_min
        while t <= end_min:
            h, m = divmod(t, 60)
            if 0 <= h <= 23:
                times.append(f"{h:02d}:{m:02d}")
            t += step
        return times

    @staticmethod
    def _build_cron(schedule_times: List[str], days_of_week: List[int],
                    interval: int, unit: str) -> str:
        """產生 cron 表達式"""
        days_str = ','.join(str(d) for d in sorted(days_of_week))
        if unit == 'min':
            hours = sorted({int(t.split(':')[0]) for t in schedule_times})
            h_range = (f"{hours[0]}-{hours[-1]}" if len(hours) > 1
                       else str(hours[0])) if hours else '*'
            return f"*/{interval} {h_range} * * {days_str}"
        else:
            hours = sorted(int(t.split(':')[0]) for t in schedule_times)
            return f"0 {','.join(str(h) for h in hours)} * * {days_str}"

    def _wizard_schedule(self) -> Dict[str, Any]:
        # ── 1/3 選執行日期 ──────────────────────────────────
        while True:
            day_indices = menu_multiselect(
                title       = "⏰  步驟 2／2   排程設定  1/3  執行日期",
                options     = self.DAYS_LABELS,
                subtitle    = "Space 切換勾選，Enter 確認",
                preselected = [0, 1, 2, 3, 4]
            )
            if day_indices is None:  # Esc 忽略
                continue
            if not day_indices:
                print("\n  ⚠️  請至少選擇一天。")
                continue
            break

        # ── 2/3 輸入起始 / 結束時間 ─────────────────────────
        print("\n" + "=" * 52)
        print("  ⏰  排程設定  2/3  通知時段")
        print("=" * 52)

        while True:
            raw = input("\n  始於（例 09:00）：")
            start_time = self._parse_time(raw)
            if start_time:
                break
            print("  ❌ 格式錯誤，請重新輸入。")

        while True:
            raw = input("  結束（例 17:00）：")
            end_time = self._parse_time(raw)
            if not end_time:
                print("  ❌ 格式錯誤，請重新輸入。")
                continue
            if end_time < start_time:
                print(f"  ❌ 結束時間不可早於起始時間（{start_time}）。")
                continue
            break

        # ── 3/3 選間隔單位，再輸入數字 ──────────────────────
        while True:
            unit_idx = menu_select(
                title    = "⏰  排程設定  3/3  通知間隔",
                options  = ["小時", "分鐘"],
                hints    = ["每 N 小時通知一次", "每 N 分鐘通知一次"],
                subtitle = "選擇間隔單位"
            )
            if unit_idx != -1:
                break
        unit     = 'hour' if unit_idx == 0 else 'min'
        unit_str = '小時' if unit == 'hour' else '分鐘'

        while True:
            raw = input(f"\n  間隔（數字，單位：{unit_str}）：").strip()
            if raw.isdigit() and int(raw) > 0:
                interval = int(raw)
                break
            print("  ❌ 請輸入正整數。")

        # ── 組合結果 ────────────────────────────────────────
        days_of_week   = [self.DAYS_VALUES[i] for i in day_indices]
        schedule_times = self._generate_times(start_time, end_time, interval, unit)
        cron           = self._build_cron(schedule_times, days_of_week, interval, unit)

        day_names   = [self.DAYS_LABELS[i] for i in day_indices]
        description = (f"{'、'.join(day_names)}  "
                       f"{start_time}–{end_time}  每 {interval} {unit_str}")

        return {
            'enabled':        True,
            'days_of_week':   days_of_week,
            'start_time':     start_time,
            'end_time':       end_time,
            'interval_hours': interval if unit == 'hour' else round(interval / 60, 2),
            'schedule_times': schedule_times,
            'description':    description,
            'cron':           cron,
        }

    # -------------------------------------------------------
    # 設定精靈：主流程
    # -------------------------------------------------------

    def _run_setup_wizard(self) -> bool:
        print("\n" + "=" * 52)
        print("  ⚙️   大草原匯率計算器  —  初次設定")
        print("=" * 52)
        print("  完成兩個步驟即可開始使用：管理頻道 → 設定排程\n")

        # 步驟一：多頻道管理（必須完成）
        channels = self._wizard_channels()
        self.config['channels'] = channels
        ch_names = '、'.join(self._ch_display_name(ch['type']) for ch in channels)
        if self._save_config(self.config):
            print(f"\n  ✅ 頻道已設定：{ch_names}")
        else:
            print(f"\n  ⚠️  無法自動儲存，請手動編輯 config.json")
            for ch in channels:
                print(f"      {{type: {ch['type']}, target: {ch.get('target', '')}}}")

        # 步驟二：排程（必須完成）
        schedule = self._wizard_schedule()
        self.config['schedule'] = schedule
        if self._save_config(self.config):
            print(f"\n  ✅ 排程已設定：{schedule['description']}")
        else:
            print(f"\n  ⚠️  無法自動儲存排程，請手動編輯 config.json")

        # 將排程登記到 OpenClaw cron/jobs.json
        self._register_cron_job(schedule['cron'])

        # 測試訊息
        print()
        want_test = confirm(
            "🧪  設定完成！要發送一則測試訊息確認頻道正常嗎？"
        )
        if want_test:
            self._send_test_message()

        print("\n" + "=" * 52)
        print("  🎉  設定完成！")
        print("=" * 52)
        print(f"  📡 頻道：{ch_names}")
        print(f"  ⏰ 排程：{schedule['description']}")
        print(f"\n  排程通知請使用：python scripts/cny_rate.py --run")
        return True

    # -------------------------------------------------------
    # 測試訊息
    # -------------------------------------------------------

    def _send_test_message(self) -> bool:
        channels  = self.config.get('channels', [])
        sched     = self.config.get('schedule', {})
        ch_names  = '、'.join(self._ch_display_name(ch['type']) for ch in channels)

        msg = (
            "🦞 大草原匯率計算器 - 測試訊息\n\n"
            f"✅ 頻道設定：{ch_names}\n"
            f"✅ 排程設定：{sched.get('description', '已啟用')}\n\n"
            "這是一則測試訊息，確認設定正確。\n"
            "正式匯率通知將依照排程時間發送。\n\n"
            f"測試時間：{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}"
        )

        print(f"\n  📤 發送測試訊息到 {ch_names}...")
        ok = self.send_message(msg)
        if ok:
            print("  ✅ 測試訊息發送成功！")
        else:
            print("  ❌ 測試訊息發送失敗，請檢查設定。", file=sys.stderr)
        return ok

    # -------------------------------------------------------
    # 匯率抓取與計算
    # -------------------------------------------------------

    def fetch_rate(self) -> Optional[Tuple[float, float, str]]:
        """抓取台銀人民幣即期匯率，回傳 (買入, 賣出, 更新時間)"""
        try:
            resp = self.session.get(self.BOT_URL, timeout=30)
            resp.encoding = 'utf-8'
            html = resp.text

            time_match = re.search(r'牌價最新掛牌時間：(\d{4}/\d{2}/\d{2} \d{2}:\d{2})', html)
            update_time = (time_match.group(1) if time_match
                           else datetime.now().strftime("%Y/%m/%d %H:%M"))

            # 即期買入（group 3）、即期賣出（group 4）
            pattern = (
                r'人民幣 \(CNY\)[\s\S]*?'
                r'(\d+\.\d{3})[\s\S]*?'
                r'(\d+\.\d{3})[\s\S]*?'
                r'(\d+\.\d{3})[\s\S]*?'
                r'(\d+\.\d{3})'
            )
            m = re.search(pattern, html)
            if m:
                return float(m.group(3)), float(m.group(4)), update_time

            print("Error: Cannot parse CNY rate", file=sys.stderr)
            return None

        except requests.RequestException as e:
            print(f"Network error: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return None

    @staticmethod
    def round3(v: float) -> float:
        return round(v * 1000) / 1000

    def calculate(self, buy: float, sell: float) -> dict:
        mid    = self.round3((buy + sell) / 2)
        deltas = self.config.get('formula', {}).get('deltas', self.PRICE_DELTAS)
        labels = self.config.get('formula', {}).get('labels', self.PRICE_LABELS)
        return {
            'buy_rate':  buy,
            'sell_rate': sell,
            'prices': [
                {'label': lbl, 'price': self.round3(mid + d), 'delta': d}
                for d, lbl in zip(deltas, labels)
            ]
        }

    def format_output(self, results: dict, update_time: str) -> List[str]:
        m = re.search(r'(\d{4})/(\d{2})/(\d{2})', update_time)
        date_str = (f"{m.group(2)}.{m.group(3)}" if m
                    else datetime.now().strftime("%m.%d"))

        msg1 = (f"{date_str}即期匯率\n"
                f"台銀買入：{results['buy_rate']}\n"
                f"台銀賣出：{results['sell_rate']}")
        msg2 = '\n'.join(f"{p['label']}：{p['price']:.3f}" for p in results['prices'])
        msg3 = "LINE官方：\nhttps://bit.ly/47vlVrq\n\n台銀匯率：\nhttps://rate.bot.com.tw/xrt"
        return [msg1, msg2, msg3]

    # -------------------------------------------------------
    # 訊息發送
    # -------------------------------------------------------

    def send_message(self, message: str) -> bool:
        channels = self.config.get('channels', [])
        if not channels:
            print(message)
            return True
        all_ok = True
        for ch in channels:
            ok = self._send_to_channel(ch.get('type', 'console').strip(),
                                       ch.get('target', '').strip(),
                                       message)
            if not ok:
                all_ok = False
        return all_ok

    def _send_to_channel(self, t: str, tgt: str, message: str) -> bool:
        if t == 'console':
            print(message)
            return True
        elif t == 'telegram':
            return self._send_telegram(tgt, message)
        elif t == 'discord':
            return self._send_discord(tgt, message)
        elif t in ('slack', 'googlechat', 'webhook'):
            return self._send_webhook(tgt, message)
        elif t in ('signal', 'whatsapp', 'imessage', 'irc'):
            return self._send_via_gateway(t, tgt, message)
        else:
            # 未知頻道類型 → 嘗試透過 OpenClaw Gateway 發送
            print(f"  ℹ️  未知頻道 [{t}]，嘗試透過 Gateway 發送...")
            return self._send_via_gateway(t, tgt, message)

    def _send_telegram(self, chat_id: str, message: str) -> bool:
        token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        if not token:
            path = self._find_openclaw_config()
            if path:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        oc = json.load(f)
                    token = oc.get('channels', {}).get('telegram', {}).get('botToken', '')
                except Exception:
                    pass
        if not token:
            print("❌ 缺少 TELEGRAM_BOT_TOKEN", file=sys.stderr)
            return False
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={'chat_id': chat_id, 'text': message},
                timeout=30
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"❌ Telegram 發送失敗：{e}", file=sys.stderr)
            return False

    def _send_discord(self, webhook_url: str, message: str) -> bool:
        try:
            resp = requests.post(webhook_url, json={'content': message}, timeout=30)
            return resp.status_code == 204
        except Exception as e:
            print(f"❌ Discord 發送失敗：{e}", file=sys.stderr)
            return False

    def _send_webhook(self, url: str, message: str) -> bool:
        try:
            resp = requests.post(url, json={'text': message, 'message': message}, timeout=30)
            return resp.status_code in (200, 201, 204)
        except Exception as e:
            print(f"❌ Webhook 發送失敗：{e}", file=sys.stderr)
            return False

    def _send_via_gateway(self, channel_type: str, target: str, message: str) -> bool:
        gateway_url   = os.environ.get('OPENCLAW_GATEWAY_URL', '')
        gateway_token = os.environ.get('OPENCLAW_GATEWAY_TOKEN', '')

        if not gateway_url or not gateway_token:
            path = self._find_openclaw_config()
            if path:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        oc = json.load(f)
                    gw   = oc.get('gateway', {})
                    port = gw.get('port', 18790)
                    bind = gw.get('bind', 'loopback')
                    host = '127.0.0.1' if bind in ('loopback', 'localhost') else '0.0.0.0'
                    gateway_url   = gateway_url   or f"http://{host}:{port}"
                    gateway_token = gateway_token or gw.get('auth', {}).get('token', '')
                except Exception:
                    pass

        if not gateway_token:
            print(f"❌ 缺少 OPENCLAW_GATEWAY_TOKEN，無法發送 {channel_type}", file=sys.stderr)
            return False

        gateway_url = gateway_url or "http://127.0.0.1:18790"
        try:
            resp = requests.post(
                f"{gateway_url.rstrip('/')}/v1/messages/send",
                json={'channel': channel_type, 'to': target, 'text': message},
                headers={'Authorization': f'Bearer {gateway_token}'},
                timeout=30
            )
            if resp.status_code in (200, 201):
                return True
            print(f"❌ Gateway 回應 {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"❌ Gateway 發送失敗：{e}", file=sys.stderr)
            return False

    # -------------------------------------------------------
    # 新頻道偵測
    # -------------------------------------------------------

    def _check_new_channels(self) -> None:
        """比對 openclaw.json 與目前設定，若有新啟用頻道則發通知提醒"""
        detected   = self._detect_channels()
        configured = {ch['type'] for ch in self.config.get('channels', [])}

        new_channels = [ch for ch in detected if ch['type'] not in configured]
        if not new_channels:
            return

        channel_lines = '\n'.join(
            f"{i+1}. {ch['name']}" for i, ch in enumerate(new_channels)
        )
        alert = (
            f"📡 偵測到新啟用頻道\n\n"
            f"以下頻道可加入匯率通知清單：\n"
            f"{channel_lines}\n\n"
            f"回覆頻道名稱或編號即可加入\n"
            f"（例：Discord 或 1）\n"
            f"回覆「略過」忽略此提示"
        )
        names = '、'.join(ch['name'] for ch in new_channels)
        print(f"\n  ⚠️  偵測到新頻道：{names}（尚未加入通知清單）")
        self.send_message(alert)

    # -------------------------------------------------------
    # 排程執行主流程
    # -------------------------------------------------------

    def run_scheduled(self) -> bool:
        errors = self.validate_config()
        if errors:
            for e in errors:
                print(e, file=sys.stderr)
            return False

        channels = self.config.get('channels', [])
        sched    = self.config.get('schedule', {})
        ch_names = '、'.join(self._ch_display_name(ch['type']) for ch in channels)
        print(f"  📡 頻道：{ch_names}   ⏰ 排程：{sched.get('description','')}\n")

        self._check_new_channels()

        print("  📡 抓取台銀即期匯率中...")
        result = self.fetch_rate()
        if not result:
            print("  ❌ 無法取得匯率，請稍後再試。", file=sys.stderr)
            return False

        buy, sell, update_time = result
        print(f"  ✅ {update_time}  買入 {buy}  賣出 {sell}")

        calculated = self.calculate(buy, sell)
        messages   = self.format_output(calculated, update_time)

        print(f"\n  📤 發送 {len(messages)} 則通知...")
        all_ok = True
        for i, msg in enumerate(messages, 1):
            ok = self.send_message(msg)
            print(f"  {'✅' if ok else '❌'} 訊息 {i}/{len(messages)}")
            if not ok:
                all_ok = False

        print(f"\n  {'✅ 全部發送完成。' if all_ok else '⚠️  部分訊息發送失敗。'}")
        return all_ok

    # -------------------------------------------------------
    # 頻道管理 CLI（供 OpenClaw agent 呼叫）
    # -------------------------------------------------------

    def list_channels_json(self) -> None:
        """輸出目前設定與可用頻道的 JSON，供 agent 讀取"""
        configured     = self.config.get('channels', [])
        configured_set = {ch['type'] for ch in configured}
        detected       = self._detect_channels()
        available      = [
            {'type': ch['type'], 'name': ch['name']}
            for ch in detected if ch['type'] not in configured_set
        ]
        print(json.dumps({
            'configured': configured,
            'available':  available,
        }, ensure_ascii=False, indent=2))

    def add_channel(self, ch_type: str, target: str) -> bool:
        """新增一個頻道到通知清單"""
        channels = list(self.config.get('channels', []))
        for ch in channels:
            if ch['type'] == ch_type and ch.get('target', '') == target:
                print(f"⚠️  頻道已存在：{ch_type}（{target}）")
                return False
        channels.append({'type': ch_type, 'target': target})
        self.config['channels'] = channels
        if self._save_config(self.config):
            name = self._ch_display_name(ch_type)
            print(f"✅ 已加入頻道：{name}（{target}）")
            return True
        return False

    def remove_channel(self, ch_type: str, target: str = '') -> bool:
        """從通知清單移除頻道（type 相符即移除，若有 target 則精確比對）"""
        channels = list(self.config.get('channels', []))
        before   = len(channels)
        if target:
            channels = [ch for ch in channels
                        if not (ch['type'] == ch_type and ch.get('target', '') == target)]
        else:
            channels = [ch for ch in channels if ch['type'] != ch_type]
        if len(channels) == before:
            print(f"⚠️  找不到頻道：{ch_type}" + (f"（{target}）" if target else ""))
            return False
        self.config['channels'] = channels
        if self._save_config(self.config):
            name = self._ch_display_name(ch_type)
            print(f"✅ 已移除頻道：{name}" + (f"（{target}）" if target else ""))
            return True
        return False

    # -------------------------------------------------------
    # 自動套用基本設定（不需互動）
    # -------------------------------------------------------

    def auto_setup(self) -> bool:
        """自動套用基本設定：偵測第一個可用頻道 + 預設排程，不需互動"""
        detected = self._detect_channels()
        if not detected:
            print("❌ 找不到任何已啟用的 OpenClaw 頻道，無法自動設定。", file=sys.stderr)
            return False

        first = detected[0]
        ch_type = first['type']

        # 需要 target 的頻道，從 openclaw.json 自動取得
        target = ''
        if ch_type != 'console':
            oc_path = self._find_openclaw_config()
            if oc_path:
                try:
                    with open(oc_path, 'r', encoding='utf-8') as f:
                        oc = json.load(f)
                    ch_cfg = oc.get('channels', {}).get(ch_type, {})
                    # Telegram 取 allowFrom 第一筆作為 chat_id
                    if ch_type == 'telegram':
                        allow = ch_cfg.get('allowFrom', [])
                        target = allow[0] if allow else ''
                    else:
                        target = ch_cfg.get('webhookUrl', ch_cfg.get('url', ''))
                except Exception:
                    pass

        if not target and ch_type != 'console':
            print(f"⚠️  無法自動取得 {ch_type} 的 target，請手動執行設定精靈。", file=sys.stderr)
            return False

        self.config['channels'] = [{'type': ch_type, 'target': target}]
        self.config['schedule'] = self.DEFAULT_SCHEDULE.copy()

        if not self._save_config(self.config):
            print("❌ 無法儲存自動設定。", file=sys.stderr)
            return False

        self._register_cron_job(self.DEFAULT_SCHEDULE['cron'])

        name = self._ch_display_name(ch_type)
        print(f"✅ 已自動套用基本設定")
        print(f"   頻道：{name}（{target}）")
        print(f"   排程：{self.DEFAULT_SCHEDULE['description']}")
        print(f"   如需調整，請執行：python scripts/cny_rate.py")
        return True

    # -------------------------------------------------------
    # 主入口
    # -------------------------------------------------------

    def run(self) -> bool:
        print("=" * 52)
        print("  🦞  大草原匯率計算器")
        print("=" * 52)

        return self._run_setup_wizard()


# =========================================================
# CLI 入口
# =========================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='大草原匯率計算器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "使用範例:\n"
            "  python scripts/cny_rate.py                          # 互動式設定精靈\n"
            "  python scripts/cny_rate.py --auto-setup             # 自動套用基本設定\n"
            "  python scripts/cny_rate.py --run                    # 執行排程通知\n"
            "  python scripts/cny_rate.py --list-channels          # 列出頻道狀態（JSON）\n"
            "  python scripts/cny_rate.py --add-channel telegram 123456789\n"
            "  python scripts/cny_rate.py --remove-channel telegram\n"
            "  python scripts/cny_rate.py --remove-channel telegram 123456789\n"
        )
    )
    parser.add_argument('--config',         '-c', help='指定 config.json 路徑')
    parser.add_argument('--run',            '-r', action='store_true', help='執行排程通知（跳過設定精靈）')
    parser.add_argument('--auto-setup',           action='store_true', help='自動套用基本設定（第一個可用頻道 + 預設排程）')
    parser.add_argument('--list-channels',        action='store_true', help='列出頻道狀態（JSON 輸出）')
    parser.add_argument('--add-channel',          nargs=2, metavar=('TYPE', 'TARGET'), help='新增頻道')
    parser.add_argument('--remove-channel',       nargs='+', metavar=('TYPE', 'TARGET'), help='移除頻道')
    args = parser.parse_args()

    try:
        calc = CNYRateCalculator(args.config)

        if args.auto_setup:
            sys.exit(0 if calc.auto_setup() else 1)

        if args.list_channels:
            calc.list_channels_json()
            sys.exit(0)

        if args.add_channel:
            sys.exit(0 if calc.add_channel(args.add_channel[0], args.add_channel[1]) else 1)

        if args.remove_channel:
            ch_type  = args.remove_channel[0]
            target   = args.remove_channel[1] if len(args.remove_channel) > 1 else ''
            sys.exit(0 if calc.remove_channel(ch_type, target) else 1)

        if args.run:
            print("=" * 52)
            print("  🦞  大草原匯率計算器")
            print("=" * 52)
            sys.exit(0 if calc.run_scheduled() else 1)

        sys.exit(0 if calc.run() else 1)

    except ConfigError as e:
        print(f"\n{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        print(f"\n❌ 發生錯誤：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
