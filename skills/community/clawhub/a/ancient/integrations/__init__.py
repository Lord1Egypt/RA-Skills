"""
Ancientman-CN LangChain/LlamaIndex 集成模块

用法示例:

LangChain ChatModel:
```python
from ancientman.integrations import AncientmanCompressionHandler
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    callbacks=[AncientmanCompressionHandler(mode="standard")]
)
response = llm.predict("帮我写一个数据库连接池")
```

LangChain Document Transformer:
```python
from ancientman.integrations import AncientmanDocumentTransformer

documents = ["文档1内容...", "文档2内容..."]
transformer = AncientmanDocumentTransformer(mode="ultra")
results = transformer.transform_documents(documents)
```

LlamaIndex Query:
```python
from ancientman.integrations import AncientmanQueryRewriter

rewriter = AncientmanQueryRewriter()
compressed_query = rewriter.rewrite("如何优化PostgreSQL的查询性能")
```
"""

from .langchain_integration import AncientmanCompressionHandler, AncientmanDocumentTransformer
from .llamaindex_integration import AncientmanQueryRewriter

__all__ = [
    "AncientmanCompressionHandler",
    "AncientmanDocumentTransformer", 
    "AncientmanQueryRewriter",
]
