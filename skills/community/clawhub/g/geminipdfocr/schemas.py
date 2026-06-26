"""Schemas for OCR Cloud module - Gemini cloud OCR processing."""

from pydantic import BaseModel, ConfigDict, Field


class OcrPageSchema(BaseModel):
    """Schema for a single OCR-processed page."""

    model_config = ConfigDict(from_attributes=True)

    page_number: int = Field(..., description="Page number (1-indexed)")
    text: str = Field(..., description="Extracted text from the page")
    status: str = Field(..., description="Processing status: success, error, skipped")
    char_count: int = Field(0, description="Number of characters extracted")
    error: str | None = Field(None, description="Error message if status is error")


class OcrResultSchema(BaseModel):
    """Schema for OCR result of a complete document."""

    model_config = ConfigDict(from_attributes=True)

    pdf_name: str = Field(..., description="Original PDF filename")
    total_pages: int = Field(..., description="Total number of pages processed")
    pages: list[OcrPageSchema] = Field(
        default_factory=list, description="OCR results per page"
    )
    total_chars: int = Field(0, description="Total characters extracted")
    status: str = Field("success", description="Overall processing status")
