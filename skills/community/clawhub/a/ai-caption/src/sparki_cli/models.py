"""Pydantic models for API responses and CLI output."""

from pydantic import BaseModel, computed_field

from sparki_cli.constants import TELEGRAM_FILE_SIZE_LIMIT


class AssetInfo(BaseModel):
    object_key: str
    file_name: str
    status: int
    file_size: int
    is_duplicate: bool = False
    duration: float | None = None
    resolution: str | None = None


class UploadResponse(BaseModel):
    object_key: str
    file_name: str
    file_size: int
    status: int
    is_duplicate: bool = False


class ProjectInfo(BaseModel):
    task_id: str
    status: str
    created_at: str | None = None
    result_url: str | None = None
    thumbnail_url: str | None = None
    duration: float | None = None
    resolution: str | None = None
    filesize: int | None = None


class DownloadResult(BaseModel):
    task_id: str
    file_path: str
    file_size: int
    result_url: str

    @computed_field
    @property
    def delivery_hint(self) -> str:
        return "telegram_direct" if self.file_size <= TELEGRAM_FILE_SIZE_LIMIT else "link_only"


class RunResult(BaseModel):
    task_id: str
    status: str
    file_path: str
    file_size: int
    result_url: str

    @computed_field
    @property
    def delivery_hint(self) -> str:
        return "telegram_direct" if self.file_size <= TELEGRAM_FILE_SIZE_LIMIT else "link_only"
