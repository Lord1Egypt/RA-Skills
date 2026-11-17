#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""runtime.py —— dingtalk_auto_reply 技能的基础层（可移植 + 运行期健壮性 + 共享配置）。

包含：
  - 轻量 .env 加载器（零依赖，保证可移植）
  - CodeBuddy Agent SDK 可用性探测（_SDK_AVAILABLE）
  - 路径自动探测（DWS / CodeBuddy / node / 微信推送等二进制）
  - 全部共享常量（二进制路径、模型/认证、工作空间、运行开关、视觉、缓存/锁/审计等）
  - 运行期健壮性辅助：日志轮转、单实例锁、媒体缓存清理
  - 鉴权与日志：log_debug / log_audit / 认证健康检查

其它模块通过 `from runtime import (...)` 复用这里的一切；入口 dingtalk_unread_monitor.py
再统一 re-export，保证旧的 `import dingtalk_unread_monitor as M` 调用方无需改动。

注意：会被运行时修改的「可变配置」（DRY_RUN、SELF_OPEN_ID）在子模块里一律通过
`runtime.DRY_RUN` / `runtime.SELF_OPEN_ID` 访问（模块属性而非 import 副本），
确保 recover_missed.py 等外部脚本 `runtime.DRY_RUN = False` 能真正生效。
"""
import subprocess, json, time, os, datetime, socket, glob, re, sys, base64

# 无窗口标志：Windows 上让子进程（node/dws/cmd）不弹控制台黑框；非 Windows 上为 0（忽略）。
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


# ---------- 轻量 .env 加载器（零依赖，保证可移植） ----------
def parse_env_text(text):
    """把 .env 文本解析为 {KEY: VALUE} 字典（纯函数，供 _load_env_file /
    _setup_env.py 复用，消除两处重复解析逻辑）。
    支持的写法：KEY=VALUE、KEY="带空格的值"、# 注释、空行。"""
    out = {}
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        if not k:
            continue
        # 去首尾引号
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        out[k] = v
    return out


def _load_env_file(path):
    """加载 .env 到 os.environ（已存在的环境变量不被覆盖，.env 只补缺）。
    返回加载的 key 数。"""
    if not path or not os.path.exists(path):
        return 0
    n = 0
    try:
        with open(path, encoding="utf-8") as f:
            for k, v in parse_env_text(f.read()).items():
                if k not in os.environ:   # 不覆盖已存在的环境变量
                    os.environ[k] = v
                    n += 1
    except Exception:
        pass
    return n


# 技能目录下的 .env（cp .env.example .env 后填写）。必须在所有 _resolve 之前加载，
# 这样 .env 里的显式路径/参数能覆盖自动探测默认值。
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
_load_env_file(os.path.join(_SKILL_DIR, ".env"))

# CodeBuddy Agent SDK（生成回复的唯一后端；未装则无法自动回复，调用方走「不代发」逻辑）
# 装法：pip install codebuddy-agent-sdk（装到运行本脚本的 python 环境）
try:
    from codebuddy_agent_sdk import (
        query as _sdk_query, CodeBuddyAgentOptions, AppendSystemPrompt,
        AssistantMessage, TextBlock, ResultMessage,
        # ⚠️ 2026-08-03 流式轨迹调试：思考/工具调用/工具结果 block（DEBUG_AGENT_TRACE=1 时
        # reply.py 把它们打进日志，排查「agent 到底调没调 dws / 查到了什么」）
        ThinkingBlock, ToolUseBlock, ToolResultBlock,
    )
    _SDK_AVAILABLE = True
except ImportError:
    # 即便 SDK 未装，也把这些名字定义为 None，供 vision.py / reply.py 顶层
    # `from runtime import (...)` 能成功；它们内部都有 _SDK_AVAILABLE 守卫，不会真正调用。
    _SDK_AVAILABLE = False
    _sdk_query = CodeBuddyAgentOptions = AppendSystemPrompt = None
    AssistantMessage = TextBlock = ResultMessage = None
    ThinkingBlock = ToolUseBlock = ToolResultBlock = None

# ---------- SDK 运行环境（显式声明，安装时由 _setup_env.py 写入 .env） ----------
# 装了 codebuddy-agent-sdk 的 python 解释器绝对路径。skill 运行时若被错误的 python 拉起
# （当前解释器没装 SDK），monitor 的 __main__ 守卫会用这个 python 重新拉起自己，保证 SDK
# 一定可用。留空 = 用当前解释器（要求自身已装 SDK）。agent 安装时跑 _setup_env.py 自动探测写入。
CODEBUDDY_SDK_PYTHON = os.environ.get("CODEBUDDY_SDK_PYTHON", "")


def sdk_reexec_target():
    """返回应当用来「重拉」本进程的 python 路径；无需/无法重拉返回 None。

    场景：本 skill 被某个不含 SDK 的 python 拉起（如裸 managed python、系统 python），
    但 .env 里 CODEBUDDY_SDK_PYTHON 指向另一个确实装了 SDK 的解释器。monitor __main__
    守卫调用本函数，若返回非空则用 os.execv 以该 python 重拉（保留 os.environ）。

    防死循环：仅当「当前无 SDK」且「目标存在」且「目标 ≠ 当前解释器」才返回目标；
    重拉后子进程 sys.executable == 目标，再次进入守卫时目标==自身 → 返回 None，不再重拉。
    """
    sdk_py = CODEBUDDY_SDK_PYTHON
    if _SDK_AVAILABLE or not sdk_py:
        return None
    sdk_py = os.path.abspath(sdk_py)
    if not os.path.isfile(sdk_py):
        return None
    if sdk_py == os.path.abspath(sys.executable):
        return None
    return sdk_py


