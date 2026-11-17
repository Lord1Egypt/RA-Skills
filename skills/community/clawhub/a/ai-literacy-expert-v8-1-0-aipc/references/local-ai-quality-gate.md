> **V7 质量门规范**：本文件为 V7 原生版本，完整集成 V7 端云协同增强能力。V7 在 V6 的 15 维质量门基础上，新增 4 个端云协同专属维度（#16-#19），形成 19 维完整质量门体系。
> V7 核心 references：`references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md` / `references/deployment-guide.md`。
> 原始文件版本：V6 · 升级版本：V7 · 升级日期：2026-08-15 · 当前维度：19 维

# 本地 AI 质量门规范

> V7 版 19 维质量门的完整定义。V5 原有 11 维 → V6 增加 4 维本地 AI 相关维度（共 15 维）→ V7 增加 4 维端云协同专属维度（共 19 维）。

## 质量门总览

### V5 原有 11 维（继承）

| # | 维度 | 检查内容 | 通过标准 |
|---|------|----------|----------|
| 1 | HTML 结构 | DOCTYPE, lang, meta charset, viewport | 全部存在且正确 |
| 2 | p5.js 规范 | 使用 p5.js 2.x CDN，Instance Mode | 版本正确，模式合规 |
| 3 | 单文件完整 | 所有 CSS/JS 内联，无外部依赖（CDN 除外） | 单文件可独立运行 |
| 4 | 中文内容 | 所有界面文本为中文 | 零英文残留（代码除外） |
| 5 | 教学准确 | 内容与 AI 通识课教材一致 | 知识点无错误 |
| 6 | 交互完整 | 所有按钮/交互可正常工作 | 零死链、零死按钮 |
| 7 | 响应式 | 适配桌面和平板 | 1024px+ 正常显示 |
| 8 | 无障碍 | 基本 a11y（alt, aria, 对比度） | WCAG 2.1 AA 级 |
| 9 | 代码质量 | 命名规范，注释充分，无 console.error | 零错误、零警告 |
| 10 | 离线支持 | Service Worker + IndexedDB | 离线可加载，数据可恢复 |
| 11 | 安全合规 | 无敏感信息泄露，内容安全 | 零安全风险 |

### V6 新增 4 维

| # | 维度 | 检查内容 | 通过标准 | 权重 |
|---|------|----------|----------|------|
| 12 | 本地 AI 集成 | OCR/ASR/TTS/RAG 调用正确 | 工具调用成功率 ≥99% | 必检 |
| 13 | 跨平台兼容 | Qoder/WorkBuddy/TRAE Work 适配 | 3 平台均可正常运行 | 必检 |
| 14 | 流水线完整 | 多工具 Pipeline 串联正确 | 端到端执行成功率 ≥95% | 必检 |
| 15 | 商用交付 | README/演示/部署文档齐全 | 交付清单 100% 完成 | 必检 |

### V7 新增 4 维（端云协同专属）

| # | 维度 | 检查内容 | 通过标准 | 权重 |
|---|------|----------|----------|------|
| 16 | 端云协同分工验证 | 边缘预处理/云端轻决策分工明确 | 端云分工 100% 标注，协议合规 | 必检 |
| 17 | 零上传隐私计算 | 4 级 PII 脱敏 + ZUP 证明 + 数据生命周期 | 零 PII 上传，法规合规 | 必检 |
| 18 | NPU 智能调度 | 异构调度/OpenVINO 量化/性能基准 | NPU 加速 ≥4x，资源池分配合规 | 必检 |
| 19 | 端云成本监控 | 单次成本/月度累计/告警/熔断 | 单次 ≤$0.001，月度 ≤$10 | 必检 |

---

## 维度 12：本地 AI 集成质量门

### 检查项

#### 12.1 工具调用正确性
```
□ OCR 调用格式符合 local-ocr-integration.md 规范
□ ASR 调用格式符合 local-asr-integration.md 规范
□ TTS 调用格式符合 local-tts-integration.md 规范
□ RAG 调用格式符合 local-rag-integration.md 规范
□ Analysis 调用格式符合 local-data-analysis.md 规范
□ Gateway 统一入口调用正确
```

