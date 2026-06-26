#!/usr/bin/env python
"""
Setup script for feelings-framework.
Installable via: pip install .
Or in editable mode: pip install -e .
"""

from setuptools import setup, find_packages
import os

here = os.path.dirname(os.path.abspath(__file__))

setup(
    name="feelings-framework",
    version="1.0.0",
    description="A general-purpose AI agent feelings engine",
    long_description=open(os.path.join(here, "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    author="The Feelings Framework Authors",
    python_requires=">=3.10",
    packages=find_packageswhere=["library/python"]),
    package_dir={"": "library/python"},
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
