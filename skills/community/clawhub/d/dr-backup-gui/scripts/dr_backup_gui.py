#!/usr/bin/env python3
"""
DR Backup GUI — Unified disaster recovery & migration tool
Combines: Velero + Rclone + Rsync + Coriolis
Requires: Python 3.9+, PyQt6
"""

import json
import subprocess
import threading
import os
import sys
import datetime
import shutil
import re
from pathlib import Path
from typing import Optional

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFormLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QStatusBar, QMenuBar,
    QMenu, QMessageBox, QFileDialog, QDialog, QScrollArea, QFrame,
    QSizePolicy, QStyledItemDelegate, QListWidget, QListWidgetItem,
    QAbstractItemView, QToolBar, QDialogButtonBox, QTabWidget,
    QSplitter, QListView, QCalendarWidget, QDateTimeEdit, QPlainTextEdit,
)
from PyQt6.QtCore import (
    Qt, QTimer, QProcess, QThread, pyqtSignal, QObject, QSize,
    QDateTime, QMutex, QMutexLocker,
)
from PyQt6.QtGui import (
    QAction, QIcon, QFont, QPalette, QColor, QTextCursor,
    QStandardItemModel, QStandardItem,
)

# ── Config dir ─────────────────────────────────────────────────────────────────
CONFIG_DIR = Path.home() / ".dr_backup_gui"
CONFIG_DIR.mkdir(exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"
PROFILES_FILE = CONFIG_DIR / "profiles.json"
JOBS_FILE = CONFIG_DIR / "jobs.json"
LOG_FILE = CONFIG_DIR / "activity.log"


# ── Utilities ──────────────────────────────────────────────────────────────────
def log(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def check_tool(name: str) -> bool:
    return shutil.which(name) is not None


def run_async(cmd: list, on_done, on_err=None, cwd=None, env=None):
    """Run a command asynchronously, call on_done(str_output) when done."""
    def worker():
        try:
            env = env or os.environ.copy()
            p = subprocess.run(
                cmd, capture_output=True, text=True, cwd=cwd, env=env,
                timeout=3600,
            )
            out = (p.stdout or "") + (p.stderr or "")
            on_done(out, p.returncode)
        except subprocess.TimeoutExpired:
            on_done("TIMEOUT after 1 hour", -1)
        except Exception as e:
            if on_err:
                on_err(str(e))
            else:
                on_done(str(e), -1)

    t = threading.Thread(target=worker, daemon=True)
    t.start()


# ── Signal hub for log output ──────────────────────────────────────────────────
class LogEmitter(QObject):
    sig = pyqtSignal(str, str)  # (tool_name, message)

_log_emitter = LogEmitter()


# ══════════════════════════════════════════════════════════════════════════════
# TOOL BACKENDS
# ══════════════════════════════════════════════════════════════════════════════

class VeleroBackend:
    """Velero Kubernetes backup/restore."""

    def __init__(self):
        self.available = check_tool("velero")

    def discover_clusters(self):
        try:
            result = subprocess.run(
                ["kubectl", "config", "get-contexts", "-o", "name"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                return [c.strip() for c in result.stdout.strip().split("\n") if c.strip()]
        except Exception:
            pass
        return []

    def backup(self, name: str, context: str, namespaces: list, ttl: str,
               include_resources: list, exclude_resources: list,
               snapshot_volumes: bool, on_done, on_err):
        cmd = ["velero", "backup", "create", name]
        if context:
            cmd += ["--context", context]
        if namespaces:
            cmd += ["--include-namespaces", ",".join(namespaces)]
        if include_resources:
            cmd += ["--include-resources", ",".join(include_resources)]
        if exclude_resources:
            cmd += ["--exclude-resources", ",".join(exclude_resources)]
        if not snapshot_volumes:
            cmd += ["--snapshot-volumes=false"]
        cmd += ["--ttl", ttl]
        log(f"[Velero] Starting backup: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)

    def restore(self, backup_name: str, context: str, namespace_mapping: dict,
                include_namespaces: list, on_done, on_err):
        cmd = ["velero", "restore", "create", f"restore-{backup_name}-{datetime.date.today()}"]
        if context:
            cmd += ["--context", context]
        if namespace_mapping:
            for src, dst in namespace_mapping.items():
                cmd += ["--namespace-mappings", f"{src}:{dst}"]
        if include_namespaces:
            cmd += ["--include-namespaces", ",".join(include_namespaces)]
        cmd += ["--from-backup", backup_name]
        log(f"[Velero] Starting restore: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)

    def list_backups(self, context: str, on_done, on_err):
        cmd = ["velero", "backup", "get"]
        if context:
            cmd += ["--context", context]
        run_async(cmd, on_done=on_done, on_err=on_err)

    def schedule_backup(self, name: str, context: str, namespaces: list,
                        schedule: str, ttl: str, on_done, on_err):
        cmd = ["velero", "schedule", "create", name, "--schedule", schedule]
        if context:
            cmd += ["--context", context]
        if namespaces:
            cmd += ["--include-namespaces", ",".join(namespaces)]
        cmd += ["--ttl", ttl]
        log(f"[Velero] Creating schedule: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)


class RcloneBackend:
    """Rclone cloud storage sync."""

    def __init__(self):
        self.available = check_tool("rclone")

    def list_remotes(self):
        try:
            result = subprocess.run(
                ["rclone", "listremotes"], capture_output=True, text=True,
            )
            if result.returncode == 0:
                return [r.strip().rstrip(":") for r in result.stdout.strip().split("\n") if r.strip()]
        except Exception:
            pass
        return []

    def sync(self, source: str, dest: str, mode: str, filters: list,
             dry_run: bool, on_done, on_err):
        cmd = ["rclone", "sync", source, dest]
        if mode.startswith("复制"):
            cmd = ["rclone", "copy", source, dest]
        elif mode.startswith("检查"):
            cmd = ["rclone", "check", source, dest]
            dry_run = False
        if dry_run:
            cmd += ["--dry-run"]
        if filters:
            for f in filters:
                if f.startswith("exclude:"):
                    cmd += ["--exclude", f.replace("exclude:", "")]
                elif f.startswith("include:"):
                    cmd += ["--include", f.replace("include:", "")]
        cmd += ["--progress", "--stats", "1s"]
        log(f"[Rclone] Sync: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)

    def copy(self, source: str, dest: str, dry_run: bool, on_done, on_err):
        cmd = ["rclone", "copy", source, dest]
        if dry_run:
            cmd += ["--dry-run"]
        cmd += ["--progress"]
        log(f"[Rclone] Copy: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)

    def bandwidth_limit(self, limit: str, on_done, on_err):
        return on_done(f"Bandwidth limit set to {limit} (not persisted in this session)", 0)


class RsyncBackend:
    """Rsync file-level sync."""

    def __init__(self):
        self.available = check_tool("rsync")

    def sync(self, source: str, dest: str, options: dict, dry_run: bool,
             on_done, on_err):
        cmd = ["rsync"]
        if options.get("archive"):
            cmd += ["-a"]
        if options.get("compress"):
            cmd += ["-z"]
        if options.get("verbose"):
            cmd += ["-v"]
        if options.get("progress"):
            cmd += ["--progress"]
        if options.get("delete"):
            cmd += ["--delete"]
        if options.get("checksum"):
            cmd += ["--checksum"]
        if options.get("bwlimit"):
            cmd += ["--bwlimit", str(options["bwlimit"])]
        if options.get("exclude"):
            for ex in options["exclude"].split(","):
                cmd += ["--exclude", ex.strip()]
        if options.get("include"):
            for inc in options["include"].split(","):
                cmd += ["--include", inc.strip()]
        ssh_port = options.get("ssh_port", 22)
        ssh_key = options.get("ssh_key", "")
        ssh_user = options.get("ssh_user", "")
        if ssh_port != 22:
            cmd += ["-e", f"ssh -p {ssh_port}"]
        if ssh_key:
            cmd += ["-e", f"ssh -i {ssh_key}"]
        if ssh_user and "@" not in dest:
            # prepend user if not already in path
            dest = f"{ssh_user}@{dest}"
        if dry_run:
            cmd += ["--dry-run"]
        cmd += [source, dest]
        if options.get("delete"):
            log(f"[Rsync] ⚠️  注意: --delete 已启用，目标目录中与源不一致的文件将被删除！")
        log(f"[Rsync] Sync: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)


class CoriolisBackend:
    """Coriolis cloud migration (replica & migration workflows)."""

    def __init__(self):
        self.available = check_tool("coriolis")
        self.endpoint = "http://localhost:8077"  # default

    def list_endpoints(self, on_done, on_err):
        cmd = ["coriolis", "endpoint", "list", "--format", "json"]
        run_async(cmd, on_done=on_done, on_err=on_err)

    def list_minions_pools(self, on_done, on_err):
        cmd = ["coriolis", "minion-pool", "list", "--format", "json"]
        run_async(cmd, on_done=on_done, on_err=on_err)

    def migrate(self, source_endpoint: str, dest_endpoint: str, vm_ids: list,
                minion_pool: str, on_done, on_err):
        cmd = ["coriolis", "migration", "create",
               "--source-endpoint", source_endpoint,
               "--destination-endpoint", dest_endpoint,
               "--vm", vm_ids[0] if vm_ids else ""]
        if minion_pool:
            cmd += ["--minion-pool", minion_pool]
        cmd += ["--output", "json"]
        log(f"[Coriolis] Migration: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)

    def replica(self, source_endpoint: str, dest_endpoint: str, vm_ids: list,
                on_done, on_err):
        cmd = ["coriolis", "replica", "create",
               "--source-endpoint", source_endpoint,
               "--destination-endpoint", dest_endpoint,
               "--vm", vm_ids[0] if vm_ids else ""]
        cmd += ["--output", "json"]
        log(f"[Coriolis] Replica: {' '.join(cmd)}")
        run_async(cmd, on_done=on_done, on_err=on_err)

    def list_migrations(self, on_done, on_err):
        cmd = ["coriolis", "migration", "list", "--format", "json"]
        run_async(cmd, on_done=on_done, on_err=on_err)


# ══════════════════════════════════════════════════════════════════════════════
# CONFIG MANAGER
# ══════════════════════════════════════════════════════════════════════════════

class ConfigManager:
    """Persists profiles and jobs to JSON files."""

    def __init__(self):
        self.config = self._load(CONFIG_FILE, {})
        self.profiles = self._load(PROFILES_FILE, {
            "velero": {},
            "rclone": {},
            "rsync": {},
            "coriolis": {},
        })
        self.jobs = self._load(JOBS_FILE, [])

    def _load(self, path: Path, default):
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return default
        return default

    def save(self):
        CONFIG_FILE.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")
        PROFILES_FILE.write_text(json.dumps(self.profiles, indent=2, ensure_ascii=False), encoding="utf-8")
        JOBS_FILE.write_text(json.dumps(self.jobs, indent=2, ensure_ascii=False), encoding="utf-8")

    def save_profile(self, tool: str, name: str, data: dict):
        self.profiles.setdefault(tool, {})[name] = data
        self.save()

    def get_profile(self, tool: str, name: str):
        return self.profiles.get(tool, {}).get(name, {})

    def list_profiles(self, tool: str):
        return list(self.profiles.get(tool, {}).keys())

    def delete_profile(self, tool: str, name: str):
        if name in self.profiles.get(tool, {}):
            del self.profiles[tool][name]
            self.save()

    def save_job(self, job: dict):
        if job.get("id") is None:
            job["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.jobs = [j for j in self.jobs if j.get("id") != job.get("id")]
        self.jobs.append(job)
        self.save()
        return job

    def delete_job(self, job_id: str):
        self.jobs = [j for j in self.jobs if j.get("id") != job_id]
        self.save()


# ══════════════════════════════════════════════════════════════════════════════
# STYLE HELPERS
# ══════════════════════════════════════════════════════════════════════════════

class Colors:
    BG = "#1e1e2e"
    SURFACE = "#2a2a3e"
    SURFACE2 = "#363650"
    BORDER = "#4a4a70"
    TEXT = "#cdd6f4"
    SUBTEXT = "#a6adc8"
    ACCENT = "#89b4fa"
    GREEN = "#a6e3a1"
    RED = "#f38ba8"
    YELLOW = "#f9e2af"
    BLUE = "#89b4fa"
    PURPLE = "#cba6f7"


def apply_dark_theme(app: QApplication):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(Colors.BG))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Colors.TEXT))
    palette.setColor(QPalette.ColorRole.Base, QColor(Colors.SURFACE))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Colors.SURFACE2))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(Colors.SURFACE))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(Colors.TEXT))
    palette.setColor(QPalette.ColorRole.Text, QColor(Colors.TEXT))
    palette.setColor(QPalette.ColorRole.Button, QColor(Colors.SURFACE2))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Colors.TEXT))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(Colors.RED))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Colors.ACCENT))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Colors.BG))
    app.setPalette(palette)
    app.setStyleSheet(f"""
        QWidget {{ background-color: {Colors.BG}; color: {Colors.TEXT}; font-size: 13px; }}
        QTabWidget::pane {{ border: 1px solid {Colors.BORDER}; background: {Colors.SURFACE}; }}
        QTabBar::tab {{ background: {Colors.SURFACE2}; color: {Colors.SUBTEXT}; padding: 8px 16px; margin-right: 2px; border-radius: 4px 4px 0 0; }}
        QTabBar::tab:selected {{ background: {Colors.SURFACE}; color: {Colors.ACCENT}; font-weight: bold; }}
        QPushButton {{ background: {Colors.SURFACE2}; color: {Colors.TEXT}; border: 1px solid {Colors.BORDER}; padding: 6px 16px; border-radius: 4px; }}
        QPushButton:hover {{ background: {Colors.BORDER}; }}
        QPushButton:pressed {{ background: {Colors.ACCENT}; color: {Colors.BG}; }}
        QPushButton:disabled {{ opacity: 0.4; }}
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit, QPlainTextEdit {{
            background: {Colors.SURFACE}; color: {Colors.TEXT}; border: 1px solid {Colors.BORDER};
            border-radius: 4px; padding: 4px 8px;
        }}
        QComboBox QAbstractItemView {{ background: {Colors.SURFACE}; color: {Colors.TEXT}; selection-background-color: {Colors.ACCENT}; }}
        QGroupBox {{ border: 1px solid {Colors.BORDER}; border-radius: 6px; margin-top: 8px; padding-top: 12px; font-weight: bold; color: {Colors.ACCENT}; }}
        QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top left; padding: 0 6px; color: {Colors.ACCENT}; }}
        QTableWidget, QListWidget {{ background: {Colors.SURFACE}; color: {Colors.TEXT}; border: 1px solid {Colors.BORDER}; border-radius: 4px; gridline-color: {Colors.BORDER}; }}
        QHeaderView::section {{ background: {Colors.SURFACE2}; color: {Colors.TEXT}; border: none; border-right: 1px solid {Colors.BORDER}; border-bottom: 1px solid {Colors.BORDER}; padding: 4px; }}
        QProgressBar {{ border: 1px solid {Colors.BORDER}; border-radius: 4px; text-align: center; background: {Colors.SURFACE}; color: {Colors.TEXT}; }}
        QProgressBar::chunk {{ background: {Colors.ACCENT}; border-radius: 3px; }}
        QStatusBar {{ background: {Colors.SURFACE2}; color: {Colors.SUBTEXT}; border-top: 1px solid {Colors.BORDER}; }}
        QMenuBar {{ background: {Colors.SURFACE2}; color: {Colors.TEXT}; border-bottom: 1px solid {Colors.BORDER}; }}
        QMenuBar::item:selected {{ background: {Colors.ACCENT}; color: {Colors.BG}; }}
        QMenu {{ background: {Colors.SURFACE}; color: {Colors.TEXT}; border: 1px solid {Colors.BORDER}; }}
        QMenu::item:selected {{ background: {Colors.ACCENT}; color: {Colors.BG}; }}
        QToolBar {{ background: {Colors.SURFACE2}; border: none; spacing: 6px; padding: 4px; }}
        QLabel {{ color: {Colors.TEXT}; }}
        QCheckBox {{ color: {Colors.TEXT}; spacing: 6px; }}
        QCheckBox::indicator {{ width: 16px; height: 16px; border: 1px solid {Colors.BORDER}; border-radius: 3px; background: {Colors.SURFACE}; }}
        QCheckBox::indicator:checked {{ background: {Colors.ACCENT}; }}
        QScrollBar:vertical {{ background: {Colors.SURFACE}; width: 10px; border-radius: 5px; }}
        QScrollBar::handle:vertical {{ background: {Colors.BORDER}; border-radius: 5px; min-height: 20px; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QScrollBar:horizontal {{ background: {Colors.SURFACE}; height: 10px; border-radius: 5px; }}
        QScrollBar::handle:horizontal {{ background: {Colors.BORDER}; border-radius: 5px; min-width: 20px; }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
    """)


