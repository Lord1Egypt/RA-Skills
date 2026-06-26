#!/usr/bin/env bash
# DocCoverage -- Documentation Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Public API completely undocumented
#   high     -- Documentation present but incomplete
#   medium   -- Project-level doc gap or best practice violation
#   low      -- Informational, improvement opportunity
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, etc.)

set -euo pipefail

# -- Pattern registries by documentation category ----------------------------
#
# Format: "regex|severity|check_id|description|recommendation"
# Patterns use POSIX extended grep regex (ERE) syntax.

# ===========================================================================
# 1. MISSING FUNCTION/METHOD DOCS (20 patterns)
# ===========================================================================

declare -a DOCCOVERAGE_MISSING_PATTERNS=()

DOCCOVERAGE_MISSING_PATTERNS+=(
  # JS/TS -- exported function without JSDoc
  'CONTEXT_CHECK_JSDOC_EXPORT_FUNCTION|critical|MD-001|Exported function without JSDoc comment (JS/TS)|Add JSDoc block before exported function: /** @param {type} name - description */'

  # JS/TS -- exported const arrow function without JSDoc
  'CONTEXT_CHECK_JSDOC_EXPORT_CONST|critical|MD-002|Exported const/arrow function without JSDoc (JS/TS)|Add JSDoc block before exported const: /** @description ... */'

  # JS/TS -- exported class without JSDoc
  'CONTEXT_CHECK_JSDOC_EXPORT_CLASS|critical|MD-003|Exported class without JSDoc comment (JS/TS)|Add JSDoc block before exported class: /** @class Description */'

  # Python -- public function without docstring
  'CONTEXT_CHECK_PYTHON_DOCSTRING_FUNC|critical|MD-004|Public function without docstring (Python)|Add docstring after def: """Description of function."""'

  # Python -- public class without docstring
  'CONTEXT_CHECK_PYTHON_DOCSTRING_CLASS|critical|MD-005|Public class without docstring (Python)|Add docstring after class: """Description of class."""'

  # Python -- __init__ without docstring
  'CONTEXT_CHECK_PYTHON_INIT_DOCSTRING|medium|MD-006|__init__ method without docstring (Python)|Add docstring to __init__: """Initialize ClassName with parameters."""'

  # Python -- public method without docstring
  'CONTEXT_CHECK_PYTHON_METHOD_DOCSTRING|high|MD-007|Public method without docstring (Python)|Add docstring after def: """Description of method."""'

  # Go -- exported function without godoc comment
  'CONTEXT_CHECK_GO_FUNC_DOC|critical|MD-008|Exported function without godoc comment (Go)|Add comment before function: // FuncName does something.'

  # Go -- exported type without godoc comment
  'CONTEXT_CHECK_GO_TYPE_DOC|high|MD-009|Exported type without godoc comment (Go)|Add comment before type: // TypeName represents something.'

  # Go -- exported method without godoc comment
  'CONTEXT_CHECK_GO_METHOD_DOC|high|MD-010|Exported method without godoc comment (Go)|Add comment before method: // MethodName does something.'

  # Java -- public method without Javadoc
  'CONTEXT_CHECK_JAVA_METHOD_DOC|critical|MD-011|Public method without Javadoc (Java)|Add Javadoc before method: /** Description. @param name description @return description */'

  # Java -- public class without Javadoc
  'CONTEXT_CHECK_JAVA_CLASS_DOC|critical|MD-012|Public class without Javadoc (Java)|Add Javadoc before class: /** Description of class. */'

  # Java -- public constructor without Javadoc
  'CONTEXT_CHECK_JAVA_CONSTRUCTOR_DOC|medium|MD-013|Public constructor without Javadoc (Java)|Add Javadoc before constructor: /** Creates a new instance. @param name description */'

  # Ruby -- public method without YARD doc
  'CONTEXT_CHECK_RUBY_METHOD_DOC|critical|MD-014|Public method without YARD doc (Ruby)|Add YARD doc before method: # Description of method'

  # Ruby -- class without YARD doc
  'CONTEXT_CHECK_RUBY_CLASS_DOC|high|MD-015|Class without YARD doc (Ruby)|Add YARD doc before class: # Description of class'

  # Ruby -- module without YARD doc
  'CONTEXT_CHECK_RUBY_MODULE_DOC|high|MD-016|Module without YARD doc (Ruby)|Add YARD doc before module: # Description of module'

  # JS/TS -- React component without prop docs
  'CONTEXT_CHECK_REACT_PROP_DOCS|medium|MD-017|Exported React component without prop descriptions (JS/TS)|Document component props with JSDoc or PropTypes descriptions'

  # TS -- interface members without doc comments
  'CONTEXT_CHECK_TS_INTERFACE_MEMBER_DOC|medium|MD-018|TypeScript interface member without doc comment|Add doc comment before interface member: /** Description */'

  # Python -- abstract method without docstring
  'CONTEXT_CHECK_PYTHON_ABSTRACT_DOC|medium|MD-019|Abstract method without docstring (Python)|Add docstring to abstract method for implementors'

  # Go -- exported constant/variable without godoc
  'CONTEXT_CHECK_GO_CONST_DOC|low|MD-020|Exported const/var without godoc comment (Go)|Add comment before const/var: // ConstName is the description.'
)

