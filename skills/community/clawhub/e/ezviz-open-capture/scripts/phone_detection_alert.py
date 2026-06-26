#!/usr/bin/env python3
"""
Phone Detection Alert Script

Detects phone usage from camera snapshot and sends voice alert to Ezviz device.

Workflow:
1. Capture snapshot from camera
2. Call phone detection API
3. If phone detected: generate TTS audio, upload to Ezviz, send to device
"""

import sys
import os
import json
import time
import hashlib
import hmac
import requests
from datetime import datetime

# Configuration
TOKEN_GET_API_URL = "https://open.ys7.com/api/lapp/token/get"  # 获取 AccessToken 接口
DEVICE_CAPTURE_API_URL = "https://open.ys7.com/api/lapp/device/capture"  # 设备抓拍图片接口
PHONE_DETECTION_API_URL = "https://open.ys7.com/api/service/intelligence/algo/analysis/play_phone_detection"  # 玩手机算法分析接口
VOICE_UPLOAD_API_URL = "https://open.ys7.com/api/lapp/voice/upload"  # 语音文件上传接口
VOICE_SEND_API_URL = "https://open.ys7.com/api/lapp/voice/send"  # 语音文件下发接口

# These should be provided by the user or environment
APP_KEY = os.environ.get("EZVIZ_APP_KEY", "")
APP_SECRET = os.environ.get("EZVIZ_APP_SECRET", "")
DEVICE_SERIAL = os.environ.get("EZVIZ_DEVICE_SERIAL", "")
CHANNEL_NO = os.environ.get("EZVIZ_CHANNEL_NO", "1")


def get_current_timestamp():
    """Get current Unix timestamp in milliseconds."""
    return int(time.time() * 1000)


def generate_sign(accessToken, timestamp):
    """Generate API signature for Ezviz API."""
    # sign = md5(accessToken + timestamp)
    sign_str = f"{accessToken}{timestamp}"
    return hashlib.md5(sign_str.encode()).hexdigest()


def get_access_token(app_key, app_secret):
    """
    Get access token using appKey and appSecret.
    
    API: POST /api/lapp/token/get
    Content-Type: application/x-www-form-urlencoded
    
    Args:
        app_key: Your application key
        app_secret: Your application secret
    
    Returns:
        dict: {success: bool, access_token: str, expire_time: int, error: str}
    """
    print(f"[INFO] Getting access token...")
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "appKey": app_key,
        "appSecret": app_secret
    }
    
    try:
        response = requests.post(
            TOKEN_GET_API_URL,
            headers=headers,
            data=data,
            timeout=30
        )
        
        result = response.json()
        # Don't log full response to avoid leaking credentials
        
        if result.get("code") == "200":
            data = result.get("data", {})
            expire_time = data.get("expireTime", 0)
            expire_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time / 1000))
            print(f"[SUCCESS] Token obtained, expires: {expire_str}")
            return {
                "success": True,
                "access_token": data.get("accessToken", ""),
                "expire_time": expire_time
            }
        else:
            error_msg = result.get("msg", "Unknown error")
            print(f"[ERROR] Get token failed: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "code": result.get("code")
            }
    
    except Exception as e:
        print(f"[ERROR] Get token failed: {type(e).__name__}")
        return {
            "success": False,
            "error": str(e)
        }


def capture_device_image(access_token, device_serial, channel_no=1):
    """
    Capture image from device.
    
    API: POST /api/lapp/device/capture
    Content-Type: application/x-www-form-urlencoded
    
    Args:
        access_token: Ezviz access token
        device_serial: Device serial number (uppercase letters)
        channel_no: Channel number (default 1 for IPC)
    
    Returns:
        dict: {success: bool, pic_url: str, error: str}
    """
    print(f"[INFO] Capturing image from device: {device_serial}")
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "accessToken": access_token,
        "deviceSerial": device_serial.upper(),
        "channelNo": str(channel_no)
    }
    
    try:
        response = requests.post(
            DEVICE_CAPTURE_API_URL,
            headers=headers,
            data=data,
            timeout=30
        )
        
        result = response.json()
        # Don't log full response
        
        if result.get("code") == "200":
            data = result.get("data", {})
            pic_url = data.get("picUrl", "")
            print(f"[SUCCESS] Image captured: {pic_url[:50]}...")
            return {
                "success": True,
                "pic_url": pic_url,
                "expire_hours": 2
            }
        else:
            error_msg = result.get("msg", "Capture failed")
            print(f"[ERROR] Capture failed: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "code": result.get("code")
            }
    
    except Exception as e:
        print(f"[ERROR] Device capture failed: {type(e).__name__}")
        return {
            "success": False,
            "error": str(e)
        }


