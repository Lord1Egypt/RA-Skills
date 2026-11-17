# -*- coding: utf-8 -*-
"""adapters/dumate.py — 百度搭子（DuMate）数据源适配器

把百度搭子桌面客户端（qianfan-desktop-app / DuMate）的本地用量数据归一化为
agent-analytics-report 的统一 trace / session schema，复用同一套聚合与报告
渲染逻辑。

背景（数据归属未证实）
  百度搭子客户端当前的数据**按 WorkBuddy 的布局**落在 `~/.workbuddy`，本适配器
  因此按 WorkBuddy 那套路径常量读取该目录：
    - ~/.workbuddy/traces/<pid>/trace_*.json   （token / 模型 / 时长）
    - ~/.workbuddy/workbuddy.db                 （会话 / 自动化 / 信用）
    - ~/.workbuddy/usage-log.json               （技能使用记录）
    - ~/.workbuddy/projects/ + sessions/        （会话转录定位）
    - ~/WorkBuddy/<会话目录>                     （产出文件 / 记忆日志）
  ⚠️**数据归属未证实**：这些记录里没有任何字段能区分它来自百度搭子还是
  WorkBuddy。本机 `workbuddy.db` 的 217 个会话中，cwd / title 匹配
  qianfan / dumate 关键词命中 0 行、`id LIKE 'ses_%'` 命中 0 行；1165 个
  trace 里既无 `ses_` 形态的 sessionId，也没有任何归属字段。百度搭子自己的
  数据落在 `~/.qianfan/workspace/.../.dumate/ses_*/flows/*.yml`，是 yml 流转
  格式，不是本技能的 trace schema。也就是说 `--source dumate` 跑出来的内容
  **可能完全是 WorkBuddy 的**。详细边界见 docs/ADAPTERS.md §6.4。
  所以本适配器的定位是「读取 WorkBuddy 布局目录的通用入口」，**归属由使用者
  自行确认**；不作为「已验证支持百度搭子」的能力对外承诺。

  那适配器还有什么用？三个职责，缺一不可：
    1. **显式声明口径**：`--source dumate` 让报告标题 / 来源清单显示
       「百度搭子」，标明本次采集走的是这个入口，而不是借 workbuddy 的名义
       冒充另一份数据源——它并不证明数据是百度搭子的；
    2. **路径隔离**：支持 `DUMATE_HOME` 环境变量覆盖数据目录（默认
       ~/.workbuddy），另可用 `DUMATE_OUTPUTS_DIR` 单独覆盖产出 / 记忆目录。
       若 dumate 更换数据布局 / 迁移目录，或在多账号场景下，只需在该适配器
       内部重映射路径，不改采集器与报告端；
    3. **可测试隔离**：测试通过 `DUMATE_HOME` 把 fixture 指向 tmp_path，
       绝不读取用户真实目录（与 CLAUDE_PROJECTS_DIR / QWENWORK_HOME 同约定）。

实现方式
  采集链路既然读的是 WorkBuddy 那套布局常量，直接复用 ca_sources 的函数
  （collect_db_data / collect_traces / collect_skill_usage /
  collect_session_outputs）。ca_sources 的路径常量是模块级名字，因此
  collect_dumate 在调用前临时替换 ca_sources 模块命名空间里的路径常量，
  调用结束后恢复 —— 与 qwenwork / claude-code 适配器「自带路径解析」相比，
  本适配器把「路径可变」做在模块名字层，改动面最小，且不触碰
  collect_usage_data.py 的 workbuddy 默认分支。
"""

import contextlib
import os
import sqlite3
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import ca_sources as cs  # noqa: E402
from ca_core import ts_to_date  # noqa: E402

__all__ = [
    "DUMATE_HOME",
    "SUPPORTS_COST",
    "collect_dumate",
    "resolve_dumate_home",
]

# 显式能力声明：token 为上游回传真值（读的是 WorkBuddy 的 traces，非本地估算），
# 成本可走静态价表估算（L2），支持 `--import-official` 对账或直接计价。
# ⚠️ 与「是否支持百度搭子」无关——数据归属未证实，见模块 docstring 与 §6.4。
SUPPORTS_COST = True

# ca_sources 中依赖 ~/.workbuddy 布局的模块级路径常量（collect_dumate
# 切换数据目录时逐项替换；key ∈ ca_sources 模块命名空间）。
_PATH_ATTRS = (
    "WB_DIR",
    "TRACES_DIR",
    "SESSIONS_DIR",
    "PROJECTS_DIR",
    "DB_PATH",
    "USAGE_LOG_PATH",
    "WORKBUDDY_SESSIONS",
)


def resolve_dumate_home():
    """定位百度搭子数据目录。

    优先级：
      1. 环境变量 DUMATE_HOME —— 直接指向主目录（测试 fixture / 多账号）
      2. 平台默认：~/.workbuddy（当前按 WorkBuddy 布局读取的目录，归属未证实）
    返回 Path；目录可能不存在（未使用过百度搭子），调用方负责判空。
    """
    env = os.environ.get("DUMATE_HOME")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".workbuddy"


