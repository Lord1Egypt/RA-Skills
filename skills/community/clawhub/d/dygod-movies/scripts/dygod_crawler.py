#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电影天堂(DYGod)电影爬虫
爬取 https://dygod.net/html/gndy/dyzz/ 最新电影信息
支持查询最近更新、高分电影，获取下载链接
"""

import requests
import json
import re
import time
from datetime import datetime
from typing import Optional, List, Dict
from pathlib import Path
from bs4 import BeautifulSoup

# 全局配置
BASE_URL = "https://dygod.net"

# 电影分类
MOVIE_URL = f"{BASE_URL}/html/gndy/dyzz/"

# 电视剧分类
TV_URLS = {
    "国产剧": f"{BASE_URL}/html/tv/hytv/",
    "日韩剧": f"{BASE_URL}/html/tv/rihantv/",
    "欧美剧": f"{BASE_URL}/html/tv/oumeitv/",
}

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_FILE = DATA_DIR / "movies_cache.json"
TV_CACHE_FILE = DATA_DIR / "tv_cache.json"
CACHE_EXPIRE_SECONDS = 3600  # 缓存1小时


def get_headers() -> dict:
    """生成请求头"""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }


def get_page_html(url: str, retry: int = 3) -> Optional[str]:
    """获取页面HTML"""
    for i in range(retry):
        try:
            response = requests.get(url, headers=get_headers(), timeout=15)
            response.raise_for_status()
            response.encoding = "gb2312"
            return response.text
        except Exception as e:
            print(f"[错误] 获取页面失败 (尝试 {i+1}/{retry}): {e}")
            if i < retry - 1:
                time.sleep(2)
    return None


def parse_movie_list(html: str) -> List[Dict]:
    """解析电影列表页，提取电影基本信息和详情链接"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, "html.parser")
    movies = []
    
    # 查找所有电影链接 - 电影天堂的列表结构
    # <a href="/html/gndy/dyzz/20260312/12345.html" class="ulink">片名</a>
    for link in soup.select("a.ulink"):
        href = link.get("href", "")
        title = link.get_text(strip=True)
        
        if href and title and "/html/gndy/dyzz/" in href:
            movies.append({
                "title": title,
                "detail_url": BASE_URL + href if href.startswith("/") else href,
                "update_date": extract_date_from_url(href)
            })
    
    return movies


def extract_date_from_url(url: str) -> Optional[str]:
    """从URL中提取日期 (格式: /html/gndy/dyzz/20260312/xxx.html)"""
    match = re.search(r'/(\d{8})/', url)
    if match:
        date_str = match.group(1)
        try:
            return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
        except:
            pass
    return None


