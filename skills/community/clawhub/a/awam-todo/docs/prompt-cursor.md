# awam-todo 待办管理（Cursor 版完整提示词）

本仓库自带待办技能。凡用户提到「记一下 / 加个待办 / 提醒 / 安排 / 完成 / 删除 /
改期 / 标记状态」等，或给出疑似待办的一句话，必须走本仓库的自动分诊入口，
禁止自行猜测分类、禁止改写原文。

## 1. 分诊（只读）

```
python scripts\todo.py triage --text "<原文>"
```

输出 JSON 契约：`{ok, action: add|update|status|delete|unknown, confidence,
need_confirm, text, target, candidates, status, fields, suggested_tags,
fallback_action}`；退出码 3 = 需要确认。
Windows 下用引号直传中文参数，不要经 echo / 管道转码。

## 2. 执行映射

- **add**:
  ```
  python scripts\todo.py add --text "<原文>"
      [--due "时间"] [--importance 重要|不重要] [--urgent 紧急|不紧急]
      [--tags a;b]
  ```
  仅当 fields 有原文未含的字段时显式补传；重复命中时先问用户新增还是更新。
- **update**:
  ```
  python scripts\todo.py add --update-id <T-ID> --text "<新内容>"
  ```
- **status**: `done` / `start` / `reopen <T-ID>`；改期 `postpone <T-ID> "新时间"`
- **delete**: `python scripts\todo.py delete <T-ID>` —— 必须先经用户确认

## 3. 确认

`need_confirm=true` 或 `action=unknown` 或退出码 3 → 先向用户确认；
candidates 多个 → 列出让用户选；任何删除前必确认；未确认不得写 storage/。

## 4. 约束

storage/、index.json、env.json 不入 Git；CLI 输出英文、回复用户用其语言；
改动后用 `list` / `show` 核对；网页 UI 端口 http://127.0.0.1:8796/。
