"""
财务报表审查工具 - 安装配置
Financial Statement Review Tool - Setup Configuration
"""
from setuptools import setup, find_packages
from pathlib import Path

# 读取 README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# 读取 requirements.txt
requirements = []
if (this_directory / "requirements.txt").exists():
    with open(this_directory / "requirements.txt", encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="financial-statement-review",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="基于中国会计准则和税法的财务报表智能审查工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/financial-statement-review",
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'examples']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "pdf": [
            "pdfplumber>=0.6.0",
            "PyPDF2>=3.0.0",
        ],
        "word": [
            "python-docx>=0.8.11",
        ],
    },
    entry_points={
        "console_scripts": [
            "fsr-review=scripts.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.md", "*.txt"],
        "data": ["*.csv"],
        "references": ["*.md"],
    },
    zip_safe=False,
    keywords="财务, 会计, 审计, 税务, 报表, 审查, finance, accounting, audit, tax, statement",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/financial-statement-review/issues",
        "Source": "https://github.com/yourusername/financial-statement-review",
        "Documentation": "https://github.com/yourusername/financial-statement-review/wiki",
    },
)
