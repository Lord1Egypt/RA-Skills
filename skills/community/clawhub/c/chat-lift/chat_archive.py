#!/usr/bin/env python3
"""
ChatLift — HTML Archive Generator
Generate static HTML archive with search and navigation.

Author: Shadow Rose
License: MIT
"""

import json
import html
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ArchiveGenerator:
    """Generate static HTML archive of conversations."""
    
    def __init__(self, archive_dir: str = 'chat-archive'):
        """
        Initialize archive generator.
        
        Args:
            archive_dir: Directory containing archived conversations
        """
        self.archive_dir = Path(archive_dir)
        self.json_dir = self.archive_dir / 'json'
        self.output_dir = self.archive_dir / 'web'
        
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
        
        # Sort by date (newest first)
        self.conversations.sort(
            key=lambda x: x.get('create_time', 0),
            reverse=True
        )
        
        print(f"Loaded {len(self.conversations)} conversation(s)")
    
    def generate_archive(self):
        """Generate complete HTML archive."""
        self.output_dir.mkdir(exist_ok=True)
        
        # Generate index page
        self._generate_index()
        
        # Generate individual conversation pages
        for conv in self.conversations:
            self._generate_conversation_page(conv)
        
        # Generate CSS file
        self._generate_css()
        
        # Generate JavaScript file
        self._generate_js()
        
        print(f"\n✅ Archive generated: {self.output_dir}/index.html")
        print(f"   Open in browser to view")
    
    def _generate_index(self):
        """Generate index page with search and navigation."""
        # Build conversation list JSON for search
        conv_list = []
        for conv in self.conversations:
            conv_list.append({
                'id': conv['id'],
                'title': conv['title'],
                'source': conv.get('source', 'unknown'),
                'create_time': conv.get('create_time'),
                'message_count': len(conv.get('messages', [])),
            })
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Chat Archive</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <header>
      <h1>💬 Chat Archive</h1>
      <p class="subtitle">{len(self.conversations)} conversations archived</p>
    </header>
    
    <div class="search-bar">
      <input type="text" id="searchInput" placeholder="Search conversations..." autocomplete="off">
      <select id="sourceFilter">
        <option value="">All Sources</option>
        <option value="chatgpt">ChatGPT</option>
        <option value="claude">Claude</option>
        <option value="gemini">Gemini</option>
      </select>
    </div>
    
    <div id="conversationList" class="conversation-list">
"""
        
        # Add conversation cards
        for conv in self.conversations:
            create_time = self._format_timestamp(conv.get('create_time', ''))
            message_count = len(conv.get('messages', []))
            
            html_content += f"""
      <div class="conversation-card" data-source="{conv.get('source', 'unknown')}" data-title="{html.escape(conv['title']).lower()}">
        <a href="{conv['id']}.html">
          <h3>{html.escape(conv['title'])}</h3>
          <div class="card-meta">
            <span class="source source-{conv.get('source', 'unknown')}">{conv.get('source', 'unknown')}</span>
            <span class="date">{create_time}</span>
            <span class="count">{message_count} messages</span>
          </div>
        </a>
      </div>
"""
        
        html_content += """
    </div>
    
    <div id="noResults" class="no-results" style="display: none;">
      No conversations found matching your search.
    </div>
  </div>
  
  <script src="search.js"></script>
