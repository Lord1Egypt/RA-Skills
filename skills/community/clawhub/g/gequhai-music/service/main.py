"""
Gequhai Music Service - FastAPI 服务
自动注册到 Skill Gateway
支持下载后自动重命名
"""

import sys
import os
from pathlib import Path
import asyncio
from datetime import datetime

# 添加 skill 路径
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx

# 导入 skill 功能
from scripts.gequhai_crawler import (
    search_songs, get_download_url, download_song as do_download,
    auto_process_downloads, process_rename_queue
)

# 创建应用
app = FastAPI(
    title="Gequhai Music Service",
    description="歌曲海音乐搜索与下载服务",
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

class Song(BaseModel):
    id: str
    title: str
    artist: str
    album: str = ""


class DownloadResult(BaseModel):
    success: bool
    message: str
    url: Optional[str] = None
    quality: Optional[str] = None


# ==================== API 端点 ====================

@app.get("/")
def root():
    """服务信息"""
    return {
        "service": "gequhai-music",
        "version": "1.0.0",
        "endpoints": ["/search", "/detail/{id}", "/download"]
    }


@app.get("/search", response_model=List[Song])
def search(keyword: str = Query(..., description="搜索关键词")):
    """搜索歌曲"""
    try:
        results = search_songs(keyword)
        return [
            Song(
                id=str(s.get("id", "")),
                title=s.get("title", ""),
                artist=s.get("artist", ""),
                album=s.get("album", "")
            )
            for s in results[:20]
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/detail/{song_id}")
def get_detail(song_id: str):
    """获取歌曲详情和下载链接"""
    try:
        detail = get_download_url(song_id)
        return detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download", response_model=DownloadResult)
def download(song_id: str = Query(..., description="歌曲ID"), keyword: str = Query(None, description="搜索关键词")):
    """下载歌曲到群晖（自动重命名）"""
    try:
        # 如果有关键词，先搜索
        if keyword:
            songs = search_songs(keyword)
            if songs:
                song_id = str(songs[0].get("id", song_id))
        
        # 获取下载链接
        detail = get_download_url(song_id)
        
        # 下载（自动重命名）
        result = do_download(detail, auto_rename=True)
        
        return DownloadResult(
            success=result.get("success", False),
            message=result.get("error", "") or f"已下载，目标文件名: {result.get('target_name', 'N/A')}",
            url=result.get("url"),
            quality=detail.get("quality")
        )
    except Exception as e:
        return DownloadResult(success=False, message=str(e))


@app.post("/process-renames")
def process_renames():
    """手动处理重命名队列"""
    result = auto_process_downloads()
    return result


@app.get("/rename-queue")
def get_rename_queue():
    """查看重命名队列"""
    from scripts.gequhai_crawler import load_rename_queue
    queue = load_rename_queue()
    return {"count": len(queue), "items": queue}


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "ok"}


# ==================== 自动注册 ====================

async def register_to_gateway():
    """自动注册到 Skill Gateway"""
    GATEWAY_URL = os.getenv("SKILL_GATEWAY_URL", "http://localhost:8200")
    SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8001))
    SERVICE_HOST = os.getenv("SERVICE_HOST", "192.168.123.162")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{GATEWAY_URL}/api/services/register",
                json={
                    "name": "gequhai-music",
                    "description": "歌曲海音乐搜索与下载服务",
                    "base_url": f"http://{SERVICE_HOST}:{SERVICE_PORT}",
                    "capabilities": ["search", "download", "ranking", "auto_rename"],
                    "endpoints": [
                        {"path": "/search", "method": "GET", "description": "搜索歌曲"},
                        {"path": "/detail/{id}", "method": "GET", "description": "获取歌曲详情"},
                        {"path": "/download", "method": "POST", "description": "下载歌曲（自动重命名）"},
                        {"path": "/process-renames", "method": "POST", "description": "处理重命名队列"},
                        {"path": "/rename-queue", "method": "GET", "description": "查看重命名队列"}
                    ]
                },
                timeout=5.0
            )
            
            if response.status_code == 200:
                print(f"[Gequhai] 已注册到 Skill Gateway: {GATEWAY_URL}")
            else:
                print(f"[Gequhai] 注册失败: {response.text}")
                
        except Exception as e:
            print(f"[Gequhai] 注册失败: {e}")


async def background_rename_processor():
    """后台任务：定期处理重命名队列"""
    while True:
        try:
            await asyncio.sleep(30)  # 每30秒检查一次
            result = auto_process_downloads()
            if result.get("processed"):
                print(f"[后台任务] 处理了 {len(result['processed'])} 个重命名任务")
        except Exception as e:
            print(f"[后台任务错误] {e}")


@app.on_event("startup")
async def startup():
    """启动时自动注册和启动后台任务"""
    await register_to_gateway()
    asyncio.create_task(background_rename_processor())


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
