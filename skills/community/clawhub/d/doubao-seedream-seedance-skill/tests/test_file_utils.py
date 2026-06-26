"""
Tests for file utilities.

Tests verify file download, save, and organization.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import httpx
from toolkit.utils.file_utils import FileUtils
from toolkit.error_handler import FileError, NetworkError


class TestFileUtils:
    """Test cases for FileUtils."""
    
    def test_ensure_directory(self, tmp_path):
        """Test directory creation."""
        dir_path = tmp_path / "test" / "nested" / "dir"
        result = FileUtils.ensure_directory(dir_path)
        
        assert result.exists()
        assert result.is_dir()
    
    def test_ensure_directory_existing(self, tmp_path):
        """Test ensuring existing directory."""
        dir_path = tmp_path / "existing"
        dir_path.mkdir()
        
        result = FileUtils.ensure_directory(dir_path)
        assert result.exists()
    
    def test_save_bytes(self, tmp_path):
        """Test saving bytes to file."""
        data = b"test content"
        output_path = tmp_path / "test.bin"
        
        result = FileUtils.save_bytes(data, output_path)
        
        assert result.exists()
        assert result.read_bytes() == data
    
    def test_save_bytes_creates_directory(self, tmp_path):
        """Test saving bytes creates parent directory."""
        data = b"test"
        output_path = tmp_path / "nested" / "dir" / "test.bin"
        
        result = FileUtils.save_bytes(data, output_path)
        
        assert result.exists()
        assert result.read_bytes() == data
    
    def test_get_unique_filename(self, tmp_path):
        """Test getting unique filename."""
        result = FileUtils.get_unique_filename(tmp_path, "test", ".txt")
        
        assert result.parent == tmp_path
        assert result.name == "test.txt"
    
    def test_get_unique_filename_with_conflict(self, tmp_path):
        """Test unique filename when file exists."""
        (tmp_path / "test.txt").touch()
        
        result = FileUtils.get_unique_filename(tmp_path, "test", ".txt")
        
        assert result.name == "test_1.txt"
    
    def test_get_unique_filename_multiple_conflicts(self, tmp_path):
        """Test unique filename with multiple conflicts."""
        (tmp_path / "test.txt").touch()
        (tmp_path / "test_1.txt").touch()
        
        result = FileUtils.get_unique_filename(tmp_path, "test", ".txt")
        
        assert result.name == "test_2.txt"
    
    def test_get_unique_filename_extension_without_dot(self, tmp_path):
        """Test unique filename with extension without dot."""
        result = FileUtils.get_unique_filename(tmp_path, "test", "txt")
        
        assert result.name == "test.txt"
    
    def test_get_file_size(self, tmp_path):
        """Test getting file size."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")
        
        size = FileUtils.get_file_size(file_path)
        
        assert size == len(b"test content")
    
    def test_get_file_size_nonexistent(self, tmp_path):
        """Test getting size of nonexistent file."""
        file_path = tmp_path / "nonexistent.txt"
        
        with pytest.raises(FileError):
            FileUtils.get_file_size(file_path)
    
    @patch('httpx.Client.get')
    def test_download_file(self, mock_get, tmp_path):
        """Test file download."""
        mock_response = Mock()
        mock_response.iter_bytes.return_value = [b"test", b" content"]
        mock_response.raise_for_status = Mock()
        mock_get.return_value.__enter__ = Mock(return_value=Mock(get=Mock(return_value=mock_response)))
        
        url = "https://example.com/file.txt"
        output_path = tmp_path / "downloaded.txt"
        
        result = FileUtils.download_file(url, output_path)
        
        assert result.exists()
    
    @patch('httpx.Client.get')
    def test_download_file_network_error(self, mock_get, tmp_path):
        """Test download with network error."""
        mock_get.side_effect = httpx.NetworkError("Connection failed")
        
        url = "https://example.com/file.txt"
        output_path = tmp_path / "downloaded.txt"
        
        with pytest.raises(NetworkError):
            FileUtils.download_file(url, output_path)
    
    def test_organize_output(self, tmp_path):
        """Test organizing output file."""
        source = tmp_path / "output.png"
        source.write_bytes(b"image data")
        
        output_dir = tmp_path / "organized"
        result = FileUtils.organize_output(source, output_dir, "image", "task-123")
        
        assert result.exists()
        assert result.parent == output_dir / "image" / "task-123"
        assert not source.exists()
    
    def test_organize_output_same_location(self, tmp_path):
        """Test organizing when already in correct location."""
        output_dir = tmp_path / "organized"
        output_dir.mkdir()
        task_dir = output_dir / "image" / "task-123"
        task_dir.mkdir(parents=True)
        
        source = task_dir / "output.png"
        source.write_bytes(b"image data")
        
        result = FileUtils.organize_output(source, output_dir, "image", "task-123")
        
        assert result == source
        assert source.exists()
