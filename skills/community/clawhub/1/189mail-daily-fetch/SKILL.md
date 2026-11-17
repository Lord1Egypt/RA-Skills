---
name: 189mail-daily-fetch
description: "Automatically log in to 189.cn mailbox, fetch the latest email, and save it as .eml file to the desktop. Use when user wants to download the newest email from 189 mailbox, or needs to set up scheduled daily email fetching. Triggers include 下载最新邮件, 获取189邮箱最新邮件, 每天自动取邮件, 189邮箱, fetch latest email, daily email download."
name_cn: 189邮箱每日取件
description_cn: 自动登录189邮箱，下载最新邮件到桌面，支持每日定时执行
---

# 189邮箱每日取件

自动登录189邮箱，获取收件箱中最新一封邮件，以EML原始格式保存到电脑桌面。

## 适用场景

- 每日定时自动下载最新邮件存档
- 需要离线查看或备份重要邮件
- 配合定时任务实现无人值守的邮件归档

## 工作流程

### 第一步：登录189邮箱

1. 使用 Playwright 浏览器打开 `https://mail.189.cn/`
2. 确保在「账号登录」标签页
3. 在 iframe `#iframeLogin` 中填写用户提供的手机号和密码
4. 点击「登录」按钮（如遇遮挡层，使用 `force: true` 强制点击）
5. 等待页面跳转至邮箱主页，确认 URL 包含 `mailbox.html`

### 第二步：进入收件箱并打开最新邮件

1. 点击左侧导航树中的「收件箱」
2. 等待邮件列表加载完成（通常需 3-5 秒）
3. 点击邮件列表中第一封（最新的）邮件

### 第三步：导出EML文件到桌面

1. 在邮件阅读页顶部工具栏点击「更多」按钮
2. 在弹出菜单中点击「EML格式导出」链接
3. 浏览器自动下载 .eml 文件至 playwright-mcp 目录
4. 将下载的文件复制到用户桌面

导出链接格式：
```
/w2/downLoadAttachNormal.do?messageid={邮件ID}&msid={文件夹ID}&partid=9999&customerFileName={文件名}.eml
```

### 第四步：报告结果

向用户汇报：邮件主题、发件人、收件时间、本地保存路径。

## 注意事项

- **登录凭据**：由用户在对话中提供，绝不硬编码到脚本或配置中
- **跨域iframe**：189邮箱登录页使用跨域 iframe，需通过 Playwright 的 `contentFrame()` 方法操作内部元素
- **加载等待**：邮件列表加载后可能需要等待 3-5 秒，建议使用显式等待
- **密码特殊字符**：如密码包含特殊字符，填写时需确保正确转义
- **文件移动**：下载的 EML 文件默认保存在 playwright-mcp 目录，需手动复制到桌面
- **安全验证**：如邮箱触发短信验证或滑块验证，需用户手动介入
