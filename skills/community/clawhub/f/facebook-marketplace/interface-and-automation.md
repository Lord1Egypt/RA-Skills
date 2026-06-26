# Interface and Automation - Facebook Marketplace

Use this when the user asks what can be done on web, mobile, API, CLI, or automation.

## Surface Map

Treat Marketplace as three different surfaces:

### 1. Public Web

Useful for:
- opening the Marketplace landing page
- browsing categories and locations
- opening public item pages
- collecting read-only context from public listings

This is the safest surface for browser-assisted research.

### 2. Signed-In Web

Useful for:
- managing listings
- messaging through Marketplace threads
- checking account and seller workflows that depend on login

Do not assume every mobile feature exists here.

### 3. Mobile App

Treat mobile as the place where feature availability may differ.
If the user is asking about ratings, shipping, checkout, or reporting flows, verify whether their account and surface actually support it.

## API and CLI Reality

Default assumption:
- there is no documented public Marketplace API from Meta for consumer buying and selling flows
- there is no official Marketplace CLI for consumer listing, messaging, or transaction actions

Therefore:
- do not invent Graph API endpoints
- do not promise scripted posting or message automation
- do not model Marketplace like an open ecommerce platform

## Safe Automation Boundary

Allowed only with explicit user approval:
- read-only browser automation on public pages
- structured note-taking from public listings
- local comparison tables built from user-approved listing data

High-risk or refused:
- logged-in scraping at scale
- mass messaging
- auto-posting or reposting
- account farming, anti-detection, or restriction bypass

## Practical Recommendation

When the user wants results fast:
- use manual or assistive mode for signed-in actions
- use read-only research mode for public listing scans
- keep all irreversible actions behind explicit confirmation

If the workflow depends on unsupported automation, redesign the workflow instead of forcing the tool.
