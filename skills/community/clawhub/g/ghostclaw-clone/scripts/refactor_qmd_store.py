#!/usr/bin/env python3
"""
Refactor qmd_store.py:
- Remove inner extract_searchable_text function from _ensure_fts
- Add _register_searchable_function helper after _ensure_fts
- Add import of the module-level function at top
"""

import sys
from pathlib import Path

file_path = Path("src/ghostclaw/core/qmd_store.py")
content = file_path.read_text()
lines = content.splitlines(keepends=True)

# Ensure the module-level function exists at top (after logger)
# We'll insert it after the logger definition line.
logger_line_idx = None
for i, line in enumerate(lines):
    if line.strip() == 'logger = logging.getLogger("ghostclaw.qmd")':
        logger_line_idx = i
        break

if logger_line_idx is None:
    print("Could not find logger line", file=sys.stderr)
    sys.exit(1)

# Check if function already exists
if "_extract_searchable_text_impl" not in content:
    # Insert function definition after logger line
    func_code = '''

def _extract_searchable_text_impl(report_json_str: str) -> str:
    """Pure Python function to extract searchable text from a JSON report string."""
    try:
        report = json.loads(report_json_str)
    except (json.JSONDecodeError, TypeError):
        return ""
    parts = []
    # Issues
    for issue in report.get("issues", []):
        if isinstance(issue, dict):
            parts.append(issue.get("message", ""))
            if issue.get("file"):
                parts.append(f"file:{issue['file']}")
        else:
            parts.append(str(issue))
    # Architectural ghosts
    for ghost in report.get("architectural_ghosts", []):
        if isinstance(ghost, dict):
            parts.append(ghost.get("message", ""))
        else:
            parts.append(str(ghost))
    # Red flags
    for flag in report.get("red_flags", []):
        if isinstance(flag, dict):
            parts.append(flag.get("message", ""))
        else:
            parts.append(str(flag))
    # AI synthesis and reasoning
    for field in ("ai_synthesis", "ai_reasoning"):
        if report.get(field):
            parts.append(str(report[field]))
    return " ".join(parts)
'''
    lines.insert(logger_line_idx + 1, func_code)
    print("Inserted _extract_searchable_text_impl function")

# Now find _ensure_fts method and replace its body
# Find start: "    async def _ensure_fts(self) -> None:"
start_idx = None
for i, line in enumerate(lines):
    if line.strip() == "async def _ensure_fts(self) -> None:":
        start_idx = i
        break
if start_idx is None:
    print("Could not find _ensure_fts definition", file=sys.stderr)
    sys.exit(1)

# Find the end of _ensure_fts: look for the next line that is a method definition or comment block at same indentation level
# Methods are indented with 4 spaces. The method body is indented 8 spaces.
# We'll find the next line at indentation <=4 that is not blank and is after the method.
end_idx = None
for i in range(start_idx + 1, len(lines)):
    stripped = lines[i].strip()
    if not stripped:
        continue
    # Check if this line is at class level indentation (4 spaces) or less (could be comment)
    indent = len(lines[i]) - len(lines[i].lstrip())
    if indent <= 4:
        end_idx = i
        break
if end_idx is None:
    end_idx = len(lines) - 1

print(f"Replacing _ensure_fts from line {start_idx+1} to {end_idx}")

# Build new _ensure_fts body (without inner function)
new_body = '''    async def _ensure_fts(self) -> None:
        """Create FTS5 virtual table for BM25 search if not exists."""
        if self._fts_initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Check if FTS table exists
            async with db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='reports_fts'"
            ) as cursor:
                exists = await cursor.fetchone()

            if not exists:
                # Create FTS5 virtual table with content column
                await db.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS reports_fts
                    USING fts5(
                        report_id UNINDEXED,
                        content,
                        tokenize = 'porter'
                    )
                """)
                # Populate FTS from existing reports
                await db.execute("""
                    INSERT INTO reports_fts(report_id, content)
                    SELECT id, extract_searchable_text(report_json)
                    FROM reports
                """)
                # Create triggers for future inserts/updates
                await db.executescript("""
                    CREATE TRIGGER reports_ai AFTER INSERT ON reports BEGIN
                        INSERT INTO reports_fts(report_id, content)
                        VALUES (new.id, extract_searchable_text(new.report_json));
                    END;

                    CREATE TRIGGER reports_ad AFTER DELETE ON reports BEGIN
                        DELETE FROM reports_fts WHERE report_id = old.id;
                    END;

                    CREATE TRIGGER reports_au AFTER UPDATE ON reports BEGIN
                        UPDATE reports_fts SET content = extract_searchable_text(new.report_json)
                        WHERE report_id = new.id;
                    END;
                """)
                logger.info("Created FTS5 table and triggers")
            self._fts_initialized = True

    async def _register_searchable_function(self, db) -> None:
        """Register the extract_searchable_text function on the given connection."""
        await db.create_function("extract_searchable_text", 1, _extract_searchable_text_impl)

'''
# Note: new_body ends with a newline. We'll replace the entire method block including the blank line after it?
# We'll replace lines from start_idx to end_idx (exclusive?) with new_body.
# Actually we want to replace from start_idx through end_idx-1? Because end_idx points to the next non-blank class-level line (like the comment "List runs"). We want to keep that line. So we replace [start_idx, end_idx) with new_body.

lines[start_idx:end_idx] = [new_body]

# Write back
file_path.write_text(''.join(lines))
print("Refactored qmd_store.py successfully")
