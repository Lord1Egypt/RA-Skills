> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 商用生产级标准（V4.3 新增）

> 本文档定义 V4.3 技能在商用生产环境下的全套标准，涵盖 8 个维度：SLA、输入输出契约、错误降级、调用成本预算、可观测性审计、安全最小权限、版本解耦管理、QA 全量验收门控。任何 V4.3 交付物（课件 / 游戏 / 备课包）必须满足本文档全部要求。

## 1. SLA（服务等级）

### 1.1 响应时间
| 场景 | 目标 P50 | 目标 P95 | 硬上限 |
|------|----------|----------|--------|
| 单 HTML 课件生成 | ≤ 30 s | ≤ 60 s | 120 s |
| 单 HTML 游戏生成 | ≤ 45 s | ≤ 90 s | 180 s |
| 备课包生成（4 格式 + zip） | ≤ 60 s | ≤ 120 s | 240 s |

### 1.2 可用性
- 99.5% 月度可用性（允许月宕机时间 ≤ 3.6 小时）
- 关键路径 CDN 必须有主备（cdnjs → jsdelivr → local fallback）

### 1.3 并发
- 单用户视角无并发限制
- 后端批量场景（如全校教师同时备课）需在调度层做并发限流

## 2. 输入输出契约

### 2.1 输入契约
- 课件：自然语言需求 + 可选模板参考
- 游戏：模块选择（A/B/C/D）+ 难度（1–5）
- 备课包：受众 + 模块（多选）+ 粒度

### 2.2 输出契约
- 课件/游戏：单 HTML 文件（UTF-8、≤ 200 KB、含 CDN 引用）
- 备课包：单 HTML（含交互式表单 + 一键下载 4 格式 zip，HTML ≤ 500 KB）

### 2.3 错误码
| 错误码 | 含义 | 用户操作 |
|--------|------|----------|
| E001 | CDN 资源加载失败 | 检查网络 |
| E002 | p5.js API 误用 | 重新生成 |
| E003 | JS 库（SheetJS / docx / pptxgenjs / jsPDF / JSZip）失败 | 刷新 |
| E004 | AI 接口超时 | 重试 |
| E005 | 备课包生成失败（内容缺失） | 补全约束 |

## 3. 错误降级

### 3.1 CDN 降级链

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"></script>
<script>
  if (typeof p5 === 'undefined') {
    document.write('<script src="https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js"><\/script>');
  }
  if (typeof p5 === 'undefined') {
    document.write('<script src="./vendor/p5.min.js"><\/script>');  // 本地兜底
  }
</script>
```

### 3.2 JS 库降级
- 备课 HTML 必须用 try/catch 包裹所有库调用
- 库加载失败时给用户友好提示，并保留已生成的内容（部分降级）
- JSZip 失败时回退到"4 文档分别下载"（V4 行为）

### 3.3 AI 接口降级
- 超时：自动重试 1 次；仍失败则返回"AI 不可用"提示
- 限流：熔断 60 s，期间返回"系统繁忙稍后重试"

## 4. 调用成本预算

- 单 HTML 课件：AI token ≤ 8K
- 单 HTML 游戏：AI token ≤ 12K
- 备课包（4 格式 + zip）：AI token ≤ 20K
- 硬上限：单次任务 ≤ 30K token；超出则熔断并提示用户精简需求

## 5. 可观测性审计

### 5.1 调用日志模板

```javascript
const audit = {
  ts: Date.now(),
  skill: 'ai-literacy-expert-v4.3',
  ability: 'lesson-builder',   // courseware | game | lesson-builder
  phase: 'phase-4-content-gen',
  input: { audience: '大学生', modules: ['C1'], granularity: '单元' },
  output: { files: 4, totalBytes: 245678 },
  errors: [],
  durationMs: 45321
};
// 异步上报到 /api/audit（生产环境必接）
```

### 5.2 用户行为日志
- 触发词命中次数（用于优化能力路由）
- 交付物采纳率（用户是否真正使用生成的课件 / 游戏 / 备课包）

## 6. 安全最小权限

### 6.1 API Key 存放
- 禁止：在前端 HTML 内嵌明文 API Key
- 必须：服务端代理 + 环境变量（dotenv）
- 沙箱约定：`/sandbox/workspace/.wind_env`、`/sandbox/workspace/.mx_env`

### 6.2 数据脱敏
- 学生姓名 / 教师电话 / 邮箱 → 不收集 / 不输出
- 备课内容含敏感信息时提示用户脱敏

## 7. 版本解耦管理

- 版本号遵循 semver：`v主.次.补丁`（如 v4.3.0）
- V3 / V4 / V4.3 并存，互不替换
- 用户可指定使用哪个版本（默认最新）
- 兼容性矩阵详见 SKILL.md「版本兼容矩阵」章节

## 8. QA 全量验收门控

每个交付物必须通过以下 12 项检查：

- 静态自检（语法 / API 黑名单 / 已移除 API）✅
- 语法验证（node --check 或浏览器）✅
- 逻辑预演（脑走流程）✅
- 透明声明（已验证项 / 需用户实测项）✅
- 强制测试门控结果块（附在交付物末尾）✅
- CDN 降级链完整（cdnjs → jsdelivr → local）✅
- 关键库版本号明确（p5.js 2.0.3、SheetJS 0.18.5、JSZip 3.10.1 等）✅
- 单 HTML 文件 ≤ 200 KB（备课 HTML 可放宽到 500 KB）✅
- 移动端响应式（viewport meta + CSS @media）✅
- 跨浏览器兼容（Chrome / Edge / Safari / Firefox）✅
- 教学准确性（不凭空编造 AI 概念，与 V3/V4 references 一致）✅
- 用户操作门槛（教师无需编程经验即可使用）✅

任一项未通过 → 不得交付。

## 9. 交付物清单

| 能力 | 标准交付物 | V4.3 增强 |
|------|-----------|-----------|
| 课件 | 单 HTML | + README、版本号、SHA256 |
| 游戏 | 单 HTML | + README、版本号、SHA256 |
| 备课 | 单 HTML | **+ 4 格式 zip 一键打包下载**（JSZip） |

## 10. 并发限流

- 单用户视角：无并发限制
- 全局视角：单实例 QPS ≤ 10，超出则排队（用户感知 5 s 内响应）
- 熔断：连续 5 次 E004/500 → 熔断 60 s