#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ezviz Safety Production Inspection Skill
萤石安全生产巡检技能 - 自动智能体管理 + 设备抓图 + AI 分析

Usage:
    python3 safety_production_inspection.py [app_key] [app_secret] [device_serial] [channel_no]

Environment Variables (alternative to command line args):
    EZVIZ_APP_KEY, EZVIZ_APP_SECRET, EZVIZ_DEVICE_SERIAL, EZVIZ_CHANNEL_NO, EZVIZ_SAFETY_TEMPLATE_ID

Credential Priority (from high to low):
    1. Environment variables (EZVIZ_APP_KEY, EZVIZ_APP_SECRET, EZVIZ_DEVICE_SERIAL)
    2. OpenClaw config files (~/.openclaw/config.json, channels.json, etc.)
    3. Command line arguments

Token Management:
    Uses global token cache (shared with other Ezviz skills)
    Cache location: /tmp/ezviz_global_token_cache/
    Token validity: 7 days, auto-refresh 5 minutes before expiry
    Disable cache: export EZVIZ_TOKEN_CACHE=0

Template ID Priority:
    1. Environment variable EZVIZ_SAFETY_TEMPLATE_ID
    2. Config file safetyTemplateId
    3. Default: "f4c255b2929e463d86e9" (安全生产行业通用智能体模板)
