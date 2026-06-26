# -*- coding: utf-8 -*-
"""
Global Cognitive Brain - Multi-layer thinking engine with persistent memory
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
import re

# Import jieba for Chinese segmentation
try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

# Memory paths
MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'brain_memory')
WORKING_FILE = os.path.join(MEMORY_DIR, 'working.json')
EPISODIC_FILE = os.path.join(MEMORY_DIR, 'episodic.json')
SEMANTIC_FILE = os.path.join(MEMORY_DIR, 'semantic.json')
META_FILE = os.path.join(MEMORY_DIR, 'meta.json')

# Initialize memory files
def init_memory():
    """Initialize memory files if they don't exist."""
    os.makedirs(MEMORY_DIR, exist_ok=True)

    for file_path in [WORKING_FILE, EPISODIC_FILE, SEMANTIC_FILE, META_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    # Load existing memory
    global working_memory, episodic_memory, semantic_memory, meta_memory
    working_memory = load_json(WORKING_FILE)
    episodic_memory = load_json(EPISODIC_FILE)
    semantic_memory = load_json(SEMANTIC_FILE)
    meta_memory = load_json(META_FILE)

def load_json(filepath: str) -> Dict:
    """Load JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json(filepath: str, data: Dict):
    """Save JSON file with UTF-8 encoding."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Working Memory
def add_working_memory(message: str, role: str = 'assistant'):
    """Add message to working memory."""
    working_memory.setdefault('recent_dialogues', []).append({
        'timestamp': time.time(),
        'role': role,
        'message': message
    })
    # Keep last 20 messages
    if len(working_memory['recent_dialogues']) > 20:
        working_memory['recent_dialogues'] = working_memory['recent_dialogues'][-20:]
    save_json(WORKING_FILE, working_memory)

# Episodic Memory
def store_event(summary: str, details: Optional[str] = None, importance: int = 1):
    """Store an event in episodic memory."""
    episodic_memory.setdefault('events', []).append({
        'timestamp': time.time(),
        'summary': summary,
        'details': details,
        'importance': importance
    })
    save_json(EPISODIC_FILE, episodic_memory)

def retrieve_events(query: str, limit: int = 5) -> List[Dict]:
    """Retrieve relevant events from episodic memory."""
    if not query:
        return []

    # Simple keyword matching
    query_words = set(query.lower().split())
    relevant_events = []

    for event in episodic_memory.get('events', []):
        event_words = set(event.get('summary', '').lower().split())
        match_count = len(query_words & event_words)

        if match_count > 0:
            relevant_events.append({
                'event': event,
                'match_count': match_count
            })

    # Sort by relevance and limit
    relevant_events.sort(key=lambda x: x['match_count'], reverse=True)
    return [x['event'] for x in relevant_events[:limit]]

# Semantic Memory
def update_fact(key: str, value: str, confidence: float = 1.0):
    """Update or add a fact to semantic memory."""
    semantic_memory.setdefault('facts', {})[key] = {
        'value': value,
        'updated': time.time(),
        'confidence': confidence
    }
    save_json(SEMANTIC_FILE, semantic_memory)

def search_knowledge(query: str, limit: int = 5) -> List[Dict]:
    """Search semantic memory for relevant facts."""
    if not query:
        return []

    query_words = set(query.lower().split())
    relevant_facts = []

    for key, value in semantic_memory.get('facts', {}).items():
        fact_words = set(str(value['value']).lower().split())
        match_count = len(query_words & fact_words)

        if match_count > 0:
            relevant_facts.append({
                'key': key,
                'value': value['value'],
                'updated': value['updated'],
                'confidence': value['confidence'],
                'match_count': match_count
            })

    relevant_facts.sort(key=lambda x: x['match_count'], reverse=True)
    return relevant_facts[:limit]

# Meta Memory
def update_meta(key: str, value: str):
    """Update meta knowledge."""
    meta_memory.setdefault('knowledge', {})[key] = {
        'value': value,
        'updated': time.time()
    }
    save_json(META_FILE, meta_memory)

def retrieve_meta(query: str) -> List[Dict]:
    """Retrieve meta knowledge."""
    if not query:
        return []

    query_words = set(query.lower().split())
    relevant_meta = []

    for key, value in meta_memory.get('knowledge', {}).items():
        meta_words = set(str(value['value']).lower().split())
        match_count = len(query_words & meta_words)

        if match_count > 0:
            relevant_meta.append({
                'key': key,
                'value': value['value'],
                'match_count': match_count
            })

    relevant_meta.sort(key=lambda x: x['match_count'], reverse=True)
    return relevant_meta[:5]

# Knowledge Extraction (back to simple version that works)
def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text using jieba segmentation."""
    if not text:
        return []

    if JIEBA_AVAILABLE:
        words = jieba.lcut(text)
    else:
        words = text.split()

    # Stopwords (simplified)
    stopwords = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'to', 'of', 'in', 'for',
        'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
        'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
        'just', 'also', 'now', 'please', 'thank', 'thanks', 'yes', 'no', 'ok',
        'okay', 'yeah', 'yep', 'ah', 'oh', 'uh', 'um', 'hmm', 'well', 'like',
        'want', 'needs', 'need', 'get', 'got', 'going', 'go', 'did', 'do', 'does',
        'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 'having'
    }

    # Filter words
    keywords = []
    for word in words:
        word_lower = word.lower().strip()
        if len(word_lower) > 1 and word_lower not in stopwords:
            keywords.append(word_lower)

    return keywords

# Five-Layer Thinking
def layer1_immediate(user_input: str) -> Dict:
    """L1: Immediate intent detection."""
    input_lower = user_input.lower()
    keywords = extract_keywords(input_lower)

    # Define intent keywords (with precise, non-overlapping terms where possible)
    intent_keywords = {
        'github': ['github', 'git', 'issue', 'bug', 'report', 'pull request', 'pull', 'request', 'pr', 'commit', 'repo', 'repository', 'fork', 'clone', 'push', 'merge', 'review', 'release', 'branch', 'workflow', 'action', 'ci', 'cd', 'github actions'],
        'sql': ['sql', 'query', 'select', 'insert', 'update', 'delete', 'join', 'duplicate', 'stored procedure', 'trigger', 'index', 'schema', 'mysql', 'postgresql', 'sqlite', 'oracle', 'mssql', 'database', 'report', 'sales', 'inventory', 'transaction', 'stock', 'product', 'customer', 'order'],  # added ERP business terms; avoid UI 'table','column'
        'tavily': ['research', 'best practices', 'examples', 'code example', 'tutorial', 'guide', 'documentation', 'latest', 'trends', 'compare', 'review', 'performance', 'faster', 'optimize', 'improve', 'tuning', 'speed', 'efficiency'],  # AI-optimized search incl. performance tuning
        'search': ['search', 'find', 'google', 'lookup', 'look up', 'what is', 'what are', 'why', 'who', 'when', 'where', 'how to', 'how do', 'information'],  # General search
        'frontend': [
            'vue', 'react', 'frontend', 'css', 'html', 'javascript', 'js', 'component', 'ui', 'ux', 'style', 'dropdown', 'menu', 'bootstrap', 'tailwind', 'responsive', 'layout',
            'form', 'button', 'input', 'field', 'modal', 'dialog', 'popup', 'toast', 'notification', 'tab', 'accordion', 'carousel', 'slider', 'nav', 'navbar', 'sidebar',
            'grid', 'flex', 'spacing', 'padding', 'margin', 'border', 'shadow', 'animation', 'transition', 'transform', 'opacity', 'color', 'font', 'typography',
            'media query', 'mobile', 'desktop', 'tablet', 'breakpoint', 'viewport', 'rem', 'em', 'px', '%', 'vh', 'vw',
            'dom', 'event', 'click', 'hover', 'focus', 'blur', 'submit', 'change', 'keydown', 'keyup',
            'api call', 'fetch', 'axios', 'ajax', 'json', 'rest', 'graphql',
            'angular', 'svelte', 'next', 'nuxt', 'gatsby', 'vite', 'webpack',
            'dark mode', 'light mode', 'theme', 'toggle', 'switch',
            'class', 'id', 'element', 'page', 'website', 'web app', 'pwa',
            'web design', 'app design', 'interface design',
            'data table', 'table', 'column', 'sort', 'filter', 'pagination'  # added table/column for UI data grid
        ],
        'healthcheck': ['health', 'audit', 'vulnerability', 'security', 'scan', 'monitor', 'assess', 'check', 'inspect', 'examine'],
        'coding': [
            'code', 'script', 'program', 'function', 'class', 'method', 'implement', 'develop', 'build', 'write', 'create', 'generate', 'make',
            'python', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'typescript', 'javascript', 'js',
            'fix', 'refactor', 'convert', 'deploy', 'configure', 'debug', 'troubleshoot', 'optimize', 'improve', 'update', 'upgrade', 'patch', 'modify', 'change',
            'pdo', 'odbc', 'jdbc', 'driver', 'dbal',
            'api', 'endpoint', 'restful', 'soap', 'xml', 'json',
            'oop', 'object', 'class', 'inheritance', 'polymorphism',
            'security', 'authentication', 'authorization', 'encryption', 'jwt', 'oauth',
            'performance', 'caching', 'queue', 'async', 'await', 'promise',
            'testing', 'unit test', 'integration test', 'e2e', 'mocking'
        ],
        'summarize': ['summarize', 'summary', 'shorten', 'condense', 'brief', 'summarise', 'overview', 'recap', 'key points', 'takeaway'],
        'weather': ['weather', 'forecast', 'temperature', 'rain', 'snow', 'humidity', 'wind', 'storm', 'cloudy', 'sunny']
    }

    # Calculate match counts for each intent
    intent_scores = {}
    for intent, trigger_words in intent_keywords.items():
        score = 0
        for kw in keywords:
            if kw in trigger_words:
                score += 1
        if score > 0:
            intent_scores[intent] = score

    # Determine intent: highest score wins, ties broken by priority order
    detected_intent = None
    if intent_scores:
        max_score = max(intent_scores.values())
        # Pick first intent in priority order with max_score
        for intent in intent_keywords:
            if intent in intent_scores and intent_scores[intent] == max_score:
                detected_intent = intent
                break

    return {
        'raw_input': user_input,
        'intent_keywords': keywords,
        'input_length': len(user_input),
        'detected_intent': detected_intent,
        'intent_scores': intent_scores  # for debugging
    }

def layer2_working_memory(user_input: str, layer1_result: Dict) -> Dict:
    """L2: Working memory integration."""
    # Add to working memory
    add_working_memory(user_input, 'user')

    # Retrieve related dialogues
    recent_dialogues = working_memory.get('recent_dialogues', [])
    related_dialogues = recent_dialogues[-5:]  # Last 5 messages

    # Count related patterns
    user_keywords = layer1_result['intent_keywords']
    related_count = sum(
        1 for d in recent_dialogues
        if any(word in user_keywords for word in extract_keywords(d.get('message', '')))
    )

    return {
        'recent_dialogues': related_dialogues,
        'related_found': related_count,
        'related_examples': related_dialogues[-3:] if related_count > 0 else []
    }

def layer3_episodic_memory(user_input: str, layer1_result: Dict, layer2_result: Dict) -> Dict:
    """L3: Episodic memory retrieval."""
    # Search for relevant events
    query = user_input[:50]  # Use first 50 chars as query
    related_events = retrieve_events(query)

    return {
        'total_events': len(episodic_memory.get('events', [])),
        'recent_checked': len(related_events),
        'related_events': related_events
    }

def layer4_semantic_memory(user_input: str, layer1_result: Dict, layer2_result: Dict, layer3_result: Dict) -> Dict:
    """L4: Semantic memory retrieval."""
    # Search for relevant facts
    query = user_input[:50]
    related_facts = search_knowledge(query)

    return {
        'total_facts': len(semantic_memory.get('facts', {})),
        'related_facts': related_facts
    }

def layer5_meta_reflection(user_input: str, all_layers: Dict) -> Dict:
    """L5: Meta reflection on the thinking process."""
    # Analyze the input
    intent = all_layers['layer1_immediate']['detected_intent']
    input_length = all_layers['layer1_immediate']['input_length']
    related_facts = all_layers['layer4_semantic_memory']['related_facts']
    related_events = all_layers['layer3_episodic_memory']['related_events']

    # 🚨 OVERRIDE: Direct content-based check (bypass L1 errors)
    user_lower = user_input.lower()
    
    # 1. Force tavily for RESEARCH/LEARNING queries (not practical coding/deployment)
    # Do NOT override if it contains practical coding/database terms
    if any(term in user_lower for term in [
        'research', 'best practices', 'examples', 'code example', 'tutorial', 'guide', 'documentation',
        'latest', 'trends', 'compare', 'review'  # removed 'performance', 'optimize', 'improve', 'faster', 'how to' - these can be practical
    ]):
        meta_question = "This requires AI-optimized search/research - need tavily-search"
        suggestions = [
            "Use tavily-search skill for comprehensive research",
            "Search for authoritative sources and examples",
            "Synthesize findings with AI"
        ]
        return {
            'meta_question': meta_question,
            'suggestions': suggestions,
            'detected_intent': 'tavily',
            'confidence': 0.9
        }
    
    # 2. Force github for GitHub-specific operations (even if L1 missed)
    if any(term in user_lower for term in [
        'pull request', 'pull', 'request', 'create pr', 'open pr', 'new repository', 'init repo', 'git commit', 'git push', 'merge branch', 'fork repo', 'release tag', 'github action', 'workflow'
    ]):
        meta_question = "This involves GitHub repository operations - need github skill"
        suggestions = [
            "Use github skill",
            "Perform repository management",
            "Handle pull requests and issues"
        ]
        return {
            'meta_question': meta_question,
            'suggestions': suggestions,
            'detected_intent': 'github',
            'confidence': 0.9
        }
    
    # 3. Force sql for database schema/table creation (exclude UI 'form fields')
    # Only trigger when clear DB terms: table, index, schema, query, column + creation verbs
    if any(verb in user_lower for verb in ['create table', 'add index', 'create index', 'define schema', 'create database', 'create view', 'create trigger', 'create procedure']):
        meta_question = "This involves database schema creation - need sql-toolkit"
        suggestions = [
            "Use sql-toolkit skill",
            "Create tables and define schema",
            "Consider indexes and constraints"
        ]
        return {
            'meta_question': meta_question,
            'suggestions': suggestions,
            'detected_intent': 'sql',
            'confidence': 0.9
        }
    
    # 4. Force frontend for UI component creation (must have explicit UI element AND form/layout context)
    # Avoid conflict with database 'field' - require UI-specific terms: form, page, component, layout, design
    if any(ui_element in user_lower for ui_element in ['form', 'page', 'component', 'layout', 'design', 'ui', 'ux', 'dropdown', 'modal', 'popup', 'toast', 'tab', 'accordion', 'carousel', 'navbar', 'sidebar']):
        if any(verb in user_lower for verb in ['create', 'build', 'make', 'add', 'new', 'design']):
            meta_question = "This involves UI/UX component creation - need frontend skill"
            suggestions = [
                "Use frontend skill",
                "Create UI components",
                "Implement responsive design"
            ]
            return {
                'meta_question': meta_question,
                'suggestions': suggestions,
                'detected_intent': 'frontend',
                'confidence': 0.8
            }

    # Intent-based meta reflection (primary)
    if intent == 'github':
        meta_question = "This involves GitHub operations - need to use GitHub skills"
        suggestions = [
            "Use GitHub skill",
            "Handle repository management",
            "Manage issues and pull requests"
        ]
    elif intent == 'sql':
        meta_question = "This involves SQL/database operations - need to use sql-toolkit"
        suggestions = [
            "Use sql-toolkit skill",
            "Write efficient SQL queries",
            "Consider database security and performance"
        ]
    elif intent == 'frontend':
        meta_question = "This is a frontend/UI task - need to use frontend or React skills"
        suggestions = [
            "Use frontend or React skill",
            "Create responsive components",
            "Follow best practices for UI/UX"
        ]
    elif intent == 'healthcheck':
        meta_question = "This is a security/health check - need to audit"
        suggestions = [
            "Use healthcheck skill",
            "Check for vulnerabilities",
            "Provide security recommendations"
        ]
    elif intent == 'coding':
        meta_question = "This requires coding - need to generate code"
        suggestions = [
            "Use coding-agent skill",
            "Generate code with proper structure",
            "Include comments and documentation"
        ]
    elif intent == 'tavily':
        # Explicit AI-optimized research request
        meta_question = "This requires AI-optimized research - need tavily-search"
        suggestions = [
            "Use tavily-search skill (AI-optimized for research)",
            "Search for code examples and best practices",
            "Find authoritative documentation"
        ]
        return {
            'meta_question': meta_question,
            'suggestions': suggestions,
            'detected_intent': 'tavily',
            'confidence': 0.9
        }
    elif intent == 'search':
        # General search (non-research)
        meta_question = "This asks for general information - need multi-search-engine"
        suggestions = [
            "Use multi-search-engine skill (privacy-focused)",
            "Search across multiple engines",
            "Aggregate results"
        ]
        return {
            'meta_question': meta_question,
            'suggestions': suggestions,
            'detected_intent': 'search',
            'confidence': 0.8
        }
    elif intent == 'summarize':
        meta_question = "This requires summarization - need to condense"
        suggestions = [
            "Use summarize skill",
            "Extract key points",
            "Maintain original meaning"
        ]
    elif intent == 'weather':
        meta_question = "This asks for weather information"
        suggestions = [
            "Use weather skill",
            "Provide current conditions and forecast"
        ]
    elif related_facts:
        meta_question = "This asks for information - retrieving stored facts"
        suggestions = [
            "Leverage semantic memory facts",
            "Provide factual answer",
            "Cite sources if available"
        ]
    elif related_events:
        meta_question = "This may relate to past events - check episodic memory"
        suggestions = [
            "Review related events",
            "Provide context from past interactions"
        ]
    elif input_length > 100:
        meta_question = "This is a complex request - need structured response"
        suggestions = [
            "Break down into steps",
            "Provide clear structure",
            "Include examples if helpful"
        ]
    else:
        meta_question = "General question - need to provide helpful answer"
        suggestions = [
            "Understand the question fully",
            "Provide clear, concise answer",
            "Ask clarifying questions if needed"
        ]

    return {
        'meta_question': meta_question,
        'assumptions': [],
        'risks': [],
        'suggestions': suggestions
    }

def five_layer_thinking(user_input: str) -> Dict:
    """Execute the five-layer thinking process."""
    start_time = time.time()

    # L1
    layer1 = layer1_immediate(user_input)

    # L2
    layer2 = layer2_working_memory(user_input, layer1)

    # L3
    layer3 = layer3_episodic_memory(user_input, layer1, layer2)

    # L4
    layer4 = layer4_semantic_memory(user_input, layer1, layer2, layer3)

    # L5
    layer5 = layer5_meta_reflection(user_input, {
        'layer1_immediate': layer1,
        'layer2_working_memory': layer2,
        'layer3_episodic_memory': layer3,
        'layer4_semantic_memory': layer4
    })

    return {
        'input': user_input,
        'layer1_immediate': layer1,
        'layer2_working_memory': layer2,
        'layer3_episodic_memory': layer3,
        'layer4_semantic_memory': layer4,
        'layer5_meta_reflection': layer5,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')
    }

# Skill Selection - Model-First Approach
def select_skill(user_input: str) -> str:
    """Select the most appropriate skill based on model reflection (L5)."""
    # Execute all layers to get meta reflection
    layer1 = layer1_immediate(user_input)
    layer2 = layer2_working_memory(user_input, layer1)
    layer3 = layer3_episodic_memory(user_input, layer1, layer2)
    layer4 = layer4_semantic_memory(user_input, layer1, layer2, layer3)
    layer5 = layer5_meta_reflection(user_input, {
        'layer1_immediate': layer1,
        'layer2_working_memory': layer2,
        'layer3_episodic_memory': layer3,
        'layer4_semantic_memory': layer4
    })

    meta_question = layer5['meta_question'].lower()

    # Priority 1: Meta question-based (model's primary decision)
    # These patterns come from model's reflection, not keyword matching
    if 'health' in meta_question or 'security' in meta_question or 'vulnerability' in meta_question:
        return 'healthcheck'
    elif 'coding' in meta_question or 'generate code' in meta_question or 'write code' in meta_question:
        return 'coding-agent'
    elif 'summarize' in meta_question or 'condense' in meta_question or 'summarise' in meta_question:
        return 'summarize'
    elif 'weather' in meta_question:
        return 'weather'
    elif 'tavily' in meta_question or 'research' in meta_question or 'best practices' in meta_question or 'code example' in meta_question or 'tutorial' in meta_question or 'documentation' in meta_question:
        return 'tavily-search'
    elif 'search' in meta_question or 'information' in meta_question or 'retrieve' in meta_question:
        return 'multi-search-engine'
    elif 'github' in meta_question or 'github operations' in meta_question:
        return 'github'
    elif 'sql' in meta_question or 'database' in meta_question or 'sql query' in meta_question:
        return 'sql-toolkit'
    elif 'frontend' in meta_question or 'ui' in meta_question or 'css' in meta_question:
        return 'frontend'

    # Priority 2: Keyword-based fallback (only if meta question doesn't specify)
    # Use this as backup when model's reflection is ambiguous
    input_lower = user_input.lower()
    keywords = layer1['intent_keywords']

    # Check for high-priority keywords (these are more reliable)
    high_priority_keywords = {
        'github': ['github', 'git', 'issue', 'bug', 'report', 'pull request', 'pr', 'commit', 'repo', 'repository', 'fork', 'clone', 'push', 'merge', 'review', 'release', 'branch', 'workflow', 'action', 'ci', 'cd'],
        'sql': ['sql', 'query', 'select', 'insert', 'update', 'delete', 'join', 'duplicate', 'stored procedure', 'trigger', 'index', 'schema', 'mysql', 'postgresql', 'sqlite', 'oracle', 'mssql', 'database'],
        'tavily': ['research', 'best practices', 'examples', 'code example', 'tutorial', 'guide', 'documentation', 'latest', 'trends', 'compare', 'review'],
        'search': ['search', 'find', 'google', 'lookup', 'what is', 'what are', 'latest version', 'how to', 'how do', 'why', 'who', 'when', 'where', 'information'],
        'frontend': [
            'vue', 'react', 'frontend', 'css', 'html', 'javascript', 'js', 'component', 'ui', 'ux', 'style', 'dropdown', 'menu', 'bootstrap', 'tailwind', 'responsive', 'layout',
            'form', 'button', 'input', 'field', 'modal', 'dialog', 'popup', 'toast', 'notification', 'tab', 'accordion', 'carousel', 'slider', 'nav', 'navbar', 'sidebar',
            'grid', 'flex', 'spacing', 'padding', 'margin', 'border', 'shadow', 'animation', 'transition', 'transform', 'opacity', 'color', 'font', 'typography',
            'media query', 'mobile', 'desktop', 'tablet', 'breakpoint', 'viewport', 'rem', 'em', 'px', '%', 'vh', 'vw',
            'dom', 'event', 'click', 'hover', 'focus', 'blur', 'submit', 'change', 'keydown', 'keyup',
            'angular', 'svelte', 'next', 'nuxt', 'gatsby', 'vite', 'webpack',
            'dark mode', 'light mode', 'theme', 'toggle', 'switch',
            'page', 'website', 'web app', 'pwa',
            'table', 'column', 'sort', 'filter', 'pagination'
        ],
        'healthcheck': ['health', 'audit', 'vulnerability', 'security', 'scan', 'monitor', 'assess', 'check'],
        'coding': [
            'code', 'script', 'program', 'function', 'class', 'method', 'implement', 'develop', 'build', 'write', 'create', 'generate', 'make',
            'python', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'typescript', 'javascript',
            'fix', 'refactor', 'convert', 'deploy', 'configure', 'debug', 'troubleshoot', 'optimize', 'improve', 'update', 'upgrade', 'patch', 'modify', 'change',
            'pdo', 'odbc', 'jdbc', 'driver', 'dbal', 'api', 'endpoint', 'restful', 'soap', 'xml', 'json',
            'oop', 'object', 'inheritance', 'polymorphism',
            'security', 'authentication', 'authorization', 'encryption', 'jwt', 'oauth',
            'performance', 'caching', 'queue', 'async', 'await', 'promise',
            'testing', 'unit test', 'integration test', 'e2e', 'mocking'
        ],
        'summarize': ['summarize', 'summary', 'shorten', 'condense', 'brief', 'summarise', 'overview', 'recap', 'key points', 'takeaway'],
        'weather': ['weather', 'forecast', 'temperature', 'rain', 'snow', 'humidity', 'wind', 'storm', 'cloudy', 'sunny']
    }

    for intent, trigger_words in high_priority_keywords.items():
        for keyword in keywords:
            if keyword in trigger_words:
                return intent_skills.get(intent, 'coding-agent')

    # Priority 3: Semantic memory facts
    related_facts = layer4['related_facts']
    if related_facts:
        if len(related_facts) > 3:
            return 'summarize'
        else:
            return 'multi-search-engine'

    # Priority 4: Episodic memory events
    related_events = layer3['related_events']
    if related_events:
        return 'summarize'

    # Priority 5: Input length-based
    input_length = layer1['input_length']
    if input_length > 200:
        return 'summarize'

    # Priority 6: Default - coding-agent
    return 'coding-agent'

# Intent skills mapping (for keyword-based fallback)
intent_skills = {
    'github': 'github',
    'sql': 'sql-toolkit',
    'tavily': 'tavily-search',
    'search': 'multi-search-engine',
    'frontend': 'frontend',
    'healthcheck': 'healthcheck',
    'coding': 'coding-agent',
    'summarize': 'summarize',
    'weather': 'weather'
}

def run(user_input: str) -> Dict:
    """Main entry point - execute five-layer thinking and return result."""
    # Execute thinking
    thought_trace = five_layer_thinking(user_input)

    # Select skill
    selected_skill = select_skill(user_input)

    # Build response
    final_response = build_response(user_input, thought_trace, selected_skill)

    # Auto-save all memory after each run
    save_json(WORKING_FILE, working_memory)
    save_json(EPISODIC_FILE, episodic_memory)
    save_json(SEMANTIC_FILE, semantic_memory)
    save_json(META_FILE, meta_memory)

    return {
        'status': 'success',
        'thought_trace': thought_trace,
        'selected_skill': selected_skill,
        'response_suggestion': final_response
    }

def build_response(user_input: str, thought_trace: Dict, selected_skill: str) -> str:
    """Build a suggested response based on the thinking trace."""
    layers = thought_trace

    # Start with meta reflection
    response = f"**Thinking Process:**\n"
    response += f"- Intent detected: {layers['layer1_immediate']['detected_intent'] or 'None'}\n"
    response += f"- Meta reflection: {layers['layer5_meta_reflection']['meta_question']}\n\n"

    # Add semantic facts if available
    if layers['layer4_semantic_memory']['related_facts']:
        response += "**Related Knowledge:**\n"
        for fact in layers['layer4_semantic_memory']['related_facts'][:3]:
            response += f"- {fact['key']}: {fact['value']}\n"
        response += "\n"

    # Add suggestions
    response += "**Suggestions:**\n"
    for suggestion in layers['layer5_meta_reflection']['suggestions']:
        response += f"- {suggestion}\n"

    return response

# Initialize memory on import
init_memory()

__all__ = [
    'init_memory',
    'add_working_memory',
    'store_event',
    'update_fact',
    'search_knowledge',
    'extract_keywords',
    'five_layer_thinking',
    'select_skill',
    'run'
]
