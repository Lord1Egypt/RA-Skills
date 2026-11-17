#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find-skills++ 自带的技能安全静态扫描器（零依赖，仅用标准库）。

用途：在下载/安装一个社区技能（zip 解压后）之前或之后，对 SKILL.md 及其
附带的 scripts/ references/ assets/ 做一次静态审查，输出风险信号与人工审阅清单。

设计参考：sandbaseai/workbuddy-skill 的"真实脚本化审查"思路（已注明派生与参考，
本脚本为独立自研、纯标准库实现）。源头：vercel-labs/skills 的 find-skills。

误报控制（重要）：
- 按代码围栏（```bash/sh/powershell/python...）区分「可执行块」与「文档正文」。
  正文里的危险词只算「提及」，降一级，避免把"描述攻击模式"误判为"实施攻击"。
- `rm -rf` 只在目标是 / 、~ 、系统盘、上级目录时才判 P0；临时目录清理不算。
- 扫描器自身文件（security_scan.py）不参与命中，避免自引用噪声。

用法：
    python3 security_scan.py --path <技能目录或SKILL.md路径>
    python3 security_scan.py --path <目录> --json
    python3 security_scan.py --path <目录> --lang zh-CN

退出码：0 = 安全(P2) / 1 = 需确认(P1) / 2 = 高危阻断(P0) / 3 = 路径错误
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shlex
import sys
from pathlib import Path

# 允许清单内的可信主机（社区源下载的技能若外呼这些，不算风险）
TRUSTED_HOSTS = (
    "lightmake.site", "skillhub.cn", "clawhub.com", "skills.sh",
    "github.com", "raw.githubusercontent.com", "npmjs.com",
    "vercel.com", "objects.githubusercontent.com",
)

FRONTMATTER_FIELDS = (
    "name", "description", "description_zh", "description_en",
    "version", "author", "license", "allowed-tools", "compatibility",
)

# 可执行语境的代码围栏语言
LIVE_FENCE = {"bash", "sh", "shell", "zsh", "ps1", "powershell", "cmd", "bat",
              "python", "py", "js", "ts", "node", "javascript", "typescript"}

# 静态风险信号：每条是 (标签, 正则, 定级, 仅可执行块才算高危)
# dangerous_target：rm -rf 只有在目标是系统/家/上级目录时才高危
SIGNALS = [
    ("混淆执行:eval/exec", r"\beval\s*\(|\beval\s+[`\"]|exec\s*\(", "P0"),
    ("混淆执行:base64解码", r"base64\s+(-d|--decode)|FromBase64String|base64\.b64decode", "P0"),
    ("混淆执行:powershell编码", r"powershell\s+(-enc|-EncodedCommand)", "P0"),
    ("远程执行:管道到sh", r"(curl|wget)\s+[^|]*\|\s*(sudo\s+)?(ba)?sh|curl[^|]*\|\s*sh", "P0"),
    ("破坏系统:rm -rf 高危目标", r"\brm\s+-rf\s+[\"']?\s*(/|~|\.\./|%USERPROFILE%|%SYSTEMDRIVE%|/etc|/usr|/System)", "P0"),
    ("破坏系统:提权/格式化", r"\bsudo\b|\bmkfs\b|:\(\)\s*\{.*\}&", "P0"),
    ("可疑外呼:未知域名", r"https?://(?![\w.-]*(?:" + "|".join(TRUSTED_HOSTS) + r"))[\w.-]+\.[a-z]{2,}", "P1"),
    ("凭据索取:token/secret", r"\b(token|secret|api[_-]?key|password|passwd|授权码|access[_-]?key)\b", "P1"),
    ("提示注入:忽略指令", r"ignore\s+(previous|all|above)\s+(instructions|prompt)|忽略(此前|以上|之前)的?指令", "P1"),
    # --- 对标 skill-vetter（31 万下载，同类头部）补齐的红旗项 ---
    ("凭据目录读取:ssh/aws/config", r"(~|\$HOME|%USERPROFILE%)?[\\/.]\s*(ssh|aws)\b|aws[\\/]credentials|id_rsa|id_ed25519|\.npmrc\b|\.netrc\b|\.docker[\\/]config|\.gnupg\b", "P0"),
    ("Agent身份/记忆文件访问", r"\b(MEMORY|USER|SOUL|IDENTITY|CLAUDE|AGENTS)\.md\b", "P0"),
    ("网络:裸IP直连", r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "P1"),
    ("浏览器凭据:cookie/session", r"cookies\.sqlite|--user-data-dir|Login\s*Data|document\.cookie|browser\s+cookie", "P0"),
    ("静默安装依赖包", r"\b(pip3?|npm|pnpm|yarn|apt-get|apt|brew|winget|choco)\s+install\b", "P1"),
    ("混淆代码:转义/压缩", r"(\\x[0-9a-fA-F]{2}){6,}|(\\u[0-9a-fA-F]{4}){6,}|String\.fromCharCode|charCodeAt\s*\(", "P0"),
    ("系统目录写入", r"(?:>\s*|tee\s+|mv\s+|cp\s+)[^|\n]*?\s+(/etc/|/usr/|/System/|C:\\?\\?Windows)", "P0"),
    ("权限放宽:chmod 777", r"chmod\s+(-R\s+)?(777|a\+rwx)", "P1"),
]