def _child_paths(home):
    """由数据目录推导出 ca_sources 全套路径常量（与 ca_core 中默认布局一一对应）。

    ⚠️ 注意最后一项：产出 / 记忆日志的会话目录**不直接取 `Path.home()`**，
    而是过 `_resolve_outputs_dir()` —— 优先 `$DUMATE_OUTPUTS_DIR`，否则由
    home 的 parent 派生（dumate 的 home 默认 `~/.workbuddy`，parent 正是
    WorkBuddy 主目录）。若这里写死 `Path.home() / "WorkBuddy"`，把
    DUMATE_HOME 指到临时目录时 outputs / memory_logs 仍会读回用户真实目录，
    隔离就名存实亡了（audit hook 实测抓到 17 次真实 HOME 访问）。
    """
    home = Path(home)
    return {
        "WB_DIR": home,
        "TRACES_DIR": home / "traces",
        "SESSIONS_DIR": home / "sessions",
        "PROJECTS_DIR": home / "projects",
        "DB_PATH": home / "workbuddy.db",
        "USAGE_LOG_PATH": home / "usage-log.json",
        # 产出 / 记忆日志的会话目录按 WorkBuddy 约定在 HOME 的同级 WorkBuddy 下；
        # DUMATE_HOME=<x>/.workbuddy 时 parent 即 <x>，还原 ca_core 的默认位置。
        "WORKBUDDY_SESSIONS": _resolve_outputs_dir(home),
    }


def _resolve_outputs_dir(home):
    """产出 / 记忆日志的会话目录：DUMATE_OUTPUTS_DIR 优先，否则 home 的同级 WorkBuddy。

    dumate 的 home 默认是 `~/.workbuddy`，其 parent 恰好是 WorkBuddy 主目录，
    因此默认分支从 home 派生而非 `Path.home()`，这样 DUMATE_HOME 指向临时目录
    时也会跟着隔离（默认 outputs 落到 <tmp>/WorkBuddy）。
    """
    env = os.environ.get("DUMATE_OUTPUTS_DIR")
    if env:
        return Path(env).expanduser()
    return Path(home).parent / "WorkBuddy"


@contextlib.contextmanager
def _patched_paths(home):
    """临时把 ca_sources 的路径常量指向 dumate 数据目录，用完恢复。

    用于支持 DUMATE_HOME 覆盖，同时保证多次调用之间无全局状态残留。
    """
    new_paths = _child_paths(home)
    saved = {name: getattr(cs, name) for name in _PATH_ATTRS}
    try:
        for name, value in new_paths.items():
            setattr(cs, name, value)
        yield
    finally:
        for name, value in saved.items():
            setattr(cs, name, value)


def _supplement_out_of_window_sessions(home, traces, sessions_by_id):
    """补全窗口内有 trace、但会话创建于窗口外的会话（与 workbuddy 分支同款修复）。

    确保 token 统计能关联到任务类型，且 sid_to_rawmodel 含这些会话的通道
    真相（sessions.model 带接口通道前缀），避免通道误判。
    """
    trace_sids = {t.get("session_id") for t in traces if t.get("session_id")}
    missing = trace_sids - set(sessions_by_id)
    if not missing:
        return []
    db_path = Path(home) / "workbuddy.db"
    if not db_path.exists():
        return []
    rows = []
    # 只读打开：WAL 模式下可写连接会额外创建 -wal / -shm，且客户端持锁时
    # 可写连接会抛 SQLITE_BUSY。参照 adapters/qwenwork.py 的 _db_connect。
    cdb = None
    try:
        uri = "file:" + str(db_path).replace("\\", "/") + "?mode=ro"
        cdb = sqlite3.connect(uri, uri=True, timeout=1.0)
        cdb.row_factory = sqlite3.Row
        ph = ",".join("?" * len(missing))
        rows = cdb.execute(
            "SELECT * FROM sessions WHERE id IN ({}) AND deleted_at IS NULL".format(ph),
            list(missing),
        ).fetchall()
    except (sqlite3.Error, OSError):
        return []
    finally:
        if cdb is not None:
            cdb.close()
    return [
        {
            "id": r["id"],
            "cwd": r["cwd"],
            "title": r["title"] or "",
            "custom_title": r["custom_title"] or "",
            "status": r["status"],
            "created_at": r["created_at"],
            "created_date": ts_to_date(r["created_at"]),
            "updated_at": r["updated_at"],
            "mode": r["mode"],
            "model": r["model"],
            "is_background_automation": bool(r["is_background_automation"]),
        }
        for r in rows
    ]


def collect_dumate(start_date, end_date):
    """一次性返回 (traces, db_data)，供 collect_usage_data.py --source dumate 使用。

    trace 与 db_data 的 schema 与 WorkBuddy 源一致（读的是同一套路径常量）。
    ⚠️ 但**数据归属未证实**：这些记录可能全部来自 WorkBuddy，见模块 docstring。
      - sessions / automation_runs / session_credits 来自 workbuddy.db
      - traces 来自 traces/<pid>/trace_*.json（含补全会话后的通道重关联）
      - skill_usage 来自 usage-log.json
      - outputs / memory_logs 来自 DUMATE_OUTPUTS_DIR（默认 home 的同级
        WorkBuddy 目录）下的会话目录，不是 home 内部
    """
    home = resolve_dumate_home()
    with _patched_paths(home):
        db_data = cs.collect_db_data(start_date, end_date)
        sid_to_rawmodel = {
            s["id"]: (s.get("model") or "default") for s in db_data["sessions"]
        }
        traces = cs.collect_traces(start_date, end_date, sid_to_rawmodel)

        # 补全窗口外会话（与 workbuddy 分支同款修复），然后重采 trace
        extra = _supplement_out_of_window_sessions(
            home, traces, {s["id"] for s in db_data["sessions"]}
        )
        for s in extra:
            db_data["sessions"].append(s)
        for s in db_data["sessions"]:
            sid_to_rawmodel.setdefault(s["id"], s.get("model") or "default")
        traces = cs.collect_traces(start_date, end_date, sid_to_rawmodel)

        skill_usage = cs.collect_skill_usage(start_date, end_date)
        outputs, memory_logs = cs.collect_session_outputs(start_date, end_date)

    db_data["skill_usage"] = skill_usage
    db_data["outputs"] = outputs
    db_data["memory_logs"] = memory_logs
    return traces, db_data


DUMATE_HOME = resolve_dumate_home()
