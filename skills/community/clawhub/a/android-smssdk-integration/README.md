# android-smssdk-integration

一个面向 OpenClaw / ClawHub 的 Android SMSSDK (短信验证) 集成 Skill，采用交互式工作流程。

## 用途

当用户提到以下主题时触发：

- 我要在app中增加短信验证
- 帮我集成 SMSSDK 到 Android 项目
- 帮我配置短信验证
- android smssdk
- SMSSDK 集成
- 短信验证码
- MobSDK 短信功能接入

## 目录结构

```
android-smssdk-integration/
├── SKILL.md                              # 核心 Skill 定义（交互式工作流程）
├── README.md                             # 本文件
├── assets/
│   └── generate_excel_template.py        # 生成 Excel 模板的脚本
└── examples/
    └── example-prompts.md                # 示例触发问法
```

## 交互式集成工作流

本 Skill 采用交互式工作流程，每步操作前都会展示内容给用户确认：

1. **启动流程**：询问并验证项目路径
2. **获取配置信息**：引导用户从 MobTech 后台获取 AppKey / AppSecret
3. **完成 Gradle 集成**：逐个文件展示修改内容，确认后执行
4. **配置隐私合规**：插入隐私授权代码
5. **完成集成**：生成项目级 README 文档

## 支持功能

- Android Gradle Plugin 7.0+
- Android Gradle Plugin 7.0 以下
- MobSDK 插件集成
- SMSSDK AppKey / AppSecret 配置
- 首次冷启动隐私授权回传
- Google Play 版本配置（GPP）
- 短信验证码 API 调用示例

## 重要提醒

- **工信部合规必需**：用户同意隐私协议后才能调用 `MobSDK.submitPolicyGrantResult()`
- **minSdkVersion 19**：最低支持 Android 5.0
- **MobTech 后台配置**：确保包名与后台配置一致

## 建议放置位置

将此目录放入 OpenClaw workspace 的 `skills/` 目录中。

## 参考资料

- [Mob 文档中心](https://www.mob.com/wiki/list)
- [产品简介](https://mob.com/wiki/detailed?wiki=163&id=23)
- [短信验证集成指南](https://mob.com/wiki/detailed?wiki=440&id=23)
- [SDK API](https://mob.com/wiki/detailed?wiki=440&id=23)
- [服务端验证 API](https://mob.com/wiki/detailed?wiki=112&id=23)
- [短信设置](https://mob.com/wiki/detailed?wiki=452&id=23)
- [合规指南](https://mob.com/wiki/detailed?wiki=210&id=23)
- [常见问题](https://mob.com/wiki/detailed?wiki=123&id=23)
- [关于短信签名申请规则更新的公告](https://mob.com/wiki/detailed?wiki=732&id=23)
