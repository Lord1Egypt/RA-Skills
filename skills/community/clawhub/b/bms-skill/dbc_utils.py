#!/usr/bin/env python3
"""
DBC Utility Functions for BMS CAN Analyzer Skill

This module provides functions to work with DBC files and validate signals.
"""

import cantools
import os
from typing import List, Dict, Optional


def load_dbc_file(dbc_path: str) -> cantools.database.can.Database:
    """
    Load a DBC file and return the database object.
    
    Args:
        dbc_path (str): Path to the DBC file
        
    Returns:
        cantools.database.can.Database: Loaded DBC database
        
    Raises:
        FileNotFoundError: If DBC file doesn't exist
        cantools.database.Error: If DBC file is invalid
    """
    if not os.path.exists(dbc_path):
        raise FileNotFoundError(f"DBC file not found: {dbc_path}")
    
    try:
        db = cantools.database.load_file(dbc_path)
        return db
    except Exception as e:
        raise cantools.database.Error(f"Failed to load DBC file: {e}")


def validate_signal_exists(db: cantools.database.can.Database, signal_name: str) -> bool:
    """
    Check if a signal exists in the DBC database.
    
    Args:
        db (cantools.database.can.Database): DBC database
        signal_name (str): Signal name to check
        
    Returns:
        bool: True if signal exists, False otherwise
    """
    for message in db.messages:
        for signal in message.signals:
            if signal.name == signal_name:
                return True
    return False


def get_signal_info(db: cantools.database.can.Database, signal_name: str) -> Dict:
    """
    Get detailed information about a signal.
    
    Args:
        db (cantools.database.can.Database): DBC database
        signal_name (str): Signal name
        
    Returns:
        Dict: Signal information including message ID, start bit, length, etc.
    """
    for message in db.messages:
        for signal in message.signals:
            if signal.name == signal_name:
                return {
                    'signal_name': signal.name,
                    'message_id': message.frame_id,
                    'message_name': message.name,
                    'start_bit': signal.start,
                    'length': signal.length,
                    'unit': signal.unit or 'N/A',
                    'minimum': signal.minimum,
                    'maximum': signal.maximum,
                    'scale': signal.scale,
                    'offset': signal.offset,
                    'is_signed': signal.is_signed,
                    'is_float': signal.is_float
                }
    return {}


def list_available_signals(db: cantools.database.can.Database) -> List[str]:
    """
    List all available signal names in the DBC database.
    
    Args:
        db (cantools.database.can.Database): DBC database
        
    Returns:
        List[str]: List of signal names
    """
    signals = []
    for message in db.messages:
        for signal in message.signals:
            signals.append(signal.name)
    return sorted(signals)


def get_message_for_signal(db: cantools.database.can.Database, signal_name: str):
    """
    Get the message object that contains the specified signal.
    
    Args:
        db (cantools.database.can.Database): DBC database
        signal_name (str): Signal name
        
    Returns:
        cantools.database.can.message.Message: Message containing the signal, or None
    """
    for message in db.messages:
        for signal in message.signals:
            if signal.name == signal_name:
                return message
    return None