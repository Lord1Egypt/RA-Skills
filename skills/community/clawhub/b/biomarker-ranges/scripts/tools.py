from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def calculate_phenoage(
    biomarkers: null
) -> Dict[str, Any]:
    """
    Calculate biological age using the Morgan Levine PhenoAge clock based on blood biomarkers
    
    Args:
        biomarkers: Blood biomarker values for PhenoAge calculation
    
    Returns:
        
    """
    arguments = {
        "biomarkers": biomarkers
    }
    
    return call_api("1777316659748867", "calculate_phenoage", arguments)

def get_biomarker_ranges(
) -> Dict[str, Any]:
    """
    Get reference ranges and optimal values for PhenoAge biomarkers
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659748867", "get_biomarker_ranges", arguments)

