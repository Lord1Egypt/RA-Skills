"""Factory for creating MLLM provider instances."""

from ..config import ProviderConfig
from .base import MLLMProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider

_PROVIDERS: dict[str, type[MLLMProvider]] = {
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
}


def create_provider(name: str, config: ProviderConfig) -> MLLMProvider:
    """Create an MLLM provider by name.

    Args:
        name: Provider identifier ("openai" or "gemini").
        config: Provider configuration with api_key, base_url, model.

    Returns:
        Configured MLLMProvider instance.

    Raises:
        ValueError: If the provider name is not supported.
    """
    cls = _PROVIDERS.get(name)
    if cls is None:
        supported = ", ".join(sorted(_PROVIDERS))
        raise ValueError(
            f"Unknown provider '{name}'. Supported: {supported}"
        )

    if not config.api_key:
        raise ValueError(
            f"API key is required for provider '{name}'. "
            "Set it in config.yaml or via MLLM_API_KEY environment variable."
        )

    return cls(
        api_key=config.api_key,
        base_url=config.base_url,
        model=config.model,
    )
