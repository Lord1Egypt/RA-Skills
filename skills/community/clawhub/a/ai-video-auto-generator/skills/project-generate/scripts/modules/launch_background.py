"""
后台启动器 — 通过 PowerShell .NET API 启动流水线，不弹任何窗口。
进程使用 UseShellExecute 启动，完全脱离父进程，不会被 WorkBuddy 杀死。

原理: PowerShell 的 System.Diagnostics.ProcessStartInfo 支持 UseShellExecute=$true，
这样子进程通过 Windows Shell 启动，不绑定到父进程的 job object。配合 WindowStyle=Hidden
和 CreateNoWindow=$true 实现无窗口运行。stdout 通过 cmd.exe /c 重定向到 pipeline.log。

用法:
  python scripts/modules/launch_background.py <项目路径> <子命令> [参数...]

示例:
  python scripts/modules/launch_background.py D:/Projects/my_drama auto
  python scripts/modules/launch_background.py . generate-scenes
  python scripts/modules/launch_background.py . poll
"""
import subprocess
import sys
import os


def launch_background(project: str, *args: str) -> int:
    """启动 detached 进程。args 是传给 project_generate.py 的子命令和参数。"""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pg = os.path.join(script_dir, "scripts", "project_generate.py")
    if not os.path.isfile(pg):
        pg = os.path.join(script_dir, "project_generate.py")
    if not os.path.isfile(pg):
        print(f"[ERROR] 未找到 project_generate.py", flush=True)
        return 1

    py = os.path.abspath(sys.executable)
    proj_abs = os.path.abspath(project)
    log = os.path.join(proj_abs, "pipeline.log")

    # 使用 PowerShell 的 .NET Process API 启动
    # UseShellExecute=$true → Windows Shell 执行，不绑定 job object
    # WindowStyle=Hidden → 不显示窗口
    # 通过 cmd.exe /c 重定向 stdout 到日志（PowerShell 的 -RedirectStandardOutput 不支持中文路径）
    ps_cmd = (
        f"[System.Diagnostics.ProcessStartInfo]$psi=New-Object System.Diagnostics.ProcessStartInfo;"
        f'$psi.FileName="cmd.exe";'
        f'$psi.Arguments=\'/c ""{py}" -u "{pg}" --project "{proj_abs}" {" ".join(args)} > "{log}" 2>&1"\';'
        f'$psi.WindowStyle=[System.Diagnostics.ProcessWindowStyle]::Hidden;'
        f'$psi.UseShellExecute=$true;'
        f'$psi.CreateNoWindow=$true;'
        f'$p=[System.Diagnostics.Process]::Start($psi);'
        f'Write-Host "PID=$($p.Id)"'
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps_cmd],
        capture_output=True, timeout=15,
        encoding="gbk", errors="replace",
    )
    print(result.stdout.strip(), f" log={log}", flush=True)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"用法: {sys.argv[0]} <项目路径> <子命令> [参数...]")
        print(f"示例: {sys.argv[0]} . auto")
        sys.exit(1)
    sys.exit(launch_background(sys.argv[1], *sys.argv[2:]))
