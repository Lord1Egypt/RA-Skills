#!/usr/bin/env python3
"""
Hippocampus V2 - Brain-Inspired Memory System
==============================================
Merged version: Chronicle + Monograph with rich metadata
- Dual storage: SQLite index + Markdown files
- Keyword extraction + association generation
- File organization + analysis
- User-configurable via USER_CONFIG.md

Uses built-in sqlite3 - no external dependencies.
"""

import os
import re
import json
import yaml
import time
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import Counter

# ============================================================================
# Configuration - Read from USER_CONFIG.md
# ============================================================================

SKILL_DIR = Path(__file__).parent.parent
USER_CONFIG_FILE = SKILL_DIR / "USER_CONFIG.md"
CONFIG_CACHE_FILE = SKILL_DIR / "config.json"

# Default configuration (fallback)
DEFAULT_VALUES = {
    "ROUND_THRESHOLD": 25,
    "TIME_HOURS": 6,
    "TOKEN_THRESHOLD": 10000,
    "BASE_PATH": "./assets/hippocampus",
    "CHRONICLE_DIR": "chronicle",
    "MONOGRAPH_DIR": "monograph",
    "INDEX_DIR": "index",
    "WORKFLOW_DIR": "workflows",
    "FILE_ORG_ENABLED": True,
    "FILE_ORG_AUTO_MOVE": False,
    "FILE_SCAN_PATHS": ["./workspace"],
    "FILE_EXCLUDE_PATHS": [".openclaw", "node_modules", ".git"],
    "KEYWORD_COUNT": 20,
    "ASSOCIATION_DEPTH": 3,
    "AUTO_SAVE": True,
    "MICRO_MACRO_ENABLED": True,
    "PROACTIVE_TRIGGERS_ENABLED": True,
    "PROACTIVE_KEYWORDS": {},  # dict: keyword_lower -> monograph_topic
    "READINGBETWEENTHELINES_ENABLED": True,
    "INSTANT_TRIGGERS": "error->error-patterns,database->database-architecture,api->api-design,deploy->deployment-checklist,test->test-strategy",
    "THRESHOLD_TRIGGERS": "project->5,api->4,config->4,feature->4,data->3",
    "HEARTBEAT_INTERVAL": 1,
    "SLIDING_WINDOW": 10,
    "TRIGGER_COOLDOWN": 5,
}

def parse_bool(value: str) -> bool:
    """Parse boolean from string"""
    return value.strip().lower() in ['true', 'yes', '1', 'on']

def parse_list(value: str) -> List[str]:
    """Parse list from comma-separated string"""
    return [item.strip() for item in value.split(',') if item.strip()]

def load_user_config() -> Dict:
    """Load configuration from USER_CONFIG.md"""
    config = DEFAULT_VALUES.copy()
    
    if not USER_CONFIG_FILE.exists():
        # Generate default USER_CONFIG.md
        save_user_config(config)
        return config
    
    # Parse USER_CONFIG.md
    with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if key in config:
                # Type inference
                if key in ['ROUND_THRESHOLD', 'TIME_HOURS', 'TOKEN_THRESHOLD',
                           'KEYWORD_COUNT', 'ASSOCIATION_DEPTH']:
                    config[key] = int(value)
                elif key in ['FILE_ORG_ENABLED', 'FILE_ORG_AUTO_MOVE', 'AUTO_SAVE',
                              'MICRO_MACRO_ENABLED', 'PROACTIVE_TRIGGERS_ENABLED']:
                    config[key] = parse_bool(value)
                elif key in ['FILE_SCAN_PATHS', 'FILE_EXCLUDE_PATHS']:
                    config[key] = parse_list(value)
                elif key in ['INSTANT_TRIGGERS', 'THRESHOLD_TRIGGERS']:
                    # Store as string; parsed at runtime by check functions
                    config[key] = value.strip()
                elif key in ['HEARTBEAT_INTERVAL', 'SLIDING_WINDOW', 'TRIGGER_COOLDOWN']:
                    config[key] = int(value)
                elif key == 'PROACTIVE_KEYWORDS':
                    # Parse KEYWORD->TOPIC,KEYWORD->TOPIC format
                    triggers = {}
                    for pair in parse_list(value):
                        if '->' in pair:
                            kw, topic = pair.split('->', 1)
                            if kw.strip() and topic.strip():
                                triggers[kw.strip().lower()] = topic.strip()
                    config[key] = triggers
                elif key == 'READINGBETWEENTHELINES_ENABLED':
                    config[key] = parse_bool(value)
                else:
                    config[key] = value
    
    return config

def save_user_config(config: Dict):
    """Save USER_CONFIG.md from dict"""
    lines = [
        "# User Configuration for Hippocampus",
        "#",
        "# IMPORTANT: Edit this file to customize your memory behavior",
        "# After editing, the skill will automatically reload these values",
        "# Format: KEY = VALUE (one per line, no quotes needed)",
        "",
        "# ============================================",
        "# Trigger Settings",
        "# ============================================",
        "",
        f"ROUND_THRESHOLD = {config.get('ROUND_THRESHOLD', 25)}",
        f"TIME_HOURS = {config.get('TIME_HOURS', 6)}",
        f"TOKEN_THRESHOLD = {config.get('TOKEN_THRESHOLD', 10000)}",
        "",
        "# ============================================",
        "# Storage Settings",
        "# ============================================",
        "",
        f"BASE_PATH = {config.get('BASE_PATH', './assets/hippocampus')}",
        f"CHRONICLE_DIR = {config.get('CHRONICLE_DIR', 'chronicle')}",
        f"MONOGRAPH_DIR = {config.get('MONOGRAPH_DIR', 'monograph')}",
        f"INDEX_DIR = {config.get('INDEX_DIR', 'index')}",
        "",
        "# ============================================",
        "# File Organization",
        "# ============================================",
        "",
        f"FILE_ORG_ENABLED = {str(config.get('FILE_ORG_ENABLED', True)).lower()}",
        f"FILE_ORG_AUTO_MOVE = {str(config.get('FILE_ORG_AUTO_MOVE', False)).lower()}",
        f"FILE_SCAN_PATHS = {','.join(config.get('FILE_SCAN_PATHS', ['./workspace']))}",
        f"FILE_EXCLUDE_PATHS = {','.join(config.get('FILE_EXCLUDE_PATHS', ['.openclaw', 'node_modules', '.git']))}",
        "",
        "# ============================================",
        "# Keyword & Association",
        "# ============================================",
        "",
        f"KEYWORD_COUNT = {config.get('KEYWORD_COUNT', 20)}",
        f"ASSOCIATION_DEPTH = {config.get('ASSOCIATION_DEPTH', 3)}",
        "",
        "# ============================================",
        "# Auto-Save",
        "# ============================================",
        "",
        f"AUTO_SAVE = {str(config.get('AUTO_SAVE', True)).lower()}",
    ]
    
    USER_CONFIG_FILE.write_text('\n'.join(lines), encoding='utf-8')

# Lazy load config
_config_cache = None

def get_config() -> Dict:
    """Get current configuration (cached)"""
    global _config_cache
    if _config_cache is None:
        _config_cache = load_user_config()
    return _config_cache

def reload_config():
    """Force reload configuration"""
    global _config_cache
    _config_cache = load_user_config()
    return _config_cache

# ============================================================================
# Path Management
# ============================================================================

def get_base_path() -> Path:
    """Get base storage path"""
    config = get_config()
    base = config.get("BASE_PATH", "./assets/hippocampus")
    if not base.startswith('/'):
        base = SKILL_DIR / base
    return Path(base)

def get_chronicle_path() -> Path:
    """Get chronicle directory"""
    config = get_config()
    name = config.get("CHRONICLE_DIR", "chronicle")
    return get_base_path() / name

def get_monograph_path() -> Path:
    """Get monograph directory"""
    config = get_config()
    name = config.get("MONOGRAPH_DIR", "monograph")
    return get_base_path() / name

def get_index_path() -> Path:
    """Get index directory"""
    config = get_config()
    name = config.get("INDEX_DIR", "index")
    return get_base_path() / name

def get_workflow_path() -> Path:
    """Get workflows directory"""
    config = get_config()
    name = config.get("WORKFLOW_DIR", "workflows")
    return get_base_path() / name

# ============================================================================
# 察言观色 — ReadingBetweenTheLines
# ============================================================================

