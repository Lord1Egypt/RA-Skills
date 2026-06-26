# 问专家技能 - 使用 Playwriter 控制已登录的浏览器

## 技能描述
使用 Playwriter 连接用户已登录的 Chrome 浏览器，通过 Gemini 等 AI 助手获取专业建议。

## 触发关键词
- "问专家"
- "问 Gemini"
- "问 AI"
- "使用专家模式"

## 完整流程

### 步骤 1：打开浏览器
```bash
open -a "Google Chrome"
```

### 步骤 2：移动鼠标并点击扩展图标
```bash
# 移动鼠标到扩展图标位置 (1294, 86)，等待 5 秒，点击
python3 -c "
import pyautogui
import time
pyautogui.moveTo(1294, 86)
time.sleep(5)
pyautogui.click()
"
```

### 步骤 3：创建 Playwriter 会话
```bash
playwriter session new
# 输出: Session X created. Use with: playwriter -s X -e "..."
```

### 步骤 4：打开网页
```bash
# 先创建页面再导航（重要！）
playwriter -s X -e 'state.page = await context.newPage(); await state.page.goto("URL")'
```

### 步骤 5：输入问题并发送
```bash
# 输入问题
playwriter -s X -e 'await state.page.keyboard.type("问题内容")'

# 发送
playwriter -s X -e 'await state.page.keyboard.press("Enter")'
```

### 步骤 6：获取回答
```bash
# 等待一段时间后获取文本
sleep 15
playwriter -s X -e 'const text = await state.page.locator("message-content").last().textContent(); console.log(text)'

# 或截图
playwriter -s X -e 'await state.page.screenshot({ path: "path/to/screenshot.png" })'
```

## 常见问题

### Q: 扩展未连接
**A**: 需要用户手动点击 Chrome 右上角的 Playwriter 扩展图标，确保显示连接状态

### Q: page undefined 错误
**A**: 需要先创建页面：`state.page = await context.newPage()`

### Q: 连接断开
**A**: 使用 `playwriter session reset <id>` 重置会话，然后重新创建

## 适用场景
- 需要登录账号才能使用的 AI 网站（Gemini、ChatGPT 等）
- 需要保持登录状态的浏览器操作
- 需要绕过机器人检测的场景
- 询问专业问题获取 AI 建议

## 技术优势
- 使用用户已登录的浏览器，无需重新登录
- 通过 Chrome 扩展连接，安全稳定
- 支持会话管理，可以保持状态

## 安装前置条件
1. 安装 Playwriter：`npm install -g playwriter@latest`
2. Chrome 安装 Playwriter 扩展：
   - 扩展 ID: `jfeammnjpkecdekppnclgkkffahnhfhe`
   - 或从 Chrome 网上应用店搜索 "Playwriter" 安装
