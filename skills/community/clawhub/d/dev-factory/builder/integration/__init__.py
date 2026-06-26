"""통합 모듈 (Notion, GitHub, Memory)

Phase 1: Basic integration
Phase 2: Enhanced spec validation and template management
"""

from builder.integration.notion_sync import NotionSync
from builder.integration.spec_validator import SpecValidator, SpecValidationReport
from builder.integration.template_manager import SpecTemplateManager

__all__ = [
    'NotionSync',
    'SpecValidator',
    'SpecValidationReport',
    'SpecTemplateManager'
]
