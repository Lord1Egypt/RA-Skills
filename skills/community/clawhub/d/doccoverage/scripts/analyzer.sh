#!/usr/bin/env bash
# DocCoverage -- Core Analysis Engine
# Provides: language detection, file discovery, doc coverage scanning,
#           context-aware doc checks, README analysis, CHANGELOG verification,
#           coverage percentage, report generation, policy enforcement,
#           SARIF output, and pre-commit hook handler.
#
# This file is sourced by doccoverage.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# -- Colors (safe to re-declare; sourcing scripts may set these) ---------------

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
DOCCOVERAGE_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

# Global coverage counters
TOTAL_PUBLIC_SYMBOLS=0
DOCUMENTED_SYMBOLS=0

# -- Language Detection --------------------------------------------------------

# Detect the programming language for a given file.
detect_language() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local ext="${basename_f##*.}"
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')

  case "$ext" in
    js|mjs|cjs)         echo "javascript" ;;
    ts|tsx|mts|cts)      echo "typescript" ;;
    jsx)                 echo "javascript" ;;
    py|pyw)              echo "python" ;;
    go)                  echo "go" ;;
    java)                echo "java" ;;
    rb|rake)             echo "ruby" ;;
    md)                  echo "markdown" ;;
    yml|yaml)            echo "yaml" ;;
    graphql|gql)         echo "graphql" ;;
    proto)               echo "protobuf" ;;
    erb)                 echo "ruby" ;;
    *)
      case "$basename_lower" in
        rakefile|gemfile)   echo "ruby" ;;
        readme|readme.*)    echo "markdown" ;;
        changelog|history)  echo "markdown" ;;
        *)                  echo "unknown" ;;
      esac
      ;;
  esac
}

# Get display label for a language
language_label() {
  local lang="$1"
  case "$lang" in
    javascript)  echo "JavaScript" ;;
    typescript)  echo "TypeScript" ;;
    python)      echo "Python" ;;
    go)          echo "Go" ;;
    java)        echo "Java" ;;
    ruby)        echo "Ruby" ;;
    markdown)    echo "Markdown" ;;
    yaml)        echo "YAML" ;;
    graphql)     echo "GraphQL" ;;
    protobuf)    echo "Protobuf" ;;
    *)           echo "Unknown" ;;
  esac
}

# -- Discover Source Files -----------------------------------------------------

discover_source_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  if [[ -f "$search_dir" ]]; then
    local lang
    lang=$(detect_language "$search_dir")
    if [[ "$lang" != "unknown" ]]; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 8 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name "__pycache__" \
       -o -name ".venv" -o -name "venv" -o -name "dist" -o -name "build" \
       -o -name ".next" -o -name ".nuxt" -o -name "target" -o -name "bin" \) -prune -o \
    \( -name "*.js" -o -name "*.mjs" -o -name "*.cjs" -o -name "*.jsx" \
       -o -name "*.ts" -o -name "*.tsx" -o -name "*.mts" -o -name "*.cts" \
       -o -name "*.py" -o -name "*.pyw" \
       -o -name "*.go" \
       -o -name "*.java" \
       -o -name "*.rb" -o -name "*.rake" \
       -o -name "*.graphql" -o -name "*.gql" \
       -o -name "*.proto" \) \
    -type f -print0 2>/dev/null)
}

# -- Context-Aware Doc Checks --------------------------------------------------
# These check whether a function/class at a given line has preceding docs.

# Check if line N has a JSDoc block ending on line N-1 or nearby above
has_jsdoc_above() {
  local filepath="$1"
  local line_num="$2"

  # Look at the 5 lines above the target line for a JSDoc closing */
  local start=$((line_num - 5))
  [[ $start -lt 1 ]] && start=1

  local above
  above=$(sed -n "${start},$((line_num - 1))p" "$filepath" 2>/dev/null)

  if echo "$above" | grep -qE '\*/[[:space:]]*$'; then
    return 0
  fi

  # Also check for single-line /** ... */ comment
  if echo "$above" | grep -qE '/\*\*.*\*/'; then
    return 0
  fi

  # Check for // comments directly above
  local prev_line
  prev_line=$(sed -n "$((line_num - 1))p" "$filepath" 2>/dev/null)
  if echo "$prev_line" | grep -qE '^[[:space:]]*(//|/\*\*)'; then
    return 0
  fi

  return 1
}

# Check if Python function/class at line N has docstring on line N+1 or N+2
has_python_docstring() {
  local filepath="$1"
  local line_num="$2"

  local next_lines
  next_lines=$(sed -n "$((line_num + 1)),$((line_num + 3))p" "$filepath" 2>/dev/null)

  if echo "$next_lines" | grep -qE '^[[:space:]]*("""|'"'"''"'"''"'"')'; then
    return 0
  fi

  return 1
}

# Check if Go exported func at line N has // comment on line N-1
has_godoc_above() {
  local filepath="$1"
  local line_num="$2"

  if [[ $line_num -le 1 ]]; then
    return 1
  fi

  local prev_line
  prev_line=$(sed -n "$((line_num - 1))p" "$filepath" 2>/dev/null)

  if echo "$prev_line" | grep -qE '^[[:space:]]*//'; then
    return 0
  fi

  return 1
}

# Check if Java method at line N has Javadoc ending on a line above
has_javadoc_above() {
  local filepath="$1"
  local line_num="$2"

  local start=$((line_num - 8))
  [[ $start -lt 1 ]] && start=1

  local above
  above=$(sed -n "${start},$((line_num - 1))p" "$filepath" 2>/dev/null)

  if echo "$above" | grep -qE '\*/[[:space:]]*$'; then
    if echo "$above" | grep -qE '/\*\*'; then
      return 0
    fi
  fi

  return 1
}

# Check if Ruby method at line N has # comment on line N-1
has_yard_above() {
  local filepath="$1"
  local line_num="$2"

  if [[ $line_num -le 1 ]]; then
    return 1
  fi

  local prev_line
  prev_line=$(sed -n "$((line_num - 1))p" "$filepath" 2>/dev/null)

  if echo "$prev_line" | grep -qE '^[[:space:]]*#'; then
    return 0
  fi

  return 1
}

# -- Scan JS/TS Files for Missing Docs ----------------------------------------