def card(parent, title: str = "") -> QGroupBox:
    """Create a styled card/groupbox."""
    g = QGroupBox(title, parent)
    g.setStyleSheet(f"""
        QGroupBox {{ border: 1px solid {Colors.BORDER}; border-radius: 8px;
                     margin-top: 10px; padding: 14px 10px 10px; background: {Colors.SURFACE}; }}
        QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px;
                           color: {Colors.ACCENT}; font-size: 13px; font-weight: bold; }}
    """)
    return g


def row(*widgets, stretch=False) -> QHBoxLayout:
    h = QHBoxLayout()
    for w in widgets:
        h.addWidget(w)
        if stretch and w in widgets[:-1]:
            h.addStretch()
    return h


def col(*widgets, stretch=False) -> QVBoxLayout:
    v = QVBoxLayout()
    for w in widgets:
        v.addWidget(w)
        if stretch and w in widgets[:-1]:
            v.addStretch()
    return v


def label(text: str, parent=None, color: str = Colors.TEXT) -> QLabel:
    lbl = QLabel(text, parent)
    lbl.setStyleSheet(f"color: {color}; font-size: 13px;")
    return lbl


def btn(text: str, parent=None, icon: str = "", tooltip: str = "") -> QPushButton:
    b = QPushButton(text, parent)
    if icon:
        b.setIcon(QIcon(icon))
    if tooltip:
        b.setToolTip(tooltip)
    return b


