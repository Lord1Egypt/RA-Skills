---
name: cross-branch-audit
description: A universal cross-branch migration audit tool. When users need to migrate a module or specific feature from one branch to another, use this skill for pre-migration audit. Supports three input modes: (1) Module Path Mode — analyzes all commits under a specified directory; (2) Feature Mode — locates feature-related commits via keywords/commit lists/time range + author; (3) Hybrid Mode — module path + feature keywords combined. It automatically identifies commits involving external files, determines dependency types (strong/weak/resource/transitive), evaluates four-level conflict risk (🟢🟡🔴⚫), and generates an interactive HTML audit report with a critical-risk alert panel. Also supports incremental audit during migration (quick diagnosis of compilation errors) and provides a post-cherry-pick checklist. Applicable to projects of any language and framework. Trigger words: cross-branch audit, module migration analysis, commit dependency analysis, migration audit, cross-branch migration, module migration, branch migration, feature migration, cherry-pick analysis, feature audit, migration compilation error, migration conflict analysis, 跨分支审计, 模块迁移分析, commit依赖分析, 迁移审计, 跨分支迁移, 模块迁移, 分支迁移, 功能迁移, cherry-pick分析, 功能审计, 迁移编译错误, 迁移冲突分析.
---

# Cross-Branch Migration Audit Skill (Universal)

## Overview

This skill performs comprehensive pre-migration audits before cross-branch code migration. It analyzes git history, diff content, and code semantics to automatically identify external dependencies, evaluate migration risks, and generate structured audit reports.

**Applicable to any language, any framework, any project type.**

**Important**: Generate all output (reports, suggestions, checklists) in the user's preferred language. If the user communicates in Chinese, output in Chinese. If in English, output in English.

## Use Cases

- Migrating a feature module from one long-diverged branch to another
- Porting a feature (possibly spanning multiple directories) from one branch to another
- Two branches cannot be directly `git merge`d — need to precisely identify migration scope
- Evaluating migration workload and risk
- Determining cherry-pick order and strategy
- Pre-judging which files will conflict and how severe the conflicts will be

## Three Input Modes

### Mode A: Module Path Mode

**Use when**: Migrating a complete directory/module with clear boundaries.

**Input**:
- Source branch, target branch
- Module path(s) (one or more directories)

**Characteristics**:
- Automatically scans all commits under the path
- Highest coverage, no omissions
- Best for whole-module migration

### Mode B: Feature Mode

**Use when**: Migrating a feature whose code is scattered across multiple directories, composed of multiple commits.

**Input** (any combination):
- Exact commit list (user-known SHAs)
- Feature keywords (for searching commit messages)
- Time range + author
- TAPD/Jira/Issue ID

**Characteristics**:
- Uses multi-strategy cross-validation to find all related commits
- Requires human confirmation of commit range completeness
- Best for feature porting

### Mode C: Hybrid Mode

**Use when**: Primarily module-path based, but need to also capture module-external related changes.

**Input**:
- Module path + feature keywords
- First scan by path, then supplement with keyword search for external commits

## Execution Flow

### Step 0: Environment Detection & Project Identification

Before starting the audit, automatically detect the project type to use correct dependency analysis strategies:

```bash
# Detect project type
ls -la  # Check root directory structure

# Identify by characteristic files:
# - build.gradle / settings.gradle → Android/Java/Kotlin (Gradle)
# - pom.xml → Java/Kotlin (Maven)
# - package.json → JavaScript/TypeScript (Node.js)
# - go.mod → Go
# - Cargo.toml → Rust
# - requirements.txt / setup.py / pyproject.toml → Python
# - Podfile / *.xcodeproj → iOS (Swift/ObjC)
# - CMakeLists.txt → C/C++
# - *.sln / *.csproj → C# (.NET)
# - mix.exs → Elixir
# - Gemfile → Ruby
```

Also detect **multi-channel/multi-flavor structure**:
```bash
# Check for flavor/variant structure (Android)
grep -r "productFlavors" --include="*.gradle" . | head -5

# Check for multi-environment config (Node.js)
ls .env* 2>/dev/null

# Check for multiple targets (iOS)
grep -c "target" *.xcodeproj/project.pbxproj 2>/dev/null
```

