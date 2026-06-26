# 预订流程

对用户展示、下载须遵循 [output-rules.md](./output-rules.md)（仅使用 `userView` 与顶层 `message`）。  
安装与密钥配置见 [INSTALL.md](../INSTALL.md)、[user-appkey-config.md](./user-appkey-config.md)。

未配置采购密钥时，仅支持演示查价（`POST /ai/shopping`），不支持校验与生单。

## 流程步骤

| 步骤 | 命令 | 用户确认 |
|------|------|----------|
| 1 | `nl_to_search.py parse` → `skill_search_client.py search --selection direct\|transfer` | 选择直飞或中转 |
| 2 | `skill_booking_client.py parse-passengers --text "..."` | 「乘客信息确认无误」 |
| 3 | `skill_booking_client.py verify --passenger-confirmed` | — |
| 3b | 若返回 **304016**（身份不一致） | 须重新执行 **search**（新配置 APPKEY 后必做） |
| 4 | 展示 `userView.orderPreview` | 「确认生单」 |
| 5 | `skill_booking_client.py order --user-confirmed` | — |

## 命令示例（Agent 在 Skill 根目录执行）

```bash
set PYTHONIOENCODING=utf-8

python scripts/nl_to_search.py parse --text "深圳到曼谷 6月2日"
python scripts/skill_search_client.py search --payload-file .cache/pending_search.json --selection direct

python scripts/skill_booking_client.py parse-passengers --text "张三 男 1990-01-15 护照E12345678，2030-12-31到期 国籍CN。联系人：张三 手机13800138000 邮箱 zhangsan@example.com"

python scripts/skill_booking_client.py verify --passenger-confirmed

python scripts/skill_booking_client.py order --user-confirmed
```

本地缓存（勿作为用户下载内容）：

| 文件 | 说明 |
|------|------|
| `.cache/pending_search.json` | 搜索请求体 |
| `.cache/booking_context.json` | 选定报价与校验上下文 |
| `.cache/passengers.json` | 已解析乘客与联系人 |

## 乘客信息示例（对用户说明时可引用）

```
乘客：张三，男，1990-01-15，护照 E12345678，2030-12-31 到期，国籍 CN。
联系人：张三，手机 13800138000，邮箱 zhangsan@example.com
```

`parse-passengers` 成功后，向用户展示 `passengerDisplay` 中的姓名拼音、证件等字段对照，待用户确认后再校验。
