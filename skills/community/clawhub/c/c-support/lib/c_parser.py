"""
C Language Parser - AST Analysis for C code
Supports tree-sitter (primary) and pycparser (fallback)
"""

import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from pathlib import Path

# Try to import tree-sitter
try:
    from tree_sitter import Language, Parser
    import tree_sitter_c as tsp_c
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False

# Try to import pycparser as fallback
try:
    from pycparser import parse_file, c_parser, c_ast
    PYC_PARSER_AVAILABLE = True
except ImportError:
    PYC_PARSER_AVAILABLE = False


@dataclass
class CSymbol:
    """Represents a C symbol (function, variable, macro, etc.)"""
    name: str
    symbol_type: str  # function, variable, macro, struct, union, enum, typedef
    file: str
    line: int
    column: int = 0
    signature: Optional[str] = None  # For functions
    value: Optional[str] = None  # For macros/variables
    is_static: bool = False
    is_extern: bool = False


@dataclass
class CInclude:
    """Represents an #include directive"""
    path: str
    is_system: bool  # True for <header.h>, False for "header.h"
    line: int


@dataclass
class CType:
    """Represents a C type definition"""
    name: str
    kind: str  # struct, union, enum, typedef
    definition: str
    file: str
    line: int
    fields: List[Dict] = field(default_factory=list)


@dataclass
class CFunction:
    """Represents a C function"""
    name: str
    return_type: str
    parameters: List[Dict]
    file: str
    line: int
    is_static: bool = False
    is_inline: bool = False
    body_start: int = 0
    body_end: int = 0


@dataclass
class CFileInfo:
    """Complete information about a C source file"""
    path: str
    functions: List[CFunction] = field(default_factory=list)
    symbols: List[CSymbol] = field(default_factory=list)
    includes: List[CInclude] = field(default_factory=list)
    types: List[CType] = field(default_factory=list)
    macros: List[CSymbol] = field(default_factory=list)
    globals: List[CSymbol] = field(default_factory=list)


