#!/usr/bin/env bash
# debug skill - Error analysis, explanation, and fix suggestions
# Usage: bash script.sh <analyze|explain|suggest> [input]
set -euo pipefail

COMMAND="${1:-}"
INPUT="${2:-}"

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

separator() { printf '%s\n' "─────────────────────────────────────"; }

usage() {
  cat <<EOF
${BOLD}debug skill${RESET} — Error analysis and fix suggestions

Commands:
  analyze <error>    Parse and diagnose an error message or stack trace
  explain <code>     Explain what an error code or exception means
  suggest <error>    Get fix suggestions for an error

Examples:
  bash script.sh analyze "TypeError: Cannot read property 'x' of undefined"
  bash script.sh explain ECONNREFUSED
  bash script.sh suggest "ModuleNotFoundError: No module named 'requests'"
  cat error.log | bash script.sh analyze -
EOF
  exit 0
}

# Read input from arg or stdin
get_input() {
  local arg="${1:-}"
  if [[ "$arg" == "-" || -z "$arg" ]]; then
    cat
  else
    echo "$arg"
  fi
}

# Main Python analyzer
run_python_analyzer() {
  local mode="$1"
  local text="$2"

  python3 -u - "$mode" "$text" <<'PYEOF'
import sys
import re
import json

mode = sys.argv[1]
text = sys.argv[2]

# ── Error pattern database ──────────────────────────────────────────────────
PATTERNS = [
    # Python
    {
        "id": "py_type_error_none",
        "regex": r"AttributeError: 'NoneType' object has no attribute",
        "lang": "Python", "type": "AttributeError", "severity": "HIGH",
        "summary": "Accessing attribute on a None value",
        "cause": "A variable that was expected to hold an object is None.\nThis usually means a function returned None instead of the expected value,\nor an optional lookup (dict.get, query result) returned nothing.",
        "fixes": [
            "Add a None check before accessing the attribute:\n      if obj is not None:\n          obj.method()",
            "Use a default value with dict.get():\n      val = data.get('key', default_value)",
            "Trace where the variable is assigned and why it might be None",
        ]
    },
    {
        "id": "py_index_error",
        "regex": r"IndexError: list index out of range",
        "lang": "Python", "type": "IndexError", "severity": "HIGH",
        "summary": "List index is out of valid range",
        "cause": "Trying to access list[i] where i >= len(list) or i < -len(list).",
        "fixes": [
            "Check list length before indexing:\n      if i < len(lst):\n          val = lst[i]",
            "Use a try/except block to handle missing indices",
            "Use lst[-1] to safely access the last element",
        ]
    },
    {
        "id": "py_module_not_found",
        "regex": r"ModuleNotFoundError: No module named '(.+)'",
        "lang": "Python", "type": "ModuleNotFoundError", "severity": "MEDIUM",
        "summary": "Python cannot locate the specified module",
        "cause": "The package is not installed in the current Python environment,\nor the virtual environment is not activated.",
        "fixes": [
            "Install the package:\n      pip install {match1}",
            "If using a virtualenv, activate it first:\n      source venv/bin/activate",
            "Check which Python is running:\n      which python3 && python3 -m pip list",
            "Verify the module name spelling (typos are common)",
        ]
    },
    {
        "id": "py_syntax_error",
        "regex": r"SyntaxError: (.+)",
        "lang": "Python", "type": "SyntaxError", "severity": "HIGH",
        "summary": "Python source code has a syntax error",
        "cause": "The Python parser found unexpected or invalid syntax.",
        "fixes": [
            "Check for mismatched brackets, parentheses, or braces",
            "Look for missing colons after if/for/def/class statements",
            "Check for invalid characters or encoding issues",
            "Run: python3 -m py_compile your_file.py  to get exact location",
        ]
    },
    {
        "id": "py_key_error",
        "regex": r"KeyError: (.+)",
        "lang": "Python", "type": "KeyError", "severity": "MEDIUM",
        "summary": "Dictionary key does not exist",
        "cause": "Accessing dict[key] where key is not present in the dictionary.",
        "fixes": [
            "Use dict.get() with a default:\n      val = d.get({match1}, None)",
            "Check if key exists first:\n      if {match1} in d:\n          val = d[{match1}]",
            "Use collections.defaultdict for auto-initialization",
        ]
    },
    {
        "id": "py_value_error",
        "regex": r"ValueError: (.+)",
        "lang": "Python", "type": "ValueError", "severity": "MEDIUM",
        "summary": "Function received an argument with an invalid value",
        "cause": "An operation or function received an argument of the right type\nbut with an inappropriate value (e.g., int('abc')).",
        "fixes": [
            "Validate input before passing to the function",
            "Use try/except ValueError to handle conversion failures",
            "Print the actual value to inspect it: print(repr(value))",
        ]
    },
    # Node.js / JavaScript
    {
        "id": "js_type_error_undefined",
        "regex": r"TypeError: Cannot read propert(?:y|ies) '?(.+?)'? of (undefined|null)",
        "lang": "JavaScript/Node.js", "type": "TypeError", "severity": "HIGH",
        "summary": "Accessing property on undefined or null",
        "cause": "A variable is undefined or null when you try to access a property on it.\nCommon in async code where a value hasn't loaded yet.",
        "fixes": [
            "Use optional chaining (ES2020+):\n      const val = obj?.{match1}",
            "Add a guard check:\n      if (obj && obj.{match1}) {{ ... }}",
            "Check async/await: ensure you're awaiting the promise",
            "Use nullish coalescing: obj ?? defaultValue",
        ]
    },
    {
        "id": "js_ref_error",
        "regex": r"ReferenceError: (.+) is not defined",
        "lang": "JavaScript/Node.js", "type": "ReferenceError", "severity": "HIGH",
        "summary": "Variable or function is not defined in current scope",
        "cause": "Referencing a variable before it is declared, or outside its scope.",
        "fixes": [
            "Declare the variable with let/const/var before use",
            "Check for typos in the variable name",
            "Ensure the import/require statement is correct:\n      const {match1} = require('./{match1}')",
            "Check if the variable is in the correct scope",
        ]
    },
    {
        "id": "js_syntax_error",
        "regex": r"SyntaxError: Unexpected token (.+)",
        "lang": "JavaScript/Node.js", "type": "SyntaxError", "severity": "HIGH",
        "summary": "JavaScript parser found unexpected token",
        "cause": "Invalid JavaScript syntax, often a missing bracket, comma, or semicolon.",
        "fixes": [
            "Check for missing/extra commas in objects or arrays",
            "Verify all brackets and braces are matched",
            "Use a linter: npx eslint your_file.js",
            "Check if you're using ES6+ features without transpilation",
        ]
    },
    # Go
    {
        "id": "go_nil_pointer",
        "regex": r"runtime error: invalid memory address or nil pointer dereference",
        "lang": "Go", "type": "nil pointer dereference", "severity": "CRITICAL",
        "summary": "Dereferencing a nil pointer — program will panic",
        "cause": "Accessing a method or field on a nil pointer. A variable of pointer type\nwas not initialized before use.",
        "fixes": [
            "Always check error returns and nil before dereferencing:\n      if ptr == nil {\n          // handle\n      }",
            "Initialize structs properly:\n      obj := &MyStruct{}",
            "Use the ok pattern for map and type assertions:\n      val, ok := m[key]",
        ]
    },
    {
        "id": "go_undefined",
        "regex": r"undefined: (.+)",
        "lang": "Go", "type": "Compile Error", "severity": "HIGH",
        "summary": "Identifier is not defined in this package",
        "cause": "Using a variable, function, or type that doesn't exist or isn't imported.",
        "fixes": [
            "Check the import block — the package may be missing",
            "Verify the identifier is exported (starts with uppercase for cross-package use)",
            "Run: go get <package> to install missing dependencies",
        ]
    },
    # System / Network
    {
        "id": "sys_econnrefused",
        "regex": r"ECONNREFUSED|Connection refused|connect: connection refused",
        "lang": "System/Network", "type": "ECONNREFUSED", "severity": "HIGH",
        "summary": "Connection actively refused by the target host",
        "cause": "The service at the target address is not running, not listening on that port,\nor a firewall is blocking the connection.",
        "fixes": [
            "Check if the service is running:\n      sudo systemctl status <service>",
            "Verify port binding:\n      ss -tlnp | grep <port>",
            "Check firewall:\n      sudo ufw status",
            "Confirm the host and port in your configuration",
        ]
    },
    {
        "id": "sys_enoent",
        "regex": r"ENOENT|No such file or directory",
        "lang": "System", "type": "ENOENT", "severity": "MEDIUM",
        "summary": "File or directory does not exist",
        "cause": "A file operation was attempted on a path that doesn't exist.",
        "fixes": [
            "Check the path is correct and the file exists:\n      ls -la /path/to/file",
            "Ensure the working directory is what you expect:\n      pwd",
            "Check for typos in the path string",
            "Create the file or directory if it should exist:\n      mkdir -p /path/to/dir",
        ]
    },
    {
        "id": "sys_permission",
        "regex": r"Permission denied|EACCES|403 Forbidden",
        "lang": "System", "type": "Permission Denied", "severity": "HIGH",
        "summary": "Insufficient permissions for the operation",
        "cause": "The current user does not have the required read/write/execute permissions.",
        "fixes": [
            "Check file permissions:\n      ls -la /path/to/file",
            "For system files, use sudo (carefully)",
            "Fix ownership:\n      chown $USER /path/to/file",
            "Fix permissions:\n      chmod 644 /path/to/file",
        ]
    },
    {
        "id": "sys_timeout",
        "regex": r"ETIMEDOUT|Connection timed out|Read timeout|deadline exceeded",
        "lang": "System/Network", "type": "Timeout", "severity": "MEDIUM",
        "summary": "Operation timed out before completing",
        "cause": "Network latency, server overload, or a too-short timeout setting.",
        "fixes": [
            "Increase timeout in your client/config",
            "Check network connectivity to the target",
            "Verify the server is not overloaded",
            "Check DNS resolution:\n      nslookup <hostname>",
        ]
    },
    {
        "id": "sys_oom",
        "regex": r"Out of memory|OOM|Cannot allocate memory|killed.*OOM",
        "lang": "System", "type": "Out of Memory", "severity": "CRITICAL",
        "summary": "Process ran out of available memory",
        "cause": "The process exceeded available RAM. May be a memory leak or insufficient resources.",
        "fixes": [
            "Check memory usage:\n      free -h && cat /proc/meminfo",
            "Increase available memory or add swap",
            "Profile for memory leaks in your application",
            "Process data in smaller chunks instead of loading all at once",
        ]
    },
    # Docker / Container
    {
        "id": "docker_no_such_image",
        "regex": r"Unable to find image|No such image|pull access denied",
        "lang": "Docker", "type": "ImageNotFound", "severity": "MEDIUM",
        "summary": "Docker image not found locally or in registry",
        "cause": "The image name or tag is wrong, or you lack access to the registry.",
        "fixes": [
            "Check the image name and tag spelling",
            "Pull the image explicitly:\n      docker pull <image>:<tag>",
            "Log in to the registry:\n      docker login <registry>",
            "List available local images:\n      docker images",
        ]
    },
    # Git
    {
        "id": "git_merge_conflict",
        "regex": r"CONFLICT|Merge conflict|Automatic merge failed",
        "lang": "Git", "type": "Merge Conflict", "severity": "MEDIUM",
        "summary": "Git cannot automatically merge changes",
        "cause": "Two branches made conflicting changes to the same lines.",
        "fixes": [
            "Find conflicted files:\n      git status",
            "Edit each file to resolve <<<<< ===== >>>>> markers",
            "After resolving:\n      git add <file>\n      git merge --continue",
            "To abort the merge:\n      git merge --abort",
        ]
    },
    # Database
    {
        "id": "db_deadlock",
        "regex": r"deadlock detected|Deadlock found|Lock wait timeout",
        "lang": "Database", "type": "Deadlock", "severity": "HIGH",
        "summary": "Database detected a deadlock between transactions",
        "cause": "Two or more transactions are waiting for each other to release locks.",
        "fixes": [
            "Retry the transaction (standard deadlock handling)",
            "Ensure consistent lock ordering across transactions",
            "Keep transactions short — commit as early as possible",
            "Use SELECT ... FOR UPDATE only when necessary",
        ]
    },
    # Generic
    {
        "id": "generic_segfault",
        "regex": r"Segmentation fault|SIGSEGV|segfault",
        "lang": "C/C++/Native", "type": "SIGSEGV", "severity": "CRITICAL",
        "summary": "Segmentation fault — invalid memory access",
        "cause": "The process accessed memory it is not allowed to access.\nCommon causes: null pointer dereference, buffer overflow, use-after-free.",
        "fixes": [
            "Run with a debugger:\n      gdb ./program core",
            "Use AddressSanitizer:\n      gcc -fsanitize=address -g your_code.c",
            "Use Valgrind:\n      valgrind --leak-check=full ./program",
            "Check for array out-of-bounds writes and pointer arithmetic",
        ]
    },
]

SEVERITY_COLOR = {"CRITICAL": "\033[0;31m", "HIGH": "\033[1;33m", "MEDIUM": "\033[0;33m", "LOW": "\033[0;32m"}
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[0;36m"

def find_pattern(text):
    for p in PATTERNS:
        m = re.search(p["regex"], text, re.IGNORECASE)
        if m:
            return p, m
    return None, None

def format_fixes(fixes, match=None):
    result = []
    for i, fix in enumerate(fixes, 1):
        f = fix
        if match:
            for j, g in enumerate(match.groups(), 1):
                f = f.replace(f"{{match{j}}}", g or "")
        result.append(f"  {i}. {f}")
    return "\n".join(result)

sep = "─" * 45

if mode == "analyze":
    pattern, match = find_pattern(text)
    if pattern:
        sev_color = SEVERITY_COLOR.get(pattern["severity"], "")
        print(f"\n{BOLD}🔍 Error Analysis{RESET}")
        print(sep)
        print(f"Language : {pattern['lang']}")
        print(f"Type     : {pattern['type']}")
        print(f"Severity : {sev_color}{pattern['severity']}{RESET}")
        print(f"Summary  : {pattern['summary']}")
        print(f"\n{BOLD}Root Cause:{RESET}")
        print(f"  {pattern['cause'].replace(chr(10), chr(10)+'  ')}")
        print(f"\n{BOLD}Fix Suggestions:{RESET}")
        print(format_fixes(pattern["fixes"], match))
        print()
    else:
        print(f"\n{BOLD}🔍 Error Analysis{RESET}")
        print(sep)
        print(f"No known pattern matched for this error.\n")
        # Generic hints
        lines = text.strip().splitlines()
        for line in lines:
            if re.search(r'error|exception|fail|fatal', line, re.IGNORECASE):
                print(f"  Detected keyword: {CYAN}{line.strip()}{RESET}")
        print(f"\n{BOLD}General debugging steps:{RESET}")
        print("  1. Read the full error message carefully — the cause is often stated explicitly")
        print("  2. Check the line number referenced in the stack trace")
        print("  3. Search the error message online for known solutions")
        print("  4. Add logging/print statements around the failing code")
        print("  5. Simplify your input to reproduce the minimal failing case")
        print()

elif mode == "explain":
    pattern, match = find_pattern(text)
    if pattern:
        print(f"\n{BOLD}📖 Error Explanation{RESET}")
        print(sep)
        print(f"Name     : {pattern['type']}")
        print(f"Language : {pattern['lang']}")
        print(f"Severity : {SEVERITY_COLOR.get(pattern['severity'], '')}{pattern['severity']}{RESET}")
        print(f"\n{BOLD}Description:{RESET}")
        print(f"  {pattern['summary']}")
        print(f"\n{BOLD}Common Causes:{RESET}")
        for line in pattern["cause"].splitlines():
            print(f"  {line}")
        print()
    else:
        # Try built-in errno / HTTP status explanations
        http_codes = {
            "400": ("Bad Request", "The server cannot process the request due to malformed syntax."),
            "401": ("Unauthorized", "Authentication is required and has failed or not been provided."),
            "403": ("Forbidden", "The server understood the request but refuses to authorize it."),
            "404": ("Not Found", "The requested resource could not be found on the server."),
            "408": ("Request Timeout", "The server timed out waiting for the request."),
            "429": ("Too Many Requests", "Rate limit exceeded. Slow down and retry after a delay."),
            "500": ("Internal Server Error", "The server encountered an unexpected condition."),
            "502": ("Bad Gateway", "The upstream server returned an invalid response."),
            "503": ("Service Unavailable", "The server is temporarily unavailable, usually due to overload."),
            "504": ("Gateway Timeout", "The upstream server failed to respond in time."),
        }
        code = text.strip()
        if code in http_codes:
            name, desc = http_codes[code]
            print(f"\n{BOLD}📖 HTTP Status Code {code}{RESET}")
            print(sep)
            print(f"Name        : {name}")
            print(f"Description : {desc}")
            print()
        else:
            print(f"\n{BOLD}📖 Error Code: {text}{RESET}")
            print(sep)
            print("This error code is not in the built-in database.")
            print("Try: man errno | grep -A2 <code>  for system errors")
            print("Or search: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status")
            print()

elif mode == "suggest":
    pattern, match = find_pattern(text)
    if pattern:
        print(f"\n{BOLD}💡 Fix Suggestions{RESET}")
        print(sep)
        print(f"Error    : {pattern['type']}")
        print(f"Summary  : {pattern['summary']}")
        print(f"\n{BOLD}Suggested Fixes:{RESET}")
        print(format_fixes(pattern["fixes"], match))
        print()
    else:
        print(f"\n{BOLD}💡 Fix Suggestions{RESET}")
        print(sep)
        print("No specific fixes found for this error pattern.\n")
        print(f"{BOLD}General approach:{RESET}")
        print("  1. Isolate the error: reproduce it with minimal code")
        print("  2. Read the error type and message carefully")
        print("  3. Check recent code changes (git diff)")
        print("  4. Search the exact error message in your language's issue tracker")
        print("  5. Add assertions to verify assumptions about variable values")
        print()
PYEOF
}

case "$COMMAND" in
  analyze)
    if [[ -z "$INPUT" ]]; then
      INPUT="$(cat)"
    elif [[ "$INPUT" == "-" ]]; then
      INPUT="$(cat)"
    fi
    run_python_analyzer "analyze" "$INPUT"
    ;;
  explain)
    if [[ -z "$INPUT" ]]; then
      echo "Usage: bash script.sh explain <error_code_or_name>"
      exit 1
    fi
    run_python_analyzer "explain" "$INPUT"
    ;;
  suggest)
    if [[ -z "$INPUT" ]]; then
      INPUT="$(cat)"
    elif [[ "$INPUT" == "-" ]]; then
      INPUT="$(cat)"
    fi
    run_python_analyzer "suggest" "$INPUT"
    ;;
  help|--help|-h|"")
    usage
    ;;
  *)
    echo -e "${RED}Unknown command: $COMMAND${RESET}"
    echo "Run: bash script.sh help"
    exit 1
    ;;
esac
