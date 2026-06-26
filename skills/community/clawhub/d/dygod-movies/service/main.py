"""
DYGod Movies Service - FastAPI 服务
自动注册到 Skill Gateway
"""

import sys
import os
from pathlib import Path
import asyncio
from datetime import datetime

# 添加 skill 路径
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx

# 导入 skill 功能
from scripts.dygod_crawler import (
    get_movies, get_high_score_movies, search_movies,
    search_tv, get_tv_detail, download_movie
)

# 创建应用
app = FastAPI(
    title="DYGod Movies Service",
    description="电影天堂影视搜索与下载服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 响应模型 ====================

class Movie(BaseModel):
    title: str
    片名: str = ""
    译名: str = ""
    年代: str = ""
    产地: str = ""
    类别: str = ""
    豆瓣评分: Optional[float] = None
    IMDb评分: Optional[float] = None
    导演: str = ""
    主演: str = ""
    文件大小: str = ""
    download_links: List[str] = []


class TVShow(BaseModel):
    title: str
    detail_url: str = ""
    category: str = ""


# ==================== API 端点 ====================

@app.get("/")
def root():
    """服务信息"""
    return {
        "service": "dygod-movies",
        "version": "1.0.0",
        "endpoints": ["/movies", "/high-score", "/search", "/tv/search", "/download"]
    }


@app.get("/movies", response_model=List[Movie])
def list_movies(
    pages: int = Query(1, description="爬取页数"),
    recent: int = Query(None, description="最近N天更新的电影"),
    use_cache: bool = Query(True, description="使用缓存")
):
    """获取电影列表"""
    try:
        movies = get_movies(
            max_pages=pages,
            use_cache=use_cache
        )
        
        if recent:
            # 筛选最近更新的
            from datetime import datetime, timedelta
            cutoff = datetime.now() - timedelta(days=recent)
            movies = [m for m in movies if m.get("update_time") and 
                     datetime.fromisoformat(m["update_time"]) >= cutoff]
        
        return [Movie(**m) for m in movies[:50]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/high-score", response_model=List[Movie])
def get_high_score(
    min_douban: float = Query(7.5, description="最低豆瓣评分"),
    min_imdb: float = Query(7.0, description="最低IMDb评分"),
    pages: int = Query(2, description="爬取页数")
):
    """获取高分电影"""
    try:
        movies = get_movies(max_pages=pages)
        high_score = get_high_score_movies(movies, min_douban=min_douban, min_imdb=min_imdb)
        return [Movie(**m) for m in high_score[:30]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search", response_model=List[Movie])
def search(
    keyword: str = Query(..., description="搜索关键词"),
    pages: int = Query(2, description="爬取页数")
):
    """搜索电影"""
    try:
        movies = get_movies(max_pages=pages)
        results = search_movies(movies, keyword)
        return [Movie(**m) for m in results[:20]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tv/search", response_model=List[TVShow])
def search_tv_show(
    keyword: str = Query(..., description="搜索关键词"),
    category: str = Query(None, description="分类: hytv/rihantv/oumeitv")
):
    """搜索电视剧"""
    try:
        results = search_tv(keyword, category=category)
        return [TVShow(**t) for t in results[:20]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tv/{tv_id}")
def get_tv(tv_id: str):
    """获取电视剧详情"""
    try:
        # tv_id 是 detail_url 的一部分
        detail_url = f"https://www.dygod.net/html/tv/{tv_id}"
        detail = get_tv_detail(detail_url)
        return detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download")
def download(
    magnet: str = Query(..., description="磁力链接"),
    destination: str = Query("video/电影", description="下载目录")
):
    """下载电影/电视剧到群晖"""
    try:
        result = download_movie({"download_links": [magnet]}, destination=destination)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "ok"}


# ==================== 自动注册 ====================

async def register_to_gateway():
    """自动注册到 Skill Gateway"""
    GATEWAY_URL = os.getenv("SKILL_GATEWAY_URL", "http://localhost:8200")
    SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8002))
    SERVICE_HOST = os.getenv("SERVICE_HOST", "192.168.123.162")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{GATEWAY_URL}/api/services/register",
                json={
                    "name": "dygod-movies",
                    "description": "电影天堂影视搜索与下载服务",
                    "base_url": f"http://{SERVICE_HOST}:{SERVICE_PORT}",
                    "capabilities": ["movies", "tv", "search", "download", "high_score"],
                    "endpoints": [
                        {"path": "/movies", "method": "GET", "description": "获取电影列表"},
                        {"path": "/high-score", "method": "GET", "description": "获取高分电影"},
                        {"path": "/search", "method": "GET", "description": "搜索电影"},
                        {"path": "/tv/search", "method": "GET", "description": "搜索电视剧"},
                        {"path": "/download", "method": "POST", "description": "下载到群晖"}
                    ]
                },
                timeout=5.0
            )
            
            if response.status_code == 200:
                print(f"[DYGod] 已注册到 Skill Gateway: {GATEWAY_URL}")
            else:
                print(f"[DYGod] 注册失败: {response.text}")
                
        except Exception as e:
            print(f"[DYGod] 注册失败: {e}")


@app.on_event("startup")
async def startup():
    """启动时自动注册"""
    await register_to_gateway()


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