Record project type and multi-channel structure for subsequent steps.

### Step 1: Confirm Input Parameters

Confirm the following with the user:

**Required parameters**:
- **Source branch**: The branch with complete feature
- **Target branch**: The branch that needs to receive the code

**Mode-specific parameters**:

| Mode | Parameters to confirm |
|------|----------------------|
| A (Module Path) | Module path(s), e.g., `src/audio/`, `lib/player/` |
| B (Feature) | Commit list / keywords / time range + author / Issue ID |
| C (Hybrid) | Module path + feature keywords |

**Optional parameters**:
- **Start commit**: Analysis starting point, defaults to merge-base of two branches
- **Exclude paths**: Directories to skip (e.g., `test/`, `docs/`)
- **Watch paths**: User-known external directories that may be affected

### Step 2: Determine Commit Range

#### Mode A: Path Scan

```bash
# Get merge-base of two branches
git merge-base origin/<source-branch> origin/<target-branch>

# Get all commits on source branch for the target module (exclude merges)
git log <start-commit>..origin/<source-branch> --oneline --no-merges -- <module-path-1> <module-path-2> ...
```

#### Mode B: Multi-Strategy Cross-Validation Commit Discovery

Execute the following strategies in order, merge and deduplicate:

**Strategy 1: Exact commit list** (if user provided)
```bash
git log --oneline <sha1> <sha2> <sha3> ...
```

**Strategy 2: Keyword search** (AI auto-expands keyword variants)
```bash
# User's original keyword
git log <start>..<source> --oneline --no-merges --grep="<keyword>"

# AI auto-expanded variants (translations, abbreviations, related concepts)
git log <start>..<source> --oneline --no-merges --grep="<variant1>"
git log <start>..<source> --oneline --no-merges --grep="<variant2>"
# ... merge and deduplicate
```

Keyword expansion rules:
- Chinese ↔ English translation (e.g., "支付" ↔ "payment")
- Abbreviation ↔ full name (e.g., "tts" ↔ "text to speech")
- Related concepts (e.g., "play" → "player", "pause", "resume")
- Module/class names (e.g., "PaymentService", "OrderHandler")

**Strategy 3: Time range + author**
```bash
git log <start>..<source> --oneline --no-merges --author="<author>" --since="<start-date>" --until="<end-date>"
```

**Strategy 4: Issue/TAPD ID search**
```bash
git log <start>..<source> --oneline --no-merges --grep="<issue-id>"
```

**Strategy 5: File path reverse tracking**
```bash
# Extract files from known commits
git diff-tree --no-commit-id -r --name-only <known-sha>

# Reverse-find other commits that modified these files
git log <start>..<source> --oneline --no-merges -- <file1> <file2> ...
```

**Strategy 6: Code reference chain analysis**
```bash
# From known core classes/functions, find all files that reference them
grep -rn "<CoreClassName>" --include="*.<ext>" . | grep -v build | grep -v node_modules

# Find commits that modified these referencing files
git log <start>..<source> --oneline --no-merges -- <referencing-files>
```

**After merging and deduplication, present to user for confirmation**:
```
I found N related commits through the following strategies:
- Keyword search ("payment", "order", "checkout"): found X
- File reverse tracking: additionally found Y
- Code reference chain: additionally found Z

Complete list:
1. abc1234 - feat: add payment processing
2. def5678 - fix: fix order validation
...

Please confirm if anything is missing. Provide additional info if needed.
```

#### Mode C: Hybrid Mode

Execute Mode A path scan first, then Mode B keyword search, merge and deduplicate.

### Step 3: Identify Commits Involving External Files

For each commit in the determined range, check if it involves files outside the migration scope:

```bash
for sha in <commit-list>; do
    all_files=$(git diff-tree --no-commit-id -r --name-only "$sha")
    external_files=$(echo "$all_files" | grep -v "^<module-path-pattern>")
    if [ -n "$external_files" ]; then
        echo "=== $sha ==="
        echo "$external_files"
    fi
done
```

For Feature Mode, the definition of "external files" needs dynamic determination:
- If user specified core paths → files outside core paths are external
- If no core path specified → analyze all files, cluster by directory, mark primary vs auxiliary change areas

