# 12321 字段映射参考

## 表单字段

| 字段 | ID | name | 类型 | 值说明 |
|------|----|------|------|--------|
| 您的手机号码 | `phone` | phone | text | maxlength=13 |
| 图片验证码 | `w_code` | w_code | text | OCR识别 |
| 短信验证码 | `p_code` | p_code | text | 用户回复 |
| 骚扰来电号码 | `sms_phone` | sms_phone | text | 仅数字/+/-，"未知号码" |
| 来电日期 | `d241` | called_date | text(readonly) | YYYY-MM-DD，JS赋值 |
| 来电时间 | `d242` | called_time | text(readonly) | HH:mm，JS赋值 |
| 通话时长 | `d243` | long_time | select | 见下方 |
| 骚扰形式 | — | type | radio | 见下方 |
| 不良类型 | — | bad_type | radio | 见下方 |
| 来电描述 | `sms_content` | sms_content | textarea | ≥15字，maxlength=1000 |
| 同意条款 | `xuzhi` | xuzhi | checkbox | 默认勾选 |
| 同意防护服务 | `user_intention_flag` | user_intention_flag | checkbox | 默认未勾选 |
| 提交按钮 | `btnSubmit` | — | button | — |

## 通话时长选项 (d243)

| 显示文字 | value |
|---------|-------|
| 未产生通话 | 4 |
| 3分钟以下 | 0 |
| 3到5分钟 | 1 |
| 5到10分钟 | 2 |
| 10分钟以上 | 3 |

## 骚扰形式 (name=type)

| 显示文字 | value |
|---------|-------|
| 响一声挂 | 0 |
| 自动语音骚扰 | 1 |
| 人工骚扰 | 2 |

## 不良类型 (name=bad_type)

| 显示文字 | value |
|---------|-------|
| 淫秽色情 | 1 |
| 虚假票证 | 2 |
| 反动谣言 | 3 |
| 房产中介 | 4 |
| 保险推销 | 5 |
| 教育培训 | 6 |
| 贷款理财 | 7 |
| 猎头招聘 | 8 |
| 欠款催收 | 9 |
| 医疗保健 | 10 |
| 股票证券 | 11 |
| 其他营销 | 12 |
| 旅游推广 | 13 |
| 食药推销 | 14 |
| POS机推销 | 21 |
| 装修建材 | 22 |
| 网络游戏 | 23 |
| App推广 | 24 |
| 出行拉货 | 25 |
| 零售业推销 | 26 |
| 电信业务推广 | 27 |

## 校验错误元素

| 元素ID | 对应字段 |
|--------|---------|
| `sc_xg_1` | 手机号/验证码区域 |
| `sc_xg_2` | 来电时间区域 |
| `sc_ts_1` | 手机号错误提示 |
| `sc_ts_2` | 时间错误提示 |

检查方式：`el.style.display !== 'none'` 且有文本内容则为有错误。

## 关键事件绑定

日期(d241)的 jQuery 事件：
- click[0]: 弹出日历控件
- click[1]: 校验 — `$(this).val().length == 0` 时显示错误

时间(d242)的 jQuery 事件：
- click[0]: 弹出时间控件
- click[1]: 启动 `setInterval("myInterval()", 600)`
- blur: 仅改边框颜色，无校验逻辑

**结论：** JS 直接赋值 + 触发 blur 即可通过校验（d241 校验只检查空值）。
