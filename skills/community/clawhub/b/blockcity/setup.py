from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blockcity-skill",
    version="1.2.0",
    author="hgta23",
    author_email="hgta23@hotmail.com",
    description="ClawHub Skill for fetching BlockCity data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hgta23/blockcity-skill",
    packages=find_packages(),
    py_modules=["blockcity_skill"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
    ],
    keywords="blockcity skill clawhub api",
    project_urls={
        "Bug Reports": "https://github.com/hgta23/blockcity-skill/issues",
        "Source": "https://github.com/hgta23/blockcity-skill",
    },
)
