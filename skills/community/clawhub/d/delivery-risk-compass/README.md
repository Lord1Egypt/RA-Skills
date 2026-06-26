# delivery-risk-compass

项目交付罗盘：按行业、阶段、项目形态和风险信号输出交付风险判断与行动建议。

## 运行

```bash
npm test
node src/index.js --quick --project "某平台升级项目" --industry "政府/公共服务" --type "实施+开发" --cycle "6个月" --signals "环境未准备,验收口径变化"
```

## 输入参数

- `--project`：项目代称
- `--industry`：政府、零售、制造、金融等
- `--type`：纯开发、实施+开发、纯实施、运维
- `--cycle`：项目周期
- `--team-size`：团队人数
- `--payment`：付款节点
- `--client-location`：交付方式
- `--phase`：当前阶段
- `--signals`：风险信号，逗号分隔

## 输出模块

- 项目健康度
- 当前阶段建议
- 行业风险侧重点
- 推荐交付卡点
- 沟通策略
- 救急方案
- 下一步动作

## 内容原则

本 Skill 使用行业化经验方法论，不包含真实个人、真实客户、真实厂商、真实项目名称或具体项目数据。
