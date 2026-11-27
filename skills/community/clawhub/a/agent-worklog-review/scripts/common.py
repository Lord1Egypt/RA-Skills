#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""共享工具模块：环境探测、路径发现、时间戳归一、zstd 兼容。

设计目标：环境无关。自动适配 Windows / Linux / macOS，有无 WSL 均可。
所有脚本优先 import 本模块，杜绝硬编码用户名与路径。
"""
import os, sys, re, glob, json

IS_WIN = os.name == "nt"
HOME = os.path.expanduser("~")


# ---------- 环境探测 ----------
from functools import lru_cache

# WSL UNC 路径探测在某些 Python（如 Anaconda）下会卡死；且重复探测很慢。
# 用缓存文件统一：由第一个能访问 UNC 的解释器（run_all 用普通 python）探测并写入，
# 其他解释器（如带 zstandard 的 anaconda）直接读缓存，不再碰 UNC 目录列举。
_PATH_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_env_paths_cache.json")


def _write_path_cache(homes):
    try:
        with open(_PATH_CACHE, "w", encoding="utf-8") as f:
            json.dump({"wsl_homes": homes}, f, ensure_ascii=False)
    except Exception:
        pass


def _read_path_cache():
    try:
        d = json.load(open(_PATH_CACHE, encoding="utf-8"))
        return list(d.get("wsl_homes", []))
    except Exception:
        return None


@lru_cache(maxsize=1)
def _wsl_homes_cached():
    cached = _read_path_cache()
    if cached is not None:
        return tuple(cached)
    # 缓存不存在：不在本进程现场探测（UNC 访问可能卡死），
    # 返回空。run_all.py 会先用 probe_wsl.py（独立进程+超时）生成缓存。
    return tuple()


def wsl_homes():
    """返回所有 WSL 发行版的用户 home（UNC 路径），读缓存文件。"""
    return list(_wsl_homes_cached())


def _wsl_homes_uncached():
    """返回所有 WSL 发行版的用户 home（UNC 路径）。非 Windows 或无 WSL 返回 []。

    关键坑：Windows Python 下 glob('//wsl.localhost/*/home/*') 返回空、
    os.listdir('//wsl.localhost') 可能报“网络名不可用”，必须逐个候选校验。
    """
    out, seen = [], set()
    if not IS_WIN:
        return out
    # 不在 UNC 根上做 os.listdir：某些 Python（Anaconda）下会长时间卡死。
    # 改用「候选发行版 × 候选用户名 + isdir 校验」；os.path.isdir 对不存在的
    # UNC 路径会快速返回 False。用户名候选含 Windows 用户名 + 常见名，
    # 并通过环境变量 WORKLOG_WSL_USER 让同事补充自己的特殊用户名。
    distros = ["Ubuntu", "Ubuntu-22.04", "Ubuntu-24.04", "debian", "Debian",
               "kali-linux", "openSUSE-Leap-15.6", "Arch", "fedora",
               os.environ.get("WORKLOG_WSL_DISTRO", "")]
    distros = [d for d in dict.fromkeys(distros) if d]
    # 常见 WSL 用户名兜底；非常规用户名用 WORKLOG_WSL_USER 或 --interactive 指定
    fallback_users = ["root", "ubuntu", os.path.basename(HOME),
                      os.environ.get("WORKLOG_WSL_USER", "")]
    users = [u for u in dict.fromkeys(fallback_users) if u]
    # 关键：\\wsl.localhost 与 \\wsl$ 指向同一文件，只能保留一种前缀，
    # 否则同一会话被扫两次、token 翻倍。优先 wsl.localhost。
    for d in distros:
        for u in users:
            for suffix in (f"home\\{u}",) if u != "root" else ("home\\root", "root"):
                for unc in ["\\\\wsl.localhost", "\\\\wsl$"]:
                    p = f"{unc}\\{d}\\{suffix}"
                    if os.path.isdir(p):
                        if p not in seen:
                            seen.add(p); out.append(p)
                        break  # 该后缀已找到可用前缀，不再试另一种 UNC
    return out


def extra_roots():
    """用户自定义的额外搜索根目录（Agent 会话库在非标准位置时）。

    来源：环境变量 WORKLOG_EXTRA_ROOTS（分号/逗号分隔）或
    config/local/extra_roots.json 的 {"roots": [...]}。
    """
    out = []
    env = os.environ.get("WORKLOG_EXTRA_ROOTS", "")
    for sep in (";", ","):
        env = env.replace(sep, "|")
    out += [p.strip() for p in env.split("|") if p.strip()]
    cfg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "config", "local", "extra_roots.json")
    if os.path.isfile(cfg):
        try:
            d = json.load(open(cfg, encoding="utf-8"))
            out += [p for p in (d.get("roots") or []) if isinstance(p, str) and p.strip()]
        except Exception:
            pass
    return list(dict.fromkeys(p for p in out if os.path.isdir(p)))


def all_homes():
    """本机 home + 所有 WSL home + 用户自定义根目录，去重。"""
    homes = [HOME] + wsl_homes() + extra_roots()
    seen, out = set(), []
    for h in homes:
        k = os.path.normpath(h).lower()
        if k not in seen and os.path.isdir(h):
            seen.add(k); out.append(h)
    return out


def appdata_roots():
    """返回配置根目录候选（Windows AppData / macOS / Linux）。"""
    roots = []
    if IS_WIN:
        for k in ("APPDATA", "LOCALAPPDATA"):
            v = os.environ.get(k)
            if v: roots.append(v)
        roots += [os.path.join(HOME, "AppData", "Roaming"),
                  os.path.join(HOME, "AppData", "Local")]
    elif sys.platform == "darwin":
        roots.append(os.path.join(HOME, "Library", "Application Support"))
    else:
        roots.append(os.path.join(HOME, ".config"))
    return list(dict.fromkeys(r for r in roots if os.path.isdir(r)))


def extra_disk_roots():
    """Windows 下其他磁盘根目录（项目级 .claude/.codex 探测用）。"""
    if not IS_WIN:
        return []
    roots = []
    for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        p = f"{letter}:\\"
        if os.path.isdir(p) and p.lower() != (os.path.splitdrive(HOME)[0] + "\\").lower():
            roots.append(p)
    return roots


def detect_python_with_zstd():
    """返回一个带 zstandard 模块的 Python 解释器路径，供 dsh 解压使用。

    优先级：当前解释器 → conda 常见路径 → PATH 中的 python。
    找不到返回 None（脚本应优雅降级，跳过 dsh 并说明）。
    """
    import subprocess
    candidates = [sys.executable]
    if IS_WIN:
        candidates += [
            r"C:\ProgramData\anaconda3\python.exe",
            r"C:\ProgramData\miniconda3\python.exe",
            os.path.join(HOME, "anaconda3", "python.exe"),
            os.path.join(HOME, "miniconda3", "python.exe"),
        ]
        for base in [r"C:\ProgramData\anaconda3\envs", os.path.join(HOME, "anaconda3", "envs")]:
            if os.path.isdir(base):
                candidates += [os.path.join(base, e, "python.exe") for e in os.listdir(base)]
    for exe in ("python3", "python"):
        from shutil import which
        w = which(exe)
        if w: candidates.append(w)
    for exe in candidates:
        if not exe or not os.path.isfile(exe):
            continue
        try:
            r = subprocess.run([exe, "-c", "import zstandard"],
                               capture_output=True, timeout=15)
            if r.returncode == 0:
                return os.path.abspath(exe)
        except Exception:
            pass
    return None


# ---------- 交互询问（可选，默认关闭） ----------
def interactive_enabled():
    """是否允许交互提示：需显式开关 + 必须是 TTY，两个条件都满足才提示。

    默认返回 False——run_all 常在后台/CI 跑，弹提示会直接卡死。
    开启方式：`python run_all.py --interactive` 或环境变量 WORKLOG_PROMPT=1。
    """
    flag = os.environ.get("WORKLOG_PROMPT", "").strip().lower()
    if flag not in ("1", "true", "yes", "on"):
        return False
    try:
        return sys.stdin.isatty()
    except Exception:
        return False


def ask(prompt, default="", validator=None):
    """交互式询问；非交互模式直接返回 default（静默跳过）。

    - 回车 / EOF / Ctrl+C 都返回 default，绝不强制。
    - validator(val) 返回 False 时视为无效，返回 default。
    - 只问非敏感信息（用户名/路径/项目名），调用方负责遵守。
    """
    if not interactive_enabled():
        return default
    suffix = f" [回车跳过: {default}]" if default else " [回车跳过]"
    try:
        line = input(f"? {prompt}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        return default
    if not line:
        return default
    if validator is not None:
        try:
            if not validator(line):
                print("  输入无效，已跳过。")
                return default
        except Exception:
            return default
    return line


# ---------- 路径与文件 ----------
def under(p, roots):
    """路径是否位于任一根目录之下。"""
    p = os.path.normpath(p).lower()
    return any(p.startswith(os.path.normpath(r).lower()) for r in roots)


def find_files(roots, pattern, recursive=True, exclude=()):
    """在多个根目录下按 glob 模式找文件（默认递归子目录）。

    注意：pattern 不含 ** 时自动加 **/ 前缀，否则 glob 只匹配根目录，
    会漏掉按日期/项目分目录存储的会话（Codex/Claude/dsh 都是这种结构）。
    """
    if recursive and "**" not in pattern:
        pattern = os.path.join("**", pattern)
    out = []
    for r in roots:
        if not os.path.isdir(r):
            continue
        for fp in glob.glob(os.path.join(r, pattern), recursive=recursive):
            low = fp.replace("/", "\\").lower()
            if any(x.replace("/", "\\").lower() in low for x in exclude):
                continue
            if os.path.isfile(fp):
                out.append(fp)
    return out


def out_dir():
    """输出目录：SKILL 根目录下的 output/（可通过环境变量覆盖）。"""
    d = os.environ.get("WORKLOG_OUT_DIR")
    if d:
        os.makedirs(d, exist_ok=True)
        return d
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = os.path.join(root, "output")
    os.makedirs(d, exist_ok=True)
    return d


def load_jsonl(path):
    rows = []
    if not os.path.isfile(path):
        return rows
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


# Agent 名称归一化：不同脚本/适配器对同一 agent 写法不同，统一映射。
AGENT_ALIAS = {
    "codex": "Codex", "openai codex": "Codex", "codexcli": "Codex",
    "workbuddy": "WorkBuddy", "claudecode": "ClaudeCode", "claude code": "ClaudeCode",
    "dsh": "dsh", "deepseek": "dsh", "qoder": "Qoder", "openakita": "OpenAkita",
    "cursor": "Cursor", "cursortraecodebuddy": "Cursor", "trae": "Cursor",
    "codebuddy": "Cursor", "windsurf": "Cursor", "marscode": "Cursor",
    "kimicode": "Kimi Code", "kimi": "Kimi Code", "kimi code": "Kimi Code",
}


def norm_agent(name):
    """把 agent 名归一到统一显示名（去空格/斜杠/连字符 + 别名映射）。"""
    s = str(name or "").strip()
    key = s.replace(" ", "").replace("/", "").replace("-", "").lower()
    return AGENT_ALIAS.get(key, AGENT_ALIAS.get(s.lower(), s))


def installed_agents(out=None):
    """本机「已安装且在用」的 Agent 集合：实际产出过任务或 token 的 agent。

    判定口径：all_tasks.jsonl / token_usage.jsonl 中出现过的 agent。
    - 只装了但没产生任何会话数据的 Agent 不算「在用」，不进报告；
    - 未安装但适配器按公开格式写了的 Agent（ZCode/Hermes/...）同样不进报告；
    - 返回统一名称集合，配合 norm_agent() 做过滤。
    """
    out = out or out_dir()
    names = set()
    for fn in ("all_tasks.jsonl", "token_usage.jsonl"):
        for r in load_jsonl(os.path.join(out, fn)):
            a = r.get("agent")
            if a:
                names.add(norm_agent(a))
    return names


# ---------- 时间与文本 ----------
def ts(v):
    """统一时间戳为 ISO 字符串。"""
    if v is None:
        return ""
    if isinstance(v, (int, float)):
        from datetime import datetime, timezone
        try:
            return datetime.fromtimestamp(v / 1000 if v > 1e12 else v, tz=timezone.utc).isoformat()
        except Exception:
            return str(v)
    return str(v)


def month_of(tsv):
    """从时间戳提取 YYYY-MM。"""
    if not tsv:
        return "未知"
    s = str(tsv)
    try:
        if s.replace(".", "", 1).isdigit():
            v = int(float(s))
            if v > 1e11:
                v /= 1000
            from datetime import datetime
            return datetime.fromtimestamp(v).strftime("%Y-%m")
        from datetime import datetime
        return datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%Y-%m")
    except Exception:
        m = re.match(r"(\d{4}-\d{2})", s)
        return m.group(1) if m else "未知"


def clean(s, limit=600):
    if not isinstance(s, str):
        return ""
    return re.sub(r"\s+", " ", s.replace("\r", " ").replace("\n", " ")).strip()[:limit]


def env_summary():
    """打印环境探测摘要，便于调试。"""
    return {
        "HOME": HOME,
        "is_windows": IS_WIN,
        "wsl_homes": wsl_homes(),
        "appdata_roots": appdata_roots(),
        "extra_disks": extra_disk_roots(),
        "python_with_zstd": detect_python_with_zstd(),
    }


if __name__ == "__main__":
    print(json.dumps(env_summary(), ensure_ascii=False, indent=2))
