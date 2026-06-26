"""
Format utilities for Volcengine API Skill.

Provides formatting for file sizes, durations, and timestamps.
"""

from datetime import datetime
from typing import Union


class Formatters:
    """Formatting utilities."""
    
    @staticmethod
    def format_file_size(bytes_size: Union[int, float]) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            bytes_size: Size in bytes
            
        Returns:
            Formatted string (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if abs(bytes_size) < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} PB"
    
    @staticmethod
    def format_duration(seconds: Union[int, float]) -> str:
        """
        Format duration in human-readable format.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted string (e.g., "2m 30s")
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    @staticmethod
    def format_timestamp(
        timestamp: Union[datetime, str, float],
        format_str: str = "%Y-%m-%d %H:%M:%S"
    ) -> str:
        """
        Format timestamp to string.
        
        Args:
            timestamp: Datetime object, ISO string, or Unix timestamp
            format_str: Output format string
            
        Returns:
            Formatted timestamp string
        """
        if isinstance(timestamp, datetime):
            dt = timestamp
        elif isinstance(timestamp, str):
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            dt = datetime.fromtimestamp(timestamp)
        
        return dt.strftime(format_str)
    
    @staticmethod
    def format_progress(current: int, total: int, width: int = 50) -> str:
        """
        Format progress bar.
        
        Args:
            current: Current progress value
            total: Total value
            width: Progress bar width in characters
            
        Returns:
            Progress bar string
        """
        if total == 0:
            percentage = 100
        else:
            percentage = min(100, int((current / total) * 100))
        
        filled = int(width * percentage / 100)
        bar = '█' * filled + '░' * (width - filled)
        
        return f"[{bar}] {percentage}%"
    
    @staticmethod
    def format_number(number: Union[int, float]) -> str:
        """
        Format number with thousand separators.
        
        Args:
            number: Number to format
            
        Returns:
            Formatted string (e.g., "1,234,567")
        """
        return f"{number:,}"
    
    @staticmethod
    def format_percentage(value: Union[int, float], decimals: int = 1) -> str:
        """
        Format percentage.
        
        Args:
            value: Value between 0 and 100
            decimals: Number of decimal places
            
        Returns:
            Formatted string (e.g., "95.5%")
        """
        return f"{value:.{decimals}f}%"
