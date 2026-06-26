#!/usr/bin/env python3
"""Code Review Checklist Handler - Systematic code review guidance and checklists."""
import sys
import json
import re

def detect_intent(text):
    """Detect what type of code review help the user needs."""
    text_lower = text.lower()
    
    if any(k in text_lower for k in ["清单", "checklist", "列表", "项目"]):
        return "checklist"
    elif any(k in text_lower for k in ["审查", "review", "检查"]):
        return "review"
    elif any(k in text_lower for k in ["安全", "security", "漏洞"]):
        return "security"
    elif any(k in text_lower for k in ["性能", "performance", "优化"]):
        return "performance"
    elif any(k in text_lower for k in ["测试", "test", "coverage"]):
        return "testing"
    elif any(k in text_lower for k in ["前端", "frontend", "react", "vue", "css"]):
        return "frontend"
    elif any(k in text_lower for k in ["后端", "backend", "api", "server"]):
        return "backend"
    elif any(k in text_lower for k in ["python"]):
        return "python"
    elif any(k in text_lower for k in ["javascript", "typescript", "js", "ts"]):
        return "javascript"
    elif any(k in text_lower for k in ["java"]):
        return "java"
    elif any(k in text_lower for k in ["go", "golang"]):
        return "go"
    elif any(k in text_lower for k in ["工作流", "workflow", "流程", "步骤"]):
        return "workflow"
    elif any(k in text_lower for k in ["准备", "prepare", "自审查"]):
        return "prepare"
    elif any(k in text_lower for k in ["标准", "standard", "规范"]):
        return "standards"
    elif any(k in text_lower for k in ["问题", "issue", "blocking"]):
        return "issues"
    else:
        return "general"

def get_full_checklist():
    """Return the complete code review checklist."""
    return """
## Code Review Checklist (Complete)

### 1. Correctness and Logic
- [ ] Code produces expected output for all cases
- [ ] Edge cases are properly handled
- [ ] No off-by-one errors in loops/arrays
- [ ] Logic is sound and complete
- [ ] No infinite loops or recursion issues
- [ ] Proper use of data structures
- [ ] Null/undefined checks where needed

### 2. Code Style and Readability
- [ ] Follows project coding standards
- [ ] Naming is clear and descriptive
- [ ] Functions are appropriately sized (not too long)
- [ ] Code is not duplicated (DRY principle)
- [ ] Complex logic has explanatory comments
- [ ] Formatting is consistent
- [ ] No commented-out dead code
- [ ] Import statements are organized

### 3. Performance and Efficiency
- [ ] No unnecessary loops or iterations
- [ ] Proper use of caching when applicable
- [ ] Database queries are optimized (no N+1)
- [ ] No memory leaks
- [ ] Appropriate algorithmic complexity
- [ ] Resources are properly released
- [ ] Lazy loading where appropriate

### 4. Security
- [ ] Input validation on all user inputs
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No hardcoded secrets/passwords/API keys
- [ ] Proper authentication/authorization
- [ ] Sensitive data properly protected
- [ ] HTTPS used where needed
- [ ] No security misconfigurations
- [ ] Dependencies are up-to-date

### 5. Error Handling
- [ ] Errors are caught and handled appropriately
- [ ] Error messages are user-friendly
- [ ] No empty catch blocks
- [ ] Logging is appropriate (not too much/too little)
- [ ] Graceful degradation where needed
- [ ] No exposing internal error details to users
- [ ] Errors are logged with context

### 6. Testing
- [ ] Unit tests exist for new code
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests are maintainable
- [ ] Mock usage is appropriate
- [ ] Test coverage meets requirements
- [ ] No flaky tests introduced
- [ ] Integration tests cover flows

### 7. Documentation
- [ ] Public APIs are documented
- [ ] Complex logic has comments
- [ ] README updated if needed
- [ ] API changes are documented
- [ ] Breaking changes are noted
- [ ] Deployment steps documented

### 8. Architecture and Design
- [ ] Follows project architecture patterns
- [ ] Single Responsibility Principle followed
- [ ] Dependencies are properly injected
- [ ] Coupling is minimized
- [ ] Changes are localized appropriately
- [ ] No unnecessary tech debt introduced
- [ ] Reusability considered
- [ ] API design is RESTful/consistent

### 9. Git and Process
- [ ] Commit messages are meaningful
- [ ] PR description is clear
- [ ] Related tests are included
- [ ] No debug/console statements
- [ ] No large files committed
- [ ] Sensitive data not committed
"""

