---
name: court-notice
description: 法院文书自动处理技能。当用户收到、转发法院短信，或要求处理/解析法院文书PDF时触发。自动完成：下载PDF→提取信息→判断文书类型→创建日历（传票/出庭通知）→设置提前1天提醒→生成概要报告→PDF存桌面。全程零弹窗、零手动操作。
---

# 法院文书自动处理

## 工作流程

收到法院短信后，按以下步骤处理：

```
1. 解析链接 → 下载PDF到桌面
2. pypdf提取文本内容
3. 判断文书类型（传票/出庭通知→建日历，其他→仅汇报）
4. AppleScript直接写入"工作"日历（无弹窗）
5. launchd plist设置提前1天系统通知提醒
6. 生成文书概要报告
7. PDF存桌面回传用户
```

## 判断规则

| 文书类型 | 关键词 | 处理 |
|----------|--------|------|
| 传票/出庭通知 | 开庭审理、开庭时间、传唤 | ✅ 建日历 |
| 撤诉裁定 | 撤诉、裁定准予 | 📋 仅汇报 |
| 应诉通知书 | 应诉、答辩 | ✅ 建日历 |
| 其他 | - | 📋 仅汇报 |

## 关键信息提取

从PDF提取：
- `案号`：正则匹配 `（\d{4}）.+\d+号`
- `案由`：案由行
- `被传唤人`：被传唤人行
- `开庭时间`：年月日+时间
- `地点`：法庭/地点行

## 执行脚本

### 1. PDF解析
```bash
python3 skills/court-notice/scripts/parse_court_pdf.py <pdf路径>
```

### 2. 创建日历
```bash
python3 skills/court-notice/scripts/create_court_calendar.py <案号> <案由> <YYYY-MM-DD HH:MM> <地点> [日历名称] [PDF链接]
```

时间格式：`YYYY-MM-DD HH:MM`（如 `2026-04-24 10:00`）

launchd plist存至 `~/Library/LaunchAgents/com.mm.court-{案号hash}.plist`

### 3. 下载PDF到桌面
```bash
curl -s -o ~/Desktop/recv_court_notice.pdf "<链接>"
```

## 日历事件内容

| 字段 | 内容 |
|------|------|
| summary | ⚖️ 开庭：{案由} |
| description | 案号 - 案由 - 开庭地点（纯文本，不含链接） |
| url | PDF链接（从短信链接传入） |
| location | 开庭地点 |
| start/end | 开庭时间（2小时时长） |

**注意**：description不含URL，保持纯净；URL通过AppleScript的url属性传入日历事件，点开事件可直接访问PDF。

## 标准短信模板

收到法院短信时，自动按以下格式处理：
```
【{法院名称}】{法院名称}向您发送了{案号}案件及相关文书，请及时签收。点击链接查阅：{链接}
```

## 输出格式

处理完成后输出：

```
📋 文书概要

类型：{传票/裁定书/...}
案号：{案号}
案由：{案由}
当事人：{被传唤人/原告/被告}
开庭时间：{时间}
地点：{地点}

✅ 完成清单
- 📄 PDF → 桌面
- 📅 日历 → 已创建（"工作"分组，含PDF链接）
- ⏰ 提醒 → 提前1天
```

## 参考资料

- 文书类型判断规则：[references/document_types.md](references/document_types.md)
- 标准短信模板：[references/sms_template.txt](references/sms_template.txt)

## 更新记录

- 2026-04-08：新增PDF链接支持（url字段），description不再放链接
