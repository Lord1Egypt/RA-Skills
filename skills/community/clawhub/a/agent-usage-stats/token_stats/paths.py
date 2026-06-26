"""Cross-platform data path discovery and saved path configuration."""

from __future__ import annotations

import json
import os
import sys

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "token-stats")
CONFIG_FILE = os.path.join(CONFIG_DIR, "paths.json")

_WSL_HOMES_CACHE = None


def get_wsl_homes():
    """Windows 上枚举 WSL 发行版中可能存放 Agent 数据的 home 目录。返回路径列表（缓存结果）。"""
    global _WSL_HOMES_CACHE
    if _WSL_HOMES_CACHE is not None:
        return _WSL_HOMES_CACHE
    if sys.platform != "win32":
        _WSL_HOMES_CACHE = []
        return []
    homes = []

    try:
        import subprocess
        distros_out = subprocess.run(
            ["wsl.exe", "-l", "-q"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=5,
        )
        for line in distros_out.stdout.decode("utf-16-le", errors="ignore").splitlines():
            distro = line.strip()
            if not distro:
                continue
            try:
                home_out = subprocess.run(
                    ["wsl.exe", "-d", distro, "--", "bash", "-c", "echo $HOME"],
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=5,
                )
                wsl_home = home_out.stdout.decode("utf-8", errors="ignore").strip()
                if wsl_home and wsl_home.startswith("/"):
                    homes.append(f"//wsl.localhost/{distro}{wsl_home}")
            except Exception:
                pass
    except Exception:
        pass

    if not homes:
        for wsl_root in [r"\\wsl.localhost", r"\\wsl$"]:
            try:
                for distro in os.listdir(wsl_root):
                    distro_dir = os.path.join(wsl_root, distro)
                    if not os.path.isdir(distro_dir):
                        continue
                    for sub in ["home", "root"]:
                        home_base = os.path.join(distro_dir, sub)
                        if os.path.isdir(home_base):
                            try:
                                for user in os.listdir(home_base):
                                    uh = os.path.join(home_base, user)
                                    if os.path.isdir(uh):
                                        homes.append(uh)
                            except (OSError, PermissionError):
                                pass
            except (OSError, PermissionError, FileNotFoundError):
                continue

    homes = [h.replace("\\", "/") for h in homes]
    _WSL_HOMES_CACHE = homes
    return homes


def resolve_path(relative_path):
    """解析路径：先查本机 ~，再查 WSL home（Windows + wsl.exe 探测），返回首个存在的路径。"""
    native = os.path.join(os.path.expanduser("~"), relative_path)
    if os.path.exists(native):
        return native
    for wh in get_wsl_homes():
        wp = os.path.join(wh, relative_path)
        if os.path.exists(wp):
            return wp
        if sys.platform == "win32":
            try:
                import subprocess
                parts = wh.replace("\\", "/").strip("/").split("/")
                if len(parts) >= 4 and parts[0] in ("wsl.localhost", "wsl$"):
                    distro = parts[1]
                    wsl_path = "/" + "/".join(parts[3:]) + "/" + relative_path.lstrip(".")
                    probe = subprocess.run(
                        ["wsl.exe", "-d", distro, "--", "test", "-e", wsl_path],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3,
                    )
                    if probe.returncode == 0:
                        return wp
            except Exception:
                pass
    return native


def is_wsl_unc(path: str) -> bool:
    """检测路径是否为 WSL UNC 路径（如 //wsl.localhost/Distro/...）。"""
    return path.replace("\\", "/").startswith("//wsl.")


def wsl_unc_to_linux(unc_path):
    """WSL UNC 路径 → (distro, linux_path)。非 WSL 返回 (None, None)。"""
    p = unc_path.replace("\\", "/")
    for prefix in ("//wsl.localhost/", "//wsl$/"):
        if p.startswith(prefix):
            rest = p[len(prefix):]
            idx = rest.find("/")
            if idx > 0:
                return rest[:idx], "/" + rest[idx + 1:]
    return None, None


def hermes_collect_via_wsl(db_path, from_ts=None, to_ts=None):
    """通过 wsl.exe 在 WSL 内查询 Hermes 数据库。返回 dict 或 None。"""
    import subprocess
    distro, linux_path = wsl_unc_to_linux(db_path)
    if not distro:
        return None
    where = ""
    if from_ts or to_ts:
        parts = []
        if from_ts:
            grace = from_ts - 86400
            parts.append(f"(started_at >= {from_ts} OR (ended_at IS NULL AND started_at >= {grace}) OR ended_at >= {from_ts})")
        if to_ts:
            parts.append(f"started_at <= {to_ts}")
        where = " WHERE " + " AND ".join(parts)
    script = (
        "import sqlite3,json;c=sqlite3.connect(r'%s');c.row_factory=sqlite3.Row;"
        "cols={r[1] for r in c.execute('PRAGMA table_info(sessions)')};"
        "has_ac='api_call_count' in cols;has_tc='tool_call_count' in cols;"
        "ac='api_call_count' if has_ac else '0';tc='tool_call_count' if has_tc else '0';"
        "rows=[dict(r) for r in c.execute("
        "f'SELECT model,SUM(input_tokens) inp,SUM(output_tokens) out,SUM(cache_read_tokens) cache,'"
        "f'SUM('+ac+') calls,SUM('+tc+') tools,COUNT(*) cnt FROM sessions%s GROUP BY model')];"
        "sc=c.execute('SELECT COUNT(*) FROM sessions%s').fetchone()[0];"
        "c.close();print(json.dumps({'rows':rows,'sc':sc},default=str))"
    ) % (linux_path, where, where)
    try:
        r = subprocess.run(
            ["wsl.exe", "-d", distro, "--", "python3", "-c", script],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=15,
        )
        return json.loads(r.stdout.decode("utf-8", errors="ignore"))
    except Exception:
        return None


def codex_collect_via_wsl(db_path, from_ts=None, to_ts=None):
    """通过 wsl.exe 在 WSL 内查询 CodeX 数据库。返回 dict 或 None。"""
    import subprocess
    distro, linux_path = wsl_unc_to_linux(db_path)
    if not distro:
        return None
    where = ""
    if from_ts or to_ts:
        parts = []
        if from_ts:
            parts.append(f"updated_at >= {int(from_ts)}")
        if to_ts:
            parts.append(f"updated_at <= {int(to_ts)}")
        where = " WHERE " + " AND ".join(parts)
    script = (
        "import sqlite3,json;c=sqlite3.connect(r'%s');c.row_factory=sqlite3.Row;"
        "rows=[dict(r) for r in c.execute("
        "'SELECT model,model_provider,SUM(tokens_used) tokens,COUNT(*) cnt FROM threads%s GROUP BY model,model_provider')];"
        "sc=c.execute('SELECT COUNT(*) FROM threads%s').fetchone()[0];"
        "c.close();print(json.dumps({'rows':rows,'sc':sc},default=str))"
    ) % (linux_path, where, where)
    try:
        r = subprocess.run(
            ["wsl.exe", "-d", distro, "--", "python3", "-c", script],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=15,
        )
        return json.loads(r.stdout.decode("utf-8", errors="ignore"))
    except Exception:
        return None


def load_agent_paths() -> dict:
    """加载已保存的 Agent 数据路径配置"""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_agent_paths(paths: dict):
    """保存 Agent 数据路径配置"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(paths, f, indent=2, ensure_ascii=False)


def scan_all_agent_paths() -> dict:
    """扫描本机所有 Agent 的数据路径（含 WSL），返回 {agent_name: data_path}"""
    homes = [os.path.expanduser("~")] + get_wsl_homes()
    paths = {}
    for h in homes:
        for p in [os.path.join(h, ".hermes", "state.db"),
                  os.path.join(h, ".config", "hermes", "state.db")]:
            if os.path.exists(p):
                paths["hermes_db"] = p
                break
        if "hermes_db" in paths:
            break
    for h in homes:
        for p in [os.path.join(h, ".hermes", "sessions", "sessions.json"),
                  os.path.join(h, ".config", "hermes", "sessions", "sessions.json")]:
            if os.path.exists(p):
                paths["hermes_sessions"] = p
                break
        if "hermes_sessions" in paths:
            break
    for h in homes:
        p = os.path.join(h, ".claude")
        if os.path.isdir(os.path.join(p, "projects")):
            paths["claude_dir"] = p
            break
    for h in homes:
        p = os.path.join(h, ".codex")
        if os.path.isdir(p):
            paths["codex_dir"] = p
            break
    for h in homes:
        p = os.path.join(h, ".openclaw", "agents", "main", "sessions", "sessions.json")
        if os.path.exists(p):
            paths["openclaw_sessions"] = p
            break
    return paths