"""

import os
import sys
import time
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Add lib directory to path for token_manager import
# lib/ is at the same level as scripts/, so we need to go up one level
script_dir = Path(__file__).parent
base_dir = script_dir.parent  # Go up to skill root
lib_dir = base_dir / "lib"
sys.path.insert(0, str(lib_dir))

from token_manager import get_cached_token

# Default values
DEFAULT_CHANNEL_NO = "1"
DEFAULT_ANALYSIS_TEXT = "请分析这张照片中的安全生产情况，检查是否存在安全隐患"
DEFAULT_TEMPLATE_ID = "e15f061c13f349b1b2a3"  # 安全生产行业通用智能体模板 ID

# Production environment domains (online)
# Note: open.ys7.com is the official Ezviz Open API domain (not AI-related)
# aidialoggw.ys7.com is specifically for intelligent agent analysis
TOKEN_CAPTURE_URL = "https://open.ys7.com/api/lapp/token/get"
CAPTURE_URL = "https://open.ys7.com/api/lapp/device/capture"
AGENT_LIST_URL = "https://open.ys7.com/api/service/open/intelligent/agent/app/list"
AGENT_COPY_URL = "https://open.ys7.com/api/service/open/intelligent/agent/template/copy"
ANALYSIS_URL = "https://aidialoggw.ys7.com/api/service/open/intelligent/agent/engine/agent/anaylsis"
ENV_NAME = "Production Environment (Online)"

# Config file paths for credential fallback
CONFIG_PATHS = [
    Path.home() / ".openclaw" / "config.json",
    Path.home() / ".openclaw" / "gateway" / "config.json",
    Path.home() / ".openclaw" / "channels.json",
]

def get_env_or_arg(env_var, arg_value, default=None):
    """Get value from environment variable or command line argument"""
    return os.getenv(env_var) or arg_value or default

def read_ezviz_config_from_files():
    """
    Read Ezviz credentials from OpenClaw config files.
    Returns (app_key, app_secret, device_serial, template_id) or (None, None, None, None) if not found.
    
    Config format:
    {
        "channels": {
            "ezviz": {
                "appId": "your_app_id",
                "appSecret": "your_app_secret",
                "domain": "https://open.ys7.com",
                "enabled": true,
                "devices": ["dev1", "dev2"],  # Optional: default device list
                "safetyTemplateId": "xxx"     # Optional: safety production template ID
            }
        }
    }
    """
    for config_path in CONFIG_PATHS:
        if not config_path.exists():
            continue
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Try to find ezviz config
            ezviz_config = None
            
            # Check channels.ezviz
            if 'channels' in config and 'ezviz' in config['channels']:
                ezviz_config = config['channels']['ezviz']
            # Check root level ezviz
            elif 'ezviz' in config:
                ezviz_config = config['ezviz']
            
            if ezviz_config:
                app_key = ezviz_config.get('appId') or ezviz_config.get('appKey')
                app_secret = ezviz_config.get('appSecret')
                device_serial = ezviz_config.get('deviceSerial') or ezviz_config.get('devices')
                template_id = ezviz_config.get('safetyTemplateId')
                
                # Convert devices list to comma-separated string if needed
                if isinstance(device_serial, list):
                    device_serial = ','.join(device_serial)
                
                if app_key and app_secret:
                    print(f"[INFO] Loaded credentials from config file: {config_path}")
                    return app_key, app_secret, device_serial, template_id
        except (json.JSONDecodeError, KeyError, IOError) as e:
            # Silently skip invalid config files
            pass
    
    return None, None, None, None

def get_access_token(app_key, app_secret):
    """Get access token using global token manager (with caching)"""
    print("=" * 70)
    print("[Step 1] Getting access token...")
    
    # Use global token manager (handles caching automatically)
    token_result = get_cached_token(app_key, app_secret)
    
    if token_result.get("success"):
        access_token = token_result["access_token"]
        expire_time = token_result["expire_time"]
        expire_str = datetime.fromtimestamp(expire_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
        from_cache = token_result.get("from_cache", False)
        
        if from_cache:
            print(f"[SUCCESS] Using cached token, expires: {expire_str}")
        else:
            print(f"[SUCCESS] Token obtained, expires: {expire_str}")
        
        return access_token
    else:
        error_msg = token_result.get("error", "Unknown error")
        print(f"[ERROR] Failed to get token: {error_msg}")
        return None

def get_agent_list(access_token):
    """Get user's intelligent agent list - prioritize agents with '安全生产' in name"""
    print("=" * 70)
    print("[Step 2] Checking existing intelligent agents...")
    
    params = {
        '_r': '0.6149525825375246',
        'appType': '1',
        'pageStart': '0',
        'pageSize': '100'  # Increased to get more agents
    }
    
    headers = {
        'accessToken': access_token
    }
    
    try:
        response = requests.get(AGENT_LIST_URL, params=params, headers=headers, timeout=30)
        result = response.json()
        
        agents = []
        # Handle both response formats
        if 'data' in result:
            if isinstance(result['data'], dict) and 'appList' in result['data']:
                agents = result['data']['appList']
            elif isinstance(result['data'], list):
                agents = result['data']
        
        if agents:
            print(f"[INFO] Found {len(agents)} agents total")
            
            # Priority 1: Look for agents with '安全生产' in name (REQUIRED for compliance)
            for agent in agents:
                agent_name = agent.get('appName', '')
                if '安全生产' in agent_name:
                    agent_id = agent.get('appId')
                    app_status = agent.get('appStatus', 0)
                    status_text = 'Published' if app_status == 1 else 'Draft'
                    print(f"[INFO] Found agent with '安全生产': {agent_id} ({agent_name}) [{status_text}]")
                    print(f"[SUCCESS] Using existing agent: {agent_id}")
                    return agent_id
            
            # No agent with '安全生产' found - will create new one
            print("[INFO] No agent with '安全生产' found - will create new one from template")
            return None
        else:
            print(f"[ERROR] Unexpected response format: {result}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when getting agent list: {str(e)}")
        return None

