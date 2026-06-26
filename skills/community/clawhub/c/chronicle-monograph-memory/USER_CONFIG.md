# User Configuration for Hippocampus
#
# IMPORTANT: Edit this file to customize your memory behavior
# After editing, the skill will automatically reload these values
# Format: KEY = VALUE (one per line, no quotes needed)

# ============================================
# Trigger Settings
# ============================================

ROUND_THRESHOLD = 25
TIME_HOURS = 6
TOKEN_THRESHOLD = 10000

# ============================================
# Storage Settings
# ============================================

BASE_PATH = ./assets/hippocampus
CHRONICLE_DIR = chronicle
MONOGRAPH_DIR = monograph
INDEX_DIR = index
WORKFLOW_DIR = workflows

# ============================================
# File Organization
# ============================================

FILE_ORG_ENABLED = true
FILE_ORG_AUTO_MOVE = false
FILE_SCAN_PATHS = ./workspace
FILE_EXCLUDE_PATHS = .openclaw,node_modules,.git

# ============================================
# Keyword & Association
# ============================================

KEYWORD_COUNT = 20
ASSOCIATION_DEPTH = 3

# ============================================
# Auto-Save
# ============================================

AUTO_SAVE = true

# ============================================
# Micro-Macro Workflow Memory
# ============================================
# When user says a micro (short command), hippocampus retrieves
# the corresponding macro (full workflow) automatically.
MICRO_MACRO_ENABLED = true

# ============================================
# Proactive Keyword Triggers
# ============================================
# When user message contains these keywords, hippocampus
# proactively loads the associated memory before answering.
# Format: KEYWORD->TOPIC (comma-separated, case-insensitive)
# TOPIC = monograph file name (without .md)
PROACTIVE_TRIGGERS_ENABLED = true
PROACTIVE_KEYWORDS = project->default-project,database->database-architecture,api->api-design,error->error-patterns

# ============================================
# 察言观色 — ReadingBetweenTheLines
# ============================================
# Proactive memory loading based on sustained conversation patterns.
# Runs on heartbeat to analyze recent messages and load relevant memories.

READINGBETWEENTHELINES_ENABLED = true

# Heartbeat interval (minutes) — how often to check
HEARTBEAT_INTERVAL = 1

# Sliding window (minutes) — how far back to analyze
SLIDING_WINDOW = 10

# Instant triggers: KEYWORD->MONOGRAPH_TOPIC (fires immediately)
INSTANT_TRIGGERS = error->error-patterns,database->database-architecture,api->api-design,deploy->deployment-checklist,test->test-strategy

# Threshold triggers: KEYWORD->OCCURRENCE_COUNT (fires after N occurrences)
THRESHOLD_TRIGGERS = project->5,api->4,config->4,feature->4,data->3

# Cooldown (minutes) — minimum time before reloading the same memory
TRIGGER_COOLDOWN = 5
