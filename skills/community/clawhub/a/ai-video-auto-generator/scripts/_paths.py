"""
三层路径模型 — Layer 1：Skill 根目录定位（与安装平台无关）
========================================================

核心原则：执行路径即身份。
不依赖全局环境变量，不绑定 .workbuddy / .codex 等平台目录名。
每个进程的 __file__ 不同 → 找到的 skill_root 不同 → 配置天然隔离。
可以用三个平台同时跑三个不同的项目，互不干扰。

用法:
    from _paths import resolve_skill_root, skill_paths
    root = resolve_skill_root()          # 从调用者 __file__ 向上找 SKILL.md
    paths = skill_paths()                # 返回 skill 内关键入口路径
"""

import os


def resolve_skill_root(start: str | None = None) -> str:
    """从任意子脚本位置向上找 skill 根目录，与安装平台无关。

    谁在调用，就解析到谁的那份安装目录。
    WorkBuddy 调用 → .../workbuddy/skills/xxx/
    Codex 调用     → .../codex/skills/xxx/
    OpenCode 调用  → .../opencode/skills/xxx/

    Args:
        start: 起始目录（默认 __file__ 所在目录）。

    Returns:
        skill 根目录的绝对路径。

    Raises:
        RuntimeError: 向上搜索 10 层仍未找到 SKILL.md。
    """
    cur = os.path.abspath(start or os.path.dirname(__file__))
    for _ in range(10):
        if os.path.isfile(os.path.join(cur, "SKILL.md")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    raise RuntimeError(
        f"无法定位 skill 根目录（从 {start or os.path.dirname(__file__)} 向上 "
        f"10 层未找到 SKILL.md）"
    )


def skill_paths(start: str | None = None) -> dict[str, str]:
    """返回 skill 内各关键入口的绝对路径。"""
    root = resolve_skill_root(start)
    pg = os.path.join(root, "skills", "project-generate", "scripts")
    return {
        "root": root,
        "pipeline": os.path.join(pg, "pipeline.py"),
        "project_generate": os.path.join(pg, "project_generate.py"),
        "create_project": os.path.join(root, "scripts", "create_project.py"),
        "sample": os.path.join(root, "sample"),
    }


# ── 配置加载（与路径走，不依赖全局 env）──

def find_config_files(
    skill_root: str,
    project: str | None = None,
) -> list[str]:
    """按优先级返回候选配置文件路径。

    优先级（高 → 低）:
        1. <project>/config/keys.env           ← 当前视频项目专属
        2. <project>/config/config.toml
        3. <skill_root>/config/keys.env        ← 当前平台这份 skill 专属
        4. <skill_root>/config/config.toml

    不读全局 ~/.workbuddy/config.toml —— 那是 WorkBuddy 专属路径，
    不应该被其他平台读取。各平台读各自 skill_root/config/ 下的配置。

    Args:
        skill_root: skill 根目录（resolve_skill_root 返回值）。
        project: 可选的项目目录（--project 参数值）。

    Returns:
        候选路径列表（高优先级在前）。
    """
    candidates: list[str] = []

    # 1-2) 项目级配置（最优先）
    if project:
        candidates.append(os.path.join(project, "config", "keys.env"))
        candidates.append(os.path.join(project, "config", "config.toml"))

    # 3-4) 当前平台这份 skill 的配置
    candidates.append(os.path.join(skill_root, "config", "keys.env"))
    candidates.append(os.path.join(skill_root, "config", "config.toml"))

    return candidates


def find_first_config(skill_root: str, project: str | None = None) -> str | None:
    """返回第一个存在的配置文件路径。"""
    for path in find_config_files(skill_root, project):
        if os.path.isfile(path):
            return path
    return None


# ── 工具路径解析（vendor / tools.toml / PATH / legacy fallback）──

def has_legacy_marker(skill_root: str) -> bool:
    """检查 skill_root 内是否有 .legacy-workbuddy 标记文件。

    只有在旧 WorkBuddy 环境中迁移时才存在此标记。
    标记存在时，配置/工具路径可 fallback 到 ~/.workbuddy/。
    """
    return os.path.isfile(os.path.join(skill_root, ".legacy-workbuddy"))


def resolve_tool(tool: str, skill_root: str) -> str | None:
    """查找工具（ffmpeg / node 等）的可执行文件路径。

    优先级链（由高到低）：
        1. <skill_root>/vendor/<tool>/                   ← 随 skill 打包
        2. <skill_root>/config/tools.toml                ← 这份 skill 声明的路径
        3. 系统 PATH                                     ← 用户自己装的
        4. (仅 legacy 标记) ~/.workbuddy/binaries/<tool>/ ← 旧 WorkBuddy 环境

    Args:
        tool: 工具名（如 "ffmpeg" / "node"）。
        skill_root: skill 根目录。

    Returns:
        可执行文件的绝对路径，未找到则返回 None。
    """
    # 1) skill 内 vendor/
    vendor_dir = os.path.join(skill_root, "vendor", tool)
    if os.path.isdir(vendor_dir):
        # 查找可执行文件
        for name in (tool + ext for ext in ("", ".exe", ".cmd", ".bat")):
            exe = os.path.join(vendor_dir, name)
            if os.path.isfile(exe):
                return os.path.abspath(exe)
        # 也可能在 vendor/tool/bin/ 下
        bin_dir = os.path.join(vendor_dir, "bin")
        if os.path.isdir(bin_dir):
            for name in (tool + ext for ext in ("", ".exe", ".cmd", ".bat")):
                exe = os.path.join(bin_dir, name)
                if os.path.isfile(exe):
                    return os.path.abspath(exe)

    # 2) config/tools.toml
    tools_cfg = os.path.join(skill_root, "config", "tools.toml")
    if os.path.isfile(tools_cfg):
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                tomllib = None
        if tomllib:
            try:
                with open(tools_cfg, "rb") as f:
                    cfg = tomllib.load(f)
                rel_path = cfg.get("tools", {}).get(tool, "")
                if rel_path and isinstance(rel_path, str):
                    abs_path = os.path.normpath(os.path.join(skill_root, rel_path))
                    if os.path.isfile(abs_path):
                        return abs_path
            except Exception:
                pass

    # 3) 系统 PATH
    exe = _which(tool)
    if exe:
        return exe

    # 4) legacy fallback（仅当有 legacy 标记时）
    if has_legacy_marker(skill_root):
        legacy_dir = os.path.expanduser(f"~/.workbuddy/binaries/{tool}")
        if os.path.isdir(legacy_dir):
            for name in (tool + ext for ext in ("", ".exe", ".cmd", ".bat")):
                exe = os.path.join(legacy_dir, name)
                if os.path.isfile(exe):
                    return exe

    return None


def resolve_ffmpeg(skill_root: str) -> str | None:
    """查找 ffmpeg 可执行文件（resolve_tool 的 ffmpeg 特化）。"""
    return resolve_tool("ffmpeg", skill_root)


def resolve_ffprobe(skill_root: str) -> str | None:
    """查找 ffprobe 可执行文件。"""
    result = resolve_tool("ffprobe", skill_root)
    if result:
        return result
    # ffprobe 可能跟 ffmpeg 在同一目录
    ffmpeg = resolve_ffmpeg(skill_root)
    if ffmpeg:
        probe = ffmpeg.replace("ffmpeg", "ffprobe")
        if os.path.isfile(probe):
            return probe
    return None


def resolve_node(skill_root: str) -> str | None:
    """查找 node 可执行文件。"""
    return resolve_tool("node", skill_root)


def resolve_node_modules(skill_root: str) -> str | None:
    """查找 node_modules 目录。

    优先级：
        1. <skill_root>/vendor/node/node_modules/
        2. <skill_root>/node_modules/
        3. 系统默认（npm root -g 输出）
    """
    candidates = [
        os.path.join(skill_root, "vendor", "node", "node_modules"),
        os.path.join(skill_root, "node_modules"),
    ]
    for p in candidates:
        if os.path.isdir(p):
            return os.path.abspath(p)

    # 系统默认
    try:
        import subprocess
        r = subprocess.run(
            ["npm", "root", "-g"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            return os.path.normpath(r.stdout.strip())
    except Exception:
        pass

    return None


# ── 内部工具 ──────────────────────────────────────

def _which(name: str) -> str | None:
    """检查系统 PATH 中是否存在指定可执行文件。"""
    import shutil
    exe = shutil.which(name)
    if exe:
        return os.path.abspath(exe)

    # Windows 下尝试带扩展名
    if os.name == "nt":
        for ext in (".exe", ".cmd", ".bat"):
            exe = shutil.which(name + ext)
            if exe:
                return os.path.abspath(exe)
    return None
