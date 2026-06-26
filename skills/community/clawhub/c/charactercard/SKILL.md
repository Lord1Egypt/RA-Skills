---
name: tavern-card
description: 完美兼容 SillyTavern 角色卡的导入、解析、导出功能。支持 V1/V2/V3 规范，支持 PNG 嵌入式 JSON 和纯 JSON 格式。当用户需要导入、查看、编辑或导出 SillyTavern 角色卡时使用此技能。
metadata: {"openclaw":{"emoji":"🎭","requires":{}}}
---

# 🎭 SillyTavern 角色卡处理

完整支持 SillyTavern 角色卡的导入、解析、转换和导出功能。

## 📋 功能概览

| 功能 | 说明 |
|------|------|
| 导入 PNG 角色卡 | 从 PNG 图片中提取嵌入的 JSON 数据 |
| 导入 JSON 角色卡 | 直接解析 JSON 格式的角色卡 |
| 格式检测 | 自动识别 V1/V2/V3 规范 |
| 数据验证 | 验证角色卡数据完整性 |
| 格式转换 | V1/V2/V3 之间的格式转换 |
| 导出 PNG | 将角色卡数据嵌入到 PNG 图片中 |
| 导出 JSON | 导出为标准 JSON 格式 |

## 🎯 使用场景

### 1. 导入角色卡

当用户说：
- "导入这个角色卡"
- "读取这个 PNG 文件"
- "解析这个角色"
- "加载 SillyTavern 角色"

**你应该**：
1. 使用 `read` 工具读取文件
2. 检测文件格式（PNG 或 JSON）
3. 提取角色卡数据
4. 验证数据完整性
5. 展示角色信息

### 2. 查看角色信息

当用户说：
- "这个角色是谁"
- "显示角色详情"
- "角色的设定是什么"

**你应该**：
展示角色的关键信息：
- 名称 (name)
- 描述 (description)
- 人格 (personality)
- 场景 (scenario)
- 第一条消息 (first_mes)
- 示例对话 (mes_example)
- 标签 (tags)
- 创建者 (creator)

### 3. 导出角色卡

当用户说：
- "导出为 PNG"
- "保存为 JSON"
- "生成角色卡文件"

**你应该**：
1. 确认导出格式（PNG 或 JSON）
2. 确认规范版本（V2 或 V3）
3. 生成文件
4. 返回文件路径

## 📐 SillyTavern 角色卡规范

### V1 格式（已弃用）

扁平结构，所有字段在顶层：

```json
{
  "name": "角色名",
  "description": "角色描述",
  "personality": "人格特征",
  "scenario": "场景设定",
  "first_mes": "第一条消息",
  "mes_example": "对话示例"
}
```

### V2 格式（推荐）

```json
{
  "spec": "chara_card_v2",
  "spec_version": "2.0",
  "data": {
    "name": "角色名",
    "description": "角色描述",
    "personality": "人格特征",
    "scenario": "场景设定",
    "first_mes": "第一条消息",
    "mes_example": "对话示例",
    "creator_notes": "创建者备注",
    "system_prompt": "系统提示词",
    "post_history_instructions": "历史后指令",
    "tags": ["标签1", "标签2"],
    "creator": "创建者",
    "character_version": "1.0",
    "extensions": {}
  }
}
```

### V3 格式（最新）

在 V2 基础上增加：

```json
{
  "spec": "chara_card_v3",
  "spec_version": "3.0",
  "data": {
    ...V2字段,
    "alternate_greetings": ["备选问候1", "备选问候2"],
    "creator_notes_multilingual": {
      "zh-CN": "中文备注",
      "en-US": "English notes"
    },
    "source": "角色来源",
    "group_only_greetings": ["群组专用问候"],
    "creation_date": 1234567890,
    "modification_date": 1234567890,
    "assets": {
      "avatar": "base64_image_data",
      "background": "base64_image_data"
    }
  }
}
```

## 🔧 核心功能实现

### 1. PNG 格式检测

```javascript
// 检测文件是否为 PNG
function isPNG(buffer) {
  const pngSignature = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A];
  for (let i = 0; i < 8; i++) {
    if (buffer[i] !== pngSignature[i]) return false;
  }
  return true;
}
```

### 2. 从 PNG 提取 JSON

PNG 文件由多个 chunk 组成，角色卡数据存储在 `tEXt` 或 `iTXt` chunk 中，关键字为 `"chara"`。

