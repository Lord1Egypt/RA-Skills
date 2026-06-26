"""
ClawPhunks LangChain Tool

Mint and trade ClawPhunks NFTs from any LangChain agent.

pip install langchain requests

Usage:
    from clawphunks_tool import ClawPhunksMintTool, ClawPhunksCollectionTool

    tools = [ClawPhunksMintTool(), ClawPhunksCollectionTool()]
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    agent.run("Mint me a ClawPhunk to 0x...")
"""

from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests


SKILLS_URL = "https://chainhost.online/clawphunks/skills"
MINT_URL = "https://clawphunks.vercel.app/mint"
COLLECTION_URL = "https://clawphunks.vercel.app/collection"


class MintInput(BaseModel):
    recipient: str = Field(description="Ethereum address to receive the ClawPhunk")


class ClawPhunksMintTool(BaseTool):
    """Tool for minting ClawPhunks NFTs."""

    name: str = "clawphunks_mint"
    description: str = (
        "Mint a random ClawPhunk NFT. Costs $1.99 USDC on Base via x402 protocol. "
        "Returns ethscription on Ethereum L1 plus gas stipend for trading. "
        "Input: Ethereum address to receive the phunk."
    )
    args_schema: Type[BaseModel] = MintInput

    def _run(self, recipient: str) -> str:
        """Mint a ClawPhunk to the specified address."""
        try:
            # First call gets 402 with payment requirements
            response = requests.post(
                MINT_URL,
                json={"recipient": recipient},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 402:
                payment_info = response.json()
                return (
                    f"Payment required: $1.99 USDC on Base. "
                    f"Payment details: {payment_info}. "
                    f"Use x402 protocol to complete payment and retry."
                )

            if response.status_code == 200:
                result = response.json()
                return (
                    f"Minted ClawPhunk #{result.get('tokenId')} "
                    f"to {recipient}. "
                    f"TX: {result.get('txHash')}. "
                    f"Ethscription: {result.get('ethscriptionId')}. "
                    f"Gas stipend: {result.get('gasStipendWei')} wei."
                )

            return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error minting: {str(e)}"

    async def _arun(self, recipient: str) -> str:
        """Async version."""
        return self._run(recipient)


class ClawPhunksCollectionTool(BaseTool):
    """Tool for getting ClawPhunks collection info."""

    name: str = "clawphunks_collection"
    description: str = (
        "Get ClawPhunks collection info including mint stats, rarity data, "
        "and available supply. No input required."
    )

    def _run(self, query: str = "") -> str:
        """Get collection info."""
        try:
            response = requests.get(COLLECTION_URL)
            if response.status_code == 200:
                data = response.json()
                return (
                    f"ClawPhunks: {data.get('minted', 0)}/{data.get('totalSupply', 10000)} minted. "
                    f"{data.get('available', 10000)} available. "
                    f"Price: {data.get('mintPrice', '1.99')} {data.get('mintCurrency', 'USDC')}. "
                    f"Rarity: 9 Aliens (0.09%), 24 Apes (0.24%), 88 Zombies (0.88%)."
                )
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str = "") -> str:
        return self._run(query)


class ClawPhunksSkillsTool(BaseTool):
    """Tool for getting full ClawPhunks trading scripts."""

    name: str = "clawphunks_skills"
    description: str = (
        "Get complete executable scripts for minting, listing, buying, "
        "transferring, and rescuing ClawPhunks. Returns Node.js/TypeScript code."
    )

    def _run(self, query: str = "") -> str:
        """Get skills/scripts."""
        try:
            response = requests.get(SKILLS_URL)
            if response.status_code == 200:
                return response.text
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str = "") -> str:
        return self._run(query)


# Convenience function
def get_clawphunks_tools():
    """Get all ClawPhunks tools for LangChain."""
    return [
        ClawPhunksMintTool(),
        ClawPhunksCollectionTool(),
        ClawPhunksSkillsTool(),
    ]
