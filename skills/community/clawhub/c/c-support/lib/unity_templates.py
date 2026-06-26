"""
Unity Test Templates - Generate Unity testing framework code
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class CParameter:
    name: str
    type: str


@dataclass
class CFunction:
    name: str
    return_type: str
    parameters: List[CParameter]
    file: str
    line: int


class UnityTestGenerator:
    """
    Generate Unity test framework code for C functions
    """
    
    def __init__(self):
        self.header = '''/* Unity Test File - Auto Generated */
#include "unity.h"
#include <stdint.h>
#include <stdbool.h>

/* Setup and Teardown */
void setUp(void) {
    /* Called before each test */
}

void tearDown(void) {
    /* Called after each test */
}

'''
        
        self.footer = '''
/* Main entry point */
int main(void) {
    UNITY_BEGIN();
    {test_calls}
    return UNITY_END();
}
'''
    
    def generate_test_file(self, functions: List[CFunction], header_file: str) -> str:
        """Generate a complete Unity test file"""
        lines = [self.header]
        
        # Add include for the module under test
        lines.append(f'#include "{header_file}"')
        lines.append('')
        lines.append('/* Test cases */')
        lines.append('')
        
        test_calls = []
        
        for func in functions:
            test_cases = self._generate_test_cases(func)
            lines.extend(test_cases)
            lines.append('')
            
            # Add RUN_TEST calls for main()
            test_name = f"test_{func.name}_normal"
            test_calls.append(f'    RUN_TEST({test_name});')
        
        # Add footer
        footer = self.footer.replace('{test_calls}', '\n'.join(test_calls))
        lines.append(footer)
        
        return '\n'.join(lines)
    
    def _generate_test_cases(self, func: CFunction) -> List[str]:
        """Generate test cases for a single function"""
        lines = []
        
        # Normal case test
        lines.append(f'/* Test {func.name} - normal case */')
        lines.append(f'void test_{func.name}_normal(void) {{')
        lines.append(self._generate_test_body(func, 'normal'))
        lines.append('}')
        lines.append('')
        
        # Edge cases
        lines.append(f'/* Test {func.name} - edge cases */')
        lines.append(f'void test_{func.name}_edge_cases(void) {{')
        lines.append(self._generate_test_body(func, 'edge'))
        lines.append('}')
        
        # Error cases if applicable
        if self._can_have_error_cases(func):
            lines.append('')
            lines.append(f'/* Test {func.name} - error cases */')
            lines.append(f'void test_{func.name}_error_cases(void) {{')
            lines.append(self._generate_test_body(func, 'error'))
            lines.append('}')
        
        return lines
    
    def _generate_test_body(self, func: CFunction, case_type: str) -> str:
        """Generate the body of a test function"""
        lines = []
        
        # Generate variable declarations
        for param in func.parameters:
            lines.append(f'    {param.type} {param.name} = {self._get_sample_value(param.type, case_type)};')
        
        # Call the function
        if func.parameters:
            param_names = ', '.join(p.name for p in func.parameters)
            call = f'{func.name}({param_names})'
        else:
            call = f'{func.name}()'
        
        # Handle return value
        if func.return_type != 'void':
            lines.append(f'    {func.return_type} result = {call};')
            lines.append(f'    {self._generate_assertion(func.return_type, case_type)}')
        else:
            lines.append(f'    {call};')
            lines.append('    /* TODO: Add assertions for side effects */')
        
        return '\n'.join(lines)
    
    def _get_sample_value(self, type_str: str, case_type: str) -> str:
        """Generate a sample value for a type"""
        type_lower = type_str.lower()
        
        if case_type == 'normal':
            if 'int' in type_lower:
                if 'unsigned' in type_lower or 'uint' in type_lower:
                    return '42U'
                return '42'
            elif 'float' in type_lower:
                return '3.14f'
            elif 'double' in type_lower:
                return '3.14'
            elif 'bool' in type_lower:
                return 'true'
            elif 'char' in type_lower and '*' in type_lower:
                return '"test"'
            elif 'void' in type_lower and '*' in type_lower:
                return 'NULL'
            else:
                return '0'
        
        elif case_type == 'edge':
            if 'int' in type_lower:
                if 'unsigned' in type_lower or 'uint' in type_lower:
                    return '0U'
                return '0'
            elif 'float' in type_lower or 'double' in type_lower:
                return '0.0'
            elif 'bool' in type_lower:
                return 'false'
            elif 'char' in type_lower and '*' in type_lower:
                return '""'
            elif 'void' in type_lower and '*' in type_lower:
                return 'NULL'
            else:
                return '0'
        
        elif case_type == 'error':
            if 'int' in type_lower:
                if 'unsigned' in type_lower or 'uint' in type_lower:
                    return 'UINT32_MAX'
                return '-1'
            elif 'float' in type_lower or 'double' in type_lower:
                return '-1.0'
            elif 'char' in type_lower and '*' in type_lower:
                return 'NULL'
            elif 'void' in type_lower and '*' in type_lower:
                return 'NULL'
            else:
                return '-1'
        
        return '0'
    
    def _generate_assertion(self, return_type: str, case_type: str) -> str:
        """Generate an assertion based on return type"""
        type_lower = return_type.lower()
        
        if 'bool' in type_lower:
            return 'TEST_ASSERT_TRUE(result);'
        elif 'int' in type_lower or 'float' in type_lower or 'double' in type_lower:
            return 'TEST_ASSERT_EQUAL(/* TODO: expected value */, result);'
        elif 'void' in type_lower and '*' in type_lower:
            return 'TEST_ASSERT_NOT_NULL(result);'
        else:
            return '/* TODO: Add assertion for return value */'
    
    def _can_have_error_cases(self, func: CFunction) -> bool:
        """Check if function can have error cases"""
        # Functions returning pointers or ints often have error cases
        return_type = func.return_type.lower()
        return ('int' in return_type or 
                '*' in return_type or
                'bool' in return_type)
    
    def generate_cmake_integration(self, test_files: List[str]) -> str:
        """Generate CMakeLists.txt content for Unity tests"""
        content = '''# Unity Testing Framework
include(FetchContent)
FetchContent_Declare(
    unity
    GIT_REPOSITORY https://github.com/ThrowTheSwitch/Unity.git
    GIT_TAG v2.5.2
)
FetchContent_MakeAvailable(unity)

enable_testing()

# Helper function to add Unity tests
function(add_unity_test test_name test_file)
    add_executable(${test_name} ${test_file})
    target_link_libraries(${test_name} unity)
    target_include_directories(${test_name} PRIVATE 
        ${unity_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/src
    )
    add_test(NAME ${test_name} COMMAND ${test_name})
endfunction()

'''
        
        for test_file in test_files:
            test_name = test_file.replace('.c', '').replace('/', '_')
            content += f'add_unity_test({test_name} {test_file})\n'
        
        return content
    
    def generate_test_for_function(self, func: CFunction) -> str:
        """Generate a single test function"""
        lines = self._generate_test_cases(func)
        return '\n'.join(lines)
    
    def generate_mock_template(self, header_file: str, functions: List[CFunction]) -> str:
        """Generate a mock header for unit testing"""
        guard = header_file.upper().replace('.', '_').replace('/', '_')
        
        lines = [
            f'/* Mock header for {header_file} */',
            f'#ifndef {guard}_MOCK',
            f'#define {guard}_MOCK',
            '',
            '#include <stdbool.h>',
            '#include <stdint.h>',
            '',
            '/* Mock control structures */'
        ]
        
        for func in functions:
            func_upper = func.name.upper()
            lines.append(f'')
            lines.append(f'/* Mock for {func.name} */')
            lines.append(f'extern bool {func.name}_called;')
            
            if func.return_type != 'void':
                lines.append(f'extern {func.return_type} {func.name}_return_value;')
            
            for param in func.parameters:
                lines.append(f'extern {param.type} {func.name}_{param.name}_expected;')
        
        lines.append('')
        lines.append('#endif')
        
        return '\n'.join(lines)


class UnityCMakeTemplates:
    """Templates for CMake Unity integration"""
    
    FETCHCONTENT_TEMPLATE = '''
# Unity Testing Framework via FetchContent
include(FetchContent)
FetchContent_Declare(
    unity
    GIT_REPOSITORY https://github.com/ThrowTheSwitch/Unity.git
    GIT_TAG v2.5.2
)
FetchContent_MakeAvailable(unity)
'''
    
    ENABLE_TESTING = '''
# Enable CTest
enable_testing()
'''
    
    ADD_UNITY_TEST_FUNCTION = '''
# Helper function to add Unity tests
function(add_unity_test test_name test_source)
    add_executable(${test_name} ${test_source})
    target_link_libraries(${test_name} unity)
    target_include_directories(${test_name} PRIVATE 
        ${unity_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/include
    )
    add_test(NAME ${test_name} COMMAND ${test_name})
    
    # Add Valgrind memory check if available
    find_program(VALGRIND valgrind)
    if(VALGRIND)
        add_test(NAME ${test_name}_memcheck 
            COMMAND valgrind --leak-check=full --error-exitcode=1 $<TARGET_FILE:${test_name}>)
    endif()
endfunction()
'''
    
    COVERAGE_TEMPLATE = '''
# Coverage support
option(ENABLE_COVERAGE "Enable code coverage" OFF)
if(ENABLE_COVERAGE)
    if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
        add_compile_options(--coverage)
        add_link_options(--coverage)
    endif()
endif()
'''
    
    @classmethod
    def get_full_cmake_integration(cls) -> str:
        """Get complete CMake integration template"""
        return f'''{cls.FETCHCONTENT_TEMPLATE}
{cls.ENABLE_TESTING}
{cls.ADD_UNITY_TEST_FUNCTION}
{cls.COVERAGE_TEMPLATE}
'''


def generate_unity_main(test_functions: List[str]) -> str:
    """Generate Unity main.c file"""
    lines = [
        '/* Unity Test Runner - Auto Generated */',
        '#include "unity.h"',
        '',
        '/* External test functions */',
    ]
    
    for func in test_functions:
        lines.append(f'extern void {func}(void);')
    
    lines.extend([
        '',
        'void setUp(void) {}',
        'void tearDown(void) {}',
        '',
        'int main(void) {',
        '    UNITY_BEGIN();',
    ])
    
    for func in test_functions:
        lines.append(f'    RUN_TEST({func});')
    
    lines.extend([
        '    return UNITY_END();',
        '}',
    ])
    
    return '\n'.join(lines)


# Unity assertion reference
UNITY_ASSERTIONS = '''
/* Common Unity Assertions for C */

/* Integer assertions */
TEST_ASSERT_EQUAL(expected, actual);
TEST_ASSERT_NOT_EQUAL(unexpected, actual);
TEST_ASSERT_GREATER_THAN(threshold, actual);
TEST_ASSERT_LESS_THAN(threshold, actual);
TEST_ASSERT_GREATER_OR_EQUAL(threshold, actual);
TEST_ASSERT_LESS_OR_EQUAL(threshold, actual);
TEST_ASSERT_WITHIN(delta, expected, actual);

/* Pointer assertions */
TEST_ASSERT_NULL(pointer);
TEST_ASSERT_NOT_NULL(pointer);
TEST_ASSERT_EQUAL_PTR(expected, actual);

/* String assertions */
TEST_ASSERT_EQUAL_STRING(expected, actual);
TEST_ASSERT_EQUAL_STRING_LEN(expected, actual, len);

/* Memory assertions */
TEST_ASSERT_EQUAL_MEMORY(expected, actual, len);
TEST_ASSERT_BYTES_EQUAL(expected, actual);

/* Array assertions */
TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, num_elements);
TEST_ASSERT_EQUAL_PTR_ARRAY(expected, actual, num_elements);

/* Bit assertions */
TEST_ASSERT_BITS(mask, expected, actual);
TEST_ASSERT_BIT_HIGH(bit, actual);
TEST_ASSERT_BIT_LOW(bit, actual);

/* Boolean assertions */
TEST_ASSERT_TRUE(condition);
TEST_ASSERT_FALSE(condition);

/* Float assertions */
TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual);
TEST_ASSERT_DOUBLE_WITHIN(delta, expected, actual);
'''
