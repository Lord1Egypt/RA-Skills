#!/usr/bin/env python3
"""
Test script for C Support Library
"""

import sys
import os

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from c_parser import CParser, analyze_project, get_project_summary
from cmake_parser import CMakeParser, analyze_cmake_project
from unity_templates import UnityTestGenerator, UnityCMakeTemplates
from c_security_rules import CSecurityChecker, CSecurityRules


def test_c_parser():
    """Test C parser with sample code"""
    print("=" * 60)
    print("Testing C Parser")
    print("=" * 60)
    
    sample_c = '''
#include <stdio.h>
#include "myheader.h"

#define MAX_SIZE 100
#define DEBUG 1

typedef struct {
    int x;
    int y;
} Point;

static int internal_counter = 0;

int calculate_sum(int a, int b) {
    return a + b;
}

void process_data(char *buffer, int size) {
    strcpy(buffer, "test");  // Dangerous!
    printf(buffer);          // Format string issue!
}

int main(void) {
    char buf[50];
    gets(buf);  // Very dangerous!
    printf("Hello World\\n");
    return 0;
}
'''
    
    # Write sample file
    with open('/tmp/test_sample.c', 'w') as f:
        f.write(sample_c)
    
    parser = CParser()
    info = parser.parse_file('/tmp/test_sample.c')
    
    print(f"✓ Parsed file: {info.path}")
    print(f"✓ Functions: {len(info.functions)}")
    for func in info.functions:
        print(f"  - {func.return_type} {func.name}() at line {func.line}")
    
    print(f"✓ Includes: {len(info.includes)}")
    for inc in info.includes:
        print(f"  - {'<' if inc.is_system else '"'}{inc.path}{'>' if inc.is_system else '"'}")
    
    print(f"✓ Macros: {len(info.macros)}")
    for macro in info.macros:
        print(f"  - #define {macro.name} {macro.value or ''}")
    
    # Test dangerous function detection
    dangers = parser.find_dangerous_calls('/tmp/test_sample.c')
    print(f"✓ Dangerous calls found: {len(dangers)}")
    for d in dangers:
        print(f"  Line {d['line']}: {d['function']} - {d['advice']}")
    
    return True


def test_cmake_parser():
    """Test CMake parser with sample CMakeLists.txt"""
    print("\n" + "=" * 60)
    print("Testing CMake Parser")
    print("=" * 60)
    
    sample_cmake = '''
cmake_minimum_required(VERSION 3.10)
project(PokeClaw VERSION 1.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

include_directories(${CMAKE_SOURCE_DIR}/include)
add_compile_options(-Wall -Wextra -Werror)
add_definitions(-DDEBUG_MODE)

add_executable(pokeclaw
    src/main.c
    src/pokemon.c
    src/battle.c
)

target_include_directories(pokeclaw PRIVATE src)
target_link_libraries(pokeclaw m)

add_library(utils STATIC
    src/utils.c
    src/helpers.c
)

enable_testing()
add_test(NAME unit_tests COMMAND pokeclaw_test)

add_subdirectory(tests)
'''
    
    parser = CMakeParser()
    project = parser.parse_content(sample_cmake)
    
    print(f"✓ Project name: {project.name}")
    print(f"✓ Version: {project.version}")
    print(f"✓ Languages: {project.languages}")
    print(f"✓ Targets: {len(project.targets)}")
    for target in project.targets:
        print(f"  - {target.name} ({target.target_type})")
        print(f"    Sources: {len(target.sources)} files")
        if target.link_libraries:
            print(f"    Links: {target.link_libraries}")
    
    print(f"✓ Include dirs: {project.include_dirs}")
    print(f"✓ Tests: {len(project.tests)}")
    print(f"✓ Subdirectories: {project.subdirectories}")
    print(f"✓ Compile options: {project.compile_options}")
    
    return True


def test_unity_templates():
    """Test Unity test generator"""
    print("\n" + "=" * 60)
    print("Testing Unity Templates")
    print("=" * 60)
    
    from dataclasses import dataclass
    
    @dataclass
    class CParam:
        name: str
        type: str
    
    @dataclass
    class CFunc:
        name: str
        return_type: str
        parameters: list
        file: str
        line: int
    
    funcs = [
        CFunc("calculate_damage", "int", [CParam("attack", "int"), CParam("defense", "int")], "battle.c", 10),
        CFunc("heal_pokemon", "void", [CParam("pokemon", "Pokemon*"), CParam("amount", "int")], "battle.c", 25),
    ]
    
    generator = UnityTestGenerator()
    test_code = generator.generate_test_file(funcs, "battle.h")
    
    print("✓ Generated Unity test file")
    print("=" * 40)
    print(test_code[:1000])
    print("...")
    print("=" * 40)
    
    # Test CMake integration
    cmake_integration = UnityCMakeTemplates.get_full_cmake_integration()
    print("✓ Generated CMake integration")
    print(cmake_integration[:500])
    print("...")
    
    return True


def test_security_rules():
    """Test security checker"""
    print("\n" + "=" * 60)
    print("Testing Security Rules")
    print("=" * 60)
    
    sample_code = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void unsafe_function(char *user_input) {
    char buffer[100];
    
    // Dangerous: strcpy without bounds checking
    strcpy(buffer, user_input);
    
    // Dangerous: format string vulnerability
    printf(user_input);
    
    // Dangerous: gets (removed in C11)
    gets(buffer);
    
    // Dangerous: system with user input
    system(user_input);
}

void memory_issues(void) {
    char *ptr = malloc(100);  // No NULL check!
    strcpy(ptr, "test");
    
    int result = strcmp("a", "b");  // Return value ignored
    
    char buf[10];
    scanf("%s", buf);  // No width limit!
}

void credentials(void) {
    const char *password = "super_secret_123";  // Hardcoded!
    const char *api_key = "AKIAIOSFODNN7EXAMPLE";  // AWS key!
}
'''
    
    with open('/tmp/test_security.c', 'w') as f:
        f.write(sample_code)
    
    checker = CSecurityChecker()
    issues = checker.check_file('/tmp/test_security.c', sample_code)
    
    print(f"✓ Found {len(issues)} security issues:")
    
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for issue in issues:
        severity_counts[issue.severity.value] += 1
    
    print(f"  Critical: {severity_counts['critical']}")
    print(f"  High: {severity_counts['high']}")
    print(f"  Medium: {severity_counts['medium']}")
    print(f"  Low: {severity_counts['low']}")
    
    print("\nTop issues:")
    for issue in issues[:10]:
        print(f"  Line {issue.line:3d} [{issue.severity.value.upper():8s}] {issue.cwe_id}: {issue.title}")
    
    return True


def main():
    """Run all tests"""
    print("C Support Library - Integration Test")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(("C Parser", test_c_parser()))
    except Exception as e:
        print(f"✗ C Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("C Parser", False))
    
    try:
        results.append(("CMake Parser", test_cmake_parser()))
    except Exception as e:
        print(f"✗ CMake Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("CMake Parser", False))
    
    try:
        results.append(("Unity Templates", test_unity_templates()))
    except Exception as e:
        print(f"✗ Unity Templates test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Unity Templates", False))
    
    try:
        results.append(("Security Rules", test_security_rules()))
    except Exception as e:
        print(f"✗ Security Rules test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Security Rules", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:10s} {name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
