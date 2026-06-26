#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_integration.py - Integration tests for ChinaTour Skill + Backend API

Tests:
1. API Client functionality
2. Fallback mechanism
3. End-to-end question answering
"""

import json
import os
import sys
import time
from typing import Dict, List

# Handle Windows console encoding
if sys.platform == 'win32':
    import io
    if not isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add scripts to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def log(color: str, message: str):
    """Print colored message"""
    print(f"{getattr(Colors, color, '')}{message}{Colors.RESET}")


# ============== Test Cases ==============

TEST_CASES = [
    {
        "name": "Chinese Opening Hours Question",
        "question": "故宫开放时间是什么？",
        "expected_keywords": ["开放", "时间", "8:00", "18:00"],
        "language": "zh",
    },
    {
        "name": "English Opening Hours Question",
        "question": "What are the opening hours of Forbidden City?",
        "expected_keywords": ["open", "Forbidden City", "8:00"],
        "language": "en",
    },
    {
        "name": "General Tourism Question",
        "question": "故宫有哪些必看的景点？",
        "expected_keywords": ["故宫", "景点", "太和殿"],
        "language": "zh",
    },
    {
        "name": "Local Fallback Test",
        "question": "故宫游览路线推荐",
        "expected_keywords": ["路线", "故宫", "推荐"],
        "language": "zh",
        "test_fallback": True,
    },
]


def run_api_client_tests() -> Dict:
    """Test API client functionality"""
    log('CYAN', '\n=== API Client Tests ===')

    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'tests': []
    }

    try:
        from api_client import ChinaTourClient

        client = ChinaTourClient(debug=False)

        # Test 1: Health check
        log('DIM', '\nTest 1: Health Check')
        results['total'] += 1
        try:
            health = client.health_check()
            if health.success:
                log('GREEN', '  PASS: API health check passed')
                results['passed'] += 1
                results['tests'].append({'name': 'health_check', 'passed': True})
            else:
                log('YELLOW', f'  WARN: API unhealthy - {health.error}')
                results['failed'] += 1
                results['tests'].append({'name': 'health_check', 'passed': False, 'error': health.error})
        except Exception as e:
            log('RED', f'  FAIL: Health check error - {e}')
            results['failed'] += 1
            results['tests'].append({'name': 'health_check', 'passed': False, 'error': str(e)})

        # Test 2: Attractions list
        log('DIM', '\nTest 2: Attractions List')
        results['total'] += 1
        try:
            attractions = client.get_attractions(limit=5)
            if len(attractions) > 0:
                log('GREEN', f'  PASS: Got {len(attractions)} attractions')
                results['passed'] += 1
                results['tests'].append({'name': 'attractions_list', 'passed': True, 'count': len(attractions)})
            else:
                log('YELLOW', '  WARN: No attractions returned')
                results['failed'] += 1
                results['tests'].append({'name': 'attractions_list', 'passed': False, 'error': 'No attractions'})
        except Exception as e:
            log('RED', f'  FAIL: Attractions list error - {e}')
            results['failed'] += 1
            results['tests'].append({'name': 'attractions_list', 'passed': False, 'error': str(e)})

        # Test 3: Ask question
        log('DIM', '\nTest 3: Ask Question')
        results['total'] += 1
        try:
            result = client.ask("故宫开放时间?", use_cache=True)
            if result.success and result.answer:
                log('GREEN', f'  PASS: Got answer ({result.processing_time_ms}ms, cache={result.from_cache})')
                results['passed'] += 1
                results['tests'].append({
                    'name': 'ask_question',
                    'passed': True,
                    'processing_time': result.processing_time_ms,
                    'from_cache': result.from_cache
                })
            else:
                log('RED', f'  FAIL: No answer - {result.error}')
                results['failed'] += 1
                results['tests'].append({'name': 'ask_question', 'passed': False, 'error': result.error})
        except Exception as e:
            log('RED', f'  FAIL: Ask question error - {e}')
            results['failed'] += 1
            results['tests'].append({'name': 'ask_question', 'passed': False, 'error': str(e)})

    except ImportError as e:
        log('RED', f'Cannot import API client: {e}')
        results['tests'].append({'name': 'import', 'passed': False, 'error': str(e)})

    return results


def run_fallback_tests() -> Dict:
    """Test fallback mechanism"""
    log('CYAN', '\n=== Fallback Handler Tests ===')

    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'tests': []
    }

    try:
        from fallback_handler import FallbackHandler

        # Test 1: Fallback with API available
        log('DIM', '\nTest 1: Fallback with API Available')
        results['total'] += 1
        try:
            handler = FallbackHandler(debug=False)
            result = handler.ask("故宫开放时间?")
            if result.success and result.source == 'api':
                log('GREEN', f'  PASS: Used API source')
                results['passed'] += 1
                results['tests'].append({'name': 'fallback_api', 'passed': True, 'source': result.source})
            else:
                log('YELLOW', f'  WARN: Source was {result.source}')
                results['failed'] += 1
                results['tests'].append({'name': 'fallback_api', 'passed': False, 'source': result.source})
        except Exception as e:
            log('RED', f'  FAIL: {e}')
            results['failed'] += 1
            results['tests'].append({'name': 'fallback_api', 'passed': False, 'error': str(e)})

        # Test 2: Fallback with invalid API
        log('DIM', '\nTest 2: Fallback with Invalid API (Local Fallback)')
        results['total'] += 1
        try:
            handler = FallbackHandler(api_url="http://invalid-server:9999", debug=False)
            result = handler.ask("故宫开放时间?")
            if result.success and result.source == 'local':
                log('GREEN', f'  PASS: Used local fallback')
                results['passed'] += 1
                results['tests'].append({'name': 'fallback_local', 'passed': True, 'source': result.source})
            else:
                log('YELLOW', f'  WARN: Source was {result.source}')
                results['failed'] += 1
                results['tests'].append({'name': 'fallback_local', 'passed': False, 'source': result.source})
        except Exception as e:
            log('RED', f'  FAIL: {e}')
            results['failed'] += 1
            results['tests'].append({'name': 'fallback_local', 'passed': False, 'error': str(e)})

        # Test 3: Fallback disabled
        log('DIM', '\nTest 3: Fallback Disabled')
        results['total'] += 1
        try:
            handler = FallbackHandler(api_url="http://invalid-server:9999", enable_fallback=False, debug=False)
            result = handler.ask("故宫开放时间?")
            if result.source == 'error':
                log('GREEN', f'  PASS: Returned error when fallback disabled')
                results['passed'] += 1
                results['tests'].append({'name': 'fallback_disabled', 'passed': True, 'source': result.source})
            else:
                log('YELLOW', f'  WARN: Source was {result.source}')
                results['failed'] += 1
                results['tests'].append({'name': 'fallback_disabled', 'passed': False, 'source': result.source})
        except Exception as e:
            log('RED', f'  FAIL: {e}')
            results['failed'] += 1
            results['tests'].append({'name': 'fallback_disabled', 'passed': False, 'error': str(e)})

    except ImportError as e:
        log('RED', f'Cannot import fallback handler: {e}')
        results['tests'].append({'name': 'import', 'passed': False, 'error': str(e)})

    return results


def run_e2e_tests() -> Dict:
    """Run end-to-end tests"""
    log('CYAN', '\n=== End-to-End Tests ===')

    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'tests': []
    }

    try:
        from fallback_handler import FallbackHandler

        handler = FallbackHandler(debug=False)

        for test_case in TEST_CASES:
            log('DIM', f"\nTest: {test_case['name']}")
            results['total'] += 1

            try:
                result = handler.ask(test_case['question'], language=test_case['language'])

                # Check for expected keywords
                answer_lower = result.answer.lower()
                found_keywords = [kw for kw in test_case['expected_keywords']
                                 if kw.lower() in answer_lower]

                min_keywords = 2 if not test_case.get('test_fallback') else 1
                passed = len(found_keywords) >= min_keywords

                if passed:
                    log('GREEN', f'  PASS: Found {len(found_keywords)}/{len(test_case["expected_keywords"])} keywords')
                    results['passed'] += 1
                    results['tests'].append({
                        'name': test_case['name'],
                        'passed': True,
                        'keywords_found': len(found_keywords),
                        'source': result.source
                    })
                else:
                    log('RED', f'  FAIL: Only found {len(found_keywords)}/{len(test_case["expected_keywords"])} keywords')
                    results['failed'] += 1
                    results['tests'].append({
                        'name': test_case['name'],
                        'passed': False,
                        'keywords_found': len(found_keywords),
                        'source': result.source
                    })

            except Exception as e:
                log('RED', f'  FAIL: {e}')
                results['failed'] += 1
                results['tests'].append({'name': test_case['name'], 'passed': False, 'error': str(e)})

    except ImportError as e:
        log('RED', f'Cannot import fallback handler: {e}')
        results['tests'].append({'name': 'import', 'passed': False, 'error': str(e)})

    return results


def main():
    """Run all integration tests"""
    print('\n' + '=' * 60)
    print('ChinaTour Skill + Backend API Integration Tests')
    print('=' * 60)

    start_time = time.time()

    # Run tests
    api_results = run_api_client_tests()
    fallback_results = run_fallback_tests()
    e2e_results = run_e2e_tests()

    # Combine results
    total_tests = api_results['total'] + fallback_results['total'] + e2e_results['total']
    total_passed = api_results['passed'] + fallback_results['passed'] + e2e_results['passed']
    total_failed = api_results['failed'] + fallback_results['failed'] + e2e_results['failed']

    duration = time.time() - start_time

    # Print summary
    print('\n' + '=' * 60)
    print('Test Summary')
    print('=' * 60)
    print(f'\nAPI Client Tests: {api_results["passed"]}/{api_results["total"]} passed')
    print(f'Fallback Tests: {fallback_results["passed"]}/{fallback_results["total"]} passed')
    print(f'E2E Tests: {e2e_results["passed"]}/{e2e_results["total"]} passed')
    print(f'\nTotal: {total_passed}/{total_tests} passed ({total_failed} failed)')
    print(f'Duration: {duration:.1f}s')

    # Overall result
    if total_passed == total_tests:
        log('GREEN', '\nAll tests passed!')
        return 0
    elif total_passed > total_failed:
        log('YELLOW', '\nMost tests passed, some failures')
        return 1
    else:
        log('RED', '\nMany tests failed')
        return 2


if __name__ == '__main__':
    exit(main())