# ---------- 路径自动探测（可移植核心） ----------
def _ver_key(path):
    """按路径中的数字段做数值版本排序（替代字典序 reverse=True）。
    ⚠️ 字典序会把 '22.9.1' 排在 '22.10.1' 之后（'9' > '1'），选错 node/codebuddy 版本；
    re 已在模块顶部 import。"""
    parts = re.findall(r'\d+', os.path.basename(path))
    return tuple(int(x) for x in parts) if parts else (-1,)


def _resolve(explicit, fixed_subpath, versioned_glob=None):
    """优先级：环境变量显式覆盖 → 固定子路径(~下) → 版本目录 glob(取最新的) → 固定子路径串兜底"""
    if explicit and os.environ.get(explicit):
        return os.environ[explicit]
    home = os.path.expanduser("~")
    if fixed_subpath:
        cand = os.path.join(home, fixed_subpath)
        if os.path.exists(cand):
            return cand
    if versioned_glob:
        matches = sorted(glob.glob(os.path.join(home, versioned_glob)), key=_ver_key, reverse=True)
        for m in matches:
            if os.path.exists(m):
                return m
    # 兜底：返回最可能的绝对路径串（即便不存在，便于报错提示）
    if fixed_subpath:
        return os.path.join(home, fixed_subpath)
    return ""


def _bin_exts():
    """当前平台下可执行文件可能的扩展名候选（含空串）。
    Windows：先 .cmd 后 .exe 最后无扩展；POSIX：仅无扩展。"""
    if sys.platform.startswith("win"):
        return [".cmd", ".exe", ""]
    return [""]


def _resolve_bin(explicit_env, subpath_no_ext, versioned_glob_no_ext=None):
    """针对可执行文件的分平台路径解析（在 _resolve 基础上按平台尝试扩展名）。
    用于 dws / codebuddy / node —— 它们在 Windows 是 .cmd/.exe，在 POSIX 无扩展名。
    优先级：环境变量显式覆盖 → 固定子路径(带平台扩展名) → 版本目录 glob(带扩展名) → 兜底串。"""
    if explicit_env and os.environ.get(explicit_env):
        return os.environ[explicit_env]
    home = os.path.expanduser("~")
    for ext in _bin_exts():
        if subpath_no_ext:
            cand = os.path.join(home, subpath_no_ext + ext)
            if os.path.exists(cand):
                return cand
        if versioned_glob_no_ext:
            for m in sorted(glob.glob(os.path.join(home, versioned_glob_no_ext + ext)), key=_ver_key, reverse=True):
                if os.path.exists(m):
                    return m
    if subpath_no_ext:
        return os.path.join(home, subpath_no_ext + _bin_exts()[0])
    return ""


def _scan_local_storage(matcher):
    """遍历 ~/.codebuddy/local_storage 下 entry_*.info 文件，用 matcher(文本) 判定。
    返回 True=任一文件命中；False=目录缺失/无 entry 文件/全部未命中。
    _detect_china_edition 与 _cli_credentials_present 共用此遍历逻辑（消除重复）。"""
    try:
        ls_dir = os.path.join(os.path.expanduser("~"), ".codebuddy", "local_storage")
        if not os.path.isdir(ls_dir):
            return False
        for fn in os.listdir(ls_dir):
            if not fn.startswith("entry_") or not fn.endswith(".info"):
                continue
            try:
                with open(os.path.join(ls_dir, fn), encoding="utf-8", errors="ignore") as f:
                    if matcher(f.read()):
                        return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def _detect_china_edition():
    """检测是否为中国版（api.copilot.tencent.com）。
    CodeBuddy CLI 把网络环境标记存在 ~/.codebuddy/local_storage/ 下某个 entry 文件，
    内容恰好是字符串 "internal"（已在本机确认：某个 entry_*.info = "internal"）。
    命中即中国版，生成时须注入 CODEBUDDY_INTERNET_ENVIRONMENT=internal，否则连不上。
    返回 True/False。"""
    return _scan_local_storage(lambda txt: '"internal"' in txt)


DWS_CMD = _resolve_bin("DWS_CMD",
                        os.path.join(".workbuddy", "binaries", "node", "cli-connector-packages", "dws"))
CODEBUDDY_CMD = _resolve_bin("CODEBUDDY_CMD", None,
                             os.path.join(".workbuddy", "binaries", "node", "versions", "*", "codebuddy"))
NODE = _resolve_bin("NODE", None,
                   os.path.join(".workbuddy", "binaries", "node", "versions", "*", "node"))
SEND_JS = _resolve("WEIXIN_SEND_JS",
                   os.path.join(".workbuddy", "skills", "weixinclaw-proactive-push", "send.js"))
# dws 的 node 入口：直接 node 调它（绕过 cmd /c），避免中文/emoji/特殊字符(< > | &)
# 经 cmd 代码页转换导致乱码，或被 shell 元字符截断（老板回复里偶尔含这些字符）。
DWS_ENTRY = _resolve("DWS_ENTRY", None,
                         os.path.join(".workbuddy", "binaries", "node", "cli-connector-packages",
                                      "node_modules", "dingtalk-workspace-cli", "bin", "dws.js"))

