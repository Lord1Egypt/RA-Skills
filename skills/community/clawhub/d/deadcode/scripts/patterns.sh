#!/usr/bin/env bash
# DeadCode -- Dead Code Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Significant dead code that wastes resources or causes confusion
#   high     -- Unused exports, imports, or orphan files
#   medium   -- Commented-out code, empty bodies, minor cruft
#   low      -- TODOs, minor style issues, informational
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use literal quotes instead of \x27
# - Avoid Perl-only features (\d, \w, etc.)
#
# Patterns starting with PLACEHOLDER_ are handled by file-level checks
# in analyzer.sh, not by direct grep matching.

set -euo pipefail

# ============================================================================
# 1. JAVASCRIPT / TYPESCRIPT PATTERNS (DC-JS)
# ============================================================================

declare -a DEADCODE_JS_PATTERNS=()

DEADCODE_JS_PATTERNS+=(
  # --- Unused exports (file-level check) ---
  'PLACEHOLDER_UNUSED_EXPORT|critical|DC-JS-001|Exported function/class/constant never imported by any other file|Remove the unused export or verify it is consumed by an external package'

  # --- Orphan files (file-level check) ---
  'PLACEHOLDER_ORPHAN_FILE|high|DC-JS-002|File is never imported or required by any other file in the project|Delete the orphan file or add an import from a consuming module'

  # --- console.log / console.debug left in production code ---
  'console\.log[[:space:]]*\(|medium|DC-JS-003|console.log statement left in code|Remove console.log or replace with a proper logging framework'
  'console\.debug[[:space:]]*\(|medium|DC-JS-004|console.debug statement left in code|Remove console.debug or replace with a proper logging framework'
  'console\.warn[[:space:]]*\(|low|DC-JS-005|console.warn statement in code|Consider replacing with a structured logging framework'
  'console\.info[[:space:]]*\(|low|DC-JS-006|console.info statement in code|Consider replacing with a structured logging framework'

  # --- Commented-out code blocks ---
  '^[[:space:]]*//.*(function|const|let|var|class|import|export|return|if|for|while)[[:space:]]|medium|DC-JS-007|Commented-out code detected (single-line)|Remove commented-out code; it belongs in version control history'
  'PLACEHOLDER_LARGE_COMMENT_BLOCK_JS|medium|DC-JS-008|Large block of commented-out code (5+ lines)|Remove the commented-out block; use git history to recover if needed'

  # --- TODO / FIXME / HACK comments ---
  '//[[:space:]]*(TODO|FIXME|HACK|XXX|TEMP)[[:space:]:]|low|DC-JS-009|TODO/FIXME/HACK comment indicates incomplete or temporary code|Complete the TODO or file an issue and remove the comment'
  '/\*[[:space:]]*(TODO|FIXME|HACK|XXX|TEMP)[[:space:]:]|low|DC-JS-010|TODO/FIXME/HACK in block comment|Complete the TODO or file an issue and remove the comment'

  # --- Unreachable code after return/throw/break/continue ---
  'return[[:space:]]+[^;]*;[[:space:]]*[a-zA-Z]|high|DC-JS-011|Code appears after return statement on same line|Remove unreachable code after the return statement'
  'PLACEHOLDER_UNREACHABLE_AFTER_RETURN_JS|high|DC-JS-012|Code on lines after an unconditional return/throw in a block|Remove unreachable statements after return/throw'
  'throw[[:space:]]+new[[:space:]]+[A-Z].*;[[:space:]]*[a-zA-Z]|high|DC-JS-013|Code appears after throw statement on same line|Remove unreachable code after the throw statement'

  # --- Empty function bodies ---
  'function[[:space:]]+[a-zA-Z_$][a-zA-Z0-9_$]*[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}|medium|DC-JS-014|Empty function body (no-op)|Implement the function or remove it if unused'
  '=>[[:space:]]*\{[[:space:]]*\}|medium|DC-JS-015|Empty arrow function body|Implement the function or remove it if unused'

  # --- Unused variable declarations ---
  'PLACEHOLDER_UNUSED_VAR_JS|high|DC-JS-016|Variable declared but never referenced in the file|Remove the unused variable declaration'

  # --- Dead switch/case branches ---
  'case[[:space:]]+[^:]+:[[:space:]]*break[[:space:]]*;|medium|DC-JS-017|Switch case with only a break statement (empty case)|Add implementation or remove the dead case branch'
  'case[[:space:]]+[^:]+:[[:space:]]*$|medium|DC-JS-018|Switch case with no code (fall-through without comment)|Add implementation, a fall-through comment, or remove the case'

  # --- Deprecated markers ---
  '@deprecated|low|DC-JS-019|@deprecated JSDoc tag -- function/class marked for removal|Remove the deprecated code if no consumers remain'

  # --- Empty catch blocks ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}|medium|DC-JS-020|Empty catch block -- errors are silently swallowed|Add error handling, logging, or rethrow the error'
  'catch[[:space:]]*\{[[:space:]]*\}|medium|DC-JS-021|Empty catch block (no parameter) -- errors silently swallowed|Add error handling or logging in the catch block'

  # --- Triple-slash reference directives ---
  '///[[:space:]]*<reference[[:space:]]+path=|low|DC-JS-022|Triple-slash reference directive may be stale|Verify the reference is still needed; prefer import statements'
  '///[[:space:]]*<reference[[:space:]]+types=|low|DC-JS-023|Triple-slash types reference may be stale|Verify the types reference is needed; prefer tsconfig includes'

  # --- debugger statements ---
  '^[[:space:]]*debugger[[:space:]]*;|high|DC-JS-024|debugger statement left in code|Remove the debugger statement before committing'

  # --- Unused type/interface (TypeScript) ---
  'PLACEHOLDER_UNUSED_TYPE_TS|medium|DC-JS-025|TypeScript type or interface defined but never used in file|Remove the unused type definition or export it if needed elsewhere'

  # --- Alert statements ---
  'alert[[:space:]]*\(|medium|DC-JS-026|alert() call left in code|Remove alert() calls; use proper UI notifications instead'
)

