#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emoji Wrapper Skill
- Bridges OpenClaw messages to local-auto-emoji
- Processes [标记] and sends emoji images
"""

import sys
import os
from pathlib import Path

# Add local-auto-emoji to path (relative to this file)
_current_file = Path(__file__).resolve()
_workspace_root = _current_file.parent.parent.parent  # ~/.openclaw/workspace
LOCAL_EMOJI_PATH = _workspace_root / "skills" / "local-auto-emoji" / "scripts"
if LOCAL_EMOJI_PATH.exists():
    sys.path.insert(0, str(LOCAL_EMOJI_PATH))
else:
    # Fallback: try relative
    alt_path = _current_file.parent.parent / "local-auto-emoji" / "scripts"
    if alt_path.exists():
        sys.path.insert(0, str(alt_path))

try:
    from send_emoji import LocalAutoEmoji
except ImportError as e:
    print(f"[EmojiWrapper] Failed to import LocalAutoEmoji: {e}")
    print(f"[EmojiWrapper] Tried: {LOCAL_EMOJI_PATH}")
    print(f"[EmojiWrapper] Make sure local-auto-emoji skill is installed")
    # Don't raise - let skill load anyway and fail gracefully
    LocalAutoEmoji = None


class EmojiWrapper:
    """
    OpenClaw Skill Wrapper for local-auto-emoji

    This skill intercepts messages containing [emoji markers] and expands them
    into text + emoji image messages.
    """

    def __init__(self):
        """Initialize the wrapper and emoji bot"""
        self.bot = None
        self._initialized = False

        # Try to initialize LocalAutoEmoji
        if LocalAutoEmoji is not None:
            try:
                self.bot = LocalAutoEmoji()
                self._initialized = True
                print("[EmojiWrapper] Initialized successfully")
            except Exception as e:
                print(f"[EmojiWrapper] Failed to initialize bot: {e}")
                self.bot = None

    def _ensure_user(self, userid: str):
        """Ensure user exists in emoji system"""
        if not self.bot:
            return False
        try:
            if userid not in self.bot.manager.index["users"]:
                self.bot.ensure_user(userid)
            self.bot.userid = userid
            return True
        except Exception as e:
            print(f"[EmojiWrapper] _ensure_user error: {e}")
            return False

    def _extract_user_message(self, message) -> str:
        """Extract text from message object"""
        if hasattr(message, 'content'):
            return message.content
        elif hasattr(message, 'text'):
            return message.text
        else:
            return str(message)

    def _extract_userid(self, session) -> str:
        """Extract userid from session object"""
        if not session:
            return "default_user"

        # Try different session structures
        if hasattr(session, 'user') and hasattr(session.user, 'id'):
            return session.user.id
        elif hasattr(session, 'userid'):
            return session.userid
        elif hasattr(session, 'user') and isinstance(session.user, dict):
            return session.user.get('id', 'default_user')
        elif hasattr(session, 'channel'):
            # Fallback to channel label
            channel = session.channel
            if hasattr(channel, 'label'):
                return f"channel_{channel.label}"
            elif isinstance(channel, dict):
                return f"channel_{channel.get('label', 'unknown')}"

        return "default_user"

    def process_message(self, message, session=None, context=None, callback=None):
        """
        OpenClaw skill entry point

        Args:
            message: The incoming message object
            session: Session object (contains user info)
            context: Additional context
            callback: Function to send response

        Returns:
            None (let OpenClaw continue) or list of messages
        """
        if not self._initialized or not self.bot:
            print("[EmojiWrapper] Bot not initialized, skipping")
            return None

        try:
            # Extract user message
            user_message = self._extract_user_message(message)

            # Extract userid
            userid = self._extract_userid(session)

            # Ensure user exists
            if not self._ensure_user(userid):
                return None

            # Process emoji markers
            messages = self.bot.replace_emoji_markers(user_message)

            # Send via callback or return
            if callback and callable(callback):
                for msg in messages:
                    callback(msg)
                return None
            else:
                return messages

        except Exception as e:
            import traceback
            error_msg = f"[EmojiWrapper] Error: {e}\n{traceback.format_exc()}"
            print(error_msg, file=sys.stderr)
            return None


# For direct testing
if __name__ == "__main__":
    wrapper = EmojiWrapper()

    # Test message
    test_msg = type('Message', (), {'content': '凯哥真厉害！[可爱][眨眼] 要抱抱[抱抱]！'})
    wrapper._ensure_user("test_user_123")

    result = wrapper.process_message(test_msg)
    print("Test result:")
    for msg in result:
        print(f"  {msg}")
