# HTML 邮件模板 HTML Email Templates

专业邮件 HTML 模板，支持中英文场景。使用时将占位符 `{变量名}` 替换为实际内容。

---

## 1. 商务报告模板 Business Report

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="background:linear-gradient(135deg,#1a5276,#2e86c1);padding:30px 40px;color:#ffffff;">
<h1 style="margin:0;font-size:22px;">{report_title}</h1>
<p style="margin:8px 0 0;font-size:14px;opacity:0.9;">{report_period} | {report_date}</p>
</td></tr>
<tr><td style="padding:30px 40px;">
<p style="margin:0 0 20px;font-size:15px;color:#333;">{greeting}，</p>
<p style="margin:0 0 20px;font-size:14px;color:#555;line-height:1.8;">{summary}</p>
<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;margin:20px 0;">
<thead><tr style="background:#eaf2f8;">
<th style="padding:12px 16px;text-align:left;font-size:13px;color:#1a5276;border-bottom:2px solid #2e86c1;">{col1_header}</th>
<th style="padding:12px 16px;text-align:right;font-size:13px;color:#1a5276;border-bottom:2px solid #2e86c1;">{col2_header}</th>
<th style="padding:12px 16px;text-align:right;font-size:13px;color:#1a5276;border-bottom:2px solid #2e86c1;">{col3_header}</th>
<th style="padding:12px 16px;text-align:right;font-size:13px;color:#1a5276;border-bottom:2px solid #2e86c1;">{col4_header}</th>
</tr></thead>
<tbody>
{table_rows}
</tbody>
</table>
<p style="margin:20px 0 0;font-size:14px;color:#555;line-height:1.8;">{detail_text}</p>
</td></tr>
<tr><td style="background:#f9f9f9;padding:20px 40px;border-top:1px solid #eee;font-size:12px;color:#999;text-align:center;">
{sender_name} | {sender_department}<br>
此邮件由 emailbox 自动发送
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
```

**表格行模板：**
```html
<tr style="border-bottom:1px solid #eee;">
<td style="padding:10px 16px;font-size:14px;color:#333;">{col1_value}</td>
<td style="padding:10px 16px;text-align:right;font-size:14px;color:#555;">{col2_value}</td>
<td style="padding:10px 16px;text-align:right;font-size:14px;color:#555;">{col3_value}</td>
<td style="padding:10px 16px;text-align:right;font-size:14px;font-weight:bold;color:{positive_color};">{col4_value}</td>
</tr>
```

---

## 2. 会议邀请模板 Meeting Invitation

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="background:linear-gradient(135deg,#6c3483,#a569bd);padding:35px 40px;color:#ffffff;text-align:center;">
<h1 style="margin:0;font-size:24px;">{event_title}</h1>
<p style="margin:10px 0 0;font-size:16px;opacity:0.9;">诚挚邀请您参加</p>
</td></tr>
<tr><td style="padding:30px 40px;">
<table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 25px;">
<tr><td style="padding:8px 0;font-size:14px;color:#888;width:80px;">🕐 时间</td><td style="padding:8px 0;font-size:15px;color:#333;font-weight:bold;">{event_time}</td></tr>
<tr><td style="padding:8px 0;font-size:14px;color:#888;">📍 地点</td><td style="padding:8px 0;font-size:15px;color:#333;font-weight:bold;">{event_location}</td></tr>
<tr><td style="padding:8px 0;font-size:14px;color:#888;">👤 主持人</td><td style="padding:8px 0;font-size:15px;color:#333;font-weight:bold;">{event_host}</td></tr>
<tr><td style="padding:8px 0;font-size:14px;color:#888;">📋 会议号</td><td style="padding:8px 0;font-size:15px;color:#333;font-weight:bold;">{meeting_id}</td></tr>
</table>
<p style="margin:0 0 5px;font-size:14px;color:#333;font-weight:bold;">会议议程：</p>
<ol style="margin:5px 0 20px;padding-left:20px;font-size:14px;color:#555;line-height:2;">
{agenda_items}
</ol>
<p style="margin:0 0 5px;font-size:14px;color:#333;font-weight:bold;">参会要求：</p>
<ul style="margin:5px 0 20px;padding-left:20px;font-size:13px;color:#666;line-height:1.8;">
{requirements}
</ul>
<table width="100%" cellpadding="0" cellspacing="0"><tr>
<td align="center" style="padding:10px;"><a href="{accept_url}" style="display:inline-block;padding:12px 30px;background:#27ae60;color:#ffffff;text-decoration:none;border-radius:5px;font-size:14px;font-weight:bold;">✅ 接受邀请</a></td>
<td align="center" style="padding:10px;"><a href="{decline_url}" style="display:inline-block;padding:12px 30px;background:#e74c3c;color:#ffffff;text-decoration:none;border-radius:5px;font-size:14px;font-weight:bold;">❌ 无法参加</a></td>
</tr></table>
</td></tr>
<tr><td style="background:#f9f9f9;padding:15px 40px;font-size:12px;color:#999;text-align:center;">
{sender_name} | 联系方式：{contact_info}
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
```

