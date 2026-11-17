# Release workflow 适配与验收

默认直接公开。先确认应用、包管理器、锁文件、工作目录、版本源、平台/架构、构建测试命令和签名配置，再选择对应栈模板。

| 栈 | 推荐流程 |
| --- | --- |
| Tauri | 校验测试 → 官方 tauri-action 矩阵暂存草稿 → 检查 updater 平台覆盖与摘要 → 自动公开。 |
| Electron | 校验测试 → 平台构建 artifacts → 单一 job 检查本地清单/摘要并直接 Release。 |
| WPF | Windows 测试 → 发布 profile、签名、安装器、ZIP 解包 smoke → 直接 Release。 |

1. 按实际路径和脚本适配缓存、安装、构建和资产 glob。PR 只读，可信 tag job 才注入写令牌与签名凭据。
2. 检查 tag 与版本一致，测试和发布使用同一源码提交。required checks 包含应用承诺的测试。
3. Electron/WPF 校验后直接发布；Tauri 用 releaseDraft: true 暂存，完整校验后自动公开。人工审批、attestation、SBOM、构建证据仅在项目明确需要时配置。
4. 保留 updater 对应的所有载体、签名和元数据；Electron 检查最终资产名与清单 URL/SHA-512，Tauri 使用官方 Action 生成清单。
5. 发布说明列出实际平台、下载选择、签名状态与校验入口。稳定版与预发布的 channel 分别测试。
6. 验证重跑、缺文件、错误哈希及测试失败；随后按授权验证公开下载和 N→N+1 更新。记录实际执行和缺少的 runner/设备。

多应用 release hub、immutable releases 和原生模块交叉架构按项目真实约束适配。已有可用的 workflow 可以沿用。

涉及包型、更新缓存、资产 readiness 或 winget 时，按[发布流程](../references/release-flow.md)选择对应检查。交付引用实际入口和验证结果，复用已有项目记录。