# ============================================================================
# 2. PYTHON PATTERNS (DC-PY)
# ============================================================================

declare -a DEADCODE_PY_PATTERNS=()

DEADCODE_PY_PATTERNS+=(
  # --- Functions defined but never called (file-level check) ---
  'PLACEHOLDER_UNUSED_FUNC_PY|high|DC-PY-001|Function defined but never called within the module|Remove the unused function or verify it is imported by another module'

  # --- Unused imports ---
  'PLACEHOLDER_UNUSED_IMPORT_PY|high|DC-PY-002|Import statement where the imported name is never used in the file|Remove the unused import'

  # --- pass-only function/class bodies ---
  'def[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\([^)]*\)[[:space:]]*:[[:space:]]*$|medium|DC-PY-003|Function definition that may have a pass-only body|Implement the function or remove it if it is a placeholder'
  'PLACEHOLDER_PASS_ONLY_BODY|medium|DC-PY-004|Function or class body contains only pass (placeholder)|Implement the body or remove the placeholder definition'

  # --- Commented-out code blocks ---
  '^[[:space:]]*#.*(def |class |import |from |return |if |for |while )|medium|DC-PY-005|Commented-out Python code detected|Remove commented-out code; use git history to recover if needed'
  'PLACEHOLDER_LARGE_COMMENT_BLOCK_PY|medium|DC-PY-006|Large block of commented-out code (5+ lines)|Remove the commented-out block; use git history to recover'

  # --- Dead code after return/raise/break ---
  'PLACEHOLDER_UNREACHABLE_AFTER_RETURN_PY|high|DC-PY-007|Code after unconditional return/raise/break is unreachable|Remove the unreachable statements'

  # --- __all__ exports that don't match definitions (file-level check) ---
  'PLACEHOLDER_ALL_MISMATCH|medium|DC-PY-008|__all__ lists names not defined in the module|Update __all__ to match actual module definitions'

  # --- Empty except blocks ---
  'except[[:space:]]*:$|medium|DC-PY-009|Bare except clause -- catches all exceptions including SystemExit|Specify the exception type: except ValueError:'
  'except[[:space:]]+[A-Za-z]+[[:space:]]*:[[:space:]]*$|medium|DC-PY-010|Except clause with likely empty body|Add error handling or logging in the except block'
  'PLACEHOLDER_EMPTY_EXCEPT|medium|DC-PY-011|Empty except block -- exceptions are silently swallowed|Add error handling, logging, or re-raise the exception'

  # --- TODO/FIXME/HACK ---
  '#[[:space:]]*(TODO|FIXME|HACK|XXX|TEMP)[[:space:]:]|low|DC-PY-012|TODO/FIXME/HACK comment indicates incomplete code|Complete the TODO or file an issue and remove the comment'

  # --- Dead else branches ---
  'PLACEHOLDER_DEAD_ELSE_PY|low|DC-PY-013|Else branch that appears unreachable|Verify the else branch can be reached; remove if dead'

  # --- Duplicate function definitions ---
  'PLACEHOLDER_DUPLICATE_FUNC_PY|high|DC-PY-014|Function defined multiple times in the same file -- earlier definition is dead|Remove the duplicate function definition'

  # --- print() left in production code ---
  '^[[:space:]]*print[[:space:]]*\(|medium|DC-PY-015|print() statement left in code|Remove print() or replace with logging module'

  # --- pdb/breakpoint debugging ---
  'import[[:space:]]+pdb|high|DC-PY-016|pdb import left in code|Remove the pdb import before committing'
  'pdb\.set_trace[[:space:]]*\(|high|DC-PY-017|pdb.set_trace() left in code|Remove the debugger call before committing'
  'breakpoint[[:space:]]*\(|high|DC-PY-018|breakpoint() call left in code|Remove the breakpoint before committing'
)

