from logger import log_journal

def self_correct(task_results):
    lessons = []
    for r in task_results:
        if "Skipped" in r:
            lessons.append("Task skipped: consider lowering cost or increasing expected gain")
        elif "Executed" in r:
            lessons.append("Task executed successfully: continue strategy")
    log_journal("Lessons Learned: " + "; ".join(lessons))
    return lessons
