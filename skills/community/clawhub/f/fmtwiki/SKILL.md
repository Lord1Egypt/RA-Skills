---
name: fmtwiki
description: >
  FMTWiki 肠菌移植专业知识库运营与维护 Skill。

  触发场景（精确匹配）：
  - 用户说"更新FMTWiki"、"更新知识库"、"刷新词条"
  - 用户提到具体疾病词条（rCDI/UC/CD/ASD等）+ "更新"或"补充"
  - 用户说"发布新文献"、"添加PubMed"、"补充论文"
  - 用户说"给FMTWiki加知识"、"扩展FMTWiki"
  - 用户说"运行定时任务"、"触发文献追踪"、"执行更新"
  - 用户说"查看FMTWiki"、"打开知识库"、"fmtwiki"

  禁止自动触发（负例）：
  - 用户只说"FMT是什么" → 应调用 medical 子代理，而非直接更新知识库
  - 用户说"帮我搜一下FMT文献" → 应调用搜索，而非更新数据文件
  - 用户说"FMT最新进展" → 应调用 daily-hot-ai-news，而非更新 wiki 数据
---

# FMTWiki Skill

## 项目定位

FMTWiki 是面向临床医生、医学生、研究人员、患者的**垂直领域循证知识库**，聚焦粪菌移植（Fecal Microbiota Transplantation，FMT）。

**部署地址：** https://pvphcoybalzc.space.minimaxi.com
**项目路径：** `/workspace/projects/fmtwiki/fmtwiki-query/`
**GitHub：** `zmy1006-sudo/fmtwiki-query`

---

## 核心原则（强制执行）

| 原则 | 说明 | 违反后果 |
|------|------|---------|
| **循证优先** | 所有词条必须有原始文献引用（PMID/DOI/Science） | 禁止 |
| **来源必链** | 所有信息必须附来源链接，禁止无链接断言 | 禁止 |
| **M-DQA 强制** | 医学内容新增/修改必须经 Generator→Evaluator 双代理 QA | 强制 |
| **PMID 验证** | 通过 PubMed 搜索标题+期刊+年份验证，不使用猜测 PMID | 强制 |
| **双标签分级** | Oxford（研究设计）+ GRADE（证据质量）双标签 | 强制 |

---

## 项目结构

```
fmtwiki-query/
├── src/
│   ├── data/          ← 知识库数据（TypeScript 常量）
│   │   ├── diseases.ts       14个适应证（含临床方案、PMID溯源）
│   │   ├── teams.ts          21个国内研究团队
│   │   ├── aiApps.ts         19个AI×FMT应用
│   │   ├── science.ts         7篇 Science 期刊论文
│   │   ├── patientEdu.ts     35篇患者科普
│   │   ├── patient.ts         6个患者版适应证（通俗版）
│   │   ├── decisionTree.ts   15节点临床决策树（PMID已验证）
│   │   ├── drugInteractions.ts  15条药物相互作用
│   │   ├── hospitalMap.ts    10家全国FMT医院
│   │   └── searchIndex.ts    全站搜索索引（BM25+同义词）
│   ├── lib/
│   │   ├── aiSearch.ts       GLM API 调用（含无Key降级）
│   │   └── utils.ts          工具函数
│   └── components/
│       ├── App.tsx            路由状态机
│       ├── LoginPage.tsx      双入口（医生蓝/患者薄荷绿）
│       ├── DoctorPortal.tsx   医生五Tab（适应证/患者版/团队/AI应用/Science）
│       ├── PatientPortal.tsx  患者九Tab + 顶部搜索栏
│       ├── AISearchPanel.tsx  AI搜索界面（双栏+证据卡片）
│       └── EvidenceGuide.tsx 证据等级说明（Oxford/GRADE）
├── wiki/                ← 源文档层（raw markdown，Generator来源）
│   ├── diseases/
│   ├── teams/
│   ├── science/
│   └── ai-apps/
├── scripts/            ← 定时任务脚本
│   ├── tracker.ts      状态追踪器
│   └── reports/        执行报告
└── dist/               ← 部署产物
```

---

## 数据文件字段定义

### diseases.ts
```typescript
interface Disease {
  id: string;                    // 英文ID，如 "rCDI"
  name: string;                 // 中文名，如 "复发性艰难梭菌感染"
  nameEn: string;                // 英文名
  category: string;             // 分类，如 "感染性疾病"
  evidenceGrade: string;         // "Oxford 1b · GRADE A" 格式
  gradeLabel: string;            // "A级"
  gradeColor: string;            // Tailwind 配色类
  efficacy: string;              // 疗效摘要
  routes: string;                // 给药途径
  summary: string;              // 循证摘要
  administrationRoute: string;   // 临床方案：途径
  dosage: string;               // 临床方案：剂量
  frequency: string;            // 临床方案：疗程
  protocolNote?: string;        // 临床方案：备注
  sources: Source[];             // 循证文献列表
  keyRef: string;               // 关键引用说明
  contraindications: string;    // 禁忌证
  warnings?: string;            // 警示
}

interface Source {
  type: 'PMID' | 'NCT' | 'DOI' | 'URL';
  label: string;
  url: string;
}
```

