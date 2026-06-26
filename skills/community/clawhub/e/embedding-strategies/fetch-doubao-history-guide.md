# 豆包今日会话记录自动导出指南

**创建时间**: 2026-03-05 19:40  
**目标**: 自动从豆包网页版抓取今天的会话记录

---

## 🎯 方案对比

| 方案 | 难度 | 自动化程度 | 推荐度 |
|------|------|-----------|--------|
| **手动复制** | ⭐ | 低 | ⭐⭐ |
| **简化脚本** | ⭐⭐ | 中 | ⭐⭐⭐⭐ |
| **完全自动化** | ⭐⭐⭐⭐ | 高 | ⭐⭐⭐⭐⭐ |

---

## 🚀 方案 1：简化脚本（立即可用）

**脚本**: `fetch-doubao-history.ps1`

**使用步骤**:
```powershell
# 1. 打开豆包网页
https://www.doubao.com

# 2. 在侧边栏找到今天的对话列表

# 3. 运行脚本
powershell -ExecutionPolicy Bypass -File C:\Users\Xiabi\.openclaw\workspace\fetch-doubao-history.ps1

# 4. 输入对话数量（例如：5）

# 5. 逐个粘贴对话内容

# 6. 自动格式化 + 保存到知识库
```

**优点**:
- ✅ 立即可用
- ✅ 自动格式化
- ✅ 自动保存到知识库
- ✅ 自动更新索引

**缺点**:
- ❌ 需要手动复制粘贴

---

## 🤖 方案 2：完全自动化（需要配置）

**脚本**: `fetch-doubao-auto.ps1`（待创建）

**工作原理**:
```powershell
# 1. 自动打开豆包网页
browser.open https://www.doubao.com

# 2. 等待页面加载
wait 3000

# 3. 捕获侧边栏结构
browser.snapshot refs="aria"

# 4. 提取今天的对话列表
# 使用 CSS 选择器定位侧边栏
$sidebar = document.querySelector('aside.sidebar')
$conversations = $sidebar.querySelectorAll('.conversation-item')

# 5. 过滤今天的对话
$today = Get-Date -Format "yyyy-MM-dd"
$todayConversations = $conversations | Where-Object {
    $_.querySelector('.date').innerText -eq $today
}

# 6. 逐个打开并保存
foreach ($conv in $todayConversations) {
    # 点击对话
    $conv.click()
    wait 2000
    
    # 捕获对话内容
    $content = document.querySelector('.conversation-content').innerText
    
    # 保存到文件
    Save-Conversation -Content $content
}

# 7. 生成汇总报告
Generate-Report -Date $today
```

**优点**:
- ✅ 完全自动化
- ✅ 一键运行
- ✅ 无需手动操作

**缺点**:
- ⚠️ 需要配置浏览器自动化
- ⚠️ 豆包页面结构变化时需要更新脚本

---

## 📋 豆包页面结构分析

### 侧边栏 HTML 结构（推测）

```html
<aside class="sidebar">
  <div class="conversation-list">
    <div class="conversation-item" data-date="2026-03-05">
      <div class="conversation-title">网页总结技巧</div>
      <div class="conversation-date">今天 18:30</div>
    </div>
    <div class="conversation-item" data-date="2026-03-05">
      <div class="conversation-title">代码审查建议</div>
      <div class="conversation-date">今天 17:45</div>
    </div>
    <!-- 更多对话... -->
  </div>
</aside>
```

### 对话内容 HTML 结构（推测）

```html
<div class="conversation-content">
  <div class="message user">
    <div class="message-content">
      帮我总结这个网页...
    </div>
  </div>
  <div class="message assistant">
    <div class="message-content">
      好的，这个网页主要讲了...
    </div>
  </div>
  <!-- 更多消息... -->
</div>
```

---

## 🛠️ 配置步骤（完全自动化）

### 第 1 步：确保浏览器可用

