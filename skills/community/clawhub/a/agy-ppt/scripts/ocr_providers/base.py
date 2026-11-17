"""Provider interface; execution and fallback orchestration live elsewhere."""
from abc import ABC, abstractmethod
from .models import OCRProviderCapabilities, OCRRequest, OCREvidence

class OCRProvider(ABC):
    @property
    @abstractmethod
    def provider_id(self) -> str: ...

    @property
    @abstractmethod
    def provider_version(self) -> str: ...

    @property
    @abstractmethod
    def capabilities(self) -> OCRProviderCapabilities: ...

    @abstractmethod
    def recognize(self, request: OCRRequest) -> OCREvidence: ...
