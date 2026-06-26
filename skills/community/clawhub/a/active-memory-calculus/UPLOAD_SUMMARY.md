# Active Memory for Calculus Teaching - 上传摘要

## 基本信息

| 属性 | 值 |
|------|-----|
| **Skill ID** | active-memory-calculus |
| **显示名称** | Active Memory for Calculus Teaching |
| **版本** | 1.0.0 |
| **作者** | daigxok |
| **分类** | Education / Mathematics |
| **许可证** | MIT |
| **OpenClaw 版本要求** | >= 2026.4.10 |

## 核心功能

1. **Active Memory 主动记忆**
   - 零触发自动记忆学生偏好
   - 实时追踪概念掌握度
   - 识别并预警错误模式

2. **梦境系统 (Dreaming System)**
   - 每20分钟自动整理学习摘要
   - 构建知识图谱，发现学习断层
   - 生成个性化学习建议

3. **高等数学专项优化**
   - 覆盖12个核心章节，60+概念
   - 识别12种典型错误模式
   - 自适应学习路径推荐

## 文件清单

### 核心文件
- `SKILL.md` - Skill 描述文档 (10,290 bytes)
- `hermes.config.yaml` - OpenClaw 配置 (4,677 bytes)
- `_meta.json` - 注册表元数据 (1,528 bytes)
- `README.md` - 项目说明 (6,907 bytes)

### 工具脚本 (Python)
- `tools/memory_extract.py` - 记忆提取 (6,978 bytes)
- `tools/memory_apply.py` - 记忆应用 (7,578 bytes)
- `tools/dream_generator.py` - 梦境生成 (14,119 bytes)
- `tools/knowledge_graph.py` - 知识图谱 (8,669 bytes)

### 提示词
- `prompts/system.md` - 系统提示词 (6,380 bytes)

### 示例文档
- `examples/example_basic_usage.md` - 基础使用示例 (2,812 bytes)
- `examples/example_integration.md` - Skill 集成示例 (3,195 bytes)
- `examples/example_dream_output.md` - 梦境输出示例 (2,911 bytes)

### 其他
- `QUICKSTART.md` - 快速开始指南
- `PUBLISH.md` - 发布指南
- `publish.sh` - 一键发布脚本
- `package.json` - Node.js 配置
- `requirements.txt` - Python 依赖
- `LICENSE` - MIT 许可证
- `.gitignore` - Git 忽略配置

## 依赖 Skills

- `calculus-concept-visualizer` - 概念可视化
- `derivation-animator` - 推导动画
- `error-analyzer` - 错题分析

## 集成 Skills

- `exam-problem-generator` - 智能出题（接收难度调整）
- `resource-harvester` - 资源采集（接收偏好数据）
- `personal-learning` - 个人学习（接收学习路径）

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CALCULUS_MEMORY_PATH` | `~/obsidian/calculus-memory` | 记忆数据存储路径 |
| `DREAM_INTERVAL` | `20m` | 梦境系统心跳间隔 |
| `active_memory.mode` | `recent` | 记忆模式 (message/recent/full) |
| `dreaming.enabled` | `true` | 是否启用梦境系统 |

## 性能指标

| 指标 | 数值 |
|------|------|
| 记忆提取延迟 | < 200ms |
| 梦境生成时间 | 5-10s/次 |
| 知识图谱更新 | < 1s |
| 预期记忆准确率 | 85%+ |
| 预期学生满意度提升 | 35%+ |

## 发布命令

```bash
# 方式1: 使用发布脚本
./publish.sh

# 方式2: CLI 直接发布
clawhub publish . \
  --slug active-memory-calculus \
  --name "Active Memory for Calculus Teaching" \
  --version 1.0.0 \
  --changelog "Initial release: Active Memory and Dreaming System for calculus education"

# 方式3: Web 界面上传
# 访问 https://clawhub.ai/publish-skill
```

## 验证安装

```bash
# 安装
clawhub install active-memory-calculus

# 验证
openclaw skills status active-memory-calculus

# 预期输出:
# active-memory-calculus: enabled ✓
#   Version: 1.0.0
#   Mode: recent
#   Dreaming: enabled
```

## 更新日志

### v1.0.0 (2026-04-12)
- 初始版本发布
- 集成 OpenClaw v2026.4.10 Active Memory
- 集成梦境系统增强版
- 高等数学教学场景专项优化
- 支持6种核心概念掌握度追踪
- 支持12种高数典型错误模式识别

## 联系方式

- **作者**: 代国兴 (daigxok)
- **GitHub**: https://github.com/daigxok/active-memory-calculus
- **ClawHub**: https://clawhub.ai/daigxok
- **邮箱**: daigxok@example.com

## 致谢

- OpenClaw 团队提供 Active Memory 和 Dreaming System 核心技术
- 高等数学智慧课程项目组成员的支持
- 所有测试用户的反馈

---

**发布日期**: 2026-04-12  
**Skill 包大小**: ~80 KB  
**总文件数**: 18 个文件
