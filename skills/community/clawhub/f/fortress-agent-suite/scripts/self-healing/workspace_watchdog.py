import subprocess, os, pathlib

WORKSPACE = pathlib.Path('/root/.openclaw/workspace')

def check_integrity():
    # Kiểm tra git status
    if (WORKSPACE / '.git').exists():
        status = subprocess.check_output(['git', '-C', str(WORKSPACE), 'status', '--porcelain']).decode()
        if status:
            # If there are uncommitted changes, auto-commit them (backup mode) / Nếu có thay đổi chưa commit, tự động commit (backup kiểu git)
            os.system(f"git -C {WORKSPACE} add . && git -C {WORKSPACE} commit -m 'Auto-backup: {os.popen('date').read().strip()}'")

    # Kiểm tra crontab
    cron = subprocess.check_output(['crontab', '-l']).decode()
    required = ["backup.py", "health_check.py", "system_watchdog.py"]
    for r in required:
        if r not in cron:
            os.system(f"crontab -l | {{ cat; echo '*/30 * * * * /root/.openclaw/.venv/bin/python /root/.openclaw/scripts/self-healing/{r}'; }} | crontab -")

if __name__ == "__main__": check_integrity()
