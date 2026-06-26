#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dahua AI Device Image Analysis - OpenClaw Skill
Single-file implementation combining device snapshot capture with AI analysis.

Required environment variables:
  - DAHUA_CLOUD_PRODUCT_ID: AppID from Dahua Cloud
  - DAHUA_CLOUD_AK: Access Key from Dahua Cloud
  - DAHUA_CLOUD_SK: Secret Key from Dahua Cloud

Required dependency:
  - requests (pip install requests)

Usage:
  python device_image_analysis.py --device-sn <SN> --prompt "<question>"
"""

import sys
import os
import argparse
import io
import json
from pathlib import Path
from typing import Optional, Dict, Any
import requests
import hmac
import hashlib
import time
import uuid


# ============================================================================
# Constants
# ============================================================================

DEFAULT_API_BASE_URL = 'https://open.cloud-dahua.com/'
DEFAULT_CHANNEL_NO = 0
TOKEN_EXPIRY_SECONDS = 3600

# API Endpoints
API_AUTH_TOKEN = '/open-api/api-base/auth/getAppAccessToken'
API_DEVICE_SNAPSHOT = '/open-api/api-iot/device/setDeviceSnapEnhanced'
API_AI_ANALYSIS = '/open-api/api-ai/largeModelDetect/imageAnalysis'

# HTTP Timeouts (seconds)
TIMEOUT_AUTH = 60
TIMEOUT_SNAPSHOT = 60
TIMEOUT_DOWNLOAD = 300
TIMEOUT_ANALYSIS = 120

# Retry Configuration
URL_VERIFY_RETRIES = 3
URL_VERIFY_DELAY = 1
SNAPSHOT_RETRY_DELAY = 1

# Environment Variable Names
ENV_CLOUD_ID = 'DAHUA_CLOUD_PRODUCT_ID'
ENV_CLOUD_AK = 'DAHUA_CLOUD_AK'
ENV_CLOUD_SK = 'DAHUA_CLOUD_SK'


def fix_encoding():
    """Fix encoding for Windows PowerShell/CMD to ensure proper display"""
    if sys.platform == 'win32':
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def get_token_sign(access_key: str, timestamp: str, nonce: str, secret: str) -> str:
    """
    Auth API signature (for getting Token)
    Signature factor: access_key + timestamp + nonce
    """
    auth_factor = f'{access_key}{timestamp}{nonce}'
    return hmac.new(
        secret.encode('utf-8'),
        auth_factor.encode('utf-8'),
        hashlib.sha512
    ).hexdigest().upper()


def business_api_sign(access_key: str, app_access_token: str, timestamp: str, nonce: str, secret: str) -> str:
    """
    Business API signature (for snapshot/AI analysis)
    Signature factor: access_key + app_access_token + timestamp + nonce
    """
    auth_factor = f'{access_key}{app_access_token}{timestamp}{nonce}'
    return hmac.new(
        secret.encode('utf-8'),
        auth_factor.encode('utf-8'),
        hashlib.sha512
    ).hexdigest().upper()


# ============================================================================
# Dahua Snapshot Client
# ============================================================================

class DahuaSnapshotClient:
    """Dahua IoT Snapshot Client - Lightweight implementation using requests library"""
    
    def __init__(
        self,
        app_id: str,
        access_key: str,
        secret_key: str,
        api_base_url: str = DEFAULT_API_BASE_URL
    ):
        self.config = {
            'app_id': app_id,
            'access_key': access_key,
            'secret_key': secret_key,
            'api_base_url': api_base_url.rstrip('/')
        }
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.token_expiry: int = 0
    
    def get_app_access_token(self) -> Optional[str]:
        """Get AppAccessToken"""
        print("[Step 1] Getting AppAccessToken...")
        
        try:
            timestamp_auth = str(int(time.time() * 1000))
            nonce_auth = str(uuid.uuid4())
            trace_id_auth = f"tid-{int(time.time())}"
            
            # Generate signature (for getting Token)
            signature_auth = get_token_sign(
                self.config['access_key'],
                timestamp_auth,
                nonce_auth,
                self.config['secret_key']
            )
            
            headers_auth = {
                'Content-Type': 'application/json',
                'AccessKey': self.config['access_key'],
                'Timestamp': timestamp_auth,
                'Nonce': nonce_auth,
                'Sign': signature_auth,
                'ProductId': self.config['app_id'],
                'X-TraceId-Header': trace_id_auth,
                'Version': 'V1',
                'Sign-Type': 'simple'
            }
            
            payload_auth = {'productId': self.config['app_id']}
            
            url = self.config['api_base_url'] + API_AUTH_TOKEN
            response = self.session.post(url, headers=headers_auth, json=payload_auth, timeout=TIMEOUT_AUTH)
            
            result = response.json()
            
            if result.get('success'):
                self.access_token = result.get('data', {}).get('appAccessToken')
                self.token_expiry = int(time.time()) + TOKEN_EXPIRY_SECONDS
                print("[OK] Token obtained successfully")
                return self.access_token
            else:
                print(f"API Error: {result.get('msg')}")
                return None
                
        except Exception as e:
            print(f"Request Exception: {e}")
            return None
    
    def capture_snapshot(self, device_id: str, channel_no: int, is_retry: bool = False) -> Dict[str, Any]:
        """
        Capture device snapshot
        
        Args:
            device_id: Device serial number
            channel_no: Channel number
            is_retry: Whether this is a retry capture
            
        Returns:
            Dictionary containing snapshot result
        """
        current_time = int(time.time())
        if not self.access_token or current_time > self.token_expiry:
            if not self.get_app_access_token():
                return {'success': False, 'message': 'Failed to get access token'}
        
        step_label = "[Step 2-Retry]" if is_retry else "\n[Step 2]"
        print(f"{step_label} Capturing snapshot")
        print(f"  DeviceId/SN: {device_id}, ChannelId: {channel_no}")
        
        body = {
            'deviceId': device_id,
            'channelId': str(channel_no)
        }
        
        try:
            timestamp_img = str(int(time.time() * 1000))
            nonce_img = str(uuid.uuid4())
            trace_id_img = f"tid-{int(time.time())}"
            
            # Generate signature (business API signature)
            signature_img = business_api_sign(
                self.config['access_key'],
                self.access_token,
                timestamp_img,
                nonce_img,
                self.config['secret_key']
            )
            
            headers_img = {
                'Content-Type': 'application/json',
                'AccessKey': self.config['access_key'],
                'Timestamp': timestamp_img,
                'Nonce': nonce_img,
                'Sign': signature_img,
                'ProductId': self.config['app_id'],
                'X-TraceId-Header': trace_id_img,
                'Version': 'V1',
                'Sign-Type': 'simple',
                'AppAccessToken': self.access_token
            }
            
            url = self.config['api_base_url'] + API_DEVICE_SNAPSHOT
            response = self.session.post(url, headers=headers_img, json=body, timeout=TIMEOUT_SNAPSHOT)
            
            result = response.json()
            
            if result.get('success') and result.get('data'):
                image_data = result['data']
                image_url = image_data.get('url')
                if image_url:
                    local_path = self.download_and_save(image_url, device_id, channel_no)                    
                    return {
                        'success': True,
                        'device_id': device_id,
                        'channel_id': channel_no,
                        'image_url': image_url,
                        'local_path': local_path,
                        'timestamp': int(time.time() * 1000),
                        'message': 'Snapshot captured successfully'
                    }
                else:
                    return {'success': False, 'message': 'No image URL in response'}
            else:
                error_msg = result.get('msg') or result.get('message') or 'Unknown error'
                print(f"[ERROR] {error_msg}")
                return {'success': False, 'message': error_msg}
                
        except Exception as e:
            print(f"[EXCEPTION] Capture failed: {e}")
            return {'success': False, 'message': str(e)}
    
    def download_and_save(
        self,
        image_url: str,
        device_id: str,
        channel_no: int
    ) -> Optional[str]:
        """
        Download image and save to local
        
        Args:
            image_url: Image URL
            device_id: Device serial number
            channel_no: Channel number
            
        Returns:
            Local file path, None if failed
        """
        try:
            output_dir = Path('captured_images') / device_id
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f'ch{channel_no}_{int(time.time())}.jpg'
            filepath = output_dir / filename
            
            print(f'[DEBUG] Downloading image from: {image_url}')
            
            # Retry logic for OSS URL readiness
            # Wait 1s before first download, max 5 retries
            max_retries = 5
            retry_delay = 1
            
            for attempt in range(max_retries):
                # Wait 1 second before downloading (except first attempt if desired)
                # According to requirement: wait 1s after getting URL, then download
                if attempt > 0:
                    print(f'[DEBUG] Waiting {retry_delay}s before retry {attempt + 1}/{max_retries}...')
                    time.sleep(retry_delay)
                else:
                    # First attempt: wait 1s as required
                    print(f'[DEBUG] Waiting {retry_delay}s before first download attempt...')
                    time.sleep(retry_delay)
                
                try:
                    response = requests.Session().get(image_url, timeout=30)
                    print(f'[DEBUG] Download response status: {response.status_code} (attempt {attempt + 1}/{max_retries})')
                    if response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        print(f'[DEBUG] Image saved to: {filepath}')
                        return str(filepath.absolute())
                    elif response.status_code == 404:
                        # OSS not ready yet, retry
                        if attempt < max_retries - 1:
                            print(f'[DEBUG] Image not ready (404), will retry...')
                            continue
                        else:
                            print(f'[WARN] Failed to download image after {max_retries} attempts: HTTP 404')
                            return None
                    else:
                        print(f'[WARN] Failed to download image: HTTP {response.status_code}')
                        # For other errors, also retry
                        if attempt < max_retries - 1:
                            continue
                        return None
                except Exception as e:
                    print(f'[DEBUG] Download attempt {attempt + 1} failed: {e}')
                    if attempt < max_retries - 1:
                        continue
                    else:
                        print(f'[WARN] Download failed after {max_retries} attempts: {e}')
                        return None
                
        except Exception as e:
            print(f'[WARN] Local save failed: {e}')
            return None


# ============================================================================
# Cloud AI Analysis Client
# ============================================================================

def verify_image_url_accessible(image_url: str, max_retries: int = URL_VERIFY_RETRIES) -> bool:
    """
    Verify if image URL is accessible
    
    Args:
        image_url: Image URL
        max_retries: Max retry attempts
        
    Returns:
        Whether accessible
    """
    # Simulate browser headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    for attempt in range(max_retries):
        try:
            response = requests.head(image_url, headers=headers, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return True
        except Exception:
            pass
        if attempt < max_retries - 1:
            time.sleep(URL_VERIFY_DELAY)
    return False


def analyze_with_dahua_ai(
    access_key: str,
    app_access_token: str,
    secret_key: str,
    app_id: str,
    image_url: str,
    prompt: str,
    base_url: str = DEFAULT_API_BASE_URL
) -> Dict[str, Any]:
    """
    Call Dahua Cloud AI for image analysis
    
    Args:
        access_key: AccessKey
        app_access_token: AppAccessToken
        secret_key: SecretKey
        app_id: AppID (ProductId)
        image_url: Image URL
        prompt: Analysis prompt
        base_url: API base URL
        
    Returns:
        Analysis result dictionary
    """
    print('\n[Step 3] Calling Dahua Cloud AI for image analysis')
    
    try:
        timestamp_img = str(int(time.time() * 1000))
        nonce_img = str(uuid.uuid4())
        trace_id_img = f"tid-{int(time.time())}"
        
        # Generate signature (business API signature)
        signature_img = business_api_sign(
            access_key,
            app_access_token,
            timestamp_img,
            nonce_img,
            secret_key
        )
        
        headers_img = {
            'Content-Type': 'application/json',
            'AccessKey': access_key,
            'Timestamp': timestamp_img,
            'Nonce': nonce_img,
            'Sign': signature_img,
            'ProductId': app_id,
            'X-TraceId-Header': trace_id_img,
            'Version': 'V1',
            'Sign-Type': 'simple',
            'AppAccessToken': app_access_token
        }
        
        payload_img = {'pictureUrl': image_url, 'prompt': prompt}
        
        # Print request info
        print(f'  Request Payload: {json.dumps(payload_img, ensure_ascii=False)}')
        
        response = requests.post(
            f'{base_url.rstrip("/")}{API_AI_ANALYSIS}',
            headers=headers_img,
            json=payload_img,
            timeout=TIMEOUT_ANALYSIS
        )
        
        result = response.json()
        
        # Print full API response
        print(f'  API Response: {json.dumps(result, ensure_ascii=False)}')
        
        success = result.get('success')
        code = result.get('code')
        msg = result.get('msg')
        data = result.get('data', {})
        
        if success:
            print(f"[OK] AI analysis successful. Result: {data.get('content', 'N/A')}")
        
        return {
            'success': success,
            'code': code,
            'message': msg,
            'data': data,
            'result': data.get('content', '')
        }
        
    except Exception as e:
        return {
            'success': False,
            'code': 'REQUEST_ERROR',
            'message': f'Error calling image analysis API: {str(e)}',
            'data': {}
        }


# ============================================================================
# Main Analysis Function
# ============================================================================

def analyze_device_camera(
    device_sn: str,
    prompt: str,
    channel_no: int = DEFAULT_CHANNEL_NO
) -> Dict[str, Any]:
    """
    Complete device image analysis workflow: capture -> download -> AI analysis
    
    Args:
        device_sn: Device serial number (SN)
        prompt: Analysis prompt
        channel_no: Channel number (default: 0)
        
    Returns:
        Dictionary containing complete analysis result
    """
    print('\n' + '='*80)
    print('Dahua AI Device Image Analysis Tool')
    print('='*80)
    print(f'Device SN: {device_sn}')
    print(f'Prompt: {prompt}')
    print(f'Channel: {channel_no}')
    print('-'*80)
    
    # Get credentials from environment variables
    app_id = os.environ.get(ENV_CLOUD_ID)
    access_key = os.environ.get(ENV_CLOUD_AK)
    secret_key = os.environ.get(ENV_CLOUD_SK)
    
    if not all([app_id, access_key, secret_key]):
        raise ValueError(
            'Missing required cloud credentials!\n'
            'Please set environment variables:\n'
            f'  {ENV_CLOUD_ID}\n'
            f'  {ENV_CLOUD_AK}\n'
            f'  {ENV_CLOUD_SK}'
        )
    
    # Initialize client
    client = DahuaSnapshotClient(app_id, access_key, secret_key)
    
    # Step 1: Capture snapshot
    print(f'\n[Step 1] Capturing snapshot from device: {device_sn}')
    
    capture_result = client.capture_snapshot(device_sn, channel_no)
    
    if not capture_result or not capture_result.get('success'):
        return {
            'success': False,
            'step': 'capture',
            'error': capture_result.get('message', 'Unknown error') if capture_result else 'Snapshot failed',
            'details': capture_result
        }
    
    image_url = capture_result.get('image_url')
    local_path = capture_result.get('local_path')
    
    if not image_url:
        return {
            'success': False,
            'step': 'capture',
            'error': 'Failed to extract image URL from response'
        }
    
    if local_path:
        print(f'Local Image Saved: {local_path}')
    
    # Step 2: AI Analysis
    print('\n[Step 2] Analyzing image with Dahua Cloud AI...')
    
    ai_result = analyze_with_dahua_ai(
        access_key=access_key,
        app_access_token=client.access_token,
        secret_key=secret_key,
        app_id=app_id,
        image_url=image_url,
        prompt=prompt
    )
    
    # Build complete result
    return {
        'success': ai_result.get('success'),
        'device_sn': device_sn,
        'channel_no': channel_no,
        'image_url': image_url,
        'local_image_path': local_path,
        'analysis': ai_result
    }


# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    """Command line interface main function"""
    parser = argparse.ArgumentParser(description='Dahua AI Device Image Analysis Tool')
    parser.add_argument('--device-sn', '-d', type=str, required=True,
                       help='Device serial number (SN)')
    parser.add_argument('--prompt', '-p', type=str, required=True,
                       help='AI analysis prompt/question')
    parser.add_argument('--channel', '-c', type=int, default=DEFAULT_CHANNEL_NO,
                       help=f'Camera channel number (default: {DEFAULT_CHANNEL_NO})')
    
    args = parser.parse_args()
    
    try:
        result = analyze_device_camera(
            device_sn=args.device_sn,
            prompt=args.prompt,
            channel_no=args.channel
        )
        
        print('\n' + '='*80)
        print('ANALYSIS RESULTS')
        print('='*80)
        
        if result.get('success'):
            print('Success: True')
            print(f"Device: {result['device_sn']}")
            print(f"Channel: {result['channel_no']}")
            
            local_path = result.get('local_image_path')
            if local_path:
                print(f'\nIMAGE PATH: {local_path}')
            else:
                print('\n[INFO] No local image saved')
            
            analysis = result.get('analysis', {})
            if isinstance(analysis, dict):
                content = analysis.get('result', '')
                print('\nAI Analysis Result:')
                print(content if content else 'N/A')
                
                if analysis.get('code'):
                    print(f"\nCode: {analysis.get('code')}")
                if analysis.get('message'):
                    print(f"Message: {analysis.get('message')}")
            else:
                print(f'Analysis: {analysis}')
        else:
            print('Success: False')
            print(f"Error Step: {result.get('step', 'Unknown')}")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        print('='*80)
        
        sys.exit(0 if result.get('success') else 1)
        
    except ValueError as e:
        print(f'\n❌ Configuration Error: {e}')
        print('\nPlease set the following environment variables:')
        print(f'  Windows PowerShell: $env:{ENV_CLOUD_ID}=\'xxx\'')
        print(f'  Linux/Mac: export {ENV_CLOUD_ID}=\'xxx\'')
        print('\nOr refer to README.md for more configuration methods')
        print('='*80)
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ Unexpected Error: {str(e)}')
        print('='*80)
        sys.exit(1)


if __name__ == "__main__":
    fix_encoding()
    main()