### Step 4: Determine Dependency Strength

For each commit involving external files, run `git show <sha>` to examine diff content. Apply these **universal criteria**:

| Criterion | Classification | Explanation |
|-----------|---------------|-------------|
| External file adds symbols referenced by migrated code (class/function/variable/type) | **Strong dependency** | Migrated code compilation/runtime depends on this change |
| External file modifies function signature called by migrated code | **Strong dependency** | Signature mismatch causes compilation failure |
| External file references symbols within migration scope | **Strong dependency** | External code integrates migrated functionality |
| External file changes have no reference relationship with migrated code | **Weak dependency** | Unrelated changes in the same commit |
| External file is a build configuration file | **Infrastructure** | Module registration/dependency declaration |
| External file is a test file | **Test dependency** | Optional migration |
| External file is a resource file (strings/drawable/layout etc.) | **Resource dependency** | Check for duplicate definitions |

#### Language-Specific Reference Identification

Based on project type detected in Step 0, use corresponding reference identification methods:

| Project Type | Reference Identification Method |
|-------------|-------------------------------|
| Java/Kotlin | `import` statements, class inheritance, interface implementation, method calls, constructor parameters |
| JavaScript/TypeScript | `import`/`require` statements, `export` declarations |
| Python | `import`/`from...import` statements |
| Go | `import` statements, package references |
| C/C++ | `#include` directives, function declarations/definitions |
| Rust | `use`/`mod` statements, `extern crate` |
| Swift/ObjC | `import`/`#import` statements |
| Ruby | `require`/`require_relative` statements |
| C# | `using` statements, namespace references |
| Generic | Filename/path string references in code |

### Step 5: Evaluate Conflict Risk

For each strongly-dependent external file, evaluate conflict risk:

```bash
# Get diff statistics between two branches
git diff origin/<target-branch> origin/<source-branch> --stat -- <file>

# Get file total lines (evaluate complexity)
wc -l <file>

# Check if target branch also modified this file (bidirectional = high conflict probability)
git log <start>..origin/<target-branch> --oneline --no-merges -- <file>

# Check line ending format (CR/LF/CRLF)
file <file>
```

Risk level determination:
- 🟢 **Low risk**: New file / diff < 50 lines / append-only changes / target branch unmodified
- 🟡 **Medium risk**: 50 < diff < 200 lines / modifications not in core logic / target branch has minor changes
- 🔴 **High risk**: diff > 200 lines / file > 5000 lines / heavy bidirectional modifications / core logic involved
- ⚫ **Critical risk**: file > 10000 lines + heavy bidirectional modifications / abnormal line endings / file renamed or moved

### Step 6: Check Special Situations

During the audit, additionally check these **universal** common pitfalls:

#### Universal Checks

1. **Line ending differences**: `file <path>` — check for "CR line terminators" (Windows/Mac mixed)
   - ⚠️ CR line ending files cause git to treat the entire file as a "single line", merge/diff completely fails
   - Must mark such files with 🔴 in the report
2. **Function/method signature differences**: Compare signatures of the same function/method between two branches
   - Focus on: parameter count, parameter types, return types
   - Pay special attention to constructor signature differences
3. **Bidirectional modification conflicts**: Same file modified in both branches
4. **Delete vs modify conflicts**: Source branch deleted code that target branch is using
5. **File rename/move**: File renamed or moved to new path in source branch
6. **Binary files**: Images, fonts, compiled artifacts that cannot be merged
7. **Large files**: Single file > 5000 lines, cherry-pick risk is extremely high
8. **Permission/attribute changes**: File permission bit changes (e.g., 755 → 644)
9. **Parent/base class method visibility differences**: Check if parent class methods called by migrated code are accessible in target branch (private/protected/public)
   - Pay special attention when parent class comes from binary dependencies (aar/jar) — source code cannot be modified
10. **Target branch unique code**: Check if target branch has code that doesn't exist in source branch (cherry-pick may overwrite)
11. **Resource file duplicate definitions**: Check if resource files (strings.xml / colors.xml etc.) will have duplicate items after cherry-pick

#### Transitive Dependency Check (Important!)

