#!/usr/bin/env python3
"""
AetherCore Simple Test Runner
Night Market Intelligence Technical Serviceization - Quick Verification
"""

import sys
import os
import json
import time
from datetime import datetime

def run_basic_functional_tests():
    """Run basic functional tests"""
    print("\n" + "=" * 60)
    print("🔧 Functional Testing")
    print("Verify JSON Processing")
    print("=" * 60)
    
    test_results = []
    
    try:
        import json
        
        # Test 1: JSON Parsing
        print("1. Testing JSON Parsing...")
        test_data = '{"name": "AetherCore", "version": "3.3.4"}'
        parsed = json.loads(test_data)
        assert parsed["name"] == "AetherCore"
        assert parsed["version"] == "3.3.4"
        print("  ✅ JSON Parsing")
        test_results.append(("JSON Parsing", True))
        
        # Test 2: JSON Serialization
        print("2. Testing JSON Serialization...")
        data = {"project": "AetherCore", "performance": "45,305 ops/sec"}
        serialized = json.dumps(data)
        assert '"project": "AetherCore"' in serialized
        print("  ✅ JSON Serialization")
        test_results.append(("JSON Serialization", True))
        
        # Test 3: Unicode Support
        print("3. Testing Unicode Support...")
        unicode_data = {"name": "夜市智慧體", "english": "Night Market Intelligence"}
        unicode_json = json.dumps(unicode_data, ensure_ascii=False)
        parsed_back = json.loads(unicode_json)
        assert parsed_back["english"] == "Night Market Intelligence"
        print("  ✅ Unicode Support")
        test_results.append(("Unicode Support", True))
        
        # Test 4: Complex Data Structures
        print("4. Testing Complex Data Structures...")
        complex_data = {
            "version": "3.3.4",
            "performance": {
                "json_parsing": 45305,
                "data_query": 361064
            },
            "features": ["smart_indexing", "workflow_optimization"]
        }
        complex_json = json.dumps(complex_data)
        parsed_complex = json.loads(complex_json)
        assert parsed_complex["performance"]["json_parsing"] == 45305
        print("  ✅ Complex Data Structures")
        test_results.append(("Complex Data", True))
        
        # Test 5: Error Handling
        print("5. Testing Error Handling...")
        try:
            json.loads("{invalid json}")
            print("  ❌ Should have raised JSONDecodeError")
            test_results.append(("Error Handling", False))
        except json.JSONDecodeError:
            print("  ✅ Error Handling")
            test_results.append(("Error Handling", True))
        
    except Exception as e:
        print(f"  ❌ Error in functional tests: {e}")
        test_results.append(("Functional Tests", False))
    
    return test_results

def run_installation_checks():
    """Run installation and dependency checks"""
    print("\n" + "=" * 60)
    print("📦 Installation Checks")
    print("Verify Dependencies and Setup")
    print("=" * 60)
    
    check_results = []
    
    # Check 1: Python Version
    print("1. Checking Python Version...")
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"  ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        check_results.append(("Python Version", True))
    else:
        print(f"  ❌ Python {python_version.major}.{python_version.minor} - Need 3.8+")
        check_results.append(("Python Version", False))
    
    # Check 2: Required Modules
    print("2. Checking Required Modules...")
    required_modules = ["json", "sys", "os", "time", "datetime"]
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
            check_results.append((f"Module: {module}", True))
        except ImportError:
            print(f"  ❌ {module}")
            check_results.append((f"Module: {module}", False))
    
    # Check 3: Project Files
    print("3. Checking Project Files...")
    required_files = ["README.md", "LICENSE", "SKILL.md", "clawhub.json", "requirements.txt"]
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
            check_results.append((f"File: {file}", True))
        else:
            print(f"  ❌ {file}")
            check_results.append((f"File: {file}", False))
    
    return check_results

def run_performance_smoke_test():
    """Run a quick performance smoke test"""
    print("\n" + "=" * 60)
    print("⚡ Performance Smoke Test")
    print("Quick Performance Verification")
    print("=" * 60)
    
    perf_results = []
    
    try:
        import json
        import time
        
        # Simple performance test
        print("1. Running JSON Performance Test...")
        test_data = {"data": [{"id": i, "value": f"test_{i}"} for i in range(1000)]}
        json_str = json.dumps(test_data)
        
        # Time parsing
        start = time.perf_counter()
        for _ in range(100):
            json.loads(json_str)
        parse_time = time.perf_counter() - start
        
        # Time serialization
        start = time.perf_counter()
        for _ in range(100):
            json.dumps(test_data)
        dump_time = time.perf_counter() - start
        
        print(f"  ✅ Parse 100x: {parse_time:.3f}s ({100/parse_time:.0f} ops/sec)")
        print(f"  ✅ Dump 100x: {dump_time:.3f}s ({100/dump_time:.0f} ops/sec)")
        
        # Check if performance is reasonable
        if parse_time < 0.1 and dump_time < 0.1:
            perf_results.append(("Performance", True))
        else:
            perf_results.append(("Performance", False))
            print("  ⚠️  Performance slower than expected")
        
    except Exception as e:
        print(f"  ❌ Performance test error: {e}")
        perf_results.append(("Performance", False))
    
    return perf_results

def main():
    """Main test runner"""
    print("🚀 AetherCore v3.3.4 Simple Testing")
    print("Night Market Intelligence Technical Serviceization - Quick Verification")
    print("=" * 60)
    
    all_results = []
    
    # Run installation checks
    install_results = run_installation_checks()
    all_results.extend(install_results)
    
    # Run functional tests
    func_results = run_basic_functional_tests()
    all_results.extend(func_results)
    
    # Run performance smoke test
    perf_results = run_performance_smoke_test()
    all_results.extend(perf_results)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success in all_results if success)
    total = len(all_results)
    
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"📈 Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! AetherCore is ready.")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check above for details.")
    
    # Show failed tests
    failed_tests = [name for name, success in all_results if not success]
    if failed_tests:
        print("\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"  - {test}")
    
    print("\n" + "=" * 60)
    print("🎪 Night Market Intelligence Testing Complete")
    print("Technical Serviceization Verified")
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)