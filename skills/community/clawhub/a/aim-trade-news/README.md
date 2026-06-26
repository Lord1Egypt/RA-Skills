# aim-trade-news

外贸资讯查询 Skill —— 查询最近 1~3 天的外贸相关资讯，返回 AI 生成的标题和摘要。数据源为 AEP Gateway 的 trending_hub 服务。

## 功能

- 查询最近 1/2/3 天的外贸动态、进出口政策、国际贸易资讯
- 返回 AI 改写标题和智能摘要
- 每次调用实时查询，不缓存数据
- 轻量级，只需一个 AEP 凭证即可运行

## 前置条件

### 密钥配置

使用前需要获取 `AEP_AUTHORIZATION` 凭证（Bearer token）：

1. 前往 [https://tools.mentarc.cn/aim-skills/](https://tools.mentarc.cn/aim-skills/) 注册账号
2. 获取你的 `AEP_AUTHORIZATION` token
3. 复制配置模板并填入密钥：

```bash
cp .env.example .env
```

编辑 `.env`，将 token 填入：

```
AEP_AUTHORIZATION=你的token
```

> 脚本会自动补全 `Bearer` 前缀，只需填写 token 值。

### Python 依赖

```bash
pip install -r requirements.txt
```

## 使用方式

### 查询最近 3 天（默认）

```bash
python3 scripts/search_news.py
```

### 查询最近 1 天

```bash
python3 scripts/search_news.py --days 1
```

### 检查凭证配置状态

```bash
python3 scripts/search_news.py --check-config
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--days` | 查询最近几天的资讯，仅支持 1、2、3 | `3` |
| `--check-config` | 检查 AEP 凭证是否已配置 | — |

## 输出示例

```json
{
  "success": true,
  "dataUpdateTime": "2026-04-15 10:30:00",
  "dataSize": 15,
  "items": [
    {
      "aiTitle": "AI改写后的标题",
      "title": "原始标题",
      "publishDate": "2026-04-15",
      "url": "https://example.com/article",
      "summary": "AI生成的摘要内容"
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `success` | `true` = 查询成功，`false` = 失败 |
| `dataUpdateTime` | 数据更新时间 |
| `dataSize` | 资讯条数 |
| `items[].aiTitle` | AI 改写标题（优先使用） |
| `items[].title` | 原始标题 |
| `items[].publishDate` | 发布日期 |
| `items[].url` | 原文链接 |
| `items[].summary` | AI 生成摘要 |
| `message` | 仅失败时存在，错误信息 |

## 文件结构

```
aim-trade-news/
├── .env.example              # 凭证配置模板
├── .env                      # 凭证配置（需自行创建，已 gitignore）
├── SKILL.md                  # Skill 详细文档
├── scripts/
│   └── search_news.py        # 主脚本：凭证检查 + 资讯查询
├── agents/
│   └── search_news.yaml      # Agent 接口定义
├── references/
│   └── aep-setup.md          # AEP 凭证配置指引
├── requirements.txt          # Python 依赖
```

## 注意事项

- 查询范围仅限 1~3 天，不支持自定义时间范围
- 不适用于国内新闻、娱乐资讯、实时行情查询（汇率/股价）
- API 请求超时 30 秒，失败时直接返回错误信息，不自动重试
- 请勿将 `.env` 中的凭证提交到代码仓库
