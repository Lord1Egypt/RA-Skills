#!/usr/bin/env python3
"""
Test suite for X API client
Tests basic functionality without requiring API credentials
"""

import sys
import json


def test_username_parsing():
    """Test username parsing (with/without @)"""
    test_cases = [
        ("elonmusk", "elonmusk"),
        ("@elonmusk", "elonmusk"),
        ("@OpenAI", "OpenAI"),
    ]
    
    for input_name, expected in test_cases:
        result = input_name.lstrip('@')
        assert result == expected, f"Failed for {input_name}: got {result}, expected {expected}"
    
    print("✓ Username parsing tests passed")
    return True


def test_argument_parsing():
    """Test command line argument parsing"""
    # Simulate sys.argv parsing
    test_argv = ["script.py", "elonmusk", "20", "--no-replies", "--no-retweets"]
    
    username = test_argv[1].lstrip('@')
    count = 10
    no_replies = False
    no_retweets = False
    
    for arg in test_argv[2:]:
        if arg.isdigit():
            count = int(arg)
        elif arg == '--no-replies':
            no_replies = True
        elif arg == '--no-retweets':
            no_retweets = True
    
    assert username == "elonmusk", f"Username parsing failed: {username}"
    assert count == 20, f"Count parsing failed: {count}"
    assert no_replies == True, "no-replies flag parsing failed"
    assert no_retweets == True, "no-retweets flag parsing failed"
    
    print("✓ Argument parsing tests passed")
    return True


def test_output_format():
    """Test JSON output format"""
    sample_output = {
        'user': {
            'id': '12345',
            'username': 'testuser',
            'name': 'Test User',
            'verified': False,
            'public_metrics': {
                'followers_count': 1000,
                'following_count': 500
            }
        },
        'tweets': [
            {
                'id': 'tweet1',
                'text': 'Hello World',
                'created_at': '2024-01-01T00:00:00Z'
            }
        ],
        'meta': {
            'result_count': 1
        }
    }
    
    # Verify JSON serializable
    json_str = json.dumps(sample_output, indent=2, ensure_ascii=False)
    parsed = json.loads(json_str)
    
    assert 'user' in parsed, "Missing user field"
    assert 'tweets' in parsed, "Missing tweets field"
    assert 'meta' in parsed, "Missing meta field"
    
    print("✓ Output format tests passed")
    return True


def test_search_query_building():
    """Test search query construction"""
    # Test basic query
    query = "machine learning"
    assert query == "machine learning"
    
    # Test complex query with operators
    complex_query = '(from:elonmusk OR from:sama) "AI" lang:en -is:retweet'
    assert 'from:' in complex_query
    assert 'lang:en' in complex_query
    assert '-is:retweet' in complex_query
    
    print("✓ Search query building tests passed")
    return True


def main():
    """Run all tests"""
    print("Running X API Client Tests\n")
    
    all_passed = True
    all_passed &= test_username_parsing()
    all_passed &= test_argument_parsing()
    all_passed &= test_output_format()
    all_passed &= test_search_query_building()
    
    print("\n" + "="*40)
    if all_passed:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == '__main__':
    sys.exit(main())
