---
name: codex-delete-republish-test
version: 0.0.1
description: 验证 ClawHub 删除后是否允许同 slug 重新发布的测试技能。
license: MIT
author: davidme6
---

# Delete Republish Test

这个技能只用于验证 ClawHub 的一个发布行为：
- 先发布一个技能
- 删除这条技能
- 再用同一个 slug 重新发布

## 作用

- 观察删除后的 slug 是否立即可复用
- 观察旧 tag 和旧版本映射是否会被清空
- 评估是否可以用同样的方式重建真实技能

## 预期

如果平台允许同 slug 重建，那么删除之后应该可以重新发布成功。
如果平台不允许，那么会返回 slug 冲突或重定向相关错误。