# ===========================================================================
# 2. INCOMPLETE DOCUMENTATION (18 patterns)
# ===========================================================================

declare -a DOCCOVERAGE_INCOMPLETE_PATTERNS=()

DOCCOVERAGE_INCOMPLETE_PATTERNS+=(
  # JSDoc missing @param tags
  'CONTEXT_CHECK_JSDOC_MISSING_PARAM|high|ID-001|JSDoc present but missing @param tag(s) (JS/TS)|Add @param {type} name - description for each parameter'

  # JSDoc missing @returns
  'CONTEXT_CHECK_JSDOC_MISSING_RETURNS|high|ID-002|JSDoc present but missing @returns tag (JS/TS)|Add @returns {type} description for non-void functions'

  # Python docstring missing Args section
  'CONTEXT_CHECK_PYTHON_MISSING_ARGS|high|ID-003|Docstring present but missing Args section (Python)|Add Args: section listing each parameter and its description'

  # Python docstring missing Returns section
  'CONTEXT_CHECK_PYTHON_MISSING_RETURNS|high|ID-004|Docstring present but missing Returns section (Python)|Add Returns: section describing the return value'

  # @deprecated without replacement info
  '@deprecated[[:space:]]*$|medium|ID-005|@deprecated tag without replacement information|Add replacement info: @deprecated Use newFunction() instead'
  '@deprecated[[:space:]]*\*/|medium|ID-006|@deprecated tag without replacement information (end of block)|Specify what to use instead: @deprecated Use alternative() instead'

  # Missing @throws/@raises
  'CONTEXT_CHECK_MISSING_THROWS|medium|ID-007|Function throws exceptions but JSDoc/@raises missing|Document exceptions: @throws {ErrorType} description'

  # Generic placeholder docs
  'TODO:[[:space:]]*document|medium|ID-008|Placeholder documentation (TODO: document)|Replace TODO with actual documentation'
  'FIXME:[[:space:]]*add[[:space:]]*(docs|documentation)|medium|ID-009|Placeholder documentation (FIXME: add docs)|Replace FIXME with actual documentation'
  'XXX:[[:space:]]*needs?[[:space:]]*(docs|documentation)|medium|ID-010|Placeholder documentation (XXX: needs docs)|Replace XXX placeholder with actual documentation'

  # Copy-paste docs (identical docstrings)
  'CONTEXT_CHECK_DUPLICATE_DOCS|medium|ID-011|Duplicate documentation detected (copy-paste docs)|Write unique documentation for each function/method'

  # @param with wrong name
  'CONTEXT_CHECK_PARAM_NAME_MISMATCH|high|ID-012|@param name does not match function parameter|Update @param name to match actual parameter name'

  # Missing @example on public API
  'CONTEXT_CHECK_MISSING_EXAMPLE|low|ID-013|Public API function without @example section|Add @example showing typical usage of this function'

  # Java Javadoc missing @param
  'CONTEXT_CHECK_JAVADOC_MISSING_PARAM|high|ID-014|Javadoc present but missing @param tag(s) (Java)|Add @param name description for each parameter'

  # Java Javadoc missing @return
  'CONTEXT_CHECK_JAVADOC_MISSING_RETURN|high|ID-015|Javadoc present but missing @return tag (Java)|Add @return description for non-void methods'

  # Ruby YARD missing @param
  'CONTEXT_CHECK_YARD_MISSING_PARAM|high|ID-016|YARD doc present but missing @param tag(s) (Ruby)|Add @param [Type] name description for each parameter'

  # Ruby YARD missing @return
  'CONTEXT_CHECK_YARD_MISSING_RETURN|high|ID-017|YARD doc present but missing @return tag (Ruby)|Add @return [Type] description for return value'

  # Go godoc missing parameter description
  'CONTEXT_CHECK_GODOC_MISSING_PARAM_DESC|medium|ID-018|Godoc comment does not describe function parameters (Go)|Include parameter descriptions in the godoc comment'
)

