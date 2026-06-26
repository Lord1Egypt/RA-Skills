"""
Pydantic models for FormatGate API.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SupportedFormat = Literal["json", "yaml", "toml"]


class ConvertRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str = Field(..., min_length=1, max_length=500_000, description="Content to convert.")
    input_format: SupportedFormat = Field(..., description="Format of the input.")
    output_format: SupportedFormat = Field(..., description="Desired output format.")


class ConvertResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool = Field(..., description="Whether conversion succeeded.")
    result: str = Field(default="", description="Converted content.")
    error: str = Field(default="", description="Error message if conversion failed.")
    input_format: str = Field(..., description="Input format used.")
    output_format: str = Field(..., description="Output format used.")
