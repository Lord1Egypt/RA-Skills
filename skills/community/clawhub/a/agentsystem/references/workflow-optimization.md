# Workflow Optimization Guide

## Overview

Workflow Optimization provides template-based workflow improvement through pattern reuse and context-aware recommendations.

## Core Concepts

### What is Workflow Optimization?

Workflow optimization is the process of:
1. Identifying reusable task patterns
2. Applying proven workflows to new tasks
3. Continuously improving based on outcomes

### Optimization Cycle

```
       ┌────────────────────────────────────────────┐
       │                                            │
       ▼                                            │
┌─────────────┐     ┌─────────────┐                │
│   Analyze   │────▶│   Recommend │                │
│             │     │             │                │
│ • Context   │     │ • Match     │                │
│ • History   │     │   patterns  │                │
│ • Goals     │     │ • Rank      │                │
└─────────────┘     └──────┬──────┘                │
                          │                        │
                          ▼                        │
                   ┌─────────────┐                 │
                   │   Execute   │                 │
                   │             │                 │
                   │ • Apply     │                 │
                   │   workflow  │                 │
                   │ • Monitor   │                 │
                   └──────┬──────┘                 │
                          │                        │
                          ▼                        │
                   ┌─────────────┐                 │
                   │   Evaluate  │─────────────────┘
                   │             │
                   │ • Success?  │
                   │ • Improve?  │
                   └─────────────┘
```

---

## Workflow Templates

### Built-in Templates

#### 1. Document Analysis Template

```yaml
name: document_analysis
description: Analyze and summarize documents
steps:
  - name: load_document
    action: read_file
    params:
      file_path: "{input_file}"
  
  - name: extract_content
    action: extract_text
    params:
      include_tables: true
  
  - name: analyze_structure
    action: identify_sections
    params:
      max_depth: 3
  
  - name: generate_summary
    action: summarize
    params:
      max_length: 500
  
  - name: save_results
    action: write_file
    params:
      output_path: "{output_file}"
```

#### 2. Data Processing Template

```yaml
name: data_processing
description: Clean and process data files
steps:
  - name: load_data
    action: read_csv
    params:
      encoding: "utf-8"
  
  - name: validate_data
    action: check_schema
    params:
      required_columns: []
  
  - name: clean_data
    action: transform
    params:
      remove_duplicates: true
      handle_missing: "drop"
  
  - name: analyze_data
    action: compute_stats
    params: {}
  
  - name: export_results
    action: write_csv
    params:
      format: "cleaned"
```

#### 3. Report Generation Template

```yaml
name: report_generation
description: Generate structured reports
steps:
  - name: gather_data
    action: collect_inputs
    params: {}
  
  - name: process_content
    action: organize_sections
    params:
      structure: "standard"
  
  - name: format_output
    action: apply_template
    params:
      style: "professional"
  
  - name: review
    action: quality_check
    params: {}
  
  - name: finalize
    action: export_document
    params:
      format: "{output_format}"
```

---

## Template Customization

### Creating Custom Templates

```python
from scripts.workflow_templates import TemplateManager

templates = TemplateManager()

# Create custom template
templates.create(
    name="email_digest",
    description="Generate daily email digest",
    steps=[
        {"name": "fetch_emails", "action": "get_emails", "params": {"hours": 24}},
        {"name": "categorize", "action": "classify", "params": {"categories": ["urgent", "normal", "newsletter"]}},
        {"name": "summarize", "action": "create_summary", "params": {}},
        {"name": "send_digest", "action": "email", "params": {"to": "{user_email}"}}
    ]
)
```

### Template Parameters

| Parameter Type | Example | Description |
|---------------|---------|-------------|
| `{input_file}` | `report.pdf` | User-provided input |
| `{output_file}` | `summary.md` | Generated output |
| `{user_preference}` | `markdown` | From user model |
| `{timestamp}` | `20260409` | Auto-generated |

---

## Context-Aware Recommendations

### Recommendation Engine

```python
class WorkflowRecommender:
    def recommend(self, context, task_description):
        """
        Recommend optimal workflow for current task.
        
        Args:
            context: Current task context
            task_description: User's task description
            
        Returns:
            List of recommended workflows with scores
        """
        # Extract task features
        features = self._extract_features(task_description)
        
        # Find matching patterns
        patterns = self.pattern_matcher.find(context, features)
        
        # Rank by suitability
        ranked = self._rank_workflows(patterns, context)
        
        return ranked
```

### Recommendation Display

```
Agent: "检测到文档处理任务，推荐以下工作流程：

       1. 文档分析流程 (推荐度: 92%)
          - 加载 → 提取 → 分析 → 摘要 → 保存
          - 适用于: PDF、Word文档
          - 平均耗时: 2分钟
       
       2. 快速摘要流程 (推荐度: 78%)
          - 加载 → 提取关键 → 生成摘要
          - 适用于: 长文档快速浏览
          - 平均耗时: 30秒
       
       选择哪个流程？"
```

---

## Workflow Execution

### Step-by-Step Execution

