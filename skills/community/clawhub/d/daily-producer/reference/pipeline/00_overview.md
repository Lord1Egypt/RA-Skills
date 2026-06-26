# 日报生产流水线总览

## 流程

```
00 【读取历史 feedback】          自动加载前一天 data/feedback/{date}.json，用于加权排序
        ↓
01 build_queries.py              生成搜索查询（关键词 cn/en 分组）
        ↓
02 collect_sources_with_opencli.py  采集候选池（平台 + 网站）
        ↓
03 filter_index.py               时间筛选（保留时间窗口内 + 网站类）
        ↓
04 collect_detail.py             深抓正文（网站类用 web read）
        ↓
05 prepare_payload.py            去噪打分（profile 关键词匹配 + feedback 加权）
        ↓
06 【AI 执行】                    生成日报 JSON（按 profile.yaml 中 daily.target_items 精选 + 写 summary + sidebar）
        ↓
07 validate_payload.py           校验 JSON（不通过则回到 06 修改）
        ↓
08 render_daily.py               渲染 HTML
        ↓
09 send_feishu_card.py           飞书卡片通知（msg_type: interactive，禁止降级为纯文本）
        ↓
10 feedback_server.py            启动反馈服务（后台，同时自动启动 graphify watch）
```

## 一键执行

```bash
DATE=$(date +%Y-%m-%d)

# Step 00: feedback 由 prepare_payload.py 自动读取，无需手动操作

# 步骤 01-05（脚本自动化）
python3 scripts/build_queries.py --date $DATE --window 3
python3 scripts/collect_sources_with_opencli.py --date $DATE --max-keywords 5 --max-results 5
python3 scripts/filter_index.py --date $DATE --window 3
python3 scripts/collect_detail.py --date $DATE
python3 scripts/prepare_payload.py --date $DATE

# 步骤 06（AI 读取 candidates.json，按 profile.yaml 中 daily.target_items 生成日报 JSON）
# → output/daily/$DATE.json

# 步骤 07-08（脚本验证+渲染）
python3 scripts/validate_payload.py output/daily/$DATE.json
python3 scripts/render_daily.py output/daily/$DATE.json --output output/daily/$DATE.html --force

# Step 09: 飞书卡片通知（必须用交互卡片，不得用纯文本）
PUBLIC_URL=$(grep 'public_url' config/profile.yaml | head -1 | awk -F'"' '{print $2}')
python3 scripts/send_feishu_card.py "${PUBLIC_URL}/daily/${DATE}.html"

# Step 10: 启动反馈服务（同时自动启动 graphify watch，如果 profile 中已启用）
nohup python3 scripts/feedback_server.py >> output/server.log 2>&1 &
```

> **注意**：以上命令须在 skill 根目录（含 `SKILL.md` 的目录）下运行，或设置 `DAILY_ROOT` 环境变量指向该目录。

## 产出文件

| 步骤 | 文件 | 说明 |
|------|------|------|
| 01 | `output/raw/{date}_queries.txt` | 搜索查询列表 |
| 02 | `output/raw/{date}_index.txt` | 原始候选池 |
| 03 | `output/raw/{date}_index_filtered.txt` | 时间筛选后 |
| 04 | `output/raw/{date}_detail.txt` | 深抓详情 |
| 05 | `output/raw/{date}_candidates.json` | 去噪打分后的结构化候选 |
| 06 | `output/daily/{date}.json` | 最终日报 JSON |
| 07 | （无文件，校验结果输出到 stdout） | — |
| 08 | `output/daily/{date}.html` | 日报 HTML 页面 |
| 09 | （Feishu API 响应，无本地文件） | 飞书卡片通知 |
| 10 | `output/server.log` | 反馈服务日志 |

## 数据量变化（典型，target_items=20）

```
01  ~90 条查询
02  ~950 条原始候选
03  ~130 条（时间筛选后）
04  ~90 条（平台类直接保留 + 网站类深抓）
05  ~70 条（去噪后）
06  20 条（AI 精选，按 profile.yaml daily.target_items）
```

## 各步骤详细文档

- [01_build_queries.md](01_build_queries.md)
- [02_collect_sources.md](02_collect_sources.md)
- [03_filter_index.md](03_filter_index.md)
- [04_collect_detail.md](04_collect_detail.md)
- [05_prepare_payload.md](05_prepare_payload.md)
- [06_generate_json.md](06_generate_json.md)
- [07_validate_payload.md](07_validate_payload.md)
- [08_render_html.md](08_render_html.md)
- [09_notify_feishu.md](09_notify_feishu.md)
