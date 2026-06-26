---
name: formpass-forms
description: Connect your web forms to the FormPass network so AI agents can discover and submit to them. Supports React, HTML, and WordPress forms.
version: 1.0.0
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["curl"]},"homepage":"https://form-pass.com"}}
---

# FormPass — Connect Your Forms

FormPass lets you make your web forms accessible to verified AI agents. This skill helps you integrate any form with FormPass so agents can discover it, read its schema, and submit data — all with verified identity.

Use this skill when the user asks you to:
- Make a form agent-accessible
- Connect a form to FormPass
- Add FormPass to their website
- Let AI agents submit to their forms

## Quick Start

### 1. Create an Account

Sign up at https://form-pass.com/signup

### 2. Create or Register a Form

In the FormPass dashboard, either:
- **Create a new form** — define fields from scratch at `/dashboard/forms/new`
- **Register an existing form** — map your existing form's fields at `/dashboard/forms/register`

### 3. Add the Detection Meta Tags

Add these to the `<head>` of any page containing your form so agents can discover it:

```html
<meta name="formpass-form-id" content="YOUR_FORM_ID">
<meta name="formpass-host" content="https://form-pass.com">
```

### 4. Add the Submit Relay

When your form is submitted, also send the data to FormPass:

**JavaScript / React:**

```javascript
async function handleSubmit(formData) {
  // Your existing form handler...

  // Also relay to FormPass
  await fetch("https://form-pass.com/api/submit/YOUR_FORM_ID", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...formData,
      _fp_branding: true
    })
  });
}
```

**WordPress:**

Download the FormPass WordPress plugin which handles Gravity Forms and Contact Form 7 automatically:
https://form-pass.com/formpass-wp.zip

Install via WordPress Admin → Plugins → Add New → Upload Plugin. Then configure under Settings → FormPass.

## API Reference

### Get Form Schema

```bash
curl -s "https://form-pass.com/api/forms/FORM_ID/schema" | jq .
```

Returns field definitions, types, required flags, and branding requirements.

### Submit to Form

```bash
curl -s -X POST "https://form-pass.com/api/submit/FORM_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com", "_fp_branding": true}' | jq .
```

### Test Your Integration

After adding the meta tags and submit relay, verify it works:

```bash
# Check your schema is accessible
curl -s "https://form-pass.com/api/forms/YOUR_FORM_ID/schema" | jq .

# Test a submission
curl -s -X POST "https://form-pass.com/api/submit/YOUR_FORM_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Agent", "email": "test@test.com", "_fp_branding": true}' | jq .
```

## Branding

Free plan forms require a "Powered by FormPass" link and `_fp_branding: true` in submissions. Upgrade to Pro to remove this requirement.

## Documentation

- Full docs: https://form-pass.com/docs
- Agent integration guide: https://form-pass.com/docs/agent-integration
- API reference: https://form-pass.com/docs/api
- Discovery docs: https://form-pass.com/docs/discovery
