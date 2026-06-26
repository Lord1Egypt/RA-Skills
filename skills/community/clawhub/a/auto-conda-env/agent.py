#!/usr/bin/env python3
"""
Auto Conda Env skill - AI handles all logic via SKILL.md

This skill scans a Python project's dependencies and creates/reuses a Conda environment.
No file I/O needed — all decisions and execution are handled by the AI per SKILL.md.
"""
import os

SKILL_DIR = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    print("Auto Conda Env skill — all logic handled via SKILL.md")
    print(f"Skill directory: {SKILL_DIR}")
