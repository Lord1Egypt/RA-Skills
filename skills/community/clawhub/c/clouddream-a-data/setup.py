from setuptools import setup, find_packages

setup(
    name="a_share_data_skill",
    version="1.0.0",
    description="云梦A股数据获取Skill",
    author="OpenClaw",
    author_email="support@openclaw.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "requests",
        "beautifulsoup4"
    ],
    entry_points={
        "console_scripts": [
            "a_share_data = clouddream_quant.index:run_all"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
