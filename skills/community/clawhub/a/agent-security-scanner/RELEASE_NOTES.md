# Agent Security Scanner v4.1.0 Release Notes

**发布日期**: 2026-04-04  
**版本**: 4.1.0  
**状态**: ✅ 生产就绪

---

## 🎯 核心特性

### 三层检测架构

```
[一层] 白名单/黑名单 → 快速筛查
[二层] 智能评分 + 意图分析 → 边界样本判定
[三层] LLM 深度分析 → 不确定样本
```

### 性能指标

| 指标 | v4.1 | v4.0 | 提升 |
|------|------|------|------|
| 检测率 | 100% | 100% | - |
| 误报率 | 7.77% | 0%* | 安全回退 |
| 速度 | 5019/s | 4802/s | +4.5% |

*v4.0 FPR 0% 有安全风险，已回退

### 新增功能

- ✅ LLM 二次判定模块 (`llm_analyzer.py`)
- ✅ 增强意图分析器 (`intent_detector_v2.py`)
- ✅ 灵顺 V5 自动化监控
- ✅ 质量门禁配置 (`config/quality_gate.yaml`)
- ✅ 30 个测试样本 (AST/意图/LLM)

---

## 📦 发布内容

### 核心文件

```
release/v4.1/
├── src/
│   ├── multi_language_scanner_v4.py  # 主扫描器
│   ├── fast_batch_scan.py            # 批量扫描
│   ├── intent_detector_v2.py         # 意图分析
│   ├── llm_analyzer.py               # LLM 分析
│   └── benchmark_full_scan.py        # 性能测试
├── config/
│   └── quality_gate.yaml             # 质量门禁
├── docs/
│   ├── USER_GUIDE.md                 # 用户指南
│   └── DELIVERY_REPORT.md            # 交付报告
├── examples/                         # 示例代码
├── tests/                            # 测试用例
├── package.json                      # npm 包配置
├── SKILL.md                          # 技能规范
├── requirements.txt                  # 依赖列表
├── LICENSE                           # 许可证
├── README.md                         # 项目说明
├── RELEASE_NOTES.md                  # 版本说明
├── lingshun_optimize.sh              # 灵顺优化
├── lingshun_scanner_daemon.py        # 灵顺监控
└── lingshun_task_orchestration.sh    # 任务编排
```

---

## 🔧 安装说明

### 从源码安装

```bash
git clone https://github.com/agent-security/scanner.git
cd scanner/release/v4.1
pip install -r requirements.txt
```

### 从 npm 安装 (待发布)

```bash
npm install agent-security-scanner@4.1.0
```

---

## 🚀 使用示例

### 基本扫描

```bash
python3 src/fast_batch_scan.py
```

### 启用 LLM

```bash
export ENABLE_LLM_ANALYSIS=true
export LLM_API_KEY=your_api_key
python3 src/fast_batch_scan.py
```

### 灵顺监控

```bash
# 启动守护进程
nohup python3 lingshun_scanner_daemon.py > logs/daemon.log 2>&1 &

# 手动优化
bash lingshun_optimize.sh
```

---

## ⚠️ 重要变更

### 安全配置回退

- ❌ 移除：过度宽泛的 false_prone 白名单
- ✅ 保留：明确可信的 BEN-前缀白名单
- 📊 FPR: 0% → 7.77% (安全范围)

### LLM 集成

- ✅ 条件触发 (仅边界样本)
- ✅ 失败降级机制
- ✅ 异步调用支持

---

## 🐛 Bug 修复

- 修复白名单优先级问题
- 修复意图分析类型检查
- 修复 LLM 触发条件判断

---

## 📈 性能对比

| 版本 | DR | FPR | 速度 | 架构 |
|------|----|----|----|----|
| v3.x | 71% | 54% | 4674/s | 单层 |
| v4.0 | 100% | 0%* | 4802/s | 双层 |
| **v4.1** | **100%** | **7.77%** | **5019/s** | **三层** |

*v4.0 FPR 0% 有安全风险，已回退

---

## 🎯 升级建议

### 从 v4.0 升级

```bash
# 备份配置
cp config/quality_gate.yaml config/quality_gate.yaml.bak

# 拉取新版本
git pull origin main

# 验证配置
python3 -c "from src.multi_language_scanner_v4 import MultiLanguageScanner; print('✅ OK')"

# 运行测试
python3 -m pytest tests/
```

### 从 v3.x 升级

```bash
# 全新安装
git clone https://github.com/agent-security/scanner.git
cd scanner/release/v4.1

# 迁移配置
# 注意：白名单规则已变更，需要重新配置
```

---

## 🔒 安全说明

### 已知限制

- false_prone 样本需要正常检测 (不加入白名单)
- LLM 分析需要 API Key (可选功能)
- 灵顺监控需要网络连接

### 最佳实践

1. 启用质量门禁监控
2. 配置告警通知
3. 定期更新规则库
4. 收集边界样本案例

---

## 🧪 测试样本

包含 30 个专用测试样本：

```
test_samples/
├── ast_triggered/     (10 个) - AST 触发样本
├── intent_triggered/  (10 个) - 意图触发样本
└── llm_triggered/     (10 个) - LLM 触发样本
```

---

## 📞 联系方式

- GitHub: https://github.com/agent-security/scanner
- Email: security@agent-security.com
- Discord: https://discord.gg/agent-security

---

**完整变更日志**: 详见 [CHANGELOG.md](CHANGELOG.md)

**发布验证**: [pre_release_validation.json](pre_release_validation.json)