#### 12.2 错误处理完备性
```
□ 每个工具调用都有 try-catch 包裹
□ 服务不可达时有 Fallback 降级（云端 API）
□ 超时处理（OCR:10s, ASR:30s, TTS:5s, RAG:8s）
□ 错误信息对用户友好（非技术语言）
□ 错误日志记录到 console.warn（非 console.error）
```

#### 12.3 OpenVINO 优化验证
```
□ 模型加载使用正确的设备分配（参考 openvino-optimization-guide.md）
□ INT8 量化后精度损失 <2%
□ 推理延迟在目标范围内
□ 内存占用在设备限制内
```

#### 12.4 工具链状态检测
```javascript
// 必须实现的健康检查
async function checkAITools() {
  const tools = ['ocr', 'asr', 'tts', 'rag', 'analysis'];
  const status = {};
  
  for (const tool of tools) {
    try {
      const res = await fetch(`http://localhost:8900/health?tool=${tool}`, {
        signal: AbortSignal.timeout(3000)
      });
      status[tool] = res.ok ? 'ready' : 'degraded';
    } catch {
      status[tool] = 'unavailable';
    }
  }
  
  return status;
}
// 通过标准：至少 3/5 工具为 'ready' 状态
```

### 通过标准
- 工具调用格式 100% 符合规范
- 错误处理覆盖率 100%（每个工具调用都有 Fallback）
- 健康检查实现且逻辑正确
- OpenVINO 配置符合优化指南

---

## 维度 13：跨平台兼容质量门

### 检查项

#### 13.1 Skill 接口规范
```
□ SKILL.md 符合 agent-tool-adaptation.md 中的 JSON Schema
□ inputSchema 定义完整（type, properties, required）
□ outputSchema 定义完整
□ 版本号遵循 semver
```

#### 13.2 平台适配
```
□ Qoder 平台：Skill 注册和调用正常
□ WorkBuddy 平台：MCP 协议适配正确
□ TRAE Work 平台：工具描述和调用兼容
□ 平台检测逻辑正确（自动识别当前平台）
```

#### 13.3 降级策略
```
□ 平台不支持某工具时优雅降级
□ 降级提示信息清晰
□ 核心功能不依赖单一平台特性
```

### 通过标准
- Skill Schema 验证通过
- 至少适配 2 个平台（推荐 3 个全适配）
- 降级策略文档化

---

## 维度 14：流水线完整质量门

### 检查项

#### 14.1 Pipeline 定义
```
□ 预定义流水线（教材数字化/课堂录音分析/有声课件/学情分析）至少实现 1 个
□ 流水线步骤顺序正确
□ 步骤间数据传递格式正确
□ 流水线状态可追踪
```

#### 14.2 端到端执行
```
□ 流水线可从起点执行到终点
□ 中间步骤失败时有重试或跳过机制
□ 最终产出物完整可用
□ 执行日志可导出
```

#### 14.3 数据流验证
```
□ OCR → RAG：文本正确传递，编码一致（UTF-8）
□ ASR → TTS：音频格式转换正确
□ RAG → Analysis：查询结果可被分析引擎消费
□ 全链路：数据无丢失、无损坏
```

### 通过标准
- 至少 1 条预定义流水线可端到端执行
- 数据流验证通过（无丢失/损坏）
- 流水线状态可追踪

---

## 维度 15：商用交付质量门

### 检查项

#### 15.1 文档完整性
```
□ README.md：项目说明、功能列表、安装步骤、使用方法
□ 演示文档：使用截图或 GIF 展示核心功能
□ 部署指南：环境要求、安装命令、配置说明、故障排除
□ API 文档：工具接口说明（如使用了本地 AI）
```

#### 15.2 交付物格式
```
□ HTML 文件符合 commercial-delivery-suite.md 标准
□ 包含标准 meta 标签和 CDN 回退
□ 文件命名规范（小写、连字符、无空格）
□ 打包格式正确（ZIP/单文件/项目目录）
□ 课件/游戏 HTML 文件体积 ≤ 200KB
□ 备课 HTML 文件体积 ≤ 500KB
□ CDN 3 级回退验证通过：cdnjs → jsdelivr → local vendor
```

#### 15.3 商用级品质
```
□ 无硬编码的测试数据
□ 无 console.log 调试输出
□ 无 TODO/FIXME 注释
□ 错误信息用户友好
□ 加载状态有提示
```

### 通过标准
- README + 部署指南 100% 完成
- HTML 符合商用模板标准
- 零 TODO/FIXME，零调试输出
- 课件/游戏 HTML ≤ 200KB，备课 HTML ≤ 500KB
- CDN 3 级回退（cdnjs → jsdelivr → local vendor）验证通过

---

## 维度 16：端云协同分工验证质量门

### 检查项

#### 16.1 边缘预处理完整性
```
□ 端侧数据预处理流程完整（OCR 文本清洗、ASR 标点修正、图像裁剪）
□ 预处理后的数据可直接用于云端决策（格式标准化）
□ 预处理异常时有本地兜底处理
□ 预处理日志可追溯
```

#### 16.2 云端轻决策正确性
```
□ 云端仅处理 4 类轻决策（creative/analytical/educational/strategic）
□ 决策类型标注正确（符合 edge-cloud-protocol.md 定义）
□ 决策结果在端侧正确执行和应用
□ 决策缓存命中率 ≥ 40%
```

#### 16.3 协议格式合规（<10KB）
```
□ 每次端云请求 abstract_data < 10KB（Edge-Cloud Protocol v1.0 约束）
□ 请求体符合 6 段结构（protocol_version/request_id/timestamp/source/abstract/request/callback）
□ 协议版本号正确（"1.0"）
□ 超限时自动截断或分片
```

#### 16.4 降级策略有效性
```
□ 5 级降级策略（L1-L5）全部实现并可触发
□ L1→L5 各级触发条件正确
□ 降级过程用户无感知（或提示友好）
□ 降级恢复后自动回到 L1
```

#### 16.5 审计日志完整性
```
□ 每次端云交互生成 ZUP 审计记录
□ 审计日志包含：request_id、timestamp、decision_type、cost、latency
□ 审计日志存储于端侧 `/var/log/ai-literacy/zup/`
□ 审计日志不可篡改、可导出
```

### 通过标准
- 端云分工标注覆盖率 100%
- 协议格式 100% 合规（<10KB/请求）
- 5 级降级策略全部可触发
- ZUP 审计日志完整

---

## 维度 17：零上传隐私计算质量门

### 检查项

#### 17.1 4 级 PII 脱敏完整性
```
□ L1 标识符脱敏：姓名/身份证/手机/邮箱/学号 → 端侧替换为匿名 ID
□ L2 关系脱敏：住址/学校/班级/家长 → 端侧泛化处理
□ L3 行为脱敏：时间戳/答题路径/行为模式 → 端侧聚合统计
□ L4 内容脱敏：作文/发言/心理评估 → 端侧摘要提取（仅上传摘要）
□ 4 级脱敏全部在端侧 NPU 完成，原始数据零上传
```

#### 17.2 ZUP 证明格式正确
```
□ 每次端云请求附带 `pii_detected: false` 声明
□ ZUP 证明包含脱敏前后数据哈希对比
□ ZUP 证明格式符合 zero-upload-privacy.md 规范
□ ZUP 证明可被第三方审计工具验证
```

#### 17.3 数据生命周期合规（7 天原始/30 天元数据）
```
□ 原始数据端侧保留 ≤ 7 天（到期自动加密删除）
□ 抽象元数据端侧+云端保留 ≤ 30 天
□ 教学决策数据端侧永久保留
□ 数据清理任务自动执行（cron job）
□ 清理日志可审计
```

#### 17.4 法规合规（GDPR/PIPL/COPPA）
```
□ GDPR 合规：数据最小化、目的限制、存储限制、问责制
□ 中国《个人信息保护法》合规：知情同意、最小必要、数据本地化
□ COPPA 合规：13 岁以下监护人同意、不超范围收集
□ 隐私政策文档完整且可访问
□ 用户可查看/导出/删除个人数据
```

#### 17.5 应急响应机制
```
□ PII 泄露应急预案文档化
□ 检测到 PII 上传时自动阻断并告警
□ 应急响应流程可在 15 分钟内启动
□ 应急演练记录（至少每季度 1 次）
```

### 通过标准
- 4 级 PII 脱敏 100% 实现
- ZUP 证明格式正确率 100%
- 数据生命周期合规（7/30 天规则严格执行）
- 三大法规（GDPR/PIPL/COPPA）合规
- 应急响应机制完备

---

## 维度 18：NPU 智能调度质量门

### 检查项

#### 18.1 异构调度正确性（NPU/iGPU/CPU）
```
□ OCR 任务分配到 NPU（INT8 量化模型）
□ ASR 任务分配到 NPU（INT4 量化模型）
□ TTS 任务分配到 NPU（FP16 模型）
□ VLM 任务分配到 iGPU（Qwen2.5-VL-7B INT4）
□ 端侧 LLM 降级任务分配到 CPU（Qwen-1.5B INT4）
□ 设备分配可通过配置文件调整
□ 设备不可用时自动降级到次优设备
```

#### 18.2 OpenVINO 量化配置
```
□ OCR 模型：INT8 量化（精度损失 <2%）
□ ASR 模型：INT4 量化（WER 增加 <1%）
□ RAG 嵌入模型：INT8 量化
□ VLM 模型：INT4 量化
□ 端侧 LLM：INT4 量化
□ 所有量化模型通过 NNCF 工具链验证
```

#### 18.3 性能基准达标（4x+ 加速）
```
□ NPU 推理速度 ≥ CPU 推理速度的 4 倍
□ OCR 单次推理延迟 < 200ms（NPU）
□ ASR 实时率（RTF）< 0.3（NPU）
□ TTS 合成延迟 < 500ms/句（NPU）
□ RAG 查询延迟 < 100ms（NPU）
□ 性能基准测试脚本可复现
```

#### 18.4 NPU 利用率监控
```
□ NPU 利用率实时可查（Prometheus 指标 `v7_npu_utilization`）
□ 利用率 > 90% 持续 5 分钟触发告警
□ 利用率数据可回溯（Grafana 可视化）
□ 利用率异常时自动调整调度策略
```

### 通过标准
- 异构调度正确率 100%
- OpenVINO 量化配置符合规范
- NPU 加速比 ≥ 4x（对比 CPU）
- NPU 监控指标完整

---

## 维度 19：端云成本监控质量门

### 检查项

#### 19.1 单次请求成本控制（≤$0.001）
```
□ 每次端云请求成本 ≤ $0.001
□ 成本计算包含：API 调用费 + 数据传输费 + 缓存开销
□ max_tokens 限制生效（L1:500, L2:250）
□ 成本统计精确到单次请求级别
```

#### 19.2 月度累计成本控制（≤$10）
```
□ 月度云端总成本 ≤ $10
□ 成本统计仪表盘可实时查看
□ 成本数据可按日/周/月粒度查看
□ 成本趋势可预测（基于历史数据）
```

#### 19.3 成本告警阈值（80% 预算）
```
□ 月度成本达到 80% 预算（$8）时触发告警
□ 告警通知发送到管理员（邮件/IM）
□ 告警记录可查询
□ 告警阈值可配置
```

#### 19.4 自动熔断机制
```
□ 月度成本达到 100% 预算（$10）时自动熔断
□ 熔断后切换到纯端侧模式（L3-L5 降级）
□ 熔断状态可手动解除
□ 熔断事件记录到审计日志
```

#### 19.5 成本审计日志
```
□ 每次云端调用记录成本（精确到 $0.0001）
□ 成本日志包含：timestamp、provider、model、tokens、cost_usd
□ 成本日志可导出（CSV/JSON）
□ 成本日志与 ZUP 审计日志关联
```

### 通过标准
- 单次请求成本 ≤ $0.001
- 月度累计成本 ≤ $10
- 80% 预算告警正常触发
- 自动熔断机制有效
- 成本审计日志完整

---

## 质量门执行流程

### 自动检查（代码级）

```javascript
// V7 质量门自动检查器
class V7QualityGate {
  constructor(html, skillMd) {
    this.html = html;
    this.skillMd = skillMd;
    this.results = [];
  }
  
