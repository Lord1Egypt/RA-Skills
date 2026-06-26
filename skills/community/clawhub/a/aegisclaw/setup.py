#!/usr/bin/env python3
"""
金甲龙虾 (AegisClaw) - 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aegisclaw",
    version="1.0.0",
    author="AegisClaw Team",
    author_email="",
    description="🦞 金甲龙虾 - 币安安全赚币与护境神将",
    long_description=long_description,
    url="https://github.com/hyy2099/aegisclaw",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "python-dateutil>=2.8.2",
    ],
    keywords=[
        "binance",
        "trading",
        "arbitrage",
        "security",
        "ai",
        "cryptocurrency",
        "bnb",
        "launchpool",
        "funding-rate"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "aegisclaw=main:main",
        ],
    },
)