def line(parent=None, placeholder: str = "") -> QLineEdit:
    e = QLineEdit(parent)
    if placeholder:
        e.setPlaceholderText(placeholder)
    return e


def log_view(parent=None) -> QTextEdit:
    t = QTextEdit(parent)
    t.setReadOnly(True)
    t.setMaximumBlockCount(10000)
    return t


# ══════════════════════════════════════════════════════════════════════════════
# TOOL PANELS
# ══════════════════════════════════════════════════════════════════════════════

class ToolStatusBanner(QFrame):
    """Top banner showing which tools are installed."""

    def __init__(self, backends: dict, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(36)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        layout.addWidget(QLabel("🔧 工具状态:"))
        for tool, be in backends.items():
            status = "✅ 已安装" if be.available else "❌ 未安装"
            color = Colors.GREEN if be.available else Colors.RED
            lbl = QLabel(f"{tool}: {status}")
            lbl.setStyleSheet(f"color: {color}; font-weight: bold; padding: 2px 8px; "
                              f"background: {Colors.SURFACE2}; border-radius: 4px;")
            layout.addWidget(lbl)
        layout.addStretch()
        self.setStyleSheet(f"background: {Colors.SURFACE2}; border-bottom: 1px solid {Colors.BORDER};")


class VeleroPanel(QWidget):
    def __init__(self, backend: VeleroBackend, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self.be = backend
        self.cfg = cfg
        self._build_ui()
        self._refresh_clusters()

    def _build_ui(self):
        vl = QVBoxLayout(self)
        vl.setContentsMargins(12, 12, 12, 12)
        vl.setSpacing(10)

        # ── Toolbar ────────────────────────────────────────────────────────────
        toolbar = QHBoxLayout()
        self.btn_backup = btn("▶ 执行备份", tooltip="创建新备份")
        self.btn_restore = btn("↩ 恢复", tooltip="从备份恢复")
        self.btn_schedule = btn("⏰ 定时备份", tooltip="创建定时备份计划")
        self.btn_list = btn("📋 查看备份", tooltip="列出所有备份")
        self.btn_refresh = btn("🔄 刷新")
        for b in [self.btn_backup, self.btn_restore, self.btn_schedule,
                  self.btn_list, self.btn_refresh]:
            toolbar.addWidget(b)
        toolbar.addStretch()
        vl.addLayout(toolbar)

        # ── Form ───────────────────────────────────────────────────────────────
        sw = QScrollArea()
        sw.setWidgetResizable(True)
        sw.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")
        cont = QWidget()
        fl = QFormLayout(cont)
        fl.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        fl.setSpacing(10)

        # Profile selector
        prof_h = QHBoxLayout()
        self.prof_combo = QComboBox()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("velero"))
        self.btn_save_prof = btn("💾 保存配置")
        self.btn_load_prof = btn("📂 加载配置")
        self.btn_del_prof = btn("🗑 删除")
        prof_h.addWidget(self.prof_combo)
        prof_h.addWidget(self.btn_load_prof)
        prof_h.addWidget(self.btn_save_prof)
        prof_h.addWidget(self.btn_del_prof)
        fl.addRow("配置档案:", prof_h)

        # Cluster context
        self.ctx_combo = QComboBox()
        self.ctx_combo.setMinimumWidth(200)
        fl.addRow("集群上下文:", self.ctx_combo)

        # Backup name
        self.backup_name = line()
        self.backup_name.setPlaceholderText("backup-2024-01-01")
        fl.addRow("备份名称:", self.backup_name)

        # Namespaces
        ns_h = QHBoxLayout()
        self.ns_edit = line()
        self.ns_edit.setPlaceholderText("default,kube-system (留空=全部)")
        self.select_ns_btn = btn("选择...")
        ns_h.addWidget(self.ns_edit)
        ns_h.addWidget(self.select_ns_btn)
        fl.addRow("命名空间:", ns_h)

        # TTL
        self.ttl_combo = QComboBox()
        self.ttl_combo.addItems(["720h (30天)", "2160h (90天)", "168h (7天)", "48h (2天)", "24h (1天)"])
        fl.addRow("保留时间 (TTL):", self.ttl_combo)

        # Resources
        self.include_res = line()
        self.include_res.setPlaceholderText("deployments,services (留空=全部)")
        fl.addRow("包含资源:", self.include_res)

        self.exclude_res = line()
        self.exclude_res.setPlaceholderText("events,limitranges (留空=不排除)")
        fl.addRow("排除资源:", self.exclude_res)

        # Snapshot
        self.snap_cbox = QCheckBox("快照持久卷 (PVC)")
        self.snap_cbox.setChecked(True)
        fl.addRow("", self.snap_cbox)

        # Schedule
        self.schedule_expr = line()
        self.schedule_expr.setPlaceholderText("@every 6h  或  0 2 * * *")
        fl.addRow("定时表达式:", self.schedule_expr)

        # Namespace mapping (restore)
        self.ns_map = line()
        self.ns_map.setPlaceholderText("old-ns:new-ns, app-ns:prod-ns")
        fl.addRow("命名空间映射:", self.ns_map)

        sw.setWidget(cont)
        vl.addWidget(sw)

        # ── Output log ─────────────────────────────────────────────────────────
        log_gb = card(self, "📤 执行日志")
        log_layout = QVBoxLayout(log_gb)
        self.log_text = log_view()
        log_layout.addWidget(self.log_text)
        vl.addWidget(log_gb)

        # ── Signals ───────────────────────────────────────────────────────────
        self.btn_backup.clicked.connect(self._do_backup)
        self.btn_restore.clicked.connect(self._do_restore)
        self.btn_schedule.clicked.connect(self._do_schedule)
        self.btn_list.clicked.connect(self._do_list)
        self.btn_refresh.clicked.connect(self._refresh_clusters)
        self.btn_save_prof.clicked.connect(self._save_profile)
        self.btn_load_prof.clicked.connect(self._load_profile)
        self.btn_del_prof.clicked.connect(self._delete_profile)

    def _refresh_clusters(self):
        clusters = self.be.discover_clusters()
        self.ctx_combo.clear()
        self.ctx_combo.addItem("")
        self.ctx_combo.addItems(clusters)
        self._log(f"[Velero] 发现 {len(clusters)} 个 K8s 上下文")

    def _log(self, msg: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f'<span style="color:{Colors.SUBTEXT}">[{ts}]</span> {msg}')
        log(msg)

    def _get_form(self) -> dict:
        return {
            "context": self.ctx_combo.currentText(),
            "backup_name": self.backup_name.text(),
            "namespaces": [n.strip() for n in self.ns_edit.text().split(",") if n.strip()],
            "ttl": self.ttl_combo.currentText().split(" ")[0],
            "include_resources": [r.strip() for r in self.include_res.text().split(",") if r.strip()],
            "exclude_resources": [r.strip() for r in self.exclude_res.text().split(",") if r.strip()],
            "snapshot_volumes": self.snap_cbox.isChecked(),
            "schedule": self.schedule_expr.text(),
            "ns_mapping": self.ns_map.text(),
        }

    def _do_backup(self):
        f = self._get_form()
        name = f["backup_name"] or f"backup-{datetime.date.today()}"
        self._log(f"[Velero] 开始备份: {name}")
        self.be.backup(
            name=name, context=f["context"], namespaces=f["namespaces"],
            ttl=f["ttl"], include_resources=f["include_resources"],
            exclude_resources=f["exclude_resources"],
            snapshot_volumes=f["snapshot_volumes"],
            on_done=lambda out, rc: self._log(
                f"[Velero] 备份完成 (rc={rc}): {out[:500]}"),
        )

    def _do_restore(self):
        f = self._get_form()
        backup = self.backup_name.text() or "latest"
        mapping = {}
        if f["ns_mapping"]:
            for m in f["ns_mapping"].split(","):
                parts = m.split(":")
                if len(parts) == 2:
                    mapping[parts[0].strip()] = parts[1].strip()
        confirm = QMessageBox(self)
        confirm.setWindowTitle("确认恢复操作")
        confirm.setText("⚠️  恢复操作会覆盖目标集群中的现有资源。\n\n"
                        f"备份: {backup}\n"
                        f"命名空间: {f['namespaces']}\n"
                        f"上下文: {f['context']}\n\n"
                        "确定要继续吗？")
        confirm.setIcon(QMessageBox.Icon.Warning)
        confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm.exec() != QMessageBox.StandardButton.Yes:
            self._log("[Velero] 恢复已取消")
            return
        self._log(f"[Velero] 从 {backup} 恢复...")
        self.be.restore(
            backup_name=backup, context=f["context"],
            namespace_mapping=mapping,
            include_namespaces=f["namespaces"],
            on_done=lambda out, rc: self._log(
                f"[Velero] 恢复完成 (rc={rc}): {out[:500]}"),
        )

    def _do_schedule(self):
        f = self._get_form()
        if not f["schedule"]:
            self._log("[Velero] 错误: 请填写定时表达式")
            return
        name = f["backup_name"] or f"scheduled-{datetime.date.today()}"
        self._log(f"[Velero] 创建定时任务: {name} → {f['schedule']}")
        self.be.schedule_backup(
            name=name, context=f["context"], namespaces=f["namespaces"],
            schedule=f["schedule"], ttl=f["ttl"],
            on_done=lambda out, rc: self._log(
                f"[Velero] 定时任务已创建 (rc={rc}): {out[:500]}"),
        )

    def _do_list(self):
        f = self._get_form()
        self._log("[Velero] 列出备份...")
        self.be.list_backups(
            context=f["context"],
            on_done=lambda out, rc: self._log(
                f"[Velero] 备份列表 (rc={rc}):\n{out}"),
        )

    def _save_profile(self):
        name, ok = self._prompt_name("保存配置", "配置名称:")
        if ok and name:
            self.cfg.save_profile("velero", name, self._get_form())
            self._rebuild_profiles()
            self._log(f"[Velero] 配置 '{name}' 已保存")

    def _load_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            data = self.cfg.get_profile("velero", name)
            if data:
                self.ctx_combo.setCurrentText(data.get("context", ""))
                self.backup_name.setText(data.get("backup_name", ""))
                self.ns_edit.setText(",".join(data.get("namespaces", [])))
                idx = self.ttl_combo.findText(data.get("ttl", "720h") + " ")
                if idx >= 0:
                    self.ttl_combo.setCurrentIndex(idx)
                self.include_res.setText(",".join(data.get("include_resources", [])))
                self.exclude_res.setText(",".join(data.get("exclude_resources", [])))
                self.snap_cbox.setChecked(data.get("snapshot_volumes", True))
                self.schedule_expr.setText(data.get("schedule", ""))
                self._log(f"[Velero] 配置 '{name}' 已加载")

    def _delete_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            self.cfg.delete_profile("velero", name)
            self._rebuild_profiles()
            self._log(f"[Velero] 配置 '{name}' 已删除")

    def _rebuild_profiles(self):
        self.prof_combo.blockSignals(True)
        self.prof_combo.clear()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("velero"))
        self.prof_combo.blockSignals(False)

    def _prompt_name(self, title: str, prompt: str):
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, title, prompt)
        return name, ok


