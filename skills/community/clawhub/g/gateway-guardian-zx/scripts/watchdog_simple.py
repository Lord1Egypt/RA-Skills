# -*- coding: utf-8 -*-
"""
OpenClaw Gateway Guardian / OpenClaw 看门狗
=========================================
自动监控 OpenClaw Gateway 状态，宕机时自动重启，支持配置守护和模型故障转移。

Features:
- Auto-check Gateway status (every 15 seconds)
- Auto-restart after 30s downtime (max 3 retries)
- Config guardian - monitor config changes, auto-backup
- Model failover support - auto-switch to backup model
- Feishu/WeChat notifications
- Auto-start on boot (Windows Task Scheduler)
"""

import os
import sys
import json
import time
import hashlib
import socket
import subprocess
import logging
import base64
import urllib.request
import urllib.error
import threading
from datetime import datetime
from pathlib import Path

# ===== Configuration =====
USERPROFILE = os.environ.get('USERPROFILE', os.path.expanduser('~'))
APPDATA = os.environ.get('APPDATA', os.path.join(USERPROFILE, 'AppData', 'Roaming'))

DEFAULT_OPENCLAW_DATA = os.path.join(USERPROFILE, '.openclaw')
DEFAULT_OPENCLAW_EXE = os.path.join(APPDATA, 'npm', 'openclaw.cmd')
# ================================

# Setup logging
LOG_DIR = Path(DEFAULT_OPENCLAW_DATA) / "watchdog" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"guardian_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Guardian')

# Load config
CONFIG_PATH = Path(__file__).parent / 'config.json'
CONFIG = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        CONFIG = json.load(f)

# Settings
openclaw_config = CONFIG.get('openclaw', {})
OPENCLAW_EXE = openclaw_config.get('exePath', DEFAULT_OPENCLAW_EXE)
OPENCLAW_DATA = openclaw_config.get('dataDir', DEFAULT_OPENCLAW_DATA)
GATEWAY_PORT = openclaw_config.get('gatewayPort', 18789)

watchdog_config = CONFIG.get('watchdog', {})
CHECK_INTERVAL = watchdog_config.get('checkIntervalMs', 15000) // 1000
MAX_DOWNTIME = watchdog_config.get('maxDowntimeMs', 30000) // 1000
MAX_RETRIES = watchdog_config.get('maxRetries', 3)
STOP_FLAG = Path(watchdog_config.get('stopFlagPath', os.path.join(DEFAULT_OPENCLAW_DATA, 'stop.flag')))
LOG_DIR = Path(watchdog_config.get('logDir', os.path.join(DEFAULT_OPENCLAW_DATA, 'watchdog', 'logs')))

# Config Guardian Settings
guardian_config = CONFIG.get('configGuardian', {})
ENABLE_CONFIG_GUARDIAN = guardian_config.get('enabled', True)
CONFIG_CHECK_INTERVAL = guardian_config.get('checkIntervalSec', 60)
CONFIG_CHANGE_ALERT = guardian_config.get('alertOnChange', True)

# Model Failover Settings
model_config = CONFIG.get('modelFailover', {})
ENABLE_MODEL_FAILOVER = model_config.get('enabled', False)
PRIMARY_MODEL = model_config.get('primaryModel', '')
FALLBACK_MODEL = model_config.get('fallbackModel', '')

BACKUP_DIR = Path(DEFAULT_OPENCLAW_DATA) / "watchdog" / "backup"

feishu_config = CONFIG.get('feishu', {})
FEISHU_WEBHOOK = feishu_config.get('webhookUrl', '')
if FEISHU_WEBHOOK and 'YOUR_WEBHOOK' in FEISHU_WEBHOOK:
    FEISHU_WEBHOOK = ''

# State
crash_count = 0
downtime_start = None
running = True
last_config_hash = None
config_guardian_running = True


def compute_hash(filepath):
    """Compute SHA256 hash of file"""
    h = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None


def backup_config():
    """Backup openclaw config"""
    try:
        config_file = Path(OPENCLAW_DATA) / "openclaw.json"
        if not config_file.exists():
            return None
        
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'rb') as f:
            data = f.read()
        
        file_hash = hashlib.sha256(data).hexdigest()
        
        backup_info = {
            'timestamp': datetime.now().isoformat(),
            'hash': file_hash,
            'data': base64.b64encode(data).decode('utf-8')
        }
        
        backup_file = BACKUP_DIR / f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w') as f:
            json.dump(backup_info, f)
        
        logger.info(f"✅ Config backed up: {backup_file}")
        
        backups = sorted(BACKUP_DIR.glob('config_*.json'), key=lambda x: x.stat().st_mtime, reverse=True)
        for old in backups[5:]:
            old.unlink()
        
        return backup_file
    except Exception as e:
        logger.error(f"❌ Backup failed: {e}")
        return None


