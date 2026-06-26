# 🔐 环境变量安全管理器
## 核心亮点
1. 🛡️ **AES-256加密存储**：敏感信息自动加密，即使配置文件泄露也无法获取明文密钥
2. 🚫 **自动脱敏机制**：自动检测并脱敏输出中的敏感信息，防止密钥泄露到日志/聊天记录
3. 🔑 **权限控制**：访问敏感值需要显式授权，避免意外泄露
4. 🔄 **自动密钥生成**：首次使用自动生成安全密钥，也支持自定义密钥

## 🎯 适用场景
- 管理API密钥、数据库密码等敏感信息
- 防止敏感信息泄露到日志、输出或会话历史
- 批量加载环境变量，统一管理配置
- 多Agent环境下的安全配置共享

## 📝 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | 是 | 操作类型：init/set/get/list/delete/redact/loadFromEnv |
| key | string | 否 | set/get/delete操作必填，环境变量名，大写字母+下划线 |
| value | string | 否 | set操作必填，变量值 |
| isSecret | boolean | 否 | set操作可选，是否为敏感信息，默认false |
| allowSecret | boolean | 否 | get操作可选，是否允许获取敏感值，默认false |
| text | string | 否 | redact操作必填，要脱敏的文本 |
| prefix | string | 否 | loadFromEnv操作可选，环境变量前缀，默认OPENCLAW_ |
| encryptionKey | string | 否 | init操作可选，自定义32位加密密钥 |

## 💡 开箱即用示例
### 初始化（可选，建议启动时调用）
```typescript
// 使用自定义密钥
await skills.envSecureManager({
  action: "init",
  encryptionKey: "你的32位安全密钥"
});

// 自动生成密钥
await skills.envSecureManager({ action: "init" });
```

### 存储敏感密钥
```typescript
await skills.envSecureManager({
  action: "set",
  key: "OPENAI_API_KEY",
  value: "sk-xxx",
  isSecret: true
});
```

### 安全获取密钥
```typescript
const result = await skills.envSecureManager({
  action: "get",
  key: "OPENAI_API_KEY",
  allowSecret: true // 必须显式授权才能获取敏感值
});
```

### 输出自动脱敏
```typescript
// 即使日志里不小心打印了密钥，也会自动脱敏
const logText = `调用OpenAI API，密钥是sk-xxx，参数是xxx`;
const redacted = await skills.envSecureManager({
  action: "redact",
  text: logText
});
// 输出：调用OpenAI API，密钥是***REDACTED***，参数是xxx
```

## 🔧 技术实现说明
- 使用AES-GCM 256位加密算法，符合企业级安全标准
- 敏感信息永远不以明文存储，运行时解密
- 自动脱敏机制支持多值替换，覆盖所有泄露场景
- 轻量无依赖，不影响Agent执行性能
