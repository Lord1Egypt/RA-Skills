"""Error and exit code definitions (migrated from legacy script)."""

from enum import IntEnum


class ExitCode(IntEnum):
    SUCCESS = 0
    NETWORK_ERROR = 10
    DATA_ERROR = 20
    VALIDATION_ERROR = 30
    FILE_ERROR = 40


class CharacterLoaderError(Exception):
    exit_code = ExitCode.DATA_ERROR


class NetworkError(CharacterLoaderError):
    exit_code = ExitCode.NETWORK_ERROR


class DataError(CharacterLoaderError):
    exit_code = ExitCode.DATA_ERROR


class ValidationError(CharacterLoaderError):
    exit_code = ExitCode.VALIDATION_ERROR


class FileError(CharacterLoaderError):
    exit_code = ExitCode.FILE_ERROR