class CParser:
    """
    C Language Parser using tree-sitter or pycparser
    """
    
    DANGEROUS_FUNCTIONS = {
        'strcpy': 'Use strncpy or strlcpy instead',
        'strcat': 'Use strncat or strlcat instead',
        'sprintf': 'Use snprintf instead',
        'gets': 'Use fgets instead (gets is removed in C11)',
        'wcscpy': 'Use wcsncpy instead',
        'wcscat': 'Use wcsncat instead',
        'vsprintf': 'Use vsnprintf instead',
        'scanf': 'Use scanf with width limits or fgets + sscanf',
    }
    
    def __init__(self):
        self.parser = None
        self.language = None
        self._init_parser()
    
    def _init_parser(self):
        """Initialize the parser (tree-sitter preferred)"""
        if TREE_SITTER_AVAILABLE:
            try:
                self.language = Language(tsp_c.language())
                self.parser = Parser(self.language)
            except Exception as e:
                print(f"Tree-sitter init failed: {e}")
                self.parser = None
        
        if self.parser is None and PYC_PARSER_AVAILABLE:
            self.parser = c_parser.CParser()
    
    def parse_file(self, filepath: str) -> Optional[CFileInfo]:
        """Parse a C file and return structured information"""
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if TREE_SITTER_AVAILABLE and self.parser:
            return self._parse_with_tree_sitter(filepath, content)
        elif PYC_PARSER_AVAILABLE:
            return self._parse_with_pycparser(filepath, content)
        else:
            # Fallback: regex-based parsing
            return self._parse_with_regex(filepath, content)
    
    def _parse_with_tree_sitter(self, filepath: str, content: str) -> CFileInfo:
        """Parse using tree-sitter"""
        tree = self.parser.parse(content.encode('utf-8'))
        root = tree.root_node
        
        info = CFileInfo(path=filepath)
        
        # Walk the AST
        self._walk_tree_sitter_node(root, content, info, filepath)
        
        return info
    
    def _walk_tree_sitter_node(self, node, content: str, info: CFileInfo, filepath: str):
        """Recursively walk tree-sitter AST nodes"""
        node_type = node.type
        node_text = content[node.start_byte:node.end_byte]
        
        if node_type == 'function_definition':
            func = self._extract_function_tree_sitter(node, content, filepath)
            if func:
                info.functions.append(func)
                info.symbols.append(CSymbol(
                    name=func.name,
                    symbol_type='function',
                    file=filepath,
                    line=node.start_point[0] + 1,
                    signature=func.return_type
                ))
        
        elif node_type == 'preproc_include':
            include = self._extract_include_tree_sitter(node, content, filepath)
            if include:
                info.includes.append(include)
        
        elif node_type == 'preproc_def':
            macro = self._extract_macro_tree_sitter(node, content, filepath)
            if macro:
                info.macros.append(macro)
                info.symbols.append(macro)
        
        elif node_type in ('struct_specifier', 'union_specifier', 'enum_specifier'):
            type_def = self._extract_type_tree_sitter(node, content, filepath)
            if type_def:
                info.types.append(type_def)
        
        # Recurse into children
        for child in node.children:
            self._walk_tree_sitter_node(child, content, info, filepath)
    
    def _extract_function_tree_sitter(self, node, content: str, filepath: str) -> Optional[CFunction]:
        """Extract function info from tree-sitter node"""
        func_name = None
        return_type = "void"
        params = []
        is_static = False
        is_inline = False
        
        for child in node.children:
            if child.type == 'storage_class_specifier':
                specifier = content[child.start_byte:child.end_byte]
                if 'static' in specifier:
                    is_static = True
                if 'inline' in specifier:
                    is_inline = True
            
            elif child.type == 'function_declarator':
                # Extract function name and parameters
                for subchild in child.children:
                    if subchild.type == 'identifier':
                        func_name = content[subchild.start_byte:subchild.end_byte]
                    elif subchild.type == 'parameter_list':
                        params = self._extract_params_tree_sitter(subchild, content)
            
            elif child.type in ('primitive_type', 'type_identifier'):
                return_type = content[child.start_byte:child.end_byte]
        
        if func_name:
            return CFunction(
                name=func_name,
                return_type=return_type,
                parameters=params,
                file=filepath,
                line=node.start_point[0] + 1,
                is_static=is_static,
                is_inline=is_inline,
                body_start=node.start_point[0] + 1,
                body_end=node.end_point[0] + 1
            )
        return None
    
    def _extract_params_tree_sitter(self, node, content: str) -> List[Dict]:
        """Extract parameter list from tree-sitter"""
        params = []
        for child in node.children:
            if child.type == 'parameter_declaration':
                param_text = content[child.start_byte:child.end_byte]
                params.append({'declaration': param_text})
        return params
    
    def _extract_include_tree_sitter(self, node, content: str, filepath: str) -> Optional[CInclude]:
        """Extract #include directive"""
        for child in node.children:
            if child.type == 'string_literal' or child.type == 'system_lib_string':
                include_text = content[child.start_byte:child.end_byte]
                is_system = child.type == 'system_lib_string' or include_text.startswith('<')
                # Clean up quotes
                path = include_text.strip('"<>')
                return CInclude(path=path, is_system=is_system, line=node.start_point[0] + 1)
        return None
    
    def _extract_macro_tree_sitter(self, node, content: str, filepath: str) -> Optional[CSymbol]:
        """Extract #define macro"""
        lines = content[node.start_byte:node.end_byte].split('\n', 1)
        first_line = lines[0]
        
        # Parse #define NAME value
        match = re.match(r'#define\s+(\w+)\s+(.*)', first_line)
        if match:
            name = match.group(1)
            value = match.group(2).strip()
            return CSymbol(
                name=name,
                symbol_type='macro',
                file=filepath,
                line=node.start_point[0] + 1,
                value=value
            )
        return None
    
    def _extract_type_tree_sitter(self, node, content: str, filepath: str) -> Optional[CType]:
        """Extract struct/union/enum definition"""
        kind = node.type.replace('_specifier', '')
        definition = content[node.start_byte:node.end_byte]
        
        # Try to extract name
        name = None
        for child in node.children:
            if child.type == 'type_identifier' or child.type == 'identifier':
                name = content[child.start_byte:child.end_byte]
        
        if name:
            return CType(
                name=name,
                kind=kind,
                definition=definition[:100] + '...' if len(definition) > 100 else definition,
                file=filepath,
                line=node.start_point[0] + 1
            )
        return None
    
    def _parse_with_pycparser(self, filepath: str, content: str) -> CFileInfo:
        """Fallback: parse using pycparser"""
        info = CFileInfo(path=filepath)
        
        # pycparser requires preprocessed input, so we use regex fallback for now
        return self._parse_with_regex(filepath, content)
    
    def _parse_with_regex(self, filepath: str, content: str) -> CFileInfo:
        """Fallback: regex-based parsing (less accurate but always works)"""
        info = CFileInfo(path=filepath)
        lines = content.split('\n')
        
        # Pattern for function definitions
        func_pattern = re.compile(
            r'(\bstatic\s+)?(\binline\s+)?(\w+)\s+(\w+)\s*\(([^)]*)\)\s*\{',
            re.MULTILINE
        )
        
        # Pattern for includes
        include_pattern = re.compile(r'#include\s+([<"])([^>"]+)[>"]')
        
        # Pattern for macros
        macro_pattern = re.compile(r'#define\s+(\w+)(?:\s+(.*))?')
        
        # Pattern for struct/enum/union
        struct_pattern = re.compile(r'(struct|union|enum)\s+(\w+)')
        
        for i, line in enumerate(lines, 1):
            # Match includes
            include_match = include_pattern.search(line)
            if include_match:
                is_system = include_match.group(1) == '<'
                path = include_match.group(2)
                info.includes.append(CInclude(path=path, is_system=is_system, line=i))
            
            # Match macros
            macro_match = macro_pattern.search(line)
            if macro_match:
                name = macro_match.group(1)
                value = macro_match.group(2) or ''
                macro = CSymbol(name=name, symbol_type='macro', file=filepath, line=i, value=value.strip())
                info.macros.append(macro)
                info.symbols.append(macro)
            
            # Match struct/enum/union
            struct_match = struct_pattern.search(line)
            if struct_match:
                kind = struct_match.group(1)
                name = struct_match.group(2)
                type_def = CType(name=name, kind=kind, definition='', file=filepath, line=i)
                info.types.append(type_def)
        
        # Match functions (multiline)
        for match in func_pattern.finditer(content):
            is_static = bool(match.group(1))
            is_inline = bool(match.group(2))
            return_type = match.group(3)
            name = match.group(4)
            params = match.group(5)
            
            # Calculate line number
            line_num = content[:match.start()].count('\n') + 1
            
            func = CFunction(
                name=name,
                return_type=return_type,
                parameters=[{'declaration': p.strip()} for p in params.split(',') if p.strip()],
                file=filepath,
                line=line_num,
                is_static=is_static,
                is_inline=is_inline
            )
            info.functions.append(func)
            info.symbols.append(CSymbol(
                name=name,
                symbol_type='function',
                file=filepath,
                line=line_num,
                signature=return_type
            ))
        
        return info
    
    def find_dangerous_calls(self, filepath: str) -> List[Dict]:
        """Find dangerous function calls in a C file"""
        if not os.path.exists(filepath):
            return []
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for func, advice in self.DANGEROUS_FUNCTIONS.items():
                # Match function calls (not declarations)
                pattern = rf'\b{func}\s*\('
                if re.search(pattern, line):
                    # Check if it's not a comment
                    comment_pos = line.find('//')
                    if comment_pos == -1 or line.find(func) < comment_pos:
                        issues.append({
                            'line': i,
                            'function': func,
                            'code': line.strip(),
                            'advice': advice,
                            'severity': 'critical'
                        })
        
        return issues
    
    def extract_function_bodies(self, filepath: str) -> Dict[str, str]:
        """Extract function bodies for analysis"""
        if not os.path.exists(filepath):
            return {}
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        functions = {}
        
        # Simple regex to find functions and their bodies
        # This is a simplified version - full brace matching is complex
        func_pattern = re.compile(
            r'((?:\bstatic\s+)?(?:\binline\s+)?(?:\w+)\s+(\w+)\s*\([^)]*\)\s*\{)',
            re.MULTILINE
        )
        
        for match in func_pattern.finditer(content):
            start = match.end() - 1  # Position of opening brace
            name = match.group(2)
            
            # Find matching closing brace
            brace_count = 1
            pos = start + 1
            while brace_count > 0 and pos < len(content):
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            if brace_count == 0:
                body = content[start:pos]
                functions[name] = body
        
        return functions


