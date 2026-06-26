#!/usr/bin/env python3
"""
Fun-ASR-Nano-2512 FastAPI 服务
提供 HTTP API 接口进行语音识别
"""

import os
import sys
import tempfile
import uvicorn
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

# 将 scripts 目录加入路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 全局模型实例
transcriber = None

class TranscriptionResponse(BaseModel):
    """转写响应模型"""
    success: bool
    text: str
    duration: Optional[float] = None
    rtf: Optional[float] = None
    error: Optional[str] = None

class TranscriptionRequest(BaseModel):
    """转写请求模型（用于 URL 方式）"""
    audio_url: str
    language: str = "auto"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理 - 启动时加载模型"""
    global transcriber
    
    logger.info("🚀 正在启动 Fun-ASR-Nano-2512 服务...")
    logger.info("📦 加载模型中，请稍候...")
    
    try:
        from FunAsrTranscriber import AsrTranscriber
        
        # 切换到 scripts 目录
        original_cwd = os.getcwd()
        os.chdir(script_dir)
        
        # 加载模型（只加载一次）
        transcriber = AsrTranscriber()
        
        os.chdir(original_cwd)
        logger.info("✅ 模型加载完成！服务已就绪")
        
    except Exception as e:
        logger.error(f"❌ 模型加载失败: {e}")
        raise
    
    yield
    
    # 关闭时清理
    logger.info("🛑 服务正在关闭...")
    transcriber = None

# 创建 FastAPI 应用
app = FastAPI(
    title="Fun-ASR-Nano-2512 语音转写服务",
    description="基于 FastAPI 的高性能语音识别服务",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """根路径 - 服务状态检查"""
    return {
        "service": "Fun-ASR-Nano-2512",
        "status": "running",
        "model_loaded": transcriber is not None
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    if transcriber is None:
        raise HTTPException(status_code=503, detail="模型未加载")
    return {"status": "healthy", "model": "Fun-ASR-Nano-2512"}

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(..., description="音频文件 (WAV, MP3, M4A)")
):
    """
    上传音频文件进行转写
    
    - **audio**: 音频文件 (支持 WAV, MP3, M4A, AAC, OGG)
    - 返回转写文本
    """
    if transcriber is None:
        raise HTTPException(status_code=503, detail="模型未加载，请稍后重试")
    
    # 检查文件类型
    allowed_extensions = {'.wav', '.mp3', '.m4a', '.aac', '.ogg', '.flac'}
    file_ext = Path(audio.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件格式: {file_ext}。支持的格式: {', '.join(allowed_extensions)}"
        )
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        tmp_path = tmp_file.name
        content = await audio.read()
        tmp_file.write(content)
    
    try:
        logger.info(f"🎵 开始转写: {audio.filename} ({len(content)} bytes)")
        
        # 切换到 scripts 目录
        original_cwd = os.getcwd()
        os.chdir(script_dir)
        
        # 执行转写
        import time
        start_time = time.time()
        
        result = transcriber.transcribe_sync(tmp_path)
        
        duration = time.time() - start_time
        
        os.chdir(original_cwd)
        
        # 清理临时文件
        background_tasks.add_task(os.remove, tmp_path)
        
        logger.info(f"✅ 转写完成: {result[:50]}...")
        
        return TranscriptionResponse(
            success=True,
            text=result,
            duration=round(duration, 3),
            rtf=round(duration / 3, 3)  # 假设音频约3分钟
        )
        
    except Exception as e:
        # 确保清理临时文件
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        logger.error(f"❌ 转写失败: {e}")
        return TranscriptionResponse(
            success=False,
            text="",
            error=str(e)
        )

@app.post("/transcribe/path")
async def transcribe_from_path(
    file_path: str,
    background_tasks: BackgroundTasks
):
    """
    转写服务器本地路径的音频文件
    
    - **file_path**: 音频文件的绝对路径
    - 返回转写文本
    """
    if transcriber is None:
        raise HTTPException(status_code=503, detail="模型未加载")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")
    
    try:
        logger.info(f"🎵 开始转写本地文件: {file_path}")
        
        # 切换到 scripts 目录
        original_cwd = os.getcwd()
        os.chdir(script_dir)
        
        import time
        start_time = time.time()
        
        result = transcriber.transcribe_sync(file_path)
        
        duration = time.time() - start_time
        
        os.chdir(original_cwd)
        
        logger.info(f"✅ 转写完成")
        
        return TranscriptionResponse(
            success=True,
            text=result,
            duration=round(duration, 3)
        )
        
    except Exception as e:
        logger.error(f"❌ 转写失败: {e}")
        return TranscriptionResponse(
            success=False,
            text="",
            error=str(e)
        )

@app.get("/stats")
async def get_stats():
    """获取服务统计信息"""
    return {
        "model": "Fun-ASR-Nano-2512",
        "model_loaded": transcriber is not None,
        "device": "cpu",  # 可以从 transcriber 获取实际设备
        "supported_formats": [".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"]
    }

def main():
    """启动服务"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     Fun-ASR-Nano-2512 FastAPI 语音转写服务               ║
    ╠══════════════════════════════════════════════════════════╣
    ║  地址: http://127.0.0.1:11890                            ║
    ║  文档: http://127.0.0.1:11890/docs                       ║
    ╠══════════════════════════════════════════════════════════╣
    ║  端点:                                                   ║
    ║    • GET  /          - 服务状态                          ║
    ║    • GET  /health    - 健康检查                          ║
    ║    • POST /transcribe - 上传音频转写                     ║
    ║    • POST /transcribe/path - 本地文件转写                ║
    ║    • GET  /stats     - 服务统计                          ║
    ╠══════════════════════════════════════════════════════════╣
    ║  安全: 只监听 127.0.0.1，不对外暴露                      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=11890,
        log_level="info"
    )

if __name__ == "__main__":
    main()
