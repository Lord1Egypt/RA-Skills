from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class CreateDocResult:
    document_id: str
    title: str | None = None
    raw: Any = None


@dataclass(slots=True)
class TextElementSummary:
    content: str | None = None
    text_color: int | None = None
    background_color: int | None = None
    bold: bool | None = None
    italic: bool | None = None
    underline: bool | None = None
    strikethrough: bool | None = None
    inline_code: bool | None = None
    raw: Any = None


@dataclass(slots=True)
class DocumentMeta:
    document_id: str
    title: str | None = None
    revision_id: int | None = None
    raw: Any = None


@dataclass(slots=True)
class BlockSummary:
    block_id: str
    parent_id: str | None
    block_type: int
    text: str | None = None
    children: list[str] | None = None
    elements: list[TextElementSummary] | None = None
    raw: Any = None


@dataclass(slots=True)
class DocumentReadResult:
    meta: DocumentMeta
    raw_content: str | None
    blocks: list[BlockSummary]


@dataclass(slots=True)
class AppendBlocksResult:
    document_id: str
    parent_block_id: str
    block_ids: list[str]
    raw: Any = None


@dataclass(slots=True)
class UploadImageResult:
    file_token: str
    raw: Any = None
