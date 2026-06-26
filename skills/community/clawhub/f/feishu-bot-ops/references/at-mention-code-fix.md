# AT_MAP 代码补丁（@mention 转换）

## 问题

Feishu adapter 的 `_build_outbound_payload()` 始终返回纯文本 `{"text": content}`，`@用户名` 只是装饰性文字，不触发飞书通知。需要通过 `FEISHU_AT_MAP` 环境变量将 `@显示名` 自动转为飞书 post 消息的 `<at>` 标签。

## 5 处代码改动

以下改动在 `gateway/platforms/feishu.py` 中进行。

### 改动 1：FeishuAdapterSettings 新增字段

```python
at_mention_map: Dict[str, str] = field(default_factory=dict)  # display_name → open_id
```

### 改动 2：_load_settings 读取环境变量

```python
at_mention_map=_parse_at_mention_map(
    os.getenv("FEISHU_AT_MAP", "")
),
```

### 改动 3：_apply_settings 赋值

```python
self._at_mention_map = settings.at_mention_map
```

### 改动 4：新增两个函数

`_parse_at_mention_map()` 和 `_build_at_mention_post_payload()`，插入在 `_build_markdown_post_payload` 之前。

- `_parse_at_mention_map`：解析 `name1=ou_xxx,name2=ou_yyy` 格式，按名称长度降序排序
- `_build_at_mention_post_payload`：扫描内容中的 `@display_name`，匹配后拆分为 `{"tag":"md", ...}` 和 `{"tag":"at","user_id":"ou_xxx","user_name":"名字"}` 交替排列的 post content

**⚠️ 已知 bug**：`\b` 边界匹配对中文名无效（中文字符不是 `\w`），会导致 `@中文名` 检测失败。修复：去掉 regex 中的 `\\b` 或使用其他边界检测方式。

### 改动 5：_build_outbound_payload 调用 @mention 转换

在 markdown table 检查后、markdown hint 检查前插入：

```python
at_post = _build_at_mention_post_payload(content, self._at_mention_map)
if at_post is not None:
    return "post", at_post
```

> 必须在 `_MARKDOWN_HINT_RE`（markdown 转 post）之前，因为 @mention 必须以 post 类型发送。

## 环境变量

```bash
# .env
FEISHU_AT_MAP=显示名=open_id,别名=open_id
```

多个映射用逗号分隔，允许多个显示名指向同一 open_id。

## 验证

```bash
# 检测补丁是否存在
grep "at_mention_map\|_parse_at_mention" <hermes_home>/gateway/platforms/feishu.py

# 应有至少 5 处匹配。如果返回空 → 补丁已丢失
```

发送 `@某人` 测试消息后，用飞书 API 反查：

```bash
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" | \
  grep -oP '"tenant_access_token":"\K[^"]+')

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://open.feishu.cn/open-apis/im/v1/messages/<message_id>"
```

- `msg_type: post` + `mentions` 含目标 open_id = ✅ 生效
- `msg_type: text` = ❌ 未生效

## 备份

改前先备份：

```bash
cp <hermes_home>/gateway/platforms/feishu.py{,.bak.$(date +%Y%m%d_%H%M%S)}
```
