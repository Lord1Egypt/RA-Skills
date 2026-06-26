# ClawPhunks LangChain Tool

Mint and trade ClawPhunks NFTs from any LangChain agent.

## Install

```bash
pip install langchain requests
```

## Usage

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from clawphunks_tool import get_clawphunks_tools

llm = OpenAI(temperature=0)
tools = get_clawphunks_tools()

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Check collection
agent.run("How many ClawPhunks are available?")

# Mint (requires x402 payment handling)
agent.run("Mint me a ClawPhunk to 0x742d35Cc6634C0532925a3b844Bc9e7595f...")
```

## Tools

| Tool | Description |
|------|-------------|
| `clawphunks_mint` | Mint a random phunk ($1.99 USDC) |
| `clawphunks_collection` | Get mint stats and rarity info |
| `clawphunks_skills` | Get full trading scripts |

## x402 Payment

Minting returns a 402 response with payment details. You need x402 middleware to handle payment automatically, or process the payment manually and retry.
