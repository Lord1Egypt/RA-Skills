# 百度有驾汽车查询 API Key 配置指南

当 `YOUJIA_API_KEY` 未配置时，有两种方式获取 Key。

## 方式一：手机号验证码获取（推荐）

通过手机号 + 验证码自动获取 `X-Youjia-OpenAPI-Key`，无需手动配置。

### 流程概述

1. 发送手机号 → 接收验证码
2. 输入验证码 → 返回 API Key
3. Key 自动持久化到 `~/.youjia/key.json`，并**覆盖**环境变量 `YOUJIA_API_KEY` 与 skill 包内 `.env`

> 验证码重新申请拿到的新 Key 会覆盖本地旧配置，避免旧 Key 因解析优先级继续生效。

详细流程见 `tempkey-guide.md`。

---

## 方式二：手动配置

如果你已有 `X-Youjia-OpenAPI-Key`，可通过以下方式手动配置：

### 1. 配置环境变量

```bash
export YOUJIA_API_KEY="sk-xxxxxxxxxxxxx"
```

### 2. 配置到 .env 文件（推荐）

在本 skill 目录下创建 `.env` 文件（参考 `.env.example`）：

```bash
cp .env.example .env
# 编辑 .env，填入你的 Key
```

或使用代码：

```python
from youjia_client import save_key_to_dotenv

save_key_to_dotenv("sk-xxxxxxxxxxxxx")
```

---

## API 详情

- **车价查询端点**: `GET https://youjia.baidu.com/bff-third-api/openapi/v1/clue/askprice/popbefore`
- **认证方式**: `X-Youjia-OpenAPI-Key` 请求头
- **参数**:
  - `query` (必填): 查询内容，必须包含车系名
  - `city` (可选): 城市名，默认北京
  - `clue_source_type` (固定): `ai_price`

### 示例请求

curl --location 'https://youjia.baidu.com/bff-third-api/openapi/v1/clue/askprice/popbefore?query=%E5%A5%A5%E8%BF%AAA4L&city=%E5%8C%97%E4%BA%AC&clue_source_type=ai_price' \
  --header 'X-Youjia-OpenAPI-Key: sk-xxxxxxxxxxxxx'
```

## Key 解析优先级

1. 用户传入参数 `YoujiaClient(key="...")`
2. 环境变量 `YOUJIA_API_KEY`
3. skill 包内 `.env` 文件
4. `~/.youjia/key.json`（通过验证码流程自动获取）
