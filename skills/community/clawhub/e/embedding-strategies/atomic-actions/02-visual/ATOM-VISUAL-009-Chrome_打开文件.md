# ATOM-VISUAL-009 - Chrome 打开文件

> 版本：V1.0  
> 状态：✅ 已固化  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** Chrome 打开文件  
**分类：** 呈现层（Visual Layer）  
**编号：** ATOM-VISUAL-009

**一句话描述：** 用 Chrome 浏览器打开本地文件（HTML/PDF 等）

---

## 🎯 输入输出

### 输入
- **类型：** 文件路径
- **内容：** 本地文件绝对路径

### 输出
- **类型：** 系统操作
- **效果：** Chrome 浏览器窗口打开

---

## ⚙️ 偏好设置

### 打开方式
- **命令：** Start-Process chrome.exe
- **模式：** 独立窗口
- **显示：** 前台显示

---

## 📝 操作步骤

```powershell
# 1. 确认文件存在
$filePath = "C:\Users\Xiabi\.openclaw\workspace\expert-review.html"
if (-not (Test-Path $filePath)) {
    Write-Host "❌ 文件不存在：$filePath"
    return
}

# 2. Chrome 打开
Start-Process "chrome.exe" -ArgumentList $filePath

# 3. 确认
Write-Host "✅ Chrome 已打开：$filePath"
```

---

## 🔄 使用场景

### 场景 1：HTML 专家点评生成后
```
触发：HTML 文件生成完成
  ↓
调用：ATOM-VISUAL-009
  ↓
输出：Chrome 浏览器窗口打开 HTML
```

### 场景 2：PDF 报告查看
```
触发：PDF 报告生成
  ↓
调用：ATOM-VISUAL-009
  ↓
输出：Chrome 浏览器窗口打开 PDF
```

---

## 🔗 关联动作

### 前置动作
- ATOM-VISUAL-005：生成 HTML 文件

### 后置动作
- 无

### 常组合使用
- ATOM-VISUAL-005 + ATOM-VISUAL-009
  （生成 HTML → Chrome 打开）

---

## ✅ 检查清单

执行前确认：
- [ ] 文件存在
- [ ] 绝对路径
- [ ] Chrome 已安装
- [ ] 文件类型 Chrome 支持

---

## ⚠️ 常见错误

### 错误 1：文件不存在
```
❌ 错误：路径错误
✅ 正确：先用 Test-Path 检查
```

### 错误 2：相对路径
```
❌ 错误：.\file.html
✅ 正确：C:\Users\...\file.html
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