class RclonePanel(QWidget):
    def __init__(self, backend: RcloneBackend, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self.be = backend
        self.cfg = cfg
        self._build_ui()
        self._refresh_remotes()

    def _build_ui(self):
        vl = QVBoxLayout(self)
        vl.setContentsMargins(12, 12, 12, 12)
        vl.setSpacing(10)

        toolbar = QHBoxLayout()
        self.btn_sync = btn("🔄 同步")
        self.btn_copy = btn("📋 复制")
        self.btn_bwlimit = btn("⚡ 限速")
        self.btn_refresh = btn("🔄 刷新远端")
        for b in [self.btn_sync, self.btn_copy, self.btn_bwlimit, self.btn_refresh]:
            toolbar.addWidget(b)
        toolbar.addStretch()
        vl.addLayout(toolbar)

        sw = QScrollArea()
        sw.setWidgetResizable(True)
        sw.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")
        cont = QWidget()
        fl = QFormLayout(cont)
        fl.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        fl.setSpacing(10)

        # Profile
        prof_h = QHBoxLayout()
        self.prof_combo = QComboBox()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("rclone"))
        for btn_cfg, fn in [
            (btn("📂 加载"), self._load_profile),
            (btn("💾 保存"), self._save_profile),
            (btn("🗑 删除"), self._delete_profile),
        ]:
            prof_h.addWidget(btn_cfg)
            if fn == self._load_profile:
                self.btn_load_p = btn_cfg
            elif fn == self._save_profile:
                self.btn_save_p = btn_cfg
            else:
                self.btn_del_p = btn_cfg
        fl.addRow("配置档案:", self.prof_combo)
        fl.addRow("", prof_h)

        # Source / Dest
        self.src_edit = QComboBox()
        self.src_edit.setEditable(True)
        self.src_edit.setMinimumWidth(300)
        self.dest_edit = QComboBox()
        self.dest_edit.setEditable(True)
        self.dest_edit.setMinimumWidth(300)
        fl.addRow("源路径:", self.src_edit)
        fl.addRow("目标路径:", self.dest_edit)

        # Mode
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "同步 (Sync — 删除目标多余文件)",
            "复制 (Copy — 复制到目标)",
            "镜像 (Mirror — 等同复制)",
            "检查 (Check — 仅比较不操作)",
        ])
        fl.addRow("操作模式:", self.mode_combo)

        # Options
        self.dry_run = QCheckBox("预演模式 (不实际操作)")
        fl.addRow("", self.dry_run)

        self.bwlimit_edit = line()
        self.bwlimit_edit.setPlaceholderText("10M, 1G (留空=不限速)")
        fl.addRow("带宽限制:", self.bwlimit_edit)

        self.filters_edit = line()
        self.filters_edit.setPlaceholderText("exclude:*.tmp, include:*.pdf")
        fl.addRow("过滤规则:", self.filters_edit)

        self.transfers_spin = QSpinBox()
        self.transfers_spin.setRange(1, 32)
        self.transfers_spin.setValue(4)
        fl.addRow("并发数:", self.transfers_spin)

        sw.setWidget(cont)
        vl.addWidget(sw)

        # Log
        log_gb = card(self, "📤 执行日志")
        log_layout = QVBoxLayout(log_gb)
        self.log_text = log_view()
        log_layout.addWidget(self.log_text)
        vl.addWidget(log_gb)

        # Signals
        self.btn_sync.clicked.connect(self._do_sync)
        self.btn_copy.clicked.connect(self._do_copy)
        self.btn_bwlimit.clicked.connect(self._do_bwlimit)
        self.btn_refresh.clicked.connect(self._refresh_remotes)
        self.btn_load_p.clicked.connect(self._load_profile)
        self.btn_save_p.clicked.connect(self._save_profile)
        self.btn_del_p.clicked.connect(self._delete_profile)

    def _refresh_remotes(self):
        remotes = self.be.list_remotes()
        for cbox in [self.src_edit, self.dest_edit]:
            current = cbox.currentText()
            cbox.blockSignals(True)
            cbox.clear()
            cbox.addItems(remotes)
            if current in remotes:
                cbox.setCurrentText(current)
            cbox.blockSignals(False)
        self._log(f"[Rclone] 发现 {len(remotes)} 个远端存储")

    def _log(self, msg: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f'<span style="color:{Colors.SUBTEXT}">[{ts}]</span> {msg}')
        log(msg)

    def _get_form(self) -> dict:
        filters = [f.strip() for f in self.filters_edit.text().split(",") if f.strip()]
        return {
            "source": self.src_edit.currentText(),
            "dest": self.dest_edit.currentText(),
            "mode": self.mode_combo.currentText(),
            "dry_run": self.dry_run.isChecked(),
            "bwlimit": self.bwlimit_edit.text(),
            "filters": filters,
            "transfers": self.transfers_spin.value(),
        }

    def _do_sync(self):
        f = self._get_form()
        if not f["source"] or not f["dest"]:
            self._log("[Rclone] 错误: 请填写源和目标路径")
            return
        mode = f["mode"]
        msg = f"即将执行 Rclone 操作:\n\n源: {f['source']}\n目标: {f['dest']}\n模式: {mode}\n\n是否继续？"
        if "同步" in mode and "删除" in mode:
            msg += "\n\n⚠️ 注意: 此模式会删除目标端多余文件！"
        from PyQt6.QtWidgets import QMessageBox
        if QMessageBox.question(self, "确认 Rclone 操作", msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            self._log("[Rclone] 操作已取消")
            return
        self._log(f"[Rclone] 开始同步: {f['source']} → {f['dest']}")
        self.be.sync(
            source=f["source"], dest=f["dest"], mode=f["mode"],
            filters=f["filters"], dry_run=f["dry_run"],
            on_done=lambda out, rc: self._log(f"[Rclone] 完成 (rc={rc}): {out[:800]}"),
        )

    def _do_copy(self):
        f = self._get_form()
        if not f["source"] or not f["dest"]:
            self._log("[Rclone] 错误: 请填写源和目标路径")
            return
        from PyQt6.QtWidgets import QMessageBox
        if QMessageBox.question(self, "确认 Rclone 操作",
                f"即将复制:\n\n源: {f['source']}\n目标: {f['dest']}\n\n是否继续？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            self._log("[Rclone] 操作已取消")
            return
        self._log(f"[Rclone] 开始复制: {f['source']} → {f['dest']}")
        self.be.copy(
            source=f["source"], dest=f["dest"], dry_run=f["dry_run"],
            on_done=lambda out, rc: self._log(f"[Rclone] 完成 (rc={rc}): {out[:800]}"),
        )

    def _do_bwlimit(self):
        lim = self.bwlimit_edit.text() or "unlimited"
        self._log(f"[Rclone] 带宽限制: {lim}")
        self.be.bandwidth_limit(lim,
            on_done=lambda out, rc: self._log(f"[Rclone] {out}"))

    def _save_profile(self):
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "保存配置", "配置名称:")
        if ok and name:
            self.cfg.save_profile("rclone", name, self._get_form())
            self._rebuild_profiles()
            self._log(f"[Rclone] 配置 '{name}' 已保存")

    def _load_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            data = self.cfg.get_profile("rclone", name)
            if data:
                self.src_edit.setCurrentText(data.get("source", ""))
                self.dest_edit.setCurrentText(data.get("dest", ""))
                idx = self.mode_combo.findText(data.get("mode", ""))
                if idx >= 0:
                    self.mode_combo.setCurrentIndex(idx)
                self.dry_run.setChecked(data.get("dry_run", False))
                self.bwlimit_edit.setText(data.get("bwlimit", ""))
                self.filters_edit.setText(", ".join(data.get("filters", [])))
                self.transfers_spin.setValue(data.get("transfers", 4))
                self._log(f"[Rclone] 配置 '{name}' 已加载")

    def _delete_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            self.cfg.delete_profile("rclone", name)
            self._rebuild_profiles()
            self._log(f"[Rclone] 配置 '{name}' 已删除")

    def _rebuild_profiles(self):
        self.prof_combo.blockSignals(True)
        self.prof_combo.clear()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("rclone"))
        self.prof_combo.blockSignals(False)


