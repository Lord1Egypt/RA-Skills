# chrome-cdp-skill

> 让AI agent访问你已打开的Chrome标签页

## 简介

chrome-cdp-skill 通过Chrome远程调试协议(CDP)连接你已经在用的Chrome会话，让AI可以：
- 读取已登录账户的页面(Gmail、GitHub等)
- 与你正在工作的标签页交互
- 查看真实页面状态（非重新加载的干净状态）

## 安装

### 前提条件
- Chrome浏览器
- Node.js 22+

### 启用Chrome远程调试

1. 在Chrome地址栏输入：`chrome://inspect/#remote-debugging`
2. 打开"启用远程调试"开关

### 安装Skill

```bash
# 克隆仓库
git clone https://github.com/pasky/chrome-cdp-skill.git
cd chrome-cdp-skill

# 或复制 skills/chrome-cdp/ 目录到你的agent skills目录
```

## 使用方法

### 基本命令

```bash
# 列出打开的标签页
node scripts/cdp.mjs list

# 截图
node scripts/cdp.mjs shot <targetId>

# 获取可访问性树
node scripts/cdp.mjs snap <targetId>

# 获取HTML
node scripts/cdp.mjs html <targetId> [".selector"]

# 点击元素
node scripts/cdp.mjs click <targetId> "selector"

# 输入文字
node scripts/cdp.mjs type <targetId> "text"

# 导航
node scripts/cdp.mjs nav <targetId> https://...

# 评估JavaScript
node scripts/cdp.mjs eval <targetId> "expression"

# 网络资源计时
node scripts/cdp.mjs net <targetId>

# 加载更多（点击"加载更多"直到消失）
node scripts/cdp.mjs loadall <targetId> "selector"
```

### 获取targetId

首先运行 `list` 命令获取标签页的targetId：
```bash
$ node scripts/cdp.mjs list
TargetID  Title                     URL
---------  -----                     ---
abc123def  Gmail - Google Account   https://mail.google.com/...
def456ghi  GitHub                   https://github.com/...
```

然后用targetId前缀操作：
```bash
node scripts/cdp.mjs snap abc
node scripts/cdp.mjs click abc "#compose"
node scripts/cdp.mjs type abc "Hello World"
```

## 与OpenClaw集成

### 方法1：直接调用脚本

在OpenClaw中通过exec调用：
```bash
node /path/to/chrome-cdp-skill/scripts/cdp.mjs list
```

### 方法2：创建MCP服务器

可以将其封装为MCP服务器供OpenClaw调用。

### 方法3：创建OpenClaw Skill

参考 `skills/chrome-cdp/index.js` 创建完整Skill。

## 优势对比

| 特性 | chrome-cdp | Puppeteer类工具 |
|------|------------|----------------|
| 浏览器 | 已有Chrome | 新启动浏览器 |
| 登录状态 | 保持 | 需重新登录 |
| 页面状态 | 真实状态 | 干净状态 |
| 标签页数量 | 100+不卡 | 容易超时 |
| 依赖 | 仅Node.js | Puppeteer+浏览器 |

## 注意事项

1. 首次访问标签页时，Chrome会弹出"允许调试"确认框
2. 守护进程20分钟无活动自动退出
3. 目标ID只需唯一前缀即可匹配

## 参考

- GitHub: https://github.com/pasky/chrome-cdp-skill
- 作者: pasky
- Stars: 1000+
