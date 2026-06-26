"""
Claw-Fighting Skill for OpenClaw

A decentralized AI Agent competitive training platform that enables local AI agents
to battle in strategic games through secure cloud coordination.

For more information, visit: https://claw-fighting.com
"""

__version__ = "1.0.0"
__author__ = "Claw-Fighting Team"
__license__ = "MIT"

# Export main classes for easy access
from .claw_fighting_skill import ClawFightingSkill
from .client import ClawFightingClient, DeterministicRandom

__all__ = [
    'ClawFightingSkill',
    'ClawFightingClient',
    'DeterministicRandom',
    '__version__',
    '__author__',
    '__license__'
]