def get_category_checklist(category):
    """Return a specific category checklist."""
    categories = {
        "security": """
## Security Checklist

- [ ] Input validation on all user inputs
- [ ] No SQL injection vulnerabilities (use parameterized queries)
- [ ] No XSS vulnerabilities (escape output, use CSP headers)
- [ ] No hardcoded secrets/passwords/API keys
- [ ] Proper authentication checks
- [ ] Proper authorization checks (RBAC/permissions)
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit (HTTPS)
- [ ] No security misconfigurations
- [ ] Dependencies are secure and up-to-date
- [ ] Rate limiting on public endpoints
- [ ] No sensitive data in logs
- [ ] CORS configured correctly
- [ ] CSRF tokens where applicable
""",
        "performance": """
## Performance Checklist

- [ ] No N+1 query problems
- [ ] Database indexes on queried columns
- [ ] Queries use appropriate indexes
- [ ] No unnecessary loops
- [ ] Lazy loading used where appropriate
- [ ] Caching implemented for expensive operations
- [ ] No memory leaks
- [ ] Connections properly pooled/released
- [ ] Large data sets processed in batches
- [ ] No blocking operations on main thread
- [ ] Compression enabled for large responses
- [ ] Images/assets optimized
- [ ] CDN used for static assets
- [ ] Algorithm complexity reviewed (O(n squared) to O(n))
- [ ] No synchronous file I/O in request path
""",
        "testing": """
## Testing Checklist

### Unit Tests
- [ ] New code has unit tests
- [ ] Happy path is covered
- [ ] Edge cases are covered
- [ ] Error cases are tested
- [ ] Tests are isolated
- [ ] Tests are deterministic (no flakiness)

### Test Quality
- [ ] Test names are descriptive
- [ ] Tests follow AAA pattern (Arrange-Act-Assert)
- [ ] No test logic duplication
- [ ] Test data is realistic
- [ ] Assertions are specific

### Coverage
- [ ] Coverage meets minimum threshold
- [ ] Critical paths have high coverage
- [ ] No untested critical logic

### Integration
- [ ] Key user flows have integration tests
- [ ] API endpoints are tested
- [ ] Database interactions are tested
""",
        "frontend": """
## Frontend Code Review Checklist

### React/Vue/Angular
- [ ] Components are properly separated
- [ ] State management is appropriate
- [ ] No prop drilling
- [ ] Hooks used correctly
- [ ] Memory leaks avoided (event listeners cleaned up)
- [ ] Error boundaries used

### JavaScript/TypeScript
- [ ] Types are properly defined (no 'any' abuse)
- [ ] No console.log/debug statements
- [ ] Promises handled properly
- [ ] Async/await used correctly
- [ ] No blocking main thread
- [ ] Event handlers properly cleaned up

### CSS/Styling
- [ ] CSS is organized
- [ ] No inline styles (unless dynamic)
- [ ] Responsive design considerations
- [ ] No duplicate styles
- [ ] CSS variables used for theming

### Accessibility
- [ ] Semantic HTML used
- [ ] Alt text on images
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Color contrast sufficient
- [ ] ARIA attributes used appropriately
""",
        "backend": """
## Backend Code Review Checklist

### API Design
- [ ] RESTful conventions followed
- [ ] Consistent naming
- [ ] Proper HTTP methods used
- [ ] Status codes are appropriate
- [ ] Pagination implemented for lists
- [ ] API versioning considered

### Data Handling
- [ ] Input validation
- [ ] Output sanitization
- [ ] Transactions used for related operations
- [ ] Database connections pooled
- [ ] Connection strings not hardcoded

### Business Logic
- [ ] Logic is in service layer (not controller)
- [ ] Business rules are centralized
- [ ] Validation is consistent
- [ ] Error handling is consistent
- [ ] Logging is appropriate

### Scalability
- [ ] Stateless where possible
- [ ] Caching strategy defined
- [ ] Queue for async processing
- [ ] Rate limiting considered
""",
        "python": """
## Python Code Review Checklist

### Style (PEP 8)
- [ ] Follows PEP 8 guidelines
- [ ] Import ordering is correct
- [ ] Naming conventions followed
- [ ] Line length under 120 chars

### Type Hints
- [ ] Function arguments typed
- [ ] Return types annotated
- [ ] Complex types handled (List[int], Optional[str])

### Best Practices
- [ ] List/dict comprehensions used appropriately
- [ ] Context managers used (with statements)
- [ ] No bare except clauses
- [ ] F-strings used (not old percent formatting)
- [ ] Type checking with mypy

### Documentation
- [ ] Docstrings for public functions
- [ ] Module docstring at top
- [ ] Complex logic explained
- [ ] README updated if needed
""",
        "javascript": """
## JavaScript/TypeScript Code Review Checklist

### TypeScript
- [ ] Strict mode enabled
- [ ] No 'any' type without justification
- [ ] Interfaces/types properly defined
- [ ] Generics used correctly
- [ ] Enums used for fixed sets

### Async
- [ ] Promises handled correctly
- [ ] Async/await used properly
- [ ] Error handling in async code
- [ ] No missing awaits

### Best Practices
- [ ] Const used where values do not change
- [ ] No console.log left in code
- [ ] No eval() used
- [ ] 'use strict' or ES modules
""",
        "java": """
## Java Code Review Checklist

### Best Practices
- [ ] Try-with-resources used
- [ ] Stream API used appropriately
- [ ] Optional handling correct
- [ ] Null safety considered
- [ ] Immutability where appropriate

### Concurrency
- [ ] Thread-safe collections used
- [ ] Synchronization proper
- [ ] No race conditions
- [ ] ExecutorService properly managed

### Spring (if applicable)
- [ ] @Transactional used correctly
- [ ] @Valid for input validation
- [ ] No @Autowired on fields (use constructor)
""",
        "go": """
## Go Code Review Checklist

### Conventions
- [ ] Error handling follows Go idioms
- [ ] ctx passed through call chain
- [ ] Naming follows Go conventions
- [ ] Error wrapping with percent-w

### Concurrency
- [ ] Goroutines properly cleaned up
- [ ] No goroutine leaks
- [ ] Mutexes used correctly
- [ ] Channels used appropriately
- [ ] WaitGroups/Context for lifecycle

### Best Practices
- [ ] No panics in production code
- [ ] Deferred called in all paths
- [ ] Slices pre-allocated when size known
- [ ] Strings.Builder for concatenation
"""
    }
    return categories.get(category, get_full_checklist())

