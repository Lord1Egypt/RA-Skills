"""ASRSkill — ASR 技能主类"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import httpx
import yaml

from .exceptions import ASRServiceError, ASRTranscriptionError
from .iff_manager import IFFManager
from .postprocessor import Postprocessor, TranscriptionResult

log = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


class ASRSkill:
    """ASR 技能 — CLI + API + 程序调用统一入口"""

    def __init__(self, config_path: str | Path | None = None):
        config = self._load_config(config_path)

        service = config.get("service", {})
        self._service_name = service.get("name", "sensevoice-small")
        self._base_url = service.get("base_url", "http://localhost:8881").rstrip("/")
        self._switch_timeout = service.get("switch_timeout", 120)
        self._health_timeout = service.get("health_timeout", 120)
        self._max_attempts = config.get("retry", {}).get("max_attempts", 3)

        defaults = config.get("defaults", {})
        self._default_language = defaults.get("language")  # None → 自动检测
        self._default_response_format = defaults.get("response_format", "json")

        self._iff_manager = IFFManager(
            service_name=self._service_name,
            base_url=self._base_url,
            switch_timeout=self._switch_timeout,
            health_timeout=self._health_timeout,
        )
        self._postprocessor = Postprocessor()

    @staticmethod
    def _load_config(config_path: str | Path | None) -> dict:
        """加载 config.yaml（默认同目录 config.yaml），失败时回退空配置"""
        path = DEFAULT_CONFIG_PATH if config_path is None else Path(config_path)
        if not path.exists():
            log.warning("config not found: %s, using defaults", path)
            return {}
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    # ─── 核心 API ─────────────────────────────

    def transcribe(
        self,
        audio_path: str | Path,
        language: str | None = None,      # auto-detect if None
        response_format: str = "json",    # json / text / verbose_json
        speaker_labels: bool = False,     # 说话人分离（spk=true）
    ) -> TranscriptionResult:
        """
        核心方法：
        1. iff_manager.ensure_running() → 确保 ASR 服务运行
        2. httpx.post(f"{base_url}/v1/audio/transcriptions", files=..., data=..., timeout=120)
        3. postprocessor.process(response.json(), response_format)
        4. 返回 TranscriptionResult

        关键约束：
        - 必须显式传 model="sensevoice"，不依赖 API 默认值
        - 不使用 /asr 端点（会无条件触发 vLLM 加载）
        """
        audio = Path(audio_path)
        if not audio.exists():
            raise ASRTranscriptionError(f"audio file not found: {audio}")

        language = language if language is not None else self._default_language
        response_format = response_format or self._default_response_format

        base_url = self._iff_manager.ensure_running()

        last_error: Exception | None = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                with open(audio, "rb") as f:
                    resp = httpx.post(
                        f"{base_url}/v1/audio/transcriptions",
                        files={"file": f},
                        data={
                            "model": "sensevoice",
                            "language": language or "auto",
                            "response_format": response_format,
                            **({"spk": "true"} if speaker_labels else {}),
                        },
                        timeout=120,
                    )
                resp.raise_for_status()
                raw = resp.text if response_format == "text" else resp.json()
                return self._postprocessor.process(raw, response_format)
            except Exception as e:
                last_error = e
                if attempt < self._max_attempts:
                    log.warning("Transcription attempt %d/%d failed: %s",
                                attempt, self._max_attempts, e)
                    time.sleep(1)
                    continue
        raise ASRTranscriptionError(
            f"transcription failed after {self._max_attempts} attempts: {last_error}"
        ) from last_error

    # ─── 字幕输出 ────────────────────────────

    def transcribe_srt(
        self,
        audio_path: str | Path,
        language: str | None = None,
        speaker_labels: bool = False,
    ) -> str:
        """转写并返回 SRT 格式字幕"""
        result = self.transcribe(
            audio_path,
            language=language,
            response_format="verbose_json",
            speaker_labels=speaker_labels,
        )
        if not result.segments:
            raise ASRTranscriptionError("no segments returned (required for SRT)")
        return Postprocessor.to_srt(result.segments)

    def transcribe_vtt(
        self,
        audio_path: str | Path,
        language: str | None = None,
        speaker_labels: bool = False,
    ) -> str:
        """转写并返回 VTT 格式字幕"""
        result = self.transcribe(
            audio_path,
            language=language,
            response_format="verbose_json",
            speaker_labels=speaker_labels,
        )
        if not result.segments:
            raise ASRTranscriptionError("no segments returned (required for VTT)")
        return Postprocessor.to_vtt(result.segments)

    def serve_status(self) -> dict:
        """
        查询 ASR 服务状态：
        1. GET /health
        2. 返回 {"healthy": bool, "details": response.json() or error message}
        """
        try:
            resp = httpx.get(f"{self._base_url}/health", timeout=3)
            return {"healthy": resp.status_code == 200, "details": resp.json()}
        except Exception as e:
            return {"healthy": False, "details": str(e)}
