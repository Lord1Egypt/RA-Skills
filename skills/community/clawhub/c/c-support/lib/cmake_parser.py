"""
CMake Parser - Parse CMakeLists.txt and extract build information
"""

import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from pathlib import Path


@dataclass
class CMakeTarget:
    """Represents a CMake build target"""
    name: str
    target_type: str  # executable, library, custom
    sources: List[str] = field(default_factory=list)
    include_dirs: List[str] = field(default_factory=list)
    link_libraries: List[str] = field(default_factory=list)
    compile_definitions: List[str] = field(default_factory=list)
    compile_options: List[str] = field(default_factory=list)
    link_options: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Other targets


@dataclass
class CMakeTest:
    """Represents a CTest test definition"""
    name: str
    command: str
    args: List[str] = field(default_factory=list)
    working_dir: Optional[str] = None
    env_vars: Dict[str, str] = field(default_factory=dict)


@dataclass
class CMakeProject:
    """Complete CMake project information"""
    name: str
    version: Optional[str] = None
    languages: List[str] = field(default_factory=list)
    targets: List[CMakeTarget] = field(default_factory=list)
    tests: List[CMakeTest] = field(default_factory=list)
    subdirectories: List[str] = field(default_factory=list)
    include_dirs: List[str] = field(default_factory=list)  # Global includes
    link_directories: List[str] = field(default_factory=list)
    compile_options: List[str] = field(default_factory=list)
    definitions: List[str] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)


