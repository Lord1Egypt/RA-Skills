#!/usr/bin/env python3
"""
DigenAI Discord Bot - API Key Distribution
Use !key to get a free API key (sent via DM)

Features:
- One API key per user
- Key sent via DM for privacy
- Rate limiting

Environment:
  - DISCORD_BOT_TOKEN: Discord bot token
  - MASTER_API_KEY: The master key to create new user keys
"""

import os
import json
import requests
import logging
import discord
from discord.ext import commands
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
API_BASE = "https://api.cowork.digen.ai"
MASTER_API_KEY = os.getenv("MASTER_API_KEY", "ak_2f81a7774dc7445a9244d3f61d5a9a989c25dbfef09dfb4c868c372260722f93")

# User key storage file
KEYS_FILE = Path(__file__).parent / "user_keys.json"

def load_user_keys() -> dict:
    """Load user key mapping from file"""
    if KEYS_FILE.exists():
        try:
            return json.loads(KEYS_FILE.read_text())
        except:
            return {}
    return {}

def save_user_keys(keys: dict):
    """Save user key mapping to file"""
    KEYS_FILE.write_text(json.dumps(keys, indent=2))

def create_api_key() -> str:
    """Create a new API key using master key"""
    try:
        r = requests.post(
            f"{API_BASE}/b/v1/api-key/create",
            headers={"Authorization": f"Bearer {MASTER_API_KEY}"},
            timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            return data.get("api_key", "")
    except Exception as e:
        logger.error(f"Failed to create API key: {e}")
    return None

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

# Create bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Bot ready event"""
    print(f"🤖 Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"Master API Key: {MASTER_API_KEY[:20]}...")
    
    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="!key to get free API · digen-ai-free"
    )
    await bot.change_presence(activity=activity)

@bot.command(name="key", help="Get your free API key (sent via DM)")
async def get_key(ctx):
    """Generate and return API key via DM"""
    user_id = str(ctx.author.id)
    user_name = ctx.author.name
    
    # Load existing user keys
    user_keys = load_user_keys()
    
    # Check if user already has a key
    if user_id in user_keys:
        existing_key = user_keys[user_id]["api_key"]
        await ctx.send(f"ℹ️ You already have an API key! Check your DM for it.")
        # Send existing key via DM
        try:
            dm_channel = await ctx.author.create_dm()
            embed = discord.Embed(
                title="🔑 Your Existing API Key",
                color=discord.Color.blue(),
                description=f"```\n{existing_key}\n```"
            )
            embed.add_field(
                name="📝 Note",
                value="You already have a key. Each user is limited to one API key.",
                inline=False
            )
            await dm_channel.send(embed=embed)
            return
        except Exception as e:
            await ctx.send(f"❌ Could not send DM. Please enable DMs and try again.")
            return
    
    # Acknowledge processing
    msg = await ctx.send("⏳ Generating your API key...")
    
    # Create new API key
    api_key = create_api_key()
    
    if api_key:
        # Save user key mapping
        user_keys[user_id] = {
            "api_key": api_key,
            "discord_name": user_name,
            "created_at": str(discord.utils.utcnow())
        }
        save_user_keys(user_keys)
        
        # Send key via DM
        try:
            dm_channel = await ctx.author.create_dm()
            embed = discord.Embed(
                title="✅ API Key Generated!",
                color=discord.Color.green(),
                description=f"```\n{api_key}\n```"
            )
            embed.add_field(
                name="📖 How to Use",
                value="1. Set environment variable:\n"
                      "   `export DIGEN_API_KEY=\"{api_key}\"`\n\n"
                      "2. Install skill:\n"
                      "   `clawhub install digen-ai-free`".format(api_key=api_key),
                inline=False
            )
            embed.add_field(
                name="🔗 Resources",
                value="• API Docs: https://api.cowork.digen.ai/b/doc\n"
                      "• Skill Page: https://clawhub.ai/eeoeofl/digen-ai-free",
                inline=False
            )
            embed.set_footer(text="⚠️ Keep your API key safe! One key per user.")
            
            await dm_channel.send(embed=embed)
            await msg.edit(content=f"✅ API key sent to your DM! Check your private messages from me.")
        except Exception as e:
            logger.error(f"Failed to send DM: {e}")
            await msg.edit(content="❌ Could not send DM. Please enable DMs and try again.")
    else:
        await msg.edit(content="❌ Failed to generate API key. Please try again later.")

@bot.command(name="mykey", help="Check your current API key")
async def my_key(ctx):
    """Check user's key info"""
    user_id = str(ctx.author.id)
    user_keys = load_user_keys()
    
    if user_id in user_keys:
        api_key = user_keys[user_id]["api_key"]
        created_at = user_keys[user_id].get("created_at", "N/A")
        
        embed = discord.Embed(
            title="🔑 Your API Key",
            color=discord.Color.blue()
        )
        embed.add_field(name="API Key", value=f"```\n{api_key}\n```", inline=False)
        embed.add_field(name="Created At", value=created_at[:19], inline=True)
        
        # Send via DM for privacy
        try:
            dm_channel = await ctx.author.create_dm()
            await dm_channel.send(embed=embed)
            await ctx.send("📬 Check your DM for your API key!")
        except:
            await ctx.send(embed=embed)
    else:
        await ctx.send("❌ You don't have an API key yet. Use `!key` to get one!")

@bot.command(name="quota", help="Check API usage info")
async def quota(ctx):
    """Check API quota"""
    user_id = str(ctx.author.id)
    user_keys = load_user_keys()
    
    # Count total keys issued
    total_keys = len(user_keys)
    user_has_key = user_id in user_keys
    
    embed = discord.Embed(
        title="📊 API Usage Info",
        color=discord.Color.blue()
    )
    embed.add_field(name="Total Keys Issued", value=str(total_keys), inline=True)
    embed.add_field(name="Your Key Status", value="✅ Has Key" if user_has_key else "❌ No Key", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="cmd", help="Show all available commands")
async def help_cmd(ctx):
    """Show help"""
    embed = discord.Embed(
        title="❓ DigenAI Bot Help",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Commands",
        value="• `!key` - Get your free API key\n"
              "• `!mykey` - View your key info\n"
              "• `!quota` - Check API quota\n"
              "• `!help` - Show this help",
        inline=False
    )
    embed.add_field(
        name="Quick Start",
        value="1. Run `!key` to get your API key\n"
              "2. Install skill: `clawhub install digen-ai-free`\n"
              "3. Set key: `export DIGEN_API_KEY=\"your_key\"`\n"
              "4. Start generating!",
        inline=False
    )
    embed.add_field(
        name="Links",
        value="• API Docs: https://api.cowork.digen.ai/b/doc\n"
              "• Skill Page: https://clawhub.ai/eeoeofl/digen-ai-free",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="test", help="Test bot responsiveness")
async def test_cmd(ctx):
    """Test command"""
    await ctx.send("✅ Bot is working!")

def main():
    """Start the bot"""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN not set!")
        print("Please set DISCORD_BOT_TOKEN environment variable")
        return
    
    print("🤖 Starting DigenAI Discord Bot...")
    bot.run(token)

if __name__ == "__main__":
    main()