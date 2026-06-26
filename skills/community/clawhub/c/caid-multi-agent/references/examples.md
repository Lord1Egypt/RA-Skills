# CAID Multi-Agent Examples

## Example 1: Python Library from Scratch (Commit0-style)

> **Engineer limit:** Max 4 engineers for Commit0-style tasks (clear file structure, test-to-file mappings)

### Phase 0: Manager Pre-Setup

```bash
# BEFORE any delegation, manager prepares the environment

# 1. Ensure runtime environment
cd /path/to/repository
python -m venv venv
source venv/bin/activate
pip install -e . 2>/dev/null || pip install pytest

# 2. Add minimal function stubs so imports work
mkdir -p src/mylib
cat > src/mylib/__init__.py << 'EOF'
"""MyLib package."""
from .utils import validate_input, format_output
from .core import CoreClass
from .api import APIClient
from .cli import main

__version__ = "0.1.0"
EOF

# Create stub files with empty functions
touch src/mylib/utils.py src/mylib/core.py src/mylib/api.py src/mylib/cli.py

# 3. Commit to main so engineers start from consistent base
git add .
git commit -m "setup: initial stubs and package structure"
git push origin main
```

### Phase 1: Analyze and Build Dependency Graph

```python
# Manager analyzes repository structure
import_statements = analyze_imports("src/mylib/")
test_files = discover_tests("tests/")

# Build dependency graph from imports and test mappings
dependency_graph = {
    "nodes": {
        "utils": {"file": "src/mylib/utils.py", "deps": [], "tests": ["tests/test_utils.py"]},
        "core": {"file": "src/mylib/core.py", "deps": ["utils"], "tests": ["tests/test_core.py"]},
        "api": {"file": "src/mylib/api.py", "deps": ["core"], "tests": ["tests/test_api.py"]},
        "cli": {"file": "src/mylib/cli.py", "deps": ["api"], "tests": ["tests/test_cli.py"]},
    },
    "parallel_groups": [
        ["utils"],  # Round 1: No dependencies
        ["core"],   # Round 2: Depends on utils
        ["api"],    # Round 3: Depends on core
        ["cli"],    # Round 4: Depends on api
    ]
}

# Ready condition: Ready(v) ⇔ all deps completed
```

### Phase 2: Create PHYSICALLY Isolated Worktrees

```bash
# Manager creates worktrees for engineers (PHYSICAL isolation, not soft)
git worktree add ../workspace-engineer-1 feature/utils
git worktree add ../workspace-engineer-2 feature/core

# Each engineer gets own directory with full copy of repo
# ls -la ..
# workspace-engineer-1/  workspace-engineer-2/
```

### Phase 3: Delegate Tasks (Round 1)

**Engineer 1 (utils) - NO dependencies:**
```json
{
  "task_id": "implement-utils",
  "task_description": "Implement utility functions: validate_input(), format_output(), sanitize_string()",
  "target_files": ["src/mylib/utils.py"],
  "target_functions": ["validate_input", "format_output", "sanitize_string"],
  "dependencies": [],
  "expected_outcome": "All utility functions implemented with type hints, docstrings, and passing tests",
  "verification_command": "pytest tests/test_utils.py -v",
  "restricted_files": ["src/mylib/__init__.py", "src/mylib/core.py", "src/mylib/api.py", "src/mylib/cli.py"],
  "priority": "high"
}
```

### Phase 4: Spawn Engineers (OpenClaw)

```javascript
// Manager spawns Engineer 1
const eng1 = await sessions_spawn({
  runtime: "subagent",
  task: formatTask(utilsTask),
  agentId: "coding-agent",
  mode: "run",
  runTimeoutSeconds: 400
});

// Wait for completion
const result = await pollForCompletion(eng1.sessionKey);
```

### Phase 5: Engineer Self-Verification and Commit

