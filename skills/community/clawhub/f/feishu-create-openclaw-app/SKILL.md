# Feishu App Creator Skill

Automates the creation of a Feishu (Lark) enterprise self-built application for OpenClaw integration via browser automation.

## When to Use

- User wants to create a new Feishu application for OpenClaw
- Need to automate the Feishu developer console setup
- Requires browser-based OAuth login and app configuration

## Important: Personal Account Limitations


## Complete Workflow

### Step 1: Open Feishu Developer Console

```
browser action=open url=https://open.feishu.cn/app
```

### Step 2: Check Login Status

Take snapshot and check for "创建企业自建应用" button. If visible, user is logged in.

### Step 3: Create App

**Click "创建企业自建应用" button**

Wait for dialog to open.

**Fill form using real user input simulation:**

```javascript
// Click name input, type app name
browser action=act kind=click ref=<name_input_ref>
browser action=act kind=type ref=<name_input_ref> text="openclaw"

// Click description textarea, type description
browser action=act kind=click ref=<desc_textarea_ref>
browser action=act kind=type ref=<desc_textarea_ref> text="OpenClaw integration app"

// Click an icon (RobotFilled)
browser action=act kind=click ref=<icon_ref>

// Click Create button
browser action=act kind=click ref=<create_button_ref>
```

### Step 4: Navigate to Permission Management

After app created, click "权限管理" in sidebar.

### Step 5: Import Permissions

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "docs:document.content:read",
      "event:ip_list",
      "im:chat",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.group_msg",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource",
      "sheets:spreadsheet",
      "wiki:wiki:readonly"
    ],
    "user": [
      "aily:file:read",
      "aily:file:write",
      "im:chat.access_event.bot_p2p_chat:read"
    ]
  }
}
```

**Import Process:**

1. Click "批量导入/导出权限" button

2. **Clear editor using Ctrl+A then fill:**
```javascript
browser action=act kind=evaluate fn="() => {
  const ta = document.querySelector('textarea[aria-label*=\"Editor\"]');
  if(ta) {
    ta.value = '';  // Clear first
    const json = 'YOUR_JSON_HERE';
    ta.value = json;
    ta.dispatchEvent(new Event('input', {bubbles:true, composed:true}));
    ta.dispatchEvent(new Event('change', {bubbles:true, composed:true}));
    return 'done:' + ta.value.length;
  }
  return 'err';
}"
```

3. Click "下一步，确认新增权限"

4. Review permissions dialog:
   - Shows "以下权限已申请，本次不会重复申请 (X)" for existing permissions
   - Shows new permissions to be added

5. Click "申请开通"

### Step 6: Extract Credentials

Navigate to "凭证与基础信息" page.

- **App ID**: Visible directly (e.g., `cli_xxxxxxxxxxxx`)
- **App Secret**: Click eye icon to reveal, display full secret to user

## Key Points

### Form Elements
- **应用名称**: `input[type="text"]` in dialog - use `type` action
- **应用描述**: `textarea` in dialog - use `type` action
- **图标**: `[aria-label*="Filled"]` icons in dialog - click to select

### Permission Editor
- **JSON Editor**: `textarea[aria-label*="Editor"]` - can use direct value assignment
- **Clear First**: Always clear with `ta.value = ''` before filling
- **Trigger Events**: Must dispatch `input` and `change` events

### Account Type Detection
- **Personal Account**: Only 2-3 permissions can be enabled
- **Enterprise Account**: All permissions can be enabled
- **Detection**: Check permission list after import - if only 3 permissions show, it's personal account

## Output

After successful creation:
```
✅ 应用创建成功！

应用名称：openclaw
App ID: cli_xxxxxxxxxxxx
App Secret: <FULL_SECRET>
状态：待上线


下一步：
1. 复制 App Secret（立即保存，只显示一次）
2. 在 OpenClaw 配置中填入 App ID 和 App Secret
3. 创建应用版本并发布
```
