#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Literature Search - Utility Functions
Common utilities for configuration, logging, and file operations.
"""

import os
import sys
import yaml
import logging
from pathlib import Path
from datetime import datetime

# ==================== Configuration Loading ====================

def load_config(config_path=None):
    """
    Load configuration from YAML file.
    Supports environment variable substitution.
    """
    if config_path is None:
        # Default config paths
        possible_paths = [
            Path(__file__).parent.parent / "config" / "config.yaml",
            Path(__file__).parent / "config.yaml",
            Path.cwd() / "config.yaml",
        ]
        for path in possible_paths:
            if path.exists():
                config_path = path
                break
    
    if config_path is None or not Path(config_path).exists():
        raise FileNotFoundError(
            "Configuration file not found. Please create config.yaml "
            "or specify path with --config option."
        )
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    # Substitute environment variables
    config_content = substitute_env_vars(config_content)
    
    # Parse YAML
    config = yaml.safe_load(config_content)
    
    # Resolve paths
    if 'papers_dir' in config:
        papers_dir = Path(config['papers_dir']).expanduser()
        config['papers_dir'] = papers_dir
        
        # Resolve category directories
        if 'categories' in config:
            for cat_key, cat_config in config['categories'].items():
                if 'directory' in cat_config:
                    cat_config['directory'] = papers_dir / cat_config['directory']
        
        # Resolve log directory
        if 'log_dir' in config:
            config['log_dir'] = papers_dir / config['log_dir']
        
        # Resolve upload directory
        if 'upload_dir' in config:
            config['upload_dir'] = papers_dir / config['upload_dir']
    
    return config

def substitute_env_vars(content):
    """
    Substitute environment variables in YAML content.
    Supports: ${VAR_NAME} and ${VAR_NAME:-default}
    """
    import re
    
    def replace_env(match):
        var_expr = match.group(1)
        if ':-' in var_expr:
            # With default value: ${VAR:-default}
            var_name, default = var_expr.split(':-', 1)
            return os.getenv(var_name, default)
        else:
            # Simple variable: ${VAR}
            var_name = var_expr
            return os.getenv(var_name, '')
    
    pattern = r'\$\{([^}]+)\}'
    return re.sub(pattern, replace_env, content)

# ==================== Logging Setup ====================

def setup_logging(config, log_file=None):
    """
    Configure logging based on configuration.
    """
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO').upper())
    
    # Create logger
    logger = logging.getLogger('daily_literature')
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Console handler
    if log_config.get('console', True):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_config.get('file', True) and log_file:
        # Ensure log directory exists
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

# ==================== Directory Management ====================

def ensure_directories(config):
    """
    Create necessary directories if they don't exist.
    """
    dirs_to_create = []
    
    # Category directories
    if 'categories' in config:
        for cat_config in config['categories'].values():
            if 'directory' in cat_config:
                dirs_to_create.append(cat_config['directory'])
    
    # Log directory
    if 'log_dir' in config:
        dirs_to_create.append(config['log_dir'])
    
    # Upload directory
    if 'upload_dir' in config:
        dirs_to_create.append(config['upload_dir'])
    
    # Create all directories
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)

# ==================== Date/Time Utilities ====================

def get_today_str():
    """Get today's date as YYYY-MM-DD string."""
    return datetime.now().strftime("%Y-%m-%d")

def get_timestamp_str():
    """Get current timestamp as YYYY-MM-DD HH:MM:SS string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_cutoff_date(days):
    """Get cutoff date for filtering (N days ago)."""
    from datetime import timedelta
    return datetime.now() - timedelta(days=days)

# ==================== DOI Utilities ====================

def normalize_doi(doi):
    """
    Normalize DOI to standard format.
    Removes https://doi.org/ prefix and converts to lowercase.
    """
    if not doi:
        return None
    
    doi = str(doi).strip()
    
    # Remove common prefixes
    prefixes = [
        "https://doi.org/",
        "http://doi.org/",
        "doi.org/",
        "doi:",
    ]
    
    for prefix in prefixes:
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
            break
    
    return doi.lower()

def extract_doi_from_text(text):
    """
    Extract DOI from text using regex.
    Returns first match or None.
    """
    import re
    
    doi_pattern = r"10\.\d+[/\w\.\-]+"
    matches = re.findall(doi_pattern, text, re.IGNORECASE)
    
    return matches[0] if matches else None

# ==================== File Utilities ====================

def safe_filename(title, max_length=50):
    """
    Create a safe filename from title.
    Removes special characters and limits length.
    """
    import re
    
    # Remove special characters
    safe_name = re.sub(r'[^\w\s\-\.\(\)]', '', title)
    
    # Replace multiple spaces with single space
    safe_name = re.sub(r'\s+', ' ', safe_name)
    
    # Truncate to max length
    safe_name = safe_name[:max_length].strip()
    
    # Replace spaces with underscores
    safe_name = safe_name.replace(' ', '_')
    
    return safe_name

def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

# ==================== Report Utilities ====================

def generate_report_filename(prefix, date=None):
    """Generate standardized report filename."""
    if date is None:
        date = get_today_str()
    return f"{prefix}_{date}.md"

def generate_log_filename(prefix, date=None):
    """Generate standardized log filename."""
    if date is None:
        date = get_today_str()
    return f"{prefix}_{date}.log"
