class DatabaseSkillError(Exception):
    """Base exception for all database-skill errors."""


class DatabaseConnectionError(DatabaseSkillError):
    """Raised when database connection fails."""


class QueryError(DatabaseSkillError):
    """Raised when SQL query execution fails."""


class ConfigurationError(DatabaseSkillError):
    """Raised when configuration loading fails."""


class UnsupportedDatabaseError(DatabaseSkillError):
    """Raised when the JDBC URL does not match any supported database."""
