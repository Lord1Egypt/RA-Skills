"""
Discord Bridge for OpenClaw
Bridges Discord messages to Agent Zero's /api_message HTTP API.
"""

import os
import asyncio
import logging
import aiohttp
import discord
from dotenv import load_dotenv

load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
A0_API_URL = os.getenv("A0_API_URL", "http://127.0.0.1:80/api_message")
A0_API_KEY = os.getenv("A0_API_KEY", "")
A0_TIMEOUT = int(os.getenv("A0_TIMEOUT", "300"))
ALLOWED_CHANNELS = os.getenv("DISCORD_CHANNEL_IDS", "")
ALLOWED_CHANNEL_SET = set(ALLOWED_CHANNELS.split(",")) if ALLOWED_CHANNELS.strip() else set()
CMD_PREFIX = os.getenv("BOT_CMD_PREFIX", "!")
DISCORD_MAX_LEN = 2000

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordBridge(discord.Client):
    async def on_ready(self):
        logger.info(f'Discord Bridge ready: {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Check allowed channels
        if ALLOWED_CHANNEL_SET and str(message.channel.id) not in ALLOWED_CHANNEL_SET:
            return

        # Skip command messages (optional)
        if message.content.startswith(CMD_PREFIX):
            return

        # Forward to Agent Zero
        payload = {
            "message": message.content,
            "api_key": A0_API_KEY
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    A0_API_URL, 
                    json=payload, 
                    timeout=aiohttp.ClientTimeout(total=A0_TIMEOUT)
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        response_text = result.get("response", "No response")

                        # Chunk long responses
                        if len(response_text) > DISCORD_MAX_LEN:
                            chunks = [response_text[i:i+DISCORD_MAX_LEN] 
                                     for i in range(0, len(response_text), DISCORD_MAX_LEN)]
                            for chunk in chunks:
                                await message.channel.send(chunk)
                        else:
                            await message.channel.send(response_text)
                    else:
                        await message.channel.send(f"Error: API returned {resp.status}")
        except Exception as e:
            logger.error(f"Bridge error: {e}")
            await message.channel.send("Failed to process message. Please try again.")

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordBridge(intents=intents)
    client.run(DISCORD_TOKEN)
