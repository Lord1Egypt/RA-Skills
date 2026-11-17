#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
awam-todo —— 输入与管理 To-Do 的实现脚本。

职责：
  1. 把一条待办追加到按日期划分的存储文件 storage/YYYY-MM-DD.md
  2. 维护索引 index.json（待办 / 进行中 / 紧急 / 结束 / 归档文件）
  3. 支持完成 / 重新打开 / 标记进行中；某文件全部任务完成则自动标记归档
  4. 支持从自然语言解析时间（今天 / 明天 / 星期X / X天 / X小时 / 具体时间）作为兜底，
     主要语义解析由调用它的 Agent 在会话中完成。
  5. 存储格式带 schema 版本（文件头 `schema: N`，index.json 的 schema_version），
     旧版本用 `migrate` 迁移；按周统计一律以「周一」为起点。
  6. 进入新月份时，把上月及更早的「可归档日文件」合并进 storage/archive/YYYY-MM.md。
  7. 成功添加 / 维护待办后自动检查本地网页服务（web/server.py）是否在运行，未启动时
     弹框询问用户是否启动 UI（ui.port / ui.prompt 可配置，见下）。

用法示例：
  python todo.py add --text "撰写季度报告" --importance 重要 --due "2026-10-05 10:00"
  python todo.py add --text "背单词" --blocker "晚上刷手机" --counter "打开手机前先背 20 个"
  python todo.py add --text "预约体检" --urgent 紧急 --note "带身份证" --tags "健康;生活"
  python todo.py add --update-id T-20261002-001 --text "撰写季度报告"   # 确认后更新已有
  python todo.py add --force --text "撰写季度报告"                     # 跳过重复检测强制新建
  python todo.py check --text "撰写季度报告"                           # 只读查重
  python todo.py suggest-tags --text "背单词"                          # 只读推测标签（只建议，不写入）
  python todo.py list
  python todo.py list --state urgent
  python todo.py list --state overdue                                 # 逾期（带天数与出口提示）
  python todo.py done T-20261002-001
  python todo.py start T-20261002-001
  python todo.py reopen T-20261002-001
  python todo.py postpone T-20261002-001 "下周一"                      # 调整计划（改截止日）
  python todo.py postpone T-20261002-001 --clear                      # 取消截止日
  python todo.py dep T-20261002-001 --add T-20261002-003   # 设置依赖链
  python todo.py dep T-20261002-001                        # 查看依赖
  python todo.py add --text "子任务" --parent T-20261002-001   # 新增子任务（归属于主任务）
  python todo.py children T-20261002-001                   # 列出某主任务下的子任务
  python todo.py deparent T-20261002-003                   # 解除子任务归属
  python todo.py archive 2026-10-01                        # 强制归档某天
  python todo.py archive-month --dry-run                   # 预览月度归档
  python todo.py archive-month --month 2026-09             # 归档指定月份
  python todo.py migrate                                   # 预览 schema 迁移
  python todo.py migrate --apply                           # 执行迁移
  python todo.py show T-20261002-001
  python todo.py show 2026-09                              # 查看月度归档文件
  python todo.py index --rebuild

配置（存 env.json，用 `env` 命令查看 / 修改）：
  python todo.py init                                      # 探测环境（含编辑器）并写入 env.json
  python todo.py env                                       # 查看当前生效配置
  python todo.py env --set storage_dir="D:/awam-todo-data"                 # 改存储目录（旧目录有数据时要求二选一）
  python todo.py env --set storage_dir="D:/awam-todo-data" --migrate       # 连数据一起搬过去
  python todo.py env --set storage_dir="D:/awam-todo-data" --no-migrate    # 只改配置，不搬
  python todo.py env --set editor.path="D:/Apps/Cursor/Cursor.exe"         # 配置「用编辑器打开」用的编辑器
  python todo.py env --set editor.label="Cursor" --set "editor.args=--new-window"
  python todo.py env --set ui.port=9000                 # 网页 UI 服务端口（默认 8796）
  python todo.py env --set ui.prompt=off                # 维护后不弹框询问启动网页 UI
  python todo.py env --reset                               # 重新探测（含编辑器）
  python todo.py env --set path_style=windows              # 路径风格
  python todo.py env --set defaults.status=待开始          # 新增待办的默认值

两条可配置能力（技能需知晓，也是本脚本的对外契约）：
  1. storage_dir —— 待办数据放哪里。默认 <技能目录>/storage；改配置后所有读写
     （含 archive/ 月度归档、index.json 重建）都跟着走。搬数据必须显式选
     --migrate/--no-migrate，见 cmd_env()。
  2. editor —— 「用编辑器打开工作区」用哪个编辑器。未配置/路径失效时一律报错，
     不按软件名猜路径、不静默回退系统默认程序。见 resolve_editor() / open_editor()。

依赖链说明：
  - 通过 `dep`（或 `add --deps`）为任务标记前置依赖（任务 ID，用 ; 分隔）。
  - 依赖硬检查是死的：目标状态推进到「进行中/结束」时，若前置依赖未全部结束，
    脚本拒绝（exit 3）并列出冲突，提示 AI 向用户确认；用户确认后由 AI 以 --force 强制推进。
  - 设置依赖时会做存在性校验与循环依赖检测，成环/引用不存在任务直接报错。

子任务说明：
  - 通过 `add --parent <主任务ID>` 新增子任务；子任务拥有与其他任务相同的全部属性。
  - 父任务完成硬检查：把存在未完成子任务的任务标记为「结束」时，脚本拒绝（exit 3），
    交由 AI 向用户确认后决定是否 --force 强制结束；子任务全部完成后父任务才能正常结束。
  - 父子归属可嵌套但不得成环；`children <id>` 查看某主任务的子任务，`deparent <id>` 解除归属。

口径与不变量说明：
  - **周口径**：任何按周统计一律以「周一」为起点（WEEK_START_ISO=1），周一 00:00 至周日 23:59。
  - **月度归档**：进入新月份后，上月及更早的「全部任务已结束」的日文件会自动合并进
    storage/archive/YYYY-MM.md，原日文件删除；未完成的文件不动。可用 `archive-month` 手动触发。
  - **不推算原则**：缺失输入（无截止、无进展记录、样本不足）时派生指标一律返回 None，
    调用方渲染「—」或「暂无推算」，禁止用 0 或假日期顶替。
  - **置顶必带理由**：逾期 / 停滞 / 今日到期的任务会被置顶，并在索引里给出 pin_reason。
