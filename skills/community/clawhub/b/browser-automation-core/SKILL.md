---
name: browser-automation-core
description: Core browser automation library for OpenClaw agents. Provides reusable navigation, interaction, and capture capabilities for both Facet (Onshape learning) and Ace (competition entry). Use when any agent needs to automate web browser interactions.
---

# Browser Automation Core Skill

## Purpose
A reusable browser automation library that provides common web interaction capabilities for multiple OpenClaw agents. Designed to be extended by agent-specific skills while maintaining a single, well-tested core.

## Primary Users
1. **Facet** - Onshape CAD learning automation
2. **Ace** - Competition entry and form filling
3. **Future agents** - Any web automation needs

## Architecture
```
browser-automation-core/          # This skill
├── navigation/                   # URL loading, waiting
├── interaction/                  # Click, type, select
├── capture/                      # Screenshot, HTML capture
├── forms/                        # Form detection and filling
└── sessions/                     # Tab/window management

facets-browser-learning/          # Facet-specific extension
└── uses core + Onshape-specific logic

ace-competition-automation/       # Ace-specific extension  
└── uses core + competition-specific logic
```

## Core Capabilities

### Navigation
- **URL loading** with timeout and retry
- **Wait conditions** (element visible, page loaded)
- **History management** (back, forward, refresh)
- **Tab/window control** (open, close, switch)

### Interaction
- **Element finding** (CSS selectors, XPath, text)
- **Basic actions** (click, type, clear, submit)
- **Mouse operations** (hover, drag, scroll)
- **Keyboard operations** (key presses, shortcuts)

### Capture
- **Screenshots** (full page, element, viewport)
- **HTML capture** (page source, element HTML)
- **Text extraction** (visible text, attributes)
- **Performance metrics** (load times, resources)

### Forms
- **Form detection** (find all forms on page)
- **Field mapping** (match fields to data)
- **Validation** (required fields, formats)
- **Submission** (submit buttons, AJAX handling)

### Sessions
- **Cookie management** (save/load sessions)
- **Authentication state** (login persistence)
- **Profile management** (user agent, viewport)
- **Cleanup** (close browsers, clear data)

## Quick Start

### Installation
```bash
# Install from ClawHub (when published)
npx clawhub@latest install browser-automation-core

# Or use local development version
cp -r /path/to/skill /root/.openclaw/workspace/skills/
```

### Basic Usage
```python
# Example: Navigate and take screenshot
from browser_core import BrowserAutomation

browser = BrowserAutomation()
browser.navigate("https://example.com")
browser.take_screenshot("example.png")
browser.close()
```

### Agent-Specific Examples

#### For Facet (Onshape Learning)
```python
from browser_core import BrowserAutomation
from facets_onshape import OnshapeAutomation

browser = BrowserAutomation()
onshape = OnshapeAutomation(browser)

# Login to Onshape
onshape.login(email="facet.ai.oc@gmail.com", password="***")

# Navigate to tutorials
onshape.navigate_to_tutorial("getting-started")

# Complete tutorial steps
onshape.complete_tutorial_step(1)
onshape.take_progress_screenshot()
```

#### For Ace (Competition Entry)
```python
from browser_core import BrowserAutomation
from ace_competition import CompetitionAutomation

browser = BrowserAutomation()
competition = CompetitionAutomation(browser)

# Navigate to competition
competition.navigate_to_competition("https://competition.example.com")

# Fill entry form
entry_data = {
    "name": "Stef Ferreira",
    "email": "ace@supplystoreafrica.com",
    "phone": "+27726386189"
}
competition.fill_entry_form(entry_data)

# Submit and capture proof
competition.submit_entry()
competition.capture_submission_proof()
```

## Configuration

