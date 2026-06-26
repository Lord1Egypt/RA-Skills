"""
File utilities for Volcengine API Skill.

Provides file download, save, and organization utilities.
"""

from pathlib import Path
from typing import Optional, Union
import httpx
from toolkit.error_handler import FileError, NetworkError


class FileUtils:
    """Utilities for file operations."""
    
    @staticmethod
    def download_file(
        url: str,
        output_path: Union[str, Path],
        chunk_size: int = 8192
    ) -> Path:
        """
        Download file from URL.
        
        Args:
            url: File URL to download
            output_path: Local path to save file
            chunk_size: Download chunk size in bytes
            
        Returns:
            Path to downloaded file
            
        Raises:
            NetworkError: On download failure
            FileError: On file write failure
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.get(url, follow_redirects=True)
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_bytes(chunk_size=chunk_size):
                        f.write(chunk)
                
                return output_path
                
        except httpx.HTTPError as e:
            raise NetworkError(
                message=f"Failed to download file from {url}",
                original_error=str(e)
            )
        except IOError as e:
            raise FileError(
                message=f"Failed to write file to {output_path}",
                file_path=str(output_path),
                original_error=str(e)
            )
    
    @staticmethod
    def save_bytes(
        data: bytes,
        output_path: Union[str, Path]
    ) -> Path:
        """
        Save bytes to file.
        
        Args:
            data: Bytes to save
            output_path: Local path to save file
            
        Returns:
            Path to saved file
            
        Raises:
            FileError: On file write failure
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'wb') as f:
                f.write(data)
            return output_path
        except IOError as e:
            raise FileError(
                message=f"Failed to save file to {output_path}",
                file_path=str(output_path),
                original_error=str(e)
            )
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if needed.
        
        Args:
            path: Directory path
            
        Returns:
            Path object for directory
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def get_unique_filename(
        directory: Union[str, Path],
        base_name: str,
        extension: str
    ) -> Path:
        """
        Get unique filename in directory.
        
        Args:
            directory: Directory path
            base_name: Base filename without extension
            extension: File extension (with or without dot)
            
        Returns:
            Path to unique filename
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        
        if not extension.startswith('.'):
            extension = f'.{extension}'
        
        counter = 0
        filename = f"{base_name}{extension}"
        filepath = directory / filename
        
        while filepath.exists():
            counter += 1
            filename = f"{base_name}_{counter}{extension}"
            filepath = directory / filename
        
        return filepath
    
    @staticmethod
    def get_file_size(path: Union[str, Path]) -> int:
        """
        Get file size in bytes.
        
        Args:
            path: File path
            
        Returns:
            File size in bytes
            
        Raises:
            FileError: If file doesn't exist
        """
        path = Path(path)
        
        if not path.exists():
            raise FileError(
                message=f"File not found: {path}",
                file_path=str(path)
            )
        
        return path.stat().st_size
    
    @staticmethod
    def organize_output(
        file_path: Union[str, Path],
        output_dir: Union[str, Path],
        task_type: str,
        task_id: str
    ) -> Path:
        """
        Organize output file into structured directory.
        
        Args:
            file_path: Source file path
            output_dir: Base output directory
            task_type: Type of task (image, video, audio)
            task_id: Task identifier
            
        Returns:
            Path to organized file
        """
        file_path = Path(file_path)
        output_dir = Path(output_dir)
        
        organized_dir = output_dir / task_type / task_id
        organized_dir.mkdir(parents=True, exist_ok=True)
        
        organized_path = organized_dir / file_path.name
        
        if file_path != organized_path:
            file_path.rename(organized_path)
        
        return organized_path
