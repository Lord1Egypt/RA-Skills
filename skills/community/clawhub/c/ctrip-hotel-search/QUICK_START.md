# 快速开始指南

## 🎯 立即使用（无需等待浏览器下载）

### 1. 查看演示数据
```bash
node tests/demo.js
```
这将展示完整的搜索结果示例，帮助您了解输出格式。

### 2. 根据演示数据手动搜索
根据演示数据中的酒店名称，在携程官网手动搜索并预订。

---

## 🔧 完整使用（等待浏览器下载完成）

### 步骤1：配置账号
编辑 `config.json`：
```json
{
  "ctrip": {
    "username": "您的携程账号",
    "password": "您的携程密码"
  }
}
```

### 步骤2：运行搜索
```bash
# 搜索建水古城酒店
node -e "
const { search } = require('./src/index');
search({
  city: '建水古城',
  checkInDate: '2026-04-09',
  checkOutDate: '2026-04-10',
  priceRange: { min: 200, max: 400 }
}).then(result => {
  console.log(JSON.stringify(result.report, null, 2));
});
"
```

### 步骤3：查看结果
搜索结果将包含：
- 酒店列表（名称、价格、评分、位置）
- 对比分析（性价比、评分排序）
- 推荐列表（最经济、评分最高、性价比最高）

---

## 📱 针对您的行程

### 建水古城（4月9日）
```bash
node -e "
const { search } = require('./src/index');
search({
  city: '建水古城',
  checkInDate: '2026-04-09',
  checkOutDate: '2026-04-10',
  priceRange: { min: 200, max: 400 },
  hotelType: 'homestay'
}).then(result => {
  console.log('🏨 建水古城酒店推荐:');
  result.report.topPicks.forEach((pick, index) => {
    console.log(\`\${index + 1}. \${pick.name} - ¥\${pick.price} - \${pick.rating}\`);
    console.log(\`   理由: \${pick.reason}\`);
  });
});
"
```

### 南沙镇（4月12日）
```bash
node -e "
const { search } = require('./src/index');
search({
  city: '南沙镇',
  checkInDate: '2026-04-12',
  checkOutDate: '2026-04-13',
  priceRange: { min: 150, max: 300 },
  hotelType: 'homestay'
}).then(result => {
  console.log('🏨 南沙镇酒店推荐:');
  result.report.topPicks.forEach((pick, index) => {
    console.log(\`\${index + 1}. \${pick.name} - ¥\${pick.price} - \${pick.rating}\`);
    console.log(\`   理由: \${pick.reason}\`);
  });
});
"
```

---

## 🛠️ 故障排除

### 问题1：浏览器下载慢
**解决方案：**
- 等待下载完成（约10-20分钟）
- 或使用演示数据手动搜索

### 问题2：登录失败
**解决方案：**
1. 手动登录携程确认账号状态
2. 检查账号密码是否正确
3. 确认网络连接正常

### 问题3：搜索无结果
**解决方案：**
1. 检查城市名称是否正确
2. 确认日期格式是否正确
3. 尝试扩大价格范围
4. 使用更通用的城市名称（如"元阳"代替"南沙镇"）

### 问题4：验证码问题
**解决方案：**
- 技能会自动检测验证码
- 需要手动完成验证码输入
- 建议提前手动登录一次携程

---

## 💡 使用建议

### 1. 提前准备
- 提前手动登录携程，保持登录状态
- 准备好携程账号密码
- 确认网络连接稳定

### 2. 合理使用
- 避免频繁搜索（每分钟不超过3次）
- 尊重网站规则，不要过度爬取
- 搜索结果仅供参考，最终以官网为准

### 3. 数据安全
- 妥善保管配置文件
- 不要分享包含账号密码的文件
- 定期更新密码

---

## 📞 获取帮助

如果遇到问题：
1. 查看 `README.md` 了解详细功能
2. 查看 `USAGE.md` 了解使用方法
3. 查看 `PROJECT_SUMMARY.md` 了解项目详情
4. 检查浏览器下载进度：`process list`

---

## 🎯 下一步行动

### 立即行动（推荐）
1. 运行 `node tests/demo.js` 查看演示数据
2. 根据演示数据中的酒店名称，在携程官网手动搜索
3. 根据推荐选择合适的酒店进行预订

### 等待完整功能
1. 等待浏览器下载完成（约10-20分钟）
2. 配置携程账号
3. 运行完整搜索流程

---

**祝您旅途愉快！** 🎉