#!/usr/bin/env python3
"""
Ezviz Open Video Skill (萤石设备视频流)
Generate Ezviz camera live and playback streaming links for PC and mobile devices.

Usage:
    python3 generate_preview.py [appKey] [appSecret] [deviceSerial] [channelNo]

Environment Variables:
    EZVIZ_APP_KEY         - Ezviz appKey (required, or via config file)
    EZVIZ_APP_SECRET      - Ezviz appSecret (required, or via config file)
    EZVIZ_DEVICE_SERIAL   - Device serial number (optional, or via argument)
    EZVIZ_CHANNEL_NO      - Channel number, default 1 (optional)
    EZVIZ_TOKEN_CACHE     - Token cache: 1=enabled (default), 0=disabled
"""

import os
import sys
import json
from datetime import datetime

# Add lib directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
lib_dir = os.path.join(base_dir, 'lib')
sys.path.insert(0, lib_dir)

try:
    from token_manager import get_cached_token
    TokenManagerError = Exception
except ImportError as e:
    print("❌ Error: Cannot import token_manager module")
    print(f"   lib_dir: {lib_dir}")
    print(f"   Error: {e}")
    print(f"   Files: {os.listdir(lib_dir) if os.path.exists(lib_dir) else 'Directory not found'}")
    sys.exit(1)


def print_banner():
    """Print banner"""
    print("=" * 70)
    print("Ezviz Open Video Skill (萤石设备视频流)")
    print("=" * 70)


def print_security_validation(cred_source, device_serial):
    """Print security validation info"""
    print()
    print("=" * 70)
    print("SECURITY VALIDATION")
    print("=" * 70)
    
    # Validate device serial format
    if device_serial and len(device_serial) >= 6:
        print("[OK] Device serial format validated")
    else:
        print("[WARN] Device serial format may be invalid")
    
    # Show credential source
    print(f"[OK] Using credentials from {cred_source}")
    print()


def generate_links(access_token, device_serial, channel_no):
    """Generate preview links (live + playback)"""
    # Live links
    live_pc_url = (
        f"https://openai.ys7.com/console/jssdk/pc.html"
        f"?url=ezopen://open.ys7.com/{device_serial}/{channel_no}.live"
        f"&accessToken={access_token}"
    )
    
    live_mobile_url = (
        f"https://openai.ys7.com/console/jssdk/mobile.html"
        f"?url=ezopen://open.ys7.com/{device_serial}/{channel_no}.live"
        f"&accessToken={access_token}"
    )
    
    # Playback links
    playback_pc_url = (
        f"https://openai.ys7.com/console/jssdk/pc.html"
        f"?url=ezopen://open.ys7.com/{device_serial}/{channel_no}.rec"
        f"&accessToken={access_token}"
    )
    
    playback_mobile_url = (
        f"https://openai.ys7.com/console/jssdk/mobile.html"
        f"?url=ezopen://open.ys7.com/{device_serial}/{channel_no}.rec"
        f"&accessToken={access_token}"
    )
    
    return live_pc_url, live_mobile_url, playback_pc_url, playback_mobile_url


def mask_serial(serial):
    """Anonymize device serial number"""
    if len(serial) <= 4:
        return serial
    return f"{serial[:2]}*******{serial[-1]}"


def mask_token(token):
    """Anonymize accessToken"""
    if len(token) <= 40:
        return token
    return f"{token[:40]}***********"


