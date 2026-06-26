"""
C Security Rules - Security vulnerability detection for C code
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class SecurityIssue:
    rule_id: str
    cwe_id: str
    title: str
    description: str
    severity: Severity
    line: int
    code: str
    fix: str
    references: List[str]


class CSecurityRules:
    """
    Security rules for C code analysis
    Based on CWE and CERT C Secure Coding Standard
    """
    
    # Dangerous functions that should be avoided
    DANGEROUS_FUNCTIONS = {
        # Buffer overflow risks
        'strcpy': {
            'cwe': 'CWE-120',
            'title': 'Buffer Overflow - strcpy',
            'description': 'strcpy() does not check buffer sizes, leading to buffer overflow',
            'severity': Severity.CRITICAL,
            'fix': 'Use strncpy(), strlcpy(), or strcpy_s() with size limit',
            'references': ['https://cwe.mitre.org/data/definitions/120.html']
        },
        'strcat': {
            'cwe': 'CWE-120',
            'title': 'Buffer Overflow - strcat',
            'description': 'strcat() does not check buffer sizes',
            'severity': Severity.CRITICAL,
            'fix': 'Use strncat(), strlcat(), or strcat_s() with size limit',
            'references': ['https://cwe.mitre.org/data/definitions/120.html']
        },
        'sprintf': {
            'cwe': 'CWE-120',
            'title': 'Buffer Overflow - sprintf',
            'description': 'sprintf() can write beyond buffer bounds',
            'severity': Severity.CRITICAL,
            'fix': 'Use snprintf() or sprintf_s() with buffer size',
            'references': ['https://cwe.mitre.org/data/definitions/120.html']
        },
        'vsprintf': {
            'cwe': 'CWE-120',
            'title': 'Buffer Overflow - vsprintf',
            'description': 'vsprintf() can write beyond buffer bounds',
            'severity': Severity.CRITICAL,
            'fix': 'Use vsnprintf() or vsprintf_s()',
            'references': ['https://cwe.mitre.org/data/definitions/120.html']
        },
        'gets': {
            'cwe': 'CWE-242',
            'title': 'Use of Inherently Dangerous Function - gets',
            'description': 'gets() is inherently dangerous and removed in C11',
            'severity': Severity.CRITICAL,
            'fix': 'Use fgets() with size limit',
            'references': ['https://cwe.mitre.org/data/definitions/242.html']
        },
        'scanf': {
            'cwe': 'CWE-120',
            'title': 'Buffer Overflow Risk - scanf',
            'description': 'scanf() without field width can overflow buffers',
            'severity': Severity.HIGH,
            'fix': 'Use scanf with width limits (e.g., %99s) or fgets + sscanf',
            'references': ['https://cwe.mitre.org/data/definitions/120.html']
        },
        
        # Format string vulnerabilities
        'printf': {
            'cwe': 'CWE-134',
            'title': 'Format String Vulnerability',
            'description': 'Passing user input directly to printf can lead to format string attacks',
            'severity': Severity.HIGH,
            'fix': 'Use printf("%s", user_input) instead of printf(user_input)',
            'references': ['https://cwe.mitre.org/data/definitions/134.html']
        },
        'fprintf': {
            'cwe': 'CWE-134',
            'title': 'Format String Vulnerability',
            'severity': Severity.HIGH,
            'fix': 'Use fprintf(stream, "%s", user_input)',
            'references': ['https://cwe.mitre.org/data/definitions/134.html']
        },
        'syslog': {
            'cwe': 'CWE-134',
            'title': 'Format String Vulnerability',
            'severity': Severity.HIGH,
            'fix': 'Use syslog(priority, "%s", user_input)',
            'references': ['https://cwe.mitre.org/data/definitions/134.html']
        },
        
        # Command injection
        'system': {
            'cwe': 'CWE-78',
            'title': 'OS Command Injection',
            'description': 'system() executes shell commands - dangerous with user input',
            'severity': Severity.CRITICAL,
            'fix': 'Use execve() family or avoid shell execution',
            'references': ['https://cwe.mitre.org/data/definitions/78.html']
        },
        'popen': {
            'cwe': 'CWE-78',
            'title': 'OS Command Injection',
            'severity': Severity.CRITICAL,
            'fix': 'Use safer alternatives or validate/escape input',
            'references': ['https://cwe.mitre.org/data/definitions/78.html']
        },
        
        # Memory management
        'malloc': {
            'cwe': 'CWE-252',
            'title': 'Unchecked Return Value - malloc',
            'description': 'malloc() return value should be checked for NULL',
            'severity': Severity.MEDIUM,
            'fix': 'Check if (ptr == NULL) after malloc',
            'references': ['https://cwe.mitre.org/data/definitions/252.html']
        },
        'calloc': {
            'cwe': 'CWE-252',
            'title': 'Unchecked Return Value - calloc',
            'severity': Severity.MEDIUM,
            'fix': 'Check if (ptr == NULL) after calloc',
            'references': ['https://cwe.mitre.org/data/definitions/252.html']
        },
        
        # Path traversal
        'chroot': {
            'cwe': 'CWE-243',
            'title': 'Unsafe chroot',
            'description': 'chroot() alone is not sufficient for sandboxing',
            'severity': Severity.HIGH,
            'fix': 'Use chroot with privilege dropping and proper setup',
            'references': ['https://cwe.mitre.org/data/definitions/243.html']
        },
    }
    
    # Wide character versions
    WIDE_CHAR_FUNCTIONS = {
        'wcscpy': 'wcsncpy',
        'wcscat': 'wcsncat',
        'swprintf': 'swprintf with count',
    }
    
    # Patterns for vulnerable code
    VULNERABLE_PATTERNS = [
        {
            'id': 'CWE-134-FMT',
            'cwe': 'CWE-134',
            'pattern': r'printf\s*\(\s*[^"\']*\$\w+',
            'title': 'Format String Vulnerability',
            'description': 'Potential format string vulnerability with variable format',
            'severity': Severity.HIGH,
            'fix': 'Use constant format string: printf("%s", var)',
            'references': ['https://cwe.mitre.org/data/definitions/134.html']
        },
        {
            'id': 'CWE-89-SQLI',
            'cwe': 'CWE-89',
            'pattern': r'sqlite3_exec\s*\([^)]*\+',
            'title': 'SQL Injection',
            'description': 'Potential SQL injection with string concatenation',
            'severity': Severity.CRITICAL,
            'fix': 'Use parameterized queries or prepared statements',
            'references': ['https://cwe.mitre.org/data/definitions/89.html']
        },
        {
            'id': 'CWE-190-INT-OVERFLOW',
            'cwe': 'CWE-190',
            'pattern': r'\w+\s*\*\s*\w+\s*\+\s*sizeof',
            'title': 'Integer Overflow Risk',
            'description': 'Potential integer overflow in allocation calculation',
            'severity': Severity.HIGH,
            'fix': 'Check for overflow: if (n > SIZE_MAX / size) handle_error()',
            'references': ['https://cwe.mitre.org/data/definitions/190.html']
        },
        {
            'id': 'CWE-362-RACE',
            'cwe': 'CWE-362',
            'pattern': r'access\s*\([^)]+\)\s*[^;{]*;\s*\n[^\n]*open\s*\(',
            'title': 'TOCTOU Race Condition',
            'description': 'Time-of-check-time-of-use race condition',
            'severity': Severity.HIGH,
            'fix': 'Use file descriptors consistently or check after open',
            'references': ['https://cwe.mitre.org/data/definitions/362.html']
        },
    ]
    
    # Hardcoded credential patterns
    CREDENTIAL_PATTERNS = [
        {
            'pattern': r'password\s*=\s*["\'][^"\']+["\']',
            'title': 'Hardcoded Password',
            'cwe': 'CWE-798',
            'severity': Severity.CRITICAL,
        },
        {
            'pattern': r'api_key\s*=\s*["\'][^"\']+["\']',
            'title': 'Hardcoded API Key',
            'cwe': 'CWE-798',
            'severity': Severity.CRITICAL,
        },
        {
            'pattern': r'secret\s*=\s*["\'][^"\']+["\']',
            'title': 'Hardcoded Secret',
            'cwe': 'CWE-798',
            'severity': Severity.CRITICAL,
        },
        {
            'pattern': r'A[SK]IA[0-9A-Z]{16}',
            'title': 'AWS Access Key ID',
            'cwe': 'CWE-798',
            'severity': Severity.CRITICAL,
        },
    ]
    
    @classmethod
    def get_dangerous_function_info(cls, func_name: str) -> Optional[Dict]:
        """Get information about a dangerous function"""
        return cls.DANGEROUS_FUNCTIONS.get(func_name)
    
    @classmethod
    def is_dangerous_function(cls, func_name: str) -> bool:
        """Check if a function is in the dangerous list"""
        return func_name in cls.DANGEROUS_FUNCTIONS
    
    @classmethod
    def get_all_dangerous_functions(cls) -> List[str]:
        """Get list of all dangerous functions"""
        return list(cls.DANGEROUS_FUNCTIONS.keys())
    
    @classmethod
    def get_replacement_function(cls, func_name: str) -> Optional[str]:
        """Get the safe replacement for a dangerous function"""
        info = cls.DANGEROUS_FUNCTIONS.get(func_name)
        if info:
            fix = info['fix']
            # Extract function name from fix recommendation
            if 'Use ' in fix:
                return fix.split('Use ')[1].split()[0].rstrip(',')
        return None


class CSecurityChecker:
    """
    Check C code for security vulnerabilities
    """
    
    def __init__(self):
        self.rules = CSecurityRules()
    
    def check_file(self, filepath: str, content: str = None) -> List[SecurityIssue]:
        """Check a C file for security issues"""
        issues = []
        
        if content is None:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        
        lines = content.split('\n')
        
        # Check for dangerous function calls
        issues.extend(self._check_dangerous_functions(lines, filepath))
        
        # Check for vulnerable patterns
        issues.extend(self._check_vulnerable_patterns(content, lines, filepath))
        
        # Check for hardcoded credentials
        issues.extend(self._check_hardcoded_credentials(lines, filepath))
        
        # Check for common C security issues
        issues.extend(self._check_c_specific_issues(lines, filepath))
        
        return sorted(issues, key=lambda x: (x.line, x.severity.value))
    
    def _check_dangerous_functions(self, lines: List[str], filepath: str) -> List[SecurityIssue]:
        """Check for calls to dangerous functions"""
        issues = []
        dangerous_funcs = CSecurityRules.get_all_dangerous_functions()
        
        import re
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            code = line.split('//')[0]
            
            for func in dangerous_funcs:
                # Match function call (not declaration)
                pattern = rf'\b{func}\s*\('
                if re.search(pattern, code):
                    info = CSecurityRules.get_dangerous_function_info(func)
                    if info:
                        issues.append(SecurityIssue(
                            rule_id=f"{info['cwe']}-{func.upper()}",
                            cwe_id=info['cwe'],
                            title=info['title'],
                            description=info['description'],
                            severity=info['severity'],
                            line=i,
                            code=line.strip(),
                            fix=info['fix'],
                            references=info['references']
                        ))
        
        return issues
    
    def _check_vulnerable_patterns(self, content: str, lines: List[str], filepath: str) -> List[SecurityIssue]:
        """Check for vulnerable code patterns"""
        issues = []
        import re
        
        for pattern_info in CSecurityRules.VULNERABLE_PATTERNS:
            pattern = pattern_info['pattern']
            for match in re.finditer(pattern, content, re.IGNORECASE):
                # Calculate line number
                line_num = content[:match.start()].count('\n') + 1
                line_content = lines[line_num - 1] if line_num <= len(lines) else ""
                
                issues.append(SecurityIssue(
                    rule_id=pattern_info['id'],
                    cwe_id=pattern_info['cwe'],
                    title=pattern_info['title'],
                    description=pattern_info['description'],
                    severity=pattern_info['severity'],
                    line=line_num,
                    code=line_content.strip(),
                    fix=pattern_info['fix'],
                    references=pattern_info['references']
                ))
        
        return issues
    
    def _check_hardcoded_credentials(self, lines: List[str], filepath: str) -> List[SecurityIssue]:
        """Check for hardcoded credentials"""
        issues = []
        import re
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            code = line.split('//')[0]
            
            for cred_pattern in CSecurityRules.CREDENTIAL_PATTERNS:
                if re.search(cred_pattern['pattern'], code, re.IGNORECASE):
                    issues.append(SecurityIssue(
                        rule_id=f"{cred_pattern['cwe']}-HARDCODED",
                        cwe_id=cred_pattern['cwe'],
                        title=cred_pattern['title'],
                        description=f"Potential {cred_pattern['title'].lower()} detected",
                        severity=cred_pattern['severity'],
                        line=i,
                        code=line.strip(),
                        fix='Move credentials to environment variables or secure storage',
                        references=['https://cwe.mitre.org/data/definitions/798.html']
                    ))
        
        return issues
    
    def _check_c_specific_issues(self, lines: List[str], filepath: str) -> List[SecurityIssue]:
        """Check for C-specific security issues"""
        issues = []
        import re
        
        # Track variables for malloc/free analysis
        malloc_vars = {}
        
        for i, line in enumerate(lines, 1):
            code = line.split('//')[0]
            
            # Check for malloc without NULL check
            malloc_match = re.search(r'(\w+)\s*=\s*malloc\s*\(', code)
            if malloc_match:
                var_name = malloc_match.group(1)
                malloc_vars[var_name] = i
                
                # Check next few lines for NULL check
                has_null_check = False
                for j in range(i, min(i + 5, len(lines))):
                    if var_name in lines[j] and ('NULL' in lines[j] or '!'+var_name in lines[j]):
                        has_null_check = True
                        break
                
                if not has_null_check:
                    issues.append(SecurityIssue(
                        rule_id='CWE-252-MALLOC',
                        cwe_id='CWE-252',
                        title='Unchecked malloc Return Value',
                        description=f'malloc() return value not checked for NULL',
                        severity=Severity.MEDIUM,
                        line=i,
                        code=line.strip(),
                        fix=f'Add NULL check: if ({var_name} == NULL) {{ handle_error(); }}',
                        references=['https://cwe.mitre.org/data/definitions/252.html']
                    ))
            
            # Check for potential buffer overflow in array access
            array_match = re.search(r'(\w+)\s*\[\s*(\w+)\s*\]', code)
            if array_match:
                array_name = array_match.group(1)
                index_name = array_match.group(2)
                
                # This is a heuristic - in practice, need more analysis
                # Just flagging it as potential issue
                pass
            
            # Check for strcmp return value not checked
            strcmp_match = re.search(r'strcmp\s*\([^)]+\)\s*;', code)
            if strcmp_match:
                issues.append(SecurityIssue(
                    rule_id='CERT-EXP12-C',
                    cwe_id='CWE-252',
                    title='Unchecked strcmp Return Value',
                    description='strcmp() return value should be checked',
                    severity=Severity.LOW,
                    line=i,
                    code=line.strip(),
                    fix='Check the return value: int result = strcmp(a, b);',
                    references=['https://wiki.sei.cmu.edu/confluence/display/c/EXP12-C.+Do+not+ignore+values+returned+by+functions']
                ))
            
            # Check for scanf without width limit
            scanf_match = re.search(r'scanf\s*\(\s*"([^"]+)"', code)
            if scanf_match:
                format_str = scanf_match.group(1)
                # Check for %s without width
                if '%s' in format_str and '%' + str(len(format_str)) + 's' not in format_str:
                    if not any(f'%{n}s' in format_str for n in range(1, 1000)):
                        issues.append(SecurityIssue(
                            rule_id='CWE-120-SCANF',
                            cwe_id='CWE-120',
                            title='scanf Without Width Limit',
                            description='scanf with %s without width limit can overflow buffer',
                            severity=Severity.HIGH,
                            line=i,
                            code=line.strip(),
                            fix='Use width limit: scanf("%99s", buffer)',
                            references=['https://cwe.mitre.org/data/definitions/120.html']
                        ))
        
        return issues


def get_security_summary(issues: List[SecurityIssue]) -> Dict:
    """Get summary of security issues"""
    summary = {
        'total': len(issues),
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0,
        'by_cwe': {},
        'issues': []
    }
    
    for issue in issues:
        summary[issue.severity.value] += 1
        
        if issue.cwe_id not in summary['by_cwe']:
            summary['by_cwe'][issue.cwe_id] = 0
        summary['by_cwe'][issue.cwe_id] += 1
        
        summary['issues'].append({
            'line': issue.line,
            'severity': issue.severity.value,
            'cwe': issue.cwe_id,
            'title': issue.title,
            'fix': issue.fix
        })
    
    return summary


# Export common rules for easy access
DANGEROUS_FUNCTIONS = CSecurityRules.DANGEROUS_FUNCTIONS
VULNERABLE_PATTERNS = CSecurityRules.VULNERABLE_PATTERNS
CREDENTIAL_PATTERNS = CSecurityRules.CREDENTIAL_PATTERNS