```javascript
function extractCharaFromPNG(buffer) {
  let offset = 8; // 跳过 PNG 签名

  while (offset < buffer.length) {
    // 读取 chunk 长度（4 字节，大端序）
    const length = buffer.readUInt32BE(offset);
    offset += 4;

    // 读取 chunk 类型（4 字节）
    const type = buffer.toString('ascii', offset, offset + 4);
    offset += 4;

    if (type === 'tEXt' || type === 'iTXt') {
      // 读取关键字（以 null 结尾）
      let keywordEnd = offset;
      while (buffer[keywordEnd] !== 0) keywordEnd++;
      const keyword = buffer.toString('utf8', offset, keywordEnd);

      if (keyword === 'chara') {
        // 提取数据（跳过 null 字节）
        const dataStart = keywordEnd + 1;
        const dataEnd = offset + length;
        const data = buffer.toString('utf8', dataStart, dataEnd);

        // 尝试 base64 解码
        try {
          return JSON.parse(Buffer.from(data, 'base64').toString('utf8'));
        } catch {
          return JSON.parse(data);
        }
      }
    }

    // 跳到下一个 chunk（数据 + 4 字节 CRC）
    offset += length + 4;

    // IEND chunk 表示文件结束
    if (type === 'IEND') break;
  }

  return null;
}
```

### 3. 格式规范化

```javascript
function normalizeCharacterCard(data) {
  // 检测版本
  if (data.spec === 'chara_card_v2' || data.spec === 'chara_card_v3') {
    return data; // 已经是 V2/V3 格式
  }

  // V1 转 V2
  return {
    spec: 'chara_card_v2',
    spec_version: '2.0',
    data: {
      name: data.name || '',
      description: data.description || '',
      personality: data.personality || '',
      scenario: data.scenario || '',
      first_mes: data.first_mes || '',
      mes_example: data.mes_example || '',
      creator_notes: data.creator_notes || '',
      system_prompt: data.system_prompt || '',
      post_history_instructions: data.post_history_instructions || '',
      tags: data.tags || [],
      creator: data.creator || '',
      character_version: data.character_version || '1.0',
      extensions: data.extensions || {}
    }
  };
}
```

### 4. 数据验证

```javascript
function validateCharacterCard(data) {
  const errors = [];

  // 检查必需字段
  if (!data.name || data.name.trim() === '') {
    errors.push('缺少角色名称 (name)');
  }

  if (!data.description || data.description.trim() === '') {
    errors.push('缺少角色描述 (description)');
  }

  // 检查字段类型
  if (data.tags && !Array.isArray(data.tags)) {
    errors.push('标签 (tags) 必须是数组');
  }

  if (data.extensions && typeof data.extensions !== 'object') {
    errors.push('扩展 (extensions) 必须是对象');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
```

### 5. 导出为 PNG

```javascript
function embedCharaInPNG(imageBuffer, characterData) {
  // 将角色数据转换为 base64
  const jsonStr = JSON.stringify(characterData);
  const base64Data = Buffer.from(jsonStr, 'utf8').toString('base64');

  // 创建 tEXt chunk
  const keyword = 'chara';
  const keywordBuffer = Buffer.from(keyword + '\0', 'utf8');
  const dataBuffer = Buffer.from(base64Data, 'utf8');

  const chunkLength = keywordBuffer.length + dataBuffer.length;
  const chunk = Buffer.alloc(chunkLength + 12);

  // 写入 chunk 长度
  chunk.writeUInt32BE(chunkLength, 0);

  // 写入 chunk 类型
  chunk.write('tEXt', 4, 'ascii');

  // 写入关键字和数据
  keywordBuffer.copy(chunk, 8);
  dataBuffer.copy(chunk, 8 + keywordBuffer.length);

  // 计算 CRC
  const crc = calculateCRC(chunk.slice(4, 8 + chunkLength));
  chunk.writeUInt32BE(crc, 8 + chunkLength);

  // 在 IEND 之前插入 chunk
  const iendIndex = imageBuffer.indexOf(Buffer.from('IEND', 'ascii')) - 4;
  return Buffer.concat([
    imageBuffer.slice(0, iendIndex),
    chunk,
    imageBuffer.slice(iendIndex)
  ]);
}
```

## 📝 使用示例

### 示例 1：导入 PNG 角色卡