# dws.exe 直接路径（绕过 node + dws.js 壳），为 run_dws 首选调用目标（最快）。
# 根因（2026-07-15 石锤 + 重启验证）：dws.exe 是 Node 打包二进制，其对匿名管道（PIPE）的
# stdout 异步写会在进程退出前丢失 → 管道读到 0 字节；与父进程是否控制台无关（python.exe
# console 环境重启后仍复现）。故所有 dws 调用统一用临时文件承接 stdout（见 _run_dws_once）。
DWS_EXE = _resolve("DWS_EXE", None,
                    os.path.join(".workbuddy", "binaries", "node", "cli-connector-packages",
                                 "node_modules", "dingtalk-workspace-cli", "vendor", "dws.exe"))

# CodeBuddy 认证：自动化场景首选 API Key（README 明确推荐）；未设则复用 CLI 已登录凭据。
CODEBUDDY_API_KEY = os.environ.get("CODEBUDDY_API_KEY", "")  # 来自 .env 或环境变量；空串=用 CLI 凭据
# 中国版标记（auto 检测 ~/.codebuddy/local_storage 下 entry="internal"）
CHINA_EDITION = _detect_china_edition()
# 当前使用的 CodeBuddy 主模型（deepseek-v4-flash）。SDK 调用统一从这里取，单一真实来源：
# 环境变量 CODEBUDDY_MODEL 可覆盖（如切其它账户支持的模型），不配置则默认 deepseek-v4-flash。
CODEBUDDY_MODEL = os.environ.get("CODEBUDDY_MODEL", "deepseek-v4-flash")

# dws 实际调用追踪（测试/排查用）：DEBUG_DWS_CALL=1 时，每次 dws 调用都记录
# 实际 argv（NODE-direct 还是 DWS_CMD 兜底）、返回码、stdout 长度 —— 便于把
# 「配置的路径」与「实际 invoked 的命令」做比对，定位 PATH/入口解析问题。
# 今天排查石锤：dws 不在 PATH 上会导致进程/终端找不到 dws；本开关是排障比对手段。
_DWS_CALL_TRACE = os.environ.get("DEBUG_DWS_CALL") == "1"

# 钉钉自动回复工作空间（cwd）：CodeBuddy 自动加载该空间记忆
# （~/.workbuddy/.../MEMORY.md），agent 也可经 Write/Edit 写回此文件做长期记忆。
# 工作空间名随机器可能不同 → 用环境变量 DINGTALK_WORKSPACE 覆盖（默认本机路径）。
DINGTALK_WORKSPACE = os.environ.get(
    "DINGTALK_WORKSPACE",
    os.path.join(os.path.expanduser("~"), "WorkBuddy", "dingtalk_auto_reply"))
# 老板在钉钉的身份（userId），过滤"我名下"（项目/待办）统一用这个。
# 隐私：真值只在私密 .env 的 BOSS_UID 里，源码默认空串（强制新用户到 .env 配置）。
BOSS_UID = os.environ.get("BOSS_UID", "")
# 老板钉钉昵称/姓名（仅用于查表 grounding 提示词的人称，如"X名下"）；默认中性词"老板"。
BOSS_NAME = os.environ.get("BOSS_NAME", "老板")
# 公司身份与职位（仅用于回复人设的"你是某公司某职位员工、平级回同事"语境，
# 让 agent 以普通员工身份而非上级口吻回同事；真值在私密 .env 的 BOSS_COMPANY/BOSS_TITLE，
# 源码默认中性词，不硬编码真实公司/职位隐私）。
BOSS_COMPANY = os.environ.get("BOSS_COMPANY", "本公司")
BOSS_TITLE = os.environ.get("BOSS_TITLE", "工程师")

# 多维表结构（老板专属配置）：全部经环境变量注入，源码不硬编码任何
# baseId/tableId/字段 ID（隐私安全，随包分发不会泄漏）。
# 填法见 .env.example 的「多维表 grounding」段；不填则 fetch_table_context 自动退化为纯人设代复。
# ⚠️ 易混点：ROS_* 与 FB_* 是「检查ROS项目和待解决问题」定时任务盯的【两张不同的表】，
#   不是"ROS 表 + 飞书表"。FB_* 即「问题实时反馈与更新需求汇总」表（第二张）。
#   两张表都属 ROS 检查定时任务，回复时务必区分，不要混淆。
FB_BASE = os.environ.get("FB_BASE", "")        # 问题实时反馈与更新需求汇总 表（ROS 检查·表2）base
FB_TAB = os.environ.get("FB_TAB", "")        # 问题实时反馈与更新需求汇总 表 table
FB_STATUS = os.environ.get("FB_STATUS", "")    # 解决状态字段（≠"已解决"=待解决）
FB_HANDLER = os.environ.get("FB_HANDLER", "")   # 处理人字段（成员，userId 匹配 BOSS_UID）
FB_SUMM = os.environ.get("FB_SUMM", "")      # 问题概要字段
ROS_BASE = os.environ.get("ROS_BASE", "")      # ROS软件项目管理表（ROS 检查·表1）base
ROS_TAB = os.environ.get("ROS_TAB", "")       # ROS软件项目管理表 table
ROS_PROG = os.environ.get("ROS_PROG", "")     # 进度字段
ROS_OWNER = os.environ.get("ROS_OWNER", "")   # 负责人字段（成员，userId 匹配 BOSS_UID）
ROS_NAME = os.environ.get("ROS_NAME", "")      # 项目名称字段
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))  # 秒，可环境变量调
DEBUG_LOG = os.path.expanduser("~/.workbuddy/dingtalk_auto_debug.log")
DEBUG_LOG_MAX = 1024 * 1024            # 调试日志单文件上限 1MB，超出重命名为 .1（保留一份回溯）
LOCK_FILE = os.path.expanduser("~/.workbuddy/dingtalk_auto.lock")  # 旧 PID 文件锁残留路径（已弃用，仅清理用）
LOCK_PORT = 18733   # 单实例锁端口：bind 127.0.0.1:LOCK_PORT 成功者持有，其余失败退出
_LOCK_SOCK = None  # 持锁 socket（全局，进程退出时 close 释放端口）
DRY_RUN = os.environ.get("DRY_RUN") == "1"
TEST_MODE = os.environ.get("TEST_MODE") == "1"    # 测试模式：生成的回复只发给老板自己（钉钉自己会话 + 微信），绝不发给原发送人
ONCE = os.environ.get("ONCE") == "1"              # 单次轮询后退出（用于自测，不常驻）
TABLE_GROUNDING = os.environ.get("TABLE_GROUNDING", "1") != "0"  # 默认开启：回复前按意图预拉多维表做事实 grounding

