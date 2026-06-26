#!/usr/bin/env python3
"""
FAQ Forge - Publisher
Author: Shadow Rose
License: MIT
quality-verified

Generate publishable FAQ documentation in HTML, Markdown, and plain text.
Professional templates with search, navigation, and collapsible sections.
"""

import json
import os
from datetime import datetime
from typing import List, Optional
from faq_forge import FAQDatabase, FAQEntry


class FAQPublisher:
    """Generate FAQ documentation in multiple formats."""
    
    def __init__(self, db: FAQDatabase):
        self.db = db
    
    def publish_html(self, output_file: str, product: Optional[str] = None,
                     title: str = "Frequently Asked Questions",
                     show_search: bool = True, collapsible: bool = True,
                     show_toc: bool = True):
        """
        Generate professional HTML FAQ page with search and navigation.
        Static page - no server required.
        """
        entries = self.db.search(product=product)
        
        if not entries:
            print("Warning: No FAQ entries found")
            return
        
        # Group by category
        by_category = {}
        for entry in entries:
            if entry.category not in by_category:
                by_category[entry.category] = []
            by_category[entry.category].append(entry)
        
        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .search-box {{
            padding: 20px 30px;
            background: #f9f9f9;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 25px;
            outline: none;
            transition: border-color 0.3s;
        }}
        
        .search-box input:focus {{
            border-color: #667eea;
        }}
        
        .toc {{
            padding: 20px 30px;
            background: #fafafa;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .toc h2 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #667eea;
        }}
        
        .toc ul {{
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .toc li a {{
            display: inline-block;
            padding: 8px 16px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 20px;
            color: #667eea;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .toc li a:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .category {{
            margin-bottom: 40px;
        }}
        
        .category-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .faq-item {{
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            transition: box-shadow 0.3s;
        }}
        
        .faq-item:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .faq-question {{
            padding: 18px 20px;
            background: #f9f9f9;
            cursor: pointer;
            font-weight: 600;
            font-size: 1.1em;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s;
        }}
        
        .faq-question:hover {{
            background: #f0f0f0;
        }}
        
        .faq-question .icon {{
            font-size: 1.2em;
            transition: transform 0.3s;
        }}
        
        .faq-item.active .faq-question .icon {{
            transform: rotate(180deg);
        }}
        
        .faq-answer {{
            padding: 20px;
            background: white;
            display: none;
            line-height: 1.8;
        }}
        
        .faq-item.active .faq-answer {{
            display: block;
        }}
        
        .faq-meta {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #f0f0f0;
            font-size: 0.9em;
            color: #666;
        }}
        
        .tag {{
            display: inline-block;
            padding: 4px 10px;
            background: #e8eaf6;
            color: #5c6bc0;
            border-radius: 12px;
            font-size: 0.85em;
            margin-right: 5px;
            margin-top: 5px;
        }}
        
        .priority-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }}
        
        .priority-critical {{
            background: #ffebee;
            color: #c62828;
        }}
        
        .priority-high {{
            background: #fff3e0;
            color: #e65100;
        }}
        
        .priority-normal {{
            background: #e8f5e9;
            color: #2e7d32;
        }}
        
        .priority-low {{
            background: #f5f5f5;
            color: #757575;
        }}
        
        .related-questions {{
            margin-top: 15px;
            padding: 15px;
            background: #f5f7fa;
            border-radius: 6px;
        }}
        
        .related-questions h4 {{
            margin-bottom: 10px;
            color: #667eea;
            font-size: 0.95em;
        }}
        
        .related-questions ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .related-questions li {{
            margin: 5px 0;
        }}
        
        .related-questions a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .related-questions a:hover {{
            text-decoration: underline;
        }}
        
        footer {{
            padding: 20px 30px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            background: #f9f9f9;
            border-top: 1px solid #e0e0e0;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.1em;
        }}
        
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}
            
            .category-title {{
                font-size: 1.4em;
            }}
            
            .toc ul {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p>Find answers to common questions</p>
        </header>
"""
        
        if show_search:
            html += """
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search questions and answers..." />
        </div>
"""
        
        if show_toc:
            html += """
        <div class="toc">
            <h2>Categories</h2>
            <ul>
"""
            for category in sorted(by_category.keys()):
                cat_id = category.lower().replace(" ", "-")
                html += f'                <li><a href="#{cat_id}">{category}</a></li>\n'
            
            html += """            </ul>
        </div>
"""
        
        html += """
        <div class="content">
"""
        
        for category in sorted(by_category.keys()):
            cat_id = category.lower().replace(" ", "-")
            html += f'            <div class="category" id="{cat_id}">\n'
            html += f'                <h2 class="category-title">{category}</h2>\n'
            
            for entry in by_category[category]:
                active_class = "" if collapsible else "active"
                html += f'                <div class="faq-item {active_class}" data-id="{entry.id}">\n'
                html += '                    <div class="faq-question">\n'
                html += f'                        <span>{entry.question}</span>\n'
                
                if entry.priority in ["critical", "high"]:
                    html += f'                        <span class="priority-badge priority-{entry.priority}">{entry.priority.upper()}</span>\n'
                
                if collapsible:
                    html += '                        <span class="icon">▼</span>\n'
                
                html += '                    </div>\n'
                html += '                    <div class="faq-answer">\n'
                html += f'                        <p>{entry.answer}</p>\n'
                
                if entry.tags or entry.related:
                    html += '                        <div class="faq-meta">\n'
                    
                    if entry.tags:
                        for tag in entry.tags:
                            html += f'                            <span class="tag">{tag}</span>\n'
                    
                    if entry.related:
                        html += '                            <div class="related-questions">\n'
                        html += '                                <h4>Related Questions:</h4>\n'
                        html += '                                <ul>\n'
                        for related_id in entry.related:
                            related_entry = self.db.get(related_id)
                            if related_entry:
                                html += f'                                    <li><a href="#" data-related="{related_id}">{related_entry.question}</a></li>\n'
                        html += '                                </ul>\n'
                        html += '                            </div>\n'
                    
                    html += '                        </div>\n'
                
                html += '                    </div>\n'
                html += '                </div>\n'
            
            html += '            </div>\n'
        
        html += """        </div>
        
        <div class="no-results" id="noResults" style="display: none;">
            No questions found matching your search.
        </div>
        
        <footer>
            <p>Generated by FAQ Forge &bull; Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</p>
        </footer>
    </div>
    
    <script>
        // Toggle FAQ items
        document.querySelectorAll('.faq-question').forEach(question => {
            question.addEventListener('click', function() {
                const item = this.closest('.faq-item');
                item.classList.toggle('active');
            });
        });
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const query = this.value.toLowerCase();
                const items = document.querySelectorAll('.faq-item');
                let visibleCount = 0;
                
                items.forEach(item => {
                    const question = item.querySelector('.faq-question span').textContent.toLowerCase();
                    const answer = item.querySelector('.faq-answer p').textContent.toLowerCase();
                    
                    if (question.includes(query) || answer.includes(query)) {
                        item.style.display = '';
                        visibleCount++;
                        if (query.length > 0) {
                            item.classList.add('active');
                        }
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                // Show/hide categories based on visible items
                document.querySelectorAll('.category').forEach(category => {
                    const visibleItems = category.querySelectorAll('.faq-item[style=""]').length;
                    category.style.display = visibleItems > 0 ? '' : 'none';
                });
                
                // Show "no results" message
                document.getElementById('noResults').style.display = visibleCount === 0 ? 'block' : 'none';
                document.querySelector('.content').style.display = visibleCount === 0 ? 'none' : 'block';
            });
        }
        
        // Related question links
        document.querySelectorAll('a[data-related]').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('data-related');
                const targetItem = document.querySelector(`.faq-item[data-id="${targetId}"]`);
                
                if (targetItem) {
                    targetItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    targetItem.classList.add('active');
                    
                    // Highlight effect
                    targetItem.style.backgroundColor = '#fff9c4';
                    setTimeout(() => {
                        targetItem.style.backgroundColor = '';
                    }, 2000);
                }
            });
        });
    </script>
