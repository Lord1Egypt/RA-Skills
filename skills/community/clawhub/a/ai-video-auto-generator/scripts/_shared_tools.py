"""
ai-video-auto-generator 生态共享工具函数。

6 个纯工具函数 + 日志系统 + 配置加载（load_config + init_config）。
被 project-generate 和 agnes-ai 两个子 skill 的 config.py 同时引用。

配置加载原则：执行路径即身份。
不依赖全局环境变量，不绑定 .workbuddy / .codex 等平台目录名。
配置只来自两个地方：
  - <project>/config/        ← 当前视频项目专属（最高优先级）
  - <skill_root>/config/     ← 当前平台这份 skill 专属
"""

import json, os, sys


# ── 日志系统（共享同一 _LOG_FILE_STREAM，无需回调同步）──

LOG_LEVEL = 1  # 0=quiet, 1=normal, 2=verbose
_LOG_FILE_STREAM = None  # type: ignore


def set_log_file(path: str | None) -> None:
    """设置日志文件路径，后续 _log 输出会同时写入文件。"""
    global _LOG_FILE_STREAM
    if _LOG_FILE_STREAM:
        try:
            _LOG_FILE_STREAM.close()
        except Exception:
            pass
    if path:
        parent = os.path.dirname(path)
        if parent:
            try:
                os.makedirs(parent, exist_ok=True)
            except Exception:
                pass
        try:
            _LOG_FILE_STREAM = open(path, "a", encoding="utf-8")
        except Exception as e:
            print(f"[_shared_tools] ⚠️ 日志文件无法打开: {e}", file=sys.stderr)
            _LOG_FILE_STREAM = None
    else:
        _LOG_FILE_STREAM = None


def _log(msg: str, level: int = 1) -> None:
    """条件输出：仅当 level <= LOG_LEVEL 时打印，同时追加到日志文件。"""
    if level <= LOG_LEVEL:
        print(msg, flush=True)
    stream = _LOG_FILE_STREAM
    if stream:
        try:
            stream.write(msg + "\n")
            stream.flush()
        except Exception:
            pass


# ── 配置加载器（与路径走，不依赖全局 env）──

_ACTIVE_SKILL_ROOT: str | None = None
_ACTIVE_PROJECT: str | None = None
_ACTIVE_CONFIG: dict | None = None


def has_legacy_marker(skill_root: str | None = None) -> bool:
    """检查 skill_root 内是否有 .legacy-workbuddy 标记文件。

    标记文件存在时，旧 WorkBuddy 环境可读取 ~/.workbuddy/config.toml 作为 fallback。
    新平台默认跳过，实现零共享隔离。
    """
    root = skill_root or _ACTIVE_SKILL_ROOT
    if not root:
        return False
    return os.path.isfile(os.path.join(root, ".legacy-workbuddy"))


def _read_toml(path: str) -> dict:
    """安全读取 TOML 文件，失败返回空 dict。"""
    if not os.path.isfile(path):
        return {}
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}


def _read_key_value_env(path: str) -> dict:
    """读取 keys.env 格式文件（KEY=VALUE 每行一行）。"""
    if not os.path.isfile(path):
        return {}
    result: dict = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    result[k.strip()] = v.strip()
    except Exception:
        pass
    return result


def load_config(
    skill_root: str,
    project: str | None = None,
) -> dict:
    """分层加载配置，返回合并后的 dict。

    优先级（高 → 低; 后者覆盖前者）:
        1. <project>/config/keys.env           ← 当前视频项目专属
        2. <project>/config/config.toml
        3. <skill_root>/config/keys.env        ← 当前平台这份 skill 专属
        4. <skill_root>/config/config.toml

    不读全局 ~/.workbuddy/config.toml —— 那是 WorkBuddy 专属路径，
    不应该被其他平台读取。各平台读各自 skill_root/config/ 下的配置。
    仅在 skill_root 内有 .legacy-workbuddy 标记时才读旧路径。

    返回合并后的 dict，结构等同 TOML 嵌套 dict（section → key → value）。
    keys.env 的纯 KEY=VALUE 格式放在根 dict 的 "flat" 键下。

    Args:
        skill_root: skill 根目录（resolve_skill_root 返回值）。
        project: 可选的项目目录（--project 参数值）。

    Returns:
        合并后的配置 dict。
    """
    merged: dict = {}

    def _merge(layer: dict) -> None:
        """将 layer 合并到 merged，后者覆盖前者。"""
        for section, values in layer.items():
            if section not in merged:
                merged[section] = {}
            if isinstance(values, dict):
                merged[section].update(values)
            elif values is not None:
                merged[section] = values

    layers: list[str] = []

    # 1-2) 项目级配置（最优先 — 最后加载，所以放在列表最后）
    if project:
        layers.append(os.path.join(project, "config", "keys.env"))
        layers.append(os.path.join(project, "config", "config.toml"))

    # 3-4) 当前平台这份 skill 的配置
    layers.append(os.path.join(skill_root, "config", "keys.env"))
    layers.append(os.path.join(skill_root, "config", "config.toml"))

    # 5) legacy（仅当标记存在时）
    if has_legacy_marker(skill_root):
        layers.append(os.path.expanduser("~/.workbuddy/config.toml"))

    for path in layers:
        if path.endswith(".env"):
            _merge(_read_key_value_env(path))
        else:
            _merge(_read_toml(path))

    return merged


