# 欧路词典/法语助手/德语助手/西语助手 (Eudic OpenAPI)

本技能提供 欧路词典/法语助手/德语助手/西语助手OpenAPI 的调用能力，用于管理生词本、笔记和语音评分等功能。

## 何时使用 (触发条件)

当用户提出以下类型的请求时，应使用本技能：

- "查看我的生词本"
- "添加单词到生词本"
- "查询某个单词"
- "添加笔记"
- "查看笔记"
- "删除生词本/单词/笔记"
- "语音评分"

## 环境配置

### 获取 API Token

1. 访问 https://my.eudic.net/OpenAPI/Authorization 获取 API Token
2. 格式：`NIS {token}`

### 支持的语言与应用名称

| 语言 | language 参数 | 应用名称 |
|------|--------------|----------|
| 英语 | en | 欧路词典 |
| 法语 | fr | 法语助手 |
| 德语 | de | 德语助手 |
| 西班牙语 | es | 西语助手 |

**注意**: 调用 API 时需要通过 `language` query 参数指定语言。

---

## 核心功能与用法

### 1. 获取所有生词本

```bash
# language: en=欧路词典, fr=法语助手, de=德语助手, es=西语助手
curl -s "https://api.frdic.com/api/open/v1/studylist/category?language=en" \
  -H "Authorization: NIS {你的Token}"
```

**参数**: 
- `language`: en/fr/de/es (必填)

**返回**: 生词本列表 (id, language, name, add_time)

---

### 2. 添加新生词本

```bash
curl -s -X POST "https://api.frdic.com/api/open/v1/studylist/category" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"language": "en", "name": "新单词本"}'
```

**参数**:
- `language`: en/fr/de/es (必填)
- `name`: 生词本名称 (必填)

---

### 3. 重命名生词本

```bash
curl -s -X PATCH "https://api.frdic.com/api/open/v1/studylist/category" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"id": "生词本ID", "language": "en", "name": "新名称"}'
```

**参数**:
- `id`: 生词本ID (必填)
- `language`: en/fr/de/es (必填)
- `name`: 新名称 (必填)

---

### 4. 删除生词本

```bash
curl -s -X DELETE "https://api.frdic.com/api/open/v1/studylist/category" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"id": "生词本ID", "language": "en", "name": "生词本名称"}'
```

---

### 5. 获取生词本单词

```bash
curl -s "https://api.frdic.com/api/open/v1/studylist/words?language=en&category_id=0&page=1&page_size=100" \
  -H "Authorization: NIS {你的Token}"
```

**参数**:
- `language`: en/fr/de/es (必填)
- `category_id`: 生词本ID (必填)
- `page`: 页码 (可选，默认1)
- `page_size`: 每页数量 (可选，默认100)

**返回**: 单词列表 (word, phon, exp, add_time, star, context_line)

---

### 6. 批量添加单词

```bash
curl -s -X POST "https://api.frdic.com/api/open/v1/studylist/words" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"language": "en", "category_id": "0", "words": ["apple", "banana", "orange"]}'
```

**参数**:
- `language`: en/fr/de/es (必填)
- `category_id`: 生词本ID (必填)
- `words`: 单词数组 (必填)

---

### 7. 删除单词

```bash
curl -s -X DELETE "https://api.frdic.com/api/open/v1/studylist/words" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"language": "en", "category_id": "0", "words": ["apple"]}'
```

---

### 8. 新增单个单词

```bash
curl -s -X POST "https://api.frdic.com/api/open/v1/studylist/word" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"language": "en", "word": "hello", "star": 2, "context_line": "Hello, how are you?"}'
```

**参数**:
- `language`: en/fr/de/es (必填)
- `word`: 单词 (必填)
- `star`: 星级 1-5 (可选)
- `context_line`: 语境例句 (可选)
- `category_ids`: 分组ID列表 (可选)

---

### 9. 查询单词

```bash
curl -s "https://api.frdic.com/api/open/v1/studylist/word?language=en&word=hello" \
  -H "Authorization: NIS {你的Token}"
```

**参数**:
- `language`: en/fr/de/es (必填)
- `word`: 单词 (必填)

**返回**: 单词详情

---

### 10. 获取笔记列表

```bash
curl -s "https://api.frdic.com/api/open/v1/studylist/notes?page=0&page_size=100" \
  -H "Authorization: NIS {你的Token}"
```

**参数**:
- `page`: 页码 (可选，默认0)
- `page_size`: 每页数量 (可选，默认100)

**返回**: 笔记列表 (word, note, language, add_time)

---

### 11. 获取单个单词笔记

```bash
curl -s "https://api.frdic.com/api/open/v1/studylist/note?word=hello" \
  -H "Authorization: NIS {你的Token}"
```

**参数**:
- `word`: 单词 (必填)

**返回**:单词笔记不存在会返回404.存在会返回单词内容
---

### 12. 新增笔记

```bash
curl -s -X POST "https://api.frdic.com/api/open/v1/studylist/note" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"word": "hello", "note": "这是笔记内容"}'
```

**参数**:
- `word`: 单词 (必填)
- `note`: 笔记内容 (必填)

---

### 13. 删除笔记

```bash
curl -s -X DELETE "https://api.frdic.com/api/open/v1/studylist/note" \
  -H "Authorization: NIS {你的Token}" \
  -H "Content-Type: application/json" \
  -d '{"word": "hello"}'
```

---

### 14. 语音评估

```bash
curl -s -X POST "https://api.frdic.com/api/open/v1/voice/eval" \
  -H "Authorization: NIS {你的Token}" \
  -F "line=Hello world" \
  -F "voice=@test.wav"
```

**注意**: 目前只支持英语，语音文件支持 wav 格式

**返回**: 评估结果 (score综合分数, words单词列表, phones音节分数)

---

## 响应码

| 响应码 | 含义 |
|--------|------|
| 200 | 成功 (GET) |
| 201 | 创建/修改成功 (POST/PATCH) |
| 204 | 删除成功 (DELETE) |
| 400 | 参数错误 |
| 401 | 授权认证失败 |
| 403 | 访问过于频繁 |

## 流量限制

| 周期 | 限制次数 | 封停时间 |
|------|----------|----------|
| 1分钟 | 30次 | 1小时 |
| 30分钟 | 500次 | 24小时 |