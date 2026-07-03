from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def find_nth_char(
    text: str,
    char: str,
    n: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    Find index of nth occurrence of a character. Returns -1 if not found.
    
    Args:
        text: null
        char: null
        n: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "char": char,
        "n": n
    }
    
    return call_api("1777419060716547", "find_nth_char", arguments)

def find_all_char_indices(
    text: str,
    char: str
) -> Dict[str, Any]:
    """
    Find all indices where a character appears. Returns empty list if not found.
    
    Args:
        text: null
        char: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "char": char
    }
    
    return call_api("1777419060716547", "find_all_char_indices", arguments)

def find_nth_substring(
    text: str,
    substring: str,
    n: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    Find starting index of nth occurrence of a substring. Returns -1 if not found.
    
    Args:
        text: null
        substring: null
        n: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "substring": substring,
        "n": n
    }
    
    return call_api("1777419060716547", "find_nth_substring", arguments)

def find_all_substring_indices(
    text: str,
    substring: str
) -> Dict[str, Any]:
    """
    Find all starting indices where a substring appears (includes overlaps).
    
    Args:
        text: null
        substring: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "substring": substring
    }
    
    return call_api("1777419060716547", "find_all_substring_indices", arguments)

def split_at_indices(
    text: str,
    indices: null
) -> Dict[str, Any]:
    """
    Split text at exact index positions. Indices auto-sorted and deduplicated.
    
    Args:
        text: null
        indices: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "indices": indices
    }
    
    return call_api("1777419060716547", "split_at_indices", arguments)

def insert_at_index(
    text: str,
    index: int,
    insertion: str
) -> Dict[str, Any]:
    """
    Insert text at index position without replacing. Supports negative indices.
    
    Args:
        text: null
        index: null
        insertion: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "index": index,
        "insertion": insertion
    }
    
    return call_api("1777419060716547", "insert_at_index", arguments)

def delete_range(
    text: str,
    start: int,
    end: int
) -> Dict[str, Any]:
    """
    Delete characters in range [start, end).
    
    Args:
        text: null
        start: null
        end: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "start": start,
        "end": end
    }
    
    return call_api("1777419060716547", "delete_range", arguments)

def replace_range(
    text: str,
    start: int,
    end: int,
    replacement: str
) -> Dict[str, Any]:
    """
    Replace characters in range [start, end) with new text.
    
    Args:
        text: null
        start: null
        end: null
        replacement: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "start": start,
        "end": end,
        "replacement": replacement
    }
    
    return call_api("1777419060716547", "replace_range", arguments)

def find_regex_matches(
    text: str,
    pattern: str
) -> Dict[str, Any]:
    """
    Find all regex matches with positions. Returns list of {start, end, match} dicts.
    
    Args:
        text: null
        pattern: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "pattern": pattern
    }
    
    return call_api("1777419060716547", "find_regex_matches", arguments)

def extract_between_markers(
    text: str,
    start_marker: str,
    end_marker: str,
    occurrence: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    Extract content between markers with positions. Returns dict with content and position info.
    
    Args:
        text: null
        start_marker: null
        end_marker: null
        occurrence: null
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "start_marker": start_marker,
        "end_marker": end_marker,
        "occurrence": occurrence
    }
    
    return call_api("1777419060716547", "extract_between_markers", arguments)

def count_chars(
    text: str
) -> Dict[str, Any]:
    """
    Count character statistics. Returns dict with total, without_spaces, letters, digits, spaces, special.
    
    Args:
        text: null
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777419060716547", "count_chars", arguments)

def extract_substrings(
    text: str,
    ranges: null
) -> Dict[str, Any]:
    """
    Extract substrings by index ranges. Supports negative indices and omitting end. Returns list of {start, end, substring, length} dicts.
    
    Args:
        text: null
        ranges: null
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "ranges": ranges
    }
    
    return call_api("1777419060716547", "extract_substrings", arguments)

