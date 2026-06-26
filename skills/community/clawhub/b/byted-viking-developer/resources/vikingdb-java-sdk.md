# VikingDB 向量库 Java SDK 文档导引

本导引文件用于辅助用户使用 VikingDB 向量库 Java SDK（V2）进行开发。
文档范围：`resources/VikingDB 向量库/SDK V2参考/Java SDK/` 目录及其子目录下的 Markdown 文档。

## 其他
- 向量数据库 Viking DB 支持通过 Java SDK 操作数据库。: [安装与client初始化.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E5%AE%89%E8%A3%85%E4%B8%8Eclient%E5%88%9D%E5%A7%8B%E5%8C%96.md)

## 控制面SDK / 任务(Task)
- 删除指定的任务，删除后任务将终止: [deleteVikingdbTask.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/deleteVikingdbTask.md)
- 查询指定 task 的详情信息和执行进度: [getVikingdbTask.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/getVikingdbTask.md)
- 获取多个task的信息，最多一次性展示20条: [listVikingdbTask.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/listVikingdbTask.md)
- 更新指定的任务，当前任务更新只用于**删除**任务的人工确认 环节: [updateVikingdbTask.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/updateVikingdbTask.md)

## 控制面SDK / 任务(Task) / createVikingdbTask
- 按特定条件批量导出Collection中的数据: [DataExport.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/createVikingdbTask/DataExport.md)
- 将 数据导入到 Collection 中，要求文件的列名必须和 Collection fields 重合，否则会解析失败: [DataImport.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/createVikingdbTask/DataImport.md)
- 按特定条件批量删除Collection中的数据: [FilterDelete.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/createVikingdbTask/FilterDelete.md)
- 按特定条件批量更新数据，不支持vector、sparse_vector、text 类型字段的更新: [FilterUpdate.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E4%BB%BB%E5%8A%A1%28Task%29/createVikingdbTask/FilterUpdate.md)

## 控制面SDK / 数据集(collection)
- 接口用于对向量数据库的创建，单账号下最多创建200个数据集。: [createVikingdbCollection.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%E9%9B%86%28collection%29/createVikingdbCollection.md)
- DeleteCollection 用于删除已创建的数据集 Collection。: [deleteVikingdbCollection.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%E9%9B%86%28collection%29/deleteVikingdbCollection.md)
- getCollection 用于查询指定数据集 Collection 的详情信息。: [getVikingdbCollection.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%E9%9B%86%28collection%29/getVikingdbCollection.md)
- listCollections 用于查询数据集 Collection 列表。: [listVikingdbCollection.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%E9%9B%86%28collection%29/listVikingdbCollection.md)
- updateCollection 用于为指定数据集 Collection 增加字段。: [updateVikingdbCollection.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%E9%9B%86%28collection%29/updateVikingdbCollection.md)

## 控制面SDK / 索引(Index)
- createIndex 用于为指定的数据集 Collection 创建索引 Index。: [createVikingdbIndex.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E7%B4%A2%E5%BC%95%28Index%29/createVikingdbIndex.md)
- DeleteIndex 用于删除指定数据集 Collection 的指定索引 Index。: [deleteVikingdbIndex.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E7%B4%A2%E5%BC%95%28Index%29/deleteVikingdbIndex.md)
- getIndex 用于查询索引 Index 详情。: [getVikingdbIndex.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E7%B4%A2%E5%BC%95%28Index%29/getVikingdbIndex.md)
- listIndexes 用于查询和数据集 Collection 关联的索引 Index列表。: [listVikingdbIndex.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E7%B4%A2%E5%BC%95%28Index%29/listVikingdbIndex.md)
- updateIndex 接口用于更新指定 Index 的描述、cpuQuota、scalarIndex。: [updateVikingdbIndex.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%8E%A7%E5%88%B6%E9%9D%A2SDK/%E7%B4%A2%E5%BC%95%28Index%29/updateVikingdbIndex.md)

## 数据面SDK
- 聚合统计能指定字段进行分组聚合，并可添加过滤操作，最终得到相应的聚合统计结果，辅助了解数据分布等情况。: [aggregate.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/aggregate.md)
- embedding 用于将非结构化数据向量化，通过深度学习神经网络提取文本、图片、音视频等非结构化数据里的内容和语义，把文本、图片、音视频等变成特征向量。: [embedding.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/embedding.md)

## 数据面SDK / 数据(Data)
- deleteData 用于在指定的 Collection 删除数据，根据主键删除单条或多条数据，单次最多允许删除100条数据。: [deleteData.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%28Data%29/deleteData.md)
- 根据主键在指定的 Collection 中查询单条或多条数据，单次最多可查询100条数据。: [fetchDataInCollection.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%28Data%29/fetchDataInCollection.md)
- fetchData 用于 Index 数据查询。: [fetchDataInIndex.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%28Data%29/fetchDataInIndex.md)
- updateData 用于为已存在数据的部分字段进行更新。: [updateData.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%28Data%29/updateData.md)
- 接口用于在指定的数据集 Collection 内写入数据。: [upsertData.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%95%B0%E6%8D%AE%28Data%29/upsertData.md)

## 数据面SDK / 检索(Search)
- searchById 用于主键 id 检索。: [searchById.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/searchById.md)
- SearchByKeywords 用于关键词检索，适用于带有text字段向量化配置（vectorize参数）的索引，支持多个关键词的检索。: [searchByKeywords.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/searchByKeywords.md)
- searchWithMultiModal 用于多模态数据检索。: [searchByMultiModal.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/searchByMultiModal.md)
- 随机检索是一种在未指定查询内容的情况下，从数据集中随机返回若干条记录的检索方式。: [searchByRandom.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/searchByRandom.md)
- 接口适用于含有int64/float32类型标量索引字段的索引。: [searchByScalar.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/searchByScalar.md)
- searchByVector 用于向量检索。: [searchByVector.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/searchByVector.md)
- 检索功能包括多个接口组成，分别对应不同的检索模式和业务场景。: [检索公共参数.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/%E6%A3%80%E7%B4%A2%E5%85%AC%E5%85%B1%E5%8F%82%E6%95%B0.md)
- **当前检索能力在检索范式中的定位：**: [检索后处理算子-PostProcess.md](VikingDB%20%E5%90%91%E9%87%8F%E5%BA%93/SDK%20V2%E5%8F%82%E8%80%83/Java%20SDK/%E6%95%B0%E6%8D%AE%E9%9D%A2SDK/%E6%A3%80%E7%B4%A2%28Search%29/%E6%A3%80%E7%B4%A2%E5%90%8E%E5%A4%84%E7%90%86%E7%AE%97%E5%AD%90-PostProcess.md)
