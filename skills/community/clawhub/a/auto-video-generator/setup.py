#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for Auto Video Generator
======================================

This is a legacy setup.py for compatibility with older pip versions.
Primary configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
import os

# Read version from package
version = "3.0.0"

# Read long description from README
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="auto-video-generator",
    version=version,
    
    # Package metadata
    author="AVG Team",
    author_email="team@avg.dev",
    maintainer="AVG Team",
    maintainer_email="team@avg.dev",
    url="https://github.com/avg-team/auto-video-generator",
    license="MIT",
    
    description="Professional demo video generation from HTML pages with AI voice narration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    keywords=[
        "video-generation", "demo", "screenshot", "automation",
        "testing", "playwright", "tts", "voice-over", "presentation"
    ],
    
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Software Development :: Testing",
    ],
    
    python_requires=">=3.8",
    
    packages=find_packages(exclude=['tests', 'tests.*', '*.tests', '*.tests.*']),
    
    install_requires=[
        "playwright>=1.40.0",
        "edge-tts>=6.1.0",
        "Pillow>=10.0.0",
        "ffmpeg-python>=0.2.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "click>=8.1.0",
        "aiofiles>=23.0.0",
        "httpx>=0.25.0",
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "web": [
            "flask>=3.0.0",
            "flask-cors>=4.0.0",
            "flask-socketio>=5.3.0",
        ],
        "all": [
            "auto-video-generator[dev,web]",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "avg = auto_video_generator.cli:main",
            "avg-generate = auto_video_generator.cli:generate",
            "avg-web = auto_video_generator.web:start_web_ui",
            "avg-init = auto_video_generator.cli:init_project",
        ],
        "avg.adapters": [
            "ant-design-vue = auto_video_generator.adapters:AntDesignVueAdapter",
            "react-antd = auto_video_generator.adapters:ReactAntdAdapter",
            "element-ui = auto_video_generator.adapters:ElementUIAdapter",
            "vuetify = auto_video_generator.adapters:VuetifyAdapter",
            "naive-ui = auto_video_generator.adapters:NaiveUIAdapter",
            "arco-design = auto_video_generator.adapters:ArcoDesignAdapter",
        ],
    },
    
    include_package_data=True,
    zip_safe=False,
)
