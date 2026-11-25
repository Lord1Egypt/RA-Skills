"""AgentPathfinder — pip-installable setup."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentpathfinder",
    version="1.3.0",
    author="CertainLogic",
    author_email="hello@certainlogic.ai",
    description="Cryptographically signed audit trails for AI agent tool calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CertainLogicAI/agentpathfinder",
    packages=find_packages(include=["agentpathfinder*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-asyncio>=0.21"],
    },
    entry_points={
        "console_scripts": [
            "pf=agentpathfinder.__main__:main",
            "agentpathfinder=agentpathfinder.__main__:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
