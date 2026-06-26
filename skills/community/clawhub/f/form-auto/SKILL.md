---
name: form-auto
description: Universal form auto-fill tool for OpenClaw. Use when user needs to fill out web forms automatically. Supports job applications, registrations, surveys, and any web form. Requires OpenClaw v2026.3.22+ with browser access. 表单自动填写、一键填表、自动填报。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📝", "requires": {"bins": ["python3"], "env": []}, "minVersion": "2026.3.22", "needsBrowser": true}}
---

# Form Auto

Universal web form auto-fill tool. Automatically fills out any web form using OpenClaw's browser automation.

## Features

- 📝 **Universal Form Fill**: Works with any web form
- 🔐 **Browser Session**: Uses existing login state
- 🎯 **Smart Detection**: Auto-detects form fields
- 📋 **Template Support**: Save and reuse form data
- 🌍 **Multi-Language**: Supports Chinese and English
- ⚡ **Fast & Accurate**: Reliable form filling

## Trigger Conditions

- "帮我填表" / "Help me fill out this form"
- "自动填写报名表" / "Auto-fill registration form"
- "填写求职申请" / "Fill job application"
- "填写问卷" / "Fill out survey"
- "form-auto [url]"

---

## ⚠️ Privacy Warning

**This skill accesses your browser profile to fill forms.**

- 🔐 Reads browser session to access forms
- 📝 Fills form fields with your data
- 🌐 Interacts with websites on your behalf
- ⚠️ Only use on trusted websites

---

## Step 1: Get User Information

Ask user for the information needed to fill the form:

```
请提供需要填写的信息：

基本信息：
- 姓名: ___
- 手机号: ___
- 邮箱: ___
- 地址: ___

其他信息（根据表单）：
- 公司: ___
- 职位: ___
- 备注: ___
```

Or use saved profile from previous sessions.

---

## Step 2: Open Form URL

```javascript
// Open the form page
await browser.open({
  url: "https://example.com/form"
})

// Wait for page load
await browser.wait({ timeout: 5000 })
```

---

## Step 3: Detect Form Fields

```javascript
// Detect all form fields on the page
const formFields = await browser.evaluate(() => {
  const fields = []
  
  // Find all input elements
  document.querySelectorAll('input, select, textarea').forEach(el => {
    const field = {
      type: el.type || el.tagName.toLowerCase(),
      name: el.name || '',
      id: el.id || '',
      placeholder: el.placeholder || '',
      label: '',
      required: el.required
    }
    
    // Try to find associated label
    if (el.id) {
      const label = document.querySelector(`label[for="${el.id}"]`)
      if (label) field.label = label.innerText.trim()
    }
    
    // Or find parent label
    if (!field.label) {
      const parentLabel = el.closest('label')
      if (parentLabel) field.label = parentLabel.innerText.trim()
    }
    
    // Or use placeholder as label
    if (!field.label && el.placeholder) {
      field.label = el.placeholder
    }
    
    fields.push(field)
  })
  
  return fields
})

console.log("检测到的表单字段:", formFields)
```

---

## Step 4: Fill Form Fields

```javascript
// Fill each field based on type and label
async function fillForm(userData) {
  for (const field of formFields) {
    const value = matchFieldToData(field, userData)
    
    if (value) {
      // Fill input/textarea
      if (field.type === 'text' || field.type === 'email' || 
          field.type === 'tel' || field.type === 'textarea') {
        await browser.evaluate((id, name, val) => {
          const el = id ? document.getElementById(id) : 
                     document.querySelector(`[name="${name}"]`)
          if (el) {
            el.value = val
            el.dispatchEvent(new Event('input', { bubbles: true }))
            el.dispatchEvent(new Event('change', { bubbles: true }))
          }
        }, field.id, field.name, value)
      }
      
      // Fill select
      if (field.type === 'select-one') {
        await browser.evaluate((id, name, val) => {
          const el = id ? document.getElementById(id) : 
                     document.querySelector(`[name="${name}"]`)
          if (el) {
            el.value = val
            el.dispatchEvent(new Event('change', { bubbles: true }))
          }
        }, field.id, field.name, value)
      }
      
      // Fill checkbox/radio
      if (field.type === 'checkbox' || field.type === 'radio') {
        if (value === 'true' || value === true) {
          await browser.evaluate((id, name) => {
            const el = id ? document.getElementById(id) : 
                       document.querySelector(`[name="${name}"]`)
            if (el && !el.checked) {
              el.click()
            }
          }, field.id, field.name)
        }
      }
    }
  }
}
```

