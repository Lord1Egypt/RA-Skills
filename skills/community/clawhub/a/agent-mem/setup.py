from setuptools import setup, find_packages

setup(
    name="agent-mem",
    version="0.1.0",
    description="Multi-Agent Memory + Dispatch System",
    author="AgentMem Contributors",
    packages=find_packages(),
    install_requires=[
        "chromadb>=0.4.0",
    ],
    python_requires=">=3.10",
)
