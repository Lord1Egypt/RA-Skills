# MobLink 集成说明

本文档由 MobLink 集成 skill 生成，用于记录当前项目的 MobLink 接入信息。

## 已完成配置

- MobSDK Maven 仓库：`https://mvn.mob.com/android`
- MobSDK Gradle 插件：`com.mob.sdk:MobSDK2:+`
- MobLink 配置块：`MobSDK { MobLink { ... } }`
- 隐私授权提交：`MobSDK.submitPolicyGrantResult(...)`
- 场景还原监听：`MobLink.setRestoreSceneListener(...)`
- 场景还原 Activity：`SceneRestorable`

## 关键参数

- appKey：`{appKey}`
- appSecret：已配置，勿在文档中明文扩散
- uriScheme：`{uriScheme}`
- appLinkHost：`{appLinkHost}`
- 默认场景路径：`{defaultScenePath}`
- 承接 Activity：`{restoreActivity}`
- spEdition：`{spEdition}`

## 后续维护

1. 如需新增业务场景，创建新的 `Scene` 并设置 `path` 与 `params`。
2. 使用 `MobLink.getMobID(scene, listener)` 获取 mobID 后拼接到业务链接。
3. 在承接 Activity 的 `onReturnSceneData(Scene scene)` 中解析参数并跳转业务页面。
4. Activity 需要重写 `onNewIntent` 并调用 `MobLink.updateNewIntent(getIntent(), this)`。
5. 隐私政策变更时，同步确认 `MobSDK.submitPolicyGrantResult(...)` 的调用时机仍在用户授权之后。

## 官方文档

- Android 集成指南：https://www.mob.com/wiki/detailed?wiki=115&id=34
- Android SDK API：https://www.mob.com/wiki/detailed?wiki=116&id=34
- Android 合规指南：https://www.mob.com/wiki/detailed?wiki=222&id=34
- 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=660&id=34
