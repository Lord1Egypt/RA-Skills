import hashlib, random, socket, json, os
import subprocess

def report_event(event_type):
    uid_path = "/root/.openclaw/workspace/memory/cyber-persona/uid.txt"
    if not os.path.exists(uid_path):
        os.makedirs(os.path.dirname(uid_path), exist_ok=True)
        uid = hashlib.sha256((socket.gethostname()+str(random.random())).encode()).hexdigest()[:16]
        with open(uid_path, 'w') as f:
            f.write(uid)
    else:
        with open(uid_path, 'r') as f:
            uid = f.read().strip()

    # 异步上报事件到 Vercel API
    cmd = f"curl -s -X POST https://cyber-persona.vercel.app/api/event -H 'Content-Type: application/json' -d '{{\"type\":\"{event_type}\",\"uid\":\"{uid}\"}}' &"
    subprocess.Popen(cmd, shell=True)

if __name__ == '__main__':
    # 测试安装事件上报
    report_event('install')
