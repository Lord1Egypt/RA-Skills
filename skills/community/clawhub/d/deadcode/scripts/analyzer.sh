#!/usr/bin/env bash
# DeadCode -- Core Analysis Engine
# Provides: language detection, file discovery, pattern scanning, risk scoring,
#           orphan detection, report generation, SARIF output, and hook integration.
#
# This file is sourced by deadcode.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# --- Colors (safe to re-declare; sourcing scripts may set these) --------------

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
SKILL_DIR="${SKILL_DIR:-$(dirname "$SCRIPT_DIR")}"
DEADCODE_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

# ============================================================================
# Language Detection
# ============================================================================

# Detect the language/category for a given file.
# Outputs one of: js, py, go, css, unknown
detect_lang_type() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')
  local ext="${basename_lower##*.}"

  # JavaScript / TypeScript
  case "$ext" in
    js|jsx|ts|tsx|mjs|cjs|mts|cts)
      echo "js"
      return 0
      ;;
  esac

  # Python
  case "$ext" in
    py|pyw|pyi)
      echo "py"
      return 0
      ;;
  esac

  # Go
  if [[ "$ext" == "go" ]]; then
    echo "go"
    return 0
  fi

  # CSS / SCSS / SASS / LESS
  case "$ext" in
    css|scss|sass|less)
      echo "css"
      return 0
      ;;
  esac

  echo "unknown"
}

# ============================================================================
# Find Source Files
# ============================================================================

# Find all source files in a directory tree
find_source_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  if [[ -f "$search_dir" ]]; then
    local ltype
    ltype=$(detect_lang_type "$search_dir")
    if [[ "$ltype" != "unknown" ]]; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  # JavaScript / TypeScript files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 8 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".next" -o -name "dist" -o -name "build" -o -name "coverage" -o -name "__pycache__" -o -name ".venv" -o -name "venv" \) -prune -o \
    \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.mjs" -o -name "*.cjs" \) \
    -type f -print0 2>/dev/null)

  # Python files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 8 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name "__pycache__" -o -name ".venv" -o -name "venv" -o -name ".tox" -o -name ".eggs" \) -prune -o \
    \( -name "*.py" -o -name "*.pyw" \) \
    -type f -print0 2>/dev/null)

  # Go files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 8 \
    \( -name ".git" -o -name "vendor" -o -name "node_modules" \) -prune -o \
    -name "*.go" \
    -type f -print0 2>/dev/null)

  # CSS / SCSS / LESS files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 8 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name "dist" -o -name "build" \) -prune -o \
    \( -name "*.css" -o -name "*.scss" -o -name "*.sass" -o -name "*.less" \) \
    -type f -print0 2>/dev/null)
}

# ============================================================================
# Scan File With Patterns
# ============================================================================

# Scan a single file against its language's patterns.
# Appends findings to global FINDINGS array.
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
scan_file_with_patterns() {
  local filepath="$1"
  local lang_type="$2"

  # First apply language-specific patterns
  local patterns_name
  patterns_name=$(get_patterns_for_lang "$lang_type")

  if [[ -n "$patterns_name" ]]; then
    local -n _patterns_ref="$patterns_name"

    for entry in "${_patterns_ref[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

      # Skip placeholder patterns (handled by file-level checks)
      [[ "$regex" == PLACEHOLDER_* ]] && continue

      # Use grep -nE to find matches with line numbers
      local matches
      matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local matched_text="${match_line#*:}"
          # Trim whitespace
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
          # Truncate long lines
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi
          FINDINGS+=("${filepath}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}")
        done <<< "$matches"
      fi
    done
  fi

  # Also apply general patterns to all files
  for entry in "${DEADCODE_GENERAL_PATTERNS[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

    # Skip placeholder patterns
    [[ "$regex" == PLACEHOLDER_* ]] && continue

    local matches
    matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

    if [[ -n "$matches" ]]; then
      while IFS= read -r match_line; do
        [[ -z "$match_line" ]] && continue
        local line_num="${match_line%%:*}"
        local matched_text="${match_line#*:}"
        matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        if [[ ${#matched_text} -gt 120 ]]; then
          matched_text="${matched_text:0:117}..."
        fi
        FINDINGS+=("${filepath}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}")
      done <<< "$matches"
    fi
  done

  # Run file-level checks based on language type
  run_file_level_checks "$filepath" "$lang_type"
}

# ============================================================================
# File-Level Checks
# ============================================================================

# These checks look at the file as a whole (absence of references, structural issues, etc.)
run_file_level_checks() {
  local filepath="$1"
  local lang_type="$2"

  # Common cross-language checks
  check_large_comment_blocks "$filepath" "$lang_type"
  check_todo_density "$filepath" "$lang_type"

  case "$lang_type" in
    js)
      check_js_file_level "$filepath"
      ;;
    py)
      check_py_file_level "$filepath"
      ;;
    go)
      check_go_file_level "$filepath"
      ;;
    css)
      check_css_file_level "$filepath"
      ;;
  esac
}

# --- Large comment block detection (cross-language) ---