### Environment Variables
```bash
# Browser settings
export BROWSER_HEADLESS="true"           # Run without display
export BROWSER_TIMEOUT="30"              # Default timeout seconds
export BROWSER_VIEWPORT="1280,720"       # Window size
export BROWSER_USER_AGENT="OpenClaw Agent" # Custom user agent

# CDP settings (OpenClaw browser)
export CDP_URL="http://localhost:18800/json"
export CDP_WEBSOCKET="ws://localhost:18800/devtools/page/..."

# Storage settings
export SCREENSHOT_DIR="/path/to/screenshots"
export SESSION_DIR="/path/to/sessions"
```

### OpenClaw Integration
```json5
{
  "skills": {
    "browser-automation-core": {
      "enabled": true,
      "config": {
        "cdpUrl": "http://localhost:18800/json",
        "headless": true,
        "timeout": 30,
        "screenshotDir": "/root/.openclaw/workspace/screenshots"
      }
    }
  }
}
```

## Implementation Details

### CDP (Chrome DevTools Protocol)
This skill uses OpenClaw's built-in browser via CDP:
- **Connection**: WebSocket to `ws://localhost:18800/devtools/page/...`
- **Commands**: Standard CDP methods (Page.navigate, DOM.querySelector, etc.)
- **Events**: Async event handling for page loads, network requests

### Error Handling
- **Retry logic**: Automatic retry on network failures
- **Timeout management**: Configurable timeouts per operation
- **Fallback strategies**: Alternative selectors, different interaction methods
- **Recovery procedures**: Page reload, session restore

### Performance
- **Connection pooling**: Reuse WebSocket connections
- **Command batching**: Batch CDP commands when possible
- **Caching**: Cache page structure, element positions
- **Parallel operations**: Async operations where safe

## Extension Points

### Creating Agent-Specific Extensions

#### 1. Create Extension Skill
```bash
python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/init_skill.py facets-browser-learning
```

#### 2. Import Core Library
```python
# In extension skill
import sys
sys.path.append("/root/.openclaw/workspace/skills/browser-automation-core")
from browser_core import BrowserAutomation

class OnshapeAutomation:
    def __init__(self):
        self.browser = BrowserAutomation()
    
    def onshape_specific_method(self):
        # Use core capabilities
        self.browser.navigate("https://cad.onshape.com")
        # Add Onshape-specific logic
```

#### 3. Add Specialized Logic
- Site-specific selectors (Onshape CSS classes, competition form fields)
- Domain-specific workflows (tutorial navigation, competition rules)
- Custom capture requirements (progress tracking, entry proof)
- Error handling for specific sites

## Testing Strategy

### Unit Tests
```bash
# Test core functionality
cd /root/.openclaw/workspace/skills/browser-automation-core
python3 -m pytest tests/unit/
```

### Integration Tests
```bash
# Test with actual browser
python3 tests/integration/test_navigation.py
python3 tests/integration/test_forms.py
```

### Agent-Specific Tests
```bash
# Test Facet extension
cd /root/.openclaw/workspace/skills/facets-browser-learning
python3 tests/test_onshape_automation.py

# Test Ace extension  
cd /root/.openclaw/workspace/skills/ace-competition-automation
python3 tests/test_competition_automation.py
```

## Common Use Cases

### Use Case 1: Form Filling (Ace)
```python
# Competition entry automation
data = {
    "full_name": "Stef Ferreira",
    "email": "ace@supplystoreafrica.com",
    "phone": "+27726386189",
    "address": "123 Street, City, South Africa"
}

browser.navigate(competition_url)
browser.fill_form("form#entry-form", data)
browser.click("button[type='submit']")
browser.wait_for_element(".success-message")
browser.take_screenshot("entry_proof.png")
```

### Use Case 2: Tutorial Navigation (Facet)
```python
# Onshape learning automation
browser.navigate("https://cad.onshape.com")
browser.login(credentials)  # Custom method in extension
browser.navigate("/learning/tutorials")

# Complete tutorial
tutorial_steps = browser.extract_tutorial_steps()
for step in tutorial_steps:
    browser.complete_step(step)  # Custom method
    browser.take_screenshot(f"step_{step.number}.png")
    
browser.capture_certificate()
```

