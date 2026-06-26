# ADD v7.20: 数据真实性强制执行机制

**版本**: v7.20.0  
**日期**: 2026-03-13  
**问题**: "不假设、不预估、不用假数据"是固化规则，但多次被违反  
**根因**: 规则只在文档中，无强制执行机制  
**方法**: 第一性原理 + 思维链 + MECE 拆解 + 自我校验

---

## 🎯 第一性原理分析

### 问题承认

**已固化的规则**（来自 IDENTITY.md）:
```
❌ 不预设任务方向
❌ 不假设任务前提
❌ 不虚假实现
❌ 不虚假汇报
❌ 不虚假验证
```

**已固化的规则**（来自 .workflow/汇报机制规范.md）:
```
❌ 不编造进度
❌ 验证后汇报
```

**问题**: 规则写在文档里，但**没有强制执行机制**

### 根因链

```
为什么规则被违反？
→ 因为没有强制执行机制
  ↓
为什么没有强制执行机制？
→ 因为只写在文档里，没有代码实现
  ↓
为什么没有代码实现？
→ 因为假设会自觉遵守
  ↓
为什么假设会自觉遵守？
→ 因为过度信任，缺乏制衡
```

**核心洞察**:
```
文档规则 = 建议
代码规则 = 强制

要确保规则被执行，必须：
1. 写入代码，不是文档
2. 自动检测违规
3. 自动阻止违规
4. 违规时告警
```

---

## 📐 MECE 拆解

### 维度 1: 规则类型

| 规则类型 | 当前状态 | 需要机制 |
|----------|----------|----------|
| **不假设** | ❌ 文档 | ✅ 代码检测 |
| **不预估** | ❌ 文档 | ✅ 代码检测 |
| **不编造** | ❌ 文档 | ✅ 代码检测 |
| **验证后汇报** | ❌ 文档 | ✅ 代码检测 |

### 维度 2: 执行机制

| 机制 | 复杂度 | 效果 | 实施时间 |
|------|--------|------|----------|
| **方案 1**: 违规检测器 | 中 | ✅ 自动发现 | 1 小时 |
| **方案 2**: 汇报前验证 | 中 | ✅ 阻止假数据 | 1 小时 |
| **方案 3**: 数据来源标注 | 低 | ✅ 强制标注 | 30 分钟 |
| **方案 4**: 违规告警 | 低 | ✅ 及时纠正 | 30 分钟 |

### 维度 3: 检测点

| 检测点 | 检测内容 | 拦截方式 |
|--------|----------|----------|
| **汇报生成** | 是否验证 | 阻止未验证汇报 |
| **数据使用** | 是否标注来源 | 阻止无来源数据 |
| **模型选择** | 是否官方数据 | 阻止编造数据 |
| **进度汇报** | 是否真实 | 阻止虚假进度 |

---

## 🔧 强制执行机制

### 机制 1: 数据真实性验证器

**文件**: `skills/agile-workflow/core/data-verifier.js`

```javascript
class DataVerifier {
  constructor() {
    this.rules = {
      'no-fabrication': {
        name: '不编造数据',
        check: (data) => {
          // 检测是否有来源标注
          return data.source !== undefined;
        },
        message: '❌ 数据必须标注来源'
      },
      'no-estimation': {
        name: '不预估数据',
        check: (data) => {
          // 检测是否包含估算标记
          return !data.content?.includes('估算') && 
                 !data.content?.includes('预计');
        },
        message: '❌ 不能使用预估数据'
      },
      'verify-before-report': {
        name: '验证后汇报',
        check: (report) => {
          // 检测是否有验证标记
          return report.verified === true;
        },
        message: '❌ 汇报前必须验证'
      }
    };
  }

  /**
   * 验证数据
   */
  verify(data, type) {
    const rule = this.rules[type];
    if (!rule) {
      throw new Error(`未知规则类型：${type}`);
    }

    const passed = rule.check(data);
    
    return {
      passed,
      rule: rule.name,
      message: passed ? '✅ 验证通过' : rule.message,
      data
    };
  }

  /**
   * 强制验证（失败则抛出异常）
   */
  forceVerify(data, type) {
    const result = this.verify(data, type);
    
    if (!result.passed) {
      console.error(`🚨 数据真实性违规：${result.message}`);
      throw new Error(result.message);
    }
    
    return result;
  }
}
```

