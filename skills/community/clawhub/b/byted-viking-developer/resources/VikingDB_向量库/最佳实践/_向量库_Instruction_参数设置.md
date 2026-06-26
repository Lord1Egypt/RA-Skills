
向量库新版本（V2）中：

* 若您通过VikingDB在写入和检索时自动向量化，则无需单独配置instruction， [CreateVikingCollection](https://www.volcengine.com/docs/84313/1791154?lang=zh) 接口和 [SearchByMultimodel](https://www.volcengine.com/docs/84313/1791135?lang=zh) 接口已提供默认参数配置 instruction 内容；
* 若用户有额外配置需求，可使用 [向量化计算(Embedding)](https://www.volcengine.com/docs/84313/1791161?lang=zh) 接口对 instruction参数进行自定义配置，再通过VikingDB写入和检索向量数据。

## 设置 instruction 字段
instructions 字段是影响模型效果的关键。为了显著提升向量表示的精度，您需要根据具体的业务场景来定制该指令。**请勿直接使用系统默认值。**
通过合理设置 instructions，您可以引导模型更准确地聚焦输入内容的关键信息，从而适配特定的任务需求。这在跨模态检索、特定领域数据处理等场景中尤其有效。
> 注意：仅 doubao-embedding-vision-251215 及后续版本支持 instruction 字段。

### **配置规则**
构建指令前需明确两种核心角色，二者在不同任务中的配置规则差异显著：

* **Query（查询侧）**：发起检索 / 查询的主体，如用户输入的问题、检索关键词、待匹配的图片/视频等。
* **Corpus（语料侧）**：被查询的对象，如文档库、图片库、视频库中的单条数据样本。

根据任务类型不同，Instruction 字段分为 **召回 / 排序类** 和 **聚类 / 分类 / 语义文本相似度（STS）类** 两大场景，具体配置模板如下表：
| 任务类型 | 是否区分 Query/Corpus | 核心配置模板 |
| --- | --- | --- |
| 召回、排序类 | 是 | Query：Target_modality: {}.\nInstruction:{}\nQuery: <br> Corpus：Instruction:Compress the {} into one word.\nQuery: |
| 聚类、分类、STS 类 | 否 | 所有数据：Target_modality: {}.\nInstruction:{}\nQuery: |
**通用要求**：所有模板仅需填充 {} 部分，其余固定内容**禁止修改**。
### 召回、排序类任务配置规则
此类任务用于根据 Query 计算与 Corpus 的相似度，实现目标内容的召回或排序，Query 和 Corpus 需分别配置 Instruction。
#### **Query 侧配置**
```Plain Text
Target_modality: {}.\nInstruction:{}\nQuery:
```

**字段填写说明**

1. **Target_modality 填充规则**
   * 填写依据：**与 Query 自身模态无关**，完全取决于待召回的 **Corpus 底库的模态类型**。
   * 多模态混合场景：若 Corpus 库中存在多种独立模态样本（如部分为 text、部分为 image、部分为 video、部分为 text and video），需用 / 分隔所有模态；若 Corpus 库中每条样本均包含多种模态（如每条样本都有 text + video），则用 and 连接。
   * 常见示例

| Corpus 库模态情况 | Target_modality 填写值 |
| --- | --- |
| 所有样本均为纯文本 | text |
| 所有样本均为图片 + 文本组合 | text and image |
| 所有样本均为纯视频 | video |
| 所有样本均为文本 + 视频组合 | text and video |
| 样本包含 text、image、video 三类 | text/image/video |
| 样本包含 text、video、text and video 三类 | text/video/text and video |
注意
Target_modality的填写错误会直接导致检索精度下降，请严格匹配 Corpus 库或数据集的模态。

2. **Instruction 填充规则**
   * 核心原则：**禁止使用默认值** **Compress the text into one word**，需根据业务场景定制。
   * 推荐示例
      * 文本检索：为这个句子生成表示以用于检索相关文章
      * 跨模态问答：根据这个问题，找到能回答这个问题的相应文本或图片

#### Corpus 侧配置
```Plain Text
Instruction:Compress the {} into one word.\nQuery:
```

**字段填写说明**

* 填充依据：仅需匹配 **当前单条 Corpus 数据的模态**，无需考虑整个 Corpus 库的模态分布。
* 常见示例：text、image、video、text and image、text and video、image and video

### 聚类、分类、STS 类任务配置规则
此类任务不区分 Query 和 Corpus，所有数据采用**完全相同**的 Instruction 配置。
```Plain Text
Target_modality: {}.\nInstruction:{}\nQuery:
```

**字段填写说明**

1. **Target_modality 填充规则**
   * 填写依据：**整个数据集的统一模态类型**，所有数据的该字段值保持一致。
   * 填写格式：与召回类任务的 Target_modality 格式一致（单模态填对应值，多模态组合用 and）。
2. **Instruction 填充规则**
   * 核心原则：**禁止使用默认值**，需贴合具体任务场景。
   * 典型示例
      * STS 语义相似度任务：Retrieve semantically similar text

### 高级用法
若上述指令无法满足需求，可以参考 MTEB (Massive Text Embedding Benchmark) 提供的 [示例](https://github.com/embeddings-benchmark/mteb/blob/main/mteb/models/model_implementations/seed_1_6_embedding_models.py#L333) 指令进行尝试。
### 典型场景配置示例
#### 纯文本任务
##### 场景 1：对称检索（STS 语义相似度匹配）

* **场景描述**：检索语义相似句子，如对比 “一只熊猫正从滑梯上滑下来” 和 “熊猫从滑梯上滑下来”。
* **配置规则**：两条样本的 Instruction 完全一致。
* **Instruction 字段示例**

```Plain Text
Target_modality: text.\nInstruction:Retrieve semantically similar text\nQuery:
```


* **Input 字段**：填写样本正文（如上述两个句子）。

##### 场景 2：非对称检索（问答、摘要搜全文）

* **场景描述**：用短 Query（问题 / 摘要）检索长 Corpus（答案 / 全文）。
* **配置示例**

| 角色 | Instruction 字段配置 |
| --- | --- |
| Query | Target_modality: text.\nInstruction:为这个句子生成表示以用于检索相关文章\nQuery: |
| Corpus | Instruction:Compress the text into one word.\nQuery: |
#### 多模态任务
##### 场景 1：对称检索（文 / 图 / 视频互搜）

* **通用前提**：当文本为图片 / 视频的**完整描述**时（例如“蓝色的天空下，一只狗在草坪上奔跑，草坪上还有一些帐篷”），可使用默认指令配置。
* **配置示例**

| 检索类型 | Query 侧 Instruction 配置 | Corpus 侧 Instruction 配置 |
| --- | --- | --- |
| 文搜图 | Target_modality: image.\nInstruction:Compress the text into one word.\nQuery: | Instruction:Compress the image into one word.\nQuery: |
| 文搜视频 | Target_modality: video.\nInstruction:Compress the text into one word.\nQuery: | Instruction:Compress the video into one word.\nQuery: |
| 图搜文 | Target_modality: text.\nInstruction:Compress the image into one word.\nQuery: | Instruction:Compress the text into one word.\nQuery: |
| 视频搜文 | Target_modality: text.\nInstruction:Compress the video into one word.\nQuery: | Instruction:Compress the text into one word.\nQuery: |
| 图搜图（整体内容匹配） | Target_modality: image.\nInstruction:Compress the image into one word.\nQuery: | Instruction:Compress the image into one word.\nQuery: |

* **特殊提示**：若 Query 为**短词文搜图**（如 “蓝色海景”），建议替换 Query 侧 Instruction 为：Find me an everyday image that matches the given caption。
* **注意**：图片局部截取检索原图，不属于对称检索，需按非对称检索配置。

##### 场景 2：非对称检索

* **通用规则**：仅在 Query 侧定制指令，Corpus 侧使用默认模板；指令需明确匹配规则。
* **典型场景示例**

| 业务场景 | Query 侧 Instruction 配置 | Corpus 侧 Instruction 配置 |
| --- | --- | --- |
| 跨模态问答（Query：文本问题；Corpus：文本 / 图片） | Target_modality: text/image.\nInstruction:根据这个问题，找到能回答这个问题的相应文本或图片\nQuery: | 文本 Corpus：Instruction:Compress the text into one word.\nQuery: <br> 图片 Corpus：Instruction:Compress the image into one word.\nQuery: |
| 原图检索（忽略 PS 处理） | Target_modality: image.\nInstruction:查找与本图完全相同的图片，可能经过了ps处理，包含缩放、裁剪和水印，请忽略PS处理痕迹\nQuery: | Instruction:Compress the image into one word.\nQuery: |
| 电商服装检索（忽略背景 / 人物） | Target_modality: image.\nInstruction:忽略背景以及人物主体并查找这张图片中出现的同款商品图片\nQuery: | Instruction:Compress the image into one word.\nQuery: |
| 电商商品检索（文本描述搜图） | Target_modality: image.\nInstruction:根据下面的文本中对商品的描述，找到对应的符合条件的商品图片\nQuery: | Instruction:Compress the image into one word.\nQuery: |
| 菜品检索（文本描述搜图） | Target_modality: image.\nInstruction:根据这段文本中提到的有关的菜品，找到相关的菜品的图片\nQuery: | Instruction:Compress the image into one word.\nQuery: |
## 
