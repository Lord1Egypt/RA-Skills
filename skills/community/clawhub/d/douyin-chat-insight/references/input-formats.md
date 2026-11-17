# 输入格式

本 skill **只吃用户自备导出**。

## 1. ChatLab JSONL（优先）

每行一个 JSON。常见 `_type`：

- `header`：`meta.name` / `meta.type` / `meta.platform`
- `member`：`platformId` / `accountName`
- `message`：`sender` / `accountName` / `timestamp` / `content` / `type`

`douyin-chat-export` 等工具的导出通常兼容。群成员很多时，即便 header 写成 private，解析器会按成员数纠成 group。

## 2. 目录

```
exports/
  group-a.jsonl
  dm-b.jsonl
```

`inventory` 每个文件一行概况。

## 3. 简易 JSON

```json
[
  {"sender": "于先生", "content": "陪跑怎么收费？", "ts": 1710000000}
]
```

或：

```json
{
  "name": "某群",
  "type": "group",
  "messages": [
    {"sender": "A", "content": "…", "ts": 1}
  ]
}
```

## 4. 纯文本

```
张三: 你好
李四: 怎么安装？
```

可选 `[时间] 昵称: 内容`。

## 不支持

- 直接贴 cookie / sessionid 让 skill 去拉
- 加密数据库裸文件（先自行导出成上文格式）
