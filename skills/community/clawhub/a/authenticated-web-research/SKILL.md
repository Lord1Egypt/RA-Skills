---
name: authenticated-web-research
description: Use stronger lawful workflows for sites the user is authorized to access, including local browser login, session-aware browsing, JS-heavy pages, and post-login extraction. Do not bypass access controls.
---

# Authenticated Web Research

Use this skill when the target site requires login, renders content dynamically, or is available only after the user signs in with their own account.

## Hard Rule

Do not bypass access controls, paywalls, or anti-bot protections.

This skill is for user-authorized access only:

- the user logs in with their own account
- the browser session stays local
- extraction continues only after access is legitimately available

## When To Use

- direct fetch returns login pages or partial shells
- search results show content exists, but direct fetch is blocked
- the site depends on client-side rendering
- the user explicitly wants help with a site they can access themselves

## Workflow

### 1. Diagnose the failure mode

Classify the blocker:

- login required
- JS-heavy rendering
- geo or locale mismatch
- thin snippet-only indexing
- temporary fetch incompatibility

### 2. Use browser-based loading

Before concluding the page is unavailable:

- open the page in the local browser
- wait for client-side content to render
- inspect visible text, links, and network behavior where appropriate
- prefer the browser path over plain fetch for JS-heavy pages

### 3. Let the user complete login locally

If login is required and the user is authorized:

- open the login flow in the local browser
- ask only for the minimum interaction needed, such as "please complete login in the opened page"
- do not ask for raw passwords or secrets in chat when browser login is possible

### 4. Continue within the authenticated session

After user login:

- navigate to the target page
- search within the site or account area
- extract the needed facts, links, or structured results
- note which facts came from authenticated views

### 5. Prefer official post-login surfaces

If available, prefer:

- account dashboards
- export pages
- official APIs
- RSS or feeds
- site search
- sitemaps
- downloadable reports

## Output Pattern

Return:

1. what was reachable publicly
2. what required authenticated access
3. whether the user completed login locally
4. what was extracted after authorized access
5. what still remains unavailable
