# 执行流程

## 状态管理

```javascript
// 内存存储（不写文件）
class StateManager {
  constructor() {
    this.states = new Map();
  }
  
  saveState(userId, state) {
    this.states.set(userId, state);
  }
  
  loadState(userId) {
    return this.states.get(userId);
  }
}
```

## 输入验证

```javascript
function validateInput(input, maxLength = 1000) {
  if (!input || typeof input !== 'string') {
    return { valid: false, error: '输入无效' };
  }
  if (input.length > maxLength) {
    return { valid: false, error: `输入过长` };
  }
  
  // 过滤危险字符
  const dangerous = /[<>{}[\]\\\/]/;
  if (dangerous.test(input)) {
    return { valid: false, error: '输入包含非法字符' };
  }
  
  return { valid: true, sanitized: input.trim() };
}
```

## 日志脱敏

```javascript
function sanitizeLog(input) {
  if (typeof input !== 'string') return input;
  
  // 邮箱脱敏
  input = input.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '[EMAIL_REDACTED]');
  
  // 手机号脱敏
  input = input.replace(/1[3-9]\d{9}/g, '[PHONE_REDACTED]');
  
  // 凭证脱敏
  const sensitiveKeys = ['token', 'secret', 'password', 'key', 'credential'];
  for (const key of sensitiveKeys) {
    const regex = new RegExp(`(${key}['":\\s]*)(['\"]?[^'\"\\s,]+)`, 'gi');
    input = input.replace(regex, '$1[REDACTED]');
  }
  
  return input;
}
```

## 完成配置

```javascript
function completeConfiguration(userId) {
  const state = loadState(userId);
  
  return {
    message: `🎉 配置完成！
    
配置摘要：
- 基础配置：已设置
- 渠道：${state.step_data[4]?.platform || '未设置'}
- 人格：${state.step_data[7]?.type || '未设置'}

💡 提示：
- 说"上一步"可以回退修改
- 说"状态"查看进度
- 重启后配置会清除（内存存储）`,
    completed: true
  };
}
```