# gbrain 知识库（MCP HTTP 服务）开关与配置，风格对齐 TABLE_GROUNDING。
# 取代「工作空间内 产品资料/项目文件/.workbuddy/memory 文档」的旧知识注入方式：
# 回复 agent 经 mcp_servers 直连 gbrain HTTP 端点，调用 search/query 做语义检索（更快更准）。
# 默认开启；GBRAIN_GROUNDING=0 关闭（退回纯人设代复，不依赖 gbrain）。
# 端点/Token 缺省时从 WorkBuddy 的 mcp.json(gbrain) 自动读取，单一真源、避免 token 在源码/多处重复配置。
GBRAIN_GROUNDING = os.environ.get("GBRAIN_GROUNDING", "1") != "0"
_GB_URL = os.environ.get("GBRAIN_MCP_URL", "")
_GB_TOKEN = os.environ.get("GBRAIN_MCP_TOKEN", "")
if not _GB_URL or not _GB_TOKEN:
    try:
        _mp = os.path.join(os.path.expanduser("~"), ".workbuddy", "mcp.json")
        if os.path.exists(_mp):
            with open(_mp, encoding="utf-8") as _f:
                _mpd = json.load(_f)
            _ge = _mpd.get("mcpServers", {}).get("gbrain", {})
            if not _GB_URL and _ge.get("url"):
                _GB_URL = _ge["url"]
            if not _GB_TOKEN:
                _ga = _ge.get("headers", {}).get("Authorization", "")
                if _ga.startswith("Bearer "):
                    _GB_TOKEN = _ga[len("Bearer "):]
    except Exception:
        pass
GBRAIN_MCP_URL = _GB_URL
GBRAIN_MCP_TOKEN = _GB_TOKEN

# 本地代码库检索路径（可选能力，通用配置，不绑定任何特定项目/型号）。
# 分号(;)分隔的绝对路径列表；配置后，回复 agent 可检索这些源码库，
# 回答「源码 / 接口 / 实现细节」类问题（话题名、节点名、参数名、launch/配置文件、
# 具体 .py/.cpp 实现逻辑等），与 gbrain 文档知识互补（gbrain 查文档、代码库查实现）。
# 通用 skill 设计：源码零硬编码真实路径，由部署者在 .env 的 CODE_SEARCH_ROOTS 填写
# （Windows 用反斜杠或正斜杠均可）；未配置/路径不存在 → 不注入检索指令（防悬空）。
CODE_SEARCH_ROOTS_RAW = os.environ.get("CODE_SEARCH_ROOTS", "")

# 代码检索工具 search.py（可选，rg 全文搜索 + ctags 符号定位的封装脚本）。
# 优先用该工具检索（比裸 Grep 全库扫更快更准，还支持 --pkg 限定包、--symbol 定位符号定义）；
# 未配置/不存在时自动回退「Grep/Glob/Read 直接搜」。默认自动探测本机安装位置，可经
# CODE_SEARCH_TOOL 环境变量覆盖（装到其它路径/机器时配置）。
CODE_SEARCH_TOOL_RAW = os.environ.get(
    "CODE_SEARCH_TOOL",
    os.path.join(os.path.expanduser("~"), ".workbuddy", "tools", "code-search", "search.py"))


# 私有化 few-shot 示例文件（可选，去项目化后本机专属真实案例，不随包分发）：
# 通用 skill 的 few-shot 已去项目化（中性占位），真实项目案例放此私有文件（默认 skill 目录下
# dws-reply-examples.private.md，已 gitignore）。reply.py 运行时读它追加注入；
# 不配置/文件不存在则只用通用中性示例。可用环境变量 FEW_SHOT_PRIVATE_FILE 覆盖。
FEW_SHOT_PRIVATE_FILE = os.environ.get(
    "FEW_SHOT_PRIVATE_FILE",
    os.path.join(_SKILL_DIR, "dws-reply-examples.private.md"))


def code_search_roots():
    """返回【实际存在】的代码检索根路径列表（过滤不存在的，防悬空指令）。

    与 build_knowledge_instruction 同思路：prompt 指令与实际可用性严格一致——
    路径存在才写进 system_prompt 让 agent 去检，不存在/未配置则整段不注入。
    """
    _roots = []
    for _r in CODE_SEARCH_ROOTS_RAW.split(";"):
        _r = _r.strip()
        if _r and os.path.isdir(_r):
            _roots.append(_r)
    return _roots