check_large_comment_blocks() {
  local filepath="$1"
  local lang_type="$2"
  local comment_prefix

  case "$lang_type" in
    js|go)   comment_prefix="//" ;;
    py)      comment_prefix="#" ;;
    css)     comment_prefix="/\*" ;;  # Handled differently for CSS
    *)       return ;;
  esac

  if [[ "$lang_type" == "css" ]]; then
    # For CSS, count lines inside /* */ blocks
    local block_comment_lines
    block_comment_lines=$(awk '
      /\/\*/ { in_comment=1 }
      in_comment { count++ }
      /\*\// { if (count >= 5) { print count; count=0 }; in_comment=0 }
    ' "$filepath" 2>/dev/null | head -1)

    if [[ -n "$block_comment_lines" && "$block_comment_lines" -ge 5 ]]; then
      FINDINGS+=("${filepath}|1|low|DC-CSS-005|Large block of commented-out CSS (${block_comment_lines} lines)|Remove the commented-out block|${block_comment_lines} consecutive comment lines")
    fi
    return
  fi

  # For JS/Go/Python, count consecutive single-line comments
  local max_consecutive=0
  local current_run=0
  local run_start_line=0

  while IFS= read -r line; do
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//')
    if echo "$trimmed" | grep -qE "^${comment_prefix}" 2>/dev/null; then
      current_run=$((current_run + 1))
      if [[ $current_run -eq 1 ]]; then
        run_start_line=$(grep -n "^.*$" "$filepath" 2>/dev/null | grep -c "" || echo "1")
      fi
      if [[ $current_run -gt $max_consecutive ]]; then
        max_consecutive=$current_run
      fi
    else
      current_run=0
    fi
  done < "$filepath"

  if [[ $max_consecutive -ge 10 ]]; then
    local check_id
    case "$lang_type" in
      js) check_id="DC-JS-008" ;;
      py) check_id="DC-PY-006" ;;
      go) check_id="DC-GO-007" ;;
      *)  check_id="DC-GEN-002" ;;
    esac
    FINDINGS+=("${filepath}|1|medium|${check_id}|Large block of commented-out code (${max_consecutive} consecutive lines)|Remove the commented-out block; use git history to recover|${max_consecutive} consecutive comment lines")
  fi
}

# --- TODO/FIXME/HACK density check ---

check_todo_density() {
  local filepath="$1"
  local lang_type="$2"

  local todo_count
  todo_count=$(grep -ciE "(TODO|FIXME|HACK|XXX|TEMP)[[:space:]:]" "$filepath" 2>/dev/null || echo "0")

  if [[ "$todo_count" -gt 5 ]]; then
    FINDINGS+=("${filepath}|1|medium|DC-GEN-003|More than 5 TODO/FIXME/HACK comments in this file (found ${todo_count})|Resolve TODOs or convert them to tracked issues|${todo_count} TODO/FIXME/HACK comments")
  fi
}

# ============================================================================
# JavaScript/TypeScript File-Level Checks
# ============================================================================

check_js_file_level() {
  local filepath="$1"

  # Check for empty function bodies in multi-line format
  check_js_empty_functions "$filepath"

  # Check for unused variables (simple heuristic)
  check_js_unused_vars "$filepath"

  # Check for unreachable code after return/throw
  check_js_unreachable_code "$filepath"
}

check_js_empty_functions() {
  local filepath="$1"

  # Look for function declarations followed by empty body
  # Pattern: function name(...) { } across potentially multiple lines
  local line_num=0
  local in_func_decl=false
  local func_line=0
  local brace_count=0

  while IFS= read -r line; do
    line_num=$((line_num + 1))
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//')

    # Detect function declaration opening
    if echo "$trimmed" | grep -qE "^(export[[:space:]]+)?(async[[:space:]]+)?function[[:space:]]+[a-zA-Z_].*\{[[:space:]]*$" 2>/dev/null; then
      in_func_decl=true
      func_line=$line_num
      brace_count=1
      continue
    fi

    if [[ "$in_func_decl" == true ]]; then
      # Check if next non-empty line is just a closing brace
      if [[ -n "$trimmed" ]]; then
        if [[ "$trimmed" == "}" ]]; then
          FINDINGS+=("${filepath}|${func_line}|medium|DC-JS-014|Empty function body (no-op)|Implement the function or remove it if unused|Empty function at line $func_line")
        fi
        in_func_decl=false
      fi
    fi
  done < "$filepath"
}