---

## 3. 通知公告模板 Notification / Announcement

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="background:#c0392b;padding:6px 40px;text-align:center;">
<span style="color:#ffffff;font-size:12px;font-weight:bold;letter-spacing:2px;">🔴 重要通知 IMPORTANT NOTICE</span>
</td></tr>
<tr><td style="padding:30px 40px;">
<h2 style="margin:0 0 5px;font-size:20px;color:#c0392b;">{notice_title}</h2>
<p style="margin:0 0 20px;font-size:13px;color:#999;">发布时间：{notice_date} | 发布人：{notice_author}</p>
<div style="padding:20px;background:#fdf2f2;border-left:4px solid #c0392b;margin:0 0 20px;font-size:14px;color:#333;line-height:1.8;">
{notice_summary}
</div>
<p style="margin:0 0 20px;font-size:14px;color:#333;line-height:1.8;">{notice_detail}</p>
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f8f9fa;border-radius:6px;margin:0 0 20px;">
<tr><td style="padding:15px 20px;font-size:13px;color:#555;line-height:1.8;">
<strong>⚠️ 注意事项：</strong><br>
{notice_action_items}
</td></tr>
</table>
<p style="margin:0;font-size:14px;color:#555;">如有疑问，请联系：{contact_info}</p>
</td></tr>
<tr><td style="background:#f9f9f9;padding:15px 40px;font-size:12px;color:#999;text-align:center;">
{sender_department} | 此邮件由 emailbox 自动发送
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
```

---

## 4. 感谢信模板 Thank You Letter

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="background:linear-gradient(135deg,#f39c12,#e67e22);padding:35px 40px;color:#ffffff;text-align:center;">
<h1 style="margin:0;font-size:28px;">🙏 感谢您</h1>
<p style="margin:10px 0 0;font-size:16px;opacity:0.9;">Thank You</p>
</td></tr>
<tr><td style="padding:30px 40px;">
<p style="margin:0 0 20px;font-size:15px;color:#333;">亲爱的 {recipient_name}，</p>
<p style="margin:0 0 20px;font-size:14px;color:#555;line-height:1.8;">{thank_message}</p>
<table width="100%" cellpadding="0" cellspacing="0" style="background:#fef9e7;border-radius:6px;margin:0 0 20px;">
<tr><td style="padding:15px 20px;font-size:14px;color:#7d6608;text-align:center;font-style:italic;line-height:1.6;">
"{quote_text}"
</td></tr>
</table>
<p style="margin:0 0 10px;font-size:14px;color:#555;line-height:1.8;">{additional_message}</p>
<p style="margin:20px 0 0;font-size:15px;color:#333;">此致<br>敬礼</p>
<p style="margin:5px 0 0;font-size:14px;color:#666;">{sender_name}<br>{sender_title}</p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
```

---