class RsyncPanel(QWidget):
    def __init__(self, backend: RsyncBackend, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self.be = backend
        self.cfg = cfg
        self._build_ui()

    def _build_ui(self):
        vl = QVBoxLayout(self)
        vl.setContentsMargins(12, 12, 12, 12)
        vl.setSpacing(10)

        toolbar = QHBoxLayout()
        self.btn_sync = btn("🔄 开始同步")
        self.btn_dry = btn("🔍 预演测试")
        toolbar.addWidget(self.btn_sync)
        toolbar.addWidget(self.btn_dry)
        toolbar.addStretch()
        vl.addLayout(toolbar)

        sw = QScrollArea()
        sw.setWidgetResizable(True)
        sw.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")
        cont = QWidget()
        fl = QFormLayout(cont)
        fl.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        fl.setSpacing(10)

        # Profile
        self.prof_combo = QComboBox()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("rsync"))
        prof_h = QHBoxLayout()
        for lbl, fn in [("📂 加载", self._load_profile), ("💾 保存", self._save_profile), ("🗑 删除", self._delete_profile)]:
            b = btn(lbl)
            b.clicked.connect(fn)
            prof_h.addWidget(b)
        fl.addRow("配置档案:", self.prof_combo)
        fl.addRow("", prof_h)

        # Source / Dest
        src_h = QHBoxLayout()
        self.src_edit = line()
        self.src_edit.setPlaceholderText("user@host:/path/to/source/")
        self.src_btn = btn("📁 浏览")
        src_h.addWidget(self.src_edit)
        src_h.addWidget(self.src_btn)
        fl.addRow("源路径:", src_h)

        dest_h = QHBoxLayout()
        self.dest_edit = line()
        self.dest_edit.setPlaceholderText("user@host:/path/to/dest/")
        self.dest_btn = btn("📁 浏览")
        dest_h.addWidget(self.dest_edit)
        dest_h.addWidget(self.dest_btn)
        fl.addRow("目标路径:", dest_h)

        # SSH options
        ssh_gb = card(self, "SSH / 网络选项")
        ssh_fl = QFormLayout(ssh_gb)
        self.ssh_user = line()
        self.ssh_user.setPlaceholderText("root")
        ssh_fl.addRow("SSH 用户:", self.ssh_user)

        self.ssh_key = line()
        self.ssh_key.setPlaceholderText("/path/to/id_rsa (留空=默认)")
        ssh_fl.addRow("SSH 密钥:", self.ssh_key)

        self.ssh_port = QSpinBox()
        self.ssh_port.setRange(1, 65535)
        self.ssh_port.setValue(22)
        ssh_fl.addRow("SSH 端口:", self.ssh_port)
        vl.addWidget(ssh_gb)

        # Options
        opt_gb = card(self, "同步选项")
        opt_fl = QFormLayout(opt_gb)
        self.opt_archive = QCheckBox("-a (归档模式,保留属性)")
        self.opt_archive.setChecked(True)
        self.opt_compress = QCheckBox("-z (压缩传输)")
        self.opt_verbose = QCheckBox("-v (详细输出)")
        self.opt_verbose.setChecked(True)
        self.opt_delete = QCheckBox("--delete (删除目标多余文件)")
        self.opt_checksum = QCheckBox("--checksum (按 checksum 比较)")
        self.opt_progress = QCheckBox("--progress (显示进度)")
        self.opt_progress.setChecked(True)

        self.bwlimit = QSpinBox()
        self.bwlimit.setRange(0, 100000)
        self.bwlimit.setSuffix(" KB/s")
        self.bwlimit.setValue(0)

        self.exclude_edit = line()
        self.exclude_edit.setPlaceholderText("*.tmp, .cache, node_modules/")
        self.include_edit = line()
        self.include_edit.setPlaceholderText("*.py, *.sh")

        for w in [self.opt_archive, self.opt_compress, self.opt_verbose,
                  self.opt_delete, self.opt_checksum, self.opt_progress]:
            opt_fl.addRow("", w)
        opt_fl.addRow("带宽限制:", self.bwlimit)
        opt_fl.addRow("排除规则:", self.exclude_edit)
        opt_fl.addRow("包含规则:", self.include_edit)
        vl.addWidget(opt_gb)

        sw.setWidget(cont)
        vl.addWidget(sw)

        # Log
        log_gb = card(self, "📤 执行日志")
        log_layout = QVBoxLayout(log_gb)
        self.log_text = log_view()
        log_layout.addWidget(self.log_text)
        vl.addWidget(log_gb)

        self.btn_sync.clicked.connect(self._do_sync)
        self.btn_dry.clicked.connect(self._do_dry)
        self.src_btn.clicked.connect(lambda: self._browse(self.src_edit, True))
        self.dest_btn.clicked.connect(lambda: self._browse(self.dest_edit, True))

    def _log(self, msg: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f'<span style="color:{Colors.SUBTEXT}">[{ts}]</span> {msg}')
        log(msg)

    def _get_opts(self) -> dict:
        return {
            "archive": self.opt_archive.isChecked(),
            "compress": self.opt_compress.isChecked(),
            "verbose": self.opt_verbose.isChecked(),
            "progress": self.opt_progress.isChecked(),
            "delete": self.opt_delete.isChecked(),
            "checksum": self.opt_checksum.isChecked(),
            "bwlimit": self.bwlimit.value(),
            "exclude": self.exclude_edit.text(),
            "include": self.include_edit.text(),
            "ssh_port": self.ssh_port.value(),
            "ssh_user": self.ssh_user.text(),
            "ssh_key": self.ssh_key.text(),
        }

    def _do_sync(self):
        src = self.src_edit.text()
        dst = self.dest_edit.text()
        if not src or not dst:
            self._log("[Rsync] 错误: 请填写源和目标路径")
            return
        self._log(f"[Rsync] 开始同步: {src} → {dst}")
        self.be.sync(src, dst, self._get_opts(), False,
            on_done=lambda out, rc: self._log(f"[Rsync] 完成 (rc={rc}):\n{out[:800]}"),
        )

    def _do_dry(self):
        src = self.src_edit.text()
        dst = self.dest_edit.text()
        if not src or not dst:
            self._log("[Rsync] 错误: 请填写源和目标路径")
            return
        self._log(f"[Rsync] 预演模式: {src} → {dst}")
        self.be.sync(src, dst, self._get_opts(), True,
            on_done=lambda out, rc: self._log(f"[Rsync] 预演结果 (rc={rc}):\n{out[:1000]}"),
        )

    def _browse(self, edit: QLineEdit, folder_only: bool):
        if folder_only:
            path = QFileDialog.getExistingDirectory(self, "选择目录")
            if path:
                edit.setText(path)

    def _save_profile(self):
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        name, ok = QInputDialog.getText(self, "保存配置", "配置名称:")
        if ok and name:
            opts = self._get_opts()
            if opts.get("ssh_user") or opts.get("ssh_key"):
                warn = QMessageBox(self)
                warn.setWindowTitle("安全提醒")
                warn.setText("⚠️  配置中包含 SSH 用户名或密钥路径，已明文保存到本地配置文件中。\n请注意：如有敏感凭证，请勿将 profiles.json 提交到公开仓库。")
                warn.setIcon(QMessageBox.Icon.Warning)
                warn.exec()
            self.cfg.save_profile("rsync", name, opts)
            self._rebuild_profiles()
            self._log(f"[Rsync] 配置 '{name}' 已保存")

    def _load_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            d = self.cfg.get_profile("rsync", name)
            if d:
                self.opt_archive.setChecked(d.get("archive", True))
                self.opt_compress.setChecked(d.get("compress", False))
                self.opt_verbose.setChecked(d.get("verbose", True))
                self.opt_progress.setChecked(d.get("progress", True))
                self.opt_delete.setChecked(d.get("delete", False))
                self.opt_checksum.setChecked(d.get("checksum", False))
                self.bwlimit.setValue(d.get("bwlimit", 0))
                self.exclude_edit.setText(d.get("exclude", ""))
                self.include_edit.setText(d.get("include", ""))
                self.ssh_port.setValue(d.get("ssh_port", 22))
                self.ssh_user.setText(d.get("ssh_user", ""))
                self.ssh_key.setText(d.get("ssh_key", ""))
                self._log(f"[Rsync] 配置 '{name}' 已加载")

    def _delete_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            self.cfg.delete_profile("rsync", name)
            self._rebuild_profiles()
            self._log(f"[Rsync] 配置 '{name}' 已删除")

    def _rebuild_profiles(self):
        self.prof_combo.blockSignals(True)
        self.prof_combo.clear()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("rsync"))
        self.prof_combo.blockSignals(False)