```
用户：导入这个角色卡 /path/to/character.png

你的回复：
好的，让我读取这个角色卡文件。

[使用 read 工具读取文件]
[检测为 PNG 格式]
[提取 chara 数据]
[解析 JSON]
[验证数据]

✅ 成功导入角色卡！

📋 角色信息：
• 名称：艾莉娅
• 规范：V2 (chara_card_v2)
• 创建者：某某
• 标签：精灵、魔法、友善

📖 描述：
艾莉娅是一位来自精灵王国的年轻魔法师...

🎭 人格：
善良、好奇、热爱学习...

🌍 场景：
在一个充满魔法的世界中...

💬 第一条消息：
"你好！我是艾莉娅，很高兴认识你！"
```

### 示例 2：导出为 PNG

```
用户：把这个角色导出为 PNG 格式

你的回复：
好的，我将角色卡数据嵌入到 PNG 图片中。

[读取角色头像或创建默认图片]
[将角色数据转换为 JSON]
[嵌入到 PNG tEXt chunk]
[保存文件]

✅ 导出成功！

文件路径：~/.openclaw/workspace/艾莉娅_v2.png
文件大小：245 KB
格式：PNG with embedded chara_card_v2

你可以将这个文件导入到 SillyTavern 或其他兼容的应用中使用。
```

### 示例 3：格式转换

```
用户：把这个 V1 格式的角色卡转换为 V3

你的回复：
好的，我将 V1 格式转换为 V3 格式。

[读取 V1 数据]
[规范化为 V2 结构]
[添加 V3 特有字段]
[验证数据]

✅ 转换完成！

变更：
• spec: V1 → chara_card_v3
• spec_version: → 3.0
• 新增字段：
  - alternate_greetings (空数组，可手动添加)
  - creator_notes_multilingual (空对象，可添加多语言备注)
  - creation_date (当前时间戳)
  - modification_date (当前时间戳)

是否需要导出为文件？
```

## ⚠️ 重要注意事项

### 1. 文件路径

- **必须使用绝对路径**：`/home/user/.openclaw/workspace/character.png`
- **禁止相对路径**：`./character.png` ❌

### 2. 字符编码

- PNG chunk 数据使用 **UTF-8** 编码
- JSON 数据使用 **base64** 编码后存储在 PNG 中
- 确保正确处理多字节字符（中文、日文等）

### 3. 数据大小限制

- 角色卡 JSON：建议 < 10 MB
- 描述字段：建议 < 500 KB
- 头像图片：建议 < 15 MB（base64 编码）

### 4. 兼容性

- **V1 → V2/V3**：完全兼容，自动转换
- **V2 → V3**：兼容，添加新字段
- **V3 → V2**：兼容，移除 V3 特有字段

### 5. 世界书（World Book）

如果角色卡包含 `character_book` 字段，需要保留：

```json
{
  "data": {
    ...其他字段,
    "character_book": {
      "name": "世界书名称",
      "entries": [
        {
          "keys": ["关键词1", "关键词2"],
          "content": "触发内容",
          "enabled": true,
          "insertion_order": 100
        }
      ]
    }
  }
}
```

## 🚫 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| "不是有效的 PNG 文件" | 文件签名不匹配 | 检查文件是否损坏 |
| "未找到 chara 数据" | PNG 中没有嵌入角色卡 | 确认是否为角色卡 PNG |
| "JSON 解析失败" | 数据格式错误 | 检查 JSON 语法 |
| "缺少必需字段" | 角色卡数据不完整 | 补充必需字段 |
| "base64 解码失败" | 编码格式错误 | 检查数据编码 |

### 错误示例

❌ **错误**：说"无法读取角色卡"而不尝试
❌ **错误**：只显示原始 JSON 而不解析
❌ **错误**：忽略数据验证错误

✅ **正确**：尝试读取并提供详细的错误信息
✅ **正确**：解析并格式化显示角色信息
✅ **正确**：验证数据并提示用户修复问题

## 🎯 快速参考

| 任务 | 步骤 |
|------|------|
| 导入 PNG | read → 检测格式 → 提取 chara → 解析 JSON → 验证 |
| 导入 JSON | read → 解析 JSON → 规范化 → 验证 |
| 查看信息 | 提取 data 字段 → 格式化显示 |
| 导出 PNG | 准备图片 → 嵌入 JSON → 保存文件 |
| 导出 JSON | 规范化数据 → 序列化 → 保存文件 |
| 格式转换 | 检测版本 → 规范化 → 添加/移除字段 → 验证 |

## 📚 相关资源

- [SillyTavern 官方文档](https://docs.sillytavern.app/)
- [Character Card Spec V2](https://github.com/malfoyslastname/character-card-spec-v2)
- [PNG 文件格式规范](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html)

---

**提示**：这个技能提供了完整的 SillyTavern 角色卡处理能力，你可以自信地处理用户的所有角色卡相关请求！