def get_review_workflow():
    """Return the recommended review workflow."""
    return """
## Code Review Workflow

### Step 1: Context (2-3 min)
Before diving into code:
1. Read PR description and motivation
2. Understand what changed and why
3. Check related issues or documentation
4. Note any related code in the codebase

### Step 2: Overview (3-5 min)
Get the big picture:
1. Scan all changed files
2. Identify high-risk areas
3. Note files needing deep review
4. Consider impact on other parts

### Step 3: Detailed Review (15-30 min)
Follow the checklist by priority:

**Must Fix (Blocking)**:
1. Correctness - does it work?
2. Security - is it safe?
3. Data - no corruption?

**Should Fix (Important)**:
4. Performance issues
5. Error handling
6. Test coverage

**Nice to Have (Suggestions)**:
7. Code style
8. Documentation
9. Code organization

For each issue:
- Comment with specific location (file:line)
- Explain the problem clearly
- Suggest a fix
- Use prefixes: blocking, suggestion, question

### Step 4: Summary (3-5 min)
Wrap up:
1. Summarize all findings
2. Categorize issues by severity
3. List what looks good
4. State recommendation

### Recommendation Options
- **Approve** - Ready to merge
- **Request Changes** - Needs fixes before merge
- **Comment** - Discussion, no blocking issues
- **Approve with Suggestions** - Minor nits, author's call

## Time Allocation

| PR Size | Time | Focus |
|---------|------|-------|
| Small (under 100 lines) | 10-15 min | Quick scan, security, logic |
| Medium (100-500 lines) | 20-30 min | Full checklist |
| Large (500+ lines) | 45-60 min | Architectural impact, split review |

Tip: Reviews over 60 min? Ask to split into smaller PRs.
"""

