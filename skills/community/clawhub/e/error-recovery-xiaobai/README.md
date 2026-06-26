# Error Recovery - 系统化错误恢复 🩹

> 失败不可怕，可怕的是假装成功

## 问题

AI Agent遇到错误时的常见问题：
- ❌ 静默失败 — 假装成功
- ❌ 无限重试 — 同一错误反复尝试
- ❌ 错误升级 — 用错误方法修复错误

## 解决方案：4R法则

1. **Record** — 记录错误
2. **Reason** — 分析原因
3. **Recover** — 尝试恢复（最多3次）
4. **Report** — 汇报结果

## 快速开始

```bash
git clone https://github.com/aptratcn/skill-error-recovery.git

# 诊断错误
node scripts/error-diagnose.mjs --error "ENOENT"
node scripts/error-diagnose.mjs --error "timeout" --context "git push"
```

## 支持的错误类型

ENOENT, EACCES, EISDIR, 401, 403, 404, 429, 500, timeout, SIGKILL, SIGTERM

## License

MIT

---

**Created by 小白** 🤍