class CoriolisPanel(QWidget):
    def __init__(self, backend: CoriolisBackend, cfg: ConfigManager, parent=None):
        super().__init__(parent)
        self.be = backend
        self.cfg = cfg
        self._build_ui()
        self._discover()

    def _build_ui(self):
        vl = QVBoxLayout(self)
        vl.setContentsMargins(12, 12, 12, 12)
        vl.setSpacing(10)

        toolbar = QHBoxLayout()
        self.btn_migrate = btn("🚀 执行迁移")
        self.btn_replica = btn("🔁 创建副本")
        self.btn_list_ep = btn("📋 端点列表")
        self.btn_list_mig = btn("📋 迁移列表")
        self.btn_refresh = btn("🔄 刷新")
        for b in [self.btn_migrate, self.btn_replica, self.btn_list_ep,
                  self.btn_list_mig, self.btn_refresh]:
            toolbar.addWidget(b)
        toolbar.addStretch()
        vl.addLayout(toolbar)

        sw = QScrollArea()
        sw.setWidgetResizable(True)
        sw.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")
        cont = QWidget()
        fl = QFormLayout(cont)
        fl.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        fl.setSpacing(10)

        # Profile
        self.prof_combo = QComboBox()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("coriolis"))
        prof_h = QHBoxLayout()
        for lbl, fn in [("📂 加载", self._load_profile), ("💾 保存", self._save_profile), ("🗑 删除", self._delete_profile)]:
            b = btn(lbl)
            b.clicked.connect(fn)
            prof_h.addWidget(b)
        fl.addRow("配置档案:", self.prof_combo)
        fl.addRow("", prof_h)

        # Endpoints
        self.src_endpoint = QComboBox()
        self.src_endpoint.setEditable(True)
        self.src_endpoint.setMinimumWidth(250)
        self.dest_endpoint = QComboBox()
        self.dest_endpoint.setEditable(True)
        self.dest_endpoint.setMinimumWidth(250)
        fl.addRow("源端点:", self.src_endpoint)
        fl.addRow("目标端点:", self.dest_endpoint)

        # VMs
        self.vm_ids = line()
        self.vm_ids.setPlaceholderText("vm-uuid-1, vm-uuid-2 (留空=全部)")
        fl.addRow("VM ID (多个逗号分隔):", self.vm_ids)

        # Minion pool
        self.minion_pool = QComboBox()
        self.minion_pool.setEditable(True)
        fl.addRow("Minion 池:", self.minion_pool)

        # Options
        dw = QLabel("⚠️ 迁移和副本操作无预演模式，请确认目标环境后再执行")
        dw.setStyleSheet("color: #e67e22; font-weight: bold;")
        dw.setWordWrap(True)
        fl.addRow("", dw)

        sw.setWidget(cont)
        vl.addWidget(sw)

        # Log
        log_gb = card(self, "📤 执行日志")
        log_layout = QVBoxLayout(log_gb)
        self.log_text = log_view()
        log_layout.addWidget(self.log_text)
        vl.addWidget(log_gb)

        self.btn_migrate.clicked.connect(self._do_migrate)
        self.btn_replica.clicked.connect(self._do_replica)
        self.btn_list_ep.clicked.connect(self._do_list_endpoints)
        self.btn_list_mig.clicked.connect(self._do_list_migrations)
        self.btn_refresh.clicked.connect(self._discover)

    def _log(self, msg: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f'<span style="color:{Colors.SUBTEXT}">[{ts}]</span> {msg}')
        log(msg)

    def _discover(self):
        self._log("[Coriolis] 发现端点...")
        self.be.list_endpoints(
            on_done=lambda out, rc: self._update_endpoints(out, rc),
            on_err=lambda e: self._log(f"[Coriolis] 端点发现失败: {e}"),
        )
        self.be.list_minions_pools(
            on_done=lambda out, rc: self._update_pools(out, rc),
            on_err=lambda e: self._log(f"[Coriolis] Minion池发现失败: {e}"),
        )

    def _update_endpoints(self, out: str, rc: int):
        self._log(f"[Coriolis] 端点列表 (rc={rc}): {out[:600]}")
        try:
            data = json.loads(out)
            names = [e.get("name", "?") for e in (data if isinstance(data, list) else [])]
        except Exception:
            names = []
        for cbox in [self.src_endpoint, self.dest_endpoint]:
            cur = cbox.currentText()
            cbox.blockSignals(True)
            cbox.clear()
            cbox.addItems(names)
            if cur in names:
                cbox.setCurrentText(cur)
            cbox.blockSignals(False)

    def _update_pools(self, out: str, rc: int):
        self._log(f"[Coriolis] Minion池 (rc={rc}): {out[:400]}")
        try:
            data = json.loads(out)
            names = [p.get("name", "?") for p in (data if isinstance(data, list) else [])]
        except Exception:
            names = []
        cur = self.minion_pool.currentText()
        self.minion_pool.blockSignals(True)
        self.minion_pool.clear()
        self.minion_pool.addItems(names)
        if cur in names:
            self.minion_pool.setCurrentText(cur)
        self.minion_pool.blockSignals(False)

    def _do_migrate(self):
        src = self.src_endpoint.currentText()
        dst = self.dest_endpoint.currentText()
        vms = [v.strip() for v in self.vm_ids.text().split(",") if v.strip()]
        mp = self.minion_pool.currentText()
        confirm = QMessageBox(self)
        confirm.setWindowTitle("确认迁移操作")
        confirm.setText(f"⚠️  迁移是高影响操作，将把 VM 从 {src} 迁移到 {dst}。\n\nVM: {vms}\n目标端点: {dst}\n\n确定要继续吗？")
        confirm.setIcon(QMessageBox.Icon.Warning)
        confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm.exec() != QMessageBox.StandardButton.Yes:
            self._log("[Coriolis] 迁移已取消")
            return
        self._log(f"[Coriolis] 发起迁移: {src} → {dst}, VMs={vms}, Minion={mp}")
        self.be.migrate(
            source_endpoint=src, dest_endpoint=dst, vm_ids=vms,
            minion_pool=mp,
            on_done=lambda out, rc: self._log(f"[Coriolis] 迁移任务已创建 (rc={rc}): {out[:500]}"),
        )

    def _do_replica(self):
        src = self.src_endpoint.currentText()
        dst = self.dest_endpoint.currentText()
        vms = [v.strip() for v in self.vm_ids.text().split(",") if v.strip()]
        confirm = QMessageBox(self)
        confirm.setWindowTitle("确认副本操作")
        confirm.setText(f"⚠️  创建副本将在 {dst} 端点生成 VM 副本，可能产生额外资源费用。\n\n源: {src}\n目标: {dst}\nVM: {vms}\n\n确定要继续吗？")
        confirm.setIcon(QMessageBox.Icon.Warning)
        confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm.exec() != QMessageBox.StandardButton.Yes:
            self._log("[Coriolis] 副本操作已取消")
            return
        self._log(f"[Coriolis] 创建副本: {src} → {dst}")
        self.be.replica(
            source_endpoint=src, dest_endpoint=dst, vm_ids=vms,
            on_done=lambda out, rc: self._log(f"[Coriolis] 副本任务已创建 (rc={rc}): {out[:500]}"),
        )

    def _do_list_endpoints(self):
        self._log("[Coriolis] 获取端点列表...")
        self.be.list_endpoints(
            on_done=lambda out, rc: self._log(f"[Coriolis] 端点 (rc={rc}):\n{out}"),
        )

    def _do_list_migrations(self):
        self._log("[Coriolis] 获取迁移列表...")
        self.be.list_migrations(
            on_done=lambda out, rc: self._log(f"[Coriolis] 迁移列表 (rc={rc}):\n{out}"),
        )

    def _save_profile(self):
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "保存配置", "配置名称:")
        if ok and name:
            data = {
                "source_endpoint": self.src_endpoint.currentText(),
                "dest_endpoint": self.dest_endpoint.currentText(),
                "vm_ids": self.vm_ids.text(),
                "minion_pool": self.minion_pool.currentText(),
            }
            self.cfg.save_profile("coriolis", name, data)
            self._rebuild_profiles()
            self._log(f"[Coriolis] 配置 '{name}' 已保存")

    def _load_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            d = self.cfg.get_profile("coriolis", name)
            if d:
                self.src_endpoint.setCurrentText(d.get("source_endpoint", ""))
                self.dest_endpoint.setCurrentText(d.get("dest_endpoint", ""))
                self.vm_ids.setText(d.get("vm_ids", ""))
                self.minion_pool.setCurrentText(d.get("minion_pool", ""))
                self._log(f"[Coriolis] 配置 '{name}' 已加载")

    def _delete_profile(self):
        name = self.prof_combo.currentText()
        if name and name != "— 新建 —":
            self.cfg.delete_profile("coriolis", name)
            self._rebuild_profiles()
            self._log(f"[Coriolis] 配置 '{name}' 已删除")

    def _rebuild_profiles(self):
        self.prof_combo.blockSignals(True)
        self.prof_combo.clear()
        self.prof_combo.addItems(["— 新建 —"] + self.cfg.list_profiles("coriolis"))
        self.prof_combo.blockSignals(False)


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