## 5. 周报/日报模板 Weekly/Daily Report

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="background:linear-gradient(135deg,#1abc9c,#16a085);padding:25px 40px;color:#ffffff;">
<h1 style="margin:0;font-size:20px;">📋 {report_type}周报</h1>
<p style="margin:5px 0 0;font-size:13px;opacity:0.9;">{reporter_name} | {report_period}</p>
</td></tr>
<tr><td style="padding:25px 40px;">
<h3 style="margin:0 0 15px;font-size:16px;color:#1abc9c;">✅ 本周完成</h3>
<ul style="margin:0 0 20px;padding-left:20px;font-size:14px;color:#333;line-height:2;">
{completed_items}
</ul>
<h3 style="margin:0 0 15px;font-size:16px;color:#e67e22;">🔄 进行中</h3>
<ul style="margin:0 0 20px;padding-left:20px;font-size:14px;color:#333;line-height:2;">
{in_progress_items}
</ul>
<h3 style="margin:0 0 15px;font-size:16px;color:#3498db;">📋 下周计划</h3>
<ul style="margin:0 0 20px;padding-left:20px;font-size:14px;color:#333;line-height:2;">
{next_week_items}
</ul>
<table width="100%" cellpadding="0" cellspacing="0" style="background:#fef9e7;border-radius:6px;margin:0 0 20px;">
<tr><td style="padding:15px 20px;font-size:14px;color:#7d6608;">
<strong>⚠️ 需协调事项：</strong>{blocker_items}
</td></tr>
</table>
</td></tr>
<tr><td style="background:#f9f9f9;padding:15px 40px;font-size:12px;color:#999;text-align:center;">
{sender_name} | {department} | {date}
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
```

---

## 6. 发票/单据通知模板 Invoice Notification

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="background:linear-gradient(135deg,#2c3e50,#34495e);padding:25px 40px;color:#ffffff;">
<h1 style="margin:0;font-size:20px;">📄 {document_type}通知</h1>
<p style="margin:5px 0 0;font-size:13px;opacity:0.9;">单据编号：{document_id}</p>
</td></tr>
<tr><td style="padding:25px 40px;">
<p style="margin:0 0 20px;font-size:15px;color:#333;">{greeting}，</p>
<p style="margin:0 0 20px;font-size:14px;color:#555;line-height:1.8;">{document_description}</p>
<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;margin:0 0 20px;">
<tr style="background:#2c3e50;"><td style="padding:10px 16px;color:#ffffff;font-size:13px;font-weight:bold;">项目</td><td style="padding:10px 16px;color:#ffffff;font-size:13px;font-weight:bold;text-align:right;">详情</td></tr>
{document_rows}
<tr style="background:#eaf2f8;border-top:2px solid #2c3e50;"><td style="padding:10px 16px;font-size:14px;font-weight:bold;color:#2c3e50;">合计</td><td style="padding:10px 16px;font-size:14px;font-weight:bold;color:#2c3e50;text-align:right;">{total_amount}</td></tr>
</table>
<p style="margin:0 0 10px;font-size:13px;color:#999;">📎 附件：{attachment_info}</p>
<p style="margin:0 0 10px;font-size:13px;color:#999;">⏰ 截止日期：{deadline}</p>
<p style="margin:10px 0 0;font-size:14px;color:#555;">如有疑问，请联系 {contact_person}（{contact_info}）</p>
</td></tr>
<tr><td style="background:#f9f9f9;padding:15px 40px;font-size:12px;color:#999;text-align:center;">
{sender_department} | 此邮件由 emailbox 自动发送
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
```

---

## 7. 正式信函模板 Formal Letter

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="padding:40px;">
<p style="margin:0 0 5px;font-size:14px;color:#666;">{sender_address}</p>
<p style="margin:0 0 20px;font-size:13px;color:#999;">{send_date}</p>
<p style="margin:0 0 5px;font-size:15px;color:#333;">{recipient_title} {recipient_name}</p>
<p style="margin:0 0 20px;font-size:14px;color:#666;">{recipient_address}</p>
<p style="margin:0 0 20px;font-size:15px;color:#333;">{subject_line}</p>
<p style="margin:0 0 20px;font-size:15px;color:#333;">{salutation}，</p>
<div style="font-size:14px;color:#333;line-height:2;">{letter_body}</div>
<p style="margin:30px 0 5px;font-size:15px;color:#333;">此致<br>敬礼</p>
<p style="margin:20px 0 0;font-size:14px;color:#333;">{sender_name}</p>
<p style="margin:0;font-size:13px;color:#666;">{sender_title}</p>
<p style="margin:0;font-size:13px;color:#666;">{sender_organization}</p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
```

---

## 使用说明

1. 选择合适的模板
2. 将 `{变量名}` 替换为实际内容
3. 将替换后的 HTML 保存为文件，例如 `${OPENCLAW_WORKSPACE}/.emailbox_body.html`
4. 使用 `--html-file` 参数发送：

```bash
python3 scripts/send_mail.py \
  --to recipient@example.com \
  --subject "周报 - 张三 - 2026年第16周" \
  --html-file "${OPENCLAW_WORKSPACE}/.emailbox_body.html" \
  --provider qq
```