# ============================================================================
# 3. GO PATTERNS (DC-GO)
# ============================================================================

declare -a DEADCODE_GO_PATTERNS=()

DEADCODE_GO_PATTERNS+=(
  # --- Unused imports (file-level check) ---
  'PLACEHOLDER_UNUSED_IMPORT_GO|high|DC-GO-001|Import not used in the file|Remove the unused import (Go compiler enforces this but stale vendor may remain)'

  # --- Exported functions never called (file-level check) ---
  'PLACEHOLDER_UNUSED_EXPORTED_FUNC|high|DC-GO-002|Exported function never referenced in tests or other packages|Remove the unused exported function or unexport it'

  # --- Dead code after return/panic ---
  'PLACEHOLDER_UNREACHABLE_AFTER_RETURN_GO|high|DC-GO-003|Code after unconditional return or panic is unreachable|Remove the unreachable statements'

  # --- Empty function bodies ---
  'func[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\([^)]*\)[[:space:]]*[^{]*\{[[:space:]]*\}|medium|DC-GO-004|Empty function body|Implement the function or remove it if unused'
  'func[[:space:]]*\([^)]*\)[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\([^)]*\)[[:space:]]*[^{]*\{[[:space:]]*\}|medium|DC-GO-005|Empty method body|Implement the method or remove it if unused'

  # --- Commented-out code blocks ---
  '^[[:space:]]*//.*(func |var |const |type |import |return |if |for |switch )|medium|DC-GO-006|Commented-out Go code detected|Remove commented-out code; use git history to recover'
  'PLACEHOLDER_LARGE_COMMENT_BLOCK_GO|medium|DC-GO-007|Large block of commented-out code (5+ lines)|Remove the commented-out block; use git history to recover'

  # --- Empty init() functions ---
  'func[[:space:]]+init[[:space:]]*\([[:space:]]*\)[[:space:]]*\{[[:space:]]*\}|medium|DC-GO-008|Empty init() function does nothing|Remove the empty init() function'
  'PLACEHOLDER_INIT_ONLY_COMMENT|medium|DC-GO-009|init() function body contains only comments|Remove the init() function or implement its intended behavior'

  # --- TODO/FIXME/HACK ---
  '//[[:space:]]*(TODO|FIXME|HACK|XXX|TEMP)[[:space:]:]|low|DC-GO-010|TODO/FIXME/HACK comment indicates incomplete code|Complete the TODO or file an issue and remove the comment'

  # --- fmt.Println debugging left in code ---
  'fmt\.Println[[:space:]]*\(|medium|DC-GO-011|fmt.Println left in code -- likely debug output|Remove fmt.Println or use a proper logging package'
  'fmt\.Printf[[:space:]]*\(|low|DC-GO-012|fmt.Printf left in code -- may be debug output|Verify fmt.Printf is intentional; consider a logging package'
  'log\.Println[[:space:]]*\(.*debug|low|DC-GO-013|Debug log statement left in code|Remove debug logging before release'

  # --- Unreachable code after os.Exit ---
  'os\.Exit[[:space:]]*\([^)]*\)[[:space:]]*$|medium|DC-GO-014|Code after os.Exit is unreachable|Remove unreachable code after os.Exit call'
)

# ============================================================================
# 4. CSS / SCSS PATTERNS (DC-CSS)
# ============================================================================

declare -a DEADCODE_CSS_PATTERNS=()

