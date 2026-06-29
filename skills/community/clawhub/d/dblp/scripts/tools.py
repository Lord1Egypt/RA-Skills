from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_instructions(
) -> Dict[str, Any]:
    """
    Get detailed DBLP usage instructions. Key points:
- Batch searches in parallel (5-10 at a time) for efficiency
- Add entries immediately after each search result (don't batch add_bibtex_entry calls)
- Use author+year for best results: search('Vaswani 2017') not just title
- Copy dblp_key EXACTLY from search results to add_bibtex_entry
- Export once at the end with export_bibtex
Call this tool for complete workflow details, search strategies, and examples.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419064649731", "get_instructions", arguments)

def search(
    query: str,
    max_results: Optional[float] = None,
    year_from: Optional[float] = None,
    year_to: Optional[float] = None,
    venue_filter: Optional[str] = None,
    include_bibtex: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Search DBLP for publications using a boolean query string.
Arguments:
  - query (string, required): A query string that may include boolean operators 'and' and 'or' (case-insensitive).
    For example, 'Swin and Transformer'. Parentheses are not supported.
  - max_results (number, optional): Maximum number of publications to return. Default is 10.
  - year_from (number, optional): Lower bound for publication year.
  - year_to (number, optional): Upper bound for publication year.
  - venue_filter (string, optional): Case-insensitive substring filter for publication venues (e.g., 'iclr').
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a list of publication objects including title, authors, venue, year, type, doi, ee, and url.
    
    Args:
        query: null
        max_results: null
        year_from: null
        year_to: null
        venue_filter: null
        include_bibtex: null
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "max_results": max_results,
        "year_from": year_from,
        "year_to": year_to,
        "venue_filter": venue_filter,
        "include_bibtex": include_bibtex
    }
    
    return call_api("1777419064649731", "search", arguments)

def fuzzy_title_search(
    title: str,
    similarity_threshold: float,
    max_results: Optional[float] = None,
    year_from: Optional[float] = None,
    year_to: Optional[float] = None,
    venue_filter: Optional[str] = None,
    include_bibtex: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Search DBLP for publications with fuzzy title matching.
Arguments:
  - title (string, required): Full or partial title of the publication (case-insensitive).
  - similarity_threshold (number, required): A float between 0 and 1 where 1.0 means an exact match.
  - max_results (number, optional): Maximum number of publications to return. Default is 10.
  - year_from (number, optional): Lower bound for publication year.
  - year_to (number, optional): Upper bound for publication year.
  - venue_filter (string, optional): Case-insensitive substring filter for publication venues.
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a list of publication objects sorted by title similarity score.
    
    Args:
        title: null
        similarity_threshold: null
        max_results: null
        year_from: null
        year_to: null
        venue_filter: null
        include_bibtex: null
    
    Returns:
        
    """
    arguments = {
        "title": title,
        "similarity_threshold": similarity_threshold,
        "max_results": max_results,
        "year_from": year_from,
        "year_to": year_to,
        "venue_filter": venue_filter,
        "include_bibtex": include_bibtex
    }
    
    return call_api("1777419064649731", "fuzzy_title_search", arguments)

def get_author_publications(
    author_name: str,
    similarity_threshold: float,
    max_results: Optional[float] = None,
    include_bibtex: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Retrieve publication details for a specific author with fuzzy matching.
Arguments:
  - author_name (string, required): Full or partial author name (case-insensitive).
  - similarity_threshold (number, required): A float between 0 and 1 where 1.0 means an exact match.
  - max_results (number, optional): Maximum number of publications to return. Default is 20.
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a dictionary with keys: name, publication_count, publications, and stats (which includes top venues, years, and types).
    
    Args:
        author_name: null
        similarity_threshold: null
        max_results: null
        include_bibtex: null
    
    Returns:
        
    """
    arguments = {
        "author_name": author_name,
        "similarity_threshold": similarity_threshold,
        "max_results": max_results,
        "include_bibtex": include_bibtex
    }
    
    return call_api("1777419064649731", "get_author_publications", arguments)

def get_venue_info(
    venue_name: str
) -> Dict[str, Any]:
    """
    Retrieve information about a publication venue from DBLP.
Arguments:
  - venue_name (string, required): Venue name or abbreviation (e.g., 'ICLR', 'NeurIPS', or full name).
Returns a dictionary with fields:
  - venue: Full venue title
  - acronym: Venue acronym/abbreviation (if available)
  - type: Venue type (e.g., 'Conference or Workshop', 'Journal', 'Repository')
  - url: Canonical DBLP URL for the venue
Note: Publisher, ISSN, and other metadata are not available through this endpoint.
    
    Args:
        venue_name: null
    
    Returns:
        
    """
    arguments = {
        "venue_name": venue_name
    }
    
    return call_api("1777419064649731", "get_venue_info", arguments)

def calculate_statistics(
    results: null
) -> Dict[str, Any]:
    """
    Calculate statistics from a list of publication results.
Arguments:
  - results (array, required): An array of publication objects, each with at least 'title', 'authors', 'venue', and 'year'.
Returns a dictionary with:
  - total_publications: Total count.
  - time_range: Dictionary with 'min' and 'max' publication years.
  - top_authors: List of tuples (author, count) sorted by count.
  - top_venues: List of tuples (venue, count) sorted by count (empty venue is treated as '(empty)').
    
    Args:
        results: null
    
    Returns:
        
    """
    arguments = {
        "results": results
    }
    
    return call_api("1777419064649731", "calculate_statistics", arguments)

def add_bibtex_entry(
    dblp_key: str,
    citation_key: str
) -> Dict[str, Any]:
    """
    Add a BibTeX entry to the collection for later export. Call this once for each paper you want to export.
Arguments:
  - dblp_key (string, required): The DBLP key from search results (e.g., 'conf/nips/VaswaniSPUJGKP17').
  - citation_key (string, required): The citation key to use in the .bib file (e.g., 'Vaswani2017').
Workflow:
  1. Fetches BibTeX directly from DBLP using the provided key
  2. Replaces the citation key with your custom key
  3. Adds to collection (duplicate citation_key will be overwritten)
  4. Returns count of entries currently in collection
After adding all entries, call export_bibtex to save them to a .bib file.
    
    Args:
        dblp_key: null
        citation_key: null
    
    Returns:
        
    """
    arguments = {
        "dblp_key": dblp_key,
        "citation_key": citation_key
    }
    
    return call_api("1777419064649731", "add_bibtex_entry", arguments)

def export_bibtex(
    path: str
) -> Dict[str, Any]:
    """
    Export all collected BibTeX entries to a .bib file. Call this after adding all entries with add_bibtex_entry.
Workflow:
  1. Saves all collected entries to a .bib file at the specified path
  2. Clears the collection for next export
  3. Returns the full path to the exported file
Returns error if no entries have been added yet.
    
    Args:
        path: Absolute path for the .bib file (e.g., '/path/to/refs.bib'). The .bib extension is added automatically if missing. Parent directories are created if needed.
    
    Returns:
        
    """
    arguments = {
        "path": path
    }
    
    return call_api("1777419064649731", "export_bibtex", arguments)

