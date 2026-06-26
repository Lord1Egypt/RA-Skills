import shutil, pathlib, os
BACKUP_DIR = pathlib.Path('/root/.openclaw/workspace/backups')
CONFIG = pathlib.Path('/root/.openclaw/openclaw.json')

def run_restore():
    # Tìm backup mới nhất
    backups = sorted([b for b in BACKUP_DIR.iterdir() if b.is_dir()], reverse=True)
    if not backups: return
    latest = backups[0]
    shutil.copy2(latest / 'openclaw.json', CONFIG)
    print(f"Restored from {latest}")
    os.system('openclaw gateway restart')

if __name__ == "__main__": run_restore()
