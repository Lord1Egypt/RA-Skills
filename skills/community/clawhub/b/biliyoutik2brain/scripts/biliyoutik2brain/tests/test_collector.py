"""
BiliYouTik2Brain — 采集策略决策测试
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.collector import CollectionResult, decide_strategy


class TestDecideStrategy:
    """采集策略决策测试"""

    def test_subtitle_available(self):
        """有字幕时优先用字幕"""
        cr = CollectionResult(
            url="https://example.com/video",
            subtitle_available=True,
            subtitle_text="这是字幕文本" * 20,  # >50 字符
            audio_path="/tmp/test.m4a",
        )
        assert decide_strategy(cr) == "subtitle"

    def test_subtitle_too_short(self):
        """字幕太短时回退到音频（如音频路径存在）"""
        cr = CollectionResult(
            url="https://example.com/video",
            subtitle_available=True,
            subtitle_text="短",
            audio_path="",  # 无音频→回退video
        )
        assert decide_strategy(cr) in ("audio", "video")

    def test_no_audio_no_subtitle(self):
        """无字幕无音频时回退到视频"""
        cr = CollectionResult(
            url="https://example.com/video",
            subtitle_available=False,
            audio_path="",
        )
        assert decide_strategy(cr) == "video"

    def test_audio_path_exists(self):
        """有真实音频文件路径时优先用音频"""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as f:
            f.write(b"fake audio")
            audio_path = f.name
        try:
            cr = CollectionResult(
                url="https://example.com/video",
                subtitle_available=False,
                audio_path=audio_path,
            )
            assert decide_strategy(cr) == "audio"
        finally:
            os.unlink(audio_path)


class TestCollectionResult:
    """数据结构完整性测试"""

    def test_default_values(self):
        cr = CollectionResult(url="https://example.com/video")
        assert cr.subtitle_available is False
        assert cr.audio_path == ""
        assert cr.duration_s == 0
        assert cr.recommended_strategy == ""

    def test_full_initialization(self):
        cr = CollectionResult(
            url="https://example.com/video",
            video_title="测试视频",
            uploader="测试UP主",
            duration_s=300,
            subtitle_available=True,
            subtitle_text="测试字幕",
            audio_path="/tmp/audio.m4a",
        )
        assert cr.video_title == "测试视频"
        assert cr.uploader == "测试UP主"
        assert cr.duration_s == 300
