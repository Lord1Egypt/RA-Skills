"""Gemini Client Wrapper for OCR and LLM interactions."""

from pathlib import Path

from google import genai

from config import settings


class GeminiClient:
    """Wrapper for Google Gemini API interactions."""

    DEFAULT_MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self._api_key = api_key or settings.google_api_key
        self._model = (
            model or getattr(settings, "ocr_model", None) or self.DEFAULT_MODEL
        )
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        """Lazy initialization of Gemini client."""
        if self._client is None:
            self._client = genai.Client(api_key=self._api_key)
        return self._client

    async def ocr_pdf_page_async(
        self, file_path: str | Path, prompt: str | None = None
    ) -> str:
        """
        Async version using native genai async client.
        Uses a dedicated client per call to avoid httpx connection sharing
        when multiple pages are processed concurrently.
        """
        prompt = prompt or "Extract absolutely all the text from the pdf"
        file_path = str(file_path)

        client = genai.Client(api_key=self._api_key)
        async with client.aio as aclient:
            file_to_ocr = await aclient.files.upload(file=file_path)
            response = await aclient.models.generate_content(
                model=self._model,
                contents=[prompt, file_to_ocr],
            )
            return response.candidates[0].content.parts[0].text


# Singleton instance
_gemini_client: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    """Get or create singleton Gemini client instance."""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
