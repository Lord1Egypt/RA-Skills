---
name: ad-agent-test
description: 腾讯广告投放Agent（ad.qq.com/atlas/{account_id}/agent）自动化体验测试技能。通过Cookie注入+Playwright浏览器自动化，对投放Agent的对话功能、快捷指令、常用指令面板、自由对话、妙招功能进行完整体验测试，并生成UX体验报告。适用场景：(1) 用户要求测试ad.qq.com投放Agent (2) 用户提到"投放Agent体验" (3) 用户需要对广告投放平台的Agent功能做产品体验/竞品分析 (4) 涉及ad.qq.com的自动化测试。需要用户提供adhome免登录Cookie。
---

# 投放Agent自动化体验测试

通过 Playwright 浏览器自动化 + Cookie注入 对 ad.qq.com 投放Agent功能进行完整UX测试。

## 前置条件

1. **中文字体**：服务器需安装中文字体（否则截图中文为方块）
2. **Cookie**：需要用户提供有效的 adhome 免登录 Cookie
3. **Playwright**：需要 Node.js + playwright 已安装

### 安装中文字体
```bash
yum install -y google-noto-sans-cjk-sc-fonts
```

### 检查Playwright
```bash
npx playwright --version
```

## Cookie 获取流程

引导用户操作：
1. 打开 adhome 免登录页面，选择目标账户
2. 点击免登录进入 ad.qq.com/atlas/{account_id}/agent
3. 在浏览器 F12 控制台执行 `document.cookie` 
4. 将结果发给 Agent

### Cookie 解析要点
- 必需Cookie：`gdt_mlogin`、`gdt_owner`、`tap_free_login_token`、`tap_free_login_userid`
- `.woa.com` 域Cookie（`RIO_TOKEN`等）用于内网认证
- `.qq.com` 域Cookie（`ptcz`、`RK`等）用于QQ登录态
- Cookie有效期约2小时（会话级），过期会跳转登录页

### Cookie 注入代码模板

参见 [scripts/inject_cookies.js](scripts/inject_cookies.js) — 解析用户提供的 cookie 字符串并注入到 Playwright context。

## 测试流程

### 第一阶段：环境验证
1. 注入Cookie
2. 访问 `https://ad.qq.com/atlas/{account_id}/agent`
3. 等待8秒页面加载
4. 验证是否进入Agent页面（非登录页）— 检查页面是否包含"对话"/"妙招"等文字

### 第二阶段：对话功能测试

#### 2.1 首页快捷指令
遍历首页展示的快捷指令卡片（通常4个），依次：
1. 点击指令
2. 等待3秒
3. 截图记录模板展示
4. 提取输入框中的模板文案（含slot类型）
5. 新开会话测试下一个

#### 2.2 常用指令面板
1. 点击底部"常用指令"按钮（`[title="常用指令"]`）
2. 截图完整指令面板
3. 提取所有指令分类和名称

#### 2.3 模板Slot交互
1. 点击快捷指令后，在模板中点击 asset slot
2. 记录下拉列表内容
3. 点击 select slot，记录选项

#### 2.4 自由对话
测试覆盖投放全链路：

**投放前**：
- 预算规划："我有5000元预算，想推广一个教育类小程序，应该怎么设置投放计划？"
- 选品定向："我是做电商的，卖女装，适合选择什么投放版位和定向人群？"

**投放中**：
- 数据查询："帮我查一下今天的广告消耗和转化数据"
- 优化建议："我的广告点击率很低只有0.5%，有什么优化建议？"
- 调预算："帮我把所有在投的广告日预算统一调整到200元"

**投放后**：
- 复盘分析："帮我分析一下上周的投放效果，哪些广告ROI最高？"
- 批量关停："帮我把转化成本超过50元的广告全部暂停"

每轮对话：输入 → 等待25秒 → 截图 → 提取回复文本

### 第三阶段：妙招功能测试

1. 切换到妙招页面（点击侧边栏"妙招"或首页"探索投放妙招"卡片）
2. 逐一点击每个妙招卡片，截图配置面板
3. 测试"一键执行"：
   - 验证按钮默认disabled状态（`title="请先完成必要配置"`）
   - 通过规则选择广告
   - 验证按钮变为enabled
   - 点击执行，观察结果反馈

## 输出物

### 截图命名规范
```
{序号}_{场景}.png
```
示例：`01_home.png`、`05_chat_fashion.png`、`07_miaozahao.png`

### 报告结构
参见 [references/report-template.md](references/report-template.md) — 完整报告 Markdown 模板。

报告核心章节：
1. 功能全景（对话 + 妙招）
2. 对话功能体验（快捷指令 + 自由对话）
3. 妙招功能体验（配置面板 + 一键执行）
4. 信息架构与体验一致性
5. 优化建议（按P0/P1/P2分级）
6. 体验亮点

### 报告输出
- 本地Markdown文件：`output/agent-test/体验报告_投放Agent_{date}.md`
- 企微文档（通过 `wecom_mcp` 的 `smartpage_create` 上传）

## 关键选择器参考

| 元素 | 选择器 |
|------|--------|
| 快捷指令卡片 | `[class*="guideCard"]` 或 `text=模仿优质广告新建` |
| 常用指令按钮 | `[title="常用指令"]` 或 `[class*="commandButton"]` |
| 输入框 | `[contenteditable="true"]` |
| 发送按钮 | `[class*="sendButton"]` |
| 妙招侧边栏 | `[class*="menuItem"]` 含文字"妙招" |
| 一键执行按钮 | `button` 含文字"一键执行" |
| 广告选择规则 | `[class*="ruleSelect"]` 或含"规则"文字的tab |

## 注意事项

- Cookie约2小时过期，过期后自动跳转登录页
- 如截图中文显示为方块，先安装 `google-noto-sans-cjk-sc-fonts`
- Agent回复需要10-25秒，部分场景会卡在"分析中"状态
- 使用DOM文本提取（`page.evaluate`）比截图更可靠，确保内容被记录
- 首次进入Agent页面需等8秒完成SPA加载
- 每次发送对话后建议新开会话（避免上下文串扰测试结果）
