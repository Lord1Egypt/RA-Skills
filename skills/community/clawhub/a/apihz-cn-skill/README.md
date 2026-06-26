# 接口盒子 API Skill

> 409+ 企业级 API 接口 - 稳定、高效、易用

## 📦 安装

```bash
clawhub install apihz
```

## 🚀 快速开始

### 1. 获取认证信息

访问 https://www.apihz.cn/?shareid=10013679 注册账号，获取：
- **开发者 ID** (数字)
- **通讯 Key** (字符串)

### 2. 配置认证

```bash
node skills/apihz/scripts/init-wizard.js
```

### 3. 使用示例

```javascript
const { ApiHzClient } = require('./skills/apihz/src/client-enhanced.js');

const client = new ApiHzClient({
  id: '你的 ID',
  key: '你的 KEY',
  baseUrl: 'https://cn.apihz.cn'
});

// 查询天气
const weather = await client.weather({ 
  province: '安徽', 
  city: '芜湖' 
});
console.log(weather);
```

## 📋 核心 API

| API | 说明 | 免费额度 |
|-----|------|---------|
| 天气预报 | 国内城市天气预报 | ✅ 100 次/天 |
| 地震数据 | 最新地震信息 | ✅ 100 次/天 |
| 时间戳 | 北京时间 | ✅ 100 次/天 |
| IP 归属地 | 全球 IP 定位 | ✅ 100 次/天 |
| ICP 备案 | 企业备案查询 | ✅ 100 次/天 |
| 临时邮箱 | 生成随机邮箱 | ✅ 100 次/天 |
| 翻译服务 | 多语言翻译 | ✅ 100 次/天 |

## 🔧 使用方式

### 交互式调用 (推荐)

```bash
node skills/apihz/scripts/call-api.js
```

**调用流程:**
```
=========================================
接口盒子 API - 交互式调用
=========================================

✅ 已加载配置：开发者 ID 10013679
✅ 获取到 41 个分类

📦 选择 API 分类
==================================================
  1. 综合分类
  2. 时间操作
  3. 邮件短信
  ...
请输入分类编号：13

📂 已选择分类：天气预报
✅ 获取到 15 个 API

🔌 选择 API 接口
==================================================
  1. 国内城市天气预报 [免费]
  2. IP 定位天气查询 [免费]
  ...
请输入 API 编号：1

🔌 已选择 API: 国内城市天气预报
请输入 API 参数:
省份 (默认：安徽):
城市 (默认：芜湖):

正在调用 API...
✅ 调用成功!
```

### 代码调用

```javascript
const { ApiHzClient } = require('./skills/apihz/src/client-enhanced.js');
const client = new ApiHzClient({ id, key, baseUrl });
const weather = await client.weather({ province: '安徽', city: '芜湖' });
```

## 💎 会员升级

| 等级 | 价格 | 频次 |
|------|------|------|
| 免费 | ¥0 | 10 次/分钟 |
| 彩钻 | ¥30/月 | 310 次/分钟 |
| 炫钻 | ¥50/月 | 1010 次/分钟 |

## 📞 支持

- 官网：https://www.apihz.cn
- QQ 群：500700444

## 📄 License

MIT
