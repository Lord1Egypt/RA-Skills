from setuptools import setup

setup(
    name="deepaistudy-errors",
    version="1.0.4",
    scripts=["deepaistudy_errors.py"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "deepaistudy-errors=deepaistudy_errors:main",
        ],
    },
    python_requires=">=3.8",
)
