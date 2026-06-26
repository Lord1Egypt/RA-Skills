---
name: feishu-public-table-monitor
description: 监控公开可访问的飞书 Wiki/文档中指定章节下的价格表或模型表，检测版本日期、模型新增/删除、倍率与价格变化，并输出适合 Telegram/Markdown 的变更通知。适用于用户要求监控公开飞书表格、价格表、模型列表、倍率表、产品清单变动并推送提醒的场景。
---

# Feishu Public Table Monitor

用于监控**公开可访问**的飞书 Wiki/文档页面中的目标价格表或模型表。

## 适用场景

当用户提出这些需求时使用本 skill：
- 监控公开飞书页面中的价格表变化
- 监控模型列表、倍率表、资费表、商品表变化
- 需要把变动内容整理成 Markdown 通知
- 需要为该监控生成可定时执行的脚本或 cron job

## 限制

- 仅适用于**无需登录即可访问**的飞书页面
- 会在指定章节附近优先定位包含“模型名称 / 倍率 / Tokens 价格”等字段的表格，避免误抓说明表
- 支持飞书公开文档大表分页补齐；如果页面结构大改，可能仍需要调整脚本

## 快速用法

脚本路径：
- `scripts/monitor_feishu_price_table.py`

先抓取一次基线：
```bash
python3 scripts/monitor_feishu_price_table.py \
  'https://example.feishu.cn/wiki/XXXX' \
  --section-title '三、模型列表与倍率价格表（所有模型可用）'
```

如果只想看当前解析结果：
```bash
python3 scripts/monitor_feishu_price_table.py \
  'https://example.feishu.cn/wiki/XXXX' \
  --section-title '三、模型列表与倍率价格表（所有模型可用）' \
  --print-snapshot
```

兼容说明：
- 支持旧版 `clientVars: Object({...})` HTML 内嵌数据
- 支持 `Object(JSON.parse("..."))`、`Object(decodeURIComponent("..."))` 等包装格式
- 支持飞书公开文档 `client_vars` 分页接口，能补齐初始 HTML 未预加载的大表单元格
- 如果飞书返回 `Object()` 空壳或关闭公开访问，脚本会给出清楚错误，不再抛误导性的 `JSONDecodeError: Expecting value`

## 常用参数

- `--section-title`：要监控的章节标题
- `--title`：通知标题，文案默认可自定义
- `--state-dir`：状态目录，用于存放基线快照
- `--print-snapshot`：打印当前解析出来的表格快照

## 推荐工作流

1. 先用 `--print-snapshot` 确认表格抓对了
2. 再正常跑一次初始化基线
3. 然后把脚本挂到 cron 定时执行
4. 若输出是 `NO_REPLY` 就表示没变化
5. 若输出是 Markdown 文本，就直接发送给用户

## 与 OpenClaw cron 搭配

如果用户要“有变化就推送给我”：
- 用本脚本生成差异输出
- 在 cron 的 `agentTurn` 里执行脚本
- 规则写成：
  - 输出 `NO_REPLY` 或 `INIT_ONLY` 时只回复 `NO_REPLY`
  - 其他输出原样发送

## 自定义建议

如果用户希望排版更像公告：
- 用 `--title` 自定义标题
- 保持 Markdown 样式输出
- 需要更细分类时，可扩展为涨价、降价、新增、下架四段
