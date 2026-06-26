"""
china-luggage-sourcing - OpenClaw skill for China luggage industry intelligence
Provides structured data access to manufacturing clusters, supply chain, and sourcing guidance.
"""

import json
import os
from typing import Dict, List, Optional, Union

# Load data once at module level
_DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")

with open(_DATA_PATH, "r", encoding="utf-8") as f:
    LUGGAGE_DATA = json.load(f)

# --- Helper functions ---
def _get_nested(data: Dict, path: str, default=None):
    """Safely get nested dictionary value using dot notation path."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

# --- Public API functions ---
def get_industry_overview() -> Dict:
    """Return overview of China's luggage industry scale and targets."""
    return LUGGAGE_DATA.get("industry_overview", {})

def get_supply_chain_structure() -> Dict:
    """Return the complete luggage supply chain structure."""
    return LUGGAGE_DATA.get("supply_chain_structure", {})

def get_regional_clusters(region: Optional[str] = None) -> Union[List[Dict], Dict]:
    """
    Return all regional clusters or a specific cluster by name.
    If region is None, returns list of all clusters.
    If region is specified, returns that cluster's details.
    """
    clusters = LUGGAGE_DATA.get("regional_clusters", [])
    
    if region is None:
        return clusters
    
    region_lower = region.lower()
    for cluster in clusters:
        if region_lower in cluster.get("region", "").lower():
            return cluster
    
    return {"error": f"Cluster '{region}' not found. Available regions: {[c['region'] for c in clusters]}"}

def find_clusters_by_specialization(specialization: str) -> List[Dict]:
    """Find clusters that specialize in a given luggage type."""
    spec_lower = specialization.lower()
    clusters = LUGGAGE_DATA.get("regional_clusters", [])
    results = []
    
    for cluster in clusters:
        specializations = cluster.get("specializations", [])
        if any(spec_lower in s.lower() for s in specializations):
            results.append({
                "region": cluster["region"],
                "specializations": cluster["specializations"][:3],
                "key_hubs": cluster.get("key_hubs", []),
                "strengths": cluster.get("strengths", [])
            })
    
    return results

def get_subsector_info(subsector: str) -> Dict:
    """Return detailed information about a specific luggage subsector."""
    subsectors = LUGGAGE_DATA.get("subsector_details", {})
    
    # Try exact match first
    if subsector in subsectors:
        return subsectors[subsector]
    
    # Try case-insensitive partial match on key names
    subsector_lower = subsector.lower()
    for key, value in subsectors.items():
        if subsector_lower in key.lower():
            return value
    
    # Keyword mapping for common terms
    keyword_mapping = {
        "suitcase": "travel_luggage",
        "luggage": "travel_luggage",
        "trolley": "travel_luggage",
        "hard-side": "travel_luggage",
        "handbag": "handbags_fashion_bags",
        "bag": "handbags_fashion_bags",
        "backpack": "backpacks",
        "rucksack": "backpacks",
        "business": "business_bags",
        "briefcase": "business_bags",
        "laptop": "business_bags",
        "camera": "specialty_bags",
        "diaper": "specialty_bags"
    }
    
    if subsector_lower in keyword_mapping:
        mapped_key = keyword_mapping[subsector_lower]
        if mapped_key in subsectors:
            return subsectors[mapped_key]
    
    return {"error": f"Subsector '{subsector}' not found. Available: {list(subsectors.keys())}"}

def get_sourcing_guide() -> Dict:
    """Return supplier evaluation and sourcing best practices."""
    guide = LUGGAGE_DATA.get("sourcing_guide", {})
    # Normalize evaluation_criteria field name
    if "supplier_evaluation_metrics" in guide and "evaluation_criteria" not in guide:
        guide["evaluation_criteria"] = guide["supplier_evaluation_metrics"]
    return guide

def get_faq(question: Optional[str] = None) -> Union[List[Dict], Dict]:
    """Return FAQ list or answer to a specific question."""
    faqs = LUGGAGE_DATA.get("faq", [])
    
    if question is None:
        return faqs
    
    question_lower = question.lower()
    for faq in faqs:
        if question_lower in faq.get("question", "").lower():
            return faq
    
    return {"error": f"No FAQ found matching '{question}'"}

def get_glossary(term: Optional[str] = None) -> Union[Dict, str]:
    """Return glossary of terms or definition of a specific term."""
    glossary = LUGGAGE_DATA.get("glossary", {})
    
    if term is None:
        return glossary
    
    term_lower = term.lower()
    for key, value in glossary.items():
        if term_lower == key.lower() or term_lower in value.lower():
            return {key: value}
    
    return f"Term '{term}' not found in glossary"

def search_data(query: str) -> List[Dict]:
    """
    Simple search across all data for a query string.
    Returns list of matching items with context.
    """
    query_lower = query.lower()
    results = []
    
    # Search in regional clusters
    for cluster in LUGGAGE_DATA.get("regional_clusters", []):
        if any(query_lower in str(v).lower() for v in cluster.values()):
            results.append({
                "type": "regional_cluster",
                "region": cluster.get("region"),
                "match_preview": f"Specializations: {cluster.get('specializations', [])[:2]}"
            })
    
    # Search in subsectors
    for subsector_name, subsector_data in LUGGAGE_DATA.get("subsector_details", {}).items():
        if query_lower in subsector_name.lower() or query_lower in str(subsector_data).lower():
            results.append({
                "type": "subsector",
                "name": subsector_name,
                "match_preview": subsector_data.get("description", "")[:100]
            })
    
    return results

def get_metadata() -> Dict:
    """Return metadata about the data source and last update."""
    return LUGGAGE_DATA.get("metadata", {})

# --- If run directly, provide interactive example ---
if __name__ == "__main__":
    print("🧳 China Luggage Sourcing Skill (CLI Test Mode)")
    print("=" * 60)
    
    print("\n📊 Industry Overview:")
    overview = get_industry_overview()
    print(f"2026 Target: {overview.get('summary', 'N/A')}")
    
    print("\n📍 Regional Clusters:")
    clusters = get_regional_clusters()
    for c in clusters[:3]:
        print(f"• {c.get('region')}: {', '.join(c.get('specializations', [])[:2])}")
    
    print("\n💡 Example usage in OpenClaw:")
    print('  from do import get_regional_clusters, find_clusters_by_specialization, get_subsector_info')
    print('  get_regional_clusters("Pearl River Delta")')
    print('  find_clusters_by_specialization("handbags")')
    print('  get_subsector_info("travel_luggage")')