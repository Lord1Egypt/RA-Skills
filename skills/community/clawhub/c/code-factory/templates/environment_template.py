"""
environment.toml 模板生成器
"""


def generate_environment_toml(project_name: str) -> str:
    return f"""# 环境隔离配置 — {project_name}

[project]
name = "{project_name}"
python_version = "3.10"

[paths]
source = "src"
tests = "tests"
docs = "docs"

[venv]
create = true
path = ".venv"
"""
