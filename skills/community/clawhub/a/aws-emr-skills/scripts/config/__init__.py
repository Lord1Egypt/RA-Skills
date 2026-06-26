"""Unified EMR Skill configuration.

Exports:
    EMRSkillConfig: Dataclass holding all configuration fields.
    EMRSkillConfigError: Exception for configuration errors.
    load_emr_skill_config: Factory function to load config from env/file.
"""

from scripts.config.emr_config import (
    EMRSkillConfig,
    EMRSkillConfigError,
    load_emr_skill_config,
)

__all__ = [
    "EMRSkillConfig",
    "EMRSkillConfigError",
    "load_emr_skill_config",
]
