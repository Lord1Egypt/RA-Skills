# -*- coding: utf-8 -*-
"""
Shared fixtures and configuration for article-to-video test suite.

Provides:
- Script path constants
- Sample input data fixtures
- Existing output data loaders (from the completed pipeline run)
"""

import json
import os
import subprocess
import sys
import tempfile
import shutil
import pytest

# ============================================================
# Path Setup
# ============================================================

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_ROOT, "scripts")
# SKILL_ROOT = .../article-to-video
# Need to go up 3 levels to reach workspace root:
#   article-to-video -> skills -> .trae -> ArticalToVideo
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(SKILL_ROOT)))

# Make scripts importable
sys.path.insert(0, SCRIPTS_DIR)


# ============================================================
# Path Fixtures
# ============================================================

@pytest.fixture(scope="session")
def scripts_dir():
    """Path to the scripts directory."""
    return SCRIPTS_DIR

@pytest.fixture(scope="session")
def workspace_dir():
    """Path to the workspace root."""
    return WORKSPACE

@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory."""
    d = os.path.join(SKILL_ROOT, "tests", "test_data")
    os.makedirs(d, exist_ok=True)
    return d


# ============================================================
# Sample Input Fixtures
# ============================================================

@pytest.fixture
def sample_txt_file(test_data_dir):
    """Create a sample .txt file for testing."""
    content = """第一章 引言

这是一个测试段落，用于验证文本解析功能是否正常工作。
它包含多个句子，应该被合并到同一个场景中。

第二章 方法

这是方法部分的说明。
讲述了如何实现文档到视频的转换。"""
    path = os.path.join(test_data_dir, "sample.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

@pytest.fixture
def sample_md_file(test_data_dir):
    """Create a sample .md file for testing."""
    content = """# 测试文档标题

## 第一节

