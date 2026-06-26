#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Error handling utilities for Auto Create AI Team Skill
"""

import sys
import os
import logging
from pathlib import Path


class AITeamError(Exception):
    """Base exception for AI Team errors"""
    pass


class ProjectPathError(AITeamError):
    """Raised when project path is invalid"""
    pass


class ConfigurationError(AITeamError):
    """Raised when configuration is invalid"""
    pass


def setup_logging(log_file=None):
    """Setup logging for the skill"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )


def validate_project_path(project_path):
    """Validate project path exists and is accessible"""
    path = Path(project_path)
    if not path.exists():
        raise ProjectPathError(f"Project path does not exist: {project_path}")
    if not path.is_dir():
        raise ProjectPathError(f"Project path is not a directory: {project_path}")
    if not os.access(path, os.W_OK):
        raise ProjectPathError(f"Project path is not writable: {project_path}")


def handle_error(error, project_path=None, logger=None):
    """Handle errors gracefully
    
    Args:
        error: The error that occurred
        project_path: Optional project path to write error log to
        logger: Optional logger instance
    """
    if logger:
        logger.error(f"Error occurred: {str(error)}")
    else:
        print(f"Error: {str(error)}", file=sys.stderr)
    
    # Write to project-specific error log if project_path provided
    if project_path:
        try:
            error_log = Path(project_path) / "ai-team" / "logs" / "errors.log"
            error_log.parent.mkdir(parents=True, exist_ok=True)
            with open(error_log, "a", encoding="utf-8") as f:
                f.write(f"{error}\n")
        except Exception:
            pass  # Don't fail on error logging failure


def safe_create_directory(path):
    """Safely create directory with error handling"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        raise AITeamError(f"Failed to create directory {path}: {str(e)}")