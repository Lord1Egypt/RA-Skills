# shuangseqiu (双色球筛选 Skill)

SkillHub 双色球号码筛选与预测分析 AI Skill。

## 项目结构

```
shuangseqiu/
├── SKILL.md                  # 技能核心文件（入口）
├── references/
│   ├── filter-rules.md       # 过滤规则参考文档
│   └── draw-history.csv      # 开奖数据缓存（运行时生成）
├── scripts/
│   └── ssq_analyzer.py       # Python 号码筛选分析脚本
└── AGENTS.md                 # 本文件
```

## 发布到 SkillHub

两种方式：

### 方式一：通过 CLI 发布
```bash
# 安装 SkillHub CLI
curl -fsSL https://skillhub.cn/install/skillhub.md | sh

# 登录
skillhub login

# 初始化（在项目根目录执行）
skillhub init

# 推送技能文件
skillhub push

# 发布上线
skillhub publish
```

### 方式二：通过官网发布
1. 访问 https://skillhub.cloud.tencent.com/publish
2. 填写技能信息（名称/描述/分类等）
3. 上传 SKILL.md 及参考文件
4. 提交审核

## 开发指引

- 技能名 `shuangseqiu` 必须与目录名一致
- 修改 SKILL.md 后需重新推送
- 所有脚本支持 `--type` 参数：ssq(双色球) fc3d(福彩3D) qlc(七乐彩) kl8(快乐8) df61(东方6+1) 15x5(15选5)
- 数据文件按玩法分别缓存：`references/{玩法简称}-history.csv`
- 走势图按玩法分目录：`assets/charts/{玩法简称}/`
- 如需加速全组合过滤计算，可升级 `scripts/ssq_analyzer.py`
- 审核标准：TRACE 评测（可信任度/可靠性/适用性/规范性/有效性）
