#!/usr/bin/env python3
"""
add_worker.py —— 添加新员工（纯 Python 版，避免 shell 编码问题）
用法: python3 add_worker.py <名字> <引擎> <角色> [可选参数]
示例: python3 add_worker.py 小龙 openclaw research
      python3 add_worker.py 小克 cli code --cli-profile claude-code
"""
import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional
from urllib import error, request

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from deerflow_runtime import (
    DEFAULT_MODEL as DEERFLOW_DEFAULT_MODEL,
    DEFAULT_REASONING_EFFORT as DEERFLOW_DEFAULT_REASONING_EFFORT,
    DEFAULT_RECURSION_LIMIT as DEERFLOW_DEFAULT_RECURSION_LIMIT,
    DEFAULT_TASK_TIMEOUT as DEERFLOW_DEFAULT_TIMEOUT,
    ensure_deerflow_runtime,
    ensure_worker_home,
    missing_prerequisites,
    runtime_update_on_add,
    write_worker_runtime_config,
)

# ════════════════════════════════════════════════════════════
# 路径配置
# ════════════════════════════════════════════════════════════
OFFICE_DIR = Path(os.environ.get("HERMES_OFFICE_DIR", Path.home() / ".hermes" / "office"))
STATE_FILE = OFFICE_DIR / "state" / "office_state.json"
WORKER_SERVER = SKILL_DIR / "worker_server.py"
TEMPLATE_DIR = SKILL_DIR / "templates"

ENGINE_TEMPLATES = {
    "openclaw": "openclaw_prompt.md",
    "hermes": "hermes_prompt.md",
    "deerflow": "deerflow_prompt.md",
    "cli": "cli_prompt.md",
    "external": "external_prompt.md",
    "stub": "stub_prompt.md",
}

ROLE_DESCRIPTIONS = {
    "research": "竞品调研、信息收集、事实核查与资料整理",
    "code": "脚本开发、代码实现、问题排查与技术修复",
    "design": "界面设计、页面结构、视觉与交互建议",
    "finance": "财务记录、记账核对与台账整理",
    "complex": "复杂任务拆解、跨步骤推进与整体验收",
    "general": "通用执行、沟通协调与任务跟进",
}

ENGINE_TIMEOUTS = {
    "openclaw": 120,
    "hermes": 120,
    "deerflow": 300,
    "cli": 600,
    "external": 300,
    "stub": 30,
}

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


# ════════════════════════════════════════════════════════════
# 工具函数
# ════════════════════════════════════════════════════════════
def pinyin(name: str) -> str:
    """中文名字 → worker_id (拼音)"""
    m = {
        '小':'xiao','龙':'long','扣':'kou','设':'she','秘':'mi',
        '虾':'xia','会':'hui','计':'ji','助':'zhu','行':'xing',
        '政':'zheng','理':'li','D':'d','d':'d',
        '阿':'a','杰':'jie','文':'wen','案':'an','财':'cai',
        '务':'wu'
    }
    result = []
    i = 0
    s = name.strip()
    while i < len(s):
        two = s[i:i+2]
        if len(two) == 2 and two in m:
            result.append(m[two]); i += 2; continue
        ch = s[i]
        if ch in m:
            result.append(m[ch])
        elif ch.isascii():
            result.append(ch)
        i += 1
    pid = re.sub(r'[^a-z0-9]', '_', ''.join(result).lower())
    return pid if pid else f"worker_{int(time.time())}"


