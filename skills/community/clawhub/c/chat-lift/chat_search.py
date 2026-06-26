#!/usr/bin/env python3
"""
ChatLift — Conversation Search
Full-text search across archived conversations.

Author: Shadow Rose
License: MIT
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ConversationSearcher:
    """Search engine for archived conversations."""
    
    def __init__(self, archive_dir: str = 'chat-archive'):
        """
        Initialize searcher.
        
        Args:
            archive_dir: Directory containing archived conversations
        """
        self.archive_dir = Path(archive_dir)
        self.json_dir = self.archive_dir / 'json'
        
        self.conversations = []
        self._load_conversations()
    
    def _load_conversations(self):
        """Load all conversations from JSON archive."""
        if not self.json_dir.exists():
            print(f"Warning: Archive directory not found: {self.json_dir}")
            return
        
        for json_file in self.json_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    conv = json.load(f)
                    self.conversations.append(conv)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        print(f"Loaded {len(self.conversations)} conversation(s)")
    
    def search(
        self,
        query: str,
        case_sensitive: bool = False,
        regex: bool = False,
        source_filter: Optional[str] = None,
        role_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Search conversations for query.
        
        Args:
            query: Search query string
            case_sensitive: If True, search is case-sensitive
            regex: If True, treat query as regex pattern
            source_filter: Filter by source (chatgpt, claude, gemini)
            role_filter: Filter by message role (user, assistant, system)
            
        Returns:
            List of search result dictionaries
        """
        results = []
        
        # Compile regex if needed
        if regex:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern = re.compile(query, flags)
            except re.error as e:
                print(f"Invalid regex pattern: {e}")
                return []
        else:
            # Simple string search
            search_query = query if case_sensitive else query.lower()
        
        for conv in self.conversations:
            # Apply source filter
            if source_filter and conv.get('source') != source_filter:
                continue
            
            # Search in title
            title = conv.get('title', '')
            title_match = False
            
            if regex:
                title_match = bool(pattern.search(title))
            else:
                search_title = title if case_sensitive else title.lower()
                title_match = search_query in search_title
            
            # Search in messages
            message_matches = []
            
            for idx, msg in enumerate(conv.get('messages', [])):
                # Apply role filter
                if role_filter and msg.get('role') != role_filter:
                    continue
                
                content = msg.get('content', '')
                
                if regex:
                    matches = list(pattern.finditer(content))
                    if matches:
                        for match in matches:
                            message_matches.append({
                                'message_index': idx,
                                'role': msg.get('role'),
                                'match': match.group(),
                                'start': match.start(),
                                'end': match.end(),
                                'context': self._get_context(content, match.start(), match.end()),
                            })
                else:
                    search_content = content if case_sensitive else content.lower()
                    if search_query in search_content:
                        # Find all occurrences
                        start = 0
                        while True:
                            pos = search_content.find(search_query, start)
                            if pos == -1:
                                break
                            
                            message_matches.append({
                                'message_index': idx,
                                'role': msg.get('role'),
                                'match': content[pos:pos + len(query)],
                                'start': pos,
                                'end': pos + len(query),
                                'context': self._get_context(content, pos, pos + len(query)),
                            })
                            
                            start = pos + 1
            
            # Add to results if title matched or messages matched
            if title_match or message_matches:
                results.append({
                    'conversation': conv,
                    'title_match': title_match,
                    'message_matches': message_matches,
                    'total_matches': len(message_matches) + (1 if title_match else 0),
                })
        
        # Sort by relevance (total matches)
        results.sort(key=lambda x: x['total_matches'], reverse=True)
        
        return results
    
    def _get_context(self, text: str, start: int, end: int, context_chars: int = 80) -> str:
        """
        Get context around match.
        
        Args:
            text: Full text
            start: Match start position
            end: Match end position
            context_chars: Characters of context on each side
            
        Returns:
            Context string
        """
        # Find context boundaries
        context_start = max(0, start - context_chars)
        context_end = min(len(text), end + context_chars)
        
        # Get context
        before = text[context_start:start]
        match = text[start:end]
        after = text[end:context_end]
        
        # Add ellipsis if truncated
        if context_start > 0:
            before = '...' + before
        if context_end < len(text):
            after = after + '...'
        
        return f"{before}**{match}**{after}"
    
    def search_by_date(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Search conversations by date range.
        
        Args:
            start_date: Start date (ISO format or timestamp)
            end_date: End date (ISO format or timestamp)
            
        Returns:
            List of conversations in date range
        """
        from datetime import datetime
        
        results = []
        
        # Parse dates
        start_ts = self._parse_date(start_date) if start_date else None
        end_ts = self._parse_date(end_date) if end_date else None
        
        for conv in self.conversations:
            create_time = conv.get('create_time')
            if not create_time:
                continue
            
            if isinstance(create_time, str):
                conv_ts = self._parse_date(create_time)
            else:
                conv_ts = create_time
            
            # Check date range
            if start_ts and conv_ts < start_ts:
                continue
            if end_ts and conv_ts > end_ts:
                continue
            
            results.append(conv)
        
        # Sort by date
        results.sort(key=lambda x: x.get('create_time', 0), reverse=True)
        
        return results
    
    def _parse_date(self, date_str: str) -> float:
        """Parse date string to timestamp."""
        from datetime import datetime
        
        # Try timestamp first
        try:
            return float(date_str)
        except:
            pass
        
        # Try ISO format
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.timestamp()
        except:
            pass
        
        # Try common formats
        formats = [
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.timestamp()
            except:
                continue
        
        raise ValueError(f"Could not parse date: {date_str}")
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about archived conversations.
        
        Returns:
            Statistics dictionary
        """
        from collections import Counter
        
        total_conversations = len(self.conversations)
        total_messages = sum(len(conv.get('messages', [])) for conv in self.conversations)
        
        sources = Counter(conv.get('source') for conv in self.conversations)
        
        # Message role distribution
        roles = Counter()
        for conv in self.conversations:
            for msg in conv.get('messages', []):
                roles[msg.get('role', 'unknown')] += 1
        
        # Total word count (approximate)
        total_words = 0
        for conv in self.conversations:
            for msg in conv.get('messages', []):
                content = msg.get('content', '')
                total_words += len(content.split())
        
        return {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'total_words': total_words,
            'sources': dict(sources),
            'roles': dict(roles),
            'average_messages_per_conversation': total_messages / total_conversations if total_conversations else 0,
        }


def main():
    """CLI for conversation search."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ChatLift Conversation Search')
    parser.add_argument('action', choices=['search', 'date', 'stats'],
                       help='Action to perform')
    parser.add_argument('--archive-dir', default='chat-archive', help='Archive directory')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--regex', action='store_true', help='Use regex search')
    parser.add_argument('--case-sensitive', action='store_true', help='Case-sensitive search')
    parser.add_argument('--source', choices=['chatgpt', 'claude', 'gemini'], help='Filter by source')
    parser.add_argument('--role', help='Filter by message role')
    parser.add_argument('--start-date', help='Start date for date search')
    parser.add_argument('--end-date', help='End date for date search')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    
    args = parser.parse_args()
    
    searcher = ConversationSearcher(args.archive_dir)
    
    if args.action == 'search':
        if not args.query:
            print("Error: --query required for search")
            return
        
        print(f"\nSearching for: {args.query}")
        print("-" * 70)
        
        results = searcher.search(
            args.query,
            case_sensitive=args.case_sensitive,
            regex=args.regex,
            source_filter=args.source,
            role_filter=args.role
        )
        
        if not results:
            print("No matches found.")
            return
        
        print(f"Found {len(results)} conversation(s) with matches\n")
        
        for i, result in enumerate(results[:args.limit] if args.limit else results, 1):
            conv = result['conversation']
            print(f"[{i}] {conv['title']}")
            print(f"    Source: {conv.get('source', 'unknown')}")
            print(f"    Matches: {result['total_matches']}")
            
            if result['title_match']:
                print(f"    ✓ Title match")
            
            if result['message_matches']:
                print(f"    Message matches:")
                for match in result['message_matches'][:3]:  # Show first 3
                    print(f"      - {match['role']}: {match['context']}")
                
                if len(result['message_matches']) > 3:
                    print(f"      ... and {len(result['message_matches']) - 3} more")
            
            print()
    
    elif args.action == 'date':
        print(f"\nSearching by date range:")
        if args.start_date:
            print(f"  Start: {args.start_date}")
        if args.end_date:
            print(f"  End: {args.end_date}")
        print("-" * 70)
        
        results = searcher.search_by_date(args.start_date, args.end_date)
        
        if not results:
            print("No conversations found in date range.")
            return
        
        print(f"Found {len(results)} conversation(s)\n")
        
        for i, conv in enumerate(results[:args.limit] if args.limit else results, 1):
            from datetime import datetime
            create_time = conv.get('create_time', 'unknown')
            if isinstance(create_time, (int, float)):
                create_time = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"[{i}] {conv['title']}")
            print(f"    Created: {create_time}")
            print(f"    Source: {conv.get('source', 'unknown')}")
            print()
    
    elif args.action == 'stats':
        stats = searcher.get_statistics()
        
        print("\nArchive Statistics")
        print("=" * 70)
        print(f"Total Conversations: {stats['total_conversations']}")
        print(f"Total Messages:      {stats['total_messages']}")
        print(f"Total Words:         {stats['total_words']:,}")
        print(f"Avg Messages/Conv:   {stats['average_messages_per_conversation']:.1f}")
        
        print("\nSources:")
        for source, count in stats['sources'].items():
            print(f"  {source:15} {count}")
        
        print("\nMessage Roles:")
        for role, count in stats['roles'].items():
            print(f"  {role:15} {count}")
        print()


if __name__ == '__main__':
    main()
