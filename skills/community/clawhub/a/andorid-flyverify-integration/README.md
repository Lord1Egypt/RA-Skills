# android-flyverify-integration

一个面向 OpenClaw / ClawHub 的 Android FlyVerify (秒验) 集成 Skill，采用 5 步交互式工作流程。

## 用途

当用户提到以下主题时触发：

- "我要在app中增加一键登录"
- "帮我集成 FlyVerify 到 Android 项目"
- "帮我配置一键登录"
- android flyverify
- 秒验集成
- FlyVerify 一键登录 SDK 接入
- FlyVerify Gradle 配置
- FlyVerify 隐私合规

## 目录结构

```
android-flyverify-integration/
├── SKILL.md                              # 核心 Skill 定义（5步交互式工作流程）
├── README.md                             # 本文件
├── assets/
│   ├── FlyVerify_Config_Template.xlsx    # Excel 配置模板（供用户填写）
│   └── generate_excel_template.py        # 生成 Excel 模板的脚本
└── examples/
    └── example-prompts.md                # 示例触发问法
```

## 5 步交互式集成工作流

本 Skill 采用交互式工作流程，每步操作前都会展示内容给用户确认：

1. **启动流程**：询问并验证项目路径
2. **注册配置信息**：生成 Excel 配置模板，用户填写后读取验证
3. **完成 SDK 集成**：逐个文件展示修改内容，确认后执行
4. **配置权限和组件**：展示并添加 AndroidManifest.xml 配置
5. **补充说明**：插入隐私授权代码，生成项目级 README 文档

## 支持功能

- Android Gradle Plugin 7.0+
- Android Gradle Plugin 7.0 以下
- MobTech FlyVerify appKey / appSecret 配置
- 首次冷启动隐私授权回传
- 预取号接口调用
- 一键验证/登录流程
- 自定义 UI 配置（竖屏/横屏）
- 秒验审核提醒

## 重要提醒

- **秒验审核必需**：必须在 MobTech 后台提交秒验审核并通过后才能正常使用
- **移动网络必需**：秒验必须在手机开启移动蜂窝网络的前提下才能成功取号
- **运营商支持**：仅支持中国移动、联通、电信三大运营商

## 建议放置位置

将此目录放入 OpenClaw workspace 的 `skills/` 目录中。

## 参考资料

- [Mob 文档中心](https://www.mob.com/wiki/list)
- [秒验集成指南](https://www.mob.com/wiki/detailed?wiki=551&id=78)
- [SDK API 文档](https://www.mob.com/wiki/detailed?wiki=297&id=78)
- [Mob SDK 合规指南](https://www.mob.com/wiki/detailed?wiki=421&id=717)
