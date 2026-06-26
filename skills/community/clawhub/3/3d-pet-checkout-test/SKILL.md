---
name: 3d-pet-checkout-test
description: 执行 3D Pet 宠物下单测试完整流程，包含登录、选择产品、上传图片、等待生成、验证结账。用于自动化测试 joyarti 3D 宠物产品购买流程。
---

# 3D Pet 下单测试

执行 3D 宠物产品下单完整流程，验证购买路径是否正常。

## 触发条件

- 用户说"测试3D宠物"、"测试下单"、"3D Pet test"、"运行工作流"
- cron 定时任务触发
- 手动执行测试

## 关键配置

| 配置 | 环境变量 | 默认值 |
|------|----------|--------|
| 网站 | - | https://joyarti.com |
| 账号邮箱 | JOYARTI_EMAIL | (无默认值，请设置) |
| 账号密码 | JOYARTI_PASSWORD | (无默认值，请设置) |
| 测试图片 | JOYARTI_IMAGE_URL | (可选) |
| 推送目标 | FEISHU_TARGET | (无默认值，需配置) |

## 环境变量设置

在运行前设置环境变量（可选，如不设置则使用默认值）：

```bash
export JOYARTI_EMAIL="your-email@example.com"
export JOYARTI_PASSWORD="your-password"
export JOYARTI_IMAGE_URL="https://example.com/image.jpg"
export FEISHU_TARGET="chat:oc_xxxxxxxxxxxxxxxxxx"
```

## 执行步骤

### Step A: 登录
1. navigate 到 https://joyarti.com/account/login
2. wait 2000ms
3. evaluate 填写邮箱密码并点击 Login
4. wait 4000ms 等待跳转
5. evaluate 验证登录成功（URL 含 /account）

### Step B: 选择产品
1. evaluate 点击导航 '3D Figure'
2. wait 3000ms，验证 URL 含 figmaker
3. evaluate 点击 'For Pets' **（必须用 BUTTON 元素）**
4. wait 3000ms
5. evaluate 点击 'Minimal Style' 的 Create 按钮 **（必须用 BUTTON 元素）**
6. wait 3000ms，验证 URL 含 style2 且有文件上传框

### Step C: 上传图片
1. exec 下载图片到 /tmp/openclaw/uploads/pet_image.jpg
2. exec 运行 CDP 上传脚本：
   ```bash
   CDP_SCRIPT="${WORKSPACE}/cdp_upload.py"  # 或从 skill 目录读取
   python3 "$CDP_SCRIPT" /tmp/openclaw/uploads/pet_image.jpg joyarti
   ```
   - 成功输出：`OK: files=1`
   - 失败输出：`ERR: ...`
3. wait 3000ms
4. evaluate 点击 Create Preview 按钮

### Step D: 等待生成
1. **禁止用 browser wait 超过 20s**
2. 用 exec + curl 轮询，每次 sleep 30s：
   ```bash
   sleep 30 && curl -s http://127.0.0.1:18800/json/list | python3 -c "
   import json,sys
   tabs=json.load(sys.stdin)
   for t in tabs:
       if 'joyarti' in t.get('url','') and 'projectId' in t.get('url',''):
           print('DONE:', t['url'])
   "
   ```
3. 检测输出含 `DONE:` 即生成完成，提取 projectId

### Step E: 验证结账
1. evaluate 点击 Buy Now
2. wait 4000ms
3. evaluate 验证跳转到 Shopify（URL 含 myshopify.com 或 checkout）
4. evaluate 读取结账关键字段（产品、价格）
5. 验证：产品含 'Pet'/'Figure'，价格含 '$89.99'
6. **必须登出并关闭浏览器**

## 消息规则

每个 Step 开始和完成必须发消息到飞书群：

```javascript
message(action=send, channel=feishu, target=FEISHU_TARGET, message="...")
```

- Step 开始：`⏳ Step X: xxx 开始...`
- Step 完成：`✅ Step X: xxx 完成 — {关键结果}`
- Step 失败：`❌ Step X: xxx 失败 — {原因}`

## 最终报告模板

```
🧪 3D Pet 下单测试报告
时间：{startTime}–{endTime}（约 {duration} 分钟）
**账号：** JOYARTI_EMAIL

A: 登录 - {结果}
B: 选择产品 - {结果}
C: 上传图片 - {结果}
D: 3D 生成 - {结果}
E: 结账验证 - {结果}

projectId: {projectId}
产品: {product}
价格: {price}

结论：{通过/失败}
```

## 注意事项

1. **点击必须用 BUTTON**：禁止点击 SPAN/DIV 元素，必须用 `querySelectorAll('button')` 限定
2. **上传用 CDP 脚本**：`browser.upload()` 不触发 React onChange
3. **生成等待用 exec**：禁止 `browser.act kind=wait timeMs>20000`
4. **必须登出关闭浏览器**：确保下次测试干净
5. **禁止点击 Place order/Pay now**：只验证不付款