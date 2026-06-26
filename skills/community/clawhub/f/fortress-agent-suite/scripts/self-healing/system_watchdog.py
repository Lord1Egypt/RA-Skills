import shutil, psutil, os, subprocess

def check_system():
    # Disk space check (thấp hơn 500MB thì dọn log)
    total, used, free = shutil.disk_usage("/")
    if free < 500 * 1024 * 1024:
        os.system('find /root/.openclaw/logs -name "*.log" -mtime +7 -delete')

    # Memory check (nếu swap đầy thì dọn rác)
    if psutil.swap_memory().percent > 90:
        os.system('sync; echo 3 > /proc/sys/vm/drop_caches')

if __name__ == "__main__": check_system()