def code_search_tool():
    """返回【实际存在】的 search.py 检索工具路径；未安装返回 None（回退 Grep/Glob 直接搜）。"""
    _t = (CODE_SEARCH_TOOL_RAW or "").strip()
    if _t and os.path.isfile(_t):
        return _t
    return None


# CodeBuddy Agent SDK 生成回复超时（秒）。
# 常规调用 240s 足够；但 agent 首次被 --agent 加载时，codebuddy 有一次性的冷启动注册延迟
# （实测 7~26 分钟），硬编码 240s 会让「注册后首条真实消息」在 240s 超时 -> 静默转人工、不代发。
# 故首次调用（进程内尚未成功生成过一次）放宽到 AGENT_FIRST_CALL_TIMEOUT，成功一次后切回常规超时。
AGENT_CALL_TIMEOUT = int(os.environ.get("AGENT_CALL_TIMEOUT", "240"))
AGENT_FIRST_CALL_TIMEOUT = int(os.environ.get("AGENT_FIRST_CALL_TIMEOUT", "1800"))

# 代复 / 看图等自动路径中，agent 被禁止调用的危险工具（黑名单模式）。
# 默认只禁：Write/Edit（防 agent 误写/篡改本地文件——这是唯一真正高危、可能造成破坏的操作）。
# WebSearch/WebFetch/Read/Grep/Glob/Bash 默认放开：agent 可查 gbrain(MCP) 也可按需读本地/联网，
# 但 system_prompt 仍以软约束要求「事实优先查 gbrain、内部资料不丢公网」——硬禁只保留 Write/Edit 这一道。
# gbrain 与 dws 均为 MCP 工具（mcp__gbrain__* / mcp__dws__*），不受此禁影响。
# 可用环境变量 DINGTALK_AGENT_DISALLOWED_TOOLS 覆盖（逗号分隔，如 "Write,Edit,Bash"）。
_DISALLOWED_RAW = os.environ.get("DINGTALK_AGENT_DISALLOWED_TOOLS")
if _DISALLOWED_RAW:
    DISALLOWED_TOOLS = [t.strip() for t in _DISALLOWED_RAW.split(",") if t.strip()]
else:
    DISALLOWED_TOOLS = ["Write", "Edit"]


# ---------- 运行期健壮性辅助（日志轮转 / 单实例锁 / 缓存清理） ----------
def _maybe_rotate(path, max_bytes):
    """日志文件超过上限则重命名为 .1（覆盖旧备份），避免常驻进程无限撑爆磁盘。"""
    try:
        if os.path.exists(path) and os.path.getsize(path) > max_bytes:
            bak = path + ".1"
            try:
                if os.path.exists(bak):
                    os.remove(bak)
            except OSError:
                pass
            os.rename(path, bak)
    except Exception:
        pass


def _clean_legacy_lock_file():
    """兼容清理：旧 PID 文件锁若残留则删除（已被端口锁取代，仅清理历史残留）。"""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except OSError:
        pass


def _acquire_lock():
    """单实例锁：用固定本地端口绑定（最稳，彻底绕开 Windows 进程树/PID/OpenProcess 全部坑）。
    第一个实例 bind 127.0.0.1:LOCK_PORT 成功并持有该 socket（直到进程退出）；
    其余实例 bind 同端口必 OSError(WSAEADDRINUSE) → 返回 False 退出。
    优于文件 PID 锁：不受「父壳 spawn worker 后退出导致锁指向死 PID」
    「OpenProcess 跨进程权限差异」等 Windows 怪象影响——端口由真正常驻的进程持有。
    返回 True=拿到锁；False=已有其它实例在跑（本进程应退出）。"""
    global _LOCK_SOCK
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 不设 SO_REUSEADDR：Windows 上 REUSEADDR=1 会允许「多个进程同时
        # bind 同一端口」而互不报错（与 Linux 相反）→ 双开！默认(0)下
        # 端口被占用时第二个 bind 必 WSAEADDRINUSE 失败 → 拦住，确保单实例。
        s.bind(("127.0.0.1", LOCK_PORT))
        s.listen(1)
        _LOCK_SOCK = s
        _clean_legacy_lock_file()
        return True
    except OSError:
        return False
    except Exception as _e:
        log_debug(f"[_acquire_lock] exception={_e}, 保守退出(return False)避免双实例")
        return False   # 锁异常时保守退出：双推/双回比不跑危害大，交由看门狗拉起


def _release_lock():
    """释放单实例锁：关闭持有的端口 socket（端口随即释放，供看门狗拉起新实例）。"""
    global _LOCK_SOCK
    try:
        if _LOCK_SOCK is not None:
            _LOCK_SOCK.close()
            _LOCK_SOCK = None
    except Exception:
        pass
    _clean_legacy_lock_file()


def _clean_media_cache(max_age_days=7):
    """定期清理图片下载缓存（默认保留 7 天），防止常驻进程下缓存无限增长。"""
    try:
        if not os.path.isdir(MEDIA_CACHE_DIR):
            return
        cutoff = time.time() - max_age_days * 86400
        for fn in os.listdir(MEDIA_CACHE_DIR):
            try:
                fp = os.path.join(MEDIA_CACHE_DIR, fn)
                if os.path.isfile(fp) and os.path.getmtime(fp) < cutoff:
                    os.remove(fp)
            except OSError:
                pass
    except Exception:
        pass


