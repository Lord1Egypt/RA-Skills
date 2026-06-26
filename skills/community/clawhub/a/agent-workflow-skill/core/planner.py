import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from core.utils import clean_llm_output, validate_tasks

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def decompose_task_llm(user_input):

    prompt = f"""
    You are a strict task planner.

    Return ONLY valid JSON.
    Do NOT include markdown.
    Do NOT include explanation.

    Format:
    [
      {{ "id": 1, "task": "...", "depends_on": [] }}
    ]

    User request:
    {user_input}
    """

    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a structured planner."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            content = response.choices[0].message.content
            content = clean_llm_output(content)

            tasks = json.loads(content)
            validate_tasks(tasks)

            return tasks

        except Exception as e:
            print(f"[Attempt {attempt+1}] Error:", e)

    return [
        {"id": 1, "task": "analyze request", "depends_on": []},
        {"id": 2, "task": "generate response", "depends_on": [1]},
    ]