RANK = {"P0": 2, "P1": 1, "P2": 0}

# 四级风险分类（对标 skill-vetter 的 LOW/MEDIUM/HIGH/EXTREME + 动作映射）。
# 关键：区分「执行块里的真实高危」与「文档正文里的提及」——后者多为误报。
RISK_CLASS = {
    "EXTREME": ("⛔ 禁止安装", "Do NOT install"),
    "HIGH": ("🔴 需人工批准", "Human approval required"),
    "MEDIUM": ("🟡 完整审查后安装", "Full code review required"),
    "LOW": ("🟢 可安装", "Install OK"),
}


def classify_risk(hits):
    """把 P0/P1/P2 命中按「执行块 vs 文档提及」语境归并为四级风险。

    EXTREME = 执行块里出现 P0（真实高危，禁止安装）
    HIGH    = 文档提及 P0（多为示范）或执行块里出现 P1（需人工确认）
    MEDIUM  = 仅文档提及 P1
    LOW     = 无命中
    """
    def has(level, ctx_keyword):
        return any(h.get("level") == level and ctx_keyword in (h.get("context") or "")
                   for h in hits)
    exec_ = ("执行块", "AST", "shell")
    doc_ = ("文档提及",)
    if any(has("P0", k) for k in exec_):
        return "EXTREME"
    if any(has("P0", k) for k in doc_) or any(has("P1", k) for k in exec_):
        return "HIGH"
    if any(has("P1", k) for k in doc_):
        return "MEDIUM"
    return "LOW"


# 权限清单提取：回答 skill-vetter Step 3 的三个问题
# ——需要读哪些文件 / 访问哪些网络 / 执行哪些命令
_URL_RE = re.compile(r"https?://([\w.-]+)(?:[:/][^\s\"'`)\]>]*)?")
_PATH_RE = re.compile(
    r"(?:~|\$HOME|%USERPROFILE%)[\\/][\w.\\/-]{2,60}"
    r"|\.(?:ssh|aws|gnupg|docker|config|npmrc|netrc|env)\b[\w.\\/-]*"
    r"|(?:/etc|/usr|/var|/System|C:\\Windows)[\\/][\w.\\/-]{0,60}"
    r"|\b(?:MEMORY|USER|SOUL|IDENTITY|CLAUDE|AGENTS)\.md\b"
)
_CMD_NAMES = {
    "curl", "wget", "pip", "pip3", "npm", "pnpm", "yarn", "apt-get", "apt",
    "brew", "winget", "choco", "sudo", "rm", "mv", "cp", "chmod", "chown",
    "git", "ssh", "scp", "docker", "kubectl", "python", "python3", "node",
    "bash", "sh", "powershell", "iex",
}
# 行内命令分隔符：管道 / && / ; / $(...)
_SPLIT_RE = re.compile(r"[|;&]+|\$\(")
# 段首命令（允许 sudo 前缀），用于识别 `sudo chmod ...` 这类非行首命令
_LEAD_CMD_RE = re.compile(r"^(?:sudo\s+)?([A-Za-z_][\w.-]*)\b")


