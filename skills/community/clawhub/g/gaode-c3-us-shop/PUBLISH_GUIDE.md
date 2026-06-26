# POI Debug Orchestrator 技能发布指南

> 将技能发布到 Aone Market (https://open.aone.alibaba-inc.com/market)

---

## 📋 发布前准备

### 1. 已完成的准备工作

✅ **技能目录结构** - 已创建完整
```
poi-debug-orchestrator/
├── package.json              # ✅ npm 包配置
├── SKILL.md                  # ✅ 技能定义
├── README.md                 # ✅ 使用文档
├── PUBLISH_README.md         # ✅ Aone Market 展示文档
├── scripts/
│   └── poi-debug.sh          # ✅ 执行脚本
└── references/
    ├── source_id_map.md      # ✅ 58 个 sourceId 映射
    ├── fields.md             # ✅ 字段说明
    └── faq.md                # ✅ FAQ
```

✅ **package.json** - 已配置
- 名称：`poi-debug-orchestrator`
- 版本：`0.2.0`
- 描述：POI 详情页问题排查编排器
- 作者：土曜 (501280)

---

## 🚀 发布步骤

### Step 1: 登录 Aone 平台

```bash
cd /app/501280/working/.claude/skills/poi-debug-orchestrator
aone-kit login
```

**操作说明**:
1. 执行命令后会提示在浏览器中打开授权链接
2. 使用你的阿里账号登录
3. 完成授权后返回终端

---

### Step 2: 验证登录状态

```bash
aone-kit whoami
```

**预期输出**:
```
Logged in as: 土曜 (501280)
Email: xxx@alibaba-inc.com
```

---

### Step 3: 执行发布（先 dry-run）

```bash
#  dry-run 模式（不会真正发布）
aone-kit skill publish --dry-run
```

**检查项**:
- ✅ 所有文件都包含在 `files` 字段中
- ✅ `package.json` 配置正确
- ✅ 没有错误提示

---

### Step 4: 正式发布

```bash
# 发布到 latest 版本
aone-kit skill publish

# 或者发布 beta 版本（测试用）
aone-kit skill publish --tag beta
```

**预期输出**:
```
📦 Publishing poi-debug-orchestrator@0.2.0...
✅ Published successfully!
🔗 View at: https://open.aone.alibaba-inc.com/market/skill/poi-debug-orchestrator
```

---

### Step 5: 验证发布结果

1. 打开 Aone Market: https://open.aone.alibaba-inc.com/market
2. 搜索 `poi-debug-orchestrator`
3. 查看技能详情页

**检查项**:
- ✅ 技能名称和描述正确
- ✅ 展示文档渲染正常
- ✅ 安装命令可用

---

## 📊 技能元数据

### 基本信息

| 字段 | 值 |
|------|-----|
| **名称** | poi-debug-orchestrator |
| **版本** | 0.2.0 |
| **描述** | POI 详情页问题排查编排器。自动执行 6 步排查流程 |
| **分类** | 开发效率 |
| **标签** | POI, 调试，日志分析，高德，编排器 |
| **作者** | 土曜 (501280) |
| **License** | MIT |

### 触发词

```
POI 排查、poi 问题、详情页异常、gsid 排查、traceId 分析、
poi 调试、contentPerson、手艺人模块、作品集排查、contentCaseBook
```

---

## 🔧 常见问题

### Q1: 发布失败 "Permission denied"

**原因**: 没有发布权限或登录过期

**解决**:
```bash
aone-kit logout
aone-kit login
# 重新授权后再试
```

---

### Q2: 发布失败 "Missing required files"

**原因**: `files` 字段配置不完整

**解决**: 检查 `package.json` 的 `files` 字段，确保包含所有必需文件：
```json
"files": [
  "SKILL.md",
  "README.md",
  "scripts/",
  "references/"
]
```

---

### Q3: 技能搜索不到

**原因**: 
- 发布后需要几分钟索引时间
- 技能名称或关键词不匹配

**解决**:
- 等待 5-10 分钟
- 使用完整名称搜索 `poi-debug-orchestrator`

---

### Q4: 更新技能版本

**步骤**:
1. 修改 `package.json` 中的 `version` 字段
2. 更新 `SKILL.md` 中的版本号
3. 重新执行发布：
   ```bash
   aone-kit skill publish
   ```

---

## 📝 发布后的操作

### 1. 分享给团队

发送技能链接给团队成员：
```
https://open.aone.alibaba-inc.com/market/skill/poi-debug-orchestrator
```

### 2. 安装使用说明

告诉团队成员如何安装：
```bash
aone-kit skill install poi-debug-orchestrator
```

### 3. 收集反馈

- 记录使用问题
- 收集改进建议
- 准备下一个版本迭代

---

## 📈 版本规划

### v0.3.0 (计划)
- [ ] 支持更多应用
- [ ] 添加自动修复建议
- [ ] 批量排查支持

### v1.0.0 (计划)
- [ ] 支持其他接口类型
- [ ] Web UI 界面
- [ ] 机器学习辅助分析

---

## 🔗 相关链接

- **Aone Market**: https://open.aone.alibaba-inc.com/market
- **技能源码**: `/app/501280/working/.claude/skills/poi-debug-orchestrator`
- **文档**: `/app/501280/working/.claude/skills/poi-debug-orchestrator/docs`

---

## 📞 联系方式

如有疑问，请联系：
- **作者**: 土曜 (501280)
- **项目**: lse2-us-business-service

---

_最后更新：2026-03-31_
