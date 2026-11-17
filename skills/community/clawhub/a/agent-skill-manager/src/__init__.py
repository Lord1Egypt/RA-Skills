"""Agent Skill Manager - Cross-platform skill management for domestic AI agent products.

Layered package layout (mirrors MoneyPrinterTurbo's ``app/`` structure):
    config/       product registry & platform constants
    controllers/  user-facing CLI
    models/       typed data shapes (TypedDicts)
    services/     business logic (sync, audit)
    utils/        cross-platform filesystem helpers
"""

__version__ = "0.7.0"
__all__ = ["config", "controllers", "models", "services", "utils"]
