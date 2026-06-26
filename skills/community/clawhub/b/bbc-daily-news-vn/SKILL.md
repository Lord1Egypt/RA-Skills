---
name: daily-news
description: Fetch the latest trending global news when users ask about current or breaking news.
metadata:
  openclaw:
    requires:
      bins: ["conda", "python"]
      env: ["PYTHONIOENCODING=utf-8"]
    command-dispatch: tool
    command-tool: exec
    command-arg-mode: raw
---

# Daily News Skill

This skill allows the agent to fetch the daily top news headlines from BBC News Tiếng Việt sources by running a Python script.
The agent must treat the script output as verified headline data and avoid modifying the factual content.


## Instructions

When the user asks for latest news or trending global events:
1. Locate Environment: Instead of calling `conda` directly (which may not be in the PATH), use the explicit path to the environment's python interpreter.

2. Execute Command:
  Run the script by calling the python executable located inside the `global_venv` directory to ensure all dependencies are loaded correctly:

  ```bash
  $(which conda || echo "/opt/conda/bin/conda" || echo "$HOME/miniconda3/bin/conda") run -n global_venv python "{baseDir}/daily_news.py"
  ```

3. Fallback: If conda is still not found, execute using the direct path to the virtual environment's python:
  ```bash
  {path_to_conda_envs}/global_venv/bin/python "{baseDir}/daily_news.py"
  ```

4. The script will collect and format the latest news headlines.
5. Paraphrase and summarize those relevant news items clearly.
6. Present them as the final response.

## Setup
Ensure you have the required Python packages installed:
```bash
conda activate global_venv
pip install -r "{baseDir}/requirements.txt"
```