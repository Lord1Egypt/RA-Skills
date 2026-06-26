---
name: interact
description: Click buttons, type text, fill forms, scroll pages, and interact with web page elements. Use when the user wants to click something, fill in a form, type into an input, press a button, submit a form, scroll a page, select an option, log in to a website, or perform any interactive web action. 点击按钮、输入文字、填写表单、滚动页面、登录网站、提交表单、选择选项、拖拽元素、网页操作。
allowed-tools: Bash, Read, Write
---

# Interact

Perform interactive actions on web pages.

## Core Pattern: Observe → Act → Verify

### 1. Observe
- Read the DOM to find the target element and its coordinates
- Or capture a screenshot to see the current state

### 2. Act
- **Click**: at the element's pixel coordinates
- **Type**: click the input field first, then type text
- **Key press**: press Enter, Tab, Escape, etc.
- **Scroll**: scroll up/down/left/right by a given amount
- **Drag**: from one coordinate to another

### 3. Verify
- Capture a screenshot to confirm the action worked

## Common Patterns

### Click a Button
1. Read DOM → find button by label → get coordinates
2. Click at those coordinates
3. Screenshot to verify

### Fill a Form
1. Read DOM → identify all input fields
2. For each field: click it → type the value → Tab to next
3. Click submit button
4. Screenshot to verify result

### Login Flow
1. Navigate to login page
2. Find username field → click → type username
3. Find password field → click → type password
4. Click login button
5. Screenshot to verify success

## Important

- **Always observe before acting** — get DOM or screenshot first
- **Always verify after acting** — screenshot to confirm
- **Coordinate-based** — clicking uses pixel coordinates, not CSS selectors

Refer to [browser-context](../browser-context/SKILL.md) for available tools per backend.
