"""ASRSkill 单元测试 — 不依赖真实服务"""

from unittest import mock

import pytest

from asr_service import ASRServiceError, ASRTranscriptionError, ASRSkill, TranscriptionResult
from asr_service.iff_manager import IFFManager
from asr_service.postprocessor import Postprocessor


class TestTranscriptionResult:
    def test_transcription_result_dataclass(self):
        r = TranscriptionResult(text="你好世界")
        assert r.text == "你好世界"
        assert r.language is None
        assert r.duration is None
        assert r.segments is None

    def test_transcription_result_full(self):
        r = TranscriptionResult(text="你好", language="zh", duration=1.5,
                                segments=[{"start": 0.0, "text": "你好"}])
        assert r.language == "zh"
        assert r.duration == 1.5
        assert r.segments == [{"start": 0.0, "text": "你好"}]


class TestPostprocessor:
    def test_postprocessor_json(self):
        pp = Postprocessor()
        r = pp.process({"text": "你好世界"}, "json")
        assert r == TranscriptionResult(text="你好世界")

    def test_postprocessor_text(self):
        pp = Postprocessor()
        r = pp.process("你好世界", "text")
        assert r == TranscriptionResult(text="你好世界")

    def test_postprocessor_verbose_json(self):
        pp = Postprocessor()
        raw = {
            "text": "你好世界",
            "language": "zh",
            "duration": 2.5,
            "segments": [
                {"start": 0.0, "end": 1.0, "text": "你好"},
                {"start": 1.0, "end": 2.5, "text": "世界"},
            ],
        }
        r = pp.process(raw, "verbose_json")
        assert r.text == "你好世界"
        assert r.language == "zh"
        assert r.duration == 2.5
        assert len(r.segments) == 2


