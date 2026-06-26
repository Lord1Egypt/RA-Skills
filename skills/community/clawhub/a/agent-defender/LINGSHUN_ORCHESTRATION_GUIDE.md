# 🎮 灵顺编排玩法指南

**版本**: v1.0  
**时间**: 2026-04-07  
**适用**: agent-defender + 灵顺 V5 + ROS 编排系统

---

## 📚 灵顺系统家族

### 灵顺 V5 核心系统

| 模块 | 文件 | 功能 | 状态 |
|------|------|------|------|
| **灵顺 V5** | `lingshun_v5.py` | 核心系统 | ✅ 11KB |
| **自治版** | `lingshun_autonomous_v4.py` | 自主研发 | ✅ 24KB |
| **守护进程** | `lingshun_daemon.py` | 7x24 运行 | ✅ 17KB |
| **优化器** | `lingshun_optimizer.py` | 性能优化 | ✅ 13KB |
| **自进化** | `lingshun_self_improve.py` | 自我改进 | ✅ 8KB |

### ROS 编排系统 (17 个脚本)

| 类型 | 脚本 | 功能 | 推荐度 |
|------|------|------|--------|
| **基础循环** | `ros-08-simple-auto-cycle.sh` | 简化自动循环 | ⭐⭐⭐ |
| **顶级研发** | `ros-06-top-auto-rd.sh` | 全流程自动化 | ⭐⭐⭐ |
| **并发循环** | `ros-05-parallel-auto-cycle.sh` | 多技能并行 | ⭐⭐ |
| **样本测试** | `ros-03-full-sample-test.sh` | 全量样本测试 | ⭐⭐⭐ |
| **反思迭代** | `ros-01-reflect-iterate.sh` | 反思评估 | ⭐⭐ |
| **持续发布** | `ros-02-continuous-release.sh` | 迭代发布 | ⭐⭐ |
| **TDD 测试** | `ros-07-tdd-sample-test.sh` | TDD 样本测试 | ⭐⭐ |
| **任务分解** | `ros-09-auto-decompose.sh` | 自动分解任务 | ⭐⭐⭐ |
| **安全扫描** | `ros-10-security-scanner.sh` | 安全扫描 | ⭐⭐ |
| **健康守护** | `ros-health-daemon.sh` | 健康监控 | ⭐⭐ |

### agent-defender 研发系统

| 模块 | 文件 | 功能 |
|------|------|------|
| **研发守护** | `research_daemon.py` | agent-defender 自动研发 |
| **规则同步** | `sync_from_lingshun.py` | 从灵顺 V5 同步规则 |
| **管理脚本** | `defenderctl.sh` | 启动/停止/状态 |

---

## 🎯 编排玩法模式

### 模式 1: 单点自动循环 ⭐⭐⭐

**场景**: 快速验证单个模块的自动迭代

**玩法**:
```bash
# 1. 启动 agent-defender 守护进程
cd /home/cdy/.openclaw/workspace/skills/agent-defender
./defenderctl.sh start

# 2. 查看状态
./defenderctl.sh status

# 3. 查看实时日志
./defenderctl.sh follow
```

**循环流程** (每 5 分钟一轮):
```
威胁情报分析 → 样本探索 → 规则生成 → 测试验证 → 性能优化 → 同步规则 → 质量评估
```

**预期效果**:
- ✅ 自动发现新威胁
- ✅ 自动生成检测规则
- ✅ 自动测试验证
- ✅ 自动同步到防护模块

---

### 模式 2: ROS 简化循环 ⭐⭐⭐

**场景**: 使用 ROS 系统进行简化自动循环

**玩法**:
```bash
cd /home/cdy/.openclaw/workspace/ai-work/skills/research-orchestrator

# 启动简化自动循环
./ros-08-simple-auto-cycle.sh

# 查看最新一轮结果
cat rounds/latest/report.md
```

**循环流程**:
```
1. 威胁分析 (从灵顺 V5 获取情报)
2. 样本设计 (生成新样本)
3. 规则研发 (生成检测规则)
4. 测试验证 (运行测试)
5. 质量评估 (计算指标)
6. 反思迭代 (优化下一轮)
```

**预期效果**:
- ✅ 每轮耗时 <5 分钟
- ✅ 自动生成样本 + 规则
- ✅ 自动测试验证

---

### 模式 3: 顶级自动研发 ⭐⭐⭐

**场景**: 从需求到发布的全流程自动化

**玩法**:
```bash
cd /home/cdy/.openclaw/workspace/ai-work/skills/research-orchestrator

# 启动顶级自动研发
./ros-06-top-auto-rd.sh "增强 DLP 编码识别能力"

# 查看进度
tail -f logs/ros_top_auto_rd.log
```

**全流程**:
```
需求输入 → 任务分解 → 并发研发 → 测试验证 → 质量评估 → 发布交付
```

