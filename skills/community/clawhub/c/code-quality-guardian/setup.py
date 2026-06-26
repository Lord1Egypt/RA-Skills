"""
Code Quality Guardian - Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# 读取 requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text(encoding="utf-8").split("\n")
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="code-quality-guardian",
    version="1.0.0",
    description="A comprehensive code quality analysis tool supporting Python, JavaScript, and Go",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ClawHub",
    author_email="admin@clawhub.com",
    url="https://github.com/clawhub/code-quality-guardian",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "quality-guardian=code_quality_guardian.cli:cli",
            "cqg=code_quality_guardian.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    keywords="code quality analysis lint security complexity",
    project_urls={
        "Bug Reports": "https://github.com/clawhub/code-quality-guardian/issues",
        "Source": "https://github.com/clawhub/code-quality-guardian",
    },
)