After migrating a module, must check if all third-party libraries imported by the module are declared in the target branch's build configuration:

```bash
# Example: Java/Kotlin project
grep -rh "^import " <module-path> --include="*.java" --include="*.kt" | \
  grep -v "<project-package>" | grep -v "android\|java\|kotlin" | sort -u

# Compare with build.gradle / pom.xml dependency declarations
```

⚠️ **Transitive dependency chains may differ between branches**. Libraries obtained through transitive dependencies in the source branch may not be available in the target branch. Must explicitly declare all directly-used dependencies.

#### Build System Checks (auto-selected based on project type)

| Project Type | Check Items |
|-------------|-------------|
| Gradle (Java/Android/Kotlin) | build.gradle dependencies, settings.gradle module registration, flavor config, local aar/jar dependencies, AGP library module restrictions (fileTree cannot include .aar) |
| Maven (Java) | pom.xml dependencies, module structure, parent pom version |
| npm/yarn (JS/TS) | package.json dependency versions, lock file differences, workspace config |
| Go | go.mod dependency versions, replace directives |
| Cargo (Rust) | Cargo.toml dependency versions, workspace members |
| pip (Python) | requirements.txt versions, setup.py/pyproject.toml config |
| CocoaPods (iOS) | Podfile dependencies, .xcodeproj config |
| CMake (C/C++) | CMakeLists.txt targets and link libraries |
| .NET (C#) | .csproj references, NuGet package versions |

### Step 7: Generate Audit Report

Generate an interactive HTML report, saved to the project's `docs/` directory (create if not exists).

Report contents:

1. **Overview Statistics**
   - Total commit count
   - Commits involving external files count
   - Strong / weak / infrastructure / test / resource dependency counts
   - Risk distribution (🟢🟡🔴⚫)
   - Estimated workload (person-days)

2. **Commit Discovery Process** (Feature Mode only)
   - Which search strategies were used
   - How many commits each strategy found
   - User confirmation status

3. **⚠️ Critical Risk Alert Panel** (pinned to top)
   - CR line ending files list
   - Large files list (>5000 lines)
   - Function signature differences (functions/constructors with different signatures between branches)
   - Parent class method visibility issues
   - Missing transitive dependencies list
   - Target branch unique code that may be overwritten

4. **Strong Dependency Commit List**
   - Each commit's SHA, message, author, time
   - External files involved
   - Dependency determination reasoning (what symbols are referenced)
   - Suggested handling approach
   - Suggested cherry-pick order

5. **External File Risk Matrix**
   - Sorted by risk level
   - File path, diff lines, total file lines
   - Bidirectional modification marker
   - Line ending format marker
   - Suggested handling approach

6. **Special Situation Warnings**
   - Line ending issues
   - Signature differences
   - Binary files
   - Large files
   - Resource file duplication risk

7. **Suggested Migration Strategy**
   - Phased migration plan
   - Estimated workload
   - Specific operation steps for each phase

8. **Post-Cherry-pick Checklist** (printable)
   - Conflict marker residue check
   - Signature matching check
   - Resource duplication check
   - Compilation verification

Report interactive features:
- Filter by risk level
- Filter by dependency type
- Expand/collapse detailed diff for each commit
- Search by file path
- Search by commit message
- Export as CSV (file list)
- Export as Markdown (migration plan)

### Step 8: Generate Migration Plan Suggestions

Based on audit results, provide phased migration plan:

```
Phase 0: Infrastructure
  - Build config files (build.gradle / package.json / go.mod etc.)
  - Module registration/declaration
  - New dependency modules (e.g., model layer)
  ✅ Compile verification immediately after completion

Phase 1: Core Code Migration
  - Approach A (whole-module overwrite): Directly overwrite target branch with source branch's module directory
    - Confirm target branch module directory has no unique code before overwriting
    - Check transitive dependencies after overwriting
  - Approach B (per-commit cherry-pick): Cherry-pick in chronological order
  ✅ Compile verification immediately after completion

Phase 2: Low-Risk External Dependencies
  - New files (direct copy)
  - Append-only changes (cherry-pick without conflict)
  - Files unmodified in target branch
  ✅ Compile verification immediately after completion

Phase 3: Medium-Risk External Dependencies
  - Per-commit cherry-pick, manually resolve minor conflicts
  - Or manually merge differences
  - Execute checklist after each cherry-pick
  ✅ Compile verification immediately after completion

Phase 4: High-Risk External Dependencies
  - Manual handling
  - Keep target branch version + manually add necessary changes
  - Do NOT cherry-pick large files as a whole
  - CR line ending files need format conversion before editing
  ✅ Compile verification immediately after completion

Phase 5: Verification
  - Compilation verification
  - Unit tests
  - Functional tests
  - Regression tests
```

## Output Artifacts

1. **Audit Report HTML** — saved to `docs/migration-audit-<timestamp>.html`
2. **Migration Plan** — text output to user
3. **Risk File List** — files sorted by priority
4. **Commit List** — commits to cherry-pick in suggested order
5. **Post-Cherry-pick Checklist** — checks to perform after each cherry-pick

## Key Considerations

### Cherry-pick Strategy Recommendations

| File Type | Recommended Strategy |
|-----------|---------------------|
| Internal file conflicts (within migration scope) | Directly overwrite with source branch's final version |
| External file conflicts | Manually resolve, preserve target branch's unique logic |
| Large files (>5000 lines) | Do NOT cherry-pick as whole, keep target branch version + manually add |
| Build config files | Manually merge, do NOT overwrite target branch's config |
| Binary files | Directly overwrite with source branch version (cannot merge) |
| Test files | Optional migration, lowest priority |
| Resource files (strings.xml etc.) | Check for duplicate definitions after cherry-pick |
| CR line ending files | `tr '\r' '\n'` convert → edit → `tr '\n' '\r'` convert back |

### Post-Cherry-pick Mandatory Checklist

After each cherry-pick, AI must remind user to perform these checks:

1. **Conflict marker residue**: `grep -rn "<<<<<<" --include="*.<ext>" .`
   - If found, must clean immediately — do NOT proceed to next cherry-pick
   - If file is severely corrupted, restore to target branch original version, then manually add needed changes
2. **Method signature matching**: Check if method calls introduced by cherry-pick match target branch's interface signatures
3. **Constructor parameter matching**: Check constructor call parameter count and types
4. **Target branch unique code**: Compare with target branch original version, restore overwritten unique methods
5. **Resource file duplicates**: Check strings.xml / colors.xml etc. for duplicate items
6. **Compilation verification**: Compile immediately — do NOT accumulate multiple cherry-picks before verifying
7. **Commit current changes**: For easier rollback later

### Common Pitfall Warnings

Proactively flag these risks in the report:

1. **Line ending issues** → Warn that git merge/cherry-pick may produce false conflicts, or treat entire file as single line
2. **Function signature differences** → Warn that cherry-pick may cause parameter mismatch compilation failures
   - Note: Same interface may have different method signatures between branches (e.g., target branch has an extra parameter)
   - Solution: Restore target branch's original calling approach, adapt via wrapper methods
3. **Constructor signature differences** → Warn about different parameter count/types
4. **Access permission issues** → Warn that some methods/properties may not be accessible in target branch
   - Note: When parent class comes from binary dependencies (aar/jar), source code cannot be modified
   - Solution: Use underlying public APIs instead (bypass private parent class methods, call library's public API directly)
5. **Transitive dependency differences** → Warn about inconsistent third-party library versions or different transitive chains
   - Solution: Explicitly declare all directly-used third-party libraries in module's build config
6. **Target branch unique code overwritten** → Warn that cherry-pick will delete target branch's unique functionality
   - Solution: Compare with target branch original version after cherry-pick, restore overwritten unique methods
7. **Circular dependencies** → Warn that migration may introduce circular dependencies
8. **Environment variable/config differences** → Warn that different branches may have different environment configs
9. **AGP library module restrictions** → Warn that Android library modules cannot depend on local .aar via fileTree
   - Solution: Configure flatDir in root build.gradle → use `api(name:'xxx', ext:'aar')` in module
10. **Resource file duplicate definitions** → Warn that cherry-pick may introduce items duplicating existing resources
11. **Git conflict marker residue** → Warn that multiple cherry-picks may accumulate unresolved conflict markers
    - Symptoms: Compilation errors like "illegal character", "class, interface, or enum expected"

### Feature Mode Completeness Assurance

When using Feature Mode, AI must:

1. **Proactively expand keywords** — Don't just use the user's single keyword; infer translations, abbreviations, related concepts
2. **Use file reverse tracking** — From known commits' files, reverse-find other commits that modified these files
3. **Use code reference chains** — From core classes/functions, find referencing files, then find commits that modified them
4. **Explicitly inform user of coverage risk** — Feature Mode cannot guarantee 100% coverage; user must confirm
5. **Provide omission detection suggestions** — Suggest user discover missed commits through compilation errors after migration

### Incremental Audit During Migration

When user encounters compilation errors or runtime issues during migration, AI should:

1. **Analyze compilation errors** — Based on error type (symbol not found, parameter mismatch, package not found etc.), quickly locate the cause
2. **Determine if additional commits are needed** — If error is due to a missed commit, help locate that commit
3. **Suggest fix strategy** — Based on error type, provide fix priority:
   - Restore target branch original version (if unique code was overwritten)
   - Supplement from source branch (if source branch added new methods/resources)
   - Adaptation wrapper (if two branches have different interface signatures)

## Example Conversations

### Example 1: Module Path Mode

**User**: I need to migrate the payment module from feature/payment branch to main branch, help me do an audit

**AI**: OK, I'll perform a cross-branch module migration audit. Please confirm:
- Source branch: `feature/payment`
- Target branch: `main`
- Module path: Please tell me the payment module's directory path (e.g., `src/modules/payment/`)
- Start commit: Should I auto-find the merge-base?

### Example 2: Feature Mode

**User**: I need to migrate the "user authentication refactoring" feature from develop branch to release/v2.0

**AI**: OK, I'll perform a feature-level migration audit. This feature may span multiple directories and commits. I need to first locate all related commits.

Please provide (the more the better):
- Related commit SHAs you know (if any)
- Feature-related keywords (e.g., "auth", "login", "authentication")
- Who was the main developer?
- Approximate development time range?
- Any associated Issue/TAPD IDs?

I'll use multi-strategy cross-validation to find all related commits, then ask you to confirm.

### Example 3: Hybrid Mode

**User**: Migrate `src/audio/` module, but it also depends on some shared component changes

**AI**: OK, I'll use Hybrid Mode:
1. First scan all commits under `src/audio/` path
2. Then keyword-search for audio-related commits in shared components
3. Merge and analyze all external dependencies

Please confirm source and target branch names?

### Example 4: Compilation Error During Migration

**User**: After cherry-pick, compilation error: "actual and formal argument lists differ in length"

**AI**: This is a typical **interface signature difference** issue. Let me check the signature differences between the two branches...
(Compare interface definitions between branches, provide specific fix plan)

## Audit Report HTML Template

Report structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Cross-Branch Migration Audit Report</title>
    <!-- Inline CSS: Modern clean design, dark/light mode support -->
    <!-- Inline JS: Filter, search, expand/collapse, export CSV -->
</head>
<body>
    <!-- 0. Critical Risk Alert Panel (pinned top, red/orange background) -->
    <!-- 1. Report header: project name, source branch, target branch, generation time -->
    <!-- 2. Overview statistics cards (commit count, dependency count, risk distribution, estimated workload) -->
    <!-- 3. Commit discovery process (Feature Mode) -->
    <!-- 4. Risk matrix table (filterable, sortable) -->
    <!-- 5. Commit detail list (expandable diff) -->
    <!-- 6. Special situation warning panel -->
    <!-- 7. Migration strategy suggestions (phased) -->
    <!-- 8. Post-cherry-pick checklist (printable) -->
    <!-- 9. Action buttons (export CSV, export Markdown, print) -->
</body>
</html>
```

Report style requirements:
- Modern clean CSS design (no external dependencies, all inline)
- Dark/light mode toggle support
- Tables support sorting and filtering
- Each commit's diff expandable/collapsible
- Risk levels distinguished by color tags (🟢🟡🔴⚫)
- Critical risk alert panel pinned to top with prominent red/orange background
- Responsive layout, print-friendly
- File list exportable as CSV
- Migration plan exportable as Markdown
