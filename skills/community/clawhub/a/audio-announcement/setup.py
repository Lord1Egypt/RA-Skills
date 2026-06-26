"""audio-announcement: Make your OpenClaw Agent talk!"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README.md
this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8") if (this_dir / "README.md").exists() else ""

setup(
    name="audio-announcement",
    version="2.0.8",
    author="miaoweilin (wililam)",
    author_email="uinecn@126.com",
    description="Make your OpenClaw Agent talk! Real-time voice announcements for AI actions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wililam/audio-announcement-skills",
    project_urls={
        "Bug Reports": "https://github.com/wililam/audio-announcement-skills/issues",
        "Source": "https://github.com/wililam/audio-announcement-skills",
        "ClawHub": "https://clawhub.ai/skill/audio-announcement",
    },
    packages=find_packages(include=["audio_announcement", "audio_announcement.*"]),
    include_package_data=True,
    package_data={
        "audio_announcement": ["scripts/*.py", "scripts/*.sh"],
    },
    install_requires=[
        "edge-tts>=6.1.3",
        "pygame>=2.0.0; platform_system=='Windows'",
    ],
    extras_require={
        "dev": ["pytest", "black"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "audio-announce=audio_announcement.cli:main",
        ],
    },
    keywords=["openclaw", "tts", "text-to-speech", "announcement", "voice", "audio"],
)
