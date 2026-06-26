#!/usr/bin/env python3
"""
FAQ Forge Demo & Test Script
Author: Shadow Rose

Quick demonstration and verification that FAQ Forge works correctly.
Run this to test the installation and see features in action.
"""

import os
import sys
import tempfile
import shutil

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from faq_forge import FAQDatabase, FAQEntry
from faq_publish import FAQPublisher
from faq_import import FAQImporter
from faq_templates import FAQTemplates


def test_basic_operations():
    """Test basic FAQ operations."""
    print("\n=== Testing Basic Operations ===\n")
    
    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_file = os.path.join(temp_dir, "test_faq.json")
    db = FAQDatabase(db_file)
    
    print("✓ Database created")
    
    # Add entries
    entry1 = FAQEntry(
        "How do I get started?",
        "Visit our website and sign up for a free account.",
        category="Getting Started",
        tags=["signup", "account"],
        priority="high"
    )
    
    entry2 = FAQEntry(
        "What payment methods do you accept?",
        "We accept Visa, Mastercard, and PayPal.",
        category="Billing",
        tags=["payment", "billing"],
        priority="normal"
    )
    
    id1 = db.add(entry1)
    id2 = db.add(entry2)
    print(f"✓ Added 2 entries: {id1}, {id2}")
    
    # Search
    results = db.search("payment")
    assert len(results) == 1, "Search failed"
    print(f"✓ Search works: found {len(results)} result(s)")
    
    # Update
    db.update(id1, answer="Updated answer with more detail.")
    updated_entry = db.get(id1)
    assert "Updated" in updated_entry.answer, "Update failed"
    print("✓ Update works")
    
    # Related questions
    db.add_related(id1, id2)
    assert id2 in db.get(id1).related, "Related link failed"
    print("✓ Related questions work")
    
    # Stats
    stats = db.get_stats()
    assert stats['total_entries'] == 2, "Stats failed"
    print(f"✓ Stats: {stats['total_entries']} entries")
    
    # Delete
    db.delete(id2)
    assert db.get(id2) is None, "Delete failed"
    print("✓ Delete works")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("\n✅ All basic operations passed!\n")


def test_publishing():
    """Test publishing to different formats."""
    print("\n=== Testing Publishing ===\n")
    
    # Create temporary database with sample data
    temp_dir = tempfile.mkdtemp()
    db_file = os.path.join(temp_dir, "test_faq.json")
    db = FAQDatabase(db_file)
    
    # Add sample entries
    categories = ["Getting Started", "Billing", "Support"]
    for i, cat in enumerate(categories):
        entry = FAQEntry(
            f"Question {i+1} in {cat}?",
            f"This is the answer to question {i+1}.",
            category=cat,
            tags=[cat.lower()],
            priority="normal"
        )
        db.add(entry)
    
    print(f"✓ Created test database with {len(db.entries)} entries")
    
    publisher = FAQPublisher(db)
    
    # Test HTML output
    html_file = os.path.join(temp_dir, "test.html")
    publisher.publish_html(html_file)
    assert os.path.exists(html_file), "HTML output failed"
    
    with open(html_file, 'r') as f:
        html_content = f.read()
        assert "Question 1" in html_content, "HTML content missing"
        assert "searchInput" in html_content, "HTML search missing"
    
    print("✓ HTML publishing works")
    
    # Test Markdown output
    md_file = os.path.join(temp_dir, "test.md")
    publisher.publish_markdown(md_file)
    assert os.path.exists(md_file), "Markdown output failed"
    print("✓ Markdown publishing works")
    
    # Test text output
    txt_file = os.path.join(temp_dir, "test.txt")
    publisher.publish_text(txt_file)
    assert os.path.exists(txt_file), "Text output failed"
    print("✓ Text publishing works")
    
    # Test nested directory creation
    nested_file = os.path.join(temp_dir, "output", "nested", "test.html")
    publisher.publish_html(nested_file)
    assert os.path.exists(nested_file), "Nested directory creation failed"
    print("✓ Nested directory creation works")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("\n✅ All publishing tests passed!\n")


