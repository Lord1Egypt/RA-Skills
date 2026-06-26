# Quickstart

## 场景 1：上传账单并导入

用户上传：

- `owner_alipay_2025-03.csv`

然后说：

```text
帮我导入一下
```

期望行为：

- OpenClaw 识别为记账导入场景
- 如果当前消息上下文已经提供本地 inbound 文件路径，优先直接使用该路径
- 如果没有本地路径、只有附件引用，再通过附件下载链路获取 `download.local_path`
- bookkeeping skill 使用最终解析出的本地路径调用 `bookkeeping import <file> --json`
- 文件类型判断优先依据附件原始文件名或 MIME 信息，而不是只看 inbound 落盘文件名后缀

## 场景 2：上传账单后查重

用户上传：

- `owner_wx_2025-03.xlsx`

然后说：

```text
这个文件导入过没有
```

期望行为：

- bookkeeping skill 识别为检查类意图
- 优先走重复导入检查流程
- 如果当前指代不清，先澄清具体文件

## 场景 3：直接查询历史数据

用户说：

```text
看一下 2025 年 3 月支付宝支出概览
```

期望行为：

- 识别为汇总类意图
- 调用 `bookkeeping summary overview --json`

## 场景 4：多附件场景

用户上传两个账单附件后说：

```text
这些帮我处理一下
```

期望行为：

- 不静默批量导入
- 先列出候选附件
- 询问是全部处理、只处理其中一个，还是先检查重复

## 场景 5：只上传文件，不直接执行写操作

用户只上传一个 `.csv` 文件，没有其他文字。

期望行为：

- 不直接导入
- 优先询问用户是要导入、查重，还是先看摘要

## 场景 6：自然语言记录单笔支出

用户说：

```text
吃午饭微信20
```

期望行为：

- 识别为单笔支出记账
- 从自然语言中推断方向、金额、平台与分类
- 分类必须落在固定分类集合内
- 高置信度下直接调用 `bookkeeping record expense --payload <json> --json`
- 如果返回 `reminders`，把预算提醒一并返回给用户

## 场景 7：自然语言记录单笔收入

用户说：

```text
支付宝到账100
```

期望行为：

- 识别为单笔收入记账
- 分类必须落在固定收入分类集合内
- 低置信度时回退到 `其他收入`
- 调用 `bookkeeping record income --payload <json> --json`

## 场景 8：设置预算并在后续记账时提醒

用户先说：

```text
帮我设置这个月支出预算 1000
```

之后再说：

```text
晚饭微信120
```

期望行为：

- 第一步调用 `bookkeeping budget set ... --json`
- 第二步调用单笔记账命令
- 如果 CLI 返回 `reminders`，优先使用其中的 `channel_text` 作为聊天提醒文案
- 当 `status` 为 `unset` / `warning` / `exceeded` 时，要在回复中明确体现预算状态
- `budget_checks` 用于完整结构化判断，`reminders` 用于直接面向 IM 输出
