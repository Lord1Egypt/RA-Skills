# 依赖升级工作流

## 升级类型

| 类型 | 示例 | 验证 |
| ---- | ---- | ---- |
| 安全补丁 | 传递依赖 CVE、patch 版本 | 安装、audit、目标测试 |
| 小版本升级 | 兼容性功能版本 | typecheck、测试、构建 |
| 大版本迁移 | React/Vue/Next/Vite/Storybook 大版本 | 迁移指南、完整验证矩阵 |
| 工具链切换 | ESLint、TypeScript、bundler、test runner | 配置 diff、CI 对齐、样例失败 |
| 清理 | 移除未使用包 | 引用搜索、构建、测试 |

## 来源检查清单

- 官方 release notes 或 migration guide。
- 包管理器兼容性和 lockfile 格式。
- Node 版本和浏览器支持范围。
- Peer dependency 版本范围。
- ESM/CJS 导出变化。
- TypeScript 最低版本和类型变化。
- SSR、RSC、edge runtime 或 browser-only 约束。

## 分批策略

- 框架大版本升级与样式、测试、lint 升级分开处理。
- 当 peer 版本范围要求时，adapter 与宿主工具放在同一批升级。
- Monorepo 中要验证受影响包，并至少验证一个消费这些包的应用。
- 每个成功批次都记录通过的命令，必要时单独提交或单独报告。

## 失败分诊

1. 复现最小失败命令。
2. 判断失败属于配置、类型表面、运行时行为还是 peer dependency。
3. 优先采用官方迁移步骤，而不是本地临时 hack。
4. 如果某个包阻塞当前批次，先 pin 住并记录原因；只有剩余批次仍然自洽时才继续。

## 报告模板

```markdown
## 依赖升级摘要

| 包 | 从 | 到 | 原因 | 风险 | 依据 |
| -- | -- | -- | ---- | ---- | ---- |

## 验证

- install:
- typecheck:
- test:
- build:
- e2e/storybook/manual:

## 剩余风险

- ...
```