_RECENT_CACHE = {}   # cid -> (expiry_ts, msgs)：活跃检测用的「最近消息」短时缓存，避免窗口内重复拉 dws
# 群聊微信推送策略（仅影响群消息是否推微信；单聊代复+提醒不受影响）：
#   atme = 仅 @我 / @all 才推（默认，最清净）
#   all  = 所有群消息都推（旧行为）
#   off  = 群聊完全不推微信
GROUP_PUSH = os.environ.get("GROUP_PUSH", "atme").lower()

# 群聊 AI 草稿预览（可选能力，2026-08-05 新增，默认关）：
# 开启后，群聊 @我 且【有文本】的消息复用单聊机制（2min 延迟窗口 + 背景历史 + AI 生成回复），
# 但生成结果【绝不直接发到钉钉群】——只推微信给老板预览验证（红线：不在群聊替老板发言）。
# 老板确认草稿后如需代发，另行人工/指令处理。验证期用；GROUP_REPLY_PREVIEW=1 开启。
GROUP_REPLY_PREVIEW = os.environ.get("GROUP_REPLY_PREVIEW", "0") == "1"

def _split_set(env_name, default):
    """从环境变量（逗号分隔）读取集合；未设置则用默认值。
    用于 SKIP_SENDERS / SELF_SENDERS 的可配置化（不必硬编码改源码）。"""
    raw = os.environ.get(env_name)
    if raw and raw.strip():
        return set(x.strip().lower() for x in raw.split(",") if x.strip())
    return set(x.lower() for x in default)

# 不自动回复的名单（昵称包含其一即只通知不代发）；可用环境变量 SKIP_SENDERS="家人甲,某总" 配置
SKIP_SENDERS = _split_set("SKIP_SENDERS", [])
# 老板本人的昵称/关键字：最新消息若来自老板自己，不代复（避免"回复自己"的社死）
# 主判据用 openid 精确匹配（启动时缓存 SELF_OPEN_ID），昵称仅作 openid 拿不到时的兜底
# 隐私：源码不硬编码真实昵称，请在私密 .env 里配 SELF_SENDERS="你的昵称,你的英文名"
SELF_SENDERS = _split_set("SELF_SENDERS", ["老板"])
# 老板本人的 openDingTalkId（运行时由 get_self_openid() 填充，经 runtime.SELF_OPEN_ID 访问，
# 避免 import 副本导致 _is_self 看不到启动期探测结果）。
SELF_OPEN_ID = ""
# 仅用于自测脚本 _validate.py 验证 reply 命令形态时的 --text 占位符；
# 主流程（main）在生成失败/媒体无文本时绝不直接代发此兜底话术，而是转人工通知。
FALLBACK_REPLY = "收到，稍后回你。"
NOTIFIED = {}  # cid -> 已处理的 最新消息 openMessageId/lastMsgCreateAt
# 抢答防护：延迟窗口 + 老板活跃检测
REPLY_DELAY_SEC = int(os.environ.get("REPLY_DELAY_SEC", "120"))
ACTIVE_WINDOW_SEC = int(os.environ.get("ACTIVE_WINDOW_SEC", "300"))
PENDING = {}  # cid -> {deadline, ts, sender, msg_id, sender_open_id, content}
GNOTIFY = {}  # cid -> {deadline, ts, title, sender, body, img_desc, at_me, msgs:[...], defers}
            # 群聊延迟通知窗口（类单聊 PENDING）：到期才推微信，期间老板在群活跃则取消、多条@合并
LAST_SELF_SENT = {}  # cid -> 程序成功代复时的 epoch 时间戳（用于活跃检测排除自身消息，防自锁死）

AUDIT_LOG = os.path.expanduser("~/.workbuddy/dingtalk_auto_audit.jsonl")  # 审计：代发了什么给谁
AUDIT_LOG_MAX = 512 * 1024            # 审计日志上限 512KB，超出轮转


# ---------- 图片识别（多模态）配置 ----------
# 后端：与文本回复同一套 CodeBuddy Agent SDK（deepseek-v4-flash 支持视觉，可看图识别），
# 零额外 key、图片不出域。视觉模型默认跟随文本主模型 CODEBUDDY_MODEL，无需单独配置；
# 如有特殊需要仍可用 VISION_MODEL 单独指定 CodeBuddy 侧视觉模型。
# 视觉能力与文本一致，统一由 SDK 可用性决定。
VISION_MODEL = os.environ.get("VISION_MODEL", CODEBUDDY_MODEL)
# 「视觉能力」= SDK 可用即可（与文本生成同构），默认开箱即用识别，无需任何 key。
VISION_ENABLED = _SDK_AVAILABLE
MEDIA_CACHE_DIR = os.path.join(_SKILL_DIR, "_media_cache")  # 运行时生成的图片下载缓存目录
# 单聊图片是否 AI 自动代复（基于"文字说明+图片识别描述"生成回复）。
# 默认开：老板要求「图片也默认代复」，故改为「除非显式设 0 才关」。
#   .env 设 AUTO_REPLY_IMAGE=0 可降级为「仅识别+微信通知，不代发」(防社死)。
# 依赖 SDK 视觉（VISION_ENABLED=SDK 可用）；未配视觉时自动降级为仅通知。
AUTO_REPLY_IMAGE = os.environ.get("AUTO_REPLY_IMAGE") != "0"


# ---------- 群聊 @我 检测（共享正则） ----------
# dws 单条消息对象无结构化 atUsers 字段，@ 只体现在内容纯文本 '@昵称'。
# 判据见 dingtalk_api.group_msg_is_at_me（2026-08-05 改为任意位置子串匹配，兼容 @@ 双@/句中@）。
# 这是基于展示名的启发式（零额外 API 调用、廉价可靠）；若老板群昵称特殊，用 MENTION_NAMES 覆盖。
# 隐私：源码不硬编码真实昵称，请在私密 .env 里配 MENTION_NAMES="你的群昵称"（逗号分隔）。
MENTION_NAMES = set(x.strip() for x in os.environ.get("MENTION_NAMES", "老板").split(",") if x.strip())

