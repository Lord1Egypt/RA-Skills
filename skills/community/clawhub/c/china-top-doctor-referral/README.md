# 🏥 三甲专家推荐 — OceanBus P2P 实时查询

**1,721 位三甲医院专家，8 城市 × 29+ 科室。OceanBus P2P 实时查询，不再使用本地 JSON。**

[![ClawHub](https://img.shields.io/badge/ClawHub-china--top--doctor--referral-blue)](https://clawhub.ai/skills/china-top-doctor-referral)
[![clones](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ryanbihai/china-top-doctor-referral/main/clones.json)](https://github.com/ryanbihai/china-top-doctor-referral/graphs/traffic)
[![GitHub stars](https://img.shields.io/github/stars/ryanbihai/china-top-doctor-referral)](https://github.com/ryanbihai/china-top-doctor-referral)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)

---

## v2 重大变更

- **废弃本地 experts.json**（228位）→ OceanBus P2P 实时查询 DoctorDataSvc（1,721位）
- **新增城市**：上海（原仅北京/天津/成都/深圳/苏州/佛山/青岛）
- **废弃 refer.py** → 新 `search-doctors.js`（纯 Node.js）
- 6 条反幻觉强制约束，杜绝 LLM 编造医生

## 安装

```bash
openclaw skills install china-top-doctor-referral
cd ~/.openclaw/workspace/skills/china-top-doctor-referral
npm install
```

## 使用

```bash
# 按科室+城市搜索
node scripts/search-doctors.js search --city "北京" --depts "消化科"

# 关键词过滤
node scripts/search-doctors.js search --city "上海" --depts "神经科" --keyword "冬雷"

# 查看可用城市/科室
node scripts/search-doctors.js list-cities
node scripts/search-doctors.js list-depts

# 联系客服（OceanBus P2P）
node scripts/send-cs.js "用户:xxx | 消息:xxx"
```

## 数据

OceanBus DoctorDataSvc：1,721 位专家 · 8 城市 · 29 科室。P2P 加密传输。

## 相关项目

- [OceanBus SDK](https://www.npmjs.com/package/oceanbus) — 核心基础设施
- [ocean-desk](https://github.com/ryanbihai/ocean-desk) — B 端坐席工单系统
- [health-checkup-recommender](https://clawhub.ai/skills/health-checkup-recommender) — 循证体检推荐
- [Ocean Chat](https://clawhub.ai/skills/ocean-chat) — P2P 消息 + 通讯录

## License

MIT-0
