# Viking 知识库 Python SDK 文档导引

本导引文件用于辅助用户使用 Viking 知识库 Python SDK 进行开发。
文档范围：`resources/Viking 知识库/SDK参考/Python SDK/` 目录及其子目录下的 Markdown 文档。

## 其他
- 本节将说明如何单独调用rerank模型，以计算两段文本间的相似度: [rerank 重排.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/rerank%20%E9%87%8D%E6%8E%92.md)
- 本页面提供一个通过 Python SDK 完成知识库文档导入与知识问答的完整流程请求示例，涵盖文档上传、向量检索及大模型问答调用，注意使用时根据实际情况填充账户鉴权信息、collection 名称、文档路径和查询内容。: [核心流程.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E6%A0%B8%E5%BF%83%E6%B5%81%E7%A8%8B.md)

## 切片（Point）
- add_point 用于新增知识库下文档的一个切片: [add_point.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E5%88%87%E7%89%87%EF%BC%88Point%EF%BC%89/add_point.md)
- delete_point 用于删除知识库下的某个切片: [delete_point.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E5%88%87%E7%89%87%EF%BC%88Point%EF%BC%89/delete_point.md)
- get_point 用于查看知识库下的指定切片的信息: [get_point.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E5%88%87%E7%89%87%EF%BC%88Point%EF%BC%89/get_point.md)
- list_points 用于查看知识库下的切片列表，默认按照 point_id 从小到大排序: [list_points.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E5%88%87%E7%89%87%EF%BC%88Point%EF%BC%89/list_points.md)
- update_point 用于更新知识库下的切片内容: [update_point.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E5%88%87%E7%89%87%EF%BC%88Point%EF%BC%89/update_point.md)

## 文档（Doc）
- add_doc_v2 用于向已创建的知识库添加文档。: [add_doc_v2.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E6%96%87%E6%A1%A3%EF%BC%88Doc%EF%BC%89/add_doc_v2.md)
- delete_doc 用于删除知识库下的文档: [delete_doc.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E6%96%87%E6%A1%A3%EF%BC%88Doc%EF%BC%89/delete_doc.md)
- get_doc 用于查看知识库下的文档信息。: [get_doc.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E6%96%87%E6%A1%A3%EF%BC%88Doc%EF%BC%89/get_doc.md)
- list_docs 用于查询知识库上文档的列表，默认按照文档的上传时间倒序。: [list_docs.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E6%96%87%E6%A1%A3%EF%BC%88Doc%EF%BC%89/list_docs.md)
- update_doc 用于更新某个文档信息如文档标题，文档信息更新会自动触发索引中的数据更新。: [update_doc.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E6%96%87%E6%A1%A3%EF%BC%88Doc%EF%BC%89/update_doc.md)
- update_doc_meta 用于更新知识库上文档信息，文档 meta 信息更新会自动触发索引中的数据更新。: [update_doc_meta.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E6%96%87%E6%A1%A3%EF%BC%88Doc%EF%BC%89/update_doc_meta.md)

## 知识库（Collection）
- 本节将说明如何基于多轮历史对话，使用大语言模型进行回答生成: [chat_completions（新）.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E7%9F%A5%E8%AF%86%E5%BA%93%EF%BC%88Collection%EF%BC%89/chat_completions%EF%BC%88%E6%96%B0%EF%BC%89.md)
- search_knowledge 用于对知识库进行检索和前后处理，当前会默认对原始文本加工后的知识内容进行检索。: [search_knowledge.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E7%9F%A5%E8%AF%86%E5%BA%93%EF%BC%88Collection%EF%BC%89/search_knowledge.md)
- service_chat 支持基于一个已创建的知识服务进行检索/问答。: [service_chat.md](Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/Python%20SDK/%E7%9F%A5%E8%AF%86%E5%BA%93%EF%BC%88Collection%EF%BC%89/service_chat.md)