# ===========================================================================
# 3. README & PROJECT DOCS (15 patterns)
# ===========================================================================

declare -a DOCCOVERAGE_README_PATTERNS=()

DOCCOVERAGE_README_PATTERNS+=(
  # Missing README.md
  'FILE_CHECK_MISSING_README|high|RD-001|No README.md found in project root|Create a README.md with at minimum: project description, installation, and usage sections'

  # README without installation section
  'SECTION_CHECK_README_INSTALL|medium|RD-002|README.md missing installation/setup section|Add an ## Installation or ## Getting Started section'

  # README without usage section
  'SECTION_CHECK_README_USAGE|medium|RD-003|README.md missing usage section|Add a ## Usage section with examples'

  # README without API section for libraries
  'SECTION_CHECK_README_API|medium|RD-004|Library README.md missing API documentation section|Add an ## API section documenting the public interface'

  # README with broken internal links
  'LINK_CHECK_README_BROKEN|medium|RD-005|README.md contains broken internal link(s)|Fix or remove broken links in README.md'

  # Missing CONTRIBUTING.md for open source
  'FILE_CHECK_MISSING_CONTRIBUTING|low|RD-006|No CONTRIBUTING.md found (recommended for open source)|Create a CONTRIBUTING.md with contribution guidelines'

  # Missing LICENSE file
  'FILE_CHECK_MISSING_LICENSE|medium|RD-007|No LICENSE file found in project root|Add a LICENSE file specifying the project license'

  # Missing CHANGELOG
  'FILE_CHECK_MISSING_CHANGELOG|medium|RD-008|No CHANGELOG.md or HISTORY.md found|Create a CHANGELOG.md following Keep a Changelog format'

  # Outdated badges in README
  'BADGE_CHECK_README_OUTDATED|low|RD-009|README.md may contain outdated or broken badge URLs|Verify badge URLs point to correct CI/CD and status endpoints'

  # Empty sections in README
  'SECTION_CHECK_README_EMPTY|medium|RD-010|README.md contains empty section(s)|Fill in empty sections or remove them if not applicable'

  # README missing description/title
  'SECTION_CHECK_README_TITLE|low|RD-011|README.md missing project title or description|Add a clear project title and one-line description at the top'

  # README missing license mention
  'SECTION_CHECK_README_LICENSE_REF|low|RD-012|README.md does not reference the project license|Add a ## License section referencing your LICENSE file'

  # README too short (under 10 lines)
  'LENGTH_CHECK_README_SHORT|low|RD-013|README.md is very short (fewer than 10 lines)|Expand README with installation, usage, and API sections'

  # Missing code of conduct
  'FILE_CHECK_MISSING_COC|low|RD-014|No CODE_OF_CONDUCT.md found (recommended for open source)|Add a CODE_OF_CONDUCT.md for community projects'

  # Missing .github templates (issue/PR)
  'FILE_CHECK_MISSING_TEMPLATES|low|RD-015|No issue/PR templates found in .github/|Add issue and PR templates for consistent contributions'
)

# ===========================================================================
# 4. API DOCUMENTATION (14 patterns)
# ===========================================================================

declare -a DOCCOVERAGE_API_PATTERNS=()

DOCCOVERAGE_API_PATTERNS+=(
  # REST endpoints without docs -- Express/Koa/Fastify
  'app\.(get|post|put|patch|delete)\([[:space:]]*["\x27/]|medium|AD-001|REST endpoint handler without documentation comment|Add JSDoc or comment above route handler describing endpoint, params, and response'

  # REST endpoints without docs -- Flask/Django
  '@app\.route\(|medium|AD-002|Flask route without docstring|Add docstring to route handler describing endpoint behavior and parameters'
  'path\([[:space:]]*["\x27].*view|medium|AD-003|Django URL pattern referencing view without docstring|Add docstring to view function/class describing endpoint'

  # GraphQL types without descriptions
  'type[[:space:]]+[A-Z][a-zA-Z]*[[:space:]]*\{|medium|AD-004|GraphQL type without description comment|Add description above GraphQL type: """Description of type"""'

  # OpenAPI missing descriptions
  'paths:[[:space:]]*$|medium|AD-005|OpenAPI spec detected -- verify all endpoints have descriptions|Ensure every path and operation has a description field'
  'schema:[[:space:]]*$|low|AD-006|OpenAPI schema detected -- verify all schemas have descriptions|Add description fields to all schema definitions'

  # gRPC service methods without comments
  'rpc[[:space:]]+[A-Z][a-zA-Z]*[[:space:]]*\(|medium|AD-007|gRPC service method without preceding comment|Add comment above rpc method describing its behavior and parameters'

  # Missing request/response examples
  'CONTEXT_CHECK_MISSING_API_EXAMPLE|low|AD-008|API endpoint without request/response examples|Add example requests and responses in documentation'

  # WebSocket events undocumented
  '\.on\([[:space:]]*["\x27][a-zA-Z]+["\x27]|low|AD-009|WebSocket event handler without documentation|Document WebSocket event: name, payload format, and expected behavior'

  # Missing error response documentation
  'CONTEXT_CHECK_MISSING_ERROR_DOCS|low|AD-010|API handler does not document error responses|Document possible error responses with status codes and error formats'

  # Missing authentication documentation
  'CONTEXT_CHECK_MISSING_AUTH_DOCS|medium|AD-011|API endpoint with auth middleware but no auth documentation|Document authentication requirements in endpoint documentation'

  # REST handler -- Go net/http
  'func[[:space:]]+[a-zA-Z]*Handler[[:space:]]*\(|medium|AD-012|Go HTTP handler without godoc comment|Add godoc comment describing the endpoint, method, path, and response'

  # REST handler -- Java Spring
  '@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)|medium|AD-013|Spring controller method without Javadoc|Add Javadoc describing endpoint behavior, parameters, and response'

  # REST handler -- Ruby Rails
  'def[[:space:]]+(index|show|create|update|destroy)[[:space:]]*$|medium|AD-014|Rails controller action without YARD doc|Add YARD doc above action describing endpoint behavior'
)

