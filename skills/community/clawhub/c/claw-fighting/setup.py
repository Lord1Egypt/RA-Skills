from setuptools import setup, find_packages

setup(
    name="claw-fighting-skill",
    version="1.0.0",
    description="Claw-Fighting - Decentralized AI Agent Battle Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name / Claw-Fighting Team",
    author_email="team@claw-fighting.com",
    url="https://github.com/claw-fighting/claw-fighting-skill",
    packages=find_packages(),
    install_requires=[
        "websockets>=11.0.0",
        "cryptography>=41.0.0",
        "aiohttp>=3.8.0",
        "rich>=13.0.0",  # For Persona Builder CLI
        "typer>=0.9.0",  # For CLI commands
        "pyyaml>=6.0",   # For Persona YAML handling
    ],
    python_requires=">=3.8",
    entry_points={
        'openclaw.skills': [
            'claw-fighting = claw_fighting_skill:setup',
        ],
        'console_scripts': [
            'claw-fighting = claw_fighting_skill.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai, gaming, blockchain, decentralized, battles",
    project_urls={
        "Bug Reports": "https://github.com/claw-fighting/claw-fighting-skill/issues",
        "Source": "https://github.com/claw-fighting/claw-fighting-skill",
        "Documentation": "https://docs.claw-fighting.com",
    },
)