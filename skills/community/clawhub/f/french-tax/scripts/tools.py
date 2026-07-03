from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_tax_info_from_web(
    tax_topic: str,
    year: Optional[null] = None
) -> Dict[str, Any]:
    """
    Get tax information from official French government websites like impots.gouv.fr, service-public.fr, or legifrance.gouv.fr
    
    Args:
        tax_topic: null
        year: null
    
    Returns:
        null
    """
    arguments = {
        "tax_topic": tax_topic,
        "year": year
    }
    
    return call_api("1777419065008131", "get_tax_info_from_web", arguments)

def get_tax_brackets(
    year: Optional[null] = None
) -> Dict[str, Any]:
    """
    Get income tax brackets (tranches d'imposition) for a specific year
    
    Args:
        year: null
    
    Returns:
        null
    """
    arguments = {
        "year": year
    }
    
    return call_api("1777419065008131", "get_tax_brackets", arguments)

def get_form_details(
    form_number: str,
    year: Optional[null] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific tax form including fields and instructions
    
    Args:
        form_number: null
        year: null
    
    Returns:
        null
    """
    arguments = {
        "form_number": form_number,
        "year": year
    }
    
    return call_api("1777419065008131", "get_form_details", arguments)

def get_cached_tax_info(
    tax_topic: str,
    year: Optional[null] = None
) -> Dict[str, Any]:
    """
    Get cached tax information when web scraping fails
    
    Args:
        tax_topic: null
        year: null
    
    Returns:
        null
    """
    arguments = {
        "tax_topic": tax_topic,
        "year": year
    }
    
    return call_api("1777419065008131", "get_cached_tax_info", arguments)

def calculate_income_tax(
    net_taxable_income: float,
    household_parts: Optional[float] = 1.0,
    year: Optional[null] = None
) -> Dict[str, Any]:
    """
    Calculate French income tax based on net taxable income and household composition
    
    Args:
        net_taxable_income: null
        household_parts: null
        year: null
    
    Returns:
        null
    """
    arguments = {
        "net_taxable_income": net_taxable_income,
        "household_parts": household_parts,
        "year": year
    }
    
    return call_api("1777419065008131", "calculate_income_tax", arguments)

def get_tax_procedure(
    procedure_name: str
) -> Dict[str, Any]:
    """
    Get information about a tax procedure from service-public.fr
    
    Args:
        procedure_name: null
    
    Returns:
        null
    """
    arguments = {
        "procedure_name": procedure_name
    }
    
    return call_api("1777419065008131", "get_tax_procedure", arguments)

def get_tax_deadlines(
    year: Optional[null] = None
) -> Dict[str, Any]:
    """
    Get tax deadlines from service-public.fr
    
    Args:
        year: null
    
    Returns:
        null
    """
    arguments = {
        "year": year
    }
    
    return call_api("1777419065008131", "get_tax_deadlines", arguments)

def health_check(
) -> Dict[str, Any]:
    """
    Simple health check to verify the server is responsive
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419065008131", "health_check", arguments)

def get_tax_article(
    article_id: str
) -> Dict[str, Any]:
    """
    Get information about a tax law article from legifrance.gouv.fr
    
    Args:
        article_id: null
    
    Returns:
        null
    """
    arguments = {
        "article_id": article_id
    }
    
    return call_api("1777419065008131", "get_tax_article", arguments)

def search_tax_law(
    query: str
) -> Dict[str, Any]:
    """
    Search for tax law articles on legifrance.gouv.fr
    
    Args:
        query: null
    
    Returns:
        null
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777419065008131", "search_tax_law", arguments)

def generate_tax_report(
    tax_data: null,
    topic_name: str,
    output_file: Optional[null] = None,
    format: Optional[str] = "markdown"
) -> Dict[str, Any]:
    """
    Generate a detailed report about a specific tax topic
    
    Args:
        tax_data: null
        topic_name: null
        output_file: null
        format: null
    
    Returns:
        null
    """
    arguments = {
        "tax_data": tax_data,
        "topic_name": topic_name,
        "output_file": output_file,
        "format": format
    }
    
    return call_api("1777419065008131", "generate_tax_report", arguments)

