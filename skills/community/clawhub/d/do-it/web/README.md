# 🌪️ do-it Web MVP - 快速启动指南

**版本：** v0.1 MVP  
**日期：** 2026-03-15

---

## 🚀 快速启动

### 方式 1：直接打开 (最简单)

```bash
# 直接用浏览器打开
open /home/admin/.openclaw/workspace/skills/do-it/web/index.html
```

或者双击 `index.html` 文件即可！

---

### 方式 2：本地服务器

```bash
# Python 3
cd /home/admin/.openclaw/workspace/skills/do-it/web
python3 -m http.server 8080

# 然后访问 http://localhost:8080
```

---

### 方式 3：Vercel 部署 (推荐生产环境)

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
cd web
vercel

# 按提示操作，获得免费 HTTPS 链接
```

---

## 📱 功能清单

### ✅ 已有功能

- [x] 首页展示
- [x] 问题输入表单
- [x] 加载动画
- [x] 结果展示
- [x] 用户反馈
- [x] 案例展示
- [x] 响应式设计 (手机/PC)

### 🚧 待开发功能

- [ ] 真实 AI 判断集成
- [ ] 用户系统
- [ ] 历史记录保存
- [ ] 案例详情查看
- [ ] 分享功能
- [ ] 数据可视化

---

## 🎨 页面预览

### 首页
```
┌─────────────────────────────────┐
│     🌪️ do-it                   │
│  你只管 do it，判断交给滚滚       │
├─────────────────────────────────┤
│         🤔                      │
│   有什么纠结的事儿？            │
│                                 │
│   [开始判断 →]                  │
│                                 │
│   📋 最近案例                   │
│   • 38 岁财务 BP...              │
│   • 35 岁程序员...               │
└─────────────────────────────────┘
```

### 输入页
```
┌─────────────────────────────────┐
│ ← 返回   填写问题详情           │
├─────────────────────────────────┤
│ 你的问题：                      │
│ [_________________________]     │
│                                 │
│ 问题类型：                      │
│ ○职业 ○感情 ○投资 ○生活        │
│                                 │
│ 当前状态：                      │
│ [_________________________]     │
│                                 │
│ [提交分析 →]                    │
└─────────────────────────────────┘
```

### 结果页
```
┌─────────────────────────────────┐
│ ← 返回   滚滚的判断             │
├─────────────────────────────────┤
│ ✅ 推荐选择：方案 B             │
│                                 │
│ 理由：                          │
│ 1. 数据表明成功率更高           │
│ 2. 风险可控                     │
│ 3. 符合长期目标                 │
│                                 │
│ 👍 有用 | 👎 无用 | 💬 反馈     │
└─────────────────────────────────┘
```

---

## 🔧 自定义配置

### 修改 Slogan

编辑 `index.html` 第 13 行：
```html
<h1 class="text-4xl font-bold text-indigo-600 mb-2">🌪️ do-it</h1>
<p class="text-gray-600">你只管 do it，判断交给滚滚</p>
```

### 修改主题色

编辑 `index.html`，搜索 `indigo` 替换为其他颜色：
- `blue` - 蓝色
- `purple` - 紫色
- `green` - 绿色
- `red` - 红色

### 添加真实 API

编辑 `index.html` 第 272 行，替换 `submitProblem` 函数：

```javascript
async function submitProblem(event) {
    event.preventDefault();
    
    const problemData = {
        title: document.getElementById('problem-title').value,
        type: document.querySelector('input[name="problem-type"]:checked').value,
        // ... 其他字段
    };
    
    showLoading();
    
    // 调用真实 API
    const response = await fetch('YOUR_API_URL', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(problemData)
    });
    
    const result = await response.json();
    showResult(result.html);
}
```

---

## 📊 数据统计

目前 Web MVP 已包含：

| 项目 | 数量 |
|------|------|
| HTML 页面 | 1 个 |
| CSS 样式 | Tailwind CDN |
| JavaScript | 原生 JS |
| 代码行数 | ~400 行 |
| 文件大小 | ~15KB |
| 加载速度 | <1 秒 |

---

## 🎯 下一步优化

### 短期 (1 周)
- [ ] 集成真实 AI 判断 API
- [ ] 添加 LocalStorage 保存历史
- [ ] 优化移动端体验

### 中期 (1 月)
- [ ] Vue 3 重构
- [ ] 用户系统
- [ ] 案例详情查看
- [ ] 数据可视化图表

### 长期 (3 月)
- [ ] 小程序版本
- [ ] 付费功能
- [ ] 社区功能
- [ ] APP 版本

---

## 💡 使用技巧

### 测试流程

1. 打开 `index.html`
2. 点击"开始判断"
3. 填写问题（随便写）
4. 点击"提交分析"
5. 等待加载动画
6. 查看结果
7. 提交反馈

### 查看案例

首页会显示 3 个示例案例，点击可以查看（待实现详情）

### 收集反馈

用户点击 👍/👎 后，数据会记录到控制台（待实现后端）

---

## 🐛 已知问题

- [ ] 结果目前是模拟数据
- [ ] 历史记录未保存
- [ ] 案例详情未实现
- [ ] 分享功能未实现

---

## 📞 技术支持

**问题反馈：**
- GitHub Issues
- 邮件：support@do-it.ai (待设置)

**文档：**
- PRODUCT-DESIGN.md - 产品设计文档
- PRODUCT-PLAN.md - 产品计划
- data/README.md - 数据说明

---

## 🌟 演示链接

**本地访问：**
```
file:///home/admin/.openclaw/workspace/skills/do-it/web/index.html
```

**生产环境 (待部署)：**
```
https://do-it.vercel.app
```

---

**创建人：** 滚滚 & 地球人  
**创建时间：** 2026-03-15  
**状态：** 🚀 MVP 完成，等待测试