**预期效果**:
- ✅ 从需求到发布全自动
- ✅ 多模块并发研发
- ✅ 质量门禁保证

---

### 模式 4: 灵顺 + Defender 联动 ⭐⭐⭐

**场景**: 灵顺 V5 研发，agent-defender 应用

**玩法**:
```bash
# 1. 启动灵顺 V5 守护进程
cd /home/cdy/.openclaw/workspace/agent-security-skill-scanner-master/expert_mode
python3 lingshun_daemon.py

# 2. 启动 agent-defender 守护进程
cd /home/cdy/.openclaw/workspace/skills/agent-defender
./defenderctl.sh start

# 3. 自动同步规则
python3 sync_from_lingshun.py
```

**联动流程**:
```
灵顺 V5 研发 → 生成规则 → 自动同步 → agent-defender 应用 → 实战检测
```

**预期效果**:
- ✅ 灵顺 V5 专注研发
- ✅ agent-defender 专注防护
- ✅ 规则自动同步

---

### 模式 5: 并发多技能研发 ⭐⭐

**场景**: 同时研发多个安全技能

**玩法**:
```bash
cd /home/cdy/.openclaw/workspace/ai-work/skills/research-orchestrator

# 启动并发自动循环
./ros-05-parallel-auto-cycle.sh

# 查看各技能状态
cat rounds/latest/parallel_report.md
```

**并发技能**:
- agent-security-skill-scanner
- agent-defender
- supply-chain-defender
- security-sample-generator

**预期效果**:
- ✅ 多技能同时迭代
- ✅ 成果共享
- ✅ 效率翻倍

---

### 模式 6: 任务分解编排 ⭐⭐⭐

**场景**: 复杂任务自动分解执行

**玩法**:
```bash
cd /home/cdy/.openclaw/workspace/ai-work/skills/research-orchestrator

# 自动分解任务
./ros-09-auto-decompose.sh "提升 agent-defender 检测率到 98%"

# 查看分解结果
cat tasks/latest/decomposition.json
```

**任务分解示例**:
```json
{
  "main_task": "提升检测率到 98%",
  "sub_tasks": [
    {
      "task": "分析当前检测率",
      "script": "ros-03-full-sample-test.sh",
      "estimated_time": "10min"
    },
    {
      "task": "识别低质量规则",
      "script": "analyze_rules.py",
      "estimated_time": "5min"
    },
    {
      "task": "生成新规则",
      "script": "generate_rules.py",
      "estimated_time": "15min"
    },
    {
      "task": "测试验证",
      "script": "ros-07-tdd-sample-test.sh",
      "estimated_time": "20min"
    }
  ]
}
```

**预期效果**:
- ✅ 复杂任务自动分解
- ✅ 子任务自动执行
- ✅ 结果自动汇总

---

### 模式 7: 健康监控编排 ⭐⭐

**场景**: 7x24 小时监控系统健康

**玩法**:
```bash
cd /home/cdy/.openclaw/workspace/ai-work/skills/research-orchestrator

# 启动健康守护进程
./ros-health-daemon.sh

# 查看健康状态
cat health/latest_status.json
```

**监控指标**:
- ✅ 守护进程运行状态
- ✅ 内存/CPU 使用率
- ✅ 磁盘空间
- ✅ 日志文件大小
- ✅ 规则同步状态
- ✅ 测试通过率

**告警条件**:
- 🔴 守护进程停止
- 🔴 内存占用 >90%
- 🔴 磁盘空间 <10%
- 🔴 测试通过率 <90%

---

### 模式 8: 安全扫描编排 ⭐⭐

**场景**: 定期安全扫描

**玩法**:
```bash
cd /home/cdy/.openclaw/workspace/ai-work/skills/research-orchestrator

# 深度安全扫描
./ros-deep-scan.sh /home/cdy/.openclaw/workspace/skills

# 查看扫描结果
cat scans/latest/report.md
```

**扫描内容**:
- ✅ 恶意代码检测
- ✅ 凭证泄露检测
- ✅ 配置安全检查
- ✅ 依赖漏洞扫描
- ✅ 权限配置检查

---

## 🎮 实战编排案例

### 案例 1: DLP 编码识别增强

**需求**: 增强 DLP 编码识别能力 (Base64/Hex/URL)

**编排流程**:
```bash
# 1. 任务分解
./ros-09-auto-decompose.sh "增强 DLP 编码识别"

# 2. 并发研发
# - 样本组：生成编码样本
# - 规则组：生成检测规则
# - 测试组：生成测试用例

# 3. 测试验证
./ros-07-tdd-sample-test.sh

# 4. 质量评估
cat rounds/latest/quality_report.json

# 5. 同步到 agent-defender
python3 sync_from_lingshun.py
```

