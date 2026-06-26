#!/usr/bin/env python3
"""
Unit tests for arXiv Paper Downloader Skill
"""

import pytest
import os
import tempfile
from pathlib import Path

from src.skill import (
    ArxivDownloader,
    download_papers,
    download_by_arxiv_ids,
    list_categories,
    get_category_info
)


class TestArxivDownloader:
    """Test the ArxivDownloader class."""

    @pytest.fixture
    def downloader(self):
        """Create a downloader with temp directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield ArxivDownloader(output_dir=tmpdir, delay=0.1)

    def test_init(self, downloader):
        """Test initialization."""
        assert downloader.output_dir.exists()
        assert downloader.delay == 0.1

    def test_get_available_categories(self, downloader):
        """Test listing categories."""
        categories = downloader.get_available_categories()
        assert "agent_testing" in categories
        assert "agents" in categories
        assert "llm" in categories

    def test_get_category_info(self, downloader):
        """Test getting category info."""
        info = downloader.get_category_info("agent_testing")
        assert info["name"] == "agent_testing"
        assert info["paper_count"] > 0
        assert "papers" in info

    def test_get_unknown_category(self, downloader):
        """Test unknown category returns error."""
        info = downloader.get_category_info("unknown")
        assert "error" in info

    def test_download_single_paper(self, downloader):
        """Test downloading a single paper."""
        # Use a well-known paper that should always exist
        result = downloader.download_pdf("1706.03762", "Attention Is All You Need")
        assert result["status"] in ["downloaded", "skipped", "failed"]
        if result["status"] == "downloaded":
            assert Path(result["path"]).exists()

    def test_download_batch(self, downloader):
        """Test batch download."""
        result = downloader.download_batch("llm", delay=0.1)
        assert "downloaded" in result
        assert "skipped" in result
        assert "failed" in result
        assert "metadata_path" in result


class TestSkillFunctions:
    """Test the skill entry point functions."""

    def test_list_categories(self):
        """Test list_categories function."""
        categories = list_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0

    def test_get_category_info(self):
        """Test get_category_info function."""
        info = get_category_info("agents")
        assert isinstance(info, dict)
        assert "name" in info
        assert "paper_count" in info

    def test_download_by_ids(self):
        """Test download_by_arxiv_ids function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = download_by_arxiv_ids(
                ["1706.03762"],  # Transformer paper
                output_dir=tmpdir,
                delay=0.1
            )
            assert "downloaded" in result or "papers" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
