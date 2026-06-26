# DealPilot - 运行与测试指南

## 技能状态
- **版本**: v0.1.0 (MVP 骨架)
- **状态**: 骨架完成，返回 mock 数据
- **平台适配器**: 全部为 stub 实现

## 快速测试

### 1. 运行自测脚本
```bash
cd /Users/jianghaidong/.openclaw/skills/dealpilot
node scripts/test-stub.js
```

输出示例:
```
=== DealPilot 骨架自测 ===
输入规范化: { ... }
--- 运行决策引擎 ---
决策报告生成: ✓
推荐平台: pdd
结论: 针对"蓝牙耳机"，综合价格、品质、售后风险...
```

### 2. 在代码中调用
```javascript
const { normalizeRequest } = require('./scripts/normalize.js');
const { decide } = require('./scripts/decide.js');
const { formatReport } = require('./scripts/analyze.js');

async function test() {
  const request = normalizeRequest({ 
    product: "iPhone 15", 
    budget: { max: 5000 },
    urgency: "medium" 
  });
  const report = await decide(request);
  console.log(formatReport(report));
}

test();
```

## 目录结构
```
dealpilot/
├── SKILL.md                 # 技能定义（OpenClaw 使用）
├── clawhub.json            # 技能元数据
├── package.json            # 依赖配置
├── README.md               # 项目说明
├── RUNNING.md              # 本文件
├── engine/                 # 决策引擎
│   ├── router.ts          # 路由层（决策入口）
│   └── types.ts           # 类型定义
├── platforms/              # 平台适配器
│   ├── base.ts            # 适配器基类
│   ├── taobao.ts          # 淘宝适配器（stub）
│   ├── pdd.ts             # 拼多多适配器（stub）
│   ├── jd.ts              # 京东适配器（stub）
│   ├── yhd.ts             # 一号店适配器（stub）
│   └── vip.ts             # 唯品会适配器（stub）
└── scripts/               # 工具脚本
    ├── normalize.js       # 需求解析
    ├── decide.js          # 决策调用
    ├── analyze.js         # 报告格式化
    └── test-stub.js       # 自测脚本
```

## 开发下一步

### 阶段 1: 接入真实数据
1. **淘宝平台** - 接入 `taobao` skill 的搜索功能
2. **拼多多平台** - 接入 `pdd-shopping` skill 的百亿补贴检查
3. **京东平台** - 接入 `jingdong` skill 的自营商品搜索
4. **一号店/唯品会** - 实现基础搜索功能

### 阶段 2: 增强功能
1. **价格抓取** - 实时价格、优惠券、满减计算
2. **风险评估** - 店铺信誉、评论分析、假货识别
3. **时机判断** - 促销日历、历史价格趋势
4. **个性化推荐** - 基于用户历史偏好的权重调整

### 阶段 3: 生产就绪
1. **错误处理** - 网络超时、平台 API 变化
2. **缓存策略** - 价格缓存、搜索结果缓存
3. **性能优化** - 并行搜索、结果聚合
4. **监控告警** - 成功率监控、异常检测

## 验证清单
- [x] `openclaw skills check` 可识别 dealpilot
- [x] `test-stub.js` 运行成功
- [x] SKILL.md 包含完整使用说明
- [x] 所有平台适配器骨架就位
- [ ] 接入真实平台数据
- [ ] 端到端测试真实商品
- [ ] 性能测试与优化

## 故障排除
1. **TypeScript 编译问题**: 当前使用 .js 文件，如需 TypeScript 编译需添加 tsconfig.json
2. **路径问题**: 确保从 `/Users/jianghaidong/.openclaw/skills/dealpilot/` 目录运行脚本
3. **模块导入**: 使用 ES module 语法 (`import`)，确保 `package.json` 有 `"type": "module"`

## 相关链接
- [SKILL.md](./SKILL.md) - 技能完整文档
- [PM 进度跟踪](../../shared/pm-progress/dealpilot.json) - 项目状态
- [GitHub 仓库](https://github.com/harrylabsj/dealpilot) - 源代码