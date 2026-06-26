#!/usr/bin/env python3
"""Setup script for Daily Intelligence Briefing."""

from setuptools import setup, find_packages

setup(
    name="daily-briefing",
    version="1.0.0",
    description="Daily AI/Tech intelligence briefing generator for global audiences",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sun Wukong",
    author_email="sunwukong@openclaw.ai",
    url="https://github.com/openclaw/daily-briefing",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: News :: News/Weather",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="ai tech news briefing automation openclaw",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "briefing=daily_briefing.scripts.briefing:main",
        ],
    },
)
