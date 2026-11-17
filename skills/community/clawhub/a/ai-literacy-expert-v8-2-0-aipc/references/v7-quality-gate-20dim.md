# V7 19 维质量门（V7 Quality Gate · 19 Dimensions）

> **文件名说明**：文件名保留 `20dim` 是为了向后兼容 V7.1 的引用路径。V7.2 删除了第 20 维度（跨 Skill 联动），实际内容为 19 维。
>
> V7.2 升级：V6 的 15 维 + V7 新增 4 维 = 19 维完整质量门控体系。

## 概述

V7 质量门在 V6 的 15 个维度基础上，新增 4 个端云协同专属维度，形成 19 维全面质量保障体系。完整的质量门检查逻辑、V7QualityGate 类实现和各维度详细标准，请参阅 `references/local-ai-quality-gate.md`。

## 19 维度总览

### V6 继承维度（#1 ~ #15）

| # | 维度 | 检查要点 |
|---|------|----------|
| 1 | 内容准确性 | 知识点无错误、教学目标对齐课标 |
| 2 | 教学适配性 | 符合目标学段认知水平 |
| 3 | 互动性 | 课件/游戏含有效交互逻辑 |
| 4 | 可访问性 | 响应式布局 + 基础无障碍支持 |
| 5 | 代码质量 | 无语法错误、中文注释完整 |
| 6 | 性能 | 首屏加载 < 3s、帧率 >= 30fps |
| 7 | 离线可用性 | Service Worker 注册 + 离线 fallback |
| 8 | 数据安全 | 本地存储加密、无明文敏感信息 |
| 9 | 商用合规 | SLA/契约/容错/成本/可观测性 |
| 10 | 版本管理 | 语义化版本 + 变更日志 |
| 11 | 协作支持 | 多教师协作冲突检测 |
| 12 | 评估有效性 | 题目覆盖认知层级 >= 3 级 |
| 13 | 推荐精准度 | 推荐匹配度 >= 80% |
| 14 | 游戏沉浸度 | 6 态状态机完整 + 难度梯度 3 级 |
| 15 | 课件艺术性 | p5.js 视觉效果 + 创意编程质量 |

### V7 新增维度（#16 ~ #19）

| # | 维度 | 检查要点 | 通过标准 |
|---|------|----------|----------|
| 16 | 端云协同分工 | 端侧重计算 + 云端轻决策分工明确 | 请求符合 6 段结构、决策类型匹配 |
| 17 | 零上传合规 | 原始数据零上传、元数据级交互 | PII 检测召回率 > 95%、ZUP 证明完整 |
| 18 | NPU 调度效率 | Intel 酷睿 Ultra NPU 优先调度 | NPU 利用率 > 60%、三级调度正确 |
| 19 | 成本可控性 | 单次请求成本 < $0.01、月预算告警 | 累计追踪 + 50%/80%/100% 三级告警 |

## V7QualityGate 类（自动化检查器）

```python
class V7QualityGate:
    """V7 19 维质量门自动化检查器"""
    
    DIMENSIONS = 19
    V6_DIMS = 15  # 继承自 V6
    V7_NEW_DIMS = 4  # V7 新增
    
    def check_all(self, artifact):
        """执行全部 19 维检查"""
        results = {}
        for dim in range(1, 20):
            results[dim] = self._check_dimension(dim, artifact)
        return results
    
    def score(self, results):
        """计算总分（每维度 5 分，满分 100）"""
        return sum(results.values()) / len(results) * 5
    
    def pass_gate(self, results, threshold=80):
        """判断是否通过质量门（>= 80 分）"""
        return self.score(results) >= threshold
```

## 评分映射

| 分数区间 | 等级 | 发布建议 |
|----------|------|----------|
| 90-100 | S | 可直接发布 |
| 80-89 | A | 修复建议项后发布 |
| 70-79 | B | 需修复关键项后重审 |
| < 70 | C | 需全面修改后重审 |

## 详细参考

完整的各维度检查方法、验证脚本和实现细节，请参阅：
- **基础质量门（#1-#15）**：`references/local-ai-quality-gate.md`
- **端云协同协议**：`references/edge-cloud-protocol.md`
- **零上传隐私**：`references/zero-upload-privacy.md`
- **NPU 调度**：`references/npu-scheduling-guide.md`
- **成本优化**：`references/cost-optimization.md`

---

> **V7.2 改进说明**：本文档为 V7.2 更新的独立索引文件，解决 SKILL.md/README.md 引用缺失问题。完整质量门内容统一维护在 `references/local-ai-quality-gate.md` 中。已删除 V7.1 的第 20 维度（跨 Skill 联动），聚焦 AI 通识课独立完整性。
