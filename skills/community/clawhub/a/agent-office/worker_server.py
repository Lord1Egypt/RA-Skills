#!/usr/bin/env python3
"""
Generic Agent Office Worker HTTP Server

用法:
    python3 worker_server.py --port 5012 --worker-id xiaolong --name 小龙 --role research --engine openclaw

支持引擎:
    - stub:     直接返回固定响应（测试用）
    - openclaw: 调用 openclaw CLI 执行任务
    - hermes:   调用 hermes CLI 执行任务
    - deerflow: 转发给本地 DeerFlow runtime
    - cli:      调用本机通用 CLI 员工
"""
import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib import error, request

SKILL_DIR = Path(__file__).resolve().parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from deerflow_runtime import (
    DEFAULT_MODEL as DEERFLOW_DEFAULT_MODEL,
    DEFAULT_REASONING_EFFORT as DEERFLOW_DEFAULT_REASONING_EFFORT,
    DEFAULT_RECURSION_LIMIT as DEERFLOW_DEFAULT_RECURSION_LIMIT,
    DEFAULT_TASK_TIMEOUT as DEERFLOW_DEFAULT_TIMEOUT,
)

# ── MemPalace 配置（可选，默认关闭）──────────────────────────
# 通过环境变量启用：
#   MEMORY_CLI   — MemPalace CLI 路径，如 /usr/local/bin/memory-cli
#   （如未设置，MemPalace 功能自动禁用，不影响 worker 正常运行）
MEMORY_CLI = os.environ.get("MEMORY_CLI")          # 无默认值，不泄露路径
MEMORY_QUERY_LIMIT = 3
DEERFLOW_RUNTIME_RUNNER = SKILL_DIR / "deerflow_runtime_runner.py"
DEERFLOW_TASK_TEMPLATE = SKILL_DIR / "templates" / "deerflow_task_prompt.txt"
CLI_PROFILES = {
    "codex": {
        "display_name": "OpenAI Codex CLI",
        "executables": ("codex",),
        "base_args": ("exec", "--skip-git-repo-check"),
        "prompt_mode": "stdin",
        "prompt_flag": "",
        "timeout": 600,
    },
    "claude-code": {
        "display_name": "Claude Code",
        "executables": ("claude", "claude-code"),
        "base_args": (),
        "prompt_mode": "stdin",
        "prompt_flag": "",
        "timeout": 600,
    },
    "aider": {
        "display_name": "Aider",
        "executables": ("aider",),
        "base_args": (),
        "prompt_mode": "arg",
        "prompt_flag": "--message",
        "timeout": 600,
    },
    "gemini-cli": {
        "display_name": "Gemini CLI",
        "executables": ("gemini", "gemini-cli"),
        "base_args": (),
        "prompt_mode": "stdin",
        "prompt_flag": "",
        "timeout": 600,
    },
    "opencode": {
        "display_name": "OpenCode",
        "executables": ("opencode",),
        "base_args": (),
        "prompt_mode": "stdin",
        "prompt_flag": "",
        "timeout": 600,
    },
}
EXTERNAL_DEFAULT_TIMEOUT = 300
EXTERNAL_DEFAULT_POLL_INTERVAL = 2.0
ROLE_DESCRIPTIONS = {
    "research": "竞品调研、信息收集、事实核查与资料整理",
    "code": "脚本开发、代码实现、问题排查与技术修复",
    "design": "界面设计、页面结构、视觉与交互建议",
    "finance": "财务记录、记账核对与台账整理",
    "complex": "复杂任务拆解、跨步骤推进与整体验收",
    "general": "通用执行、沟通协调与任务跟进",
}


def _find_memory_cli():
    """查找 MemPalace CLI，支持多路径多名称"""
    if MEMORY_CLI and os.path.exists(MEMORY_CLI):
        return MEMORY_CLI
    candidates = [
        os.environ.get("MEMORY_CLI", ""),
        "/usr/local/bin/memory-cli",
        "/usr/local/bin/memorial",
        shutil.which("memory-cli") or "",
        shutil.which("memorial") or "",
    ]
    for c in candidates:
        if c and os.path.exists(c) and os.access(c, os.X_OK):
            return c
    return None


def _memory_command(cli: str, *args: str) -> list[str]:
    if cli.endswith(".py"):
        python_bin = sys.executable or "python3"
        return [python_bin, cli, *args]
    return [cli, *args]