scan_jsts_missing_docs() {
  local filepath="$1"

  # Find exported functions
  local line_num=0
  while IFS= read -r line; do
    line_num=$((line_num + 1))

    # export function name(
    if echo "$line" | grep -qE '^[[:space:]]*export[[:space:]]+(async[[:space:]]+)?function[[:space:]]+[a-zA-Z_]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_jsdoc_above "$filepath" "$line_num"; then
        local fname
        fname=$(echo "$line" | grep -oE 'function[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*' | head -1 | sed 's/function[[:space:]]*//')
        FINDINGS+=("${filepath}|${line_num}|critical|MD-001|Exported function '${fname}' without JSDoc comment|Add JSDoc block before exported function|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
        # Check for incomplete JSDoc
        check_jsdoc_completeness "$filepath" "$line_num" "$line"
      fi
    fi

    # export const name = (arrow function or function expression)
    if echo "$line" | grep -qE '^[[:space:]]*export[[:space:]]+(const|let|var)[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*='; then
      # Check if it looks like a function (arrow or function expression)
      local next_content
      next_content=$(sed -n "${line_num},$((line_num + 2))p" "$filepath" 2>/dev/null)
      if echo "$next_content" | grep -qE '(=>|\bfunction\b)'; then
        TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
        if ! has_jsdoc_above "$filepath" "$line_num"; then
          local cname
          cname=$(echo "$line" | grep -oE '(const|let|var)[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*' | head -1 | sed 's/(const|let|var)[[:space:]]*//')
          FINDINGS+=("${filepath}|${line_num}|critical|MD-002|Exported const/arrow function without JSDoc|Add JSDoc block before exported const|${line}")
        else
          DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
        fi
      fi
    fi

    # export class
    if echo "$line" | grep -qE '^[[:space:]]*export[[:space:]]+(default[[:space:]]+)?class[[:space:]]+[A-Z]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_jsdoc_above "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|critical|MD-003|Exported class without JSDoc comment|Add JSDoc block before exported class|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # export interface (TypeScript)
    if echo "$line" | grep -qE '^[[:space:]]*export[[:space:]]+(default[[:space:]]+)?interface[[:space:]]+[A-Z]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_jsdoc_above "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|medium|TD-001|Exported TypeScript interface without doc comment|Add JSDoc above interface|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # export type
    if echo "$line" | grep -qE '^[[:space:]]*export[[:space:]]+(default[[:space:]]+)?type[[:space:]]+[A-Z]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_jsdoc_above "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|medium|TD-002|Exported TypeScript type alias without doc comment|Add JSDoc above type|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

  done < "$filepath"
}

# Check JSDoc completeness for a documented function
check_jsdoc_completeness() {
  local filepath="$1"
  local func_line="$2"
  local func_text="$3"

  # Extract JSDoc block above the function
  local start=$((func_line - 20))
  [[ $start -lt 1 ]] && start=1

  local jsdoc_block
  jsdoc_block=$(sed -n "${start},$((func_line - 1))p" "$filepath" 2>/dev/null)

  # Count function parameters
  local params
  params=$(echo "$func_text" | grep -oE '\([^)]*\)' | head -1 | tr ',' '\n' | grep -cE '[a-zA-Z_]' || echo "0")

  if [[ "$params" -gt 0 ]]; then
    # Check for @param tags
    local param_count
    param_count=$(echo "$jsdoc_block" | grep -cE '@param' || echo "0")
    if [[ "$param_count" -eq 0 ]]; then
      FINDINGS+=("${filepath}|${func_line}|high|ID-001|JSDoc present but missing @param tag(s)|Add @param {type} name - description for each parameter|${func_text}")
    fi
  fi

  # Check for @returns tag (skip void/undefined returns)
  if ! echo "$jsdoc_block" | grep -qE '@returns?[[:space:]]'; then
    if ! echo "$func_text" | grep -qE ':[[:space:]]*(void|undefined|never)'; then
      FINDINGS+=("${filepath}|${func_line}|high|ID-002|JSDoc present but missing @returns tag|Add @returns {type} description for non-void functions|${func_text}")
    fi
  fi
}

# -- Scan Python Files for Missing Docs ---------------------------------------

scan_python_missing_docs() {
  local filepath="$1"

  local line_num=0
  local in_class=false
  local class_indent=0

  while IFS= read -r line; do
    line_num=$((line_num + 1))

    # Public function (not starting with _)
    if echo "$line" | grep -qE '^def[[:space:]]+[a-z][a-zA-Z0-9_]*[[:space:]]*\('; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_python_docstring "$filepath" "$line_num"; then
        local fname
        fname=$(echo "$line" | grep -oE 'def[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*' | head -1 | sed 's/def[[:space:]]*//')
        FINDINGS+=("${filepath}|${line_num}|critical|MD-004|Public function '${fname}' without docstring|Add docstring after def|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
        check_python_docstring_completeness "$filepath" "$line_num" "$line"
      fi
    fi

    # Public class
    if echo "$line" | grep -qE '^class[[:space:]]+[A-Z][a-zA-Z0-9_]*'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_python_docstring "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|critical|MD-005|Public class without docstring|Add docstring after class|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # __init__ method
    if echo "$line" | grep -qE '[[:space:]]+def[[:space:]]+__init__[[:space:]]*\('; then
      if ! has_python_docstring "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|medium|MD-006|__init__ method without docstring|Add docstring to __init__|${line}")
      fi
    fi

    # Public method (indented def, not starting with _)
    if echo "$line" | grep -qE '^[[:space:]]+def[[:space:]]+[a-z][a-zA-Z0-9_]*[[:space:]]*\(self'; then
      local mname
      mname=$(echo "$line" | grep -oE 'def[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*' | head -1 | sed 's/def[[:space:]]*//')
      if [[ "$mname" != _* ]]; then
        TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
        if ! has_python_docstring "$filepath" "$line_num"; then
          FINDINGS+=("${filepath}|${line_num}|high|MD-007|Public method '${mname}' without docstring|Add docstring after def|${line}")
        else
          DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
        fi
      fi
    fi

    # Abstract method
    if echo "$line" | grep -qE '@abstractmethod'; then
      local next_def_line=$((line_num + 1))
      local next_line_content
      next_line_content=$(sed -n "${next_def_line}p" "$filepath" 2>/dev/null)
      if echo "$next_line_content" | grep -qE 'def[[:space:]]+'; then
        if ! has_python_docstring "$filepath" "$next_def_line"; then
          FINDINGS+=("${filepath}|${next_def_line}|medium|MD-019|Abstract method without docstring|Add docstring to abstract method|${next_line_content}")
        fi
      fi
    fi

  done < "$filepath"
}

# Check Python docstring completeness
check_python_docstring_completeness() {
  local filepath="$1"
  local func_line="$2"
  local func_text="$3"

  # Count parameters (excluding self, cls)
  local params
  params=$(echo "$func_text" | grep -oE '\([^)]*\)' | head -1 | tr ',' '\n' | grep -cvE '(self|cls|^[[:space:]]*$)' || echo "0")

  if [[ "$params" -gt 0 ]]; then
    # Read the docstring block
    local docstring
    docstring=$(sed -n "$((func_line + 1)),$((func_line + 30))p" "$filepath" 2>/dev/null)

    # Check for Args: section
    if ! echo "$docstring" | grep -qE '(Args:|Parameters:|:param[[:space:]])'; then
      FINDINGS+=("${filepath}|${func_line}|high|ID-003|Docstring present but missing Args section|Add Args: section listing each parameter|${func_text}")
    fi

    # Check for Returns: section
    if ! echo "$docstring" | grep -qiE '(Returns:|:returns?:|:rtype:)'; then
      if ! echo "$func_text" | grep -qE '->[[:space:]]*None'; then
        FINDINGS+=("${filepath}|${func_line}|high|ID-004|Docstring present but missing Returns section|Add Returns: section describing the return value|${func_text}")
      fi
    fi
  fi
}

# -- Scan Go Files for Missing Docs -------------------------------------------

scan_go_missing_docs() {
  local filepath="$1"

  local line_num=0
  while IFS= read -r line; do
    line_num=$((line_num + 1))

    # Exported function (starts with uppercase letter)
    if echo "$line" | grep -qE '^func[[:space:]]+[A-Z][a-zA-Z0-9_]*[[:space:]]*\('; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_godoc_above "$filepath" "$line_num"; then
        local fname
        fname=$(echo "$line" | grep -oE 'func[[:space:]]+[A-Z][a-zA-Z0-9_]*' | head -1 | sed 's/func[[:space:]]*//')
        FINDINGS+=("${filepath}|${line_num}|critical|MD-008|Exported function '${fname}' without godoc comment|Add // ${fname} comment above function|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # Exported method (receiver type)
    if echo "$line" | grep -qE '^func[[:space:]]+\([^)]+\)[[:space:]]+[A-Z][a-zA-Z0-9_]*[[:space:]]*\('; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_godoc_above "$filepath" "$line_num"; then
        local mname
        mname=$(echo "$line" | grep -oE '\)[[:space:]]+[A-Z][a-zA-Z0-9_]*' | head -1 | sed 's/)[[:space:]]*//')
        FINDINGS+=("${filepath}|${line_num}|high|MD-010|Exported method '${mname}' without godoc comment|Add // ${mname} comment above method|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # Exported type
    if echo "$line" | grep -qE '^type[[:space:]]+[A-Z][a-zA-Z0-9_]*[[:space:]]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_godoc_above "$filepath" "$line_num"; then
        local tname
        tname=$(echo "$line" | grep -oE 'type[[:space:]]+[A-Z][a-zA-Z0-9_]*' | head -1 | sed 's/type[[:space:]]*//')
        FINDINGS+=("${filepath}|${line_num}|high|MD-009|Exported type '${tname}' without godoc comment|Add // ${tname} comment above type|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

  done < "$filepath"
}

# -- Scan Java Files for Missing Docs -----------------------------------------

scan_java_missing_docs() {
  local filepath="$1"

  local line_num=0
  while IFS= read -r line; do
    line_num=$((line_num + 1))

    # Public class
    if echo "$line" | grep -qE 'public[[:space:]]+(abstract[[:space:]]+)?class[[:space:]]+[A-Z]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_javadoc_above "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|critical|MD-012|Public class without Javadoc|Add Javadoc before class|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # Public method
    if echo "$line" | grep -qE 'public[[:space:]]+(static[[:space:]]+)?[a-zA-Z<>\[\]]+[[:space:]]+[a-z][a-zA-Z0-9]*[[:space:]]*\('; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_javadoc_above "$filepath" "$line_num"; then
        local mname
        mname=$(echo "$line" | grep -oE '[a-z][a-zA-Z0-9]*[[:space:]]*\(' | head -1 | sed 's/[[:space:]]*(//')
        FINDINGS+=("${filepath}|${line_num}|critical|MD-011|Public method '${mname}' without Javadoc|Add Javadoc before method|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
        check_javadoc_completeness "$filepath" "$line_num" "$line"
      fi
    fi

  done < "$filepath"
}

check_javadoc_completeness() {
  local filepath="$1"
  local method_line="$2"
  local method_text="$3"

  local start=$((method_line - 20))
  [[ $start -lt 1 ]] && start=1

  local javadoc_block
  javadoc_block=$(sed -n "${start},$((method_line - 1))p" "$filepath" 2>/dev/null)

  # Count parameters
  local params
  params=$(echo "$method_text" | grep -oE '\([^)]*\)' | head -1 | tr ',' '\n' | grep -cE '[a-zA-Z_]' || echo "0")

  if [[ "$params" -gt 0 ]]; then
    local param_count
    param_count=$(echo "$javadoc_block" | grep -cE '@param' || echo "0")
    if [[ "$param_count" -eq 0 ]]; then
      FINDINGS+=("${filepath}|${method_line}|high|ID-014|Javadoc present but missing @param tag(s)|Add @param name description|${method_text}")
    fi
  fi

  # Check @return (skip void)
  if ! echo "$method_text" | grep -qE 'void[[:space:]]'; then
    if ! echo "$javadoc_block" | grep -qE '@returns?[[:space:]]'; then
      FINDINGS+=("${filepath}|${method_line}|high|ID-015|Javadoc present but missing @return tag|Add @return description|${method_text}")
    fi
  fi
}

# -- Scan Ruby Files for Missing Docs -----------------------------------------

scan_ruby_missing_docs() {
  local filepath="$1"

  local line_num=0
  local in_private=false

  while IFS= read -r line; do
    line_num=$((line_num + 1))

    # Track private/protected sections
    if echo "$line" | grep -qE '^[[:space:]]*(private|protected)[[:space:]]*$'; then
      in_private=true
      continue
    fi
    if echo "$line" | grep -qE '^[[:space:]]*public[[:space:]]*$'; then
      in_private=false
      continue
    fi

    # Class definition
    if echo "$line" | grep -qE '^[[:space:]]*class[[:space:]]+[A-Z]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_yard_above "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|high|MD-015|Class without YARD doc|Add # comment above class|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # Module definition
    if echo "$line" | grep -qE '^[[:space:]]*module[[:space:]]+[A-Z]'; then
      TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
      if ! has_yard_above "$filepath" "$line_num"; then
        FINDINGS+=("${filepath}|${line_num}|high|MD-016|Module without YARD doc|Add # comment above module|${line}")
      else
        DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
      fi
    fi

    # Public method (not in private section, not starting with _)
    if [[ "$in_private" == false ]]; then
      if echo "$line" | grep -qE '^[[:space:]]*def[[:space:]]+[a-z][a-zA-Z0-9_!?]*'; then
        TOTAL_PUBLIC_SYMBOLS=$((TOTAL_PUBLIC_SYMBOLS + 1))
        if ! has_yard_above "$filepath" "$line_num"; then
          local mname
          mname=$(echo "$line" | grep -oE 'def[[:space:]]+[a-zA-Z_][a-zA-Z0-9_!?]*' | head -1 | sed 's/def[[:space:]]*//')
          FINDINGS+=("${filepath}|${line_num}|critical|MD-014|Public method '${mname}' without YARD doc|Add # comment above method|${line}")
        else
          DOCUMENTED_SYMBOLS=$((DOCUMENTED_SYMBOLS + 1))
        fi
      fi
    fi

  done < "$filepath"
}

# -- Scan File with Regex Patterns ---------------------------------------------

scan_file_with_regex_patterns() {
  local filepath="$1"
  local lang="$2"

  # Run regex-based patterns (non-CONTEXT_CHECK patterns)
  local categories=("incomplete" "api" "quality")

  for category in "${categories[@]}"; do
    local patterns_name
    patterns_name=$(get_patterns_for_category "$category")
    [[ -z "$patterns_name" ]] && continue

    local -n _patterns_ref="$patterns_name"

    for entry in "${_patterns_ref[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

      # Skip context-check patterns (handled by language-specific scanners)
      [[ "$regex" == CONTEXT_CHECK_* || "$regex" == FILE_CHECK_* || "$regex" == SECTION_CHECK_* || "$regex" == LINK_CHECK_* || "$regex" == BADGE_CHECK_* || "$regex" == LENGTH_CHECK_* ]] && continue

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
  done
}

# -- Scan a Single File -------------------------------------------------------

scan_file() {
  local filepath="$1"
  local lang
  lang=$(detect_language "$filepath")

  # Language-specific missing-doc analysis
  case "$lang" in
    javascript|typescript)
      scan_jsts_missing_docs "$filepath"
      ;;
    python)
      scan_python_missing_docs "$filepath"
      ;;
    go)
      scan_go_missing_docs "$filepath"
      ;;
    java)
      scan_java_missing_docs "$filepath"
      ;;
    ruby)
      scan_ruby_missing_docs "$filepath"
      ;;
  esac

  # Regex-based pattern scanning (API docs, incomplete docs, quality)
  scan_file_with_regex_patterns "$filepath" "$lang"
}