def capture_snapshot(camera_id=None, output_path="/tmp/camera_snapshot.jpg"):
    """
    Capture a snapshot from the camera and upload to get URL.
    In OpenClaw environment, this would use the nodes tool.
    For standalone use, implement camera capture logic here.
    
    Returns:
        tuple: (local_path, image_url) - The URL is needed for the detection API
    """
    print(f"[INFO] Capturing snapshot from camera: {camera_id or 'default'}")
    # This is a placeholder - in OpenClaw, use nodes tool with camera_snap action
    # The API requires a URL, not local file, so you need to upload the image somewhere
    # For now, return the output path - user needs to implement image hosting
    return output_path, None  # URL needs to be provided by user


def detect_phone_usage(image_url, access_token, img_width=1280, img_height=720):
    """
    Call phone detection API to analyze if someone is using a phone.
    
    API: POST /api/service/intelligence/algo/analysis/play_phone_detection
    Content-Type: application/json
    
    Args:
        image_url: URL of the image to analyze
        access_token: Ezviz access token
        img_width: Image width (default 1280)
        img_height: Image height (default 720)
    
    Returns:
        dict: Detection result with 'is_phone_detected' boolean and details
    """
    print(f"[INFO] Analyzing image for phone usage: {image_url}")
    
    headers = {
        "accessToken": access_token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "taskType": "",
        "dataInfo": [
            {
                "data": image_url,
                "type": "url",
                "modal": "image"
            }
        ],
        "dataParams": [
            {
                "modal": "image",
                "img_width": img_width,
                "img_height": img_height
            }
        ]
    }
    
    try:
        response = requests.post(
            PHONE_DETECTION_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        result = response.json()
        # Don't log full response to avoid leaking data
        
        # Parse response based on actual API structure
        # meta.code == 200 means success
        if result.get("meta", {}).get("code") == 200:
            data = result.get("data", {})
            images = data.get("images")
            
            # Handle case where images is None (no people detected in image)
            if images is None:
                print("[INFO] No people detected in image")
                return {
                    "success": True,
                    "is_phone_detected": False,
                    "details": data,
                    "confidence": 0.0
                }
            
            # Check if any bbox has play_phone behavior
            is_detected = False
            confidence = 0.0
            
            for img in images:
                content_ann = img.get("contentAnn", {})
                bboxes = content_ann.get("bboxes", [])
                for bbox in bboxes:
                    tag_info = bbox.get("tagInfo", {})
                    labels = tag_info.get("labels", [])
                    for label in labels:
                        if label.get("key") == "behavior" and label.get("label") == "play_phone":
                            is_detected = True
                            confidence = max(confidence, label.get("labelWeight", 0))
            
            if is_detected:
                print(f"[ALERT] Phone usage detected! (confidence: {confidence:.2f})")
            else:
                print("[INFO] No phone usage detected")
            
            return {
                "success": True,
                "is_phone_detected": is_detected,
                "details": data,
                "confidence": confidence
            }
        else:
            meta = result.get("meta", {})
            error_msg = meta.get("message", "Unknown error")
            print(f"[ERROR] Detection failed: {error_msg}")
            return {
                "success": False,
                "is_phone_detected": False,
                "error": error_msg,
                "code": meta.get("code")
            }
    
    except Exception as e:
        print(f"[ERROR] Phone detection failed: {type(e).__name__}")
        return {
            "success": False,
            "is_phone_detected": False,
            "error": str(e)
        }


def generate_tts_audio(text, output_path="/tmp/alert_audio.mp3"):
    """
    Generate TTS audio file using edge-tts (Microsoft Azure TTS).
    
    Args:
        text: Text to convert to speech
        output_path: Output audio file path
    
    Returns:
        str: Path to generated audio file
    """
    print(f"[INFO] Generating TTS audio: '{text}'")
    
    try:
        # Try to use edge-tts (free Microsoft Azure TTS)
        import asyncio
        import edge_tts
        
        async def generate_audio():
            communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
            await communicate.save(output_path)
        
        asyncio.run(generate_audio())
        print(f"[INFO] TTS audio saved to: {output_path}")
        
        # Verify file size
        file_size = os.path.getsize(output_path)
        print(f"[INFO] Audio file size: {file_size} bytes")
        
        if file_size < 1000:
            print("[WARNING] Audio file seems too small, may be invalid")
        
        return output_path
        
    except ImportError:
        print("[INFO] edge-tts not installed, trying gTTS...")
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='zh-cn')
            tts.save(output_path)
            print(f"[INFO] TTS audio saved to: {output_path}")
            return output_path
            
        except ImportError:
            print("[WARNING] No TTS library available. Creating placeholder...")
            print("[INFO] Install edge-tts: pip install edge-tts")
            print("[INFO] Or install gTTS: pip install gTTS")
            
            # Download a sample beep sound as placeholder
            import urllib.request
            try:
                # Use a minimal valid MP3
                sample_url = "https://www.soundjay.com/button/beep-07.wav"
                urllib.request.urlretrieve(sample_url, output_path.replace(".mp3", ".wav"))
                output_path = output_path.replace(".mp3", ".wav")
                print(f"[INFO] Downloaded sample sound: {output_path}")
                return output_path
            except:
                print("[ERROR] Could not download sample sound")
                return None
    
    except Exception as e:
        print(f"[ERROR] TTS generation failed: {e}")
        return None


