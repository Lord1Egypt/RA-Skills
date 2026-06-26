from core.planner import decompose_task_llm
from core.executor import execute_tasks
import json

if __name__ == "__main__":
    user_input = input("Enter task: ")

    print("\n--- LLM Task Decomposition ---")
    tasks = decompose_task_llm(user_input)
    print(json.dumps(tasks, indent=2))

    print("\n--- Execution ---")
    result = execute_tasks(tasks)

    print("\n--- Final Execution Order ---")
    print(result)