def load_ezviz_config_from_channels():
    """
    Load EZVIZ appId and appSecret from channels configuration.
    Does NOT load devices - device serial should be specified by user.
    
    Search order:
    1. ~/.openclaw/config.json
    2. ~/.openclaw/gateway/config.json
    3. ~/.openclaw/channels.json
    
    Returns:
        dict: {appId: str, appSecret: str} or None
    """
    config_paths = [
        os.path.expanduser('~/.openclaw/config.json'),
        os.path.expanduser('~/.openclaw/gateway/config.json'),
        os.path.expanduser('~/.openclaw/channels.json'),
    ]
    
    for config_path in config_paths:
        if not os.path.exists(config_path):
            continue
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            channels = config.get('channels', {})
            ezviz_config = channels.get('ezviz', {})
            
            if isinstance(ezviz_config, dict):
                app_id = ezviz_config.get('appId') or ezviz_config.get('app_id')
                app_secret = ezviz_config.get('appSecret') or ezviz_config.get('app_secret')
                
                if app_id and app_secret:
                    print(f"[INFO] Loaded EZVIZ config from channels: {config_path}")
                    print(f"[INFO] AppKey prefix: {app_id[:8]}...")
                    return {
                        'appId': app_id,
                        'appSecret': app_secret
                    }
        
        except (json.JSONDecodeError, IOError) as e:
            print(f"[WARNING] Failed to read config from {config_path}: {e}")
            continue
    
    return None


def get_credentials_from_env():
    """Get credentials from environment variables (fallback to channels config for AK/SK only)"""
    app_key = os.environ.get('EZVIZ_APP_KEY', '')
    app_secret = os.environ.get('EZVIZ_APP_SECRET', '')
    device_serial = os.environ.get('EZVIZ_DEVICE_SERIAL', '')
    channel_no = os.environ.get('EZVIZ_CHANNEL_NO', '1')
    use_cache = os.environ.get('EZVIZ_TOKEN_CACHE', '1') != '0'
    
    cred_source = 'environment variables'
    
    # Try channels config for AK/SK if env vars are empty
    # Device serial is NOT loaded from config - user must specify it
    if not app_key or not app_secret:
        channels_config = load_ezviz_config_from_channels()
        if channels_config:
            if not app_key:
                app_key = channels_config['appId']
            if not app_secret:
                app_secret = channels_config['appSecret']
            cred_source = 'channels config'
    
    # Convert to None if still empty
    app_key = app_key if app_key else None
    app_secret = app_secret if app_secret else None
    
    return app_key, app_secret, device_serial, channel_no, use_cache, cred_source


def get_credentials_from_config():
    """Get credentials from config files"""
    config_paths = [
        os.path.expanduser('~/.openclaw/config.json'),
        os.path.expanduser('~/.openclaw/gateway/config.json'),
        os.path.expanduser('~/.openclaw/channels.json'),
    ]
    
    for config_path in config_paths:
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    ezviz_config = config.get('channels', {}).get('ezviz', {})
                    if ezviz_config.get('enabled', True):
                        app_key = ezviz_config.get('appId') or ezviz_config.get('appKey')
                        app_secret = ezviz_config.get('appSecret')
                        if app_key and app_secret:
                            device_serial = os.environ.get('EZVIZ_DEVICE_SERIAL')
                            channel_no = os.environ.get('EZVIZ_CHANNEL_NO', '1')
                            use_cache = os.environ.get('EZVIZ_TOKEN_CACHE', '1') != '0'
                            return app_key, app_secret, device_serial, channel_no, use_cache, f'config file ({config_path})'
        except (json.JSONDecodeError, IOError):
            continue
    
    return None, None, None, None, True, 'none'


def get_credentials_from_args():
    """Get credentials from command line arguments"""
    if len(sys.argv) >= 4:
        app_key = sys.argv[1]
        app_secret = sys.argv[2]
        device_serial = sys.argv[3]
        channel_no = sys.argv[4] if len(sys.argv) >= 5 else '1'
        use_cache = os.environ.get('EZVIZ_TOKEN_CACHE', '1') != '0'
        return app_key, app_secret, device_serial, channel_no, use_cache, 'command line arguments'
    
    return None, None, None, None, True, 'none'