def upload_voice_file(audio_path, access_token, voice_name=None):
    """
    Upload voice file to Ezviz cloud.
    
    Returns:
        dict: Upload result with voice URL if successful
    """
    print(f"[INFO] Uploading voice file: {audio_path}")
    
    if voice_name is None:
        voice_name = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    
    timestamp = get_current_timestamp()
    sign = generate_sign(access_token, timestamp)
    
    params = {
        "accessToken": access_token,
        "time": timestamp,
        "sign": sign
    }
    
    try:
        with open(audio_path, 'rb') as f:
            files = {
                'voiceFile': (voice_name, f, 'audio/mpeg')
            }
            data = {
                'voiceName': voice_name
            }
            response = requests.post(
                VOICE_UPLOAD_API_URL,
                params=params,
                files=files,
                data=data,
                timeout=30
            )
        
        result = response.json()
        # Don't log full response
        
        if result.get("code") == "200":
            data = result.get("data", {})
            voice_url = data.get("url", "")
            print(f"[SUCCESS] Voice uploaded: {voice_url[:50]}...")
            return {
                "success": True,
                "voice_url": voice_url,
                "voice_name": data.get("name", voice_name)
            }
        else:
            error_msg = result.get("msg", "Upload failed")
            print(f"[ERROR] Voice upload failed: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
    
    except Exception as e:
        print(f"[ERROR] Voice upload failed: {type(e).__name__}")
        return {
            "success": False,
            "error": str(e)
        }


def send_voice_to_device(device_serial, voice_url, access_token, channel_no=1):
    """
    Send voice file to Ezviz device for playback.
    
    API: POST /api/lapp/voice/send
    Content-Type: application/x-www-form-urlencoded
    
    Args:
        device_serial: Device serial number
        voice_url: Voice file URL (from upload API response)
        access_token: Ezviz access token
        channel_no: Channel number (default 1)
    """
    print(f"[INFO] Sending voice to device: {device_serial}")
    
    headers = {
        "accessToken": access_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "deviceSerial": device_serial,
        "channelNo": str(channel_no),
        "fileUrl": voice_url
    }
    
    try:
        response = requests.post(
            VOICE_SEND_API_URL,
            headers=headers,
            data=data,
            timeout=30
        )
        
        result = response.json()
        # Don't log full response
        
        if result.get("code") == "200":
            print(f"[SUCCESS] Alert sent to device {device_serial}!")
            return {
                "success": True,
                "message": "Voice sent successfully"
            }
        else:
            error_msg = result.get("msg", "Send failed")
            print(f"[ERROR] Voice send failed: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "code": result.get("code")
            }
    
    except Exception as e:
        print(f"[ERROR] Voice send failed: {type(e).__name__}")
        return {
            "success": False,
            "error": str(e)
        }


def parse_device_list(device_str, channel_str="1"):
    """
    Parse device list from string.
    
    Supports formats:
    - Single device: "BA5918431" or "BA5918431,1"
    - Multiple devices: "BA5918431,BA5918432,BA5918433"
    - Multiple devices with channels: "BA5918431:1,BA5918432:1,BA5918433:2"
    - Mixed: "BA5918431,BA5918432:2,BA5918433"
    
    Args:
        device_str: Device serial(s), comma-separated
        channel_str: Default channel number (used if not specified per device)
    
    Returns:
        list: [(device_serial, channel_no), ...]
    """
    devices = []
    
    if not device_str:
        return devices
    
    for item in device_str.split(","):
        item = item.strip()
        if not item:
            continue
        
        if ":" in item:
            # Format: deviceSerial:channelNo
            parts = item.split(":")
            serial = parts[0].strip().upper()
            channel = int(parts[1].strip()) if len(parts) > 1 else int(channel_str)
        else:
            # Format: deviceSerial only
            serial = item.upper()
            channel = int(channel_str)
        
        devices.append((serial, channel))
    
    return devices


def main():
    """
    Main workflow: get token -> capture images from multiple devices -> detect phones -> alert.
    
    Complete flow:
    1. Get access token (appKey + appSecret)
    2. For each device:
       - Capture device image
       - Detect phone usage
       - If detected: generate TTS -> upload voice -> send to device
    """
    print("=" * 60)
    print("Phone Detection Alert System")
    print("=" * 60)
    
    # Configuration from environment or arguments
    app_key = APP_KEY or sys.argv[1] if len(sys.argv) > 1 else ""
    app_secret = APP_SECRET or sys.argv[2] if len(sys.argv) > 2 else ""
    device_str = DEVICE_SERIAL or sys.argv[3] if len(sys.argv) > 3 else ""
    channel_str = CHANNEL_NO or (sys.argv[4] if len(sys.argv) > 4 else "1")
    
    # Parse device list (supports multiple devices)
    devices = parse_device_list(device_str, channel_str)
    
    if not devices:
        print("[ERROR] At least one device serial required.")
        print("[INFO] Format: \"device1,device2,device3\" or \"device1:1,device2:2\"")
        print("[INFO] Set EZVIZ_DEVICE_SERIAL env var or pass as argument.")
        sys.exit(1)
    
    print(f"[INFO] Detected {len(devices)} device(s): {devices}")
    
    # Step 0: Get access token
    if not app_key or not app_secret:
        print("[ERROR] APP_KEY and APP_SECRET required.")
        print("[INFO] Set EZVIZ_APP_KEY and EZVIZ_APP_SECRET env vars.")
        sys.exit(1)
    
    token_result = get_access_token(app_key, app_secret)
    if not token_result["success"]:
        print(f"[ERROR] Failed to get token: {token_result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    access_token = token_result["access_token"]
    expire_time = token_result.get("expire_time", 0)
    expire_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time / 1000))
    print(f"[INFO] Token obtained, expires: {expire_str}")
    
    # Track detection results
    detection_summary = {
        "total": len(devices),
        "detected": 0,
        "not_detected": 0,
        "failed": 0,
        "alerts_sent": 0
    }
    
    # Process each device
    for device_serial, channel_no in devices:
        print(f"\n{'='*60}")
        print(f"[Device] {device_serial} (Channel: {channel_no})")
        print(f"{'='*60}")
        
        # Step 1: Capture device image
        capture_result = capture_device_image(access_token, device_serial, channel_no)
        
        if not capture_result["success"]:
            print(f"[ERROR] Capture failed: {capture_result.get('error', 'Unknown error')}")
            detection_summary["failed"] += 1
            continue
        
        image_url = capture_result["pic_url"]
        print(f"[INFO] Image captured: {image_url[:50]}...")
        
        # Step 2: Detect phone usage
        detection_result = detect_phone_usage(image_url, access_token)
        
        if not detection_result["success"]:
            print(f"[ERROR] Detection failed: {detection_result.get('error', 'Unknown error')}")
            detection_summary["failed"] += 1
            continue
        
        if detection_result["is_phone_detected"]:
            print(f"[ALERT] Phone usage detected! (confidence: {detection_result['confidence']:.2f})")
            detection_summary["detected"] += 1
            
            # Step 3: Generate TTS audio
            alert_text = "检测到有人玩手机"
            audio_path = generate_tts_audio(alert_text)
            
            if not audio_path:
                print(f"[ERROR] TTS generation failed")
                continue
            
            # Step 4: Upload voice file
            upload_result = upload_voice_file(audio_path, access_token)
            
            if not upload_result["success"]:
                print(f"[ERROR] Voice upload failed: {upload_result.get('error', 'Unknown error')}")
                continue
            
            voice_url = upload_result["voice_url"]
            print(f"[INFO] Voice uploaded: {voice_url[:60]}...")
            
            # Step 5: Send voice to device
            send_result = send_voice_to_device(device_serial, voice_url, access_token, channel_no)
            
            if send_result["success"]:
                print(f"[SUCCESS] Alert sent to device {device_serial}!")
                detection_summary["alerts_sent"] += 1
            else:
                print(f"[ERROR] Failed to send alert: {send_result.get('error', 'Unknown error')}")
        else:
            print("[INFO] No phone usage detected.")
            detection_summary["not_detected"] += 1
    
    if not detection_result["success"]:
        print(f"[ERROR] Detection failed: {detection_result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    if detection_result["is_phone_detected"]:
        print(f"[ALERT] Phone usage detected! (confidence: {detection_result['confidence']:.2f})")
        
        # Step 3: Generate TTS audio
        alert_text = "检测到有人玩手机"
        audio_path = generate_tts_audio(alert_text)
        
        # Step 4: Upload voice file
        upload_result = upload_voice_file(audio_path, access_token)
        
        if not upload_result["success"]:
            print(f"[ERROR] Voice upload failed: {upload_result.get('error', 'Unknown error')}")
            sys.exit(1)
        
        voice_url = upload_result["voice_url"]
        print(f"[INFO] Voice uploaded: {voice_url}")
        
        # Step 5: Send voice to device
        if device_serial:
            send_result = send_voice_to_device(
                device_serial, voice_url, access_token, channel_no
            )
            
            if send_result["success"]:
                print("[SUCCESS] Alert sent to device successfully!")
            else:
                print(f"[ERROR] Failed to send alert: {send_result.get('error', 'Unknown error')}")
                sys.exit(1)
        else:
            print("[INFO] Device serial not provided. Voice uploaded but not sent.")
        
    else:
        print("[INFO] No phone usage detected. No alert needed.")
        detection_summary["not_detected"] += 1
    
    # Print summary
    print(f"\n{'='*60}")
    print("DETECTION SUMMARY")
    print(f"{'='*60}")
    print(f"  Total devices:     {detection_summary['total']}")
    print(f"  Phone detected:    {detection_summary['detected']}")
    print(f"  Not detected:      {detection_summary['not_detected']}")
    print(f"  Failed:            {detection_summary['failed']}")
    print(f"  Alerts sent:       {detection_summary['alerts_sent']}")
    print(f"{'='*60}")
    
    if detection_summary["detected"] > 0:
        print(f"[RESULT] {detection_summary['detected']}/{detection_summary['total']} device(s) detected phone usage")
        print(f"[ACTION] {detection_summary['alerts_sent']} alert(s) sent successfully")
    else:
        print("[RESULT] No phone usage detected on any device")
    
    print("=" * 60)
    print("Workflow completed")
    print("=" * 60)


def test_alert_workflow(access_token, device_str, channel_str="1"):
    """
    Test the complete alert workflow without detection.
    This is for testing purposes only.
    
    Supports multiple devices.
    """
    print("=" * 60)
    print("Phone Detection Alert System - TEST MODE")
    print("=" * 60)
    
    devices = parse_device_list(device_str, channel_str)
    
    if not devices:
        print("[ERROR] No devices specified")
        return False
    
    print(f"[TEST] Testing alert workflow on {len(devices)} device(s): {devices}")
    
    results = {"success": 0, "failed": 0}
    
    for device_serial, channel_no in devices:
        print(f"\n{'='*60}")
        print(f"[Device] {device_serial} (Channel: {channel_no})")
        print(f"{'='*60}")
        
        # Step 1: Generate TTS audio
        alert_text = "检测到有人玩手机"
        print(f"\n[Step 1] Generating TTS: '{alert_text}'")
        audio_path = generate_tts_audio(alert_text)
        
        if not audio_path or not os.path.exists(audio_path):
            print(f"[ERROR] TTS audio file not created: {audio_path}")
            results["failed"] += 1
            continue
        
        # Step 2: Upload voice file
        print(f"\n[Step 2] Uploading voice file: {audio_path}")
        upload_result = upload_voice_file(audio_path, access_token)
        
        if not upload_result["success"]:
            print(f"[ERROR] Voice upload failed: {upload_result.get('error', 'Unknown error')}")
            results["failed"] += 1
            continue
        
        voice_url = upload_result["voice_url"]
        print(f"[SUCCESS] Voice uploaded: {voice_url[:60]}...")
        
        # Step 3: Send voice to device
        print(f"\n[Step 3] Sending voice to device: {device_serial}")
        send_result = send_voice_to_device(device_serial, voice_url, access_token, channel_no)
        
        if send_result["success"]:
            print(f"[SUCCESS] Alert sent to device {device_serial}!")
            results["success"] += 1
        else:
            print(f"[ERROR] Failed to send alert: {send_result.get('error', 'Unknown error')}")
            results["failed"] += 1
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"  Total devices:  {len(devices)}")
    print(f"  Success:        {results['success']}")
    print(f"  Failed:         {results['failed']}")
    print(f"{'='*60}")
    
    if results["failed"] == 0:
        print("TEST COMPLETED - All steps passed!")
        return True
    else:
        print("TEST COMPLETED - Some devices failed")
        return False


if __name__ == "__main__":
    # Check if test mode is requested
    if len(sys.argv) > 5 and sys.argv[5] == "--test":
        # Test mode: skip detection, test alert workflow
        app_key = APP_KEY or sys.argv[1] if len(sys.argv) > 1 else ""
        app_secret = APP_SECRET or sys.argv[2] if len(sys.argv) > 2 else ""
        device_str = DEVICE_SERIAL or sys.argv[3] if len(sys.argv) > 3 else ""
        channel_str = CHANNEL_NO or (sys.argv[4] if len(sys.argv) > 4 else "1")
        
        if not app_key or not app_secret:
            print("[ERROR] APP_KEY and APP_SECRET required")
            sys.exit(1)
        
        # Get token
        token_result = get_access_token(app_key, app_secret)
        if not token_result["success"]:
            print(f"[ERROR] Failed to get token: {token_result.get('error')}")
            sys.exit(1)
        
        access_token = token_result["access_token"]
        
        if not device_str:
            print("[ERROR] Device serial required")
            sys.exit(1)
        
        success = test_alert_workflow(access_token, device_str, channel_str)
        sys.exit(0 if success else 1)
    else:
        # Normal mode: full detection workflow
        main()
