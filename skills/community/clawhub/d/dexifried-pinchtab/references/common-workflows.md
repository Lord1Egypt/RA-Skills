# Common Workflows

This document shows automation patterns with PinchTab.

## 1. Login Automation
Automate login to a service:
1. Navigate to the login page.
2. Use the `/fill` API to populate the username and password fields.
3. Submit the form with `/click`.

## 2. Form Filling
Populate forms programmatically:
1. Navigate to the form page.
2. Send `/fill` requests for each input field.
3. Submit the form with `/click`.

## 3. Data Extraction
Extract texts or data from loaded pages:
1. Use `/navigate` to access the page.
2. Send `/snapshot` with `format=json` to retrieve the structure.