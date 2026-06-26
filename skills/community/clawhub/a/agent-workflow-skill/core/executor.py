from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from core.tools import tool_registry


def run_task(task, context):
    task_name = task["task"].lower()
    print(f"Running: {task_name}")

    # collect dependency results
    inputs = [context.get(dep, "") for dep in task["depends_on"]]
    input_text = " | ".join(inputs)

    for key, tool in tool_registry.items():
        if key in task_name:
            result = tool(task_name + " | " + input_text, context)
            break
    else:
        result = f"[DEFAULT] {task_name} | inputs: {input_text}"

    context[task["id"]] = result
    time.sleep(1)

    return task["id"], result


def execute_tasks(tasks):

    completed = set()
    results = {}
    execution_order = []

    while len(completed) < len(tasks):

        runnable = [
            task for task in tasks
            if task["id"] not in completed
            and all(dep in completed for dep in task["depends_on"])
        ]

        if not runnable:
            raise RuntimeError("Deadlock detected")

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(run_task, task, results) for task in runnable]

            for future in as_completed(futures):
                task_id, result = future.result()

                print(f"Completed: {result}")
                execution_order.append(result)
                completed.add(task_id)

    return execution_order