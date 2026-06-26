import os
import requests
from pathlib import Path
from typing import Optional

BASE_URL = "http://info.aicodingyard.com"

def _parse_dotenv_value(env_file: Path, key: str) -> Optional[str]:
    if not env_file.exists():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            if k.strip() == key:
                return v.strip()
    return None

def get_token() -> str:
    token = os.environ.get("BITSOUL_TOKEN")
    if token:
        return token
    env_file = os.environ.get("BITSOUL_TOKEN_ENV_FILE")
    if env_file:
        token_from_file = _parse_dotenv_value(Path(env_file).expanduser(), "BITSOUL_TOKEN")
        if token_from_file:
            return token_from_file
    return ""

def request_download_url(file_name: str, token_key: str) -> str:
    url = f"{BASE_URL}/api/download_file"
    params = {
        "file_name": file_name,
        "token_key": token_key
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            download_url = data.get("download_url", "")
            return download_url
        else:
            return ""
    except Exception as e:
        print(f"request_download_url error: {e}")
        return ""

def download_data_file(file_name: str, output_path: str, max_retries: int = 3) -> bool:
    token = get_token()
    if not token:
        print("Error: No token set, cannot download data file.")
        return False

    for retry in range(max_retries):
        try:
            download_url = request_download_url(file_name, token)
            if not download_url:
                print(f"Error: Failed to get download url for {file_name}, please check if your token is valid.")
                return False

            print(f"Starting to download {file_name} ...")
            print(f"Download url: {download_url}")

            with requests.get(download_url, stream=True, timeout=300) as response:
                if response.status_code != 200:
                    print(f"Download failed, HTTP status code: {response.status_code}")
                    if retry < max_retries - 1:
                        print(f"Retrying {retry + 1}/{max_retries} ...")
                        continue
                    return False

                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                chunk_size = 1024 * 1024

                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                pct = (downloaded / total_size) * 100
                                if downloaded % (10 * chunk_size) < chunk_size:
                                    print(f"Download progress: {pct:.1f}%")

            print(f"File downloaded successfully: {output_path}")
            return True

        except Exception as e:
            print(f"Download error: {str(e)}")
            if retry < max_retries - 1:
                print(f"Retrying {retry + 1}/{max_retries} ...")
            else:
                print("Download failed, reached maximum retries.")
                return False

    return False

def init():
    import platform
    import stat
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    is_windows = platform.system().lower() == 'windows'
    exe_name = "BitSoulBeauty.exe" if is_windows else "BitSoulBeauty"
    
    exe_file = os.path.join(current_dir, exe_name)
    if not os.path.exists(exe_file):
        print(f"Local file {exe_name} not found, downloading from server...")
        if not download_data_file(exe_name, exe_file, max_retries=3):
            print(f"Error: {exe_name} download failed, initialization aborted.")
            return
            
        # Give execution permission on Mac/Linux
        if not is_windows:
            st = os.stat(exe_file)
            os.chmod(exe_file, st.st_mode | stat.S_IEXEC)
        
if __name__ == "__main__":
    init()
