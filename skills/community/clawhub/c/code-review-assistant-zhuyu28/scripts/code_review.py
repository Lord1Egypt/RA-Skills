#!/usr/bin/env python3
"""
Code Review Assistant - Automated code review tool
Analyzes code for common issues, style violations, and security concerns.
"""

import os
import sys
import json
import subprocess
from typing import List, Dict, Any

def analyze_code(file_path: str, language: str = None) -> Dict[str, Any]:
    """
    Analyze code file for issues and provide review feedback.
    
    Args:
        file_path: Path to the code file to analyze
        language: Programming language (auto-detected if not provided)
    
    Returns:
        Dictionary containing analysis results and suggestions
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    # Auto-detect language if not provided
    if language is None:
        ext = os.path.splitext(file_path)[1].lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php'
        }
        language = language_map.get(ext, 'unknown')
    
    results = {
        "file": file_path,
        "language": language,
        "issues": [],
        "suggestions": [],
        "summary": ""
    }
    
    # Basic analysis based on language
    if language == 'python':
        results = analyze_python_code(file_path)
    elif language == 'javascript':
        results = analyze_javascript_code(file_path)
    else:
        # Generic analysis for unknown languages
        results["issues"].append({
            "type": "info",
            "message": f"Generic analysis for {language} files",
            "severity": "low"
        })
    
    return results

def analyze_python_code(file_path: str) -> Dict[str, Any]:
    """Analyze Python code using basic checks."""
    results = {
        "file": file_path,
        "language": "python",
        "issues": [],
        "suggestions": [],
        "summary": ""
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Check for common Python issues
        line_count = len(lines)
        if line_count > 500:
            results["issues"].append({
                "type": "complexity",
                "message": "File is very long (>500 lines), consider splitting into smaller modules",
                "severity": "medium",
                "line": None
            })
        
        # Check for missing docstrings in functions
        in_function = False
        function_line = 0
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('def ') or stripped.startswith('class '):
                in_function = True
                function_line = i
                has_docstring = False
            elif in_function and stripped.startswith('"""') or stripped.startswith("'''"):
                has_docstring = True
            elif in_function and stripped and not stripped.startswith('#'):
                if not has_docstring:
                    results["issues"].append({
                        "type": "documentation",
                        "message": f"Function/Class at line {function_line} lacks docstring",
                        "severity": "low",
                        "line": function_line
                    })
                in_function = False
        
        # Check for print statements (debug code)
        for i, line in enumerate(lines, 1):
            if 'print(' in line and not line.strip().startswith('#'):
                results["issues"].append({
                    "type": "debug",
                    "message": f"Potential debug print statement at line {i}",
                    "severity": "low",
                    "line": i
                })
        
        results["summary"] = f"Analyzed {line_count} lines of Python code"
        
    except Exception as e:
        results["error"] = f"Error analyzing Python code: {str(e)}"
    
    return results

def analyze_javascript_code(file_path: str) -> Dict[str, Any]:
    """Analyze JavaScript code using basic checks."""
    results = {
        "file": file_path,
        "language": "javascript",
        "issues": [],
        "suggestions": [],
        "summary": ""
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        line_count = len(lines)
        
        # Check for console.log statements
        for i, line in enumerate(lines, 1):
            if 'console.log(' in line and not line.strip().startswith('//'):
                results["issues"].append({
                    "type": "debug",
                    "message": f"Potential debug console.log at line {i}",
                    "severity": "low",
                    "line": i
                })
        
        # Check for var usage (prefer let/const)
        for i, line in enumerate(lines, 1):
            if 'var ' in line and not line.strip().startswith('//'):
                results["issues"].append({
                    "type": "style",
                    "message": f"Using 'var' at line {i}, prefer 'let' or 'const'",
                    "severity": "low",
                    "line": i
                })
        
        results["summary"] = f"Analyzed {line_count} lines of JavaScript code"
        
    except Exception as e:
        results["error"] = f"Error analyzing JavaScript code: {str(e)}"
    
    return results

def main():
    """Main entry point for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python code_review.py <file_path> [language]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None
    
    results = analyze_code(file_path, language)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()