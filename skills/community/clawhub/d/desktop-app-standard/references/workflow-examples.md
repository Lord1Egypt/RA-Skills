# 大型桌面项目的 CI 与 Release 参考

链接固定到具体提交，用于查看实现结构；实际采用时按项目需求和所用 Action 版本适配。

| 项目 | 实际工作流 | 本技能采用的部分 |
| --- | --- | --- |
| Flow Launcher，WPF | Windows restore/build/test 后调用项目的 post_build.ps1，上传安装器、便携包、更新包和 RELEASES artifacts。release_deploy.yml 在已发布事件后更新网站和分发渠道。 | 测试与打包脚本相连，资产来自实际输出目录。 |
| Joplin，Electron | macOS M1 workflow 从 tag 设置 PUBLISH_ENABLED，分别执行构建发布和 --publish=never，并注入签名配置；存在项目自己的资产修改逻辑。 | 按平台和发布条件调用已有打包器，明确可信 tag 和 PR 的发布权限。 |
| Zettlr，Electron | 多平台构建 artifacts，单一 prepare_release 汇总并生成 SHA256；正式版使用 softprops 创建草稿，nightly 上传自有服务器。 | 构建与单一发布器的结构。本技能 Tauri 模板暂存草稿并在校验后自动公开，Electron 模板采用 draft: false，已有草稿流程按项目要求保留。 |
| Clash Verge Rev，Tauri | 多平台 tauri-action，另有批准快照、草稿准备、源码校验、通知和渠道逻辑，最后自动公开。 | 使用框架 Action 构建和生成 updater 元数据。项目特有审批流程按实际需要添加。 |
| dnSpyEx，WPF | Windows 按 framework/RID 矩阵调用 build.ps1，复制整个构建输出并上传 artifacts。 | 发布完整目录，保留资源，按支持范围设置矩阵。 |

[Flow Launcher CI](https://github.com/Flow-Launcher/Flow.Launcher/blob/ff99ea05d7ad198de6e26e2878215f7221860dac/.github/workflows/dotnet.yml) · [Flow Launcher 发布后部署](https://github.com/Flow-Launcher/Flow.Launcher/blob/ff99ea05d7ad198de6e26e2878215f7221860dac/.github/workflows/release_deploy.yml)

[Joplin macOS 构建](https://github.com/laurent22/joplin/blob/34696bc462bf9004bd7111038d83b1248ea800ca/.github/workflows/build-macos-m1.yml)

[Zettlr 工作流](https://github.com/Zettlr/Zettlr/blob/fe48751120f269e10b02d069a00ce7982a04d082/.github/workflows/build.yml)

[Clash Verge Rev 发布](https://github.com/clash-verge-rev/clash-verge-rev/blob/2c60f55f45c51200fbfa0444779e46348fdd3365/.github/workflows/release.yml)

[dnSpyEx 工作流目录](https://github.com/dnSpyEx/dnSpy/tree/304885bfc814fa0b6253c248c4e95a635b10ea17/.github/workflows)

Tauri 官方 Action 的 releaseDraft 默认 false，支持自动发布说明、原生资产上传和 latest.json 生成。模板直接使用这些能力。softprops 的 draft、文件匹配失败和 latest 参数按其当前 README 适配。[Tauri Action](https://github.com/tauri-apps/tauri-action) · [softprops Release Action](https://github.com/softprops/action-gh-release)
