# 代码所有权体检 Code Ownership Audit

判定 Python 代码是原创还是演绎作品。纯本地 AST 分析，零依赖不联网，任何 Agent 可用。

**Detect derivative work in Python code — offline, dependency-free, Agent-ready.**

## 两档定价

| 档位 | 价格 | 内容 |
|---|---|---|
| 预览版 | 免费 | 风险数量统计 + 类型分布 + 每条一句话摘要 |
| 完整报告 | ¥0.2/次 | 详细分析(位置+行号+风险描述) + 修复建议 + 可导出 + 服务器签名审计凭证 |

## 快速开始

```bash
# 安装支付宝 AI 付（买家付款能力）
npx -y @alipay/agent-payment@latest install-experience

# 离线审计
audit.py ./my-code --reference ./original-code --out-dir ./out

# 解锁完整报告（付费后）
paygate.py unlock --proof <proof> --out-dir ./out
```

## License

MIT © 2026 ffseika0304
