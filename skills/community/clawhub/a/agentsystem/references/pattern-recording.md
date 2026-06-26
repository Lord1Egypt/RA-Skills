# Pattern Recording Guide

## Overview

Pattern Recording enables recording and recall of successful task workflows, helping agents improve service quality through accumulated experience.

## Core Concepts

### What is a Pattern?

A pattern is a reusable workflow structure extracted from successful task executions:

```python
class Pattern:
    id: str
    name: str
    description: str
    task_type: str              # e.g., "document_analysis"
    steps: List[str]            # Sequence of actions
    conditions: dict            # When this pattern applies
    success_rate: float         # Historical success rate
    usage_count: int            # Times this pattern was used
    created_at: datetime
    updated_at: datetime
```

### Pattern Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Detection  │────▶│  Validation │────▶│   Storage   │
│             │     │             │     │             │
│ • Analyze   │     │ • Confirm   │     │ • Save      │
│   workflow  │     │   with user │     │ • Index     │
│ • Extract   │     │ • Rate      │     │ • Tag       │
│   structure │     │   quality   │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                        │
       │                                        ▼
       │            ┌─────────────┐     ┌─────────────┐
       └───────────▶│   Recall    │◀────│   Search    │
                    │             │     │             │
                    │ • Match     │     │ • Query     │
                    │   context   │     │ • Filter    │
                    │ • Retrieve  │     │ • Rank      │
                    │ • Present   │     │             │
                    └─────────────┘     └─────────────┘
```

---

## Recording Process

### Step 1: Workflow Detection

Detect patterns from successful interactions:

```python
class PatternDetector:
    def detect_pattern(self, interaction):
        """
        Analyzes an interaction to detect reusable patterns.
        
        Args:
            interaction: Dict with user_input, actions, outcome
            
        Returns:
            Pattern object if pattern detected, None otherwise
        """
        # Extract workflow structure
        workflow = self._extract_workflow(interaction)
        
        # Check if similar pattern exists
        existing = self._find_similar(workflow)
        
        if existing:
            # Update existing pattern
            return self._update_pattern(existing, interaction)
        elif self._is_reusable(workflow):
            # Create new pattern
            return self._create_pattern(workflow, interaction)
        
        return None
```

### Step 2: User Confirmation

**Required**: All patterns must be confirmed by user before storage.

```
Agent: "检测到可复用的工作流程：
       [步骤1] 加载文件
       [步骤2] 提取内容
       [步骤3] 生成摘要
       [步骤4] 保存结果
       
       是否记录此模式？"

User: "确认"

Agent: "已记录为'文档摘要工作流'"
```

### Step 3: Storage & Indexing

```python
class PatternStorage:
    def store(self, pattern, user_confirmation=True):
        """
        Stores a confirmed pattern.
        
        Raises:
            PermissionError: If user_confirmation is False
        """
        if not user_confirmation:
            raise PermissionError("Pattern storage requires user confirmation")
        
        self.patterns.append(pattern)
        self._index(pattern)
        self._save_to_disk(pattern)
```

---

## Pattern Matching

### Context-Aware Retrieval

```python
class PatternMatcher:
    def find_matching_patterns(self, context, task_type=None):
        """
        Find patterns that match current context.
        
        Args:
            context: Current task context
            task_type: Optional task type filter
            
        Returns:
            List of matching patterns, sorted by relevance
        """
        candidates = self._filter_by_type(task_type)
        
        # Score each pattern
        scored = []
        for pattern in candidates:
            score = self._calculate_match_score(pattern, context)
            if score >= self.min_match_threshold:
                scored.append((pattern, score))
        
        # Sort by score
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def _calculate_match_score(self, pattern, context):
        """
        Calculate how well a pattern matches current context.
        
        Factors:
        - Context similarity (40%)
        - Success rate (30%)
        - Usage frequency (20%)
        - Recency (10%)
        """
        context_score = self._compare_context(pattern.conditions, context)
        success_score = pattern.success_rate
        usage_score = min(pattern.usage_count / 100, 1.0)
        recency_score = self._calculate_recency(pattern.updated_at)
        
        return (
            0.4 * context_score +
            0.3 * success_score +
            0.2 * usage_score +
            0.1 * recency_score
        )
```

---

## Usage Examples

### Example 1: Record a Pattern

```python
from scripts.pattern_recorder import PatternRecorder

recorder = PatternRecorder()

# After a successful task
recorder.record(
    task_type="data_analysis",
    steps=[
        "load_csv",
        "clean_data",
        "analyze_columns",
        "generate_report",
        "save_results"
    ],
    context={
        "file_type": "csv",
        "analysis_type": "statistical"
    },
    success=True
)
```

### Example 2: Recall Patterns

```python
# Find patterns for current task
matches = recorder.recall(
    context={"file_type": "csv"},
    task_type="data_analysis"
)

# Present to user
if matches:
    print("找到以下相关模式：")
    for pattern, score in matches[:3]:
        print(f"- {pattern.name} (相关度: {score:.0%})")
```

### Example 3: Apply Pattern

```python
# Get pattern by ID
pattern = recorder.get_pattern("pattern_001")

# Use as template
workflow = pattern.steps
for step in workflow:
    execute_step(step)
```

---

## Pattern Quality Metrics

### Success Rate Tracking

```python
class PatternMetrics:
    def record_usage(self, pattern_id, success):
        """
        Record pattern usage result.
        """
        pattern = self.get_pattern(pattern_id)
        pattern.usage_count += 1
        
        # Update success rate (exponential moving average)
        alpha = 0.1
        pattern.success_rate = (
            alpha * (1.0 if success else 0.0) +
            (1 - alpha) * pattern.success_rate
        )
        
        self._save_pattern(pattern)
```

### Quality Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Success Rate | < 0.5 | Flag for review |
| Usage Count | < 3 | Mark as experimental |
| Last Used | > 90 days | Archive |

---

## Best Practices

### Do's ✅

1. **Always confirm with user** before recording
2. **Include clear context** conditions
3. **Track success metrics** actively
4. **Cleanup low-quality patterns** regularly
5. **Use descriptive names** for patterns

### Don'ts ❌

1. **Never record without confirmation**
2. **Don't store sensitive information** in patterns
3. **Avoid overly specific patterns** (low reusability)
4. **Don't ignore quality metrics**
5. **Never bypass user control**

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No patterns found | Too few recorded | Record more workflows |
| Poor matches | Vague conditions | Add specific context |
| Low success rate | Outdated patterns | Update or remove |
| Slow retrieval | Too many patterns | Run cleanup |

### Pattern Cleanup

```python
# Remove low-quality patterns
recorder.cleanup(
    min_success_rate=0.5,
    min_usage=3,
    max_age_days=90
)
```

---

## Integration with Memory System

Patterns are integrated with the Memory System:

```python
# When recording a pattern
episode_id = memory.add_episode(
    user_input=user_request,
    actions=workflow_steps,
    outcome="success"
)

pattern_id = recorder.record(
    source_episode=episode_id,
    ...
)

# Link pattern to episode
memory.link_pattern(episode_id, pattern_id)
```

This enables:
- Traceability: Know which interaction created a pattern
- Validation: Verify patterns from historical data
- Updates: Refine patterns based on new experience
