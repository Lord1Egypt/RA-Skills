---
name: claude-code-unicode-audit
description: 检查本机 Claude Code 二进制是否含有向系统提示词日期行注入近不可见 Unicode 撇号（U+2019/U+02BC/U+02B9）的隐写标记代码，并在受影响时升级到干净版本。受影响区间 v2.1.193–2.1.196，v2.1.197 起已回滚。
metadata:
  version: "1.0.2"
  author: "wuwenbin-bj-st-01"
  license: "MIT"
---

# Claude Code 日期行 Unicode 隐写审计 V1.0.2

> **中文名**：Claude给中国用户的"标记"扫描器
> **版本**：1.0.2 ｜ **作者**：wuwenbin-bj-st-01 ｜ **协议**：MIT

## 触发词

Claude Code 日期行 Unicode / 审计日期行 Unicode / 检查 Claude 日期撇号 / 检查系统提示词 Unicode 异常 / 中国用户标记 / 清理 Claude Code / upgrade claude-code / claude code unicode

## 背景

Claude Code v2.1.193–v2.1.196 在系统提示词 `Today's date is` 中嵌入隐蔽信道：当时区为 `Asia/Shanghai` 或 `Asia/Urumqi`（和/或代理主机名命中 XOR(密钥91) 加密的中转域名清单）时，把撇号替换为近不可见 Unicode 变体（U+2019/U+02BC/U+02B9），并把日期分隔符 `-` 换为 `/`，供服务端静默识别"中国/代理用户"。该行为已在 v2.1.197 回滚。

## 工作流程

1. **审计**：`python3 scripts/audit_cc_date_prompt.py [--json]`
   - 退出码 0 = CLEAN（无隐写），2 = AFFECTED/SUSPECT（受影响或可疑）
2. **判定**：
   - CLEAN → 结束
   - SUSPECT → 建议升级
   - AFFECTED → 需清理
3. **清理**（AFFECTED/SUSPECT 且用户同意）：`python3 scripts/upgrade_cc.py --apply`
   - 执行 `npm install -g @anthropic-ai/claude-code@latest` 并复检
4. **确认**：重新运行步骤 1，返回 CLEAN 则完成

## 检测信号（二进制特征）

详见 `references/known_versions.md`，关键信号：

| 信号 | 描述 |
|---|---|
| `Asia/Shanghai` + `Asia/Urumqi` | 时区判定字节 |
| `Today${...}s date is` | 变量撇号模板（隐写注入点）|
| `Kup=91` / `r^91` | XOR(密钥91) 域名清单解码特征 |
| `endsWith("."+r)` | 代理域名匹配逻辑 |
| 11 个实验室关键词字节 | moonshot/zhipu/deepseek/minimax 等 |
| U+2019/U+02BC/U+02B9 计数 | 标记码点（仅参考，非判定依据）|

## 注意事项

- **升级需用户明确同意**：`--apply` 改动全局 npm 包，必须先确认
- **仅升级能彻底去除**：时区标记独立于代理，改配置无法绕过
- **不要手动 patch 二进制**：脆弱、易破坏、升级即覆盖
