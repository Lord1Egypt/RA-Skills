# File Classification Manager Skill

## Description
**Dual-purpose intelligent file classification system** that manages BOTH project outputs AND temporary files with synchronized directory structures. Automatically organizes files into proper `projects/` and `temp/` directories based on content type, purpose, and project context. Prevents file clutter in workspace root by enforcing structured dual-storage.

## Key Principle: Synchronized Dual Storage
**Every project has TWO corresponding directories:**
- **`projects/{project_name}/`** - For **permanent, valuable outputs** (reports, final documents, deliverables)
- **`temp/{project_name}/`** - For **temporary, intermediate files** (scripts, extracted data, cache, working files)

Both directories are **automatically created together** and **share the same project name** to maintain clear association between final outputs and their supporting temporary files.

## Capabilities
- **Dual Directory Management**: Simultaneously manages `projects/` (outputs) and `temp/` (intermediate files) directories
- **Synchronized Project Naming**: Ensures identical project names across both storage areas for clear association
- **Purpose-Based Classification**: Automatically determines whether a file belongs in outputs vs intermediate based on content and file patterns
- **Project Detection**: Identifies project context from user input or file content
- **Automatic Structure Creation**: Creates standardized dual directory structure for any new project
- **Smart File Routing**: Routes files to correct subdirectories in the appropriate storage area (projects vs temp)
- **Legacy File Cleanup**: Migrates existing misplaced files to proper dual-storage locations
- **Cross-Agent Compatibility**: Works with subagents and ACP coding sessions

## Usage Scenarios
- When generating new files (reports, scripts, data)
- When processing files via other skills (PDF Extract, Summarize Pro, etc.)
- When organizing existing workspace clutter
- When working with multiple concurrent projects

## API Functions

### `classify_and_route_file(filepath, project_context)`
Routes a file to the appropriate directory based on its type and project context.

**Parameters:**
- `filepath`: Path to the file to be classified
- `project_context`: Project name or context object

**Returns:** Final destination path

### `ensure_project_structure(project_name)`
Creates the standard directory structure for a project if it doesn't exist.

**Parameters:**
- `project_name`: Name of the project (alphanumeric + underscores only)

**Directory Structure Created:**
```
projects/{project_name}/
├── outputs/
└── assets/
temp/{project_name}/
├── intermediate/
└── cache/
```

### `detect_project_from_content(content)`
Analyzes file content to determine likely project association.

**Parameters:**
- `content`: File content or metadata to analyze

**Returns:** Suggested project name or null

### `cleanup_workspace_root()`
Scans workspace root for misplaced files and routes them appropriately.

**Returns:** Migration report

## File Type Classification Rules

**Files are automatically routed to the CORRECT storage area based on their purpose:**

### 🎯 Projects Storage (Permanent Outputs)
| File Pattern | Destination | Purpose |
|-------------|------------|---------|
| `*_review.md`, `*_literature.md` | `projects/{project}/outputs/` | Literature reviews and analyses |
| `final_*.md`, `comprehensive_*.md` | `projects/{project}/outputs/` | Final reports and deliverables |
| `summary_*.md`, `conclusion_*.md` | `projects/{project}/outputs/` | Executive summaries and conclusions |

### ⚡ Temp Storage (Temporary Files)  
| File Pattern | Destination | Purpose |
|-------------|------------|---------|
| `*.py`, `*.js`, `*.m` | `temp/{project}/intermediate/` | Analysis and processing scripts |
| `*_content.txt`, `*_extract.txt` | `temp/{project}/intermediate/` | Extracted raw content |
| `*.pdf`, `*.docx` | `temp/{project}/intermediate/` | Source documents for processing |
| `*.mat`, `*.csv`, `*.json` | `temp/{project}/intermediate/` | Intermediate data files |
| `*.png`, `*.jpg`, `*.gif` | `temp/{project}/intermediate/` | Generated or processed images |
| `cache_*`, `temp_*` | `temp/{project}/cache/` | Cached API responses and temporary data |

**Key Rule**: The system maintains **synchronized project names** - if a file goes to `projects/dipleg_review/outputs/`, its supporting files go to `temp/dipleg_review/intermediate/`.

## Integration Guidelines

### For Other Skills:
When developing skills that generate files, import this skill and use:
```javascript
const fcm = require('file-classification-manager');
const outputPath = fcm.classify_and_route_file(filename, projectContext);
```

### For Subagents:
Pass project context when spawning subagents:
```javascript
sessions_spawn({
  task: "Process documents",
  runtime: "subagent",
  attachments: [{name: "fcm_config.json", content: JSON.stringify({project: "my_project"})}]
})
```

## Safety Rules
- Never delete files without confirmation
- Always backup before moving critical files  
- Preserve original file timestamps and metadata
- Log all file operations to `memory/YYYY-MM-DD.md`

## Error Handling
- If project context is ambiguous, prompt user for clarification
- If file type is unrecognized, place in `temp/general/intermediate/`
- If directory creation fails, fall back to safe temporary location

## Examples

### Basic Usage:
```javascript
// Classify a literature review file
const result = classify_and_route_file("brain_dipleg_review.md", "dipleg_research");
// Result: "projects/dipleg_research/outputs/brain_dipleg_review.md"
```

### Project Setup:
```javascript
// Ensure project structure exists
ensure_project_structure("pv_topology_analysis");
// Creates projects/pv_topology_analysis/ and temp/pv_topology_analysis/ directories
```

### Workspace Cleanup:
```javascript
// Clean up misplaced files
const report = cleanup_workspace_root();
console.log(report.movedFiles); // Array of successfully moved files
```

## Version
1.0.0

## Author
OpenClaw Assistant

## License
MIT