# -- README Analysis -----------------------------------------------------------

scan_readme() {
  local search_dir="$1"

  local readme_path=""
  for candidate in "$search_dir/README.md" "$search_dir/readme.md" "$search_dir/README" "$search_dir/Readme.md"; do
    if [[ -f "$candidate" ]]; then
      readme_path="$candidate"
      break
    fi
  done

  if [[ -z "$readme_path" ]]; then
    FINDINGS+=("${search_dir}|0|high|RD-001|No README.md found in project root|Create a README.md with project description, installation, and usage sections|Missing README.md")
    return
  fi

  local readme_content
  readme_content=$(cat "$readme_path" 2>/dev/null)
  local readme_lines
  readme_lines=$(wc -l < "$readme_path" 2>/dev/null || echo "0")

  # Check for installation section
  if ! echo "$readme_content" | grep -qiE '^#+[[:space:]]*(install|setup|getting[[:space:]]+started)'; then
    FINDINGS+=("${readme_path}|0|medium|RD-002|README.md missing installation/setup section|Add an ## Installation or ## Getting Started section|No install section found")
  fi

  # Check for usage section
  if ! echo "$readme_content" | grep -qiE '^#+[[:space:]]*(usage|how[[:space:]]+to[[:space:]]+use|examples?)'; then
    FINDINGS+=("${readme_path}|0|medium|RD-003|README.md missing usage section|Add a ## Usage section with examples|No usage section found")
  fi

  # Check for API section (if package.json or setup.py exists -> library)
  if [[ -f "$search_dir/package.json" || -f "$search_dir/setup.py" || -f "$search_dir/pyproject.toml" || -f "$search_dir/Cargo.toml" ]]; then
    if ! echo "$readme_content" | grep -qiE '^#+[[:space:]]*(api|reference|documentation|public[[:space:]]+interface)'; then
      FINDINGS+=("${readme_path}|0|medium|RD-004|Library README.md missing API documentation section|Add an ## API section documenting the public interface|No API section found")
    fi
  fi

  # Check for empty sections
  local prev_was_heading=false
  local prev_heading_line=0
  local current_line=0
  while IFS= read -r line; do
    current_line=$((current_line + 1))
    if echo "$line" | grep -qE '^#+[[:space:]]'; then
      if [[ "$prev_was_heading" == true ]]; then
        FINDINGS+=("${readme_path}|${prev_heading_line}|medium|RD-010|README.md contains empty section|Fill in empty sections or remove them|Empty section at line ${prev_heading_line}")
      fi
      prev_was_heading=true
      prev_heading_line=$current_line
    elif [[ -n "$(echo "$line" | tr -d '[:space:]')" ]]; then
      prev_was_heading=false
    fi
  done < "$readme_path"

  # Check README length
  if [[ "$readme_lines" -lt 10 ]]; then
    FINDINGS+=("${readme_path}|0|low|RD-013|README.md is very short (fewer than 10 lines)|Expand README with installation, usage, and API sections|${readme_lines} lines")
  fi

  # Check for license mention
  if ! echo "$readme_content" | grep -qiE '(license|licence)'; then
    FINDINGS+=("${readme_path}|0|low|RD-012|README.md does not reference the project license|Add a ## License section referencing your LICENSE file|No license mention")
  fi
}

