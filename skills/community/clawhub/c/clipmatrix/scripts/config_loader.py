"""
Panda Workflow 配置加载器
读取 config.yaml，环境变量覆盖，零硬编码
"""
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

_CFG = {}

def _find_project_dir() -> Path:
    """自动探测项目根目录（往上找 config.yaml）"""
    d = Path.cwd()
    for _ in range(10):
        if (d / "config.yaml").exists():
            return d
        if d.parent == d:
            break
        d = d.parent
    # fallback: scripts 的父目录
    return Path(__file__).resolve().parent.parent


def load_config(config_path: str = None) -> dict:
    """加载 config.yaml，环境变量优先"""
    global _CFG
    if _CFG:
        return _CFG

    if config_path:
        cfg_file = Path(config_path)
    else:
        cfg_file = _find_project_dir() / "config.yaml"

    if not cfg_file.exists():
        raise FileNotFoundError(
            f"config.yaml not found. Create one at {cfg_file.parent}")

    # 支持 yaml 或 json
    if yaml:
        with open(cfg_file) as f:
            cfg = yaml.safe_load(f)
    else:
        import json
        with open(cfg_file) as f:
            cfg = json.load(f)

    # --- 环境变量覆盖 ---
    # DeepSeek
    cfg.setdefault("api", {}).setdefault("deepseek", {})
    if os.environ.get("DEEPSEEK_API_KEY"):
        cfg["api"]["deepseek"]["api_key"] = os.environ["DEEPSEEK_API_KEY"]
    if os.environ.get("DEEPSEEK_BASE_URL"):
        cfg["api"]["deepseek"]["base_url"] = os.environ["DEEPSEEK_BASE_URL"]

    # Metricool
    cfg["api"].setdefault("metricool", {})
    if os.environ.get("METRICOOL_TOKEN"):
        cfg["api"]["metricool"]["token"] = os.environ["METRICOOL_TOKEN"]
    if os.environ.get("METRICOOL_USER_ID"):
        cfg["api"]["metricool"]["user_id"] = os.environ["METRICOOL_USER_ID"]

    # Feishu
    cfg.setdefault("feishu", {})
    for k in ("app_id", "app_secret", "open_id"):
        env_key = f"FEISHU_{k.upper()}"
        if os.environ.get(env_key):
            cfg["feishu"][k] = os.environ[env_key]

    # 路径
    project_dir = Path(cfg.get("paths", {}).get("project_dir", "") or
                       str(cfg_file.parent))
    cfg["paths"] = cfg.get("paths", {})
    for key in ("output_dir", "library_dir", "workspace_dir",
                "config_dir", "templates_dir", "sounds_dir", "gaps_dir"):
        cfg["paths"][key] = str(project_dir / cfg["paths"].get(key, key))

    cfg["paths"]["project_dir"] = str(project_dir)

    _CFG = cfg
    return cfg


# --- 便捷访问 ---

def get(key_path: str, default=None):
    """点号分隔获取配置值，如 'api.deepseek.model'"""
    cfg = load_config()
    parts = key_path.split(".")
    v = cfg
    for p in parts:
        if isinstance(v, dict):
            v = v.get(p)
        else:
            return default
    return v if v is not None else default


def get_path(key_parts: str) -> str:
    """获取路径（相对于project_dir）"""
    return get(f"paths.{key_parts}", "")


def project_dir() -> str:
    return get("paths.project_dir", "")


def output_dir(account_id: str = None) -> str:
    d = get("paths.output_dir", "output")
    if account_id:
        d = os.path.join(d, account_id)
    return d


def library_dir() -> str:
    return get("paths.library_dir", "")


# 自动加载（import时）
try:
    load_config()
except FileNotFoundError:
    pass
