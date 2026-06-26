# ATOM-DELIVERY-012 - 飞书发送文件

> 版本：V1.0  
> 状态：🟡 待规范  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 飞书发送文件  
**分类：** 交付层（Delivery Layer）  
**编号：** ATOM-DELIVERY-012

**一句话描述：** 发送文件附件到飞书（带说明文字）

---

## 🎯 输入输出

### 输入
- **类型：** 文件路径 + 说明文字
- **内容：** 本地文件 + 消息

### 输出
- **类型：** 飞书消息（含附件）
- **返回：** messageId

---

## ⚙️ 偏好设置

### 文件大小
- **限制：** <20MB（飞书限制）
- **格式：** 任意格式（doc/docx/xls/xlsx/pdf/png/jpg 等）

### 说明文字
- **格式：** Markdown
- **长度：** <500 字符
- **内容：** 文件名 + 用途说明

### 目标用户
- **默认：** 当前会话用户
- **飞书 ID：** ou_*（个人）或 chat_*（群聊）

---

## 📝 操作步骤

```powershell
# 1. 确认文件存在
$filePath = "C:\Users\Xiabi\.openclaw\workspace\报告.docx"
if (-not (Test-Path $filePath)) {
    Write-Host "❌ 文件不存在：$filePath"
    return
}

# 2. 准备说明文字
$message = @"
## 📄 文件：报告.docx

这是本周的周报，请查收。
"@

# 3. 发送飞书
Invoke-MessageSend `
    -Action "send" `
    -FilePath $filePath `
    -Message $message `
    -Target "ou_e3a0d4a64a9e0932ee919b97f17ec210"

# 4. 确认
Write-Host "✅ 文件已发送：$filePath"
```

---

## 🔄 使用场景

### 场景 1：周报提交
```
触发：周三 15:00 周报生成
  ↓
调用：ATOM-DELIVERY-012
  ↓
输出：飞书消息 + workreport.txt 附件
```

### 场景 2：HTML 报告分享
```
触发：专家点评 HTML 生成
  ↓
调用：ATOM-DELIVERY-012
  ↓
输出：飞书消息 + HTML 文件附件
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- 无

### 常组合使用
- ATOM-DELIVERY-012 + ATOM-DELIVERY-010
  （文件 + 文字说明）

---

## ✅ 检查清单

执行前确认：
- [ ] 文件存在
- [ ] 文件大小<20MB
- [ ] 说明文字简洁
- [ ] target 用户 ID 正确

---

## ⚠️ 常见错误

### 错误 1：文件过大
```
❌ 错误：>20MB（飞书拒绝）
✅ 正确：压缩或用云盘链接
```

### 错误 2：文件不存在
```
❌ 错误：路径错误
✅ 正确：先用 Test-Path 检查
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
