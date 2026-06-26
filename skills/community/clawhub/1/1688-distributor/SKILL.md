---
name: 1688-distributor
description: Automate 1688.com AI product selection and distribution workflow. Use this skill when you want to search for products on 1688.com, select items, distribute them to your shop, and check distribution logs. This skill handles the complete flow: AI selection → batch select → distribute → view logs. Trigger on mentions of "1688铺货", "1688选品", "1688代发", "1688分销", or when user provides shop name and product selection criteria.

---

# 1688 Distributor - AI选品铺货自动化

自动化完成1688分销AI工作台的选品、铺货和日志查看全流程。

## 使用场景

当你说类似以下内容时触发：
- "1688铺货" / "1688代发" / "1688分销"
- "1688选品" / "AI选品"
- "去1688找点货"
- 提供店铺名和选品条件时

## 准备信息

执行前需要你提供：

1. **店铺名称** - 例如：kyeshop小店
2. **选品条件**（可选，使用默认值如果不提供）
   - 一件起批
   - 48小时发货
   - 7天无理由退货
   - 包邮
   - 价格范围：10-30元（可自定义）
   - 退货率低于10%
   - 最近好卖的商品

**示例：**
> 去1688帮我铺货20个商品到kyeshop小店，条件是：一件起批，48小时发货，7天无理由，包邮，价格10-30元，退货率低于10%

## 自动化流程

### 步骤1：访问1688 AI选品页面

导航至：https://air.1688.com/app/channel-fe/distribution-work/ai-assistant.html#/multi-agent

### 步骤2：AI选品搜索

使用JavaScript执行以下操作：

```javascript
// 点击AI选品按钮
const aiSelectBtn = [...document.querySelectorAll('*')].find(el => el.textContent.includes('ai选品'));
if(aiSelectBtn) aiSelectBtn.click();

// 输入选品条件（可替换）
const searchBox = document.querySelector('[placeholder*="一句提问"], [placeholder*="秒级解答"]');
if(searchBox) {
  searchBox.value = "一件起批，48小时发货，7天无理由，包邮，价格在10-30元，退货率低于10%，最近好卖的商品";
  searchBox.dispatchEvent(new Event('input', { bubbles: true }));
}

// 等待AI生成（检查"查看详情"按钮）
await new Promise(resolve => {
  const checkBtn = setInterval(() => {
    const btn = [...document.querySelectorAll('*')].find(el => el.textContent.includes('查看详情'));
    if(btn && btn.offsetParent !== null) {
      clearInterval(checkBtn);
      resolve(btn);
    }
  }, 500);
  setTimeout(() => clearInterval(checkBtn), 30000); // 30秒超时
}).then(btn => btn?.click());
```

### 步骤3：查看并全选商品

```javascript
// 等待商品表格加载
await new Promise(resolve => setTimeout(resolve, 3000));

// 点击"本页全选"
const selectAllCheckbox = document.querySelector('[aria-label="Select all"], input[type="checkbox"][aria-label*="all"]');
if(selectAllCheckbox && !selectAllCheckbox.checked) {
  selectAllCheckbox.click();
}

// 确认全选成功（检查20个商品）
const checkedCount = document.querySelectorAll('table input[type="checkbox"]:checked').length;
console.log(`已选择 ${checkedCount} 个商品`);
```

### 步骤4：立即铺货

```javascript
// 查找并点击"立即铺货"按钮
const distributeBtn = [...document.querySelectorAll('button, div[role="button"]')].find(el => 
  el.textContent && el.textContent.includes('立即铺货') && el.offsetParent !== null
);

if(distributeBtn) {
  distributeBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
  distributeBtn.click();
} else {
  console.error('未找到"立即铺货"按钮');
}
```

### 步骤5：选择店铺并确认

如果弹出店铺选择框，选择目标店铺：

```javascript
// 查找并点击目标店铺（替换店铺名）
const targetShop = "kyeshop小店"; // 从用户输入获取
const shopElements = [...document.querySelectorAll('*')].filter(el => 
  el.textContent && el.textContent.includes(targetShop) && el.offsetParent !== null
);

if(shopElements.length > 0) {
  shopElements[shopElements.length - 1].click();
}

// 查找并点击确认按钮
const confirmBtn = [...document.querySelectorAll('*')].find(el => 
  el.textContent && el.textContent.includes('立即铺货') && el.offsetParent !== null
);
if(confirmBtn) confirmBtn.click();
```

### 步骤6：查看铺货日志

```javascript
// 方式一：点击弹窗中的"铺货日志"按钮
const logBtn = [...document.querySelectorAll('*')].find(el => 
  el.textContent && el.textContent.includes('铺货日志') && el.offsetParent !== null
);
if(logBtn) logBtn.click();

// 方式二：通过导航菜单进入
const distributeMenu = [...document.querySelectorAll('*')].find(el => 
  el.textContent && el.textContent.includes('铺货') && el.offsetParent !== null
);
if(distributeMenu) distributeMenu.click();

// 等待后点击"复制日志"
await new Promise(resolve => setTimeout(resolve, 2000));
const copyLogBtn = [...document.querySelectorAll('*')].find(el => 
  el.textContent && el.textContent.includes('复制日志') && el.offsetParent !== null
);
if(copyLogBtn) copyLogBtn.click();
```

## 执行输出

执行完成后返回以下信息：

```
✅ AI选品完成 - 找到 [数量] 个商品
✅ 已全选 [数量] 个商品
✅ 铺货提交成功
📦 目标店铺：[店铺名]
📊 铺货数量：[数量]
📝 铺货状态：正在铺货中...
```

## 常见问题

**Q: 如果"立即铺货"按钮找不到怎么办？**
A: 等待3-5秒让页面完全加载，然后使用快照查看页面状态，确认按钮位置。

**Q: 店铺选择框没有自动弹出？**
A: 检查是否已经有默认店铺被选中，或手动点击铺货按钮后等待弹窗。

**Q: 铺货日志页面一直在加载？**
A: 等待5-10秒，系统需要时间处理铺货请求。如果超过30秒仍无响应，检查是否有错误提示。

## 关键页面元素

| 功能 | 元素标识 |
|------|----------|
| AI选品按钮 | 文本包含"ai选品" |
| 搜索框 | placeholder包含"一句提问" |
| 查看详情 | 文本包含"查看详情" |
| 本页全选 | aria-label="Select all" |
| 立即铺货 | 文本包含"立即铺货" |
| 铺货日志 | 文本包含"铺货日志" |
| 复制日志 | 文本包含"复制日志" |
| kyeshop小店 | 文本包含"kyeshop小店" |

## 优化技巧

1. **批量执行**：将所有JavaScript操作合并到一个命令中，减少页面交互次数
2. **快速等待**：使用短间隔轮询（500ms）检查元素出现，而不是固定等待
3. **错误重试**：对关键操作（如点击"立即铺货"）添加自动重试机制
4. **日志确认**：每次操作后console.log状态，便于调试

## 示例调用

> 请去1688帮我选品，铺货到kyeshop小店，价格10-30元，其他条件默认

**执行结果：**
```
🔍 正在访问1688 AI选品...
🤖 AI选品条件：一件起批，48小时发货，7天无理由，包邮，价格在10-30元，退货率低于10%，最近好卖的商品
⏳ 等待AI生成结果...
✅ 找到563个商品
📋 正在全选商品...
✅ 已全选20个商品
🚀 正在提交铺货...
✅ 铺货提交成功
📦 目标店铺：kyeshop小店
📊 铺货数量：20个商品
📝 铺货状态：正在铺货中...可在铺货日志中查看详情
```
