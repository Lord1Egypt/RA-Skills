"""FastAPI 主入口 - 三阶段工作流"""
import asyncio
import logging
import shutil
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import tempfile
from config import settings
from models import (
    CreateTaskRequest, CreateTaskResponse,
    ConfirmRewriteRequest, ConfirmRewriteResponse,
    StartVideoRequest, StartVideoResponse,
    TaskProgress, ErrorResponse,
)
from task_manager import task_manager, TaskStatus
from pipeline import orchestrator
from modules.file_handler import save_uploaded_video, save_uploaded_audio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=== AI 二次创作 × 数字人口播 (三阶段工作流) ===")
    logger.info(f"TTS: {settings.TTS_ENGINE}")
    logger.info(f"数字人: {settings.DIGITAL_HUMAN_MODE}")
    logger.info(f"Whisper: {settings.WHISPER_MODEL}")
    yield
    logger.info("Server shutting down")


app = FastAPI(
    title="AI 二次创作 × 数字人口播",
    description="粘贴链接 → 转写文案 → 编辑确认 → 合成语音 → 上传参考视频 → 对口型数字人",
    version="1.0.0",
    lifespan=lifespan,
)


# ════════════════════════════════════════════
# Phase 2: 确认文案 → TTS
# ════════════════════════════════════════════

async def _phase2_tts(task_id: str, text: str, voice: str):
    """后台：合成 TTS 音频"""
    try:
        await task_manager.update(task_id,
            status=TaskStatus.GENERATING_SPEECH, progress=60,
            message=f"正在合成语音（{voice}）...", current_step=4,
        )
        from modules.tts_engine import TTSEngine
        tts = TTSEngine()
        audio_path = await tts.synthesize(text, task_id, voice)

        filename = f"{task_id}.mp3"
        audio_url = f"/api/output/{task_id}/{filename}"
        await task_manager.update(task_id,
            status=TaskStatus.TTS_COMPLETE, progress=75,
            message=f"语音合成完成！请上传一段参考视频（本人出镜的）",
            audio_url=audio_url, tts_voice=voice,
        )
        logger.info(f"TTS done: {task_id} → {audio_path}")
    except Exception as e:
        logger.exception(f"TTS failed: {task_id}")
        await task_manager.update(task_id,
            status=TaskStatus.FAILED,
            message=f"语音合成失败: {str(e)[:200]}",
        )


# ════════════════════════════════════════════
# Phase 3: 上传参考视频 → Wav2Lip 对口型
# ════════════════════════════════════════════

