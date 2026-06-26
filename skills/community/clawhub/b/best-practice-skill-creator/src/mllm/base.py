"""Abstract base class for Multimodal LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MLLMResponse:
    text: str
    model: str
    usage: dict | None = None


class MLLMProvider(ABC):
    """Abstract interface for multimodal LLM providers."""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    @abstractmethod
    def analyze_images(
        self, images_base64: list[str], prompt: str
    ) -> MLLMResponse:
        """Send images with a text prompt to the MLLM and get a response.

        Args:
            images_base64: List of base64-encoded images.
            prompt: Text prompt describing what to analyze.

        Returns:
            MLLMResponse with the model's text output.
        """
        ...