---

### 机制 2: 汇报前强制验证

**文件**: `skills/agile-workflow/core/report-validator.js`

```javascript
class ReportValidator {
  constructor() {
    this.verifier = new DataVerifier();
  }

  /**
   * 验证汇报内容
   */
  async validateReport(report) {
    const validations = [];

    // 1. 验证进度数据
    if (report.progress) {
      const progressValid = await this.verifyProgress(report.progress);
      validations.push(progressValid);
    }

    // 2. 验证状态数据
    if (report.status) {
      const statusValid = await this.verifyStatus(report.status);
      validations.push(statusValid);
    }

    // 3. 验证 token 数据
    if (report.tokenUsage) {
      const tokenValid = await this.verifyTokenData(report.tokenUsage);
      validations.push(tokenValid);
    }

    // 汇总结果
    const allPassed = validations.every(v => v.passed);
    
    return {
      passed: allPassed,
      validations,
      canReport: allPassed,
      blockedReason: allPassed ? null : '数据未通过真实性验证'
    };
  }

  /**
   * 验证进度数据
   */
  async verifyProgress(progress) {
    // 检查是否有验证标记
    if (!progress.verified) {
      return {
        type: 'progress',
        passed: false,
        message: '❌ 进度数据未验证'
      };
    }

    // 检查是否有验证时间
    if (!progress.verifiedAt) {
      return {
        type: 'progress',
        passed: false,
        message: '❌ 进度数据缺少验证时间'
      };
    }

    return {
      type: 'progress',
      passed: true,
      message: '✅ 进度数据已验证'
    };
  }

  /**
   * 验证 token 数据
   */
  async verifyTokenData(tokenData) {
    // 检查数据来源
    if (!tokenData.source) {
      return {
        type: 'token',
        passed: false,
        message: '❌ Token 数据必须标注来源'
      };
    }

    // 检查是否为官方数据
    if (tokenData.source !== 'official') {
      return {
        type: 'token',
        passed: false,
        message: '⚠️ Token 数据非官方来源：' + tokenData.source
      };
    }

    return {
      type: 'token',
      passed: true,
      message: '✅ Token 数据来自官方'
    };
  }
}
```

---

### 机制 3: 违规告警系统

**文件**: `skills/agile-workflow/core/violation-alarm.js`

```javascript
class ViolationAlarm {
  constructor() {
    this.violations = [];
    this.alarmLog = '/home/ubutu/.openclaw/workspace/logs/violations.log';
  }

  /**
   * 记录违规
   */
  recordViolation(type, details) {
    const violation = {
      timestamp: new Date().toISOString(),
      type,
      details,
      severity: this.getSeverity(type)
    };

    this.violations.push(violation);
    this.logViolation(violation);
    this.triggerAlarm(violation);
  }

  /**
   * 获取违规严重程度
   */
  getSeverity(type) {
    const severityMap = {
      'fabrication': 'critical',  // 编造数据
      'estimation': 'high',       // 预估数据
      'unverified': 'medium',     // 未验证
      'no-source': 'low'          // 无来源
    };
    return severityMap[type] || 'medium';
  }

  /**
   * 记录到日志
   */
  logViolation(violation) {
    const fs = require('fs');
    const log = `[${violation.timestamp}] ${violation.severity.toUpperCase()}: ${violation.type} - ${JSON.stringify(violation.details)}\n`;
    fs.appendFileSync(this.alarmLog, log);
  }

  /**
   * 触发告警
   */
  triggerAlarm(violation) {
    console.error(`\n🚨 数据真实性违规告警`);
    console.error(`类型：${violation.type}`);
    console.error(`严重程度：${violation.severity}`);
    console.error(`详情：${JSON.stringify(violation.details)}`);
    console.error(`时间：${violation.timestamp}\n`);
  }

  /**
   * 获取违规统计
   */
  getViolationStats() {
    const stats = {
      total: this.violations.length,
      byType: {},
      bySeverity: {}
    };

    for (const v of this.violations) {
      stats.byType[v.type] = (stats.byType[v.type] || 0) + 1;
      stats.bySeverity[v.severity] = (stats.bySeverity[v.severity] || 0) + 1;
    }

    return stats;
  }
}
```

