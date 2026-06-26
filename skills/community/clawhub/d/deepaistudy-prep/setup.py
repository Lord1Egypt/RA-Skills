from setuptools import setup, find_packages

setup(
    name="deepaistudy-prep",
    version="1.0.0",
    packages=find_packages(),
    scripts=["deepaistudy_prep.py"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "deepaistudy-prep=deepaistudy_prep:main",
        ],
    },
    python_requires=">=3.8",
)
