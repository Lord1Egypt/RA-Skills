---
name: authorized-session-scrape
description: Continue searching and extracting within a user-authorized local browser session after the user logs in. Use for pagination, site search, tab-by-tab extraction, and post-login discovery without bypassing access controls.
---

# Authorized Session Scrape

Use this skill when the user has legitimate access and the work should continue inside their own logged-in browser session.

## Hard Rule

Do not bypass login or session controls.

This skill begins only after:

- the user confirms they want to proceed
- the login flow is opened locally
- the user completes sign-in themselves

## Best Use Cases

- account-only pages
- post-login search or filtering
- paginated dashboards or content libraries
- collections where one page is not enough
- workflows where plain fetch misses the authenticated state

## Workflow

### 1. Open the user session

- use the local browser path
- navigate to the target area
- if needed, prompt the user to finish login in the browser

### 2. Verify real access

Before scraping deeply, confirm:

- account home or target page is visible
- search box, filters, or result list are actually present
- content is not still hidden behind a modal or loading shell

### 3. Expand within the site

Once logged in:

- use the site's own search
- apply filters, sorting, and date ranges when helpful
- open multiple relevant items or tabs
- continue through pagination until results become repetitive or low-value

### 4. Extract systematically

Track internally:

- which sections were searched
- what filters were applied
- which pages or tabs produced useful signal
- where the session still limits access

### 5. Summarize with provenance

Distinguish:

- facts seen in public pages
- facts seen only after authenticated login
- what still requires manual action by the user

## Output Pattern

Return:

1. where you searched inside the logged-in session
2. what filters or navigation paths were used
3. what the strongest results were
4. what remains partial or unavailable
5. what next click path you would use if continuing
