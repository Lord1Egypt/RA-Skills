# AUBO 机器人技能包 - 上传说明

**版本：** v1.0.0  
**创建时间：** 2026-04-04  
**作者：** RobotQu / JMO

---

## 📁 文件结构

```
aubo-robot-upload/
├── 📄 README_上传说明.md       # 本文件
├── 📄 SKILL.md                 # 技能文档（必需）
├── 📄 aubo_openclaw_driver.py  # OpenClaw 驱动（必需）
├── 📄 manifest.json            # 配置信息（必需）
├── 📄 package.json             # npm 配置（可选）
│
├── 🧪 测试脚本/
│   ├── demo_motion_auto.py     # 自动演示
│   ├── test_rtde_official.py   # RTDE 测试
│   └── read_pose_simple.py     # 位姿读取
│
├── 📚 文档/
│   ├── PUBLISH.md              # 推送指南
│   └── INTEGRATION_SUMMARY.md  # 集成总结
│
└── 📝 依赖说明.txt             # 依赖说明
```

---

## 🎯 上传到不同平台

### 1. 上传到 ClawHub.ai

**必需文件：**
```
- SKILL.md
- aubo_openclaw_driver.py
- manifest.json
- README.md
```

**步骤：**
1. 访问 https://clawhub.ai
2. 登录账号
3. 创建技能 → 上传
4. 选择上述文件
5. 填写元数据
6. 提交审核

---

### 2. 上传到 GitHub

**完整文件：**
```
整个 aubo-robot-upload/ 文件夹
```

**步骤：**
1. 创建新仓库：`aubo-robot-skill`
2. 上传所有文件
3. 添加 LICENSE
4. 更新 README
5. 创建 Release v1.0.0

---

### 3. 集成到 OpenClaw 主框架

**核心文件：**
```
- aubo_openclaw_driver.py  → robots/
- SKILL.md                 → skills/
- manifest.json            → config/
```

**步骤：**
1. 复制到主框架对应目录
2. 更新主技能注册表
3. 测试集成
4. 提交 PR

---

## 📋 上传前检查清单

- [ ] 所有文件已准备
- [ ] 文档已更新
- [ ] 测试通过
- [ ] 依赖说明完整
- [ ] 许可证文件
- [ ] 版本号正确

---

## 🔗 相关资源

- **AUBO 官网:** https://www.aubo-robotics.cn/
- **OpenClaw:** https://docs.openclaw.ai
- **ClawHub:** https://clawhub.ai

---

*创建时间：2026-04-04*
