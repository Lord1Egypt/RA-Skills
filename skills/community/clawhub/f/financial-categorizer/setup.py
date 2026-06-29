from setuptools import setup

setup(
    name="financial-categorizer",
    packages=["financial_categorizer"],
    py_modules=["cli"],
    entry_points={
        "console_scripts": [
            "financial-categorizer=cli:main",
        ],
    },
)
