"""Style checker and linter integration for code review."""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .logger import setup_logger, log_style_issue

logger = setup_logger(__name__)


@dataclass
class StyleIssue:
    """Code style issue found."""

    severity: str  # error, warning, info
    category: str  # PEP8, naming, complexity, etc.
    description: str
    line_number: int
    filename: str
    code_snippet: str
    suggestion: str


class StyleChecker:
    """Code style checker using static analysis."""

    def __init__(self):
        self.issues: List[StyleIssue] = []
        logger.debug("Style checker initialized")

    def check_diff(self, diff_content: str, repo_name: str) -> List[StyleIssue]:
        """Check diff content for style issues.

        Args:
            diff_content: Diff content from PR
            repo_name: Repository name for context

        Returns:
            List of style issues found
        """
        logger.debug(f"Checking diff for style issues in {repo_name} ({len(diff_content)} chars)")
        self.issues = []

        try:
            self._check_line_length(diff_content)
            self._check_naming_conventions(diff_content)
            self._check_import_order(diff_content)
            self._check_blank_lines(diff_content)
            self._check_whitespace(diff_content)
            self._check_docstrings(diff_content)

            # Log each style issue
            for issue in self.issues:
                log_style_issue(logger, issue.severity, issue.category, issue.filename, issue.line_number)

            logger.info(f"Style check complete: {len(self.issues)} issues found")
            return self.issues

        except Exception as e:
            logger.error(f"Error during style check: {e}")
            # Return any issues found before the error
            return self.issues

    def _check_line_length(self, diff_content: str):
        """Check for lines that are too long (PEP8: 79 characters)."""
        lines = diff_content.split('\n')

        for i, line in enumerate(lines, 1):
            # Skip diff headers and metadata
            if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
                continue

            # Check actual code lines (start with +)
            if line.startswith('+') and not line.startswith('++'):
                code_line = line[1:]  # Remove + prefix
                if len(code_line) > 88:  # PEP8 recommends 79, but 88 is more practical
                    self.issues.append(StyleIssue(
                        severity='warning',
                        category='Line Length',
                        description=f'Line too long ({len(code_line)} > 88 characters)',
                        line_number=i,
                        filename='unknown',
                        code_snippet=code_line[:100] + '...',
                        suggestion='Break the line or use parentheses for implicit line continuation'
                    ))

    def _check_naming_conventions(self, diff_content: str):
        """Check for PEP8 naming convention violations."""
        lines = diff_content.split('\n')

        for i, line in enumerate(lines, 1):
            if not line.startswith('+') or line.startswith('++'):
                continue

            code_line = line[1:].strip()

            # Check class names (should be CapWords)
            class_match = re.search(r'class\s+([a-z][a-z0-9_]*)\s*:', code_line)
            if class_match:
                class_name = class_match.group(1)
                self.issues.append(StyleIssue(
                    severity='error',
                    category='Naming Convention',
                    description=f'Class name should use CapWords convention: {class_name}',
                    line_number=i,
                    filename='unknown',
                    code_snippet=class_match.group(0),
                    suggestion=f'Rename to {class_name.title().replace("_", "")}'
                ))

            # Check function names (should be lowercase_with_underscores)
            func_match = re.search(r'def\s+([A-Z][a-zA-Z0-9_]*)\s*\(', code_line)
            if func_match:
                func_name = func_match.group(1)
                self.issues.append(StyleIssue(
                    severity='error',
                    category='Naming Convention',
                    description=f'Function name should use lowercase_with_underscores: {func_name}',
                    line_number=i,
                    filename='unknown',
                    code_snippet=func_match.group(0),
                    suggestion=f'Rename to {re.sub(r"(?<!^)(?=[A-Z])", "_", func_name).lower()}'
                ))

            # Check variable names (should be lowercase_with_underscores)
            var_match = re.search(r'([A-Z][a-zA-Z0-9_]*)\s*=', code_line)
            if var_match:
                var_name = var_match.group(1)
                # Exclude class names (CamelCase starting with uppercase)
                if var_name[0].isupper() and '_' in var_name:
                    self.issues.append(StyleIssue(
                        severity='warning',
                        category='Naming Convention',
                        description=f'Variable name should use lowercase_with_underscores: {var_name}',
                        line_number=i,
                        filename='unknown',
                        code_snippet=var_match.group(0),
                        suggestion=f'Rename to {var_name.lower()}'
                    ))

    def _check_import_order(self, diff_content: str):
        """Check for proper import order (PEP8: stdlib, third-party, local)."""
        lines = diff_content.split('\n')

        import_lines = []
        for i, line in enumerate(lines, 1):
            if line.startswith('+import ') or line.startswith('+from '):
                import_lines.append((i, line[1:].strip()))

        if len(import_lines) < 2:
            return  # Not enough imports to check

        # Very basic check: imports should be grouped
        current_group = None
        for line_num, import_line in import_lines:
            if import_line.startswith('from .') or import_line.startswith('from ..'):
                group = 'local'
            elif import_line.startswith('from ') or import_line.startswith('import '):
                # Try to determine if it's stdlib
                module = import_line.replace('from ', '').replace('import ', '').split()[0]
                module = module.split('.')[0]
                stdlib_modules = {'os', 'sys', 'json', 're', 'typing', 'dataclasses', 'pathlib'}
                if module in stdlib_modules:
                    group = 'stdlib'
                else:
                    group = 'third_party'
            else:
                continue

            if current_group and group != current_group:
                self.issues.append(StyleIssue(
                    severity='info',
                    category='Import Order',
                    description=f'Import groups not properly ordered ({current_group} -> {group})',
                    line_number=line_num,
                    filename='unknown',
                    code_snippet=import_line,
                    suggestion='Group imports: stdlib, third-party, then local imports'
                ))

            current_group = group

    def _check_blank_lines(self, diff_content: str):
        """Check for proper blank line usage."""
        lines = diff_content.split('\n')

        for i in range(len(lines)):
            line = lines[i]
            if not line.startswith('+') or line.startswith('++'):
                continue

            code_line = line[1:].strip()

            # Check for multiple blank lines before a function definition
            if code_line.startswith('def ') or code_line.startswith('class '):
                # Count consecutive blank lines before this definition
                blank_count = 0
                j = i - 1
                while j >= 0:
                    prev_line = lines[j]
                    # Check for lines starting with + (in diff) or empty lines
                    if prev_line.startswith('+'):
                        content = prev_line[1:].strip()
                        if content == '':
                            blank_count += 1
                        elif content:  # Non-empty line, stop counting
                            break
                    elif prev_line.strip() == '':  # Empty line (not part of diff)
                        blank_count += 1
                    else:  # Non-diff line, stop counting
                        break
                    j -= 1

                if blank_count >= 2:
                    self.issues.append(StyleIssue(
                        severity='warning',
                        category='Blank Lines',
                        description=f'Multiple blank lines ({blank_count}) before definition',
                        line_number=i,
                        filename='unknown',
                        code_snippet=code_line[:50],
                        suggestion='Use exactly 2 blank lines before top-level definitions'
                    ))

    def _check_whitespace(self, diff_content: str):
        """Check for whitespace issues."""
        lines = diff_content.split('\n')

        for i, line in enumerate(lines, 1):
            if not line.startswith('+') or line.startswith('++'):
                continue

            code_line = line[1:]

            # Trailing whitespace
            if code_line.rstrip() != code_line.rstrip('\n').rstrip('\r'):
                self.issues.append(StyleIssue(
                    severity='warning',
                    category='Whitespace',
                    description='Trailing whitespace detected',
                    line_number=i,
                    filename='unknown',
                    code_snippet=code_line[:80] + '...',
                    suggestion='Remove trailing whitespace'
                ))

            # Check for inconsistent indentation (spaces mixed with tabs)
            if '\t' in code_line and code_line.lstrip()[0:1] == ' ':
                self.issues.append(StyleIssue(
                    severity='warning',
                    category='Whitespace',
                    description='Mixed tabs and spaces in indentation',
                    line_number=i,
                    filename='unknown',
                    code_snippet=code_line[:80],
                    suggestion='Use consistent indentation (4 spaces or 1 tab)'
                ))

    def _check_docstrings(self, diff_content: str):
        """Check for missing docstrings in functions and classes."""
        lines = diff_content.split('\n')

        for i, line in enumerate(lines, 1):
            if not line.startswith('+') or line.startswith('++'):
                continue

            code_line = line[1:]

            # Check for function/class definitions
            func_match = re.search(r'def\s+\w+\s*\(', code_line)
            class_match = re.search(r'class\s+\w+\s*:', code_line)

            if func_match or class_match:
                # Check if next few lines have a docstring
                has_docstring = False
                for j in range(i, min(i + 5, len(lines))):
                    if lines[j].startswith('+'):
                        content = lines[j][1:].strip()
                        if content.startswith('"""') or content.startswith("'''"):
                            has_docstring = True
                            break
                        elif content and not content.startswith('#') and not content.startswith('def ') and not content.startswith('class '):
                            break

                if not has_docstring:
                    self.issues.append(StyleIssue(
                        severity='info',
                        category='Docstrings',
                        description=f'Missing docstring for {"class" if class_match else "function"}',
                        line_number=i,
                        filename='unknown',
                        code_snippet=code_line[:80],
                        suggestion='Add a docstring to document the function/class purpose'
                    ))

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of style issues found.

        Returns:
            Dictionary with severity breakdown
        """
        summary = {
            'error': 0,
            'warning': 0,
            'info': 0,
            'total': len(self.issues),
            'by_category': {}
        }

        for issue in self.issues:
            summary[issue.severity] += 1

            category = issue.category
            if category not in summary['by_category']:
                summary['by_category'][category] = 0
            summary['by_category'][category] += 1

        return summary
