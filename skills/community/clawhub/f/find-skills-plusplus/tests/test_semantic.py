import findskills


def test_tokenize_returns_triple():
    w, c, t = findskills.tokenize("Hello 世界 PDF")
    assert "hello" in w
    assert "世" in c
    assert "hello 世界 pdf" in t


def test_semantic_high_overlap():
    s = findskills.semantic_score("处理pdf文档", "PDF 读取/合并/拆分/水印 处理")
    assert s > 0.5


def test_semantic_intent_expand():
    # "股票" 命中 finance 同义词，应与金融描述相关
    s = findskills.semantic_score("股票行情", "实时股票行情、基金、选股、财报分析")
    assert s > 0.5


def test_semantic_low_overlap():
    s = findskills.semantic_score("星际旅行计划", "PDF 文档处理与转换")
    assert s < 0.1
