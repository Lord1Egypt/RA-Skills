#!/usr/bin/env python3
"""
批量跑视频：跑前清Chrome、跑后清Chrome、跑完自动通知
用法: python3 batch_runner.py <account_id> <start_date> <end_date>
"""
import sys, os, subprocess, time, json, logging
sys.path.insert(0, os.path.dirname(__file__))
from config_loader import get_path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

account_id = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]

# 生成日期列表
from datetime import datetime, timedelta
start = datetime.strptime(start_date, '%Y-%m-%d')
end = datetime.strptime(end_date, '%Y-%m-%d')
dates = []
d = start
while d <= end:
    dates.append((d.strftime('%Y-%m-%d'), 'AM'))
    dates.append((d.strftime('%Y-%m-%d'), 'PM'))
    d += timedelta(days=1)

total = len(dates)
ok = fail = 0
start_ts = time.time()

SCRIPT = os.path.join(os.path.dirname(__file__), 'run_and_notify.py')

def cleanup_chrome():
    subprocess.run(['pkill', '-9', '-f', 'Google Chrome'], capture_output=True, timeout=5)

def cleanup_workspace():
    ws = os.path.join(os.path.dirname(__file__), '..', get_path("workspace_dir"))
    if os.path.exists(ws):
        for f in os.listdir(ws):
            fp = os.path.join(ws, f)
            try:
                if os.path.isfile(fp):
                    os.unlink(fp)
                elif os.path.isdir(fp) and f != '__pycache__': 
                    import shutil; shutil.rmtree(fp)
            except: pass

cleanup_chrome()
# 尝试飞书通知（可选）
try:
    from feishu_notify import send_message
    send_message(f"🦞 {account_id}号 批量开始！\n{total}条 ({start_date}→{end_date})")
except (ImportError, Exception):
    logger.info(f"{account_id}号 批量开始 {total}条 {start_date}→{end_date}")

for i, (sd, ap) in enumerate(dates, 1):
    cleanup_chrome()
    logger.info(f"[{i}/{total}] {sd} {ap}")
    
    # 同步调用子进程（不是后台exec）
    r = subprocess.run(
        ['python3', SCRIPT, account_id, '--' + ap.lower(), '--date', sd],
        capture_output=True, text=True, timeout=1200
    )
    
    elapsed = int(time.time() - start_ts)
    code = r.returncode
    
    if code == 0:
        ok += 1
        logger.info(f"✅ [{i}/{total}] {sd} {ap}")
    elif code == 2:
        ok += 1  # 渲染成功，发布失败也算成功
        logger.info(f"⚠️ [{i}/{total}] {sd} {ap} 渲染OK发布失败")
    elif code == 3:
        fail += 1
        logger.warning(f"⛔ [{i}/{total}] {sd} {ap} 素材缺口，跳过继续")
        send_message(f"🦞 {account_id}号 ⛔ {sd} {ap} 素材缺口，跳过，继续下一条")
    else:
        fail += 1
        logger.error(f"❌ [{i}/{total}] {sd} {ap} 失败")
    
    # 每2条报一次进度
    if i % 2 == 0 or i == total:
        send_message(f"🦞 {account_id}号 进度 {i}/{total}\n✅ {ok} ❌ {fail} ⏱ {elapsed//60}分")
    
    cleanup_chrome()
    cleanup_workspace()

elapsed_t = int(time.time() - start_ts)
send_message(f"🦞 {account_id}号 跑完！\n✅ {ok}成功 ❌ {fail}失败 共{total}条\n⏱ {elapsed_t//60}分")
