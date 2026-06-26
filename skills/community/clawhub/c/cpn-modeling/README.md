# CPN Modeling Skill

> 着色 Petri 网（Colored Petri Net）业务流程建模技能，适用于 Claude Code / Kiro 等 AI 编程助手。

**Author:** fanyouyang  
**Company:** [habitat.cn](https://www.habitat.cn/)  
**License:** MIT

---

## 简介

这是一个面向业务流程建模的 AI Skill，帮助 Claude 从自然语言描述中提取 CPN 模型，输出：

- **JSON 模型**：结构化的库所、变迁、弧、依赖关系
- **CPN Tools XML**：可直接导入 CPN Tools 4.x 的 `.cpn` 文件
- **HTML 可视化**：带动画的 Canvas Petri 网，支持自动运行、单步、4套主题切换

适用场景：审批流程、电商订单、餐厅点餐、工程工序、医院门诊等任何有并发和资源竞争的业务流程。

---

## 核心特性

- **角色链划分**：按并发参与者（员工/主管/HR）划分子项目，而非顺序阶段
- **资源库所模式**：人工参与者建模为资源库所，初始持有 token，消耗后归还，自然建模资源竞争
- **防死锁验证**：逐一检查每个变迁的输入库所是否有 token 来源
- **无意义变迁检测**：识别并消除只搬运 token 的 silent transition
- **交互引导模式**：用业务语言一步步引导不懂 CPN 的用户完成建模
- **动态可视化**：粒子动画展示 token 流动，泳道背景区分角色链，4套宋式配色

---

## 快速开始

### 安装（Claude Code / Superpowers）

将本目录放入你的 skills 路径：

```bash
~/.claude/skills/cpn-modeling/
```

或通过 openclaw 插件市场安装。

### 使用示例

```
用户：帮我对请假审批流程建模，员工提交申请，主管审批，HR 确认
```

Claude 会自动识别并输出：
1. 完整 JSON 模型（含资源库所、依赖关系）
2. CPN Tools XML（可导入 CPN Tools 4.x）
3. HTML 可视化文件（浏览器直接打开）

---

## 文件结构

```
cpn-modeling/
├── SKILL.md                    # 技能主文件（模式判断、建模规则、输出流程）
├── README.md                   # 本文件
└── references/
    ├── modeling-guide.md       # 建模方法论（库所/变迁/依赖/子项目划分）
    ├── example-restaurant.md   # 经典示例：餐厅点餐流程
    ├── json-schema.md          # JSON 格式规范
    ├── cpn-xml-template.md     # CPN Tools XML 模板
    └── html-viz-template.md    # HTML 可视化模板（Canvas 动画）
```

---

## 建模原则

### 为什么按角色链划分，而不是按阶段划分？

| 错误做法（按阶段） | 正确做法（按角色链） |
|---|---|
| 申请阶段 / 审批阶段 / 通知阶段 | 员工链 / 主管链 / HR链 |
| 顺序流程图，无并发 | 三条链并发运行，通过资源库所同步 |
| 无法回答"多个请求同时到来会怎样" | 能建模资源竞争和并发等待 |

CPN 的核心价值是回答：**同时有 3 个员工请假，主管只有 1 个，第 2、3 个请求会在哪里等待？**

### 资源库所模式

```
P_主管空闲（初始 token: 1）
T_主管审批 输入：申请_已提交 + 主管_空闲
T_主管审批 输出：主管_已决定 + 主管_空闲（归还）
```

消耗 + 归还 = 占用期间阻塞其他请求，完成后释放。

---

## 可视化效果

- 圆形 = 库所，矩形 = 变迁，实线箭头 = 弧
- 有 token 的库所发光，可触发的变迁高亮
- 粒子动画展示 token 在节点间流动
- 泳道背景区分不同角色链
- 4套宋式主题：天青（汝窑）/ 墨夜（极简）/ 石青（冷灰）/ 朱砂（暖白）

---

## License

MIT © [fanyouyang](https://www.habitat.cn/) · [GitHub](https://github.com/theosunny/cpn-modeling-skill)
