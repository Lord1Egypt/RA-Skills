# Viking 记忆库最佳实践导引

本导引文件用于汇总 Viking 记忆库在业务落地中的最佳实践与方案示例。
文档范围：`resources/Viking 记忆库/最佳实践/` 目录及其子目录下的 Markdown 文档。

## 其他
- 本章将以火山引擎“豆包大模型”为例，向您展示如何将记忆库与大模型相结合，构建一个具备长期记忆能力的对话式AI。: [串联大模型最佳实践.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E4%B8%B2%E8%81%94%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5.md)
- **为什么需要算子？**: [使用记忆库算子实现画像精准抽取.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E4%BD%BF%E7%94%A8%E8%AE%B0%E5%BF%86%E5%BA%93%E7%AE%97%E5%AD%90%E5%AE%9E%E7%8E%B0%E7%94%BB%E5%83%8F%E7%B2%BE%E5%87%86%E6%8A%BD%E5%8F%96.md)
- 为何需要图文记忆库: [图文记忆库最佳实践.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E5%9B%BE%E6%96%87%E8%AE%B0%E5%BF%86%E5%BA%93%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5.md)
- 实时写入数据+获取上下文接口使用指南: [实时写入数据+获取上下文接口使用指南.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E5%AE%9E%E6%97%B6%E5%86%99%E5%85%A5%E6%95%B0%E6%8D%AE%2B%E8%8E%B7%E5%8F%96%E4%B8%8A%E4%B8%8B%E6%96%87%E6%8E%A5%E5%8F%A3%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)
- 本章将详细描述如何在 RTC 的实时对话式 AI 中，使用 Viking 长期记忆 和 Viking 知识库。: [打通 RTC 服务，在实时对话式 AI 中使用 Viking 长期记忆和知识库.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E6%89%93%E9%80%9A%20RTC%20%E6%9C%8D%E5%8A%A1%EF%BC%8C%E5%9C%A8%E5%AE%9E%E6%97%B6%E5%AF%B9%E8%AF%9D%E5%BC%8F%20AI%20%E4%B8%AD%E4%BD%BF%E7%94%A8%20Viking%20%E9%95%BF%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%92%8C%E7%9F%A5%E8%AF%86%E5%BA%93.md)
- 本文介绍如何使用 **时间压缩算子（TIME_COMPRESS）** 实现记忆的时间分层管理，使系统能够根据时间范围自动调整记忆粒度，保持近期记忆清晰、长期记忆简化。: [时间压缩算子：实现记忆随时间自动模糊.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E6%97%B6%E9%97%B4%E5%8E%8B%E7%BC%A9%E7%AE%97%E5%AD%90%EF%BC%9A%E5%AE%9E%E7%8E%B0%E8%AE%B0%E5%BF%86%E9%9A%8F%E6%97%B6%E9%97%B4%E8%87%AA%E5%8A%A8%E6%A8%A1%E7%B3%8A.md)
- 在AddSession接口中，有一个可选字段profiles，其作用是定义需要特别关注或更新的画像信息列表。: [添加 Session 时指定画像更新范围，实现画像的准确更新.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E6%B7%BB%E5%8A%A0%20Session%20%E6%97%B6%E6%8C%87%E5%AE%9A%E7%94%BB%E5%83%8F%E6%9B%B4%E6%96%B0%E8%8C%83%E5%9B%B4%EF%BC%8C%E5%AE%9E%E7%8E%B0%E7%94%BB%E5%83%8F%E7%9A%84%E5%87%86%E7%A1%AE%E6%9B%B4%E6%96%B0.md)
- 记忆更新时机和记忆更新方式怎么配置？: [画像记忆更新时机和更新方式配置示例.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E7%94%BB%E5%83%8F%E8%AE%B0%E5%BF%86%E6%9B%B4%E6%96%B0%E6%97%B6%E6%9C%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E6%96%B9%E5%BC%8F%E9%85%8D%E7%BD%AE%E7%A4%BA%E4%BE%8B.md)
- 为什么要自定义事件记忆权重: [自定义事件记忆权重，让记忆检索更懂业务.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E8%87%AA%E5%AE%9A%E4%B9%89%E4%BA%8B%E4%BB%B6%E8%AE%B0%E5%BF%86%E6%9D%83%E9%87%8D%EF%BC%8C%E8%AE%A9%E8%AE%B0%E5%BF%86%E6%A3%80%E7%B4%A2%E6%9B%B4%E6%87%82%E4%B8%9A%E5%8A%A1.md)
- 记忆库 TTL 设置与清理最佳实践: [记忆库 TTL 设置与清理最佳实践.md](Viking%20%E8%AE%B0%E5%BF%86%E5%BA%93/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/%E8%AE%B0%E5%BF%86%E5%BA%93%20TTL%20%E8%AE%BE%E7%BD%AE%E4%B8%8E%E6%B8%85%E7%90%86%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5.md)
