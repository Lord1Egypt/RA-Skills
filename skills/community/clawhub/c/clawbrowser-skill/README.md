# ClawBrowser 技能包

## 文件說明

```
clawbrowser-skill/
├── SKILL.md              # 技能說明文檔（必需）
├── browser_tool_py36.py  # 核心工具（Python 3.6 兼容）
└── web_scraper.py        # 網頁抓取工具（可選）
```

## 安裝依賴

```bash
# 安裝 agent-browser CLI
npm install -g agent-browser
agent-browser install  # 下載 Chrome
```

## 發布到 ClawHub

### 方法 A：Web 發布
1. 登錄 https://clawhub.ai
2. 點擊 "Publish Skill"
3. 上傳整個文件夾
4. 提交發布

### 方法 B：CLI 發布
```bash
# 安裝 CLI（可選）
npm install -g clawhub

# 或使用 npx（免安裝）
npx clawhub skill publish ./clawbrowser-skill

# 驗證
npx clawhub inspect clawbrowser
```

## 使用示例

```python
from browser_tool import BrowserTool

browser = BrowserTool(session_name="task")
browser.open("https://example.com")
browser.snapshot()
browser.click("@e1")
```

## 開發者

**作者**: RedOpenClaw  
**完成日期**: 2026.04.02  
**簽名**: 🦞 RedOpenClaw - 生活太快⚡️...老逼快跑💨...