check_js_unused_vars() {
  local filepath="$1"

  # Simple heuristic: find const/let/var declarations and check if the name
  # appears more than once in the file. This is approximate but useful.
  local var_declarations
  var_declarations=$(grep -nE "^[[:space:]]*(const|let|var)[[:space:]]+([a-zA-Z_$][a-zA-Z0-9_$]*)[[:space:]]*=" "$filepath" 2>/dev/null || true)

  if [[ -z "$var_declarations" ]]; then
    return
  fi

  while IFS= read -r decl_line; do
    [[ -z "$decl_line" ]] && continue
    local line_num="${decl_line%%:*}"
    local rest="${decl_line#*:}"

    # Extract variable name
    local var_name
    var_name=$(echo "$rest" | sed -n 's/^[[:space:]]*\(const\|let\|var\)[[:space:]]\+\([a-zA-Z_$][a-zA-Z0-9_$]*\).*/\2/p')

    if [[ -z "$var_name" || ${#var_name} -le 1 ]]; then
      continue
    fi

    # Skip common patterns (destructuring results in short names, _ prefix is intentional)
    if [[ "$var_name" == _* ]]; then
      continue
    fi

    # Count occurrences of the variable name in the file
    local occurrence_count
    occurrence_count=$(grep -c "[^a-zA-Z0-9_$]${var_name}[^a-zA-Z0-9_$]" "$filepath" 2>/dev/null || echo "0")
    # Also count if var is at start/end of file
    local occurrence_count2
    occurrence_count2=$(grep -c "^${var_name}[^a-zA-Z0-9_$]" "$filepath" 2>/dev/null || echo "0")
    local occurrence_count3
    occurrence_count3=$(grep -c "[^a-zA-Z0-9_$]${var_name}$" "$filepath" 2>/dev/null || echo "0")

    local total_occ=$((occurrence_count + occurrence_count2 + occurrence_count3))

    # If it only appears once (the declaration), it is unused
    if [[ $total_occ -le 1 ]]; then
      FINDINGS+=("${filepath}|${line_num}|high|DC-JS-016|Variable '${var_name}' declared but never referenced|Remove the unused variable declaration|${var_name} appears only in its declaration")
    fi
  done <<< "$var_declarations"
}

check_js_unreachable_code() {
  local filepath="$1"

  local line_num=0
  local prev_was_return=false
  local prev_line_num=0
  local brace_depth=0

  while IFS= read -r line; do
    line_num=$((line_num + 1))
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

    # Track brace depth to know if return is at block level
    local open_braces
    open_braces=$(echo "$trimmed" | tr -cd '{' | wc -c)
    local close_braces
    close_braces=$(echo "$trimmed" | tr -cd '}' | wc -c)
    brace_depth=$((brace_depth + open_braces - close_braces))

    # Skip empty lines and comments
    if [[ -z "$trimmed" || "$trimmed" == //* || "$trimmed" == \** || "$trimmed" == \#* ]]; then
      continue
    fi

    # If previous statement was a return/throw and this line is not a closing brace
    # or another control structure, it is likely unreachable
    if [[ "$prev_was_return" == true ]]; then
      if [[ "$trimmed" != "}" && "$trimmed" != "case "* && "$trimmed" != "default:"* && "$trimmed" != "else"* && "$trimmed" != "catch"* && "$trimmed" != "finally"* ]]; then
        FINDINGS+=("${filepath}|${line_num}|high|DC-JS-012|Code after unconditional return/throw is unreachable|Remove unreachable statement at line ${line_num}|${trimmed}")
        prev_was_return=false
        continue
      fi
      prev_was_return=false
    fi

    # Detect unconditional return/throw (not inside an if or ternary)
    if echo "$trimmed" | grep -qE "^return[[:space:]]|^return;|^throw[[:space:]]" 2>/dev/null; then
      prev_was_return=true
      prev_line_num=$line_num
    fi
  done < "$filepath"
}

# ============================================================================
# Python File-Level Checks
# ============================================================================

check_py_file_level() {
  local filepath="$1"

  check_py_pass_only_bodies "$filepath"
  check_py_unused_imports "$filepath"
  check_py_unreachable_code "$filepath"
  check_py_empty_except "$filepath"
  check_py_duplicate_functions "$filepath"
}

check_py_pass_only_bodies() {
  local filepath="$1"

  # Look for def/class followed by pass on the next non-empty, non-comment line
  local line_num=0
  local in_def=false
  local def_line=0
  local saw_docstring=false

  while IFS= read -r line; do
    line_num=$((line_num + 1))
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//')

    if echo "$trimmed" | grep -qE "^(def|class)[[:space:]]+" 2>/dev/null; then
      in_def=true
      def_line=$line_num
      saw_docstring=false
      continue
    fi

    if [[ "$in_def" == true ]]; then
      # Skip empty lines
      [[ -z "$trimmed" ]] && continue
      # Skip docstrings
      if echo "$trimmed" | grep -qE "^(\"\"\"|\x27\x27\x27)" 2>/dev/null; then
        saw_docstring=true
        # If single-line docstring, keep going
        if echo "$trimmed" | grep -qE "(\"\"\".*\"\"\"|'''.*''')" 2>/dev/null; then
          continue
        fi
        # Multi-line docstring -- skip until closing
        while IFS= read -r line; do
          line_num=$((line_num + 1))
          if echo "$line" | grep -qE "(\"\"\"|\x27\x27\x27)" 2>/dev/null; then
            break
          fi
        done
        continue
      fi
      # Skip comments
      if [[ "$trimmed" == \#* ]]; then
        continue
      fi
      # Check if it is pass
      if [[ "$trimmed" == "pass" ]]; then
        FINDINGS+=("${filepath}|${def_line}|medium|DC-PY-004|Function or class body contains only pass (placeholder)|Implement the body or remove the placeholder definition|pass-only body at line $def_line")
      fi
      in_def=false
    fi
  done < "$filepath"
}

check_py_unused_imports() {
  local filepath="$1"

  # Extract import names and check if they appear elsewhere in the file
  local imports
  imports=$(grep -nE "^(import[[:space:]]+[a-zA-Z_]|from[[:space:]]+[a-zA-Z_].*import[[:space:]]+)" "$filepath" 2>/dev/null || true)

  if [[ -z "$imports" ]]; then
    return
  fi

  while IFS= read -r import_line; do
    [[ -z "$import_line" ]] && continue
    local line_num="${import_line%%:*}"
    local rest="${import_line#*:}"

    # Extract imported name(s)
    local import_name=""

    # Handle "import foo" style
    if echo "$rest" | grep -qE "^import[[:space:]]+[a-zA-Z_][a-zA-Z0-9_.]*[[:space:]]*$" 2>/dev/null; then
      import_name=$(echo "$rest" | sed -n 's/^import[[:space:]]\+\([a-zA-Z_][a-zA-Z0-9_.]*\).*/\1/p')
      # Get the last component for dotted imports
      import_name="${import_name##*.}"
    fi

    # Handle "import foo as bar" style
    if echo "$rest" | grep -qE "^import[[:space:]].*[[:space:]]as[[:space:]]" 2>/dev/null; then
      import_name=$(echo "$rest" | sed -n 's/.*[[:space:]]as[[:space:]]\+\([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/p')
    fi

    # Handle "from foo import bar" style
    if echo "$rest" | grep -qE "^from[[:space:]].*import[[:space:]]" 2>/dev/null; then
      local import_part
      import_part=$(echo "$rest" | sed -n 's/.*import[[:space:]]\+\(.*\)/\1/p')
      # Take the first imported name (before any comma)
      import_name=$(echo "$import_part" | sed 's/,.*//' | sed 's/[[:space:]]//g')
      # Handle "as" aliases
      if echo "$import_name" | grep -qE "[[:space:]]as[[:space:]]" 2>/dev/null; then
        import_name=$(echo "$import_name" | sed 's/.*as[[:space:]]*//')
      fi
    fi

    if [[ -z "$import_name" || ${#import_name} -le 1 || "$import_name" == "*" ]]; then
      continue
    fi

    # Skip __future__ imports and typing imports (commonly used for annotations only)
    if echo "$rest" | grep -qE "from[[:space:]]+__future__|from[[:space:]]+typing" 2>/dev/null; then
      continue
    fi

    # Count occurrences outside the import line itself
    local usage_count
    usage_count=$(grep -c "$import_name" "$filepath" 2>/dev/null || echo "0")

    if [[ "$usage_count" -le 1 ]]; then
      FINDINGS+=("${filepath}|${line_num}|high|DC-PY-002|Import '${import_name}' is never used in the file|Remove the unused import|${import_name} appears only in its import statement")
    fi
  done <<< "$imports"
}

check_py_unreachable_code() {
  local filepath="$1"

  local line_num=0
  local prev_was_return=false
  local indent_level=0

  while IFS= read -r line; do
    line_num=$((line_num + 1))
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//')

    # Skip empty lines and comments
    if [[ -z "$trimmed" || "$trimmed" == \#* ]]; then
      continue
    fi

    # Calculate indent level
    local leading_spaces
    leading_spaces=$(echo "$line" | sed 's/[^ ].*//' | wc -c)
    leading_spaces=$((leading_spaces - 1))

    if [[ "$prev_was_return" == true ]]; then
      # If same or deeper indentation and not a new function/class/decorator
      if [[ $leading_spaces -ge $indent_level ]]; then
        if [[ "$trimmed" != "def "* && "$trimmed" != "class "* && "$trimmed" != "@"* && "$trimmed" != "elif "* && "$trimmed" != "else:"* && "$trimmed" != "except"* && "$trimmed" != "finally:"* ]]; then
          FINDINGS+=("${filepath}|${line_num}|high|DC-PY-007|Code after unconditional return/raise/break is unreachable|Remove unreachable statement at line ${line_num}|${trimmed}")
          prev_was_return=false
          continue
        fi
      fi
      prev_was_return=false
    fi

    if echo "$trimmed" | grep -qE "^(return[[:space:]]|return$|raise[[:space:]]|break$|continue$)" 2>/dev/null; then
      prev_was_return=true
      indent_level=$leading_spaces
    fi
  done < "$filepath"
}

check_py_empty_except() {
  local filepath="$1"

  local line_num=0
  local in_except=false
  local except_line=0

  while IFS= read -r line; do
    line_num=$((line_num + 1))
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//')

    if echo "$trimmed" | grep -qE "^except[[:space:]]*:" 2>/dev/null || echo "$trimmed" | grep -qE "^except[[:space:]]+[A-Za-z].*:" 2>/dev/null; then
      in_except=true
      except_line=$line_num
      continue
    fi

    if [[ "$in_except" == true ]]; then
      [[ -z "$trimmed" ]] && continue
      if [[ "$trimmed" == "pass" ]]; then
        FINDINGS+=("${filepath}|${except_line}|medium|DC-PY-011|Empty except block -- exceptions silently swallowed|Add error handling, logging, or re-raise the exception|except: pass at line $except_line")
      fi
      in_except=false
    fi
  done < "$filepath"
}

check_py_duplicate_functions() {
  local filepath="$1"

  # Find function names that appear more than once
  local func_names
  func_names=$(grep -oE "^def[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*" "$filepath" 2>/dev/null | sed 's/^def[[:space:]]*//' | sort | uniq -d)

  if [[ -n "$func_names" ]]; then
    while IFS= read -r func_name; do
      [[ -z "$func_name" ]] && continue
      local first_line
      first_line=$(grep -n "^def[[:space:]]\+${func_name}[[:space:]]*(" "$filepath" 2>/dev/null | head -1 | cut -d: -f1)
      if [[ -n "$first_line" ]]; then
        FINDINGS+=("${filepath}|${first_line}|high|DC-PY-014|Function '${func_name}' defined multiple times -- earlier definition is dead|Remove the duplicate function definition|${func_name} is defined more than once")
      fi
    done <<< "$func_names"
  fi
}

# ============================================================================
# Go File-Level Checks
# ============================================================================

check_go_file_level() {
  local filepath="$1"

  check_go_unreachable_code "$filepath"
  check_go_empty_init "$filepath"
}

check_go_unreachable_code() {
  local filepath="$1"

  local line_num=0
  local prev_was_return=false
  local brace_depth=0

  while IFS= read -r line; do
    line_num=$((line_num + 1))
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

    local open_braces
    open_braces=$(echo "$trimmed" | tr -cd '{' | wc -c)
    local close_braces
    close_braces=$(echo "$trimmed" | tr -cd '}' | wc -c)
    brace_depth=$((brace_depth + open_braces - close_braces))

    [[ -z "$trimmed" || "$trimmed" == //* ]] && continue

    if [[ "$prev_was_return" == true ]]; then
      if [[ "$trimmed" != "}" && "$trimmed" != "case "* && "$trimmed" != "default:"* ]]; then
        FINDINGS+=("${filepath}|${line_num}|high|DC-GO-003|Code after unconditional return/panic is unreachable|Remove unreachable statement at line ${line_num}|${trimmed}")
        prev_was_return=false
        continue
      fi
      prev_was_return=false
    fi

    if echo "$trimmed" | grep -qE "^return[[:space:]]|^return$|^panic[[:space:]]*\(" 2>/dev/null; then
      prev_was_return=true
    fi
  done < "$filepath"
}

check_go_empty_init() {
  local filepath="$1"

  # Check if init() has only comments in its body
  local in_init=false
  local init_line=0
  local brace_count=0
  local has_code=false
  local line_num=0

  while IFS= read -r line; do
    line_num=$((line_num + 1))
    local trimmed
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//')

    if echo "$trimmed" | grep -qE "^func[[:space:]]+init[[:space:]]*\(\)[[:space:]]*\{" 2>/dev/null; then
      in_init=true
      init_line=$line_num
      brace_count=1
      has_code=false
      # Check if it is single-line empty
      if echo "$trimmed" | grep -qE "\{[[:space:]]*\}$" 2>/dev/null; then
        # Already handled by pattern DC-GO-008
        in_init=false
      fi
      continue
    fi

    if [[ "$in_init" == true ]]; then
      local open_braces
      open_braces=$(echo "$trimmed" | tr -cd '{' | wc -c)
      local close_braces
      close_braces=$(echo "$trimmed" | tr -cd '}' | wc -c)
      brace_count=$((brace_count + open_braces - close_braces))

      if [[ -n "$trimmed" && "$trimmed" != //* && "$trimmed" != "}" ]]; then
        has_code=true
      fi

      if [[ $brace_count -eq 0 ]]; then
        if [[ "$has_code" == false ]]; then
          FINDINGS+=("${filepath}|${init_line}|medium|DC-GO-009|init() function body contains only comments|Remove the init() function or implement its intended behavior|Empty init() at line $init_line")
        fi
        in_init=false
      fi
    fi
  done < "$filepath"
}

# ============================================================================
# CSS/SCSS File-Level Checks
# ============================================================================

check_css_file_level() {
  local filepath="$1"

  check_css_duplicate_selectors "$filepath"
  check_css_important_overuse "$filepath"
  check_css_unused_variables "$filepath"
}

check_css_duplicate_selectors() {
  local filepath="$1"

  # Extract selectors (lines ending with {) and find duplicates
  local selectors
  selectors=$(grep -oE "^[^{/]+\{" "$filepath" 2>/dev/null | sed 's/{$//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | sort | uniq -d)

  if [[ -n "$selectors" ]]; then
    while IFS= read -r selector; do
      [[ -z "$selector" ]] && continue
      local first_line
      first_line=$(grep -n "${selector}" "$filepath" 2>/dev/null | head -1 | cut -d: -f1)
      if [[ -n "$first_line" ]]; then
        FINDINGS+=("${filepath}|${first_line}|medium|DC-CSS-003|Duplicate selector '${selector}' declared multiple times|Merge duplicate selectors into one rule block|${selector} appears multiple times")
      fi
    done <<< "$selectors"
  fi
}

check_css_important_overuse() {
  local filepath="$1"

  local important_count
  important_count=$(grep -c "!important" "$filepath" 2>/dev/null || echo "0")

  if [[ "$important_count" -ge 5 ]]; then
    FINDINGS+=("${filepath}|1|medium|DC-CSS-006|Excessive !important declarations (${important_count}) in file|Refactor specificity instead of using !important|${important_count} !important declarations")
  fi
}

check_css_unused_variables() {
  local filepath="$1"

  # Find CSS custom property definitions
  local var_defs
  var_defs=$(grep -oE "--[a-zA-Z][a-zA-Z0-9_-]*[[:space:]]*:" "$filepath" 2>/dev/null | sed 's/[[:space:]]*:$//' | sort -u)

  if [[ -z "$var_defs" ]]; then
    return
  fi

  while IFS= read -r var_name; do
    [[ -z "$var_name" ]] && continue

    # Check if the variable is used with var()
    local usage_count
    usage_count=$(grep -c "var(${var_name})" "$filepath" 2>/dev/null || echo "0")

    if [[ "$usage_count" -eq 0 ]]; then
      local def_line
      def_line=$(grep -n "${var_name}[[:space:]]*:" "$filepath" 2>/dev/null | head -1 | cut -d: -f1)
      FINDINGS+=("${filepath}|${def_line:-1}|high|DC-CSS-008|CSS variable '${var_name}' defined but never used with var()|Remove the unused CSS variable definition|${var_name} defined but not referenced")
    fi
  done <<< "$var_defs"
}

# ============================================================================
# Calculate Dead Code Score
# ============================================================================

# Calculate a score (0-100, higher is better) from findings.
# Score starts at 100 and points are deducted per finding.
calculate_deadcode_score() {
  local score=100

  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _file _line severity _check _desc _rec _text <<< "$finding"
    local deduction
    deduction=$(severity_to_points "$severity")
    score=$((score - deduction))
  done

  # Floor at 0
  if [[ $score -lt 0 ]]; then
    score=0
  fi

  echo "$score"
}

# Score to letter grade
score_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 50 ]]; then echo "D"
  else echo "F"
  fi
}

# Color for grade
grade_color() {
  local grade="$1"
  case "$grade" in
    A) echo "$GREEN" ;;
    B) echo "$GREEN" ;;
    C) echo "$YELLOW" ;;
    D) echo "$RED" ;;
    F) echo "$RED" ;;
    *) echo "$NC" ;;
  esac
}

# Severity color
severity_color() {
  local sev="$1"
  case "$sev" in
    critical) echo "$RED" ;;
    high)     echo "$MAGENTA" ;;
    medium)   echo "$YELLOW" ;;
    low)      echo "$CYAN" ;;
    *)        echo "$NC" ;;
  esac
}

# Severity label
severity_label() {
  local sev="$1"
  case "$sev" in
    critical) echo "CRITICAL" ;;
    high)     echo "HIGH    " ;;
    medium)   echo "MEDIUM  " ;;
    low)      echo "LOW     " ;;
    *)        echo "UNKNOWN " ;;
  esac
}

