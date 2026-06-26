# Strict Safety Rules

To protect the user's CSDN account and comply with platform terms of service, this automation script strictly adheres to the following boundaries.

## 🔴 ABSOLUTELY PROHIBITED ACTIONS (DO NOT DO)

1. **NO Automated Publishing**: The script MUST NEVER click the final "Publish" (发布) button.
2. **NO Headless Execution**: The script MUST NEVER run in `headless=True` mode. The user must always see what is happening.
3. **NO Credential Harvesting**: The script MUST NEVER ask for, read, or save the user's CSDN username or password.
4. **NO Session Hijacking**: The script MUST NEVER read, extract, save, export, or print `document.cookie`, `localStorage`, `sessionStorage`, or Playwright's `storage_state`. 
5. **NO Background Requests**: The script MUST NEVER use CSDN's internal API endpoints (e.g., `POST /api/publish`) to bypass the frontend UI.
6. **NO CAPTCHA Bypassing**: The script MUST NEVER use external services or ML models to solve CAPTCHAs, sliders, or SMS verifications.
7. **NO Mass Action**: The script is strictly designed for 1-to-1 processing. It MUST NOT loop through arrays of accounts or bulk-publish articles.
8. **NO Interaction Farming**: The script MUST NOT auto-like, auto-comment, or auto-follow.

## 🟢 PERMITTED ACTIONS (SAFE TO DO)

1. **Open Pages**: Open `https://editor.csdn.net/md/`.
2. **Type Text**: Type strings into standard input fields (`<input>`, `<textarea>`, `<div contenteditable="true">`) IF they are related to drafting an article.
3. **Wait for User**: Pause execution (`page.wait_for_timeout` or similar) to allow the user to complete login or verification.
4. **Close Browser**: Exit safely when the process is done or the user closes the window.

Any modification to `scripts/draft_to_csdn.example.py` must be audited against these rules. If a modification violates a rule, it must be rejected.
