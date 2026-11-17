"""Abstract base adapter - re-exports from llm_core for backward compatibility."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from llm_core.adapters.base import BaseAdapter
from llm_core.types import ChatMessage, ChatResponse, ContentChunk, ToolCall

__all__ = ["BaseAdapter", "ChatMessage", "ChatResponse", "ContentChunk", "ToolCall"]