**Engineer 1 in `../workspace-engineer-1/`:**
```bash
# Implement functions...
# Run self-verification (MANDATORY before submission)
pytest tests/test_utils.py -v

# If tests fail, iterate until pass:
# 1. Fix implementation
# 2. Re-run tests
# 3. Repeat until all pass

# Only submit when ALL tests pass
git add src/mylib/utils.py
git commit -m "implement: utility functions with validation"
```

### Phase 6: Manager Integration

```bash
# Manager attempts merge to main
cd /path/to/repository
git checkout main
git merge feature/utils

# Success! Update dependency graph:
# utils: ✓ COMPLETED
# core: Ready (all deps satisfied)
```

### Phase 7: Round 2 - Delegate Dependent Task

**Engineer 2 (core) - NOW Ready:**
```json
{
  "task_id": "implement-core",
  "task_description": "Implement CoreClass with process_data() using utils.validate_input()",
  "target_files": ["src/mylib/core.py"],
  "target_functions": ["CoreClass", "process_data", "initialize"],
  "dependencies": ["implement-utils"],
  "expected_outcome": "CoreClass validates input via utils and processes data correctly",
  "verification_command": "pytest tests/test_core.py -v",
  "restricted_files": ["src/mylib/__init__.py", "src/mylib/utils.py"],
  "priority": "high"
}
```

### Phase 8: Handle Merge Conflict (Example)

Scenario: Engineer 2's branch diverged while Engineer 1 was finishing.

```bash
# Manager attempts merge
git merge feature/core
# CONFLICT in pyproject.toml

# Engineer 2 is RESPONSIBLE for resolution
cd ../workspace-engineer-2
git pull origin main              # Gets Engineer 1's changes

# Resolve conflicts in pyproject.toml
# Editor: fix merge markers

# Verify resolution didn't break anything
pytest tests/test_core.py -v

# Re-commit
git add pyproject.toml
git commit --amend -m "implement: CoreClass with dependency resolution"

# Manager retries merge
git checkout main
git merge feature/core  # Success!
```

### Phase 9: Continue Until Complete

Rounds 3-4: api → cli (same pattern)

Final state:
```
Dependency graph:
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│  utils  │─→│  core   │─→│   api   │─→│   cli   │
│   ✓     │  │   ✓     │  │   ✓     │  │   ✓     │
└─────────┘  └─────────┘  └─────────┘  └─────────┘

All tasks completed and integrated!
```

---

## Example 2: Paper Reproduction (PaperBench-style)

> **Engineer limit:** Max 2 engineers for PaperBench-style tasks (inferred dependencies, no test mappings)

### Phase 0: Manager Pre-Setup

```bash
# Setup project structure
mkdir reproduction-paper
cd reproduction-paper
git init

# Create minimal structure with stubs
mkdir -p src/models src/data src/training src/evaluation
touch src/__init__.py src/models/__init__.py src/data/__init__.py

git add .
git commit -m "setup: initial project structure"
```

### Phase 1: Read Paper and Infer Dependencies

```python
# Manager reads paper to understand main contributions
paper_analysis = {
    "title": "Novel Architecture for X",
    "main_contribution": "Section 3: Proposed Model Architecture",
    "implementation_order": [
        ("data_preprocessing", "Section 4.1: Data loading and preprocessing"),
        ("model_architecture", "Section 3: Neural network architecture"),
        ("training_loop", "Section 4.2: Training procedure with custom loss"),
        ("evaluation", "Section 5: Metrics and evaluation protocol"),
    ],
    "dependencies": {
        "data_preprocessing": [],
        "model_architecture": [],  # Can parallel with data
        "training_loop": ["data_preprocessing", "model_architecture"],
        "evaluation": ["training_loop"],
    }
}

# Note: Max 2 engineers for PaperBench - manager task is harder
```

### Phase 2: Create Worktrees (2 max)

```bash
git worktree add ../workspace-eng1 feature/data-pipeline
git worktree add ../workspace-eng2 feature/model-arch
```

### Phase 3: Delegate Round 1 (Parallel)

