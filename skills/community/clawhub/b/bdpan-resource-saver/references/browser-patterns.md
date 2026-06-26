# Browser Automation Patterns for Baidu Netdisk

## Pattern 1: Accessing Share Link with Password

```
# Navigate to share link
browser navigate https://pan.baidu.com/s/[SHARE_CODE]

# If password page appears, enter password
browser type --ref=[password-input-ref] --text=[PASSWORD]
browser click --ref=[submit-button-ref]

# Wait and snapshot to verify
browser snapshot
```

## Pattern 2: Saving File to Netdisk

```
# After accessing share page with file list visible
# Click "保存到网盘" button
browser click --ref=[save-button-ref]

# If folder selection dialog appears
# Click target folder (e.g., "我的资源")
browser click --ref=[folder-ref]

# Confirm save
browser click --ref=[confirm-button-ref]
```

## Pattern 3: Handling Login Popup

When "保存到网盘" triggers login popup:

```
# Close popup with Escape
browser key --key=Escape

# Alternative: User must manually log in first
# Then retry save operation
```

## Common Element References

### Share Page Elements
- Password input: Usually `e15` or similar textbox
- Submit button: Usually near password input
- File name link: `e90`, `e103`, etc.
- Save button: "保存到网盘" link
- Download button: "下载" link

### Login Popup Elements
- QR code image: For mobile app scan
- Account login tab: "账号登录"
- Phone input: Textbox with placeholder
- SMS code input: Textbox for verification code

## Troubleshooting

### Element Not Found
- Page may have changed, get fresh snapshot
- Element may not be visible yet, wait and retry
- Reference may have expired, use new snapshot

### Gateway Timeout
- Browser connection lost
- Restart browser: `browser restart`
- Retry operation

### Login Required
- Browser session not authenticated
- Use bdpan CLI (already authenticated) instead
- Or have user manually log in via browser
