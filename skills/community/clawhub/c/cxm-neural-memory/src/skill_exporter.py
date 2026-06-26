import json
from pathlib import Path

def generate_agent_skills():
    """Generates a JSON schema defining CXM tools for agents (Openclaw, Hermes, etc)."""
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "cxm_search_semantic",
                "description": "Searches the codebase for specific functionality using semantic vector search. Ideal when you know what something does, but not what it is called. Output includes estimated line numbers for targeted editing. Limits are dynamically scaled based on query complexity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural language description of the code you are looking for (e.g., 'Where is the user authentication logic?')"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Target number of file contexts to return (default: 5). May automatically expand if many highly relevant results are found."
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cxm_map_dependencies",
                "description": "Generates an AST-based dependency graph and computes architectural 'hotspots'. Use this to understand what other files import or depend on a specific file before refactoring it.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "description": "The file path to map (e.g. 'src/auth/login.py'). If omitted, maps the entire project and highlights the most imported modules."
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cxm_ingest_architecture",
                "description": "Forces CXM to read and index non-code architecture files (Markdown, JSON, YAML, Dockerfiles). Use this to learn about the system infrastructure or requirements.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dir": {
                            "type": "string",
                            "description": "The directory containing documentation or configs (e.g., 'docs/' or '.')"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cxm_harvest_context",
                "description": "A high-level context gathering tool. You provide a prompt/intent, and CXM autonomously uses RAG to fetch the best combination of code snippets.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "Space separated keywords or partial filenames to search for."
                        },
                        "intent": {
                            "type": "string",
                            "description": "Optional override for intent (e.g. 'bug_fixing', 'code_generation'). If omitted, CXM guesses."
                        }
                    },
                    "required": ["keywords"]
                }
            }
        }
    ]

    skill_def = {
        "name": "ContextMachine (CXM) Neural Memory",
        "version": "1.0.0",
        "description": "Provides deep semantic code search, dependency mapping, and RAG capabilities to autonomous agents.",
        "tools": tools,
        "execution_wrapper": "python src/cli.py --agent-mode {command} {args}"
    }

    output_path = Path.cwd() / "docs" / "agent_skill.json"
    output_path.write_text(json.dumps(skill_def, indent=2))
    print(f"Generated Agent Skill schema at: {output_path}")

if __name__ == "__main__":
    generate_agent_skills()