**Engineer 1 (data) - NO dependencies:**
```json
{
  "task_id": "data-pipeline",
  "task_description": "Implement data preprocessing as described in Section 4.1. Load dataset, apply normalization per Equation 1.",
  "target_files": ["src/data/loader.py", "src/data/preprocess.py"],
  "dependencies": [],
  "expected_outcome": "Data pipeline loads dataset and outputs normalized tensors",
  "verification_command": "python -c 'from src.data.loader import load_data; d = load_data(); print(d.shape)'",
  "restricted_files": ["src/__init__.py", "src/models/", "src/training/"],
  "paper_sections": ["4.1"],
  "equations": ["Equation 1: Normalization"],
  "priority": "high"
}
```

**Engineer 2 (model) - NO dependencies:**
```json
{
  "task_id": "model-arch",
  "task_description": "Implement neural network architecture from Section 3. Include all layers shown in Figure 2.",
  "target_files": ["src/models/network.py", "src/models/layers.py"],
  "dependencies": [],
  "expected_outcome": "Model instantiates and runs forward pass successfully",
  "verification_command": "python -c 'from src.models.network import Model; import torch; m = Model(); print(m(torch.randn(1,3,224,224)).shape)'",
  "restricted_files": ["src/__init__.py", "src/data/", "src/training/"],
  "paper_sections": ["3.1", "3.2", "3.3"],
  "figure": "Figure 2",
  "priority": "high"
}
```

### Phase 4: Both Engineers Self-Verify and Commit

**Engineer 1:**
```bash
cd ../workspace-eng1
python -c 'from src.data.loader import load_data; d = load_data(); print(f"Data shape: {d.shape}")'
# Output: Data shape: (1000, 3, 224, 224)
git add src/data/
git commit -m "implement: data preprocessing pipeline (Section 4.1)"
```

**Engineer 2:**
```bash
cd ../workspace-eng2
python -c 'from src.models.network import Model; import torch; m = Model(); print(f"Output shape: {m(torch.randn(1,3,224,224)).shape}")'
# Output: torch.Size([1, 10])
git add src/models/
git commit -m "implement: neural network architecture (Section 3)"
```

### Phase 5: Manager Integrates Both

```bash
# Merge data pipeline first
git checkout main
git merge feature/data-pipeline  # Success

# Merge model architecture
git merge feature/model-arch  # Success

# Both complete! Update dependency graph
```

### Phase 6: Round 2 - Training Loop (now Ready)

```bash
# Create new worktree for training
git worktree add ../workspace-eng3 feature/training
```

**Engineer 3:**
```json
{
  "task_id": "training-loop",
  "task_description": "Implement training loop with custom loss from Section 4.2. Use data pipeline and model.",
  "target_files": ["src/training/trainer.py", "src/training/loss.py"],
  "dependencies": ["data-pipeline", "model-arch"],
  "expected_outcome": "Training loop runs for 1 epoch without errors",
  "verification_command": "python src/training/trainer.py --epochs 1 --dry-run",
  "restricted_files": ["src/__init__.py", "src/data/loader.py", "src/models/network.py"],
  "paper_sections": ["4.2", "4.3"],
  "priority": "high"
}
```

### Comparison: Why PaperBench is Harder

| Aspect | Commit0 | PaperBench |
|--------|---------|------------|
| Dependency clarity | Explicit (imports, tests) | Inferred (paper text) |
| Engineer limit | 4 | 2 |
| Test mappings | Clear | None |
| Manager task | File-level analysis | Semantic understanding |
| Risk of miscoordination | Low | High |

---

## Example 3: Context Management for Manager

### The Problem

After 10 rounds, manager's context explodes with:
- Full conversation history
- All git diffs
- All test outputs
- Error tracebacks

### The Solution: LLMSummarizingCondenser