# -- Project File Checks ------------------------------------------------------

scan_project_files() {
  local search_dir="$1"

  # Check for LICENSE file
  local has_license=false
  for candidate in "LICENSE" "LICENSE.md" "LICENSE.txt" "LICENCE" "LICENCE.md"; do
    if [[ -f "$search_dir/$candidate" ]]; then
      has_license=true
      break
    fi
  done
  if [[ "$has_license" == false ]]; then
    FINDINGS+=("${search_dir}|0|medium|RD-007|No LICENSE file found in project root|Add a LICENSE file specifying the project license|Missing LICENSE")
  fi

  # Check for CHANGELOG
  local has_changelog=false
  for candidate in "CHANGELOG.md" "CHANGELOG" "HISTORY.md" "HISTORY" "CHANGES.md"; do
    if [[ -f "$search_dir/$candidate" ]]; then
      has_changelog=true
      break
    fi
  done
  if [[ "$has_changelog" == false ]]; then
    FINDINGS+=("${search_dir}|0|medium|RD-008|No CHANGELOG.md or HISTORY.md found|Create a CHANGELOG.md following Keep a Changelog format|Missing CHANGELOG")
  fi

  # Check for CONTRIBUTING.md
  if [[ -f "$search_dir/package.json" || -f "$search_dir/.github" ]] && [[ ! -f "$search_dir/CONTRIBUTING.md" ]]; then
    FINDINGS+=("${search_dir}|0|low|RD-006|No CONTRIBUTING.md found (recommended for open source)|Create a CONTRIBUTING.md with contribution guidelines|Missing CONTRIBUTING.md")
  fi
}

