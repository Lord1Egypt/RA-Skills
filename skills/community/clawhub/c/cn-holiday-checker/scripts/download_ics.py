import os
import requests
import json

# 获取当前脚本所在目录的父目录（即项目根目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 修改为读取 JSON 文件
ENV_PATH = os.path.join(BASE_DIR, 'config.json')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'cn_zh.ics')

def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            return json.load(f)
    return {}

def download_ics():
    env = load_env()
    urls = [env.get('PRIMARY_URL'), env.get('BACKUP_URL')]
    
    for url in urls:
        if not url:
            continue
        try:
            print(f"正在尝试下载: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(DATA_PATH, 'wb') as f:
                f.write(response.content)
            print(f"成功下载至: {DATA_PATH}")
            return True
        except Exception as e:
            print(f"下载失败: {url}, 错误: {e}")
    
    print("所有源下载均失败。")
    return False

if __name__ == "__main__":
    download_ics()