```python
# Every 5 rounds, compress context
if round_number % 5 == 0:
    compressed_state = {
        "round": round_number,
        "summary": "Rounds 1-5 completed. Implemented utils (✓), core (✓), 
                    api (✓). Training in progress.",
        "completed_tasks": {
            "implement-utils": {"commit": "abc123", "tests": "5/5 passed"},
            "implement-core": {"commit": "def456", "tests": "12/12 passed"},
            "implement-api": {"commit": "ghi789", "tests": "8/8 passed"},
        },
        "ready_tasks": ["implement-training"],
        "blocked_tasks": ["implement-evaluation: waiting for training"],
        "current_dependency_graph": {
            "utils": "completed",
            "core": "completed",
            "api": "completed",
            "training": "in_progress",
            "evaluation": "blocked"
        },
        "unresolved_errors": [],
        "main_branch_commits": ["abc123", "def456", "ghi789"]
    }
    
    # Replace full history with compressed state
    context = compressed_state
```

### Preserved vs Discarded

| Preserved | Discarded |
|-----------|-----------|
| Dependency graph (current) | Old versions of graph |
| Completed task IDs + commits | Full task descriptions |
| Commit hashes | Full diffs |
| Error summaries | Full tracebacks |
| Test pass/fail counts | Full test output |
| Blocked tasks list | Why they were blocked |

---

## Example 4: Complete OpenClaw Implementation

```javascript
// Complete CAID implementation for OpenClaw

class CAIDManager {
  constructor(config) {
    this.maxEngineers = config.maxEngineers || 4; // 2 for PaperBench, 4 for Commit0
    this.round = 0;
    this.completed = new Set();
    this.dependencyGraph = null;
  }

  async run(projectPath, tasks) {
    // Phase 0: Pre-setup
    await this.preSetup(projectPath);
    
    // Phase 1: Build dependency graph
    this.dependencyGraph = await this.buildDependencyGraph(tasks);
    
    // Main loop
    while (this.hasReadyTasks()) {
      this.round++;
      
      // Get Ready tasks
      const readyTasks = this.getReadyTasks()
        .slice(0, this.maxEngineers);
      
      if (readyTasks.length === 0) break;
      
      // Phase 2: Create worktrees
      const worktrees = await this.createWorktrees(readyTasks);
      
      // Phase 3-4: Spawn engineers and execute
      const engineers = await this.spawnEngineers(readyTasks, worktrees);
      const results = await this.waitForCompletion(engineers);
      
      // Phase 5-6: Integrate and update
      for (const result of results) {
        if (result.success) {
          const mergeResult = await this.mergeToMain(result.taskId);
          if (mergeResult.success) {
            this.completed.add(result.taskId);
            this.updateDependencyGraph();
          } else {
            // Conflict resolution
            await this.resolveConflict(result.taskId, mergeResult.conflicts);
          }
        }
      }
      
      // Phase 7: Context compression
      if (this.round % 5 === 0) {
        this.compressContext();
      }
    }
    
    return this.getFinalStatus();
  }

  async preSetup(projectPath) {
    // Prepare runtime
    await exec(`cd ${projectPath} && pip install -e .`);
    
    // Create stubs
    await this.createStubs(projectPath);
    
    // Commit to main
    await exec(`cd ${projectPath} && git add . && git commit -m "setup: initial"`);
  }

  async createWorktrees(tasks) {
    const worktrees = [];
    for (let i = 0; i < tasks.length; i++) {
      const branch = `feature/${tasks[i].id}`;
      const path = `../workspace-eng-${i}`;
      await exec(`git worktree add ${path} ${branch}`);
      worktrees.push({ taskId: tasks[i].id, path, branch });
    }
    return worktrees;
  }

  async spawnEngineers(tasks, worktrees) {
    const engineers = [];
    for (let i = 0; i < tasks.length; i++) {
      const result = await sessions_spawn({
        runtime: "subagent",
        task: this.formatTask(tasks[i]),
        agentId: "coding-agent",
        mode: "run",
        runTimeoutSeconds: 400
      });
      engineers.push({
        taskId: tasks[i].id,
        sessionKey: result.sessionKey,
        worktree: worktrees[i]
      });
    }
    return engineers;
  }

  formatTask(task) {
    return `