def analyze_project(project_path: str) -> Dict[str, CFileInfo]:
    """Analyze all C files in a project"""
    parser = CParser()
    results = {}
    
    project_path = Path(project_path)
    
    # Find all C files
    for ext in ['*.c', '*.h']:
        for filepath in project_path.rglob(ext):
            try:
                info = parser.parse_file(str(filepath))
                if info:
                    results[str(filepath.relative_to(project_path))] = info
            except Exception as e:
                print(f"Error parsing {filepath}: {e}")
    
    return results


def get_project_summary(project_path: str) -> Dict:
    """Get a summary of the C project"""
    results = analyze_project(project_path)
    
    summary = {
        'total_files': len(results),
        'total_functions': sum(len(f.functions) for f in results.values()),
        'total_macros': sum(len(f.macros) for f in results.values()),
        'total_types': sum(len(f.types) for f in results.values()),
        'system_includes': set(),
        'local_includes': set(),
        'files': list(results.keys())
    }
    
    for info in results.values():
        for inc in info.includes:
            if inc.is_system:
                summary['system_includes'].add(inc.path)
            else:
                summary['local_includes'].add(inc.path)
    
    # Convert sets to sorted lists
    summary['system_includes'] = sorted(summary['system_includes'])
    summary['local_includes'] = sorted(summary['local_includes'])
    
    return summary


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python c_parser.py <c-file-or-project>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        parser = CParser()
        info = parser.parse_file(path)
        if info:
            print(f"File: {info.path}")
            print(f"Functions: {len(info.functions)}")
            for func in info.functions:
                print(f"  - {func.return_type} {func.name}() at line {func.line}")
            print(f"\nIncludes: {len(info.includes)}")
            for inc in info.includes:
                print(f"  - {'<' if inc.is_system else '"'}{inc.path}{'>' if inc.is_system else '"'}")
            print(f"\nMacros: {len(info.macros)}")
            for macro in info.macros:
                print(f"  - #define {macro.name} {macro.value or ''}")
    else:
        summary = get_project_summary(path)
        print(json.dumps(summary, indent=2))