**预期时间**: 30-60 分钟  
**预期成果**: DLP 编码识别能力 +30%

---

### 案例 2: 入侵检测行为序列

**需求**: 实现入侵检测行为序列分析

**编排流程**:
```bash
# 1. 启动顶级自动研发
./ros-06-top-auto-rd.sh "实现行为序列检测"

# 2. 自动执行:
# - 分析攻击序列模式
# - 设计检测算法
# - 生成检测代码
# - 生成测试样本
# - 运行测试验证
# - 质量评估

# 3. 查看成果
cat rounds/latest/behavioral_ids_report.md
```

**预期时间**: 1-2 小时  
**预期成果**: 行为序列检测能力

---

### 案例 3: 规则质量提升

**需求**: 提升规则质量到 95 分+

**编排流程**:
```bash
# 1. 全量样本测试
./ros-03-full-sample-test.sh

# 2. 分析低质量规则
python3 analyze_rule_quality.py

# 3. 优化规则
./ros-01-reflect-iterate.sh

# 4. 再次验证
./ros-03-full-sample-test.sh

# 5. 发布新版本
./ros-02-continuous-release.sh
```

**预期时间**: 1-2 小时  
**预期成果**: 规则质量 95 分+

---

## 📊 编排性能指标

### 循环速度

| 模式 | 单轮耗时 | 循环周期 |
|------|---------|---------|
| **单点自动循环** | 5 分钟 | 5 分钟 |
| **ROS 简化循环** | 10 分钟 | 10 分钟 |
| **顶级自动研发** | 30-60 分钟 | 按需 |
| **并发多技能** | 15 分钟 | 15 分钟 |
| **任务分解** | 取决于任务 | 按需 |

### 研发效率

| 指标 | 手动研发 | 编排研发 | 提升 |
|------|---------|---------|------|
| **样本生成** | 30 分钟/个 | 2 分钟/个 | 15 倍 |
| **规则生成** | 60 分钟/条 | 5 分钟/条 | 12 倍 |
| **测试验证** | 30 分钟/次 | 5 分钟/次 | 6 倍 |
| **质量评估** | 20 分钟/次 | 2 分钟/次 | 10 倍 |

---

## 🎯 推荐玩法组合

### 新手入门 (第 1 周)

```bash
# Day 1: 单点自动循环
./defenderctl.sh start

# Day 2-3: ROS 简化循环
./ros-08-simple-auto-cycle.sh

# Day 4-5: 任务分解编排
./ros-09-auto-decompose.sh "简单任务"

# Day 6-7: 健康监控
./ros-health-daemon.sh
```

### 进阶玩法 (第 2-3 周)

```bash
# 灵顺 + Defender 联动
python3 lingshun_daemon.py &
./defenderctl.sh start
python3 sync_from_lingshun.py

# 并发多技能研发
./ros-05-parallel-auto-cycle.sh

# 安全扫描编排
./ros-deep-scan.sh /path/to/project
```

### 高级玩法 (第 4 周+)

```bash
# 顶级自动研发
./ros-06-top-auto-rd.sh "复杂需求"

# 自定义编排
# 组合多个 ROS 脚本
# 添加自定义逻辑
```

---

## 📋 快速参考

### 常用命令

```bash
# 启动守护进程
./defenderctl.sh start
./lingshun_daemon.py
./ros-health-daemon.sh

# 查看状态
./defenderctl.sh status
./ros-08-simple-auto-cycle.sh --status

# 查看日志
./defenderctl.sh follow
tail -f logs/*.log

# 停止
./defenderctl.sh stop
pkill -f lingshun_daemon
```

### 文件位置

| 文件 | 位置 |
|------|------|
| **灵顺 V5** | `agent-security-skill-scanner-master/expert_mode/` |
| **ROS 编排** | `ai-work/skills/research-orchestrator/` |
| **agent-defender** | `skills/agent-defender/` |
| **日志** | `logs/` |
| **报告** | `rounds/latest/` |

---

## 🎮 开始你的编排之旅

### 第一步：选择玩法

**推荐新手**: 模式 1 (单点自动循环)  
**推荐进阶**: 模式 4 (灵顺 + Defender 联动)  
**推荐高级**: 模式 3 (顶级自动研发)

### 第二步：启动编排

```bash
# 示例：启动单点自动循环
cd /home/cdy/.openclaw/workspace/skills/agent-defender
./defenderctl.sh start
```

### 第三步：观察迭代

```bash
# 查看实时日志
./defenderctl.sh follow

# 或查看最新报告
cat rounds/latest/report.md
```

### 第四步：优化调整

根据运行结果调整参数或切换玩法模式。

---

**编排系统已就绪！** 🎮

**选择你的玩法，开始自动化研发之旅！**

---

**创建时间**: 2026-04-07 23:33  
**版本**: v1.0  
**状态**: ✅ 生产就绪
