"""
Tests for guide generator.

Tests verify guidance generation and contextual suggestions.
"""

import pytest
from toolkit.guide_generator import GuideGenerator
from toolkit.models.base import TaskType
from toolkit.state_manager import StateManager


class TestGuideGenerator:
    """Test cases for GuideGenerator."""
    
    def test_get_welcome_guide(self):
        """Test welcome guide generation."""
        guide = GuideGenerator.get_welcome_guide()
        
        assert "火山引擎API助手" in guide
        assert "生成图像" in guide
        assert "生成视频" in guide
        assert "视觉理解" in guide
        assert "任务管理" in guide
    def test_get_post_operation_guide_image(self):
        """Test post-operation guide for image."""
        guide = GuideGenerator.get_post_operation_guide(TaskType.IMAGE_GENERATION)
        
        assert "图片生成成功" in guide
        assert "生成视频" in guide
    
    def test_get_post_operation_guide_image_with_url(self):
        """Test post-operation guide with URL."""
        result = {"url": "https://example.com/image.png"}
        guide = GuideGenerator.get_post_operation_guide(TaskType.IMAGE_GENERATION, result)
        
        assert "https://example.com/image.png" in guide
    
    def test_get_post_operation_guide_video(self):
        """Test post-operation guide for video."""
        guide = GuideGenerator.get_post_operation_guide(TaskType.VIDEO_T2V)
        
        assert "视频生成成功" in guide
        assert "继续创作" in guide or "提取视频帧" in guide
    
    def test_get_post_operation_guide_video_with_url(self):
        """Test post-operation guide with video URL."""
        result = {"url": "https://example.com/video.mp4"}
        guide = GuideGenerator.get_post_operation_guide(TaskType.VIDEO_I2V, result)
        
        assert "https://example.com/video.mp4" in guide
    
    def test_get_post_operation_guide_vision(self):
        """Test post-operation guide for vision."""
        guide = GuideGenerator.get_post_operation_guide(TaskType.VISION_DETECTION)
        
        assert "图像分析完成" in guide
    def test_get_contextual_suggestions_with_preferences(self, tmp_path):
        """Test contextual suggestions with user preferences."""
        state_manager = StateManager(state_dir=tmp_path)
        state_manager.set_preference("default_model", "seedream-4.0")
        
        suggestions = GuideGenerator.get_contextual_suggestions(state_manager)
        
        assert len(suggestions) > 0
        assert any("seedream-4.0" in s for s in suggestions)
    
    def test_get_contextual_suggestions_with_history(self, tmp_path):
        """Test contextual suggestions with operation history."""
        state_manager = StateManager(state_dir=tmp_path)
        state_manager.add_history_entry("image_generation")
        state_manager.add_history_entry("image_generation")
        state_manager.add_history_entry("video_generation")
        
        suggestions = GuideGenerator.get_contextual_suggestions(state_manager)
        
        assert len(suggestions) > 0
        assert any("image_generation" in s for s in suggestions)
    
    def test_get_contextual_suggestions_with_context(self, tmp_path):
        """Test contextual suggestions with current context."""
        state_manager = StateManager(state_dir=tmp_path)
        context = {"has_image": True}
        
        suggestions = GuideGenerator.get_contextual_suggestions(state_manager, context)
        
        assert any("视频" in s for s in suggestions)
    
    def test_get_contextual_suggestions_limited(self, tmp_path):
        """Test suggestions are limited to top 3."""
        state_manager = StateManager(state_dir=tmp_path)
        state_manager.set_preference("key1", "value1")
        state_manager.set_preference("key2", "value2")
        state_manager.set_preference("key3", "value3")
        state_manager.set_preference("key4", "value4")
        
        for i in range(10):
            state_manager.add_history_entry(f"operation_{i}")
        
        suggestions = GuideGenerator.get_contextual_suggestions(state_manager)
        
        assert len(suggestions) <= 3