def test_import():
    """Test import functionality."""
    print("\n=== Testing Import ===\n")
    
    # Create temporary files
    temp_dir = tempfile.mkdtemp()
    db_file = os.path.join(temp_dir, "test_faq.json")
    db = FAQDatabase(db_file)
    
    # Create sample markdown file
    md_content = """# FAQ

## Getting Started

### How do I sign up?
Visit our website and click "Sign Up". Fill out the form and verify your email.

### What do I need to get started?
Just an email address and a password.

**Can I try before buying?**
Yes! We offer a 14-day free trial with no credit card required.

Q: How long does setup take?
A: Most users complete setup in under 5 minutes.
"""
    
    md_file = os.path.join(temp_dir, "sample.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Test import
    importer = FAQImporter(db)
    imported = importer.import_from_markdown(md_file, category="Getting Started")
    
    assert imported >= 1, f"Import failed: only {imported} entries"
    print(f"✓ Imported {imported} entries from markdown (heuristic parsing)")
    
    # Test JSON export
    json_file = os.path.join(temp_dir, "export.json")
    importer.export_to_json(json_file)
    assert os.path.exists(json_file), "JSON export failed"
    print("✓ JSON export works")
    
    # Test JSON import
    db2 = FAQDatabase(os.path.join(temp_dir, "test_faq2.json"))
    importer2 = FAQImporter(db2)
    imported2 = importer2.import_from_json(json_file)
    assert imported2 == imported, "JSON import failed"
    print("✓ JSON import works")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("\n✅ All import tests passed!\n")


def test_templates():
    """Test template functionality."""
    print("\n=== Testing Templates ===\n")
    
    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_file = os.path.join(temp_dir, "test_faq.json")
    db = FAQDatabase(db_file)
    
    templates = FAQTemplates(db)
    
    # Test applying template
    added = templates.apply_template("digital-products", customize=False)
    assert added > 5, f"Template failed: only {added} entries"
    print(f"✓ Applied template: {added} entries added")
    
    # Verify categories
    categories = db.get_categories()
    assert len(categories) > 0, "No categories created"
    print(f"✓ Categories created: {', '.join(sorted(categories))}")
    
    # Verify priorities
    high_priority = db.search(priority="high")
    assert len(high_priority) > 0, "No high-priority questions"
    print(f"✓ Priority system works: {len(high_priority)} high-priority questions")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("\n✅ All template tests passed!\n")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n=== Testing Edge Cases ===\n")
    
    temp_dir = tempfile.mkdtemp()
    db_file = os.path.join(temp_dir, "test_faq.json")
    db = FAQDatabase(db_file)
    
    # Test unicode and special characters
    entry = FAQEntry(
        "How do I use émojis 🎉?",
        "Just type them! We support unicode: 中文, العربية, 日本語",
        category="Technical Support",
        tags=["unicode", "emoji"]
    )
    entry_id = db.add(entry)
    
    # Reload and verify
    db2 = FAQDatabase(db_file)
    loaded_entry = db2.get(entry_id)
    assert loaded_entry is not None, "Unicode entry failed to load"
    assert "🎉" in loaded_entry.question, "Emoji not preserved"
    print("✓ Unicode and emoji support works")
    
    # Test ID collision handling
    entry1 = FAQEntry("How do I reset my password?", "Answer 1")
    entry2 = FAQEntry("How do I reset my password?", "Answer 2")
    id1 = db.add(entry1)
    id2 = db.add(entry2)
    assert id1 != id2, "ID collision not handled"
    print("✓ ID collision handling works")
    
    # Test empty search
    all_entries = db.search()
    assert len(all_entries) > 0, "Empty search failed"
    print("✓ Empty search returns all entries")
    
    # Test non-existent entry
    result = db.get("non-existent-id")
    assert result is None, "Non-existent entry should return None"
    print("✓ Non-existent entry handling works")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("\n✅ All edge case tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("FAQ Forge - Comprehensive Test Suite")
    print("="*60)
    
    try:
        test_basic_operations()
        test_publishing()
        test_import()
        test_templates()
        test_edge_cases()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! FAQ Forge is working correctly.")
        print("="*60)
        print("\nFAQ Forge is ready to use!")
        print("\nNext steps:")
        print("  1. Try a template: python faq_templates.py apply digital-products")
        print("  2. Add a question: python faq_forge.py add 'Question?' 'Answer'")
        print("  3. Publish: python faq_publish.py html faq.html")
        print("\nSee README.md for complete documentation.\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
