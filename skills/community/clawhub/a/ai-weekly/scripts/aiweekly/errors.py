"""aiweekly.errors — 人话错误码体系（P1-4：错误提示人性化）。

设计原则：
- 每个可预见的失败路径一个 ERR-* 代码（短、稳定、可检索）
- 默认输出「用户可见」层：emoji + 代码 + 人话描述 + 解决步骤
- 开启 --verbose / DEBUG 时才输出开发者层（原始异常 + 堆栈）
- 日志层（写入 .run.log）始终完整记录

用法：
    raise UserFacingError("ERR-GH-PAT-001",
        title="GitHub Pages 部署失败",
        steps=["去 https://github.com/settings/tokens 重新生成 PAT",
               "勾选 repo + pages:write",
               "将新 PAT 填入 scripts/deploy_ghpages.py 第 12 行"],
        verbose="git push 返回 403: token lacks pages:write scope")
"""
from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path
from typing import Sequence


# ---------------------------------------------------------------------------
# 错误码命名空间
# ---------------------------------------------------------------------------
# GH = GitHub / Pages 相关
# COS = 腾讯云 COS 相关
# FEISHU = 飞书推送相关
# CONFIG = 配置缺失 / 格式错误
# INPUT = 输入参数校验
# DEPLOY = 部署命令执行失败
# NETWORK = 网络抓取失败
ERR_GH_MISSING_PAT        = "ERR-GH-PAT-001"
ERR_GH_PAGES_SCOPE        = "ERR-GH-PAGES-002"
ERR_COS_MISSING_CONFIG    = "ERR-COS-CONF-001"
ERR_FEISHU_CONNECTOR_MISSING = "ERR-FS-CON-001"
ERR_INPUT_MISSING_FILE    = "ERR-INPUT-FILE-001"
ERR_NETWORK_TIMEOUT       = "ERR-NET-TIMEOUT-001"


# ---------------------------------------------------------------------------
# 异常类
# ---------------------------------------------------------------------------
class UserFacingError(RuntimeError):
    """人话错误：CLI main() 捕获后打印友好提示，--verbose 时追加堆栈。"""

    def __init__(
        self,
        code: str,
        title: str,
        steps: Sequence[str],
        *,
        verbose: str = "",
        log_extra: str = "",
    ):
        self.code = code
        self.title = title
        self.steps = list(steps)
        self.verbose = verbose
        self.log_extra = log_extra
        super().__init__(f"{code}: {title}")

    @property
    def human_message(self) -> str:
        lines = [f"\n❌ [{self.code}] {self.title}", ""]
        lines += [f"  {i+1}. {s}" for i, s in enumerate(self.steps)]
        if self.verbose and os.environ.get("DEBUG"):
            lines += ["", "  --- 调试信息（DEBUG=1）---"]
            lines.append(self.verbose)
        return "\n".join(lines)

    @property
    def log_message(self) -> str:
        parts = [str(self)]
        if self.verbose:
            parts.append(f"[verbose] {self.verbose}")
        if self.log_extra:
            parts.append(self.log_extra)
        parts.append(traceback.format_exc())
        return "\n".join(parts)


# ---------------------------------------------------------------------------
# 便捷工厂
# ---------------------------------------------------------------------------
def err_missing_file(path: Path) -> UserFacingError:
    return UserFacingError(
        ERR_INPUT_MISSING_FILE,
        f"文件不存在：{path.name}",
        [f"请确认路径正确：{path.resolve()}",
         "若刚下载/移动过该文件，重新指定 --html 参数"],
        verbose=f"os.path.exists({path!r}) == False",
    )


# ---------------------------------------------------------------------------
# 日志落盘（best-effort）
# ---------------------------------------------------------------------------
_LOG_PATH = Path.home() / ".aiweekly" / "run.log"


def write_log(line: str) -> None:
    try:
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass  # 日志落盘失败不干扰主流程


def print_error(exc: UserFacingError, *, file=sys.stderr) -> None:
    sys.stderr.write(exc.human_message + "\n")
    write_log(exc.log_message)
