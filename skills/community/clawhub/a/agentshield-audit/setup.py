"""
AgentShield Audit - Setup Script

Enables pip installation of the skill as a Python package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "scripts" / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")

setup(
    name="agentshield-audit",
    version="1.0.0",
    description="AgentShield security audit framework for AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kalle-OC (bartelmost)",
    author_email="",
    url="https://github.com/bartelmost/agentshield",
    license="MIT",
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Include non-Python files
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.md", "*.txt"],
    },
    
    # Dependencies
    install_requires=requirements,
    python_requires=">=3.8",
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "agentshield-audit=scripts.initiate_audit:main",
            "agentshield-verify=scripts.verify_peer:main",
            "agentshield-cert=scripts.show_certificate:main",
        ],
    },
    
    # Metadata
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
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ai agent security audit cryptography trust certificates",
    
    # Additional URLs
    project_urls={
        "Bug Reports": "https://github.com/bartelmost/agentshield/issues",
        "Source": "https://github.com/bartelmost/agentshield",
        "Documentation": "https://github.com/bartelmost/agentshield",
    },
)
