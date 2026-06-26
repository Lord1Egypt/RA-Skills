# AppDev Skill - 通用应用软件开发工作流

基于 **豆因DeveloperSkill-workflow v2.3** 提炼的通用HarmonyOS应用开发工作流。

## 特性

- ✅ **六阶段开发流程**：产品设计 → 规划 → 生成 → 实现 → 验证 → 集成
- ✅ **PRD工具链**：自动生成需求文档、用户流程、数据埋点设计
- ✅ **TDD支持**：Red-Green-Refactor完整测试驱动开发
- ✅ **代码生成**：Model/Service/Page/ViewModel一键生成
- ✅ **调试诊断**：日志/状态/性能/指南四维诊断工具
- ✅ **编译验证**：强制DevEco编译通过，提前发现问题
- ✅ **版本管理**：自动化版本归档与CHANGELOG生成

## 快速开始

### 1. 创建新项目

```bash
bash scripts/init-project.sh ./MyApp UserManager
cd MyApp
```

### 2. 产品功能设计

```bash
# 初始化PRD文档
bash scripts/prd.sh init '用户管理'

# 生成用户流程图
bash scripts/prd.sh flow '用户管理'

# 设计数据埋点
bash scripts/prd.sh tracking '用户管理'
```

### 3. 生成代码骨架

```bash
# 生成数据模型
bash scripts/generate.sh model User

# 生成服务
bash scripts/generate.sh service UserService

# 生成页面
bash scripts/generate.sh page User

# 生成ViewModel
bash scripts/generate.sh viewmodel User
```

### 4. TDD开发

```bash
# 启动TDD流程
bash scripts/tdd.sh start UserService getUserInfo

# 运行测试（Red Phase）
bash scripts/tdd.sh run

# 实现业务逻辑（或智能填充）
bash scripts/fill-logic.sh UserService getUserInfo

# 运行测试（Green Phase）
bash scripts/tdd.sh run

# 重构检查
bash scripts/tdd.sh refactor
```

### 5. 编译验证

```bash
# 编译检查
bash scripts/build-check.sh

# 规范检查
bash scripts/lint.sh src/services/UserService.ts

# 运行测试
bash scripts/test.sh UserService
```

### 6. 版本归档

```bash
./scripts/update.sh minor "完成用户管理功能"
```

## 项目结构

```
MyApp/
├── docs/
│   └── prd/                    # PRD文档
│       ├── 用户管理_PRD.md
│       ├── 用户管理_flow.md
│       └── 用户管理_tracking.md
├── src/
│   ├── models/                 # 数据模型
│   │   └── User.ts
│   ├── services/               # 业务服务
│   │   └── UserService.ts
│   ├── pages/                  # 页面组件
│   │   └── UserPage.ets
│   ├── viewmodels/             # 状态管理
│   │   └── UserViewModel.ts
│   └── common/                 # 公共工具
│       └── utils/
├── test/
│   └── unittest/
│       └── UserService.test.ts
├── scripts/                    # 工作流脚本
│   ├── init-project.sh
│   ├── prd.sh
│   ├── generate.sh
│   ├── tdd.sh
│   ├── debug.sh
│   ├── build-check.sh
│   └── update.sh
├── templates/                  # 代码模板
├── PROJECT.md                  # 项目配置
└── version.json                # 版本信息
```

## 六阶段开发流程

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  产品   │ →  │  规划   │ →  │  生成   │ →  │  实现   │ →  │  验证   │ →  │  集成   │
│(Product)│    │ (Plan)  │    │(Generate)│   │(Implement)│   │(Validate) │   │(Integrate)│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
    1h            30min          1h            2-4h           30min          30min
   PRD文档       需求对齐       代码骨架       业务逻辑       编译+测试       版本归档
```

## 工具脚本清单

| 脚本 | 用途 | 示例 |
|-----|------|------|
| `init-project.sh` | 项目初始化 | `bash scripts/init-project.sh ./MyApp UserManager` |
| `prd.sh init` | 初始化PRD | `bash scripts/prd.sh init '用户管理'` |
| `prd.sh flow` | 生成用户流程 | `bash scripts/prd.sh flow '用户管理'` |
| `prd.sh tracking` | 设计数据埋点 | `bash scripts/prd.sh tracking '用户管理'` |
| `generate.sh` | 代码生成 | `bash scripts/generate.sh service UserService` |
| `tdd.sh` | TDD流程 | `bash scripts/tdd.sh start UserService getUser` |
| `fill-logic.sh` | 代码填充 | `bash scripts/fill-logic.sh UserService getUser` |
| `debug.sh` | 调试诊断 | `bash scripts/debug.sh . logs 100` |
| `build-check.sh` | 编译验证 | `bash scripts/build-check.sh` |
| `update.sh` | 版本管理 | `./scripts/update.sh minor "完成功能"` |

## 规范检查规则

| 规则ID | 级别 | 说明 |
|-------|------|------|
| HOS-001 | 警告 | 使用@ObservedV2替代@Observed |
| HOS-002 | 错误 | 禁止使用any类型 |
| PERF-001 | 警告 | 避免在循环中使用await |
| SEC-001 | 错误 | 敏感数据使用SecureStorage |
| BUILD-001 | 错误 | DevEco编译必须通过 |

## 与豆因DeveloperSkill的区别

| 特性 | 豆因DeveloperSkill | AppDev Skill |
|-----|-------------------|--------------|
| 适用范围 | 豆因咖啡应用 | 任意HarmonyOS应用 |
| 业务模板 | 咖啡领域专用（口味指纹等） | 通用模板 |
| 复杂度 | 高（含复杂算法） | 中（标准业务） |
| 定制化 | 深度定制 | 可配置 |
| 学习曲线 | 陡峭 | 平缓 |

## 适用场景

- ✅ 企业级HarmonyOS应用开发
- ✅ 创业团队MVP快速开发
- ✅ 个人开发者项目标准化
- ✅ 教学/培训标准化流程
- ✅ HarmonyOS创新赛参赛项目

## 扩展开发

### 添加自定义模板

1. 创建模板文件 `templates/my-template.hbs.txt`
2. 使用Handlebars语法定义变量
3. 在generate.sh中添加生成逻辑

### 添加自定义检查规则

1. 编辑 `references/harmonyos-rules.md`
2. 在lint.sh中添加检查逻辑

## 许可证

MIT License - 可自由用于商业和非商业项目

## 致谢

基于 [豆因DeveloperSkill-workflow](https://github.com/your-repo) v2.3 提炼优化

---

**版本**: v1.0
**更新日期**: 2026-03-20
**兼容平台**: HarmonyOS 4.0+