def parse_movie_detail(html: str, movie: Dict) -> Dict:
    """解析电影详情页，提取完整信息和下载链接"""
    if not html:
        return movie
    
    soup = BeautifulSoup(html, "html.parser")
    
    # 提取电影信息文本
    text_content = soup.get_text(separator="\n", strip=True)
    
    # 按字段解析
    info = {}
    lines = text_content.split("\n")
    
    def clean_value(text: str) -> str:
        """清理字段值，移除前缀符号"""
        # 移除开头的◎和其他特殊符号
        text = re.sub(r"^[◎\s]+", "", text).strip()
        # 如果以/开头，也移除
        text = re.sub(r"^/+", "", text).strip()
        return text
    
    for line in lines:
        line = line.strip()
        
        if "译　　名" in line or "译 名" in line:
            info["译名"] = clean_value(re.sub(r"译[　\s]*名[　\s]*", "", line))
        elif "片　　名" in line or "片 名" in line:
            info["片名"] = clean_value(re.sub(r"片[　\s]*名[　\s]*", "", line))
        elif "年　　代" in line or "年 代" in line:
            info["年代"] = clean_value(re.sub(r"年[　\s]*代[　\s]*", "", line))
        elif "产　　地" in line or "产 地" in line:
            info["产地"] = clean_value(re.sub(r"产[　\s]*地[　\s]*", "", line))
        elif "类　　别" in line or "类 别" in line:
            info["类别"] = clean_value(re.sub(r"类[　\s]*别[　\s]*", "", line))
        elif "语　　言" in line or "语 言" in line:
            info["语言"] = clean_value(re.sub(r"语[　\s]*言[　\s]*", "", line))
        elif "字　　幕" in line or "字 幕" in line:
            info["字幕"] = clean_value(re.sub(r"字[　\s]*幕[　\s]*", "", line))
        elif "上映日期" in line:
            info["上映日期"] = clean_value(re.sub(r"上映日期[　\s]*", "", line))
        elif "豆瓣评分" in line:
            score = clean_value(re.sub(r"豆瓣评分[　\s]*", "", line))
            # 提取评分数字
            match = re.search(r"([\d.]+)", score)
            if match:
                info["豆瓣评分"] = float(match.group(1))
        elif "IMDb评分" in line or "IMDb" in line:
            score = clean_value(re.sub(r"IMDb评分[　\s]*", "", line))
            match = re.search(r"([\d.]+)", score)
            if match:
                info["IMDb评分"] = float(match.group(1))
        elif "文件格式" in line:
            info["文件格式"] = clean_value(re.sub(r"文件格式[　\s]*", "", line))
        elif "视频尺寸" in line:
            info["视频尺寸"] = clean_value(re.sub(r"视频尺寸[　\s]*", "", line))
        elif "文件大小" in line:
            info["文件大小"] = clean_value(re.sub(r"文件大小[　\s]*", "", line))
        elif "片　　长" in line or "片 长" in line:
            info["片长"] = clean_value(re.sub(r"片[　\s]*长[　\s]*", "", line))
        elif "导　　演" in line or "导 演" in line:
            info["导演"] = clean_value(re.sub(r"导[　\s]*演[　\s]*", "", line))
        elif "主　　演" in line or "主 演" in line:
            info["主演"] = clean_value(re.sub(r"主[　\s]*演[　\s]*", "", line))
        elif "简　　介" in line or "简 介" in line:
            info["简介"] = clean_value(re.sub(r"简[　\s]*介[　\s]*", "", line))
    
    # 提取下载链接
    download_links = []
    for link in soup.select("a[href*='magnet:'], a[href*='ed2k:'], a[href*='ftp://'], a[href*='http']"):
        href = link.get("href", "")
        if any(proto in href for proto in ["magnet:", "ed2k:", "ftp://"]):
            download_links.append(href)
    
    # 查找 torrent 下载链接
    for link in soup.select("a[href*='.torrent']"):
        href = link.get("href", "")
        if href.startswith("/"):
            href = BASE_URL + href
        download_links.append(href)
    
    info["download_links"] = list(set(download_links))
    
    # 合并信息
    movie.update(info)
    return movie


def crawl_movies(max_pages: int = 1, fetch_detail: bool = True) -> List[Dict]:
    """
    爬取电影列表
    :param max_pages: 最大爬取页数
    :param fetch_detail: 是否获取详情页
    :return: 电影列表
    """
    all_movies = []
    
    for page in range(1, max_pages + 1):
        url = MOVIE_URL if page == 1 else f"{MOVIE_URL}index_{page}.html"
        print(f"[爬取] 第 {page} 页: {url}")
        
        html = get_page_html(url)
        if not html:
            print(f"[跳过] 第 {page} 页获取失败")
            continue
        
        movies = parse_movie_list(html)
        print(f"[解析] 第 {page} 页找到 {len(movies)} 部电影")
        
        if fetch_detail:
            for i, movie in enumerate(movies):
                print(f"[详情] 获取 {movie['title']} ({i+1}/{len(movies)})")
                detail_html = get_page_html(movie["detail_url"])
                movies[i] = parse_movie_detail(detail_html, movie)
                time.sleep(1)  # 礼貌爬取，避免请求过快
        
        all_movies.extend(movies)
        time.sleep(1)
    
    # 去重
    seen = set()
    unique_movies = []
    for m in all_movies:
        key = m.get("片名") or m.get("title")
        if key and key not in seen:
            seen.add(key)
            unique_movies.append(m)
    
    print(f"[完成] 共爬取 {len(unique_movies)} 部电影")
    return unique_movies


