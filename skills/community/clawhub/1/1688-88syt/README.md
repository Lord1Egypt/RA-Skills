# 88syt-skill

88 生意通采购单管理助手 —— 帮你管理 1688 线下交易采购单，支持创建、签署、退款等全流程操作。

## 能做什么

- **账号查询**：查询账号状态，检查是否主账号、已签约、已实名、已绑卡
- **采购单创建**：发起采购单，填写商品信息，邀请对方确认
- **采购单查询**：查看采购单列表、详情、汇总数据
- **签署管理**：签署采购单或拒绝签署
- **确认收货**：买家确认收货，完成交易
- **采购单失效**：将采购单标记为失效
- **退款管理**：申请退款

## 安装

在 Claw 对话框里直接输入下面这段话，让 OpenClaw 帮你自动安装：

```text
请帮我安装这个 skill：git clone https://github.com/next-1688/1688-88syt.git
```

## 使用前准备

1. 登录 [ClawHub](https://clawhub.1688.com/)
2. 点击右上角钥匙按钮，在弹框中点击重新生成，复制你的 AK（Access Key）
3. 对 AI 说："我的AK是 xxx"

配置完成后就可以开始使用 88 生意通功能了。

## 快速上手

直接用自然语言和 AI 对话即可：

- "查一下我的账号状态"
- "帮我创建一个采购单，我是买家，对方是 xxx"
- "查看我的采购单列表"
- "采购单 88SYT20260324419012 的详情"
- "确认收货，单号是 xxx"
- "申请退款，单号是 xxx"

## 命令行（CLI）

本仓库提供统一入口 `cli.py`，需本机已安装 **Python 3**。环境变量 `SYT_API_KEY` 或由命令 `configure` 写入的配置需与 ClawHub 中的 AK 一致。

```bash
python3 cli.py <command> [options]
```

| 命令 | 说明 | 示例 |
|------|------|------|
| `account` | 查询账号状态 | `python3 cli.py account` |
| `contract-list` | 查询采购单列表 | `python3 cli.py contract-list --role BUYER` |
| `contract-detail` | 查询采购单详情 | `python3 cli.py contract-detail --draft-no 88SYT20260324419012` |
| `contract-summary` | 查询采购单汇总 | `python3 cli.py contract-summary` |
| `create-order` | 创建采购单 | `python3 cli.py create-order --role BUYER --counterparty "对方登录名" --items '[...]'` |
| `sign-order` | 签署采购单 | `python3 cli.py sign-order --draft-no 88SYT20260324419012` |
| `sign-reject` | 拒绝签署 | `python3 cli.py sign-reject --draft-no 88SYT20260324419012` |
| `confirm-receipt` | 确认收货 | `python3 cli.py confirm-receipt --draft-no 88SYT20260324419012` |
| `invalidate-order` | 采购单失效 | `python3 cli.py invalidate-order --draft-no 88SYT20260324419012` |
| `refund-apply` | 申请退款 | `python3 cli.py refund-apply --draft-no 88SYT20260324419012` |
| `configure` | 配置 AK | `python3 cli.py configure YOUR_AK` |
| `check` | 检查配置 | `python3 cli.py check` |

所有命令 stdout 为 JSON：`{"success": bool, "markdown": str, "data": {...}}`。人类可读说明一般在 `markdown` 字段。**Agent / Skill 编排约定**见根目录 [`SKILL.md`](./SKILL.md)（含安全规则、异常处理与各能力参考文档路径）。

## 支持功能

| 功能 | 买家 | 卖家 |
|------|------|------|
| 查询账号状态 | ✅ | ✅ |
| 创建采购单 | ✅ | ✅ |
| 查询采购单 | ✅ | ✅ |
| 签署采购单 | ✅ | ✅ |
| 拒绝签署 | ✅ | ✅ |
| 确认收货 | ✅ | - |
| 采购单失效 | ✅ | ✅ |
| 申请退款 | ✅ | - |
| 取消退款 | ✅ | - |

## 业务限制

- **仅支持主账号**：子账号引导至网页端操作
- **仅支持采购单**：合同类交易引导至网页端

## 常见问题

**Q: AK 是什么？怎么获取？**
AK 是你访问 88 生意通的身份凭证。在 [ClawHub](https://clawhub.1688.com/) 中点击右上角钥匙按钮获取。

**Q: 为什么提示"非主账号"？**
88 生意通仅支持主账号操作。请使用 1688 主账号登录，或前往网页端操作。

**Q: 为什么提示"未签约"/"未实名"/"未绑卡"？**
使用 88 生意通前需要完成：签署用户服务协议、实名认证、绑定收款银行卡（卖家）。请前往 [88 生意通页面](https://syt.1688.com/page/SYT/buyer?tracelog=88sytskill) 完成相关操作。

**Q: 支持支付吗？**
当前技能暂不支持支付，如有需要请前往 88 生意通网页端操作。

**Q: 电子合同/采购单有法律效力吗？**
经过买卖双方确认的采购单及电子合同，具有与纸质合同同等的法律效力。

## 反馈与支持

使用中遇到问题，可以联系 88 生意通技术支持。

---

**免责声明**：以上信息根据当前查询结果整理，具体以 88 生意通页面及银行/平台实际处理为准。若与您页面不一致，请以页面展示为准。