```powershell
# 检查浏览器状态
browser.status

# 如果需要，重启 Gateway
openclaw gateway restart
```

### 第 2 步：打开豆包并捕获结构

```powershell
# 打开豆包
browser.open https://www.doubao.com

# 等待加载
Start-Sleep -Seconds 3

# 捕获页面结构
browser.snapshot refs="aria"
```

### 第 3 步：分析侧边栏选择器

从 snapshot 结果中找到：
- 侧边栏容器（`aside.sidebar` 或 `div[class*="sidebar"]`）
- 对话列表项（`.conversation-item`）
- 日期字段（`.conversation-date` 或 `.date`）
- 标题字段（`.conversation-title` 或 `.title`）

### 第 4 步：创建自动化脚本

基于实际的选择器创建脚本 `fetch-doubao-auto.ps1`

### 第 5 步：测试运行

```powershell
powershell -ExecutionPolicy Bypass -File fetch-doubao-auto.ps1
```

---

## 📁 输出文件格式

**文件名**: `doubao-history-2026-03-05.md`

**格式**:
```markdown
# 豆包会话记录 - 2026-03-05

**导出时间**: 2026-03-05 19:40:00  
**来源**: 豆包 AI  
**对话数量**: 5  
**文件**: doubao-history-2026-03-05.md

---

## 📋 会话列表

### 对话 1: 网页总结技巧
**时间**: 今天 18:30

**用户**: 帮我总结这个网页...
**豆包**: 好的，这个网页主要讲了...

---

### 对话 2: 代码审查建议
**时间**: 今天 17:45

**用户**: 帮我看看这段代码...
**豆包**: 这段代码有几个问题...

---

## 🏷️ 标签

#豆包 #AI 对话 #会话记录 #知识库 #2026-03-05

---

_本文档由 fetch-doubao-auto.ps1 自动生成_
```

---

## 🔍 当前限制

### 浏览器工具状态

**问题**: Chrome extension relay 运行中，但没有标签页连接

**解决**:
1. 打开 Chrome 浏览器
2. 点击 OpenClaw Chrome 扩展图标
3. 在豆包标签页上启用（徽章变亮）
4. 重新运行脚本

**或者**:
- 使用简化脚本（手动复制粘贴）
- 等待浏览器可用后再运行完全自动化

---

## 🎯 推荐流程

### 今天（立即）
```
使用简化脚本 fetch-doubao-history.ps1
手动复制 + 自动格式化
```

### 明天（配置后）
```
使用完全自动化脚本 fetch-doubao-auto.ps1
一键运行，自动抓取
```

---

## 💡 进阶功能

### 1. 自动分类
```powershell
# 根据对话内容自动打标签
if ($content -match "代码") {
    $tags += "#编程"
} elseif ($content -match "总结") {
    $tags += "#学习"
}
```

### 2. 定时导出
```powershell
# 配置 Cron 任务
# 每天 23:00 自动导出当天会话
```

### 3. 智能汇总
```powershell
# 生成每日学习摘要
# 提取关键知识点
# 创建复习卡片
```

---

## 📞 需要帮助？

**遇到问题随时告诉我**，我可以：
- 帮您调试浏览器自动化
- 更新 CSS 选择器
- 创建完全自动化脚本

---

## 🚀 快速开始

### 现在就试试简化版！

1. **打开豆包**
   ```
   https://www.doubao.com
   ```

2. **找到今天的对话列表**

3. **运行脚本**
   ```powershell
   powershell -ExecutionPolicy Bypass -File C:\Users\Xiabi\.openclaw\workspace\fetch-doubao-history.ps1
   ```

4. **输入对话数量**（例如：3）

5. **逐个粘贴对话内容**

6. **完成！** 自动保存到知识库

---

**Thomas 先生，现在就可以试试简化版脚本！** 🚀

**或者告诉我，我帮您配置完全自动化版本！** 🐾