这是一个 **加粗** 的段落，包含 [链接](http://example.com) 和 `行内代码`。

## 第二节

- 列表项一
- 列表项二

普通段落文本。
"""
    path = os.path.join(test_data_dir, "sample.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

@pytest.fixture
def sample_blocks():
    """Sample parsed blocks for scene building tests."""
    return [
        {"type": "heading", "level": 1, "text": "测试标题"},
        {"type": "paragraph", "level": 0, "text": "这是第一个段落的文本内容，用于测试场景构建。"},
        {"type": "heading", "level": 2, "text": "子章节"},
        {"type": "paragraph", "level": 0, "text": "这是第二个段落的文本内容，同样用于测试。"},
        {"type": "table", "level": 0, "text": "列1 | 列2 | 列3\n值1 | 值2 | 值3\n值4 | 值5 | 值6"},
    ]

@pytest.fixture
def sample_scene():
    """A single sample scene dict."""
    return {
        "index": 0,
        "heading": "测试场景标题",
        "level": 1,
        "narration": "这是一段用于测试的叙述文本。",
        "slide_text": "这是一段用于测试的叙述文本。",
        "image_prompt": "Test image prompt",
        "char_count": 14,
        "estimated_duration": 3.1,
        "text_hash": "abc123def456"
    }

@pytest.fixture
def sample_scenes_json(tmp_path):
    """Create a minimal scenes.json for testing downstream stages."""
    data = {
        "title": "测试视频标题",
        "scenes": [
            {
                "index": 0,
                "heading": "场景一",
                "level": 1,
                "narration": "这是第一个场景的叙述内容，用于测试。",
                "slide_text": "这是第一个场景的叙述内容。",
                "image_prompt": "Test prompt 1",
                "char_count": 20,
                "estimated_duration": 4.4,
                "text_hash": "hash001"
            },
            {
                "index": 1,
                "heading": "场景二",
                "level": 1,
                "narration": "这是第二个场景的叙述内容。",
                "slide_text": "这是第二个场景的叙述内容。",
                "image_prompt": "Test prompt 2",
                "char_count": 14,
                "estimated_duration": 3.1,
                "text_hash": "hash002"
            },
        ],
        "total_chars": 34,
        "estimated_duration_sec": 7.5,
        "language": "zh",
        "content_type": "default"
    }
    path = os.path.join(tmp_path, "scenes.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# ============================================================
# Content Type Test Data
# ============================================================

@pytest.fixture
def finance_blocks():
    """Sample blocks with finance keywords for content type detection."""
    return [
        {"type": "heading", "level": 1, "text": "2024年金融投资报告"},
        {"type": "paragraph", "level": 0,
         "text": "本季度股票市场表现良好，基金收益稳步增长。银行利率维持稳定，债券投资风险可控。"
                 "资产配置建议关注估值合理的优质标的，市盈率处于历史低位。"},
    ]


@pytest.fixture
def technology_blocks():
    """Sample blocks with technology keywords for content type detection."""
    return [
        {"type": "heading", "level": 1, "text": "人工智能技术发展趋势"},
        {"type": "paragraph", "level": 0,
         "text": "近年来人工智能和机器学习技术快速发展。云计算平台提供了强大的算法支持，"
                 "开源框架降低了开发门槛。大数据和API架构成为核心技术栈，区块链应用逐步落地。"},
    ]


@pytest.fixture
def business_blocks():
    """Sample blocks with business keywords for content type detection."""
    return [
        {"type": "heading", "level": 1, "text": "企业战略管理"},
        {"type": "paragraph", "level": 0,
         "text": "现代企业需要制定清晰的战略方向。市场营销和品牌运营是核心竞争力，"
                 "供应链管理和客户关系决定商业模式成败。竞争格局下的并购整合值得关注。"},
    ]


@pytest.fixture
def generic_blocks():
    """Sample blocks with no strong content type signal."""
    return [
        {"type": "heading", "level": 1, "text": "概述"},
        {"type": "paragraph", "level": 0,
         "text": "这是一段普通的文本内容，没有明显的内容类型特征。"},
    ]


@pytest.fixture
def sample_scenes_json_with_content_type(tmp_path):
    """Create a scenes.json with content_type set to 'technology'."""
    data = {
        "title": "AI技术深度解析",
        "scenes": [
            {
                "index": 0,
                "heading": "AI技术概述",
                "level": 1,
                "narration": "人工智能技术正在改变世界。",
                "slide_text": "人工智能技术概述",
                "image_prompt": "AI technology illustration",
                "char_count": 15,
                "estimated_duration": 3.3,
                "text_hash": "tech001"
            },
        ],
        "total_chars": 15,
        "estimated_duration_sec": 3.3,
        "language": "zh",
        "content_type": "technology"
    }
    path = os.path.join(tmp_path, "scenes_tech.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# ============================================================
# Existing Output Fixtures (from the completed pipeline run)
# ============================================================

@pytest.fixture(scope="session")
def existing_scenes_json(workspace_dir):
    """Load the existing scenes.json from the completed pipeline run."""
    path = os.path.join(workspace_dir, "scenes.json")
    if not os.path.exists(path):
        pytest.skip("scenes.json not found - run the pipeline first")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture(scope="session")
def existing_timing_json(workspace_dir):
    """Load the existing timing.json from the completed pipeline run."""
    path = os.path.join(workspace_dir, "audio", "timing.json")
    if not os.path.exists(path):
        pytest.skip("timing.json not found - run the pipeline first")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture(scope="session")
def existing_manifest_json(workspace_dir):
    """Load the existing slides manifest.json."""
    path = os.path.join(workspace_dir, "slides", "manifest.json")
    if not os.path.exists(path):
        pytest.skip("manifest.json not found - run the pipeline first")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture(scope="session")
def existing_video_path(workspace_dir):
    """Path to the existing final video output."""
    path = os.path.join(workspace_dir, "final_video.mp4")
    if not os.path.exists(path):
        pytest.skip("final_video.mp4 not found - run the pipeline first")
    return path

@pytest.fixture(scope="session")
def existing_srt_path(workspace_dir):
    """Path to the existing SRT subtitle file."""
    path = os.path.join(workspace_dir, "final_video.srt")
    if not os.path.exists(path):
        pytest.skip("final_video.srt not found - run the pipeline first")
    return path


# ============================================================
# Temp Directory Fixture
# ============================================================

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a clean temp directory for test outputs."""
    d = os.path.join(tmp_path, "output")
    os.makedirs(d, exist_ok=True)
    return d


# ============================================================
# Real Audio File Fixture (for BGM upload tests)
# ============================================================

@pytest.fixture(scope="session")
def sample_audio_file(tmp_path_factory):
    """Create a real, valid 5-second silent WAV file using ffmpeg.

    Uses WAV (PCM) format to avoid MP3 encoder dependency.
    This is needed because upload_bgm_file validates files with ffprobe,
    so fake null-byte files won't pass validation.
    """
    from config import PATHS_CONFIG
    ffmpeg = PATHS_CONFIG["ffmpeg"]
    audio_path = str(tmp_path_factory.mktemp("audio") / "test_silence.wav")
    result = subprocess.run(
        [
            ffmpeg,
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-t", "5",
            "-c:a", "pcm_s16le",
            "-y",
            audio_path,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"ffmpeg not available to create test audio: {result.stderr[:200]}")
    return audio_path
