# android-sharesdk-integration

一个面向 OpenClaw / ClawHub 的 Android ShareSDK 集成 Skill，采用 6 步交互式工作流程。

## 用途

当用户提到以下主题时触发：

- "我要在app中增加分享能力"
- "帮我集成ShareSDK到Android项目"
- "帮我配置微信分享"
- android sharesdk
- ShareSDK 集成
- Mob ShareSDK 接入
- ShareSDK Gradle 配置
- ShareSDK 隐私合规

## 目录结构

```
android-sharesdk-integration/
├── SKILL.md                              # 核心 Skill 定义（6步交互式工作流程）
├── REQUIRE.md                            # 平台配置字段详细说明（内部参考）
├── README.md                             # 本文件
├── examples/
│   └── example-prompts.md                # 示例触发问法
├── assets/
│   ├── ShareSDK_Config_Template.xlsx     # Excel 配置模板（供用户填写）
│   └── generate_excel_template.py        # 生成 Excel 模板的脚本
└── templates/
    └── SHARESDK_README.md                # 项目级 README 模板
```

## 6 步交互式集成工作流

本 Skill 采用交互式工作流程，每步操作前都会展示内容给用户确认：

1. **启动流程**：询问并验证项目路径
2. **注册社交平台信息**：生成 Excel 配置模板，用户填写后读取验证
3. **完成 SDK 集成**：逐个文件展示修改内容，确认后执行
4. **插入隐私授权回调**：询问回调位置，展示代码后插入
5. **插入分享代码**：收集分享需求，生成代码后插入
6. **补充说明**：生成项目级 README 文档

## 适配方向

- Android Gradle Plugin 7.0+
- Android Gradle Plugin 7.0 以下
- MobTech ShareSDK appKey / appSecret / devInfo 配置
- 首次冷启动隐私授权回传
- 一键分享面板 / 指定平台分享

## 建议放置位置

将此目录放入 OpenClaw workspace 的 `skills/` 目录中。

## 参考资料

- [Mob 文档中心](https://www.mob.com/wiki/list)
- [Mob SDK 下载中心](https://www.mob.com/download)
- [Mob SDK 合规指南](https://www.mob.com/wiki/detailed?wiki=421&id=717)
