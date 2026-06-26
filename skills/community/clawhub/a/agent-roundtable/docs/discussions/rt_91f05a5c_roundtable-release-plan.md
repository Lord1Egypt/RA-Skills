# 圆桌讨论结论：roundtable 发布到各大 skill 平台以及开源的相关事宜

## 基本信息
- **讨论 ID**: rt_91f05a5c
- **日期**: 2026-05-23
- **参与者**: 协调者（小赫）、饼哥（产品总监）、像素姐（设计师）、码飞（开发工程师）
- **轮次**: 3 轮

---

## 共识点

1. **版本号**: 0.1.0（最小可信发布，留余地）
2. **发布平台**: 0.1.0 只发 Hermes Skill Hub，PyPI 和 npm 后续版本再铺
3. **LICENSE**: Apache 2.0（专利保护更友好）
4. **产品定位**: "让 AI Agent 学会开会"
5. **推广策略**: Demo 视频 + 真实案例 + 社区互动，先 Hermes 生态内跑通再向外辐射
6. **技术准备时间**: 2 天足够，D3 上线

---

## 行动项

### 饼哥（产品总监）
| 时间 | 任务 | 状态 |
|------|------|------|
| D0 | CHANGELOG.md + SECURITY.md 初稿 | ⬜ |
| D1 | README banner 终稿确认，Demo 脚本定稿（90 秒横版） | ⬜ |
| D2 | Demo 视频录制剪辑，发布 checklist 走查 | ⬜ |

### 像素姐（设计师）
| 时间 | 任务 | 状态 |
|------|------|------|
| D0 | Banner 设计稿（1280×640 深色主题） | ⬜ |
| D1 | Demo 视频分镜脚本 + 关键帧设计 | ⬜ |
| D2 | Demo 视频视觉包装（片头/转场/字幕） | ⬜ |

### 码飞（开发工程师）
| 时间 | 任务 | 状态 |
|------|------|------|
| D0 | Apache 2.0 LICENSE、CHANGELOG.md、SECURITY.md、CI/CD 流水线 | ⬜ |
| D1 | PyPI 基础设施（不发布）、Skill Hub 打包验证、Demo 技术素材 | ⬜ |
| D2 | 全量回归测试、版本号锁定 0.1.0、打 tag | ⬜ |

### 补充项（全员确认）
- CONTRIBUTING.md（码飞 D0）
- CODE_OF_CONDUCT.md（码飞 D0）
- NOTICE 文件（第三方依赖 license 声明）
- Issue/PR 模板（码飞 D0）
- README banner + OG image（像素姐 D0）
- 内部文档清理：OPC-EXPERIENCE-REPORT.md、PRD.md 等（码飞 D0）

---

## 发布节奏

```
D0（今天）  → 技术基础设施 + 文档补全 + Banner 设计
D1          → Demo 脚本 + 分镜 + Skill Hub 打包验证
D2          → 视频制作 + 全量测试 + 冻结
D3（上午）  → Hermes Skill Hub 上线
D3-D7       → 内部 dogfood，收真实反馈
D7+         → 社区推广（PyPI、npm、Product Hunt 等）
```

---

## 设计规范

- **Banner**: 1280×640，深色主题，左侧项目名+定位，右侧 WebViewer 截图
- **Logo**: 暂用文字方案，0.2.0 出正式版
- **Demo 视频**: 1920×1080，60fps，90 秒横版，深色终端背景，字体 ≥16px
- **配色**: 深靛蓝 #1a1a2e + 亮橙 #ff6b35 或翠绿 #00d4aa

---

## 详细发言记录

### 第 1 轮

**协调者**：开场，提出讨论框架（平台选择、开源准备、版本号、推广策略）

**饼哥**：建议分 P0/P1/P2 三梯队发布。P0 = Hermes Skill Hub + GitHub；P1 = npm + Awesome Lists；P2 = Product Hunt/HN/Twitter。定位"让 AI Agent 学会开会"。版本号 0.1.0。推广以 demo 视频和真实案例为核心。

**像素姐**：logo 用圆桌+气泡意象，配色深靛蓝+亮橙/翠绿。README 要有 banner（1200×630 OG image）+ badges。WebViewer 用三栏布局。Demo 视频做竖版 30 秒 + 横版 90 秒两个版本。

**码飞**：三通道发布（PyPI + npm + Hermes Skill Hub）。CI/CD 三阶段（PR lint+test → main 集成测试 → tag 发布）。测试需分离核心测试和 Hermes 集成测试。Python ≥3.10，Windows 兼容性注意。紧急项：LICENSE 缺失、内部文档需移除、build-backend 需修复。

### 第 2 轮

**协调者**：总结共识和分歧，提出行动项初稿。

**饼哥**：支持 Hermes 优先，0.1.0 只发 Skill Hub。WebViewer 暂不独立拆包。紧急项排序：LICENSE > 内部文档 > build-backend。MVP = Skill Hub 单包 + 30 秒 Demo + README。

**像素姐**：同意"先窄后宽"。Banner 先行 logo 后置。Demo 视频规格：1920×1080，60fps，90 秒。"第一印象三件套"：banner + demo GIF + quick start。

**码飞**：同意只发 Skill Hub，但 PyPI 基础设施必须现在准备好。LICENSE 选 Apache 2.0。代码清理 2 天计划。CI/CD 最小方案：GitHub Actions 一条 workflow。

### 第 3 轮

**协调者**：确认行动项，要求各位明确负责事项和时间节点。

**饼哥**：补 CHANGELOG.md + SECURITY.md。D0-D2 时间节点，D3 上线。先内部 dogfood 再推社区。"最小可信发布，不是最小可发就发"。

**像素姐**：Banner D0，Demo 分镜 D1，视频包装 D2。CHANGELOG 格式模板。Banner 设计需 D0 上午对齐品牌调性。

**码飞**：D0 补 LICENSE/CHANGELOG/SECURITY/CI/CD。D1 PyPI 基础设施 + Skill Hub 验证。D2 回归测试 + 打 tag。补 Contributing 指南和 Issue/PR 模板。"时间线合理，2 天绑绑有余"。

---

## 结论

全员高度共识，无重大分歧。行动项按角色分配清晰，D0-D2 并行推进，D3 上线 Hermes Skill Hub。后续版本（0.2.0+）再铺 PyPI 和 npm。
