---
name: fofa-search-use
description: 用于调用 FOFA OpenAPI 进行批量检索并导出 CSV/JSON。用户提到 FOFA、资产测绘、批量查询、自动翻页、导出 CSV、key+查询语句等需求时优先加载本 skill。
---

# FOFA Search Use

## First

- 目标是让用户只提供 `key` 和 `query` 就能检索并导出数据。
- 脚本自动选择翻页策略：
  1) 优先 `search/next`
  2) 不支持时回退 `search/all?page`
- 默认导出 `CSV`，可选导出 `JSON`。
- 本 skill 不依赖固定机器路径，整个文件夹可直接复制到任意项目使用。

## 入口脚本

- 主脚本：`scripts/fofa_search_cli.py`
- 运行方式：
  - AI 无交互推荐：
    - `python3 scripts/fofa_search_cli.py --no-interactive --key "$FOFA_KEY" --query 'title="test"' --output-file results.csv --json-output`
  - 兼容交互：
    - `python3 scripts/fofa_search_cli.py`

## 环境与安装（可移植）

- 推荐虚拟环境：
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`（Windows PowerShell: `.venv\Scripts\Activate.ps1`）
  - `pip install -r scripts/requirements.txt`
- 最小依赖文件：`scripts/requirements.txt`

## 参数说明

- `--key`：FOFA API key
- `--query`：FOFA 查询语句
- `--fields`：返回字段，默认 `host,ip,port,protocol,title`
- `--max-records`：最大导出条数，默认 `1000`
- `--page-size`：每页请求数量，默认 `10000`（最大 `10000`）
- `--output-file`：CSV 文件名，默认 `fofa_results.csv`
- `--json-output`：额外导出 JSON
- `--base-url`：FOFA 地址，默认 `https://fofa.info`
- `--no-interactive`：禁止交互输入，缺参直接报错

## 推荐执行策略

- 先用小样本测试语句（如 `--max-records 10`）。
- 字段尽量精简，减少无效数据和消耗。
- 大批量导出时优先使用无交互参数模式，便于自动化和复现。

## CSV 导出帮助

- 自定义导出字段：使用 `--fields`，字段顺序即 CSV 列顺序。
- 常用字段示例：`host,ip,port,protocol,title,country,city,server`
- 无交互导出示例：
  - `python3 scripts/fofa_search_cli.py --no-interactive --key "$FOFA_KEY" --query 'title="test"' --fields "ip,port,host,title,country,city" --max-records 500 --page-size 100 --output-file fofa_custom.csv`
- 交互导出要点：
  - 运行脚本后在 `fields` 提示中输入逗号分隔字段。
  - 如果某列为空，CSV 中对应单元格会保留空值，这是正常现象。
- Excel 打开乱码处理：
  - 脚本默认用 `utf-8-sig` 写出 CSV，通常可直接被 Excel 正确识别。
  - 若仍异常，导入时手动选择 `UTF-8` 编码。

## 安全注意事项

- 不要把真实 `key` 写入仓库文件或提交历史。
- 推荐通过环境变量注入：`FOFA_KEY`。
- 必须持久化时使用本地安全存储，不要明文保存在代码库。