def restore_config():
    """Restore config from latest backup"""
    try:
        backups = sorted(BACKUP_DIR.glob('config_*.json'), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not backups:
            logger.warning("⚠️ No backups found")
            return False
        
        with open(backups[0], 'r') as f:
            backup = json.load(f)
        
        data = base64.b64decode(backup['data'])
        current_hash = hashlib.sha256(data).hexdigest()
        
        if current_hash != backup['hash']:
            logger.error("❌ Hash verification failed!")
            return False
        
        config_file = Path(OPENCLAW_DATA) / "openclaw.json"
        with open(config_file, 'wb') as f:
            f.write(data)
        
        logger.info(f"✅ Config restored from: {backups[0]}")
        return True
    except Exception as e:
        logger.error(f"❌ Restore failed: {e}")
        return False


def check_gateway():
    """Check if gateway port is reachable"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('127.0.0.1', GATEWAY_PORT))
        sock.close()
        return result == 0
    except:
        return False


def check_port_in_use(port):
    """Check if a port is in use"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False


def kill_process_on_port(port):
    """Kill process using the specified port"""
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.strip().split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    logger.warning(f"⚠️ Killing process {pid} on port {port}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    time.sleep(2)
                    return True
        return False
    except Exception as e:
        logger.error(f"❌ Failed to kill process: {e}")
        return False


def check_stop_flag():
    """Check if stop flag exists"""
    return STOP_FLAG.exists()


def start_openclaw():
    """Start OpenClaw gateway"""
    try:
        logger.info("🚀 Starting OpenClaw...")
        
        # Kill existing process on port
        if check_port_in_use(GATEWAY_PORT):
            kill_process_on_port(GATEWAY_PORT)
        
        proc = subprocess.Popen(
            ["openclaw", "gateway", "start"],
            cwd=OPENCLAW_DATA,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            shell=True
        )
        
        logger.info(f"📍 Started OpenClaw with PID: {proc.pid}")
        
        # Wait for startup
        time.sleep(5)
        
        if check_gateway():
            logger.info("✅ OpenClaw started successfully!")
            return True
        else:
            logger.error("❌ OpenClaw failed to start")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to start OpenClaw: {e}")
        return False


def send_feishu_notification(title, content, color="red"):
    """Send notification to Feishu"""
    if not FEISHU_WEBHOOK:
        logger.info(f"📱 Notification: {title} - {content}")
        return False
    
    try:
        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": title},
                    "template": color
                },
                "elements": [
                    {"tag": "div", "text": {"tag": "plain_text", "content": content}}
                ]
            }
        }
        
        req = urllib.request.Request(
            FEISHU_WEBHOOK,
            data=json.dumps(card).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except Exception as e:
        logger.error(f"❌ Feishu notification failed: {e}")
        return False


def get_recent_errors():
    """Get recent error logs"""
    try:
        log_file = Path(DEFAULT_OPENCLAW_DATA).parent / ".openclaw" / "logs" / "openclaw.log"
        if not log_file.exists():
            return "No log file found"
        
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        errors = [l for l in lines[-100:] if 'error' in l.lower() or 'exception' in l.lower()]
        sanitized = ''.join(c for c in ''.join(errors[-50:]) if ord(c) >= 32 or c in '\n\r\t')
        
        if len(sanitized) > 5000:
            sanitized = sanitized[:5000] + "\n... [truncated]"
        
        return sanitized or "No errors found"
    except Exception as e:
        return f"Failed to read logs: {e}"


def switch_to_fallback_model():
    """Switch to fallback model in config"""
    try:
        config_file = Path(OPENCLAW_DATA) / "openclaw.json"
        if not config_file.exists():
            logger.error("❌ Config file not found")
            return False
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Try to switch model
        if 'agents' in config and 'defaults' in config['agents']:
            if 'model' in config['agents']['defaults']:
                current = config['agents']['defaults']['model'].get('primary', '')
                logger.info(f"🔄 Switching model: {current} -> {FALLBACK_MODEL}")
                config['agents']['defaults']['model']['primary'] = FALLBACK_MODEL
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                
                logger.info(f"✅ Model switched to: {FALLBACK_MODEL}")
                send_feishu_notification(
                    "🔄 模型已切换",
                    f"主模型: {current}\n备用模型: {FALLBACK_MODEL}",
                    "blue"
                )
                return True
        
        return False
    except Exception as e:
        logger.error(f"❌ Model switch failed: {e}")
        return False


def config_guardian_worker():
    """Background worker to monitor config changes"""
    global last_config_hash, config_guardian_running
    
    config_file = Path(OPENCLAW_DATA) / "openclaw.json"
    if not config_file.exists():
        return
    
    # Initial hash
    last_config_hash = compute_hash(config_file)
    
    while config_guardian_running and running:
        try:
            time.sleep(CONFIG_CHECK_INTERVAL)
            
            current_hash = compute_hash(config_file)
            if current_hash and current_hash != last_config_hash:
                logger.warning(f"⚠️ Config changed! Hash: {current_hash[:16]}...")
                
                if CONFIG_CHANGE_ALERT:
                    send_feishu_notification(
                        "⚠️ 配置已更改",
                        f"检测到配置文件变更\n新Hash: {current_hash[:16]}...\n自动备份已创建",
                        "orange"
                    )
                
                # Auto backup on change
                backup_config()
                last_config_hash = current_hash
                
        except Exception as e:
            logger.error(f"❌ Config guardian error: {e}")


def recover():
    """Execute recovery"""
    global crash_count
    
    if check_stop_flag():
        logger.warning("⏸️ Stop flag detected, skipping recovery")
        return False
    
    logger.info("🔧 Starting recovery...")
    
    # Backup current config first
    backup_config()
    
    # Restore from backup
    restore_config()
    
    # Try model failover if enabled
    if ENABLE_MODEL_FAILOVER and FALLBACK_MODEL:
        logger.info("🔄 Attempting model failover...")
        switch_to_fallback_model()
    
    # Start OpenClaw
    if start_openclaw():
        crash_count = 0
        
        if STOP_FLAG.exists():
            STOP_FLAG.unlink()
        
        send_feishu_notification(
            "✅ OpenClaw 已恢复",
            f"重启时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n当前状态: 正常",
            "green"
        )
        
        return True
    else:
        return False


def main():
    global downtime_start, crash_count, running
    
    logger.info("=" * 50)
    logger.info("🛡️ OpenClaw Gateway Guardian Started")
    logger.info(f"   Gateway Port: {GATEWAY_PORT}")
    logger.info(f"   Check Interval: {CHECK_INTERVAL}s")
    logger.info(f"   Max Downtime: {MAX_DOWNTIME}s")
    logger.info(f"   Max Retries: {MAX_RETRIES}")
    logger.info(f"   Config Guardian: {'ON' if ENABLE_CONFIG_GUARDIAN else 'OFF'}")
    logger.info(f"   Model Failover: {'ON' if ENABLE_MODEL_FAILOVER else 'OFF'}")
    logger.info("=" * 50)
    
    # Start config guardian thread
    config_guardian_thread = None
    if ENABLE_CONFIG_GUARDIAN:
        config_guardian_thread = threading.Thread(target=config_guardian_worker, daemon=True)
        config_guardian_thread.start()
        logger.info("🛡️ Config Guardian started")
    
    # Initial backup
    backup_config()
    
    while running:
        try:
            gateway_ok = check_gateway()
            
            if not gateway_ok:
                if downtime_start is None:
                    downtime_start = time.time()
                    logger.warning("🔴 Gateway is DOWN!")
                
                downtime = time.time() - downtime_start
                
                if downtime >= MAX_DOWNTIME:
                    logger.error(f"⏰ Downtime exceeded {MAX_DOWNTIME}s, initiating recovery")
                    
                    if crash_count < MAX_RETRIES:
                        crash_count += 1
                        logger.info(f"🔄 Recovery attempt {crash_count}/{MAX_RETRIES}")
                        
                        if recover():
                            downtime_start = None
                        else:
                            time.sleep(5)
                    else:
                        logger.critical("❌ Max retries exceeded!")
                        
                        errors = get_recent_errors()
                        send_feishu_notification(
                            "🚨 OpenClaw 需要人工介入",
                            f"连续崩溃次数: {crash_count} 次\n错误摘要: {errors[:500]}\n建议: 检查日志",
                            "red"
                        )
                        
                        downtime_start = None
                        time.sleep(60)
            else:
                if downtime_start is not None:
                    logger.info("🟢 Gateway recovered")
                    downtime_start = None
                crash_count = 0
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("👋 Watchdog stopped by user")
            running = False
        except Exception as e:
            logger.error(f"❌ Watchdog error: {e}")
            time.sleep(CHECK_INTERVAL)
    
    config_guardian_running = False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'status':
            status = "UP" if check_gateway() else "DOWN"
            print(f"Gateway Port {GATEWAY_PORT}: {status}")
            sys.exit(0)
        elif sys.argv[1] == 'backup':
            result = backup_config()
            print(f"✅ Backup created: {result}" if result else "❌ Backup failed")
            sys.exit(0)
        elif sys.argv[1] == 'restore':
            result = restore_config()
            print("✅ Restored" if result else "❌ Restore failed")
            sys.exit(0)
    
    main()
