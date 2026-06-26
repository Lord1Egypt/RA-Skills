---
name: Automation Quality Assurance & Testing Protocol
id: automation-qa-testing
version: 1.1.0
description: A comprehensive framework for testing and validating automation projects to ensure stability, security, and scalability.
author: Moamen Mohamed
---

# Automation Quality Assurance & Testing Protocol

This skill is the primary authority for testing any automation project within the OpenClaw environment. It ensures operational stability, prevents regressions, and maintains high-quality standards across all automated workflows.

---

## Agent: How to Use This Skill

Read this protocol fully before modifying or deploying any automation script. Follow the steps sequentially.

### 1. Comprehensive Automation Testing Strategy
To ensure a robust automation, every project must pass through these 6 critical testing layers:

- **Layer 1: Unit Testing (Logic)** - Test individual functions, mathematical calculations, and internal logic branches in isolation.
- **Layer 4: Idempotency & Recovery** - Ensure that if a script fails and restarts, it does not produce side effects (e.g., no duplicate emails or redundant API calls). The script must be "Safe to Restart."
- **Layer 2: Integration Testing (Connectors)** - Verify successful communication with external services (Meta API, Google Sheets, SMTP, etc.) using real or sandbox credentials.
- **Layer 3: End-to-End (E2E) Flow** - Simulate a complete lifecycle of the automation (e.g., Budget Breach -> Pause -> Notify) to ensure the entire chain works.
- **Layer 5: Regression Testing** - Always run the full `run_tests.py` suite after any change to confirm that existing features remain functional.
- **Layer 6: Observability & Logging Verification** - Confirm that the script produces clear, actionable logs for every step, especially during failures, to ensure "blind spots" are eliminated.

---

### 2. Execution Protocol
Do find and execute tests before and after every modification:
1. **Discover:** Always look for `run_tests.py` or a `tests/` directory within the project root.
2. **Execute:** 
   ```bash
   python3 path/to/project/run_tests.py
   ```
3. **Initialize:** If the project lacks tests, **you are mandated** to create a `run_tests.py` file implementing the 6 layers above.

---

### 3. Standard Exit Criteria (Definition of Done)
A task is considered "Complete" only when:
- **100% Pass Rate:** All 6 testing layers pass without errors.
- **Timezone Uniformity:** All timestamps and scheduling are synchronized to the environment's local time (e.g., `Africa/Cairo`).
- **Security Compliance:** Zero hardcoded secrets. All tokens and passwords must be isolated in `.env` or config files.
- **Failure Resilience:** The script handles API timeouts and connection drops gracefully without crashing.
- **Documentation:** The code is clean, commented, and includes a brief explanation of any new test cases added.

---

## Maintenance & Scalability
- The Test Suite must grow with the project. Every new feature requires a corresponding test case.
- Any project without a functional `run_tests.py` is considered "Substandard" and must be fixed immediately.