```python
class WorkflowExecutor:
    def execute(self, workflow, context):
        """
        Execute workflow step by step with user visibility.
        """
        results = []
        
        for i, step in enumerate(workflow.steps):
            # Show current step
            print(f"[{i+1}/{len(workflow.steps)}] 执行: {step.name}")
            
            # Execute step
            result = self._execute_step(step, context)
            results.append(result)
            
            # Update context
            context.update(result)
            
            # Checkpoint for user
            if step.checkpoint:
                self._save_checkpoint(workflow, i, context)
        
        return results
```

### Error Handling

```python
def execute_step(self, step, context):
    try:
        result = step.action(**step.params)
        return {"success": True, "output": result}
    except Exception as e:
        # Log error
        self.logger.error(f"Step {step.name} failed: {e}")
        
        # Offer recovery options
        recovery = self._suggest_recovery(step, e)
        
        return {
            "success": False,
            "error": str(e),
            "recovery_options": recovery
        }
```

---

## Performance Metrics

### Workflow Analytics

```python
class WorkflowAnalytics:
    def get_metrics(self, workflow_id):
        """
        Get performance metrics for a workflow.
        """
        return {
            "total_runs": self._count_runs(workflow_id),
            "success_rate": self._calc_success_rate(workflow_id),
            "avg_duration": self._calc_avg_duration(workflow_id),
            "common_errors": self._get_common_errors(workflow_id),
            "improvement_trend": self._calc_trend(workflow_id)
        }
```

### Metric Thresholds

| Metric | Good | Warning | Poor |
|--------|------|---------|------|
| Success Rate | > 90% | 70-90% | < 70% |
| Avg Duration | < target | ±20% | > +50% |
| Error Rate | < 5% | 5-15% | > 15% |

---

## Continuous Improvement

### Learning from Feedback

```python
class WorkflowImprover:
    def learn_from_feedback(self, workflow_id, feedback):
        """
        Improve workflow based on user feedback.
        """
        workflow = self.get_workflow(workflow_id)
        
        if feedback["type"] == "step_order":
            # User suggests different step order
            self._reorder_steps(workflow, feedback["suggestion"])
        
        elif feedback["type"] == "missing_step":
            # User identifies missing step
            self._add_step(workflow, feedback["suggestion"])
        
        elif feedback["type"] == "param_tweak":
            # User adjusts parameters
            self._update_params(workflow, feedback["suggestion"])
        
        self._save_improvement(workflow, feedback)
```

### A/B Testing

```python
def test_workflow_variant(self, workflow_id, variant):
    """
    Test workflow variant against original.
    """
    # Run both workflows
    original_results = self._run_original(workflow_id)
    variant_results = self._run_variant(variant)
    
    # Compare metrics
    comparison = {
        "success_rate_diff": variant_results.success_rate - original_results.success_rate,
        "duration_diff": variant_results.avg_duration - original_results.avg_duration,
        "user_satisfaction_diff": variant_results.satisfaction - original_results.satisfaction
    }
    
    return comparison
```

---

## Best Practices

### Workflow Design ✅

1. **Keep it simple**: Fewer steps = better maintainability
2. **Add checkpoints**: Allow resumption after failures
3. **Clear naming**: Use descriptive step names
4. **Handle errors**: Provide recovery options
5. **Log everything**: Enable debugging and analysis

### User Experience ✅

1. **Show progress**: Keep user informed
2. **Allow cancellation**: User can stop anytime
3. **Provide estimates**: Expected time/duration
4. **Offer alternatives**: Multiple workflow options
5. **Explain choices**: Why this workflow is recommended

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow execution | Too many steps | Optimize or parallelize |
| High error rate | Unstable steps | Add error handling |
| Poor recommendations | Vague context | Improve context capture |
| Low user adoption | Complex workflows | Simplify or add guidance |

### Debugging Tools

```python
# Debug workflow execution
debugger = WorkflowDebugger()
trace = debugger.trace(workflow_id)

print("Execution trace:")
for step in trace:
    print(f"  {step.name}: {step.status} ({step.duration}ms)")
    if step.error:
        print(f"    Error: {step.error}")
```

---

## Integration Example

### Complete Workflow

```python
from scripts.pattern_recorder import PatternRecorder
from scripts.memory_manager import MemoryManager
from scripts.workflow_templates import TemplateManager

# Initialize components
memory = MemoryManager()
recorder = PatternRecorder()
templates = TemplateManager()

# Get context
context = memory.get_context(user_id="default")

# Find matching patterns
patterns = recorder.recall(
    context=context,
    task_type="document_analysis"
)

# Select best pattern
if patterns:
    workflow = patterns[0].to_workflow()
else:
    # Use default template
    workflow = templates.get("document_analysis")

# Execute with visibility
executor = WorkflowExecutor()
results = executor.execute(workflow, context)

# Record success
recorder.record(
    task_type="document_analysis",
    steps=workflow.steps,
    context=context,
    success=True
)

# Update memory
memory.add_episode(
    user_input="分析文档",
    actions=[s.name for s in workflow.steps],
    outcome="成功"
)
```