def init_config(skill_root: str, project: str | None = None) -> dict:
    """初始化全局活动配置。

    入口脚本（pipeline.py / project_generate.py）在启动时调用一次。
    此后 _ACTIVE_CONFIG 可以被 get() 等函数读取。

    Args:
        skill_root: skill 根目录。
        project: 可选的项目目录。

    Returns:
        加载的配置 dict（同时也是 _ACTIVE_CONFIG）。
    """
    global _ACTIVE_SKILL_ROOT, _ACTIVE_PROJECT, _ACTIVE_CONFIG
    _ACTIVE_SKILL_ROOT = skill_root
    _ACTIVE_PROJECT = project
    _ACTIVE_CONFIG = load_config(skill_root, project)
    return _ACTIVE_CONFIG


def get(section: str, key: str, fallback: str | None = None) -> str | None:
    """从活动配置读取（需先调用 init_config）。"""
    if _ACTIVE_CONFIG is None:
        # 自动初始化（兼容未显式调用 init_config 的旧代码路径）
        init_config(_resolve_skill_root_auto())
    try:
        val = _ACTIVE_CONFIG.get(section, {}).get(key)  # type: ignore
        if val and isinstance(val, str):
            return val.strip()
    except (KeyError, TypeError, AttributeError):
        pass
    return fallback


def _legacy(file_path: str, env_var: str) -> str | None:
    """向下兼容的文件/环境变量读取。

    用于共享凭证（~/.agnes-api-key 等），非平台级配置。
    两平台共用同一 Agnes 账号时读同一文件不冲突。
    """
    path = os.path.expanduser(file_path)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    return os.environ.get(env_var)


def _resolve_skill_root_auto() -> str:
    """自动解析 skill 根目录（用于 get() 的自动初始化）。"""
    from _paths import resolve_skill_root
    return resolve_skill_root()


# ── 工具函数（无状态，纯函数）──

def _aspect_to_size(aspect: str) -> str:
    """映射 script.aspect_ratio 到尺寸参数。"""
    return {"9:16": "720x1280", "16:9": "1280x720", "1:1": "720x720"}.get(aspect, "1024x1024")


def _auto_size(project: str) -> str:
    """从 script.json 的 aspect_ratio 自动映射尺寸。"""
    sp = os.path.join(project, "script.json")
    if not os.path.isfile(sp):
        return "1024x1024"
    with open(sp, encoding="utf-8") as f:
        scr = json.load(f)
    return _aspect_to_size(scr.get("script", {}).get("aspect_ratio", ""))


def _parse_shot_range(s: str) -> list[int]:
    """解析 shot 范围字符串为 ID 列表。如 '2-9' → [2,3,...,9]"""
    result: set[int] = set()
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                lo, hi = int(a.strip()), int(b.strip())
                result.update(range(lo, hi + 1))
            except ValueError:
                continue
        else:
            try:
                result.add(int(part))
            except ValueError:
                continue
    return sorted(result)


def _safe_write_json(path: str, data: dict) -> None:
    """JSON 安全写入：先写临时文件再 rename。"""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _progress_str(idx: int, total: int) -> str:
    """进度字符串，如 [2/8]"""
    return f"[{idx + 1}/{total}]"


def _resolve_generation_refs(project: str, ref: dict) -> list[str]:
    """从 generation.reference_images 解析参考图路径。"""
    paths: list[str] = []

    def _has_path(entry: dict) -> str | None:
        p = entry.get("path", "")
        if p and isinstance(p, str):
            if os.path.isfile(p if os.path.isabs(p) else os.path.join(project, p)):
                return p
        return None

    def _semantic_paths(entry: dict) -> list[str]:
        r: list[str] = []
        scene = entry.get("scene", "")
        if scene and isinstance(scene, str):
            nm = scene.replace("/", "_")
            sd = os.path.join(project, "images", "scenes")
            if os.path.isdir(sd):
                for f in sorted(os.listdir(sd)):
                    if f.startswith(nm) and f.endswith(".png"):
                        r.append(f"images/scenes/{f}")
                        break
        troop = entry.get("troop", "")
        if troop and isinstance(troop, str):
            tp = f"images/troops/{troop}.png"
            if os.path.isfile(os.path.join(project, tp)):
                r.append(tp)
        for c in (entry.get("characters") or []):
            if isinstance(c, str):
                cp = f"images/characters/{c}.png"
                if os.path.isfile(os.path.join(project, cp)):
                    r.append(cp)
        return r

    kf_keys = sorted([k for k in ref if k.startswith("kf") and k[2:].isdigit()], key=lambda k: int(k[2:]))
    if kf_keys:
        for key in kf_keys:
            entry = ref[key]
            if not isinstance(entry, dict):
                continue
            pp = _has_path(entry)
            if pp:
                paths.append(pp)
                continue
            paths.extend(_semantic_paths(entry))
        if paths:
            return paths

    if isinstance(ref, dict):
        pp = _has_path(ref)
        if pp:
            return [pp]
        paths = _semantic_paths(ref)
        if paths:
            return paths

    return paths
