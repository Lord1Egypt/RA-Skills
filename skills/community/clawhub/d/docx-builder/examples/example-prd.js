/**
 * Docx Skill 使用示例 — 生成一份极简 PRD
 */

const {
  createDoc, saveDoc,
  PH1, PH2, PH3, P, PB, Pbullet, pageBreak,
  reqTable, precondTable, boundaryTable, acTable, changeTable,
  callout, divider,
} = require('./docx-skill');

const doc = createDoc({
  title: '产品需求文档 (PRD)',
  subtitle: '智能体市场与创建管理',
  meta: [
    '模块：1.1.1  |  版本：v1.1.0  |  状态：评审中',
    '产品：蜂动智能体平台  |  日期：2026-04-21',
  ],
  headerText: '蜂动智能体平台  |  PRD v1.1',
  footerText: '产品团队 · 蜂动智能体平台',
  children: [
    // 变更日志
    changeTable([
      { ver: 'v1.0.0', date: '2026-04-14', author: '产品团队', desc: '初稿完成' },
      { ver: 'v1.1.0', date: '2026-04-21', author: '产品团队', desc: '补充验收标准与 API 契约' },
    ]),

    pageBreak(),

    // 1. 文档说明
    PH1('1  文档说明'),
    PH2('1.1  阅读指引'),
    P([PB('文档约定：')]),
    Pbullet('每条需求均有唯一编号，可跨文档引用'),
    Pbullet('P0 = 阻塞性；P1 = 重要；P2 = 优化'),

    pageBreak(),

    // 2. 功能需求
    PH1('2  功能需求详述'),
    PH2('2.1  智能体市场'),
    PH3('2.1.1  前置条件'),
    precondTable([
      { type: '用户身份', item: '浏览权限', desc: '所有用户均可浏览模板列表' },
      { type: '用户身份', item: '部署权限', desc: '需登录且具备智能体创建权限' },
    ]),

    divider(),

    PH3('2.1.2  功能需求'),
    reqTable([
      { id: 'MK-01', pri: 'P0', name: '网格布局', desc: '卡片网格，桌面端 4 列，1280px 以下 3 列' },
      { id: 'MK-02', pri: 'P0', name: '搜索',   desc: 'debounce 300ms 触发，最大长度 50 字符' },
    ]),

    divider(),

    PH3('2.1.3  边界条件'),
    boundaryTable([
      { id: 'BC-01', scene: '模板列表为空', trigger: '后端返回 []', behavior: '展示空态插画', recover: '点击重试' },
      { id: 'BC-02', scene: 'Demo 超频', trigger: '1 分钟 > 20 条', behavior: '禁用输入框 60s', recover: '倒计时结束后自动恢复' },
    ]),

    pageBreak(),

    // 3. 验收标准
    PH1('3  验收标准'),
    acTable([
      { id: 'AC-01', item: '首屏加载', expected: 'FCP < 1.5s', method: 'Lighthouse', pri: 'P0' },
      { id: 'AC-02', item: '搜索防抖', expected: '300ms debounce', method: '网络面板', pri: 'P0' },
    ]),

    pageBreak(),

    // 4. 风险提示
    PH1('4  风险提示'),
    callout('注意', '本文档为机密文件，仅限内部流通。'),
  ]
});

saveDoc(doc, './example-prd.docx');
