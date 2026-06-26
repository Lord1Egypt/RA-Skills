# feishu-bitable-sync

`feishu-bitable-sync` 是飞书同步 skill。它读取 `wechat-report` 的结果，把文章逐条写入飞书多维表，并按 `source_url` 去重。

## 这个 skill 能做什么

- 读取本地 `wechat-report.md` 或 raw JSON
- 一篇文章一行同步到飞书多维表
- 按 `source_url` 去重更新，而不是重复新增
- 优先使用用户授权 token
- 直写失败时导出 CSV 作为手工导入兜底

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 必需环境变量

```bash
export FEISHU_APP_ID=...
export FEISHU_APP_SECRET=...
export FEISHU_BITABLE_APP_TOKEN=...
export FEISHU_BITABLE_TABLE_ID=...
```

### 推荐先完成用户授权

先运行一次 `feishu-user-auth`，再同步：

```bash
.venv/bin/python -m skill_runtime.cli run-skill feishu-user-auth \
  --input content-production/inbox/20260407-harness-engineering-wechat-report.md
```

## 输入和输出

**输入**

- `content-production/inbox/YYYYMMDD-<slug>-wechat-report.md`
- 或 `content-production/inbox/raw/wechat-report/YYYY-MM-DD/<slug>.json`

**输出**

- `content-production/published/YYYYMMDD-<slug>-feishu-sync.md`
- 若直写失败：`content-production/published/YYYYMMDD-<slug>-feishu-import.csv`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill feishu-bitable-sync \
  --input content-production/inbox/20260407-harness-engineering-wechat-report.md
```

## 什么时候用

- 你已经看过 `wechat-report` 本地结果，并确认要发飞书
- 你想把公众号对比结果沉淀为可检索的多维表资产
- 你想保留一份 CSV 兜底文件，避免同步失败后没有后手

## 注意事项

- 本 skill 不应默认自动触发，应该放在“用户确认后”执行
- 默认 `FEISHU_SYNC_AUTH_MODE=user`
- 若没有用户授权缓存，会生成 `auth_required` 回执并提示先跑 `feishu-user-auth`

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [feishu-schema.md](../../docs/feishu-schema.md)