def init_state():
    """初始化状态文件"""
    OFFICE_DIR.mkdir(parents=True, exist_ok=True)
    (OFFICE_DIR / "state").mkdir(exist_ok=True)
    if not STATE_FILE.exists():
        data = {
            "workers": {},
            "port_pool": {
                "used": [],
                "available": list(range(5011, 5021))
            }
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def load_state() -> dict:
    init_state()
    with open(STATE_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_state(data: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def alloc_port(state: dict) -> Optional[int]:
    available = state.get("port_pool", {}).get("available", [])
    if not available:
        return None
    return available[0]


def alloc_port_commit(state: dict, port: int):
    state["port_pool"]["available"] = [p for p in state["port_pool"].get("available", []) if p != port]
    state["port_pool"]["used"] = sorted(set(state["port_pool"].get("used", []) + [port]))


def role_description(role: str) -> str:
    return ROLE_DESCRIPTIONS.get(role, f"{role} 相关任务执行与交付")


def get_cli_profile(profile_id: str) -> dict:
    normalized = (profile_id or "codex").strip().lower()
    if normalized not in CLI_PROFILES:
        available = ", ".join(sorted(CLI_PROFILES))
        raise ValueError(f"未知 CLI profile: {profile_id}，支持: {available}")
    return CLI_PROFILES[normalized]


def cli_profile_display(profile_id: str) -> str:
    return get_cli_profile(profile_id)["display_name"]


def cli_executable_ready(cli_cmd: str, cli_profile: str) -> bool:
    if cli_cmd:
        try:
            parts = shlex.split(cli_cmd)
        except ValueError:
            return False
        if not parts:
            return False
        executable = parts[0]
        return bool(shutil.which(executable) or os.path.exists(os.path.expanduser(executable)))

    profile = get_cli_profile(cli_profile)
    for candidate in profile["executables"]:
        if shutil.which(candidate):
            return True
    return False


def normalize_workspace_dir(worker_dir: Path, workspace_override: str) -> str:
    if workspace_override:
        return str(Path(os.path.expanduser(workspace_override)).resolve())
    return str(worker_dir)


def render_template(template_text: str, values: dict[str, str]) -> str:
    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def worker_healthcheck(port: int, timeout: int = 5) -> bool:
    url = f"http://127.0.0.1:{port}/health"
    try:
        with request.urlopen(url, timeout=timeout) as resp:
            if resp.status != 200:
                return False
            payload = json.loads(resp.read().decode("utf-8"))
            return payload.get("status") == "ok"
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError, ValueError):
        return False


def normalize_external_upstream_url(url: str, port: int = 0) -> str:
    raw = (url or "").strip()
    if not raw and port:
        raw = f"http://127.0.0.1:{port}"
    if not raw:
        return ""
    if "://" not in raw:
        raw = f"http://{raw}"
    return raw.rstrip("/")


def external_upstream_ready(url: str, timeout: int = 5) -> bool:
    if not url:
        return False
    health_url = f"{normalize_external_upstream_url(url)}/health"
    try:
        with request.urlopen(health_url, timeout=timeout) as resp:
            if resp.status != 200:
                return False
            payload = json.loads(resp.read().decode("utf-8"))
            return payload.get("status") == "ok"
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError, ValueError):
        return False


# ════════════════════════════════════════════════════════════
# 核心逻辑
# ════════════════════════════════════════════════════════════
def check_duplicate(state: dict, name: str, worker_id: str, engine: str):
    """重名检测，两层都查：state文件 + openclaw agents"""
    # ── 层1：state文件中的name ──────────────────────────
    for wid, w in state.get("workers", {}).items():
        if wid == worker_id:
            print(f"❌ 工号 '{worker_id}' 已存在")
            print(f"   已有员工: {w.get('name', wid)}")
            print(f"   端口: {w.get('port','?')} | 引擎: {w.get('engine','?')} | 状态: {w.get('status','?')}")
            sys.exit(1)
        if w.get("name") == name:
            print(f"❌ 员工「{name}」已存在")
            print(f"   工号: {wid}")
            print(f"   端口: {w.get('port','?')} | 引擎: {w.get('engine','?')} | 状态: {w.get('status','?')}")
            print()
            print(f"   请换一个新名字，例如：")
            print(f"   · {name} → {name}2 / 阿杰 / {name}同学")
            print()
            print(f"   或先移除旧员工：python3 remove_worker.py {wid}")
            sys.exit(1)

    # ── 层2：openclaw agents（仅openclaw/hermes）──────
    if engine in ("openclaw", "hermes"):
        try:
            r = subprocess.run(
                ["openclaw", "agents", "list", "--json"],
                capture_output=True, text=True, timeout=3
            )
            if r.returncode == 0:
                try:
                    agents = json.loads(r.stdout)
                    ids = [a.get("id") for a in agents] if isinstance(agents, list) else []
                    if worker_id in ids:
                        print(f"❌ openclaw agent '{worker_id}' 已存在（与「{name}」同名冲突）")
                        print(f"   请换一个员工名字")
                        sys.exit(1)
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass  # 网络/进程问题不阻塞


def check_engine(
    engine: str,
    cli_profile: str = "codex",
    cli_cmd: str = "",
    external_upstream_url: str = "",
) -> bool:
    """检测引擎是否可用。只检测，不安装；未安装时提示用户手动安装。"""
    if engine == "stub":
        print("📦 stub 模式无需安装（纯模拟，不启动真实进程）")
        return True

    if engine == "openclaw":
        if subprocess.run(["which", "openclaw"], capture_output=True).returncode == 0:
            v = subprocess.run(["openclaw", "--version"],
                             capture_output=True, text=True, timeout=3)
            print(f"✅ openclaw 已安装: {v.stdout.strip() or 'ok'}")
            return True
        print("❌ openclaw 未安装。请先安装：pip install openclaw")
        return False

    if engine == "hermes":
        if subprocess.run(["which", "hermes"], capture_output=True).returncode == 0:
            print("✅ hermes 已安装")
            return True
        print("❌ hermes 未安装。请先安装：pip install hermes-ai")
        return False

    if engine == "deerflow":
        missing = missing_prerequisites()
        if not missing:
            print("✅ deerflow 引擎可用（技能内将自动安装/复用共享 DeerFlow runtime）")
            return True
        print("❌ deerflow 引擎缺少自动安装依赖: " + ", ".join(missing))
        return False

    if engine == "cli":
        if cli_executable_ready(cli_cmd, cli_profile):
            profile_name = cli_profile_display(cli_profile)
            if cli_cmd:
                print(f"✅ cli 引擎可用（命令覆盖: {cli_cmd}）")
            else:
                print(f"✅ cli 引擎可用（profile: {profile_name}）")
            return True
        profile_name = cli_profile_display(cli_profile)
        print(f"❌ cli 引擎不可用。当前 profile: {profile_name}")
        print("   请先安装对应 CLI，或通过 --cli-cmd 指定可执行命令。")
        return False

    if engine == "external":
        if not external_upstream_url:
            print("❌ external 引擎需要 --external-upstream-url 或 --external-upstream-port")
            return False
        if external_upstream_ready(external_upstream_url):
            print(f"✅ external 引擎可用（上游: {normalize_external_upstream_url(external_upstream_url)}）")
            return True
        print(f"❌ external 引擎无法连通上游: {normalize_external_upstream_url(external_upstream_url)}")
        print("   需要上游 worker 兼容 /health 与 /tasks HTTP 协议。")
        return False

    return True


def write_soul(
    worker_dir: Path,
    name: str,
    worker_id: str,
    role: str,
    engine: str,
    port: int,
    cli_profile: str = "",
    external_upstream_url: str = "",
):
    """生成 SOUL.md（基于 templates/ 渲染）"""
    template_name = ENGINE_TEMPLATES.get(engine, "openclaw_prompt.md")
    template_path = TEMPLATE_DIR / template_name
    if template_path.exists():
        template_text = template_path.read_text(encoding="utf-8")
    else:
        template_text = (
            "# {{NAME}}\n\n"
            "- 工号：{{WORKER_ID}}\n"
            "- 职责：{{ROLE}}\n"
            "- 引擎：{{ENGINE}}\n"
        )

    rendered = render_template(
        template_text,
        {
            "NAME": name,
            "ROLE": role,
            "WORKER_ID": worker_id,
            "PORT": port,
            "ROLE_DESCRIPTION": role_description(role),
            "TIMEOUT": ENGINE_TIMEOUTS.get(engine, 120),
            "ENGINE": engine,
            "CLI_PROFILE": cli_profile or "-",
            "CLI_PROFILE_DISPLAY": cli_profile_display(cli_profile) if cli_profile else "-",
            "EXTERNAL_UPSTREAM_URL": external_upstream_url or "-",
        },
    )
    with open(worker_dir / "SOUL.md", "w", encoding="utf-8") as f:
        f.write(rendered.strip() + "\n")


def register_openclaw_agent(worker_id: str, worker_dir: Path, name: str, role: str):
    """注册 openclaw agent"""
    try:
        # 先检查是否已存在（设短超时）
        r = subprocess.run(
            ["openclaw", "agents", "list", "--json"],
            capture_output=True, text=True, timeout=3
        )
        existing_ids = []
        if r.returncode == 0:
            try:
                existing_ids = [a.get("id") for a in json.loads(r.stdout)]
            except json.JSONDecodeError:
                pass

        if worker_id not in existing_ids:
            print(f"📋 注册 openclaw agent: {worker_id}")
            subproc = subprocess.run(
                ["openclaw", "agents", "add", worker_id,
                 "--workspace", str(worker_dir),
                 "--non-interactive"],
                capture_output=True, text=True, timeout=10
            )
            if subproc.returncode != 0:
                print(f"   (非阻塞，{subproc.stderr[:80] if subproc.stderr else 'continue'})")

        # 设置身份
        emoji_map = {"research": "🔍", "code": "💻", "design": "🎨",
                     "finance": "💰", "complex": "🧠", "custom": "🤖"}
        emoji = emoji_map.get(role, "🤖")
        subprocess.run(
            ["openclaw", "agents", "set-identity",
             "--agent", worker_id, "--name", name, "--emoji", emoji],
            capture_output=True, timeout=5
        )
    except subprocess.TimeoutExpired:
        print(f"   (openclaw agent 注册超时，非阻塞继续)")
    except Exception as e:
        print(f"   (openclaw agent 注册非阻塞继续: {e})")


def start_worker(
    port: int,
    worker_id: str,
    name: str,
    role: str,
    engine: str,
    worker_dir: Path,
    workspace_dir: str,
    cli_profile: str = "",
    cli_cmd: str = "",
    cli_args: str = "",
    cli_timeout: int = 0,
    deerflow_runtime_python: str = "",
    deerflow_config: str = "",
    deerflow_home: str = "",
    deerflow_agent_name: str = "",
    deerflow_model: str = "",
    deerflow_reasoning_effort: str = "",
    deerflow_recursion_limit: int = 0,
    deerflow_timeout: int = 0,
    external_upstream_url: str = "",
    external_poll_interval: float = 2.0,
    external_timeout: int = 0,
):
    """启动 worker HTTP 服务器"""
    if engine == "stub":
        print("📦 stub 模式已注册（无独立进程）")
        return "idle"

    log_file = worker_dir / "logs" / "worker.log"
    log_file.parent.mkdir(exist_ok=True)

    with open(log_file, "w", encoding="utf-8") as lf:
        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting worker_server.py\n")
        lf.flush()
        cmd = [
            sys.executable, str(WORKER_SERVER),
            "--port", str(port),
            "--worker-id", worker_id,
            "--name", name,
            "--role", role,
            "--engine", engine,
            "--workspace-dir", workspace_dir,
        ]
        if engine == "cli":
            cmd += ["--cli-profile", cli_profile or "codex"]
            if cli_cmd:
                cmd += ["--cli-cmd", cli_cmd]
            if cli_args:
                cmd += ["--cli-args", cli_args]
            if cli_timeout:
                cmd += ["--cli-timeout", str(cli_timeout)]
        if engine == "deerflow":
            cmd += [
                "--deerflow-runtime-python", deerflow_runtime_python,
                "--deerflow-config", deerflow_config,
                "--deerflow-home", deerflow_home,
                "--deerflow-agent-name", deerflow_agent_name,
                "--deerflow-model", deerflow_model,
                "--deerflow-reasoning-effort", deerflow_reasoning_effort,
                "--deerflow-recursion-limit", str(deerflow_recursion_limit or DEERFLOW_DEFAULT_RECURSION_LIMIT),
                "--deerflow-timeout", str(deerflow_timeout or DEERFLOW_DEFAULT_TIMEOUT),
            ]
        if engine == "external":
            cmd += [
                "--external-upstream-url", external_upstream_url,
                "--external-poll-interval", str(external_poll_interval or 2.0),
                "--external-timeout", str(external_timeout or ENGINE_TIMEOUTS["external"]),
            ]
        proc = subprocess.Popen(
            cmd,
            stdout=lf, stderr=subprocess.STDOUT
        )

    # 等待启动并严格健康检查
    for _ in range(6):
        time.sleep(1)
        if worker_healthcheck(port):
            print(f"🚀 {name} 已启动 (PID: {proc.pid}, 端口: {port})")
            return "idle"

    print(f"⚠️ {name} 已启动 (PID: {proc.pid})，健康检查未通过")
    return "not_ready"


def create_worker(
    name: str,
    engine: str,
    role: str,
    worker_id_override: Optional[str] = None,
    cli_profile: str = "codex",
    cli_cmd: str = "",
    cli_args: str = "",
    cli_timeout: int = 0,
    workspace_override: str = "",
    deerflow_update_runtime: bool = False,
    external_upstream_url: str = "",
    external_upstream_port: int = 0,
    external_timeout: int = 0,
    external_poll_interval: float = 2.0,
) -> dict:
    valid_engines = ("openclaw", "hermes", "deerflow", "cli", "external", "stub")
    if engine not in valid_engines:
        raise ValueError(f"未知引擎: {engine}，支持: {', '.join(valid_engines)}")

    worker_id = worker_id_override or pinyin(name)
    print(f"🔍 检查 {engine} 运行环境...")

    state = load_state()
    check_duplicate(state, name, worker_id, engine)

    normalized_external_upstream = normalize_external_upstream_url(
        external_upstream_url,
        port=external_upstream_port,
    )

    if not check_engine(
        engine,
        cli_profile=cli_profile,
        cli_cmd=cli_cmd,
        external_upstream_url=normalized_external_upstream,
    ):
        raise RuntimeError("引擎未就绪，无法添加员工。请先安装对应 CLI 再重试。")

    port = alloc_port(state)
    if not port:
        raise RuntimeError("没有可用端口，请先移除一些员工")

    worker_dir = OFFICE_DIR / "workers" / worker_id
    worker_dir.mkdir(parents=True, exist_ok=True)
    (worker_dir / "logs").mkdir(exist_ok=True)
    workspace_dir = normalize_workspace_dir(worker_dir, workspace_override)
    deerflow_runtime = {}
    deerflow_home = ""
    deerflow_config = ""
    if engine == "deerflow":
        should_update_runtime = deerflow_update_runtime or runtime_update_on_add()
        print("🦌 准备 DeerFlow runtime...")
        deerflow_runtime = ensure_deerflow_runtime(update=should_update_runtime)
        deerflow_home = str(
            ensure_worker_home(
                worker_id,
                name,
                role,
                model=DEERFLOW_DEFAULT_MODEL,
            )
        )
        deerflow_config = str(
            write_worker_runtime_config(
                worker_dir,
                workspace_dir,
                worker_id,
                name,
                role,
                model=DEERFLOW_DEFAULT_MODEL,
                reasoning_effort=DEERFLOW_DEFAULT_REASONING_EFFORT,
            )
        )

    # ── 生成 SOUL.md ──────────────────────────────────
    write_soul(
        worker_dir,
        name,
        worker_id,
        role,
        engine,
        port,
        cli_profile=cli_profile if engine == "cli" else "",
        external_upstream_url=normalized_external_upstream if engine == "external" else "",
    )

    # ── 注册 openclaw agent ────────────────────────────
    if engine in ("openclaw", "hermes"):
        register_openclaw_agent(worker_id, worker_dir, name, role)

    # ── 写配置 ────────────────────────────────────────
    config = {
        "worker_id": worker_id,
        "name": name,
        "port": port,
        "role": role,
        "engine": engine,
        "workspace_dir": workspace_dir,
        "status": "onboarding",
        "added_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
    }
    if engine == "cli":
        config.update(
            {
                "cli_profile": cli_profile,
                "cli_cmd": cli_cmd,
                "cli_args": cli_args,
                "cli_timeout": cli_timeout or get_cli_profile(cli_profile)["timeout"],
            }
        )
    if engine == "deerflow":
        config.update(
            {
                "deerflow_runtime_root": deerflow_runtime["runtime_root"],
                "deerflow_runtime_backend_dir": deerflow_runtime["runtime_backend_dir"],
                "deerflow_runtime_python": deerflow_runtime["runtime_python"],
                "deerflow_config": deerflow_config,
                "deerflow_home": deerflow_home,
                "deerflow_agent_name": worker_id,
                "deerflow_model": DEERFLOW_DEFAULT_MODEL,
                "deerflow_reasoning_effort": DEERFLOW_DEFAULT_REASONING_EFFORT,
                "deerflow_recursion_limit": DEERFLOW_DEFAULT_RECURSION_LIMIT,
                "deerflow_timeout": DEERFLOW_DEFAULT_TIMEOUT,
            }
        )
    if engine == "external":
        config.update(
            {
                "external_upstream_url": normalized_external_upstream,
                "external_timeout": external_timeout or ENGINE_TIMEOUTS["external"],
                "external_poll_interval": external_poll_interval or 2.0,
                "external_mode": "bridge",
            }
        )
    with open(worker_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # ── 更新 state ─────────────────────────────────────
    state["workers"][worker_id] = {
        "name": name,
        "port": port,
        "role": role,
        "engine": engine,
        "workspace_dir": workspace_dir,
        "status": "onboarding",
        "config_path": str(worker_dir / "config.json"),
        "soul_path": str(worker_dir / "SOUL.md"),
        "added_at": config["added_at"],
        "last_active": None
    }
    if engine == "cli":
        state["workers"][worker_id]["cli_profile"] = cli_profile
    if engine == "deerflow":
        state["workers"][worker_id]["deerflow_home"] = deerflow_home
    if engine == "external":
        state["workers"][worker_id]["external_upstream_url"] = normalized_external_upstream
    alloc_port_commit(state, port)
    save_state(state)
    print("✅ 状态中心已更新")

    # ── 启动 worker ────────────────────────────────────
    status = start_worker(
        port,
        worker_id,
        name,
        role,
        engine,
        worker_dir,
        workspace_dir,
        cli_profile=cli_profile,
        cli_cmd=cli_cmd,
        cli_args=cli_args,
        cli_timeout=cli_timeout or get_cli_profile(cli_profile)["timeout"] if engine == "cli" else 0,
        deerflow_runtime_python=config.get("deerflow_runtime_python", ""),
        deerflow_config=config.get("deerflow_config", ""),
        deerflow_home=config.get("deerflow_home", ""),
        deerflow_agent_name=config.get("deerflow_agent_name", worker_id),
        deerflow_model=config.get("deerflow_model", DEERFLOW_DEFAULT_MODEL),
        deerflow_reasoning_effort=config.get("deerflow_reasoning_effort", DEERFLOW_DEFAULT_REASONING_EFFORT),
        deerflow_recursion_limit=config.get("deerflow_recursion_limit", DEERFLOW_DEFAULT_RECURSION_LIMIT),
        deerflow_timeout=config.get("deerflow_timeout", DEERFLOW_DEFAULT_TIMEOUT),
        external_upstream_url=config.get("external_upstream_url", ""),
        external_poll_interval=config.get("external_poll_interval", 2.0),
        external_timeout=config.get("external_timeout", ENGINE_TIMEOUTS["external"]),
    )

    # ── 更新状态 ──────────────────────────────────────
    state["workers"][worker_id]["status"] = status
    save_state(state)

    return {
        "ok": True,
        "worker_id": worker_id,
        "name": name,
        "engine": engine,
        "role": role,
        "port": port,
        "status": status,
        "worker_dir": str(worker_dir),
        "workspace_dir": workspace_dir,
        "cli_profile": cli_profile if engine == "cli" else "",
        "deerflow_runtime_root": config.get("deerflow_runtime_root", ""),
        "external_upstream_url": config.get("external_upstream_url", ""),
    }


# ════════════════════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Add an Agent Office worker")
    parser.add_argument("name", nargs="?", help="员工名字")
    parser.add_argument("engine", nargs="?", help="引擎: openclaw | hermes | deerflow | cli | external | stub")
    parser.add_argument("role", nargs="?", help="职责关键词")
    parser.add_argument("--worker-id", default="", help="手动指定 worker_id")
    parser.add_argument("--workspace", default="", help="真实执行工作目录；默认使用员工目录")
    parser.add_argument("--cli-profile", default="codex", help="cli 引擎 profile")
    parser.add_argument("--cli-cmd", default="", help="cli 引擎命令覆盖，例如 'codex exec'")
    parser.add_argument("--cli-args", default="", help="追加给 cli 引擎的参数")
    parser.add_argument("--cli-timeout", type=int, default=0, help="cli 引擎超时秒数")
    parser.add_argument("--deerflow-update-runtime", action="store_true", help="添加 deerflow 员工前先更新共享 runtime")
    parser.add_argument("--external-upstream-url", default="", help="external 引擎上游 URL，例如 http://127.0.0.1:18750")
    parser.add_argument("--external-upstream-port", type=int, default=0, help="external 引擎上游端口，例如 18750")
    parser.add_argument("--external-timeout", type=int, default=0, help="external 引擎整单超时秒数")
    parser.add_argument("--external-poll-interval", type=float, default=2.0, help="external 引擎轮询间隔秒数")
    parser.add_argument("--list-cli-profiles", action="store_true", help="列出内置 CLI profiles")
    args = parser.parse_args()

    if args.list_cli_profiles:
        print("可用 CLI profiles:")
        for profile_id in sorted(CLI_PROFILES):
            print(f"- {profile_id}: {CLI_PROFILES[profile_id]['display_name']}")
        return

    if not args.name or not args.engine or not args.role:
        print("❌ 用法: python3 add_worker.py <名字> <引擎> <角色> [可选参数]")
        print("   引擎: openclaw | hermes | deerflow | cli | external | stub")
        print("   示例: python3 add_worker.py 小龙 openclaw research")
        print("         python3 add_worker.py 小D deerflow complex")
        print("         python3 add_worker.py 小克 cli code --cli-profile claude-code")
        print("         python3 add_worker.py 外挂小龙 external general --external-upstream-port 18750")
        sys.exit(1)

    try:
        result = create_worker(
            args.name,
            args.engine,
            args.role,
            worker_id_override=args.worker_id or None,
            cli_profile=args.cli_profile,
            cli_cmd=args.cli_cmd,
            cli_args=args.cli_args,
            cli_timeout=args.cli_timeout,
            workspace_override=args.workspace,
            deerflow_update_runtime=args.deerflow_update_runtime,
            external_upstream_url=args.external_upstream_url,
            external_upstream_port=args.external_upstream_port,
            external_timeout=args.external_timeout,
            external_poll_interval=args.external_poll_interval,
        )
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # ── 汇报 ──────────────────────────────────────────
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ {result['name']} 入职完成")
    print(f"   工号: {result['worker_id']}")
    print(f"   引擎: {result['engine']}")
    print(f"   端口: {result['port']}")
    print(f"   职责: {result['role']}")
    print(f"   状态: {result['status']}")
    print(f"   工作目录: {result['workspace_dir']}")
    if result["engine"] == "cli":
        print(f"   CLI Profile: {result.get('cli_profile', 'codex')}")
    if result["engine"] == "deerflow":
        print(f"   DeerFlow Runtime: {result.get('deerflow_runtime_root', '-')}")
    if result["engine"] == "external":
        print(f"   Upstream: {result.get('external_upstream_url', '-')}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    main()