# -- Calculate Score -----------------------------------------------------------

calculate_score() {
  local score=100

  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _file _line severity _check _desc _rec _text <<< "$finding"
    local deduction
    deduction=$(severity_to_points "$severity")
    score=$((score - deduction))
  done

  if [[ $score -lt 0 ]]; then
    score=0
  fi

  echo "$score"
}

# Score to letter grade
get_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 50 ]]; then echo "D"
  else echo "F"
  fi
}

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

# -- Format Findings -----------------------------------------------------------

format_findings() {
  local finding="$1"
  IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"

  local color
  color=$(severity_color "$f_severity")
  local label
  label=$(severity_label "$f_severity")
  local cat
  cat=$(category_label_from_id "$f_check")

  local display_file
  display_file=$(basename "$f_file")

  echo -e "  ${color}${BOLD}${label}${NC}  ${BOLD}${display_file}${NC}:${CYAN}${f_line}${NC}  ${DIM}[${f_check}] ${cat}${NC}"
  echo -e "           ${f_desc}"
  if [[ -n "${f_text:-}" && "$f_text" != "Missing"* && "$f_text" != "No "* ]]; then
    local trimmed
    trimmed=$(echo "$f_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    if [[ ${#trimmed} -gt 120 ]]; then
      trimmed="${trimmed:0:117}..."
    fi
    echo -e "           ${DIM}> ${trimmed}${NC}"
  fi
  echo -e "           ${DIM}Fix: ${f_rec}${NC}"
  echo ""
}

# -- Print Summary -------------------------------------------------------------

print_scan_summary() {
  local files_scanned="$1"
  local doc_score="$2"

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
  grade=$(get_grade "$doc_score")
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

  # Coverage percentage
  if [[ $TOTAL_PUBLIC_SYMBOLS -gt 0 ]]; then
    local coverage_pct=$(( (DOCUMENTED_SYMBOLS * 100) / TOTAL_PUBLIC_SYMBOLS ))
    echo -e "  Doc Coverage:      ${BOLD}${coverage_pct}%${NC} (${DOCUMENTED_SYMBOLS}/${TOTAL_PUBLIC_SYMBOLS} public symbols documented)"
  fi

  echo -e "  Quality Score:     ${gcolor}${BOLD}$doc_score/100${NC} (Grade: ${gcolor}${BOLD}$grade${NC})"
  echo ""

  if [[ $doc_score -lt 70 ]]; then
    echo -e "  ${RED}${BOLD}FAIL${NC} -- Documentation score below 70. Review findings above."
  elif [[ $total -gt 0 ]]; then
    echo -e "  ${YELLOW}${BOLD}WARN${NC} -- Issues found, but score is acceptable. Review recommended."
  else
    echo -e "  ${GREEN}${BOLD}PASS${NC} -- No documentation issues detected."
  fi
}

# -- Main Scan Orchestrator ----------------------------------------------------

run_doccoverage_scan() {
  local target="$1"
  local max_files="${2:-0}"

  if [[ ! -e "$target" ]]; then
    echo -e "${RED}[DocCoverage]${NC} Target not found: ${BOLD}$target${NC}" >&2
    return 1
  fi

  local -a source_files=()
  discover_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DocCoverage]${NC} No source files found in ${BOLD}$target${NC}"
    return 0
  fi

  # Apply file limit for free tier
  local files_to_scan=("${source_files[@]}")
  local was_limited=false
  if [[ $max_files -gt 0 && ${#source_files[@]} -gt $max_files ]]; then
    files_to_scan=("${source_files[@]:0:$max_files}")
    was_limited=true
  fi

  echo -e "${BOLD}--- DocCoverage Documentation Scan ---${NC}"
  echo ""
  echo -e "Target:   ${BOLD}$target${NC}"
  echo -e "Files:    ${CYAN}${#source_files[@]}${NC} source file(s) found"

  if [[ "$was_limited" == true ]]; then
    echo -e "${YELLOW}  Free tier: scanning $max_files of ${#source_files[@]} files.${NC}"
    echo -e "${YELLOW}  Upgrade to Pro for unlimited scanning: ${CYAN}https://doccoverage.pages.dev${NC}"
  fi

  # Show detected languages
  local -A lang_counts=()
  for file in "${files_to_scan[@]}"; do
    local lang
    lang=$(detect_language "$file")
    lang_counts[$lang]=$(( ${lang_counts[$lang]:-0} + 1 ))
  done

  echo -e "Languages: ${DIM}$(for l in "${!lang_counts[@]}"; do echo -n "$(language_label "$l") (${lang_counts[$l]}) "; done)${NC}"
  echo ""

  # Scan each file
  FINDINGS=()
  TOTAL_PUBLIC_SYMBOLS=0
  DOCUMENTED_SYMBOLS=0
  local files_scanned=0

  for file in "${files_to_scan[@]}"; do
    files_scanned=$((files_scanned + 1))
    local lang
    lang=$(detect_language "$file")
    local lang_lbl
    lang_lbl=$(language_label "$lang")

    echo -e "  ${DIM}[$files_scanned/${#files_to_scan[@]}]${NC} $(basename "$file") ${DIM}($lang_lbl)${NC}"

    scan_file "$file"
  done

  echo ""

  # Also scan README and project files if scanning a directory
  if [[ -d "$target" ]]; then
    scan_readme "$target"
    scan_project_files "$target"
  fi

  # Print findings
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No documentation issues detected.${NC}"
    echo ""
    print_scan_summary "$files_scanned" 100
    return 0
  fi

  echo -e "${BOLD}--- Findings ---${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
  done

  local doc_score
  doc_score=$(calculate_score)

  print_scan_summary "$files_scanned" "$doc_score"

  if [[ $doc_score -lt 70 ]]; then
    return 1
  fi

  return 0
}

# -- Coverage Percentage -------------------------------------------------------

run_doccoverage_coverage() {
  local target="$1"

  echo -e "${BOLD}--- DocCoverage Coverage Analysis ---${NC}"
  echo ""

  local -a source_files=()
  discover_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DocCoverage]${NC} No source files found."
    return 0
  fi

  FINDINGS=()
  TOTAL_PUBLIC_SYMBOLS=0
  DOCUMENTED_SYMBOLS=0

  local -A lang_documented=()
  local -A lang_total=()

  for file in "${source_files[@]}"; do
    local lang
    lang=$(detect_language "$file")
    local lang_lbl
    lang_lbl=$(language_label "$lang")

    local before_total=$TOTAL_PUBLIC_SYMBOLS
    local before_doc=$DOCUMENTED_SYMBOLS

    scan_file "$file"

    local file_total=$((TOTAL_PUBLIC_SYMBOLS - before_total))
    local file_doc=$((DOCUMENTED_SYMBOLS - before_doc))

    lang_total[$lang]=$(( ${lang_total[$lang]:-0} + file_total ))
    lang_documented[$lang]=$(( ${lang_documented[$lang]:-0} + file_doc ))

    if [[ $file_total -gt 0 ]]; then
      local file_pct=$(( (file_doc * 100) / file_total ))
      echo -e "  $(basename "$file") ${DIM}($lang_lbl)${NC}: ${BOLD}${file_pct}%${NC} (${file_doc}/${file_total})"
    fi
  done

  echo ""
  echo -e "${BOLD}--- Coverage by Language ---${NC}"
  echo ""

  for lang in "${!lang_total[@]}"; do
    local lt=${lang_total[$lang]}
    local ld=${lang_documented[$lang]}
    if [[ $lt -gt 0 ]]; then
      local lpct=$(( (ld * 100) / lt ))
      echo -e "  $(language_label "$lang"): ${BOLD}${lpct}%${NC} (${ld}/${lt} public symbols)"
    fi
  done

  echo ""

  if [[ $TOTAL_PUBLIC_SYMBOLS -gt 0 ]]; then
    local overall_pct=$(( (DOCUMENTED_SYMBOLS * 100) / TOTAL_PUBLIC_SYMBOLS ))
    local grade_val
    if [[ $overall_pct -ge 90 ]]; then grade_val="A"
    elif [[ $overall_pct -ge 80 ]]; then grade_val="B"
    elif [[ $overall_pct -ge 70 ]]; then grade_val="C"
    elif [[ $overall_pct -ge 50 ]]; then grade_val="D"
    else grade_val="F"
    fi
    local gcolor
    gcolor=$(grade_color "$grade_val")

    echo -e "${BOLD}--- Overall Coverage ---${NC}"
    echo ""
    echo -e "  Public symbols:    ${BOLD}$TOTAL_PUBLIC_SYMBOLS${NC}"
    echo -e "  Documented:        ${BOLD}$DOCUMENTED_SYMBOLS${NC}"
    echo -e "  Coverage:          ${gcolor}${BOLD}${overall_pct}%${NC} (Grade: ${gcolor}${BOLD}$grade_val${NC})"
  else
    echo -e "  No public symbols detected."
  fi
}

# -- Hook Entry Point ----------------------------------------------------------

hook_doccoverage_scan() {
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  local -a staged_source_files=()
  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue
    local lang
    lang=$(detect_language "$file")
    if [[ "$lang" != "unknown" ]]; then
      staged_source_files+=("$file")
    fi
  done <<< "$staged_files"

  if [[ ${#staged_source_files[@]} -eq 0 ]]; then
    return 0
  fi

  echo -e "${BLUE}[DocCoverage]${NC} Scanning ${#staged_source_files[@]} staged file(s) for documentation gaps..."

  FINDINGS=()
  TOTAL_PUBLIC_SYMBOLS=0
  DOCUMENTED_SYMBOLS=0
  local has_critical_or_high=false

  for file in "${staged_source_files[@]}"; do
    scan_file "$file"
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DocCoverage]${NC} All staged files have adequate documentation."
    return 0
  fi

  echo ""
  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_critical_or_high=true
    fi
  done

  local doc_score
  doc_score=$(calculate_score)

  print_scan_summary "${#staged_source_files[@]}" "$doc_score"

  if [[ "$has_critical_or_high" == true ]]; then
    echo ""
    echo -e "${RED}${BOLD}Commit blocked: Critical/high documentation gaps found.${NC}"
    echo -e "${DIM}Run 'doccoverage scan' for details. Use 'git commit --no-verify' to skip (NOT recommended).${NC}"
    return 1
  fi

  return 0
}

# -- Generate Report -----------------------------------------------------------

generate_doccoverage_report() {
  local target="$1"

  local -a source_files=()
  discover_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DocCoverage]${NC} No source files found. Nothing to report."
    return 0
  fi

  FINDINGS=()
  TOTAL_PUBLIC_SYMBOLS=0
  DOCUMENTED_SYMBOLS=0
  local files_scanned=0

  for file in "${source_files[@]}"; do
    files_scanned=$((files_scanned + 1))
    scan_file "$file"
  done

  # Scan README and project files
  if [[ -d "$target" ]]; then
    scan_readme "$target"
    scan_project_files "$target"
  fi

  local doc_score
  doc_score=$(calculate_score)
  local grade
  grade=$(get_grade "$doc_score")

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

  local template_path="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_path" ]]; then
    echo -e "${RED}[DocCoverage]${NC} Report template not found at $template_path"
    return 1
  fi

  local report
  report=$(cat "$template_path")

  local report_date
  report_date=$(date +"%Y-%m-%d %H:%M:%S")

  # Coverage percentage
  local coverage_pct=0
  if [[ $TOTAL_PUBLIC_SYMBOLS -gt 0 ]]; then
    coverage_pct=$(( (DOCUMENTED_SYMBOLS * 100) / TOTAL_PUBLIC_SYMBOLS ))
  fi

  # Build findings table
  local findings_table=""
  if [[ $total -gt 0 ]]; then
    local idx=0
    for finding in "${FINDINGS[@]}"; do
      idx=$((idx + 1))
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"
      local lang
      lang=$(detect_language "$f_file")
      local lang_lbl
      lang_lbl=$(language_label "$lang")
      findings_table+="| $idx | \`$(basename "$f_file")\` | $f_line | **$f_severity** | $f_check | $f_desc | $lang_lbl |"$'\n'
    done
  fi

  # Build recommendations
  local recommendations_md=""
  if [[ $critical -gt 0 ]]; then
    recommendations_md+="- **URGENT:** $critical critical documentation gap(s). Public API completely undocumented. Fix immediately."$'\n'
  fi
  if [[ $high -gt 0 ]]; then
    recommendations_md+="- **HIGH PRIORITY:** $high high severity issue(s). Documentation present but incomplete."$'\n'
  fi
  if [[ $medium -gt 0 ]]; then
    recommendations_md+="- **REVIEW:** $medium medium severity issue(s). Project-level doc gaps or quality issues."$'\n'
  fi
  if [[ $total -eq 0 ]]; then
    recommendations_md="No action items. All public symbols are documented."
  fi

  # Perform substitutions
  report="${report//\{\{DATE\}\}/$report_date}"
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{QUALITY_SCORE\}\}/$doc_score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$files_scanned}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$critical}"
  report="${report//\{\{HIGH_COUNT\}\}/$high}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$medium}"
  report="${report//\{\{LOW_COUNT\}\}/$low}"
  report="${report//\{\{COVERAGE_PCT\}\}/$coverage_pct}"
  report="${report//\{\{DOCUMENTED_SYMBOLS\}\}/$DOCUMENTED_SYMBOLS}"
  report="${report//\{\{TOTAL_SYMBOLS\}\}/$TOTAL_PUBLIC_SYMBOLS}"
  report="${report//\{\{VERSION\}\}/$DOCCOVERAGE_VERSION}"

  report=$(echo "$report" | awk -v findings="$findings_table" '{gsub(/\{\{FINDINGS_TABLE\}\}/, findings); print}')
  report=$(echo "$report" | awk -v recs="$recommendations_md" '{gsub(/\{\{RECOMMENDATIONS\}\}/, recs); print}')

  local output_file="doccoverage-report-$(date +%Y%m%d-%H%M%S).md"
  echo "$report" > "$output_file"

  echo -e "${GREEN}[DocCoverage]${NC} Report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:     $files_scanned"
  echo -e "  Doc coverage:      ${coverage_pct}% (${DOCUMENTED_SYMBOLS}/${TOTAL_PUBLIC_SYMBOLS})"
  echo -e "  Quality score:     $doc_score/100 (Grade: $grade)"
}