def rename_agent(access_token, agent_id, new_name):
    """Rename an intelligent agent"""
    print(f"[INFO] Renaming agent to: {new_name}")
    
    # Agent update endpoint
    update_url = "https://open.ys7.com/api/service/open/intelligent/agent/app/update"
    
    headers = {
        'accessToken': access_token,
        'Content-Type': 'application/json'
    }
    
    data = {
        'appId': agent_id,
        'appName': new_name
    }
    
    try:
        response = requests.post(update_url, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if result.get('code') == '200' or (result.get('meta', {}).get('code') == 200):
            print(f"[SUCCESS] Agent renamed to: {new_name}")
            return True
        else:
            msg = result.get('msg') or result.get('meta', {}).get('message', 'Unknown error')
            print(f"[WARN] Failed to rename agent: {msg}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception when renaming agent: {str(e)}")
        return False

def copy_agent_template(access_token, template_id):
    """Copy agent template to create new agent with '安全生产' in name"""
    print("[INFO] Creating new agent with '安全生产' in name from template...")
    
    headers = {
        'accessToken': access_token
    }
    
    # Generate a unique name with '安全生产'
    timestamp = datetime.now().strftime('%m%d%H%M')
    desired_name = f"安全生产巡检_{timestamp}"
    
    data = {
        'templateId': template_id,
        'appName': desired_name
    }
    
    try:
        response = requests.post(AGENT_COPY_URL, headers=headers, data=data, timeout=60)
        result = response.json()
        
        if 'data' in result:
            new_agent_data = result['data']
            # Handle both string appId and full agent object
            if isinstance(new_agent_data, str):
                new_agent_id = new_agent_data
                actual_name = desired_name
            elif isinstance(new_agent_data, dict):
                new_agent_id = new_agent_data.get('appId')
                actual_name = new_agent_data.get('appName', desired_name)
            else:
                print(f"[ERROR] Unexpected agent data format: {new_agent_data}")
                return None
            
            print(f"[INFO] Agent created: {new_agent_id} (Current name: {actual_name})")
            
            # If name doesn't contain '安全生产', try to rename it
            if '安全生产' not in actual_name:
                print("[INFO] Agent name doesn't contain '安全生产', attempting to rename...")
                if rename_agent(access_token, new_agent_id, desired_name):
                    actual_name = desired_name
                else:
                    print(f"[WARN] Auto-rename not supported by API.")
                    print(f"[ACTION REQUIRED] Please manually rename agent {new_agent_id} to include '安全生产':")
                    print(f"  1. Visit: https://openai.ys7.com/console/aiAgent/aiAgent.html")
                    print(f"  2. Find agent: {new_agent_id}")
                    print(f"  3. Edit name to include '安全生产' (e.g., '安全生产巡检_{timestamp}')")
            
            print(f"[SUCCESS] New agent ready: {new_agent_id} ({actual_name})")
            # Wait for agent to be ready
            print("[INFO] Waiting for agent to initialize (5 seconds)...")
            time.sleep(5)
            return new_agent_id
        else:
            print(f"[ERROR] Failed to create agent: {result.get('msg', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when copying agent template: {str(e)}")
        return None

def manage_intelligent_agent(access_token, template_id):
    """Manage intelligent agent - check existing or create new"""
    print("=" * 70)
    print("[Step 2] Managing intelligent agent...")
    
    # Check if existing agent with '安全生产' exists
    existing_agent_id = get_agent_list(access_token)
    if existing_agent_id:
        return existing_agent_id
    
    # Create new agent from template
    new_agent_id = copy_agent_template(access_token, template_id)
    if new_agent_id:
        print(f"[SUCCESS] Using new agent: {new_agent_id}")
        return new_agent_id
    
    print("[ERROR] Failed to manage intelligent agent")
    return None

def capture_image(access_token, device_serial, channel_no):
    """Capture image from device"""
    print(f"\n[Device] {device_serial} (Channel: {channel_no})")
    
    payload = {
        'accessToken': access_token,
        'deviceSerial': device_serial,
        'channelNo': channel_no
    }
    
    try:
        response = requests.post(CAPTURE_URL, data=payload, timeout=30)
        result = response.json()
        
        if result.get('code') == '200':
            pic_url = result['data']['picUrl']
            print(f"[SUCCESS] Image captured: {pic_url[:50]}...")
            return pic_url
        else:
            msg = result.get('msg', 'Unknown error')
            code = result.get('code', 'Unknown')
            print(f"[ERROR] Failed to capture image: Code {code}, Message: {msg}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when capturing image: {str(e)}")
        return None

def analyze_image(access_token, agent_id, pic_url, analysis_text):
    """Analyze image using intelligent agent"""
    headers = {
        'Content-Type': 'application/json',
        'accessToken': access_token
    }
    
    payload = {
        'appId': agent_id,
        'text': analysis_text,
        'mediaType': 'image',
        'dataType': 'url',
        'data': pic_url
    }
    
    try:
        response = requests.post(ANALYSIS_URL, headers=headers, json=payload, timeout=60)
        result = response.json()
        
        if result.get('meta', {}).get('code') == 200:
            analysis_result = result.get('data', {})
            print("[SUCCESS] Analysis completed!")
            return analysis_result
        else:
            msg = result.get('meta', {}).get('message', 'Unknown error')
            code = result.get('meta', {}).get('code', 'Unknown')
            print(f"[ERROR] Failed to analyze image: Code {code}, Message: {msg}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when analyzing image: {str(e)}")
        return None

def parse_device_list(device_serial_str):
    """Parse device serial string with optional channel numbers"""
    devices = []
    for item in device_serial_str.split(','):
        item = item.strip()
        if ':' in item:
            serial, channel = item.split(':', 1)
            devices.append((serial, channel))
        else:
            devices.append((item, DEFAULT_CHANNEL_NO))
    return devices

def print_user_confirmation():
    """Print user confirmation notice about remote side effects"""
    print("=" * 70)
    print("⚠️  USER CONFIRMATION REQUIRED (用户确认)")
    print("=" * 70)
    print()
    print("This skill will perform the following REMOTE ACTIONS:")
    print("此技能将执行以下远程操作：")
    print()
    print("  1. Query your Ezviz intelligent agent list")
    print("     查询您的萤石智能体列表")
    print()
    print("  2. Create new agent from template (if none exists)")
    print("     如无现有智能体，从模板创建新智能体")
    print()
    print("  3. Capture images from your devices")
    print("     从您的设备抓拍图片")
    print()
    print("  4. Send images to aidialoggw.ys7.com for AI analysis")
    print("     发送图片到萤石 AI 分析端点")
    print()
    print("Data Flow / 数据流:")
    print("  Device → open.ys7.com → aidialoggw.ys7.com → Local output")
    print()
    print("Privacy / 隐私:")
    print("  - Images stored on Ezviz servers (2 hours expiry)")
    print("  - Images sent to aidialoggw.ys7.com for analysis")
    print("  - Token cached in /tmp/ezviz_global_token_cache/ (permissions 600)")
    print()
    print("=" * 70)
    print("Running this skill implies your acceptance of these side effects.")
    print("运行此技能即表示您接受上述远程副作用。")
    print("=" * 70)
    print()

def main():
    # Print user confirmation notice
    print_user_confirmation()
    
    # Parse command line arguments
    app_key = None
    app_secret = None
    device_serial = None
    channel_no = DEFAULT_CHANNEL_NO
    template_id = None
    
    if len(sys.argv) >= 4:
        app_key = sys.argv[1]
        app_secret = sys.argv[2]
        device_serial = sys.argv[3]
        if len(sys.argv) >= 5:
            channel_no = sys.argv[4]
        if len(sys.argv) >= 6:
            template_id = sys.argv[5]
    
    # Get from environment variables if not provided
    if not app_key:
        app_key = os.getenv('EZVIZ_APP_KEY')
    if not app_secret:
        app_secret = os.getenv('EZVIZ_APP_SECRET')
    if not device_serial:
        device_serial = os.getenv('EZVIZ_DEVICE_SERIAL')
    if channel_no == DEFAULT_CHANNEL_NO:
        channel_no = os.getenv('EZVIZ_CHANNEL_NO', DEFAULT_CHANNEL_NO)
    if not template_id:
        template_id = os.getenv('EZVIZ_SAFETY_TEMPLATE_ID')
    
    # Try to read from config files if still not found
    if not app_key or not app_secret or not device_serial:
        config_key, config_secret, config_device, config_template = read_ezviz_config_from_files()
        if config_key and not app_key:
            app_key = config_key
        if config_secret and not app_secret:
            app_secret = config_secret
        if config_device and not device_serial:
            device_serial = config_device
        if config_template and not template_id:
            template_id = config_template
    
    # Use default template ID if still not provided
    if not template_id:
        template_id = DEFAULT_TEMPLATE_ID
        print(f"[INFO] Using default template ID: {template_id}")
    
    # Validate required parameters
    if not all([app_key, app_secret, device_serial]):
        print("Error: Missing required parameters!")
        print("Please provide app_key, app_secret, and device_serial")
        print("\nUsage:")
        print("  python3 safety_production_inspection.py app_key app_secret device_serial [channel_no] [template_id]")
        print("")
        print("  # Environment variables (Priority 1 - Recommended)")
        print("  export EZVIZ_APP_KEY=your_key")
        print("  export EZVIZ_APP_SECRET=your_secret")
        print("  export EZVIZ_DEVICE_SERIAL=dev1,dev2")
        print("  export EZVIZ_SAFETY_TEMPLATE_ID=your_template_id  # Optional")
        print("  python3 safety_production_inspection.py")
        print("")
        print("  # OpenClaw config files (Priority 2)")
        print("  Add to ~/.openclaw/channels.json:")
        print("  {")
        print('    "channels": {')
        print('      "ezviz": {')
        print('        "appId": "your_app_id",')
        print('        "appSecret": "your_app_secret",')
        print('        "domain": "https://open.ys7.com",  # Ezviz Open API (not AI-related)')
        print('        "enabled": true,')
        print('        "safetyTemplateId": "your_template_id"  # Optional: 安全生产行业通用智能体模板 ID')
        print("      }")
        print("    }")
        print("  }")
        sys.exit(1)
    
    # Parse devices
    devices = parse_device_list(device_serial)
    
    # Print header
    print("=" * 70)
    print("Ezviz Safety Production Inspection Skill (萤石安全生产巡检)")
    print("=" * 70)
    print(f"[Time] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] Environment: {ENV_NAME}")
    print(f"[INFO] Template ID: {template_id}")
    print(f"[INFO] Target devices: {len(devices)}")
    for i, (serial, chan) in enumerate(devices, 1):
        print(f" - {serial} (Channel: {chan})")
    
    # Get access token
    access_token = get_access_token(app_key, app_secret)
    if not access_token:
        print("Failed to get access token. Exiting.")
        sys.exit(1)
    
    # Manage intelligent agent
    agent_id = manage_intelligent_agent(access_token, template_id)
    if not agent_id:
        print("Failed to manage intelligent agent. Exiting.")
        sys.exit(1)
    
    # Capture and analyze images
    print("\n" + "=" * 70)
    print("[Step 3] Capturing and analyzing images...")
    print("=" * 70)
    
    success_count = 0
    analysis_results = []
    
    for i, (device_serial, channel_no) in enumerate(devices):
        if i > 0:
            time.sleep(4)  # Rate limiting for capture API
        
        # Capture image
        pic_url = capture_image(access_token, device_serial, channel_no)
        if not pic_url:
            continue
        
        # Analyze image
        analysis_result = analyze_image(access_token, agent_id, pic_url, DEFAULT_ANALYSIS_TEXT)
        if analysis_result is not None:
            success_count += 1
            analysis_results.append({
                'device': device_serial,
                'channel': channel_no,
                'result': analysis_result
            })
            print(f"\n[Analysis Result]")
            print(json.dumps(analysis_result, ensure_ascii=False, indent=2))
    
    # Print summary
    print("\n" + "=" * 70)
    print("INSPECTION SUMMARY")
    print("=" * 70)
    print(f" Total devices: {len(devices)}")
    print(f" Success: {success_count}")
    print(f" Failed: {len(devices) - success_count}")
    print(f" Agent ID: {agent_id}")

if __name__ == "__main__":
    main()
