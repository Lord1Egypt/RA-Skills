#!/usr/bin/env python3
"""
ChatLift — AI Conversation Importer
Import and convert ChatGPT/Claude/Gemini exports to indexed formats.

Author: Shadow Rose
License: MIT
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import html


class ConversationImporter:
    """Import AI conversations from various export formats."""
    
    def __init__(self, output_dir: str = 'chat-archive'):
        """
        Initialize importer.
        
        Args:
            output_dir: Directory to store converted conversations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create format-specific subdirectories
        (self.output_dir / 'markdown').mkdir(exist_ok=True)
        (self.output_dir / 'html').mkdir(exist_ok=True)
        (self.output_dir / 'json').mkdir(exist_ok=True)
    
    def import_chatgpt(self, export_file: str) -> List[Dict]:
        """
        Import ChatGPT conversation export.
        
        ChatGPT exports are JSON with structure:
        [
          {
            "title": "Conversation title",
            "create_time": 1234567890,
            "mapping": { ... message nodes ... }
          },
          ...
        ]
        
        Args:
            export_file: Path to ChatGPT export JSON
            
        Returns:
            List of converted conversation dictionaries
        """
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = []
        
        for conv in data:
            messages = self._parse_chatgpt_messages(conv.get('mapping', {}))
            
            conversation = {
                'id': conv.get('id', self._generate_id(conv.get('title', 'Untitled'))),
                'title': conv.get('title', 'Untitled'),
                'create_time': conv.get('create_time'),
                'update_time': conv.get('update_time'),
                'source': 'chatgpt',
                'messages': messages,
            }
            
            conversations.append(conversation)
        
        return conversations
    
    def _parse_chatgpt_messages(self, mapping: Dict) -> List[Dict]:
        """Parse ChatGPT message mapping into flat list."""
        messages = []
        
        # Build message chain from mapping
        for node_id, node in mapping.items():
            message = node.get('message')
            if not message:
                continue
            
            author_role = message.get('author', {}).get('role', 'unknown')
            content_parts = message.get('content', {}).get('parts', [])
            
            # Join multi-part content
            content = '\n'.join(str(part) for part in content_parts if part)
            
            if content.strip():
                messages.append({
                    'role': author_role,
                    'content': content,
                    'timestamp': message.get('create_time'),
                })
        
        return messages
    
    def import_claude(self, export_file: str) -> List[Dict]:
        """
        Import Claude conversation export.
        
        Claude exports vary, but typically JSON with conversations array.
        
        Args:
            export_file: Path to Claude export JSON
            
        Returns:
            List of converted conversation dictionaries
        """
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = []
        
        # Handle different Claude export formats
        conv_list = data if isinstance(data, list) else data.get('conversations', [])
        
        for conv in conv_list:
            messages = []
            
            # Parse messages (format varies by Claude version)
            for msg in conv.get('messages', []):
                messages.append({
                    'role': msg.get('role', msg.get('sender', 'unknown')),
                    'content': msg.get('content', msg.get('text', '')),
                    'timestamp': msg.get('created_at', msg.get('timestamp')),
                })
            
            conversation = {
                'id': conv.get('id', conv.get('uuid', self._generate_id(conv.get('name', 'Untitled')))),
                'title': conv.get('name', conv.get('title', 'Untitled')),
                'create_time': conv.get('created_at', conv.get('timestamp')),
                'update_time': conv.get('updated_at'),
                'source': 'claude',
                'messages': messages,
            }
            
            conversations.append(conversation)
        
        return conversations
    
    def import_gemini(self, export_file: str) -> List[Dict]:
        """
        Import Google Gemini conversation export.
        
        Args:
            export_file: Path to Gemini export JSON
            
        Returns:
            List of converted conversation dictionaries
        """
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = []
        
        # Gemini export format
        for conv in (data if isinstance(data, list) else [data]):
            messages = []
            
            for msg in conv.get('messages', conv.get('history', [])):
                messages.append({
                    'role': msg.get('role', msg.get('author', 'unknown')),
                    'content': msg.get('parts', [msg.get('text', '')])[0] if 'parts' in msg else msg.get('text', ''),
                    'timestamp': msg.get('timestamp', msg.get('time')),
                })
            
            conversation = {
                'id': conv.get('id', self._generate_id(conv.get('title', 'Untitled'))),
                'title': conv.get('title', conv.get('name', 'Untitled')),
                'create_time': conv.get('create_time', conv.get('timestamp')),
                'update_time': conv.get('update_time'),
                'source': 'gemini',
                'messages': messages,
            }
            
            conversations.append(conversation)
        
        return conversations
    
    def _generate_id(self, title: str) -> str:
        """Generate conversation ID from title."""
        import hashlib
        return hashlib.md5(f"{title}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
    
    def convert_to_markdown(self, conversation: Dict) -> str:
        """
        Convert conversation to markdown format.
        
        Args:
            conversation: Conversation dictionary
            
        Returns:
            Markdown string
        """
        md = f"# {conversation['title']}\n\n"
        md += f"**Source:** {conversation['source']}  \n"
        md += f"**ID:** {conversation['id']}  \n"
        
        if conversation.get('create_time'):
            create_time = self._format_timestamp(conversation['create_time'])
            md += f"**Created:** {create_time}  \n"
        
        md += "\n---\n\n"
        
        for msg in conversation['messages']:
            role = msg['role'].upper()
            content = msg['content']
            
            md += f"## {role}\n\n"
            md += f"{content}\n\n"
            
            if msg.get('timestamp'):
                ts = self._format_timestamp(msg['timestamp'])
                md += f"*{ts}*\n\n"
            
            md += "---\n\n"
        
        return md
    
    def convert_to_json(self, conversation: Dict) -> str:
        """
        Convert conversation to clean JSON format.
        
        Args:
            conversation: Conversation dictionary
            
        Returns:
            JSON string
        """
        return json.dumps(conversation, indent=2, ensure_ascii=False)
    
    def convert_to_html(self, conversation: Dict) -> str:
        """
        Convert conversation to HTML format.
        
        Args:
            conversation: Conversation dictionary
            
        Returns:
            HTML string
        """
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '  <meta charset="UTF-8">',
            f'  <title>{html.escape(conversation["title"])}</title>',
            '  <style>',
            '    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }',
            '    .header { border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }',
            '    .message { margin-bottom: 30px; padding: 15px; border-radius: 8px; }',
            '    .user { background: #e3f2fd; }',
            '    .assistant { background: #f5f5f5; }',
            '    .system { background: #fff3e0; }',
            '    .role { font-weight: bold; margin-bottom: 10px; color: #333; }',
            '    .content { white-space: pre-wrap; line-height: 1.6; }',
            '    .timestamp { font-size: 0.85em; color: #666; margin-top: 10px; }',
            '    .metadata { color: #666; font-size: 0.9em; }',
            '  </style>',
            '</head>',
            '<body>',
            '  <div class="header">',
            f'    <h1>{html.escape(conversation["title"])}</h1>',
            f'    <div class="metadata">',
            f'      <div>Source: {conversation["source"]}</div>',
            f'      <div>ID: {conversation["id"]}</div>',
        ]
        
        if conversation.get('create_time'):
            create_time = self._format_timestamp(conversation['create_time'])
            html_parts.append(f'      <div>Created: {create_time}</div>')
        
        html_parts.extend([
            '    </div>',
            '  </div>',
        ])
        
        for msg in conversation['messages']:
            role = msg['role'].lower()
            role_class = role if role in ['user', 'assistant', 'system'] else 'assistant'
            
            html_parts.append(f'  <div class="message {role_class}">')
            html_parts.append(f'    <div class="role">{html.escape(msg["role"].upper())}</div>')
            html_parts.append(f'    <div class="content">{html.escape(msg["content"])}</div>')
            
            if msg.get('timestamp'):
                ts = self._format_timestamp(msg['timestamp'])
                html_parts.append(f'    <div class="timestamp">{ts}</div>')
            
            html_parts.append('  </div>')
        
        html_parts.extend([
            '</body>',
            '</html>',
        ])
        
        return '\n'.join(html_parts)
    
    def _format_timestamp(self, timestamp) -> str:
        """Format timestamp to readable string."""
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp)
        elif isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return timestamp
        else:
            return str(timestamp)
        
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def save_conversation(self, conversation: Dict, formats: List[str] = ['markdown', 'html', 'json']):
        """
        Save conversation in specified formats.
        
        Args:
            conversation: Conversation dictionary
            formats: List of formats to save ('markdown', 'html', 'json')
        """
        safe_id = re.sub(r'[^a-z0-9-]', '-', conversation['id'].lower())
        
        if 'markdown' in formats:
            md_content = self.convert_to_markdown(conversation)
            md_path = self.output_dir / 'markdown' / f'{safe_id}.md'
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"  ✓ Markdown: {md_path}")
        
        if 'html' in formats:
            html_content = self.convert_to_html(conversation)
            html_path = self.output_dir / 'html' / f'{safe_id}.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"  ✓ HTML: {html_path}")
        
        if 'json' in formats:
            json_content = self.convert_to_json(conversation)
            json_path = self.output_dir / 'json' / f'{safe_id}.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json_content)
            print(f"  ✓ JSON: {json_path}")