# Stop words: excluded from all token counting
STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her',
    'its', 'our', 'their', 'what', 'which', 'who', 'whom', 'and', 'or', 'but',
    'not', 'no', 'so', 'if', 'then', 'else', 'when', 'where', 'how', 'why',
    'all', 'any', 'some', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'also',
    'now', 'here', 'there', 'then', 'about', 'after', 'before', 'above',
    'below', 'between', 'into', 'through', 'during', 'under', 'again', 'further',
    'once', 'am', 'being', 'being', 'since', 'until', 'while', 'because',
    'although', 'though', 'however', 'therefore', 'thus', 'hence', 'otherwise',
    'anyway', 'besides', 'instead', 'rather', 'yet', 'still', 'already',
    'even', 'ever', 'never', 'always', 'often', 'sometimes', 'usually',
    'maybe', 'perhaps', 'probably', 'certainly', 'definitely', 'maybe',
}


def _reading_state_path() -> Path:
    """Path to the persistent state file for 察言观色"""
    return get_base_path() / "readingbetweenthelines_state.json"


def _load_reading_state() -> Dict:
    """Load persistent word-count and cooldown state"""
    fpath = _reading_state_path()
    if fpath.exists():
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"word_counts": {}, "cooldowns": {}, "last_messages": []}


def _save_reading_state(state: Dict):
    """Persist state to disk"""
    fpath = _reading_state_path()
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False)


def tokenize_and_count(messages: List[str]) -> Dict[str, int]:
    """
    Tokenize messages, remove stop words, return word frequency dict.
    """
    counter: Dict[str, int] = {}
    for msg in messages:
        words = re.findall(r'\b\w+\b', str(msg).lower())
        for w in words:
            if w not in STOP_WORDS and len(w) > 2:
                counter[w] = counter.get(w, 0) + 1
    return counter


def check_instant_triggers(word_counts: Dict[str, int], config: Dict) -> List[str]:
    """
    Return list of monograph topics to load for any instant-trigger keywords.
    Instant triggers fire immediately on first occurrence.
    """
    instant_raw = config.get('INSTANT_TRIGGERS', {})
    if isinstance(instant_raw, str):
        # Parse "word->topic,word->topic" format
        parsed = {}
        for pair in instant_raw.split(','):
            if '->' in pair:
                kw, topic = pair.split('->', 1)
                parsed[kw.strip().lower()] = topic.strip()
        instant_raw = parsed
    triggered = []
    for word in word_counts:
        if word in instant_raw:
            triggered.append(instant_raw[word])
    return triggered


def check_threshold_triggers(word_counts: Dict[str, int], config: Dict) -> List[str]:
    """
    Return list of monograph topics to load for words meeting threshold.
    Threshold triggers fire only after N occurrences within the sliding window.
    """
    thresholds_raw = config.get('THRESHOLD_TRIGGERS', {})
    if isinstance(thresholds_raw, str):
        # Parse "word->count,word->count" format
        parsed = {}
        for pair in thresholds_raw.split(','):
            if '->' in pair:
                kw, count = pair.split('->', 1)
                try:
                    parsed[kw.strip().lower()] = int(count.strip())
                except ValueError:
                    pass
        thresholds_raw = parsed
    triggered = []
    for word, threshold in thresholds_raw.items():
        if word_counts.get(word, 0) >= threshold:
            triggered.append(word)  # topic key == word for threshold triggers
    return triggered


def readingbetweenthelines(messages: List[str], sliding_window: int = 10) -> str:
    """
    Main entry point for 察言观色.
    Analyzes recent messages, checks triggers, returns triggered memories.

    Args:
        messages: List of recent user message strings
        sliding_window: Minutes of history to analyze (for context, not applied here)

    Returns:
        Triggered memory content, or empty string if nothing triggered.
    """
    config = get_config()
    if not config.get('READINGBETWEENTHELINES_ENABLED', True):
        return ""

    word_counts = tokenize_and_count(messages)
    instant_topics = check_instant_triggers(word_counts, config)
    threshold_topics = check_threshold_triggers(word_counts, config)

    # Deduplicate, instant first
    seen: set = set()
    triggered_topics: list = []
    for t in instant_topics + threshold_topics:
        if t not in seen:
            seen.add(t)
            triggered_topics.append(t)

    if not triggered_topics:
        return ""

    # Cooldown check
    state = _load_reading_state()
    now = time.time()
    cooldown_seconds = config.get('TRIGGER_COOLDOWN', 5) * 60
    newly_triggered: list = []

    for topic in triggered_topics:
        last_triggered = state.get('cooldowns', {}).get(topic, 0)
        if now - last_triggered >= cooldown_seconds:
            newly_triggered.append(topic)
            state['cooldowns'][topic] = now

    if newly_triggered:
        _save_reading_state(state)
        memories = []
        for topic in newly_triggered:
            content = _load_monograph_content(topic)
            if content:
                memories.append(content)
        if memories:
            topics_str = ', '.join(newly_triggered)
            return f"[察言观色 triggered: {topics_str}]\n\n" + "\n\n".join(memories)

    return ""


def readingbetweenthelines_stat() -> str:
    """Return current word counts and active triggers summary"""
    state = _load_reading_state()
    config = get_config()
    word_counts = state.get('word_counts', {})
    cooldowns = state.get('cooldowns', {})

    # Top 20 words
    top = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    # Check what is currently triggering
    instant_topics = check_instant_triggers(word_counts, config)
    threshold_topics = check_threshold_triggers(word_counts, config)

    cooldown_seconds = config.get('TRIGGER_COOLDOWN', 5) * 60
    now = time.time()
    in_cooldown = [t for t in (instant_topics + threshold_topics)
                   if now - cooldowns.get(t, 0) < cooldown_seconds]

    report = f"## 察言观色 — Status\n\n"
    report += f"**Words tracked**: {len(word_counts)}\n"
    report += f"**Instant triggers**: {len(instant_topics)} active\n"
    report += f"**Threshold triggers**: {len(threshold_topics)} active\n"
    report += f"**In cooldown**: {len(in_cooldown)} ({', '.join(in_cooldown) if in_cooldown else 'none'})\n\n"

    report += "**Top words**:\n"
    for word, count in top:
        tag = ""
        if word in instant_topics:
            tag = " [instant]"
        elif word in threshold_topics:
            tag = " [threshold]"
        report += f"- {word}: {count}{tag}\n"

    return report


def readingbetweenthelines_clear() -> str:
    """Clear the word count state (reset sliding window)"""
    state = _load_reading_state()
    state['word_counts'] = {}
    state['last_messages'] = []
    # Keep cooldowns
    _save_reading_state(state)
    return "察言观色 state cleared. Word counts reset."


# ============================================================================
# Initialization Guard
# ============================================================================

_initialized = False

def _lazy_init():
    """Run ensure_dirs() only once, on first use. Safe to call multiple times."""
    global _initialized
    if not _initialized:
        ensure_dirs()
        _initialized = True

# ============================================================================
# Micro-Macro Workflow Memory
# ============================================================================

def get_workflows_path() -> Path:
    """Get workflow files directory"""
    return get_workflow_path()

def load_workflow(micro: str) -> Optional[Dict]:
    """Load a workflow by micro keyword (exact match, case-insensitive)"""
    workflows_dir = get_workflows_path()
    micro_lower = micro.lower().strip()
    for fpath in workflows_dir.glob("*.yaml"):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                wf = yaml.safe_load(f)
            if wf and wf.get('micro', '').lower().strip() == micro_lower:
                return wf
        except Exception:
            continue
    return None

def match_workflow(user_input: str) -> Optional[Dict]:
    """
    Match user input against all registered micro keywords.
    Returns the first matching workflow, or None.
    """
    workflows_dir = get_workflows_path()
    input_lower = user_input.lower()
    for fpath in sorted(workflows_dir.glob("*.yaml")):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                wf = yaml.safe_load(f)
            if not wf:
                continue
            micro = wf.get('micro', '').lower().strip()
            if micro and micro in input_lower:
                return wf
        except Exception:
            continue
    return None

def save_workflow(micro: str, macro: str, keywords: List[str] = None,
                  description: str = "") -> str:
    """Save a micro-macro workflow to a YAML file"""
    workflows_dir = get_workflows_path()
    safe_name = re.sub(r'[^\w\-]', '_', micro.lower().strip())[:50]
    fpath = workflows_dir / f"{safe_name}.yaml"
    wf = {
        'micro': micro.strip(),
        'macro': macro.strip(),
        'description': description.strip(),
        'keywords': [k.strip() for k in (keywords or [])],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
    }
    with open(fpath, 'w', encoding='utf-8') as f:
        yaml.dump(wf, f, allow_unicode=True, sort_keys=False)
    return str(fpath)

