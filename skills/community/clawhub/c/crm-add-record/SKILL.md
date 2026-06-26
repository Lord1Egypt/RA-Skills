---
name: crm-add-record
description: Automate adding new CRM records to the Fractal CRM system. Use when user asks to add new CRM entries, customers, or sales leads. The skill handles navigation, login, intelligent field mapping from natural language input, and form submission.
allowed-tools: Bash(agent-browser:*)
---

# CRM新增记录

## Quick Start

Add a new CRM record from user input:
```bash
# User input: "13608847308，蒋女士，云南，体育馆票务系统。"
crm-add-record "13608847308，蒋女士，云南，体育馆票务系统。"
```

## Workflow

### 1. Open CRM Page
Navigate to the CRM modification page:
```bash
agent-browser open https://niw26kl7.fractaltest.cn/Crm/Backend/modify.html
```

### 2. Handle Login (if required)
Check if on login page:
```bash
agent-browser get url
```

If URL contains "login.html", perform login:
```bash
agent-browser snapshot -i
# Fill credentials: username="weiyj", password="weiyj123"
agent-browser fill @<username_field> "weiyj"
agent-browser fill @<password_field> "weiyj123"
agent-browser click @<login_button>
agent-browser wait --load networkidle
```

### 3. Parse User Input
Analyze the user's input string to extract information:

**Input format examples:**
- "13608847308，蒋女士，云南，体育馆票务系统。"
- "13800138000 张三 北京 软件开发"
- "13912345678 李先生 上海 咨询服务"

**Extract patterns:**
- **Phone number**: 11-digit mobile number starting with 1
- **Contact name**: Name with or without title (先生/女士)
- **Region**: City or province name
- **Project/Basic info**: Remaining text or last sentence

**Fallback strategy:**
If parsing fails or fields are ambiguous, place all input content in the "Basic Info" field.

### 4. Fill Form Fields
Get page elements:
```bash
agent-browser snapshot -i
```

Map extracted data to fields:
- Phone number → 手机号码输入框
- Contact name → 联系人输入框
- Region → 地区选择框
- Project info → 基础情况输入框

Fill fields using refs from snapshot:
```bash
agent-browser fill @<phone_field> "<phone_number>"
agent-browser fill @<contact_field> "<contact_name>"
agent-browser fill @<region_field> "<region>"
agent-browser fill @<basic_info_field> "<project_info>"
```

### 5. Submit Form
Click the save button:
```bash
agent-browser click @<save_button>
agent-browser wait --load networkidle
```

### 6. Verify Success
Check for success indicators:
```bash
agent-browser get url
agent-browser snapshot -i
```

Look for confirmation messages or redirect to list page.

## Field Mapping Reference

### Common Input Patterns

| Input Example | Phone | Contact | Region | Basic Info |
|--------------|-------|---------|--------|------------|
| "13608847308，蒋女士，云南，体育馆票务系统。" | 13608847308 | 蒋女士 | 云南 | 体育馆票务系统 |
| "13800138000 张三 北京" | 13800138000 | 张三 | 北京 | (empty) |
| "咨询李经理，上海地区" | (empty) | 李经理 | 上海 | 咨询 |

### Regex Patterns

```python
phone_pattern = r"1[3-9]\d{9}"
contact_pattern = r"([\u4e00-\u9fa5]{1,3})(?:先生|女士)?"
region_pattern = r"([\u4e00-\u9fa5]{2,4}(?:省|市|区|县)?)"
```

## Troubleshooting

### Login fails
- Verify credentials are correct: weiyj / weiyj123
- Check for CAPTCHA or 2FA requirements
- Try manual login to confirm credentials work

### Field not found
- Use `agent-browser snapshot` to get current page elements
- Check if page is fully loaded: `agent-browser wait --load networkidle`
- Verify field names may have changed

### Parsing fails
- If uncertain, place all input in "Basic Info" field
- Ask user to clarify field mapping
- Manual entry for complex cases

### Submit button unclickable
- Check for validation errors on form fields
- Ensure required fields are filled
- Wait for page to fully load before clicking

## Examples

### Example 1: Complete information
```
User: "新增CRM：13608847308，蒋女士，云南，体育馆票务系统。"
Action:
1. Navigate to CRM page
2. Login if needed
3. Extract: Phone=13608847308, Contact=蒋女士, Region=云南, Info=体育馆票务系统
4. Fill all fields
5. Click save
```

### Example 2: Minimal information
```
User: "添加CRM记录：13800138000，北京软件开发"
Action:
1. Navigate to CRM page
2. Login if needed
3. Extract: Phone=13800138000, Region=北京, Info=软件开发
4. Fill available fields
5. Click save
```

### Example 3: Ambiguous input
```
User: "新增：咨询需求，广州李总"
Action:
1. Navigate to CRM page
2. Login if needed
3. Extract: Contact=李总, Region=广州, Info=咨询需求
4. Fill available fields
5. Click save
```

## Notes

- Always verify page state with `snapshot` before interacting with elements
- Use `wait --load networkidle` after navigation and login
- Element refs (e.g., @e1, @e2) change after page reload
- Fallback to filling all input in "Basic Info" if parsing is uncertain
- Test the workflow first to ensure field names match actual page