def query_shared_memory(query_text: str, limit: int = None) -> list[dict]:
    """查询 MemPalace 共享记忆（可选功能，未配置时无操作）"""
    limit = limit or MEMORY_QUERY_LIMIT
    cli = _find_memory_cli()
    if not query_text or not cli:
        return []
    try:
        result = subprocess.run(
            _memory_command(cli, "query", query_text, "--limit", str(limit), "--json"),
            capture_output=True, text=True, timeout=12
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                return data.get("results", [])
            except json.JSONDecodeError:
                pass
    except Exception:
        pass
    return []


def write_shared_memory(worker_id: str, room: str, title: str,
                          content: str, keywords: str = "") -> bool:
    """写入一条记忆到 MemPalace（可选功能，未配置时无操作）"""
    cli = _find_memory_cli()
    if not cli:
        return False
    try:
        result = subprocess.run(
            _memory_command(
                cli,
                "write",
                "--worker", worker_id,
                "--room", room,
                "--title", title,
                "--content", content,
                "--keywords", keywords,
            ),
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False

ACTIVE_TASKS = {}
TASK_RESULTS = {}
TASK_LOCK = threading.Lock()


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())


def get_cli_profile(profile_id: str) -> dict:
    normalized = (profile_id or "codex").strip().lower()
    return CLI_PROFILES.get(normalized, CLI_PROFILES["codex"])


def role_description(role: str) -> str:
    return ROLE_DESCRIPTIONS.get(role, f"{role} 相关任务执行与交付")


class WorkerHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[{time.strftime('%H:%M:%S')}] {fmt % args}\n")
        sys.stdout.flush()

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "timestamp": now()})

        elif self.path.startswith("/tasks/"):
            parts = self.path.split("/")
            # /tasks/{id}         → parts=['', 'tasks', '{id}']          len=3
            # /tasks/{id}/result  → parts=['', 'tasks', '{id}', 'result'] len=4
            if len(parts) == 3:
                task_id = parts[2]
                # 先查结果，再查状态
                with TASK_LOCK:
                    result = TASK_RESULTS.get(task_id)
                    task = ACTIVE_TASKS.get(task_id)
                if result:
                    self.send_json(200, result)
                elif task:
                    self.send_json(200, task)
                else:
                    self.send_json(404, {"error": "task not found"})
            elif len(parts) == 4 and parts[3] == "result":
                task_id = parts[2]
                with TASK_LOCK:
                    result = TASK_RESULTS.get(task_id)
                if result:
                    self.send_json(200, result)
                else:
                    self.send_json(404, {"error": "result not found"})
            else:
                self.send_json(400, {"error": "invalid path"})

        elif self.path == "/state":
            with TASK_LOCK:
                active_count = sum(
                    1
                    for task in ACTIVE_TASKS.values()
                    if task.get("status") in {"pending", "running"}
                )
            current_status = "running" if active_count else "idle"
            self.send_json(200, {
                "worker_id": self.server.worker_id,
                "name": self.server.worker_name,
                "role": self.server.worker_role,
                "engine": self.server.worker_engine,
                "status": current_status,
                "active_task_count": active_count,
            })

        else:
            self.send_json(404, {"error": "unknown endpoint"})

    def do_POST(self):
        if self.path == "/tasks":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8", errors="replace")
            try:
                payload = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid json"})
                return

            task_id = payload.get("task_id") or str(uuid.uuid4())
            description = payload.get("description", "")
            title = payload.get("title") or description[:40] or "未命名任务"

            task_state = {
                "task_id": task_id,
                "status": "pending",
                "title": title,
                "created_at": now(),
                "updated_at": now()
            }
            with TASK_LOCK:
                ACTIVE_TASKS[task_id] = task_state

            # 后台执行
            thread = threading.Thread(
                target=self.server.execute_task,
                args=(task_id, title, description)
            )
            thread.daemon = True
            thread.start()

            self.send_json(202, {"task_id": task_id, "status": "pending"})

        else:
            self.send_json(404, {"error": "unknown endpoint"})

