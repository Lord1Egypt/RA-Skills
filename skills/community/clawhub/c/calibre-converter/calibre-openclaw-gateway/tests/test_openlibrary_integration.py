"""Test script for OpenLibrary integration."""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.openlibrary_service import openlibrary_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


def test_openlibrary_search_by_isbn():
    """Test searching for a book by ISBN."""
    print("\n=== Testing OpenLibrary Search by ISBN ===")
    
    # Test with a well-known ISBN (Harry Potter and the Philosopher's Stone)
    test_isbn = "9780747532743"
    
    result = openlibrary_service.search_by_isbn(test_isbn)
    
    if result:
        print(f"✓ Found book: {result.get('title')}")
        print(f"  Authors: {result.get('authors')}")
        print(f"  Publisher: {result.get('publishers')}")
        print(f"  Publish Date: {result.get('publish_date')}")
        print(f"  OpenLibrary URL: {result.get('openlibrary_url')}")
        print(f"  OLID: {result.get('olid')}")
        return True
    else:
        print(f"✗ No results found for ISBN: {test_isbn}")
        return False


def test_openlibrary_search_by_title_author():
    """Test searching for a book by title and author."""
    print("\n=== Testing OpenLibrary Search by Title/Author ===")
    
    # Test with a well-known book
    test_title = "The Hobbit"
    test_author = "J.R.R. Tolkien"
    
    results = openlibrary_service.search_by_title_author(test_title, test_author)
    
    if results:
        print(f"✓ Found {len(results)} results")
        for i, book in enumerate(results[:3], 1):
            print(f"  {i}. {book.get('title')} by {book.get('authors')}")
            print(f"     OLID: {book.get('olid')}")
            print(f"     First Publish Year: {book.get('first_publish_year')}")
        return True
    else:
        print(f"✗ No results found for: {test_title} by {test_author}")
        return False


def test_openlibrary_download_links():
    """Test getting download links for a book."""
    print("\n=== Testing OpenLibrary Download Links ===")
    
    # Test with a known public domain book OLID (Alice's Adventures in Wonderland)
    test_olid = "OL7353617M"
    
    download_info = openlibrary_service.get_download_links(olid=test_olid)
    
    if download_info:
        print(f"✓ Download info retrieved for: {download_info.get('title')}")
        print(f"  OLID: {download_info.get('olid')}")
        print(f"  Public Domain: {download_info.get('public_domain')}")
        print(f"  Preview URL: {download_info.get('preview_url')}")
        print(f"  Available formats: {len(download_info.get('download_formats', []))}")
        for fmt in download_info.get('download_formats', []):
            print(f"    - {fmt.get('format')}: {fmt.get('url')}")
        return True
    else:
        print(f"✗ No download links found for OLID: {test_olid}")
        return False


def test_openlibrary_author_info():
    """Test getting author information."""
    print("\n=== Testing OpenLibrary Author Info ===")
    
    test_author = "J.K. Rowling"
    
    author_info = openlibrary_service.get_author_info(test_author)
    
    if author_info:
        print(f"✓ Found author: {author_info.get('name')}")
        print(f"  OLID: {author_info.get('olid')}")
        print(f"  Bio: {author_info.get('bio')[:100] if author_info.get('bio') else 'N/A'}...")
        print(f"  Work Count: {author_info.get('work_count')}")
        return True
    else:
        print(f"✗ No author info found for: {test_author}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("OpenLibrary Integration Test Suite")
    print("=" * 60)
    
    if not openlibrary_service.enabled:
        print("\n✗ OpenLibrary service is not enabled")
        print("  Set OPENLIBRARY_ENABLED=true in .env to enable")
        return
    
    results = {
        "search_by_isbn": test_openlibrary_search_by_isbn(),
        "search_by_title_author": test_openlibrary_search_by_title_author(),
        "download_links": test_openlibrary_download_links(),
        "author_info": test_openlibrary_author_info()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ {total - passed} test(s) failed")


if __name__ == "__main__":
    main()
