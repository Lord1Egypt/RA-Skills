# chrome-cdp-skill

> OpenClaw Skill for chrome-cdp

## 安装chrome-cdp

在使用此Skill前，需要先安装chrome-cdp：

```bash
# 在 skills/chrome-cdp 目录执行
git clone https://github.com/pasky/chrome-cdp-skill.git temp-cdp

# 移动文件
mv temp-cdp/skills/chrome-cdp/* ./
rm -rf temp-cdp
```

## 启用Chrome远程调试

1. 在Chrome地址栏输入：`chrome://inspect/#remote-debugging`
2. 打开"启用远程调试"开关

## 使用示例

```javascript
const cdp = require('./index.js');

// 列出标签页
const tabs = await cdp.listTabs();
console.log(tabs);

// 截图
await cdp.screenshot('abc123');

// 点击元素
await cdp.click('abc123', '#submit-button');

// 输入文字
await cdp.type('abc123', 'Hello World');

// 导航
await cdp.navigate('abc123', 'https://github.com');

// 执行JS
const result = await cdp.evaluate('abc123', 'document.title');
```

## 对比OpenClaw Browser工具

| 特性 | chrome-cdp | OpenClaw Browser |
|------|------------|-----------------|
| 浏览器 | 已有Chrome | 新启动/已有 |
| 登录状态 | 保持 | 取决于配置 |
| 轻量程度 | 更轻量 | 更通用 |
| 标签页数 | 100+不卡 | 中等 |

## 作者

- chrome-cdp: [pasky](https://github.com/pasky)
- OpenClaw Skill: 小溪
