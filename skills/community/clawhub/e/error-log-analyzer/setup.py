"""
Setup script for Error Log Analyzer
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="error-log-analyzer",
    version="1.0.0",
    author="Max_Gaan",
    author_email="support@maxgaan.com",
    description="AI-powered error log analyzer with plain English explanations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxgaan/error-log-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "anthropic>=0.18.0",
        "openai>=1.0.0",
        "python-Levenshtein>=0.23.0",
    ],
    extras_require={
        "web": ["flask>=3.0.0"],
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.0.0",
            "flake8>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "error-analyzer=src:main",
        ],
    },
)
