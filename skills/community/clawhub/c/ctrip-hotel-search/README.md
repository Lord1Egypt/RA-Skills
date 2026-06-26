# 携程酒店搜索 Skill

自动搜索携程酒店，支持实时比价和详情获取。

## 功能特性

- ✅ 自动登录携程账号
- ✅ 实时搜索酒店（按地点、日期、价格筛选）
- ✅ 获取酒店详情和用户评价
- ✅ 多酒店对比分析
- ✅ 支持民宿/客栈搜索

## 安装要求

1. Node.js 16+
2. 携程账号

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/ctrip-hotel-search
npm install
npx playwright install
```

### 2. 配置账号

编辑 `config.json`：
```json
{
  "ctrip": {
    "username": "your_username",
    "password": "your_password"
  }
}
```

### 3. 使用示例

```javascript
const { search } = require('./src/index');

// 搜索建水古城酒店
const result = await search({
  city: '建水古城',
  checkInDate: '2026-04-09',
  checkOutDate: '2026-04-10',
  priceRange: { min: 200, max: 400 }
});

console.log(result.report);
```

## API 参考

### search(params)

搜索酒店

**参数：**
- `city` - 城市名称
- `checkInDate` - 入住日期 (YYYY-MM-DD)
- `checkOutDate` - 退房日期 (YYYY-MM-DD)
- `priceRange` - 价格范围 {min, max}
- `hotelType` - 酒店类型 ('all', 'hotel', 'homestay')
- `getDetails` - 是否获取详情 (boolean)

**返回：**
- `success` - 是否成功
- `hotels` - 酒店列表
- `comparison` - 对比分析
- `report` - 搜索报告

## 注意事项

1. **验证码处理**：如果遇到验证码，需要手动完成
2. **页面结构**：携程页面可能更新，需要定期维护选择器
3. **请求频率**：避免过快请求，防止被封IP
4. **账号安全**：妥善保管配置文件中的账号密码

## 故障排除

### 登录失败
- 检查账号密码是否正确
- 确认网络连接正常
- 手动登录携程确认账号状态

### 搜索无结果
- 检查城市名称是否正确
- 确认日期格式是否正确
- 尝试扩大价格范围

### 浏览器崩溃
- 确保安装了最新版 Playwright
- 检查系统资源是否充足

## 开发计划

- [ ] 添加验证码自动识别
- [ ] 支持更多筛选条件（星级、设施等）
- [ ] 添加预订功能
- [ ] 支持批量搜索
- [ ] 添加价格趋势分析

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT