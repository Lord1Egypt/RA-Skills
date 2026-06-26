# 飞书@提及格式说明

## 📋 官方文档

根据飞书官方文档，正确的@提及格式是 **XML 标签**。

```xml
<!-- @单个用户 -->
<at user_id="ou_xxxxxxx">用户名</at>

<!-- @机器人 -->
<at user_id="ou_xxxxxx">机器人名</at>

<!-- @所有人 -->
<at user_id="all">所有人</at>
```

---

## ✅ 正确的方式 (v2.0)

### 使用解析器自动转换（推荐）

无需手动拼接 XML 标签，使用 `feishu-mention` 技能自动处理：

```javascript
import { resolve } from './index.js';

async function send() {
  // 1. 原始文本
  const text = '请 @product 帮忙 @张三 看一下';
  
  // 2. 调用解析器 (使用 accountId='elves')
  const resolvedText = await resolve(text, 'elves', 'oc_123...');
  
  // resolvedText 结果：
  // "请 <at user_id="ou_prod_id">product</at> 帮忙 <at user_id="ou_zhangsan_id">张三</at> 看一下"
  
  // 3. 发送到飞书 (支持 text 或 post 类型)
  await sendMessage({
    msg_type: 'text',
    content: JSON.stringify({ text: resolvedText })
  });
}
```

---

## ❌ 常见错误

### 1. 直接拼接 OpenID

```javascript
// ❌ 错误 - 不会触发提醒
const message = '@张三 ou_123456 在吗';
```

### 2. 拼写错误的 XML

```javascript
// ❌ 错误 - 属性名错误
<at userid="ou_xxx">张三</at>

// ❌ 错误 - 缺少闭合标签
<at user_id="ou_xxx">张三
```

---

## 🔍 原理说明

`feishu-mention` 解析器的工作原理：

1.  **扫描**: 找出文本中所有的 `@name`。
2.  **查找**: 
    *   在 `openclaw.json` 中查找匹配的机器人。
    *   在群成员中查找匹配的用户。
3.  **替换**: 将 `@name` 替换为 `<at user_id="found_id">name</at>`。
4.  **保留**: 如果未找到对应用户，保留原文本 `@name`。
