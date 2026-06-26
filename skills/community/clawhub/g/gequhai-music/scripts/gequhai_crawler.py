#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
歌曲海(Gequhai)音乐爬虫
https://www.gequhai.com/
支持搜索歌曲、获取下载链接（优先无损/高品质）
支持下载到群晖NAS并自动重命名
"""

import requests
import re
import base64
import json
import time
from typing import Optional, List, Dict
from bs4 import BeautifulSoup
from pathlib import Path

# 全局配置
BASE_URL = "https://www.gequhai.com"
DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_FILE = DATA_DIR / "music_cache.json"
RENAME_QUEUE_FILE = DATA_DIR / "rename_queue.json"

# 全局Session（保持cookie）
_SESSION = None

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": BASE_URL,
}


def get_session() -> requests.Session:
    """获取全局Session"""
    global _SESSION
    if _SESSION is None:
        _SESSION = requests.Session()
    return _SESSION


def decode_modified_base64(encoded: str) -> Optional[str]:
    """
    解码歌曲海的特殊base64编码
    将 # 替换为 H，% 替换为 S
    """
    try:
        modified = encoded.replace("#", "H").replace("%", "S")
        decoded = base64.b64decode(modified).decode("utf-8")
        return decoded
    except Exception as e:
        print(f"[解码失败] {e}")
        return None


def search_songs(keyword: str, page: int = 1) -> List[Dict]:
    """
    搜索歌曲
    :param keyword: 搜索关键词（歌名/歌手）
    :param page: 页码
    :return: 歌曲列表
    """
    url = f"{BASE_URL}/s/{keyword}"
    if page > 1:
        url = f"{BASE_URL}/s/{keyword}/{page}"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        
        soup = BeautifulSoup(resp.text, "html.parser")
        songs = []
        
        # 解析歌曲列表
        for tr in soup.select("table tbody tr"):
            tds = tr.select("td")
            if len(tds) >= 3:
                # 获取歌曲链接和ID
                link = tds[1].select_one("a")
                if link:
                    href = link.get("href", "")
                    # 提取ID: /play/553
                    song_id = href.split("/")[-1] if href else None
                    
                    songs.append({
                        "id": song_id,
                        "title": link.get_text(strip=True),
                        "artist": tds[2].get_text(strip=True),
                        "play_url": f"{BASE_URL}{href}" if href else None
                    })
        
        print(f"[搜索成功] 找到 {len(songs)} 首歌曲")
        return songs
    
    except Exception as e:
        print(f"[搜索失败] {e}")
        return []


def get_song_detail(song_id: str) -> Dict:
    """
    获取歌曲详情和下载链接
    :param song_id: 歌曲ID
    :return: 歌曲详情（包含下载链接）
    """
    url = f"{BASE_URL}/play/{song_id}"
    session = get_session()
    
    try:
        resp = session.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 提取页面中的JavaScript变量
        script_text = resp.text
        
        info = {"id": song_id, "play_url": url}
        
        # 提取 mp3_title
        match = re.search(r"window\.mp3_title\s*=\s*['\"]([^'\"]+)['\"]", script_text)
        if match:
            info["title"] = match.group(1)
        
        # 提取 mp3_author
        match = re.search(r"window\.mp3_author\s*=\s*['\"]([^'\"]+)['\"]", script_text)
        if match:
            info["artist"] = match.group(1)
        
        # 提取 mp3_cover
        match = re.search(r"window\.mp3_cover\s*=\s*['\"]([^'\"]+)['\"]", script_text)
        if match:
            info["cover"] = match.group(1)
        
        # 提取 mp3_type (0=普通, 1=特殊)
        match = re.search(r"window\.mp3_type\s*=\s*(\d+)", script_text)
        if match:
            info["type"] = int(match.group(1))
        
        # 提取 play_id (用于API请求)
        match = re.search(r"window\.play_id\s*=\s*['\"]([^'\"]+)['\"]", script_text)
        if match:
            info["play_id"] = match.group(1)
        
        # 提取 mp3_extra_url (高品质下载链接，base64编码)
        match = re.search(r"window\.mp3_extra_url\s*=\s*['\"]([^'\"]+)['\"]", script_text)
        if match:
            extra_url = match.group(1)
            if extra_url:
                decoded_url = decode_modified_base64(extra_url)
                if decoded_url:
                    info["download_url_hq"] = decoded_url
        
        # 获取歌词
        lrc_div = soup.select_one("#content-lrc2")
        if lrc_div:
            info["lyrics"] = lrc_div.get_text(strip=True)
        
        print(f"[获取成功] {info.get('title', 'Unknown')} - {info.get('artist', 'Unknown')}")
        return info
    
    except Exception as e:
        print(f"[获取失败] {e}")
        return {"id": song_id, "error": str(e)}


def get_download_url(song_id: str, play_id: str = None) -> Dict:
    """
    获取歌曲下载链接
    :param song_id: 歌曲ID
    :param play_id: 播放ID（可选）
    :return: 下载链接信息
    """
    session = get_session()
    
    # 先获取歌曲详情页面（同时获取cookie）
    detail = get_song_detail(song_id)
    
    result = {
        "song_id": song_id,
        "title": detail.get("title"),
        "artist": detail.get("artist"),
    }
    
    # 检查高品质链接类型
    hq_url = detail.get("download_url_hq")
    if hq_url:
        # 判断是否为直接下载链接
        if any(ext in hq_url.lower() for ext in [".mp3", ".flac", ".m4a", ".wav"]):
            result["url_hq"] = hq_url
            result["quality_hq"] = "高品质/SQ"
            result["format_hq"] = hq_url.split(".")[-1] if "." in hq_url else "mp3"
        else:
            # 网盘链接，记录下来
            result["netdisk_url"] = hq_url
            result["netdisk_type"] = "夸克网盘" if "quark" in hq_url else "网盘"
    
    # 通过API获取标准品质链接（需要正确的header和cookie）
    if play_id or detail.get("play_id"):
        api_url = f"{BASE_URL}/api/music"
        try:
            # 关键：需要带上这个header！
            api_headers = {
                **HEADERS,
                "X-Requested-With": "XMLHttpRequest",
                "X-Custom-Header": "SecretKey",  # 网站需要的secret key
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": BASE_URL,
                "Referer": f"{BASE_URL}/play/{song_id}",
            }
            
            resp = session.post(
                api_url,
                headers=api_headers,
                data={
                    "id": play_id or detail.get("play_id"),
                    "type": detail.get("type", 0)
                },
                timeout=10
            )
            data = resp.json()
            if data.get("code") == 200:
                result["url"] = data["data"]["url"]
                result["quality"] = "标准品质"
                result["format"] = "mp3"
                return result
            else:
                print(f"[API返回错误] code={data.get('code')}, msg={data.get('msg')}")
        except Exception as e:
            print(f"[API获取失败] {e}")
    
    # 如果只有网盘链接
    if result.get("netdisk_url"):
        result["quality"] = "高品质(网盘)"
        result["note"] = "需要手动从网盘下载"
    
    return result


def get_hot_songs() -> List[Dict]:
    """获取热门歌曲"""
    url = f"{BASE_URL}/hot-music/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        
        soup = BeautifulSoup(resp.text, "html.parser")
        songs = []
        
        for tr in soup.select("table tbody tr"):
            tds = tr.select("td")
            if len(tds) >= 2:
                link = tds[1].select_one("a")
                if link:
                    href = link.get("href", "")
                    song_id = href.split("/")[-1] if href else None
                    songs.append({
                        "id": song_id,
                        "title": link.get_text(strip=True),
                        "artist": tds[2].get_text(strip=True) if len(tds) > 2 else "",
                        "play_url": f"{BASE_URL}{href}" if href else None
                    })
        
        return songs
    except Exception as e:
        print(f"[获取热门歌曲失败] {e}")
        return []


def get_top_songs(category: str = "new") -> List[Dict]:
    """
    获取排行榜歌曲
    :param category: 分类 (new/surge/douyin/jingdian/dianyin/wwdj)
    """
    url = f"{BASE_URL}/top/{category}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        
        soup = BeautifulSoup(resp.text, "html.parser")
        songs = []
        
        for tr in soup.select("table tbody tr"):
            tds = tr.select("td")
            if len(tds) >= 2:
                link = tds[1].select_one("a")
                if link:
                    href = link.get("href", "")
                    song_id = href.split("/")[-1] if href else None
                    songs.append({
                        "id": song_id,
                        "title": link.get_text(strip=True),
                        "artist": tds[2].get_text(strip=True) if len(tds) > 2 else "",
                        "play_url": f"{BASE_URL}{href}" if href else None
                    })
        
        return songs
    except Exception as e:
        print(f"[获取排行榜失败] {e}")
        return []


# ============ 群晖下载相关函数 ============

SYNOLOGY_HOST = "192.168.123.223"
SYNOLOGY_PORT = "5000"
SYNOLOGY_USER = "xiaoai"
SYNOLOGY_PASS = "Xx654321"
DEFAULT_MUSIC_DIR = "download/音乐下载"
FINAL_MUSIC_DIR = "music/AI音乐文件夹"  # 最终存放位置


def syno_login(session: str = "DownloadStation") -> Optional[str]:
    """登录群晖获取SID"""
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/entry.cgi"
    params = {
        "api": "SYNO.API.Auth",
        "version": 6,
        "method": "login",
        "account": SYNOLOGY_USER,
        "passwd": SYNOLOGY_PASS,
        "session": session,
        "format": "sid"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("success"):
            return data["data"]["sid"]
    except Exception as e:
        print(f"[登录失败] {e}")
    return None


def syno_logout(sid: str, session: str = "DownloadStation") -> bool:
    """登出群晖"""
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/entry.cgi"
    params = {
        "api": "SYNO.API.Auth",
        "version": 6,
        "method": "logout",
        "session": session,
        "_sid": sid
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        return resp.json().get("success", False)
    except:
        return False


def syno_add_download(uri: str, destination: str = DEFAULT_MUSIC_DIR) -> Dict:
    """
    添加下载任务到群晖
    :param uri: 下载链接
    :param destination: 下载目录
    :return: 下载结果
    """
    sid = syno_login()
    if not sid:
        return {"success": False, "error": "登录失败"}
    
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/DownloadStation/task.cgi"
    data = {
        "api": "SYNO.DownloadStation.Task",
        "version": 1,
        "method": "create",
        "uri": uri,
        "destination": destination,
        "_sid": sid
    }
    
    try:
        resp = requests.post(url, data=data, timeout=15)
        result = resp.json()
        
        if result.get("success"):
            task_id = result.get("data", {}).get("id", "unknown")
            return {"success": True, "task_id": task_id, "sid": sid}
        else:
            error_code = result.get("error", {}).get("code", "unknown")
            return {"success": False, "error": f"错误码: {error_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        syno_logout(sid)


def syno_get_task_status(task_id: str, sid: str = None) -> Dict:
    """
    获取下载任务状态
    :param task_id: 任务ID
    :param sid: Session ID（可选）
    :return: 任务状态
    """
    need_logout = False
    if not sid:
        sid = syno_login()
        need_logout = True
    
    if not sid:
        return {"success": False, "error": "登录失败"}
    
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/DownloadStation/task.cgi"
    params = {
        "api": "SYNO.DownloadStation.Task",
        "version": 1,
        "method": "list",
        "additional": "transfer",
        "_sid": sid
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        result = resp.json()
        
        if result.get("success"):
            tasks = result.get("data", {}).get("tasks", [])
            for task in tasks:
                if task.get("id") == task_id:
                    return {
                        "success": True,
                        "status": task.get("status"),
                        "title": task.get("title"),
                        "size": task.get("size"),
                        "transfer": task.get("additional", {}).get("transfer", {})
                    }
            return {"success": False, "error": "未找到任务"}
        else:
            return {"success": False, "error": "获取任务列表失败"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if need_logout:
            syno_logout(sid)


def syno_rename_file(file_path: str, new_name: str, sid: str = None) -> Dict:
    """
    重命名群晖文件
    :param file_path: 文件路径
    :param new_name: 新文件名
    :param sid: Session ID（可选）
    :return: 重命名结果
    """
    need_logout = False
    if not sid:
        sid = syno_login("FileStation")
        need_logout = True
    
    if not sid:
        return {"success": False, "error": "登录失败"}
    
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/entry.cgi"
    params = {
        "api": "SYNO.FileStation.Rename",
        "version": 1,
        "method": "rename",
        "path": file_path,
        "name": new_name,
        "_sid": sid
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        result = resp.json()
        
        if result.get("success"):
            return {"success": True, "new_path": result.get("data", {}).get("files", [{}])[0].get("path")}
        else:
            return {"success": False, "error": result.get("error", {}).get("errors", [{}])[0].get("reason", "未知错误")}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if need_logout:
            syno_logout(sid, "FileStation")


def syno_list_files(folder_path: str, sid: str = None) -> Dict:
    """
    列出群晖文件夹内容
    :param folder_path: 文件夹路径
    :param sid: Session ID（可选）
    :return: 文件列表
    """
    need_logout = False
    if not sid:
        sid = syno_login("FileStation")
        need_logout = True
    
    if not sid:
        return {"success": False, "error": "登录失败"}
    
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/entry.cgi"
    params = {
        "api": "SYNO.FileStation.List",
        "version": 2,
        "method": "list",
        "folder_path": folder_path,
        "_sid": sid
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        result = resp.json()
        
        if result.get("success"):
            return {"success": True, "files": result.get("data", {}).get("files", [])}
        else:
            return {"success": False, "error": "获取文件列表失败"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if need_logout:
            syno_logout(sid, "FileStation")


def syno_move_file(src_path: str, dest_folder: str, sid: str = None) -> Dict:
    """
    移动文件到指定目录
    :param src_path: 源文件路径
    :param dest_folder: 目标目录
    :param sid: Session ID（可选）
    :return: 移动结果
    """
    need_logout = False
    if not sid:
        sid = syno_login("FileStation")
        need_logout = True
    
    if not sid:
        return {"success": False, "error": "登录失败"}
    
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/entry.cgi"
    
    # 使用 CopyMove API 移动文件
    data = {
        "api": "SYNO.FileStation.CopyMove",
        "version": 2,
        "method": "start",
        "path": f'["{src_path}"]',
        "dest_folder_path": f'"{dest_folder}"',
        "overwrite": "true",
        "remove_src": "true",  # 移动而不是复制
        "_sid": sid
    }
    
    try:
        resp = requests.post(url, data=data, timeout=15)
        result = resp.json()
        
        if result.get("success"):
            task_id = result.get("data", {}).get("taskid", "")
            return {"success": True, "task_id": task_id}
        else:
            return {"success": False, "error": result.get("error", {}).get("code", "未知错误")}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if need_logout:
            syno_logout(sid, "FileStation")


def extract_filename_from_url(url: str) -> str:
    """从URL中提取文件名"""
    # 从URL路径中提取
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    filename = path.split("/")[-1] if path else ""
    # 移除查询参数
    if "?" in filename:
        filename = filename.split("?")[0]
    return filename


def save_rename_queue(queue: List[Dict]):
    """保存重命名队列"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(RENAME_QUEUE_FILE, "w", encoding="utf-8", newline="") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