def main():
    """Main function"""
    print_banner()
    print(f"[Time] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get credentials (priority: env vars > channels config > command line args)
    app_key, app_secret, device_serial, channel_no, use_cache, cred_source = get_credentials_from_env()
    
    # If still no credentials, try command line arguments
    if not app_key or not app_secret:
        args_key, args_secret, args_serial, args_channel, args_cache, args_source = get_credentials_from_args()
        if args_key and args_secret:
            app_key, app_secret = args_key, args_secret
            if args_serial:
                device_serial = args_serial
            if args_channel != '1':
                channel_no = args_channel
            cred_source = args_source
    
    # Check required parameters
    if not app_key or not app_secret:
        print()
        print("❌ Error: Missing required credentials")
        print()
        print("Please set environment variables:")
        print("  export EZVIZ_APP_KEY=\"your_app_key\"")
        print("  export EZVIZ_APP_SECRET=\"your_app_secret\"")
        print()
        print("Or configure in ~/.openclaw/channels.json:")
        print('  {"channels": {"ezviz": {"appId": "...", "appSecret": "..."}}}')
        print()
        sys.exit(1)
    
    # Device serial must be specified by user (not loaded from config)
    if not device_serial:
        print()
        print("❌ Error: Missing device serial number")
        print()
        print("Please specify device by:")
        print("  1. Environment variable: export EZVIZ_DEVICE_SERIAL=\"BF6985110\"")
        print(f"  2. Command line: python3 {sys.argv[0]} <appKey> <appSecret> <deviceSerial>")
        print()
        sys.exit(1)
    
    # Show device info
    print(f"[INFO] Device: {mask_serial(device_serial)} (Channel: {channel_no})")
    
    # Security validation
    print_security_validation(cred_source, device_serial)
    
    # Get Token
    print("=" * 70)
    print("[Step 1] Getting access token...")
    print("=" * 70)
    
    try:
        token_result = get_cached_token(app_key, app_secret, use_cache=use_cache)
        print(f"[DEBUG] token_result keys: {token_result.keys()}")
        print(f"[DEBUG] token_result: {token_result}")
        
        # Compatible with different return formats
        access_token = token_result.get('accessToken') or token_result.get('access_token')
        expire_time = token_result.get('expireTime') or token_result.get('expire_time', 'Unknown')
        
        if not access_token:
            print(f"[ERROR] No access_token in result: {token_result}")
            sys.exit(1)
        
        if token_result.get('from_cache'):
            print(f"[INFO] Using cached global token, expires: {expire_time}")
        else:
            print(f"[INFO] Got new token from Ezviz API, expires: {expire_time}")
        
        print(f"[SUCCESS] Token obtained, expires: {expire_time}")
        
    except Exception as e:
        print(f"[ERROR] Failed to get token: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generate links
    print()
    print("=" * 70)
    print("[Step 2] Generating links...")
    print("=" * 70)
    print()
    
    live_pc_url, live_mobile_url, playback_pc_url, playback_mobile_url = generate_links(access_token, device_serial, channel_no)
    
    print("📺 Live Links:")
    print()
    print("  🖥️  PC:")
    print(f"  {live_pc_url}")
    print()
    print("  📱  Mobile:")
    print(f"  {live_mobile_url}")
    print()
    
    print("📼 Playback Links:")
    print()
    print("  🖥️  PC:")
    print(f"  {playback_pc_url}")
    print()
    print("  📱  Mobile:")
    print(f"  {playback_mobile_url}")
    print()
    
    # Output summary
    print("=" * 70)
    print("LINKS GENERATED")
    print("=" * 70)
    print(f" Device: {device_serial} (Channel: {channel_no})")
    print(f" Token: {mask_token(access_token)}")
    print(f" Live PC: {live_pc_url[:80]}...")
    print(f" Live Mobile: {live_mobile_url[:80]}...")
    print(f" Playback PC: {playback_pc_url[:80]}...")
    print(f" Playback Mobile: {playback_mobile_url[:80]}...")
    print("=" * 70)
    
    # Output JSON format (for programmatic use)
    print()
    print("JSON Output:")
    result = {
        'device': device_serial,
        'channel': channel_no,
        'live': {
            'pc_url': live_pc_url,
            'mobile_url': live_mobile_url
        },
        'playback': {
            'pc_url': playback_pc_url,
            'mobile_url': playback_mobile_url
        },
        'token_masked': mask_token(access_token),
        'generated_at': datetime.now().isoformat()
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