# 钉钉富媒体（图片/语音/视频/文件）辅助正则：
# 钉钉把媒体内联进 content 文本：'[图片消息](mediaId=@lQLPJwBX...)' / '[语音消息](mediaId=@lR_P...)'，
# 纯文本/媒体混合消息都能命中；可能一条消息含多张图。
# 注意：mediaId 前缀不固定——有的以 '@' 开头，有的以 '$' 开头（如 '$iwEcAq...'），
# 还可能含 '-'。旧正则 [@\w\-_]+ 不认 '$' 会漏掉整条 → 图片提取为空 → 降级仅通知。
# 改为匹配到右括号/空白前的所有非空白字符，兼容任意前缀。
_MEDIA_RE = re.compile(r'mediaId=([^)\s]+)')
# ⚠️ 2026-08-07 新增：视频/语音/文件标签整段剔除（extract_media_ids 用它先剥掉非图片标签，
# 防止视频 mediaId 被当图片下载内联 → SDK 400 mime）。注意不含"图片"，图片标签保留给 _MEDIA_RE 提取。
_NON_IMAGE_TAG_RE = re.compile(r'\[[^\]]*(?:视频|语音|文件|音频)[^\]]*\]\(mediaId=[^)\s]+\)?')
# ⚠️ 2026-08-07 修复（400 mime 根因，老板纠偏）：旧正则只匹配「图片」标签且要求右括号闭合——
# ①'$' 开头的 mediaId 消息 dws 返回常【不闭合括号】→ 整段残留进背景历史；
# ②'[语音消息]/[视频消息]/[文件消息]' 等标签完全不匹配 → 残留。
# 残留的 mediaId=... 文本混进 user_msg 背景历史 → SDK 把 mediaId 当媒体 mime 解析 → 400。
# 修复：匹配【任意媒体标签】+ 右括号【可选】；纯媒体无文字说明则清空整段。
_PIC_TAG_RE = re.compile(r'\[[^\]]*\]\(mediaId=[^)\s]+\)?')
# ⚠️ 2026-08-07 补充（视频空括号标记）：dws 对视频/语音消息除 mediaId 格式外，还有
# 【空括号占位】格式 '[视频]()'（温兆龙 08-07 案例：'…辛苦看下[图片消息](mediaId=@lQD…)[视频]()'
# ——图片 mediaId 被 _PIC_TAG_RE 清掉后，'[视频]()' 残留进 main_content 喂给 AI 造成噪音）。
# 覆盖所有媒体类型空括号占位：视频/语音/文件/图片 及带"消息"后缀的变体；无括号内容才算占位。
_MEDIA_EMPTY_RE = re.compile(r'\[[^\]]*(?:视频|语音|文件|图片)[^\]]*\]\(\)')
# dws 在缺 chat/list_conversation_message_v2 权限时，会在消息文本里注入下载提示语
# （如「注意：如需下载使用dws chat message download-media命令下载…」）。这不是老板
# 该操心的内容，且会污染喂给 AI 的上下文、误导质检，统一在此剥离。
_DWS_HINT_RE = re.compile(r'注意[：:][^\n]*?download-media[^\n]*', re.IGNORECASE)
_DWS_HINT_RE2 = re.compile(r'dws chat message download-media[^\n]*', re.IGNORECASE)


# ---------- 鉴权 / 日志 / 状态 ----------
def log_audit(action, **kw):
    """审计日志（每行一个 JSON）：记录代发/跳过的时间、会话、发件人、内容、结果。
    以本人身份发消息是高风险对外操作，必须可追溯。"""
    try:
        _maybe_rotate(AUDIT_LOG, AUDIT_LOG_MAX)
        entry = {"time": datetime.datetime.now().isoformat(), "action": action, **kw}
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _free_port():
    """codebuddy CLI 启动会起 prewarm 本地 server 占 SERVER__PORT；
    若该端口与 WorkBuddy 自身实例撞车会 EADDRINUSE 挂起（表现为永远 0 字节/超时）。
    每次生成分配一个空闲端口避开冲突。"""
    try:
        s = socket.socket()
        s.bind(("", 0))
        p = s.getsockname()[1]
        s.close()
        return p
    except Exception:
        return 18732


