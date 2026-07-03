from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def extract_antv_topic(
    query: str,
    library: Optional[str] = None,
    maxTopics: Optional[int] = 5.0
) -> Dict[str, Any]:
    """
    AntV Intelligent Assistant Preprocessing Tool - Specifically designed to handle any user queries related to AntV visualization libraries.
  This tool is the first step in processing AntV technology stack issues, responsible for intelligently identifying, parsing, and structuring user visualization requirements.

**MANDATORY: Must be called for ANY new AntV-related queries, including simple questions. Always precedes query_antv_document tool.**

When to use this tool:
- **AntV-related queries**: Questions about g2/g6/l7/x6/f2/s2/g/ava/adc libraries.
- **Visualization tasks**: Creating charts, graphs, maps, or other visualizations.
- **Problem solving**: Debugging errors, performance issues, or compatibility problems.
- **Learning & implementation**: Understanding concepts or requesting code examples.

Key features:
- **Smart Library Detection**: Scans installed AntV libraries and recommends the best fit based on query and project dependencies.
- **Topic & Intent Extraction**: Intelligently extracts technical topics and determines user intent (implement/solve).
- **Task Complexity Handling**: Detects complex tasks and decomposes them into manageable subtasks.
- **Seamless Integration**: Prepares structured data for the query_antv_document tool to provide precise solutions.
    
    Args:
        query: User specific question or requirement description
        library: AntV library name (optional) - If not specified, tool will automatically detect project dependencies and intelligently recommend
        maxTopics: Maximum number of extracted topic keywords, default 5, can be increased appropriately for complex tasks
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "library": library,
        "maxTopics": maxTopics
    }
    
    return call_api("1777316659406851", "extract_antv_topic", arguments)

def query_antv_document(
    library: str,
    query: str,
    topic: str,
    intent: str,
    tokens: Optional[int] = 5000.0,
    subTasks: Optional[null] = None
) -> Dict[str, Any]:
    """
    AntV Context Retrieval Assistant - Fetches relevant documentation, code examples, and best practices from official AntV resources. Supports g2, g6, l7, x6, f2, s2, g, ava, adc libraries, and handles subtasks iterative queries.

**MANDATORY: Must be called for ANY AntV-related query (g2, g6, l7, x6, f2, s2, g, ava, adc), regardless of task complexity. No exceptions for simple tasks.**

When to use this tool:
- **Implementation & Optimization**: To implement new features, modify styles, refactor code, or optimize performance in AntV solutions.
- **Debugging & Problem Solving**: For troubleshooting errors, unexpected behaviors, or technical challenges in AntV projects.
- **Learning & Best Practices**: To explore official documentation, code examples, design patterns, or advanced features.
- **Complex Task Handling**: For multi-step tasks requiring subtask decomposition (e.g., "Build a dashboard with interactive charts").
- **Simple modifications**: Even basic changes like "Change the chart's color" or "Update legend position" in AntV context.
    
    Args:
        library: Specified AntV library type, intelligently identified based on user query
        query: User specific question or requirement description
        topic: Technical topic keywords (comma-separated). Provided by `extract_antv_topic` or directly extracted from simple questions.
        intent: Extracted user intent, provided by extract_antv_topic tool or directly extracted from simple questions.
        tokens: tokens for returned content
        subTasks: Decomposed subtask list for complex tasks, supports batch processing
    
    Returns:
        
    """
    arguments = {
        "library": library,
        "query": query,
        "topic": topic,
        "intent": intent,
        "tokens": tokens,
        "subTasks": subTasks
    }
    
    return call_api("1777316659406851", "query_antv_document", arguments)

