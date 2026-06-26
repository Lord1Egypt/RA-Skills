#!/usr/bin/env python3
"""
法大大电子签 SDK - 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fadada-esign",
    version="2.0.0",
    author="FaDaDa E-Sign Team",
    author_email="support@fadada.com",
    description="法大大电子合同与电子签署 SDK (FASC API 5.0)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fadada/fadada-esign-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "cli": [],
        "excel": ["pandas>=1.0.0", "openpyxl>=3.0.0"],
        "dev": ["pytest>=6.0", "black", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "fadada=fadada_esign.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
