# -*- coding: utf-8 -*-
"""每日金融日报一键生成"""
import sys
sys.path.insert(0, r"C:\Users\qu669\.openclaw\workspace-yoyo")
sys.stdout.reconfigure(encoding='utf-8')
import os, datetime, subprocess, logging
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(config.LOG_FILE, encoding="utf-8"), logging.StreamHandler(sys.stdout)])
log = logging.getLogger(__name__)

log.info(f"{'='*50}")
log.info(f"   每日金融日报生成  日期: {config.REPORT_DATE}")
log.info(f"{'='*50}")

scripts = [
    ("[Step 1/4] 📥 数据采集（市场+政策+企业+汇总）", "collect-market-data/scripts/run_data_collection.py"),
    ("[Step 2/4] 📄 Word 日报", "generate-word-report/scripts/generate_word.py"),
    ("[Step 3/4] 📊 PPT 简报", "generate-ppt-report/scripts/generate_ppt.py"),
    ("[Step 4/4] 📧 发送邮件", "send-email-to/scripts/send_email_to.py"),
]

for label, rel_path in scripts:
    script = os.path.join(config.SKILLS_BASE, rel_path)
    log.info(f"\n{label}...")
    if not os.path.exists(script):
        log.error(f"❌ 脚本不存在: {script}"); continue
    result = subprocess.run([config.PYTHON, script])
    if result.returncode != 0:
        log.warning(f"   ⚠️ 返回码 {result.returncode}")

log.info(f"\n{'='*50}")
log.info(f"✅ 流程完成！  日期: {config.REPORT_DATE}")
if os.path.exists(config.OUTPUT_DIR):
    for f in os.listdir(config.OUTPUT_DIR):
        if f.endswith(('.docx', '.pptx', '.json')):
            size = os.path.getsize(os.path.join(config.OUTPUT_DIR, f))
            log.info(f"   📎 {f} ({size:,} bytes)")