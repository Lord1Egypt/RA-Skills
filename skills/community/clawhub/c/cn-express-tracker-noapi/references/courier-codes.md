# 中国快递公司代码参考表

## 主流快递公司

| 代码 | 中文名称 | 常见单号前缀 |
|------|---------|-------------|
| `shunfeng` / `sf` | 顺丰速运 | SF |
| `yuantong` / `yt` | 圆通速递 | YT |
| `zhongtong` / `zto` | 中通快递 | ZTO |
| `shentong` / `sto` | 申通快递 | STO |
| `yunda` / `yundaex` | 韵达快递 | YDA |
| `ems` | EMS | EMS |
| `youzhengguonei` / `post` | 中国邮政 | DPK |
| `jingdong` / `jd` | 京东快递 | JD, JDX, JT |
| `huitongkuaidi` / `htky` | 百世快递 | HT |
| `debangwuliu` / `deppon` | 德邦物流 | DB |

## 其他快递公司

| 代码 | 中文名称 |
|------|---------|
| `ttkd` | 天天快递 |
| `zhaijisong` | 宅急送 |
| `yousu` / `uc` | 优速快递 |
| `suer` / `sure` | 速尔快递 |
| `quanfengkuaidi` / `qfkd` | 全峰快递 |
| `annengwuliu` / `ane` | 安能物流 |
| `baishiwuliu` / `best` | 百世快运 |
| `guotong` | 国通快递 |
| `dhl` | DHL |
| `fedex` / `fedexcn` | FedEx（国际） |
| `ups` | UPS |
| `tnt` | TNT |

## 状态码说明

| 状态码 | 含义 |
|--------|------|
| 0 | 在途 |
| 1 | 已揽收 |
| 2 | 疑难 |
| 3 | 已签收 |
| 4 | 退签 |
| 5 | 派件中 |
| 6 | 退回 |
| 7 | 转单 |
| 10 | 待清关 |
| 11 | 清关中 |
| 12 | 已清关 |
| 13 | 清关异常 |
| 14 | 收件人拒签 |

## 常见问题

### 单号格式
- 顺丰通常以 SF 开头，后跟数字
- 圆通通常以 YT 开头
- 中通通常以 ZTO 开头
- 京东通常以 JD 开头
- 部分快递公司的单号可能全是数字

### 查询限制
- 建议同一单号 30 分钟以上查一次
- 顺丰查询可能需要提供寄件人或收件人手机号后四位
- 新寄出的快递通常在 2-6 小时后才有第一条记录
