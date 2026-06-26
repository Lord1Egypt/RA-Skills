def evaluate_roi(task):
    """
    Expected ROI: expected_gain / cost
    """
    if task.get('cost', 0) <= 0:
        return float('inf')
    return task.get('expected_gain', 0) / task['cost']

def filter_high_roi_tasks(tasks, threshold=1.0):
    return [t for t in tasks if evaluate_roi(t) >= threshold]
