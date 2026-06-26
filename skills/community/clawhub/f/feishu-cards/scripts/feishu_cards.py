#!/usr/bin/env python3
"""
Feishu Cards - Send interactive cards to Feishu

This module provides functionality to send rich interactive cards to Feishu,
including buttons, images, and other interactive elements.

Author: OpenClaw Community
Version: 1.0.0
"""

import json
import argparse
import os
import sys
from typing import Optional, List, Dict, Any


class CardBuilder:
    """Build Feishu interactive cards with various elements."""
    
    def __init__(self):
        self.elements: List[Dict[str, Any]] = []
        self.title: Optional[str] = None
        self.header: Optional[Dict[str, Any]] = None
    
    def set_title(self, title: str, color: str = "blue") -> 'CardBuilder':
        """Set the card title with optional color.
        
        Args:
            title: Title text
            color: Header color (blue, green, red, yellow, grey)
        
        Returns:
            CardBuilder for chaining
        """
        self.header = {
            "tag": "header",
            "title": {
                "tag": "plain_text",
                "content": title
            },
            "template": color
        }
        return self
    
    def set_content(self, content: str) -> 'CardBuilder':
        """Set the main content of the card.
        
        Args:
            content: Main text content
        
        Returns:
            CardBuilder for chaining
        """
        self.elements.append({
            "tag": "div",
            "text": {
                "tag": "markdown",
                "content": content
            }
        })
        return self
    
    def add_button(
        self, 
        button_type: str, 
        text: str, 
        value: str,
        url: Optional[str] = None
    ) -> 'CardBuilder':
        """Add a button to the card.
        
        Args:
            button_type: Type of button (primary, default, danger)
            text: Button label text
            value: Button value/ID for callback
            url: Optional URL to open when clicked
        
        Returns:
            CardBuilder for chaining
        """
        button: Dict[str, Any] = {
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": text
            },
            "type": button_type,
            "value": {"action": value}
        }
        
        if url:
            button["url"] = url
        else:
            button["type"] = "interactive"
        
        self.elements.append({
            "tag": "action",
            "actions": [button]
        })
        return self
    
    def add_image(self, url: str, alt: str = "") -> 'CardBuilder':
        """Add an image to the card.
        
        Args:
            url: Image URL
            alt: Alternative text for image
        
        Returns:
            CardBuilder for chaining
        """
        self.elements.append({
            "tag": "img",
            "img_key": url,
            "alt": {
                "tag": "plain_text",
                "content": alt
            }
        })
        return self
    
    def add_div(self) -> 'CardBuilder':
        """Add a horizontal divider.
        
        Returns:
            CardBuilder for chaining
        """
        self.elements.append({"tag": "div"})
        return self
    
    def add_note(self, icon: str, text: str) -> 'CardBuilder':
        """Add a note with icon.
        
        Args:
            icon: Icon emoji (ℹ️, ⚠️, ✅, ❌, etc.)
            text: Note text content
        
        Returns:
            CardBuilder for chaining
        """
        self.elements.append({
            "tag": "note",
            "elements": [
                {
                    "tag": "plain_text",
                    "content": icon
                },
                {
                    "tag": "plain_text",
                    "content": text
                }
            ]
        })
        return self
    
    def add_options(
        self, 
        options: List[str], 
        placeholder: str = "请选择"
    ) -> 'CardBuilder':
        """Add a dropdown selector.
        
        Args:
            options: List of option values
            placeholder: Placeholder text
        
        Returns:
            CardBuilder for chaining
        """
        option_list = [
            {
                "text": {"tag": "plain_text", "content": opt},
                "value": opt
            }
            for opt in options
        ]
        
        self.elements.append({
            "tag": "select_static",
            "placeholder": {
                "tag": "plain_text",
                "content": placeholder
            },
            "options": option_list
        })
        return self
    
    def build(self) -> str:
        """Build the final card JSON.
        
        Returns:
            JSON string of the card
        """
        card: Dict[str, Any] = {"config": {"wide_screen_mode": True}}
        
        if self.header:
            card["header"] = self.header
        
        if self.elements:
            card["elements"] = self.elements
        
        # Wrap in card structure for Feishu
        return json.dumps({"card": card}, ensure_ascii=False)
    
    def print_json(self):
        """Print the card JSON for debugging."""
        print(self.build())


def send_card_via_message(
    card_json: str,
    to: str,
    message_type: str = "interactive"
) -> Dict[str, Any]:
    """Send card using OpenClaw message system.
    
    This is a placeholder - actual implementation would use
    the OpenClaw message API to send the card.
    
    Args:
        card_json: JSON string of the card
        to: Recipient (user:ou_xxx or chat:xxx)
        message_type: Type of message
    
    Returns:
        Result dictionary
    """
    # For now, just print the card
    print("Card JSON:")
    print(card_json)
    print(f"\nTo: {to}")
    print("\nNote: Use OpenClaw message tool with card content to send.")
    
    return {"status": "ready", "card": card_json}


def quick_card(
    title: str,
    content: str,
    options: List[str],
    to: Optional[str] = None
) -> str:
    """Create a quick card with options.
    
    Args:
        title: Card title
        content: Card content text
        options: List of option strings
        to: Recipient (optional)
    
    Returns:
        Card JSON string
    """
    builder = CardBuilder().set_title(title)
    
    if content:
        builder.set_content(content)
    
    if options:
        builder.add_options(options)
    
    return builder.build()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Feishu Cards - Send interactive cards to Feishu"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build a card")
    build_parser.add_argument("--title", required=True, help="Card title")
    build_parser.add_argument("--content", help="Card content")
    build_parser.add_argument("--buttons", help="Comma-separated buttons")
    build_parser.add_argument("--print", action="store_true", help="Print JSON")
    
    # Quick command
    quick_parser = subparsers.add_parser("quick", help="Quick card with options")
    quick_parser.add_argument("--title", required=True, help="Card title")
    quick_parser.add_argument("--content", help="Card content")
    quick_parser.add_argument("--options", required=True, help="Comma-separated options")
    quick_parser.add_argument("--to", help="Recipient")
    
    args = parser.parse_args()
    
    if args.command == "build":
        builder = CardBuilder().set_title(args.title)
        
        if args.content:
            builder.set_content(args.content)
        
        if args.buttons:
            buttons = args.buttons.split(",")
            for btn in buttons:
                builder.add_button("default", btn.strip(), btn.strip())
        
        if args.print:
            builder.print_json()
        else:
            print(builder.build())
    
    elif args.command == "quick":
        options = args.options.split(",")
        card_json = quick_card(args.title, args.content, options, args.to)
        print(card_json)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