</body>
</html>
"""
        
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_conversation_page(self, conv: Dict):
        """Generate individual conversation page."""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{html.escape(conv['title'])}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <nav class="breadcrumb">
      <a href="index.html">← Back to Archive</a>
    </nav>
    
    <header class="conversation-header">
      <h1>{html.escape(conv['title'])}</h1>
      <div class="metadata">
        <span class="source source-{conv.get('source', 'unknown')}">{conv.get('source', 'unknown')}</span>
        <span class="date">{self._format_timestamp(conv.get('create_time', ''))}</span>
        <span class="count">{len(conv.get('messages', []))} messages</span>
      </div>
    </header>
    
    <div class="messages">
"""
        
        # Add messages
        for idx, msg in enumerate(conv.get('messages', [])):
            role = msg.get('role', 'unknown').lower()
            role_class = role if role in ['user', 'assistant', 'system'] else 'assistant'
            timestamp = self._format_timestamp(msg.get('timestamp', ''))
            
            content_html = self._format_content(msg.get('content', ''))
            
            html_content += f"""
      <div class="message message-{role_class}" id="msg-{idx}">
        <div class="message-header">
          <span class="role">{html.escape(msg.get('role', 'unknown').upper())}</span>
          <span class="timestamp">{timestamp}</span>
        </div>
        <div class="message-content">
          {content_html}
        </div>
      </div>
"""
        
        html_content += """
    </div>
  </div>
</body>
</html>
"""
        
        safe_id = conv['id']
        with open(self.output_dir / f'{safe_id}.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _format_content(self, content: str) -> str:
        """Format message content with basic markdown support."""
        # Escape HTML first
        content = html.escape(content)
        
        # Convert markdown-style code blocks
        content = self._convert_code_blocks(content)
        
        # Convert inline code
        content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
        
        # Convert bold
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        
        # Convert line breaks
        content = content.replace('\n', '<br>')
        
        return content
    
    def _convert_code_blocks(self, content: str) -> str:
        """Convert markdown code blocks to HTML."""
        import re
        
        # Match ```language\ncode\n```
        pattern = r'```(\w+)?\n(.*?)\n```'
        
        def replace_code_block(match):
            lang = match.group(1) or 'text'
            code = match.group(2)
            return f'<pre><code class="language-{lang}">{code}</code></pre>'
        
        return re.sub(pattern, replace_code_block, content, flags=re.DOTALL)
    
    def _format_timestamp(self, timestamp) -> str:
        """Format timestamp to readable string."""
        if not timestamp:
            return ''
        
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp)
        elif isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return timestamp
        else:
            return str(timestamp)
        
        return dt.strftime('%Y-%m-%d %H:%M')
    
    def _generate_css(self):
        """Generate CSS stylesheet."""
        css = """/* ChatLift Archive Styles */

:root {
  --primary-color: #2563eb;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --text-color: #1e293b;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
  --user-bg: #dbeafe;
  --assistant-bg: #f1f5f9;
  --system-bg: #fef3c7;
  --code-bg: #f1f5f9;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg-color);
  color: var(--text-color);
  line-height: 1.6;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  padding: 40px 0 20px;
  border-bottom: 2px solid var(--border-color);
  margin-bottom: 30px;
}

header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.subtitle {
  color: var(--text-muted);
  font-size: 1.1em;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

#searchInput {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 1em;
}

#searchInput:focus {
  outline: none;
  border-color: var(--primary-color);
}

#sourceFilter {
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 1em;
  background: var(--card-bg);
}

.conversation-list {
  display: grid;
  gap: 16px;
}

.conversation-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.conversation-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.conversation-card a {
  display: block;
  padding: 20px;
  text-decoration: none;
  color: inherit;
}

.conversation-card h3 {
  margin-bottom: 10px;
  color: var(--text-color);
}

.card-meta {
  display: flex;
  gap: 16px;
  font-size: 0.9em;
  color: var(--text-muted);
}

.source {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: 600;
  text-transform: uppercase;
}

.source-chatgpt { background: #10a37f; color: white; }
.source-claude { background: #cc9b7a; color: white; }
.source-gemini { background: #4285f4; color: white; }
.source-unknown { background: var(--text-muted); color: white; }

.breadcrumb {
  margin-bottom: 20px;
}

.breadcrumb a {
  color: var(--primary-color);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.conversation-header {
  padding-bottom: 20px;
  border-bottom: 2px solid var(--border-color);
  margin-bottom: 30px;
}

.conversation-header h1 {
  margin-bottom: 10px;
}

.metadata {
  display: flex;
  gap: 16px;
  font-size: 0.95em;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid;
}

.message-user {
  background: var(--user-bg);
  border-left-color: #3b82f6;
}

.message-assistant {
  background: var(--assistant-bg);
  border-left-color: #64748b;
}

.message-system {
  background: var(--system-bg);
  border-left-color: #f59e0b;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9em;
}

.role {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.timestamp {
  color: var(--text-muted);
}

.message-content {
  line-height: 1.7;
}

.message-content code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.message-content pre {
  background: var(--code-bg);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 10px 0;
}

.message-content pre code {
  background: none;
  padding: 0;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
  font-size: 1.1em;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  header {
    padding: 20px 0 10px;
  }
  
  header h1 {
    font-size: 2em;
  }
  
  .search-bar {
    flex-direction: column;
  }
  
  .card-meta {
    flex-direction: column;
    gap: 4px;
  }
}
"""
        with open(self.output_dir / 'style.css', 'w', encoding='utf-8') as f:
            f.write(css)
    
    def _generate_js(self):
        """Generate JavaScript for search functionality."""
        js = """// ChatLift Archive Search

const searchInput = document.getElementById('searchInput');
const sourceFilter = document.getElementById('sourceFilter');
const conversationCards = document.querySelectorAll('.conversation-card');
const noResults = document.getElementById('noResults');

function filterConversations() {
  const searchTerm = searchInput.value.toLowerCase();
  const sourceValue = sourceFilter.value.toLowerCase();
  
  let visibleCount = 0;
  
  conversationCards.forEach(card => {
    const title = card.getAttribute('data-title');
    const source = card.getAttribute('data-source');
    
    const matchesSearch = !searchTerm || title.includes(searchTerm);
    const matchesSource = !sourceValue || source === sourceValue;
    
    if (matchesSearch && matchesSource) {
      card.style.display = '';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });
  
  // Show/hide no results message
  noResults.style.display = visibleCount === 0 ? 'block' : 'none';
}

// Event listeners
searchInput.addEventListener('input', filterConversations);
sourceFilter.addEventListener('change', filterConversations);

// Clear search on Escape
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    searchInput.value = '';
    filterConversations();
  }
});
"""
        with open(self.output_dir / 'search.js', 'w', encoding='utf-8') as f:
            f.write(js)


def main():
    """CLI for archive generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ChatLift HTML Archive Generator')
    parser.add_argument('--archive-dir', default='chat-archive', help='Archive directory')
    
    args = parser.parse_args()
    
    generator = ArchiveGenerator(args.archive_dir)
    generator.generate_archive()


if __name__ == '__main__':
    main()