class CMakeParser:
    """
    Parse CMakeLists.txt files and extract build information
    """
    
    def __init__(self):
        self.variables = {}
        self.targets = []
        self.tests = []
        self.includes = []
        self.link_dirs = []
    
    def parse_file(self, filepath: str) -> Optional[CMakeProject]:
        """Parse a CMakeLists.txt file"""
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return self.parse_content(content, filepath)
    
    def parse_content(self, content: str, filepath: str = "CMakeLists.txt") -> CMakeProject:
        """Parse CMake content from string"""
        project = CMakeProject(name="", variables={})
        
        # Remove comments
        content = self._remove_comments(content)
        
        # Extract project name
        project.name = self._extract_project_name(content) or "unnamed"
        project.version = self._extract_project_version(content)
        project.languages = self._extract_languages(content) or ["C"]
        
        # Extract variables
        project.variables = self._extract_variables(content)
        self.variables.update(project.variables)
        
        # Extract include directories
        project.include_dirs = self._extract_include_directories(content)
        
        # Extract link directories
        project.link_directories = self._extract_link_directories(content)
        
        # Extract compile options
        project.compile_options = self._extract_compile_options(content)
        
        # Extract definitions
        project.definitions = self._extract_compile_definitions(content)
        
        # Extract targets
        project.targets = self._extract_targets(content, filepath)
        
        # Extract tests
        project.tests = self._extract_tests(content)
        
        # Extract subdirectories
        project.subdirectories = self._extract_subdirectories(content)
        
        return project
    
    def _remove_comments(self, content: str) -> str:
        """Remove CMake comments"""
        lines = []
        for line in content.split('\n'):
            # Remove inline comments
            comment_pos = line.find('#')
            if comment_pos >= 0:
                line = line[:comment_pos]
            lines.append(line)
        return '\n'.join(lines)
    
    def _extract_project_name(self, content: str) -> Optional[str]:
        """Extract project name from CMakeLists.txt"""
        # Match: project(MyProject) or project(MyProject VERSION 1.0 LANGUAGES C)
        match = re.search(
            r'project\s*\(\s*(\w+)',
            content,
            re.IGNORECASE
        )
        return match.group(1) if match else None
    
    def _extract_project_version(self, content: str) -> Optional[str]:
        """Extract project version"""
        match = re.search(
            r'project\s*\([^)]*VERSION\s+([\d.]+)',
            content,
            re.IGNORECASE
        )
        return match.group(1) if match else None
    
    def _extract_languages(self, content: str) -> Optional[List[str]]:
        """Extract project languages"""
        match = re.search(
            r'project\s*\([^)]*LANGUAGES\s+([^)]+)',
            content,
            re.IGNORECASE
        )
        if match:
            return [lang.strip() for lang in match.group(1).split()]
        return None
    
    def _extract_variables(self, content: str) -> Dict[str, str]:
        """Extract set() variables"""
        variables = {}
        
        # Match: set(VAR value) or set(VAR "value")
        for match in re.finditer(
            r'set\s*\(\s*(\w+)\s+([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            var_name = match.group(1)
            var_value = match.group(2).strip()
            # Remove quotes
            var_value = var_value.strip('"')
            # Handle CACHE and other options
            var_value = re.sub(r'\s+CACHE\s+.*$', '', var_value, flags=re.IGNORECASE)
            var_value = re.sub(r'\s+FORCE\s*$', '', var_value, flags=re.IGNORECASE)
            variables[var_name] = var_value
        
        return variables
    
    def _extract_include_directories(self, content: str) -> List[str]:
        """Extract include directories"""
        includes = []
        
        # Match: include_directories(dir1 dir2) or include_directories(${VAR})
        for match in re.finditer(
            r'include_directories\s*\(([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            dirs = match.group(1)
            # Handle both space-separated and multiple calls
            for d in dirs.split():
                d = d.strip()
                if d:
                    # Expand variables
                    d = self._expand_variable(d)
                    includes.append(d)
        
        # Also match target_include_directories
        for match in re.finditer(
            r'target_include_directories\s*\(\s*(\w+)\s+(PUBLIC|PRIVATE|INTERFACE)\s+([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            dirs = match.group(3)
            for d in dirs.split():
                d = d.strip()
                if d:
                    d = self._expand_variable(d)
                    includes.append(d)
        
        return list(set(includes))  # Remove duplicates
    
    def _extract_link_directories(self, content: str) -> List[str]:
        """Extract link directories"""
        dirs = []
        
        for match in re.finditer(
            r'link_directories\s*\(([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            for d in match.group(1).split():
                d = d.strip()
                if d:
                    d = self._expand_variable(d)
                    dirs.append(d)
        
        return dirs
    
    def _extract_compile_options(self, content: str) -> List[str]:
        """Extract compile options"""
        options = []
        
        # Match: add_compile_options(-Wall -Wextra)
        for match in re.finditer(
            r'add_compile_options\s*\(([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            opts = match.group(1).split()
            options.extend(opts)
        
        # Match: target_compile_options(target PRIVATE ...)
        for match in re.finditer(
            r'target_compile_options\s*\(\s*\w+\s+(?:PUBLIC|PRIVATE|INTERFACE)\s+([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            opts = match.group(1).split()
            options.extend(opts)
        
        # Match: set(CMAKE_C_FLAGS "...")
        flags_match = re.search(
            r'set\s*\(\s*CMAKE_C_FLAGS\s+"([^"]+)"',
            content,
            re.IGNORECASE
        )
        if flags_match:
            options.extend(flags_match.group(1).split())
        
        return options
    
    def _extract_compile_definitions(self, content: str) -> List[str]:
        """Extract compile definitions"""
        definitions = []
        
        # Match: add_definitions(-DDEBUG) or add_compile_definitions(DEBUG)
        for match in re.finditer(
            r'add_definitions\s*\(([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            defs = match.group(1).split()
            definitions.extend(defs)
        
        for match in re.finditer(
            r'add_compile_definitions\s*\(([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            defs = match.group(1).split()
            definitions.extend(f"-D{d}" for d in defs)
        
        return definitions
    
    def _extract_targets(self, content: str, filepath: str) -> List[CMakeTarget]:
        """Extract build targets"""
        targets = []
        base_dir = os.path.dirname(filepath) or "."
        
        # Match: add_executable(name source1 source2 ...)
        for match in re.finditer(
            r'add_executable\s*\(\s*(\w+)\s+([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            name = match.group(1)
            sources = match.group(2).split()
            sources = [self._expand_variable(s) for s in sources]
            
            target = CMakeTarget(
                name=name,
                target_type='executable',
                sources=sources
            )
            
            # Look for target-specific properties
            target.include_dirs = self._extract_target_includes(content, name)
            target.link_libraries = self._extract_target_link_libs(content, name)
            target.compile_definitions = self._extract_target_definitions(content, name)
            target.compile_options = self._extract_target_options(content, name)
            
            targets.append(target)
        
        # Match: add_library(name [STATIC|SHARED|MODULE] source1 ...)
        for match in re.finditer(
            r'add_library\s*\(\s*(\w+)(?:\s+(STATIC|SHARED|MODULE))?\s+([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            name = match.group(1)
            lib_type = match.group(2) or 'STATIC'
            sources = match.group(3).split()
            sources = [self._expand_variable(s) for s in sources]
            
            target = CMakeTarget(
                name=name,
                target_type=f'library_{lib_type.lower()}',
                sources=sources
            )
            
            target.include_dirs = self._extract_target_includes(content, name)
            target.link_libraries = self._extract_target_link_libs(content, name)
            target.compile_definitions = self._extract_target_definitions(content, name)
            target.compile_options = self._extract_target_options(content, name)
            
            targets.append(target)
        
        return targets
    
    def _extract_target_includes(self, content: str, target_name: str) -> List[str]:
        """Extract include directories for a specific target"""
        includes = []
        
        pattern = rf'target_include_directories\s*\(\s*{target_name}\s+(?:PUBLIC|PRIVATE|INTERFACE)\s+([^)]+)\)'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            for d in match.group(1).split():
                d = d.strip()
                if d:
                    d = self._expand_variable(d)
                    includes.append(d)
        
        return includes
    
    def _extract_target_link_libs(self, content: str, target_name: str) -> List[str]:
        """Extract link libraries for a specific target"""
        libs = []
        
        # target_link_libraries
        pattern = rf'target_link_libraries\s*\(\s*{target_name}\s+([^)]+)\)'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            for lib in match.group(1).split():
                lib = lib.strip()
                if lib and lib.upper() not in ['PUBLIC', 'PRIVATE', 'INTERFACE']:
                    lib = self._expand_variable(lib)
                    libs.append(lib)
        
        # link_libraries (global)
        for match in re.finditer(
            r'link_libraries\s*\(([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            for lib in match.group(1).split():
                lib = lib.strip()
                if lib:
                    lib = self._expand_variable(lib)
                    libs.append(lib)
        
        return libs
    
    def _extract_target_definitions(self, content: str, target_name: str) -> List[str]:
        """Extract compile definitions for a specific target"""
        definitions = []
        
        pattern = rf'target_compile_definitions\s*\(\s*{target_name}\s+(?:PUBLIC|PRIVATE|INTERFACE)\s+([^)]+)\)'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            for d in match.group(1).split():
                d = d.strip()
                if d:
                    definitions.append(d)
        
        return definitions
    
    def _extract_target_options(self, content: str, target_name: str) -> List[str]:
        """Extract compile options for a specific target"""
        options = []
        
        pattern = rf'target_compile_options\s*\(\s*{target_name}\s+(?:PUBLIC|PRIVATE|INTERFACE)\s+([^)]+)\)'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            for opt in match.group(1).split():
                opt = opt.strip()
                if opt:
                    options.append(opt)
        
        return options
    
    def _extract_tests(self, content: str) -> List[CMakeTest]:
        """Extract CTest test definitions"""
        tests = []
        
        # Match: add_test(NAME test_name COMMAND command args...)
        for match in re.finditer(
            r'add_test\s*\(\s*NAME\s+(\w+)\s+COMMAND\s+([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            name = match.group(1)
            command_parts = match.group(2).split()
            if command_parts:
                command = command_parts[0]
                args = command_parts[1:]
                tests.append(CMakeTest(name=name, command=command, args=args))
        
        # Alternative syntax: add_test(test_name command)
        for match in re.finditer(
            r'add_test\s*\(\s*(\w+)\s+([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            name = match.group(1)
            command_parts = match.group(2).split()
            if command_parts:
                command = command_parts[0]
                args = command_parts[1:]
                tests.append(CMakeTest(name=name, command=command, args=args))
        
        return tests
    
    def _extract_subdirectories(self, content: str) -> List[str]:
        """Extract add_subdirectory calls"""
        dirs = []
        
        for match in re.finditer(
            r'add_subdirectory\s*\(\s*([^)]+)\)',
            content,
            re.IGNORECASE
        ):
            dir_str = match.group(1).strip()
            # Handle optional binary_dir parameter
            dir_name = dir_str.split()[0]
            dir_name = self._expand_variable(dir_name)
            dirs.append(dir_name)
        
        return dirs
    
    def _expand_variable(self, value: str) -> str:
        """Expand ${VAR} and $ENV{VAR} syntax"""
        # Simple variable expansion
        def replace_var(match):
            var_name = match.group(1)
            return self.variables.get(var_name, match.group(0))
        
        value = re.sub(r'\$\{(\w+)\}', replace_var, value)
        return value
    
    def is_unity_project(self, content: str) -> bool:
        """Check if project uses Unity testing framework"""
        unity_indicators = [
            r'unity',
            r'Unity\.h',
            r'UNITY_',
            r'add_unity_test',
        ]
        
        content_lower = content.lower()
        for indicator in unity_indicators:
            if re.search(indicator, content_lower):
                return True
        
        return False
    
    def suggest_unity_integration(self, project: CMakeProject) -> str:
        """Generate CMake code for Unity integration"""
        template = '''
# Unity Testing Framework Integration
include(FetchContent)
FetchContent_Declare(
    unity
    GIT_REPOSITORY https://github.com/ThrowTheSwitch/Unity.git
    GIT_TAG v2.5.2
)
FetchContent_MakeAvailable(unity)

# Enable testing
enable_testing()

# Function to add Unity tests
function(add_unity_test test_name test_source)
    add_executable(${test_name} ${test_source})
    target_link_libraries(${test_name} unity)
    target_include_directories(${test_name} PRIVATE ${unity_SOURCE_DIR}/src)
    add_test(NAME ${test_name} COMMAND ${test_name})
endfunction()

# Example usage:
# add_unity_test(test_mymodule tests/test_mymodule.c)
'''
        return template


def find_cmake_projects(project_path: str) -> List[str]:
    """Find all CMakeLists.txt files in a project"""
    cmake_files = []
    project_path = Path(project_path)
    
    for cmake_file in project_path.rglob("CMakeLists.txt"):
        cmake_files.append(str(cmake_file))
    
    return cmake_files


def analyze_cmake_project(project_path: str) -> Optional[CMakeProject]:
    """Analyze the main CMake project"""
    main_cmake = os.path.join(project_path, "CMakeLists.txt")
    
    if not os.path.exists(main_cmake):
        return None
    
    parser = CMakeParser()
    return parser.parse_file(main_cmake)


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python cmake_parser.py <cmake-project-path>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        parser = CMakeParser()
        project = parser.parse_file(path)
    else:
        project = analyze_cmake_project(path)
    
    if project:
        print(f"Project: {project.name}")
        print(f"Version: {project.version or 'not specified'}")
        print(f"Languages: {', '.join(project.languages)}")
        print(f"\nTargets:")
        for target in project.targets:
            print(f"  - {target.name} ({target.target_type})")
            print(f"    Sources: {', '.join(target.sources[:5])}{'...' if len(target.sources) > 5 else ''}")
            if target.link_libraries:
                print(f"    Links: {', '.join(target.link_libraries)}")
        print(f"\nTests: {len(project.tests)}")
        for test in project.tests:
            print(f"  - {test.name}: {test.command} {' '.join(test.args)}")
        print(f"\nInclude Dirs: {project.include_dirs}")
    else:
        print("No CMakeLists.txt found")
