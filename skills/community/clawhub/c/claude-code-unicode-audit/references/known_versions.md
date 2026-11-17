# 已知版本与隐写特征

## 受影响 / 干净版本
| 状态 | 版本 |
|---|---|
| 受影响 | 2.1.193, 2.1.194, 2.1.195, 2.1.196 |
| 干净（回滚后）| >= 2.1.197（latest 已含修复）|

## 隐写机制（v2.1.193–2.1.196 实证）
代码读取系统时区与 `ANTHROPIC_BASE_URL` 主机名：
- 时区命中 `Asia/Shanghai` 或 `Asia/Urumqi` → `cnTZ=true`
- 主机名匹配 XOR(密钥 91) 加密的中转/企业域名清单（100+ 条，含 moonshot.ai、aliyuncs.com、bytedance.net 及大量 api.* / claude-*.top 中转站）
- 主机名含中国 AI 实验室关键词 → `labKw=true`（关键词：deepseek, moonshot, minimax, xaminim, zhipu, bigmodel, baichuan, stepfun, 01ai, dashscope, volces）

拼装系统提示词日期行时做隐写：
- `edp(known, labKw)` 用近不可见 Unicode 撇号编码状态：
  - 两者皆否 → 普通 `'` (U+0027)
  - 命中域名非实验室 → U+2019 （’）
  - 命中实验室非域名 → U+02BC （ʼ）
  - 两者皆中 → U+02B9 （ʹ）
- `cnTZ` 为真时把日期 `-` 替换为 `/`

服务端据此静默识别"中国/代理用户"，终端不可见。

## 检测特征（审计脚本依据）
- 字节/字符串：`Asia/Shanghai`、`Asia/Urumqi`、`Today${...}s date is`
- 解码特征：`fromCharCode(r^91)` / `r^91` / `Kup=91`、`endsWith("."+r)`
- 实验室关键词字节：moonshot / zhipu / deepseek / minimax / dashscope / volces / stepfun / baichuan / 01ai / bigmodel / xaminim
- 码点计数（仅参考，非判定）：U+2019 / U+02BC / U+02B9
