import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "cxm") -> logging.Logger:
    """Configures a logger that writes to ~/.cxm/logs/cxm.log"""
    log_dir = Path.home() / ".cxm" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "cxm.log"

    logger = logging.getLogger(name)
    
    # Only add handlers if they don't exist yet to avoid duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File Handler (Rotating: 5MB per file, max 3 files)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Optional: Console Handler (for errors only in CLI)
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.ERROR)
        # logger.addHandler(console_handler)

    return logger

# Global default logger
logger = setup_logger()