# ===========================================================================
# 5. TYPE & INTERFACE DOCS (10 patterns)
# ===========================================================================

declare -a DOCCOVERAGE_TYPE_PATTERNS=()

DOCCOVERAGE_TYPE_PATTERNS+=(
  # Exported TS interface without docs
  'CONTEXT_CHECK_TS_INTERFACE_DOC|medium|TD-001|Exported TypeScript interface without doc comment|Add JSDoc above interface: /** Description of interface */'

  # Exported TS type without docs
  'CONTEXT_CHECK_TS_TYPE_DOC|medium|TD-002|Exported TypeScript type alias without doc comment|Add JSDoc above type: /** Description of type */'

  # Enum values without descriptions
  'CONTEXT_CHECK_ENUM_VALUE_DOC|low|TD-003|Enum value(s) without description comments|Add comment for each enum value explaining its meaning'

  # Complex type alias without explanation
  'CONTEXT_CHECK_COMPLEX_TYPE_DOC|medium|TD-004|Complex type alias without explanatory comment|Add comment explaining what this type represents and when to use it'

  # Generic type parameters without docs
  'CONTEXT_CHECK_GENERIC_PARAM_DOC|low|TD-005|Generic type parameter(s) without @template doc|Add @template T - description for generic type parameters'

  # Union types without docs
  'CONTEXT_CHECK_UNION_TYPE_DOC|low|TD-006|Union type without doc comment explaining variants|Add comment explaining each variant in the union type'

  # Mapped types without docs
  'CONTEXT_CHECK_MAPPED_TYPE_DOC|low|TD-007|Mapped type without doc comment|Add JSDoc explaining the mapped type transformation'

  # Java enum without Javadoc
  'CONTEXT_CHECK_JAVA_ENUM_DOC|medium|TD-008|Public Java enum without Javadoc|Add Javadoc to enum class and individual constants'

  # Python TypedDict without docstring
  'CONTEXT_CHECK_PYTHON_TYPEDDICT_DOC|medium|TD-009|TypedDict class without docstring (Python)|Add docstring describing the typed dictionary fields'

  # Go struct fields without comments
  'CONTEXT_CHECK_GO_STRUCT_FIELD_DOC|low|TD-010|Exported struct field(s) without comment (Go)|Add comment for exported struct fields describing their purpose'
)

# ===========================================================================
# 6. COMMENT QUALITY (8+ patterns)
# ===========================================================================

declare -a DOCCOVERAGE_QUALITY_PATTERNS=()

