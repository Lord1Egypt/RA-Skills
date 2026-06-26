#!/usr/bin/env python3
"""
单条视频跑封装：跑完自动飞书通知，日志标准输出
用法: python3 run_and_notify.py <account_id> [--am|--pm] [--date YYYY-MM-DD]
"""
import sys, os, json, argparse, logging
sys.path.insert(0, os.path.dirname(__file__))
from production_run import run_pipeline
from feishu_notify import send_message

# 输出到stdout让exec能捕获
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('account_id')
parser.add_argument('--am', action='store_true')
parser.add_argument('--pm', action='store_true')
parser.add_argument('--date', default=None)
args = parser.parse_args()

ap = 'AM' if args.am else 'PM'
logger.info(f"▶️ 开始 {args.account_id}号 {args.date} {ap}")

try:
    result = run_pipeline(args.account_id, am_pm=ap, schedule_date=args.date)
    success = result.get('success', False)
    errors = result.get('errors', [])
    
    if success:
        msg = f"✅ {args.account_id}号 {args.date} {ap} 完成"
        video = result.get('video_path', '')
        if video:
            fname = os.path.basename(str(video))
            msg += f"\n📹 {fname}"
        logger.info(msg)
        send_message(msg)
        sys.exit(0)
    else:
        # 检查视频是否存了但发布失败
        outdir = f"output/{args.account_id}"
        has_video = False
        if os.path.exists(outdir):
            date_part = args.date[5:].replace('-', '') if args.date else ''
            has_video = any(f.startswith(date_part[:4]) for f in os.listdir(outdir))
        
        if has_video and any("M6" in str(e) or "Publish" in str(e) or "Metricool" in str(e) or "timeout" in str(e).lower() for e in errors):
            msg = f"⚠️ {args.account_id}号 {args.date} {ap} 渲染成功，发布失败（Metricool超时）"
            logger.info(msg)
            send_message(msg)
            sys.exit(2)  # 2 = 渲染成功发布失败
        elif any("素材缺口" in str(e) or "MATERIAL GAP" in str(e) for e in errors):
            msg = f"⛔ {args.account_id}号 {args.date} {ap} 素材缺口\n{errors[:2]}"
            logger.warning(msg)
            send_message(msg)
            sys.exit(3)  # 3 = 素材缺口
        else:
            msg = f"❌ {args.account_id}号 {args.date} {ap} 失败\n{errors[:2]}"
            logger.error(msg)
            send_message(msg)
            sys.exit(1)
except Exception as e:
    msg = f"💥 {args.account_id}号 {args.date} {ap} 异常: {str(e)[:80]}"
    logger.error(msg)
    send_message(msg)
    sys.exit(1)