def _cmd_tokens_from(text):
    """按行提取命令名：取段首词（允许 sudo 前缀），并沿管道/&&/;/$( 拆分继续取。"""
    cmds = set()
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        for part in _SPLIT_RE.split(s):
            part = part.strip()
            # sudo 既是前缀也是命令本身，需单独计入
            if part.lower().startswith("sudo"):
                cmds.add("sudo")
            m = _LEAD_CMD_RE.match(part)
            if m and m.group(1).lower() in _CMD_NAMES:
                cmds.add(m.group(1).lower())
    return cmds


def _exec_segments(name, txt):
    """返回该文件中『可执行语境』的文本片段列表。

    .sh/.ps1/.bat/.py 整文件即为执行语境；.md 等按代码围栏取可执行块。
    """
    if name.endswith((".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".py")):
        return [txt]
    return [seg for seg, live in iter_segments(txt) if live]


def extract_permissions(texts):
    """从技能全文本中提取权限清单（网络/文件/命令），用于人工审阅。"""
    net, files, cmds = set(), set(), set()
    for name, txt in texts.items():
        for m in _URL_RE.finditer(txt):
            net.add(m.group(1))
        for m in _PATH_RE.finditer(txt):
            p = m.group(0).strip()
            if len(p) >= 3:
                files.add(p)
        for seg in _exec_segments(name, txt):
            cmds |= _cmd_tokens_from(seg)
    return {
        "network": sorted(net)[:25],
        "files": sorted(files)[:30],
        "commands": sorted(cmds)[:25],
    }


# ---------------------------------------------------------------------------
# AST 级静态分析（仅 .py 文件）：语法树级检测混淆/动态危险调用，
# 弥补纯正则无法识别的 `cmd="rm"+" -rf"+p`、base64 解码后 exec、
# os.system()、subprocess(shell=True)、__import__ 远程模块 等。
# 纯标准库 ast，零依赖；与正则分诊互补，正则无法覆盖的混淆调用由它兜底。
# ---------------------------------------------------------------------------
_AST_DANGER = {
    "eval": "P0",
    "exec": "P0",
    "compile": "P1",
    "pickle.loads": "P0",
    "marshal.loads": "P0",
    "os.system": "P0",
    "os.popen": "P0",
    "os.execv": "P0",
    "os.execve": "P0",
    "subprocess.call": "P1",
    "subprocess.run": "P1",
    "subprocess.Popen": "P1",
    "__import__": "P1",
    "ctypes.CDLL": "P1",
    "ctypes.windll": "P1",
    "builtins.eval": "P0",
    "builtins.exec": "P0",
}


def _ast_call_key(node):
    """返回调用目标的字符串标识，如 'os.system' / 'eval' / 'subprocess.run'。"""
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        parts = []
        cur = f
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
        return ".".join(reversed(parts))
    return None


def _is_shell_true(node):
    """subprocess 调用是否传了 shell=True。"""
    for kw in node.keywords:
        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
            return True
    return False


def _is_dynamic(node):
    """命令参数是否来自字符串拼接/格式化（f-string、+ 拼接、base64 解码）。"""
    if isinstance(node, (ast.BinOp, ast.JoinedStr)):
        return True
    if isinstance(node, ast.Call):
        k = _ast_call_key(node)
        if k and ("b64decode" in k or k in ("decode", "unhexlify")):
            return True
    return False


# 危险 sink：字符串若作为这些调用的参数，说明字符串被"真正使用"于
# 文件/命令/网络操作，而非只是文案或提示语。
SINK_FUNCS = {
    "open", "system", "popen", "run", "call", "check_output", "check_call",
    "Popen", "exec", "eval", "execv", "execl", "execve", "spawn",
    "remove", "rmtree", "unlink", "rmdir", "mkdir", "makedirs",
    "read_text", "write_text", "read_bytes", "write_bytes",
    "rename", "replace", "copy", "move", "chmod", "chown",
    "get", "post", "put", "request", "urlopen", "urlretrieve",
    "load", "loads", "startfile",
}


def _sink_string_lines(code: str):
    """返回「字符串常量被传入危险 sink 调用」的行号集合。

    用途：区分「真在偷读 ~/.ssh/id_rsa」与「文案里提到 ~/.ssh」——
    后者只是字符串字面量，不该判 P0。这是 AST 相对纯正则的核心优势。

    解析失败时返回 None（调用方按保守策略处理：整文件仍视为代码）。
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    lines = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        key = _ast_call_key(node)
        if not key:
            continue
        base = key.split(".")[-1]
        if base not in SINK_FUNCS:
            continue
        for arg in list(node.args) + [k.value for k in node.keywords]:
            if not isinstance(arg, ast.AST):
                continue
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    lines.add(getattr(sub, "lineno", 0))
    return lines


def scan_python_ast(code: str, relname: str):
    hits = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return hits
    seen = {"exec_eval": False, "b64": False}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        key = _ast_call_key(node)
        if not key:
            continue
        if key in ("exec", "eval"):
            seen["exec_eval"] = True
        if "b64decode" in key or key == "unhexlify":
            seen["b64"] = True
        level = _AST_DANGER.get(key)
        if level is None:
            continue
        if key.startswith("subprocess.") and _is_shell_true(node):
            level = "P0"
        dyn = bool(node.args) and _is_dynamic(node.args[0])
        extra = "（命令参数动态拼接，可能绕过字面量检测）" if dyn else ""
        hits.append({
            "file": relname,
            "signal": f"AST混淆调用:{key}{extra}",
            "level": level,
            "context": "执行块(AST)",
        })
    if seen["exec_eval"] and seen["b64"]:
        hits.append({
            "file": relname,
            "signal": "AST混淆组合:base64解码后exec/eval",
            "level": "P0",
            "context": "执行块(AST)",
        })
    return hits


def scan_shell_tokens(code: str, relname: str, language: str):
    """用 shlex 对 shell 脚本做词法级扫描，识别高危命令组合。"""
    hits = []
    posix = language != "ps1"
    for line in code.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        try:
            toks = shlex.split(s, comments=False, posix=posix)
        except ValueError:
            toks = s.split()
        if not toks:
            continue
        low = [t.lower() for t in toks]
        # rm -rf 高危目标
        if "rm" in low and any(o in low for o in ("-rf", "-fr", "--recursive", "-r")):
            idx = low.index("rm")
            target = " ".join(toks[idx + 1:])
            if re.search(r"(\.\./|/|~|%USERPROFILE%|%SYSTEMDRIVE%|/etc|/usr|/System|/home|\$HOME)",
                         target, re.I):
                hits.append({
                    "file": relname,
                    "signal": f"破坏系统:rm -rf 高危目标 [{target[:40]}]",
                    "level": "P0", "context": "执行块(shell)",
                })
        # 下载后管道到 shell（curl|sh / wget|sh / iwr|iex）
        downloader = any(d in low for d in ("curl", "wget", "iwr", "invoke-webrequest"))
        runner = any(r in low for r in ("sh", "bash", "powershell", "iex", "invoke-expression"))
        if downloader and runner and ("|" in line or "iex" in low or "invoke-expression" in low):
            hits.append({
                "file": relname,
                "signal": "远程执行:下载后管道到 shell",
                "level": "P0", "context": "执行块(shell)",
            })
        if "sudo" in low:
            hits.append({
                "file": relname, "signal": "提权:sudo", "level": "P1", "context": "执行块(shell)",
            })
        if any(t.startswith("mkfs") for t in low):
            hits.append({
                "file": relname, "signal": "破坏系统:格式化(mkfs)", "level": "P0", "context": "执行块(shell)",
            })
    return hits


def parse_frontmatter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return False, {}
    fields = {}
    stack = [(0, fields)]
    for raw in m.group(1).splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in raw:
            continue
        indent = len(raw) - len(raw.lstrip())
        k, _, v = raw.partition(":")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        # 弹栈回到正确的父级（缩进 <= 当前栈顶时，说明回到更上层）
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if v == "":
            node = parent.get(k)
            if not isinstance(node, dict):
                node = {}
                parent[k] = node
            stack.append((indent, node))
        else:
            parent[k] = v
    # 无子项的空字典还原为空字符串，保持对扁平标量的向后兼容
    def _clean(o):
        if isinstance(o, dict):
            if not o:
                return ""
            return {kk: _clean(vv) for kk, vv in o.items()}
        return o
    return True, _clean(fields)


def iter_segments(text: str):
    """把文本切成 (片段内容, 是否可执行语境)。无围栏的正文 is_live=False。"""
    fence = re.compile(r"^```(\w*)\s*$", re.M)
    pos = 0
    cur_live = False
    for m in fence.finditer(text):
        chunk = text[pos:m.start()]
        yield chunk, cur_live
        lang = (m.group(1) or "").lower()
        cur_live = lang in LIVE_FENCE
        pos = m.end()
    yield text[pos:], cur_live


def _inside_quote_or_comment(line: str, start: int) -> bool:
    """命中点是否位于引号内（被当作字符串参数）或注释行——视为'示范'而非'执行'。"""
    s = line.lstrip()
    if s.startswith("#") or s.startswith("REM ") or s.startswith("::") or s.startswith("//"):
        return True
    before = line[:start]
    if (before.count('"') % 2 == 1) or (before.count("'") % 2 == 1) or (before.count("`") % 2 == 1):
        return True
    return False


def scan_segment(text: str, is_live: bool, code_sink_lines=None,
                 no_downgrade: bool = False):
    """扫描一段文本，并按语境决定危险信号是否降级。

    is_live:         该段是否处于可执行语境。
    code_sink_lines: 对 .py 文件传入「字符串被危险 sink 使用的行号集合」
                     （见 _sink_string_lines）。命中行在集合内 ⇒ 字符串被
                     open/read/system 等真正使用 ⇒ 不降级；
                     否则只是文案/日志里的字面量 ⇒ 降级，避免误报。
                     传 None 表示非代码文件，走引号/注释判定。
    no_downgrade:    .py 语法解析失败时保守处理——一律不降级，宁可误报不漏判。
    """
    hits = []
    for label, pat, level in SIGNALS:
        for m in re.finditer(pat, text, re.I):
            eff = level
            context = "执行块" if is_live else "文档提及"
            if is_live:
                line_no = text.count("\n", 0, m.start()) + 1
                if no_downgrade:
                    real_use = True
                elif code_sink_lines is not None:
                    real_use = line_no in code_sink_lines
                else:
                    ls = text.rfind("\n", 0, m.start()) + 1
                    le = text.find("\n", m.start())
                    line = text[ls:le if le != -1 else None]
                    real_use = not _inside_quote_or_comment(line, m.start() - ls)
                if not real_use:
                    # 只是字面量/示范/文案：P0 降 P1，语境标为引用
                    eff = "P1" if level == "P0" else level
                    context = "文档提及(引用)"
            else:
                # 文档正文提及：P0 降级为 P1（多为示范/警示性写法）
                if level == "P0":
                    eff = "P1"
            hits.append((label, eff, context))
    return hits


def _is_test_path(relname: str) -> bool:
    """相对路径是否位于测试目录（如 tests/ 下的恶意样本夹具）。"""
    parts = relname.replace("\\", "/").split("/")
    return any(p in ("tests", "test", "fixtures", "__tests__") for p in parts[:-1])


def collect_texts(root: Path, exclude_tests: bool = False):
    root = root.resolve()
    if root.is_file():
        files = [root]
    else:
        files = list(root.rglob("*"))
    texts = {}
    for f in files:
        if f.is_file() and f.suffix.lower() in (".md", ".py", ".sh", ".ps1", ".js", ".ts", ".json", ".yaml", ".yml", ".bat"):
            # 排除扫描器自身，避免自引用噪声
            if f.name == "security_scan.py":
                continue
            rel = str(f.relative_to(root))
            # 测试夹具（本项目 tests/ 内含大量恶意样本）默认仍扫描——安全优先；
            # 仅自查时用 --exclude-tests 排除，否则会把自己判成 EXTREME。
            if exclude_tests and _is_test_path(rel):
                continue
            try:
                texts[rel] = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass
    return texts


def build_report(root: Path, exclude_tests: bool = False):
    texts = collect_texts(root, exclude_tests=exclude_tests)
    skill_md = next((t for n, t in texts.items() if n.endswith("SKILL.md")), "")
    valid, fields = parse_frontmatter(skill_md) if skill_md else (False, {})

    all_hits = []
    for name, txt in texts.items():
        if name.endswith(".py"):
            # AST 语法树级检测（.py 直接是执行块语境）
            all_hits.extend(scan_python_ast(txt, name))
            # 正则分诊同样要跑：AST 只认调用结构，抓不到
            # 字符串内的 \xNN / \uNNNN 转义混淆、裸 IP、凭据路径等字面量。
            # 用 AST 判定字符串是否被危险 sink 真正使用，避免把文案里的
            # "偷读 ~/.ssh" 之类字面量误判为真实窃取。
            sink = _sink_string_lines(txt)
            for label, eff, ctx in scan_segment(
                    txt, True,
                    code_sink_lines=sink,
                    no_downgrade=(sink is None)):
                all_hits.append({"file": name, "signal": label, "level": eff, "context": ctx})
        elif name.endswith((".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd")):
            lang = "ps1" if name.endswith(".ps1") else "sh"
            all_hits.extend(scan_shell_tokens(txt, name, lang))
        else:
            # .md 等：按代码围栏区分执行块/文档正文
            for seg, live in iter_segments(txt):
                for label, eff, ctx in scan_segment(seg, live):
                    all_hits.append({"file": name, "signal": label, "level": eff, "context": ctx})

    levels = [h["level"] for h in all_hits]
    top = "P2"
    for lv in ("P0", "P1"):
        if lv in levels:
            top = lv
            break

    has_license = bool(fields.get("license"))
    has_author = bool(fields.get("author"))
    missing_core = [f for f in ("name", "description") if not fields.get(f)]

    risk_class = classify_risk(all_hits)

    return {
        "target": str(root),
        "frontmatter": {"valid": valid, "fields": {k: fields[k] for k in FRONTMATTER_FIELDS if fields.get(k)}},
        "missing_core_fields": missing_core,
        "license_present": has_license,
        "author_present": has_author,
        "risk_level": top,
        "risk_class": risk_class,
        "risk_action": RISK_CLASS[risk_class][0],
        "verdict": {
            "EXTREME": "❌ 禁止安装",
            "HIGH": "⚠️ 谨慎安装（需人工批准）",
            "MEDIUM": "⚠️ 完整审查后安装",
            "LOW": "✅ 可安装",
        }[risk_class],
        "permissions": extract_permissions(texts),
        "hits": sorted(all_hits, key=lambda h: -RANK[h["level"]]),
        "checklist": {
            "frontmatter_valid": valid,
            "license_verified": has_license,
            "author_known": has_author,
            "no_p0_signal": "P0" not in levels,
            "no_p1_signal": "P1" not in levels,
            "instructions_reviewed": False,
            "network_behavior_reviewed": False,
            "permissions_reviewed": False,
        },
    }


def render_markdown(r: dict, lang: str = "en") -> str:
    zh = lang == "zh-CN"
    L = {
        "title": "技能安全审阅报告" if zh else "Skill Security Review Report",
        "target": "目标" if zh else "Target",
        "risk": "风险等级" if zh else "Risk level",
        "verdict": "结论" if zh else "Verdict",
        "perm": "权限清单（实际需求）" if zh else "Permission inventory",
        "perm_net": "网络" if zh else "Network",
        "perm_files": "文件" if zh else "Files",
        "perm_cmds": "命令" if zh else "Commands",
        "fm": "Frontmatter" if zh else "Frontmatter",
        "valid": "合法" if zh else "valid",
        "invalid": "缺失/非法" if zh else "missing/invalid",
        "miss": "缺失核心字段" if zh else "Missing core fields",
        "lic": "许可证" if zh else "License",
        "auth": "作者" if zh else "Author",
        "hits": "风险信号" if zh else "Risk signals",
        "none": "无" if zh else "none",
        "ctx_exec": "执行块" if zh else "exec-block",
        "ctx_doc": "文档提及" if zh else "doc-mention",
        "chk": "人工审阅清单" if zh else "Manual review checklist",
        "note": "静态扫描干净不代表安全保证；正文里的「文档提及」多为误报，须结合执行块语境与人工审阅判定。" if zh
                else "A clean scan is not a guarantee; 'doc-mention' hits are usually false positives—judge by exec-block context and manual review.",
    }
    lines = [
        f"# {L['title']}",
        "",
        f"- {L['target']}: `{r['target']}`",
        f"- {L['risk']}: **{r['risk_class']} — {r['risk_action']}**  (静态定级 {r['risk_level']})",
        f"- {L['verdict']}: {r['verdict']}",
        f"- {L['fm']}: {L['valid'] if r['frontmatter']['valid'] else L['invalid']}",
        f"- {L['miss']}: {', '.join(r['missing_core_fields']) or L['none']}",
        f"- {L['lic']}: {'✅' if r['license_present'] else '❌ 缺失'}  |  {L['auth']}: {'✅' if r['author_present'] else '❌ 缺失'}",
        "",
        f"## {L['hits']}",
    ]
    if r["hits"]:
        for h in r["hits"]:
            # 语境含「执行块」即视为可执行语境（兼容 执行块 / 执行块(AST) / 执行块(shell)）
            ctx = L["ctx_exec"] if str(h["context"]).startswith("执行块") else L["ctx_doc"]
            lines.append(f"- [{h['level']}] `{h['file']}` ({ctx}) — {h['signal']}")
    else:
        lines.append(f"- {L['none']}")
    lines.append("")
    # 权限清单（回答：需要读哪些文件 / 访问哪些网络 / 执行哪些命令）
    perm = r.get("permissions") or {}
    lines.append(f"## {L['perm']}")
    for key, label in (("network", L["perm_net"]), ("files", L["perm_files"]),
                       ("commands", L["perm_cmds"])):
        items = perm.get(key) or []
        shown = "、".join(items) if items else L["none"]
        lines.append(f"- {label}: {shown}")
    lines.append("")
    lines.append(f"## {L['chk']}")
    labels = {
        "frontmatter_valid": "Frontmatter 合法" if zh else "Frontmatter valid",
        "license_verified": "许可证已声明/可验证" if zh else "License declared/verifiable",
        "author_known": "作者已知（非匿名）" if zh else "Author known (not anonymous)",
        "no_p0_signal": "无 P0 高危信号" if zh else "No P0 critical signal",
        "no_p1_signal": "无 P1 需确认信号" if zh else "No P1 confirm-needed signal",
        "instructions_reviewed": "已人工审阅指令" if zh else "Instructions manually reviewed",
        "network_behavior_reviewed": "已审阅网络行为" if zh else "Network behavior reviewed",
        "permissions_reviewed": "已审阅请求权限" if zh else "Permissions reviewed",
    }
    for k, v in r["checklist"].items():
        lines.append(f"- [{'x' if v else ' '}] {labels[k]}")
    lines.append("")
    lines.append(f"> {L['note']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="find-skills++ security static scanner")
    ap.add_argument("--path", required=True, type=Path, help="技能目录或 SKILL.md 路径")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lang", choices=("en", "zh-CN"), default="zh-CN")
    ap.add_argument("--exclude-tests", action="store_true",
                    help="排除 tests/ 等测试目录（自查时用；审查第三方技能时不要用，"
                         "payload 可能藏在测试目录里）")
    args = ap.parse_args()

    if not args.path.exists():
        print(f"路径不存在: {args.path}", file=sys.stderr)
        return 3

    report = build_report(args.path, exclude_tests=args.exclude_tests)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report, args.lang), end="")
    return {"P0": 2, "P1": 1, "P2": 0}[report["risk_level"]]


if __name__ == "__main__":
    raise SystemExit(main())