# -- Policy Enforcement --------------------------------------------------------

enforce_doc_policy() {
  local target="$1"

  echo -e "${BOLD}--- DocCoverage Policy Enforcement ---${NC}"
  echo ""

  local -a custom_policies=()

  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    if command -v python3 &>/dev/null; then
      local raw
      raw=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    policies = cfg.get('skills', {}).get('entries', {}).get('doccoverage', {}).get('config', {}).get('customPolicies', [])
    for p in policies:
        print(p.get('regex', '') + '|' + p.get('severity', 'medium') + '|CUSTOM|' + p.get('description', 'Custom policy') + '|Fix according to organization policy')
except: pass
" 2>/dev/null) || true

      while IFS= read -r policy; do
        [[ -n "$policy" ]] && custom_policies+=("$policy")
      done <<< "$raw"
    fi
  fi

  if [[ ${#custom_policies[@]} -gt 0 ]]; then
    echo -e "Custom policies loaded: ${CYAN}${#custom_policies[@]}${NC}"
  else
    echo -e "${DIM}No custom policies configured.${NC}"
    echo -e "Add custom policies in ${CYAN}~/.openclaw/openclaw.json${NC}:"
    echo -e "  ${DIM}doccoverage.config.customPolicies: [{ \"regex\": \"...\", \"severity\": \"high\", \"description\": \"...\" }]${NC}"
    echo ""
  fi

  local -a source_files=()
  discover_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DocCoverage]${NC} No source files found."
    return 0
  fi

  FINDINGS=()
  TOTAL_PUBLIC_SYMBOLS=0
  DOCUMENTED_SYMBOLS=0

  for file in "${source_files[@]}"; do
    scan_file "$file"

    # Also check custom policies
    for policy in "${custom_policies[@]:-}"; do
      [[ -z "$policy" ]] && continue
      IFS='|' read -r regex severity check_id description recommendation <<< "$policy"

      local matches
      matches=$(grep -nE "$regex" "$file" 2>/dev/null || true)
      if [[ -n "$matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local matched_text="${match_line#*:}"
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi
          FINDINGS+=("${file}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}")
        done <<< "$matches"
      fi
    done
  done

  # Also scan README
  if [[ -d "$target" ]]; then
    scan_readme "$target"
    scan_project_files "$target"
  fi

  echo -e "Scanned ${BOLD}${#source_files[@]}${NC} file(s) with ${CYAN}$(doccoverage_pattern_count)${NC} built-in + ${CYAN}${#custom_policies[@]}${NC} custom patterns"
  echo ""

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}All policies pass.${NC}"
    return 0
  fi

  echo -e "${BOLD}--- Policy Violations ---${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
  done

  local doc_score
  doc_score=$(calculate_score)
  print_scan_summary "${#source_files[@]}" "$doc_score"

  if [[ $doc_score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# -- CHANGELOG Verification ---------------------------------------------------

verify_changelog() {
  local target="$1"

  echo -e "${BOLD}--- DocCoverage CHANGELOG Verification ---${NC}"
  echo ""

  # Find changelog
  local changelog_path=""
  for candidate in "$target/CHANGELOG.md" "$target/CHANGELOG" "$target/HISTORY.md" "$target/HISTORY" "$target/CHANGES.md"; do
    if [[ -f "$candidate" ]]; then
      changelog_path="$candidate"
      break
    fi
  done

  if [[ -z "$changelog_path" ]]; then
    echo -e "${RED}[DocCoverage]${NC} No CHANGELOG.md or HISTORY.md found in ${BOLD}$target${NC}"
    echo -e "  Create a CHANGELOG.md following the Keep a Changelog format."
    echo -e "  Reference: ${CYAN}https://keepachangelog.com${NC}"
    return 1
  fi

  echo -e "Checking: ${BOLD}$changelog_path${NC}"
  echo ""

  FINDINGS=()
  local changelog_content
  changelog_content=$(cat "$changelog_path")
  local issues=0

  # Check for Unreleased section
  if ! echo "$changelog_content" | grep -qiE '(unreleased|upcoming)'; then
    FINDINGS+=("${changelog_path}|0|low|RD-008|CHANGELOG missing Unreleased section|Add an ## [Unreleased] section for upcoming changes|No Unreleased section")
    issues=$((issues + 1))
  fi

  # Check for empty sections
  local prev_was_heading=false
  local prev_heading_line=0
  local current_line=0
  while IFS= read -r line; do
    current_line=$((current_line + 1))
    if echo "$line" | grep -qE '^#+[[:space:]]'; then
      if [[ "$prev_was_heading" == true ]]; then
        FINDINGS+=("${changelog_path}|${prev_heading_line}|medium|RD-010|Empty section in CHANGELOG|Fill in the section or remove it|Empty section at line ${prev_heading_line}")
        issues=$((issues + 1))
      fi
      prev_was_heading=true
      prev_heading_line=$current_line
    elif [[ -n "$(echo "$line" | tr -d '[:space:]')" ]]; then
      prev_was_heading=false
    fi
  done < "$changelog_path"

  # Check for date format consistency
  local date_entries
  date_entries=$(grep -nE '^#+.*[0-9]{4}' "$changelog_path" 2>/dev/null || true)
  if [[ -n "$date_entries" ]]; then
    local bad_dates
    bad_dates=$(echo "$date_entries" | grep -vE '[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)
    if [[ -n "$bad_dates" ]]; then
      while IFS= read -r bad_line; do
        [[ -z "$bad_line" ]] && continue
        local ln="${bad_line%%:*}"
        FINDINGS+=("${changelog_path}|${ln}|low|RD-008|CHANGELOG date format inconsistent (use YYYY-MM-DD)|Standardize dates to ISO 8601 format: YYYY-MM-DD|${bad_line#*:}")
        issues=$((issues + 1))
      done <<< "$bad_dates"
    fi
  fi

  # Check if recent git tags have changelog entries
  if git rev-parse --git-dir &>/dev/null 2>&1; then
    local recent_tags
    recent_tags=$(git tag --sort=-creatordate 2>/dev/null | head -5)
    if [[ -n "$recent_tags" ]]; then
      while IFS= read -r tag; do
        [[ -z "$tag" ]] && continue
        local clean_tag
        clean_tag=$(echo "$tag" | sed 's/^v//')
        if ! echo "$changelog_content" | grep -qF "$clean_tag"; then
          FINDINGS+=("${changelog_path}|0|medium|RD-008|Git tag '${tag}' has no corresponding CHANGELOG entry|Add entry for version ${tag} in CHANGELOG|Missing entry for tag ${tag}")
          issues=$((issues + 1))
        fi
      done <<< "$recent_tags"
    fi
  fi

  # Print results
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}CHANGELOG looks good! No issues found.${NC}"
    return 0
  fi

  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
  done

  echo -e "Found ${BOLD}$issues${NC} issue(s) in CHANGELOG"
}

# -- SARIF Output --------------------------------------------------------------

generate_sarif_output() {
  local target="$1"

  local -a source_files=()
  discover_source_files "$target" source_files

  if [[ ${#source_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[DocCoverage]${NC} No source files found."
    return 0
  fi

  FINDINGS=()
  TOTAL_PUBLIC_SYMBOLS=0
  DOCUMENTED_SYMBOLS=0

  for file in "${source_files[@]}"; do
    scan_file "$file"
  done

  if [[ -d "$target" ]]; then
    scan_readme "$target"
    scan_project_files "$target"
  fi

  local output_file="doccoverage-results-$(date +%Y%m%d-%H%M%S).sarif"

  {
    echo '{'
    echo '  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",'
    echo '  "version": "2.1.0",'
    echo '  "runs": [{'
    echo '    "tool": {'
    echo '      "driver": {'
    echo "        \"name\": \"DocCoverage\","
    echo "        \"version\": \"$DOCCOVERAGE_VERSION\","
    echo "        \"informationUri\": \"https://doccoverage.pages.dev\","
    echo "        \"semanticVersion\": \"$DOCCOVERAGE_VERSION\","
    echo '        "rules": ['

    local -A seen_rules=()
    local first_rule=true
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l f_severity f_check f_desc f_rec _t <<< "$finding"
      if [[ -z "${seen_rules[$f_check]:-}" ]]; then
        seen_rules[$f_check]=1
        local sarif_level
        case "$f_severity" in
          critical|high) sarif_level="error" ;;
          medium)        sarif_level="warning" ;;
          low)           sarif_level="note" ;;
          *)             sarif_level="none" ;;
        esac

        if [[ "$first_rule" != true ]]; then
          echo ','
        fi
        first_rule=false

        echo '          {'
        echo "            \"id\": \"$f_check\","
        echo "            \"shortDescription\": { \"text\": \"$f_desc\" },"
        echo "            \"helpUri\": \"https://doccoverage.pages.dev/rules/$f_check\","
        echo '            "defaultConfiguration": {'
        echo "              \"level\": \"$sarif_level\""
        echo '            },'
        echo '            "properties": {'
        echo "              \"tags\": [\"documentation\", \"coverage\"]"
        echo '            }'
        printf '          }'
      fi
    done

    echo ''
    echo '        ]'
    echo '      }'
    echo '    },'
    echo '    "results": ['

    local first_result=true
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"

      local sarif_level
      case "$f_severity" in
        critical|high) sarif_level="error" ;;
        medium)        sarif_level="warning" ;;
        low)           sarif_level="note" ;;
        *)             sarif_level="none" ;;
      esac

      local esc_desc
      esc_desc=$(echo "$f_desc" | sed 's/"/\\"/g')
      local esc_rec
      esc_rec=$(echo "$f_rec" | sed 's/"/\\"/g')

      if [[ "$first_result" != true ]]; then
        echo ','
      fi
      first_result=false

      local effective_line="$f_line"
      [[ "$effective_line" == "0" ]] && effective_line="1"

      echo '      {'
      echo "        \"ruleId\": \"$f_check\","
      echo "        \"level\": \"$sarif_level\","
      echo "        \"message\": { \"text\": \"$esc_desc. Fix: $esc_rec\" },"
      echo '        "locations": [{'
      echo '          "physicalLocation": {'
      echo "            \"artifactLocation\": { \"uri\": \"$f_file\" },"
      echo '            "region": {'
      echo "              \"startLine\": $effective_line"
      echo '            }'
      echo '          }'
      echo '        }]'
      printf '      }'
    done

    echo ''
    echo '    ]'
    echo '  }]'
    echo '}'
  } > "$output_file"

  echo -e "${GREEN}[DocCoverage]${NC} SARIF output generated: ${BOLD}$output_file${NC}"
  echo -e "  ${DIM}Compatible with GitHub Code Scanning, Azure DevOps, and SARIF viewers${NC}"
  echo -e "  Results: ${#FINDINGS[@]} finding(s) from ${#source_files[@]} file(s)"
}