### Use Case 3: Multi-Page Workflow
```python
# Complex automation across multiple pages
browser.open_new_tab()
browser.navigate_to_login()
browser.login(credentials)

browser.switch_to_tab(0)
browser.fill_application_form(data)

browser.switch_to_tab(1)
browser.verify_email_confirmation()

browser.capture_all_tabs_screenshots()
```

## Error Recovery Patterns

### CORS Issues (Screenshots/Evaluate Not Working)
**Problem:** Browser automation fails with CORS errors when taking screenshots or evaluating JavaScript.

**Solution:** Ensure browser is started with `--remote-allow-origins=*` flag:
```bash
# Browser startup command must include:
--remote-debugging-port=18800 --remote-allow-origins=*
```

**Verification:**
```bash
curl http://localhost:18800/json/version
# Should return browser info without CORS errors
```

### Network Issues
```python
try:
    browser.navigate(url)
except NetworkError:
    browser.reload()
    browser.wait_for_network_idle()
    # Retry operation
```

### Element Not Found
```python
# Try multiple selectors
selectors = [
    "button.submit",
    "input[type='submit']",
    ".submit-button",
    "//button[contains(text(), 'Submit')]"
]

for selector in selectors:
    if browser.element_exists(selector):
        browser.click(selector)
        break
```

### Form Validation Errors
```python
browser.submit_form()
if browser.has_validation_errors():
    errors = browser.get_validation_errors()
    for field, message in errors:
        browser.fix_field(field, message)
    browser.submit_form()  # Retry
```

## Performance Optimization

### Batch Operations
```python
# Instead of sequential commands
browser.click("button1")
browser.click("button2")
browser.type("input1", "text")

# Use batch commands
commands = [
    {"method": "click", "selector": "button1"},
    {"method": "click", "selector": "button2"},
    {"method": "type", "selector": "input1", "text": "text"}
]
browser.execute_batch(commands)
```

### Caching Strategies
```python
# Cache page structure
if not browser.has_cached_structure(url):
    structure = browser.extract_page_structure()
    browser.cache_structure(url, structure)

# Use cached selectors
selectors = browser.get_cached_selectors(url)
```

## Security Considerations

### Credential Management
- Never hardcode credentials in scripts
- Use environment variables or secure storage
- Implement credential rotation
- Log credential usage (without exposing values)

### Session Isolation
- Separate browser sessions per agent
- Clear cookies and storage between sessions
- Use incognito/private mode when possible
- Implement session timeout

### Input Validation
- Validate all user inputs before browser interaction
- Sanitize URLs to prevent navigation to malicious sites
- Limit file system access from browser
- Monitor for suspicious behavior

## Maintenance

### Versioning
- Semantic versioning (MAJOR.MINOR.PATCH)
- Backward compatibility for minor versions
- Deprecation warnings for breaking changes
- Migration guides between major versions

### Updates
- Monthly security updates
- Quarterly feature updates
- Annual architecture reviews
- Continuous integration testing

### Monitoring
- Usage statistics (which agents use which features)
- Error rates and common failures
- Performance metrics (load times, success rates)
- Agent-specific success tracking

## Contributing

### Adding New Features
1. Check if feature belongs in core or extension
2. Write tests for new functionality
3. Update documentation
4. Submit pull request

### Reporting Issues
1. Include agent context (Facet, Ace, etc.)
2. Provide reproduction steps
3. Include screenshots/logs
4. Suggest possible solutions

### Extension Development
1. Follow core API patterns
2. Reuse existing utilities when possible
3. Write agent-specific tests
4. Document extension capabilities

## References

### CDP Documentation
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [OpenClaw Browser Integration](/docs/browser-integration)
- [WebSocket Client Examples](/examples/websocket)

### Related Skills
- `facets-browser-learning` - Facet extension
- `ace-competition-automation` - Ace extension
- `browser-testing` - Testing utilities

### External Resources
- [Puppeteer Documentation](https://pptr.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Selenium Documentation](https://www.selenium.dev/)

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-30  
**Maintainer**: Bob (OpenClaw Agent)  
**License**: MIT  
**Status**: Active Development