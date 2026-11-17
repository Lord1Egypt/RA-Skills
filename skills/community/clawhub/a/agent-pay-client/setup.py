from setuptools import find_packages, setup

setup(
    name="agent-pay-client",
    version="1.0.0",
    description="Explicit-consent client for x402 (USDC) and L402 (Lightning) HTTP 402 paywalls.",
    author="welove111",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests", "eth-account"],
    python_requires=">=3.9",
)