def delete_workflow(micro: str) -> bool:
    """Delete a workflow by micro keyword"""
    wf = load_workflow(micro)
    if not wf:
        return False
    workflows_dir = get_workflows_path()
    micro_lower = micro.lower().strip()
    for fpath in workflows_dir.glob("*.yaml"):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                w = yaml.safe_load(f)
            if w and w.get('micro', '').lower().strip() == micro_lower:
                fpath.unlink()
                return True
        except Exception:
            continue
    return False

def list_workflows() -> List[Dict]:
    """List all registered workflows"""
    workflows_dir = get_workflows_path()
    result = []
    for fpath in sorted(workflows_dir.glob("*.yaml")):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                wf = yaml.safe_load(f)
            if wf:
                result.append({
                    'micro': wf.get('micro', ''),
                    'macro': wf.get('macro', '')[:100] + ('...' if len(wf.get('macro', '')) > 100 else ''),
                    'description': wf.get('description', ''),
                    'created_at': wf.get('created_at', ''),
                })
        except Exception:
            continue
    return result

# ============================================================================
# Proactive Keyword Triggers
# ============================================================================

def get_proactive_memory(user_message: str) -> str:
    """
    Check if user message contains any trigger keyword.
    If so, load and return the associated memory content.
    """
    config = get_config()
    if not config.get('PROACTIVE_TRIGGERS_ENABLED', True):
        return ""
    triggers = config.get('PROACTIVE_KEYWORDS', {})
    if not triggers:
        return ""
    msg_lower = user_message.lower()
    for keyword, topic in triggers.items():
        if keyword in msg_lower:
            memory_content = _load_monograph_content(topic)
            if memory_content:
                return memory_content
    return ""

def _load_monograph_content(topic: str) -> str:
    """Load monograph content by topic name (without .md)"""
    config = get_config()
    monograph_dir = get_monograph_path()
    safe_topic = re.sub(r'[^\w\-]', '-', topic)
    fpath = monograph_dir / f"{safe_topic}.md"
    if fpath.exists():
        return fpath.read_text(encoding='utf-8')
    return ""

def list_triggers() -> List[Dict]:
    """List all configured proactive keyword triggers"""
    config = get_config()
    triggers = config.get('PROACTIVE_KEYWORDS', {})
    result = []
    for kw, topic in triggers.items():
        content_preview = ""
        content = _load_monograph_content(topic)
        if content:
            # Get first non-empty line as preview
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    content_preview = line.strip()[:80]
                    break
        result.append({
            'keyword': kw,
            'topic': topic,
            'preview': content_preview,
        })
    return result

def add_trigger(keyword: str, topic: str) -> str:
    """Add a proactive keyword trigger"""
    config = get_config()
    triggers = config.get('PROACTIVE_KEYWORDS', {})
    kw = keyword.lower().strip()
    triggers[kw] = topic.strip()
    config['PROACTIVE_KEYWORDS'] = triggers
    save_user_config(config)
    reload_config()
    return f"Added trigger: '{keyword}' -> '{topic}'"

def remove_trigger(keyword: str) -> str:
    """Remove a proactive keyword trigger"""
    config = get_config()
    triggers = config.get('PROACTIVE_KEYWORDS', {})
    kw = keyword.lower().strip()
    if kw in triggers:
        del triggers[kw]
        config['PROACTIVE_KEYWORDS'] = triggers
        save_user_config(config)
        reload_config()
        return f"Removed trigger: '{keyword}'"
    return f"Trigger not found: '{keyword}'"

# ============================================================================
# Special Needs - Before/After Answer Memory
# ============================================================================

def get_before_answer_memory() -> str:
    """Get memory that should be loaded before each answer"""
    config = get_config()
    topic = config.get("BEFORE_ANSWER", "")
    
    if not topic:
        return ""
    
    # Read the monograph content
    safe_topic = re.sub(r'[^\w\-]', '-', topic)
    filepath = get_monograph_path() / f"{safe_topic}.md"
    
    if filepath.exists():
        return filepath.read_text(encoding='utf-8')
    
    return ""

def get_after_answer_memory() -> str:
    """Get memory that should be processed after each answer"""
    config = get_config()
    topic = config.get("AFTER_ANSWER", "")
    
    if not topic:
        return ""
    
    # Read the monograph content
    safe_topic = re.sub(r'[^\w\-]', '-', topic)
    filepath = get_monograph_path() / f"{safe_topic}.md"
    
    if filepath.exists():
        return filepath.read_text(encoding='utf-8')
    
    return ""

def check_special_needs() -> Dict[str, str]:
    """Check and return special needs configuration"""
    config = get_config()
    return {
        "before_answer": config.get("BEFORE_ANSWER", ""),
        "after_answer": config.get("AFTER_ANSWER", "")
    }

def ensure_dirs():
    """Ensure all directories exist"""
    for d in [get_chronicle_path(), get_monograph_path(), get_index_path(), get_workflows_path()]:
        d.mkdir(parents=True, exist_ok=True)
    init_db()

# ============================================================================
# SQLite Database
# ============================================================================

def get_db_path() -> Path:
    """Get SQLite database path"""
    return get_chronicle_path() / "db.sqlite"