"""

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from difflib import SequenceMatcher

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 默认存储目录（技能根目录下的 storage/）。实际生效目录以 env.json 的 dirs.storage_dir 为准，
# 未配置时才回落到这里。见 _storage_dir()。
DEFAULT_STORAGE_DIR = os.path.join(SKILL_DIR, "storage")
INDEX_PATH = os.path.join(SKILL_DIR, "index.json")
ENV_PATH = os.path.join(SKILL_DIR, "env.json")

STATUS_MARKS = {"维护": "[ ]", "进行中": "[~]", "结束": "[x]", "待开始": "[ ]", "其他": "[ ]"}
STATUS_SET = set(STATUS_MARKS.keys())
DEFAULT_STATUS = "进行中"
IMPORTANCE_SET = {"重要", "不重要"}
DEFAULT_IMPORTANCE = "不重要"
URGENT_SET = {"紧急", "不紧急"}
DEFAULT_URGENT = "不紧急"

# 重复检测：相似度阈值（含边界）；exit 3 = 发现近似重复，需确认
SIMILAR_THRESHOLD = 0.72
EXIT_NEEDS_CONFIRM = 3

# ---- 存储格式版本与统计口径 ------------------------------------------------
# schema 版本：写入每个存储文件的头部（`schema: N`）与 index.json 的 schema_version。
# 旧文件（无 schema 行）一律视为 v1，用 `migrate` 升级到当前版本。
SCHEMA_VERSION = 2
# 周口径：一周从周一起算（isoweekday 1 = 周一）。所有按周统计统一用此口径，不得临时改。
WEEK_START_ISO = 1
# 停滞阈值（天）：进行中且距「更新（无则创建）」超过该天数 → 视为停滞，滚入今日
STALL_DAYS = 3
# 预计完成日所需的最小样本数（进展记录）。当前无进展记录层，恒为「暂无推算」。
PROJECTION_MIN_SAMPLES = 3
# 月度归档目录：<storage_dir>/archive/YYYY-MM.md，随存储目录走。见 _archive_dir()。

# ---- 网页 UI 服务（本地，web/server.py）----------------------------------
# 成功「添加 / 维护」一条待办后，检查本地网页服务是否在运行；未运行时按 ui.prompt
# 配置弹框询问用户是否启动 UI，用户选择启动则后台拉起服务并自动打开浏览器。
UI_DEFAULT_PORT = 8796             # 与 web/server.py 默认端口一致
UI_PROMPT_MODE_DEFAULT = "ask"     # ask=未启动时弹框询问；off=不检查不询问
# 触发检查的命令集合（只读命令一律不触发）。别名在 main() 里仍以输入名为 args.cmd，
# 因此 continue / reschedule / replan 也在集合内；dep 带改动参数时才触发（见 _ui_prompt_needed）。
UI_PROMPT_MUTATING_CMDS = ("add", "done", "start", "work", "continue", "reopen",
                           "postpone", "reschedule", "replan", "deparent")

# 旧值 -> 新枚举 的迁移映射（兼容历史存储文件）
_OLD_STATUS = {"open": "待开始", "in_progress": "进行中", "done": "结束"}
_OLD_IMPORTANCE = {"高": "重要", "中": "不重要", "低": "不重要"}

# ---- 标签推测（只给建议，不自动写入） --------------------------------------
# 原则：宁可不给建议，绝不给离谱建议。证据不足时返回空列表，由 AI 拿去问用户。
# 词表全部是中文常量，用不上的直接增删即可，不必改代码。
TAG_MAX_SUGGEST = 3          # 最多给几个建议
TAG_MIN_KEYWORD_LEN = 2      # 短于该长度的关键词不参与匹配，避免「的/了」这类误伤
TAG_MIN_SCORE = 1.0          # 低于该把握度不给建议
TAG_RULE_SCORE = 1.0         # 关键词规则命中一次的把握度
TAG_WORKSPACE_SCORE = 0.6    # 仅由工作空间路径给出的把握度（低于阈值，需搭配其它证据才出场）
TAG_HISTORY_BASE = 1.0       # 历史标签命中的基础把握度
TAG_HISTORY_MIN_SCORE = 0.34 # 与历史任务的相关度门槛
TAG_HISTORY_MIN_TOKENS = 2   # 共享片段数门槛：达到就算同类，避免被长句稀释掉（二者取其一）
# 内容/备注关键词 -> 建议标签（每条规则最多贡献一次，长句不会刷分）
TAG_RULES = (
    ("学习", ("学习", "背单词", "单词", "读书", "阅读", "课程", "课件",
             "刷题", "复习", "考研", "论文", "教程", "网课", "预习")),
    ("英语", ("english", "英语", "单词", "口语", "听力", "雅思", "托福")),
    ("开发", ("bug", "修复", "重构", "测试", "单测", "编码", "接口", "部署",
             "脚本", "函数", "依赖", "上线", "调试", "日志")),
    ("工作", ("会议", "汇报", "周报", "月报", "评审", "对齐", "客户", "绩效", "面试")),
    ("文档", ("文档", "readme", "笔记", "总结", "复盘", "说明书", "wiki")),
    ("健康", ("体检", "跑步", "健身", "睡觉", "作息", "医院", "吃药", "减肥")),
    ("生活", ("买菜", "打扫", "洗衣", "缴费", "房租", "快递", "快递取件")),
)
# 工作空间路径中的领域词 -> 建议标签（仅作辅助证据，单独命中不足以成建议）
TAG_WORKSPACE_RULES = (
    ("开发", ("src", "code", "dev", "repo", "project", "github", "gitlab")),
    ("学习", ("course", "learn", "study", "note", "notes", "book")),
    ("文档", ("doc", "docs", "wiki", "readme")),
    ("数据", ("data", "dataset", "db", "sql", "etl")),
    ("交易", ("stock", "trade", "quant", "futures")),
)


def _norm_status(v):
    v = _norm(v)
    if v in STATUS_SET:
        return v
    return _OLD_STATUS.get(v, "其他")


def _norm_importance(v):
    v = _norm(v)
    if v in IMPORTANCE_SET:
        return v
    return _OLD_IMPORTANCE.get(v, DEFAULT_IMPORTANCE)


def _norm_urgent(v):
    v = _norm(v).lower()
    if v in ("紧急", "true", "1", "是"):
        return "紧急"
    return DEFAULT_URGENT

# ---- 时间解析（兜底） -----------------------------------------------------
_WEEKDAY = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6, "七": 6}


def _norm(s):
    return (s or "").strip()


def _parse_weekday_target(name, base):
    """解析 星期X/周X，返回落在 base 当天/之后的最近一天（datetime.date）。"""
    w = _WEEKDAY.get(name)
    if w is None:
        return None
    delta = (w - base.weekday()) % 7
    if delta == 0:
        delta = 7  # 今天不说“下周一”等，默认取未来最近一次
    return base + dt.timedelta(days=delta)


def parse_due(text, now=None):
    """把自然语言时间解析为 ISO 字符串（YYYY-MM-DD 或 YYYY-MM-DD HH:MM）。
    支持 今天/明天/后天、星期X/周X/下周X、M月D日、YYYY-MM-DD、X天后、
    HH:MM、X点(半)，以及“相对日期 + 时间”的组合（如 明天 10:00、周五 09:00）。
    解析不了返回 None。now 用于测试注入，默认取当前本地时间。"""
    s = _norm(text)
    if not s:
        return None
    now = now or dt.datetime.now()
    base = now.date()

    # 提取尾部时间部分：HH:MM 或 X点/点半
    time_part = None
    date_s = s
    m = re.search(r"(\d{1,2}):(\d{2})\s*$", s)
    if m:
        time_part = (int(m.group(1)), int(m.group(2)))
        date_s = s[:m.start()].strip()
    else:
        m = re.search(r"(\d{1,2})点(半)?\s*$", s)
        if m:
            time_part = (int(m.group(1)), 30 if m.group(2) else 0)
            date_s = s[:m.start()].strip()

    def fmt(d, t):
        if t is not None:
            return "%04d-%02d-%02d %02d:%02d" % (d.year, d.month, d.day, t[0], t[1])
        return "%04d-%02d-%02d" % (d.year, d.month, d.day)

    def date_of(ss):
        ss = _norm(ss)
        if not ss:
            return None
        m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", ss)
        if m:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.match(r"^(\d{1,2})月(\d{1,2})日$", ss)
        if m:
            return dt.date(base.year, int(m.group(1)), int(m.group(2)))
        if ss in ("今天", "今日"):
            return base
        if ss in ("明天", "明日"):
            return base + dt.timedelta(days=1)
        if ss == "后天":
            return base + dt.timedelta(days=2)
        if ss in ("昨天", "昨日"):
            return base - dt.timedelta(days=1)
        m = re.match(r"^下?(?:星期|周)([一二三四五六日天七])$", ss)
        if m:
            return _parse_weekday_target(m.group(1), base)
        m = re.match(r"^(\d+)\s*天(?:后)?$", ss)
        if m:
            return base + dt.timedelta(days=int(m.group(1)))
        return None

    # 纯时间（无日期词）→ 今天该时间
    if not date_s and time_part:
        return fmt(base, time_part)

    d = date_of(date_s)
    if d is None:
        return None
    return fmt(d, time_part)


def _fmt(d):
    return d.strftime("%Y-%m-%d %H:%M") if isinstance(d, dt.datetime) else d.strftime("%Y-%m-%d")


# ---- 工作环境识别与路径统一 ------------------------------------------------
# env.json 保存运行时环境与路径风格偏好；首次由 `init` 生成，`env` 命令查看/修改。
# 路径风格：
#   windows -> 工作空间统一为反斜杠 `G:\Projects\...`
#   posix   -> 工作空间统一为正斜杠 `G:/Projects/...`
#   mixed   -> 保持录入原样，不做转换
_PATH_STYLES = ("windows", "posix", "mixed")


def _read_saved_env():
    """读取磁盘上的 env.json；不存在或损坏返回 None（不做任何推断）。"""
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                env = json.load(f)
            if isinstance(env, dict):
                return env
        except Exception:
            pass
    return None


def _detect_env():
    """探测当前运行环境，返回环境信息 dict（不落盘）。

    存储目录与编辑器属于「用户配置」，探测不出来，改动 env.json 时原样保留：
    重新 `init` 不会把用户改过的 dirs.storage_dir / editor 冲掉。"""
    import platform
    import socket
    is_windows = os.name == "nt"
    default_style = "windows" if is_windows else "posix"
    saved = _read_saved_env() or {}
    dirs = saved.get("dirs") if isinstance(saved.get("dirs"), dict) else {}
    env = {
        "generated": _fmt(dt.datetime.now()),
        "path_style": default_style,
        "platform": {
            "os": platform.system() or ("Windows" if is_windows else "Unknown"),
            "os_name": os.name,
            "is_windows": is_windows,
            "path_sep": os.sep,
            "python_version": platform.python_version(),
            "hostname": socket.gethostname() if hasattr(socket, "gethostname") else "",
            "cwd": os.getcwd(),
        },
        "dirs": {"skill_dir": SKILL_DIR,
                 "storage_dir": _norm(dirs.get("storage_dir")) or DEFAULT_STORAGE_DIR},
    }
    if isinstance(saved.get("editor"), dict):
        env["editor"] = dict(saved["editor"])
    return env


def _load_env():
    """读取已保存的环境配置；不存在时按当前 OS 推断（不落盘）。"""
    env = _read_saved_env()
    if env is not None and env.get("path_style") in _PATH_STYLES:
        return env
    env = _detect_env()
    env["_inferred"] = True
    return env


def _save_env(env):
    os.makedirs(SKILL_DIR, exist_ok=True)
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        json.dump(env, f, ensure_ascii=False, indent=2)


def _script_cmd():
    """给用户看的操作提示里用的命令前缀（形如 python "<绝对路径>/todo.py"）。"""
    return 'python "%s"' % os.path.abspath(__file__)


def _storage_dir():
    """当前生效的存储目录：env.json 的 dirs.storage_dir；未配置时为技能根目录下 storage/。"""
    d = _norm((_load_env().get("dirs") or {}).get("storage_dir"))
    if not d:
        return DEFAULT_STORAGE_DIR
    return os.path.abspath(os.path.expanduser(d))


def _archive_dir():
    """生效存储目录下的月度归档目录。"""
    return os.path.join(_storage_dir(), "archive")


def _storage_file_stats(d):
    """统计目录下的日文件数与任务块数，用于搬迁前后校验。"""
    files = tasks = 0
    if not os.path.isdir(d):
        return 0, 0
    for fn in sorted(os.listdir(d)):
        if not re.match(r"^\d{4}-\d{2}-\d{2}\.md$", fn):
            continue
        files += 1
        with open(os.path.join(d, fn), "r", encoding="utf-8") as f:
            tasks += sum(1 for line in f if line.startswith("## T-"))
    return files, tasks


def _migrate_storage(old_dir, new_dir):
    """把旧存储目录的日文件与 archive/ 搬到新目录。

    先复制 -> 校验文件数与任务块数一致 -> 校验通过才删除旧文件；
    任何一步不通过都中止并保留旧目录，绝不出现两边都没有的数据状态。
    返回 (ok, msg)。
    """
    import shutil
    if os.path.abspath(old_dir) == os.path.abspath(new_dir):
        return True, "Same directory; nothing to migrate"
    old_files, old_tasks = _storage_file_stats(old_dir)
    if old_files == 0:
        return True, "Old directory has no todo files; nothing to migrate"
    os.makedirs(new_dir, exist_ok=True)
    created = []          # 本次新建的目标文件，失败时只回删这些，绝不动目标目录原有内容
    try:
        for fn in sorted(os.listdir(old_dir)):
            src = os.path.join(old_dir, fn)
            if os.path.isdir(src):
                if fn == "archive":
                    shutil.copytree(src, os.path.join(new_dir, fn), dirs_exist_ok=True)
                continue
            if fn.endswith(".md"):
                dst = os.path.join(new_dir, fn)
                if not os.path.exists(dst):
                    created.append(dst)
                shutil.copy2(src, dst)
    except Exception as e:  # noqa: BLE001
        for p in created:
            try:
                os.remove(p)
            except Exception:
                pass
        return False, "Copy failed; the old directory was kept intact (removed the %d target file(s) written this run): %s" % (len(created), e)
    new_files, new_tasks = _storage_file_stats(new_dir)
    if (new_files, new_tasks) != (old_files, old_tasks):
        removed = 0
        for p in created:
            try:
                os.remove(p)
                removed += 1
            except Exception:
                pass
        return False, ("Verification failed (old %d file(s)/%d todo(s) vs new %d file(s)/%d todo(s)); the old directory was "
                       "kept intact and the %d file(s) written this run were removed. If the new directory already "
                       "contains todo files, empty it or choose another directory."
                       % (old_files, old_tasks, new_files, new_tasks, removed))
    for fn in sorted(os.listdir(old_dir)):
        src = os.path.join(old_dir, fn)
        if os.path.isdir(src) or not fn.endswith(".md"):
            continue
        os.remove(src)
    return True, "Migrated %d file(s) (%d todo(s))" % (new_files, new_tasks)


# ---- 编辑器（env.json 的 editor 段） ---------------------------------------
# 只认三项：path（可执行文件/命令）、args（固定前置参数）、label（显示名，可省）。
# 解析原则：未配置或路径失效 -> 报错并停用相关入口，不按软件名猜路径、不静默回退。
def _editor_config():
    e = _load_env().get("editor")
    return e if isinstance(e, dict) else {}


def resolve_editor():
    """解析出可用的编辑器命令，返回 (cmd, error)。

    cmd 为可直接交给 subprocess.Popen 的列表（不含要打开的路径，调用方追加）；
    不可用（未配置 / 文件不存在 / 命令不在 PATH）时 cmd 为 None，error 为失败原因（英文）。"""
    e = _editor_config()
    raw = _norm(e.get("path"))
    if not raw:
        return None, "Editor not configured (env.json is missing editor.path)"
    path = os.path.expanduser(raw)
    seps = [s for s in (os.sep, os.altsep) if s]
    if os.path.isabs(path) or any(s in path for s in seps):
        if not os.path.isfile(path):
            return None, "Editor path invalid (file not found): %s" % raw
        cmd = [path]
    else:
        import shutil
        found = shutil.which(path)
        if not found:
            return None, "Editor command not found in PATH: %s" % raw
        cmd = [found]
    args = e.get("args")
    if isinstance(args, str):
        args = [x.strip() for x in args.split(";") if x.strip()]
    if not isinstance(args, list):
        args = []
    return cmd + [str(a) for a in args], None


def _editor_args_text():
    """把 editor.args 还原成 env --set 用的字符串（分号分隔）。"""
    args = _editor_config().get("args")
    if isinstance(args, str):
        return args.strip()
    if isinstance(args, list):
        return ";".join(str(a) for a in args)
    return ""


def editor_status():
    """给网页/索引用的编辑器可用性摘要。"""
    cmd, err = resolve_editor()
    label = _norm(_editor_config().get("label"))
    return {"configured": bool(_norm(_editor_config().get("path"))),
            "available": cmd is not None,
            "path": _norm(_editor_config().get("path")) or None,
            "label": label or None,
            "error": err}


def _launch_argv(cmd, target):
    """把编辑器命令 + 目标目录组装成可直接交给 Popen 的参数列表。

    Windows 上 .cmd / .bat 不是可执行映像，CreateProcess 无法直接启动，必须经 cmd.exe
    （Cursor 探测到的就往往是 cursor.CMD），否则报「不是有效的应用程序」。

    经 cmd.exe 的写法有两种坑，都已实测排除：
    - shell=True + 列表：cmd 会把 "/c" 当成脚本的第一个参数传进去（参数整体串位）。
    - 手工拼命令行字符串：路径里的空格 / 引号需要自己的转义规则，容易切碎参数。
    所以用 [comspec, "/c", 脚本, 参数...] 的列表形式，参数引用交给 subprocess 处理。"""
    argv = list(cmd) + [target]
    if os.name == "nt" and argv[0].lower().endswith((".cmd", ".bat")):
        comspec = os.environ.get("ComSpec") or "cmd.exe"
        return [comspec, "/c"] + argv
    return argv


def open_editor(target):
    """用配置好的编辑器打开目录（不等待退出）。返回 (ok, msg)。

    两点实现约束：
    1. 编辑器是 GUI 程序：启动时切断 stdio 并脱离进程组，避免它占住调用方的管道
       （否则 AI 调用 / 自测会一直等到编辑器退出）。
    2. 启动方式见 _launch_argv()：Windows 的 .cmd / .bat 必须经 cmd.exe。"""
    cmd, err = resolve_editor()
    if cmd is None:
        return False, err
    kwargs = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL,
              "stderr": subprocess.DEVNULL, "close_fds": True}
    if os.name == "nt":
        kwargs["creationflags"] = (getattr(subprocess, "DETACHED_PROCESS", 0)
                                  | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
    try:
        subprocess.Popen(_launch_argv(cmd, target), **kwargs)
    except Exception as e:  # noqa: BLE001
        return False, "Failed to launch editor: %s" % e
    return True, "Opened in editor"


# 常见编辑器探测表（按优先级从上到下，命中第一个即采用）。
# 想换成别的编辑器：直接在这张表里加一行，或用 `env --set editor.path=...` 显式指定。
# 探测不到时不写 editor 配置——不按名字猜路径，由用户显式配置。
EDITOR_CANDIDATES = (
    {"label": "Cursor", "cmd": "cursor", "paths": (
        r"%LOCALAPPDATA%\Programs\cursor\Cursor.exe",
        r"C:\Program Files\cursor\Cursor.exe",
        "/Applications/Cursor.app/Contents/MacOS/Cursor",
        "/usr/bin/cursor",
    )},
    {"label": "VS Code", "cmd": "code", "paths": (
        r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        "/Applications/Visual Studio Code.app/Contents/MacOS/Electron",
        "/usr/bin/code",
    )},
    {"label": "Trae", "cmd": "trae", "paths": (
        r"%LOCALAPPDATA%\Programs\Trae\Trae.exe",
        r"C:\Program Files\Trae\Trae.exe",
        "/Applications/Trae.app/Contents/MacOS/Trae",
    )},
    {"label": "Windsurf", "cmd": "windsurf", "paths": (
        r"%LOCALAPPDATA%\Programs\Windsurf\Windsurf.exe",
        r"C:\Program Files\Windsurf\Windsurf.exe",
        "/Applications/Windsurf.app/Contents/MacOS/Windsurf",
    )},
    {"label": "Sublime Text", "cmd": "subl", "paths": (
        r"C:\Program Files\Sublime Text\sublime_text.exe",
        "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl",
    )},
    {"label": "Zed", "cmd": "zed", "paths": (
        r"%LOCALAPPDATA%\Programs\Zed\Zed.exe",
        "/Applications/Zed.app/Contents/MacOS/zed",
        "/usr/bin/zed",
    )},
)


def _detect_editor():
    """探测本机可用的编辑器，返回 {"label","path","args"} 或 None（探测不到）。

    只做存在性判断，不启动任何进程。path 记实际命中的可执行文件，
    保证换机器/换版本后仍能用 env --set editor.path 覆盖。"""
    import shutil
    for cand in EDITOR_CANDIDATES:
        found = shutil.which(cand["cmd"])
        if found:
            return {"label": cand["label"], "path": found, "args": ""}
        for p in cand["paths"]:
            exp = os.path.expandvars(os.path.expanduser(p))
            if os.path.isfile(exp):
                return {"label": cand["label"], "path": exp, "args": ""}
    return None


def _get_path_style():
    return _load_env().get("path_style") or ("windows" if os.name == "nt" else "posix")


def _norm_path(p):
    """按当前 path_style 统一本地路径分隔符（仅用于工作空间等本地路径，不用于 URL）。"""
    p = _norm(p)
    if not p:
        return p
    style = _get_path_style()
    if style == "windows":
        return p.replace("/", "\\")
    if style == "posix":
        return p.replace("\\", "/")
    return p


# ---- 可覆盖的默认值（env.json -> defaults） ---------------------------------
# 原则：默认值只是「预填建议」，新建/网页表单都可用它预填，用户随时可覆盖。
# 例：env --set defaults.status=待开始   → 之后新增待办默认落在「待开始」。
DEFAULT_KEYS = ("status", "importance", "urgent")


def _default_of(key):
    """取某字段的默认值：优先 env.json 的 defaults.<key>，否则用内置常量。"""
    env = _load_env()
    d = env.get("defaults") or {}
    v = _norm(d.get(key))
    if key == "status":
        return v if v in STATUS_SET else DEFAULT_STATUS
    if key == "importance":
        return v if v in IMPORTANCE_SET else DEFAULT_IMPORTANCE
    if key == "urgent":
        return v if v in URGENT_SET else DEFAULT_URGENT
    return None


def _defaults_view():
    """返回当前生效的默认值（供网页表单预填）。"""
    return {k: _default_of(k) for k in DEFAULT_KEYS}


# ---- 存储文件读写 ---------------------------------------------------------
def _file_path(date):
    """date 为 'YYYY-MM-DD'。返回存储文件绝对路径。"""
    return os.path.join(_storage_dir(), date + ".md")


def _parse_from(v):
    """把 '来源' 行（`type|url`）解析为 {type,url} 对象；空则返回 None。"""
    v = _norm(v)
    if not v:
        return None
    if "|" in v:
        typ, _, url = v.partition("|")
        return {"type": _norm(typ) or None, "url": _norm(url) or None}
    return {"type": "link", "url": v}


def _parse_block(block_lines):
    """解析一个任务的 key: value 行列表为 dict。"""
    task = {"id": None, "status": DEFAULT_STATUS, "importance": DEFAULT_IMPORTANCE, "text": "",
            "note": "", "workspace": "", "docs": [], "links": [], "depends_on": [], "due": None,
            "created": None, "updated": None, "urgent": DEFAULT_URGENT, "from": None,
            "parent": "", "tags": [], "blocker": "", "counter": "", "origin_date": ""}
    for line in block_lines:
        line = line.strip()
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), _norm(v)
        if k == "状态":
            task["status"] = _norm_status(v.split()[-1])
        elif k == "重要":
            task["importance"] = _norm_importance(v)
        elif k == "内容":
            task["text"] = v
        elif k == "父任务":
            task["parent"] = v
        elif k == "备注":
            task["note"] = v
        elif k == "障碍":
            task["blocker"] = v
        elif k == "对策":
            task["counter"] = v
        elif k == "工作空间":
            task["workspace"] = _norm_path(v)
        elif k == "文档":
            task["docs"] = [x.strip() for x in v.split(";") if x.strip()]
        elif k == "链接":
            task["links"] = [x.strip() for x in v.split(";") if x.strip()]
        elif k == "依赖":
            task["depends_on"] = [x.strip() for x in v.split(";") if x.strip()]
        elif k == "标签":
            task["tags"] = [x.strip() for x in v.split(";") if x.strip()]
        elif k == "来源":
            task["from"] = _parse_from(v)
        elif k == "截止":
            task["due"] = v or None
        elif k == "创建":
            task["created"] = v or None
        elif k == "更新":
            task["updated"] = v or None
        elif k == "紧急":
            task["urgent"] = _norm_urgent(v)
        elif k == "原日期":
            # 仅月度归档文件中的任务带此行：记录它原来属于哪个日文件
            task["origin_date"] = v
    return task


def load_file(date):
    """读取存储文件，返回 {'archived': bool, 'schema': int, 'tasks': [dict,...]}；不存在则返回空。
    schema：文件头 `schema: N` 的值；缺失视为 v1（旧格式）。"""
    fp = _file_path(date)
    result = {"archived": False, "schema": 1, "tasks": []}
    if not os.path.exists(fp):
        return result
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    i = 0
    # 头：归档标记 + schema 版本
    while i < len(lines):
        line = lines[i].strip()
        if line == "---":
            i += 1
            break
        if line.startswith("归档:"):
            result["archived"] = _norm(line[3:]).lower() in ("true", "1", "是")
        elif line.startswith("schema:"):
            try:
                result["schema"] = int(_norm(line[7:]))
            except ValueError:
                result["schema"] = 1
        i += 1
    # 任务块（跳过空行，避免把空行误判成空任务块）
    blocks = []
    cur = []
    for line in lines[i:]:
        if not line.strip():
            continue
        if line.startswith("## "):
            if cur:
                blocks.append(cur)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)
    for blk in blocks:
        if not blk:
            continue
        body = blk[0][3:].strip()  # id
        tid = body.split(" ")[0] if body else None
        t = _parse_block(blk[1:])
        t["id"] = tid or t["id"]
        if t["id"]:
            result["tasks"].append(t)
    return result


def _write_block(t):
    lines = []
    lines.append("## %s" % t["id"])
    mark = STATUS_MARKS.get(t["status"], "[ ]")
    lines.append("状态: %s %s" % (mark, t["status"]))
    lines.append("重要: %s" % t["importance"])
    lines.append("紧急: %s" % t["urgent"])
    lines.append("内容: %s" % t["text"])
    if t.get("parent"):
        lines.append("父任务: %s" % t["parent"])
    if t.get("note"):
        lines.append("备注: %s" % t["note"])
    if t.get("blocker"):
        lines.append("障碍: %s" % t["blocker"])
    if t.get("counter"):
        lines.append("对策: %s" % t["counter"])
    if t.get("workspace"):
        lines.append("工作空间: %s" % t["workspace"])
    if t.get("docs"):
        lines.append("文档: %s" % "; ".join(t["docs"]))
    if t.get("links"):
        lines.append("链接: %s" % "; ".join(t["links"]))
    if t.get("depends_on"):
        lines.append("依赖: %s" % "; ".join(t["depends_on"]))
    if t.get("tags"):
        lines.append("标签: %s" % "; ".join(t["tags"]))
    if t.get("from") and (t["from"].get("type") or t["from"].get("url")):
        lines.append("来源: %s|%s" % (t["from"].get("type") or "",
                                      t["from"].get("url") or ""))
    if t.get("due"):
        lines.append("截止: %s" % t["due"])
    if t.get("created"):
        lines.append("创建: %s" % t["created"])
    if t.get("updated"):
        lines.append("更新: %s" % t["updated"])
    return "\n".join(lines)


def save_file(date, archived, tasks):
    """写回存储文件，保持 header（含 schema 版本）+ 任务块。"""
    fp = _file_path(date)
    os.makedirs(_storage_dir(), exist_ok=True)
    parts = ["# 待办 %s" % date,
             "归档: %s" % ("true" if archived else "false"),
             "schema: %d" % SCHEMA_VERSION,
             "---"]
    for t in tasks:
        parts.append("")
        parts.append(_write_block(t))
    with open(fp, "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")


def _next_id(date):
    data = load_file(date)
    base = date.replace("-", "")
    seq = 0
    for t in data["tasks"]:
        m = re.match(r"^T-%s-(\d+)$" % base, t["id"] or "")
        if m:
            seq = max(seq, int(m.group(1)))
    return "T-%s-%03d" % (base, seq + 1)


# ---- 索引 ---------------------------------------------------------------
def _due_value(due):
    """把 due 转成可比较的时间戳；解析失败返回 None。"""
    if not due:
        return None
    try:
        return dt.datetime.strptime(due, "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            return dt.datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            return None


def _is_urgent(t, now):
    """显式紧急，或截止在 24 小时内/已过期，视为紧急。"""
    if t.get("urgent") == "紧急":
        return True
    dv = _due_value(t.get("due"))
    if dv is None:
        return False
    return dv <= now + dt.timedelta(hours=24)


# ---- 派生指标（不落库，全部实时算出） --------------------------------------
# 不推算原则：输入缺失（无截止 / 已完成 / 样本不足）一律返回 None。
# 调用方（CLI / 网页）必须把 None 渲染成「—」或「暂无推算」，禁止用 0、假日期顶替。
def _days_unknown(v):
    """None -> '—'；否则原样返回（渲染层的统一兜底）。"""
    return "—" if v is None else v


def _due_in_days(t, now):
    """距截止还有几天（0 = 今天到期）；无截止或已完成返回 None。"""
    if t.get("status") == "结束":
        return None
    dv = _due_value(t.get("due"))
    if dv is None:
        return None
    return (dv.date() - now.date()).days


def _overdue_days(t, now):
    """逾期天数：仅当「未完成 + 截止已过（按自然日）」时返回 >=1 的整数，否则 None。
    今天到期但时刻已过不算逾期（避免输出「逾期 0 天」）。"""
    if t.get("status") == "结束":
        return None
    dv = _due_value(t.get("due"))
    if dv is None:
        return None
    days = (now.date() - dv.date()).days
    return days if days >= 1 else None


def _stall_days(t, now):
    """停滞天数：进行中且距「更新（无则创建）」>= STALL_DAYS 才返回天数，否则 None。"""
    if t.get("status") != "进行中":
        return None
    ref = _due_value(t.get("updated") or t.get("created"))
    if ref is None:
        return None
    days = (now.date() - ref.date()).days
    return days if days >= STALL_DAYS else None


def _projected_finish(t, now, samples=None):
    """预计完成日。需要「进展记录」样本 >= PROJECTION_MIN_SAMPLES 才推算；
    当前版本尚无进展记录层（见 优化建议.md 第 7/8 条），恒定返回 None → 渲染「暂无推算」。"""
    samples = samples or []
    if len(samples) < PROJECTION_MIN_SAMPLES:
        return None
    return None  # 预留：待记录层落地后按近 7 天均速推算


def _pin_info(t, now):
    """置顶信息与理由。返回 (rank, reason)；无理由返回 (None, None)。
    rank: 0=逾期（红） 1=停滞（琥珀，容错） 2=今天到期。
    置顶一定有理由——这是「为什么它在最前面」的唯一来源，不得静默重排。"""
    od = _overdue_days(t, now)
    if od is not None:
        return 0, "Overdue %d day(s), moved to today" % od
    sd = _stall_days(t, now)
    if sd is not None:
        return 1, "No progress for %d day(s), moved to today" % sd
    dd = _due_in_days(t, now)
    if dd == 0:
        return 2, "Due today"
    return None, None


def _week_bounds(d):
    """按「周一为起点」的口径返回 (周一 date, 周日 date)。d 为 date 或 datetime。"""
    day = d.date() if isinstance(d, dt.datetime) else d
    start = day - dt.timedelta(days=(day.isoweekday() - WEEK_START_ISO) % 7)
    return start, start + dt.timedelta(days=6)


def _scan_files():
    """返回 {date: {'archived':bool,'schema':int,'tasks':[...]}}，按日期升序。
    仅扫描 storage/YYYY-MM-DD.md（月度归档在 storage/archive/ 下，不参与日常索引）。"""
    if not os.path.isdir(_storage_dir()):
        return {}
    out = {}
    for fn in sorted(os.listdir(_storage_dir())):
        if not fn.endswith(".md"):
            continue
        date = fn[:-3]
        try:
            dt.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            continue
        out[date] = load_file(date)
    return out


# ---- 月度归档（storage/archive/YYYY-MM.md） ---------------------------------
# 规则：进入新月份后，把「上月及更早 + 全部任务已结束」的日文件合并进对应月份的归档文件，
# 原日文件删除；仍有未完成任务的日文件保持不动。归档文件不参与日常索引，只做历史留档。
_AUTO_ARCHIVED = False


def _month_of(date):
    """'YYYY-MM-DD' -> 'YYYY-MM'。"""
    return date[:7]


def _archive_path(month):
    return os.path.join(_archive_dir(), month + ".md")


def _write_archive_block(t):
    """归档文件中的任务块：在 id 之后写入「原日期」，便于回溯它来自哪一天。"""
    lines = _write_block(t).split("\n")
    lines.insert(1, "原日期: %s" % (t.get("origin_date") or ""))
    return "\n".join(lines)


def _load_archive(month):
    """读取月度归档文件，返回 {'month','source_files','tasks'}；不存在返回空。"""
    fp = _archive_path(month)
    out = {"month": month, "source_files": [], "tasks": []}
    if not os.path.exists(fp):
        return out
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "---":
            i += 1
            break
        if line.startswith("来源文件:"):
            out["source_files"] = [x.strip() for x in line[5:].split(";") if x.strip()]
        i += 1
    blocks, cur = [], []
    for line in lines[i:]:
        if not line.strip():
            continue
        if line.startswith("## "):
            if cur:
                blocks.append(cur)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)
    for blk in blocks:
        tid = blk[0][3:].strip().split(" ")[0]
        t = _parse_block(blk[1:])
        t["id"] = tid or t["id"]
        if t["id"]:
            out["tasks"].append(t)
    return out


def _save_archive(month, source_files, tasks):
    os.makedirs(_archive_dir(), exist_ok=True)
    parts = ["# 归档 %s" % month,
             "归档: true",
             "schema: %d" % SCHEMA_VERSION,
             "月份: %s" % month,
             "来源文件: %s" % "; ".join(sorted(source_files)),
             "---"]
    for t in tasks:
        parts.append("")
        parts.append(_write_archive_block(t))
    with open(_archive_path(month), "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")


def _monthly_archives_info():
    """列出已有月度归档文件的概要，供索引使用。"""
    out = []
    if not os.path.isdir(_archive_dir()):
        return out
    for fn in sorted(os.listdir(_archive_dir())):
        if not fn.endswith(".md"):
            continue
        month = fn[:-3]
        if not re.match(r"^\d{4}-\d{2}$", month):
            continue
        data = _load_archive(month)
        out.append({"month": month, "files": sorted(data["source_files"]),
                    "file_count": len(data["source_files"]), "tasks": len(data["tasks"])})
    return out


def _monthly_archive(now=None, months=None, include_current=False, dry_run=False):
    """把「可归档日文件」（全部任务已结束）按月份合并进归档文件。

    months=None 时取全部早于当前月份的可归档月份（include_current=True 则含当前月）。
    dry_run=True 只返回计划不落盘。返回 [{'month','files','tasks'}]。"""
    now = now or dt.datetime.now()
    files = _scan_files()
    cur_month = _month_of(now.strftime("%Y-%m-%d"))
    groups = {}
    for date in sorted(files):
        data = files[date]
        if not data["tasks"]:
            continue
        if not all(t["status"] == "结束" for t in data["tasks"]):
            continue
        month = _month_of(date)
        if months is not None:
            if month not in months:
                continue
        elif not include_current and month >= cur_month:
            continue
        groups.setdefault(month, []).append(date)

    plan = []
    for month in sorted(groups):
        dates = groups[month]
        merged = []
        for date in dates:
            for t in files[date]["tasks"]:
                item = dict(t)
                item["origin_date"] = date
                merged.append(item)
        if dry_run:
            plan.append({"month": month, "files": dates, "tasks": len(merged)})
            continue
        exist = _load_archive(month)
        by_id = {t["id"]: t for t in exist["tasks"]}
        for t in merged:
            by_id[t["id"]] = t
        all_tasks = [by_id[k] for k in sorted(by_id)]
        sources = sorted(set(exist["source_files"]) | set(dates))
        _save_archive(month, sources, all_tasks)
        for date in dates:
            try:
                os.remove(_file_path(date))
            except OSError:
                pass
        plan.append({"month": month, "files": dates, "tasks": len(merged)})
    return plan


def _auto_monthly_archive(now=None):
    """进入新月份时自动归档；每个进程只执行一次，避免读命令反复写盘。"""
    global _AUTO_ARCHIVED
    if _AUTO_ARCHIVED:
        return []
    _AUTO_ARCHIVED = True
    return _monthly_archive(now=now, dry_run=False)


def build_index(now=None):
    """重建 index.json。返回 dict。

    索引里每个条目都带派生信息（逾期天数 / 置顶与理由 / 预案 / 周口径统计），
    供 CLI 与网页共用同一套算法；缺失数据一律为 None，渲染层不得编造。"""
    now = now or dt.datetime.now()
    _auto_monthly_archive(now)  # 进入新月 → 自动归档上月可归档记录（每进程一次）
    files = _scan_files()
    urgent, in_progress, todo_, done = [], [], [], []
    today, overdue = [], []
    archived_files = []
    total = done_total = 0
    imp_rank = {"重要": 0, "不重要": 1}
    week_start, week_end = _week_bounds(now.date())
    week_created = week_done = 0

    def item_key(it):
        # 置顶（逾期 > 停滞 > 今天到期）→ 紧急 → 重要性 → 有截止 → 创建时间
        pin = it.get("pin")
        return (0 if pin is not None else 1,
                pin if pin is not None else 99,
                0 if it["urgent"] else 1,
                imp_rank.get(it.get("importance"), 1),
                _due_value(it.get("due")) is None,
                -(now.timestamp() if it.get("created") else 0))

    def in_this_week(stamp):
        dv = _due_value(stamp)
        if dv is None:
            return False
        return week_start <= dv.date() <= week_end

    for date, data in files.items():
        if data["archived"]:
            archived_files.append(date)
        for t in data["tasks"]:
            total += 1
            pin, reason = _pin_info(t, now)
            od = _overdue_days(t, now)
            item = {
                "id": t["id"], "text": t["text"], "importance": t["importance"],
                "status": t["status"], "due": t["due"], "file": date,
                "created": t.get("created"), "urgent": bool(_is_urgent(t, now)),
                "workspace": t.get("workspace"), "links": t.get("links"),
                "depends_on": t.get("depends_on"), "blocked": _has_unfinished_deps(t),
                "parent": t.get("parent") or "",
                "from": t.get("from"),
                "tags": t.get("tags") or [],
                # 预案（选填）：最容易拦住我的障碍 / 如果它出现，我就……
                "blocker": t.get("blocker") or "", "counter": t.get("counter") or "",
                # 派生指标：无数据为 None，渲染层显示「—」/「暂无推算」
                "overdue_days": od, "due_in_days": _due_in_days(t, now),
                "stall_days": _stall_days(t, now),
                "projected_finish": _projected_finish(t, now),
                "pin": pin, "pin_reason": reason or "",
            }
            if t["status"] == "结束":
                done.append(item)
                done_total += 1
                if in_this_week(t.get("updated") or t.get("created")):
                    week_done += 1
            elif t["status"] == "进行中":
                in_progress.append(item)
            else:
                todo_.append(item)
            if _is_urgent(t, now) and t["status"] != "结束":
                urgent.append(item)
            if in_this_week(t.get("created")):
                week_created += 1
            if pin is not None and t["status"] != "结束":
                today.append(item)
            if od is not None:
                overdue.append(item)
    for bucket in (urgent, in_progress, todo_, done, today, overdue):
        bucket.sort(key=item_key)
    monthly = _monthly_archives_info()
    index = {
        "schema_version": SCHEMA_VERSION,
        "generated": _fmt(now),
        "summary": {
            "todo": len(todo_), "in_progress": len(in_progress), "urgent": len(urgent),
            "done": len(done), "total": total, "archived_files": len(archived_files),
            "files": len(files), "today": len(today), "overdue": len(overdue),
            "week_created": week_created, "week_done": week_done,
            "monthly_archives": len(monthly),
            "archived_tasks": sum(m["tasks"] for m in monthly),
        },
        # 周口径：一律周一为起点
        "week": {"start": week_start.strftime("%Y-%m-%d"),
                 "end": week_end.strftime("%Y-%m-%d"),
                 "created": week_created, "done": week_done},
        "urgent": urgent,
        "today": today,
        "overdue": overdue,
        "in_progress": in_progress,
        "todo": todo_,
        "done": done,
        "archived_files": archived_files,
        "monthly_archives": monthly,
    }
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    return index


# ---- 重复检测 -----------------------------------------------------------
_PUNCT_RE = re.compile(
    r"[\s\u3000，。！？、；：\u201c\u201d\u2018\u2019（）()\[\]【】《》<>·…—\-_/"
    r"\\|,.;:!?\'\"`~@#$%^&*+=]+"
)


def _normalize_text(text):
    """归一化任务内容：去空白/标点、英文小写，便于相同与近似比对。"""
    s = _norm(text).lower()
    s = _PUNCT_RE.sub("", s)
    return s


def _text_similarity(a, b):
    """返回 0~1 相似度；一方包含另一方且较短方足够长时抬高为近似。"""
    na, nb = _normalize_text(a), _normalize_text(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    ratio = SequenceMatcher(None, na, nb).ratio()
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    if len(shorter) >= 4 and shorter in longer:
        contain = len(shorter) / max(len(longer), 1)
        ratio = max(ratio, 0.70 + 0.30 * contain)
    return ratio


def find_duplicates(text, exclude_id=None):
    """扫描全部任务，返回 [{'kind','score','date','task'}, ...]。
    kind: exact（归一化相同） / similar（相似度达阈值）。
    优先列出未结束任务；exact 排在 similar 前，同分按创建倒序。"""
    text = _norm(text)
    if not text:
        return []
    exact, similar = [], []
    for date, data in _scan_files().items():
        for t in data["tasks"]:
            if exclude_id and t.get("id") == exclude_id:
                continue
            score = _text_similarity(text, t.get("text") or "")
            if score >= 1.0 or _normalize_text(text) == _normalize_text(t.get("text") or ""):
                exact.append({"kind": "exact", "score": 1.0, "date": date, "task": t})
            elif score >= SIMILAR_THRESHOLD:
                similar.append({"kind": "similar", "score": score, "date": date, "task": t})

    def rank(item):
        t = item["task"]
        done = 1 if t.get("status") == "结束" else 0
        created = t.get("created") or ""
        return (done, -item["score"], created)

    exact.sort(key=rank)
    similar.sort(key=rank)
    return exact + similar


def _print_dup_hits(hits, title="Found duplicate or similar todos"):
    print(title)
    for h in hits:
        t = h["task"]
        kind_label = "exact" if h["kind"] == "exact" else "similar (%.0f%%)" % (h["score"] * 100)
        print("  [%s] %s | %s | %s | %s" % (
            kind_label, t.get("id"), h["date"], t.get("status"), t.get("text")))
        if t.get("workspace"):
            print("         workspace: %s" % t["workspace"])


def _split_list_field(raw):
    return [x.strip() for x in (raw or "").split(";") if x.strip()]


# ---- 标签推测（只读、不落库） ---------------------------------------------
_ASCII_TOKEN_RE = re.compile(r"[a-z0-9]+")
_CJK_TOKEN_RE = re.compile(r"[\u4e00-\u9fff]+")
_PATH_SPLIT_RE = re.compile(r"[^0-9a-z\u4e00-\u9fff]+")


def _suggest_tokens(text):
    """把文本切成可比对的片段：英文/数字单词、中文相邻二字组，以及中文单字。

    二字组用于抵消语序差异，单字用于兜住「背{托福|英语}单词」这类只差一两个字的近义表述；
    两者一起用，靠后面的相关度门槛把噪声压下去。
    """
    s = _norm(text).lower()
    out = set()
    for w in _ASCII_TOKEN_RE.findall(s):
        if len(w) >= TAG_MIN_KEYWORD_LEN:
            out.add(w)
    for seg in _CJK_TOKEN_RE.findall(s):
        if len(seg) < TAG_MIN_KEYWORD_LEN:
            continue
        for ch in seg:
            out.add(ch)
        for i in range(len(seg) - 1):
            out.add(seg[i:i + 2])
    return out


def _suggest_token_match(a, b):
    """返回 (相关度, 共享片段数)。相关度 = 共有片段 / 较少一方片段数，0~1；无片段时一律 0，不编造。"""
    ta, tb = _suggest_tokens(a), _suggest_tokens(b)
    if not ta or not tb:
        return 0.0, 0
    inter = len(ta & tb)
    if not inter:
        return 0.0, 0
    return min(1.0, inter / float(min(len(ta), len(tb)))), inter


def _suggest_hit_word(word, body):
    """判断关键词是否命中：纯英文/数字按词边界匹配（避免 bug 命中的 debug），中文按子串匹配。"""
    w = _norm(word).lower()
    if not w or len(w) < TAG_MIN_KEYWORD_LEN:
        return False
    if re.fullmatch(r"[a-z0-9]+", w):
        return re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", body) is not None
    return w in body


def _suggest_path_tokens(workspace):
    """切出工作空间路径里的词，用于识别领域。"""
    s = _norm(workspace).lower()
    return set(x for x in _PATH_SPLIT_RE.split(s) if x)


def _suggest_history_hits(text, note="", workspace=""):
    """扫历史任务：内容相关、且打过标签的旧任务，其标签可作为建议。"""
    probe = " ".join([text or "", note or "", workspace or ""])
    files = _scan_files()          # 只读一次，避免逐条重复扫盘
    hits = []
    for date in sorted(files.keys(), reverse=True):
        for t in files[date]["tasks"]:
            tags = [x for x in (t.get("tags") or []) if _norm(x)]
            if not tags:
                continue
            old = " ".join([t.get("text") or "", t.get("note") or "", t.get("workspace") or ""])
            score, shared = _suggest_token_match(probe, old)
            # 相关度达标，或共享片段够多（长句会把比值稀释掉），才算同一类事
            if score < TAG_HISTORY_MIN_SCORE and shared < TAG_HISTORY_MIN_TOKENS:
                continue
            for tag in tags:
                hits.append({
                    "tag": tag,
                    "score": round(TAG_HISTORY_BASE + score, 3),
                    "source": "history",
                    "evidence": "Historical task %s “%s” used tag “%s” (similarity %.2f)"
                                % (t.get("id"), t.get("text"), tag, score),
                })
    return hits


def _suggest_keyword_hits(text, note="", workspace=""):
    """按词表规则推测：正文/备注命中领域词，工作空间路径命中领域词。"""
    body = " ".join([text or "", note or ""]).lower()
    path_tokens = _suggest_path_tokens(workspace)
    hits = []
    for tag, words in TAG_RULES:
        matched = [w for w in words if _suggest_hit_word(w, body)]
        if matched:
            hits.append({
                "tag": tag, "score": TAG_RULE_SCORE, "source": "keyword",
                "evidence": "keyword match: " + ", ".join(matched[:3]),
            })
    for tag, words in TAG_WORKSPACE_RULES:
        matched = [w for w in words if w in path_tokens]
        if matched:
            hits.append({
                "tag": tag, "score": TAG_WORKSPACE_SCORE, "source": "workspace",
                "evidence": "workspace contains: " + ", ".join(matched[:3]),
            })
    return hits


def _suggest_tags(text, note="", workspace="", existing=None):
    """推测合适的标签。只读，不写入存储。

    策略：历史标签复用（同一类旧任务打过的标签）+ 词表规则（正文/备注/工作空间）。
    返回 dict：
      suggestions: 建议标签（把握度降序，最多 TAG_MAX_SUGGEST 个）；没把握则为空列表
      details:     [{'tag','score','source','evidence'}, ...]，便于向用户解释依据
      reason:      {'history':bool,'keyword':bool,'evidence':[...]} 概览
    """
    result = {"suggestions": [], "details": [], "reason": {"history": False, "keyword": False, "evidence": []}}
    text = _norm(text)
    if not text:
        return result
    have = set(_norm(x) for x in (existing or []) if _norm(x))

    history_hits = _suggest_history_hits(text, note, workspace)
    keyword_hits = _suggest_keyword_hits(text, note, workspace)
    if not history_hits and not keyword_hits:
        # 数据不足就不给建议：宁可不说，不要说错
        return result

    # 同一个标签被多条独立证据支撑时，把握度累加；只被单一弱证据支撑的会卡在阈值外
    merged = {}
    for h in history_hits + keyword_hits:
        tag = _norm(h["tag"])
        if not tag or tag in have:
            continue
        cur = merged.get(tag)
        if cur is None:
            cur = {"tag": tag, "score": 0.0, "sources": [], "evidence": ""}
            merged[tag] = cur
        cur["score"] = round(cur["score"] + h["score"], 3)
        if h["source"] not in cur["sources"]:
            cur["sources"].append(h["source"])
        # 证据去重后再拼接，避免同一句话重复出现在输出里
        if h["evidence"] and h["evidence"] not in cur["evidence"]:
            cur["evidence"] = (cur["evidence"] + "; " + h["evidence"]) if cur["evidence"] else h["evidence"]
    ranked = sorted(merged.values(), key=lambda h: (-h["score"], h["tag"]))
    kept = [h for h in ranked if h["score"] >= TAG_MIN_SCORE][:TAG_MAX_SUGGEST]

    result["details"] = [{"tag": h["tag"], "score": h["score"],
                          "source": "+".join(h["sources"]), "evidence": h["evidence"]} for h in kept]
    result["suggestions"] = [h["tag"] for h in kept]
    result["reason"] = {
        "history": bool(history_hits),
        "keyword": bool(keyword_hits),
        "evidence": [h["evidence"] for h in kept],
    }
    return result


def _print_tag_suggestion(tid, suggested):
    """把建议标签打印出来提醒确认——注意：这里只打印，绝不写入。"""
    tags_str = ";".join(suggested)
    print("  Suggested tags: %s (not written yet; to confirm use: add --update-id %s --tags \"%s\")"
          % (tags_str, tid, tags_str))


def _apply_task_fields(task, args, now, *, is_new):
    """把 add 参数落到 task。新建时填默认值；更新时仅覆盖用户显式传入的字段。"""
    if args.status is not None:
        task["status"] = args.status if args.status in STATUS_SET else DEFAULT_STATUS
    elif is_new:
        task["status"] = _default_of("status")

    if args.importance is not None:
        task["importance"] = args.importance if args.importance in IMPORTANCE_SET else DEFAULT_IMPORTANCE
    elif is_new:
        task["importance"] = _default_of("importance")

    if args.urgent is not None:
        task["urgent"] = args.urgent if args.urgent in URGENT_SET else DEFAULT_URGENT
    elif is_new:
        task["urgent"] = _default_of("urgent")

    if args.note is not None:
        task["note"] = _norm(args.note)
    elif is_new:
        task["note"] = ""

    # 预案（选填）：最容易拦住我的障碍 / 如果它出现，我就……
    if getattr(args, "blocker", None) is not None:
        task["blocker"] = _norm(args.blocker)
    elif is_new:
        task["blocker"] = ""

    if getattr(args, "counter", None) is not None:
        task["counter"] = _norm(args.counter)
    elif is_new:
        task["counter"] = ""

    if args.workspace is not None:
        task["workspace"] = _norm_path(args.workspace)
    elif is_new:
        task["workspace"] = ""

    if args.docs is not None:
        task["docs"] = _split_list_field(args.docs)
    elif is_new:
        task["docs"] = []

    if args.links is not None:
        task["links"] = _split_list_field(args.links)
    elif is_new:
        task["links"] = []

    if args.deps is not None:
        task["depends_on"] = _split_list_field(args.deps)
    elif is_new:
        task["depends_on"] = []

    if getattr(args, "tags", None) is not None:
        task["tags"] = _split_list_field(args.tags)
    elif is_new:
        task["tags"] = []

    if args.parent is not None:
        task["parent"] = _norm(args.parent)
    elif is_new:
        task["parent"] = ""

    if args.due is not None:
        parsed = parse_due(args.due, now) if args.due else None
        task["due"] = parsed
        # 不推算原则：解析不了就说出来，不静默丢弃、更不猜一个日期
        if args.due and not parsed:
            print("Warning: unrecognized time “%s”; no deadline was set (accepted forms: 明天 / 周五 / 2026-10-20 10:00)."
                  % args.due, file=sys.stderr)
    elif is_new:
        task["due"] = None

    if args.from_url is not None:
        url = _norm(args.from_url)
        task["from"] = ({"type": _norm(args.from_type) or "agent", "url": url} if url else None)
    elif is_new:
        task["from"] = None

    if is_new:
        task["text"] = _norm(args.text)
        task["created"] = _fmt(now)
        task["updated"] = None
    else:
        # 更新时若传入 text，同步刷新内容（用于近似确认后纠正措辞）
        if args.text is not None and _norm(args.text):
            task["text"] = _norm(args.text)
        task["updated"] = _fmt(now)


def _print_task_summary(prefix, tid, date, task, idx):
    print("%s %s: %s" % (prefix, tid, task["text"]))
    print("  date: %s | importance: %s | status: %s | urgent: %s" % (
        date, task["importance"], task["status"], task["urgent"]))
    if task.get("due"):
        print("  due: %s" % task["due"])
    if task.get("note"):
        print("  note: %s" % task["note"])
    if task.get("blocker"):
        print("  blocker: %s" % task["blocker"])
    if task.get("counter"):
        print("  counter: %s" % task["counter"])
    if task.get("workspace"):
        print("  workspace: %s" % task["workspace"])
    if task.get("docs"):
        print("  docs: %s" % "; ".join(task["docs"]))
    if task.get("links"):
        print("  links: %s" % "; ".join(task["links"]))
    if task.get("depends_on"):
        print("  deps: %s" % "; ".join(task["depends_on"]))
    if task.get("tags"):
        print("  tags: %s" % "; ".join(task["tags"]))
    if task.get("parent"):
        print("  parent: %s" % task["parent"])
    if task.get("from") and task["from"].get("url"):
        print("  source: %s | %s" % (task["from"].get("type"), task["from"].get("url")))
    # 置顶必须解释原因；逾期任务必须给出两个出口
    _n = dt.datetime.now()
    pin, reason = _pin_info(task, _n)
    if pin is not None:
        print("  pinned: %s" % reason)
    if _overdue_days(task, _n) is not None:
        print("  exits: advance now → start/done %s; reschedule → postpone %s <new time>" % (tid, tid))
    if _projected_finish(task, _n) is None and task["status"] != "结束":
        print("  projected finish: N/A (no progress records)")
    print("  index updated: todo=%d in_progress=%d urgent=%d" % (
        idx["summary"]["todo"], idx["summary"]["in_progress"], idx["summary"]["urgent"]))


def _update_existing_task(tid, args, now):
    """按 add 参数更新已有任务；维护归档不变量。"""
    date, data, t = _find_task(tid)
    if t is None:
        print("Task %s not found" % tid, file=sys.stderr)
        return 2
    old_status = t.get("status")
    _apply_task_fields(t, args, now, is_new=False)
    # 依赖校验：存在性 + 自依赖 + 环
    deps = t.get("depends_on") or []
    missing = _missing_deps(deps)
    if missing:
        print("Error: dependency task(s) not found: %s" % "; ".join(missing), file=sys.stderr)
        return 2
    if tid in deps:
        print("Error: a task cannot depend on itself (%s)." % tid, file=sys.stderr)
        return 2
    if _would_create_cycle(tid, deps):
        print("Error: this dependency would create a cycle (%s would indirectly depend on itself)." % tid, file=sys.stderr)
        return 2
    rc = _guard_by_deps(deps, t["status"], args.force)
    if rc != 0:
        return rc
    # 父任务校验：存在性 + 自引用 + 环
    parent = _norm(t.get("parent"))
    if parent:
        if _find_task(parent)[2] is None:
            print("Error: parent task %s not found." % parent, file=sys.stderr)
            return 2
        if parent == tid:
            print("Error: a task cannot be its own parent (%s)." % tid, file=sys.stderr)
            return 2
        if _would_create_parent_cycle(tid, parent):
            print("Error: this assignment would create a cycle (%s becoming parent of %s)." % (parent, tid), file=sys.stderr)
            return 2
    rc = _guard_children_done(tid, t["status"], args.force)
    if rc != 0:
        return rc
    all_done = all(x["status"] == "结束" for x in data["tasks"])
    data["archived"] = all_done
    save_file(date, data["archived"], data["tasks"])
    idx = build_index(now)
    _print_task_summary("updated (not recreated)", tid, date, t, idx)
    if old_status != t["status"]:
        print("  status changed: %s -> %s" % (old_status, t["status"]))
    if all_done:
        print("  all tasks in this file are done; file marked archived")
    elif old_status == "结束" and t["status"] != "结束":
        print("  archived mark cleared")
    return 0


# ---- 命令实现 -----------------------------------------------------------
def cmd_add(args, now=None):
    now = now or dt.datetime.now()
    date = args.date or now.strftime("%Y-%m-%d")
    text = _norm(args.text)
    if not text:
        print("Error: --text (task content) is required.", file=sys.stderr)
        return 2

    # 显式指定更新目标：跳过重复检测，直接更新
    if args.update_id:
        # 确认更新时未给状态 → 默认拉回「进行中」（避免只复述内容却不推进状态）
        if args.status is None:
            args.status = DEFAULT_STATUS
        return _update_existing_task(args.update_id, args, now)

    hits = [] if args.force else find_duplicates(text)
    exact_hits = [h for h in hits if h["kind"] == "exact"]
    similar_hits = [h for h in hits if h["kind"] == "similar"]

    # 相同或近似：先不落盘，交由会话确认（相同默认建议更新状态）
    if hits and not args.force:
        if exact_hits:
            _print_dup_hits(exact_hits, title="Identical todo found (default: update its status, do not create a new one):")
            if similar_hits:
                _print_dup_hits(similar_hits, title="Also found similar todos:")
            print("To confirm the update add: --update-id <id> (recommended); to force-create add: --force")
        else:
            _print_dup_hits(similar_hits, title="Similar todo found, please confirm before proceeding:")
            print("To update add: --update-id <id>; to force-create add: --force")
        return EXIT_NEEDS_CONFIRM

    data = load_file(date)
    if data["archived"]:
        # 归档文件不追加新任务：取消归档标记（视为重新打开该日文件）
        data["archived"] = False
    tid = _next_id(date)
    task = {
        "id": tid, "status": DEFAULT_STATUS, "importance": DEFAULT_IMPORTANCE,
        "text": text, "note": "", "workspace": "", "docs": [], "links": [],
        "depends_on": [], "due": None, "created": None, "updated": None,
        "urgent": DEFAULT_URGENT, "from": None, "parent": "", "tags": [],
        "blocker": "", "counter": "", "origin_date": "",
    }
    _apply_task_fields(task, args, now, is_new=True)
    # 新任务的依赖校验：存在性 + 硬检查（新建即以 进行中/结束 起步时同样受依赖约束）
    missing = _missing_deps(task.get("depends_on") or [])
    if missing:
        print("Error: dependency task(s) not found: %s" % "; ".join(missing), file=sys.stderr)
        return 2
    rc = _guard_by_deps(task.get("depends_on"), task["status"], args.force)
    if rc != 0:
        return rc
    # 新任务的父任务校验：存在性（新建任务尚无父子环）
    parent = _norm(task.get("parent"))
    if parent and _find_task(parent)[2] is None:
        print("Error: parent task %s not found." % parent, file=sys.stderr)
        return 2
    data["tasks"].append(task)
    save_file(date, data["archived"], data["tasks"])
    idx = build_index(now)
    prefix = "force-created" if args.force else "added"
    _print_task_summary(prefix, tid, date, task, idx)
    # 没给标签时才推测：只给建议，不写入——由 AI 拿着建议问用户，确认后再用 --update-id 落库
    if not _split_list_field(args.tags):
        sug = _suggest_tags(text, task.get("note", ""), task.get("workspace", ""),
                            existing=task.get("tags"))
        if sug["suggestions"]:
            _print_tag_suggestion(tid, sug["suggestions"])
            for line in sug["reason"]["evidence"][:TAG_MAX_SUGGEST]:
                print("    evidence: %s" % line)
    return 0


def cmd_suggest_tags(args):
    """只读推测标签（JSON），供 AI 在建任务之前先问用户，不必先建后改。"""
    text = _norm(args.text)
    if not text:
        print("Error: --text is required.", file=sys.stderr)
        return 2
    res = _suggest_tags(text, args.note or "", args.workspace or "")
    print(json.dumps({
        "text": text,
        "suggestions": res["suggestions"],
        "reason": res["reason"],
        "details": res["details"],
        "written": False,          # 明确告知调用方：什么都没写进存储
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_check(args):
    """检查文本是否与已有任务相同/近似（只读，不落盘）。"""
    text = _norm(args.text)
    if not text:
        print("Error: --text is required.", file=sys.stderr)
        return 2
    hits = find_duplicates(text, exclude_id=args.exclude_id or None)
    if not hits:
        print("No duplicate or similar todos")
        return 0
    _print_dup_hits(hits)
    exact_n = sum(1 for h in hits if h["kind"] == "exact")
    print("total: exact %d, similar %d" % (exact_n, len(hits) - exact_n))
    return EXIT_NEEDS_CONFIRM if hits else 0


# ---- 分诊（triage）：给一段话判定该「添加 / 更新 / 删除 / 修改状态」 -----------------
# 纯规则、确定性的初判；拿不准就 need_confirm=True（CLI 退出码 3），由会话或系统弹框
# 让用户确认。分诊只提议，绝不落盘；真正执行走 add / update / status / delete。
# 设计目标：剪贴板内容原样当作任务内容（text 恒为原文），时间/重要/紧急/路径等作为
# 附带字段解析出来，供添加或更新时预填。

_TRIAGE_ID_RE = re.compile(r"T-\d{8}-\d{3}")
_TRIAGE_WS_RE = re.compile(
    r"(?:[A-Za-z]:\\[^\s，。；;）)\]]+)|(?:\/(?:[A-Za-z0-9_.\-]+\/)+[A-Za-z0-9_.\-]+)")
_TRIAGE_TIME_RE = re.compile(
    r"(?:下(?:周|星期)[一二三四五六日天七]|(?:周|星期)[一二三四五六日天七]|"
    r"今天|今日|明天|明日|后天|昨天|昨日|\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}|"
    r"\d+天(?:后)?|\d{1,2}[:：]\d{2}|\d{1,2}点(?:半)?)")
_TRIAGE_Q_RE = re.compile(r"[？?]$|(吗|呢|怎么样|如何|是不是|有没有|哪|谁|什么)$")
_TRIAGE_HELPER_RE = re.compile(r"^(需要|要|得|必须|应该|记得|请|帮我)")
_TRIAGE_LEAD_RE = re.compile(r"^(?:把|将|给|请)")

TRIAGE_DELETE_VERBS = ("删除", "删掉", "移除", "去掉", "清除", "删了", "删", "delete", "remove", "rm")
TRIAGE_UPDATE_VERBS = ("修改", "更新", "改为", "改成", "改到", "推迟", "延后", "提前", "换成",
                       "调整", "改期", "reschedule", "postpone", "update", "change", "modify", "edit")
TRIAGE_STATUS_GROUPS = (
    ("结束", ("完成", "做完", "搞定", "收尾", "结束", "标记完成", "标为完成", "finish", "complete", "done")),
    ("进行中", ("开始", "推进", "继续", "进行中", "start", "begin")),
    ("待开始", ("待开始", "还没做", "重新打开", "恢复", "reopen")),
    ("维护", ("暂停", "挂起", "维护")),
)
TRIAGE_TARGET_MIN = 0.55   # 达到该相似度才算「指代已锁定」
TRIAGE_CANDIDATE_MIN = 0.30  # 达到该相似度才进候选列表（供用户挑选）

# 捕获服务配置（env.json 的 capture 段；合并默认值后返回）
CAPTURE_DEFAULTS = {
    "enabled": True,
    "hotkey": "Ctrl+Alt+T",
    "triage_types": {"add": True, "update": True, "delete": True, "status": True},
    "confirm_delete": True,
    "toast": True,
}
TRIAGE_TYPES_ALL = ("add", "update", "delete", "status")
HOTKEY_MODS = {"ctrl": 0x0002, "alt": 0x0001, "shift": 0x0004, "win": 0x0008}
_HOTKEY_ALIAS = {"control": "ctrl", "cmd": "win", "meta": "win", "windows": "win", "super": "win"}


def _str_to_bool(v):
    return str(v).strip().lower() in ("1", "true", "yes", "on", "开", "是")


def _hotkey_parse(expr):
    """把 "Ctrl+Alt+T" 解析为 (mods, vk)；非法返回 (None, 错误信息)。纯函数，平台无关。"""
    expr = _norm(expr or "")
    if not expr:
        return None, "hotkey must not be empty"
    parts = [p.strip().lower() for p in expr.split("+") if p.strip()]
    if not parts:
        return None, "hotkey must not be empty"
    mods = 0
    key = parts[-1]
    for m in parts[:-1]:
        m = _HOTKEY_ALIAS.get(m, m)
        if m not in HOTKEY_MODS:
            return None, "unknown modifier: %s (supported: Ctrl / Alt / Shift / Win)" % m
        mods |= HOTKEY_MODS[m]
    if mods == 0:
        return None, "hotkey needs at least one modifier (Ctrl / Alt / Shift / Win)"
    ku = key.upper()
    if re.fullmatch(r"F(?:[1-9]|1[0-9]|2[0-4])", ku):
        vk = 0x70 + int(ku[1:]) - 1
    elif re.fullmatch(r"[0-9A-Z]", ku):
        vk = ord(ku)
    elif key in ("space", "空格"):
        vk = 0x20
    elif key in ("enter", "回车"):
        vk = 0x0D
    elif key == "tab":
        vk = 0x09
    elif key in ("esc", "escape"):
        vk = 0x1B
    else:
        return None, "unsupported key: %s (use a letter, digit, F1-F24, Space, Enter, Tab, Esc)" % key
    return mods, vk


def _hotkey_format(mods, vk):
    """把 (mods, vk) 还原为可读组合，供展示。"""
    names = [n.capitalize() for n, bit in HOTKEY_MODS.items() if mods & bit]
    if 0x30 <= vk <= 0x5A:
        key = chr(vk)
    elif 0x70 <= vk <= 0x87:
        key = "F%d" % (vk - 0x70 + 1)
    elif vk == 0x20:
        key = "Space"
    elif vk == 0x0D:
        key = "Enter"
    elif vk == 0x09:
        key = "Tab"
    elif vk == 0x1B:
        key = "Esc"
    else:
        key = hex(vk)
    return "+".join(names + [key])


def _capture_config():
    """读取 env.json 的 capture 段并合并默认值（非法值回退默认）。"""
    env = _load_env()
    cap = env.get("capture")
    if not isinstance(cap, dict):
        cap = {}
    out = {}
    for k, dv in CAPTURE_DEFAULTS.items():
        v = cap.get(k, dv)
        if k == "triage_types":
            if not isinstance(v, dict):
                v = dict(dv)
            out[k] = {a: bool(v.get(a, dv.get(a, True))) for a in TRIAGE_TYPES_ALL}
        elif k in ("enabled", "confirm_delete", "toast"):
            out[k] = bool(v)
        else:
            out[k] = _norm(v) or dv
    return out


def _capture_view():
    """给 env 输出与网页设置页用的完整视图：合并默认值 + 快捷键合法性说明。"""
    cfg = _capture_config()
    mods, err = _hotkey_parse(cfg.get("hotkey"))
    cfg["hotkey_valid"] = mods is not None
    cfg["hotkey_error"] = None if mods is not None else err
    return cfg


def _extract_due_token(text):
    """从文本中挑出一个 parse_due 能解析的时间短语；解析不了返回 None。
    优先尝试「相对日期 + 时间」组合（如 明天 10:00、周五 09:00）。"""
    for m in _TRIAGE_TIME_RE.finditer(text):
        for end in range(m.end(), min(m.end() + 10, len(text) + 1)):
            cand = _norm(text[m.start():end])
            if parse_due(cand):
                return cand
        if parse_due(m.group(0)):
            return m.group(0)
    return None


def _triage_fields(text, now):
    """从原文解析附带字段（只做预填建议；全部可选，不猜）。"""
    f = {}
    tok = _extract_due_token(text)
    if tok:
        f["due"] = tok
    if "重要" in text:
        f["importance"] = "重要"
    if any(w in text for w in ("紧急", "加急", "尽快", "马上", "立刻")):
        f["urgent"] = "紧急"
    m = re.search(r"(?:备注|note)\s*[:：]\s*(.+)$", text)
    if m:
        f["note"] = _norm(m.group(1))
    m = re.search(r"(?:标签|tag)\s*[:：]\s*([^\n]+)$", text)
    if m:
        f["tags"] = [x.strip() for x in re.split(r"[;；、,，]", m.group(1)) if x.strip()]
    m = _TRIAGE_WS_RE.search(text)
    if m:
        f["workspace"] = _norm_path(m.group(0).rstrip("，。；;"))
    return f


def _triage_subject(text, action, status):
    """把指代主体从原文里抠出来（用于匹配已有任务）。启发式，拿不准就返回整句。"""
    s = _norm(text)
    s = _TRIAGE_ID_RE.sub("", s)
    s = _TRIAGE_LEAD_RE.sub("", s)
    if action == "delete":
        for v in TRIAGE_DELETE_VERBS:
            if v in s:
                s = s.split(v, 1)[-1]
                break
    elif action == "status":
        for st, words in TRIAGE_STATUS_GROUPS:
            if st != status:
                continue
            for w in words:
                if w in s:
                    before, _, after = s.partition(w)
                    if before and not re.fullmatch(r"[\s，。；、,:：]*", before):
                        s = before
                    else:
                        s = after
                    break
            break
        # 把X标记为完成 → 去掉「标记为/标为/设为」等连接词尾巴
        s = re.split(r"(?:标记(?:为|成)?|标为|设为|变为|改成)", s)[0]
    else:  # update
        for kw in ("改为", "改成", "改到", "推迟到", "延后到", "提前到", "换成", "调整为", "改期到", "更新为"):
            if kw in s:
                s = s.split(kw, 1)[0]
                break
        else:
            for v in TRIAGE_UPDATE_VERBS:
                if v in s:
                    before, _, after = s.partition(v)
                    if before and not re.fullmatch(r"[\s，。；、,:：]*", before):
                        s = before
                    break
    s = re.sub(r"^(?:这个|那个|这条|该|把|将|给)", "", s)
    return _norm(s)


def _resolve_triage_target(tid, subject):
    """锁定目标任务。返回 (best, candidates)；best=None 表示没锁住。
    优先未结束任务；candidates 是相似度达到候选门槛的列表（供弹框挑选）。"""
    if tid:
        date, _, t = _find_task(tid)
        if t:
            return {"id": t["id"], "text": t["text"], "score": 1.0, "kind": "id"}, []
        return None, []
    if not subject:
        return None, []

    def scan(only_open):
        best, cands = None, []
        for date, data in _scan_files().items():
            for t in data["tasks"]:
                if only_open and t.get("status") == "结束":
                    continue
                score = _text_similarity(subject, t.get("text") or "")
                if score < TRIAGE_CANDIDATE_MIN:
                    continue
                ent = {"id": t["id"], "text": t["text"],
                       "score": round(score, 3), "kind": "similar"}
                if score >= TRIAGE_TARGET_MIN:
                    if best is None or score > best["score"]:
                        best = ent
                else:
                    cands.append(ent)
        cands.sort(key=lambda x: -x["score"])
        return best, cands

    best, cands = scan(True)
    if best is None:
        best, _ = scan(False)
    return best, cands[:5]


def triage_text(text, now=None):
    """分诊主入口（只读）：给一段话返回结构化提议。
    返回 dict：{ok, action, confidence, need_confirm, reasons, text, target,
    candidates, status, fields, suggested_tags, fallback_action}。"""
    now = now or dt.datetime.now()
    raw = _norm(text)
    base = {
        "ok": True,
        "action": "unknown",
        "confidence": "low",
        "need_confirm": True,
        "reasons": [],
        "text": raw,
        "target": None,
        "candidates": [],
        "status": None,
        "fields": {},
        "suggested_tags": [],
        "fallback_action": None,
    }
    if not raw:
        base["reasons"].append("empty_text")
        return base
    if _TRIAGE_Q_RE.search(raw):
        base["reasons"].append("question")
        return base

    tid_m = _TRIAGE_ID_RE.search(raw)
    tid = tid_m.group(0) if tid_m else None

    # 动作判定：删除 > 状态 > 更新 > 添加
    action, status = "add", None
    if any(v in raw for v in TRIAGE_DELETE_VERBS):
        action = "delete"
    else:
        for st, words in TRIAGE_STATUS_GROUPS:
            if any(w in raw for w in words):
                action, status = "status", st
                break
        if action == "add" and any(v in raw for v in TRIAGE_UPDATE_VERBS):
            action = "update"
    # 「需要/要/必须…完成X」是承诺新任务，不是对已有任务下指令（除非带任务 ID）
    if action in ("status", "update") and not tid and _TRIAGE_HELPER_RE.match(raw):
        action = "add"

    fields = _triage_fields(raw, now)

    if action == "add":
        base["action"] = "add"
        base["fields"] = fields
        base["suggested_tags"] = _suggest_tags(raw, fields.get("note", ""),
                                               fields.get("workspace", ""))["suggestions"]
        hits = find_duplicates(raw)
        if hits:
            h = hits[0]
            base["need_confirm"] = True
            base["confidence"] = "medium"
            base["reasons"].append("duplicate")
            base["target"] = {"id": h["task"]["id"], "text": h["task"]["text"],
                              "score": round(h["score"], 3), "kind": h["kind"]}
            base["candidates"] = [{"id": x["task"]["id"], "text": x["task"]["text"],
                                   "score": round(x["score"], 3), "kind": x["kind"]}
                                  for x in hits[:5]]
        else:
            base["need_confirm"] = False
            base["confidence"] = "high"
        return base

    # 删除 / 状态 / 更新：必须锁住目标
    subject = _triage_subject(raw, action, status)
    target, cands = _resolve_triage_target(tid, subject)
    base["action"] = action
    base["status"] = status
    base["fields"] = fields
    base["candidates"] = cands
    if target:
        base["target"] = target
        if action == "delete":
            # 删除是破坏性动作：无论多确定都要求确认
            base["need_confirm"] = True
            base["confidence"] = "medium"
            base["reasons"].append("destructive")
        else:
            base["need_confirm"] = False
            base["confidence"] = "high"
    else:
        base["need_confirm"] = True
        base["confidence"] = "low"
        base["reasons"].append("target_not_found")
        base["fallback_action"] = "add"
    return base


def cmd_triage(args):
    """分诊：只读提议（JSON 输出）。need_confirm=True 时退出码 3（需确认信号）。"""
    proposal = triage_text(args.text)
    print(json.dumps(proposal, ensure_ascii=False, indent=2))
    return EXIT_NEEDS_CONFIRM if proposal["need_confirm"] else 0


def _find_task(tid):
    for date, data in _scan_files().items():
        for t in data["tasks"]:
            if t["id"] == tid:
                return date, data, t
    return None, None, None


# ---- 依赖链 ---------------------------------------------------------------
def _all_tasks_map():
    """id -> (date, data, task) 全表，用于批量存在性/环检测。"""
    m = {}
    for date, data in _scan_files().items():
        for t in data["tasks"]:
            m[t["id"]] = (date, data, t)
    return m


def _missing_deps(dep_ids):
    """返回依赖列表中不存在的任务 ID。"""
    allmap = _all_tasks_map()
    return [d for d in dep_ids if d not in allmap]


def _would_create_cycle(root_id, new_dep_ids):
    """沿「依赖」正向传播：若任一新依赖能（间接）到达 root，则新增会成环。"""
    allmap = _all_tasks_map()

    def forward(start):
        t = allmap.get(start)
        if not t:
            return ()
        return t[2].get("depends_on") or ()

    for nd in new_dep_ids:
        seen = set()
        stack = list(forward(nd))
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if cur == root_id:
                return True
            stack.extend(forward(cur))
    return False


def _has_unfinished_deps(t):
    """任务 t 是否存在未结束（或不存在）的直接依赖。"""
    for did in t.get("depends_on") or []:
        _, _, dtask = _find_task(did)
        if dtask is None or dtask["status"] != "结束":
            return True
    return False


def _guard_by_deps(dep_ids, target_status, force):
    """依赖硬检查（死的规则）：target_status 为「进行中/结束」且存在未结束的直接依赖时，
    拒绝推进并返回 EXIT_NEEDS_CONFIRM（exit 3），由会话中的 AI 向用户确认后决定是否 --force。
    force=True 或目标状态非推进态（待开始/维护/其他）时不拦截。返回 0=通过。"""
    if force or target_status not in ("进行中", "结束"):
        return 0
    conflicts = []
    for did in dep_ids or []:
        ddate, _, dtask = _find_task(did)
        if dtask is None:
            conflicts.append({"id": did, "status": "(missing)", "text": "", "date": ""})
        elif dtask["status"] != "结束":
            conflicts.append({"id": did, "status": dtask["status"], "text": dtask["text"], "date": ddate})
    if conflicts:
        print("Dependency check failed (prerequisites not finished; cannot advance to “%s”):" % target_status)
        for c in conflicts:
            print("  - %s [%s] %s %s" % (c["id"], c["status"], c["date"], c["text"]))
        print("Hint: add --force to force advance (run by the AI after the user confirms); "
              "or finish the prerequisite tasks first.")
        return EXIT_NEEDS_CONFIRM
    return 0


# ---- 子任务 ---------------------------------------------------------------
def _children_of(pid):
    """返回父任务 pid 的全部子任务 [(date, task), ...]。"""
    return [(date, t) for date, _, t in _all_tasks_map().values()
            if (t.get("parent") or "") == pid]


def _would_create_parent_cycle(tid, parent_id):
    """把 parent_id 设为 tid 的父任务时，沿父链上溯是否成环（或已存在环）。"""
    allmap = _all_tasks_map()
    cur, seen = parent_id, set()
    while cur:
        if cur == tid:
            return True
        if cur in seen:
            return True
        seen.add(cur)
        t = allmap.get(cur)
        cur = (t[2].get("parent") or "") if t else None
    return False


def _guard_children_done(tid, target_status, force):
    """父任务完成硬检查：target_status 为「结束」且存在未完成的子任务时，拒绝并返回
    EXIT_NEEDS_CONFIRM（exit 3），由 AI 向用户确认后决定是否 --force。返回 0=通过。"""
    if force or target_status != "结束":
        return 0
    unfinished = [(date, t) for date, t in _children_of(tid) if t["status"] != "结束"]
    if unfinished:
        print("Subtask check failed (unfinished subtasks exist; the parent cannot be marked done):")
        for date, t in unfinished:
            print("  - %s [%s] %s %s" % (t["id"], t["status"], date, t["text"]))
        print("Hint: add --force to force-finish (run by the AI after the user confirms); "
              "or finish the subtasks first.")
        return EXIT_NEEDS_CONFIRM
    return 0


def cmd_children(args):
    """列出某主任务下的全部子任务。"""
    pid = args.id
    _, _, pt = _find_task(pid)
    if pt is None:
        print("Parent task %s not found" % pid, file=sys.stderr)
        return 2
    children = _children_of(pid)
    children.sort(key=lambda c: (c[1].get("created") or ""))
    print("Parent %s: %s (%d subtask(s))" % (pid, pt["text"], len(children)))
    for date, t in children:
        flag = STATUS_MARKS.get(t["status"], "[ ]")
        urgent_mark = "!" if _is_urgent(t, dt.datetime.now()) else " "
        print("  %s %s [%s%s] %s · %s · %s" % (
            t["id"], flag, urgent_mark, t["importance"], t["text"],
            t["due"] or "no due", t["status"]))
        if t.get("depends_on"):
            print("     deps: %s" % "; ".join(t["depends_on"]))
    if not children:
        print("  (no subtasks)")
    return 0


def cmd_deparent(args):
    """解除子任务与父任务的归属关系。"""
    date, data, t = _find_task(args.id)
    if t is None:
        print("Task %s not found" % args.id, file=sys.stderr)
        return 2
    if not t.get("parent"):
        print("%s has no parent task." % args.id)
        return 0
    parent_id = t["parent"]
    t["parent"] = ""
    t["updated"] = _fmt(dt.datetime.now())
    data["archived"] = all(x["status"] == "结束" for x in data["tasks"])
    save_file(date, data["archived"], data["tasks"])
    build_index()
    print("%s detached from parent %s." % (args.id, parent_id))
    return 0


def cmd_dep(args):
    """设置 / 查看任务依赖。模式：
      dep <id>               查看
      dep <id> A B ...       设置（替换）依赖
      dep <id> --add A B     追加依赖
      dep <id> --remove A B  移除依赖
      dep <id> --clear       清空依赖
    任何改动都会做存在性校验与循环依赖检测。"""
    date, data, t = _find_task(args.id)
    if t is None:
        print("Task %s not found" % args.id, file=sys.stderr)
        return 2

    deps = list(t.get("depends_on") or [])
    if args.deps:
        deps = list(args.deps)
    elif args.add:
        deps.extend(args.add)
    if args.remove:
        rm = set(args.remove)
        deps = [d for d in deps if d not in rm]
    if args.clear:
        deps = []
    # 去重保序
    uniq, seen = [], set()
    for d in deps:
        if d not in seen:
            seen.add(d)
            uniq.append(d)
    deps = uniq

    missing = _missing_deps(deps)
    if missing:
        print("Error: dependency task(s) not found: %s" % "; ".join(missing), file=sys.stderr)
        return 2
    if args.id in deps:
        print("Error: a task cannot depend on itself (%s)." % args.id, file=sys.stderr)
        return 2
    if _would_create_cycle(args.id, deps):
        print("Error: this dependency would create a cycle (%s would indirectly depend on itself)." % args.id, file=sys.stderr)
        return 2

    changed = deps != (t.get("depends_on") or [])
    if changed:
        t["depends_on"] = deps
        t["updated"] = _fmt(dt.datetime.now())
        data["archived"] = all(x["status"] == "结束" for x in data["tasks"])
        save_file(date, data["archived"], data["tasks"])
        build_index()

    print("%s dependencies (%d):" % (args.id, len(deps)))
    for did in deps:
        ddate, _, dtask = _find_task(did)
        print("  - %s [%s] %s %s" % (did, dtask["status"] if dtask else "(missing)",
                                     ddate, dtask["text"] if dtask else ""))
    if not deps:
        print("  (no dependencies)")
    return 0


def _delete_task(tid, now=None, quiet=False):
    """删除任务并清理其他任务对它的依赖 / 父任务引用；维护归档不变量。
    文件清空后尝试删除文件（删除不可用时写回 归档:false 空文件）。
    返回退出码：0=成功，2=未找到。quiet=True 时不打印（网页端复用）。"""
    now = now or dt.datetime.now()
    date, data, t = _find_task(tid)
    if t is None:
        if not quiet:
            print("Task %s not found" % tid, file=sys.stderr)
        return 2
    data["tasks"] = [x for x in data["tasks"] if x.get("id") != tid]
    if data["tasks"]:
        all_done = all(x["status"] == "结束" for x in data["tasks"])
        data["archived"] = all_done
        save_file(date, data["archived"], data["tasks"])
    else:
        try:
            os.remove(_file_path(date))
        except OSError:
            data["archived"] = False
            save_file(date, False, data["tasks"])
    for d2, d2data in _scan_files().items():
        changed = False
        for x in d2data["tasks"]:
            if tid in (x.get("depends_on") or []):
                x["depends_on"] = [d for d in x.get("depends_on") if d != tid]
                x["updated"] = _fmt(now)
                changed = True
            if (x.get("parent") or "") == tid:
                x["parent"] = ""
                x["updated"] = _fmt(now)
                changed = True
        if changed:
            d2_all = all(y["status"] == "结束" for y in d2data["tasks"])
            d2data["archived"] = d2_all
            save_file(d2, d2data["archived"], d2data["tasks"])
    build_index(now)
    if not quiet:
        print("Deleted: %s %s" % (tid, t["text"]))
    return 0


def cmd_delete(args):
    return _delete_task(args.id)


def _set_status(tid, status, force=False):
    date, data, t = _find_task(tid)
    if t is None:
        print("Task %s not found" % tid, file=sys.stderr)
        return 2
    rc = _guard_by_deps(t.get("depends_on"), status, force)
    if rc != 0:
        return rc
    rc = _guard_children_done(tid, status, force)
    if rc != 0:
        return rc
    t["status"] = status
    t["updated"] = _fmt(dt.datetime.now())
    # 归档不变量：归档 ⇔ 该文件所有任务均为 结束
    all_done = all(x["status"] == "结束" for x in data["tasks"])
    data["archived"] = all_done
    save_file(date, data["archived"], data["tasks"])
    msg = "%s -> %s (%s)" % (tid, status, t["text"])
    if status == "结束" and all_done:
        msg += "; all tasks in this file are done; file marked archived"
    elif status != "结束" and not all_done:
        msg += "; archived mark cleared"
    build_index()
    print(msg)
    return 0


def cmd_work(args):
    """继续一个待办：标记进行中，若有工作区目录则用配置好的编辑器打开。"""
    date, data, t = _find_task(args.id)
    if t is None:
        print("Task %s not found" % args.id, file=sys.stderr)
        return 2
    rc = _guard_by_deps(t.get("depends_on"), "进行中", args.force)
    if rc != 0:
        return rc
    t["status"] = "进行中"
    t["updated"] = _fmt(dt.datetime.now())
    all_done = all(x["status"] == "结束" for x in data["tasks"])
    data["archived"] = all_done
    save_file(date, data["archived"], data["tasks"])
    build_index()
    print("Marked in progress: %s %s" % (args.id, t["text"]))
    ws = _norm(t.get("workspace"))
    if ws:
        label = _norm(_editor_config().get("label")) or "editor"
        ok, msg = open_editor(ws)
        if ok:
            print("Opened workspace with %s: %s" % (label, ws))
        else:
            # work 的主职责（标记进行中）已经完成，这里只报错 + 给配置出口，不改返回码
            print("Failed to open editor: %s" % msg, file=sys.stderr)
            print("Workspace dir: %s" % ws, file=sys.stderr)
            print("Configure the editor: %s env --set editor.path=\"<absolute path to editor executable>\""
                  % _script_cmd(), file=sys.stderr)
    else:
        print("This todo has no workspace directory; editor was not opened.")
    return 0


def cmd_done(args):
    return _set_status(args.id, "结束", args.force)


def cmd_start(args):
    return _set_status(args.id, "进行中", args.force)


def cmd_reopen(args):
    return _set_status(args.id, "待开始")


def cmd_archive(args):
    date = args.date
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        print("Error: date must be YYYY-MM-DD", file=sys.stderr)
        return 2
    if not os.path.exists(_file_path(date)):
        print("File not found: %s" % _file_path(date), file=sys.stderr)
        return 2
    data = load_file(date)
    if data["tasks"] and not all(t["status"] == "结束" for t in data["tasks"]):
        print("Unfinished tasks remain; refusing to force-archive (finish them or reopen first). "
              "You may edit the file manually.", file=sys.stderr)
        return 2
    data["archived"] = True
    save_file(date, True, data["tasks"])
    build_index()
    print("Archived %s" % date)
    return 0


def cmd_postpone(args):
    """调整计划：重设（或清除）某任务的截止日。这是逾期任务的第二个出口。
    时间交给 parse_due 解析，解析不了就报错并保持不变——绝不猜一个日期。"""
    date, data, t = _find_task(args.id)
    if t is None:
        print("Task %s not found" % args.id, file=sys.stderr)
        return 2
    old = t.get("due")
    if args.clear:
        t["due"] = None
    else:
        now = dt.datetime.now()
        nd = parse_due(args.due, now)
        if nd is None:
            print("Error: unrecognized time “%s”; deadline unchanged." % args.due, file=sys.stderr)
            print("Accepted: 明天 / 周五 / 3天后 / 2026-10-20 10:00 / --clear to remove the deadline",
                  file=sys.stderr)
            return 2
        t["due"] = nd
    t["updated"] = _fmt(dt.datetime.now())
    data["archived"] = all(x["status"] == "结束" for x in data["tasks"])
    save_file(date, data["archived"], data["tasks"])
    idx = build_index()
    print("Rescheduled: %s %s" % (t["id"], t["text"]))
    print("  due: %s -> %s" % (old or "no due", t["due"] or "no due"))
    print("  index updated: todo=%d in_progress=%d urgent=%d overdue=%d" % (
        idx["summary"]["todo"], idx["summary"]["in_progress"],
        idx["summary"]["urgent"], idx["summary"]["overdue"]))
    return 0


def cmd_migrate(args):
    """把旧版本存储文件迁移到当前 schema（默认只预览，--apply 才落盘）。
    迁移是无损的：读出来再按当前格式写回，补齐 schema 头与新字段默认值。"""
    files = _scan_files()
    outdated = [d for d in sorted(files) if (files[d].get("schema") or 1) < SCHEMA_VERSION]
    cur_idx_version = None
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                cur_idx_version = json.load(f).get("schema_version")
        except Exception:
            cur_idx_version = None
    if not outdated and cur_idx_version == SCHEMA_VERSION:
        print("Already on the latest schema v%d (%d storage file(s)); nothing to migrate."
              % (SCHEMA_VERSION, len(files)))
        return 0
    print("Current schema v%d; the following %d file(s) need migration:" % (SCHEMA_VERSION, len(outdated)))
    for d in outdated:
        print("  %s.md  v%s -> v%d" % (d, files[d].get("schema") or 1, SCHEMA_VERSION))
    if cur_idx_version != SCHEMA_VERSION:
        print("  index.json  v%s -> v%d" % (cur_idx_version or "none", SCHEMA_VERSION))
    if not args.apply:
        print("(preview mode; nothing changed — add --apply to run)")
        return 0
    n = 0
    for d in outdated:
        data = files[d]
        save_file(d, data["archived"], data["tasks"])
        n += 1
    idx = build_index()  # 顺带把 index.json 升到当前版本
    print("Migrated %d storage file(s); index.json schema_version=%s" % (n, idx.get("schema_version")))
    return 0


def cmd_monthly_archive(args):
    """月度归档：把「可归档日文件」（全部任务已结束）合并进 storage/archive/YYYY-MM.md。
    默认口径：只处理早于当前月份的文件；--month 指定月份；--all 含当前月；--dry-run 只预览。"""
    now = dt.datetime.now()
    months = [args.month] if args.month else None
    if args.month and not re.match(r"^\d{4}-\d{2}$", args.month):
        print("Error: --month must be YYYY-MM", file=sys.stderr)
        return 2
    plan = _monthly_archive(now=now, months=months,
                            include_current=bool(args.all), dry_run=bool(args.dry_run))
    if not plan:
        print("No archivable records (requires: all tasks in the day file finished%s)."
              % ("" if args.all else " and the month earlier than the current month"))
        return 0
    prefix = "Will archive" if args.dry_run else "Archived"
    total_files = sum(len(p["files"]) for p in plan)
    total_tasks = sum(p["tasks"] for p in plan)
    print("%s %d month(s), %d day file(s), %d record(s):" % (prefix, len(plan), total_files, total_tasks))
    for p in plan:
        print("  - %s: %d file(s) (%s), %d record(s) -> storage/archive/%s.md"
              % (p["month"], len(p["files"]), "; ".join(p["files"]), p["tasks"], p["month"]))
    if args.dry_run:
        print("(preview mode; nothing changed — run without --dry-run to apply)")
        return 0
    idx = build_index(now)
    print("Monthly archives: %d file(s), %d archived record(s); current index total=%d"
          % (idx["summary"]["monthly_archives"], idx["summary"]["archived_tasks"],
             idx["summary"]["total"]))
    return 0


def cmd_list(args, now=None):
    now = now or dt.datetime.now()
    if args.date:
        data = load_file(args.date)
        files = {args.date: data}
    else:
        files = _scan_files()
    state = args.state or "all"
    lines = []
    for date in sorted(files):
        data = files[date]
        for t in data["tasks"]:
            if state == "urgent" and not _is_urgent(t, now):
                continue
            if state == "overdue" and _overdue_days(t, now) is None:
                continue
            if state == "today" and _pin_info(t, now)[0] is None:
                continue
            if state not in ("all", "urgent", "overdue", "today") and t["status"] != state:
                continue
            flag = STATUS_MARKS.get(t["status"], "[ ]")
            urgent_mark = "!" if _is_urgent(t, now) else " "
            # 置顶理由与逾期天数：有数据才显示，没有就是「—」
            pin, reason = _pin_info(t, now)
            od = _overdue_days(t, now)
            tail = ""
            if od is not None:
                tail = " · overdue %d day(s)" % od
            lines.append("%s %s %s [%s%s] %s · %s · %s%s"
                         % (t["id"], date, flag, urgent_mark, t["importance"], t["text"],
                            t["due"] or "no due", t["status"], tail))
            if reason:
                lines.append("   pinned: %s" % reason)
            if od is not None:
                lines.append("   exits: advance now start/done %s; reschedule postpone %s <new time>"
                             % (t["id"], t["id"]))
            if t.get("note"):
                lines.append("   note: %s" % t["note"])
            if t.get("blocker") or t.get("counter"):
                lines.append("   plan: blocker “%s” → counter “%s”"
                             % (t.get("blocker") or "(not set)", t.get("counter") or "(not set)"))
            if t.get("parent"):
                lines.append("   parent: %s" % t["parent"])
            if t.get("depends_on"):
                blocked = " (blocked by dependencies)" if _has_unfinished_deps(t) else ""
                lines.append("   deps: %s%s" % ("; ".join(t["depends_on"]), blocked))
            if t.get("tags"):
                lines.append("   tags: %s" % "; ".join(t["tags"]))
            if t.get("workspace"):
                lines.append("   workspace: %s" % t["workspace"])
            if t.get("links"):
                lines.append("   links: %s" % "; ".join(t["links"]))
    if not lines:
        print("(no todos with state %s)" % state)
        return 0
    print("\n".join(lines))
    return 0


def cmd_show(args):
    tid = args.id
    if re.match(r"^\d{4}-\d{2}$", tid):
        # 月度归档文件
        data = _load_archive(tid)
        print("# Archive %s (source files: %s, %d record(s))" % (
            tid, "; ".join(data["source_files"]) or "none", len(data["tasks"])))
        for t in data["tasks"]:
            print(_write_block(t))
            print("")
        return 0
    if re.match(r"^\d{4}-\d{2}-\d{2}$", tid):
        date = tid
        fdata = load_file(date)
        print("# Todos %s (archived: %s, schema: v%s)" % (date, fdata["archived"], fdata["schema"]))
        for t in fdata["tasks"]:
            print(_write_block(t))
            print("")
        return 0
    date, data, t = _find_task(tid)
    if t is None:
        print("Task %s not found" % tid, file=sys.stderr)
        return 2
    now = dt.datetime.now()
    print("file: %s (archived: %s, schema: v%s)" % (date, data["archived"], data["schema"]))
    print(_write_block(t))
    # 派生指标：算不出来的一律显示「—」/「暂无推算」，不编数字
    od, dd, sd = _overdue_days(t, now), _due_in_days(t, now), _stall_days(t, now)
    pf = _projected_finish(t, now)
    print("")
    print("overdue days: %s | due in: %s | stalled days: %s"
          % (_days_unknown(od), _days_unknown(dd), _days_unknown(sd)))
    print("projected finish: %s" % (pf or "N/A (no progress records)"))
    pin, reason = _pin_info(t, now)
    if pin is not None:
        print("pinned: %s" % reason)
    if od is not None:
        print("exits: advance now → start/done %s; reschedule → postpone %s <new time>" % (tid, tid))
    return 0


def cmd_index(args):
    if args.rebuild:
        idx = build_index()
    else:
        if not os.path.exists(INDEX_PATH):
            idx = build_index()
        else:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                idx = json.load(f)
    print(json.dumps(idx, ensure_ascii=False, indent=2))
    return 0


def _reformat_all_workspaces(style):
    """按指定路径风格重写全部存储文件中的工作空间，返回改动文件数。

    注意：这里直接操作存储文件原文（不经 load_file 的读取期规范化），
    以确保落盘内容真正统一为指定风格，而不仅是读取时归一化。"""
    if style not in ("windows", "posix"):
        return 0
    if not os.path.isdir(_storage_dir()):
        return 0
    changed = 0
    for fn in sorted(os.listdir(_storage_dir())):
        if not fn.endswith(".md"):
            continue
        date = fn[:-3]
        try:
            dt.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            continue
        fp = os.path.join(_storage_dir(), fn)
        with open(fp, "r", encoding="utf-8") as f:
            raw = f.read()
        new_raw = _reformat_workspace_lines(raw, style)
        if new_raw != raw:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_raw)
            changed += 1
    if changed:
        build_index()
    return changed


def _reformat_workspace_lines(raw, style):
    """把存储文件文本中所有 `工作空间: <path>` 行的分隔符统一为指定风格。"""
    if style == "windows":
        return re.sub(r"^(工作空间:\s*)(.+)$",
                      lambda m: m.group(1) + m.group(2).replace("/", "\\"),
                      raw, flags=re.M)
    return re.sub(r"^(工作空间:\s*)(.+)$",
                  lambda m: m.group(1) + m.group(2).replace("\\", "/"),
                  raw, flags=re.M)


def cmd_init(args):
    """识别当前工作环境并保存到 env.json，同时把已有工作空间统一为当前路径风格。

    存储目录与编辑器属于用户配置：已保存的不会被覆盖；编辑器未配置时自动探测一次。
    """
    env = _detect_env()
    env["defaults"] = _defaults_view()   # 记录当前生效的默认值，便于用 env --set 覆盖
    if not isinstance(env.get("editor"), dict) or not _norm(env["editor"].get("path")):
        detected = _detect_editor()
        if detected:
            env["editor"] = detected
    _save_env(env)
    n = _reformat_all_workspaces(env["path_style"])
    print("Environment detected and saved -> %s" % ENV_PATH)
    print(json.dumps(env, ensure_ascii=False, indent=2))
    if n:
        print("Normalized workspace paths in %d storage file(s) to %s format" % (n, env["path_style"]))
    else:
        print("Workspace paths normalized to %s format" % env["path_style"])
    print("Effective storage directory: %s" % _storage_dir())
    st = editor_status()
    if st["available"]:
        print("Editor detected: %s (%s)" % (st["label"] or "configured", st["path"]))
    else:
        print("No usable editor detected (%s); configure one if you need “open workspace in editor”:"
              % st["error"])
        print("  %s env --set editor.path=\"<absolute path to editor executable>\"" % _script_cmd())
    return 0


def _resolve_storage_setting(v):
    """把用户给的存储目录配置解析成绝对路径并校验可写。返回 (abs_path, error)。"""
    if not v:
        return None, "storage_dir must not be empty"
    p = os.path.abspath(os.path.expanduser(os.path.expandvars(v)))
    try:
        os.makedirs(p, exist_ok=True)
    except Exception as e:  # noqa: BLE001
        return None, "Cannot create storage directory %s: %s" % (p, e)
    if not os.access(p, os.W_OK):
        return None, "Storage directory not writable: %s" % p
    return p, None


def _resolve_editor_path(v):
    """校验编辑器 path：含分隔符按文件路径校验存在；否则按命令名校验在 PATH 中。"""
    if not v:
        return "editor.path must not be empty"
    p = os.path.expanduser(os.path.expandvars(v))
    seps = [s for s in (os.sep, os.altsep) if s]
    if os.path.isabs(p) or any(s in p for s in seps):
        if not os.path.isfile(p):
            return "Editor file not found: %s" % p
        return None
    import shutil
    if not shutil.which(p):
        return "Command %s not found in PATH (you can set the absolute path to the editor executable instead)" % p
    return None


def cmd_env(args):
    """查看 / 修改已保存的环境配置。

    --set KEY=VALUE 可多次，支持：
      path_style=windows|posix|mixed
      storage_dir=<目录>              （默认只改配置；旧目录有数据时加 --migrate 才搬迁）
      editor.path=<可执行文件|命令名>
      editor.label=<显示名>           （别名 editor.name）
      editor.args=<固定前置参数，分号分隔>
      defaults.status / defaults.importance / defaults.urgent
      ui.port=<1-65535>               （网页 UI 服务端口，默认 8796）
      ui.prompt=ask|off               （维护后未启动时弹框询问启动 / 关闭）
    --reset 重新探测环境（含编辑器）；--reformat-workspaces 统一工作空间分隔符。
    """
    old_storage = _storage_dir()
    env = _load_env()
    if args.reset:
        saved = _read_saved_env() or {}
        env = _detect_env()
        # 用户配置不会被探测冲掉：存储目录与编辑器由 _detect_env 保留，默认值单独保留
        if isinstance(saved.get("defaults"), dict):
            env["defaults"] = dict(saved["defaults"])
        detected = _detect_editor()
        if detected:
            env["editor"] = detected
        else:
            env.pop("editor", None)
    new_storage = None
    for kv in args.set or []:
        if "=" not in kv:
            print("Error: --set must be KEY=VALUE, e.g. path_style=windows", file=sys.stderr)
            return 2
        k, _, v = kv.partition("=")
        k, v = k.strip(), v.strip()
        if k == "path_style":
            if v not in _PATH_STYLES:
                print("Error: path_style only supports %s" % " / ".join(_PATH_STYLES), file=sys.stderr)
                return 2
            env["path_style"] = v
        elif k == "storage_dir":
            abs_p, err = _resolve_storage_setting(v)
            if err:
                print("Error: %s" % err, file=sys.stderr)
                return 2
            env.setdefault("dirs", {})["storage_dir"] = abs_p
            new_storage = abs_p
        elif k.startswith("editor."):
            ek = k[len("editor."):]
            if ek in ("label", "name"):
                env.setdefault("editor", {})["label"] = v
            elif ek == "path":
                err = _resolve_editor_path(v)
                if err:
                    print("Error: %s" % err, file=sys.stderr)
                    return 2
                env.setdefault("editor", {})["path"] = v
            elif ek == "args":
                env.setdefault("editor", {})["args"] = v
            else:
                print("Error: unsupported editor config key %s (supported: editor.path / editor.label / editor.args)"
                      % k, file=sys.stderr)
                return 2
        elif k.startswith("defaults."):
            # 覆盖新增待办的默认值（只是预填，任何时候都能改）
            dk = k[len("defaults."):]
            if dk not in DEFAULT_KEYS:
                print("Error: unsupported defaults key %s (supported: %s)" % (k, " / ".join(
                    "defaults." + x for x in DEFAULT_KEYS)), file=sys.stderr)
                return 2
            allowed = {"status": STATUS_SET, "importance": IMPORTANCE_SET, "urgent": URGENT_SET}[dk]
            if v not in allowed:
                print("Error: defaults.%s only supports %s" % (dk, " / ".join(sorted(allowed))), file=sys.stderr)
                return 2
            env.setdefault("defaults", {})[dk] = v
        elif k.startswith("ui."):
            uk = k[len("ui."):]
            if uk == "port":
                if not re.fullmatch(r"\d{1,5}", v) or not (1 <= int(v) <= 65535):
                    print("Error: ui.port must be a port number from 1 to 65535", file=sys.stderr)
                    return 2
                env.setdefault("ui", {})["port"] = int(v)
            elif uk == "prompt":
                if v not in ("ask", "off"):
                    print("Error: ui.prompt only supports ask (default; prompt when not running) / off (disabled)",
                          file=sys.stderr)
                    return 2
                env.setdefault("ui", {})["prompt"] = v
            else:
                print("Error: unsupported web UI config key %s (supported: ui.port / ui.prompt)" % k,
                      file=sys.stderr)
                return 2
        elif k.startswith("capture."):
            # 捕获服务配置（快捷键读剪贴板 -> 分诊）：enabled / hotkey / triage_types.* /
            # confirm_delete / toast
            ck = k[len("capture."):]
            if ck == "enabled":
                env.setdefault("capture", {})["enabled"] = _str_to_bool(v)
            elif ck == "hotkey":
                mods, err = _hotkey_parse(v)
                if mods is None:
                    print("Error: %s" % err, file=sys.stderr)
                    return 2
                env.setdefault("capture", {})["hotkey"] = v
            elif ck == "confirm_delete":
                env.setdefault("capture", {})["confirm_delete"] = _str_to_bool(v)
            elif ck == "toast":
                env.setdefault("capture", {})["toast"] = _str_to_bool(v)
            elif ck.startswith("triage_types."):
                a = ck[len("triage_types."):]
                if a not in TRIAGE_TYPES_ALL:
                    print("Error: unsupported capture.triage_types key %s (supported: %s)"
                          % (k, " / ".join("capture.triage_types." + x for x in TRIAGE_TYPES_ALL)),
                          file=sys.stderr)
                    return 2
                env.setdefault("capture", {}).setdefault("triage_types", {})[a] = _str_to_bool(v)
            else:
                print("Error: unsupported capture config key %s (supported: capture.enabled / "
                      "capture.hotkey / capture.triage_types.add|update|delete|status / "
                      "capture.confirm_delete / capture.toast)" % k, file=sys.stderr)
                return 2
        else:
            print("Error: unsupported config key %s (supported: path_style / storage_dir / editor.path / "
                  "editor.label / editor.args / defaults.* / ui.port / ui.prompt / capture.*)" % k,
                  file=sys.stderr)
            return 2
    # 存储目录变更：旧目录还有待办时必须让用户显式二选一，不能悄悄改配置把数据落下
    storage_changed = bool(new_storage) and os.path.abspath(new_storage) != os.path.abspath(old_storage)
    old_files = old_tasks = 0
    if storage_changed:
        old_files, old_tasks = _storage_file_stats(old_storage)
        if old_files and not (args.migrate or args.no_migrate):
            print("Error: the old storage directory still has %d file(s) (%d todo(s)): %s"
                  % (old_files, old_tasks, old_storage), file=sys.stderr)
            print("Choose one explicitly (config unchanged so far):", file=sys.stderr)
            print("  move data too: %s env --set storage_dir=\"%s\" --migrate"
                  % (_script_cmd(), new_storage), file=sys.stderr)
            print("  config only, keep data: %s env --set storage_dir=\"%s\" --no-migrate"
                  % (_script_cmd(), new_storage), file=sys.stderr)
            return 2
    if args.reset or args.set:
        env["updated"] = _fmt(dt.datetime.now())
        _save_env(env)
    if storage_changed and old_files:
        if args.migrate:
            ok, msg = _migrate_storage(old_storage, new_storage)
            if ok:
                print("Migration done: %s" % msg)
                build_index()
            else:
                # 搬迁失败就把配置回滚，绝不留下「指向空目录」的假状态
                env.setdefault("dirs", {})["storage_dir"] = old_storage
                env["updated"] = _fmt(dt.datetime.now())
                _save_env(env)
                print("Migration incomplete: %s" % msg, file=sys.stderr)
                print("Config rolled back to the original directory: %s" % old_storage, file=sys.stderr)
                return 1
        else:
            print("Config changed, data not migrated; the old directory still has %d file(s) (%d todo(s)): %s"
                  % (old_files, old_tasks, old_storage))
    reformat_n = 0
    if args.reformat_workspaces:
        reformat_n = _reformat_all_workspaces(env.get("path_style"))
    out = {k: v for k, v in env.items() if not k.startswith("_")}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("Effective defaults (prefilled for new todos; overridable anytime):")
    print(json.dumps(_defaults_view(), ensure_ascii=False))
    print("Week boundary: Monday is the start (WEEK_START_ISO=%d)" % WEEK_START_ISO)
    print("Effective storage directory: %s" % _storage_dir())
    print("Web UI service: port %d; check & ask to start after changes: %s (%s env --set ui.prompt=off to disable)"
          % (_ui_port(), "enabled" if _ui_prompt_enabled() else "disabled", _script_cmd()))
    cap = _capture_view()
    print("Capture service (hotkey reads clipboard -> triage): %s | hotkey %s%s | triage types: %s | confirm delete: %s | toast: %s"
          % ("enabled" if cap.get("enabled") else "disabled", cap.get("hotkey"),
             "" if cap.get("hotkey_valid") else " (%s)" % cap.get("hotkey_error"),
             ", ".join(a for a in TRIAGE_TYPES_ALL if cap.get("triage_types", {}).get(a)),
             "yes" if cap.get("confirm_delete") else "no", "yes" if cap.get("toast") else "no"))
    st = editor_status()
    if st["available"]:
        print("Effective editor: %s (%s)" % (st["label"] or "configured", st["path"]))
    else:
        print("Effective editor: not configured or unavailable (%s)" % st["error"])
        print("  configure: %s env --set editor.path=\"<absolute path to editor executable>\"" % _script_cmd())
    if args.reformat_workspaces:
        if reformat_n:
            print("Normalized workspace paths in %d storage file(s) to %s format" % (reformat_n, env["path_style"]))
        else:
            print("Workspace paths normalized to %s format" % env["path_style"])
    elif env.get("_inferred"):
        print("(hint: environment config not saved yet; run `init` to detect and save it.)")
    return 0


# ---- 网页 UI 服务：维护后检查与询问启动 -----------------------------------
# 触发规则：AI（会话 / 大语言模式）或 CLI 成功「添加 / 维护」一条待办后，检查本地网页
# 服务（web/server.py，默认 http://127.0.0.1:8796/）是否在运行；未运行时按 ui.prompt
# 配置弹框询问用户是否启动 UI，用户选择启动则后台拉起服务并自动打开浏览器。
# 关闭方式：env.json 的 ui.prompt=off，或临时环境变量 AWAM_TODO_UI_PROMPT=off（自测/CI 用）。


def _ui_config():
    """读取 env.json 的 ui 段（网页服务配置），缺失返回空 dict。"""
    env = _load_env()
    ui = env.get("ui")
    return ui if isinstance(ui, dict) else {}


def _ui_port():
    """网页服务端口：env.json ui.port，缺省 8796（与 web/server.py 默认一致）。"""
    try:
        return int(_ui_config().get("port") or UI_DEFAULT_PORT)
    except (TypeError, ValueError):
        return UI_DEFAULT_PORT


def _ui_prompt_enabled():
    """维护后是否检查并询问启动网页 UI。环境变量可临时关闭（自测/CI）。"""
    v = os.environ.get("AWAM_TODO_UI_PROMPT", "").strip().lower()
    if v in ("off", "0", "no", "false"):
        return False
    if v in ("on", "1", "yes", "true"):
        return True
    v = str(_ui_config().get("prompt") or UI_PROMPT_MODE_DEFAULT).strip().lower()
    return v not in ("off", "0", "no", "false")


def _ui_url(port=None):
    return "http://127.0.0.1:%d/" % (port or _ui_port())


def _ui_server_running(port=None):
    """探测本地网页服务是否已启动：根路径能返回响应即视为在运行（只读，不落盘）。"""
    port = port or _ui_port()
    try:
        import urllib.request
        with urllib.request.urlopen(_ui_url(port), timeout=1.0) as resp:
            return resp.status < 500
    except Exception:
        return False


def _ui_server_py():
    """网页服务脚本路径：env.json 的 dirs.skill_dir 优先，其次按本文件位置推算。"""
    env = _load_env()
    skill_dir = (env.get("dirs") or {}).get("skill_dir") or SKILL_DIR
    return os.path.join(skill_dir, "web", "server.py")


def _start_ui_server(port=None, no_browser=False):
    """后台拉起 web/server.py（默认会自动打开浏览器），轮询确认真的在监听。

    no_browser=True 时不自动打开浏览器（测试用）。返回 True=已启动 / False=启动失败。"""
    port = port or _ui_port()
    server_py = _ui_server_py()
    if not os.path.exists(server_py):
        print("Web server script not found: %s" % server_py, file=sys.stderr)
        return False
    argv = [sys.executable, server_py]
    if port != UI_DEFAULT_PORT:
        argv += ["--port", str(port)]
    if no_browser:
        argv += ["--no-browser"]
    kwargs = {"cwd": os.path.dirname(os.path.dirname(server_py)),
              "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL,
              "close_fds": True}
    if os.name == "nt":
        # 脱离进程组：不随调用方退出，也不占住调用方的管道
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    try:
        subprocess.Popen(argv, **kwargs)
    except Exception as e:
        print("Failed to start web server: %s" % e, file=sys.stderr)
        return False
    # 轮询确认服务真的起来了（最多约 2 秒），避免「说启动了但端口没监听」
    for _ in range(8):
        if _ui_server_running(port):
            return True
        time.sleep(0.25)
    return False


def _ask_start_ui(port=None):
    """弹系统对话框询问是否启动网页 UI。返回 True=启动 / False=不启动 / None=无法弹框。"""
    port = port or _ui_port()
    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception:
        return None
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        ans = messagebox.askyesno(
            "awam-todo Web UI",
            "The local web UI is not running (%s).\nStart it now?" % _ui_url(port))
        root.destroy()
        return bool(ans)
    except Exception:
        return None


def _ui_prompt_needed(args):
    """本次命令是否属于「添加 / 维护待办」成功后触发检查的范围（只读命令不触发）。"""
    if args.cmd in UI_PROMPT_MUTATING_CMDS:
        return True
    if args.cmd == "dep":
        # dep 不带任何改动参数时只是查看，不触发
        return bool(args.deps or args.add or args.remove or args.clear)
    return False


def _maybe_ui_prompt(args):
    """维护命令成功落盘后调用：检查本地网页服务，未启动时询问用户是否启动 UI。"""
    if not _ui_prompt_needed(args) or not _ui_prompt_enabled():
        return
    port = _ui_port()
    if _ui_server_running(port):
        return  # 服务已在运行，不打扰
    url = _ui_url(port)
    manual = 'python "%s"' % _ui_server_py()
    choice = _ask_start_ui(port)
    if choice is None:
        # 无法弹框（无图形环境等）：只提示，不阻塞命令
        print("Note: local web UI is not running (%s); start it with: %s" % (url, manual))
        return
    if choice:
        if _start_ui_server(port):
            print("Web UI started: %s (the browser will open automatically)" % url)
        else:
            print("Failed to start web UI; start it manually: %s" % manual, file=sys.stderr)
    else:
        print("Skipped starting the web UI (start it with: %s when needed)" % manual)


def main():
    p = argparse.ArgumentParser(prog="awam-todo", description="Capture and manage personal todos")
    sub = p.add_subparsers(dest="cmd")

    pa = sub.add_parser("add", help="add a todo (identical -> update by default; similar -> ask first)")
    pa.add_argument("--text", required=True)
    # 下列字段默认 None：更新已有任务时仅覆盖用户显式传入的项
    pa.add_argument("--importance", choices=["重要", "不重要"], default=None)
    pa.add_argument("--urgent", choices=["紧急", "不紧急"], default=None, help="urgency level")
    pa.add_argument("--status", choices=["维护", "进行中", "结束", "待开始", "其他"], default=None)
    pa.add_argument("--note", default=None)
    pa.add_argument("--blocker", default=None, help="the obstacle most likely to block me (optional; shown on the card)")
    pa.add_argument("--counter", default=None, help="counter-plan: if the blocker shows up, I will … (optional)")
    pa.add_argument("--workspace", default=None)
    pa.add_argument("--docs", default=None, help="related docs, separated by ;")
    pa.add_argument("--links", default=None, help="links, separated by ;")
    pa.add_argument("--deps", default=None, help="dependency task IDs, separated by ; (e.g. T-A;T-B)")
    pa.add_argument("--tags", default=None, help="tags, separated by ; (e.g. 工作;紧急)")
    pa.add_argument("--parent", default=None, help="parent task ID (this todo becomes its subtask)")
    pa.add_argument("--due", default=None, help="natural-language time, e.g. 明天 / 星期五 / 2026-10-05 10:00")
    pa.add_argument("--date", default="", help="store into the given date file YYYY-MM-DD (default: today)")
    pa.add_argument("--from-type", default="agent", help="source type, e.g. agent/link/web (default: agent)")
    pa.add_argument("--from-url", default=None, help="source URL (e.g. an AI conversation link); omit to not record")
    pa.add_argument("--force", action="store_true", help="skip duplicate detection and force-create")
    pa.add_argument("--update-id", default="", help="after confirmation, update this existing todo instead of creating")

    pc = sub.add_parser("check", help="check whether the text is identical/similar to existing todos (read-only)")
    pc.add_argument("--text", required=True)
    pc.add_argument("--exclude-id", default="", help="task ID to exclude from comparison")

    ptg = sub.add_parser("triage", help="triage: judge whether a paragraph means add / update / delete / change status (read-only, JSON output; exit 3 when confirmation is needed)")
    ptg.add_argument("--text", required=True, help="the paragraph to judge (e.g. clipboard content)")

    pdel = sub.add_parser("delete", help="delete a todo (also cleans other todos' dependency / parent references to it)")
    pdel.add_argument("id")

    pts = sub.add_parser("suggest-tags", help="suggest tags (suggestion only, nothing is written; JSON output)")
    pts.add_argument("--text", required=True, help="todo content")
    pts.add_argument("--note", default="", help="note (also used as a hint)")
    pts.add_argument("--workspace", default="", help="workspace path (also used as a hint)")

    pd = sub.add_parser("done", help="mark done (auto-archive the file when all tasks are done; unfinished deps require confirmation)")
    pd.add_argument("id")
    pd.add_argument("--force", action="store_true", help="ignore the unfinished-dependency check and force-done")
    ps = sub.add_parser("start", help="mark in progress (unfinished deps require confirmation)")
    ps.add_argument("id")
    ps.add_argument("--force", action="store_true", help="ignore the unfinished-dependency check and force-start")
    pw = sub.add_parser("work", aliases=["continue"],
                        help="continue: mark in progress and open the workspace with the configured editor (unfinished deps require confirmation)")
    pw.add_argument("id")
    pw.add_argument("--force", action="store_true", help="ignore the unfinished-dependency check and force-start")
    pr = sub.add_parser("reopen", help="reopen (back to 待开始)")
    pr.add_argument("id")
    ppo = sub.add_parser("postpone", aliases=["reschedule", "replan"],
                         help="reschedule: reset/clear the deadline (the second exit for overdue todos)")
    ppo.add_argument("id")
    ppo.add_argument("due", nargs="?", default="",
                     help="new time, e.g. 明天 / 下周一 / 3天后 / 2026-10-20 10:00")
    ppo.add_argument("--clear", action="store_true", help="clear the deadline")
    pmi = sub.add_parser("migrate", help="migrate old storage files to the current schema (preview by default; --apply runs it)")
    pmi.add_argument("--apply", action="store_true", help="actually run the migration (default: preview only)")
    pma = sub.add_parser("archive-month", aliases=["monthly-archive"],
                         help="monthly archive: merge archivable day files into storage/archive/YYYY-MM.md")
    pma.add_argument("--month", default="", help="month YYYY-MM; default: files earlier than the current month")
    pma.add_argument("--all", action="store_true", help="include the current month")
    pma.add_argument("--dry-run", action="store_true", help="preview only, write nothing")
    pdep = sub.add_parser("dep", help="set / view task dependencies (with existence and cycle checks)")
    pdep.add_argument("id")
    pdep.add_argument("deps", nargs="*", help="set (replace) the dependency task ID list")
    pdep.add_argument("--add", nargs="+", default=[], help="append dependency task IDs")
    pdep.add_argument("--remove", nargs="+", default=[], help="remove dependency task IDs")
    pdep.add_argument("--clear", action="store_true", help="clear dependencies")
    pch = sub.add_parser("children", aliases=["sub"], help="list subtasks of a parent task")
    pch.add_argument("id")
    pdp = sub.add_parser("deparent", help="detach a subtask from its parent")
    pdp.add_argument("id")
    par = sub.add_parser("archive", help="force-archive a date file (all tasks must be done)")
    par.add_argument("date")
    pl = sub.add_parser("list", help="list todos")
    pl.add_argument("--date", default="")
    pl.add_argument("--state", choices=["维护", "进行中", "结束", "待开始", "其他",
                                        "urgent", "overdue", "today", "all"], default="all")
    psh = sub.add_parser("show", help="view a task / a day file / a monthly archive (YYYY-MM)")
    psh.add_argument("id")
    pi = sub.add_parser("index", help="view / rebuild the index")
    pi.add_argument("--rebuild", action="store_true")

    pinit = sub.add_parser("init", help="detect the environment and save it to env.json (path style / storage dir / editor, normalize workspaces)")
    penv = sub.add_parser("env", help="view / modify saved environment config (path style / storage dir / editor / defaults)")
    penv.add_argument("--set", action="append", default=[],
                      help="KEY=VALUE, repeatable; supports path_style=windows|posix|mixed, "
                           "storage_dir=<dir>, editor.path / editor.label / editor.args, "
                           "defaults.status|defaults.importance|defaults.urgent")
    penv.add_argument("--migrate", action="store_true",
                      help="with --set storage_dir: move todos from the old directory to the new one (copy first, delete old only after verification)")
    penv.add_argument("--no-migrate", action="store_true",
                      help="with --set storage_dir: change config only, explicitly do not move data and stop asking")
    penv.add_argument("--reset", action="store_true", help="re-detect the environment and save (including the editor)")
    penv.add_argument("--reformat-workspaces", action="store_true",
                      help="normalize workspace paths in all storage files to the current path_style")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 0
    handlers = {
        "add": lambda a: cmd_add(a),
        "check": lambda a: cmd_check(a),
        "triage": lambda a: cmd_triage(a),
        "delete": lambda a: cmd_delete(a),
        "suggest-tags": lambda a: cmd_suggest_tags(a),
        "done": lambda a: cmd_done(a),
        "start": lambda a: cmd_start(a),
        "work": lambda a: cmd_work(a),
        "reopen": lambda a: cmd_reopen(a),
        "postpone": lambda a: cmd_postpone(a),
        "reschedule": lambda a: cmd_postpone(a),
        "replan": lambda a: cmd_postpone(a),
        "migrate": lambda a: cmd_migrate(a),
        "archive-month": lambda a: cmd_monthly_archive(a),
        "monthly-archive": lambda a: cmd_monthly_archive(a),
        "dep": lambda a: cmd_dep(a),
        "children": lambda a: cmd_children(a),
        "sub": lambda a: cmd_children(a),
        "deparent": lambda a: cmd_deparent(a),
        "archive": lambda a: cmd_archive(a),
        "list": lambda a: cmd_list(a),
        "show": lambda a: cmd_show(a),
        "index": lambda a: cmd_index(a),
        "init": lambda a: cmd_init(a),
        "env": lambda a: cmd_env(a),
    }
    code = handlers[args.cmd](args)
    if code == 0:
        # 添加 / 维护待办成功后：检查本地网页服务，未启动时询问用户是否启动 UI
        _maybe_ui_prompt(args)
    return code


if __name__ == "__main__":
    sys.exit(main())
