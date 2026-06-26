# Agent Browser Skill

## Description
Enhanced browser automation for OpenClaw agents with advanced navigation, screenshot, and interaction capabilities.

## When to Use
Use this skill when:
- Automating web browsing tasks
- Taking screenshots of web pages
- Filling forms and clicking buttons
- Extracting data from websites
- Testing web applications
- Navigating complex web flows

## Prerequisites
- OpenClaw browser tool must be enabled
- Chrome or Chromium browser installed
- Internet connection for web access

## Examples

### Basic Navigation
```bash
# Navigate to a website
openclaw browser open --url "https://example.com"

# Take a screenshot
openclaw browser snapshot --url "https://example.com" --output screenshot.png
```

### Form Interaction
```bash
# Fill a form
openclaw browser act --url "https://forms.example.com" --kind fill --fields '{"name": "John", "email": "john@example.com"}'

# Click a button
openclaw browser act --url "https://example.com" --kind click --selector "button.submit"
```

### Data Extraction
```bash
# Extract page content
openclaw browser snapshot --url "https://news.example.com" --maxChars 5000

# Monitor page changes
openclaw browser act --url "https://status.example.com" --kind wait --textGone "Loading..."
```

## Integration with OpenClaw

This skill enhances the native OpenClaw browser tool with:
1. **Simplified commands** - Easier syntax for common tasks
2. **Error handling** - Better recovery from failures
3. **Performance optimization** - Faster page loads and interactions
4. **Accessibility support** - Better element detection

## Safety Notes
- Only automate public websites
- Respect robots.txt and terms of service
- Avoid excessive requests to prevent IP blocking
- Use delays between actions to mimic human behavior

## Troubleshooting

### Common Issues
1. **Browser not starting**: Check if Chrome is installed
2. **Element not found**: Try different selectors or wait for page load
3. **Timeout errors**: Increase timeout values for slow pages
4. **Permission denied**: Ensure OpenClaw has necessary permissions

### Debug Tips
```bash
# Enable verbose logging
openclaw browser open --url "https://example.com" --verbose

# Check browser status
openclaw browser status
```

## References
- [OpenClaw Browser Documentation](https://docs.openclaw.ai/tools/browser)
- [Playwright Automation Guide](https://playwright.dev/docs/automation)
- [Web Scraping Best Practices](https://docs.openclaw.ai/automation/web-scraping)