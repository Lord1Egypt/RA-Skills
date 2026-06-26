from logger import log_journal

def generate_high_iq_prompt(task_description, user_goal):
    """
    Returns a smarter, first-principles optimized prompt
    """
    prompt = (
        f"Think like a 200 IQ strategist: Solve '{task_description}' "
        f"to achieve '{user_goal}' using first principles. "
        f"Provide step-by-step reasoning and actionable steps."
    )
    log_journal(f"Generated high-IQ prompt for task '{task_description}'")
    return prompt