# 移动队列文件
MOVE_QUEUE_FILE = DATA_DIR / "move_queue.json"


def load_move_queue() -> List[Dict]:
    """加载移动队列"""
    if MOVE_QUEUE_FILE.exists():
        try:
            with open(MOVE_QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_move_queue(queue: List[Dict]):
    """保存移动队列"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(MOVE_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def add_to_move_queue(file_path: str, dest_folder: str, renamed_name: str = None):
    """添加到移动队列"""
    queue = load_move_queue()
    queue.append({
        "file_path": file_path,
        "dest_folder": dest_folder,
        "renamed_name": renamed_name,
        "timestamp": time.time()
    })
    save_move_queue(queue)
    print(f"[添加移动队列] {file_path} -> {dest_folder}")


def load_rename_queue() -> List[Dict]:
    """加载重命名队列"""
    if RENAME_QUEUE_FILE.exists():
        try:
            with open(RENAME_QUEUE_FILE, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except:
            return []
    return []


def add_to_rename_queue(original_name: str, target_name: str, destination: str, task_id: str = None):
    """
    添加到重命名队列
    :param original_name: 原始文件名（乱码名）
    :param target_name: 目标文件名（歌名-歌手.mp3）
    :param destination: 下载目录
    :param task_id: 下载任务ID（可选）
    """
    # 确保路径以 / 开头
    if not destination.startswith("/"):
        destination = "/" + destination
    
    queue = load_rename_queue()
    queue.append({
        "original_name": original_name,
        "target_name": target_name,
        "destination": destination,
        "task_id": task_id,
        "added_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    save_rename_queue(queue)
    print(f"[添加重命名队列] {original_name} -> {target_name}")


def process_rename_queue():
    """处理重命名队列，检查下载完成的文件并重命名"""
    queue = load_rename_queue()
    if not queue:
        print("[重命名队列] 队列为空")
        return
    
    sid = syno_login("FileStation")
    if not sid:
        print("[重命名失败] 无法登录群晖")
        return
    
    remaining = []
    
    for item in queue:
        original_name = item["original_name"]
        target_name = item["target_name"]
        destination = item["destination"]
        file_path = f"{destination}/{original_name}"
        
        # 尝试重命名
        result = syno_rename_file(file_path, target_name, sid)
        
        if result.get("success"):
            print(f"[重命名成功] {original_name} -> {target_name}")
        else:
            # 如果文件还不存在或其他错误，保留在队列中
            print(f"[重命名失败] {original_name}: {result.get('error')}")
            remaining.append(item)
    
    syno_logout(sid, "FileStation")
    save_rename_queue(remaining)


def auto_process_downloads():
    """
    自动处理下载目录中的文件：
    1. 检查重命名队列，重命名完成的文件
    2. 重命名成功后移动到最终目录 /music/AI音乐文件夹/
    """
    print("=== 自动处理下载文件 ===")
    
    # 1. 处理重命名队列
    queue = load_rename_queue()
    if not queue:
        print("[重命名队列] 为空，跳过")
        return {"success": True, "processed": [], "remaining": 0}
    
    print(f"[重命名队列] 有 {len(queue)} 个待处理任务")
    
    sid = syno_login("FileStation")
    if not sid:
        print("[处理失败] 无法登录群晖")
        return {"success": False, "error": "登录失败"}
    
    remaining = []
    processed = []
    
    for item in queue:
        original_name = item["original_name"]
        target_name = item["target_name"]
        destination = item.get("destination", DEFAULT_MUSIC_DIR)
        
        # 确保路径格式正确
        if not destination.startswith("/"):
            destination = "/" + destination
        
        file_path = f"{destination}/{original_name}"
        
        # 尝试重命名
        result = syno_rename_file(file_path, target_name, sid)
        
        if result.get("success"):
            print(f"[重命名成功] {original_name} -> {target_name}")
            
            # 重命名成功，移动到最终目录
            renamed_path = f"{destination}/{target_name}"
            final_dir = "/music/AI音乐文件夹"
            
            move_result = syno_move_file(renamed_path, final_dir, sid)
            
            if move_result.get("success"):
                print(f"[移动成功] {target_name} -> {final_dir}")
                processed.append({
                    "original_name": original_name,
                    "target_name": target_name,
                    "final_path": f"{final_dir}/{target_name}"
                })
            else:
                print(f"[移动失败] {move_result.get('error')}")
                # 添加到移动队列
                add_to_move_queue(renamed_path, final_dir, target_name)
                remaining.append(item)
        else:
            # 文件可能还没下载完，保留在队列
            error = result.get("error", "")
            if "not found" in str(error).lower() or "不存在" in str(error) or "未知错误" in str(error):
                print(f"[等待中] 文件尚未就绪: {original_name}")
            else:
                print(f"[重命名失败] {original_name}: {error}")
            remaining.append(item)
    
    syno_logout(sid, "FileStation")
    save_rename_queue(remaining)
    
    return {
        "success": True,
        "processed": processed,
        "remaining": len(remaining)
    }


def download_song(song: Dict, destination: str = DEFAULT_MUSIC_DIR, auto_rename: bool = True) -> Dict:
    """
    下载歌曲到群晖
    :param song: 歌曲信息（需包含下载链接）
    :param destination: 下载目录
    :param auto_rename: 是否自动重命名
    :return: 下载结果
    """
    url = song.get("url") or song.get("download_url_hq") or song.get("download_url")
    
    if not url:
        # 需要先获取下载链接
        song_id = song.get("id")
        if song_id:
            detail = get_download_url(song_id)
            url = detail.get("url")
            song = {**song, **detail}
    
    if not url:
        return {"success": False, "error": "没有下载链接"}
    
    result = syno_add_download(url, destination)
    
    if result["success"]:
        title = song.get("title", "Unknown")
        artist = song.get("artist", "")
        print(f"[下载成功] {title} - {artist}")
        
        # 自动重命名
        if auto_rename:
            # 从URL提取原始文件名
            original_name = extract_filename_from_url(url)
            # 构建目标文件名
            ext = original_name.split(".")[-1] if "." in original_name else "mp3"
            # 清理文件名中的非法字符
            safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
            safe_artist = re.sub(r'[<>:"/\\|?*]', '', artist)
            target_name = f"{safe_title}-{safe_artist}.{ext}"
            
            # 添加到重命名队列
            add_to_rename_queue(
                original_name=original_name,
                target_name=target_name,
                destination=destination,
                task_id=result.get("task_id")
            )
            
            result["original_name"] = original_name
            result["target_name"] = target_name
            
            # 立即尝试重命名（可能文件还没下载完，会失败但不影响）
            try:
                sid = syno_login("FileStation")
                file_path = f"{destination}/{original_name}"
                rename_result = syno_rename_file(file_path, target_name, sid)
                
                if rename_result.get("success"):
                    print(f"[立即重命名成功] {original_name} -> {target_name}")
                    # 从队列中移除
                    queue = load_rename_queue()
                    queue = [q for q in queue if q.get("original_name") != original_name]
                    save_rename_queue(queue)
                    
                    # 重命名成功后，移动到最终目录
                    if FINAL_MUSIC_DIR and destination != FINAL_MUSIC_DIR:
                        renamed_path = f"{destination}/{target_name}"
                        move_result = syno_move_file(renamed_path, FINAL_MUSIC_DIR, sid)
                        if move_result.get("success"):
                            print(f"[移动成功] {target_name} -> {FINAL_MUSIC_DIR}")
                            result["final_path"] = f"{FINAL_MUSIC_DIR}/{target_name}"
                        else:
                            print(f"[移动失败] {move_result.get('error')}")
                            # 添加到移动队列稍后重试
                            add_to_move_queue(renamed_path, FINAL_MUSIC_DIR, target_name)
                
                syno_logout(sid, "FileStation")
            except Exception as e:
                print(f"[立即重命名失败] {e}，稍后会自动重试")
    else:
        print(f"[下载失败] {result.get('error')}")
    
    return result


def search_and_download(keyword: str, destination: str = DEFAULT_MUSIC_DIR) -> Dict:
    """
    搜索并下载歌曲
    :param keyword: 搜索关键词
    :param destination: 下载目录
    :return: 下载结果
    """
    # 搜索歌曲
    songs = search_songs(keyword)
    
    if not songs:
        return {"success": False, "error": "未找到歌曲"}
    
    # 获取第一首歌的详情和下载链接
    first_song = songs[0]
    detail = get_download_url(first_song["id"])
    
    # 下载
    return download_song(detail, destination)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="歌曲海音乐爬虫")
    parser.add_argument("--search", type=str, help="搜索歌曲")
    parser.add_argument("--hot", action="store_true", help="获取热门歌曲")
    parser.add_argument("--download", type=str, help="搜索并下载歌曲")
    parser.add_argument("--detail", type=str, help="获取歌曲详情（传入歌曲ID）")
    parser.add_argument("--auto", action="store_true", help="自动处理下载文件（重命名+移动）")
    parser.add_argument("--status", action="store_true", help="查看下载队列状态")
    
    args = parser.parse_args()
    
    if args.search:
        songs = search_songs(args.search)
        for s in songs[:10]:
            print(f"  [{s['id']}] {s['title']} - {s['artist']}")
    
    elif args.hot:
        songs = get_hot_songs()
        for s in songs[:10]:
            print(f"  [{s['id']}] {s['title']} - {s['artist']}")
    
    elif args.download:
        result = search_and_download(args.download)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.detail:
        detail = get_song_detail(args.detail)
        print(json.dumps(detail, ensure_ascii=False, indent=2))
    
    elif args.auto:
        result = auto_process_downloads()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.status:
        # 显示队列状态
        rename_queue = load_rename_queue()
        move_queue = load_move_queue()
        print(f"重命名队列: {len(rename_queue)} 个任务")
        for item in rename_queue:
            print(f"  {item['original_name']} -> {item['target_name']}")
        print(f"\n移动队列: {len(move_queue)} 个任务")
        for item in move_queue:
            print(f"  {item['file_path']} -> {item['dest_folder']}")
    
    else:
        # 默认测试
        print("测试搜索：周杰伦")
        songs = search_songs("周杰伦")
        for s in songs[:5]:
            print(f"  [{s['id']}] {s['title']} - {s['artist']}")