class TestIFFManager:
    def test_iff_manager_healthy(self):
        """服务已健康 → 直接返回 base_url，不触发 iff switch"""
        with mock.patch("asr_service.iff_manager.httpx.get") as mock_get:
            mock_get.return_value = mock.Mock(status_code=200)
            mgr = IFFManager(base_url="http://localhost:8881")
            assert mgr.ensure_running() == "http://localhost:8881"
            mock_get.assert_called_once_with("http://localhost:8881/health", timeout=3)

    def test_iff_manager_switch(self):
        """服务不健康 → iff switch → 等待健康后返回 base_url"""
        with mock.patch("asr_service.iff_manager.httpx.get") as mock_get, \
                mock.patch("asr_service.iff_manager.subprocess.run") as mock_run:
            mock_get.side_effect = [
                mock.Mock(status_code=503),  # 初始检查：不健康
                mock.Mock(status_code=200),  # switch 后：健康
            ]
            mock_run.return_value = mock.Mock(returncode=0, stdout="ok", stderr="")
            mgr = IFFManager(base_url="http://localhost:8881", health_interval=0)
            assert mgr.ensure_running() == "http://localhost:8881"
            mock_run.assert_called_once()
            args, _ = mock_run.call_args
            assert args[0] == ["iff", "switch", "sensevoice-small"]

    def test_iff_manager_switch_failure(self):
        """iff switch 失败 → 抛 ASRServiceError"""
        with mock.patch("asr_service.iff_manager.httpx.get",
                        return_value=mock.Mock(status_code=503)), \
                mock.patch("asr_service.iff_manager.subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=1, stdout="", stderr="boom")
            mgr = IFFManager(base_url="http://localhost:8881")
            with pytest.raises(ASRServiceError):
                mgr.ensure_running()


class TestSkillTranscribe:
    def test_skill_transcribe(self, tmp_path):
        audio = tmp_path / "test.wav"
        audio.write_bytes(b"RIFF....WAVE")

        skill = ASRSkill()
        skill._iff_manager = mock.Mock()
        skill._iff_manager.ensure_running.return_value = "http://localhost:8881"

        with mock.patch("asr_service.skill.httpx.post") as mock_post:
            mock_post.return_value = mock.Mock(
                status_code=200,
                json=lambda: {"text": "你好世界"},
                text="你好世界",
            )
            result = skill.transcribe(audio)
            assert result.text == "你好世界"

            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            assert args[0] == "http://localhost:8881/v1/audio/transcriptions"
            assert kwargs["data"]["model"] == "sensevoice"
            assert kwargs["data"]["language"] == "auto"
            assert kwargs["data"]["response_format"] == "json"
            assert "spk" not in kwargs["data"]
            assert kwargs["timeout"] == 120

    def test_skill_transcribe_text_format(self, tmp_path):
        audio = tmp_path / "test.wav"
        audio.write_bytes(b"RIFF....WAVE")

        skill = ASRSkill()
        skill._iff_manager = mock.Mock()
        skill._iff_manager.ensure_running.return_value = "http://localhost:8881"

        with mock.patch("asr_service.skill.httpx.post") as mock_post:
            mock_post.return_value = mock.Mock(
                status_code=200,
                json=lambda: {"text": "你好世界"},
                text="你好世界",
            )
            result = skill.transcribe(audio, response_format="text")
            assert result.text == "你好世界"

    def test_skill_transcribe_missing_file(self, tmp_path):
        skill = ASRSkill()
        missing = tmp_path / "nope.wav"
        with pytest.raises(ASRTranscriptionError):
            skill.transcribe(missing)


class TestPostprocessorSubtitles:
    def test_postprocessor_to_srt(self):
        """SRT 格式：序号、HH:MM:SS,mmm 时间戳、块间空行"""
        pp = Postprocessor()
        segments = [
            {"start": 1.234, "end": 5.678, "text": "你好世界"},
            {"start": 6.0, "end": 10.5, "text": "我是第二个人"},
        ]
        srt = pp.to_srt(segments)
        assert srt == (
            "1\n00:00:01,234 --> 00:00:05,678\n你好世界\n\n"
            "2\n00:00:06,000 --> 00:00:10,500\n我是第二个人"
        )

    def test_postprocessor_to_srt_with_speaker(self):
        """带 speaker 时文本前加 [SPKx] 前缀"""
        pp = Postprocessor()
        segments = [
            {"start": 0.0, "end": 1.0, "text": "你好", "speaker": "SPK0"},
            {"start": 1.0, "end": 2.0, "text": "我是第二个人", "speaker": "SPK1"},
        ]
        srt = pp.to_srt(segments)
        assert srt.startswith("1\n00:00:00,000 --> 00:00:01,000\n[SPK0] 你好")
        assert "[SPK1] 我是第二个人" in srt

    def test_postprocessor_to_vtt(self):
        """VTT 格式：WEBVTT 头、时间戳用 . 分隔毫秒"""
        pp = Postprocessor()
        segments = [
            {"start": 1.234, "end": 5.678, "text": "你好世界"},
            {"start": 6.0, "end": 10.5, "text": "我是第二个人"},
        ]
        vtt = pp.to_vtt(segments)
        assert vtt.startswith("WEBVTT\n\n")
        assert "00:00:01.234 --> 00:00:05.678\n你好世界" in vtt
        assert "00:00:06.000 --> 00:00:10.500\n我是第二个人" in vtt


class TestSkillSubtitles:
    def test_skill_transcribe_with_speaker_labels(self, tmp_path):
        """speaker_labels=True 时传递 spk=true"""
        audio = tmp_path / "test.wav"
        audio.write_bytes(b"RIFF....WAVE")

        skill = ASRSkill()
        skill._iff_manager = mock.Mock()
        skill._iff_manager.ensure_running.return_value = "http://localhost:8881"

        with mock.patch("asr_service.skill.httpx.post") as mock_post:
            mock_post.return_value = mock.Mock(
                status_code=200,
                json=lambda: {"text": "你好世界"},
                text="你好世界",
            )
            result = skill.transcribe(audio, speaker_labels=True)
            assert result.text == "你好世界"
            _, kwargs = mock_post.call_args
            assert kwargs["data"]["spk"] == "true"

    def test_skill_transcribe_srt(self, tmp_path):
        """transcribe_srt 返回 SRT 字符串，内部走 verbose_json"""
        audio = tmp_path / "test.wav"
        audio.write_bytes(b"RIFF....WAVE")

        skill = ASRSkill()
        skill._iff_manager = mock.Mock()
        skill._iff_manager.ensure_running.return_value = "http://localhost:8881"

        with mock.patch("asr_service.skill.httpx.post") as mock_post:
            mock_post.return_value = mock.Mock(
                status_code=200,
                json=lambda: {
                    "text": "你好世界",
                    "language": "zh",
                    "duration": 2.5,
                    "segments": [
                        {"start": 1.234, "end": 5.678, "text": "你好世界"},
                    ],
                },
                text="",
            )
            srt = skill.transcribe_srt(audio)
            assert srt == "1\n00:00:01,234 --> 00:00:05,678\n你好世界"
            _, kwargs = mock_post.call_args
            assert kwargs["data"]["response_format"] == "verbose_json"

    def test_skill_transcribe_vtt(self, tmp_path):
        """transcribe_vtt 返回 VTT 字符串，内部走 verbose_json"""
        audio = tmp_path / "test.wav"
        audio.write_bytes(b"RIFF....WAVE")

        skill = ASRSkill()
        skill._iff_manager = mock.Mock()
        skill._iff_manager.ensure_running.return_value = "http://localhost:8881"

        with mock.patch("asr_service.skill.httpx.post") as mock_post:
            mock_post.return_value = mock.Mock(
                status_code=200,
                json=lambda: {
                    "text": "你好世界",
                    "segments": [
                        {"start": 1.234, "end": 5.678, "text": "你好世界"},
                    ],
                },
                text="",
            )
            vtt = skill.transcribe_vtt(audio)
            assert vtt == "WEBVTT\n\n00:00:01.234 --> 00:00:05.678\n你好世界"
            _, kwargs = mock_post.call_args
            assert kwargs["data"]["response_format"] == "verbose_json"