DOCCOVERAGE_QUALITY_PATTERNS+=(
  # Obvious/redundant comments
  '//[[:space:]]*(increment|increase)[[:space:]]+(i|j|k|x|n|count|counter)[[:space:]]+(by[[:space:]]+1|by[[:space:]]+one)|low|QC-001|Obvious/redundant comment (describes what code clearly does)|Remove obvious comments; document why, not what'
  '//[[:space:]]*(set|assign)[[:space:]]+[a-zA-Z_]+[[:space:]]+to[[:space:]]|low|QC-002|Obvious assignment comment|Remove trivial assignment comments; document business logic instead'

  # Commented-out code blocks
  '^[[:space:]]*(//|#)[[:space:]]*(if|for|while|function|def|class|return|var|let|const|import)[[:space:]]|medium|QC-003|Commented-out code block detected|Remove commented-out code; use version control to track old code'

  # Outdated comments referencing non-existent functions
  'CONTEXT_CHECK_OUTDATED_COMMENT_REF|medium|QC-004|Comment references function/variable that does not exist|Update or remove outdated comment referencing non-existent symbol'

  # TODO without ticket/issue reference
  'TODO[[:space:]]*:|low|QC-005|TODO comment without ticket/issue reference|Add ticket reference: TODO(PROJ-123): description'
  'TODO[[:space:]]*\([[:space:]]*\)|low|QC-006|TODO with empty parentheses (no ticket reference)|Add ticket reference inside parentheses: TODO(PROJ-123)'

  # FIXME without context
  'FIXME[[:space:]]*:|low|QC-007|FIXME comment detected -- may indicate known bugs|Track FIXME items in issue tracker: FIXME(PROJ-456): description'

  # Comments in wrong language (heuristic: CJK in predominantly English codebase)
  'CONTEXT_CHECK_MIXED_LANGUAGE_COMMENTS|low|QC-008|Comments detected in multiple languages|Standardize comment language across the codebase for team readability'

  # Misleading comment heuristic (return vs comment)
  'CONTEXT_CHECK_MISLEADING_COMMENT|medium|QC-009|Comment may not match code behavior (potential misleading comment)|Review comment accuracy; ensure comments reflect actual code behavior'
)

# ===========================================================================
# Utility functions
# ===========================================================================

# Get total pattern count across all categories
doccoverage_pattern_count() {
  local count=0
  count=$((count + ${#DOCCOVERAGE_MISSING_PATTERNS[@]}))
  count=$((count + ${#DOCCOVERAGE_INCOMPLETE_PATTERNS[@]}))
  count=$((count + ${#DOCCOVERAGE_README_PATTERNS[@]}))
  count=$((count + ${#DOCCOVERAGE_API_PATTERNS[@]}))
  count=$((count + ${#DOCCOVERAGE_TYPE_PATTERNS[@]}))
  count=$((count + ${#DOCCOVERAGE_QUALITY_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
doccoverage_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    MISSING)      _patterns_ref=DOCCOVERAGE_MISSING_PATTERNS ;;
    INCOMPLETE)   _patterns_ref=DOCCOVERAGE_INCOMPLETE_PATTERNS ;;
    README)       _patterns_ref=DOCCOVERAGE_README_PATTERNS ;;
    API)          _patterns_ref=DOCCOVERAGE_API_PATTERNS ;;
    TYPE)         _patterns_ref=DOCCOVERAGE_TYPE_PATTERNS ;;
    QUALITY)      _patterns_ref=DOCCOVERAGE_QUALITY_PATTERNS ;;
    all)
      doccoverage_list_patterns "MISSING"
      doccoverage_list_patterns "INCOMPLETE"
      doccoverage_list_patterns "README"
      doccoverage_list_patterns "API"
      doccoverage_list_patterns "TYPE"
      doccoverage_list_patterns "QUALITY"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    # Skip context-check and file-check patterns (handled by analyzer)
    [[ "$regex" == CONTEXT_CHECK_* || "$regex" == FILE_CHECK_* || "$regex" == SECTION_CHECK_* || "$regex" == LINK_CHECK_* || "$regex" == BADGE_CHECK_* || "$regex" == LENGTH_CHECK_* ]] && continue
    printf "%-8s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a documentation category
get_patterns_for_category() {
  local category="$1"
  case "$category" in
    missing)      echo "DOCCOVERAGE_MISSING_PATTERNS" ;;
    incomplete)   echo "DOCCOVERAGE_INCOMPLETE_PATTERNS" ;;
    readme)       echo "DOCCOVERAGE_README_PATTERNS" ;;
    api)          echo "DOCCOVERAGE_API_PATTERNS" ;;
    type)         echo "DOCCOVERAGE_TYPE_PATTERNS" ;;
    quality)      echo "DOCCOVERAGE_QUALITY_PATTERNS" ;;
    *)            echo "" ;;
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

# Category display label from check ID
category_label_from_id() {
  local check_id="$1"
  local prefix="${check_id%%-*}"
  case "$prefix" in
    MD) echo "Missing Docs" ;;
    ID) echo "Incomplete Docs" ;;
    RD) echo "README/Project" ;;
    AD) echo "API Docs" ;;
    TD) echo "Type/Interface" ;;
    QC) echo "Comment Quality" ;;
    *)  echo "Unknown" ;;
  esac
}
