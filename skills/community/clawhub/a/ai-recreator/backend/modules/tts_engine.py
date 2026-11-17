"""TTS 语音合成模块"""
import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)


class TTSEngine:
    """多引擎语音合成"""

    async def synthesize(
        self,
        text: str,
        task_id: str,
        voice: str = "zh-CN-XiaoxiaoNeural",
        engine: str = "",
    ) -> Path:
        """
        合成语音
        返回音频文件路径
        """
        engine = engine or settings.TTS_ENGINE
        output_path = settings.AUDIO_DIR / f"{task_id}.mp3"

        if engine == "edge":
            await self._synthesize_edge(text, output_path, voice)
        elif engine == "melotts":
            await self._synthesize_melotts(text, output_path, voice)
        elif engine == "cosyvoice":
            await self._synthesize_cosyvoice(text, output_path, voice)
        else:
            raise ValueError(f"不支持的 TTS 引擎: {engine}")

        if not output_path.exists():
            raise RuntimeError(f"TTS 合成失败：未生成文件")

        logger.info(f"TTS synthesized: {output_path} ({output_path.stat().st_size / 1024:.0f} KB)")
        return output_path

    async def _synthesize_edge(self, text: str, output_path: Path, voice: str):
        """edge-tts（最快，无需 GPU，中文质量好）"""
        import edge_tts

        # edge-tts 限制单次 3000 字，长文本分段
        chunk_size = 2500
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        if len(chunks) == 1:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_path))
        else:
            # 多段拼接
            temp_dir = settings.TEMP_DIR / task_id
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_files = []
            for i, chunk in enumerate(chunks):
                tmp = temp_dir / f"chunk_{i}.mp3"
                communicate = edge_tts.Communicate(chunk, voice)
                await communicate.save(str(tmp))
                temp_files.append(tmp)

            # 拼接（用 ffmpeg）
            concat_list = temp_dir / "concat.txt"
            concat_list.write_text(
                "\n".join(f"file '{f}'" for f in temp_files),
                encoding="utf-8",
            )
            subprocess.run([
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(concat_list),
                "-c", "copy",
                str(output_path),
            ], check=True, capture_output=True)

    async def _synthesize_melotts(self, text: str, output_path: Path, voice: str):
        """MeloTTS（中文质量更好，需 Python 环境）"""
        # 通过子进程调用独立的 MeloTTS 服务
        # 假设 MeloTTS 已安装为服务：melotts-server
        subprocess.run([
            "python", "-m", "melotts.server",
            "--text", text[:5000],
            "--output", str(output_path),
        ], check=True, timeout=120)

    async def _synthesize_cosyvoice(self, text: str, output_path: Path, voice: str):
        """CosyVoice（质量最高，需 GPU）"""
        # 假设 CosyVoice 已部署
        subprocess.run([
            "python", "-m", "cosyvoice.cli",
            "--text", text,
            "--output", str(output_path),
            "--voice", voice,
        ], check=True, timeout=300)
