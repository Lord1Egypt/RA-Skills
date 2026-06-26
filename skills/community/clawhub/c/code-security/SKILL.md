---
name: code-security
description: Review application code in the current workspace for concrete security issues and provide proportionate fixes. Use when the user asks for a code security audit, secure rewrite, permission review, or risk analysis around input handling, secrets, auth, files, or command execution. Do not use for host hardening or infrastructure-wide security posture. Chinese triggers: 安全审查、查漏洞、SQL 注入、XSS、路径穿越、权限问题、敏感信息泄露.
---

# 安全审查

只报真实风险，不制造恐慌。

## 工作流

1. 找出信任边界、用户输入、特权操作和敏感数据路径。
2. 重点检查注入、路径穿越、XSS、不安全反序列化、认证授权缺陷、密钥泄露、不安全日志和命令执行问题。
3. 同时评估可利用性和影响面，不夸大低置信度问题。
4. 用清晰等级标记风险，如 critical、high、medium、low。
5. 给出直接可落地的修复建议，能给代码补丁时优先给补丁。
6. 如果本轮无法彻底关闭风险，就说明残余风险和后续检查点。

## 输出

- 风险点
- 风险等级
- 影响说明
- 修复方案
- 可直接使用的补丁或代码建议
