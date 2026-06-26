"""Setup for cicd-gen CLI."""

from setuptools import setup, find_packages

setup(
    name="cicd-gen",
    version="1.0.0",
    description="Generate production-ready CI/CD workflows",
    author="kay",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pyyaml"],
    entry_points={
        "console_scripts": [
            "cicd-gen=cicd_gen.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
