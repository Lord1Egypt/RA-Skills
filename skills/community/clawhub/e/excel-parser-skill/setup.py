#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='excel-parser-skill',
    version='1.0.0',
    description='Excel content parsing skill using calamine library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Excel Parser Skill Team',
    author_email='',
    url='',
    packages=find_packages(),
    package_data={
        '': ['*.md', '*.txt', '*.env.example'],
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'excel-parser=scripts.excel_parser:main',
        ],
    },
)