### teams.ts / aiApps.ts / science.ts
类似结构，参考现有文件格式。

---

## GLM API Key 配置（Step 5）

### 当前状态
AI 搜索面板已接入 GLM API（MiniMax），当前为**演示模式**（未配置 Key 时降级）。

### 配置步骤

**Step 1：获取 API Key**
1. 访问 https://www.minimaxi.com/document
2. 注册/登录 MiniMax 账号
3. 创建 API Key（abab5.5-chat 模型）

**Step 2：创建 .env 文件**
```bash
# 在 /workspace/projects/fmtwiki/fmtwiki-query/ 下创建 .env
VITE_GLM_API_KEY=your_api_key_here
```

**Step 3：重新构建部署**
```bash
cd /workspace/projects/fmtwiki/fmtwiki-query
pnpm run build
# 构建完成后自动部署
```

**验证：** 访问 AI 搜索面板，发送问题，观察是否从"[演示模式]"切换为真实 GLM 回复。

### aiSearch.ts 关键参数
```typescript
const API_URL = 'https://api.minimaxi.com/v1/text/chatcompletion_v2';
const model = 'abab5.5-chat';
temperature = 0.3;   // 专业回答用低温
max_tokens = 800;    // 控制响应长度
```

---

## M-DQA SOP（Generator → Evaluator 双代理审查）

**触发条件：** 任何疾病词条、团队、AI应用、Science论文数据的新增或修改。

**流程：**
```
Step 1: Generator（写作代理）
  → 撰写新内容/修改，列出所有 PMID
  → 输出：草稿 + PMID 列表

Step 2: Evaluator（审查代理）
  → 独立审查内容准确性
  → 通过 PubMed 逐条验证每个 PMID（标题+期刊+年份匹配）
  → 拒绝任何无法验证的 PMID

Step 3: 写入数据文件
  → 仅在 Evaluator 通过后写入 src/data/*.ts
```

**PMID 验证方法：**
- 访问 `https://pubmed.ncbi.nlm.nih.gov/?term={PMID}`
- 核对：标题、期刊、年份完全匹配
- 不匹配 → 废弃该 PMID，重新搜索正确文献

---

## 定时任务

| 任务 | 触发 | 内容 | 脚本 |
|------|------|------|------|
| `fmtwiki-littracker-001` | 周六 09:00 | PubMed 新文献扫描 | `scripts/tracker.ts` |
| `fmtwiki-teams-update` | 每3天 09:30 | 团队最新动态 | 同上 |
| `fmtwiki-aiapps-update` | 每日 22:00 | AI应用动态 | 同上 |
| `fmtwiki-science-tracker` | 每日 08:00 | Science期刊追踪 | 同上 |

---

## 首页版本管理

| 方案 | 文件 | 状态 |
|------|------|------|
| Effect A | LandingPage.tsx | 备选（粒子宇宙暗色）|
| Effect B | LandingPageB.tsx | 备选（数据仪表盘）|
| Effect C | LandingPageC.tsx | 备选（DNA双螺旋）|
| Effect D | LandingPageD.tsx | 备选（暗场显微镜）|
| **Effect E** | **LandingPageE.tsx** | **✅ 主版本**（融合版）|

Effect E = Effect A 视觉骨架 + Effect D 文案内容 + GRADE四宫格/Oxford进度条/运行状态面板。

---

## 维护 Checklist

- [ ] **新增疾病词条**：Generator→Evaluator→PubMed验证→写入 diseases.ts
- [ ] **更新团队信息**：Generator→Evaluator→写入 teams.ts
- [ ] **添加AI应用**：Generator→Evaluator→来源链接验证→写入 aiApps.ts
- [ ] **PubMed文献追踪**：tracker.ts 执行→报告→Generator→Evaluator→写入 science.ts
- [ ] **GLM API Key 配置**：创建 .env → build → 验证 AI 搜索面板
- [ ] **首页归档**：保留 Effect E，删除 LandingPage/B/C/D

---

## 联系方式

- 项目负责人：赵铭远
- 医学顾问：苏州市立医院 FMT 团队
- 技术栈：React + TypeScript + TailwindCSS + Vite + MiniMax GLM API