</body>
</html>
"""
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ HTML FAQ published to {output_file}")
    
    def publish_markdown(self, output_file: str, product: Optional[str] = None,
                         title: str = "Frequently Asked Questions"):
        """Generate Markdown FAQ documentation."""
        entries = self.db.search(product=product)
        
        if not entries:
            print("Warning: No FAQ entries found")
            return
        
        # Group by category
        by_category = {}
        for entry in entries:
            if entry.category not in by_category:
                by_category[entry.category] = []
            by_category[entry.category].append(entry)
        
        # Generate Markdown
        md = f"# {title}\n\n"
        md += f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        
        # Table of contents
        md += "## Table of Contents\n\n"
        for category in sorted(by_category.keys()):
            cat_anchor = category.lower().replace(" ", "-")
            md += f"- [{category}](#{cat_anchor})\n"
        md += "\n---\n\n"
        
        # FAQ entries
        for category in sorted(by_category.keys()):
            cat_anchor = category.lower().replace(" ", "-")
            md += f"## {category}\n\n"
            
            for entry in by_category[category]:
                md += f"### {entry.question}\n\n"
                
                if entry.priority in ["critical", "high"]:
                    md += f"**Priority: {entry.priority.upper()}**\n\n"
                
                md += f"{entry.answer}\n\n"
                
                if entry.tags:
                    md += f"*Tags: {', '.join(entry.tags)}*\n\n"
                
                if entry.related:
                    md += "**Related questions:**\n"
                    for related_id in entry.related:
                        related_entry = self.db.get(related_id)
                        if related_entry:
                            md += f"- {related_entry.question}\n"
                    md += "\n"
                
                md += "---\n\n"
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"✓ Markdown FAQ published to {output_file}")
    
    def publish_text(self, output_file: str, product: Optional[str] = None,
                     title: str = "Frequently Asked Questions"):
        """Generate plain text FAQ documentation."""
        entries = self.db.search(product=product)
        
        if not entries:
            print("Warning: No FAQ entries found")
            return
        
        # Group by category
        by_category = {}
        for entry in entries:
            if entry.category not in by_category:
                by_category[entry.category] = []
            by_category[entry.category].append(entry)
        
        # Generate text
        txt = f"{title}\n"
        txt += "=" * len(title) + "\n\n"
        txt += f"Last updated: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for category in sorted(by_category.keys()):
            txt += f"\n{category}\n"
            txt += "-" * len(category) + "\n\n"
            
            for i, entry in enumerate(by_category[category], 1):
                txt += f"{i}. {entry.question}\n"
                
                if entry.priority in ["critical", "high"]:
                    txt += f"   [PRIORITY: {entry.priority.upper()}]\n"
                
                txt += f"\n   {entry.answer}\n"
                
                if entry.tags:
                    txt += f"\n   Tags: {', '.join(entry.tags)}\n"
                
                if entry.related:
                    txt += "\n   Related questions:\n"
                    for related_id in entry.related:
                        related_entry = self.db.get(related_id)
                        if related_entry:
                            txt += f"   - {related_entry.question}\n"
                
                txt += "\n"
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(txt)
        
        print(f"✓ Text FAQ published to {output_file}")


def main():
    """Command-line interface for FAQ publishing."""
    import sys
    
    if len(sys.argv) < 3:
        print("FAQ Forge Publisher")
        print("\nUsage:")
        print("  faq_publish.py html <output.html> [--product PROD] [--title TITLE]")
        print("  faq_publish.py markdown <output.md> [--product PROD] [--title TITLE]")
        print("  faq_publish.py text <output.txt> [--product PROD] [--title TITLE]")
        print("\nOptions:")
        print("  --product PROD    Filter by product")
        print("  --title TITLE     Custom page title")
        print("  --no-search       Disable search box (HTML only)")
        print("  --no-toc          Disable table of contents")
        print("  --no-collapse     Show all answers expanded (HTML only)")
        return
    
    db = FAQDatabase()
    format_type = sys.argv[1]
    output_file = sys.argv[2]
    
    # Parse options
    product = None
    title = "Frequently Asked Questions"
    show_search = True
    show_toc = True
    collapsible = True
    
    for i in range(3, len(sys.argv)):
        if sys.argv[i] == "--product" and i + 1 < len(sys.argv):
            product = sys.argv[i + 1]
        elif sys.argv[i] == "--title" and i + 1 < len(sys.argv):
            title = sys.argv[i + 1]
        elif sys.argv[i] == "--no-search":
            show_search = False
        elif sys.argv[i] == "--no-toc":
            show_toc = False
        elif sys.argv[i] == "--no-collapse":
            collapsible = False
    
    publisher = FAQPublisher(db)
    
    if format_type == "html":
        publisher.publish_html(output_file, product, title, show_search, collapsible, show_toc)
    elif format_type == "markdown":
        publisher.publish_markdown(output_file, product, title)
    elif format_type == "text":
        publisher.publish_text(output_file, product, title)
    else:
        print(f"Unknown format: {format_type}")
        print("Supported formats: html, markdown, text")


if __name__ == "__main__":
    main()