TASK: ${task.description}
FILES: ${task.target_files.join(', ')}
DEPS: ${task.dependencies.join(', ') || 'None'}
VERIFY: ${task.verification_command}
RESTRICTED: ${task.restricted_files.join(', ')}

RULES:
1. Work in isolated worktree
2. Run verification before ANY commit
3. Only commit when ALL tests pass
4. Do NOT modify restricted files
`;
  }

  getReadyTasks() {
    return Object.values(this.dependencyGraph.nodes)
      .filter(node => 
        node.deps.every(dep => this.completed.has(dep))
        && !this.completed.has(node.id)
      );
  }
}

// Usage
const manager = new CAIDManager({ maxEngineers: 4 });
await manager.run("/path/to/repo", taskList);
```

---

## Example 6: Worktree Cleanup and State Synchronization

### Worktree Cleanup (Required)

```bash
# After engineer completes or hits iteration limit

# 1. Remove git worktree reference
git worktree remove ../workspace-engineer-1

# 2. Clean up directory
rm -rf ../workspace-engineer-1

# 3. Verify worktree list
git worktree list
# /path/to/repo         main
# /path/to/repo2        feature-x
```

### State Synchronization Pattern

```bash
# When main advances with other engineer's changes
cd ../workspace-engineer-2

# Sync to latest main
git fetch origin
git reset --hard origin/main  # OR: git rebase origin/main

# Verify sync worked
git log --oneline -3
# abc1234 Merge feature-1
# def5678 Merge feature-2  
# ghi9012 setup: initial stubs

# Continue work from latest state
```

---

## Example 7: Manager Final Review Phase

### Final Review Checklist

```javascript
class CAIDManager {
  async finalReview() {
    // 1. Verify all tasks completed
    const incomplete = this.dependencyGraph.getIncomplete();
    if (incomplete.length > 0) {
      throw new Error(`Incomplete tasks: ${incomplete.join(', ')}`);
    }
    
    // 2. Full test suite
    const testResult = await exec('pytest tests/ -v');
    if (testResult.exitCode !== 0) {
      throw new Error('Tests failed in final review');
    }
    
    // 3. Verify integration completeness
    const mainCommits = await exec('git log --oneline main');
    const expectedCommits = this.completedTasks.map(t => t.commit);
    
    // 4. Smoke test
    await exec('python -m mypackage --version');
    
    // 5. Submit final product
    return { status: 'complete', commits: expectedCommits };
  }
}
```

### Final Review Bash Script

```bash
#!/bin/bash
# final-review.sh

set -e

echo "=== CAID Final Review ==="

# 1. Checkout main
git checkout main

# 2. Full test suite
echo "Running full test suite..."
pytest tests/ -v --tb=short

# 3. Integration verification
echo "Verifying all features integrated..."
python -c "
import mypackage
from mypackage.utils import validate_input
from mypackage.core import CoreClass
print('✓ All imports successful')
"

# 4. Version check
echo "Final version check..."
python -m mypackage --version

echo "=== Final Review Complete ==="
```

---

## Key Takeaways from Paper

1. **Pre-setup is mandatory** — Don't skip runtime prep and stub creation
2. **Physical worktree isolation** — Soft isolation degrades performance
3. **Strict engineer limits** — 2 PaperBench, 4 Commit0, never 8+
4. **Self-verification mandatory** — Tests must pass before commit
5. **Use CAID from outset** — Not as fallback after single-agent failure
6. **Structured JSON only** — No free-form chat between agents
7. **Context compression** — Every 5 rounds, summarize history
8. **Engineer resolves conflicts** — Not manager
9. **Final review required** — Manager must verify before submission
10. **Cleanup worktrees** — Delete after completion or limit reached

See SKILL.md for complete coordination workflow and warnings.