# Language type display label
lang_type_label() {
  local ltype="$1"
  case "$ltype" in
    js)   echo "JavaScript/TypeScript" ;;
    py)   echo "Python" ;;
    go)   echo "Go" ;;
    css)  echo "CSS/SCSS" ;;
    *)    echo "Unknown" ;;
  esac
}

# ============================================================================
# Format Finding
# ============================================================================

format_finding() {
  local finding="$1"
  IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"

  local color
  color=$(severity_color "$f_severity")
  local label
  label=$(severity_label "$f_severity")

  local display_file
  display_file=$(basename "$f_file")

  echo -e "  ${color}${BOLD}${label}${NC}  ${BOLD}${display_file}${NC}:${CYAN}${f_line}${NC}  ${DIM}[${f_check}]${NC}"
  echo -e "           ${f_desc}"
  if [[ -n "${f_text:-}" && "$f_text" != "Missing"* ]]; then
    echo -e "           ${DIM}> ${f_text}${NC}"
  fi
  echo -e "           ${DIM}Fix: ${f_rec}${NC}"
  echo ""
}

# ============================================================================
# Print Summary
# ============================================================================

print_scan_summary() {
  local files_scanned="$1"
  local deadcode_score="$2"

  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done

  local total=$((critical + high + medium + low))
  local grade
  grade=$(score_grade "$deadcode_score")
  local gcolor
  gcolor=$(grade_color "$grade")

  echo -e "${BOLD}--- Scan Summary ---${NC}"
  echo ""
  echo -e "  Files scanned:     ${BOLD}$files_scanned${NC}"
  echo -e "  Total issues:      ${BOLD}$total${NC}"
  if [[ $critical -gt 0 ]]; then
    echo -e "    Critical:        ${RED}${BOLD}$critical${NC}"
  else
    echo -e "    Critical:        ${DIM}$critical${NC}"
  fi
  if [[ $high -gt 0 ]]; then
    echo -e "    High:            ${MAGENTA}${BOLD}$high${NC}"
  else
    echo -e "    High:            ${DIM}$high${NC}"
  fi
  if [[ $medium -gt 0 ]]; then
    echo -e "    Medium:          ${YELLOW}$medium${NC}"
  else
    echo -e "    Medium:          ${DIM}$medium${NC}"
  fi
  if [[ $low -gt 0 ]]; then
    echo -e "    Low:             ${CYAN}$low${NC}"
  else
    echo -e "    Low:             ${DIM}$low${NC}"
  fi
  echo ""
  echo -e "  Dead Code Score:   ${gcolor}${BOLD}$deadcode_score/100${NC} (Grade: ${gcolor}${BOLD}$grade${NC})"
  echo ""

  if [[ $deadcode_score -lt 70 ]]; then
    echo -e "  ${RED}${BOLD}FAIL${NC} -- Dead code score below 70. Review findings above."
  elif [[ $total -gt 0 ]]; then
    echo -e "  ${YELLOW}${BOLD}WARN${NC} -- Dead code found, but score is acceptable. Cleanup recommended."
  else
    echo -e "  ${GREEN}${BOLD}PASS${NC} -- No dead code detected."
  fi
}

