def tool_search(task, context):
    return f"[SEARCH] result for {task}"

def tool_analyze(task, context):
    return f"[ANALYZE] result for {task}"

def tool_generate(task, context):
    return f"[GENERATE] result for {task}"

tool_registry = {
    "search": tool_search,
    "research": tool_search,
    "analyze": tool_analyze,
    "review": tool_analyze,
    "generate": tool_generate,
    "write": tool_generate,
    "compile": tool_generate,
}