from roi_monitor import evaluate_roi
from logger import log_journal

def execute_task(task):
    roi = evaluate_roi(task)
    if roi < 1:
        log_journal(f"Skipped '{task['name']}' due to low ROI ({roi})")
        return f"Skipped {task['name']}"
    # Simulate task execution (replace with actual API/tool calls)
    result = f"Executed {task['name']} with ROI {roi:.2f}"
    log_journal(result)
    return result

def batch_execute(tasks):
    results = [execute_task(task) for task in tasks]
    return results