class WorkerServer(HTTPServer):

    def __init__(
        self,
        port,
        worker_id,
        worker_name,
        worker_role,
        worker_engine,
        prompt_file,
        workspace_dir,
        cli_profile="codex",
        cli_cmd="",
        cli_args="",
        cli_timeout=0,
        deerflow_runtime_python="",
        deerflow_config="",
        deerflow_home="",
        deerflow_agent_name="",
        deerflow_model="",
        deerflow_reasoning_effort="",
        deerflow_recursion_limit=0,
        deerflow_timeout=0,
        external_upstream_url="",
        external_poll_interval=0.0,
        external_timeout=0,
    ):
        super().__init__(("127.0.0.1", port), WorkerHandler)
        self.worker_id = worker_id
        self.worker_name = worker_name
        self.worker_role = worker_role
        self.worker_engine = worker_engine
        self.prompt_file = prompt_file
        self.workspace_dir = workspace_dir or os.getcwd()
        self.cli_profile = cli_profile or "codex"
        self.cli_cmd = cli_cmd or ""
        self.cli_args = cli_args or ""
        self.cli_timeout = cli_timeout or get_cli_profile(self.cli_profile)["timeout"]
        self.deerflow_runtime_python = deerflow_runtime_python or ""
        self.deerflow_config = deerflow_config or ""
        self.deerflow_home = deerflow_home or ""
        self.deerflow_agent_name = deerflow_agent_name or worker_id
        self.deerflow_model = deerflow_model or DEERFLOW_DEFAULT_MODEL
        self.deerflow_reasoning_effort = (
            deerflow_reasoning_effort or DEERFLOW_DEFAULT_REASONING_EFFORT
        )
        self.deerflow_recursion_limit = (
            deerflow_recursion_limit or DEERFLOW_DEFAULT_RECURSION_LIMIT
        )
        self.deerflow_timeout = deerflow_timeout or DEERFLOW_DEFAULT_TIMEOUT
        self.external_upstream_url = (external_upstream_url or "").rstrip("/")
        self.external_poll_interval = (
            external_poll_interval or EXTERNAL_DEFAULT_POLL_INTERVAL
        )
        self.external_timeout = external_timeout or EXTERNAL_DEFAULT_TIMEOUT

    def execute_task(self, task_id, title, description):
        """执行任务"""
        with TASK_LOCK:
            ACTIVE_TASKS[task_id] = {
                "task_id": task_id,
                "status": "running",
                "title": title,
                "updated_at": now()
            }

        try:
            # ── 执行前：查询 MemPalace ──────────────────
            query_text = f"{title or ''}\n{description or ''}"
            memory_matches = query_shared_memory(query_text, limit=3)

            # ── 执行任务 ────────────────────────────────
            if self.worker_engine == "stub":
                time.sleep(1)
                result_content = f"[stub模式] 收到任务：{title or description[:50]}"

            elif self.worker_engine == "openclaw":
                role = self._guess_role(description)
                prompt = self._build_prompt(role, title, description, memory_matches)
                result_content = self._run_openclaw(prompt)

            elif self.worker_engine == "hermes":
                role = self._guess_role(description)
                prompt = self._build_prompt(role, title, description, memory_matches)
                result_content = self._run_hermes(prompt)

            elif self.worker_engine == "deerflow":
                result_content = self._run_deerflow(title, description, memory_matches)

            elif self.worker_engine == "cli":
                role = self._guess_role(description)
                prompt = self._build_prompt(role, title, description, memory_matches)
                result_content = self._run_cli(prompt)

            elif self.worker_engine == "external":
                result_content = self._run_external(title, description, memory_matches)

            else:
                result_content = f"[未知引擎: {self.worker_engine}]"

            # ── 执行后：写入记忆 ────────────────────────
            if self.worker_engine != "stub" and result_content and len(result_content) > 20:
                summary_text = result_content[:200].replace("\n", " ")
                room_map = {"code": "code-findings", "research": "research-findings",
                            "design": "design-findings", "complex": "complex-findings"}
                room = room_map.get(self.worker_role, "general-findings")
                write_shared_memory(
                    worker_id=self.worker_id,
                    room=room,
                    title=title or description[:30],
                    content=summary_text,
                    keywords=self.worker_role
                )

            with TASK_LOCK:
                TASK_RESULTS[task_id] = {
                    "task_id": task_id,
                    "status": "done",
                    "result": {
                        "content": result_content,
                        "format": "markdown"
                    },
                    "summary": (title or description[:50]) + " — 完成"
                }
                ACTIVE_TASKS[task_id]["status"] = "done"
                ACTIVE_TASKS[task_id]["updated_at"] = now()

        except Exception as e:
            with TASK_LOCK:
                TASK_RESULTS[task_id] = {
                    "task_id": task_id,
                    "status": "error",
                    "result": {"content": f"执行出错: {str(e)}", "format": "text"},
                    "summary": f"出错: {str(e)[:50]}"
                }
                ACTIVE_TASKS[task_id]["status"] = "error"
                ACTIVE_TASKS[task_id]["updated_at"] = now()

    def _guess_role(self, text):
        text = (text or "").lower()
        if any(k in text for k in ["代码", "script", "python", "js", "改", "bug"]):
            return "code"
        if any(k in text for k in ["调研", "research", "竞品", "查", "分析"]):
            return "research"
        if any(k in text for k in ["设计", "design", "前端", "ui", "css"]):
            return "design"
        return "general"

    def _build_prompt(self, role, title, description, memory_matches=None):
        memory_matches = memory_matches or []
        sections = [
            f"你是团队成员 {self.worker_name}，职责 {self.worker_role}。",
            "",
            "任务标题：" + (title or "(无标题)"),
            "任务描述：" + (description or "(无描述)"),
            "",
        ]

        # ── 附上 MemPalace 相关记忆 ──────────────────
        if memory_matches:
            sections += ["【团队共享记忆（MemPalace）相关结果】"]
            for i, item in enumerate(memory_matches[:3], 1):
                content = item.get("text", item.get("content", ""))
                worker = item.get("worker", "-")
                room = item.get("room", "-")
                sections.append(f"[记忆{i}] [{worker}/{room}] {content[:300]}")
            sections.append("")
        # ── 任务执行指引 ───────────────────────────────
        if role == "code":
            sections += ["请直接输出代码，用```包裹。完成后返回：", "```json", '{"status":"done","code":"..."}', "```"]
        elif role == "research":
            sections += ["请返回调研摘要，包括核心发现、数据来源、下一步建议。"]
        elif role == "design":
            sections += ["请返回设计方案，包括页面结构、组件、样式说明。"]
        else:
            sections += ["请直接回答。"]

        sections += [
            "",
            "【任务完成后，如有必要，可将结果写入共享记忆（可选，需配置 MEMORY_CLI）】"
        ]
        return "\n".join(sections)

    def _build_shared_memory_context(self, memory_matches=None):
        memory_matches = memory_matches or []
        if not memory_matches:
            return "暂无相关共享记忆。"

        sections = [
            "Shared Office Memory (MemPalace, read-only):",
            "- 只允许阅读这些上下文，不要写回共享记忆。",
            "",
        ]
        for index, item in enumerate(memory_matches[:3], 1):
            title = item.get("title") or f"记忆{index}"
            worker = item.get("worker", "-")
            room = item.get("room", "-")
            content = item.get("summary_text") or item.get("text") or item.get("content") or ""
            sections.append(f"{index}. {title} | worker={worker} | room={room}")
            sections.append(str(content)[:400])
        return "\n".join(sections)

    def _build_external_description(self, title, description, memory_matches=None):
        sections = [
            f"这是 Agent Office 转发给外部员工 {self.worker_name} 的任务。",
            "请保持你原有身份、设定和长期记忆，不要把自己重置成新的角色。",
            "",
            "任务标题：" + (title or "(无标题)"),
            "任务描述：" + (description or "(无描述)"),
            "",
            "办公室补充上下文：",
            self._build_shared_memory_context(memory_matches),
        ]
        return "\n".join(sections).strip()

    def _build_deerflow_prompt(self, title, description, memory_matches=None):
        template_text = ""
        if DEERFLOW_TASK_TEMPLATE.exists():
            template_text = DEERFLOW_TASK_TEMPLATE.read_text(encoding="utf-8")
        if not template_text:
            template_text = (
                "你是 __WORKER_NAME__（__WORKER_ID__），是 Agent Office 的 DeerFlow 2.0 团队型员工。\n"
                "职责：__ROLE_DESCRIPTION__\n\n"
                "任务标题：__TITLE__\n"
                "任务描述：__DESCRIPTION__\n"
                "共享记忆上下文：\n__SHARED_MEMORY_CONTEXT__\n\n"
                "最终只返回 JSON：\n"
                "{\n"
                '  "team_summary": "",\n'
                '  "collaboration_mode": "deerflow_team",\n'
                '  "current_scope": ["..."],\n'
                '  "next_step_suggestions": ["..."],\n'
                '  "handoff_note": ""\n'
                "}\n"
            )
        rendered = template_text
        replacements = {
            "__WORKER_ID__": self.worker_id,
            "__WORKER_NAME__": self.worker_name,
            "__ROLE__": self.worker_role,
            "__ROLE_DESCRIPTION__": role_description(self.worker_role),
            "__TITLE__": title or "(无标题)",
            "__DESCRIPTION__": description or "(无描述)",
            "__SHARED_MEMORY_CONTEXT__": self._build_shared_memory_context(memory_matches),
        }
        for key, value in replacements.items():
            rendered = rendered.replace(key, str(value))
        return rendered

    def _format_deerflow_result(self, payload):
        lines = [f"{self.worker_name} 团队已回传结果："]
        if payload.get("team_summary"):
            lines.append(str(payload["team_summary"]))
        if payload.get("current_scope"):
            lines.append("")
            lines.append("当前范围：")
            for item in payload["current_scope"]:
                lines.append(f"- {item}")
        if payload.get("next_step_suggestions"):
            lines.append("")
            lines.append("下一步建议：")
            for item in payload["next_step_suggestions"]:
                lines.append(f"- {item}")
        if payload.get("delegation_trace"):
            lines.append("")
            lines.append("团队轨迹：")
            for item in payload["delegation_trace"][:8]:
                lines.append(f"- {item}")
        if payload.get("handoff_note"):
            lines.append("")
            lines.append("交接：")
            lines.append(str(payload["handoff_note"]))
        if payload.get("parse_note"):
            lines.append("")
            lines.append("解析备注：")
            lines.append(str(payload["parse_note"]))
        if payload.get("raw_team_output"):
            lines.append("")
            lines.append("原始回复：")
            lines.append(str(payload["raw_team_output"])[:4000])
        return "\n".join(lines).strip()

    def _run_openclaw(self, prompt_text):
        try:
            result = subprocess.run(
                ["openclaw", "agent", "--agent", self.worker_id, "--json", "--message", prompt_text],
                capture_output=True, text=True, timeout=120, cwd=self.workspace_dir
            )
            if result.returncode == 0 and result.stdout.strip():
                return self._parse_openclaw_result(result.stdout)
            return f"[openclaw执行失败] {result.stderr[:200]}" if result.stderr else "[openclaw无输出]"
        except subprocess.TimeoutExpired:
            return "[超时]"
        except FileNotFoundError:
            return "[CLI 未安装]"

    def _parse_openclaw_result(self, raw):
        """解析 openclaw agent --json 的输出"""
        import json as _json
        candidates = [raw.strip()]
        candidates.extend(
            line.strip()
            for line in raw.splitlines()
            if line.strip().startswith("{") and line.strip().endswith("}")
        )
        for candidate in reversed(candidates):
            if not candidate:
                continue
            try:
                data = _json.loads(candidate)
                result = data.get("result", {})
                if isinstance(result, dict):
                    payloads = result.get("payloads", [])
                    if payloads:
                        return payloads[0].get("text", str(result))
                return str(result)
            except Exception:
                continue
        return raw.strip() if raw.strip() else "[解析失败]"

    def _run_hermes(self, prompt_text):
        try:
            result = subprocess.run(
                ["hermes", "agent", "--json", "--message", prompt_text],
                capture_output=True, text=True, timeout=120, cwd=self.workspace_dir
            )
            if result.returncode == 0:
                return self._parse_openclaw_result(result.stdout)
            return (result.stdout + "\n" + result.stderr).strip() or "[hermes执行失败]"
        except FileNotFoundError:
            return "[hermes 未安装]"

    def _run_deerflow(self, title, description, memory_matches=None):
        """直接调用嵌入式 DeerFlow runtime。"""
        runtime_python = Path(self.deerflow_runtime_python)
        config_path = Path(self.deerflow_config)
        home_dir = Path(self.deerflow_home)
        if not runtime_python.exists():
            return "[DeerFlow 未安装] 共享 runtime 尚未就绪"
        if not config_path.exists():
            return "[DeerFlow 配置缺失] 找不到 deerflow_config.yaml"
        if not DEERFLOW_RUNTIME_RUNNER.exists():
            return "[DeerFlow 运行器缺失] deerflow_runtime_runner.py 不存在"

        prompt_text = self._build_deerflow_prompt(title, description, memory_matches)
        cmd = [
            str(runtime_python),
            str(DEERFLOW_RUNTIME_RUNNER),
            "--config", str(config_path),
            "--home", str(home_dir),
            "--agent-name", self.deerflow_agent_name,
            "--model", self.deerflow_model,
            "--reasoning-effort", self.deerflow_reasoning_effort,
            "--recursion-limit", str(self.deerflow_recursion_limit),
            "--thread-id", f"{self.worker_id}-{uuid.uuid4()}",
            "--title", title or "DeerFlow任务",
            "--prompt", prompt_text,
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.deerflow_timeout,
                cwd=self.workspace_dir,
            )
            if result.returncode != 0:
                detail = (result.stderr or result.stdout or "unknown error").strip()
                return f"[DeerFlow执行失败] {detail[:500]}"
            stdout = (result.stdout or "").strip()
            if not stdout:
                return "[DeerFlow无输出]"
            try:
                payload = json.loads(stdout)
                return self._format_deerflow_result(payload)
            except json.JSONDecodeError:
                return stdout
        except subprocess.TimeoutExpired:
            return f"[DeerFlow执行超时] after {self.deerflow_timeout}s"
        except FileNotFoundError:
            return "[DeerFlow 运行环境缺失]"

    def _resolve_cli_executable(self, profile: dict) -> str:
        for candidate in profile["executables"]:
            resolved = shutil.which(candidate)
            if resolved:
                return resolved
        return profile["executables"][0]

    def _build_cli_command(self, profile: dict, prompt_text: str) -> list[str]:
        if self.cli_cmd:
            cmd = shlex.split(self.cli_cmd)
        else:
            cmd = [self._resolve_cli_executable(profile), *profile.get("base_args", ())]

        if self.cli_args:
            cmd.extend(shlex.split(self.cli_args))

        prompt_mode = profile.get("prompt_mode", "stdin")
        prompt_flag = profile.get("prompt_flag", "")
        if prompt_mode == "arg":
            if prompt_flag:
                cmd.extend([prompt_flag, prompt_text])
            else:
                cmd.append(prompt_text)
        return cmd

    def _run_cli(self, prompt_text):
        profile = get_cli_profile(self.cli_profile)
        cmd = self._build_cli_command(profile, prompt_text)
        run_kwargs = {
            "capture_output": True,
            "text": True,
            "timeout": self.cli_timeout,
            "cwd": self.workspace_dir,
        }
        if profile.get("prompt_mode", "stdin") == "stdin":
            run_kwargs["input"] = prompt_text

        try:
            result = subprocess.run(cmd, **run_kwargs)
            if result.returncode == 0:
                stdout = (result.stdout or "").strip()
                stderr = (result.stderr or "").strip()
                if stdout:
                    return stdout
                if stderr:
                    return f"[CLI stderr] {stderr}"
                return "[CLI 无输出]"
            stderr = (result.stderr or "").strip()
            stdout = (result.stdout or "").strip()
            details = stderr or stdout or "unknown error"
            return f"[CLI执行失败] {details[:300]}"
        except subprocess.TimeoutExpired:
            return f"[CLI执行超时] {profile['display_name']} after {self.cli_timeout}s"
        except FileNotFoundError:
            return f"[CLI 未安装] {profile['display_name']}"

    def _external_request(self, method, path, payload=None, timeout=15):
        if not self.external_upstream_url:
            raise RuntimeError("external upstream url 未配置")

        url = f"{self.external_upstream_url}{path}"
        body = None
        headers = {}
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = request.Request(url, data=body, headers=headers, method=method.upper())
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}

    def _extract_result_content(self, payload):
        if not isinstance(payload, dict):
            return str(payload)
        result = payload.get("result")
        if isinstance(result, dict):
            content = result.get("content")
            if content:
                return str(content)
        if payload.get("summary"):
            return str(payload["summary"])
        return json.dumps(payload, ensure_ascii=False)

    def _run_external(self, title, description, memory_matches=None):
        forwarded_description = self._build_external_description(
            title,
            description,
            memory_matches,
        )
        try:
            _, submit_payload = self._external_request(
                "POST",
                "/tasks",
                {
                    "title": title or "Agent Office 转发任务",
                    "description": forwarded_description,
                },
                timeout=min(15, self.external_timeout),
            )
            upstream_task_id = submit_payload.get("task_id")
            if not upstream_task_id:
                return "[external执行失败] 上游未返回 task_id"

            deadline = time.time() + self.external_timeout
            while time.time() < deadline:
                _, task_payload = self._external_request(
                    "GET",
                    f"/tasks/{upstream_task_id}",
                    timeout=min(15, self.external_timeout),
                )
                status = task_payload.get("status")
                if status == "done":
                    return self._extract_result_content(task_payload)
                if status == "error":
                    return self._extract_result_content(task_payload)
                time.sleep(self.external_poll_interval)
            return f"[external执行超时] after {self.external_timeout}s"
        except error.HTTPError as exc:
            return f"[external执行失败] HTTP {exc.code}"
        except error.URLError as exc:
            return f"[external执行失败] {exc.reason}"
        except json.JSONDecodeError:
            return "[external执行失败] 上游返回了非 JSON 响应"
        except Exception as exc:
            return f"[external执行失败] {exc}"