  async runAll() {
    // V5 维度 (1-11)
    this.checkHTMLStructure();      // #1
    this.checkP5jsSpec();           // #2
    this.checkSingleFile();         // #3
    this.checkChineseContent();     // #4
    this.checkTeachingAccuracy();   // #5
    this.checkInteraction();        // #6
    this.checkResponsive();         // #7
    this.checkAccessibility();      // #8
    this.checkCodeQuality();        // #9
    this.checkOfflineSupport();     // #10
    this.checkSecurity();           // #11
    
    // V6 维度 (12-15)
    this.checkLocalAIIntegration(); // #12
    this.checkCrossPlatform();      // #13
    this.checkPipelineIntegrity();  // #14
    this.checkCommercialDelivery(); // #15
    
    // V7 新增维度 (16-19)
    this.checkEdgeCloudSynergy();   // #16
    this.checkZeroUploadPrivacy();  // #17
    this.checkNPUScheduling();      // #18
    this.checkCostMonitoring();     // #19
    
    return this.results;
  }
  
  checkLocalAIIntegration() {
    const checks = [
      { name: '工具调用格式', pass: this._validateToolCalls() },
      { name: '错误处理', pass: this._validateErrorHandling() },
      { name: '健康检查', pass: this._validateHealthCheck() },
      { name: 'Fallback 降级', pass: this._validateFallback() }
    ];
    
    this.results.push({
      dimension: 12,
      name: '本地 AI 集成',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
  
  checkCrossPlatform() {
    const checks = [
      { name: 'Skill Schema', pass: this._validateSkillSchema() },
      { name: '平台适配', pass: this._validatePlatformAdapters() },
      { name: '降级策略', pass: this._validateDegradation() }
    ];
    
    this.results.push({
      dimension: 13,
      name: '跨平台兼容',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
  
  checkPipelineIntegrity() {
    const checks = [
      { name: '流水线定义', pass: this._validatePipelineDef() },
      { name: '端到端执行', pass: this._validateE2EExecution() },
      { name: '数据流', pass: this._validateDataFlow() }
    ];
    
    this.results.push({
      dimension: 14,
      name: '流水线完整',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
  
  checkCommercialDelivery() {
    const checks = [
      { name: '文档完整', pass: this._validateDocs() },
      { name: '交付格式', pass: this._validateDeliveryFormat() },
      { name: '商用品质', pass: this._validateCommercialQuality() },
      { name: '文件体积限制', pass: this._validateFileSize() },
      { name: 'CDN 3 级回退', pass: this._validateCDNFallback() }
    ];
    
    this.results.push({
      dimension: 15,
      name: '商用交付',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
  
  // === V7 新增检查方法 ===
  
  checkEdgeCloudSynergy() {
    const checks = [
      { name: '边缘预处理完整性', pass: this._validateEdgePreprocessing() },
      { name: '云端轻决策正确性', pass: this._validateCloudDecision() },
      { name: '协议格式合规（<10KB）', pass: this._validateProtocolFormat() },
      { name: '降级策略有效性', pass: this._validateDegradationLevels() },
      { name: '审计日志完整性', pass: this._validateAuditLog() }
    ];
    
    this.results.push({
      dimension: 16,
      name: '端云协同分工验证',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
  
  checkZeroUploadPrivacy() {
    const checks = [
      { name: '4 级 PII 脱敏完整性', pass: this._validatePIIMasking() },
      { name: 'ZUP 证明格式正确', pass: this._validateZUPProof() },
      { name: '数据生命周期合规', pass: this._validateDataLifecycle() },
      { name: '法规合规（GDPR/PIPL/COPPA）', pass: this._validateRegulations() },
      { name: '应急响应机制', pass: this._validateEmergencyResponse() }
    ];
    
    this.results.push({
      dimension: 17,
      name: '零上传隐私计算',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
  
  checkNPUScheduling() {
    const checks = [
      { name: '异构调度正确性', pass: this._validateHeterogeneousScheduling() },
      { name: 'OpenVINO 量化配置', pass: this._validateOpenVINOConfig() },
      { name: '性能基准达标（4x+）', pass: this._validatePerformanceBenchmark() },
      { name: 'NPU 利用率监控', pass: this._validateNPUMonitoring() }
    ];
    
    this.results.push({
      dimension: 18,
      name: 'NPU 智能调度',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
  
  checkCostMonitoring() {
    const checks = [
      { name: '单次请求成本 ≤$0.001', pass: this._validatePerRequestCost() },
      { name: '月度累计成本 ≤$10', pass: this._validateMonthlyCost() },
      { name: '成本告警阈值（80%）', pass: this._validateCostAlert() },
      { name: '自动熔断机制', pass: this._validateCircuitBreaker() },
      { name: '成本审计日志', pass: this._validateCostAuditLog() }
    ];
    
    this.results.push({
      dimension: 19,
      name: '端云成本监控',
      checks: checks,
      pass: checks.every(c => c.pass)
    });
  }
}
```

### 人工检查清单（交付前）

```
=== V7 商用交付人工检查清单 ===

基本信息
□ 项目名称清晰明确
□ 版本号正确（semver）
□ 作者信息完整

功能验证
□ 核心功能手动测试通过
□ 本地 AI 工具调用测试通过
□ Fallback 降级测试通过
□ 边界条件测试通过

文档检查
□ README.md 完整且准确
□ 安装步骤可复现
□ 演示内容完整
□ API 文档（如有）准确

商用检查
□ 无测试数据残留
□ 无调试输出
□ 错误提示友好
□ 加载状态完善
□ 离线功能正常

交付打包
□ 文件命名规范
□ 目录结构清晰
□ 打包体积合理
□ 所有依赖声明完整
□ 课件/游戏 HTML 文件 ≤ 200KB
□ 备课 HTML 文件 ≤ 500KB
□ CDN 3 级回退验证（cdnjs → jsdelivr → local vendor）

端云协同验证（V7 新增 #16）
□ 边缘预处理与云端轻决策分工明确
□ 端云协议格式合规（<10KB/请求）
□ 5 级降级策略（L1-L5）可触发
□ ZUP 审计日志完整

隐私合规验证（V7 新增 #17）
□ 4 级 PII 脱敏全部生效
□ ZUP 证明格式正确
□ 数据生命周期合规（7 天原始/30 天元数据）
□ GDPR/PIPL/COPPA 法规合规
□ 应急响应机制可执行

NPU 调度验证（V7 新增 #18）
□ NPU/iGPU/CPU 异构调度正确
□ OpenVINO 量化配置符合规范
□ NPU 加速比 ≥ 4x
□ NPU 利用率监控正常

成本监控验证（V7 新增 #19）
□ 单次请求成本 ≤ $0.001
□ 月度累计成本 ≤ $10
□ 80% 预算告警正常触发
□ 自动熔断机制有效
□ 成本审计日志完整
```

---

## 评分映射表

将 19 维质量门映射到大赛 6 个评分维度：

| 评分维度 | 权重 | 对应质量门维度 | 覆盖度 |
|----------|------|----------------|--------|
| 场景价值 | 30% | #5 教学准确, #6 交互完整, #12 AI集成, #16 端云协同, #17 零上传隐私 | 100% |
| 商用生产力 | 30% | #10 离线支持, #13 跨平台, #14 流水线, #15 商用交付, #19 成本监控 | 100% |
| 工具使用 | 20% | #12 AI集成（工具调用/错误处理/健康检查）, #18 NPU智能调度 | 100% |
| 文章质量 | 10% | #1 HTML, #2 p5.js, #3 单文件, #4 中文, #8 无障碍, #9 代码质量 | 100% |
| 创新性 | 10% | #12 AI集成（OpenVINO优化）, #14 流水线（创新组合）, #16 端云协同（协议创新）, #18 NPU调度（异构加速） | 100% |
| 传播附加分 | 5% | #15 商用交付（README/演示/部署文档） | 100% |

**总覆盖率：100%（19/19 维度全部映射）**
