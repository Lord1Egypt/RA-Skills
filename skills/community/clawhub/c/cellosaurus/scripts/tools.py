from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_cell_lines(
    query: Optional[str] = "id:HeLa",
    fields: Optional[null] = None,
    start: Optional[int] = 0.0,
    rows: Optional[int] = 10.0,
    sort_order: Optional[null] = None
) -> Dict[str, Any]:
    """
    Search for cell lines in the Cellosaurus database.

Use Solr search syntax to find cell lines by various criteria.

Examples
--------
- Basic name search: "id:HeLa" or "sy:HeLa"
- Species filter: "ox:human" or "ox:9606"
- Disease filter: "di:cancer" or "di:hepatoblastoma"
- Combined: "ox:human di:cancer ca:cancer"
- Site filter: "derived-from-site:liver"

Args:
    query: Search query using Solr syntax (default: "id:HeLa")
    fields: List of fields to return (e.g., ["id", "ac", "ox", "di"])
    start: Starting index for pagination (default: 0)
    rows: Number of results to return (default: 10, max: 1000)
    sort_order: Sort order (e.g., "group asc,derived-from-site desc")

Returns
-------
    Dictionary containing search results with cell line information
    
    Args:
        query: null
        fields: null
        start: null
        rows: null
        sort_order: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "fields": fields,
        "start": start,
        "rows": rows,
        "sort_order": sort_order
    }
    
    return call_api("1777419071553539", "search_cell_lines", arguments)

def get_cell_line_info(
    accession: str,
    fields: Optional[null] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific cell line by its accession number.

Args:
    accession: Cell line accession number (e.g., "CVCL_0030" for HeLa)
    fields: List of specific fields to return (e.g., ["id", "ac", "str", "di"])

Returns
-------
    Dictionary containing detailed cell line information
    
    Args:
        accession: null
        fields: null
    
    Returns:
        null
    """
    arguments = {
        "accession": accession,
        "fields": fields
    }
    
    return call_api("1777419071553539", "get_cell_line_info", arguments)

def get_release_info(
) -> Dict[str, Any]:
    """
    Get information about the current Cellosaurus database release.

Returns
-------
    Dictionary containing release version, date, and statistics
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419071553539", "get_release_info", arguments)

def find_cell_lines_by_disease(
    disease: str,
    species: Optional[str] = "human",
    fields: Optional[null] = None,
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    Find cell lines derived from patients with a specific disease.

Args:
    disease: Disease name or term (e.g., "hepatoblastoma", "cancer", "leukemia")
    species: Species filter (default: "human", can be "mouse", "rat", etc.)
    fields: Specific fields to return
    limit: Maximum number of results (default: 10)

Returns
-------
    Dictionary containing cell lines associated with the disease
    
    Args:
        disease: null
        species: null
        fields: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "disease": disease,
        "species": species,
        "fields": fields,
        "limit": limit
    }
    
    return call_api("1777419071553539", "find_cell_lines_by_disease", arguments)

def find_cell_lines_by_tissue(
    tissue: str,
    species: Optional[str] = "human",
    fields: Optional[null] = None,
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    Find cell lines derived from a specific tissue or organ.

Args:
    tissue: Tissue/organ name (e.g., "liver", "lung", "breast", "brain")
    species: Species filter (default: "human")
    fields: Specific fields to return
    limit: Maximum number of results (default: 10)

Returns
-------
    Dictionary containing cell lines from the specified tissue
    
    Args:
        tissue: null
        species: null
        fields: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "tissue": tissue,
        "species": species,
        "fields": fields,
        "limit": limit
    }
    
    return call_api("1777419071553539", "find_cell_lines_by_tissue", arguments)

def list_available_fields(
) -> Dict[str, Any]:
    """
    Get a list of all available fields that can be requested from the Cellosaurus API.

Returns
-------
    Dictionary mapping field names to their descriptions
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419071553539", "list_available_fields", arguments)

