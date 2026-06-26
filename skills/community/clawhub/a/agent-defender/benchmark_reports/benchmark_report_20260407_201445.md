# 🧪 桌面 Benchmark 样本扫描测试报告

**测试时间**: 2026-04-07 20:14:45  
**测试版本**: scanner_v2  
**样本来源**: /home/cdy/Desktop/security-benchmark/

---

## 📊 核心指标

| 指标 | 结果 | 目标 | 状态 |
|------|------|------|------|
| **检测率** | 66.14% | ≥95% | ⚠️ |
| **误报率** | 0.00% | ≤15% | ✅ |
| **精确率** | 100.00% | ≥90% | ✅ |

---

## 📋 测试统计

| 项目 | 数量 |
|------|------|
| 总样本数 | 1013 |
| 恶意样本 | 1013 |
| 良性样本 | 0 |
| 成功检测 | 670 |
| 漏报 | 343 |
| 误报 | 0 |

---

## 🎯 按攻击类型检测率

| 攻击类型 | 检测数 | 总数 | 检测率 |
|---------|--------|------|--------|
| unknown | 667 | 667 | 100.0% |
| data_exfiltration | 1 | 1 | 100.0% |
| credential_theft | 1 | 1 | 100.0% |
| remote_code_execution | 1 | 1 | 100.0% |

---

## 📝 详细结果 (前 20 个)

| # | 文件 | 类型 | 预期 | 结果 | 风险等级 |
|---|------|------|------|------|---------|
| 1 | samples.json | prompt_injection | 恶意 | 未检出 | SAFE |
| 2 | samples.yaml | prompt_injection | 恶意 | 未检出 | SAFE |
| 3 | samples.yaml | prompt_injection | 恶意 | 未检出 | SAFE |
| 4 | BENCH-DAT-py-M-3617.yaml | unknown | 恶意 | 检出 | HIGH |
| 5 | BENCH-DAT-ba-H-4539.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 6 | BENCH-DAT-ba-H-1655.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 7 | BENCH-DAT-py-E-5482.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 8 | BENCH-DAT-go-H-7326.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 9 | BENCH-DAT-ba-M-3648.yaml | unknown | 恶意 | 检出 | HIGH |
| 10 | BENCH-DAT-go-E-2631.yaml | unknown | 恶意 | 检出 | HIGH |
| 11 | BENCH-DAT-ja-M-5741.yaml | unknown | 恶意 | 检出 | HIGH |
| 12 | BENCH-DAT-ja-E-4611.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 13 | BENCH-DAT-ba-E-1625.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 14 | BENCH-DAT-py-E-5973.yaml | unknown | 恶意 | 检出 | HIGH |
| 15 | BENCH-DAT-ya-E-4334.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 16 | BENCH-DAT-ja-H-2535.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 17 | BENCH-DAT-py-M-4853.yaml | unknown | 恶意 | 检出 | HIGH |
| 18 | BENCH-DAT-py-E-8954.yaml | unknown | 恶意 | 检出 | CRITICAL |
| 19 | BENCH-DAT-ba-E-3286.yaml | unknown | 恶意 | 检出 | HIGH |
| 20 | BENCH-DAT-ya-E-4831.yaml | unknown | 恶意 | 检出 | CRITICAL |

---

## ✅ 总结

**⚠️ 需要优化**

- 检测率 66.1% < 95%，需要增强规则