# ---------- 共享：SDK 调用 / 图片视觉（reply.py 与 vision.py 共用，消除重复） ----------
def encode_image_b64(path):
    """读取图片文件为 base64 ascii 串（供 CodeBuddy Agent SDK 的 image 协议内联）。"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def _vision_media_type(path):
    """根据文件扩展名 + 魔数嗅探推断图片 media_type（SDK image 协议用）。

    ⚠️ 2026-08-13 修复：download_images 统一落盘 .jpg，但真实字节可能是 PNG/GIF/WEBP，
    仅按扩展名会误判 mime（SDK 多模态解码失败/偏差）。扩展名为 jpg/jpeg 时再嗅探文件头
    魔数修正真实格式；其它扩展名信任其声明（避免额外 IO）。
    """
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    _by_ext = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
               "gif": "image/gif", "webp": "image/webp"}.get(ext, "image/jpeg")
    if ext in ("jpg", "jpeg"):
        try:
            with open(path, "rb") as f:
                head = f.read(12)
            if head.startswith(b"\x89PNG\r\n\x1a\n"):
                return "image/png"
            if head[:6] in (b"GIF87a", b"GIF89a"):
                return "image/gif"
            if head.startswith(b"RIFF") and head[8:12] == b"WEBP":
                return "image/webp"
            if head.startswith(b"\xff\xd8\xff"):
                return "image/jpeg"
        except Exception:
            pass
    return _by_ext


def build_image_block(path):
    """构造 SDK image 协议块（base64 内联 + 正确 media_type）。reply/vision 共用。"""
    return {"type": "image",
            "source": {"type": "base64",
                       "media_type": _vision_media_type(path),
                       "data": encode_image_b64(path)}}


def build_sdk_env():
    """构造 CodeBuddy Agent SDK 调用所需环境变量：
    每次生成分配空闲端口避开 SERVER__PORT 冲突（否则 query() 0 字节超时）；
    中国版自动注入 CODEBUDDY_INTERNET_ENVIRONMENT；有 API Key 则注入。
    ⚠️ 2026-08-03 老板要求（agent 可自己调 dws 查同事记录）：把 dws/node 可执行目录
    注入 PATH——SDK 子进程的 Bash 是独立环境，若不注入，agent 敲 `dws contact user
    search` 会因 vendor 目录不在 PATH 而失败，只能凭印象答（实测复现：查不到→回"还没对接"）。"""
    env = {
        "SERVER__PORT": str(_free_port()),
        "CODEBUDDY_INTERNET_ENVIRONMENT": os.environ.get(
            "CODEBUDDY_INTERNET_ENVIRONMENT", "internal" if CHINA_EDITION else "public"),
    }
    if CODEBUDDY_API_KEY:
        env["CODEBUDDY_API_KEY"] = CODEBUDDY_API_KEY
    # 追加 dws(node_modules/vendor)、dws.cmd、node 所在目录到 PATH，保证 agent Bash 能直接敲 dws
    _extra_dirs = []
    for _p in (DWS_EXE, DWS_ENTRY, NODE, DWS_CMD):
        if _p and os.path.exists(_p):
            _d = os.path.dirname(os.path.abspath(_p))
            if _d not in _extra_dirs:
                _extra_dirs.append(_d)
    if _extra_dirs:
        env["PATH"] = os.pathsep.join(_extra_dirs + [os.environ.get("PATH", "")])
    return env


# 视觉识别 prompt（deepseek-v4-flash 内置视觉 / 外部 OpenAI 兼容 API 共用同一描述指令）。
VISION_PROMPT = ("请用简体中文简明描述这张图片的关键信息"
                 "（如图表数据、文字内容、界面截图、物体等），不超过150字。")


def _cli_credentials_present():
    """软检测 CodeBuddy CLI 是否已登录：~/.codebuddy/local_storage 下存在含
    token/bearer/secret 凭据词的 entry 文件（已在本机确认存在多个 entry_*.info 含此类词）。
    这是 Electron IndexedDB 私有格式，不强依赖精确字段名——只做『凭据文件存在』的粗判，
    真正的硬保证是运行时 SDK query 本身（未登录会抛鉴权错误，被 gen_reply 捕获转不代发）。"""
    _keys = ("token", "bearer", "secret", "credential", "auth")
    return _scan_local_storage(lambda txt: any(k in txt.lower() for k in _keys))


def check_codebuddy_auth():
    """启动期 CodeBuddy 认证健康检查。返回 (mode, detail) 或 None（未认证）。
    mode: 'apikey' = 用了 CODEBUDDY_API_KEY；'cli' = 复用 CLI 已登录凭据。
    两个都没有 → 返回 None，调用方应打印醒目提示并退出（让老板去登录或填 Key）。"""
    if CODEBUDDY_API_KEY:
        return ("apikey", "使用 CODEBUDDY_API_KEY 环境变量认证")
    if _cli_credentials_present():
        return ("cli", "复用 CodeBuddy CLI 已登录凭据（~/.codebuddy）")
    return None


def print_auth_banner():
    """未认证时的醒目提示（老板自己完成登录，绝不在脚本里代填凭据）。"""
    bar = "=" * 60
    msg = (
        f"\n{bar}\n"
        f"⚠️  CodeBuddy 未认证 —— 钉钉自动回复无法生成\n"
        f"{bar}\n"
        f"本脚本用 CodeBuddy Agent SDK 生成回复，需要先认证。请二选一：\n"
        f"\n"
        f"【方式一 · 终端登录（推荐，零配置）】\n"
        f"  打开系统终端，运行：\n"
        f"      codebuddy\n"
        f"  按提示完成设备码 / OAuth 登录（会打开浏览器或给验证码），\n"
        f"  登录成功后重新启动本脚本即可。\n"
        f"\n"
        f"【方式二 · API Key（适合无人值守常驻）】\n"
        f"  1) 去 CodeBuddy 控制台申请 API Key（https://copilot.tencent.com ）\n"
        f"  2) 在技能目录的 .env 里填：  CODEBUDDY_API_KEY=你的key\n"
        f"     （cp .env.example .env 后编辑）\n"
        f"  3) 重启本脚本。\n"
        f"{bar}\n"
    )
    sys.stderr.write(msg)
    try:
        log_debug("[auth] CodeBuddy 未认证，已提示老板登录/填 Key")
    except Exception:
        pass


def log_debug(msg):
    try:
        _maybe_rotate(DEBUG_LOG, DEBUG_LOG_MAX)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass
