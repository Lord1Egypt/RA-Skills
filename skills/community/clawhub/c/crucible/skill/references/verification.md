# Crucible 验证协议

> 融合 ECC verification-loop + Superpowers verification-before-completion。
> 在每个 Gate 前运行，确保 Gate 只审查已通过自动化检查的代码。

---

## Pre-Gate 自动化验证 (6 阶段)

```
Phase 1: Build        → 编译/构建成功
Phase 2: Type Check   → 类型检查无错误
Phase 3: Lint         → 代码风格无警告
Phase 4: Test Suite   → 测试通过 + 覆盖率 ≥ 80%
Phase 5: Security     → 无泄露凭证 (grep sk-, api_key, password, token) + 无调试残留 (grep console.log, debugger)
Phase 6: Diff Review  → 变更范围符合预期
```

### 按项目类型自动检测命令

| 项目类型 | Build | Type Check | Lint | Test |
|----------|-------|-----------|------|------|
| Node.js/TS | `npm run build` | `tsc --noEmit` | `eslint .` | `npm test` |
| Python | `pip install -e .` | `mypy .` | `ruff check .` | `pytest` |
| Go | `go build ./...` | (内含) | `golangci-lint` | `go test ./...` |
| Rust | `cargo build` | (内含) | `cargo clippy` | `cargo test` |
| Java | `mvn compile` | (内含) | (内含) | `mvn test` |

### 验证报告格式

```markdown
# Pre-Gate Verification Report — Stage: {name}

| Phase | Status | Details |
|-------|--------|---------|
| Build | ✅/❌ | {summary} |
| Type Check | ✅/❌ | {error count} |
| Lint | ✅/❌ | {warning count} |
| Test | ✅/❌ | {pass/total}, coverage: {%} |
| Security | ✅/❌ | {findings} |
| Diff | ✅/❌ | {files, lines +/-} |

## Verdict: READY / NOT READY
```

**只有 READY 才进 Gate。** FAIL → 回到 Stage 内部 fix 循环。

---

## Build 失败恢复协议 (from ECC build-fix)

当 Phase 1 FAIL 时启动最小 diff 修复循环：

### 规则
1. 一次修一个错误，按依赖顺序
2. 最小 diff — 不重构、不改架构、不重命名
3. 修完立即重新构建
4. **Stop-and-ask**: 修复引入更多错误 / 同一错误 3 次 / 需要架构变更 / 缺少依赖

### 恢复策略

| 错误类型 | 恢复 |
|----------|------|
| Missing module | `npm install` / `pip install` / 检查路径 |
| Type mismatch | 修正类型，不改接口 |
| Circular dependency | 提取共享类型到独立文件 |
| Version conflict | 对齐版本 |
| Missing env var | 检查 .env，报告缺少哪些 |
