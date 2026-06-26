from setuptools import setup, find_packages

setup(
    name="ai-model-steward",
    version="0.1.0",
    description="AI 模型智能管家 - 全自动模型监控、情报搜集与智能部署建议系统",
    author="老徐",
    license="MIT",
    python_requires=">=3.8",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "ai-model-steward=ai_model_steward.cli:main",
        ],
    },
)