def generate_review_output(intent, topic=None):
    """Generate appropriate output based on intent."""
    if intent == "checklist":
        return get_full_checklist()
    elif intent == "workflow":
        return get_review_workflow()
    elif intent == "standards":
        return """
## Code Review Standards

### For Your Team

**Establish clear expectations:**

1. **Response Time**
   - First review: within 24 hours
   - Follow-ups: within 4 hours

2. **PR Requirements**
   - Description required
   - Linked issue/ticket
   - Screenshots for UI changes
   - Test plan for complex changes

3. **Review Criteria**
   - Correctness first
   - Security always
   - Performance for large data
   - Style is important but not blocking

4. **Merge Requirements**
   - At least 1 approval
   - All checks passing
   - No unresolved blocking issues

5. **What Reviewers Look For**
   - Does it solve the problem?
   - Is it secure?
   - Will it scale?
   - Is it maintainable?
"""
    elif intent == "prepare":
        return """
## Self-Review Before Submitting

Before requesting a review:

**1. Read your own diff**
Run: git diff HEAD~1 --stat
Then: git diff HEAD~1 (full diff)

**2. Run through this checklist:**
- [ ] Code does what it claims
- [ ] Edge cases handled
- [ ] Error handling in place
- [ ] Tests added/updated
- [ ] No debug code left
- [ ] No secrets committed
- [ ] Documentation updated
- [ ] PR description written

**3. Common issues to catch yourself:**
- console.log/debug statements
- TODO comments left in
- Hardcoded values
- Unused imports/variables
- Code that is commented out
- Missing null checks
- Wrong variable names

**4. Test locally:**
- [ ] Unit tests pass
- [ ] Linting passes
- [ ] Build succeeds
- [ ] Manual testing done

**5. Optimize diff size:**
- Keep PRs small (under 400 lines ideal)
- Group related changes
- Separate refactoring from feature changes
"""
    elif intent == "issues":
        return """
## Common Code Review Issues

### Blocking Issues (Fix Before Merge)
1. **Logic errors** - Code fails to do what it claims
2. **Security vulnerabilities** - SQL injection, XSS, etc.
3. **Data corruption** - Wrong data saved, lost updates
4. **Missing error handling** - Silent failures
5. **No authentication/authorization** - Access control issues
6. **Secrets committed** - API keys, passwords in code

### Important Issues (Should Fix)
1. **N+1 queries** - Performance killer
2. **Missing validation** - Bad input accepted
3. **Inconsistent error handling** - Confusing UX
4. **No tests** - Cannot verify correctness
5. **Memory leaks** - Long-running service issues
6. **Race conditions** - Concurrency bugs

### Suggestions (Nice to Improve)
1. **Code duplication** - DRY it up
2. **Poor naming** - Confusing readers
3. **Missing comments** - Complex logic unexplained
4. **Overly complex** - Hard to maintain
5. **No documentation** - API unclear
6. **Style inconsistencies** - Team standards

### Questions to Ask
- "What happens if X is null?"
- "What if the API call fails?"
- "How will this scale to 1M users?"
- "Is this change backward compatible?"
- "What are the edge cases?"
"""
    elif intent in ["security", "performance", "testing", "frontend", "backend", "python", "javascript", "java", "go"]:
        return get_category_checklist(intent)
    else:
        return """
## Code Review Checklist Tool

### Quick Commands

Full checklist:
  code-review-checklist checklist

Specific category:
  code-review-checklist security
  code-review-checklist performance
  code-review-checklist testing
  code-review-checklist frontend
  code-review-checklist backend

Language specific:
  code-review-checklist python
  code-review-checklist javascript
  code-review-checklist java
  code-review-checklist go

Workflow:
  code-review-checklist workflow

Prepare for review:
  code-review-checklist prepare

Team standards:
  code-review-checklist standards

Common issues:
  code-review-checklist issues

### When to Use

As a Reviewer:
- "Review this PR"
- "Check this code for security issues"
- "What should I look for in this code?"

As a Developer:
- "Help me prepare code for review"
- "Self-review my code"
- "What issues might a reviewer find?"

As a Team Lead:
- "Set up code review standards"
- "What are common issues?"
- "How should we structure reviews?"
"""

def main():
    args = sys.argv[1:]
    
    if not args or (len(args) == 1 and args[0] in ['help', '-h', '--help']):
        print(generate_review_output("general"))
        return
    
    user_input = " ".join(args)
    intent = detect_intent(user_input)
    
    result = generate_review_output(intent)
    print(result)

if __name__ == "__main__":
    main()