def main():
    """CLI for conversation import."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ChatLift Conversation Importer')
    parser.add_argument('source', choices=['chatgpt', 'claude', 'gemini'],
                       help='Source platform')
    parser.add_argument('export_file', help='Export file path')
    parser.add_argument('--output-dir', default='chat-archive', help='Output directory')
    parser.add_argument('--formats', nargs='+', default=['markdown', 'html', 'json'],
                       choices=['markdown', 'html', 'json'], help='Output formats')
    
    args = parser.parse_args()
    
    importer = ConversationImporter(args.output_dir)
    
    print(f"\nImporting {args.source} conversations from {args.export_file}...")
    
    # Import based on source
    if args.source == 'chatgpt':
        conversations = importer.import_chatgpt(args.export_file)
    elif args.source == 'claude':
        conversations = importer.import_claude(args.export_file)
    elif args.source == 'gemini':
        conversations = importer.import_gemini(args.export_file)
    
    print(f"Found {len(conversations)} conversation(s)\n")
    
    # Save all conversations
    for i, conv in enumerate(conversations, 1):
        print(f"[{i}/{len(conversations)}] {conv['title']}")
        importer.save_conversation(conv, formats=args.formats)
        print()
    
    print(f"✅ Import complete! Files saved to {args.output_dir}/")


if __name__ == '__main__':
    main()
