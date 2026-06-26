# Viking 记忆库 Python SDK 文档导引

本导引文件用于辅助用户使用 Viking 记忆库 Python SDK 进行开发。
文档范围：`resources/Viking 记忆库/SDK参考/` 目录及其子目录下的 Markdown 文档。

## 其他
- Viking 长期记忆支持通过 Python SDK 操作记忆库，Python SDK 提供了高层次的抽象和易于使用的接口，简化开发人员的工作。: [安装与初始化.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E5%AE%89%E8%A3%85%E4%B8%8E%E5%88%9D%E5%A7%8B%E5%8C%96.md)
- 本页面提供一个通过 Python SDK 初始化记忆库、写入数据和检索记忆的完整请求示例。: [核心流程.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E6%A0%B8%E5%BF%83%E6%B5%81%E7%A8%8B.md)

## 会话管理
- 接口概述: [添加会话-AddSession.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E4%BC%9A%E8%AF%9D%E7%AE%A1%E7%90%86/%E6%B7%BB%E5%8A%A0%E4%BC%9A%E8%AF%9D-AddSession.md)
- 接口概述: [获取会话详情-SessionInfo.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E4%BC%9A%E8%AF%9D%E7%AE%A1%E7%90%86/%E8%8E%B7%E5%8F%96%E4%BC%9A%E8%AF%9D%E8%AF%A6%E6%83%85-SessionInfo.md)

## 记忆库
- 接口概述: [创建记忆库-CreateCollection.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E5%BA%93/%E5%88%9B%E5%BB%BA%E8%AE%B0%E5%BF%86%E5%BA%93-CreateCollection.md)
- 接口概述: [删除记忆库-DeleteCollection.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E5%BA%93/%E5%88%A0%E9%99%A4%E8%AE%B0%E5%BF%86%E5%BA%93-DeleteCollection.md)
- 接口概述: [更新记忆库-UpdateCollection.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9B%B4%E6%96%B0%E8%AE%B0%E5%BF%86%E5%BA%93-UpdateCollection.md)
- 接口概述: [查看记忆库列表-ListCollection.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9F%A5%E7%9C%8B%E8%AE%B0%E5%BF%86%E5%BA%93%E5%88%97%E8%A1%A8-ListCollection.md)
- 接口概述: [获取记忆库详情-CollectionInfo.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E5%BA%93/%E8%8E%B7%E5%8F%96%E8%AE%B0%E5%BF%86%E5%BA%93%E8%AF%A6%E6%83%85-CollectionInfo.md)

## 记忆检索
- 接口概述: [搜索事件记忆-SearchEventMemory.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E6%A3%80%E7%B4%A2/%E6%90%9C%E7%B4%A2%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86-SearchEventMemory.md)
- 接口概述: [搜索画像记忆-SearchProfileMemory.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E6%A3%80%E7%B4%A2/%E6%90%9C%E7%B4%A2%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86-SearchProfileMemory.md)
- 接口概述: [搜索记忆-SearchMemory.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E6%A3%80%E7%B4%A2/%E6%90%9C%E7%B4%A2%E8%AE%B0%E5%BF%86-SearchMemory.md)

## 记忆管理 / 事件记忆
- 用于单条删除已写入记忆库的事件记忆。: [删除事件记忆-DeleteEvent.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86/%E5%88%A0%E9%99%A4%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86-DeleteEvent.md)
- 用于批量删除已写入记忆库的事件记忆。: [批量删除事件记忆-BatchDeleteEvent.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86/%E6%89%B9%E9%87%8F%E5%88%A0%E9%99%A4%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86-BatchDeleteEvent.md)
- 用于更新已写入记忆库的事件记忆。: [更新事件记忆-UpdateEvent.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86/%E6%9B%B4%E6%96%B0%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86-UpdateEvent.md)
- 用于添加事件记忆。: [添加事件记忆-AddEvent.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86/%E6%B7%BB%E5%8A%A0%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86-AddEvent.md)

## 记忆管理 / 画像记忆
- 用于单条删除已写入记忆库的画像记忆。: [删除画像记忆-DeleteProfile.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86/%E5%88%A0%E9%99%A4%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86-DeleteProfile.md)
- 用于手动触发画像记忆的更新。: [手动触发画像记忆更新-TriggerUpdateProfile.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86/%E6%89%8B%E5%8A%A8%E8%A7%A6%E5%8F%91%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86%E6%9B%B4%E6%96%B0-TriggerUpdateProfile.md)
- 用于批量删除已写入记忆库的画像记忆。: [批量删除画像记忆-BatchDeleteProfile.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86/%E6%89%B9%E9%87%8F%E5%88%A0%E9%99%A4%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86-BatchDeleteProfile.md)
- 用于更新已写入库的画像记忆。: [更新画像记忆-UpdateProfile.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86/%E6%9B%B4%E6%96%B0%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86-UpdateProfile.md)
- 用于添加画像记忆。: [添加画像记忆-AddProfile.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86/%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86/%E6%B7%BB%E5%8A%A0%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86-AddProfile.md)
