"""
配置加载模块：环境变量与 .env 文件管理。

加载优先级（从高到低）：
  1. 进程启动时已有的环境变量（最高，永不被覆盖）
  2. 当前工作目录下的 .env        （项目级配置）
  3. ~/.config/milb-tracker/.env  （用户级配置）
  4. 内置默认值                    （最低）

用法：
    from milb_tracker.config import get_db_path, get_attachments_dir
    DB_PATH = get_db_path()
    ATTACHMENTS_DIR = get_attachments_dir()
"""

import os
from pathlib import Path

_env_loaded: bool = False


def _read_dotenv(path: Path) -> dict[str, str]:
    """解析 .env 文件，返回键值字典（不修改 os.environ）。"""
    result: dict[str, str] = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                # 去除可选的首尾引号
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                if key:
                    result[key] = value
    except OSError:
        pass
    return result


def load_env() -> None:
    """加载 .env 配置文件到 os.environ（幂等，多次调用只生效一次）。

    规则：
    - 进程启动前已存在的环境变量不会被任何 .env 覆盖
    - CWD/.env 优先于 ~/.config/milb-tracker/.env
    """
    global _env_loaded
    if _env_loaded:
        return
    _env_loaded = True

    # 快照进程原有的键（这些键不会被覆盖）
    original_keys: frozenset[str] = frozenset(os.environ.keys())

    user_env = Path.home() / ".config" / "milb-tracker" / ".env"
    cwd_env = Path.cwd() / ".env"

    # 读取两个文件，CWD 优先（后者覆盖前者相同的键）
    merged = _read_dotenv(user_env)
    merged.update(_read_dotenv(cwd_env))

    # 仅注入进程原本没有的键
    for key, value in merged.items():
        if key not in original_keys:
            os.environ[key] = value


def get_db_path() -> str:
    """返回数据库文件绝对路径（自动触发 .env 加载）。

    优先级：进程环境变量 > CWD/.env > ~/.config/milb-tracker/.env > 默认值
    默认值：{CWD}/data/bids.db
    """
    load_env()
    return os.environ.get("DB_PATH", str(Path.cwd() / "data" / "bids.db"))


def get_attachments_dir() -> str:
    """返回附件存储目录路径（自动触发 .env 加载）。

    优先级：进程环境变量 > CWD/.env > ~/.config/milb-tracker/.env > 默认值
    默认值：与 DB_PATH 同级的 attachments/ 子目录
    """
    load_env()
    default = str(Path(get_db_path()).parent / "attachments")
    return os.environ.get("ATTACHMENTS_DIR", default)