DEADCODE_CSS_PATTERNS+=(
  # --- Unused CSS selectors (file-level check, cross-reference with source) ---
  'PLACEHOLDER_UNUSED_SELECTOR|high|DC-CSS-001|CSS class or ID selector never referenced in HTML/JSX/TSX files|Remove the unused selector or verify it is applied dynamically'

  # --- Empty rule blocks ---
  '\{[[:space:]]*\}|medium|DC-CSS-002|Empty CSS rule block -- selector with no declarations|Remove the empty rule block or add declarations'

  # --- Duplicate selectors (file-level check) ---
  'PLACEHOLDER_DUPLICATE_SELECTOR|medium|DC-CSS-003|Same selector declared multiple times in file|Merge duplicate selectors into one rule block'

  # --- Commented-out styles ---
  '/\*.*\{.*\}.*\*/|low|DC-CSS-004|Commented-out CSS rule found|Remove commented-out CSS; use git history to recover'
  'PLACEHOLDER_LARGE_COMMENT_BLOCK_CSS|low|DC-CSS-005|Large block of commented-out CSS (5+ lines)|Remove the commented-out block'

  # --- !important overuse (file-level check) ---
  'PLACEHOLDER_IMPORTANT_OVERUSE|medium|DC-CSS-006|Excessive !important declarations (5+) in file|Refactor specificity instead of using !important'
  '!important|low|DC-CSS-007|Individual !important declaration|Consider fixing specificity instead of using !important'

  # --- Unused CSS custom properties / variables (file-level check) ---
  'PLACEHOLDER_UNUSED_CSS_VAR|high|DC-CSS-008|CSS custom property (--var) defined but never referenced with var()|Remove the unused CSS variable definition'

  # --- Empty media queries ---
  '@media[^{]*\{[[:space:]]*\}|medium|DC-CSS-009|Empty media query with no rules inside|Remove the empty media query or add rules'

  # --- Vendor prefixes when autoprefixer should handle them ---
  '-webkit-[a-z]+-[a-z]+|low|DC-CSS-010|Vendor prefix (-webkit-) may be unnecessary with autoprefixer|Remove vendor prefixes and let autoprefixer handle them'
  '-moz-[a-z]+-[a-z]+|low|DC-CSS-011|Vendor prefix (-moz-) may be unnecessary with autoprefixer|Remove vendor prefixes and let autoprefixer handle them'
  '-ms-[a-z]+-[a-z]+|low|DC-CSS-012|Vendor prefix (-ms-) may be unnecessary with autoprefixer|Remove vendor prefixes and let autoprefixer handle them'
  '-o-[a-z]+-[a-z]+|low|DC-CSS-013|Vendor prefix (-o-) may be unnecessary with autoprefixer|Remove vendor prefixes and let autoprefixer handle them'

  # --- ID selectors (specificity smell) ---
  '#[a-zA-Z][a-zA-Z0-9_-]*[[:space:]]*\{|low|DC-CSS-014|ID selector used -- high specificity can lead to !important usage|Prefer class selectors for maintainability'
)

# ============================================================================
# 5. GENERAL / CROSS-LANGUAGE PATTERNS (DC-GEN)
# ============================================================================

declare -a DEADCODE_GENERAL_PATTERNS=()

