#!/usr/bin/env python3
"""execute_command — 自举入口 + 跨平台命令执行"""
import sys, os, json, subprocess
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *

SCRIPTS_DIR = Path(__file__).parent


def execute_system_command(command, timeout=120, cwd=None, env_vars=None):
    """执行系统命令"""
    if not command or not command.strip():
        output_error("命令不能为空", EXIT_PARAM_ERROR)

    work_dir = None
    if cwd:
        work_dir = resolve_path(str(cwd))
        if not work_dir.is_dir():
            output_error(f"工作目录不存在: {work_dir}", EXIT_EXEC_ERROR)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if env_vars:
        if isinstance(env_vars, dict):
            env.update(env_vars)
        elif isinstance(env_vars, list):
            for item in env_vars:
                if "=" in item:
                    k, v = item.split("=", 1)
                    env[k.strip()] = v.strip()

    is_windows = sys.platform == "win32"

    if is_windows:
        # Windows: PowerShell
        encoding_setup = (
            "[Console]::InputEncoding = [Console]::OutputEncoding = "
            "[System.Text.Encoding]::UTF8; "
            "$OutputEncoding = [System.Text.Encoding]::UTF8; "
        )
        full_cmd = encoding_setup + command
        cmd = ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", full_cmd]
    else:
        # macOS/Linux: sh
        cmd = ["/bin/sh", "-c", command]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
            cwd=str(work_dir) if work_dir else None,
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
    except subprocess.TimeoutExpired:
        output_error(f"命令超时 ({timeout}s)", EXIT_EXEC_ERROR)
    except FileNotFoundError:
        output_error("Shell 未找到", EXIT_UNSUPPORTED_OS)
    except Exception as e:
        output_error(str(e), EXIT_EXEC_ERROR)

    # 截断过长输出
    max_output = 50000
    truncated_stdout = stdout[:max_output]
    truncated_stderr = stderr[:max_output]

    output_ok({
        "stdout": truncated_stdout,
        "stderr": truncated_stderr,
        "exit_code": result.returncode,
        "truncated": len(stdout) > max_output or len(stderr) > max_output,
        "command": command,
        "cwd": str(work_dir) if work_dir else os.getcwd(),
    })


def execute_builtin_script(script_name, script_params=None, timeout=60):
    """执行内置工具脚本"""
    script_path = SCRIPTS_DIR / f"{script_name}.py"
    if not script_path.exists():
        available = sorted(p.stem for p in SCRIPTS_DIR.glob("*.py") if p.stem != "common" and p.stem != "execute_command")
        output_error(
            f"脚本不存在: {script_name}.py\n可用脚本: {available}",
            EXIT_PARAM_ERROR,
        )

    cmd = [sys.executable, str(script_path)]
    if script_params:
        if isinstance(script_params, dict):
            cmd.append(json.dumps(script_params, ensure_ascii=False))
        else:
            cmd.append(str(script_params))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
    except subprocess.TimeoutExpired:
        output_error(f"脚本超时 ({timeout}s): {script_name}", EXIT_EXEC_ERROR)
    except Exception as e:
        output_error(f"执行脚本失败: {e}", EXIT_EXEC_ERROR)

    # 尝试解析脚本 JSON 输出
    data = None
    if stdout:
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            data = stdout

    output_ok({
        "script": script_name,
        "stdout": data if data else stdout,
        "stderr": stderr,
        "exit_code": result.returncode,
    })


def open_url(url):
    """跨平台打开 URL 或文件"""
    import webbrowser
    if not url:
        output_error("URL 不能为空", EXIT_PARAM_ERROR)

    opened = webbrowser.open(url)
    if opened:
        output_ok({"url": url, "opened": True})
    else:
        output_error(f"无法打开: {url}", EXIT_EXEC_ERROR)


def pipe_scripts(script_chain, shared_params=None, timeout=120):
    """管道串联多个内置脚本"""
    if not isinstance(script_chain, list) or len(script_chain) < 2:
        output_error("pipe 需要至少 2 个脚本名", EXIT_PARAM_ERROR)

    current_input = None
    results = []

    for i, script_name in enumerate(script_chain):
        script_path = SCRIPTS_DIR / f"{script_name}.py"
        if not script_path.exists():
            output_error(f"管道中脚本不存在: {script_name}.py", EXIT_PARAM_ERROR)

        cmd = [sys.executable, str(script_path)]

        # 第一个脚本用 shared_params，后续用上一个脚本的 stdout
        if i == 0 and shared_params:
            cmd.append(json.dumps(shared_params, ensure_ascii=False))
        elif current_input:
            cmd.append(current_input)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
            current_input = (result.stdout or "").strip()
            results.append({
                "script": script_name,
                "exit_code": result.returncode,
                "output_length": len(current_input),
            })
            if result.returncode != 0:
                output_error(
                    f"管道在 {script_name} 失败 (code={result.returncode}): {result.stderr}",
                    EXIT_EXEC_ERROR,
                )
        except subprocess.TimeoutExpired:
            output_error(f"管道在 {script_name} 超时 ({timeout}s)", EXIT_EXEC_ERROR)
        except Exception as e:
            output_error(f"管道执行失败: {e}", EXIT_EXEC_ERROR)

    # 最终结果
    final_data = None
    if current_input:
        try:
            final_data = json.loads(current_input)
        except json.JSONDecodeError:
            final_data = current_input

    output_ok({
        "chain": script_chain,
        "steps": results,
        "final_output": final_data,
    })


def main():
    params = parse_input()

    # 模式分发
    mode = get_param(params, "mode", None)

    if mode == "command":
        # 直接执行系统命令
        command = get_param(params, "command", required=True)
        timeout = get_param(params, "timeout", 120)
        cwd = get_param(params, "cwd")
        env_vars = get_param(params, "env")
        execute_system_command(command, timeout, cwd, env_vars)

    elif mode == "script":
        # 执行内置脚本
        script = get_param(params, "script", required=True)
        script_params = get_param(params, "params")
        timeout = get_param(params, "timeout", 60)
        execute_builtin_script(script, script_params, timeout)

    elif mode == "open":
        # 打开 URL/文件
        url = get_param(params, "url", required=True)
        open_url(url)

    elif mode == "pipe":
        # 管道串联
        chain = get_param(params, "chain", required=True)
        shared_params = get_param(params, "params")
        timeout = get_param(params, "timeout", 120)
        pipe_scripts(chain, shared_params, timeout)

    else:
        # 快捷模式：无 mode 时自动判断
        # --command "xxx" 或 --cmd "xxx" → 执行命令
        if params and ("command" in params or "cmd" in params):
            command = params.get("command") or params.get("cmd")
            execute_system_command(command)
        # --open "url" → 打开
        elif params and "open" in params:
            open_url(params["open"])
        # 其他 → 尝试作为脚本名执行
        else:
            # 兼容: python execute_command.py search_file '{"pattern":"*.py"}'
            if len(sys.argv) > 1 and not sys.argv[1].startswith("{") and not sys.argv[1].startswith("-"):
                script_name = sys.argv[1]
                script_params = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
                execute_builtin_script(script_name, script_params)
            else:
                output_error(
                    "用法:\n"
                    '  --mode command --command "ls -la"\n'
                    '  --mode script --script search_file --params \'{"pattern":"*.py"}\'\n'
                    '  --mode open --url "https://..."\n'
                    '  --mode pipe --chain \'["search_file","search_content"]\'\n'
                    "或快捷: python execute_command.py search_file '{\"pattern\":\"*.py\"}'",
                    EXIT_PARAM_ERROR,
                )


if __name__ == "__main__":
    main()
