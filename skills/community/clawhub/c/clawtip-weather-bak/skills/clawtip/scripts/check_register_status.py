import sys
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path


def get_public_key():
    """
    从域名获取base64编码后公钥
    """
    api_url = "https://ms.jr.jd.com/gw2/generic/hyqy/h5/m/getSMPublicKey"
    try:
        response = requests.post(api_url, timeout=10)
        response.raise_for_status()
        try:
            result = response.json()
            pub_key = result.get("resultData")
            key = pub_key if pub_key else response.text.strip()
        except json.JSONDecodeError:
            key = response.text.strip()
        return key
    except Exception as e:
        print(f"获取公钥失败: {e}")
        return None


def query_register_status(device_id: str):
    """
    Query the token register status from the API.
    """
    now = datetime.now()
    request_no = device_id
    request_time = "{:.0f}".format(now.timestamp() * 1000)
    sign_raw = request_no + request_time

    # 获取公钥并使用 encrypt.js 对 sign 进行 RSA 加密
    base64_pub_key = get_public_key()
    if not base64_pub_key:
        print("未能获取到公钥，无法加密 sign。")
        return False, None

    try:
        current_dir = Path(__file__).parent.absolute()
        js_script_path = current_dir / 'encrypt.js'
        result_sign = subprocess.run(
            ["node", str(js_script_path), sign_raw, base64_pub_key],
            capture_output=True,
            text=True,
            check=True
        )
        sign = result_sign.stdout.strip()
        print("成功调用 encrypt.js 对 sign 进行了加密。")
    except subprocess.CalledProcessError as e:
        print(f"调用加密脚本时失败: {e.stderr if hasattr(e, 'stderr') else e}")
        return False, None
    except Exception as e:
        print(f"执行加密脚本时发生异常: {e}")
        return False, None

    url = f"https://ms.jr.jd.com/gw2/generic/hyqy/h5/m/queryToken"

    body = {
        "requestNo": request_no,
        "requestTime": request_time,
        "sign": sign,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=body, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        if not result.get('success', False):
            print(f"API Error: {result.get('resultMsg', 'Unknown error')}")
            return False, result
        result_data = result.get("resultData", {})
        if "status" in result_data and result_data["status"] == "PROCESSING":
            count = result_data.get("times", 0)
            print(f"Status: processing (count: {count})")
            return False, result
        elif "tokenInfo" in result_data:
            user_token = result_data.get("tokenInfo", "")
            print(f"Status: successful")
            
            # Save the token to config
            save_token(user_token)
            return True, result
        else:
            print("Unknown response format")
            return False, result
            
    except requests.exceptions.RequestException as e:
        print(f"Error querying API: {e}")
        return False, None
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        return False, None

def save_token(token: str):
    """
    Save the obtained u to configs/config.json
    """
    current_dir = Path(__file__).parent.absolute()
    parent_dir = current_dir.parent
    config_dir = parent_dir / 'configs'
    config_file = config_dir / 'config.json'
    
    config_dir.mkdir(exist_ok=True)
    
    config_data = {}
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        except Exception:
            pass
            
    config_data['u'] = token
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False)
        print(f"Saved u")
    except Exception as e:
        print(f"Error saving config: {e}")

if __name__ == "__main__":
    device_id = "default"
    if len(sys.argv) > 1:
        device_id = sys.argv[1]
    
    query_register_status(device_id)