# ============================================================================
# Main Scan Orchestrator
# ============================================================================

# Main scan entry point. Finds source files, analyzes each, aggregates results.
# Usage: do_deadcode_scan <target> <max_files>
# max_files=0 means unlimited (Pro/Team), 5 for free tier
do_deadcode_scan() {
  local target="$1"
  local max_files="${2:-0}"

  if [[ ! -e "$target" ]]; then
    echo -e "${RED}[DeadCode]${NC} Target not found: ${BOLD}$target${NC}" >&2
    return 1
  fi

  # Find source files
  local -a source_files=()
  find_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DeadCode]${NC} No source files found in ${BOLD}$target${NC}"
    echo -e "${DIM}  Searched for: *.js, *.ts, *.jsx, *.tsx, *.py, *.go, *.css, *.scss${NC}"
    return 0
  fi

  # Apply file limit for free tier
  local files_to_scan=("${source_files[@]}")
  local was_limited=false
  if [[ $max_files -gt 0 && ${#source_files[@]} -gt $max_files ]]; then
    files_to_scan=("${source_files[@]:0:$max_files}")
    was_limited=true
  fi

  echo -e "${BOLD}--- DeadCode Scan ---${NC}"
  echo ""
  echo -e "Target:   ${BOLD}$target${NC}"
  echo -e "Files:    ${CYAN}${#source_files[@]}${NC} source file(s) found"

  if [[ "$was_limited" == true ]]; then
    echo -e "${YELLOW}  Free tier: scanning $max_files of ${#source_files[@]} files.${NC}"
    echo -e "${YELLOW}  Upgrade to Pro for unlimited scanning: ${CYAN}https://deadcode.pages.dev${NC}"
  fi

  # Show detected language types
  local -A type_counts=()
  for file in "${files_to_scan[@]}"; do
    local ltype
    ltype=$(detect_lang_type "$file")
    type_counts[$ltype]=$(( ${type_counts[$ltype]:-0} + 1 ))
  done

  echo -e "Languages:${DIM}$(for t in "${!type_counts[@]}"; do echo -n " $(lang_type_label "$t") (${type_counts[$t]})"; done)${NC}"
  echo ""

  # Scan each file
  FINDINGS=()
  local files_scanned=0

  for file in "${files_to_scan[@]}"; do
    files_scanned=$((files_scanned + 1))
    local ltype
    ltype=$(detect_lang_type "$file")
    local llabel
    llabel=$(lang_type_label "$ltype")

    echo -e "  ${DIM}[$files_scanned/${#files_to_scan[@]}]${NC} $(basename "$file") ${DIM}($llabel)${NC}"

    if [[ "$ltype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ltype"
    fi
  done

  echo ""

  # Print findings
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No dead code detected.${NC}"
    echo ""
    print_scan_summary "$files_scanned" 100
    return 0
  fi

  echo -e "${BOLD}--- Findings ---${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
  done

  local deadcode_score
  deadcode_score=$(calculate_deadcode_score)

  print_scan_summary "$files_scanned" "$deadcode_score"

  # Exit code: 0 if score >= 70, 1 otherwise
  if [[ $deadcode_score -lt 70 ]]; then
    return 1
  fi

  return 0
}

# ============================================================================
# Hook Entry Point
# ============================================================================

# Pre-commit hook entry point. Scans staged source files.
# Returns exit code 1 if critical or high severity findings.
hook_deadcode_scan() {
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  # Filter for source files only
  local -a staged_sources=()
  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue
    local ltype
    ltype=$(detect_lang_type "$file")
    if [[ "$ltype" != "unknown" ]]; then
      staged_sources+=("$file")
    fi
  done <<< "$staged_files"

  if [[ ${#staged_sources[@]} -eq 0 ]]; then
    return 0
  fi

  echo -e "${BLUE}[DeadCode]${NC} Scanning ${#staged_sources[@]} staged source file(s)..."

  FINDINGS=()
  local has_critical_or_high=false

  for file in "${staged_sources[@]}"; do
    local ltype
    ltype=$(detect_lang_type "$file")
    scan_file_with_patterns "$file" "$ltype"
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DeadCode]${NC} No dead code in staged files."
    return 0
  fi

  echo ""
  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_critical_or_high=true
    fi
  done

  local deadcode_score
  deadcode_score=$(calculate_deadcode_score)

  print_scan_summary "${#staged_sources[@]}" "$deadcode_score"

  if [[ "$has_critical_or_high" == true ]]; then
    echo ""
    echo -e "${RED}${BOLD}Commit blocked: Critical/high dead code issues found.${NC}"
    echo -e "${DIM}Run 'deadcode scan' for details. Use 'git commit --no-verify' to skip (NOT recommended).${NC}"
    return 1
  fi

  return 0
}

# ============================================================================
# Orphan File Detection
# ============================================================================

find_orphan_files() {
  local target="$1"

  if [[ ! -d "$target" ]]; then
    echo -e "${RED}[DeadCode]${NC} Target must be a directory for orphan detection." >&2
    return 1
  fi

  echo -e "${BOLD}--- DeadCode Orphan File Detection ---${NC}"
  echo ""

  local -a source_files=()
  find_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DeadCode]${NC} No source files found."
    return 0
  fi

  echo -e "Scanning ${CYAN}${#source_files[@]}${NC} source files for orphans..."
  echo ""

  # Build a list of all basenames and paths
  local -a orphan_candidates=()
  local -a non_orphans=()

  for file in "${source_files[@]}"; do
    local basename_f
    basename_f=$(basename "$file")
    local basename_lower
    basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')
    local name_no_ext="${basename_lower%.*}"

    # Skip entry points and special files
    if [[ "$name_no_ext" == "index" || "$name_no_ext" == "main" || "$name_no_ext" == "app" || "$name_no_ext" == "server" ]]; then
      continue
    fi
    # Skip test files
    if echo "$basename_lower" | grep -qE "(\.test\.|\.spec\.|_test\.|test_|\.stories\.)" 2>/dev/null; then
      continue
    fi
    # Skip config files
    if echo "$basename_lower" | grep -qE "(config|rc|setup\.py|setup\.cfg|conftest|__init__|__main__)" 2>/dev/null; then
      continue
    fi
    # Skip type definitions
    if echo "$basename_lower" | grep -qE "(\.d\.ts$|types\.)" 2>/dev/null; then
      continue
    fi

    orphan_candidates+=("$file")
  done

  # For each candidate, check if any other file references it
  local orphan_count=0
  local -a orphan_list=()

  for candidate in "${orphan_candidates[@]}"; do
    local basename_f
    basename_f=$(basename "$candidate")
    local name_no_ext="${basename_f%.*}"
    # Remove additional extensions (e.g., .module from component.module.css)
    name_no_ext="${name_no_ext%.*}"

    # Search for import/require of this file in all source files
    local is_referenced=false

    # Check common import patterns
    for file in "${source_files[@]}"; do
      [[ "$file" == "$candidate" ]] && continue

      # Check for imports containing the filename (without extension)
      if grep -qE "(import|require|from)[[:space:]]*['\"].*${name_no_ext}" "$file" 2>/dev/null; then
        is_referenced=true
        break
      fi
      # Check for Go imports
      if grep -qE "\".*/${name_no_ext}\"" "$file" 2>/dev/null; then
        is_referenced=true
        break
      fi
      # Check for CSS @import
      if grep -qE "@import.*${name_no_ext}" "$file" 2>/dev/null; then
        is_referenced=true
        break
      fi
    done

    if [[ "$is_referenced" == false ]]; then
      orphan_count=$((orphan_count + 1))
      orphan_list+=("$candidate")
      local ltype
      ltype=$(detect_lang_type "$candidate")
      local llabel
      llabel=$(lang_type_label "$ltype")
      echo -e "  ${MAGENTA}ORPHAN${NC}  $(basename "$candidate") ${DIM}($llabel)${NC}"
      echo -e "           ${DIM}$candidate${NC}"
      echo ""
    fi
  done

  echo -e "${BOLD}--- Orphan Summary ---${NC}"
  echo ""
  echo -e "  Files scanned:     ${BOLD}${#source_files[@]}${NC}"
  echo -e "  Candidates checked:${BOLD}${#orphan_candidates[@]}${NC}"
  echo -e "  Orphans found:     ${BOLD}$orphan_count${NC}"
  echo ""

  if [[ $orphan_count -eq 0 ]]; then
    echo -e "  ${GREEN}${BOLD}No orphan files detected.${NC}"
  else
    echo -e "  ${YELLOW}${BOLD}$orphan_count orphan file(s) may be safe to delete.${NC}"
    echo -e "  ${DIM}Review each file before deletion -- some may be dynamically imported.${NC}"
  fi
}

# ============================================================================
# Generate Dead Code Report
# ============================================================================

generate_deadcode_report() {
  local target="$1"

  # Find and scan all source files (unlimited)
  local -a source_files=()
  find_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DeadCode]${NC} No source files found. Nothing to report."
    return 0
  fi

  FINDINGS=()
  local files_scanned=0
  local -A lang_file_counts=()
  local -A lang_finding_counts=()

  for file in "${source_files[@]}"; do
    files_scanned=$((files_scanned + 1))
    local ltype
    ltype=$(detect_lang_type "$file")
    lang_file_counts[$ltype]=$(( ${lang_file_counts[$ltype]:-0} + 1 ))
    local before_count=${#FINDINGS[@]}
    if [[ "$ltype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ltype"
    fi
    local after_count=${#FINDINGS[@]}
    lang_finding_counts[$ltype]=$(( ${lang_finding_counts[$ltype]:-0} + (after_count - before_count) ))
  done

  local deadcode_score
  deadcode_score=$(calculate_deadcode_score)
  local grade
  grade=$(score_grade "$deadcode_score")

  # Count by severity
  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done
  local total=$((critical + high + medium + low))

  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || pwd)")

  # Read template and substitute
  local template_path="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_path" ]]; then
    echo -e "${RED}[DeadCode]${NC} Report template not found at $template_path"
    return 1
  fi

  local report
  report=$(cat "$template_path")

  local report_date
  report_date=$(date +"%Y-%m-%d %H:%M:%S")

  # Build findings table
  local findings_table=""
  if [[ $total -gt 0 ]]; then
    local idx=0
    for finding in "${FINDINGS[@]}"; do
      idx=$((idx + 1))
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"
      findings_table+="| $idx | \`$(basename "$f_file")\` | $f_line | **$f_severity** | $f_check | $f_desc |"$'\n'
    done
  fi

  # Build language breakdown
  local lang_breakdown=""
  for ltype in "${!lang_file_counts[@]}"; do
    local llabel
    llabel=$(lang_type_label "$ltype")
    lang_breakdown+="| $llabel | ${lang_file_counts[$ltype]} | ${lang_finding_counts[$ltype]:-0} |"$'\n'
  done

  # Build recommendations
  local recommendations_md=""
  if [[ $critical -gt 0 ]]; then
    recommendations_md+="- **URGENT:** $critical critical dead code issue(s). These cause real confusion or waste. Remove immediately."$'\n'
  fi
  if [[ $high -gt 0 ]]; then
    recommendations_md+="- **HIGH PRIORITY:** $high high severity issue(s). Unused exports and unreachable code inflate your codebase."$'\n'
  fi
  if [[ $medium -gt 0 ]]; then
    recommendations_md+="- **REVIEW:** $medium medium severity issue(s). Commented-out code and empty bodies should be cleaned up."$'\n'
  fi
  if [[ $total -eq 0 ]]; then
    recommendations_md="No action items. All source files pass dead code checks."
  fi

  # Perform substitutions
  report="${report//\{\{DATE\}\}/$report_date}"
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{DEADCODE_SCORE\}\}/$deadcode_score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$files_scanned}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$critical}"
  report="${report//\{\{HIGH_COUNT\}\}/$high}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$medium}"
  report="${report//\{\{LOW_COUNT\}\}/$low}"
  report="${report//\{\{VERSION\}\}/$DEADCODE_VERSION}"

  # Multi-line substitutions
  report=$(echo "$report" | awk -v findings="$findings_table" '{gsub(/\{\{FINDINGS_TABLE\}\}/, findings); print}')
  report=$(echo "$report" | awk -v breakdown="$lang_breakdown" '{gsub(/\{\{LANGUAGE_BREAKDOWN\}\}/, breakdown); print}')
  report=$(echo "$report" | awk -v recs="$recommendations_md" '{gsub(/\{\{RECOMMENDATIONS\}\}/, recs); print}')

  # Output report
  local output_file="deadcode-report-$(date +%Y%m%d-%H%M%S).md"
  echo "$report" > "$output_file"

  echo -e "${GREEN}[DeadCode]${NC} Report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:     $files_scanned"
  echo -e "  Total issues:      $total"
  echo -e "  Dead code score:   $deadcode_score/100 (Grade: $grade)"
}

# ============================================================================
# SARIF Output
# ============================================================================

generate_sarif() {
  local target="$1"

  # Run full scan
  local -a source_files=()
  find_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DeadCode]${NC} No source files found."
    return 0
  fi

  FINDINGS=()
  for file in "${source_files[@]}"; do
    local ltype
    ltype=$(detect_lang_type "$file")
    if [[ "$ltype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ltype"
    fi
  done

  local output_file="deadcode-$(date +%Y%m%d-%H%M%S).sarif"

  # Build SARIF JSON
  # Using heredoc and simple string manipulation (no jq required)
  {
    cat <<'SARIF_HEADER'
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "DeadCode",
          "informationUri": "https://deadcode.pages.dev",
SARIF_HEADER

    echo "          \"version\": \"${DEADCODE_VERSION}\","
    echo '          "rules": ['

    # Collect unique rules
    local -A seen_rules=()
    local rule_idx=0
    local rules_json=""

    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l f_severity f_check f_desc f_rec _t <<< "$finding"

      if [[ -z "${seen_rules[$f_check]:-}" ]]; then
        seen_rules[$f_check]=1
        local sarif_level="note"
        case "$f_severity" in
          critical) sarif_level="error" ;;
          high)     sarif_level="error" ;;
          medium)   sarif_level="warning" ;;
          low)      sarif_level="note" ;;
        esac

        if [[ $rule_idx -gt 0 ]]; then
          rules_json+=","
        fi
        rules_json+="
            {
              \"id\": \"${f_check}\",
              \"shortDescription\": { \"text\": \"${f_desc}\" },
              \"defaultConfiguration\": { \"level\": \"${sarif_level}\" },
              \"helpUri\": \"https://deadcode.pages.dev/rules/${f_check}\",
              \"properties\": { \"tags\": [\"dead-code\"] }
            }"
        rule_idx=$((rule_idx + 1))
      fi
    done

    echo "$rules_json"
    echo '          ]'
    echo '        }'
    echo '      },'
    echo '      "results": ['

    # Output each finding as a SARIF result
    local result_idx=0
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"

      local sarif_level="note"
      case "$f_severity" in
        critical) sarif_level="error" ;;
        high)     sarif_level="error" ;;
        medium)   sarif_level="warning" ;;
        low)      sarif_level="note" ;;
      esac

      if [[ $result_idx -gt 0 ]]; then
        echo ","
      fi

      # Escape special characters in text
      local escaped_text
      escaped_text=$(echo "$f_text" | sed 's/\\/\\\\/g; s/"/\\"/g')
      local escaped_desc
      escaped_desc=$(echo "$f_desc" | sed 's/\\/\\\\/g; s/"/\\"/g')
      local escaped_rec
      escaped_rec=$(echo "$f_rec" | sed 's/\\/\\\\/g; s/"/\\"/g')

      cat <<SARIF_RESULT
        {
          "ruleId": "${f_check}",
          "level": "${sarif_level}",
          "message": {
            "text": "${escaped_desc}. Fix: ${escaped_rec}"
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "${f_file}"
                },
                "region": {
                  "startLine": ${f_line}
                }
              }
            }
          ]
        }
SARIF_RESULT
      result_idx=$((result_idx + 1))
    done

    echo '      ]'
    echo '    }'
    echo '  ]'
    echo '}'
  } > "$output_file"

  echo -e "${GREEN}[DeadCode]${NC} SARIF report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Findings:  ${#FINDINGS[@]}"
  echo -e "  Format:    SARIF v2.1.0"
  echo -e "  ${DIM}Upload to GitHub Code Scanning, Azure DevOps, or your CI system.${NC}"
}