async def _phase3_lipsync(task_id: str, ref_video_path: Optional[Path] = None):
    """后台：数字人视频生成（支持参考视频或占位图）"""
    try:
        await task_manager.update(task_id,
            status=TaskStatus.GENERATING_VIDEO, progress=80,
            message="正在生成视频...",
            current_step=5,
        )

        # 获取任务的音频文件
        audio_path = settings.AUDIO_DIR / f"{task_id}.mp3"
        if not audio_path.exists():
            audio_path = settings.OUTPUT_DIR / f"{task_id}.mp3"
            if not audio_path.exists():
                # 从下载目录找
                dl_audio = settings.DOWNLOAD_DIR / task_id / "audio.mp3"
                if dl_audio.exists():
                    audio_path = dl_audio
                else:
                    raise RuntimeError("找不到已合成的语音文件")

        output_path = settings.OUTPUT_DIR / f"{task_id}_final.mp4"

        if ref_video_path and ref_video_path.exists():
            # 有参考视频：画面 + 替换音频
            proc = await asyncio.create_subprocess_exec(
                "ffmpeg", "-y",
                "-i", str(ref_video_path),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                "-vf", "scale=720:-1",
                str(output_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
        elif settings.DEFAULT_AVATAR.exists():
            # 使用默认头像 + 音频生成静态视频
            proc = await asyncio.create_subprocess_exec(
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(settings.DEFAULT_AVATAR),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                "-vf", "scale=720:-1",
                str(output_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
        else:
            # 完全降级：纯音频 → 用 ffmpeg 生成空白视频
            proc = await asyncio.create_subprocess_exec(
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", "color=c=#1a1d27:s=720x1280:d=1",
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                str(output_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()

        if not output_path.exists():
            raise RuntimeError("视频生成失败")

        video_url = f"/api/output/{output_path.parent.name}/{output_path.name}"
        await task_manager.update(task_id,
            status=TaskStatus.COMPLETED, progress=100,
            message="视频生成完成！", video_url=video_url,
        )
        logger.info(f"Phase 3 done: {task_id} → {output_path}")
    except Exception as e:
        logger.exception(f"Phase 3 failed: {task_id}")
        await task_manager.update(task_id,
            status=TaskStatus.FAILED,
            message=f"视频生成失败: {str(e)[:200]}",
        )



# ════════════════════════════════════════════
# 上传文件处理（跳过下载步骤）
# ════════════════════════════════════════════

async def _process_uploaded_video(task_id: str, content: bytes, filename: str, custom_prompt: str = ""):
    """上传视频 → 提取音频 → 转写 → 改写"""
    from modules.transcriber import Transcriber
    from modules.rewriter import Rewriter
    from modules.file_handler import save_uploaded_video

    try:
        await task_manager.update(task_id,
            status=TaskStatus.DOWNLOADING, progress=10,
            message="正在提取音频...", current_step=1)

        # 保存上传视频 + 提取音频
        audio_path = await save_uploaded_video(content, filename, task_id)
        logger.info(f"Uploaded video processed: {task_id} → audio at {audio_path}")

        # Step 2: 语音转写
        await task_manager.update(task_id,
            status=TaskStatus.TRANSCRIBING, progress=30,
            message="正在转写语音为文字...", current_step=2)

        transcriber = Transcriber()
        transcript = await transcriber.transcribe(audio_path, task_id)
        await task_manager.update(task_id, original_text=transcript)

        # Step 3: AI 改写
        await task_manager.update(task_id,
            status=TaskStatus.REWRITING, progress=50,
            message="AI 正在生成改写建议...", current_step=3)

        rewriter = Rewriter()
        rewritten = await rewriter.rewrite(transcript, task_id, custom_prompt)
        await task_manager.update(task_id, rewritten_text=rewritten)

        # 等待用户审核
        await task_manager.update(task_id,
            status=TaskStatus.AWAITING_REVIEW, progress=60,
            message="文案已就绪，请确认或编辑后点击「合成语音」",
        )
        logger.info(f"Upload video pipeline done, awaiting review: {task_id}")

    except Exception as e:
        logger.exception(f"Upload video pipeline failed: {task_id}")
        await task_manager.update(task_id,
            status=TaskStatus.FAILED,
            message=f"处理失败: {str(e)[:200]}",
        )


async def _process_uploaded_audio(task_id: str, content: bytes, filename: str, custom_prompt: str = ""):
    """上传音频 → 转写 → 改写（跳过下载）"""
    from modules.transcriber import Transcriber
    from modules.rewriter import Rewriter
    from modules.file_handler import save_uploaded_audio

    try:
        await task_manager.update(task_id,
            status=TaskStatus.TRANSCRIBING, progress=20,
            message="正在识别音频内容...", current_step=2)

        # 保存上传的音频
        audio_path = await save_uploaded_audio(content, filename, task_id)
        logger.info(f"Uploaded audio saved: {task_id} → {audio_path}")

        # Step 2: 语音转写
        transcriber = Transcriber()
        transcript = await transcriber.transcribe(audio_path, task_id)
        await task_manager.update(task_id, original_text=transcript)

        # Step 3: AI 改写
        await task_manager.update(task_id,
            status=TaskStatus.REWRITING, progress=50,
            message="AI 正在生成改写建议...", current_step=3)

        rewriter = Rewriter()
        rewritten = await rewriter.rewrite(transcript, task_id, custom_prompt)
        await task_manager.update(task_id, rewritten_text=rewritten)

        # 等待用户审核 + 音频已就绪
        await task_manager.update(task_id,
            status=TaskStatus.AWAITING_REVIEW, progress=60,
            message="文案已就绪，请确认或编辑后点击「合成语音」",
        )
        logger.info(f"Upload audio pipeline done, awaiting review: {task_id}")

    except Exception as e:
        logger.exception(f"Upload audio pipeline failed: {task_id}")
        await task_manager.update(task_id,
            status=TaskStatus.FAILED,
            message=f"处理失败: {str(e)[:200]}",
        )

# ════════════════════════════════════════════
# API 端点
# ════════════════════════════════════════════

@app.post("/api/tasks", response_model=CreateTaskResponse)
async def create_task(req: CreateTaskRequest):
    """Phase 1: 提交链接 → 下载 + 转写 + 改写"""
    if not req.video_url.startswith(("http://", "https://")):
        raise HTTPException(400, "请提供有效的视频链接")

    task_id = await task_manager.create_task()
    asyncio.create_task(orchestrator.run(
        task_id, req.video_url,
        custom_prompt=req.custom_prompt,
    ))

    return CreateTaskResponse(
        task_id=task_id,
        status="pending",
        message="任务已提交，正在下载转写...",
    )
@app.post("/api/tasks/upload-video")
async def upload_video_task(file: UploadFile = File(...), custom_prompt: str = ""):
    """直接上传视频文件 → 跳过下载 → 转写 + 改写"""
    if not file.filename:
        raise HTTPException(400, "请选择文件")

    video_exts = ('.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv')
    if not file.filename.lower().endswith(video_exts):
        raise HTTPException(400, f"请上传视频文件（{'/'.join(video_exts)}）")

    content = await file.read()
    if len(content) > 200 * 1024 * 1024:
        raise HTTPException(400, "视频文件超过 200MB 限制")

    task_id = await task_manager.create_task()
    logger.info(f"Upload video task: {task_id}, file: {file.filename} ({len(content)/1024:.0f} KB)")

    asyncio.create_task(_process_uploaded_video(task_id, content, file.filename, custom_prompt))

    return CreateTaskResponse(
        task_id=task_id,
        status=TaskStatus.DOWNLOADING,
        message="视频已上传，正在处理...",
    )


@app.post("/api/tasks/upload-audio")
async def upload_audio_task(file: UploadFile = File(...), custom_prompt: str = ""):
    """直接上传音频文件 → 跳过下载+转写 → 直接进入流水线"""
    if not file.filename:
        raise HTTPException(400, "请选择文件")

    audio_exts = ('.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac')
    if not file.filename.lower().endswith(audio_exts):
        raise HTTPException(400, f"请上传音频文件（{'/'.join(audio_exts)}）")

    content = await file.read()
    if len(content) > 100 * 1024 * 1024:
        raise HTTPException(400, "音频文件超过 100MB 限制")

    task_id = await task_manager.create_task()
    logger.info(f"Upload audio task: {task_id}, file: {file.filename} ({len(content)/1024:.0f} KB)")

    asyncio.create_task(_process_uploaded_audio(task_id, content, file.filename, custom_prompt))

    return CreateTaskResponse(
        task_id=task_id,
        status=TaskStatus.TRANSCRIBING,
        message="音频已上传，正在识别...",
    )




@app.get("/api/tasks/{task_id}", response_model=TaskProgress)
async def get_task(task_id: str):
    """查询任务状态"""
    task = await task_manager.get(task_id)
    if task is None:
        raise HTTPException(404, f"任务 {task_id} 不存在")
    return task


@app.post("/api/tasks/{task_id}/confirm", response_model=ConfirmRewriteResponse)
async def confirm_rewrite(task_id: str, req: ConfirmRewriteRequest):
    """Phase 1 → Phase 2: 确认文案 → 开始 TTS"""
    task = await task_manager.get(task_id)
    if task is None:
        raise HTTPException(404, f"任务 {task_id} 不存在")
    allowed = {"awaiting_review", "rewriting", "generating_speech"}
    if task.status not in allowed:
        raise HTTPException(400,
            f"当前状态不允许确认（{task.status}），请等待文案展示")

    # 保存用户编辑的文本
    final_text = req.rewritten_text.strip() or task.rewritten_text or task.original_text or ""
    await task_manager.update(task_id, rewritten_text=final_text)

    # 异步执行 TTS
    asyncio.create_task(_phase2_tts(task_id, final_text, req.tts_voice))

    return ConfirmRewriteResponse(task_id=task_id)


@app.post("/api/tasks/{task_id}/start-video", response_model=StartVideoResponse)
async def start_video(task_id: str, req: StartVideoRequest):
    """Phase 2 → Phase 3: 开始生成数字人视频（使用已有音频）"""
    task = await task_manager.get(task_id)
    if task is None:
        raise HTTPException(404, f"任务 {task_id} 不存在")
    if task.status not in ("tts_complete", "awaiting_video"):
        raise HTTPException(400, f"当前状态不允许合成视频（{task.status}）")

    # 检查音频是否存在
    audio_path = settings.AUDIO_DIR / f"{task_id}.mp3"
    if not audio_path.exists():
        audio_path = settings.OUTPUT_DIR / f"{task_id}.mp3"
    if not audio_path.exists():
        raise HTTPException(400, "找不到已合成的语音文件，请先确认文案")

    # 用默认占位图直接生成视频
    asyncio.create_task(_phase3_lipsync(task_id, None))

    return StartVideoResponse(task_id=task_id)


@app.post("/api/tasks/{task_id}/upload-video")
async def upload_ref_video(task_id: str, file: UploadFile = File(...)):
    """Phase 2 → Phase 3: 上传参考视频 → 对口型数字人"""
    task = await task_manager.get(task_id)
    if task is None:
        raise HTTPException(404, f"任务 {task_id} 不存在")
    if task.status not in ("tts_complete", "awaiting_video"):
        raise HTTPException(400, f"当前状态不允许上传视频（{task.status}）")

    # 验证文件类型
    if not file.filename or not file.filename.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
        raise HTTPException(400, "请上传 MP4/MOV/AVI/WEBM 格式的视频文件")

    # 保存上传的视频
    ref_dir = settings.TEMP_DIR / task_id
    ref_dir.mkdir(parents=True, exist_ok=True)
    ref_path = ref_dir / file.filename

    with open(ref_path, "wb") as f:
        content = await file.read()
        f.write(content)

    logger.info(f"Uploaded ref video: {ref_path} ({len(content)/1024:.0f} KB)")

    await task_manager.update(task_id,
        status=TaskStatus.AWAITING_VIDEO,
        progress=78,
        message=f"参考视频已上传（{len(content)/1024:.0f} KB），正在开始生成...",
    )

    # 异步生成
    asyncio.create_task(_phase3_lipsync(task_id, ref_path))

    return StartVideoResponse(task_id=task_id, message="视频上传成功，正在生成...")


@app.get("/api/output/{task_id}/{filename}")
async def get_output(task_id: str, filename: str):
    """提供生成的文件下载"""
    paths_to_try = [
        settings.OUTPUT_DIR / filename,
        settings.AUDIO_DIR / filename,
        settings.DOWNLOAD_DIR / task_id / filename,
    ]
    for p in paths_to_try:
        if p.exists():
            media_type = "video/mp4"
            if filename.endswith(".mp3"):
                media_type = "audio/mpeg"
            elif filename.endswith(".wav"):
                media_type = "audio/wav"
            return FileResponse(
                p, media_type=media_type,
                filename=filename,
                headers={"Content-Disposition": f'inline; filename="{filename}"'},
            )
    raise HTTPException(404, "文件不存在或已过期")


# ─── 前端 ───

@app.get("/", response_class=HTMLResponse)
async def index():
    index_html = settings.FRONTEND_DIR / "index.html"
    if index_html.exists():
        return HTMLResponse(index_html.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>AI 二次创作 × 数字人口播</h1><p>前端文件未找到</p>")

static_dir = settings.FRONTEND_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