def save_cache(movies: List[Dict]) -> None:
    """保存缓存"""
    DATA_DIR.mkdir(exist_ok=True)
    data = {
        "update_time": datetime.now().isoformat(),
        "movies": movies
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[缓存] 已保存到 {CACHE_FILE}")


def load_cache() -> Optional[List[Dict]]:
    """加载缓存"""
    if not CACHE_FILE.exists():
        return None
    
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        update_time = datetime.fromisoformat(data["update_time"])
        if (datetime.now() - update_time).total_seconds() > CACHE_EXPIRE_SECONDS:
            print("[缓存] 已过期")
            return None
        
        print(f"[缓存] 从缓存加载 {len(data['movies'])} 部电影")
        return data["movies"]
    except Exception as e:
        print(f"[缓存] 加载失败: {e}")
        return None


def get_movies(use_cache: bool = True, max_pages: int = 1) -> List[Dict]:
    """获取电影数据（优先使用缓存）"""
    if use_cache:
        cached = load_cache()
        if cached:
            return cached
    
    movies = crawl_movies(max_pages=max_pages, fetch_detail=True)
    if movies:
        save_cache(movies)
    return movies


# ============ 电视剧相关函数 ============

def crawl_tv(category: str = "国产剧", max_pages: int = 1, fetch_detail: bool = False) -> List[Dict]:
    """
    爬取电视剧列表
    :param category: 分类名称 (国产剧/日韩剧/欧美剧)
    :param max_pages: 最大爬取页数
    :param fetch_detail: 是否获取详情页
    :return: 电视剧列表
    """
    if category not in TV_URLS:
        print(f"[错误] 未知的电视剧分类: {category}")
        return []
    
    base_url = TV_URLS[category]
    all_shows = []
    
    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url}index_{page}.html"
        print(f"[爬取] {category} 第 {page} 页: {url}")
        
        html = get_page_html(url)
        if not html:
            continue
        
        soup = BeautifulSoup(html, "html.parser")
        
        # 找电视剧链接
        for link in soup.select("a.ulink"):
            href = link.get("href", "")
            title = link.get_text(strip=True)
            
            if href and title and "/html/tv/" in href:
                show = {
                    "title": title,
                    "category": category,
                    "detail_url": BASE_URL + href if href.startswith("/") else href,
                    "update_date": extract_date_from_url(href)
                }
                
                if fetch_detail:
                    detail_html = get_page_html(show["detail_url"])
                    if detail_html:
                        # 提取下载链接
                        detail_soup = BeautifulSoup(detail_html, "html.parser")
                        download_links = []
                        for a in detail_soup.find_all("a", href=True):
                            dl_href = a["href"]
                            if any(x in dl_href for x in ["magnet:", "ed2k:", "ftp://", ".torrent"]):
                                download_links.append(dl_href)
                        show["download_links"] = list(set(download_links))
                    time.sleep(1)
                
                all_shows.append(show)
        
        time.sleep(1)
    
    # 去重
    seen = set()
    unique = []
    for s in all_shows:
        if s["title"] not in seen:
            seen.add(s["title"])
            unique.append(s)
    
    print(f"[完成] {category} 共爬取 {len(unique)} 部剧")
    return unique


def crawl_all_tv(max_pages: int = 1, fetch_detail: bool = False) -> List[Dict]:
    """爬取所有电视剧分类"""
    all_shows = []
    for category in TV_URLS.keys():
        shows = crawl_tv(category, max_pages=max_pages, fetch_detail=fetch_detail)
        all_shows.extend(shows)
    return all_shows


