# Browser Automation Workflow Example

## Scenario: Login and Extract Data

This example demonstrates a complete browser automation workflow using OpenClaw's browser hosting capabilities.

### Step 1: Start Browser and Navigate
```bash
# Start the browser
openclaw browser --browser-profile openclaw start

# Navigate to login page
openclaw browser --browser-profile openclaw open https://example.com/login
```

### Step 2: Take Initial Snapshot
```bash
# Get interactive snapshot to identify form elements
openclaw browser --browser-profile openclaw snapshot --interactive
```

Expected output might include:
```
[ref=i1] Username input
[ref=i2] Password input  
[ref=e3] Login button
```

### Step 3: Fill Form and Submit
```bash
# Fill username field
openclaw browser --browser-profile openclaw type i1 "myusername"

# Fill password field  
openclaw browser --browser-profile openclaw type i2 "mypassword" --submit

# Alternative: Click login button
# openclaw browser --browser-profile openclaw click e3
```

### Step 4: Wait for Navigation and Verify
```bash
# Wait for dashboard to load
openclaw browser --browser-profile openclaw wait --url "**/dashboard" --load networkidle

# Verify successful login
openclaw browser --browser-profile openclaw snapshot --interactive
```

### Step 5: Extract Required Data
```bash
# Take snapshot of data table
openclaw browser --browser-profile openclaw snapshot --selector "#data-table" --interactive

# Extract specific information using evaluate
openclaw browser --browser-profile openclaw evaluate --fn "(el) => el.textContent" --ref t12
```

### Step 6: Clean Up
```bash
# Close browser
openclaw browser --browser-profile openclaw stop
```

## Error Handling Patterns

### Handle Dynamic Content
```bash
# Wait for element to appear before snapshotting
openclaw browser --browser-profile openclaw wait "button#submit" --timeout-ms 10000

# Retry pattern with error checking
MAX_RETRIES=3
for i in $(seq 1 $MAX_RETRIES); do
    if openclaw browser --browser-profile openclaw snapshot --interactive | grep -q "success"; then
        break
    fi
    sleep 2
done
```

### Debugging Failed Actions
```bash
# When click fails, highlight to verify target
openclaw browser --browser-profile openclaw highlight e12

# Check for JavaScript errors
openclaw browser --browser-profile openclaw errors --clear

# Monitor network requests
openclaw browser --browser-profile openclaw requests --filter api --clear
```

## Advanced Patterns

### Multi-Step Form with Validation
```bash
# Step through multi-page form
openclaw browser --browser-profile openclaw open https://example.com/form

# Page 1: Basic info
openclaw browser --browser-profile openclaw snapshot --interactive
openclaw browser --browser-profile openclaw type i1 "John"
openclaw browser --browser-profile openclaw type i2 "Doe"
openclaw browser --browser-profile openclaw click e3  # Next button

# Page 2: Contact info  
openclaw browser --browser-profile openclaw wait --url "**/form/contact"
openclaw browser --browser-profile openclaw snapshot --interactive
openclaw browser --browser-profile openclaw type i4 "john@example.com"
openclaw browser --browser-profile openclaw click e5  # Submit button

# Verify completion
openclaw browser --browser-profile openclaw wait --text "Form submitted successfully"
```

### File Upload Workflow
```bash
# Prepare file upload
openclaw browser --browser-profile openclaw upload /path/to/file.pdf

# Trigger file selection dialog
openclaw browser --browser-profile openclaw click e12

# Wait for upload completion
openclaw browser --browser-profile openclaw wait --text "Upload complete"
```

This workflow template can be adapted for various web automation scenarios while maintaining reliability and proper error handling.