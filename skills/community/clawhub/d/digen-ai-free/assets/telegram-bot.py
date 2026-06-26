#!/usr/bin/env python3
"""
DigenAI Telegram Bot - API Key Distribution
Use /key to get a free API key (sent via DM)

Features:
- One API key per user
- Key sent via DM for privacy
- User limiting to prevent abuse

Environment:
  - TELEGRAM_BOT_TOKEN: Telegram bot token
  - MASTER_API_KEY: The master key to create new user keys
"""

import os
import json
import requests
import logging
from pathlib import Path
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 Welcome to DigenAI Bot!\n\n"
        "🎬 Generate AI videos with simple prompts\n\n"
        "📌 Commands:\n"
        "  /key - Get your free API key (via DM)\n"
        "  /mykey - View your current key\n"
        "  /info - Learn how to use the API\n"
        "  /help - Show help message\n\n"
        "⚠️ Each user gets ONE API key max.\n"
        "Get started: /key"
    )

async def key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /key command - generate and return API key via DM"""
    user = update.effective_user
    user_id = str(user.id)
    user_name = user.first_name
    
    # Load existing user keys
    user_keys = load_user_keys()
    
    # Check if user already has a key
    if user_id in user_keys:
        existing_key = user_keys[user_id]["api_key"]
        # Send existing key via DM
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=f"ℹ️ You already have an API key!\n\n"
                     f"```\n{existing_key}\n```\n\n"
                     f"📝 Note: Each user is limited to one API key.\n"
                     f"Keep it safe!",
                parse_mode="Markdown"
            )
            await update.message.reply_text(
                "✅ You already have an API key! Check your DM for it."
            )
            return
        except Exception as e:
            logger.error(f"Failed to send DM: {e}")
            await update.message.reply_text(
                "❌ Could not send DM. Please try again or check your privacy settings."
            )
            return
    
    # Send "generating" message
    msg = await update.message.reply_text("⏳ Generating your API key...")
    
    # Create new API key
    api_key = create_api_key()
    
    if api_key:
        # Save user key mapping
        user_keys[user_id] = {
            "api_key": api_key,
            "telegram_name": user_name,
            "created_at": datetime.utcnow().isoformat()
        }
        save_user_keys(user_keys)
        
        # Send key via DM
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=f"✅ API Key Generated!\n\n"
                     f"```\n{api_key}\n```\n\n"
                     f"📖 How to use:\n"
                     f"1. Set: `export DIGEN_API_KEY=\"{api_key}\"`\n"
                     f"2. Install: `clawhub install digen-ai-free`\n\n"
                     f"🔗 API Docs: https://api.cowork.digen.ai/b/doc\n\n"
                     f"⚠️ Keep your API key safe!",
                parse_mode="Markdown"
            )
            await msg.edit_text(
                "✅ API key sent to your DM! Check your private messages."
            )
        except Exception as e:
            logger.error(f"Failed to send DM: {e}")
            # If DM fails, send in chat but warn
            await msg.edit_text(
                f"⚠️ Could not send DM. Here's your key:\n\n"
                f"```\n{api_key}\n```\n\n"
                f"⚠️ Warning: For privacy, consider enabling DM and using /key again.",
                parse_mode="Markdown"
            )
    else:
        await msg.edit_text(
            "❌ Failed to generate API key. Please try again later."
        )

async def mykey_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mykey command - show user's current key"""
    user = update.effective_user
    user_id = str(user.id)
    
    user_keys = load_user_keys()
    
    if user_id in user_keys:
        api_key = user_keys[user_id]["api_key"]
        created_at = user_keys[user_id].get("created_at", "N/A")
        
        await context.bot.send_message(
            chat_id=user.id,
            text=f"🔑 Your API Key\n\n"
                 f"```\n{api_key}\n```\n\n"
                 f"Created: {created_at[:19]}",
            parse_mode="Markdown"
        )
        await update.message.reply_text("📬 Check your DM for your API key!")
    else:
        await update.message.reply_text("❌ You don't have an API key yet. Use /key to get one!")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /info command"""
    await update.message.reply_text(
        "📖 DigenAI API Info\n\n"
        "🔗 Base URL: `https://api.cowork.digen.ai`\n\n"
        "📡 Endpoints:\n"
        "  • GET  /b/v1/api-key - Check key info\n"
        "  • POST /b/v1/video/generate - Generate video\n"
        "  • GET  /b/v1/video/{id} - Check status\n\n"
        "💡 Example (curl):\n"
        "```bash\n"
        "curl -X POST https://api.cowork.digen.ai/b/v1/video/generate \\\n"
        "  -H 'Authorization: Bearer YOUR_KEY' \\\n"
        "  -H 'Content-Type: application/json' \\\n"
        "  -d '{\"prompt\": \"A cat\", \"duration\": 5}'\n"
        "```",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user_keys = load_user_keys()
    user_id = str(update.effective_user.id)
    has_key = user_id in user_keys
    
    status = "✅ You have a key" if has_key else "❌ No key yet"
    
    await update.message.reply_text(
        f"❓ Help\n\n"
        f"📊 Status: {status}\n\n"
        f"1. Get API key: Send /key (one per user)\n"
        f"2. View your key: Send /mykey\n"
        f"3. Install skill: `clawhub install digen-ai-free`\n"
        f"4. Set key: `export DIGEN_API_KEY=\"your_key\"`\n"
        f"5. Generate video using Python client\n\n"
        f"📖 Documentation: https://api.cowork.digen.ai/b/doc"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown messages"""
    await update.message.reply_text(
        "Unknown command. Try /key to get your API key!"
    )

def main():
    """Start the bot"""
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        print("Please set TELEGRAM_BOT_TOKEN environment variable")
        return
    
    # Create application
    app = Application.builder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("key", key_command))
    app.add_handler(CommandHandler("mykey", mykey_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Start polling
    print("🤖 DigenAI Telegram Bot started!")
    print(f"Master API Key: {MASTER_API_KEY[:20]}...")
    print(f"User keys file: {KEYS_FILE}")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()