def save_tv_cache(shows: List[Dict]) -> None:
    """保存电视剧缓存"""
    DATA_DIR.mkdir(exist_ok=True)
    data = {
        "update_time": datetime.now().isoformat(),
        "shows": shows
    }
    with open(TV_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[缓存] 电视剧已保存到 {TV_CACHE_FILE}")


def load_tv_cache() -> Optional[List[Dict]]:
    """加载电视剧缓存"""
    if not TV_CACHE_FILE.exists():
        return None
    
    try:
        with open(TV_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        update_time = datetime.fromisoformat(data["update_time"])
        if (datetime.now() - update_time).total_seconds() > CACHE_EXPIRE_SECONDS:
            return None
        
        return data["shows"]
    except:
        return None


def get_tv_shows(use_cache: bool = True, max_pages: int = 1) -> List[Dict]:
    """获取电视剧数据"""
    if use_cache:
        cached = load_tv_cache()
        if cached:
            return cached
    
    shows = crawl_all_tv(max_pages=max_pages, fetch_detail=False)
    if shows:
        save_tv_cache(shows)
    return shows


def search_tv(keyword: str, use_cache: bool = True) -> List[Dict]:
    """搜索电视剧"""
    shows = get_tv_shows(use_cache=use_cache)
    keyword = keyword.lower()
    
    results = []
    for s in shows:
        if keyword in s.get("title", "").lower():
            results.append(s)
    
    return results


def get_tv_detail(url: str) -> Dict:
    """获取电视剧详情页的下载链接"""
    html = get_page_html(url)
    if not html:
        return {}
    
    soup = BeautifulSoup(html, "html.parser")
    
    # 提取下载链接
    download_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if any(x in href for x in ["magnet:", "ed2k:", "ftp://", ".torrent"]):
            download_links.append(href)
    
    return {
        "download_links": list(set(download_links)),
        "url": url
    }


def get_recent_movies(movies: List[Dict], days: int = 7) -> List[Dict]:
    """获取最近N天内更新的电影"""
    recent = []
    today = datetime.now().date()
    
    for m in movies:
        date_str = m.get("update_date")
        if date_str:
            try:
                movie_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if (today - movie_date).days <= days:
                    recent.append(m)
            except:
                pass
    
    return recent


def get_high_score_movies(movies: List[Dict], min_douban: float = 7.5, min_imdb: float = 7.0) -> List[Dict]:
    """获取高分电影"""
    high_score = []
    
    for m in movies:
        douban = m.get("豆瓣评分")
        imdb = m.get("IMDb评分")
        
        # 豆瓣或IMDb任一高分即可
        if (douban and douban >= min_douban) or (imdb and imdb >= min_imdb):
            high_score.append(m)
    
    # 按评分排序
    high_score.sort(key=lambda x: x.get("豆瓣评分") or x.get("IMDb评分") or 0, reverse=True)
    return high_score


def search_movies(movies: List[Dict], keyword: str) -> List[Dict]:
    """搜索电影"""
    keyword = keyword.lower()
    results = []
    
    for m in movies:
        # 在片名、译名、导演、主演中搜索
        searchable = " ".join([
            str(m.get("片名", "")),
            str(m.get("译名", "")),
            str(m.get("导演", "")),
            str(m.get("主演", "")),
            str(m.get("title", ""))
        ]).lower()
        
        if keyword in searchable:
            results.append(m)
    
    return results


def format_movie_info(movie: Dict, include_download: bool = False, use_emoji: bool = True) -> str:
    """格式化电影信息为字符串"""
    lines = []
    
    # 根据环境选择是否使用emoji
    icon_movie = "[电影] " if not use_emoji else "🎬 "
    icon_score = "" if not use_emoji else "⭐ "
    icon_download = "[下载] " if not use_emoji else "📥 "
    
    if movie.get("片名"):
        lines.append(f"{icon_movie}**{movie['片名']}**")
    if movie.get("译名"):
        lines.append(f"   译名: {movie['译名']}")
    if movie.get("年代"):
        lines.append(f"   年代: {movie['年代']}")
    if movie.get("产地"):
        lines.append(f"   产地: {movie['产地']}")
    if movie.get("类别"):
        lines.append(f"   类别: {movie['类别']}")
    
    # 评分
    scores = []
    if movie.get("豆瓣评分"):
        scores.append(f"豆瓣: {movie['豆瓣评分']}")
    if movie.get("IMDb评分"):
        scores.append(f"IMDb: {movie['IMDb评分']}")
    if scores:
        lines.append(f"   {icon_score}{' | '.join(scores)}")
    
    if movie.get("导演"):
        lines.append(f"   导演: {movie['导演']}")
    if movie.get("主演"):
        lines.append(f"   主演: {movie['主演']}")
    if movie.get("文件大小"):
        lines.append(f"   大小: {movie['文件大小']}")
    if movie.get("文件格式"):
        lines.append(f"   格式: {movie['文件格式']}")
    if movie.get("update_date"):
        lines.append(f"   更新: {movie['update_date']}")
    
    if include_download and movie.get("download_links"):
        lines.append(f"   {icon_download}下载链接:")
        for i, link in enumerate(movie["download_links"][:3], 1):
            lines.append(f"      {i}. {link[:80]}...")
    
    return "\n".join(lines)


# ============ 群晖下载相关函数 ============

SYNOLOGY_HOST = "192.168.123.223"
SYNOLOGY_PORT = "5000"
SYNOLOGY_USER = "xiaoai"
SYNOLOGY_PASS = "Xx654321"

# 默认下载目录
DEFAULT_MOVIE_DIR = "video/电影"  # 电影下载到 /video/电影
DEFAULT_TV_DIR = "video/电视剧"  # 电视剧下载到 /video/电视剧


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


def syno_add_download(uri: str, destination: str = None) -> Dict:
    """
    添加下载任务到群晖
    :param uri: 下载链接（magnet/ftp/ed2k等）
    :param destination: 下载目录（如 "download" 或 "/video/电影"）
    :return: {"success": bool, "task_id": str, "error": str}
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
        "_sid": sid
    }
    
    # 如果指定了destination，添加到请求中
    if destination:
        data["destination"] = destination
    
    try:
        resp = requests.post(url, data=data, timeout=15)
        result = resp.json()
        
        if result.get("success"):
            task_id = result.get("data", {}).get("id", "unknown")
            return {"success": True, "task_id": task_id}
        else:
            error_code = result.get("error", {}).get("code", "unknown")
            error_msg = {
                101: "参数错误",
                102: "API不存在",
                103: "方法不存在",
                104: "版本不支持",
                105: "权限不足",
                106: "会话超时",
                107: "会话中断",
                403: "目录不存在或无权限",
                406: "未设置默认下载目录",
            }.get(error_code, f"错误码: {error_code}")
            return {"success": False, "error": error_msg, "code": error_code}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        syno_logout(sid)


def syno_list_downloads() -> List[Dict]:
    """获取下载任务列表"""
    sid = syno_login()
    if not sid:
        return []
    
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/DownloadStation/task.cgi"
    params = {
        "api": "SYNO.DownloadStation.Task",
        "version": 1,
        "method": "list",
        "additional": "transfer,detail",
        "_sid": sid
    }
    
    try:
        resp = requests.get(url, params=params, timeout=15)
        result = resp.json()
        if result.get("success"):
            return result["data"]["tasks"]
    except Exception as e:
        print(f"[获取任务列表失败] {e}")
    finally:
        syno_logout(sid)
    
    return []


def syno_delete_download(task_id: str, keep_files: bool = True) -> bool:
    """删除下载任务"""
    sid = syno_login()
    if not sid:
        return False
    
    url = f"http://{SYNOLOGY_HOST}:{SYNOLOGY_PORT}/webapi/DownloadStation/task.cgi"
    params = {
        "api": "SYNO.DownloadStation.Task",
        "version": 1,
        "method": "delete",
        "id": task_id,
        "force_complete": "false" if keep_files else "true",
        "_sid": sid
    }
    
    try:
        resp = requests.get(url, params=params, timeout=15)
        return resp.json().get("success", False)
    except:
        return False
    finally:
        syno_logout(sid)


def download_movie(movie: Dict, destination: str = DEFAULT_MOVIE_DIR) -> Dict:
    """
    下载电影到群晖
    :param movie: 电影信息字典（需包含download_links）
    :param destination: 下载目录
    :return: 下载结果
    """
    links = movie.get("download_links", [])
    if not links:
        return {"success": False, "error": "没有下载链接"}
    
    # 优先使用magnet链接
    magnet_links = [l for l in links if l.startswith("magnet:")]
    ftp_links = [l for l in links if l.startswith("ftp://")]
    
    uri = magnet_links[0] if magnet_links else (ftp_links[0] if ftp_links else links[0])
    
    result = syno_add_download(uri, destination)
    if result["success"]:
        print(f"[下载成功] {movie.get('片名') or movie.get('title')} - 任务ID: {result['task_id']}")
    else:
        print(f"[下载失败] {movie.get('片名') or movie.get('title')} - {result['error']}")
    
    return result


def main():
    """主函数 - 用于测试"""
    import argparse
    
    parser = argparse.ArgumentParser(description="电影天堂爬虫")
    parser.add_argument("--pages", type=int, default=1, help="爬取页数")
    parser.add_argument("--recent", type=int, help="显示最近N天更新的电影")
    parser.add_argument("--high-score", action="store_true", help="显示高分电影")
    parser.add_argument("--search", type=str, help="搜索电影")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存")
    
    args = parser.parse_args()
    
    # 获取电影数据
    movies = get_movies(use_cache=not args.no_cache, max_pages=args.pages)
    
    if not movies:
        print("未获取到电影数据")
        return
    
    print(f"\n{'='*60}")
    print(f"共 {len(movies)} 部电影")
    print(f"{'='*60}\n")
    
    # Windows终端不支持emoji
    import platform
    use_emoji = platform.system() != "Windows"
    
    # 查询模式
    if args.recent:
        results = get_recent_movies(movies, args.recent)
        print(f"最近 {args.recent} 天更新的电影 ({len(results)} 部):\n")
        for m in results[:10]:
            print(format_movie_info(m, use_emoji=use_emoji))
            print()
    
    elif args.high_score:
        results = get_high_score_movies(movies)
        print(f"高分电影 ({len(results)} 部):\n")
        for m in results[:10]:
            print(format_movie_info(m, use_emoji=use_emoji))
            print()
    
    elif args.search:
        results = search_movies(movies, args.search)
        print(f"搜索 '{args.search}' 结果 ({len(results)} 部):\n")
        for m in results[:10]:
            print(format_movie_info(m, include_download=True, use_emoji=use_emoji))
            print()
    
    else:
        # 默认显示最新电影
        print("最新电影:\n")
        for m in movies[:10]:
            print(format_movie_info(m, use_emoji=use_emoji))
            print()


if __name__ == "__main__":
    main()