DEADCODE_GENERAL_PATTERNS+=(
  # --- Orphan files (file-level check) ---
  'PLACEHOLDER_ORPHAN_FILE_GEN|high|DC-GEN-001|File not imported or referenced by any other file in the project|Delete the orphan file or add a reference from a consuming module'

  # --- Large commented-out blocks (file-level check, 10+ lines) ---
  'PLACEHOLDER_LARGE_COMMENT_BLOCK_GEN|medium|DC-GEN-002|10+ consecutive comment lines -- likely commented-out code|Remove the large commented-out block; use git history instead'

  # --- TODO/FIXME/HACK density (file-level check, 5+ per file) ---
  'PLACEHOLDER_TODO_DENSITY|medium|DC-GEN-003|More than 5 TODO/FIXME/HACK comments in this file|Resolve TODOs or convert them to tracked issues'

  # --- Debug/test code left in production files ---
  'console\.trace[[:space:]]*\(|high|DC-GEN-004|console.trace() left in code|Remove console.trace() before deployment'
  'console\.table[[:space:]]*\(|medium|DC-GEN-005|console.table() left in code|Remove console.table() before deployment'
  'console\.count[[:space:]]*\(|medium|DC-GEN-006|console.count() left in code|Remove console.count() before deployment'
  'console\.time[[:space:]]*\(|medium|DC-GEN-007|console.time() / console.timeEnd() left in code|Remove performance timing calls before deployment'
  'console\.timeEnd[[:space:]]*\(|medium|DC-GEN-008|console.timeEnd() left in code|Remove performance timing calls before deployment'

  # --- Feature flag remnants ---
  'FEATURE_FLAG.*=.*false|medium|DC-GEN-009|Feature flag set to false -- possibly a remnant of a removed feature|Remove the dead feature flag and associated code paths'
  'FEATURE_FLAG.*=.*true|low|DC-GEN-010|Feature flag set to true -- possibly a fully rolled-out feature|Remove the feature flag and keep only the enabled code path'
  'feature[[:space:]]*=[[:space:]]*false|low|DC-GEN-011|Possible feature toggle set to false|Review whether this feature flag is still needed'

  # --- Placeholder text ---
  'lorem[[:space:]]+ipsum|low|DC-GEN-012|Lorem ipsum placeholder text found|Replace placeholder text with real content'
  'TODO:[[:space:]]*implement|medium|DC-GEN-013|TODO: implement placeholder found|Implement the functionality or remove the placeholder'
  'FIXME:[[:space:]]*implement|medium|DC-GEN-014|FIXME: implement placeholder found|Implement the functionality or remove the placeholder'
  'throw[[:space:]]+new[[:space:]]+Error[[:space:]]*\([[:space:]]*["\x27]not[[:space:]]+implemented|medium|DC-GEN-015|Not implemented error thrown -- placeholder code|Implement the functionality or remove the placeholder'
  'raise[[:space:]]+NotImplementedError|medium|DC-GEN-016|NotImplementedError raised -- placeholder code|Implement the functionality or remove the placeholder'
  'panic[[:space:]]*\([[:space:]]*"not[[:space:]]+implemented|medium|DC-GEN-017|Panic with not implemented -- placeholder code|Implement the functionality or remove the placeholder'

  # --- Dead code markers in comments ---
  '//[[:space:]]*DEAD[[:space:]]*CODE|high|DC-GEN-018|Code explicitly marked as DEAD CODE|Remove the dead code that is already identified'
  '#[[:space:]]*DEAD[[:space:]]*CODE|high|DC-GEN-019|Code explicitly marked as DEAD CODE|Remove the dead code that is already identified'
  '//[[:space:]]*UNUSED|medium|DC-GEN-020|Code explicitly marked as UNUSED|Remove the unused code'
  '#[[:space:]]*UNUSED|medium|DC-GEN-021|Code explicitly marked as UNUSED|Remove the unused code'

  # --- Stale test artifacts ---
  '\.skip[[:space:]]*\(|low|DC-GEN-022|Skipped test found (.skip()) -- may be dead test code|Re-enable or remove the skipped test'
  'xit[[:space:]]*\(|low|DC-GEN-023|Disabled Jasmine test (xit) found|Re-enable or remove the disabled test'
  'xdescribe[[:space:]]*\(|low|DC-GEN-024|Disabled Jasmine suite (xdescribe) found|Re-enable or remove the disabled test suite'
  '@pytest\.mark\.skip|low|DC-GEN-025|Skipped pytest test found|Re-enable or remove the skipped test'
  't\.Skip[[:space:]]*\(|low|DC-GEN-026|Skipped Go test found (t.Skip)|Re-enable or remove the skipped test'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all language categories
deadcode_pattern_count() {
  local count=0
  count=$((count + ${#DEADCODE_JS_PATTERNS[@]}))
  count=$((count + ${#DEADCODE_PY_PATTERNS[@]}))
  count=$((count + ${#DEADCODE_GO_PATTERNS[@]}))
  count=$((count + ${#DEADCODE_CSS_PATTERNS[@]}))
  count=$((count + ${#DEADCODE_GENERAL_PATTERNS[@]}))
  echo "$count"
}

# List patterns by language category
deadcode_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    JS)       _patterns_ref=DEADCODE_JS_PATTERNS ;;
    PY)       _patterns_ref=DEADCODE_PY_PATTERNS ;;
    GO)       _patterns_ref=DEADCODE_GO_PATTERNS ;;
    CSS)      _patterns_ref=DEADCODE_CSS_PATTERNS ;;
    GENERAL)  _patterns_ref=DEADCODE_GENERAL_PATTERNS ;;
    all)
      deadcode_list_patterns "JS"
      deadcode_list_patterns "PY"
      deadcode_list_patterns "GO"
      deadcode_list_patterns "CSS"
      deadcode_list_patterns "GENERAL"
      return
      ;;
    *)
      echo "Unknown language category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    # Skip placeholder patterns
    [[ "$regex" == PLACEHOLDER_* ]] && continue
    printf "%-12s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a language category
get_patterns_for_lang() {
  local lang_type="$1"
  case "$lang_type" in
    js)       echo "DEADCODE_JS_PATTERNS" ;;
    py)       echo "DEADCODE_PY_PATTERNS" ;;
    go)       echo "DEADCODE_GO_PATTERNS" ;;
    css)      echo "DEADCODE_CSS_PATTERNS" ;;
    general)  echo "DEADCODE_GENERAL_PATTERNS" ;;
    *)        echo "" ;;
  esac
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}
