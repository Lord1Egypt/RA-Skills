#!/usr/bin/env python3
"""
FAQ Forge - Import Tool
Author: Shadow Rose
License: MIT
quality-verified

Import Q&A pairs from existing markdown documentation.
Supports common FAQ markdown patterns and structured formats.
"""

import re
import os
from typing import List, Tuple, Optional
from faq_forge import FAQDatabase, FAQEntry


class FAQImporter:
    """Import FAQ entries from markdown files."""
    
    def __init__(self, db: FAQDatabase):
        self.db = db
    
    def import_from_markdown(self, file_path: str, category: str = "General",
                            product: str = "default", auto_tag: bool = True) -> int:
        """
        Import Q&A pairs from markdown file.
        Supports multiple markdown FAQ formats.
        Returns number of entries imported.
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try different parsing strategies
        entries = []
        
        # Strategy 1: Q: / A: format
        qa_pairs = self._parse_qa_format(content)
        if qa_pairs:
            entries.extend(qa_pairs)
        
        # Strategy 2: Heading + paragraph format (e.g., ### Question\nAnswer paragraph)
        if not entries:
            entries = self._parse_heading_format(content)
        
        # Strategy 3: Bold question + answer format (**Question**\nAnswer)
        if not entries:
            entries = self._parse_bold_format(content)
        
        if not entries:
            print(f"Warning: No Q&A pairs found in {file_path}")
            return 0
        
        # Import entries
        imported = 0
        for question, answer in entries:
            # Auto-tag based on content
            tags = []
            if auto_tag:
                tags = self._auto_generate_tags(question, answer)
            
            entry = FAQEntry(
                question=question.strip(),
                answer=answer.strip(),
                category=category,
                tags=tags,
                priority="normal",
                product=product
            )
            
            self.db.add(entry)
            imported += 1
        
        print(f"✓ Imported {imported} FAQ entries from {file_path}")
        return imported
    
    def _parse_qa_format(self, content: str) -> List[Tuple[str, str]]:
        """
        Parse Q: / A: format:
        Q: What is your return policy?
        A: We accept returns within 30 days...
        """
        entries = []
        
        # Find Q:/A: pairs (case insensitive)
        pattern = r'(?:^|\n)Q:\s*(.+?)(?:\n|\r\n)A:\s*(.+?)(?=\n\s*Q:|$)'
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        
        for question, answer in matches:
            entries.append((question.strip(), answer.strip()))
        
        return entries
    
    def _parse_heading_format(self, content: str) -> List[Tuple[str, str]]:
        """
        Parse heading + paragraph format:
        ### How do I reset my password?
        Click on "Forgot Password" on the login page...
        """
        entries = []
        
        # Split by headings (### or ##)
        sections = re.split(r'\n#{2,3}\s+', content)
        
        for section in sections[1:]:  # Skip first section (before any heading)
            # Split heading from content
            lines = section.split('\n', 1)
            if len(lines) < 2:
                continue
            
            question = lines[0].strip()
            answer = lines[1].strip()
            
            # Filter out headings that are clearly section titles, not questions
            if len(question) > 10 and len(answer) > 10:
                # Clean up answer (remove extra whitespace, keep paragraphs)
                answer = re.sub(r'\n{3,}', '\n\n', answer)
                entries.append((question, answer))
        
        return entries
    
    def _parse_bold_format(self, content: str) -> List[Tuple[str, str]]:
        """
        Parse bold question format:
        **What payment methods do you accept?**
        We accept Visa, Mastercard, PayPal...
        """
        entries = []
        
        # Find bold text followed by content
        pattern = r'\*\*(.+?)\*\*\s*\n\s*(.+?)(?=\n\s*\*\*|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for question, answer in matches:
            question = question.strip()
            answer = answer.strip()
            
            # Only accept if it looks like a question-answer pair
            if len(question) > 10 and len(answer) > 10:
                entries.append((question, answer))
        
        return entries
    
    def _auto_generate_tags(self, question: str, answer: str) -> List[str]:
        """Auto-generate tags based on content keywords."""
        tags = []
        text = (question + " " + answer).lower()
        
        # Common business keywords
        keyword_map = {
            "payment": ["payment", "pay", "credit card", "paypal", "billing"],
            "shipping": ["ship", "deliver", "freight", "tracking"],
            "refund": ["refund", "return", "money back"],
            "account": ["account", "login", "password", "profile"],
            "pricing": ["price", "cost", "discount", "coupon"],
            "support": ["support", "help", "contact", "assistance"],
            "product": ["product", "item", "feature"],
            "subscription": ["subscription", "subscribe", "plan", "membership"],
            "security": ["security", "safe", "encrypt", "privacy"],
            "technical": ["technical", "bug", "error", "issue"]
        }
        
        for tag, keywords in keyword_map.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        return tags[:5]  # Limit to 5 tags
    
    def import_from_directory(self, dir_path: str, pattern: str = "*.md",
                             category: str = "General", product: str = "default") -> int:
        """Import all markdown files from a directory."""
        import glob
        
        if not os.path.isdir(dir_path):
            print(f"Error: Directory not found: {dir_path}")
            return 0
        
        # Find all markdown files
        search_pattern = os.path.join(dir_path, pattern)
        files = glob.glob(search_pattern)
        
        if not files:
            print(f"No files matching {pattern} found in {dir_path}")
            return 0
        
        total_imported = 0
        for file_path in files:
            print(f"\nImporting from {os.path.basename(file_path)}...")
            imported = self.import_from_markdown(file_path, category, product)
            total_imported += imported
        
        print(f"\n✓ Total: {total_imported} entries imported from {len(files)} files")
        return total_imported
    
    def import_from_json(self, file_path: str) -> int:
        """
        Import from JSON format:
        [
          {
            "question": "...",
            "answer": "...",
            "category": "...",
            "tags": ["..."],
            "priority": "normal",
            "product": "default"
          }
        ]
        """
        import json
        
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("Error: JSON must be an array of FAQ objects")
            return 0
        
        imported = 0
        for item in data:
            if not isinstance(item, dict) or "question" not in item or "answer" not in item:
                print(f"Warning: Skipping invalid entry: {item}")
                continue
            
            entry = FAQEntry(
                question=item["question"],
                answer=item["answer"],
                category=item.get("category", "General"),
                tags=item.get("tags", []),
                priority=item.get("priority", "normal"),
                product=item.get("product", "default")
            )
            
            self.db.add(entry)
            imported += 1
        
        print(f"✓ Imported {imported} FAQ entries from {file_path}")
        return imported
    
    def export_to_json(self, file_path: str, product: Optional[str] = None):
        """Export FAQ database to JSON format for backup/migration."""
        import json
        
        entries = self.db.search(product=product)
        
        data = []
        for entry in entries:
            data.append({
                "question": entry.question,
                "answer": entry.answer,
                "category": entry.category,
                "tags": entry.tags,
                "priority": entry.priority,
                "product": entry.product
            })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported {len(data)} entries to {file_path}")


def main():
    """Command-line interface for FAQ import."""
    import sys
    
    if len(sys.argv) < 2:
        print("FAQ Forge Importer")
        print("\nUsage:")
        print("  faq_import.py markdown <file.md> [--category CAT] [--product PROD] [--no-auto-tag]")
        print("  faq_import.py directory <dir> [--pattern *.md] [--category CAT] [--product PROD]")
        print("  faq_import.py json <file.json>")
        print("  faq_import.py export <output.json> [--product PROD]")
        print("\nSupported markdown formats:")
        print("  - Q: / A: format")
        print("  - Heading format (### Question)")
        print("  - Bold question format (**Question**)")
        return
    
    db = FAQDatabase()
    importer = FAQImporter(db)
    
    command = sys.argv[1]
    
    if command == "markdown":
        if len(sys.argv) < 3:
            print("Error: markdown requires <file.md>")
            return
        
        file_path = sys.argv[2]
        category = "General"
        product = "default"
        auto_tag = True
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
            elif sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
            elif sys.argv[i] == "--no-auto-tag":
                auto_tag = False
        
        importer.import_from_markdown(file_path, category, product, auto_tag)
    
    elif command == "directory":
        if len(sys.argv) < 3:
            print("Error: directory requires <dir>")
            return
        
        dir_path = sys.argv[2]
        pattern = "*.md"
        category = "General"
        product = "default"
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--pattern" and i + 1 < len(sys.argv):
                pattern = sys.argv[i + 1]
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
            elif sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
        
        importer.import_from_directory(dir_path, pattern, category, product)
    
    elif command == "json":
        if len(sys.argv) < 3:
            print("Error: json requires <file.json>")
            return
        
        file_path = sys.argv[2]
        importer.import_from_json(file_path)
    
    elif command == "export":
        if len(sys.argv) < 3:
            print("Error: export requires <output.json>")
            return
        
        output_file = sys.argv[2]
        product = None
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
        
        importer.export_to_json(output_file, product)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
