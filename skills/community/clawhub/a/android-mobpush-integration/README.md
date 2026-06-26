# android-mobpush-integration

一个面向 OpenClaw / ClawHub 的 Android MobPush 集成 Skill，采用 6 步交互式工作流程。

## 用途

当用户提到以下主题时触发：

- "我要在app中增加推送能力"
- "帮我集成 MobPush 到 Android 项目"
- "帮我配置推送通知"
- android mobpush
- MobPush 集成
- MobPush 推送 SDK 接入
- MobPush Gradle 配置
- MobPush 隐私合规
- 厂商通道配置（小米、华为、OPPO、vivo、魅族、荣耀、FCM）

## 目录结构

```
android-mobpush-integration/
├── SKILL.md                              # 核心 Skill 定义（6步交互式工作流程）
├── README.md                             # 本文件
├── assets/
│   ├── MobPush_Config_Template.xlsx      # Excel 配置模板（供用户填写）
│   └── generate_excel_template.py        # 生成 Excel 模板的脚本
└── examples/
    └── example-prompts.md                # 示例触发问法
```

## 6 步交互式集成工作流

本 Skill 采用交互式工作流程，每步操作前都会展示内容给用户确认：

1. **启动流程**：询问并验证项目路径
2. **注册配置信息**：生成 Excel 配置模板，用户填写后读取验证
3. **完成 SDK 集成**：包含项目级 Gradle 配置、应用级 build.gradle 配置、gradle.properties 版本选择、混淆规则添加及 Gradle Sync
4. **配置权限**：展示并添加 AndroidManifest.xml 权限
5. **插入隐私授权回调**：询问回调位置，展示代码后插入
6. **补充说明**：生成项目级 README 文档

## 支持功能

- Android Gradle Plugin 7.0+
- Android Gradle Plugin 7.0 以下
- MobTech MobPush appKey / appSecret 配置
- 7 种厂商通道配置（华为、小米、OPPO、vivo、魅族、荣耀、FCM）
- 首次冷启动隐私授权回传
- 推送消息接收处理
- 别名与标签管理

## 建议放置位置

将此目录放入 OpenClaw workspace 的 `skills/` 目录中。

## 参考资料

- [Mob 文档中心](https://www.mob.com/wiki/list)
- [MobPush 集成指南](https://www.mob.com/wiki/detailed?wiki=498&id=136)
- [厂商通道配置](https://www.mob.com/wiki/detailed?wiki=517&id=136)
- [Mob SDK 合规指南](https://www.mob.com/wiki/detailed?wiki=421&id=717)
