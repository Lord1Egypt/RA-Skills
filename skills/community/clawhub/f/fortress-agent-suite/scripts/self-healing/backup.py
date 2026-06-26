import shutil, datetime, pathlib
BACKUP_DIR = pathlib.Path('/root/.openclaw/workspace/backups')
CONFIG = pathlib.Path('/root/.openclaw/openclaw.json')
TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def run_backup():
    dest = BACKUP_DIR / f"config_{TIMESTAMP}"
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CONFIG, dest / 'openclaw.json')
    # Backup thêm agents config
    agents_dir = pathlib.Path('/root/.openclaw/agents')
    if agents_dir.exists():
        shutil.copytree(agents_dir, dest / 'agents', dirs_exist_ok=True)
    print(f"Backup created at {dest}")

if __name__ == "__main__": run_backup()
