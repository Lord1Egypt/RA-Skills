#!/usr/bin/env python3
# mcp_orchestral Hilfsfunktionen

import logging
logger = logging.getLogger(__name__)

def validate_input(data):
    """Validiert Eingabedaten"""
    if not data:
        logger.error("Eingabedaten sind leer")
        return False
    return True

def format_output(data):
    """Formatiert Ausgabedaten"""
    if not data:
        return ""
    return str(data)

def log_error(error):
    """Protokolliert Fehler"""
    logger.error(f"Error: {error}")