class DashboardPanel(QWidget):
    def __init__(self, cfg: ConfigManager, backends: dict, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self.backends = backends
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        vl = QVBoxLayout(self)
        vl.setContentsMargins(16, 16, 16, 16)
        vl.setSpacing(14)

        # Title
        title = QLabel("🛡 DR Backup — 统一容灾备份中心")
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {Colors.ACCENT};")
        vl.addWidget(title)

        # Tool cards
        cards_h = QHBoxLayout()
        cards_h.setSpacing(12)
        for tool, be in self.backends.items():
            card_w = self._tool_card(tool, be.available)
            cards_h.addWidget(card_w, 1)
        vl.addLayout(cards_h)

        # Jobs table
        jobs_gb = card(self, "📋 保存的任务配置")
        jobs_layout = QVBoxLayout(jobs_gb)
        self.jobs_table = QTableWidget()
        self.jobs_table.setColumnCount(5)
        self.jobs_table.setHorizontalHeaderLabels(["ID", "工具", "名称", "描述", "创建时间"])
        self.jobs_table.horizontalHeader().setStretchLastSection(True)
        self.jobs_table.setMaximumHeight(200)
        jobs_layout.addWidget(self.jobs_table)
        vl.addWidget(jobs_gb)

        # Quick start guide
        guide_gb = card(self, "📖 快速开始指南")
        guide_layout = QVBoxLayout(guide_gb)
        guide_layout.addWidget(QLabel(
            f'<span style="color:{Colors.YELLOW}">Velero</span> — K8s 备份/恢复，需提前配置 kubeconfig'
            f'&nbsp;&nbsp;|&nbsp;&nbsp;'
            f'<span style="color:{Colors.YELLOW}">Rclone</span> — 云存储同步，支持 70+ 云后端'
            f'&nbsp;&nbsp;|&nbsp;&nbsp;'
            f'<span style="color:{Colors.YELLOW}">Rsync</span> — 文件级同步，支持 SSH/SFTP'
            f'&nbsp;&nbsp;|&nbsp;&nbsp;'
            f'<span style="color:{Colors.YELLOW}">Coriolis</span> — 云平台迁移 (OpenStack/VirtualBox 等)'
        ))
        guide_layout.addWidget(QLabel(
            f'💡 所有配置支持保存为档案，方便重复使用。'
            f'&nbsp;&nbsp;📂 配置目录: <code>{CONFIG_DIR}</code>'
        ))
        vl.addWidget(guide_gb)

        vl.addStretch()

    def _tool_card(self, tool: str, available: bool) -> QFrame:
        icons = {"velero": "☸", "rclone": "☁", "rsync": "📁", "coriolis": "🚀"}
        icon = icons.get(tool, "🔧")
        status = "✅ 就绪" if available else "❌ 未安装"
        status_color = Colors.GREEN if available else Colors.RED
        descs = {
            "velero": "K8s 持久卷 + 资源备份/恢复",
            "rclone": "70+ 云存储同步/复制",
            "rsync": "文件级增量同步 (支持 SSH)",
            "coriolis": "跨云平台 VM 迁移/副本",
        }

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{ background: {Colors.SURFACE}; border: 1px solid {Colors.BORDER};
                     border-radius: 8px; padding: 14px; }}
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        layout.addWidget(QLabel(f"<span style='font-size:28px'>{icon}</span>"))
        layout.addWidget(QLabel(f"<span style='font-size:16px;font-weight:bold'>{tool.upper()}</span>"))
        layout.addWidget(QLabel(f"<span style='color:{status_color};font-weight:bold'>{status}</span>"))
        layout.addWidget(QLabel(f"<span style='color:{Colors.SUBTEXT};font-size:11px'>{descs[tool]}</span>"))
        return card

    def _refresh(self):
        jobs = self.cfg.jobs
        self.jobs_table.setRowCount(len(jobs))
        for i, job in enumerate(jobs):
            self.jobs_table.setItem(i, 0, QTableWidgetItem(job.get("id", "")))
            self.jobs_table.setItem(i, 1, QTableWidgetItem(job.get("tool", "")))
            self.jobs_table.setItem(i, 2, QTableWidgetItem(job.get("name", "")))
            self.jobs_table.setItem(i, 3, QTableWidgetItem(job.get("desc", "")))
            self.jobs_table.setItem(i, 4, QTableWidgetItem(job.get("created", "")))


