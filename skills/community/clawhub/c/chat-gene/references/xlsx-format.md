# xlsx 格式规范 v3

## 文件结构

共 3 个 sheet：`group_info` / `active_members` / `message_stream`

---

## Sheet 1: group_info

| 列名 | 类型 | 说明 |
|------|------|------|
| 派id | 数字字符串 | 群唯一ID，如 "123456789" |
| 群名 | string | 群聊名称 |
| bot_config | null | 始终为 null |

示例行（header + 1行数据）：
```
派id       群名           bot_config
123456789  AI资讯交流群   null
```

---

## Sheet 2: active_members

| 列名 | 类型 | 说明 |
|------|------|------|
| id | 数字字符串 | 成员唯一ID |
| role | string | "user" 或 "assistant"（AI助手） |
| nickname | string | 微信昵称 |
| persona | string | 角色描述（年龄、职业、性格） |
| join_time | Excel时间序列数 | numFmt: `yyyy/m/d h:mm:ss;@` |

**注意**：`join_time` 含秒，格式与 `message_stream.time` 不同。

示例：
```javascript
// join_time 写法
const cell = { t: 'n', v: excelSerial, z: 'yyyy/m/d h:mm:ss;@' };
```

---

## Sheet 3: message_stream

有效列共 7 列（A–G）：

| 列 | 列名 | 类型 | 说明 |
|----|------|------|------|
| A | 轮次 | number | 从 1 开始，连续递增 |
| B | 消息类型 | string | "text" / "image" / "file" |
| C | 时间 | Excel时间序列数 | numFmt: `yyyy/m/d h:mm;@` |
| D | 发言人 | string | 成员昵称 |
| E | 内容 | string/null | text时非空，image/file时为null |
| F | task_list | null | 始终为 null |
| G | 附件 | string/null | image/file时为 image_N/file_N，text时为null |

### 消息类型规则

```
text:  内容 = "消息文字"  附件 = null
image: 内容 = null        附件 = "image_1"
file:  内容 = null        附件 = "file_1"
```

### 时间序列数计算

```javascript
function toExcelSerial(year, month, day, hour, minute, second = 0) {
  const epoch = new Date(Date.UTC(1899, 11, 30));
  const d = new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  return (d - epoch) / 86400000;
}
// 示例：2026-03-09 09:00 → 46090.375
```

### 时间分配策略

```
话题1 起始时间：当天 UTC 09:00
话题2 起始时间：当天 UTC 12:00（+0.125，约3小时）
话题3 起始时间：当天 UTC 15:00（+0.125）
每条消息间隔：0.002（约3分钟）
```

### ⚠️ numFmt Bug（必读）

`XLSX.utils.aoa_to_sheet` 和 `sheet_add_aoa` **不会保留** `z`（numFmt）属性。

**必须**对每个时间单元格手动设置：

```javascript
const addr = XLSX.utils.encode_cell({ r: rowIdx, c: colIdx });
ws[addr] = { t: 'n', v: excelSerial, z: 'yyyy/m/d h:mm;@' };
```

---

## 完整写入示例（Node.js）

```javascript
const XLSX = require('xlsx');

// 读取已有文件（含 group_info + active_members）
const wb = XLSX.readFile('output.xlsx', { cellStyles: true });
const ws = wb.Sheets['message_stream'];

msgs.forEach((msg, i) => {
  const r = i + 1; // row 0 = header
  
  function setCell(c, v, fmt) {
    const addr = XLSX.utils.encode_cell({ r, c });
    if (v === null) { ws[addr] = { t: 'z', v: null }; return; }
    if (fmt) ws[addr] = { t: 'n', v, z: fmt };
    else ws[addr] = { t: typeof v === 'number' ? 'n' : 's', v };
  }
  
  setCell(0, i + 1);                                    // 轮次
  setCell(1, msg.type);                                 // 消息类型
  setCell(2, msg.timeSerial, 'yyyy/m/d h:mm;@');        // 时间
  setCell(3, msg.speaker);                              // 发言人
  setCell(4, msg.content);                              // 内容
  setCell(5, null);                                     // task_list
  setCell(6, msg.attachment);                           // 附件
});

ws['!ref'] = `A1:G${msgs.length + 1}`;
XLSX.writeFile(wb, 'output.xlsx');
```