def main():
    parser = argparse.ArgumentParser(description="Agent Office Worker Server")
    parser.add_argument("--port", type=int, required=True, help="监听端口")
    parser.add_argument("--worker-id", required=True, help="员工工号")
    parser.add_argument("--name", required=True, help="员工名字")
    parser.add_argument("--role", default="general", help="职责关键词")
    parser.add_argument("--engine", default="stub", help="引擎类型: stub|openclaw|hermes|deerflow|cli|external")
    parser.add_argument("--prompt", default="", help="prompt文件路径")
    parser.add_argument("--workspace-dir", default="", help="员工工作目录")
    parser.add_argument("--cli-profile", default="codex", help="CLI profile")
    parser.add_argument("--cli-cmd", default="", help="CLI 命令覆盖")
    parser.add_argument("--cli-args", default="", help="CLI 额外参数")
    parser.add_argument("--cli-timeout", type=int, default=0, help="CLI 超时秒数")
    parser.add_argument("--deerflow-runtime-python", default="", help="DeerFlow runtime Python")
    parser.add_argument("--deerflow-config", default="", help="DeerFlow 配置文件")
    parser.add_argument("--deerflow-home", default="", help="DeerFlow home 目录")
    parser.add_argument("--deerflow-agent-name", default="", help="DeerFlow agent 名称")
    parser.add_argument("--deerflow-model", default="", help="DeerFlow 模型")
    parser.add_argument("--deerflow-reasoning-effort", default="", help="DeerFlow reasoning effort")
    parser.add_argument("--deerflow-recursion-limit", type=int, default=0, help="DeerFlow recursion limit")
    parser.add_argument("--deerflow-timeout", type=int, default=0, help="DeerFlow 任务超时")
    parser.add_argument("--external-upstream-url", default="", help="external 引擎上游 URL")
    parser.add_argument("--external-poll-interval", type=float, default=0.0, help="external 引擎轮询间隔")
    parser.add_argument("--external-timeout", type=int, default=0, help="external 引擎超时")
    args = parser.parse_args()

    print(f"🚀 启动 {args.name} (引擎:{args.engine}, 端口:{args.port})")
    server = WorkerServer(
        args.port,
        args.worker_id,
        args.name,
        args.role,
        args.engine,
        args.prompt,
        args.workspace_dir,
        cli_profile=args.cli_profile,
        cli_cmd=args.cli_cmd,
        cli_args=args.cli_args,
        cli_timeout=args.cli_timeout,
        deerflow_runtime_python=args.deerflow_runtime_python,
        deerflow_config=args.deerflow_config,
        deerflow_home=args.deerflow_home,
        deerflow_agent_name=args.deerflow_agent_name,
        deerflow_model=args.deerflow_model,
        deerflow_reasoning_effort=args.deerflow_reasoning_effort,
        deerflow_recursion_limit=args.deerflow_recursion_limit,
        deerflow_timeout=args.deerflow_timeout,
        external_upstream_url=args.external_upstream_url,
        external_poll_interval=args.external_poll_interval,
        external_timeout=args.external_timeout,
    )
    print(f"✅ {args.name} 已就绪 on http://127.0.0.1:{args.port}")
    print(f"   健康检查: http://127.0.0.1:{args.port}/health")
    print(f"   提交任务: POST http://127.0.0.1:{args.port}/tasks")
    server.serve_forever()


if __name__ == "__main__":
    main()