def init_db():
    """Initialize database schema"""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Chronicle index
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chronicle_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            keywords TEXT,
            content_preview TEXT,
            session_id TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Monograph index
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monograph_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL UNIQUE,
            file_path TEXT NOT NULL,
            user TEXT,
            creator TEXT DEFAULT 'OpenClaw',
            technical_environment TEXT,
            circumstance_purpose TEXT,
            key_steps TEXT,
            errors_trials TEXT,
            conclusion TEXT,
            directory TEXT,
            keywords TEXT,
            tokens_used INTEGER,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # Association table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS associations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_word TEXT NOT NULL,
            to_word TEXT NOT NULL,
            weight REAL DEFAULT 0.5,
            UNIQUE(from_word, to_word)
        )
    ''')
    
    # Indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chronicle_date ON chronicle_index(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chronicle_timestamp ON chronicle_index(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_monograph_topic ON monograph_index(topic)')
    
    conn.commit()
    conn.close()

# ============================================================================
# Keyword Extraction
# ============================================================================

class KeywordExtractor:
    """Keyword extractor with enhanced features"""
    
    STOP_WORDS = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it'
    }
    
    QUESTION_WORDS = {'how', 'what', 'why', 'when', 'where', 'which', '?'}
    ERROR_WORDS = {'error', 'fail', 'failed', 'exception', 'bug', 'issue', 'problem'}
    
    def __init__(self):
        config = get_config()
        self.keyword_count = config.get('KEYWORD_COUNT', 20)
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract keywords and metadata"""
        words = re.findall(r'[\w]+', text.lower())
        filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 1]
        freq = Counter(filtered)
        
        return {
            "word_frequency": dict(freq.most_common(self.keyword_count)),
            "questions": self._extract_questions(text),
            "errors": self._extract_errors(text),
            "unique_info": self._extract_unique(text),
            "total_words": len(filtered)
        }
    
    def _extract_questions(self, text: str) -> List[str]:
        questions = []
        for sent in re.split(r'[.!?\n]', text):
            if any(q in sent.lower() for q in self.QUESTION_WORDS):
                if sent.strip():
                    questions.append(sent.strip()[:200])
        return questions[:5]
    
    def _extract_errors(self, text: str) -> List[str]:
        errors = []
        text_lower = text.lower()
        for word in self.ERROR_WORDS:
            if word in text_lower:
                idx = text_lower.find(word)
                start, end = max(0, idx - 30), min(len(text), idx + 50)
                if text[start:end].strip():
                    errors.append(text[start:end].strip())
        return errors[:5]
    
    def _extract_unique(self, text: str) -> List[str]:
        unique = []
        unique.extend(re.findall(r'[/\\][\w\-./\\]+\.\w+', text)[:3])
        unique.extend(re.findall(r'`[^`]+`', text)[:3])
        unique.extend(re.findall(r'\d+\.\d+\.\d+', text)[:3])
        return unique

# ============================================================================
# Association Generator
# ============================================================================

class AssociationGenerator:
    """Association word generator"""
    
    ASSOCIATION_MAP = {
        'python': ['code', 'script', 'execute', 'pip'],
        'cline': ['cli', 'integration', 'call', 'windows'],
        'api': ['http', 'network', 'request', 'timeout'],
        'error': ['fail', 'exception', 'debug', 'issue'],
        'database': ['sql', 'query', 'storage', 'connection'],
        'git': ['version', 'commit', 'branch', 'push'],
        'fail': ['retry', 'error', 'debug', 'solve'],
        'timeout': ['network', 'retry', 'slow'],
        'config': ['setting', 'parameter', 'option'],
        'project': ['develop', 'code', 'task'],
        'develop': ['code', 'test', 'debug'],
    }
    
    def __init__(self):
        config = get_config()
        self.association_depth = config.get('ASSOCIATION_DEPTH', 3)
    
    def generate(self, keywords: Dict[str, int]) -> List[Dict[str, Any]]:
        associations = []
        for word, freq in keywords.items():
            word_lower = word.lower()
            if word_lower in self.ASSOCIATION_MAP:
                for assoc in self.ASSOCIATION_MAP[word_lower][:self.association_depth]:
                    if assoc != word:
                        associations.append({"from": word, "to": assoc, "weight": 0.8})
            if freq > 3:
                associations.append({"from": word, "to": "high_frequency", "weight": min(freq/10, 1.0)})
        
        seen = set()
        unique = []
        for a in associations:
            key = (a['from'], a['to'])
            if key not in seen:
                seen.add(key)
                unique.append(a)
        return unique[:20]

# ============================================================================
# Chronicle Operations
# ============================================================================

def save_chronicle(content: str, session_id: str = None) -> str:
    """Save temporal memory to Chronicle"""
    _lazy_init()
    config = get_config()
    extractor = KeywordExtractor()
    keywords = extractor.extract(content)
    
    # Filename format: YYYY-MM-DD-HH-mm.md
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{timestamp}.md"
    filepath = get_chronicle_path() / filename
    
    keyword_str = ",".join(list(keywords["word_frequency"].keys())[:10])
    
    # Build markdown
    md_content = f"""# Chronicle - {date}

## Metadata
- **Timestamp**: {timestamp}
- **Session**: {session_id or 'N/A'}
- **Keywords**: {keyword_str}

## Content
{content}

## Analysis
| Keyword | Frequency |
|---------|-----------|
"""
    for kw, cnt in list(keywords["word_frequency"].items())[:15]:
        md_content += f"| {kw} | {cnt} |\n"
    
    filepath.write_text(md_content, encoding='utf-8')
    
    # Index in SQLite
    conn = sqlite3.connect(str(get_db_path()))
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chronicle_index 
        (file_name, file_path, timestamp, date, keywords, content_preview, session_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (filename, str(filepath), timestamp, date, keyword_str, content[:200], session_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return str(filepath)

def query_chronicle(keyword: str = None, start_date: str = None, end_date: str = None, limit: int = 100) -> List[Dict]:
    """Query Chronicle via SQLite"""
    conn = sqlite3.connect(str(get_db_path()))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM chronicle_index WHERE 1=1"
    params = []
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if keyword:
        query += " AND (keywords LIKE ? OR content_preview LIKE ?)"
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    
    query += f" ORDER BY timestamp DESC LIMIT {limit}"
    cursor.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

# ============================================================================
# Monograph Operations
# ============================================================================

def save_monograph(topic: str, content: str, tokens: int, metadata: Dict = None) -> str:
    """Save important event to Monograph"""
    _lazy_init()
    extractor = KeywordExtractor()
    keywords = extractor.extract(content)
    
    # Sanitize topic name
    safe_topic = re.sub(r'[^\w\-]', '-', topic)
    filepath = get_monograph_path() / f"{safe_topic}.md"
    
    # Build metadata
    meta = metadata or {}
    keyword_str = ",".join(list(keywords["word_frequency"].keys())[:10])
    
    md_content = f"""# {topic}

## Metadata
- **Created**: {datetime.now().isoformat()}
- **User**: {meta.get('user', '')}
- **Creator**: {meta.get('creator', 'OpenClaw')}
- **Token Usage**: {tokens}
- **Keywords**: {keyword_str}

## Technical Environment
{meta.get('technical_environment', '')}

## Circumstance & Purpose
{meta.get('circumstance_and_purpose', '')}

## Key Steps
{meta.get('key_steps', '')}

## Errors & Trials
{meta.get('errors_and_trials', '')}

## Conclusion
{meta.get('conclusion', '')}

## Directory
{meta.get('directory', '')}

## Full Content
{content}

## Keyword Index
| Keyword | Frequency |
|---------|-----------|
"""
    for kw, cnt in list(keywords["word_frequency"].items())[:20]:
        md_content += f"| {kw} | {cnt} |\n"
    
    md_content += """
## Related Files
<!-- Auto-detected file paths -->

## Cross-References
<!-- Links to other monographs -->
"""
    
    filepath.write_text(md_content, encoding='utf-8')
    
    # Update index
    conn = sqlite3.connect(str(get_db_path()))
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO monograph_index 
        (topic, file_path, user, creator, technical_environment, circumstance_purpose, 
         key_steps, errors_trials, conclusion, directory, keywords, tokens_used, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (topic, str(filepath), meta.get('user', ''), meta.get('creator', 'OpenClaw'),
          meta.get('technical_environment', ''), meta.get('circumstance_and_purpose', ''),
          meta.get('key_steps', ''), meta.get('errors_and_trials', ''), meta.get('conclusion', ''),
          meta.get('directory', ''), keyword_str, tokens, datetime.now().isoformat(), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Update keyword index files
    _update_keyword_index(safe_topic, keywords["word_frequency"], filepath)
    
    return str(filepath)

def _update_keyword_index(topic: str, keywords: Dict, source_path: Path):
    """Update keyword index files — index_dir already created by _lazy_init()"""
    index_dir = get_index_path()
    # No mkdir needed: _lazy_init() already ran via save_monograph() or save_chronicle()
    
    for kw in list(keywords.keys())[:10]:
        kw_file = index_dir / f"{kw}.md"
        entry = f"""
## {topic}
- Source: {source_path}
- Updated: {datetime.now().isoformat()}
---
"""
        kw_file.write_text(entry, encoding='utf-8')

def list_monographs() -> List[Dict]:
    """List all monograph topics"""
    conn = sqlite3.connect(str(get_db_path()))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT topic, user, keywords, created_at, updated_at FROM monograph_index ORDER BY updated_at DESC")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

# ============================================================================
# File Organization
# ============================================================================

class FileOrganizer:
    """File organizer for memory-related files"""
    
    def __init__(self):
        self.workspace = Path(os.path.expanduser("~/.openclaw/workspace"))
        config = get_config()
        self.enabled = config.get('FILE_ORG_ENABLED', True)
        self.auto_move = config.get('FILE_ORG_AUTO_MOVE', False)
        self.exclude = config.get('FILE_EXCLUDE_PATHS', [".openclaw", "node_modules", ".git"])
    
    def find_related_files(self, memory_content: str) -> List[Dict]:
        if not self.enabled:
            return []
        
        paths = re.findall(r'[/\\]?([\w\-./\\]+\.\w+)', memory_content)
        related = []
        
        for path_str in set(paths):
            for full_path in self.workspace.rglob("*"):
                if full_path.name in path_str or path_str in str(full_path):
                    if full_path.is_file() and not any(ex in str(full_path) for ex in self.exclude):
                        related.append({
                            "path": str(full_path),
                            "name": full_path.name,
                            "size": full_path.stat().st_size,
                            "modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
                        })
        return related[:10]
    
    def suggest_organization(self, files: List[Dict]) -> str:
        if not files:
            return "No files found that need organization"
        
        by_dir = {}
        for f in files:
            dir_path = str(Path(f['path']).parent)
            if dir_path not in by_dir:
                by_dir[dir_path] = []
            by_dir[dir_path].append(f)
        
        suggestions = "Found the following related files:\n\n"
        for dir_path, file_list in by_dir.items():
            suggestions += f"**Directory**: `{dir_path}`\n"
            for f in file_list:
                suggestions += f"- {f['name']} ({f['size']} bytes)\n"
            suggestions += "\n"
        suggestions += "Would you like to organize them into a unified directory?"
        return suggestions

# ============================================================================
# Analysis
# ============================================================================

def analyze_memory() -> str:
    """Analyze all memory and generate report"""
    _lazy_init()
    conn = sqlite3.connect(str(get_db_path()))
    cursor = conn.cursor()
    
    # Chronicle stats
    cursor.execute("SELECT COUNT(*), MIN(date), MAX(date) FROM chronicle_index")
    c_count, c_min, c_max = cursor.fetchone()
    
    # Monograph stats
    cursor.execute("SELECT COUNT(*) FROM monograph_index")
    m_count = cursor.fetchone()[0]
    
    # Top keywords
    cursor.execute("SELECT keywords FROM chronicle_index ORDER BY timestamp DESC LIMIT 100")
    kw_text = " ".join([r[0] or "" for r in cursor.fetchall()])
    extractor = KeywordExtractor()
    top_keywords = list(extractor.extract(kw_text)["word_frequency"].items())[:30]
    
    conn.close()
    
    report = f"""# Memory Analysis Report

Generated: {datetime.now().isoformat()}

## Chronicle (Temporal) Statistics
- Total Entries: {c_count}
- Date Range: {c_min or 'N/A'} to {c_max or 'N/A'}

## Monograph (Important Events) Statistics
- Total Topics: {m_count}

## Top Keywords
| Keyword | Count |
|---------|-------|
"""
    for kw, cnt in top_keywords:
        report += f"| {kw} | {cnt} |\n"
    
    report_file = get_base_path() / "analysis.md"
    report_file.write_text(report, encoding='utf-8')
    return str(report_file)

# ============================================================================
# Auto-Save for Cron/Heartbeat
# ============================================================================

def auto_save_from_context(context: Dict = None) -> str:
    """Auto-save triggered by cron/heartbeat"""
    config = get_config()
    
    if not config.get('AUTO_SAVE', True):
        return "Auto-save disabled"
    
    # Get content from context (session history)
    content = ""
    if context and 'content' in context:
        content = context['content']
    
    if not content:
        return "No content to save"
    
    threshold = config.get('TOKEN_THRESHOLD', 10000)
    
    if len(content) > threshold:
        topic = context.get('topic', 'General') if context else 'General'
        save_monograph(topic, content, len(content))
        return f"Saved to Monograph: {topic}"
    else:
        save_chronicle(content)
        return "Saved to Chronicle"

# ============================================================================
# Main Handler
# ============================================================================

class Hippocampus:
    """Main handler for Hippocampus skill"""
    
    def __init__(self):
        self.organizer = FileOrganizer()
        self.current_topic = None
        self.round_count = 0
        self.last_save_time = time.time()
        # Reload config to get latest values
        reload_config()
    
    def process(self, command: str, args: str = "", context: Dict = None) -> str:
        """Process command"""
        context = context or {}

        # Reload config for each command (to pick up user changes)
        reload_config()

        # === Proactive trigger: load relevant memory if keyword found ===
        proactive = context.get("proactive_message", "")
        if proactive:
            proactive_content = get_proactive_memory(proactive)
            if proactive_content:
                # Prepend proactive memory to context for this turn
                ctx = dict(context)
                ctx["content"] = (proactive_content + "\n\n" + ctx.get("content", "")).strip()
                context = ctx

        # === Micro-Macro: match workflow if user input contains micro keyword ===
        config = get_config()
        if config.get('MICRO_MACRO_ENABLED', True) and proactive:
            matched = match_workflow(proactive)
            if matched:
                self.current_workflow = matched
                return f"[Workflow triggered] {matched.get('micro')} -> {matched.get('macro', '')[:200]}"

        # === Command routing ===
        if command == "new":
            return self._cmd_new(args)
        elif command == "add":
            return self._cmd_add(args)
        elif command == "save":
            return self._cmd_save(context.get("content", ""))
        elif command == "recall":
            return self._cmd_recall(args)
        elif command == "checkpoint":
            return self._cmd_checkpoint(context)
        elif command == "warn":
            return self._cmd_warn(context)
        elif command == "graph":
            return self._cmd_graph()
        elif command == "important":
            return self._cmd_important()
        elif command == "search":
            return self._cmd_search(args)
        elif command == "status":
            return self._cmd_status()
        elif command == "config":
            return self._cmd_config(args)
        elif command == "files":
            return self._cmd_files(context.get("content", ""))
        elif command == "query":
            return self._cmd_query(args)
        elif command == "analyze":
            return self._cmd_analyze()
        elif command == "collect":
            return self._cmd_collect(context.get("content", ""))
        elif command == "reload":
            return self._cmd_reload()
        elif command == "init":
            return self._cmd_init()
        elif command == "autocheck":
            return self._cmd_autocheck(context)

        # Micro-Macro commands
        elif command == "learn-workflow":
            return self._cmd_learn_workflow(args)
        elif command == "workflows":
            return self._cmd_workflows()
        elif command == "forget-workflow":
            return self._cmd_forget_workflow(args)

        # Proactive trigger commands
        elif command == "triggers":
            return self._cmd_triggers()
        elif command == "add-trigger":
            return self._cmd_add_trigger(args)
        elif command == "remove-trigger":
            return self._cmd_remove_trigger(args)

        # 察言观色 — ReadingBetweenTheLines
        elif command == "readingbetweenthelines":
            return self._cmd_readingbetweenthelines()
        elif command == "readingbetweenthelines-stat":
            return self._cmd_readingbetweenthelines_stat()
        elif command == "readingbetweenthelines-clear":
            return self._cmd_readingbetweenthelines_clear()
        elif command == "add-instant":
            return self._cmd_add_instant(args)
        elif command == "remove-instant":
            return self._cmd_remove_instant(args)
        elif command == "add-threshold":
            return self._cmd_add_threshold(args)
        elif command == "remove-threshold":
            return self._cmd_remove_threshold(args)

        # Natural language aliases
        elif command in ["setup", "setup-all", "setup memory", "configure memory", "enable auto-save"]:
            return self._cmd_setup_all()
        elif command in ["setup-hooks", "configure hooks", "enable hooks"]:
            return self._cmd_setup_hooks()
        elif command in ["sync-memory", "sync to memory", "save to memory", "remember this"]:
            return self._cmd_sync_memory()
        elif command in ["memory", "save memory", "remember"]:
            return self._cmd_save(context.get("content", ""))
        elif command in ["recall memory", "remember"]:
            return self._cmd_recall(args)

        # User confirmation handlers
        elif command in ["yes", "confirm", "do it", "execute"]:
            return self._cmd_do_setup(args)
        elif command in ["yes-hooks", "confirm-hooks"]:
            return self._cmd_do_setup_hooks()
        elif command in ["yes-sync", "confirm-sync", "do-sync"]:
            return self._cmd_do_sync_memory()
        else:
            return self._help()
    
    def _cmd_new(self, name: str) -> str:
        if not name:
            return "Please specify topic name, e.g.: /hip new ProjectX"
        self.current_topic = name
        self.round_count = 0
        save_monograph(name, f"# {name}\n\nCreated: {datetime.now().isoformat()}", 0)
        return f"Created monograph topic: **{name}**"
    
    def _cmd_add(self, content: str) -> str:
        if not self.current_topic:
            return "Please create a topic first: /hip new <name>"
        extractor = KeywordExtractor()
        keywords = extractor.extract(content)
        save_monograph(self.current_topic, content, len(content))
        return f"Content added. Keywords: {len(keywords['word_frequency'])}, Errors: {len(keywords['errors'])}"
    
    def _cmd_save(self, content: str) -> str:
        config = get_config()
        
        if not content:
            return "No content to save"
        
        threshold = config.get('TOKEN_THRESHOLD', 10000)
        
        if len(content) > threshold:
            topic = self.current_topic or "General"
            save_monograph(topic, content, len(content))
            result = f"Saved to Monograph: {topic}"
        else:
            save_chronicle(content)
            result = "Saved to Chronicle"
        
        self.round_count = 0
        self.last_save_time = time.time()
        return result
    
    def _cmd_recall(self, keyword: str) -> str:
        if not keyword:
            results = query_chronicle(limit=5)
            if not results:
                return "No records found"
            report = "## Recent Chronicle Records\n\n"
            for r in results:
                report += f"- **{r['file_name']}**: {r['content_preview'][:80]}...\n"
            return report
        
        results = query_chronicle(keyword=keyword, limit=10)
        if results:
            report = f"## Chronicle Search: '{keyword}'\n\n"
            for r in results:
                report += f"- {r['file_name']}: {r['content_preview'][:60]}...\n"
            return report
        
        monographs = list_monographs()
        matches = [m for m in monographs if keyword.lower() in m.get('topic', '').lower()]
        if matches:
            report = f"## Monograph: '{keyword}'\n\n"
            for m in matches:
                report += f"- {m['topic']} (updated: {m['updated_at'][:10]})\n"
            return report
        
        return f"No records found for '{keyword}'"
    
    def _cmd_important(self) -> str:
        monographs = list_monographs()
        if not monographs:
            return "No monograph topics found"
        report = "## Monograph Topics (Important Events)\n\n"
        for m in monographs:
            report += f"- **{m['topic']}** (updated: {m['updated_at'][:10]})\n"
        return report
    
    def _cmd_search(self, keyword: str) -> str:
        return self._cmd_recall(keyword)
    
    def _cmd_status(self) -> str:
        conn = sqlite3.connect(str(get_db_path()))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM chronicle_index")
        c_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM monograph_index")
        m_count = cursor.fetchone()[0]
        conn.close()
        
        config = get_config()
        
        # Check special needs
        before = config.get("BEFORE_ANSWER", "")
        after = config.get("AFTER_ANSWER", "")
        
        return f"""## Hippocampus Status

### Chronicle
- Records: {c_count}

### Monograph
- Topics: {m_count}
- Current: {self.current_topic or 'None'}

### Special Needs
- Before Answer: {before or '(not set)'}
- After Answer: {after or '(not set)'}

### Configuration (from USER_CONFIG.md)
- Round Threshold: {config.get('ROUND_THRESHOLD', 25)}
- Time Hours: {config.get('TIME_HOURS', 6)}
- Token Threshold: {config.get('TOKEN_THRESHOLD', 10000)}
- Auto-save: {config.get('AUTO_SAVE', True)}

### Storage
{get_base_path()}"""
    
    def _cmd_config(self, args: str) -> str:
        config = get_config()
        
        if not args:
            # Show user config file
            if USER_CONFIG_FILE.exists():
                return f"```\n{USER_CONFIG_FILE.read_text(encoding='utf-8')}\n```"
            return f"```json\n{json.dumps(config, indent=2)}\n```"
        
        # Handle edit request
        if args.strip() == "edit":
            return f"Please edit USER_CONFIG.md directly:\n{USER_CONFIG_FILE}"
        
        if args.strip() == "reload":
            return self._cmd_reload()
        
        return "Usage: /hip config (show) | /hip config reload"
    
    def _cmd_reload(self) -> str:
        reload_config()
        config = get_config()
        return f"""Config reloaded!

- Round Threshold: {config.get('ROUND_THRESHOLD')}
- Time Hours: {config.get('TIME_HOURS')}
- Token Threshold: {config.get('TOKEN_THRESHOLD')}
- Auto-save: {config.get('AUTO_SAVE')}"""
    
    def _cmd_init(self) -> str:
        """Initialize directories and database"""
        ensure_dirs()
        db_path = get_db_path()
        return f"""Initialized!

- Database: {db_path}
- Chronicle: {get_chronicle_path()}
- Monograph: {get_monograph_path()}
- Index: {get_index_path()}"""
    
    def _cmd_files(self, content: str) -> str:
        if not content:
            return "No content to analyze"
        files = self.organizer.find_related_files(content)
        if not files:
            return "No related files found"
        return self.organizer.suggest_organization(files)
    
    def _cmd_query(self, args: str) -> str:
        keyword = args.strip() or None
        results = query_chronicle(keyword=keyword, limit=10)
        if not results:
            return "No chronicle records found"
        report = "## Chronicle Records\n\n"
        for r in results:
            report += f"- [{r['date']}] {r['content_preview'][:60]}... | {r['keywords']}\n"
        return report
    
    def _cmd_analyze(self) -> str:
        report = analyze_memory()
        return f"Analysis complete: {report}"
    
    def _cmd_collect(self, content: str) -> str:
        if not content:
            return "No content to analyze"
        files = self.organizer.find_related_files(content)
        if not files:
            return "No files to collect"
        return self.organizer.suggest_organization(files)
    
    def check_trigger(self, round_count: int, token_count: int) -> Optional[str]:
        config = get_config()
        
        if round_count >= config.get('ROUND_THRESHOLD', 25):
            return "round"
        if token_count >= config.get('TOKEN_THRESHOLD', 10000):
            return "token"
        hours = (time.time() - self.last_save_time) / 3600
        if hours >= config.get('TIME_HOURS', 6):
            return "time"
        return None
    
    def _cmd_autocheck(self, context: Dict = None) -> str:
        """Check triggers and auto-save if needed - called by cron/hook"""
        config = get_config()
        
        if not config.get('AUTO_SAVE', True):
            return "Auto-save disabled"
        
        # Get content from context
        content = ""
        if context and 'content' in context:
            content = context.get('content', '')
        elif context and 'history' in context:
            # Try to get from history
            history = context.get('history', [])
            if history:
                content = "\n".join([str(h) for h in history[-20:]])
        
        if not content:
            return "No content to check"
        
        # Check token count
        token_count = len(content)
        round_count = context.get('round_count', 0) if context else 0
        
        # Check if trigger is met
        trigger_type = self.check_trigger(round_count, token_count)
        
        if trigger_type:
            # Save based on threshold
            threshold = config.get('TOKEN_THRESHOLD', 10000)
            if token_count > threshold:
                topic = context.get('topic', 'General') if context else 'General'
                save_monograph(topic, content, token_count)
                result = f"Auto-saved to Monograph (trigger: {trigger_type}, tokens: {token_count})"
            else:
                save_chronicle(content)
                result = f"Auto-saved to Chronicle (trigger: {trigger_type}, tokens: {token_count})"
            
            # Reset counters
            self.round_count = 0
            self.last_save_time = time.time()
            return result
        else:
            return f"No trigger met yet (rounds: {round_count}, tokens: {token_count}, hours: {(time.time()-self.last_save_time)/3600:.1f})"
    
    def _cmd_checkpoint(self, context: Dict = None) -> str:
        """Save current project state as a monograph"""
        content = context.get("content", "") if context else ""
        if not content:
            return "No context to save as checkpoint."
        topic = context.get("topic", "checkpoint") if context else "checkpoint"
        save_monograph(topic, content, len(content))
        return f"Checkpoint saved: **{topic}**"

    def _cmd_warn(self, context: Dict = None) -> str:
        """Check for failure patterns in recent context"""
        content = context.get("content", "") if context else ""
        if not content:
            return "No context to analyze for failure patterns."
        extractor = KeywordExtractor()
        errors = extractor.extract(content).get("errors", [])
        if not errors:
            return "No failure patterns detected in recent context."
        report = "## Failure Patterns Detected\n\n"
        for i, err in enumerate(errors, 1):
            report += f"{i}. {err}\n"
        return report

    def _cmd_graph(self) -> str:
        """Show knowledge graph overview"""
        conn = sqlite3.connect(str(get_db_path()))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM associations")
        edge_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM monograph_index")
        node_count = cursor.fetchone()[0]
        cursor.execute("SELECT from_word, to_word, weight FROM associations ORDER BY weight DESC LIMIT 10")
        top_edges = cursor.fetchall()
        conn.close()
        report = f"## Knowledge Graph\n\n- Nodes (monographs): {node_count}\n- Edges (associations): {edge_count}\n\n**Top connections:**\n"
        for from_w, to_w, weight in top_edges:
            report += f"- {from_w} --({weight:.2f})--> {to_w}\n"
        return report

    # ── Micro-Macro commands ────────────────────────────────────────────────

    def _cmd_learn_workflow(self, args: str) -> str:
        """
        Register a micro-macro workflow.
        Usage: /hippo learn-workflow <micro> -> <macro description>
        Example: /hippo learn-workflow deploy -> Run git push, then execute tests, then notify team via Slack
        """
        if '->' not in args and '→' not in args:
            return ("Format: /hippo learn-workflow <micro> -> <macro>\n"
                    "Example: /hippo learn-workflow deploy -> Run git push, then run tests, then notify team")
        separator = '->' if '->' in args else '→'
        micro, macro = args.split(separator, 1)
        micro = micro.strip()
        macro = macro.strip()
        if not micro or not macro:
            return "Both micro and macro must be non-empty."
        # Check if workflow already exists
        existing = load_workflow(micro)
        if existing:
            save_workflow(micro, macro)
            return f"Updated workflow: '{micro}' -> '{macro[:80]}...'"
        save_workflow(micro, macro)
        return f"Registered workflow: '{micro}' -> '{macro[:80]}...'"

    def _cmd_workflows(self) -> str:
        """List all registered micro-macro workflows"""
        workflows = list_workflows()
        if not workflows:
            return "No workflows registered. Use /hippo learn-workflow <micro> -> <macro>"
        report = f"## Registered Workflows ({len(workflows)})\n\n"
        for wf in workflows:
            report += f"**{wf['micro']}**\n  → {wf['macro']}\n"
            if wf.get('description'):
                report += f"  Note: {wf['description']}\n"
            report += "\n"
        return report

    def _cmd_forget_workflow(self, args: str) -> str:
        """Remove a registered workflow by micro keyword"""
        if not args.strip():
            return "Usage: /hippo forget-workflow <micro>"
        success = delete_workflow(args)
        if success:
            return f"Deleted workflow: '{args.strip()}'"
        return f"Workflow not found: '{args.strip()}'"

    # ── Proactive trigger commands ─────────────────────────────────────────

    def _cmd_triggers(self) -> str:
        """List all configured proactive keyword triggers"""
        triggers = list_triggers()
        config = get_config()
        enabled = config.get('PROACTIVE_TRIGGERS_ENABLED', True)
        report = f"## Proactive Triggers (enabled: {enabled})\n\n"
        if not triggers:
            report += "No triggers configured. Use /hippo add-trigger <keyword> -> <monograph-topic>\n"
        for t in triggers:
            report += f"- **{t['keyword']}** -> {t['topic']}\n"
            if t.get('preview'):
                report += f"  Preview: {t['preview'][:80]}\n"
        report += "\nConfigure in USER_CONFIG.md: PROACTIVE_KEYWORDS = ..."
        return report

    def _cmd_add_trigger(self, args: str) -> str:
        """
        Add a proactive keyword trigger.
        Usage: /hippo add-trigger <keyword> -> <monograph-topic>
        Example: /hippo add-trigger database -> database-architecture
        """
        if '->' not in args and '→' not in args:
            return ("Format: /hippo add-trigger <keyword> -> <monograph-topic>\n"
                    "Example: /hippo add-trigger database -> database-architecture\n"
                    "Note: monograph-topic is a file in the monograph directory (without .md)")
        separator = '->' if '->' in args else '→'
        keyword, topic = args.split(separator, 1)
        return add_trigger(keyword.strip(), topic.strip())

    def _cmd_remove_trigger(self, args: str) -> str:
        """Remove a proactive keyword trigger"""
        if not args.strip():
            return "Usage: /hippo remove-trigger <keyword>"
        return remove_trigger(args.strip())

    # ── 察言观色 — ReadingBetweenTheLines commands ─────────────────────────

    def _cmd_readingbetweenthelines(self) -> str:
        """Show 察言观色 status and configuration"""
        config = get_config()
        enabled = config.get('READINGBETWEENTHELINES_ENABLED', True)
        instant = config.get('INSTANT_TRIGGERS', '')
        threshold = config.get('THRESHOLD_TRIGGERS', '')
        interval = config.get('HEARTBEAT_INTERVAL', 1)
        window = config.get('SLIDING_WINDOW', 10)
        cooldown = config.get('TRIGGER_COOLDOWN', 5)
        report = f"""## 察言观色 — ReadingBetweenTheLines

**Status**: {'Enabled' if enabled else 'Disabled'}
**Heartbeat**: every {interval} minute(s)
**Sliding window**: {window} minutes
**Cooldown**: {cooldown} minutes

**Instant triggers** (fire immediately):
  {instant or '(none)'}

**Threshold triggers** (fire after N occurrences):
  {threshold or '(none)'}

**Commands**:
  /hippo readingbetweenthelines-stat  — Show current word counts
  /hippo readingbetweenthelines-clear — Reset word counts
  /hippo add-instant <kw> -> <topic>     — Add instant trigger
  /hippo remove-instant <kw>             — Remove instant trigger
  /hippo add-threshold <kw> -> <count>   — Add threshold trigger
  /hippo remove-threshold <kw>            — Remove threshold trigger
"""
        return report

    def _cmd_readingbetweenthelines_stat(self) -> str:
        """Show current word counts in sliding window"""
        return readingbetweenthelines_stat()

    def _cmd_readingbetweenthelines_clear(self) -> str:
        """Clear word count state"""
        return readingbetweenthelines_clear()

    def _cmd_add_instant(self, args: str) -> str:
        """Add an instant trigger: /hippo add-instant <keyword> -> <monograph-topic>"""
        if '->' not in args and '→' not in args:
            return ("Format: /hippo add-instant <keyword> -> <monograph-topic>\n"
                    "Example: /hippo add-instant error -> error-patterns")
        sep = '->' if '->' in args else '→'
        keyword, topic = args.split(sep, 1)
        kw = keyword.strip().lower()
        topic = topic.strip()
        if not kw or not topic:
            return "Both keyword and topic must be non-empty."
        config = get_config()
        raw = config.get('INSTANT_TRIGGERS', '')
        # Parse existing
        mapping = {}
        if isinstance(raw, str) and raw:
            for pair in raw.split(','):
                if '->' in pair:
                    k, v = pair.split('->', 1)
                    mapping[k.strip().lower()] = v.strip()
        mapping[kw] = topic
        # Rebuild string
        new_raw = ','.join(f'{k}->{v}' for k, v in mapping.items())
        config['INSTANT_TRIGGERS'] = new_raw
        save_user_config(config)
        reload_config()
        return f"Added instant trigger: '{kw}' -> '{topic}'"

    def _cmd_remove_instant(self, args: str) -> str:
        """Remove an instant trigger"""
        if not args.strip():
            return "Usage: /hippo remove-instant <keyword>"
        kw = args.strip().lower()
        config = get_config()
        raw = config.get('INSTANT_TRIGGERS', '')
        mapping = {}
        if isinstance(raw, str) and raw:
            for pair in raw.split(','):
                if '->' in pair:
                    k, v = pair.split('->', 1)
                    mapping[k.strip().lower()] = v.strip()
        if kw in mapping:
            del mapping[kw]
            new_raw = ','.join(f'{k}->{v}' for k, v in mapping.items())
            config['INSTANT_TRIGGERS'] = new_raw
            save_user_config(config)
            reload_config()
            return f"Removed instant trigger: '{kw}'"
        return f"Instant trigger not found: '{kw}'"

    def _cmd_add_threshold(self, args: str) -> str:
        """Add a threshold trigger: /hippo add-threshold <keyword> -> <count>"""
        if '->' not in args and '→' not in args:
            return ("Format: /hippo add-threshold <keyword> -> <count>\n"
                    "Example: /hippo add-threshold project -> 5")
        sep = '->' if '->' in args else '→'
        keyword, count_str = args.split(sep, 1)
        kw = keyword.strip().lower()
        try:
            count = int(count_str.strip())
        except ValueError:
            return f"Count must be a number, got: '{count_str.strip()}'"
        if count < 1:
            return "Count must be at least 1."
        config = get_config()
        raw = config.get('THRESHOLD_TRIGGERS', '')
        mapping = {}
        if isinstance(raw, str) and raw:
            for pair in raw.split(','):
                if '->' in pair:
                    k, v = pair.split('->', 1)
                    try:
                        mapping[k.strip().lower()] = int(v.strip())
                    except ValueError:
                        pass
        mapping[kw] = count
        new_raw = ','.join(f'{k}->{v}' for k, v in mapping.items())
        config['THRESHOLD_TRIGGERS'] = new_raw
        save_user_config(config)
        reload_config()
        return f"Added threshold trigger: '{kw}' fires after {count} occurrences"

    def _cmd_remove_threshold(self, args: str) -> str:
        """Remove a threshold trigger"""
        if not args.strip():
            return "Usage: /hippo remove-threshold <keyword>"
        kw = args.strip().lower()
        config = get_config()
        raw = config.get('THRESHOLD_TRIGGERS', '')
        mapping = {}
        if isinstance(raw, str) and raw:
            for pair in raw.split(','):
                if '->' in pair:
                    k, v = pair.split('->', 1)
                    try:
                        mapping[k.strip().lower()] = int(v.strip())
                    except ValueError:
                        pass
        if kw in mapping:
            del mapping[kw]
            new_raw = ','.join(f'{k}->{v}' for k, v in mapping.items())
            config['THRESHOLD_TRIGGERS'] = new_raw
            save_user_config(config)
            reload_config()
            return f"Removed threshold trigger: '{kw}'"
        return f"Threshold trigger not found: '{kw}'"

    def _cmd_setup_hooks(self) -> str:
        """Generate cron/hook setup commands"""
        skill_path = str(SKILL_DIR)
        return f"""# Add these cron jobs for automatic memory saving:

# 1. Time-based trigger (every {get_config().get('TIME_HOURS', 6)} hours)
cron add --name "hippocampus-autosave-time" \
  --schedule "0 */{get_config().get('TIME_HOURS', 6)} * * *" \
  --session-target isolated \
  --payload 'Run: python3 {skill_path}/scripts/memory.py autocheck'

# 2. Session end hook (automatic save on session close)
# Note: This requires OpenClaw hook configuration

# Alternative: Use heartbeat to trigger periodic checks
# Run this command to test: python3 {skill_path}/scripts/memory.py autocheck
"""
    
    def _cmd_setup_all(self) -> str:
        """Generate one-shot setup command for all cron jobs"""
        skill_path = str(SKILL_DIR)
        ws_path = str(SKILL_DIR.parent)
        
        return f"""# ========================================================
# HIPPOCAMUS One-Click Auto Setup
# ========================================================
# One-time setup - all cron jobs will be created
# Just say "yes" or "confirm" and I will execute immediately
# ========================================================

## Tasks to be created：

### 1. Auto-save (every 6 hours)
- Name: hippocampus-autosave
- Schedule: 0 */6 * * *
- Execute: python3 {skill_path}/scripts/memory.py autocheck

### 2. Daily memory file creation (midnight)
- Name: hippocampus-daily-create
- Schedule: 0 0 * * *
- Execute: create ~/.openclaw/workspace/memory/heartbeat-YYYY-MM-DD-HHMM.md

### 3. Daily analysis (23:00)
- Name: hippocampus-analyze
- Schedule: 0 23 * * *
- Execute: python3 {skill_path}/scripts/memory.py analyze

---

**Please reply "yes" or "confirm" to create all tasks**

---

## Or customize:

- Want to change time? Tell me hours (e.g. every 3 hours)
- Want only some tasks? Tell me which ones
"""
    
    def _cmd_setup_hooks(self) -> str:
        """Generate hook setup with user confirmation"""
        return """# ========================================================
# HOOK Auto-Setup Guide
# ========================================================

## Hooks to configure:

### 1. session_end Hook (Auto-save when session ends)
- Trigger: user ends session
- Action: save current memory to Chronicle
- Requires: read session content

### 2. session_start Hook (Load memory when session starts)
- Trigger: user starts new session
- Action: load BEFORE_ANSWER memory
- Requires: write to context

---

## OpenClaw Hook Configuration:

Due to security, OpenClaw requires explicit user consent to configure hooks.

**I will execute as follows:**
1. Detected hippocampus needs hook configuration
2. Explicitly ask user: "Do you consent to configure auto-save hooks?"
3. After user says "yes", auto-execute hook configuration

---

**Please reply "yes" or "confirm" to configure hooks**

---

## Or manually configure:

Add to OpenClaw config:
```json
"hooks": {{
  "session_end": [
    {{"skill": "hippocampus", "command": "autocheck"}}
  ]
}}
```
"""
    
    def _cmd_sync_memory(self) -> str:
        """Sync important memory to MEMORY.md with user confirmation"""
        # Get recent monographs as summary
        recent = list_monographs()[:5]
        
        if not recent:
            return "No monograph topics found. Create some topics first with /hip new <name>"
        
        summary = "## Hippocampus Recent Updates\n\n"
        for m in recent:
            summary += f"- **{m['topic']}**: {m['content_preview'][:100]}...\n"
        
        return f"""# ========================================================
# Sync to Main Memory
# ========================================================

## Detected important updates：

{summary}

---

## Will write to MEMORY.md "## Recent Updates" section

Content preview:：
```
{summary}
```

---

**Please reply "yes" or "confirm" to sync to MEMORY.md**

---

## Or:

- Tell me to view full content
- Tell me topic name to sync specific one
- Tell me "cancel" to cancel
"""
    
    def _cmd_do_setup(self, args: str = "") -> str:
        """Generate cron commands for user/agent to execute after confirmation"""
        skill_path = str(SKILL_DIR)
        ws_path = str(SKILL_DIR.parent)
        
        # Commands to create cron jobs - these should be executed by the agent
        return f"""# Execute these cron job creations:

## 1. Auto-save (every 6 hours)
```
cron add --name "hippocampus-autosave" --schedule "0 */6 * * *" --session-target isolated --payload "Run: python3 {skill_path}/scripts/memory.py autocheck" --delivery-mode none
```

## 2. Daily-create (midnight)
```
cron add --name "hippocampus-daily-create" --schedule "0 0 * * *" --session-target isolated --payload "Run: echo \\"$(date +%Y-%m-%d)\\"" --delivery-mode none
```

## 3. Daily-analyze (23:00)
```
cron add --name "hippocampus-analyze" --schedule "0 23 * * *" --session-target isolated --payload "Run: python3 {skill_path}/scripts/memory.py analyze" --delivery-mode none
```

---

✅ Say "done" when completed, or I will verify with `cron list`
"""
    
    def _cmd_do_setup_hooks(self, args: str = "") -> str:
        """Execute hook configuration after user confirmation"""
        # Note: OpenClaw hooks require manual configuration in openclaw.json
        # This method generates the commands the user needs to run
        config_path = "~/.openclaw/openclaw.json"
        
        return f"""# Hook Configuration

## Required Configuration

To enable automatic memory save on session end, add this to your `{config_path}`:

```json
{{
  "hooks": {{
    "session_end": [
      {{"skill": "hippocampus", "command": "autocheck"}}
    ]
  }}
}}
```

## Alternative: Using Gateway Config

Or configure via Gateway:

```
gateway config patch --path "hooks.session_end" --value '[{{"skill":"hippocampus","command":"autocheck"}}]'
```

---

**Note**: Hook configuration requires Gateway restart to take effect.
"""
    
    def _cmd_do_sync_memory(self, args: str = "") -> str:
        """Execute memory sync after user confirmation"""
        from pathlib import Path
        
        # Get memory file path
        ws_path = SKILL_DIR.parent
        memory_file = ws_path / "MEMORY.md"
        
        if not memory_file.exists():
            return "❌ MEMORY.md not found. Please check workspace path."
        
        # Get recent monographs
        recent = list_monographs()[:5]
        
        if not recent:
            return "No monograph topics to sync."
        
        # Build update section
        update_section = f"## Hippocampus Updates - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        for m in recent:
            update_section += f"- **{m['topic']}**: {m['content_preview'][:100]}...\n"
        
        try:
            # Read existing content
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if update section exists
            if "## Hippocampus Updates" in content:
                # Find and replace
                import re
                pattern = r"## Hippocampus Updates.*?(?=\n## |\Z)"
                content = re.sub(pattern, update_section.strip(), content, flags=re.DOTALL)
            else:
                # Append at end
                content += f"\n\n{update_section}"
            
            # Write back
            with open(memory_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"""# Memory Sync Complete ✅

Synced {len(recent)} topics to MEMORY.md:

{update_section}

---
"""
        except Exception as e:
            return f"❌ Sync failed: {str(e)}"
    
    def _help(self) -> str:
        config = get_config()
        return f"""## Hippocampus Commands

| Command | Description |
|---------|-------------|
| `/hippo init` | Initialize DB and directories |
| `/hippo new <topic>` | Create new monograph |
| `/hippo save` | Save current context |
| `/hippo recall <keyword>` | Precise recall |
| `/hippo checkpoint` | Save project state |
| `/hippo warn` | Check failure patterns |
| `/hippo graph` | View knowledge graph |
| `/hippo learn-workflow <micro> -> <macro>` | Register a workflow |
| `/hippo workflows` | List all workflows |
| `/hippo forget-workflow <micro>` | Remove a workflow |
| `/hippo triggers` | List proactive triggers |
| `/hippo add-trigger <kw> -> <topic>` | Add a trigger |
| `/hippo remove-trigger <keyword>` | Remove a trigger |
| `/hippo status` | View memory status |
| `/hippo config` | Show configuration |
| `/hippo analyze` | Analyze all memory |

**Auto-triggers** (from USER_CONFIG.md):
- {config.get('TIME_HOURS', 6)} hours
- {config.get('ROUND_THRESHOLD', 25)} rounds
- {config.get('TOKEN_THRESHOLD', 10000)} tokens

**Micro-Macro**: {config.get('MICRO_MACRO_ENABLED', True)}
**Proactive Triggers**: {config.get('PROACTIVE_TRIGGERS_ENABLED', True)}

Configure in USER_CONFIG.md.
"""

# ============================================================================
# Entry Point
# ============================================================================

def handle(command: str, args: str = "", context: Dict = None) -> str:
    """Entry function for OpenClaw"""
    hippocampus = Hippocampus()
    return hippocampus.process(command, args, context)


def proactive_check(message: str) -> str:
    """
    Check if user message matches any proactive trigger.
    Call this BEFORE each response to auto-load relevant memory.
    Returns the loaded memory content, or empty string if no match.
    """
    return get_proactive_memory(message)


def match_workflow_check(message: str) -> Optional[Dict]:
    """
    Check if user message matches any registered micro-macro workflow.
    Call this to retrieve workflow before executing.
    Returns the workflow dict, or None if no match.
    """
    return match_workflow(message)


if __name__ == "__main__":
    import sys
    h = Hippocampus()
    if len(sys.argv) > 1:
        print(h.process(sys.argv[1], " ".join(sys.argv[2:])))
    else:
        print(h._help())
