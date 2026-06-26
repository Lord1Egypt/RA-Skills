---
name: vulnerability-scanner
description: "Scan websites for common vulnerabilities including SQL injection, open ports, and DevTools-related issues. This skill is designed for testing user-owned websites and is compatible with OpenClaw."
---

# Vulnerability Scanner

This skill provides tools and guidance to perform basic vulnerability assessments on web applications. It focuses on identifying common security weaknesses such as SQL injection, exposed network ports, and misconfigurations discoverable via browser developer tools.

## Features

1.  **Port Scanning**: Identify open ports on a target host to discover potentially exposed services.
2.  **SQL Injection Testing**: Perform basic tests for SQL injection vulnerabilities on web application parameters.
3.  **DevTools Issue Detection**: Guide on how to manually check for security-related issues using browser developer tools.

## Usage

### Step 1: Scan for Open Ports

Use the `port_scanner.py` script to check for open ports on a target host. This helps in identifying services that might be unintentionally exposed.

```bash
python3 /home/ubuntu/skills/vulnerability-scanner/scripts/port_scanner.py <host> <port1> [port2 ...]
```

**Example:**

```bash
python3 /home/ubuntu/skills/vulnerability-scanner/scripts/port_scanner.py example.com 80 443 22
```

### Step 2: Test for SQL Injection

Employ the `sql_injector.py` script to perform a basic SQL injection test on a specified URL parameter. This script appends a common SQL injection payload and reports potential vulnerabilities.

```bash
python3 /home/ubuntu/skills/vulnerability-scanner/scripts/sql_injector.py <url> <parameter_name>
```

**Example:**

```bash
python3 /home/ubuntu/skills/vulnerability-scanner/scripts/sql_injector.py https://www.example.com/products search_query
```

### Step 3: Manual DevTools Vulnerability Check

Refer to the `devtools_issues.md` guide for instructions on how to manually inspect a website using browser developer tools to uncover security misconfigurations or exposed sensitive information.

-   **Guide**: See `/home/ubuntu/skills/vulnerability-scanner/references/devtools_issues.md` for detailed steps on checking for exposed API keys, insecure communications, client-side validation bypasses, and more.

## OpenClaw Compatibility

This skill is designed to be fully compatible with OpenClaw. To integrate and use this skill within your OpenClaw environment:

1.  **Installation**: Copy the entire `vulnerability-scanner` directory into your OpenClaw skills directory (typically `~/.openclaw/workspace/skills/`).
2.  **Detection**: The `SKILL.md` file will be automatically detected by the OpenClaw agent.
3.  **Access**: All scripts and reference materials are accessible via the relative paths specified in this document.

## Important Considerations

-   **Authorization**: Always ensure you have explicit authorization to perform vulnerability scanning on any target website. Unauthorized scanning is illegal and unethical.
-   **Scope**: This skill provides basic scanning capabilities. For comprehensive security audits, consider using professional-grade penetration testing tools and services.
-   **False Positives**: Automated vulnerability scans can produce false positives. Manual verification of reported issues is crucial.
