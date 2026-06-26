"""File storage service for temporary processing folders."""

import shutil
import tempfile
import uuid
from pathlib import Path


class FileService:
    """Service for temporary processing folders."""

    def __init__(self, base_dir: Path | None = None):
        self._base_dir = base_dir or Path(tempfile.gettempdir()) / "geminipdfocr"
        self._base_dir.mkdir(parents=True, exist_ok=True)

    @property
    def temp_dir(self) -> Path:
        """Directory for temporary processing files."""
        temp_path = self._base_dir / "temp"
        temp_path.mkdir(parents=True, exist_ok=True)
        return temp_path

    def create_temp_folder(self, prefix: str = "job") -> Path:
        """
        Create a temporary folder for processing.

        Args:
            prefix: Prefix for folder name

        Returns:
            Path to the created folder
        """
        folder_id = str(uuid.uuid4())[:8]
        folder_path = self.temp_dir / f"{prefix}_{folder_id}"
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path

    def cleanup_temp_folder(self, folder_path: Path) -> None:
        """
        Remove a temporary folder and its contents.

        Args:
            folder_path: Path to the folder to remove
        """
        if folder_path.exists() and folder_path.is_dir():
            shutil.rmtree(folder_path)


# Singleton instance
_file_service: FileService | None = None


def get_file_service() -> FileService:
    """Get or create singleton FileService instance."""
    global _file_service
    if _file_service is None:
        _file_service = FileService()
    return _file_service
