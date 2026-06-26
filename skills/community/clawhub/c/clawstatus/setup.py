import re
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("clawstatus.py", "r", encoding="utf-8") as f:
    version = re.search(r'__version__\s*=\s*"(.+?)"', f.read()).group(1)

setup(
    name="clawstatus",
    version=version,
    description="ClawStatus - OpenClaw status dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["clawstatus"],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0",
        "waitress>=2.0",
    ],
    entry_points={
        "console_scripts": [
            "clawstatus=clawstatus:main",
        ],
    },
)
