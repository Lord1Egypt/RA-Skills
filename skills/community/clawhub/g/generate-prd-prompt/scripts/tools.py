from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def generate_prd_prompt(
    technology_stack: null,
    analysis_focus: Optional[null] = None,
    project_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate an assembled Product Requirements Document prompt with specified technology stacks and analysis focus areas
    
    Args:
        technology_stack: Technology stacks to include in prompt assembly
        analysis_focus: Analysis focus areas for the PRD
        project_context: Optional project context or background information
    
    Returns:
        
    """
    arguments = {
        "technology_stack": technology_stack,
        "analysis_focus": analysis_focus,
        "project_context": project_context
    }
    
    return call_api("1777316659532803", "generate_prd_prompt", arguments)

def generate_codebase_analysis_prompt(
    technology_stack: null,
    analysis_focus: null
) -> Dict[str, Any]:
    """
    Generate an assembled codebase analysis prompt with specified technology stacks and analysis focus areas
    
    Args:
        technology_stack: Technology stacks to analyze
        analysis_focus: Areas to focus analysis on
    
    Returns:
        
    """
    arguments = {
        "technology_stack": technology_stack,
        "analysis_focus": analysis_focus
    }
    
    return call_api("1777316659532803", "generate_codebase_analysis_prompt", arguments)

def generate_bug_analysis_prompt(
    technology_stack: null,
    severity: str,
    bug_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate an assembled bug analysis prompt with specified technology stacks and severity level
    
    Args:
        technology_stack: Technology stacks involved in the bug
        severity: Bug severity level
        bug_context: Optional bug description or context
    
    Returns:
        
    """
    arguments = {
        "technology_stack": technology_stack,
        "severity": severity,
        "bug_context": bug_context
    }
    
    return call_api("1777316659532803", "generate_bug_analysis_prompt", arguments)

def get_prd_template(
) -> Dict[str, Any]:
    """
    Fetch a comprehensive Product Requirements Document markdown template with all standard sections (14 sections total)
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659532803", "get_prd_template", arguments)

def get_codebase_analysis_template(
) -> Dict[str, Any]:
    """
    Fetch a comprehensive codebase analysis markdown template with all standard sections (12 sections total)
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659532803", "get_codebase_analysis_template", arguments)

def get_bug_analysis_template(
) -> Dict[str, Any]:
    """
    Fetch a comprehensive bug analysis markdown template with all standard sections (8 sections total)
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659532803", "get_bug_analysis_template", arguments)