# ══════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cfg = ConfigManager()

        # Init backends
        self.backends = {
            "velero": VeleroBackend(),
            "rclone": RcloneBackend(),
            "rsync": RsyncBackend(),
            "coriolis": CoriolisBackend(),
        }

        self.setWindowTitle("🛡 DR Backup — 统一容灾备份工具")
        self.setMinimumSize(1100, 720)
        self._build_ui()
        log("[DR-Backup-GUI] Application started")

    def _build_ui(self):
        # ── Menu bar ──────────────────────────────────────────────────────────
        menubar = QMenuBar()
        m_file = menubar.addMenu("文件")
        m_file.addAction("打开配置目录", self._open_config_dir)
        m_file.addSeparator()
        m_file.addAction("退出", self.close)
        m_edit = menubar.addMenu("视图")
        m_edit.addAction("仪表盘", lambda: self.tabs.setCurrentIndex(0))
        m_help = menubar.addMenu("帮助")
        m_help.addAction("关于", self._show_about)
        self.setMenuBar(menubar)

        # ── Central widget ─────────────────────────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        vl = QVBoxLayout(central)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(0)

        # Tool status banner
        self.banner = ToolStatusBanner(self.backends)
        vl.addWidget(self.banner)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        vl.addWidget(self.tabs)

        # Dashboard
        self.dashboard = DashboardPanel(self.cfg, self.backends)
        self.tabs.addTab(self.dashboard, "📊 仪表盘")

        # Tool tabs
        self.tabs.addTab(VeleroPanel(self.backends["velero"], self.cfg), "☸ Velero")
        self.tabs.addTab(RclonePanel(self.backends["rclone"], self.cfg), "☁ Rclone")
        self.tabs.addTab(RsyncPanel(self.backends["rsync"], self.cfg), "📁 Rsync")
        self.tabs.addTab(CoriolisPanel(self.backends["coriolis"], self.cfg), "🚀 Coriolis")

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start(5000)

    def _update_status(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        installed = sum(1 for be in self.backends.values() if be.available)
        self.status_bar.showMessage(
            f"就绪  |  {installed}/{len(self.backends)} 工具已安装  |  {now}"
        )

    def _open_config_dir(self):
        import platform
        if platform.system() == "Darwin":
            subprocess.run(["open", CONFIG_DIR])
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", CONFIG_DIR])
        else:
            subprocess.run(["explorer", CONFIG_DIR])

    def _show_about(self):
        QMessageBox.about(self, "关于 DR Backup GUI",
            f"<b>DR Backup — 统一容灾备份工具</b><br><br>"
            f"集成了以下备份/迁移工具:<br>"
            f"• <b>Velero</b> — Kubernetes 备份与恢复<br>"
            f"• <b>Rclone</b> — 云存储同步 (70+ 后端)<br>"
            f"• <b>Rsync</b> — 文件级增量同步<br>"
            f"• <b>Coriolis</b> — 跨云平台迁移<br><br>"
            f"版本 1.0.0<br>"
            f"配置目录: <code>{CONFIG_DIR}</code>"
        )

    def closeEvent(self, event):
        log("[DR-Backup-GUI] Application closed")
        event.accept()


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DR Backup GUI")
    apply_dark_theme(app)

    # Check PyQt6
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
