# 飞猪联动 CHANGELOG

## v1.0.3 — 2026-11-06

### 去敏：移除内部服务地址和规模数字

- `travel_agent.py`：`GAODE_BASE` 改读环境变量 `GAODE_POI_BASE`，缺失时报错退出（不硬编码服务器 IP）
- `SKILL.md`：数据来源说明去掉规模数字（「995 万」「102 城」），改为「REST API，服务地址通过环境变量配置」；新增 `GAODE_POI_BASE` 到用法示例
- **重要**：运行时须同时设置 `GAODE_POI_KEY` 和 `GAODE_POI_BASE` 两个环境变量

### 下一步

- 配 GAODE_POI_BASE 实测三城，通过后发 clawhub

## v1.0.2 — 2026-10-21

### 新增：自然语言解析层

新增 `--query` 参数，agent 可直接吃整句话，无需手动拆 `--city`/`--place`/日期：

```bash
python3 travel_agent.py --query "我下周去成都宽窄巷子住两晚"
```

支持的日期表达：明天、后天、大后天、这/本周末、下周末、下周X（一~日）、YYYY-MM-DD、X月Y日。
支持的住宿天数：住N晚/N天（汉字和数字都能识别）。
城市从内置 60+ 城市列表匹配；地点用去噪后最长 token 提取。

`--city`/`--place`/`--check-in`/`--check-out` 仍可单独传入，`--query` 只填补空缺项，两者可混用。

## v1.0.1 — 2026-10-21

### 修复（小W冒烟测试发现）

- 锚定 bug（最关键）：`pick_destination` 新增名称匹配优先级，避免搜"哈德门广场"时锚到楼内"华为授权服务中心"
- 空指针：flyai 返回 `data: null` 时不再崩溃，改为自动重试一次；重试后仍无结果才降级提示
- 网络兼容：高德请求加 `User-Agent` 头，解决 macOS 代理拦截 Python 默认 UA 的问题
- flyai 偶发超时：自动重试最多 3 次（间隔 2s）

### 下一步

- Hackathon 截止 2026-10-25：补自然语言解析层 + 录 30 秒 demo

## v1.0 — 2026-10-21

### 做了什么

- 新建项目子目录 `飞猪联动/`，打通高德 POI × 飞猪酒店实时库存
- `travel_agent.py`：高德 `/search` 解析任意地名（商圈、地铁站、餐厅、小区）→ 拿规范名和坐标 → 喂给飞猪 `search-hotel` 拿真实房价和预订链接
- `SKILL.md`：OpenClaw Skill 声明，intents 覆盖 `hotel_search`/`travel_booking`/`poi_anchored_hotel_search`

### 关键决策

- **双锚定策略**：高德返回的类目非住宿时用 `--key-words`（通用，如 798艺术区）；类目是住宿时（说明输入是泛名词如"西湖"）回退用 `--poi-name`（飞猪对头部景区锚定更准）。这绕开了飞猪 `--poi-name` 只认头部景区、`--key-words` 对泛名词偏移的核心限制
- **API key 只走环境变量 `GAODE_POI_KEY`**，不写入任何文件（遵守全局安全规则）
- **高德富化可选**：`--enrich-nearby` 附上目的地 1km 内餐饮，复用现有 POI 数据库

### 验证

- 798艺术区（普通商圈）→ 3 家真实酒店，¥236–¥358，feizhu.com 预订链接，锚定"近798艺术区" ✓
- 西湖（头部景区）→ poi-name 回退后锚定"近杭州西湖风景名胜区" ✓
- 酒仙桥（非著名地名）+ `--enrich-nearby` → 周边餐饮 5 条带评分 ✓

### 发布信息

- clawhub slug：`gaode-hotel`，version `1.0.0`，versionId `k97b67je4rv69ynkp9c4re264h8gqj0j`
- 发布账号：`han815757857-cmd`
- 状态：已发布，pending clawhub moderation scan（verdict: clean，正常流程）
- 安装命令：`clawhub install gaode-hotel`（scan 通过后生效）

### 下一步待做

- Hackathon 截止 2026-10-25，还有 4 天：打包成可 `clawhub install` 的 Skill 包
- 补一个自然语言解析层：现在要手动拆 `--city`/`--place`/日期，下一步让 agent 直接吃"我下周去成都宽窄巷子出差住两晚"这种整句
- 录一个 30 秒 demo 视频：三句话三座城（798/西湖/宽窄巷子）展示任意地点锚定能力，作为提交作品