---

### 机制 4: 强制标注数据来源

**修改**: `model-switcher.js`

```javascript
/**
 * 获取模型信息（强制标注来源）
 */
getModelInfo(modelName) {
  const model = this.models[modelName];
  
  if (!model) {
    throw new Error(`未知模型：${modelName}`);
  }

  // ✅ 强制检查数据来源
  if (!model.source) {
    throw new Error(`模型 ${modelName} 缺少数据来源标注`);
  }

  // ✅ 强制检查是否为官方数据
  if (model.source !== 'official') {
    console.warn(`⚠️ 警告：${modelName} 数据来自 ${model.source}，非官方数据`);
  }

  return {
    ...model,
    verified: true,
    verifiedAt: new Date().toISOString()
  };
}
```

---

## ✅ 自我校验

### 校验 1: 违规是否被检测？

**验证**:
```javascript
const verifier = new DataVerifier();

// 测试编造数据
try {
  verifier.forceVerify(
    { content: 'Kimi 有 256K 上下文' },  // 无来源
    'no-fabrication'
  );
} catch (error) {
  console.log(error.message);  // 应该输出 "❌ 数据必须标注来源"
}
```

**预期**: ✅ 检测到违规

---

### 校验 2: 汇报前是否验证？

**验证**:
```javascript
const validator = new ReportValidator();

const report = {
  progress: { value: 50 },  // 未验证
  verified: false
};

const result = await validator.validateReport(report);
console.log(result.canReport);  // 应该输出 false
```

**预期**: ✅ 阻止未验证汇报

---

### 校验 3: 违规是否告警？

**验证**:
```javascript
const alarm = new ViolationAlarm();

alarm.recordViolation('fabrication', {
  data: '假数据',
  source: '编造'
});

// 应该输出告警信息并记录日志
```

**预期**: ✅ 触发告警

---

## 📊 执行机制对比

| 机制 | 检测能力 | 阻止能力 | 告警能力 |
|------|----------|----------|----------|
| **文档规则** | ❌ 无 | ❌ 无 | ❌ 无 |
| **数据验证器** | ✅ 自动 | ✅ 抛出异常 | ✅ 控制台 |
| **汇报验证器** | ✅ 自动 | ✅ 阻止汇报 | ✅ 控制台 |
| **违规告警** | ✅ 自动 | ❌ 仅记录 | ✅ 日志 + 控制台 |

---

## 📝 实施步骤

### 已完成（设计）

1. ✅ DataVerifier 设计
2. ✅ ReportValidator 设计
3. ✅ ViolationAlarm 设计
4. ✅ 强制标注机制设计

### 待完成（实施）

5. ⏳ 实现 DataVerifier
6. ⏳ 实现 ReportValidator
7. ⏳ 实现 ViolationAlarm
8. ⏳ 集成到工作流
9. ⏳ 测试验证

---

## ✅ 总结

### 核心问题

**规则失效**:
1. ❌ 规则只在文档中
2. ❌ 无强制执行机制
3. ❌ 无违规检测
4. ❌ 无违规告警

### 修复方案

**强制执行机制** (4 个):
1. ✅ DataVerifier（数据验证）
2. ✅ ReportValidator（汇报验证）
3. ✅ ViolationAlarm（违规告警）
4. ✅ 强制标注机制

### 核心原则固化

```
数据真实性原则（强制执行）：
1. 不编造数据 → 代码检测 ✅
2. 不预估数据 → 代码检测 ✅
3. 验证后汇报 → 代码检测 ✅
4. 标注数据来源 → 强制检查 ✅
5. 违规自动告警 → 自动触发 ✅
```

---

**下一步**: 实现强制执行组件并集成到工作流！
