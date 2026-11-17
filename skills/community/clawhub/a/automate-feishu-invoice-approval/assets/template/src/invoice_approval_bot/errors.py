class BotError(RuntimeError):
    """Base error for expected bot failures."""


class ConfigurationError(BotError):
    """Configuration is missing or invalid."""


class LarkCliError(BotError):
    """A lark-cli operation failed."""


class VisionError(BotError):
    """Codex vision extraction failed."""


class MappingError(BotError):
    """Approval mapping could not be rendered."""

