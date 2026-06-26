# Android MobLink 集成 Skill

用于指导 Agent 将 MobTech MobLink 集成到 Android 项目中，覆盖 Gradle 在线集成、MobLink 后台参数配置、隐私合规、场景还原监听和 mobID 生成代码。

## 适用场景

- Android 项目需要接入 MobLink 深度链接能力
- 需要配置 `uriScheme` 和 `appLinkHost`
- 需要实现点击链接后还原业务场景
- 需要生成 mobID 并拼接到业务分享链接
- 需要按 MobTech 合规要求提交隐私授权结果

## 需要用户准备

- Android 项目根路径
- MobTech 后台获取的 `appKey` 和 `appSecret`
- Android 包名和签名 MD5
- MobLink 后台配置的 `uriScheme`
- MobLink 后台开启 AppLink 后生成的 `appLinkHost`
- 承接场景还原的 Activity
- 隐私政策同意按钮的回调位置

## 生成文件

集成流程会先执行：

```bash
python3 assets/generate_excel_template.py
```

生成：

```text
assets/MobLink_Config_Template.xlsx
```

然后复制到用户 Android 项目根目录并命名为：

```text
MobLink_Config.xlsx
```

用户填写完成后，Agent 读取该 Excel 并继续后续集成。

## 官方文档

- 文档入口：https://www.mob.com/wiki/detailed?wiki=661&id=34
- Android 集成指南：https://www.mob.com/wiki/detailed?wiki=115&id=34
- Android SDK API：https://www.mob.com/wiki/detailed?wiki=116&id=34
- Android 合规指南：https://www.mob.com/wiki/detailed?wiki=222&id=34
- 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=660&id=34

## 维护注意

- `SKILL.md` 是 Agent 执行流程，README 只做说明。
- Excel 模板字段变更时，需要同步更新 `SKILL.md` 的验证规则。
- `generate_excel_template.py` 必须使用基于脚本目录的相对输出路径。
- 不要在 skill 中写死本机绝对路径或真实用户密钥。