---

## Step 5: Smart Field Matching

```python
def match_field_to_data(field, user_data):
    """Match form field to user data based on label/name"""
    
    label = (field.get('label', '') + ' ' + 
             field.get('name', '') + ' ' + 
             field.get('placeholder', '')).lower()
    
    # Name matching
    if any(kw in label for kw in ['姓名', '名字', 'name', '称呼']):
        return user_data.get('name', '')
    
    # Phone matching
    if any(kw in label for kw in ['手机', '电话', 'phone', 'tel', 'mobile']):
        return user_data.get('phone', '')
    
    # Email matching
    if any(kw in label for kw in ['邮箱', 'email', 'mail']):
        return user_data.get('email', '')
    
    # Address matching
    if any(kw in label for kw in ['地址', 'address', '住址']):
        return user_data.get('address', '')
    
    # Company matching
    if any(kw in label for kw in ['公司', 'company', '单位', '组织']):
        return user_data.get('company', '')
    
    # Position matching
    if any(kw in label for kw in ['职位', 'position', '岗位', '职务']):
        return user_data.get('position', '')
    
    # ID card matching
    if any(kw in label for kw in ['身份证', 'id card', '证件']):
        return user_data.get('id_card', '')
    
    return None
```

---

## Step 6: Confirm & Submit

```javascript
// Show filled form summary to user
const summary = await browser.evaluate(() => {
  const filled = []
  document.querySelectorAll('input, select, textarea').forEach(el => {
    if (el.value) {
      filled.push({
        label: el.placeholder || el.name || el.id,
        value: el.value
      })
    }
  })
  return filled
})

// Ask user to confirm
console.log("已填写的字段:")
summary.forEach(item => {
  console.log(`  ${item.label}: ${item.value}`)
})

// Wait for user confirmation before submit
// await browser.click({ selector: 'button[type="submit"]' })
```

---

## Template System

Save commonly used form data:

```json
{
  "profile_name": "个人信息",
  "data": {
    "name": "张三",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "address": "北京市朝阳区xxx",
    "company": "xxx科技有限公司",
    "position": "产品经理"
  }
}
```

---

## Example Usage

### 求职申请表

```
User: "帮我填写这个求职申请表，网址是 https://company.com/apply"

Agent:
1. 打开网址
2. 检测表单字段
3. 询问用户信息（或使用保存的模板）
4. 自动填写
5. 展示填写结果
6. 等待用户确认提交
```

### 报名表

```
User: "填写这个培训班报名表，我的信息：姓名李四，手机13912345678，邮箱lisi@test.com"

Agent:
1. 打开报名表网址
2. 检测字段
3. 直接使用用户提供的信息填写
4. 展示结果确认
```

---

## Error Handling

```
表单无法加载       → 提示用户检查网址
字段检测失败       → 提示手动填写或提供更多信息
填写失败           → 记录失败字段，继续填写其他
提交失败           → 提示用户手动提交
```

---

## Multi-Language Support

- User language → Output language
- 支持中文和英文表单

---

## Limitations

- **验证码**: 无法自动填写验证码
- **复杂表单**: 动态加载的表单可能需要额外处理
- **文件上传**: 不支持自动上传文件
- **支付表单**: 不支持自动填写支付信息

---

## Privacy & Security

### Data Handling

- ✅ No data uploaded to external servers
- ✅ All processing done locally
- ⚠️ Browser profile accessed during execution
- ⚠️ Form data entered on websites

### Recommendations

1. **Trusted sites only**: Only use on trusted websites
2. **Review before submit**: Always review before submitting
3. **Sensitive data**: Be careful with sensitive information
4. **Separate profile**: Use separate browser profile for testing

---

## Notes

- Requires OpenClaw v2026.3.22+ with browser automation
- Works with any standard HTML form
- Supports input, select, textarea, checkbox, radio
- Can save and reuse form data templates
